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
            
            if total_rows <= self.chunk_size:
                # Small file, load directly with datetime index handling
                df = pd.read_parquet(file_path)
                return self._handle_datetime_index(df)
            
            # Large file, load in chunks
            print(f"📊 Loading {file_path.name} in chunks of {self.chunk_size:,} rows...")
            
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
            
            return True
            
        except Exception as e:
            print(f"❌ Error combining data: {e}")
            return False
    
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
