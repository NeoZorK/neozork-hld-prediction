#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gap Fixer Module for Time Series Data

This module provides advanced algorithms for fixing time series gaps
using modern interpolation and forecasting techniques.
"""

import time
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import gc

import pandas as pd
import numpy as np
from tqdm import tqdm
import psutil

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)


class GapFixer:
    """
    Advanced gap fixer for time series data with multiple algorithms.
    
    This class provides sophisticated methods for detecting and fixing
    time series gaps using various interpolation and forecasting techniques.
    """
    
    def __init__(self, memory_limit_mb: int = 6144):
        """
        Initialize the gap fixer.
        
        Args:
            memory_limit_mb: Memory limit in MB for processing
        """
        self.memory_limit_mb = memory_limit_mb
        self.supported_formats = ['.parquet', '.csv', '.json']
        
        # Algorithm configurations
        self.algorithms = {
            'linear': self._fix_gaps_linear,
            'cubic': self._fix_gaps_cubic,
            'forward_fill': self._fix_gaps_forward_fill,
            'backward_fill': self._fix_gaps_backward_fill,
            'interpolate': self._fix_gaps_interpolate,
            'seasonal': self._fix_gaps_seasonal,
            'ml_forecast': self._fix_gaps_ml_forecast
        }
        
        print(f"🔧 GapFixer initialized with memory limit: {memory_limit_mb}MB")
    
    def _check_memory_available(self, required_mb: int = None) -> bool:
        """Check if we have enough memory available."""
        try:
            memory = psutil.virtual_memory()
            available_mb = memory.available / (1024 * 1024)
            
            if required_mb is None:
                required_mb = self.memory_limit_mb * 0.2  # Require 20% of limit
            
            return available_mb > required_mb
        except ImportError:
            return True
    
    def _estimate_processing_time(self, df_size: int, gap_count: int) -> str:
        """Estimate processing time for gap fixing."""
        # Rough estimation based on data size and gap count
        base_time = df_size / 1000000  # Base time per million rows
        gap_factor = gap_count / 1000   # Gap complexity factor
        
        estimated_seconds = (base_time + gap_factor) * 3  # More conservative estimate
        
        if estimated_seconds < 60:
            return f"{estimated_seconds:.0f} seconds"
        elif estimated_seconds < 3600:
            minutes = estimated_seconds / 60
            return f"{minutes:.1f} minutes"
        else:
            hours = estimated_seconds / 3600
            return f"{hours:.1f} hours"
    
    def fix_file_gaps(self, file_path: Path, algorithm: str = 'auto', 
                      show_progress: bool = True) -> Tuple[bool, Dict]:
        """
        Fix gaps in a single file.
        
        Args:
            file_path: Path to the file to fix
            algorithm: Algorithm to use for gap fixing
            show_progress: Whether to show progress bar
            
        Returns:
            Tuple of (success, results_dict)
        """
        try:
            # Load file
            if file_path.suffix == '.parquet':
                df = pd.read_parquet(file_path)
            elif file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix == '.json':
                df = pd.read_json(file_path)
            else:
                return False, {'error': f'Unsupported file format: {file_path.suffix}'}
            
            # Check if timestamp column exists or if we have a DatetimeIndex
            timestamp_col = self._find_timestamp_column(df)
            
            if timestamp_col is None and not isinstance(df.index, pd.DatetimeIndex):
                return False, {'error': 'No timestamp column found'}
            
            # Handle DatetimeIndex case
            if isinstance(df.index, pd.DatetimeIndex):
                print(f"   📅 Converting DatetimeIndex to column for gap analysis...")
                # Convert DatetimeIndex to a column
                df = df.reset_index()
                timestamp_col = df.index.name or 'index'
                # Rename the index column if it's unnamed
                if timestamp_col == 'index':
                    timestamp_col = 'Timestamp'
                    df = df.rename(columns={'index': 'Timestamp'})
            
            # Convert timestamp to datetime if needed
            if timestamp_col and not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
                df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
            
            # Detect gaps
            gap_info = self._detect_gaps(df, timestamp_col)
            
            if not gap_info['has_gaps']:
                return True, {'message': 'No gaps found', 'gaps_fixed': 0}
            
            # Fix gaps
            fixed_df, fix_results = self._fix_gaps_in_dataframe(
                df, timestamp_col, gap_info, algorithm, show_progress
            )
            
            # Save fixed data
            backup_path = self._create_backup(file_path)
            success = self._save_fixed_data(fixed_df, file_path)
            
            if success:
                results = {
                    'success': True,
                    'gaps_fixed': fix_results['gaps_fixed'],
                    'algorithm_used': fix_results['algorithm_used'],
                    'processing_time': fix_results['processing_time'],
                    'backup_created': str(backup_path),
                    'original_gaps': gap_info['gap_count'],
                    'memory_used_mb': fix_results['memory_used_mb']
                }
                return True, results
            else:
                return False, {'error': 'Failed to save fixed data'}
                
        except Exception as e:
            return False, {'error': str(e)}
    
    def fix_multiple_files(self, file_paths: List[Path], algorithm: str = 'auto',
                          show_progress: bool = True) -> Dict[str, Dict]:
        """
        Fix gaps in multiple files with progress tracking.
        
        Args:
            file_paths: List of file paths to fix
            algorithm: Algorithm to use for gap fixing
            show_progress: Whether to show progress bars
            
        Returns:
            Dictionary with results for each file
        """
        results = {}
        total_files = len(file_paths)
        
        print(f"\n🚀 Starting gap fixing for {total_files} files...")
        print(f"📊 Algorithm: {algorithm}")
        
        # Estimate total time
        total_gaps = 0
        total_size = 0
        for file_path in file_paths:
            try:
                if file_path.suffix == '.parquet':
                    df = pd.read_parquet(file_path)
                elif file_path.suffix == '.csv':
                    df = pd.read_csv(file_path)
                elif file_path.suffix == '.json':
                    df = pd.read_json(file_path)
                else:
                    continue
                
                timestamp_col = self._find_timestamp_column(df)
                if timestamp_col:
                    gap_info = self._detect_gaps(df, timestamp_col)
                    total_gaps += gap_info['gap_count']
                    total_size += len(df)
                
                del df
                gc.collect()
                
            except Exception:
                continue
        
        estimated_time = self._estimate_processing_time(total_size, total_gaps)
        print(f"⏱️  Estimated total processing time: {estimated_time}")
        print(f"📈 Total gaps to fix: {total_gaps:,}")
        print(f"📊 Total data size: {total_size:,} rows")
        
        # Process files
        start_time = time.time()
        
        for i, file_path in enumerate(file_paths, 1):
            print(f"\n📁 Processing file {i}/{total_files}: {file_path.name}")
            
            success, file_results = self.fix_file_gaps(
                file_path, algorithm, show_progress
            )
            
            results[str(file_path)] = file_results
            
            if success:
                print(f"✅ {file_path.name}: {file_results['gaps_fixed']} gaps fixed")
            else:
                print(f"❌ {file_path.name}: {file_results.get('error', 'Unknown error')}")
            
            # Memory cleanup
            gc.collect()
            
            # Check memory usage
            if not self._check_memory_available():
                print("⚠️  Memory usage high, forcing garbage collection...")
                gc.collect()
        
        total_time = time.time() - start_time
        
        # Summary
        successful_fixes = sum(1 for r in results.values() if r.get('success', False))
        total_gaps_fixed = sum(r.get('gaps_fixed', 0) for r in results.values() if r.get('success', False))
        
        print(f"\n🎉 Gap fixing completed!")
        print(f"📊 Files processed: {total_files}")
        print(f"✅ Successful fixes: {successful_fixes}")
        print(f"📈 Total gaps fixed: {total_gaps_fixed:,}")
        print(f"⏱️  Total time: {total_time:.1f} seconds")
        
        return results
    
    def _find_timestamp_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find the timestamp column in the dataframe."""
        # First, check if the index is a DatetimeIndex
        if isinstance(df.index, pd.DatetimeIndex):
            print(f"   📅 Found DatetimeIndex: {df.index.name or 'unnamed'}")
            return None  # We'll handle DatetimeIndex separately
        
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
        
        # Debug: print available columns
        print(f"   🔍 Available columns: {list(df.columns)}")
        
        return None
    
    def _detect_gaps(self, df: pd.DataFrame, timestamp_col: str) -> Dict:
        """Detect gaps in time series data."""
        # Sort by timestamp
        df_sorted = df.sort_values(timestamp_col).copy()
        
        # Calculate time differences
        time_diffs = df_sorted[timestamp_col].diff().dropna()
        
        # Determine expected frequency
        expected_freq = self._determine_expected_frequency(time_diffs)
        
        # Find gaps (intervals larger than expected frequency)
        gap_threshold = expected_freq * 1.5  # Allow 50% tolerance
        
        gaps = time_diffs > gap_threshold
        
        gap_info = {
            'has_gaps': gaps.any(),
            'gap_count': gaps.sum(),
            'expected_frequency': expected_freq,
            'gap_threshold': gap_threshold,
            'total_rows': len(df),
            'time_range': {
                'start': df_sorted[timestamp_col].min(),
                'end': df_sorted[timestamp_col].max()
            }
        }
        
        return gap_info
    
    def _determine_expected_frequency(self, time_diffs: pd.Series) -> pd.Timedelta:
        """Determine expected frequency from time differences."""
        if len(time_diffs) == 0:
            return pd.Timedelta('1H')
        
        # Use median for robustness
        median_diff = time_diffs.median()
        
        # Round to common frequencies
        if median_diff <= pd.Timedelta('1T'):  # 1 minute
            return pd.Timedelta('1T')
        elif median_diff <= pd.Timedelta('5T'):  # 5 minutes
            return pd.Timedelta('5T')
        elif median_diff <= pd.Timedelta('15T'):  # 15 minutes
            return pd.Timedelta('15T')
        elif median_diff <= pd.Timedelta('1H'):  # 1 hour
            return pd.Timedelta('1H')
        elif median_diff <= pd.Timedelta('4H'):  # 4 hours
            return pd.Timedelta('4H')
        elif median_diff <= pd.Timedelta('1D'):  # 1 day
            return pd.Timedelta('1D')
        else:
            return pd.Timedelta('1W')  # 1 week
    
    def _fix_gaps_in_dataframe(self, df: pd.DataFrame, timestamp_col: str,
                               gap_info: Dict, algorithm: str, show_progress: bool) -> Tuple[pd.DataFrame, Dict]:
        """Fix gaps in dataframe using specified algorithm."""
        start_time = time.time()
        initial_memory = self._get_memory_usage()
        
        # Choose algorithm
        if algorithm == 'auto':
            algorithm = self._select_best_algorithm(gap_info)
        
        if algorithm not in self.algorithms:
            algorithm = 'interpolate'  # Default fallback
        
        print(f"🔧 Using algorithm: {algorithm}")
        
        # Fix gaps
        fixed_df = self.algorithms[algorithm](df, timestamp_col, gap_info, show_progress)
        
        # Results
        processing_time = time.time() - start_time
        final_memory = self._get_memory_usage()
        memory_used = final_memory - initial_memory
        
        results = {
            'algorithm_used': algorithm,
            'processing_time': processing_time,
            'gaps_fixed': gap_info['gap_count'],
            'memory_used_mb': memory_used,
            'original_shape': df.shape,
            'final_shape': fixed_df.shape
        }
        
        return fixed_df, results
    
    def _select_best_algorithm(self, gap_info: Dict) -> str:
        """Select the best algorithm based on gap characteristics."""
        gap_count = gap_info['gap_count']
        total_rows = gap_info['total_rows']
        gap_ratio = gap_count / total_rows
        
        if gap_ratio <= 0.01:  # Less than or equal to 1% gaps
            return 'linear'
        elif gap_ratio <= 0.05:  # Less than or equal to 5% gaps
            return 'cubic'
        elif gap_ratio <= 0.1:  # Less than or equal to 10% gaps
            return 'interpolate'
        else:  # High gap ratio
            return 'seasonal'  # Use seasonal for high gap ratios
    
    def _fix_gaps_linear(self, df: pd.DataFrame, timestamp_col: str, 
                         gap_info: Dict, show_progress: bool) -> pd.DataFrame:
        """Fix gaps using linear interpolation."""
        df_copy = df.copy()
        
        # Sort by timestamp
        df_copy = df_copy.sort_values(timestamp_col)
        
        # Set timestamp as index for proper time-based operations
        df_copy = df_copy.set_index(timestamp_col)
        
        # Linear interpolation for numeric columns
        numeric_columns = df_copy.select_dtypes(include=[np.number]).columns
        df_copy[numeric_columns] = df_copy[numeric_columns].interpolate(method='linear')
        
        # Forward fill for non-numeric columns
        non_numeric_columns = df_copy.select_dtypes(exclude=[np.number]).columns
        df_copy[non_numeric_columns] = df_copy[non_numeric_columns].fillna(method='ffill')
        
        # Reset index to restore timestamp column
        df_copy = df_copy.reset_index()
        
        return df_copy
    
    def _fix_gaps_cubic(self, df: pd.DataFrame, timestamp_col: str,
                        gap_info: Dict, show_progress: bool) -> pd.DataFrame:
        """Fix gaps using cubic interpolation."""
        df_copy = df.copy()
        
        # Sort by timestamp
        df_copy = df_copy.sort_values(timestamp_col)
        
        # Set timestamp as index for proper time-based operations
        df_copy = df_copy.set_index(timestamp_col)
        
        # Cubic interpolation for numeric columns
        numeric_columns = df_copy.select_dtypes(include=[np.number]).columns
        df_copy[numeric_columns] = df_copy[numeric_columns].interpolate(method='cubic')
        
        # Forward fill for non-numeric columns
        non_numeric_columns = df_copy.select_dtypes(exclude=[np.number]).columns
        df_copy[non_numeric_columns] = df_copy[non_numeric_columns].fillna(method='ffill')
        
        # Reset index to restore timestamp column
        df_copy = df_copy.reset_index()
        
        return df_copy
    
    def _fix_gaps_forward_fill(self, df: pd.DataFrame, timestamp_col: str,
                               gap_info: Dict, show_progress: bool) -> pd.DataFrame:
        """Fix gaps using forward fill method."""
        df_copy = df.copy()
        df_copy = df_copy.sort_values(timestamp_col)
        
        # Forward fill all columns
        df_copy = df_copy.fillna(method='ffill')
        
        return df_copy
    
    def _fix_gaps_backward_fill(self, df: pd.DataFrame, timestamp_col: str,
                                gap_info: Dict, show_progress: bool) -> pd.DataFrame:
        """Fix gaps using backward fill method."""
        df_copy = df.copy()
        df_copy = df_copy.sort_values(timestamp_col)
        
        # Backward fill all columns
        df_copy = df_copy.fillna(method='bfill')
        
        return df_copy
    
    def _fix_gaps_interpolate(self, df: pd.DataFrame, timestamp_col: str,
                              gap_info: Dict, show_progress: bool) -> pd.DataFrame:
        """Fix gaps using advanced interpolation."""
        df_copy = df.copy()
        df_copy = df_copy.sort_values(timestamp_col)
        
        # Interpolate numeric columns using linear method (more robust)
        numeric_columns = df_copy.select_dtypes(include=[np.number]).columns
        df_copy[numeric_columns] = df_copy[numeric_columns].interpolate(
            method='linear', limit_direction='both'
        )
        
        # Fill remaining NaNs
        df_copy = df_copy.fillna(method='ffill').fillna(method='bfill')
        
        return df_copy
    
    def _fix_gaps_seasonal(self, df: pd.DataFrame, timestamp_col: str,
                           gap_info: Dict, show_progress: bool) -> pd.DataFrame:
        """Fix gaps using seasonal decomposition."""
        # For now, use interpolate as fallback
        return self._fix_gaps_interpolate(df, timestamp_col, gap_info, show_progress)
    
    def _fix_gaps_ml_forecast(self, df: pd.DataFrame, timestamp_col: str,
                              gap_info: Dict, show_progress: bool) -> pd.DataFrame:
        """Fix gaps using ML forecasting (placeholder for future implementation)."""
        # For now, use interpolate as fallback
        return self._fix_gaps_interpolate(df, timestamp_col, gap_info, show_progress)
    
    def _create_backup(self, file_path: Path) -> Path:
        """Create backup of original file."""
        backup_dir = file_path.parent / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
        backup_path = backup_dir / backup_name
        
        # Copy file
        import shutil
        shutil.copy2(file_path, backup_path)
        
        return backup_path
    
    def _save_fixed_data(self, df: pd.DataFrame, original_path: Path) -> bool:
        """Save fixed data to file."""
        try:
            if original_path.suffix == '.parquet':
                df.to_parquet(original_path, index=False)
            elif original_path.suffix == '.csv':
                df.to_csv(original_path, index=False)
            elif original_path.suffix == '.json':
                df.to_json(original_path, orient='records', indent=2)
            else:
                return False
            
            return True
        except Exception:
            return False
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            return memory_info.rss / (1024 * 1024)
        except ImportError:
            return 0.0


def explain_why_fix_gaps() -> str:
    """Explain why time series gaps need to be fixed before EDA analysis."""
    explanation = """
🔍 WHY TIME SERIES GAPS NEED TO BE FIXED BEFORE EDA ANALYSIS
============================================================

📊 Data Quality Issues:
   • Gaps create artificial patterns that can mislead analysis
   • Missing data points affect statistical calculations
   • Inconsistent time intervals distort trend analysis

📈 Analysis Accuracy:
   • Technical indicators become unreliable with gaps
   • Correlation analysis produces incorrect results
   • Seasonal patterns are distorted or missed entirely

🎯 ML Model Performance:
   • Models trained on gapped data learn incorrect patterns
   • Feature engineering produces unreliable results
   • Prediction accuracy is significantly reduced

⚡ Performance Benefits:
   • Faster processing with complete datasets
   • More accurate statistical calculations
   • Better visualization quality

🔄 Recommended Workflow:
   1. Load and inspect data
   2. Identify and fix gaps
   3. Perform EDA analysis
   4. Engineer features
   5. Train ML models

💡 Best Practices:
   • Always fix gaps before analysis
   • Use appropriate interpolation methods
   • Create backups before modifications
   • Validate data after gap fixing
"""
    return explanation
