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
            'auto': self._auto_fill_gaps,
            'forward_fill': self._forward_fill_gaps,
            'backward_fill': self._backward_fill_gaps,
            'linear_interpolation': self._linear_interpolation_gaps,
            'spline_interpolation': self._spline_interpolation_gaps,
            'mean_fill': self._mean_fill_gaps,
            'median_fill': self._median_fill_gaps
        }
    
    def fix_gaps_in_mtf_data(self, mtf_data: Dict[str, Any], 
                           gaps_info: Dict[str, Any],
                           strategy: str = 'linear_interpolation') -> Dict[str, Any]:
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
            
            if not mtf_data:
                return {'status': 'error', 'message': 'No MTF data provided'}
            
            if strategy not in self.filling_strategies:
                return {'status': 'error', 'message': f'Unknown strategy: {strategy}'}
            
            # Try different possible data structures
            loaded_data = None
            if 'loaded_data' in mtf_data:
                loaded_data = mtf_data['loaded_data']
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
            
            if not loaded_data:
                return {'status': 'error', 'message': 'No valid timeframe data found in MTF structure'}
            fixed_data = {}
            fixing_stats = {}
            
            for timeframe, df in loaded_data.items():
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
                    fixing_stats[timeframe] = {
                        'status': fix_result['status'],
                        **fix_result['stats']
                    }
            
            # Calculate overall fixing statistics
            overall_stats = self._calculate_overall_fixing_stats(fixing_stats)
            
            result = {
                'status': 'success',
                'strategy_used': strategy,
                'fixed_data': fixed_data,
                'fixing_stats': fixing_stats,
                'overall_stats': overall_stats,
                'total_timeframes': len(loaded_data),
                'processed_timeframes': len(loaded_data)
            }
            
            print_info(f"✅ Gaps fixing completed for {len(loaded_data)} timeframes")
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
    
    def _auto_fill_gaps(self, df: pd.DataFrame, gaps_info: Dict[str, Any]) -> pd.DataFrame:
        """
        Automatically choose the best gap filling strategy based on data characteristics.
        
        Args:
            df: DataFrame to fix
            gaps_info: Gap information for this timeframe
            
        Returns:
            Fixed DataFrame
        """
        try:
            # Analyze data characteristics to choose best strategy
            strategy = self._choose_best_strategy(df, gaps_info)
            
            print_debug(f"Auto-selected strategy: {strategy}")
            
            # Apply the chosen strategy
            filling_func = self.filling_strategies[strategy]
            return filling_func(df, gaps_info)
            
        except Exception as e:
            print_error(f"Error in auto gap filling: {e}")
            # Fallback to linear interpolation
            return self._linear_interpolation_gaps(df, gaps_info)
    
    def _choose_best_strategy(self, df: pd.DataFrame, gaps_info: Dict[str, Any]) -> str:
        """
        Choose the best gap filling strategy based on data characteristics.
        
        Args:
            df: DataFrame to analyze
            gaps_info: Gap information
            
        Returns:
            Best strategy name
        """
        try:
            # Get gap information
            gaps = gaps_info.get('gaps', [])
            if not gaps:
                return 'forward_fill'  # No gaps to fill
            
            # Analyze data characteristics
            data_characteristics = self._analyze_data_characteristics(df)
            gap_characteristics = self._analyze_gap_characteristics(gaps)
            
            # Decision tree for strategy selection
            if data_characteristics['is_trending'] and gap_characteristics['avg_gap_size'] < 5:
                # For trending data with small gaps, use linear interpolation
                return 'linear_interpolation'
            elif data_characteristics['is_volatile'] and gap_characteristics['avg_gap_size'] < 3:
                # For volatile data with very small gaps, use spline interpolation
                return 'spline_interpolation'
            elif data_characteristics['has_strong_trend'] and gap_characteristics['avg_gap_size'] < 10:
                # For strong trending data, use forward fill
                return 'forward_fill'
            elif data_characteristics['is_stationary'] and gap_characteristics['avg_gap_size'] < 7:
                # For stationary data, use mean fill
                return 'mean_fill'
            elif gap_characteristics['avg_gap_size'] > 20:
                # For very large gaps, use median fill (more robust)
                return 'median_fill'
            else:
                # Default to linear interpolation
                return 'linear_interpolation'
                
        except Exception as e:
            print_debug(f"Error choosing best strategy: {e}")
            return 'linear_interpolation'  # Safe fallback
    
    def _analyze_data_characteristics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze data characteristics to help choose filling strategy.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with data characteristics
        """
        try:
            if df.empty or len(df) < 3:
                return {
                    'is_trending': False,
                    'is_volatile': False,
                    'has_strong_trend': False,
                    'is_stationary': True
                }
            
            # Calculate price changes
            price_cols = ['Open', 'High', 'Low', 'Close']
            available_cols = [col for col in price_cols if col in df.columns]
            
            if not available_cols:
                return {
                    'is_trending': False,
                    'is_volatile': False,
                    'has_strong_trend': False,
                    'is_stationary': True
                }
            
            # Use Close price if available, otherwise first available
            price_col = 'Close' if 'Close' in df.columns else available_cols[0]
            prices = df[price_col].dropna()
            
            if len(prices) < 3:
                return {
                    'is_trending': False,
                    'is_volatile': False,
                    'has_strong_trend': False,
                    'is_stationary': True
                }
            
            # Calculate price changes
            price_changes = prices.pct_change().dropna()
            
            # Analyze trends
            positive_changes = (price_changes > 0).sum()
            negative_changes = (price_changes < 0).sum()
            total_changes = len(price_changes)
            
            # Calculate volatility (standard deviation of returns)
            volatility = price_changes.std()
            
            # Calculate trend strength
            trend_strength = abs(positive_changes - negative_changes) / total_changes if total_changes > 0 else 0
            
            # Determine characteristics
            is_trending = trend_strength > 0.3  # More than 30% bias in one direction
            is_volatile = volatility > 0.02  # More than 2% standard deviation
            has_strong_trend = trend_strength > 0.6  # More than 60% bias
            is_stationary = trend_strength < 0.2 and volatility < 0.01  # Low trend and volatility
            
            return {
                'is_trending': is_trending,
                'is_volatile': is_volatile,
                'has_strong_trend': has_strong_trend,
                'is_stationary': is_stationary,
                'volatility': volatility,
                'trend_strength': trend_strength
            }
            
        except Exception as e:
            print_debug(f"Error analyzing data characteristics: {e}")
            return {
                'is_trending': False,
                'is_volatile': False,
                'has_strong_trend': False,
                'is_stationary': True
            }
    
    def _analyze_gap_characteristics(self, gaps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze gap characteristics to help choose filling strategy.
        
        Args:
            gaps: List of gap dictionaries
            
        Returns:
            Dictionary with gap characteristics
        """
        try:
            if not gaps:
                return {
                    'avg_gap_size': 0,
                    'max_gap_size': 0,
                    'total_gaps': 0
                }
            
            gap_sizes = [gap.get('gap_size', 0) for gap in gaps]
            
            return {
                'avg_gap_size': sum(gap_sizes) / len(gap_sizes) if gap_sizes else 0,
                'max_gap_size': max(gap_sizes) if gap_sizes else 0,
                'total_gaps': len(gaps),
                'min_gap_size': min(gap_sizes) if gap_sizes else 0
            }
            
        except Exception as e:
            print_debug(f"Error analyzing gap characteristics: {e}")
            return {
                'avg_gap_size': 0,
                'max_gap_size': 0,
                'total_gaps': 0
            }
    
    def _create_complete_time_index(self, df: pd.DataFrame, gaps_info: Dict[str, Any]) -> pd.DatetimeIndex:
        """
        Create time index by filling only the actual gaps, not the entire time range.
        
        Args:
            df: Original DataFrame
            gaps_info: Gap information
            
        Returns:
            DatetimeIndex with gaps filled
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
                elif expected_interval.endswith('M'):
                    minutes = int(expected_interval[:-1])
                    expected_interval = timedelta(minutes=minutes)
                elif ':' in expected_interval:
                    # Handle format like "0:01:00" (hours:minutes:seconds)
                    parts = expected_interval.split(':')
                    if len(parts) == 3:
                        hours = int(parts[0])
                        minutes = int(parts[1])
                        seconds = int(parts[2])
                        expected_interval = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                    else:
                        expected_interval = timedelta(hours=1)
                else:
                    expected_interval = timedelta(hours=1)
            elif isinstance(expected_interval, timedelta):
                # Already a timedelta, use as is
                pass
            else:
                # Fallback to 1 hour
                expected_interval = timedelta(hours=1)
            
            # Get gaps information
            gaps = gaps_info.get('gaps', [])
            if not gaps:
                # No gaps to fill, return original index
                return df.index
            
            # Start with original index
            complete_times = df.index.tolist()
            
            # Fill only the actual gaps
            for i, gap in enumerate(gaps):
                gap_start = pd.to_datetime(gap['start'])
                gap_end = pd.to_datetime(gap['end'])
                
                print_debug(f"Gap {i+1}: {gap_start} to {gap_end}")
                print_debug(f"  Duration: {gap_end - gap_start}")
                print_debug(f"  Expected interval: {expected_interval}")
                
                # Calculate how many points should be in this gap
                gap_duration = gap_end - gap_start
                expected_points_in_gap = int(gap_duration / expected_interval) - 1
                
                print_debug(f"  Expected points in gap: {expected_points_in_gap}")
                
                if expected_points_in_gap > 0:
                    # Generate missing timestamps for this specific gap
                    gap_times = pd.date_range(
                        start=gap_start + expected_interval,
                        end=gap_end - expected_interval,
                        freq=expected_interval
                    )
                    
                    print_debug(f"  Generated {len(gap_times)} timestamps for gap")
                    
                    # Add gap timestamps to the complete list
                    complete_times.extend(gap_times.tolist())
                else:
                    print_debug(f"  Skipping gap - no points expected")
            
            # Sort and remove duplicates
            complete_times = pd.DatetimeIndex(complete_times).sort_values().drop_duplicates()
            
            print_debug(f"Original data points: {len(df)}")
            print_debug(f"Gaps filled: {len(gaps)}")
            print_debug(f"Points added: {len(complete_times) - len(df)}")
            print_debug(f"Final data points: {len(complete_times)}")
            
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
