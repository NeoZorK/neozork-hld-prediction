# File: src/data/data_acquisition_core.py
# -*- coding: utf-8 -*-

"""
Core data acquisition functionality.
Main entry point for data acquisition operations.
All comments are in English.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from ..common.logger import print_info, print_warning, print_error, print_success
from .data_acquisition_processing import (
    _process_demo_data, _process_csv_data, _process_api_data
)


def acquire_data(args) -> Dict[str, Any]:
    """
    Main data acquisition function.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Dictionary containing:
        - ohlcv_df: DataFrame with OHLCV data
        - data_source_label: Human-readable data source description
        - parquet_cache_file: Path to cache file (if applicable)
        - data_metrics: Dictionary with various metrics
        - error_message: Error message if any occurred
    """
    print_info("Starting data acquisition...")
    
    # Initialize data info structure
    data_info = {
        "ohlcv_df": None,
        "data_source_label": None,
        "parquet_cache_file": None,
        "data_metrics": {},
        "error_message": None
    }
    
    try:
        # Determine effective mode
        effective_mode = _determine_effective_mode(args)
        print_info(f"Effective data acquisition mode: {effective_mode}")
        
        # Process based on mode
        if effective_mode == 'demo':
            data_info = _process_demo_data(data_info)
        elif effective_mode == 'csv':
            data_info = _process_csv_data(args, data_info)
        elif effective_mode in ['yfinance', 'polygon', 'binance', 'exrate']:
            data_info = _process_api_data(args, data_info, effective_mode)
        else:
            raise ValueError(f"Unknown or unsupported mode: {effective_mode}")
        
        # Validate final result
        if data_info["ohlcv_df"] is not None and not data_info["ohlcv_df"].empty:
            print_success(f"Data acquisition completed successfully. Got {len(data_info['ohlcv_df'])} rows.")
        else:
            print_warning("Data acquisition completed but returned empty DataFrame.")
            
    except Exception as e:
        error_msg = f"Data acquisition failed: {e}"
        print_error(error_msg)
        data_info["error_message"] = error_msg
        data_info["ohlcv_df"] = pd.DataFrame()
    
    return data_info


def _determine_effective_mode(args) -> str:
    """
    Determine the effective data acquisition mode based on arguments.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        String representing the effective mode
    """
    # Check for demo mode
    if hasattr(args, 'demo') and args.demo:
        return 'demo'
    
    # Check for CSV modes
    if hasattr(args, 'csv_folder') and args.csv_folder:
        return 'csv'
    if hasattr(args, 'csv_file') and args.csv_file:
        return 'csv'
    
    # Check for API modes
    if hasattr(args, 'yfinance') and args.yfinance:
        return 'yfinance'
    if hasattr(args, 'polygon') and args.polygon:
        return 'polygon'
    if hasattr(args, 'binance') and args.binance:
        return 'binance'
    if hasattr(args, 'exrate') and args.exrate:
        return 'exrate'
    
    # Default to yfinance if no specific mode is set
    return 'yfinance'
