# File: src/data/gap_fixer_interpolation.py
# -*- coding: utf-8 -*-

"""
Interpolation algorithms for gap fixing.
Handles linear, cubic, and seasonal interpolation methods.
All comments are in English.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
from ..common.logger import print_info, print_warning, print_error, print_success


def _fix_gaps_linear(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using linear interpolation."""
    try:
        time_range = gap_info.get('time_range')
        expected_frequency = gap_info.get('expected_frequency')
        
        if not time_range or not expected_frequency:
            print_warning("Linear interpolation requires time_range and expected_frequency")
            return df
        
        start_time, end_time = time_range
        
        # Create complete time index
        complete_index = pd.date_range(
            start=start_time, 
            end=end_time, 
            freq=expected_frequency
        )
        
        # Reindex with complete time series
        result_df = df.reindex(complete_index)
        
        # Apply linear interpolation
        result_df = result_df.interpolate(method='linear', limit_direction='both')
        
        print_success(f"Linear interpolation completed. DataFrame size: {len(result_df)}")
        return result_df
        
    except Exception as e:
        print_error(f"Linear interpolation failed: {e}")
        return df


def _fix_gaps_cubic(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using cubic interpolation."""
    try:
        time_range = gap_info.get('time_range')
        expected_frequency = gap_info.get('expected_frequency')
        
        if not time_range or not expected_frequency:
            print_warning("Cubic interpolation requires time_range and expected_frequency")
            return df
        
        start_time, end_time = time_range
        
        # Create complete time index
        complete_index = pd.date_range(
            start=start_time, 
            end=end_time, 
            freq=expected_frequency
        )
        
        # Reindex with complete time series
        result_df = df.reindex(complete_index)
        
        # Apply cubic interpolation
        result_df = result_df.interpolate(method='cubic', limit_direction='both')
        
        print_success(f"Cubic interpolation completed. DataFrame size: {len(result_df)}")
        return result_df
        
    except Exception as e:
        print_error(f"Cubic interpolation failed: {e}")
        return df


def _fix_gaps_seasonal(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using seasonal decomposition and interpolation."""
    try:
        time_range = gap_info.get('time_range')
        expected_frequency = gap_info.get('expected_frequency')
        
        if not time_range or not expected_frequency:
            print_warning("Seasonal interpolation requires time_range and expected_frequency")
            return df
        
        start_time, end_time = time_range
        
        # Create complete time index
        complete_index = pd.date_range(
            start=start_time, 
            end=end_time, 
            freq=expected_frequency
        )
        
        # Reindex with complete time series
        result_df = df.reindex(complete_index)
        
        # Apply seasonal interpolation
        result_df = result_df.interpolate(method='time', limit_direction='both')
        
        print_success(f"Seasonal interpolation completed. DataFrame size: {len(result_df)}")
        return result_df
        
    except Exception as e:
        print_error(f"Seasonal interpolation failed: {e}")
        return df


def _fix_gaps_forward_fill(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using forward fill method."""
    try:
        # Apply forward fill
        result_df = df.fillna(method='ffill')
        
        print_success(f"Forward fill completed. DataFrame size: {len(result_df)}")
        return result_df
        
    except Exception as e:
        print_error(f"Forward fill failed: {e}")
        return df


def _fix_gaps_backward_fill(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using backward fill method."""
    try:
        # Apply backward fill
        result_df = df.fillna(method='bfill')
        
        print_success(f"Backward fill completed. DataFrame size: {len(result_df)}")
        return result_df
        
    except Exception as e:
        print_error(f"Backward fill failed: {e}")
        return df


def _fix_gaps_interpolate(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using pandas interpolate method."""
    try:
        # Apply pandas interpolate
        result_df = df.interpolate(method='linear', limit_direction='both')
        
        print_success(f"Pandas interpolate completed. DataFrame size: {len(result_df)}")
        return result_df
        
    except Exception as e:
        print_error(f"Pandas interpolate failed: {e}")
        return df


def _fix_gaps_ml_forecast(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using ML forecasting (placeholder implementation)."""
    try:
        print_info("ML forecasting not yet implemented. Using linear interpolation as fallback.")
        
        # Fallback to linear interpolation
        return _fix_gaps_linear(df, gap_info)
        
    except Exception as e:
        print_error(f"ML forecasting failed: {e}")
        return df


def _fix_gaps_chunked(df: pd.DataFrame, gap_info: Dict[str, Any]) -> pd.DataFrame:
    """Fix gaps using chunked processing for large datasets."""
    try:
        chunk_size = gap_info.get('chunk_size', 10000)
        
        if len(df) <= chunk_size:
            print_info("Dataset small enough, using standard interpolation")
            return _fix_gaps_linear(df, gap_info)
        
        print_info(f"Processing large dataset ({len(df)} rows) in chunks of {chunk_size}")
        
        # Process in chunks
        chunks = []
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i+chunk_size].copy()
            fixed_chunk = _fix_gaps_linear(chunk, gap_info)
            chunks.append(fixed_chunk)
        
        # Combine chunks
        result_df = pd.concat(chunks)
        
        print_success(f"Chunked processing completed. DataFrame size: {len(result_df)}")
        return result_df
        
    except Exception as e:
        print_error(f"Chunked processing failed: {e}")
        return df
