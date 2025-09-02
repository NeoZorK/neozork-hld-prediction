# File: src/data/gap_fixer_algorithms.py
# -*- coding: utf-8 -*-

"""
Gap fixing algorithms and strategy selection.
Handles algorithm selection and orchestration.
All comments are in English.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple, List
from ..common.logger import print_info, print_warning, print_error, print_success
from .gap_fixer_interpolation import (
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
        print_info(f"Original size: {len(df)}, Result size: {len(result_df)}")
    else:
        print_warning("Gap fixing completed but result is empty")
    
    return result_df


def get_available_algorithms() -> List[str]:
    """Get list of available gap fixing algorithms."""
    strategy = GapFixingStrategy()
    return list(strategy.algorithms.keys())


def validate_algorithm(algorithm_name: str) -> bool:
    """Validate if an algorithm name is supported."""
    strategy = GapFixingStrategy()
    return algorithm_name in strategy.algorithms


def get_algorithm_description(algorithm_name: str) -> str:
    """Get description of a specific algorithm."""
    descriptions = {
        'linear': 'Linear interpolation between known values',
        'cubic': 'Cubic spline interpolation for smooth curves',
        'seasonal': 'Seasonal decomposition and interpolation',
        'forward_fill': 'Fill gaps using previous values',
        'backward_fill': 'Fill gaps using next values',
        'interpolate': 'Pandas built-in interpolation',
        'ml_forecast': 'Machine learning-based forecasting (placeholder)',
        'chunked': 'Process large datasets in chunks'
    }
    
    return descriptions.get(algorithm_name, 'Unknown algorithm')


def estimate_algorithm_performance(algorithm_name: str, gap_info: Dict[str, Any]) -> Dict[str, Any]:
    """Estimate performance characteristics of an algorithm."""
    gap_size = gap_info.get('gap_size', 0)
    data_size = gap_info.get('data_size', 0)
    
    performance = {
        'algorithm': algorithm_name,
        'estimated_time': 'unknown',
        'memory_usage': 'unknown',
        'accuracy': 'unknown'
    }
    
    # Simple performance estimates
    if algorithm_name == 'forward_fill':
        performance.update({
            'estimated_time': 'fast',
            'memory_usage': 'low',
            'accuracy': 'low'
        })
    elif algorithm_name == 'linear':
        performance.update({
            'estimated_time': 'medium',
            'memory_usage': 'low',
            'accuracy': 'medium'
        })
    elif algorithm_name == 'cubic':
        performance.update({
            'estimated_time': 'slow',
            'memory_usage': 'medium',
            'accuracy': 'high'
        })
    elif algorithm_name == 'chunked':
        performance.update({
            'estimated_time': 'medium',
            'memory_usage': 'medium',
            'accuracy': 'medium'
        })
    
    return performance
