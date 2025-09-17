# -*- coding: utf-8 -*-
"""
Gaps Fixer for NeoZork Interactive ML Trading Strategy Development.

This module provides algorithms for fixing time series gaps in MTF data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import time
from src.common.logger import print_info, print_warning, print_error, print_debug


class GapsFixer:
    """
    Gaps fixer for time series data.
    
    Features:
    - Multiple gap filling strategies
    - Interpolation methods
    - Forward/backward filling
    - Linear interpolation
    - Spline interpolation
    - Custom gap filling logic
    """
    
    def __init__(self):
        """Initialize the gaps fixer."""
        self.filling_strategies = {
            'forward_fill': self._forward_fill_gaps,
            'backward_fill': self._backward_fill_gaps,
            'linear_interpolation': self._linear_interpolation_gaps,
            'spline_interpolation': self._spline_interpolation_gaps,
            'mean_fill': self._mean_fill_gaps,
            'median_fill': self._median_fill_gaps
        }
    
    def fix_gaps_in_mtf_data(self, mtf_data: Dict[str, Any], 
                           gaps_info: Dict[str, Any],
                           strategy: str = 'linear_interpolation',
                           progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """
        Fix gaps in MTF data structure.
        
        Args:
            mtf_data: MTF data structure containing multiple timeframes
            gaps_info: Gap information from GapsDetector
            strategy: Gap filling strategy to use
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary containing fixed data and statistics
        """
        try:
            print_info(f"🔧 Starting gaps fixing with strategy: {strategy}")
            
            if not mtf_data or 'loaded_data' not in mtf_data:
                return {'status': 'error', 'message': 'No MTF data provided'}
            
            if strategy not in self.filling_strategies:
                return {'status': 'error', 'message': f'Unknown strategy: {strategy}'}
            
            loaded_data = mtf_data['loaded_data']
            fixed_data = {}
            fixing_stats = {}
            total_timeframes = len(loaded_data)
            processed = 0
            
            for timeframe, df in loaded_data.items():
                if progress_callback:
                    progress_callback(processed, total_timeframes, f"Fixing gaps in {timeframe}")
                
                print_debug(f"Fixing gaps in timeframe: {timeframe}")
                
                # Get gaps for this timeframe
                timeframe_gaps = gaps_info.get('timeframe_gaps', {}).get(timeframe, {})
                
                if timeframe_gaps.get('gap_count', 0) == 0:
                    # No gaps to fix
                    fixed_data[timeframe] = df.copy()
                    fixing_stats[timeframe] = {
                        'status': 'no_gaps',
                        'gaps_fixed': 0,
                        'points_added': 0
                    }
                else:
                    # Fix gaps
                    fix_result = self._fix_gaps_in_dataframe(
                        df, timeframe_gaps, strategy
                    )
                    fixed_data[timeframe] = fix_result['fixed_data']
                    fixing_stats[timeframe] = fix_result['stats']
                
                processed += 1
            
            # Calculate overall fixing statistics
            overall_stats = self._calculate_overall_fixing_stats(fixing_stats)
            
            result = {
                'status': 'success',
                'strategy_used': strategy,
                'fixed_data': fixed_data,
                'fixing_stats': fixing_stats,
                'overall_stats': overall_stats,
                'total_timeframes': total_timeframes,
                'processed_timeframes': processed
            }
            
            print_info(f"✅ Gaps fixing completed for {processed} timeframes")
            return result
            
        except Exception as e:
            print_error(f"Error in gaps fixing: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _fix_gaps_in_dataframe(self, df: pd.DataFrame, 
                             gaps_info: Dict[str, Any], 
                             strategy: str) -> Dict[str, Any]:
        """
        Fix gaps in a single DataFrame.
        
        Args:
            df: DataFrame to fix
            gaps_info: Gap information for this timeframe
            strategy: Gap filling strategy
            
        Returns:
            Dictionary containing fixed data and statistics
        """
        try:
            if df.empty or not isinstance(df.index, pd.DatetimeIndex):
                return {
                    'status': 'error',
                    'message': 'Invalid DataFrame or non-datetime index',
                    'fixed_data': df,
                    'stats': {'gaps_fixed': 0, 'points_added': 0}
                }
            
            gaps = gaps_info.get('gaps', [])
            if not gaps:
                return {
                    'status': 'no_gaps',
                    'fixed_data': df.copy(),
                    'stats': {'gaps_fixed': 0, 'points_added': 0}
                }
            
            # Sort by index
            df_sorted = df.sort_index()
            original_length = len(df_sorted)
            
            # Apply gap filling strategy
            filling_func = self.filling_strategies[strategy]
            fixed_df = filling_func(df_sorted, gaps_info)
            
            points_added = len(fixed_df) - original_length
            
            return {
                'status': 'success',
                'fixed_data': fixed_df,
                'stats': {
                    'gaps_fixed': len(gaps),
                    'points_added': points_added,
                    'original_length': original_length,
                    'final_length': len(fixed_df)
                }
            }
            
        except Exception as e:
            print_error(f"Error fixing gaps in DataFrame: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'fixed_data': df,
                'stats': {'gaps_fixed': 0, 'points_added': 0}
            }
    
    def _forward_fill_gaps(self, df: pd.DataFrame, gaps_info: Dict[str, Any]) -> pd.DataFrame:
        """Forward fill gaps in DataFrame."""
        try:
            # Create complete time index
            complete_index = self._create_complete_time_index(df, gaps_info)
            
            # Reindex and forward fill
            fixed_df = df.reindex(complete_index, method='ffill')
            
            return fixed_df
            
        except Exception as e:
            print_error(f"Error in forward fill: {e}")
            return df
    
    def _backward_fill_gaps(self, df: pd.DataFrame, gaps_info: Dict[str, Any]) -> pd.DataFrame:
        """Backward fill gaps in DataFrame."""
        try:
            # Create complete time index
            complete_index = self._create_complete_time_index(df, gaps_info)
            
            # Reindex and backward fill
            fixed_df = df.reindex(complete_index, method='bfill')
            
            return fixed_df
            
        except Exception as e:
            print_error(f"Error in backward fill: {e}")
            return df
    
    def _linear_interpolation_gaps(self, df: pd.DataFrame, gaps_info: Dict[str, Any]) -> pd.DataFrame:
        """Linear interpolation for gaps in DataFrame."""
        try:
            # Create complete time index
            complete_index = self._create_complete_time_index(df, gaps_info)
            
            # Reindex and interpolate
            fixed_df = df.reindex(complete_index)
            fixed_df = fixed_df.interpolate(method='linear')
            
            return fixed_df
            
        except Exception as e:
            print_error(f"Error in linear interpolation: {e}")
            return df
    
    def _spline_interpolation_gaps(self, df: pd.DataFrame, gaps_info: Dict[str, Any]) -> pd.DataFrame:
        """Spline interpolation for gaps in DataFrame."""
        try:
            # Create complete time index
            complete_index = self._create_complete_time_index(df, gaps_info)
            
            # Reindex and interpolate
            fixed_df = df.reindex(complete_index)
            fixed_df = fixed_df.interpolate(method='spline', order=3)
            
            return fixed_df
            
        except Exception as e:
            print_error(f"Error in spline interpolation: {e}")
            return df
    
    def _mean_fill_gaps(self, df: pd.DataFrame, gaps_info: Dict[str, Any]) -> pd.DataFrame:
        """Fill gaps with mean values."""
        try:
            # Create complete time index
            complete_index = self._create_complete_time_index(df, gaps_info)
            
            # Reindex and fill with mean
            fixed_df = df.reindex(complete_index)
            for column in fixed_df.columns:
                if fixed_df[column].dtype in ['float64', 'int64']:
                    mean_value = df[column].mean()
                    fixed_df[column] = fixed_df[column].fillna(mean_value)
            
            return fixed_df
            
        except Exception as e:
            print_error(f"Error in mean fill: {e}")
            return df
    
    def _median_fill_gaps(self, df: pd.DataFrame, gaps_info: Dict[str, Any]) -> pd.DataFrame:
        """Fill gaps with median values."""
        try:
            # Create complete time index
            complete_index = self._create_complete_time_index(df, gaps_info)
            
            # Reindex and fill with median
            fixed_df = df.reindex(complete_index)
            for column in fixed_df.columns:
                if fixed_df[column].dtype in ['float64', 'int64']:
                    median_value = df[column].median()
                    fixed_df[column] = fixed_df[column].fillna(median_value)
            
            return fixed_df
            
        except Exception as e:
            print_error(f"Error in median fill: {e}")
            return df
    
    def _create_complete_time_index(self, df: pd.DataFrame, gaps_info: Dict[str, Any]) -> pd.DatetimeIndex:
        """
        Create complete time index by filling gaps.
        
        Args:
            df: Original DataFrame
            gaps_info: Gap information
            
        Returns:
            Complete DatetimeIndex
        """
        try:
            if df.empty:
                return pd.DatetimeIndex([])
            
            # Get expected interval
            expected_interval = gaps_info.get('expected_interval', '1H')
            if isinstance(expected_interval, str):
                # Convert string to timedelta
                if expected_interval.endswith('H'):
                    hours = int(expected_interval[:-1])
                    expected_interval = timedelta(hours=hours)
                elif expected_interval.endswith('D'):
                    days = int(expected_interval[:-1])
                    expected_interval = timedelta(days=days)
                else:
                    expected_interval = timedelta(hours=1)
            
            # Create complete range
            start_time = df.index.min()
            end_time = df.index.max()
            
            # Generate complete time range
            complete_times = pd.date_range(
                start=start_time,
                end=end_time,
                freq=expected_interval
            )
            
            return complete_times
            
        except Exception as e:
            print_error(f"Error creating complete time index: {e}")
            return df.index
    
    def _calculate_overall_fixing_stats(self, fixing_stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall fixing statistics.
        
        Args:
            fixing_stats: Statistics from all timeframes
            
        Returns:
            Dictionary containing overall statistics
        """
        try:
            total_gaps_fixed = 0
            total_points_added = 0
            timeframes_fixed = 0
            
            for timeframe, stats in fixing_stats.items():
                if stats.get('status') == 'success':
                    total_gaps_fixed += stats.get('gaps_fixed', 0)
                    total_points_added += stats.get('points_added', 0)
                    timeframes_fixed += 1
            
            return {
                'total_gaps_fixed': total_gaps_fixed,
                'total_points_added': total_points_added,
                'timeframes_fixed': timeframes_fixed,
                'total_timeframes': len(fixing_stats),
                'fixing_success_rate': (timeframes_fixed / len(fixing_stats) * 100) if fixing_stats else 0
            }
            
        except Exception as e:
            print_error(f"Error calculating overall fixing stats: {e}")
            return {
                'total_gaps_fixed': 0,
                'total_points_added': 0,
                'timeframes_fixed': 0,
                'total_timeframes': 0,
                'fixing_success_rate': 0
            }
