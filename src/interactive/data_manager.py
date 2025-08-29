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
        # Memory management settings - more conservative defaults
        self.max_memory_mb = int(os.environ.get('MAX_MEMORY_MB', '1024'))  # 1GB default
        self.chunk_size = int(os.environ.get('CHUNK_SIZE', '25000'))  # 25k rows per chunk
        self.enable_memory_optimization = os.environ.get('ENABLE_MEMORY_OPTIMIZATION', 'true').lower() == 'true'
        
        # Aggressive memory settings
        self.max_file_size_mb = int(os.environ.get('MAX_FILE_SIZE_MB', '50'))  # 50MB threshold
        self.sample_size = int(os.environ.get('SAMPLE_SIZE', '10000'))  # 10k rows for sampling
        self.enable_streaming = os.environ.get('ENABLE_STREAMING', 'true').lower() == 'true'
        
        # Memory monitoring
        self.memory_warning_threshold = 0.7  # 70% of max memory
        self.memory_critical_threshold = 0.9  # 90% of max memory
        
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
                required_mb = self.max_memory_mb * 0.3  # Require 30% of max memory
            
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
        
        # Try to detect datetime columns first
        datetime_columns = []
        try:
            # Read first few rows to detect datetime columns
            sample_df = pd.read_csv(file_path, nrows=1000)
            for col in sample_df.columns:
                if any(keyword in col.lower() for keyword in ['date', 'time', 'datetime', 'timestamp']):
                    datetime_columns.append(col)
                elif sample_df[col].dtype == 'object':
                    # Try to parse as datetime
                    try:
                        pd.to_datetime(sample_df[col].iloc[0], errors='raise')
                        datetime_columns.append(col)
                    except:
                        pass
        except Exception as e:
            print(f"⚠️  Warning: Could not detect datetime columns: {e}")
        
        # Load data in chunks if needed
        if self._should_use_chunked_loading(file_path):
            return self._load_csv_in_chunks(file_path, datetime_columns, chunk_size)
        else:
            return self._load_csv_direct(file_path, datetime_columns)
    
    def _load_csv_direct(self, file_path: Path, datetime_columns: List[str]) -> pd.DataFrame:
        """Load CSV file directly with datetime parsing."""
        try:
            # Load with datetime parsing
            df = pd.read_csv(file_path)
            
            # Parse datetime columns
            for col in datetime_columns:
                if col in df.columns:
                    try:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                        print(f"✅ Parsed datetime column: {col}")
                    except Exception as e:
                        print(f"⚠️  Could not parse datetime column {col}: {e}")
            
            return df
        except Exception as e:
            print(f"❌ Error loading CSV directly: {e}")
            raise
    
    def _load_csv_in_chunks(self, file_path: Path, datetime_columns: List[str], chunk_size: int) -> pd.DataFrame:
        """Load CSV file in chunks with datetime parsing."""
        print(f"📊 Loading {file_path.name} in chunks of {chunk_size:,} rows...")
        
        chunks = []
        total_rows = 0
        
        try:
            chunk_iter = pd.read_csv(file_path, chunksize=chunk_size)
            
            for i, chunk in enumerate(chunk_iter):
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
                return result
            else:
                raise ValueError("No chunks were loaded")
                
        except Exception as e:
            print(f"❌ Error in chunked CSV loading: {e}")
            raise
    
    def _load_parquet_with_optimization(self, file_path: Path) -> pd.DataFrame:
        """Load parquet file with memory optimization."""
        print(f"🔄 Loading Parquet: {file_path.name}")
        
        try:
            import pyarrow.parquet as pq
            
            # Get file info
            parquet_file = pq.ParquetFile(file_path)
            total_rows = parquet_file.metadata.num_rows
            
            if total_rows <= self.chunk_size:
                # Small file, load directly
                return pd.read_parquet(file_path)
            
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
                return result
            else:
                raise ValueError("No chunks were loaded")
                
        except ImportError:
            # Fallback to pandas
            return pd.read_parquet(file_path)
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
        
        # Get all subfolders in data directory
        data_folder = Path("data")
        if not data_folder.exists():
            print("❌ Data folder not found. Please ensure 'data' folder exists.")
            return False
        
        # Find all subfolders
        subfolders = [data_folder]  # Include main data folder
        for item in data_folder.iterdir():
            if item.is_dir():
                subfolders.append(item)
                # Also include sub-subfolders
                for subitem in item.iterdir():
                    if subitem.is_dir():
                        subfolders.append(subitem)
        
        print("💡 Available folders:")
        print("0. 🔙 Back to Main Menu")
        for i, folder in enumerate(subfolders, 1):
            try:
                rel_path = folder.relative_to(Path.cwd())
            except ValueError:
                rel_path = folder
            print(f"{i}. 📁 {rel_path}/")
        
        print("-" * 30)
        print("💡 Examples:")
        print("   • Enter folder number (e.g., 1 for data/)")
        print("   • Or enter folder path with mask (e.g., data gbpusd)")
        print("   • Or enter folder path with file type (e.g., data parquet)")
        print("")
        print("📋 More Examples:")
        print("   • 3 eurusd     (folder 3 with 'eurusd' in filename)")
        print("   • 8 btcusdt    (folder 8 with 'btcusdt' in filename)")
        print("   • data gbpusd  (data folder with 'gbpusd' in filename)")
        print("   • data sample  (data folder with 'sample' in filename)")
        print("   • 3 csv        (folder 3 with '.csv' files)")
        print("   • 7 parquet    (folder 7 with '.parquet' files)")
        print("   • 8 aapl       (folder 8 with 'aapl' in filename)")
        print("   • 3 btcusd     (folder 3 with 'btcusd' in filename)")
        print("   • data test    (data folder with 'test' in filename)")
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
        
        # Find all data files
        data_files = []
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            if mask:
                # Apply mask filter
                pattern = f"*{mask}*{ext}"
                data_files.extend(folder_path.glob(pattern))
                # Also try case-insensitive search
                pattern = f"*{mask.upper()}*{ext}"
                data_files.extend(folder_path.glob(pattern))
                pattern = f"*{mask.lower()}*{ext}"
                data_files.extend(folder_path.glob(pattern))
            else:
                # No mask, get all files
                data_files.extend(folder_path.glob(f"*{ext}"))
        
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
                
                # Check if we're approaching memory limits
                if total_memory_mb > self.max_memory_mb * 0.8:
                    print(f"⚠️  Memory usage high ({total_memory_mb}MB), stopping file loading")
                    break
                    
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
            # Combine DataFrames
            system.current_data = pd.concat(all_data, ignore_index=True)
            
            # Clean up intermediate data
            del all_data
            gc.collect()
            
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
    
    def restore_from_backup(self, system):
        """Restore data from backup file."""
        print("\n📥 RESTORE FROM BACKUP")
        print("-" * 30)
        
        # Implementation for backup restoration
        print("📥 Backup restoration coming soon...")
    
    def clear_data_backup(self, system):
        """Clear all backup files from the backup directory."""
        print("\n🗑️ CLEAR DATA BACKUP")
        print("-" * 30)
        
        # Implementation for clearing backups
        print("🗑️ Backup clearing coming soon...")
