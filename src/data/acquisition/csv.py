# -*- coding: utf-8 -*-
# src/../data/acquisition/csv.py

"""
CSV data acquisition functionality.
Handles loading and processing of CSV data files.
All comments are in English.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import pandas as pd
import glob


class CSVDataAcquisition:
    """Handles CSV data acquisition and processing."""
    
    def __init__(self):
        """Initialize the CSV acquisition module."""
        self.supported_formats = ['.csv', '.parquet']
        self.data_directory = Path('data')
    
    def acquire_csv_data(self, instrument: str, start_date: Optional[str] = None, 
                        end_date: Optional[str] = None, **kwargs) -> Optional[pd.DataFrame]:
        """
        Acquire CSV data for a given instrument.
        
        Args:
            instrument: Name of the instrument
            start_date: Start date for data range
            end_date: End date for data range
            **kwargs: Additional arguments
            
        Returns:
            DataFrame with CSV data or None if failed
        """
        try:
            # Find CSV files for the instrument
            csv_files = self._find_csv_files(instrument)
            
            if not csv_files:
                print(f"❌ No CSV files found for {instrument}")
                return None
            
            # Load and combine data from all files
            data_frames = []
            for csv_file in csv_files:
                df = self._load_csv_file(csv_file)
                if df is not None:
                    data_frames.append(df)
            
            if not data_frames:
                print(f"❌ Failed to load any CSV files for {instrument}")
                return None
            
            # Combine all data frames
            combined_data = pd.concat(data_frames, ignore_index=True)
            
            # Filter by date range if specified
            if start_date or end_date:
                combined_data = self._filter_by_date_range(combined_data, start_date, end_date)
            
            # Sort by timestamp
            combined_data = self._sort_by_timestamp(combined_data)
            
            print(f"✅ Loaded {len(combined_data)} rows from {len(csv_files)} CSV files")
            return combined_data
            
        except Exception as e:
            print(f"❌ Error acquiring CSV data for {instrument}: {e}")
            return None
    
    def _find_csv_files(self, instrument: str) -> List[Path]:
        """Find CSV files for a given instrument."""
        csv_files = []
        
        # Search in data directory
        if self.data_directory.exists():
            # Look for files with instrument name
            pattern = f"*{instrument}*"
            
            # Search for CSV files
            csv_pattern = self.data_directory / f"{pattern}.csv"
            csv_files.extend(glob.glob(str(csv_pattern)))
            
            # Search for parquet files
            parquet_pattern = self.data_directory / f"{pattern}.parquet"
            csv_files.extend(glob.glob(str(parquet_pattern)))
            
            # Search in subdirectories
            for subdir in self.data_directory.iterdir():
                if subdir.is_dir():
                    csv_pattern = subdir / f"{pattern}.csv"
                    csv_files.extend(glob.glob(str(csv_pattern)))
                    
                    parquet_pattern = subdir / f"{pattern}.parquet"
                    csv_files.extend(glob.glob(str(parquet_pattern)))
        
        # Convert to Path objects
        csv_files = [Path(f) for f in csv_files]
        
        print(f"🔍 Found {len(csv_files)} files for {instrument}")
        return csv_files
    
    def _load_csv_file(self, file_path: Path) -> Optional[pd.DataFrame]:
        """Load a single CSV file."""
        try:
            if file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix == '.parquet':
                df = pd.read_parquet(file_path)
            else:
                print(f"❌ Unsupported file format: {file_path.suffix}")
                return None
            
            print(f"📁 Loaded {file_path.name}: {len(df)} rows")
            return df
            
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            return None
    
    def _filter_by_date_range(self, df: pd.DataFrame, start_date: Optional[str], 
                             end_date: Optional[str]) -> pd.DataFrame:
        """Filter DataFrame by date range."""
        try:
            # Find timestamp column
            timestamp_col = self._find_timestamp_column(df)
            if timestamp_col is None:
                print("⚠️  No timestamp column found, skipping date filtering")
                return df
            
            # Convert timestamp column to datetime
            df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
            
            # Apply date filters
            if start_date:
                start_dt = pd.to_datetime(start_date)
                df = df[df[timestamp_col] >= start_dt]
            
            if end_date:
                end_dt = pd.to_datetime(end_date)
                df = df[df[timestamp_col] <= end_dt]
            
            print(f"📅 Filtered to {len(df)} rows after date filtering")
            return df
            
        except Exception as e:
            print(f"⚠️  Error during date filtering: {e}")
            return df
    
    def _sort_by_timestamp(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sort DataFrame by timestamp column."""
        try:
            timestamp_col = self._find_timestamp_column(df)
            if timestamp_col is None:
                return df
            
            # Sort by timestamp
            df = df.sort_values(timestamp_col)
            df = df.reset_index(drop=True)
            
            return df
            
        except Exception as e:
            print(f"⚠️  Error during timestamp sorting: {e}")
            return df
    
    def _find_timestamp_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find the timestamp column in the DataFrame."""
        timestamp_candidates = ['timestamp', 'time', 'date', 'datetime', 'ts']
        
        # Check for exact matches (case-insensitive)
        for col in df.columns:
            col_lower = col.lower()
            if any(candidate == col_lower for candidate in timestamp_candidates):
                return col
        
        # Check for partial matches
        for col in df.columns:
            col_lower = col.lower()
            if any(candidate in col_lower for candidate in timestamp_candidates):
                return col
        
        # Check for datetime columns
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                return col
        
        return None
