# -*- coding: utf-8 -*-
# src/data/gap_fixing/interpolation.py

"""
Gap fixing interpolation algorithms.
Provides various interpolation methods for fixing time series gaps.
All comments are in English.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
from tqdm import tqdm
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)


def _fix_gaps_linear(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using linear interpolation."""
    try:
        # Create a copy to avoid modifying the original
        result_df = df.copy()
        
        # Get numeric columns for interpolation
        numeric_columns = result_df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Apply linear interpolation to numeric columns
        for col in numeric_columns:
            if col in result_df.columns:
                result_df[col] = result_df[col].interpolate(method='linear')
        
        return result_df
    except Exception as e:
        print(f"Linear interpolation failed: {e}")
        return df


def _fix_gaps_cubic(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using cubic interpolation."""
    try:
        # Create a copy to avoid modifying the original
        result_df = df.copy()
        
        # Get numeric columns for interpolation
        numeric_columns = result_df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Apply cubic interpolation to numeric columns
        for col in numeric_columns:
            if col in result_df.columns:
                result_df[col] = result_df[col].interpolate(method='cubic')
        
        return result_df
    except Exception as e:
        print(f"Cubic interpolation failed: {e}")
        return df


def _fix_gaps_seasonal(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using seasonal interpolation."""
    try:
        # Create a copy to avoid modifying the original
        result_df = df.copy()
        
        # Get numeric columns for interpolation
        numeric_columns = result_df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Apply seasonal interpolation to numeric columns
        for col in numeric_columns:
            if col in result_df.columns:
                # Use forward fill for seasonal patterns
                result_df[col] = result_df[col].interpolate(method='ffill', limit=24)  # Assuming hourly data
                # Then use backward fill for remaining gaps
                result_df[col] = result_df[col].interpolate(method='bfill', limit=24)
        
        return result_df
    except Exception as e:
        print(f"Seasonal interpolation failed: {e}")
        return df


def _fix_gaps_forward_fill(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using forward fill."""
    try:
        # Create a copy to avoid modifying the original
        result_df = df.copy()
        
        # Apply forward fill to all columns
        result_df = result_df.fillna(method='ffill')
        
        return result_df
    except Exception as e:
        print(f"Forward fill failed: {e}")
        return df


def _fix_gaps_backward_fill(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using backward fill."""
    try:
        # Create a copy to avoid modifying the original
        result_df = df.copy()
        
        # Apply backward fill to all columns
        result_df = result_df.fillna(method='bfill')
        
        return result_df
    except Exception as e:
        print(f"Backward fill failed: {e}")
        return df


def _fix_gaps_interpolate(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using pandas interpolate with various methods."""
    try:
        # Create a copy to avoid modifying the original
        result_df = df.copy()
        
        # Get numeric columns for interpolation
        numeric_columns = result_df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Apply interpolation to numeric columns
        for col in numeric_columns:
            if col in result_df.columns:
                # Try different interpolation methods
                try:
                    result_df[col] = result_df[col].interpolate(method='polynomial', order=2)
                except:
                    try:
                        result_df[col] = result_df[col].interpolate(method='spline', order=3)
                    except:
                        result_df[col] = result_df[col].interpolate(method='linear')
        
        return result_df
    except Exception as e:
        print(f"Advanced interpolation failed: {e}")
        return df


def _fix_gaps_ml_forecast(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using machine learning forecasting."""
    try:
        # Create a copy to avoid modifying the original
        result_df = df.copy()
        
        # Get numeric columns for forecasting
        numeric_columns = result_df.select_dtypes(include=[np.number]).columns.tolist()
        
        # For now, use a simple approach - in practice you might use more sophisticated ML models
        for col in numeric_columns:
            if col in result_df.columns:
                # Use rolling mean for forecasting
                window_size = min(10, len(result_df) // 4)
                if window_size > 1:
                    rolling_mean = result_df[col].rolling(window=window_size, min_periods=1).mean()
                    result_df[col] = result_df[col].fillna(rolling_mean)
        
        return result_df
    except Exception as e:
        print(f"ML forecasting failed: {e}")
        return df


def _fix_gaps_chunked(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using chunked processing for large datasets."""
    try:
        # Create a copy to avoid modifying the original
        result_df = df.copy()
        
        # Get numeric columns for interpolation
        numeric_columns = result_df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Process in chunks to handle large datasets
        chunk_size = 10000
        total_rows = len(result_df)
        
        if total_rows <= chunk_size:
            # Small dataset, process normally
            return _fix_gaps_linear(result_df, gap_info)
        
        # Process in chunks
        for col in numeric_columns:
            if col in result_df.columns:
                for start_idx in range(0, total_rows, chunk_size):
                    end_idx = min(start_idx + chunk_size, total_rows)
                    
                    # Process chunk
                    chunk = result_df.iloc[start_idx:end_idx][col].copy()
                    chunk_fixed = chunk.interpolate(method='linear')
                    result_df.iloc[start_idx:end_idx, result_df.columns.get_loc(col)] = chunk_fixed
        
        return result_df
    except Exception as e:
        print(f"Chunked processing failed: {e}")
        return df


def apply_interpolation_method(df: pd.DataFrame, method: str, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply a specific interpolation method to fix gaps.
    
    Args:
        df: DataFrame with gaps to fix
        method: Interpolation method to use
        gap_info: Dictionary containing gap information
        
    Returns:
        DataFrame with gaps fixed
    """
    method_map = {
        'linear': _fix_gaps_linear,
        'cubic': _fix_gaps_cubic,
        'seasonal': _fix_gaps_seasonal,
        'forward_fill': _fix_gaps_forward_fill,
        'backward_fill': _fix_gaps_backward_fill,
        'interpolate': _fix_gaps_interpolate,
        'ml_forecast': _fix_gaps_ml_forecast,
        'chunked': _fix_gaps_chunked
    }
    
    if method not in method_map:
        print(f"Unknown interpolation method: {method}, using linear as fallback")
        method = 'linear'
    
    return method_map[method](df, gap_info)
