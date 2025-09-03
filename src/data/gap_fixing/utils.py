# -*- coding: utf-8 -*-
# src/../data/gap_fixing/utils.py

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
from tqdm import tqdm


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
        """Convert DatetimeIndex to a regular column for gap analysis, but preserve original structure."""
        if not isinstance(df.index, pd.DatetimeIndex):
            return df
            
        # Create a copy to avoid modifying original
        df_copy = df.copy()
        
        # Reset index to make timestamp a regular column for analysis
        df_copy = df_copy.reset_index()
        
        # Rename the index column if it's unnamed
        if df_copy.columns[0] == 'index':
            df_copy = df_copy.rename(columns={'index': 'Timestamp'})
            
        return df_copy
    
    def detect_gaps(self, df: pd.DataFrame, timestamp_col: str) -> Dict:
        """Detect gaps in time series data with progress bar for large files."""
        total_rows = len(df)
        print(f"   🔍 Starting gap detection for {total_rows:,} rows...")
        
        # Show progress bar for large files
        if total_rows > 100000:  # Show progress for files with more than 100k rows
            print(f"   📊 Large file detected, showing progress bar...")
        
        # Handle DatetimeIndex case
        if timestamp_col == "DATETIME_INDEX":
            # Use the index directly
            timestamps = df.index
        else:
            # Use the specified column
            timestamps = df[timestamp_col]
        
        # Sort timestamps
        timestamps_sorted = timestamps.sort_values()
        
        # Calculate expected frequency
        if len(timestamps_sorted) > 1:
            time_diffs = timestamps_sorted.diff().dropna()
            
            # Handle empty time_diffs
            if time_diffs.empty:
                expected_frequency = pd.Timedelta(minutes=1)
            else:
                # Convert TimedeltaIndex to Series to use mode() method
                if isinstance(time_diffs, pd.TimedeltaIndex):
                    time_diffs_series = pd.Series(time_diffs)
                else:
                    time_diffs_series = time_diffs
                
                # Use median as fallback if mode is not available or empty
                try:
                    if not time_diffs_series.empty and hasattr(time_diffs_series, 'mode'):
                        mode_result = time_diffs_series.mode()
                        expected_frequency = mode_result.iloc[0] if not mode_result.empty else time_diffs_series.median()
                    else:
                        expected_frequency = time_diffs_series.median()
                except (AttributeError, IndexError):
                    # Fallback to median if mode fails
                    try:
                        expected_frequency = time_diffs_series.median()
                    except (AttributeError, IndexError):
                        # Final fallback: use the first non-zero time difference or default
                        non_zero_diffs = time_diffs_series[time_diffs_series > pd.Timedelta(0)]
                        if not non_zero_diffs.empty:
                            expected_frequency = non_zero_diffs.iloc[0]
                        else:
                            expected_frequency = pd.Timedelta(minutes=1)
        else:
            expected_frequency = pd.Timedelta(minutes=1)
        
        # Detect gaps
        gaps = []
        gap_count = 0
        
        for i in range(1, len(timestamps_sorted)):
            current_time = timestamps_sorted.iloc[i]
            previous_time = timestamps_sorted.iloc[i-1]
            
            # Calculate time difference
            time_diff = current_time - previous_time
            
            # Check if this is a gap (more than 1.5x expected frequency)
            if time_diff > expected_frequency * 1.5:
                gap_size = int(time_diff / expected_frequency)
                gaps.append({
                    'start': previous_time,
                    'end': current_time,
                    'size': gap_size,
                    'duration': time_diff
                })
                gap_count += gap_size
        
        # Calculate gap statistics
        gap_sizes = [gap['size'] for gap in gaps]
        avg_gap_size = np.mean(gap_sizes) if gap_sizes else 0
        max_gap_size = max(gap_sizes) if gap_sizes else 0
        
        # Determine data quality
        if gap_count == 0:
            data_quality = 'excellent'
        elif gap_count <= total_rows * 0.01:  # Less than 1% gaps
            data_quality = 'good'
        elif gap_count <= total_rows * 0.05:  # Less than 5% gaps
            data_quality = 'fair'
        else:
            data_quality = 'poor'
        
        # Get time range
        time_range = {
            'start': timestamps_sorted.iloc[0] if len(timestamps_sorted) > 0 else None,
            'end': timestamps_sorted.iloc[-1] if len(timestamps_sorted) > 0 else None
        }
        
        return {
            'has_gaps': gap_count > 0,
            'gap_count': gap_count,
            'gap_details': gaps,
            'gap_size': avg_gap_size,
            'max_gap_size': max_gap_size,
            'expected_frequency': expected_frequency,
            'data_quality': data_quality,
            'time_series_type': 'regular' if gap_count == 0 else 'irregular',
            'time_range': time_range,
            'total_rows': total_rows
        }
    
    def create_backup(self, file_path: Path) -> Path:
        """Create a backup of the original file."""
        try:
            backup_dir = file_path.parent / 'backups'
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
            backup_path = backup_dir / backup_name
            
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"   ⚠️  Warning: Could not create backup: {e}")
            return file_path
    
    def save_fixed_data(self, df: pd.DataFrame, file_path: Path) -> bool:
        """Save the fixed data to the original file."""
        try:
            if file_path.suffix == '.parquet':
                df.to_parquet(file_path, index=False)
            elif file_path.suffix == '.csv':
                df.to_csv(file_path, index=False)
            elif file_path.suffix == '.json':
                df.to_json(file_path, orient='records')
            else:
                print(f"   ❌ Unsupported file format for saving: {file_path.suffix}")
                return False
            
            return True
        except Exception as e:
            print(f"   ❌ Error saving file {file_path}: {e}")
            return False
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except ImportError:
            return 0.0
    
    def check_memory_available(self, limit_mb: float) -> bool:
        """Check if memory usage is below the limit."""
        current_usage = self.get_memory_usage()
        return current_usage < limit_mb
    
    def estimate_total_processing_time(self, file_paths: List[Path]) -> str:
        """Estimate total processing time based on file sizes."""
        total_size_mb = sum(f.stat().st_size / (1024*1024) for f in file_paths)
        
        # Rough estimate: 1 MB = 1 second
        estimated_seconds = int(total_size_mb)
        
        if estimated_seconds < 60:
            return f"{estimated_seconds} seconds"
        elif estimated_seconds < 3600:
            minutes = estimated_seconds // 60
            seconds = estimated_seconds % 60
            return f"{minutes}m {seconds}s"
        else:
            hours = estimated_seconds // 3600
            minutes = (estimated_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
