# -*- coding: utf-8 -*-
# src/cli/cli_show_ind_csv.py

"""
CSV indicator file handling for CLI show mode.
"""

import pandas as pd
import time
from colorama import Fore, Style
from .cli_show_common import _initialize_metrics, _extract_datetime_filter_args, _filter_dataframe_by_date


def show_csv_indicator_file(file_info, args):
    """
    Shows a single CSV indicator file with date filtering support.
    Returns timing and metrics data.
    """
    # Initialize timing and metrics tracking
    metrics = _initialize_metrics()
    
    file_path = file_info['path']
    
    # Update file size metrics
    metrics["data_size_mb"] = file_info['size_mb']
    metrics["data_size_bytes"] = int(file_info['size_mb'] * 1024 * 1024)
    
    try:
        # Track data loading time
        load_start_time = time.time()
        
        # Extract date filtering parameters
        start, end = _extract_datetime_filter_args(args)
        
        df = pd.read_csv(file_path)
        load_end_time = time.time()
        
        # Apply date filtering if requested
        if start or end:
            print(f"Applying date filtering to CSV data...")
            original_len = len(df)
            df = _filter_dataframe_by_date(df, start, end)
            filtered_len = len(df)
            print(f"After date filtering: {filtered_len} rows remaining (from {original_len})")
            
            if filtered_len == 0:
                print(f"{Fore.YELLOW}No data found within the specified date range.{Style.RESET_ALL}")
                return metrics
        
        # Update metrics
        metrics["data_fetch_duration"] = load_end_time - load_start_time
        metrics["rows_count"] = len(df)
        metrics["columns_count"] = len(df.columns)
        
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== CSV INDICATOR FILE CONTENT ==={Style.RESET_ALL}")
        if start or end:
            print(f"Date filtered content (First 20 rows)")
        else:
            print(f"First 20 rows")
        print(f"{Fore.CYAN}Total rows:{Style.RESET_ALL} {len(df):,}")
        print(f"{Fore.CYAN}Columns ({len(df.columns)}):{Style.RESET_ALL} {', '.join(df.columns)}")
        
        # Show date range if available
        if start or end or len(df) > 0:
            _show_csv_date_range(df)
        
        print()
        print(df.head(20).to_string(index=False))
                
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        import traceback
        traceback.print_exc()
    
    return metrics


def _show_csv_date_range(df):
    """Show the date range of the CSV data."""
    try:
        # Try to find date column
        date_col = None
        if 'DateTime' in df.columns:
            date_col = 'DateTime'
        elif 'datetime' in df.columns:
            date_col = 'datetime'
        elif 'Date' in df.columns:
            date_col = 'Date'
        elif 'date' in df.columns:
            date_col = 'date'
        elif 'index' in df.columns:
            date_col = 'index'
        
        if date_col and not df.empty:
            dates = pd.to_datetime(df[date_col], errors='coerce')
            valid_dates = dates.dropna()
            if len(valid_dates) > 0:
                first_date = valid_dates.min()
                last_date = valid_dates.max()
                print(f"{Fore.CYAN}Date range:{Style.RESET_ALL} {first_date.strftime('%Y-%m-%d')} to {last_date.strftime('%Y-%m-%d')}")
    except Exception:
        # Silently ignore date range detection errors
        pass


def _show_csv_file_preview(file_path, metrics):
    """Display CSV file preview and update metrics."""
    df = pd.read_csv(file_path)
    
    # Update metrics
    metrics["rows_count"] = len(df)
    metrics["columns_count"] = len(df.columns)
    
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== CSV FILE CONTENT ==={Style.RESET_ALL} (First 10 rows)")
    print(f"{Fore.CYAN}Total rows:{Style.RESET_ALL} {len(df):,}")
    print(f"{Fore.CYAN}Columns ({len(df.columns)}):{Style.RESET_ALL} {', '.join(df.columns)}")
    print()
    print(df.head(10).to_string(index=False))
    
    return metrics
