#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Manager for Interactive System

This module handles all data-related operations including loading,
exporting, and data management functionality with aggressive memory optimization.
"""

import json
import time
import gc
import os
import psutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import warnings

import pandas as pd
import numpy as np

from ..eda import data_quality
from ..data import GapFixer, explain_why_fix_gaps


class DataManager:
    """Manages data loading, exporting, and data operations with aggressive memory optimization."""
    
    def __init__(self):
        """Initialize the data manager with aggressive memory optimization."""
        # Memory management settings - optimized for Docker with 8GB limit
        self.max_memory_mb = int(os.environ.get('MAX_MEMORY_MB', '6144'))  # 6GB default (optimized for 8GB container)
        self.chunk_size = int(os.environ.get('CHUNK_SIZE', '50000'))  # 50k rows per chunk
        self.enable_memory_optimization = os.environ.get('ENABLE_MEMORY_OPTIMIZATION', 'true').lower() == 'true'
        
        # Memory settings optimized for large datasets
        self.max_file_size_mb = int(os.environ.get('MAX_FILE_SIZE_MB', '200'))  # 200MB threshold
        self.sample_size = int(os.environ.get('SAMPLE_SIZE', '10000'))  # 10k rows for sampling
        self.enable_streaming = os.environ.get('ENABLE_STREAMING', 'true').lower() == 'true'
        
        # Memory monitoring - more permissive for large datasets
        self.memory_warning_threshold = float(os.environ.get('MEMORY_WARNING_THRESHOLD', '0.8'))  # 80% of max memory
        self.memory_critical_threshold = float(os.environ.get('MEMORY_CRITICAL_THRESHOLD', '0.95'))  # 95% of max memory
        
        # Initialize gap analysis settings
        self.gap_analysis_enabled = True
        
        print(f"🔧 DataManager initialized with memory optimization:")
        print(f"   Max memory: {self.max_memory_mb}MB")
        print(f"   Chunk size: {self.chunk_size:,} rows")
        print(f"   File size threshold: {self.max_file_size_mb}MB")
        print(f"   Sample size: {self.sample_size:,} rows")
    
    def _get_memory_info(self) -> Dict[str, float]:
        """Get current memory usage information."""
        try:
            memory = psutil.virtual_memory()
            return {
                'total_mb': memory.total / (1024 * 1024),
                'available_mb': memory.available / (1024 * 1024),
                'used_mb': memory.used / (1024 * 1024),
                'percent': memory.percent
            }
        except ImportError:
            return {
                'total_mb': 2048,
                'available_mb': 1024,
                'used_mb': 1024,
                'percent': 50.0
            }
    
    def _check_memory_available(self, required_mb: int = None) -> bool:
        """Check if we have enough memory available."""
        if not self.enable_memory_optimization:
            return True
            
        try:
            memory_info = self._get_memory_info()
            available_mb = memory_info['available_mb']
            
            if required_mb is None:
                required_mb = self.max_memory_mb * 0.1  # Require only 10% of max memory (more permissive)
            
            return available_mb > required_mb
        except Exception:
            return True
    
    def _estimate_memory_usage(self, df: pd.DataFrame) -> int:
        """Estimate memory usage of DataFrame in MB."""
        try:
            memory_usage = df.memory_usage(deep=True).sum()
            memory_mb = int(memory_usage / (1024 * 1024))
            return max(1, memory_mb)
        except Exception:
            # Conservative fallback estimation
            estimated_bytes = df.shape[0] * df.shape[1] * 32  # 32 bytes per cell
            memory_mb = estimated_bytes // (1024 * 1024)
            return max(1, memory_mb)
    
    def _get_file_size_mb(self, file_path: Path) -> float:
        """Get file size in MB."""
        try:
            return file_path.stat().st_size / (1024 * 1024)
        except Exception:
            return 0.0
    
    def _handle_datetime_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle datetime index and convert it to a column if needed."""
        # Check if the DataFrame has a datetime index
        if isinstance(df.index, pd.DatetimeIndex):
            print(f"✅ Found datetime index: {df.index.name or 'unnamed'}")
            # Reset index to make datetime a column
            df = df.reset_index()
            # Rename the index column if it's unnamed
            if df.columns[0] == 'index':
                df = df.rename(columns={'index': 'datetime'})
            return df
        
        # Check if any column is datetime
        datetime_columns = []
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                datetime_columns.append(col)
        
        if datetime_columns:
            print(f"✅ Found datetime columns: {datetime_columns}")
        
        return df
    
    def _should_use_chunked_loading(self, file_path: Path) -> bool:
        """Determine if file should be loaded in chunks."""
        if not self.enable_memory_optimization:
            return False
            
        file_size_mb = self._get_file_size_mb(file_path)
        return file_size_mb > self.max_file_size_mb
    
    def _load_csv_with_datetime_handling(self, file_path: Path, chunk_size: int = None) -> pd.DataFrame:
        """Load CSV file with proper datetime handling and memory optimization."""
        if chunk_size is None:
            chunk_size = self.chunk_size
            
        print(f"🔄 Loading CSV: {file_path.name}")
        
        # Determine header row first
        header_row = self._determine_header_row(file_path)
        
        # Try to detect datetime columns with correct header
        datetime_columns = self._detect_datetime_columns(file_path, header_row)
        
        # Load data in chunks if needed
        if self._should_use_chunked_loading(file_path):
            return self._load_csv_in_chunks(file_path, datetime_columns, chunk_size)
        else:
            return self._load_csv_direct(file_path, datetime_columns)
    
    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean column names by removing tabs, extra spaces, and trailing commas."""
        original_columns = df.columns.tolist()
        cleaned_columns = []
        
        for col in original_columns:
            # Remove tabs, extra spaces, and trailing commas
            cleaned_col = str(col).replace('\t', '').strip().rstrip(',')
            cleaned_columns.append(cleaned_col)
        
        # Check if any columns were actually cleaned
        if cleaned_columns != original_columns:
            print(f"✅ Cleaned column names (removed tabs and trailing commas)")
            print(f"   Before: {original_columns}")
            print(f"   After:  {cleaned_columns}")
            df.columns = cleaned_columns
        
        return df
    
    def _determine_header_row(self, file_path: Path) -> int:
        """Determine the correct header row for CSV file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                second_line = f.readline().strip()
            
            # Check if second line contains 'DateTime' (indicating it's the header)
            if 'DateTime' in second_line:
                # First line is metadata, second line is header
                print(f"✅ Detected metadata header, using row 1 as column headers")
                return 1
            elif 'DateTime' in first_line:
                # First line is header
                print(f"✅ Using first row as column headers")
                return 0
            else:
                # Try to detect by checking if first line looks like data
                # Check for common data patterns (digits, dots, colons)
                if any(char.isdigit() for char in first_line[:20]):  # Check first 20 chars
                    print(f"⚠️  No header detected, using first row as data")
                    return None  # No header
                else:
                    print(f"✅ Using first row as column headers")
                    return 0
        except Exception as e:
            print(f"⚠️  Warning: Could not determine header row: {e}")
            return 0  # Default to first row as header
    
    def _detect_datetime_columns(self, file_path: Path, header_row: int) -> List[str]:
        """Detect datetime columns in CSV file with correct header."""
        datetime_columns = []
        try:
            # Read first few rows to detect datetime columns with correct header
            sample_df = pd.read_csv(file_path, nrows=1000, header=header_row)
            
            # Clean column names to match what will be used in actual loading
            sample_df = self._clean_column_names(sample_df)
            
            # Check for existing datetime columns first
            for col in sample_df.columns:
                if pd.api.types.is_datetime64_any_dtype(sample_df[col]):
                    datetime_columns.append(col)
                    print(f"✅ Found existing datetime column: {col}")
            
            # If no existing datetime columns, try to detect by name
            if not datetime_columns:
                for col in sample_df.columns:
                    col_lower = col.lower()
                    if any(keyword in col_lower for keyword in ['date', 'time', 'datetime', 'timestamp']):
                        datetime_columns.append(col)
                        print(f"✅ Detected potential datetime column by name: {col}")
                    elif sample_df[col].dtype == 'object':
                        # Try to parse as datetime
                        try:
                            pd.to_datetime(sample_df[col].iloc[0], errors='raise')
                            datetime_columns.append(col)
                            print(f"✅ Detected datetime column by parsing: {col}")
                        except:
                            pass
        except Exception as e:
            print(f"⚠️  Warning: Could not detect datetime columns: {e}")
        
        return datetime_columns
    
    def _load_csv_direct(self, file_path: Path, datetime_columns: List[str]) -> pd.DataFrame:
        """Load CSV file directly with datetime parsing."""
        try:
            # Determine header row
            header_row = self._determine_header_row(file_path)
            
            # Load with appropriate header setting
            df = pd.read_csv(file_path, header=header_row)
            
            # Clean column names (remove tabs, trailing commas, etc.)
            df = self._clean_column_names(df)
            
            # Remove unnamed/empty columns
            unnamed_cols_to_drop = [col for col in df.columns if str(col).startswith('Unnamed:') or str(col) == '']
            if unnamed_cols_to_drop:
                print(f"✅ Dropping unnamed/empty columns: {unnamed_cols_to_drop}")
                df = df.drop(columns=unnamed_cols_to_drop)
            
            # Parse datetime columns
            for col in datetime_columns:
                if col in df.columns:
                    try:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                        print(f"✅ Parsed datetime column: {col}")
                    except Exception as e:
                        print(f"⚠️  Could not parse datetime column {col}: {e}")
            
            return self._handle_datetime_index(df)
        except Exception as e:
            print(f"❌ Error loading CSV directly: {e}")
            raise
    
    def _load_csv_in_chunks(self, file_path: Path, datetime_columns: List[str], chunk_size: int) -> pd.DataFrame:
        """Load CSV file in chunks with datetime parsing."""
        print(f"📊 Loading {file_path.name} in chunks of {chunk_size:,} rows...")
        
        # Determine header row
        header_row = self._determine_header_row(file_path)
        
        chunks = []
        total_rows = 0
        
        try:
            chunk_iter = pd.read_csv(file_path, chunksize=chunk_size, header=header_row)
            
            for i, chunk in enumerate(chunk_iter):
                # Clean column names for first chunk only (to avoid duplicate messages)
                if i == 0:
                    chunk = self._clean_column_names(chunk)
                
                # Remove unnamed/empty columns from chunk
                unnamed_cols_to_drop = [col for col in chunk.columns if str(col).startswith('Unnamed:') or str(col) == '']
                if unnamed_cols_to_drop:
                    chunk = chunk.drop(columns=unnamed_cols_to_drop)
                
                # Parse datetime columns in chunk
                for col in datetime_columns:
                    if col in chunk.columns:
                        try:
                            chunk[col] = pd.to_datetime(chunk[col], errors='coerce')
                        except Exception:
                            pass  # Skip if parsing fails
                
                chunks.append(chunk)
                total_rows += len(chunk)
                
                # Memory management
                if self.enable_memory_optimization:
                    gc.collect()
                
                # Progress indicator
                if (i + 1) % 5 == 0:
                    print(f"   📈 Loaded {i + 1} chunks ({total_rows:,} rows)")
                
                # Check memory
                if not self._check_memory_available():
                    print(f"⚠️  Low memory detected, stopping at chunk {i + 1}")
                    break
            
            # Combine chunks
            if chunks:
                result = pd.concat(chunks, ignore_index=True)
                del chunks
                gc.collect()
                return self._handle_datetime_index(result)
            else:
                raise ValueError("No chunks were loaded")
                
        except Exception as e:
            print(f"❌ Error in chunked CSV loading: {e}")
            raise
    
    def _load_parquet_with_optimization(self, file_path: Path) -> pd.DataFrame:
        """Load parquet file with memory optimization and datetime index handling."""
        print(f"🔄 Loading Parquet: {file_path.name}")
        
        try:
            import pyarrow.parquet as pq
            
            # Get file info
            parquet_file = pq.ParquetFile(file_path)
            total_rows = parquet_file.metadata.num_rows
            
            # First, check if the file has a datetime index by reading a small sample
            # Use pyarrow to read just the first row group to check the index
            first_row_group = parquet_file.read_row_group(0)
            sample_df = first_row_group.to_pandas()
            has_datetime_index = isinstance(sample_df.index, pd.DatetimeIndex)
            datetime_index_name = sample_df.index.name if has_datetime_index else None
            
            if total_rows <= self.chunk_size:
                # Small file, load directly with datetime index handling
                df = pd.read_parquet(file_path)
                return self._handle_datetime_index(df)
            
            # Large file, load in chunks
            print(f"📊 Loading {file_path.name} in chunks of {self.chunk_size:,} rows...")
            
            if has_datetime_index:
                print(f"📅 Detected DatetimeIndex: {datetime_index_name}, preserving during chunked loading...")
                
                # For files with DatetimeIndex, we need to load the entire file to preserve the index
                # This is because pyarrow chunks don't preserve the index structure
                # However, we'll try to load in chunks if the file is extremely large
                if total_rows > 5000000:  # 5M rows threshold
                    print(f"⚠️  Very large file with DatetimeIndex detected ({total_rows:,} rows).")
                    print(f"   Loading entire file to preserve index structure (this may use significant memory)...")
                    df = pd.read_parquet(file_path)
                    return self._handle_datetime_index(df)
                else:
                    print(f"   Loading entire file to preserve index structure...")
                    df = pd.read_parquet(file_path)
                    return self._handle_datetime_index(df)
            else:
                # No DatetimeIndex, safe to load in chunks
                chunks = []
                for i, chunk in enumerate(parquet_file.iter_batches(batch_size=self.chunk_size)):
                    chunk_df = chunk.to_pandas()
                    chunks.append(chunk_df)
                    
                    # Memory management
                    if self.enable_memory_optimization:
                        gc.collect()
                    
                    # Progress indicator
                    if (i + 1) % 10 == 0:
                        rows_loaded = (i + 1) * self.chunk_size
                        progress = min(100, (rows_loaded / total_rows) * 100)
                        print(f"   📈 Progress: {progress:.1f}% ({rows_loaded:,}/{total_rows:,} rows)")
                    
                    # Check memory
                    if not self._check_memory_available():
                        print(f"⚠️  Low memory detected, stopping at chunk {i + 1}")
                        break
                
                # Combine chunks
                if chunks:
                    result = pd.concat(chunks, ignore_index=True)
                    del chunks
                    gc.collect()
                    return self._handle_datetime_index(result)
                else:
                    raise ValueError("No chunks were loaded")
                
        except ImportError:
            # Fallback to pandas
            df = pd.read_parquet(file_path)
            return self._handle_datetime_index(df)
        except Exception as e:
            print(f"❌ Error loading parquet: {e}")
            raise
    
    def load_data_from_file(self, file_path: str) -> pd.DataFrame:
        """Load data from file path with aggressive memory optimization."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check memory before loading
        if not self._check_memory_available():
            raise MemoryError("Insufficient memory to load file")
        
        # Load based on file type
        if file_path.suffix.lower() == '.csv':
            return self._load_csv_with_datetime_handling(file_path)
        elif file_path.suffix.lower() == '.parquet':
            return self._load_parquet_with_optimization(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    def load_data_from_folder(self, folder_path: str) -> List[str]:
        """Load data files from folder path."""
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
            
        if not folder_path.is_dir():
            raise ValueError(f"Path is not a directory: {folder_path}")
        
        # Find all data files in the folder
        data_files = []
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                if file_path.suffix.lower() in ['.csv', '.parquet']:
                    data_files.append(str(file_path))
        
        return data_files
    
    def load_data(self, system) -> bool:
        """Load data interactively with aggressive memory optimization."""
        print("\n📁 LOAD DATA")
        print("-" * 30)
        
        # Ask user to choose loading strategy
        print("🎯 DATA LOADING STRATEGY")
        print("-" * 30)
        print("1. 📊 Standard Loading - Combine all files into single dataset")
        print("2. 🚀 Multi-Timeframe Loading - Proper ML strategy for multiple timeframes")
        print("0. 🔙 Back to Main Menu")
        print("")
        print("💡 For robust ML trading models, Multi-Timeframe Loading is recommended")
        print("   as it properly handles M1, M5, H1, D1, MN1 data as separate timeframes")
        print("   instead of mixing them together.")
        print("-" * 30)
        
        try:
            strategy_choice = input("Select loading strategy (1/2/0): ").strip()
        except EOFError:
            print("\n👋 Goodbye!")
            return False
        
        if strategy_choice == "0":
            return False
        elif strategy_choice == "2":
            return self.load_multi_timeframe_data(system)
        elif strategy_choice != "1":
            print("❌ Invalid choice. Using standard loading...")
        
        print("\n📁 STANDARD DATA LOADING")
        print("-" * 30)
        
        # Get all subfolders in data directory and other important folders
        data_folder = Path("data")
        
        if not data_folder.exists():
            print("❌ Data folder not found. Please ensure 'data' folder exists.")
            return False
        
        # Create necessary cache directories if they don't exist
        cache_dirs = [
            data_folder / "cache",
            data_folder / "cache" / "csv_converted",
            data_folder / "cache" / "uv_cache",
            data_folder / "backups"
        ]
        
        for cache_dir in cache_dirs:
            if not cache_dir.exists():
                cache_dir.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created cache directory: {cache_dir}")
        
        # Find all subfolders (exclude cache folders and mql5_feed)
        subfolders = [data_folder]  # Include main data folder
        
        for item in data_folder.iterdir():
            if item.is_dir():
                # Skip cache folders and mql5_feed to avoid loading cached files
                if 'cache' not in item.name.lower() and item.name != 'mql5_feed':
                    subfolders.append(item)
                    # Also include sub-subfolders (but skip cache and mql5_feed)
                    for subitem in item.iterdir():
                        if subitem.is_dir() and 'cache' not in subitem.name.lower():
                            subfolders.append(subitem)
        
        # Add csv_converted folder specifically if it exists
        csv_converted_folder = data_folder / "cache" / "csv_converted"
        if csv_converted_folder.exists() and csv_converted_folder.is_dir():
            subfolders.append(csv_converted_folder)
        
        print("💡 Available folders:")
        print("0. 🔙 Back to Main Menu")
        for i, folder in enumerate(subfolders, 1):
            try:
                rel_path = folder.relative_to(Path.cwd())
            except ValueError:
                rel_path = folder
            print(f"{i}. 📁 {rel_path}/")
        
        print("\n💡 Note: mql5_feed directory is excluded from this list")
        print("   (it's only used with run_analysis.py for CSV to Parquet conversion)")
        print("   data/cache/csv_converted is included for loading converted CSV files")
        
        print("-" * 30)
        print("💡 Examples:")
        print("   • Enter folder number (e.g., 1 for data/)")
        print("   • Or enter folder path with mask (e.g., data gbpusd)")
        print("   • Or enter folder path with file type (e.g., data parquet)")
        print("")
        print("📋 More Examples:")
        print("   • 2 eurusd     (folder 2 with 'eurusd' in filename)")
        print("   • 2 gbpusd     (folder 2 with 'gbpusd' in filename)")
        print("   • data sample  (data folder with 'sample' in filename)")
        print("   • 1 csv        (folder 1 with '.csv' files)")
        print("   • 7 parquet    (folder 7 with '.parquet' files)")
        print("   • data test    (data folder with 'test' in filename)")
        print("")
        print("🗑️  Cache Management:")
        print("   • Enter 'clear cache' to clear all cached files")
        print("-" * 30)
        
        try:
            input_text = input("Enter folder number or path (with optional mask): ").strip()
        except EOFError:
            print("\n👋 Goodbye!")
            return False
        
        if not input_text:
            print("❌ No input provided")
            return False
        
        # Check if user wants to go back
        if input_text == "0":
            return False
        
        # Check if user wants to clear cache
        if input_text.lower() == "clear cache":
            return self.clear_cache(system)
        
        # Parse input for folder and mask
        parts = input_text.split()
        
        # Check if first part is a number (folder selection)
        if parts[0].isdigit():
            folder_idx = int(parts[0]) - 1
            if 0 <= folder_idx < len(subfolders):
                folder_path = subfolders[folder_idx]
                mask = parts[1].lower() if len(parts) > 1 else None
            else:
                print(f"❌ Invalid folder number. Please select 0-{len(subfolders)}")
                return False
        else:
            # Parse input for folder path and mask
            folder_path = parts[0]
            mask = parts[1].lower() if len(parts) > 1 else None
                
            folder_path = Path(folder_path)
            if not folder_path.exists() or not folder_path.is_dir():
                print(f"❌ Folder not found: {folder_path}")
                return False
        
        # Find all data files (exclude temporary files)
        data_files = []
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            if mask:
                # Apply mask filter
                pattern = f"*{mask}*{ext}"
                files = list(folder_path.glob(pattern))
                # Filter out temporary files
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
                
                # Also try case-insensitive search
                pattern = f"*{mask.upper()}*{ext}"
                files = list(folder_path.glob(pattern))
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
                
                pattern = f"*{mask.lower()}*{ext}"
                files = list(folder_path.glob(pattern))
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
            else:
                # No mask, get all files (but exclude temporary files)
                files = list(folder_path.glob(f"*{ext}"))
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
        
        # Remove duplicates
        data_files = list(set(data_files))
        
        if not data_files:
            if mask:
                print(f"❌ No files found matching mask '{mask}' in {folder_path}")
            else:
                print(f"❌ No data files found in {folder_path}")
            return False
        
        print(f"📁 Found {len(data_files)} data files:")
        for i, file in enumerate(data_files, 1):
            file_size_mb = self._get_file_size_mb(file)
            print(f"   {i}. {file.name} ({file_size_mb:.1f}MB)")
        
        # Load files with aggressive memory management
        all_data = []
        total_rows = 0
        total_memory_mb = 0
        
        for i, file in enumerate(data_files):
            try:
                print(f"\n🔄 Loading file {i+1}/{len(data_files)}: {file.name}")
                
                # Check memory before loading
                if not self._check_memory_available():
                    print(f"⚠️  Low memory detected, skipping {file.name}")
                    continue
                
                # Load file
                df = self.load_data_from_file(str(file))
                df['source_file'] = file.name  # Add source file info
                
                # Memory usage estimation
                memory_mb = self._estimate_memory_usage(df)
                total_memory_mb += memory_mb
                total_rows += df.shape[0]
                
                all_data.append(df)
                print(f"✅ Loaded: {file.name} ({df.shape[0]:,} rows, ~{memory_mb}MB)")
                
                # Memory management after each file
                if self.enable_memory_optimization:
                    gc.collect()
                
                # Check if we're approaching memory limits - more permissive
                if total_memory_mb > self.max_memory_mb * 0.95:
                    print(f"⚠️  Memory usage critical ({total_memory_mb}MB), stopping file loading")
                    break
                elif total_memory_mb > self.max_memory_mb * 0.8:
                    print(f"⚠️  Memory usage high ({total_memory_mb}MB), but continuing...")
                    # Continue loading but with more aggressive memory management
                    gc.collect()
                    
            except Exception as e:
                print(f"❌ Error loading {file.name}: {e}")
                continue
        
        if not all_data:
            print("❌ No files could be loaded")
            return False
        
        print(f"\n📊 Memory Summary:")
        print(f"   Total files loaded: {len(all_data)}")
        print(f"   Total rows: {total_rows:,}")
        print(f"   Estimated memory usage: {total_memory_mb}MB")
        
        # Ask user if they want to fix time series gaps
        print("\n🔧 Time Series Gap Fixing")
        print("-" * 30)
        print("💡 This will detect and fix gaps in time series data before combining files.")
        print("   Gaps can occur due to missing data points, market holidays, or data collection issues.")
        print("   Fixing gaps ensures consistent time intervals for better analysis.")
        print("-" * 30)
        
        try:
            fix_gaps = input("Fix time series gaps before combining data? (y/n, default: y): ").strip().lower()
        except EOFError:
            print("\n👋 Goodbye!")
            return False
        
        if fix_gaps in ['', 'y', 'yes']:
            print("\n🔧 Fixing time series gaps...")
            all_data = self._fix_time_series_gaps(all_data)
        else:
            print("\n⏭️  Skipping time series gap fixing...")
        
        # Combine all data with memory optimization
        print("\n🔄 Combining data...")
        
        try:
            # Check if any DataFrames have DatetimeIndex
            has_datetime_index = any(isinstance(df.index, pd.DatetimeIndex) for df in all_data)
            
            if has_datetime_index:
                print("📅 Detected DatetimeIndex in loaded DataFrames, preserving during concatenation...")
                
                # Convert DatetimeIndex to 'Timestamp' column for consistent concatenation
                processed_data = []
                for df in all_data:
                    df_copy = df.copy()
                    if isinstance(df_copy.index, pd.DatetimeIndex):
                        # Reset index to make datetime a column
                        df_copy = df_copy.reset_index()
                        # Rename the index column if it's unnamed
                        if df_copy.columns[0] == 'index':
                            df_copy = df_copy.rename(columns={'index': 'Timestamp'})
                    processed_data.append(df_copy)
                
                # Combine DataFrames with consistent column structure
                system.current_data = pd.concat(processed_data, ignore_index=True)
                
                # Clean up intermediate data
                del processed_data
                gc.collect()
                
                print("✅ Successfully preserved datetime information during concatenation")
            else:
                # Check for mixed structures (some files have Timestamp column, others don't)
                has_timestamp_column = any('Timestamp' in df.columns for df in all_data)
                missing_timestamp_column = any('Timestamp' not in df.columns for df in all_data)
                
                if has_timestamp_column and missing_timestamp_column:
                    print("⚠️  Detected mixed file structures (some with Timestamp column, some without)")
                    print("📅 Normalizing file structures for consistent concatenation...")
                    
                    # Process all DataFrames to ensure consistent structure
                    processed_data = []
                    for i, df in enumerate(all_data):
                        df_copy = df.copy()
                        
                        if 'Timestamp' not in df_copy.columns:
                            # Create a dummy Timestamp column for files without it
                            # This will be filled with NaT (missing values)
                            df_copy['Timestamp'] = pd.NaT
                            print(f"   Added Timestamp column to file {i+1} (will be filled with missing values)")
                        
                        processed_data.append(df_copy)
                    
                    # Combine DataFrames with consistent column structure
                    system.current_data = pd.concat(processed_data, ignore_index=True)
                    
                    # Clean up intermediate data
                    del processed_data
                    gc.collect()
                    
                    print("✅ Successfully normalized file structures for concatenation")
                else:
                    # All files have consistent structure, use standard concatenation
                    system.current_data = pd.concat(all_data, ignore_index=True)
            
            # Clean up intermediate data
            del all_data
            gc.collect()
            
            # Check and preserve datetime columns after concatenation
            datetime_columns = []
            for col in system.current_data.columns:
                if pd.api.types.is_datetime64_any_dtype(system.current_data[col]):
                    datetime_columns.append(col)
            
            if datetime_columns:
                print(f"✅ Preserved {len(datetime_columns)} datetime column(s) after concatenation: {datetime_columns}")
            else:
                print(f"⚠️  No datetime columns found after concatenation")
            
            print(f"\n✅ Combined data loaded successfully!")
            print(f"   Total shape: {system.current_data.shape[0]:,} rows × {system.current_data.shape[1]} columns")
            print(f"   Files loaded: {len(data_files)}")
            if mask:
                print(f"   Mask used: '{mask}'")
            print(f"   Final memory usage: ~{self._estimate_memory_usage(system.current_data)}MB")
            print(f"   Columns: {list(system.current_data.columns)}")
            
            # Show data preview
            show_preview = input("\nShow data preview? (y/n): ").strip().lower()
            if show_preview in ['y', 'yes']:
                print("\n📋 DATA PREVIEW:")
                print(system.current_data.head())
                print(f"\nData types:\n{system.current_data.dtypes}")
            
            # Ask if user wants to analyze time series gaps
            try:
                analyze_gaps = input("\n🔍 Analyze time series gaps? (y/n): ").strip().lower()
                if analyze_gaps in ['y', 'yes']:
                    # Determine expected frequency based on data
                    expected_frequency = self._determine_expected_frequency(system.current_data, datetime_column='Timestamp')
                    
                    # Analyze gaps
                    self.analyze_time_series_gaps(data_files, 'Timestamp', expected_frequency)
            except EOFError:
                pass
            
            return True
            
        except Exception as e:
            print(f"❌ Error combining data: {e}")
            return False
    
    def analyze_time_series_gaps(self, data_files: List[Path], 
                                datetime_column: str = 'Timestamp',
                                expected_frequency: str = '1H') -> bool:
        """
        Analyze time series gaps in loaded files using existing EDA functionality.
        
        Args:
            data_files: List of file paths that were loaded
            datetime_column: Name of the datetime column to analyze
            expected_frequency: Expected frequency of the data
            
        Returns:
            True if analysis completed successfully
        """
        print(f"\n🔍 ANALYZING TIME SERIES GAPS")
        print("-" * 40)
        print(f"📊 Analyzing {len(data_files)} files for gaps...")
        print(f"📅 Using datetime column: '{datetime_column}'")
        print(f"⏱️  Expected frequency: {expected_frequency}")
        
        try:
            # Import colorama for colored output
            import colorama
            from colorama import Fore, Style
            colorama.init(autoreset=True)
            
            # Initialize gap summary list
            gap_summary = []
            
            # Analyze each file using existing data_quality.gap_check
            for i, file_path in enumerate(data_files, 1):
                print(f"\n📁 Analyzing file {i}/{len(data_files)}: {file_path.name}")
                
                try:
                    # Load file
                    if file_path.suffix.lower() == '.csv':
                        df = pd.read_csv(file_path)
                    elif file_path.suffix.lower() == '.parquet':
                        df = pd.read_parquet(file_path)
                    else:
                        print(f"  ⚠️  Skipping unsupported file format: {file_path.suffix}")
                        continue
                    
                    # Add file info to gap summary entries
                    def gap_check_wrapper(df, gap_summary, Fore, Style):
                        # Call the original gap_check function
                        data_quality.gap_check(df, gap_summary, Fore, Style)
                        # Add file information to all entries
                        for entry in gap_summary:
                            if 'file' not in entry:
                                entry['file'] = file_path.name
                    
                    # Check if DataFrame has datetime index and convert to column if needed
                    if isinstance(df.index, pd.DatetimeIndex):
                        print(f"  📅 Converting DatetimeIndex to column for gap analysis...")
                        df = df.reset_index()
                        if df.columns[0] == 'index':
                            df = df.rename(columns={'index': 'Timestamp'})
                    
                    # Run gap check
                    gap_check_wrapper(df, gap_summary, Fore, Style)
                    
                except Exception as e:
                    print(f"  ❌ Error analyzing {file_path.name}: {e}")
                    continue
            
            # Print gap summary using existing function
            if gap_summary:
                data_quality.print_gap_summary(gap_summary, Fore, Style)
                
                # Ask user if they want to see detailed gap information
                try:
                    show_details = input(f"\nShow detailed gap information? (y/n): ").strip().lower()
                    if show_details in ['y', 'yes']:
                        self._show_detailed_gap_info_from_eda(gap_summary, Fore, Style)
                except EOFError:
                    pass
            else:
                print(f"\n✅ No gaps found in any files!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error analyzing time series gaps: {e}")
            return False
    
    def _show_detailed_gap_info_from_eda(self, gap_summary: List[Dict], Fore, Style):
        """Show detailed gap information for files with gaps using EDA results."""
        print(f"\n📋 DETAILED GAP INFORMATION")
        print("=" * 50)
        
        if not gap_summary:
            print("No gaps found in any files.")
            return
        
        # Group gaps by file
        from collections import defaultdict
        gaps_by_file = defaultdict(list)
        for entry in gap_summary:
            gaps_by_file[entry.get('file', 'Unknown file')].append(entry)
        
        for file_name, gaps in gaps_by_file.items():
            print(f"\n📁 {file_name}")
            print(f"   📊 Summary:")
            print(f"      • Total gaps: {len(gaps)}")
            
            # Show gap details
            for i, gap in enumerate(gaps, 1):
                print(f"   ⏰ Gap {i}:")
                if 'column' in gap:
                    print(f"      • Column: {gap['column']}")
                if 'gaps_count' in gap:
                    print(f"      • Gaps count: {gap['gaps_count']}")
                if 'largest_gap' in gap:
                    print(f"      • Largest gap: {gap['largest_gap']}")
                if 'method' in gap:
                    print(f"      • Analysis method: {gap['method']}")
                # Check for different gap information formats
                if 'from' in gap and 'to' in gap and 'delta' in gap:
                    print(f"      • Period: {gap['from']} → {gap['to']} (delta: {gap['delta']})")
                elif 'largest_gap' in gap:
                    print(f"      • Largest gap: {gap['largest_gap']}")
            
            print("-" * 40)
        
        # Ask user if they want to fix gaps
        try:
            fix_gaps = input(f"\nDo you want to fix these gaps? (y/n): ").strip().lower()
            if fix_gaps in ['y', 'yes']:
                self._fix_gaps_interactive(gap_summary, Fore, Style)
        except EOFError:
            pass
    
    def _determine_expected_frequency(self, df: pd.DataFrame, datetime_column: str = 'Timestamp') -> str:
        """
        Determine the expected frequency of time series data.
        
        Args:
            df: DataFrame with time series data
            datetime_column: Name of the datetime column
            
        Returns:
            Expected frequency string (e.g., '1H', '1D', '1T')
        """
        if datetime_column not in df.columns:
            return '1H'  # Default to hourly
        
        # Get datetime column
        dt_col = df[datetime_column]
        
        # Remove NaT values
        dt_col_clean = dt_col.dropna()
        
        if len(dt_col_clean) < 2:
            return '1H'  # Default to hourly
        
        # Sort and get time differences
        dt_col_sorted = dt_col_clean.sort_values()
        time_diffs = dt_col_sorted.diff().dropna()
        
        if len(time_diffs) == 0:
            return '1H'  # Default to hourly
        
        # Calculate median time difference
        median_diff = time_diffs.median()
        median_hours = median_diff.total_seconds() / 3600
        
        # Determine frequency based on median difference
        if median_hours < 0.1:  # Less than 6 minutes
            return '1T'  # 1 minute
        elif median_hours < 1:  # Less than 1 hour
            return '15T'  # 15 minutes
        elif median_hours < 24:  # Less than 1 day
            return '1H'  # 1 hour
        elif median_hours < 168:  # Less than 1 week
            return '1D'  # 1 day
        else:
            return '1W'  # 1 week
    
    def export_results(self, system):
        """Export current results to files."""
        if not system.current_results:
            print("❌ No results to export. Please run some analysis first.")
            return
            
        print("\n📤 EXPORT RESULTS")
        print("-" * 30)
        
        # Implementation for exporting results
        print("📤 Export functionality coming soon...")
    
    def clear_cache(self, system):
        """Clear all cached files."""
        print("\n🗑️  CLEAR CACHE")
        print("=" * 50)
        
        # Define cache directories
        cache_dirs = [
            Path('data/cache'),
            Path('data/cache/csv_converted'),
            Path('data/cache/uv_cache'),
            Path('logs'),
            Path('reports')
        ]
        
        total_files = 0
        total_size_mb = 0
        cleared_files = []
        
        for cache_dir in cache_dirs:
            if not cache_dir.exists():
                continue
                
            print(f"🔍 Scanning {cache_dir}...")
            
            # Find all files in cache directory
            for file_path in cache_dir.rglob('*'):
                if file_path.is_file():
                    file_size_mb = file_path.stat().st_size / (1024 * 1024)
                    total_files += 1
                    total_size_mb += file_size_mb
                    cleared_files.append((file_path, file_size_mb))
        
        if total_files == 0:
            print("✅ No cached files found to clear.")
            return True
        
        print(f"📁 Found {total_files} cached files ({total_size_mb:.1f} MB total)")
        print("\n🗂️  Files to be cleared:")
        
        # Show first 10 files
        for i, (file_path, file_size_mb) in enumerate(cleared_files[:10], 1):
            rel_path = file_path.relative_to(Path.cwd())
            print(f"   {i}. {rel_path} ({file_size_mb:.1f} MB)")
        
        if len(cleared_files) > 10:
            print(f"   ... and {len(cleared_files) - 10} more files")
        
        # Ask for confirmation
        try:
            confirm = input(f"\n⚠️  Are you sure you want to clear {total_files} files ({total_size_mb:.1f} MB)? (y/N): ").strip().lower()
        except EOFError:
            print("\n👋 Goodbye!")
            return False
        
        if confirm not in ['y', 'yes']:
            print("❌ Cache clearing cancelled.")
            return False
        
        # Clear cache files
        print("\n🗑️  Clearing cache...")
        cleared_count = 0
        cleared_size_mb = 0
        
        for file_path, file_size_mb in cleared_files:
            try:
                file_path.unlink()
                cleared_count += 1
                cleared_size_mb += file_size_mb
                if cleared_count % 100 == 0:
                    print(f"   ✅ Cleared {cleared_count}/{total_files} files...")
            except Exception as e:
                print(f"   ⚠️  Could not delete {file_path}: {e}")
        
        print(f"\n✅ Cache cleared successfully!")
        print(f"   • Files cleared: {cleared_count}/{total_files}")
        print(f"   • Space freed: {cleared_size_mb:.1f} MB")
        
        return True
    
    def restore_from_backup(self, system):
        """Restore data from backup file."""
        print("\n📥 RESTORE FROM BACKUP")
        print("=" * 50)
        
        # Check if data is loaded
        if system.current_data is None or system.current_data.empty:
            print("❌ No data loaded. Please load some data first.")
            return False
        
        # Define backup directory
        backup_dir = Path('data/backups')
        
        if not backup_dir.exists():
            print(f"❌ Backup directory not found: {backup_dir}")
            return False
        
        # Look for all types of backup files
        backup_files = list(backup_dir.glob("backup_*.parquet"))
        data_backup_files = list(backup_dir.glob("data_backup_*.parquet"))
        data_fixed_files = list(backup_dir.glob("data_fixed_*.parquet"))
        
        # Combine all backup files
        all_backup_files = backup_files + data_backup_files + data_fixed_files
        
        if not all_backup_files:
            print(f"❌ No backup files found in {backup_dir}/")
            return False
        
        # Sort files by modification time (newest first)
        all_backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        print(f"✅ Found {len(all_backup_files)} backup files:")
        import time
        for i, backup_file in enumerate(all_backup_files, 1):
            file_size = backup_file.stat().st_size / (1024 * 1024)  # MB
            file_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(backup_file.stat().st_mtime))
            print(f"   {i}. {backup_file.name} ({file_size:.1f} MB, {file_time})")
        
        # Get user choice
        try:
            choice = input(f"\nSelect backup file to restore (1-{len(all_backup_files)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                print("❌ Restore cancelled.")
                return False
            
            choice_idx = int(choice) - 1
            if choice_idx < 0 or choice_idx >= len(all_backup_files):
                print("❌ Invalid choice.")
                return False
            
            selected_backup = all_backup_files[choice_idx]
            
            # Confirm restoration
            confirm = input(f"\nAre you sure you want to restore from {selected_backup.name}? (y/n): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("❌ Restore cancelled.")
                return False
            
            # Load backup data
            print(f"\n🔄 Restoring from {selected_backup.name}...")
            backup_data = pd.read_parquet(selected_backup)
            
            # Replace current data
            system.current_data = backup_data
            
            print(f"✅ Data restored successfully!")
            print(f"   Shape: {backup_data.shape[0]:,} rows × {backup_data.shape[1]} columns")
            print(f"   Columns: {list(backup_data.columns)}")
            
            # Mark menu as used
            system.menu_manager.mark_menu_as_used('eda', 'restore_from_backup')
            
            return True
            
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            return False
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return False
    
    def clear_data_backup(self, system):
        """Clear all backup files from the backup directory."""
        print("\n🗑️ CLEAR DATA BACKUP")
        print("=" * 50)
        
        # Define backup directory
        backup_dir = Path('data/backups')
        
        if not backup_dir.exists():
            print(f"❌ Backup directory not found: {backup_dir}")
            return False
        
        # Look for all types of backup files
        backup_files = list(backup_dir.glob("backup_*.parquet"))
        data_backup_files = list(backup_dir.glob("data_backup_*.parquet"))
        data_fixed_files = list(backup_dir.glob("data_fixed_*.parquet"))
        
        # Combine all backup files
        all_backup_files = backup_files + data_backup_files + data_fixed_files
        
        if not all_backup_files:
            print(f"✅ No backup files found in {backup_dir}/")
            return True
        
        # Calculate total size
        total_size_mb = sum(f.stat().st_size for f in all_backup_files) / (1024 * 1024)
        
        print(f"⚠️  Found {len(all_backup_files)} backup files ({total_size_mb:.1f} MB total):")
        import time
        for i, backup_file in enumerate(all_backup_files, 1):
            file_size = backup_file.stat().st_size / (1024 * 1024)  # MB
            file_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(backup_file.stat().st_mtime))
            print(f"   {i}. {backup_file.name} ({file_size:.1f} MB, {file_time})")
        
        # Confirm deletion
        confirm = input(f"\nAre you sure you want to delete ALL {len(all_backup_files)} backup files? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Backup clearing cancelled.")
            return False
        
        # Delete files
        deleted_count = 0
        deleted_size_mb = 0
        
        for backup_file in all_backup_files:
            try:
                file_size = backup_file.stat().st_size / (1024 * 1024)
                backup_file.unlink()
                deleted_count += 1
                deleted_size_mb += file_size
                print(f"✅ Deleted: {backup_file.name}")
            except Exception as e:
                print(f"❌ Error deleting {backup_file.name}: {e}")
        
        print(f"\n✅ Backup clearing completed!")
        print(f"   Files deleted: {deleted_count}/{len(all_backup_files)}")
        print(f"   Space freed: {deleted_size_mb:.1f} MB")
        
        # Mark menu as used
        system.menu_manager.mark_menu_as_used('eda', 'clear_data_backup')
        
        return True

    def _fix_gaps_interactive(self, gap_summary: List[Dict], Fore, Style):
        """Interactive gap fixing with user choice of algorithm and progress tracking."""
        print(f"\n🔧 GAP FIXING INTERFACE")
        print("=" * 50)
        
        # Show explanation of why gaps need to be fixed
        print(explain_why_fix_gaps())
        
        # Extract file paths from gap summary
        print(f"\n🔍 Searching for files to fix gaps...")
        file_paths = []
        for entry in gap_summary:
            file_name = entry.get('file', '')
            print(f"   🔍 Looking for: {file_name}")
            if file_name:
                # Try to find the actual file path in various locations
                possible_paths = [
                    Path('data') / file_name,
                    Path('data/indicators/parquet') / file_name,
                    Path('data/indicators/csv') / file_name,
                    Path('data/raw_parquet') / file_name,
                    Path('data/cache/csv_converted') / file_name,  # Add this path
                    Path('mql5_feed') / file_name,
                    Path('mql5_feed/indicators') / file_name
                ]
                
                # Also try with .csv extension if it's a .parquet file
                if file_name.endswith('.parquet'):
                    csv_name = file_name.replace('.parquet', '.csv')
                    possible_paths.extend([
                        Path('data') / csv_name,
                        Path('data/indicators/csv') / csv_name,
                        Path('mql5_feed') / csv_name
                    ])
                
                # Also try with .parquet extension if it's a .csv file
                elif file_name.endswith('.csv'):
                    parquet_name = file_name.replace('.csv', '.parquet')
                    possible_paths.extend([
                        Path('data') / parquet_name,
                        Path('data/indicators/parquet') / parquet_name,
                        Path('data/raw_parquet') / parquet_name
                    ])
                
                file_found = False
                for path in possible_paths:
                    if path.exists():
                        file_paths.append(path)  # Keep as Path object
                        file_found = True
                        print(f"   📁 Found: {path}")
                        break
                
                if not file_found:
                    print(f"   ⚠️  File not found: {file_name}")
        
        if not file_paths:
            print("❌ No valid file paths found for gap fixing.")
            print("   💡 Please check if the files exist in the expected locations:")
            print("      • data/")
            print("      • data/indicators/parquet/")
            print("      • data/indicators/csv/")
            print("      • data/raw_parquet/")
            print("      • data/cache/csv_converted/")
            print("      • mql5_feed/")
            return
        
        print(f"\n📁 Files to process: {len(file_paths)}")
        for i, path in enumerate(file_paths, 1):
            print(f"   {i}. {path.name}")
        
        # Algorithm selection
        print(f"\n🔧 Available algorithms:")
        algorithms = ['auto', 'linear', 'cubic', 'interpolate', 'forward_fill', 'backward_fill']
        for i, algo in enumerate(algorithms, 1):
            print(f"   {i}. {algo}")
        
        try:
            algo_choice = input(f"\nSelect algorithm (1-{len(algorithms)}, default: auto): ").strip()
            if algo_choice == '':
                algorithm = 'auto'
            else:
                choice_idx = int(algo_choice) - 1
                if 0 <= choice_idx < len(algorithms):
                    algorithm = algorithms[choice_idx]
                else:
                    print("❌ Invalid choice, using 'auto'")
                    algorithm = 'auto'
        except (ValueError, EOFError):
            algorithm = 'auto'
        
        print(f"\n🔧 Selected algorithm: {algorithm}")
        
        # Confirm gap fixing
        confirm = input(f"\nProceed with gap fixing? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Gap fixing cancelled.")
            return
        
        # Initialize gap fixer
        try:
            gap_fixer = GapFixer(memory_limit_mb=self.max_memory_mb)
        except Exception as e:
            print(f"❌ Error initializing gap fixer: {e}")
            return
        
        # Fix gaps with progress tracking
        print(f"\n🚀 Starting gap fixing process...")
        start_time = time.time()
        
        try:
            results = gap_fixer.fix_multiple_files(file_paths, algorithm, show_progress=True)
            
            # Process results
            successful_fixes = sum(1 for r in results.values() if r.get('success', False))
            total_gaps_fixed = sum(r.get('gaps_fixed', 0) for r in results.values() if r.get('success', False))
            
            total_time = time.time() - start_time
            
            print(f"\n🎉 Gap fixing completed!")
            print(f"📊 Summary:")
            print(f"   • Files processed: {len(file_paths)}")
            print(f"   • Successful fixes: {successful_fixes}")
            print(f"   • Total gaps fixed: {total_gaps_fixed:,}")
            print(f"   • Algorithm used: {algorithm}")
            print(f"   • Total time: {total_time:.1f} seconds")
            
            # Show detailed results
            if results:
                print(f"\n📋 Detailed Results:")
                for file_path, result in results.items():
                    if result.get('success', False):
                        print(f"   ✅ {Path(file_path).name}: {result['gaps_fixed']} gaps fixed")
                    else:
                        print(f"   ❌ {Path(file_path).name}: {result.get('error', 'Unknown error')}")
            
            # Mark menu as used
            print(f"\n✅ Gap fixing marked as completed!")
            
            # Ask if user wants to verify the fixes
            print(f"\n🔍 Verification:")
            verify_fixes = input(f"Would you like to verify that gaps were fixed? (y/n): ").strip().lower()
            
            if verify_fixes in ['y', 'yes']:
                print(f"\n🔍 Running verification check...")
                self._verify_gap_fixes(file_paths, Fore, Style)
            
        except Exception as e:
            print(f"❌ Error during gap fixing: {e}")
            import traceback
            traceback.print_exc()

    def _verify_gap_fixes(self, file_paths: List[Path], Fore, Style):
        """Verify that gaps were properly fixed by running gap analysis again using GapFixer."""
        print(f"\n🔍 VERIFICATION: CHECKING GAPS AFTER FIXING")
        print("=" * 60)
        
        try:
            from ..data import GapFixer
            
            total_files = len(file_paths)
            verification_results = []
            
            print(f"📊 Re-analyzing {total_files} files for gaps using GapFixer...")
            print(f"💡 Note: Using reliable full-data analysis instead of sampling")
            
            # Initialize GapFixer
            gap_fixer = GapFixer(memory_limit_mb=self.max_memory_mb)
            
            for i, file_path in enumerate(file_paths, 1):
                print(f"\n📁 Verifying file {i}/{total_files}: {file_path.name}")
                
                try:
                    # Load file
                    if file_path.suffix.lower() == '.parquet':
                        df = pd.read_parquet(file_path)
                    elif file_path.suffix.lower() == '.csv':
                        df = pd.read_csv(file_path)
                    else:
                        print(f"   ⚠️  Skipping unsupported format: {file_path.suffix}")
                        continue
                    
                    # Use GapFixer's reliable gap detection
                    timestamp_col = gap_fixer._find_timestamp_column(df)
                    if timestamp_col:
                        gap_info = gap_fixer._detect_gaps(df, timestamp_col)
                        
                        if gap_info['has_gaps']:
                            total_gaps = gap_info['gap_count']
                            print(f"   ⚠️  Found {total_gaps:,} gaps remaining")
                            verification_results.append({
                                'file': file_path.name,
                                'gaps_remaining': total_gaps,
                                'status': 'gaps_found',
                                'method': 'GapFixer (full data)'
                            })
                        else:
                            print(f"   ✅ No gaps found - file is clean!")
                            verification_results.append({
                                'file': file_path.name,
                                'gaps_remaining': 0,
                                'status': 'clean',
                                'method': 'GapFixer (full data)'
                            })
                    else:
                        print(f"   ❌ No timestamp column found")
                        verification_results.append({
                            'file': file_path.name,
                            'gaps_remaining': -1,
                            'status': 'error',
                            'method': 'GapFixer'
                        })
                    
                    # Memory cleanup
                    del df
                    gc.collect()
                    
                except Exception as e:
                    print(f"   ❌ Error analyzing {file_path.name}: {e}")
                    verification_results.append({
                        'file': file_path.name,
                        'gaps_remaining': -1,
                        'status': 'error',
                        'method': 'GapFixer'
                    })
            
            # Summary
            print(f"\n🔍 VERIFICATION SUMMARY")
            print("=" * 40)
            
            clean_files = sum(1 for r in verification_results if r['status'] == 'clean')
            files_with_gaps = sum(1 for r in verification_results if r['status'] == 'gaps_found')
            error_files = sum(1 for r in verification_results if r['status'] == 'error')
            total_gaps_remaining = sum(r['gaps_remaining'] for r in verification_results if r['status'] == 'gaps_found')
            
            print(f"📊 Results:")
            print(f"   ✅ Clean files (no gaps): {clean_files}")
            print(f"   ⚠️  Files with remaining gaps: {files_with_gaps}")
            print(f"   ❌ Files with errors: {error_files}")
            
            if total_gaps_remaining > 0:
                print(f"   📈 Total gaps remaining: {total_gaps_remaining:,}")
                print(f"   💡 Some gaps may still exist - consider re-running gap fixing")
            else:
                print(f"   🎉 All gaps successfully fixed!")
                print(f"   💡 Note: This verification uses reliable full-data analysis")
            
            # Show detailed results
            if verification_results:
                print(f"\n📋 Detailed Verification Results:")
                for result in verification_results:
                    if result['status'] == 'clean':
                        print(f"   ✅ {result['file']}: Clean (no gaps) - {result['method']}")
                    elif result['status'] == 'gaps_found':
                        print(f"   ⚠️  {result['file']}: {result['gaps_remaining']:,} gaps remaining - {result['method']}")
                    else:
                        print(f"   ❌ {result['file']}: Error during verification - {result['method']}")
            
        except Exception as e:
            print(f"❌ Error during verification: {e}")
            import traceback
            traceback.print_exc()
    
    def _fix_time_series_gaps(self, dataframes: List[pd.DataFrame]) -> List[pd.DataFrame]:
        """
        Fix time series gaps in all loaded dataframes before combining.
        
        Args:
            dataframes: List of DataFrames to fix
            
        Returns:
            List of fixed DataFrames
        """
        if not dataframes or dataframes is None:
            return []
        
        print(f"🔧 Starting time series gap fixing for {len(dataframes)} dataframes...")
        
        # Initialize GapFixer
        gap_fixer = GapFixer(memory_limit_mb=self.max_memory_mb)
        fixed_dataframes = []
        
        for i, df in enumerate(dataframes, 1):
            print(f"\n📁 Processing dataframe {i}/{len(dataframes)}...")
            
            try:
                # Find timestamp column
                timestamp_col = gap_fixer._find_timestamp_column(df)
                
                if timestamp_col:
                    print(f"   📅 Found timestamp column: {timestamp_col}")
                    
                    # Detect gaps
                    gap_info = gap_fixer._detect_gaps(df, timestamp_col)
                    
                    if gap_info['has_gaps']:
                        print(f"   ⚠️  Found {gap_info['gap_count']:,} gaps, fixing...")
                        
                        # Fix gaps using auto algorithm
                        fixed_df, results = gap_fixer._fix_gaps_in_dataframe(
                            df, timestamp_col, gap_info, 'auto', show_progress=True
                        )
                        
                        print(f"   ✅ Gaps fixed successfully!")
                        print(f"      • Algorithm used: {results['algorithm_used']}")
                        print(f"      • Gaps fixed: {results['gaps_fixed']:,}")
                        print(f"      • Processing time: {results['processing_time']:.2f}s")
                        print(f"      • Memory used: {results['memory_used_mb']:.1f}MB")
                        
                        fixed_dataframes.append(fixed_df)
                        
                        # Memory cleanup
                        del fixed_df
                        gc.collect()
                        
                    else:
                        print(f"   ✅ No gaps found, dataframe is clean")
                        fixed_dataframes.append(df)
                else:
                    print(f"   ⚠️  No timestamp column found, skipping gap fixing")
                    fixed_dataframes.append(df)
                
            except Exception as e:
                print(f"   ❌ Error fixing gaps in dataframe {i}: {e}")
                print(f"   💡 Continuing with original dataframe...")
                fixed_dataframes.append(df)
            
            # Memory management
            if self.enable_memory_optimization:
                gc.collect()
        
        print(f"\n✅ Time series gap fixing completed!")
        print(f"   📊 Dataframes processed: {len(dataframes)}")
        print(f"   🔧 Gaps fixed where possible")
        
        return fixed_dataframes

    def load_multi_timeframe_data(self, system) -> bool:
        """
        Load data with proper multi-timeframe strategy for robust ML trading model.
        
        This method:
        1. Identifies timeframes from filenames
        2. Loads each timeframe separately 
        3. Creates hierarchical timeframe structure
        4. Synchronizes timeframes to base timeframe
        5. Generates cross-timeframe features
        
        Returns:
            bool: True if successful, False otherwise
        """
        print("\n📁 LOAD MULTI-TIMEFRAME DATA")
        print("-" * 50)
        print("🎯 This method creates robust ML features by properly handling")
        print("   multiple timeframes (M1, M5, H1, D1, MN1) as separate datasets")
        print("   instead of mixing them in one DataFrame.")
        print("-" * 50)
        
        # Get all data files with timeframe detection
        data_folder = Path("data")
        
        if not data_folder.exists():
            print("❌ Data folder not found. Please ensure 'data' folder exists.")
            return False
        
        # Find all data files and detect timeframes
        timeframe_data = {}
        
        # Search in multiple locations
        search_locations = [
            data_folder,
            data_folder / "raw_parquet",
            data_folder / "indicators" / "parquet",
            data_folder / "cache" / "csv_converted",
            Path("mql5_feed")
        ]
        
        for location in search_locations:
            if not location.exists():
                continue
                
            for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
                files = list(location.glob(f"*{ext}"))
                files = [f for f in files if not f.name.startswith('tmp')]
                
                for file in files:
                    # Detect timeframe from filename
                    timeframe = self._detect_timeframe_from_filename(file.name)
                    
                    if timeframe not in timeframe_data:
                        timeframe_data[timeframe] = []
                    
                    timeframe_data[timeframe].append(file)
        
        if not timeframe_data:
            print("❌ No data files found")
            return False
        
        # Display found timeframes
        print(f"📊 Found data for {len(timeframe_data)} timeframes:")
        for tf, files in timeframe_data.items():
            print(f"   {tf}: {len(files)} files")
            for file in files[:3]:  # Show first 3 files
                file_size_mb = self._get_file_size_mb(file)
                print(f"      • {file.name} ({file_size_mb:.1f}MB)")
            if len(files) > 3:
                print(f"      • ... and {len(files) - 3} more files")
        
        # Ask user to select base timeframe
        print("\n🎯 SELECT BASE TIMEFRAME")
        print("-" * 30)
        print("💡 Base timeframe will be the primary timeframe for ML model.")
        print("   Other timeframes will be used as cross-timeframe features.")
        print("")
        
        available_timeframes = list(timeframe_data.keys())
        for i, tf in enumerate(available_timeframes, 1):
            print(f"{i}. {tf} ({len(timeframe_data[tf])} files)")
        
        try:
            choice = input("\nSelect base timeframe (number): ").strip()
            if not choice.isdigit():
                print("❌ Invalid choice")
                return False
                
            tf_idx = int(choice) - 1
            if tf_idx < 0 or tf_idx >= len(available_timeframes):
                print("❌ Invalid timeframe selection")
                return False
                
            base_timeframe = available_timeframes[tf_idx]
            
        except EOFError:
            print("\n👋 Goodbye!")
            return False
        
        print(f"\n✅ Selected base timeframe: {base_timeframe}")
        
        # Load base timeframe data
        print(f"\n🔄 Loading base timeframe data ({base_timeframe})...")
        base_data = []
        
        for file in timeframe_data[base_timeframe]:
            try:
                df = self.load_data_from_file(str(file))
                df['source_file'] = file.name
                df['timeframe'] = base_timeframe
                base_data.append(df)
                print(f"✅ Loaded: {file.name} ({df.shape[0]:,} rows)")
            except Exception as e:
                print(f"❌ Error loading {file.name}: {e}")
                continue
        
        if not base_data:
            print("❌ No base timeframe data could be loaded")
            return False
        
        # Combine base timeframe data
        print(f"\n🔄 Combining base timeframe data...")
        system.current_data = pd.concat(base_data, ignore_index=True)
        
        # Store timeframe information
        system.timeframe_info = {
            'base_timeframe': base_timeframe,
            'available_timeframes': timeframe_data,
            'cross_timeframes': {tf: files for tf, files in timeframe_data.items() if tf != base_timeframe}
        }
        
        print(f"✅ Base dataset created: {system.current_data.shape[0]:,} rows, {system.current_data.shape[1]} columns")
        
        # Ask if user wants to add cross-timeframe features
        if system.timeframe_info['cross_timeframes']:
            print(f"\n🔄 CROSS-TIMEFRAME FEATURES")
            print("-" * 30)
            print("💡 Add features from other timeframes to enhance ML model:")
            for tf, files in system.timeframe_info['cross_timeframes'].items():
                print(f"   • {tf}: {len(files)} files available")
            
            try:
                add_cross = input("\nAdd cross-timeframe features? (y/n, default: y): ").strip().lower()
            except EOFError:
                print("\n👋 Goodbye!")
                return False
            
            if add_cross in ['', 'y', 'yes']:
                return self._add_cross_timeframe_features(system)
        
        print(f"\n✅ Multi-timeframe data loading completed!")
        print(f"   Base timeframe: {base_timeframe}")
        print(f"   Total rows: {system.current_data.shape[0]:,}")
        print(f"   Total columns: {system.current_data.shape[1]}")
        
        return True
    
    def _detect_timeframe_from_filename(self, filename: str) -> str:
        """
        Detect timeframe from filename patterns.
        
        Args:
            filename: Name of the file
            
        Returns:
            str: Detected timeframe or 'UNKNOWN'
        """
        filename_upper = filename.upper()
        
        # Common timeframe patterns
        patterns = {
            'M1': ['_M1_', '_M1.', 'PERIOD_M1', '_1M_', '_1M.'],
            'M5': ['_M5_', '_M5.', 'PERIOD_M5', '_5M_', '_5M.'],
            'M15': ['_M15_', '_M15.', 'PERIOD_M15', '_15M_', '_15M.'],
            'M30': ['_M30_', '_M30.', 'PERIOD_M30', '_30M_', '_30M.'],
            'H1': ['_H1_', '_H1.', 'PERIOD_H1', '_1H_', '_1H.'],
            'H4': ['_H4_', '_H4.', 'PERIOD_H4', '_4H_', '_4H.'],
            'D1': ['_D1_', '_D1.', 'PERIOD_D1', '_1D_', '_1D.', '_DAILY_'],
            'W1': ['_W1_', '_W1.', 'PERIOD_W1', '_1W_', '_1W.', '_WEEKLY_'],
            'MN1': ['_MN1_', '_MN1.', 'PERIOD_MN1', '_1MN_', '_1MN.', '_MONTHLY_']
        }
        
        for timeframe, tf_patterns in patterns.items():
            for pattern in tf_patterns:
                if pattern in filename_upper:
                    return timeframe
        
        # Additional checks for common naming conventions
        if 'MINUTE' in filename_upper:
            if '1' in filename_upper:
                return 'M1'
            elif '5' in filename_upper:
                return 'M5'
            elif '15' in filename_upper:
                return 'M15'
            elif '30' in filename_upper:
                return 'M30'
        
        if 'HOUR' in filename_upper:
            if '1' in filename_upper:
                return 'H1'
            elif '4' in filename_upper:
                return 'H4'
        
        if 'DAY' in filename_upper or 'DAILY' in filename_upper:
            return 'D1'
        
        if 'WEEK' in filename_upper or 'WEEKLY' in filename_upper:
            return 'W1'
        
        if 'MONTH' in filename_upper or 'MONTHLY' in filename_upper:
            return 'MN1'
        
        return 'UNKNOWN'
    
    def _add_cross_timeframe_features(self, system) -> bool:
        """
        Add cross-timeframe features to the base dataset.
        
        Args:
            system: Interactive system instance
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n🔄 Adding cross-timeframe features...")
        
        base_timeframe = system.timeframe_info['base_timeframe']
        cross_timeframes = system.timeframe_info['cross_timeframes']
        
        # Load and process each cross-timeframe
        for tf, files in cross_timeframes.items():
            print(f"\n📊 Processing {tf} timeframe...")
            
            # Load cross-timeframe data
            cross_data = []
            for file in files:
                try:
                    df = self.load_data_from_file(str(file))
                    df['timeframe'] = tf
                    cross_data.append(df)
                    print(f"   ✅ Loaded: {file.name} ({df.shape[0]:,} rows)")
                except Exception as e:
                    print(f"   ❌ Error loading {file.name}: {e}")
                    continue
            
            if not cross_data:
                print(f"   ⚠️  No data loaded for {tf}")
                continue
            
            # Combine cross-timeframe data
            combined_cross = pd.concat(cross_data, ignore_index=True)
            
            # Add cross-timeframe features using the existing generator
            try:
                from src.ml.feature_engineering import CrossTimeframeFeatureGenerator
                
                cross_generator = CrossTimeframeFeatureGenerator()
                
                # Generate features with timeframe prefix
                cross_features = cross_generator.generate_features(combined_cross)
                
                # Add timeframe prefix to feature names
                feature_columns = [col for col in cross_features.columns 
                                 if col not in ['Open', 'High', 'Low', 'Close', 'Volume', 'source_file', 'timeframe']]
                
                rename_dict = {col: f"{tf}_{col}" for col in feature_columns}
                cross_features = cross_features.rename(columns=rename_dict)
                
                # Merge with base data (this is simplified - in practice would need proper time alignment)
                print(f"   🔄 Generated {len(feature_columns)} cross-timeframe features for {tf}")
                
                # Store cross-timeframe data separately for now
                if not hasattr(system, 'cross_timeframe_data'):
                    system.cross_timeframe_data = {}
                
                system.cross_timeframe_data[tf] = cross_features
                
            except Exception as e:
                print(f"   ❌ Error generating cross-timeframe features for {tf}: {e}")
                continue
        
        print(f"\n✅ Cross-timeframe feature generation completed!")
        return True
