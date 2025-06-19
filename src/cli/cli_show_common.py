# -*- coding: utf-8 -*-
# src/cli/cli_show_common.py

"""
Common utilities and shared functions for CLI show mode functionality.
"""

from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd
import sys
import time
import traceback
import os
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def _initialize_metrics():
    """Initialize metrics tracking dictionary."""
    return {
        "data_fetch_duration": 0,
        "calc_duration": 0,
        "plot_duration": 0,
        "rows_count": 0,
        "columns_count": 0,
        "data_size_mb": 0,
        "data_size_bytes": 0,
        "file_size_bytes": None,
        "point_size": None,
        "estimated_point": False
    }

def _extract_datetime_filter_args(args):
    """
    Utility to extract start/end from both short (--start/--end) and long (--show-start/--show-end) flags.
    """
    start = getattr(args, 'start', None) or getattr(args, 'show_start', None)
    end = getattr(args, 'end', None) or getattr(args, 'show_end', None)
    return start, end

def _filter_dataframe_by_date(df, start, end):
    """
    Filters dataframe by start/end date. Index must be DatetimeIndex or column 'DateTime'/'datetime' must exist.
    """
    if df.empty:
        return df
        
    date_index = None
    use_index = False
    
    if isinstance(df.index, pd.DatetimeIndex):
        date_index = df.index
        use_index = True
    elif 'DateTime' in df.columns:
        date_index = pd.to_datetime(df['DateTime'])
    elif 'datetime' in df.columns:
        date_index = pd.to_datetime(df['datetime'])
    elif 'index' in df.columns:
        # Try to parse the index column as datetime
        try:
            date_index = pd.to_datetime(df['index'])
        except:
            pass
    
    if date_index is not None:
        if start:
            try:
                start_date = pd.to_datetime(start)
                if use_index:
                    df = df[df.index >= start_date]
                else:
                    mask = date_index >= start_date
                    df = df[mask]
            except Exception as e:
                print(f"Warning: Could not parse start date '{start}': {e}")
        
        if end:
            try:
                end_date = pd.to_datetime(end)
                if use_index:
                    df = df[df.index <= end_date]
                else:
                    mask = date_index <= end_date
                    df = df[mask]
            except Exception as e:
                print(f"Warning: Could not parse end date '{end}': {e}")
    else:
        if start or end:
            print("Warning: No datetime column found for date filtering")
    
    return df

def get_indicator_search_dirs():
    """
    Returns the search directories for indicator files.
    """
    return [
        Path("data/indicators/parquet"),
        Path("data/indicators/csv"),
        Path("data/indicators/json")
    ]

def count_indicator_files():
    """
    Counts indicator files by format (parquet, csv, json).
    """
    search_dirs = get_indicator_search_dirs()
    format_counts = {
        'parquet': 0,
        'csv': 0,
        'json': 0
    }
    
    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        format_name = search_dir.name  # parquet, csv, or json
        for item in search_dir.iterdir():
            if item.is_file():
                if (format_name == 'parquet' and item.suffix == '.parquet') or \
                   (format_name == 'csv' and item.suffix == '.csv') or \
                   (format_name == 'json' and item.suffix == '.json'):
                    format_counts[format_name] += 1
    
    return format_counts

def _parse_indicator_search_params(args):
    """Parse format filter and keywords from args."""
    format_filter = None
    remaining_keywords = []
    
    if args.keywords:
        first_keyword = args.keywords[0].lower()
        if first_keyword in ['parquet', 'csv', 'json']:
            format_filter = first_keyword
            remaining_keywords = args.keywords[1:]
        else:
            remaining_keywords = args.keywords
    
    return format_filter, remaining_keywords

def _search_indicator_files(format_filter, remaining_keywords):
    """Search for indicator files based on format and keywords."""
    search_dirs = get_indicator_search_dirs()
    found_files = []
    
    # If no format filter, search all directories
    if format_filter is None:
        dirs_to_search = search_dirs
    else:
        # Search only in the specified format directory
        dir_map = {
            'parquet': Path("data/indicators/parquet"),
            'csv': Path("data/indicators/csv"),
            'json': Path("data/indicators/json")
        }
        dirs_to_search = [dir_map[format_filter]]
    
    search_keywords = [k.lower() for k in remaining_keywords]
    
    for search_dir in dirs_to_search:
        if not search_dir.is_dir():
            continue
            
        file_format = search_dir.name  # parquet, csv, or json
        expected_extension = f".{file_format}"
        
        for item in search_dir.iterdir():
            if item.is_file() and item.suffix == expected_extension:
                filename_lower = item.name.lower()
                if all(keyword in filename_lower for keyword in search_keywords):
                    try:
                        file_size_bytes = item.stat().st_size
                        file_size_mb = file_size_bytes / (1024 * 1024)
                        found_files.append({
                            'path': item,
                            'name': item.name,
                            'size_mb': file_size_mb,
                            'format': file_format
                        })
                    except OSError as e:
                        print(f"Warning: Could not get stats for file {item.name}. Error: {e}", file=sys.stderr)
    
    return found_files

def show_indicator_help():
    """
    Displays help for the 'show ind' mode with colorful formatting.
    """
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== SHOW INDICATOR FILES HELP ==={Style.RESET_ALL}")
    print(f"The {Fore.GREEN}'show ind'{Style.RESET_ALL} mode allows you to list and inspect calculated indicator files.")
    print(f"{Fore.YELLOW}Usage:{Style.RESET_ALL} python run_analysis.py show ind [format] [keywords...] [-d backend] [--rule RULE] [--start DATE] [--end DATE]")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Available formats:{Style.RESET_ALL}")
    print(f"  - {Fore.GREEN}parquet{Style.RESET_ALL}: Parquet indicator files (for plotting and analysis)")
    print(f"  - {Fore.GREEN}csv{Style.RESET_ALL}: CSV indicator files (for terminal display and external use)")
    print(f"  - {Fore.GREEN}json{Style.RESET_ALL}: JSON indicator files (for terminal display and external use)")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Examples:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind{Style.RESET_ALL}                {Fore.BLACK}{Style.DIM}# Show all indicator files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet{Style.RESET_ALL}       {Fore.BLACK}{Style.DIM}# List all parquet indicator files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind csv{Style.RESET_ALL}           {Fore.BLACK}{Style.DIM}# List all CSV indicator files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind json{Style.RESET_ALL}          {Fore.BLACK}{Style.DIM}# List all JSON indicator files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet mn1{Style.RESET_ALL}   {Fore.BLACK}{Style.DIM}# List parquet files containing 'mn1'{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind csv GBPUSD{Style.RESET_ALL}    {Fore.BLACK}{Style.DIM}# List CSV files containing 'GBPUSD'{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Date Filtering Examples:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet SupportResistants --start 06.06.2025{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind csv PressureVector --start 01.05.2025 --end 30.06.2025{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind json GBPUSD --end 2025-06-15{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Plotting Examples (Parquet files):{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet -d fastest{Style.RESET_ALL}  {Fore.BLACK}{Style.DIM}# Plot with fastest backend{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet -d plotly{Style.RESET_ALL}   {Fore.BLACK}{Style.DIM}# Plot with Plotly backend{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet -d mpl{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# Plot with mplfinance backend{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet -d seaborn{Style.RESET_ALL}  {Fore.BLACK}{Style.DIM}# Plot with Seaborn backend{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet -d term{Style.RESET_ALL}     {Fore.BLACK}{Style.DIM}# Plot with terminal ASCII charts{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet PV -d plotly{Style.RESET_ALL} {Fore.BLACK}{Style.DIM}# Plot PV files with Plotly{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Available Drawing Backends (-d flag):{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}-d fastest{Style.RESET_ALL}   {Fore.BLACK}{Style.DIM}# Default - Plotly+Dask+Datashader (best for large datasets){Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}-d fast{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# Dask+Datashader+Bokeh for quick visualization{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}-d plotly{Style.RESET_ALL}    {Fore.BLACK}{Style.DIM}# Interactive HTML plots with Plotly{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}-d mpl{Style.RESET_ALL}       {Fore.BLACK}{Style.DIM}# Static images with mplfinance{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}-d seaborn{Style.RESET_ALL}   {Fore.BLACK}{Style.DIM}# Statistical plots with Seaborn{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}-d term{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# Terminal ASCII charts with plotext{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Trading Rules (--rule flag):{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--rule AUTO{Style.RESET_ALL}    {Fore.BLACK}{Style.DIM}# Default - Display all calculated indicators{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--rule PV{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# Focus on Pressure Vector indicators{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--rule SR{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# Focus on Support and Resistance indicators{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--rule PHLD{Style.RESET_ALL}    {Fore.BLACK}{Style.DIM}# Focus on Predict High Low Direction indicators{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Date Filtering Options:{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--start DATE{Style.RESET_ALL}   {Fore.BLACK}{Style.DIM}# Filter data from this date onwards{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--end DATE{Style.RESET_ALL}     {Fore.BLACK}{Style.DIM}# Filter data up to this date{Style.RESET_ALL}")
    print(f"  {Fore.BLACK}{Style.DIM}Date formats: DD.MM.YYYY, YYYY-MM-DD, MM/DD/YYYY{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Note:{Style.RESET_ALL}")
    print(f"  - {Fore.MAGENTA}Parquet files{Style.RESET_ALL} can be displayed as charts with all drawing backends")
    print(f"  - {Fore.MAGENTA}CSV and JSON files{Style.RESET_ALL} are displayed as formatted terminal output")
    print(f"  - Single parquet file will automatically open chart with specified backend")
    print(f"  - Date filtering works for all formats when displaying single files")
    print(f"  - If no date flags are provided, all data will be shown")

def _display_indicator_file_list(found_files, metrics):
    """Display the list of indicator files with details."""
    print("-" * 60)
    current_format = None
    for idx, file_info in enumerate(found_files):
        if file_info['format'] != current_format:
            current_format = file_info['format']
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== {current_format.upper()} FILES ==={Style.RESET_ALL}")
        
        print(f"[{idx}] {file_info['name']}")
        print(f"    Size: {file_info['size_mb']:.3f} MB")
        print(f"    Format: {file_info['format']}")

    return metrics
