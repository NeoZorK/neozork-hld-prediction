# -*- coding: utf-8 -*-
# src/cli/cli_show_ind_json.py

"""
JSON indicator file handling for CLI show mode.
"""

import json
import pandas as pd
import time
from colorama import Fore, Style
from .cli_show_common import _initialize_metrics, _extract_datetime_filter_args, _filter_dataframe_by_date


def show_json_indicator_file(file_info, args):
    """
    Shows a single JSON indicator file with date filtering support.
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
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        load_end_time = time.time()
        
        # Update metrics
        metrics["data_fetch_duration"] = load_end_time - load_start_time
        
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== JSON INDICATOR FILE CONTENT ==={Style.RESET_ALL}")
        
        # For JSON, try to convert to DataFrame for date filtering
        if start or end:
            try:
                if isinstance(data, list) and data and isinstance(data[0], dict):
                    df = pd.DataFrame(data)
                    print(f"Applying date filtering to JSON data...")
                    original_len = len(df)
                    df = _filter_dataframe_by_date(df, start, end)
                    filtered_len = len(df)
                    print(f"After date filtering: {filtered_len} rows remaining (from {original_len})")
                    
                    if filtered_len == 0:
                        print(f"{Fore.YELLOW}No data found within the specified date range.{Style.RESET_ALL}")
                        return metrics
                    
                    # Convert back to list of dicts
                    data = df.to_dict('records')
                    print(f"Showing first 10 filtered records:")
                else:
                    print(f"Cannot apply date filtering to this JSON structure")
            except Exception as e:
                print(f"Warning: Could not apply date filtering to JSON: {e}")
        
        if isinstance(data, dict):
            metrics = _show_json_dict_preview(data, metrics, start or end)
        elif isinstance(data, list):
            metrics = _show_json_list_preview(data, metrics, start or end)
        else:
            metrics = _show_json_other_preview(data, metrics)
                
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        import traceback
        traceback.print_exc()
    
    return metrics


def _show_json_dict_preview(data, metrics, is_filtered=False):
    """Display JSON dictionary data preview."""
    metrics["rows_count"] = len(data)
    metrics["columns_count"] = len(data) if data else 0
    
    print(f"{Fore.CYAN}Data structure:{Style.RESET_ALL} Dictionary with {len(data)} keys")
    if data:
        print(f"{Fore.CYAN}Keys:{Style.RESET_ALL} {', '.join(data.keys())}")
        print()
        
        # Show first few values for each key
        max_items = 10 if is_filtered else 5
        for key, value in list(data.items())[:max_items]:
            if isinstance(value, list):
                print(f"{Fore.GREEN}{key}:{Style.RESET_ALL} [{len(value)} items]")
                if value:
                    # Show first few items
                    sample_items = value[:3]
                    for i, item in enumerate(sample_items):
                        print(f"  [{i}] {item}")
                    if len(value) > 3:
                        print(f"  ... and {len(value) - 3} more items")
            else:
                print(f"{Fore.GREEN}{key}:{Style.RESET_ALL} {value}")
            print()
    
    return metrics


def _show_json_list_preview(data, metrics, is_filtered=False):
    """Display JSON list data preview."""
    metrics["rows_count"] = len(data)
    if data and isinstance(data[0], dict):
        metrics["columns_count"] = len(data[0])
    
    print(f"{Fore.CYAN}Data structure:{Style.RESET_ALL} List with {len(data)} records")
    if data:
        first_item = data[0]
        if isinstance(first_item, dict):
            print(f"{Fore.CYAN}Record keys:{Style.RESET_ALL} {', '.join(first_item.keys())}")
        print()
        
        # Show date range if we can determine it
        _show_json_date_range(data)
        
        # Show first few records
        max_records = 15 if is_filtered else 10
        for i, record in enumerate(data[:max_records]):
            print(f"{Fore.GREEN}Record {i+1}:{Style.RESET_ALL}")
            if isinstance(record, dict):
                for key, value in record.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {record}")
            print()
        
        if len(data) > max_records:
            print(f"{Fore.BLACK}{Style.DIM}... and {len(data) - max_records} more records{Style.RESET_ALL}")
    
    return metrics


def _show_json_other_preview(data, metrics):
    """Display other JSON data types preview."""
    # Other data types
    metrics["rows_count"] = 1
    metrics["columns_count"] = 1
    
    print(f"{Fore.CYAN}Data type:{Style.RESET_ALL} {type(data).__name__}")
    data_str = json.dumps(data, indent=2)
    if len(data_str) > 2000:
        print(data_str[:2000] + f"\n{Fore.BLACK}{Style.DIM}... (truncated){Style.RESET_ALL}")
    else:
        print(data_str)
    
    return metrics


def _show_json_date_range(data):
    """Show the date range of the JSON data if available."""
    try:
        if isinstance(data, list) and data and isinstance(data[0], dict):
            # Try to find date column
            first_record = data[0]
            date_keys = ['DateTime', 'datetime', 'Date', 'date', 'index']
            date_key = None
            
            for key in date_keys:
                if key in first_record:
                    date_key = key
                    break
            
            if date_key:
                dates = []
                for record in data:
                    if date_key in record:
                        try:
                            date_val = pd.to_datetime(record[date_key])
                            dates.append(date_val)
                        except:
                            continue
                
                if dates:
                    first_date = min(dates)
                    last_date = max(dates)
                    print(f"{Fore.CYAN}Date range:{Style.RESET_ALL} {first_date.strftime('%Y-%m-%d')} to {last_date.strftime('%Y-%m-%d')}")
    except Exception:
        # Silently ignore date range detection errors
        pass


def _show_json_file_preview(file_path, metrics):
    """Display JSON file preview and update metrics."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== JSON FILE CONTENT ==={Style.RESET_ALL}")
    
    if isinstance(data, dict):
        metrics = _show_json_dict_preview(data, metrics)
    elif isinstance(data, list):
        metrics = _show_json_list_preview(data, metrics)
    else:
        metrics = _show_json_other_preview(data, metrics)
    
    return metrics
