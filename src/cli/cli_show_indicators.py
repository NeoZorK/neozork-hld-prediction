# -*- coding: utf-8 -*-
# src/cli/cli_show_indicators.py

"""
Core indicator file handling for CLI show mode.
"""

from colorama import Fore, Style
from .cli_show_common import (
    _initialize_metrics, _parse_indicator_search_params, _search_indicator_files,
    _display_indicator_file_list, show_indicator_help, count_indicator_files
)
from .cli_show_ind_csv import show_csv_indicator_file
from .cli_show_ind_json import show_json_indicator_file
from .cli_show_ind_parquet import show_parquet_indicator_file, handle_multiple_parquet_files


def handle_indicator_show_mode(args):
    """
    Handles the 'show ind' mode logic for indicator files.
    Returns timing and metrics data for execution summary.
    """
    # Initialize timing and metrics tracking
    metrics = _initialize_metrics()
    
    # Set indicator mode flag to ensure proper behavior
    args.indicator_mode = True
    
    # Handle help mode
    if not args.keywords or (len(args.keywords) == 1 and args.keywords[0] == 'help'):
        show_indicator_help()
        indicator_counts = count_indicator_files()
        print("\n=== AVAILABLE INDICATOR FILES ===")
        total_indicator_files = sum(indicator_counts.values())
        if total_indicator_files == 0:
            print("No indicator files found. Calculate indicators first using other modes.")
            return metrics
        print(f"Total indicator files: {total_indicator_files}")
        for format_name, count in indicator_counts.items():
            if count > 0:
                print(f"  - {format_name.upper()}: {count} file(s)")
        print("\nTo view specific indicator files, use: python run_analysis.py show ind [format] [keywords...]")
        return metrics
    
    # Parse search parameters
    format_filter, remaining_keywords = _parse_indicator_search_params(args)
    
    # Search for files
    found_files = _search_indicator_files(format_filter, remaining_keywords)
    
    if not found_files:
        if format_filter:
            print(f"No {format_filter} indicator files found with keywords: {remaining_keywords}")
        else:
            print(f"No indicator files found with keywords: {remaining_keywords}")
        return metrics
    
    print(f"Found {len(found_files)} indicator file(s).")
    
    # Sort files by format and name
    found_files.sort(key=lambda x: (x['format'], x['name']))
    
    # Handle single file regardless of format
    if len(found_files) == 1:
        file_info = found_files[0]
        file_format = file_info['format']
        
        if file_format == 'parquet':
            print("Single parquet indicator file found. Opening chart with specified backend.")
            args.single_file_mode = True
            # Load and display the parquet file with chart
            single_metrics = show_parquet_indicator_file(file_info, args)
        elif file_format == 'csv':
            print(f"Single CSV indicator file found. Displaying content.")
            # For single CSV files, show content with date filtering if applicable
            single_metrics = show_csv_indicator_file(file_info, args)
        elif file_format == 'json':
            print(f"Single JSON indicator file found. Displaying content.")
            # For single JSON files, show content with date filtering if applicable
            single_metrics = show_json_indicator_file(file_info, args)
        
        # Merge metrics
        for key in single_metrics:
            if key in metrics:
                metrics[key] = single_metrics[key]
        return metrics
    
    # Handle multiple parquet files with drawing backend
    handled, metrics = handle_multiple_parquet_files(args, found_files, format_filter, metrics)
    if handled:
        return metrics
    
    # Display file list for multiple files
    return _display_indicator_file_list(found_files, metrics)


def handle_indicator_mode(args):
    """Handle indicator files mode ('show ind')."""
    if not args.keywords or (len(args.keywords) == 1 and args.keywords[0] == 'help'):
        show_indicator_help()
        indicator_counts = count_indicator_files()
        print("\n=== AVAILABLE INDICATOR FILES ===")
        total_indicator_files = sum(indicator_counts.values())
        if total_indicator_files == 0:
            print("No indicator files found. Calculate indicators first using other modes.")
            print("\nTo calculate indicators, use commands like:")
            print("  python run_analysis.py show binance BTCUSDT --rule PV --export-parquet")
            return _initialize_metrics()
        print(f"Total indicator files: {total_indicator_files}")
        for format_name, count in indicator_counts.items():
            if count > 0:
                print(f"  - {format_name.upper()}: {count} file(s)")
        print("\nTo view specific indicator files, use: python run_analysis.py show ind [format] [keywords...]")
        return _initialize_metrics()
    else:
        indicator_metrics = handle_indicator_show_mode(args)
        return indicator_metrics
