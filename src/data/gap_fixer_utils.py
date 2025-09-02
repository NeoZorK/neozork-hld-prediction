# File: src/data/gap_fixer_utils.py
# -*- coding: utf-8 -*-

"""
Utility functions for gap fixing operations.
Includes file loading, gap detection, memory management, and file operations.
All comments are in English.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import shutil
import psutil


class GapFixingUtils:
    """Utility functions for gap fixing operations."""
    
    def __init__(self):
        """Initialize the utilities module."""
        pass
    
    def load_file(self, file_path: Path) -> Optional[pd.DataFrame]:
        """Load file based on its extension."""
        try:
            if file_path.suffix == '.parquet':
                return pd.read_parquet(file_path)
            elif file_path.suffix == '.csv':
                return pd.read_csv(file_path)
            elif file_path.suffix == '.json':
                return pd.read_json(file_path)
            else:
                print(f"   ❌ Unsupported file format: {file_path.suffix}")
                return None
        except Exception as e:
            print(f"   ❌ Error loading file {file_path}: {e}")
            return None
    
    def find_timestamp_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find the timestamp column in the dataframe."""
        # First, check if the index is a DatetimeIndex
        if isinstance(df.index, pd.DatetimeIndex):
            return "DATETIME_INDEX"  # Special marker for DatetimeIndex
        
        # Check for exact matches (case-insensitive)
        timestamp_candidates = ['timestamp', 'time', 'date', 'datetime', 'ts']
        
        for col in df.columns:
            col_lower = col.lower()
            if any(candidate == col_lower for candidate in timestamp_candidates):
                return col
        
        # Then check for partial matches (case-insensitive)
        for col in df.columns:
            col_lower = col.lower()
            if any(candidate in col_lower for candidate in timestamp_candidates):
                return col
        
        # Check for datetime columns
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                return col
        
        # Debug: print available columns only if no timestamp found
        print(f"   🔍 Available columns: {list(df.columns)}")
        
        return None
    
    def convert_datetime_index_to_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert DatetimeIndex to a regular column."""
        df = df.reset_index()
        timestamp_col = df.index.name or 'index'
        # Rename the index column if it's unnamed
        if timestamp_col == 'index':
            timestamp_col = 'Timestamp'
            df = df.rename(columns={'index': 'Timestamp'})
        return df
    
    def detect_gaps(self, df: pd.DataFrame, timestamp_col: str) -> Dict:
        """Detect gaps in time series data."""
        print(f"   🔍 Starting gap detection for {len(df):,} rows...")
        
        # Handle DatetimeIndex case
        if timestamp_col == "DATETIME_INDEX":
            # Use the index directly
            df_sorted = df.copy()
            time_series = df_sorted.index
        else:
            # Sort by timestamp column
            df_sorted = df.sort_values(timestamp_col).copy()
            time_series = df_sorted[timestamp_col]
        
        # Calculate time differences
        time_diffs = time_series.diff().dropna()
        
        # Show some statistics about time differences
        if len(time_diffs) > 0:
            print(f"   📈 Time diff stats:")
            print(f"      • Min: {time_diffs.min()}")
            print(f"      • Max: {time_diffs.max()}")
            print(f"      • Median: {time_diffs.median()}")
            print(f"      • Mean: {time_diffs.mean()}")
            # Handle TimedeltaIndex which doesn't have quantile method
            try:
                print(f"      • 95th percentile: {time_diffs.quantile(0.95)}")
            except AttributeError:
                # For TimedeltaIndex, calculate approximate 95th percentile
                sorted_diffs = sorted(time_diffs)
                idx_95 = int(len(sorted_diffs) * 0.95)
                print(f"      • 95th percentile: {sorted_diffs[idx_95]}")
        
        # Determine expected frequency
        expected_freq = self._determine_expected_frequency(time_diffs)
        print(f"   ⏱️  Expected frequency: {expected_freq}")
        
        # Find gaps (intervals larger than expected frequency)
        gap_threshold = expected_freq * 1.5  # Allow 50% tolerance
        print(f"   🚨 Gap threshold: {gap_threshold}")
        
        gaps = time_diffs > gap_threshold
        print(f"   🔍 Gaps found: {gaps.sum():,} out of {len(time_diffs):,} intervals")
        
        # Show some examples of gaps
        if gaps.any():
            # Handle TimedeltaIndex which doesn't have head method
            try:
                gap_examples = time_diffs[gaps].head(5)
            except AttributeError:
                # For TimedeltaIndex, convert to list and take first 5
                gap_examples = list(time_diffs[gaps])[:5]
            
            print(f"   📋 Example gaps:")
            for i, gap in enumerate(gap_examples):
                print(f"      • Gap {i+1}: {gap}")
        
        gap_info = {
            'has_gaps': gaps.any(),
            'gap_count': gaps.sum(),
            'expected_frequency': expected_freq,
            'gap_threshold': gap_threshold,
            'total_rows': len(df),
            'time_range': {
                'start': time_series.min(),
                'end': time_series.max()
            },
            'is_datetime_index': timestamp_col == "DATETIME_INDEX"
        }
        
        print(f"   ✅ Gap detection completed: {gap_info['gap_count']} gaps found")
        return gap_info
    
    def _determine_expected_frequency(self, time_diffs: pd.Series) -> pd.Timedelta:
        """Determine expected frequency from time differences."""
        if len(time_diffs) == 0:
            print(f"      ⚠️  No time differences available, using default 1H")
            return pd.Timedelta('1H')
        
        # Use median for robustness
        median_diff = time_diffs.median()
        print(f"      📊 Using median time difference: {median_diff}")
        
        # Round to common frequencies
        if median_diff <= pd.Timedelta('1T'):  # 1 minute
            print(f"      ⏱️  Selected frequency: 1 minute (1T)")
            return pd.Timedelta('1T')
        elif median_diff <= pd.Timedelta('5T'):  # 5 minutes
            print(f"      ⏱️  Selected frequency: 5 minutes (5T)")
            return pd.Timedelta('5T')
        elif median_diff <= pd.Timedelta('15T'):  # 15 minutes
            print(f"      ⏱️  Selected frequency: 15 minutes (15T)")
            return pd.Timedelta('15T')
        elif median_diff <= pd.Timedelta('1H'):  # 1 hour
            print(f"      ⏱️  Selected frequency: 1 hour (1H)")
            return pd.Timedelta('1H')
        elif median_diff <= pd.Timedelta('4H'):  # 4 hours
            print(f"      ⏱️  Selected frequency: 4 hours (4H)")
            return pd.Timedelta('4H')
        elif median_diff <= pd.Timedelta('1D'):  # 1 day
            print(f"      ⏱️  Selected frequency: 1 day (1D)")
            return pd.Timedelta('1D')
        else:
            print(f"      ⏱️  Selected frequency: 1 week (1W)")
            return pd.Timedelta('1W')  # 1 week
    
    def check_memory_available(self, memory_limit_mb: int, required_mb: int = None) -> bool:
        """Check if we have enough memory available."""
        try:
            memory = psutil.virtual_memory()
            available_mb = memory.available / (1024 * 1024)
            
            if required_mb is None:
                required_mb = memory_limit_mb * 0.2  # Require 20% of limit
            
            return available_mb > required_mb
        except ImportError:
            return True
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            return memory_info.rss / (1024 * 1024)
        except ImportError:
            return 0.0
    
    def estimate_total_processing_time(self, file_paths: List[Path]) -> str:
        """Estimate total processing time for multiple files."""
        total_gaps = 0
        total_size = 0
        
        for file_path in file_paths:
            try:
                df = self.load_file(file_path)
                if df is not None:
                    timestamp_col = self.find_timestamp_column(df)
                    if timestamp_col:
                        gap_info = self.detect_gaps(df, timestamp_col)
                        total_gaps += gap_info['gap_count']
                        total_size += len(df)
                    
                    del df
                    
            except Exception:
                continue
        
        # Rough estimation based on data size and gap count
        base_time = total_size / 1000000  # Base time per million rows
        gap_factor = total_gaps / 1000   # Gap complexity factor
        
        estimated_seconds = (base_time + gap_factor) * 3  # More conservative estimate
        
        if estimated_seconds < 60:
            return f"{estimated_seconds:.0f} seconds"
        elif estimated_seconds < 3600:
            minutes = estimated_seconds / 60
            return f"{minutes:.1f} minutes"
        else:
            hours = estimated_seconds / 3600
            return f"{hours:.1f} hours"
    
    def create_backup(self, file_path: Path) -> Path:
        """Create backup of original file."""
        backup_dir = file_path.parent / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
        backup_path = backup_dir / backup_name
        
        # Copy file
        shutil.copy2(file_path, backup_path)
        
        return backup_path
    
    def save_fixed_data(self, df: pd.DataFrame, original_path: Path) -> bool:
        """Save fixed data to file."""
        try:
            print(f"   💾 Saving fixed data to: {original_path}")
            print(f"   📊 Data shape to save: {df.shape}")
            
            if original_path.suffix == '.parquet':
                df.to_parquet(original_path, index=False)
                print(f"   ✅ Saved as Parquet file")
            elif original_path.suffix == '.csv':
                df.to_csv(original_path, index=False)
                print(f"   ✅ Saved as CSV file")
            elif original_path.suffix == '.json':
                df.to_json(original_path, orient='records', indent=2)
                print(f"   ✅ Saved as JSON file")
            else:
                print(f"   ❌ Unsupported file format: {original_path.suffix}")
                return False
            
            # Verify file was saved
            if original_path.exists():
                file_size = original_path.stat().st_size
                print(f"   📁 File saved successfully, size: {file_size / (1024*1024):.1f} MB")
                return True
            else:
                print(f"   ❌ File was not created")
                return False
                
        except Exception as e:
            print(f"   ❌ Error saving file: {e}")
            return False
