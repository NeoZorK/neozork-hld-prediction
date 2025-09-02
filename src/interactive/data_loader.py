#!/usr/bin/env python3
"""
Data loading utilities for various file formats.
Handles CSV, Parquet, and other data file loading with optimization.
"""

import pandas as pd
import gc
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
            
        # Look for common datetime column names
        datetime_columns = ['timestamp', 'time', 'date', 'datetime', 'dt']
        
        for col in datetime_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    df.set_index(col, inplace=True)
                    print(f"✅ Set '{col}' as datetime index")
                    return df
                except Exception:
                    continue
        
        # If no datetime column found, try to convert first column
        if len(df.columns) > 0:
            first_col = df.columns[0]
            try:
                df[first_col] = pd.to_datetime(df[first_col], errors='coerce')
                df.set_index(first_col, inplace=True)
                print(f"✅ Set '{first_col}' as datetime index")
                return df
            except Exception:
                pass
        
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
        Load CSV file in chunks with progress bar.
        
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
        
        try:
            chunk_iter = pd.read_csv(file_path, chunksize=chunk_size, header=header_row)
            
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
                
                # Progress indicator with percentage
                if (i + 1) % 5 == 0:
                    progress = min(100, (total_rows / (total_rows + 1000)) * 100)
                    print(f"\r   📈 Progress: {progress:.1f}% - Loaded {i + 1} chunks ({total_rows:,} rows)", end="", flush=True)
                
                # Check memory
                if not self.memory_manager.check_memory_available():
                    print(f"⚠️  Low memory detected, stopping at chunk {i + 1}")
                    break
            
            # Combine chunks
            if chunks:
                print(f"\r   📈 Loaded {len(chunks)} chunks ({total_rows:,} rows) ✅")
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
            
            # Check if file has datetime index
            first_row_group = parquet_file.read_row_group(0)
            sample_df = first_row_group.to_pandas()
            has_datetime_index = isinstance(sample_df.index, pd.DatetimeIndex)
            datetime_index_name = sample_df.index.name if has_datetime_index else None
            
            if total_rows <= self.chunk_size:
                # Small file, load directly
                df = pd.read_parquet(file_path)
                return self.handle_datetime_index(df)
            
            # Large file, load in chunks
            print(f"📊 Loading {file_path.name} in chunks of {self.chunk_size:,} rows...")
            
            if has_datetime_index:
                print(f"📅 Detected DatetimeIndex: {datetime_index_name}, preserving during loading...")
                
                # For files with DatetimeIndex, load entire file to preserve index
                if total_rows > 5000000:  # 5M rows threshold
                    print(f"⚠️  Very large file with DatetimeIndex detected ({total_rows:,} rows).")
                    print(f"   Loading entire file to preserve index structure...")
                    df = pd.read_parquet(file_path)
                    return self.handle_datetime_index(df)
                else:
                    print(f"   Loading entire file to preserve index structure...")
                    df = pd.read_parquet(file_path)
                    return self.handle_datetime_index(df)
            else:
                # No DatetimeIndex, safe to load in chunks
                chunks = []
                for i, chunk in enumerate(parquet_file.iter_batches(batch_size=self.chunk_size)):
                    chunk_df = chunk.to_pandas()
                    chunks.append(chunk_df)
                    
                    # Memory management
                    self.memory_manager.optimize_memory()
                    
                    # Progress indicator with percentage
                    if (i + 1) % 10 == 0:
                        rows_loaded = (i + 1) * self.chunk_size
                        progress = min(100, (rows_loaded / total_rows) * 100)
                        print(f"\r   📈 Progress: {progress:.1f}% ({rows_loaded:,}/{total_rows:,} rows) [{i+1} chunks]", end="", flush=True)
                    
                    # Check memory
                    if not self.memory_manager.check_memory_available():
                        print(f"⚠️  Low memory detected, stopping at chunk {i + 1}")
                        break
                
                # Combine chunks
                if chunks:
                    print(f"\r   📈 Progress: 100.0% ({total_rows:,} rows loaded) ✅")
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
                return self.load_csv_in_chunks(file_path, datetime_columns, self.chunk_size)
            else:
                return self.load_csv_direct(file_path, datetime_columns)
        elif file_path.suffix.lower() == '.parquet':
            return self.load_parquet_with_optimization(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
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
