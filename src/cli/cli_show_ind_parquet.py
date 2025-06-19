# -*- coding: utf-8 -*-
# src/cli/cli_show_ind_parquet.py

"""
Parquet indicator file handling for CLI show mode.
"""

import pandas as pd
import time
import os
from colorama import Fore, Style
from .cli_show_common import _initialize_metrics, _extract_datetime_filter_args, _filter_dataframe_by_date

# Import plotting functions
try:
    from src.plotting.fastest_auto_plot import plot_auto_fastest_parquet
except ImportError:
    plot_auto_fastest_parquet = None

try:
    from src.plotting.seaborn_auto_plot import auto_plot_from_parquet
except ImportError:
    auto_plot_from_parquet = None

try:
    from src.plotting.mplfinance_auto_plot import auto_plot_from_parquet as mpl_auto_plot_from_parquet
except ImportError:
    mpl_auto_plot_from_parquet = None

try:
    from src.plotting.fast_plot import auto_plot_from_dataframe
except ImportError:
    auto_plot_from_dataframe = None


def show_parquet_indicator_file(file_info, args):
    """
    Shows a single indicator parquet file with appropriate visualization and date filtering.
    Returns timing and metrics data.
    """
    # Initialize timing and metrics tracking
    metrics = _initialize_metrics()
    
    file_path = file_info['path']
    
    try:
        # Track data loading time
        load_start_time = time.time()
        df = pd.read_parquet(file_path)
        load_end_time = time.time()
        
        # Update metrics
        metrics["data_fetch_duration"] = load_end_time - load_start_time
        metrics["rows_count"] = len(df)
        metrics["columns_count"] = len(df.columns)
        metrics["data_size_mb"] = file_info['size_mb']
        metrics["data_size_bytes"] = int(file_info['size_mb'] * 1024 * 1024)
        
        print(f"\nLoaded indicator file: {file_info['name']}")
        print(f"Rows: {len(df):,}, Columns: {len(df.columns)}")
        print(f"Columns: {', '.join(df.columns)}")
        
        # Apply date filtering if start/end flags are provided
        start, end = _extract_datetime_filter_args(args)
        if start or end:
            print(f"Applying date filtering to indicator data...")
            original_len = len(df)
            df = _filter_dataframe_by_date(df, start, end)
            filtered_len = len(df)
            print(f"After date filtering: {filtered_len} rows remaining (from {original_len})")
            
            if filtered_len == 0:
                print(f"{Fore.YELLOW}No data found within the specified date range.{Style.RESET_ALL}")
                return metrics
            
            # Update metrics after filtering
            metrics["rows_count"] = filtered_len
        
        # Show date range
        _show_parquet_date_range(df)
        
        # Handle plotting
        metrics = _plot_indicator_parquet_file(args, df, file_info, metrics)
            
    except Exception as e:
        print(f"Error loading parquet file: {e}")
        import traceback
        traceback.print_exc()
    
    return metrics


def _show_parquet_date_range(df):
    """Show the date range of the parquet data."""
    try:
        if isinstance(df.index, pd.DatetimeIndex) and len(df) > 0:
            first_date = df.index.min()
            last_date = df.index.max()
            print(f"{Fore.CYAN}Date range:{Style.RESET_ALL} {first_date.strftime('%Y-%m-%d')} to {last_date.strftime('%Y-%m-%d')}")
        else:
            # Try to find date column
            date_col = None
            for col in ['DateTime', 'datetime', 'Date', 'date', 'index']:
                if col in df.columns:
                    date_col = col
                    break
            
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


def _plot_indicator_parquet_file(args, df, file_info, metrics):
    """Handle plotting for indicator parquet files."""
    # Set up for plotting with all available drawing backends
    args.mode = 'show'
    if not hasattr(args, 'rule') or args.rule is None:
        args.rule = 'AUTO'  # Show all calculated indicators
    
    # For indicator files, ignore calculation-related flags (--point, -t, -i)
    # These flags are only for calculation mode, not for reading existing indicator files
    point_size = 0.01  # Default point size for indicator files
    metrics["point_size"] = point_size
    metrics["estimated_point"] = True
    
    # Clear any calculation flags that shouldn't be used for indicator file display
    if hasattr(args, 'point'):
        delattr(args, 'point')  # Ignore --point flag
    if hasattr(args, 'timeframe'):
        delattr(args, 'timeframe')  # Ignore -t flag
    if hasattr(args, 'instrument'):
        delattr(args, 'instrument')  # Ignore -i flag
    
    # Use the same plotting system as other show commands
    draw_method = getattr(args, 'draw', 'fastest')
    
    # Track plotting time
    plot_start_time = time.time()
    
    if draw_method in ['term', 'terminal']:
        # Terminal mode - use plotext
        plot_title = f"Indicator File: {file_info['name']}"
        if auto_plot_from_dataframe:
            auto_plot_from_dataframe(df, plot_title)
            print(f"Successfully plotted indicator file '{file_info['name']}' using terminal mode.")
        else:
            print("Terminal plotting function not available")
    else:
        # Use generate_plot for all other backends (fastest, fast, plotly, mpl, seaborn)
        try:
            from src.cli.cli_show_mode import import_generate_plot
            generate_plot = import_generate_plot()
            
            data_info = {
                "ohlcv_df": df,
                "data_source_label": f"Indicator: {file_info['name']}",
                "rows_count": len(df),
                "columns_count": len(df.columns),
                "data_size_mb": file_info['size_mb'],
                "first_date": df.index[0] if isinstance(df.index, pd.DatetimeIndex) and len(df) > 0 else None,
                "last_date": df.index[-1] if isinstance(df.index, pd.DatetimeIndex) and len(df) > 0 else None,
                "parquet_cache_used": True,
                "parquet_cache_file": str(file_info['path']),
                "all_columns": list(df.columns)
            }
            selected_rule = args.rule if hasattr(args, 'rule') and args.rule else "AUTO"
            estimated_point = True
            generate_plot(args, data_info, df, selected_rule, point_size, estimated_point)
            print(f"Successfully plotted indicator file '{file_info['name']}' using '{draw_method}' mode.")
        except ImportError as e:
            print(f"Warning: Could not import plotting functions: {e}")
            print(f"Plotting may not be available.")
    
    plot_end_time = time.time()
    metrics["plot_duration"] = plot_end_time - plot_start_time
    
    return metrics


def handle_multiple_parquet_files(args, found_files, format_filter, metrics):
    """Handle multiple parquet files with drawing backend."""
    # For indicator mode, parquet files should behave like CSV/JSON files:
    # - List files when multiple matches
    # - Only show chart/content when a single file remains after filtering
    # Only plot multiple files if explicit draw flag is provided AND it's not indicator mode
    if (format_filter == 'parquet' and hasattr(args, 'draw') and args.draw and 
        not getattr(args, 'indicator_mode', False)):
        parquet_files = [f for f in found_files if f['format'] == 'parquet']
        if len(parquet_files) > 1:
            print(f"Multiple parquet files found. Plotting all {len(parquet_files)} files with '{args.draw}' backend.")
            total_rows = 0
            total_cols = 0
            total_size = 0
            total_plot_time = 0
            total_load_time = 0
            
            for file_info in parquet_files:
                print(f"\n{Fore.YELLOW}Processing: {file_info['name']}{Style.RESET_ALL}")
                single_metrics = show_parquet_indicator_file(file_info, args)
                total_rows += single_metrics.get("rows_count", 0)
                if single_metrics.get("columns_count", 0) > total_cols:
                    total_cols = single_metrics.get("columns_count", 0)
                total_size += single_metrics.get("data_size_mb", 0)
                total_plot_time += single_metrics.get("plot_duration", 0)
                total_load_time += single_metrics.get("data_fetch_duration", 0)
            
            # Aggregate metrics for multiple files
            metrics["rows_count"] = total_rows
            metrics["columns_count"] = total_cols
            metrics["data_size_mb"] = total_size
            metrics["plot_duration"] = total_plot_time
            metrics["data_fetch_duration"] = total_load_time
            
            return True, metrics
    
    return False, metrics
