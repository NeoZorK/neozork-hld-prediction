#!/usr/bin/env python3
"""
Data loading utilities for various file formats.
Handles CSV, Parquet, and other data file loading with optimization.
"""

import pandas as pd
import gc
import time
from pathlib import Path
from typing import List, Optional
from .memory_manager import MemoryManager


class DataLoader:
    """Handles loading of data files with memory optimization."""
    
    def __init__(self, memory_manager: MemoryManager, chunk_size: int = 50000):
        """
        Initialize DataLoader.
        
        Args:
            memory_manager: MemoryManager instance
            chunk_size: Default chunk size for loading
        """
        self.memory_manager = memory_manager
        self.chunk_size = chunk_size
    
    def handle_datetime_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle datetime index conversion.
        
        Args:
            df: DataFrame to process
            
        Returns:
            DataFrame with proper datetime index
        """
        if df is None or df.empty:
            return df
            
        # Check if index is already datetime
        if isinstance(df.index, pd.DatetimeIndex):
            return df
            
        # Check if index was originally DatetimeIndex but got reset
        # This happens when loading cleaned_data files that were saved with index=True
        if df.index.name == 'Timestamp' and not isinstance(df.index, pd.DatetimeIndex):
            print(f"📅 Restoring 'Timestamp' from index (was DatetimeIndex)")
            # Convert index to column and then set as datetime index
            df = df.reset_index()
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
            df.set_index('Timestamp', inplace=True)
            return df
            
        # Look for common datetime column names (case-insensitive)
        datetime_columns = ['timestamp', 'time', 'date', 'datetime', 'dt']
        
        # First try exact matches
        for col in datetime_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    df.set_index(col, inplace=True)
                    print(f"✅ Set '{col}' as datetime index")
                    return df
                except Exception:
                    continue
        
        # Then try case-insensitive matches
        for col in df.columns:
            col_lower = col.lower()
            if col_lower in datetime_columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    df.set_index(col, inplace=True)
                    print(f"✅ Set '{col}' as datetime index (case-insensitive match)")
                    return df
                except Exception:
                    continue
        
        # If no datetime column found, check if this might be OHLCV data without timestamp
        if len(df.columns) > 0:
            # Check if this looks like OHLCV data (Open, High, Low, Close, Volume)
            ohlcv_indicators = ['open', 'high', 'low', 'close', 'volume']
            has_ohlcv = any(indicator in str(col).lower() for col in df.columns for indicator in ohlcv_indicators)
            
            if has_ohlcv:
                # Check if there's a 'Timestamp' column that needs to be converted
                if 'Timestamp' in df.columns:
                    try:
                        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
                        df.set_index('Timestamp', inplace=True)
                        print(f"✅ Set 'Timestamp' as datetime index from OHLCV data")
                        return df
                    except Exception:
                        print(f"⚠️  Could not convert 'Timestamp' to datetime in OHLCV data")
                
                print(f"⚠️  No timestamp column found in OHLCV data. Data will be loaded without datetime index.")
                print(f"   Available columns: {list(df.columns)}")
                return df
            else:
                # Try to convert first column only if it doesn't look like OHLCV data
                first_col = df.columns[0]
                try:
                    df[first_col] = pd.to_datetime(df[first_col], errors='coerce')
                    df.set_index(first_col, inplace=True)
                    print(f"✅ Set '{first_col}' as datetime index")
                    return df
                except Exception:
                    print(f"⚠️  Could not convert '{first_col}' to datetime. Data will be loaded without datetime index.")
                    return df
        
        return df
    
    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean column names for consistency.
        
        Args:
            df: DataFrame to clean
            
        Returns:
            DataFrame with cleaned column names
        """
        if df is None or df.empty:
            return df
            
        # Clean column names
        cleaned_columns = []
        for col in df.columns:
            # Convert to string and clean
            col_str = str(col).strip()
            
            # Remove special characters and replace spaces with underscores
            col_str = col_str.replace(' ', '_').replace('-', '_').replace('.', '_')
            col_str = ''.join(c for c in col_str if c.isalnum() or c == '_')
            
            # Ensure it doesn't start with a number
            if col_str and col_str[0].isdigit():
                col_str = f"col_{col_str}"
            
            # Ensure it's not empty
            if not col_str:
                col_str = f"col_{len(cleaned_columns)}"
            
            cleaned_columns.append(col_str)
        
        df.columns = cleaned_columns
        return df
    
    def determine_header_row(self, file_path: Path) -> int:
        """
        Determine the header row in a CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            int: Row number containing headers
        """
        try:
            # Read first few lines to find header
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [f.readline() for _ in range(10)]
            
            # Look for line with most commas (likely header)
            max_commas = 0
            header_row = 0
            
            for i, line in enumerate(lines):
                comma_count = line.count(',')
                if comma_count > max_commas:
                    max_commas = comma_count
                    header_row = i
            
            return header_row
            
        except Exception:
            return 0
    
    def detect_datetime_columns(self, file_path: Path, header_row: int) -> List[str]:
        """
        Detect datetime columns in a CSV file.
        
        Args:
            file_path: Path to CSV file
            header_row: Row containing headers
            
        Returns:
            List of datetime column names
        """
        try:
            # Read sample data to detect datetime columns
            sample_df = pd.read_csv(file_path, nrows=100, header=header_row)
            
            datetime_columns = []
            for col in sample_df.columns:
                try:
                    # Try to convert to datetime
                    pd.to_datetime(sample_df[col].head(10), errors='raise')
                    datetime_columns.append(col)
                except Exception:
                    continue
            
            return datetime_columns
            
        except Exception:
            return []
    
    def load_csv_direct(self, file_path: Path, datetime_columns: List[str]) -> pd.DataFrame:
        """
        Load CSV file directly (for small files).
        
        Args:
            file_path: Path to CSV file
            datetime_columns: List of datetime column names
            
        Returns:
            DataFrame with loaded data
        """
        try:
            header_row = self.determine_header_row(file_path)
            df = pd.read_csv(file_path, header=header_row)
            
            # Clean column names
            df = self.clean_column_names(df)
            
            # Parse datetime columns
            for col in datetime_columns:
                if col in df.columns:
                    try:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    except Exception:
                        pass
            
            return self.handle_datetime_index(df)
            
        except Exception as e:
            print(f"❌ Error loading CSV directly: {e}")
            raise
    
    def load_csv_in_chunks(self, file_path: Path, datetime_columns: List[str], chunk_size: int) -> pd.DataFrame:
        """
        Load CSV file in chunks with progress bar and ETA.
        
        Args:
            file_path: Path to CSV file
            datetime_columns: List of datetime column names
            chunk_size: Size of each chunk
            
        Returns:
            DataFrame with loaded data
        """
        print(f"📊 Loading {file_path.name} in chunks of {chunk_size:,} rows...")
        
        header_row = self.determine_header_row(file_path)
        chunks = []
        total_rows = 0
        
        # First pass to count total rows for accurate progress
        print("   🔍 Counting total rows for accurate progress...")
        try:
            # Count total rows efficiently
            total_file_rows = sum(1 for _ in open(file_path)) - 1  # Subtract header
            print(f"   📊 Total rows in file: {total_file_rows:,}")
        except Exception:
            total_file_rows = None
            print("   ⚠️  Could not determine total rows, using estimated progress")
        
        try:
            chunk_iter = pd.read_csv(file_path, chunksize=chunk_size, header=header_row)
            start_time = time.time()
            
            for i, chunk in enumerate(chunk_iter):
                # Clean column names for first chunk only
                if i == 0:
                    chunk = self.clean_column_names(chunk)
                
                # Remove unnamed/empty columns
                unnamed_cols = [col for col in chunk.columns if str(col).startswith('Unnamed:') or str(col) == '']
                if unnamed_cols:
                    chunk = chunk.drop(columns=unnamed_cols)
                
                # Parse datetime columns
                for col in datetime_columns:
                    if col in chunk.columns:
                        try:
                            chunk[col] = pd.to_datetime(chunk[col], errors='coerce')
                        except Exception:
                            pass
                
                chunks.append(chunk)
                total_rows += len(chunk)
                
                # Memory management
                self.memory_manager.optimize_memory()
                
                # Progress indicator with percentage, ETA, and speed
                if (i + 1) % 5 == 0 or i == 0:
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 0:
                        # Calculate ETA
                        if total_file_rows and total_rows > 0:
                            estimated_total_chunks = total_file_rows / chunk_size
                            progress = min(100, (total_rows / total_file_rows) * 100)
                            remaining_chunks = estimated_total_chunks - (i + 1)
                            eta_seconds = (remaining_chunks * elapsed_time) / (i + 1)
                            
                            # Format ETA
                            if eta_seconds < 60:
                                eta_str = f"{eta_seconds:.0f}s"
                            elif eta_seconds < 3600:
                                eta_str = f"{eta_seconds/60:.0f}m {eta_seconds%60:.0f}s"
                            else:
                                eta_str = f"{eta_seconds/3600:.0f}h {(eta_seconds%3600)/60:.0f}m"
                            
                            # Calculate speed (rows per second)
                            speed = total_rows / elapsed_time
                            
                            print(f"\r   📈 Progress: {progress:.1f}% ({total_rows:,}/{total_file_rows:,} rows) "
                                  f"[{i+1} chunks] 🚀 {speed:.0f} rows/s ⏱️ ETA: {eta_str}", end="", flush=True)
                        else:
                            # Fallback progress without ETA
                            progress = min(100, (total_rows / (total_rows + 1000)) * 100)
                            print(f"\r   📈 Progress: {progress:.1f}% - Loaded {i + 1} chunks ({total_rows:,} rows)", end="", flush=True)
                
                # Check memory
                if not self.memory_manager.check_memory_available():
                    print(f"⚠️  Low memory detected, stopping at chunk {i + 1}")
                    break
            
            # Combine chunks
            if chunks:
                total_time = time.time() - start_time
                final_speed = total_rows / total_time if total_time > 0 else 0
                print(f"\r   📈 Progress: 100.0% ({total_rows:,} rows loaded) ✅ [{len(chunks)} chunks] "
                      f"⏱️ Total time: {total_time:.1f}s 🚀 Avg speed: {final_speed:.0f} rows/s")
                result = pd.concat(chunks, ignore_index=True)
                del chunks
                gc.collect()
                return self.handle_datetime_index(result)
            else:
                raise ValueError("No chunks were loaded")
                
        except Exception as e:
            print(f"❌ Error in chunked CSV loading: {e}")
            raise
    
    def load_parquet_with_optimization(self, file_path: Path) -> pd.DataFrame:
        """
        Load parquet file with memory optimization and progress bar.
        
        Args:
            file_path: Path to parquet file
            
        Returns:
            DataFrame with loaded data
        """
        print(f"🔄 Loading Parquet: {file_path.name}")
        
        try:
            import pyarrow.parquet as pq
            
            # Get file info
            parquet_file = pq.ParquetFile(file_path)
            total_rows = parquet_file.metadata.num_rows
            
            # Check if file has datetime index or timestamp column
            first_row_group = parquet_file.read_row_group(0)
            sample_df = first_row_group.to_pandas()
            has_datetime_index = isinstance(sample_df.index, pd.DatetimeIndex)
            datetime_index_name = sample_df.index.name if has_datetime_index else None
            
            # Also check for timestamp column in the data
            has_timestamp_column = any(col.lower() in ['timestamp', 'time', 'date', 'datetime', 'dt'] 
                                     for col in sample_df.columns)
            
            if total_rows <= self.chunk_size:
                # Small file, load directly
                df = pd.read_parquet(file_path)
                return self.handle_datetime_index(df)
            
            # Large file, load in chunks
            print(f"📊 Loading {file_path.name} in chunks of {self.chunk_size:,} rows...")
            
            if has_datetime_index or has_timestamp_column:
                if has_datetime_index:
                    print(f"📅 Detected DatetimeIndex: {datetime_index_name}, preserving during loading...")
                else:
                    print(f"📅 Detected timestamp column, preserving during loading...")
                
                # For files with DatetimeIndex or timestamp column, load in chunks to preserve memory
                print(f"   Loading in chunks to preserve timestamp structure...")
                
                chunks = []
                start_time = time.time()
                
                for i, chunk in enumerate(parquet_file.iter_batches(batch_size=self.chunk_size)):
                    chunk_df = chunk.to_pandas()
                    chunks.append(chunk_df)
                    
                    # Memory management
                    self.memory_manager.optimize_memory()
                    
                    # Progress indicator with percentage, ETA, and speed
                    if (i + 1) % 10 == 0 or i == 0:
                        elapsed_time = time.time() - start_time
                        if elapsed_time > 0:
                            rows_loaded = (i + 1) * self.chunk_size
                            progress = min(100, (rows_loaded / total_rows) * 100)
                            
                            # Calculate ETA
                            remaining_chunks = (total_rows / self.chunk_size) - (i + 1)
                            eta_seconds = (remaining_chunks * elapsed_time) / (i + 1)
                            
                            # Format ETA
                            if eta_seconds < 60:
                                eta_str = f"{eta_seconds:.0f}s"
                            elif eta_seconds < 3600:
                                eta_str = f"{eta_seconds/60:.0f}m {eta_seconds%60:.0f}s"
                            else:
                                eta_str = f"{eta_seconds/3600:.0f}h {(eta_seconds%3600)/60:.0f}m"
                            
                            # Calculate speed (rows per second)
                            speed = rows_loaded / elapsed_time
                            
                            print(f"\r📈 {progress:.1f}% ({rows_loaded:,}/{total_rows:,}) [{i+1} chunks] 🚀 {speed:.0f}/s ⏱️ {eta_str}", end="", flush=True)
                    
                    # Check memory
                    if not self.memory_manager.check_memory_available():
                        print(f"⚠️  Low memory detected, stopping at chunk {i + 1}")
                        break
                
                # Combine chunks
                if chunks:
                    total_time = time.time() - start_time
                    final_speed = total_rows / total_time if total_time > 0 else 0
                    print(f"\r📈 100% ({total_rows:,} rows) ✅ [{len(chunks)} chunks] ⏱️ {total_time:.1f}s 🚀 {final_speed:.0f}/s")
                    result = pd.concat(chunks, ignore_index=True)
                    del chunks
                    gc.collect()
                    return self.handle_datetime_index(result)
                else:
                    raise ValueError("No chunks were loaded")
            else:
                # No DatetimeIndex, safe to load in chunks
                print(f"   No timestamp columns detected, loading in chunks...")
                chunks = []
                start_time = time.time()
                
                for i, chunk in enumerate(parquet_file.iter_batches(batch_size=self.chunk_size)):
                    chunk_df = chunk.to_pandas()
                    chunks.append(chunk_df)
                    
                    # Memory management
                    self.memory_manager.optimize_memory()
                    
                    # Progress indicator with percentage, ETA, and speed
                    if (i + 1) % 10 == 0 or i == 0:
                        elapsed_time = time.time() - start_time
                        if elapsed_time > 0:
                            rows_loaded = (i + 1) * self.chunk_size
                            progress = min(100, (rows_loaded / total_rows) * 100)
                            
                            # Calculate ETA
                            remaining_chunks = (total_rows / self.chunk_size) - (i + 1)
                            eta_seconds = (remaining_chunks * elapsed_time) / (i + 1)
                            
                            # Format ETA
                            if eta_seconds < 60:
                                eta_str = f"{eta_seconds:.0f}s"
                            else:
                                eta_str = f"{eta_seconds/60:.0f}m"
                            
                            # Calculate speed (rows per second)
                            speed = rows_loaded / elapsed_time
                            
                            print(f"\r📈 {progress:.1f}% ({rows_loaded:,}/{total_rows:,}) [{i+1} chunks] 🚀 {speed:.0f}/s ⏱️ {eta_str}", end="", flush=True)
                    
                    # Check memory
                    if not self.memory_manager.check_memory_available():
                        print(f"⚠️  Low memory detected, stopping at chunk {i + 1}")
                        break
                
                # Combine chunks
                if chunks:
                    total_time = time.time() - start_time
                    final_speed = total_rows / total_time if total_time > 0 else 0
                    print(f"\r📈 100% ({total_rows:,} rows) ✅ [{len(chunks)} chunks] ⏱️ {total_time:.1f}s 🚀 {final_speed:.0f}/s")
                    result = pd.concat(chunks, ignore_index=True)
                    del chunks
                    gc.collect()
                    return self.handle_datetime_index(result)
                else:
                    raise ValueError("No chunks were loaded")
                
        except ImportError:
            # Fallback to pandas
            df = pd.read_parquet(file_path)
            return self.handle_datetime_index(df)
        except Exception as e:
            print(f"❌ Error loading parquet: {e}")
            raise
    
    def load_data_from_file(self, file_path: str) -> pd.DataFrame:
        """
        Load data from file with automatic format detection.
        
        Args:
            file_path: Path to file
            
        Returns:
            DataFrame with loaded data
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check memory before loading
        if not self.memory_manager.check_memory_available():
            raise MemoryError("Insufficient memory to load file")
        
        # Load based on file type
        if file_path.suffix.lower() == '.csv':
            datetime_columns = self.detect_datetime_columns(file_path, 0)
            
            if self.memory_manager.should_use_chunked_loading(file_path, self.chunk_size):
                result = self.load_csv_in_chunks(file_path, datetime_columns, self.chunk_size)
            else:
                result = self.load_csv_direct(file_path, datetime_columns)
        elif file_path.suffix.lower() == '.parquet':
            result = self.load_parquet_with_optimization(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        # Final validation
        if result is None:
            raise ValueError("Data loading failed - result is None")
        if result.empty:
            raise ValueError("Data loading failed - result is empty")
        
        return result
    
    def load_data_from_folder(self, folder_path: str) -> List[str]:
        """
        Load data files from folder.
        
        Args:
            folder_path: Path to folder
            
        Returns:
            List of file paths
        """
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
            
        if not folder_path.is_dir():
            raise ValueError(f"Path is not a directory: {folder_path}")
        
        # Find all data files in the folder
        data_files = []
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            files = list(folder_path.glob(f"*{ext}"))
            data_files.extend(files)
        
        return [str(f) for f in data_files]
