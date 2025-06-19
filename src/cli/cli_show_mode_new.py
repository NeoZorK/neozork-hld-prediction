# -*- coding: utf-8 -*-
# src/cli/cli_show_mode_new.py

"""
Refactored CLI show mode with modular structure.
This is the new main entry point that imports from specialized modules.
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

# Import from refactored modules
from .cli_show_common import _initialize_metrics
from .cli_show_indicators import handle_indicator_mode

# Import for indicator calculation; fallback for different relative import
try:
    from src.calculation.indicator_calculation import calculate_indicator
    from src.export.parquet_export import export_indicator_to_parquet
    from src.export.csv_export import export_indicator_to_csv
    from src.export.json_export import export_indicator_to_json
except ImportError:
    try:
        from ..calculation.indicator_calculation import calculate_indicator
        from ..export.parquet_export import export_indicator_to_parquet
        from ..export.csv_export import export_indicator_to_csv
        from ..export.json_export import export_indicator_to_json
    except ImportError:
        # Last resort: assume running from src directory
        calculate_indicator = None
        export_indicator_to_parquet = None
        export_indicator_to_csv = None
        export_indicator_to_json = None

# Import the new AUTO fastest plot function
try:
    from src.plotting.fastest_auto_plot import plot_auto_fastest_parquet
except ImportError:
    plot_auto_fastest_parquet = None

# Import auto_plot_from_parquet for seaborn/sb
try:
    from src.plotting.seaborn_auto_plot import auto_plot_from_parquet
except ImportError:
    auto_plot_from_parquet = None

# Import auto_plot_from_parquet for mpl/mplfinance
try:
    from src.plotting.mplfinance_auto_plot import auto_plot_from_parquet as mpl_auto_plot_from_parquet
except ImportError:
    mpl_auto_plot_from_parquet = None

# Import auto_plot_from_dataframe for terminal plotting
try:
    from src.plotting.fast_plot import auto_plot_from_dataframe
except ImportError:
    auto_plot_from_dataframe = None

# Import existing functions from original file that we still need
try:
    from .cli_show_mode import (
        show_help, import_generate_plot, get_search_dirs, count_files_by_source,
        get_parquet_metadata, _get_relevant_columns_for_rule, _print_indicator_result,
        _should_draw_plot, _configure_terminal_plotting_mode
    )
except ImportError:
    # If we can't import from the original file, we'll need to define these
    print("Warning: Could not import some functions from original cli_show_mode.py")
    
    def show_help():
        print("Help functionality not available")
    
    def import_generate_plot():
        return None
    
    def get_search_dirs(args):
        return [Path("data/raw_parquet")]
    
    def count_files_by_source(args=None):
        return {}
    
    def get_parquet_metadata(file_path):
        return {'num_rows': -1, 'columns': [], 'first_date': None, 'last_date': None, 'first_row': None, 'last_row': None}
    
    def _get_relevant_columns_for_rule(rule_name, all_columns=None):
        return []
    
    def _print_indicator_result(df, rule_name, datetime_column=None):
        print(df.head())
    
    def _should_draw_plot(args):
        return hasattr(args, "draw") and args.draw is not None
    
    def _configure_terminal_plotting_mode(args):
        pass


def _handle_help_mode(args):
    """Handle help mode when no source is specified or source is 'help'."""
    show_help()
    source_counts = count_files_by_source(args)
    print("\n=== AVAILABLE DATA FILES ===")
    total_files = sum([count for source, count in source_counts.items() if source not in ['csv_converted_count']])
    
    # Add indicator files count
    from .cli_show_common import count_indicator_files
    indicator_counts = count_indicator_files()
    total_indicator_files = sum(indicator_counts.values())
    
    if total_files == 0 and total_indicator_files == 0:
        print("No data files found. Use other modes to download or import data first.")
        print("\nTo convert a CSV file, use the 'csv' mode:")
        print("  python run_analysis.py csv --csv-file path/to/data.csv --point 0.01")
        return _initialize_metrics()
        
    print(f"Total cached data files: {total_files}")
    for source, count in source_counts.items():
        if source in ['csv_converted_count']:
            continue
        if count > 0:
            print(f"  - {source.upper()}: {count} file(s)")
                    
    # Display indicator files
    if total_indicator_files > 0:
        print(f"\n=== AVAILABLE INDICATOR FILES ===")
        print(f"Total indicator files: {total_indicator_files}")
        for format_name, count in indicator_counts.items():
            if count > 0:
                print(f"  - {format_name.upper()}: {count} file(s)")
        print("\nTo view indicator files, use: python run_analysis.py show ind [format] [keywords...]")
        
    print("\nTo view specific files, use: python run_analysis.py show <source> [keywords...]")
    return _initialize_metrics()


def _search_files(args, search_dirs):
    """Search for files based on source and keywords."""
    print(f"Searching for '{args.source}' files with keywords: {args.keywords}...")

    search_prefix = 'yfinance' if args.source == 'yf' else args.source
    search_keywords = [k.lower() for k in args.keywords]
    found_files = []
    
    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        for item in search_dir.iterdir():
            if item.is_file() and item.suffix == '.parquet':
                filename_lower = item.name.lower()
                # Check if filename starts with search prefix and contains all keywords
                if filename_lower.startswith(search_prefix.lower()) and \
                   all(keyword in filename_lower for keyword in search_keywords):
                    try:
                        file_size_bytes = item.stat().st_size
                        file_size_mb = file_size_bytes / (1024 * 1024)
                        found_files.append({
                            'path': item,
                            'name': item.name,
                            'size_mb': file_size_mb
                        })
                    except OSError as e:
                        print(f"Warning: Could not get stats for file {item.name}. Error: {e}", file=sys.stderr)
    
    print(f"Found {len(found_files)} file(s).")
    return found_files


def _configure_single_file_mode(args, found_files):
    """Configure args for single file mode."""
    if len(found_files) == 1:
        print("Single file found. Will automatically open chart in browser.")
        # Flag this as a single file processing for export
        args.single_file_mode = True
        # Set default rule to OHLCV when only one file is found
        if not hasattr(args, 'rule') or not args.rule:
            args.rule = 'OHLCV'


def _display_file_info(found_files):
    """Display detailed information about found files."""
    found_files.sort(key=lambda x: x['name'])
    print("-" * 40)
    for idx, file_info in enumerate(found_files):
        metadata = get_parquet_metadata(file_info['path'])
        file_info.update(metadata)
        print(f"[{idx}] {file_info['name']}")
        print(f"    Size: {file_info['size_mb']:.3f} MB")
        if metadata['num_rows'] != -1:
            print(f"    Rows: {metadata['num_rows']:,}")
        else:
            print(f"    Rows: Unable to determine")
        if len(found_files) == 1:
            print(f"    Columns ({len(file_info['columns'])}): {', '.join(file_info['columns'])}")
            first_date = None
            last_date = None
            if file_info['first_date'] is not None:
                first_date = file_info['first_date'].strftime('%Y-%m-%d')
            if file_info['last_date'] is not None:
                last_date = file_info['last_date'].strftime('%Y-%m-%d')
            if first_date and last_date and first_date != last_date:
                print(f"    Date range: {first_date} to {last_date}")
            elif first_date:
                print(f"    Date: {first_date}")
            if file_info['first_row'] is not None:
                print(f"    First row: {file_info['first_row']}")
            if file_info['last_row'] is not None and file_info['num_rows'] > 1:
                print(f"    Last row: {file_info['last_row']}")
    print("-" * 40)


def _handle_single_file_mode(args, found_files, metrics):
    """Handle single file mode - simplified version."""
    print(f"Found one file. Loading data and preparing to display...")
    print(f"Loading file data and triggering plot with method: 'fastest'")
    try:
        # Track data loading time for single file
        t_load_start = time.perf_counter()
        df = pd.read_parquet(found_files[0]['path'])
        t_load_end = time.perf_counter()
        metrics["data_fetch_duration"] = t_load_end - t_load_start
        
        # Update metrics
        metrics["rows_count"] = len(df)
        metrics["columns_count"] = len(df.columns)
        metrics["data_size_bytes"] = df.memory_usage(deep=True).sum()
        metrics["data_size_mb"] = metrics["data_size_bytes"] / (1024 * 1024)
        metrics["file_size_bytes"] = found_files[0]['path'].stat().st_size
        
        # For now, just show basic info - full plotting logic can be added later
        print(f"Successfully loaded data: {len(df)} rows, {len(df.columns)} columns")
        
        return metrics
    except Exception as e:
        print(f"Error loading file: {e}")
        traceback.print_exc()
        return metrics


def handle_show_mode(args):
    """
    Handles the 'show' mode logic: finds files, displays info, and potentially triggers plot or indicator calculation.
    Returns timing and metrics data for execution summary.
    """
    # Initialize timing and metrics tracking
    metrics = _initialize_metrics()
    
    # Always use raw data directories
    search_dirs = get_search_dirs(args)

    # Configure terminal plotting mode
    _configure_terminal_plotting_mode(args)

    # Handle indicator files mode
    if args.source == 'ind':
        return handle_indicator_mode(args)

    if not args.source or args.source == 'help':
        return _handle_help_mode(args)

    # Search for files
    found_files = _search_files(args, search_dirs)
    if not found_files:
        return metrics
    
    # Configure single file mode if applicable
    _configure_single_file_mode(args, found_files)
    
    # Display file information
    _display_file_info(found_files)

    # Plot chart when one file found
    if len(found_files) > 1:
        print("To display a chart, re-run the command with more specific keywords:")
        print(f"Example: python run_analysis.py show {args.source} <additional_keywords>")
    elif len(found_files) == 1:
        return _handle_single_file_mode(args, found_files, metrics)
    
    return metrics
