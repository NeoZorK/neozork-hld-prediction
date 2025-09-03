# -*- coding: utf-8 -*-
# src/../data/gap_fixing/algorithms.py

"""
Gap fixing algorithms and strategy selection.
Handles algorithm selection and orchestration.
All comments are in English.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple, List
from ...common.logger import print_info, print_warning, print_error, print_success
from .interpolation import (
    _fix_gaps_linear, _fix_gaps_cubic, _fix_gaps_seasonal,
    _fix_gaps_forward_fill, _fix_gaps_backward_fill,
    _fix_gaps_interpolate, _fix_gaps_ml_forecast, _fix_gaps_chunked
)


class GapFixingStrategy:
    """Strategy for selecting and applying gap fixing algorithms."""
    
    def __init__(self):
        self.algorithms = {
            'linear': _fix_gaps_linear,
            'cubic': _fix_gaps_cubic,
            'seasonal': _fix_gaps_seasonal,
            'forward_fill': _fix_gaps_forward_fill,
            'backward_fill': _fix_gaps_backward_fill,
            'interpolate': _fix_gaps_interpolate,
            'ml_forecast': _fix_gaps_ml_forecast,
            'chunked': _fix_gaps_chunked
        }
    
    def select_algorithm(self, gap_info: Dict[str, Any]) -> str:
        """Select the best algorithm based on gap characteristics."""
        gap_size = gap_info.get('gap_size', 0)
        data_quality = gap_info.get('data_quality', 'unknown')
        time_series_type = gap_info.get('time_series_type', 'unknown')
        
        # Simple rule-based selection
        if gap_size <= 5:
            return 'forward_fill'  # Small gaps: use forward fill
        elif gap_size <= 20:
            return 'linear'  # Medium gaps: use linear interpolation
        elif gap_size <= 100:
            return 'cubic'  # Large gaps: use cubic interpolation
        elif gap_size > 100:
            return 'chunked'  # Very large gaps: use chunked processing
        else:
            return 'linear'  # Default fallback
    
    def apply_algorithm(self, df: pd.DataFrame, algorithm_name: str, gap_info: Dict[str, Any]) -> pd.DataFrame:
        """Apply the specified algorithm to fix gaps."""
        if algorithm_name not in self.algorithms:
            print_warning(f"Unknown algorithm '{algorithm_name}', using linear as fallback")
            algorithm_name = 'linear'
        
        algorithm_func = self.algorithms[algorithm_name]
        
        try:
            print_info(f"Applying {algorithm_name} algorithm...")
            result_df = algorithm_func(df, gap_info)
            return result_df
        except Exception as e:
            print_error(f"Algorithm {algorithm_name} failed: {e}")
            print_info("Falling back to linear interpolation")
            return _fix_gaps_linear(df, gap_info)
    
    def fix_gaps_in_dataframe(self, df: pd.DataFrame, timestamp_col: str, gap_info: Dict[str, Any], 
                             algorithm: str = 'auto', show_progress: bool = True) -> Tuple[pd.DataFrame, Dict]:
        """
        Fix gaps in DataFrame using the specified or auto-selected algorithm.
        
        Args:
            df: DataFrame with gaps to fix
            timestamp_col: Name of the timestamp column
            gap_info: Dictionary containing gap information and metadata
            algorithm: Specific algorithm to use (if 'auto', auto-select)
            show_progress: Whether to show progress bar
            
        Returns:
            Tuple of (fixed_dataframe, results_dict)
        """
        if df is None or df.empty:
            print_warning("Empty DataFrame provided, nothing to fix")
            return df, {'gaps_fixed': 0, 'algorithm_used': 'none', 'processing_time': 0.0}
        
        # Select algorithm
        if algorithm == 'auto':
            algorithm = self.select_algorithm(gap_info)
            print_info(f"Auto-selected algorithm: {algorithm}")
        
        # Apply algorithm
        start_time = pd.Timestamp.now()
        result_df = self.apply_algorithm(df, algorithm, gap_info)
        end_time = pd.Timestamp.now()
        
        processing_time = (end_time - start_time).total_seconds()
        
        if result_df is not None and not result_df.empty:
            print_success(f"Gap fixing completed using {algorithm} algorithm")
            
            # Calculate gaps fixed
            gaps_fixed = self._calculate_gaps_fixed(df, result_df, timestamp_col)
            
            return result_df, {
                'gaps_fixed': gaps_fixed,
                'algorithm_used': algorithm,
                'processing_time': processing_time,
                'memory_used_mb': self._get_memory_usage()
            }
        else:
            print_error("Gap fixing failed")
            return df, {'gaps_fixed': 0, 'algorithm_used': algorithm, 'processing_time': processing_time}
    
    def _calculate_gaps_fixed(self, original_df: pd.DataFrame, fixed_df: pd.DataFrame, 
                             timestamp_col: str) -> int:
        """Calculate the number of gaps that were fixed."""
        try:
            # This is a simplified calculation - in practice you might want more sophisticated logic
            original_rows = len(original_df)
            fixed_rows = len(fixed_df)
            return max(0, fixed_rows - original_rows)
        except Exception:
            return 0
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except ImportError:
            return 0.0


def fix_gaps_in_dataframe(df: pd.DataFrame, gap_info: Dict[str, Any], 
                         algorithm: Optional[str] = None) -> pd.DataFrame:
    """
    Fix gaps in DataFrame using the specified or auto-selected algorithm.
    
    Args:
        df: DataFrame with gaps to fix
        gap_info: Dictionary containing gap information and metadata
        algorithm: Specific algorithm to use (if None, auto-select)
    
    Returns:
        DataFrame with gaps fixed
    """
    if df is None or df.empty:
        print_warning("Empty DataFrame provided, nothing to fix")
        return df
    
    strategy = GapFixingStrategy()
    
    # Select algorithm
    if algorithm is None:
        algorithm = strategy.select_algorithm(gap_info)
        print_info(f"Auto-selected algorithm: {algorithm}")
    
    # Apply algorithm
    result_df = strategy.apply_algorithm(df, algorithm, gap_info)
    
    if result_df is not None and not result_df.empty:
        print_success(f"Gap fixing completed using {algorithm} algorithm")
    
    return result_df
