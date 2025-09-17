# -*- coding: utf-8 -*-
"""
Gaps Detector for NeoZork Interactive ML Trading Strategy Development.

This module provides fast algorithms for detecting time series gaps in MTF data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta
import time
from src.common.logger import print_info, print_warning, print_error, print_debug


class GapsDetector:
    """
    Fast gaps detector for time series data.
    
    Features:
    - Fast gap detection algorithms
    - Multiple timeframe support
    - Memory efficient processing
    - Detailed gap statistics
    """
    
    def __init__(self):
        """Initialize the gaps detector."""
        self.gap_thresholds = {
            'M1': timedelta(minutes=1),
            'M5': timedelta(minutes=5),
            'M15': timedelta(minutes=15),
            'M30': timedelta(minutes=30),
            'H1': timedelta(hours=1),
            'H4': timedelta(hours=4),
            'D1': timedelta(days=1),
            'W1': timedelta(weeks=1),
            'MN1': timedelta(days=30)
        }
    
    def detect_gaps_in_mtf_data(self, mtf_data: Dict[str, Any], 
                               progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """
        Detect gaps in MTF data structure.
        
        Args:
            mtf_data: MTF data structure containing multiple timeframes
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary containing gap analysis results
        """
        try:
            print_info("🔍 Starting gaps detection in MTF data...")
            
            if not mtf_data:
                return {'status': 'error', 'message': 'No MTF data provided'}
            
            # Debug: Print data structure info
            print_debug(f"MTF data keys: {list(mtf_data.keys()) if isinstance(mtf_data, dict) else 'Not a dict'}")
            
            # Try different possible data structures
            loaded_data = None
            if 'loaded_data' in mtf_data:
                loaded_data = mtf_data['loaded_data']
                print_debug("Using 'loaded_data' key from MTF structure")
            elif isinstance(mtf_data, dict):
                # Check if mtf_data itself contains timeframe data (DataFrames)
                timeframe_keys = []
                for k, v in mtf_data.items():
                    if (isinstance(v, pd.DataFrame) and 
                        hasattr(v, 'index') and 
                        hasattr(v, 'columns') and
                        not k.startswith('_')):
                        timeframe_keys.append(k)
                
                if timeframe_keys:
                    loaded_data = {k: mtf_data[k] for k in timeframe_keys}
                    print_debug(f"Using direct timeframe keys: {timeframe_keys}")
            
            if not loaded_data:
                print_debug("No valid timeframe data found")
                return {'status': 'error', 'message': 'No valid timeframe data found in MTF structure'}
            
            print_debug(f"Found {len(loaded_data)} timeframes: {list(loaded_data.keys())}")
            gaps_results = {}
            total_timeframes = len(loaded_data)
            processed = 0
            
            for timeframe, df in loaded_data.items():
                if progress_callback:
                    progress_callback(processed, total_timeframes, f"Analyzing {timeframe}")
                
                print_debug(f"Analyzing gaps in timeframe: {timeframe}")
                
                # Detect gaps for this timeframe
                gaps_info = self._detect_gaps_in_dataframe(df, timeframe)
                gaps_results[timeframe] = gaps_info
                
                processed += 1
            
            # Calculate overall statistics
            overall_stats = self._calculate_overall_gaps_stats(gaps_results)
            
            result = {
                'status': 'success',
                'timeframe_gaps': gaps_results,
                'overall_stats': overall_stats,
                'total_timeframes': total_timeframes,
                'processed_timeframes': processed
            }
            
            print_info(f"✅ Gaps detection completed for {processed} timeframes")
            return result
            
        except Exception as e:
            print_error(f"Error in gaps detection: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _detect_gaps_in_dataframe(self, df: pd.DataFrame, timeframe: str) -> Dict[str, Any]:
        """
        Detect gaps in a single DataFrame.
        
        Args:
            df: DataFrame to analyze
            timeframe: Timeframe identifier
            
        Returns:
            Dictionary containing gap information
        """
        try:
            if df.empty or not isinstance(df.index, pd.DatetimeIndex):
                return {
                    'status': 'error',
                    'message': 'Invalid DataFrame or non-datetime index',
                    'gaps': [],
                    'gap_count': 0
                }
            
            # Get expected interval for this timeframe
            expected_interval = self.gap_thresholds.get(timeframe, timedelta(hours=1))
            print_debug(f"Expected interval for {timeframe}: {expected_interval}")
            
            # Sort by index to ensure proper order
            df_sorted = df.sort_index()
            print_debug(f"DataFrame shape: {df_sorted.shape}")
            print_debug(f"Index type: {type(df_sorted.index)}")
            print_debug(f"Index range: {df_sorted.index.min()} to {df_sorted.index.max()}")
            
            # Check if index is actually datetime
            if not isinstance(df_sorted.index, pd.DatetimeIndex):
                print_debug("Converting index to datetime")
                df_sorted.index = pd.to_datetime(df_sorted.index)
            
            # Check if data actually matches the expected timeframe
            actual_interval = self._detect_actual_interval(df_sorted.index)
            print_debug(f"Actual interval detected: {actual_interval}")
            
            # Store original expected interval for display
            original_expected_interval = expected_interval
            
            # If actual interval doesn't match expected timeframe, treat as M1 data
            if actual_interval != expected_interval:
                print_debug(f"Data interval ({actual_interval}) doesn't match expected timeframe ({expected_interval})")
                print_debug(f"Treating {timeframe} data as M1 data for gap analysis")
                # Use M1 logic for gap detection
                expected_interval = timedelta(minutes=1)
                timeframe_for_analysis = 'M1'
                is_interval_mismatch = True
            else:
                timeframe_for_analysis = timeframe
                is_interval_mismatch = False
            
            # Find gaps using vectorized operations
            gaps = self._find_gaps_vectorized(df_sorted.index, expected_interval, timeframe_for_analysis)
            
            # Calculate gap statistics
            gap_stats = self._calculate_gap_statistics(gaps, expected_interval)
            
            return {
                'status': 'success',
                'timeframe': timeframe,
                'actual_interval': str(actual_interval),
                'expected_interval': str(original_expected_interval),
                'is_interval_mismatch': is_interval_mismatch,
                'gaps': gaps,
                'gap_count': len(gaps),
                'statistics': gap_stats,
                'data_points': len(df),
                'time_span': {
                    'start': df_sorted.index.min().isoformat() if not df_sorted.empty else None,
                    'end': df_sorted.index.max().isoformat() if not df_sorted.empty else None
                }
            }
            
        except Exception as e:
            print_error(f"Error detecting gaps in {timeframe}: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'gaps': [],
                'gap_count': 0
            }
    
    def _detect_actual_interval(self, index: pd.DatetimeIndex) -> timedelta:
        """
        Detect the actual time interval in the data.
        
        Args:
            index: DatetimeIndex to analyze
            
        Returns:
            Most common time interval in the data
        """
        try:
            if len(index) < 2:
                return timedelta(minutes=1)
            
            # Calculate differences between consecutive timestamps
            diffs = index.to_series().diff().dropna()
            
            # Get the most common interval (mode)
            mode_interval = diffs.mode()
            if len(mode_interval) > 0:
                return mode_interval.iloc[0]
            else:
                # Fallback to median
                return diffs.median()
                
        except Exception as e:
            print_debug(f"Error detecting actual interval: {e}")
            return timedelta(minutes=1)
    
    def _find_gaps_vectorized(self, index: pd.DatetimeIndex,
                             expected_interval: timedelta, timeframe: str = 'M1') -> List[Dict[str, Any]]:
        """
        Find gaps using vectorized operations for speed.
        
        Args:
            index: DatetimeIndex to analyze
            expected_interval: Expected interval between data points
            
        Returns:
            List of gap dictionaries
        """
        try:
            if len(index) < 2:
                return []
            
            print_debug(f"Analyzing {len(index)} data points")
            print_debug(f"Expected interval: {expected_interval}")
            
            # Calculate differences between consecutive timestamps
            diffs = index.to_series().diff().dropna()
            print_debug(f"Time differences - min: {diffs.min()}, max: {diffs.max()}, mean: {diffs.mean()}")
            
            # Find gaps (differences significantly larger than expected)
            # Use 2x expected interval as threshold to account for minor variations
            gap_threshold = expected_interval * 2.0
            print_debug(f"Gap threshold: {gap_threshold}")
            
            # Find gaps that are significantly larger than expected
            gap_indices = diffs[diffs > gap_threshold].index
            print_debug(f"Found {len(gap_indices)} potential gaps")
            
            # Filter out very large gaps that might be market closures (weekends, holidays)
            # For M1 data, gaps larger than 24 hours are likely market closures
            if timeframe == 'M1':
                max_gap_threshold = timedelta(hours=24)
                gap_indices = gap_indices[diffs[gap_indices] <= max_gap_threshold]
                print_debug(f"Filtered gaps (removed >24h): {len(gap_indices)} remaining")
            
            gaps = []
            for gap_start_idx in gap_indices:
                # Find the position in the original index
                gap_start_pos = index.get_loc(gap_start_idx) - 1
                gap_end_pos = index.get_loc(gap_start_idx)
                
                if gap_start_pos >= 0:
                    gap_start = index[gap_start_pos]  # Previous timestamp
                    gap_end = index[gap_end_pos]      # Current timestamp
                    
                    gap_duration = gap_end - gap_start
                    expected_points = int(gap_duration / expected_interval) - 1
                    
                    gaps.append({
                        'start': gap_start.isoformat(),
                        'end': gap_end.isoformat(),
                        'duration': str(gap_duration),
                        'duration_seconds': gap_duration.total_seconds(),
                        'expected_missing_points': max(0, expected_points),
                        'gap_size': gap_duration / expected_interval
                    })
            
            return gaps
            
        except Exception as e:
            print_error(f"Error in vectorized gap finding: {e}")
            return []
    
    def _calculate_gap_statistics(self, gaps: List[Dict[str, Any]], 
                                expected_interval: timedelta) -> Dict[str, Any]:
        """
        Calculate statistics for detected gaps.
        
        Args:
            gaps: List of gap dictionaries
            expected_interval: Expected interval between data points
            
        Returns:
            Dictionary containing gap statistics
        """
        if not gaps:
            return {
                'total_gaps': 0,
                'total_missing_points': 0,
                'average_gap_size': 0,
                'largest_gap_size': 0,
                'smallest_gap_size': 0,
                'total_gap_duration_seconds': 0
            }
        
        gap_sizes = [gap['gap_size'] for gap in gaps]
        missing_points = [gap['expected_missing_points'] for gap in gaps]
        durations = [gap['duration_seconds'] for gap in gaps]
        
        return {
            'total_gaps': len(gaps),
            'total_missing_points': sum(missing_points),
            'average_gap_size': np.mean(gap_sizes),
            'largest_gap_size': max(gap_sizes),
            'smallest_gap_size': min(gap_sizes),
            'total_gap_duration_seconds': sum(durations),
            'gap_size_std': np.std(gap_sizes),
            'missing_points_std': np.std(missing_points)
        }
    
    def _calculate_overall_gaps_stats(self, gaps_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall statistics across all timeframes.
        
        Args:
            gaps_results: Results from all timeframes
            
        Returns:
            Dictionary containing overall statistics
        """
        try:
            total_gaps = 0
            total_missing_points = 0
            total_duration = 0
            timeframes_with_gaps = 0
            
            for timeframe, result in gaps_results.items():
                if result.get('status') == 'success' and 'statistics' in result:
                    stats = result['statistics']
                    total_gaps += stats.get('total_gaps', 0)
                    total_missing_points += stats.get('total_missing_points', 0)
                    total_duration += stats.get('total_gap_duration_seconds', 0)
                    
                    if stats.get('total_gaps', 0) > 0:
                        timeframes_with_gaps += 1
            
            return {
                'total_gaps_across_timeframes': total_gaps,
                'total_missing_points_across_timeframes': total_missing_points,
                'total_gap_duration_seconds': total_duration,
                'timeframes_with_gaps': timeframes_with_gaps,
                'total_timeframes_analyzed': len(gaps_results),
                'gaps_percentage': (timeframes_with_gaps / len(gaps_results) * 100) if gaps_results else 0
            }
            
        except Exception as e:
            print_error(f"Error calculating overall stats: {e}")
            return {
                'total_gaps_across_timeframes': 0,
                'total_missing_points_across_timeframes': 0,
                'total_gap_duration_seconds': 0,
                'timeframes_with_gaps': 0,
                'total_timeframes_analyzed': 0,
                'gaps_percentage': 0
            }
