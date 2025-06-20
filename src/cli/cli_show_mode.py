# -*- coding: utf-8 -*-
# src/core/cli_show_mode.py

from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd
import sys
import time  # Added for timing tracking
import traceback
import os  # Added for Docker detection
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

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

# Import terminal auto plot function for AUTO mode
try:
    from src.plotting.term_auto_plot import auto_plot_from_dataframe
except ImportError:
    auto_plot_from_dataframe = None

def show_help():
    """
    Displays help for the 'show' mode with colorful formatting.
    """
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== SHOW MODE HELP ==={Style.RESET_ALL}")
    print(f"The {Fore.GREEN}'show'{Style.RESET_ALL} mode allows you to list and inspect cached data files.")
    print(f"{Fore.YELLOW}Usage:{Style.RESET_ALL} python run_analysis.py show <source> [keywords...]")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Available sources:{Style.RESET_ALL}")
    print(f"  - {Fore.GREEN}csv{Style.RESET_ALL}: Converted CSV data files")
    print(f"  - {Fore.GREEN}yfinance/yf{Style.RESET_ALL}: Yahoo Finance data files")
    print(f"  - {Fore.GREEN}polygon{Style.RESET_ALL}: Polygon.io API data files")
    print(f"  - {Fore.GREEN}binance{Style.RESET_ALL}: Binance API data files")
    print(f"  - {Fore.GREEN}exrate{Style.RESET_ALL}: Exchange Rate API data files")
    print(f"  - {Fore.GREEN}ind{Style.RESET_ALL}: Calculated indicator files (parquet/csv/json)")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Examples:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show{Style.RESET_ALL}                  {Fore.BLACK}{Style.DIM}# Show statistics for all sources{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show yf{Style.RESET_ALL}               {Fore.BLACK}{Style.DIM}# List all Yahoo Finance files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show csv{Style.RESET_ALL}              {Fore.BLACK}{Style.DIM}# List all CSV-converted files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show binance{Style.RESET_ALL}          {Fore.BLACK}{Style.DIM}# List all Binance files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show polygon{Style.RESET_ALL}          {Fore.BLACK}{Style.DIM}# List all Polygon.io files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show exrate{Style.RESET_ALL}           {Fore.BLACK}{Style.DIM}# List all Exchange Rate API files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind{Style.RESET_ALL}              {Fore.BLACK}{Style.DIM}# List all indicator files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# List parquet indicator files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet -d plotly{Style.RESET_ALL} {Fore.BLACK}{Style.DIM}# Plot indicator files with Plotly{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show yf aapl{Style.RESET_ALL}          {Fore.BLACK}{Style.DIM}# List YF files containing 'aapl'{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show binance btc MN1{Style.RESET_ALL}  {Fore.BLACK}{Style.DIM}# List Binance files with 'btc' and timeframe 'MN1'{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show exrate eurusd{Style.RESET_ALL}    {Fore.BLACK}{Style.DIM}# List Exchange Rate API EURUSD files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show yf eurusd{Style.RESET_ALL}        {Fore.BLACK}{Style.DIM}# List all Yahoo Finance EURUSD files{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show csv aapl d1{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# List CSV files with 'aapl' and 'D1' timeframe{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show --start 2024-01-01{Style.RESET_ALL} {Fore.BLACK}{Style.DIM}# List files with data starting from 2024-01-01{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show yf --rule PV{Style.RESET_ALL}     {Fore.BLACK}{Style.DIM}# List YF files and apply PV indicator when viewing{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show eth{Style.RESET_ALL}              {Fore.BLACK}{Style.DIM}# Find any files containing 'eth' (e.g., Ethereum){Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show forex{Style.RESET_ALL}            {Fore.BLACK}{Style.DIM}# Find any files containing 'forex'{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Trading Rules:{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--rule OHLCV{Style.RESET_ALL}   {Fore.BLACK}{Style.DIM}# Display basic OHLCV candlestick chart{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--rule PV{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# Calculate Pressure Vector indicator{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--rule SR{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# Calculate Support and Resistance levels{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--rule PHLD{Style.RESET_ALL}    {Fore.BLACK}{Style.DIM}# Calculate Predict High Low Direction indicator{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--rule AUTO{Style.RESET_ALL}    {Fore.BLACK}{Style.DIM}# Automatically display all columns in the file{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Drawing Options (-d flag):{Style.RESET_ALL}")
    print(f"  The {Fore.MAGENTA}-d{Style.RESET_ALL} or {Fore.MAGENTA}--draw{Style.RESET_ALL} flag allows you to specify the plotting library for visualization:")
    print(f"  {Fore.MAGENTA}-d fastest{Style.RESET_ALL}   {Fore.BLACK}{Style.DIM}# Default - Plotly+Dask+Datashader (best for large datasets){Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}-d fast{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# Dask+Datashader+Bokeh for quick visualization{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}-d plotly{Style.RESET_ALL}    {Fore.BLACK}{Style.DIM}# Interactive HTML plots with Plotly (also with 'plt'){Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}-d mpl{Style.RESET_ALL}       {Fore.BLACK}{Style.DIM}# Static images with mplfinance (also with 'mplfinance'){Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}-d seaborn{Style.RESET_ALL}   {Fore.BLACK}{Style.DIM}# Statistical plots with Seaborn (also with 'sb'){Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}-d term{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# Terminal ASCII charts with plotext (great for SSH){Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Drawing Examples:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show yf aapl -d term{Style.RESET_ALL}  {Fore.BLACK}{Style.DIM}# Show AAPL data with terminal charts{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show csv --rule PV -d plotly{Style.RESET_ALL}  {Fore.BLACK}{Style.DIM}# Show CSV data with PV indicator using Plotly{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show binance btc -d seaborn{Style.RESET_ALL}  {Fore.BLACK}{Style.DIM}# Show BTC data with Seaborn plots{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet -d fastest{Style.RESET_ALL}  {Fore.BLACK}{Style.DIM}# Show indicator files with fastest backend{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python run_analysis.py show ind parquet -d mpl{Style.RESET_ALL}      {Fore.BLACK}{Style.DIM}# Show indicator files with mplfinance{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Date filtering:{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}--start, --end{Style.RESET_ALL} or {Fore.MAGENTA}--show-start, --show-end{Style.RESET_ALL} for date range filtering.")

def import_generate_plot():
    """
    Dynamically imports the generate_plot function for plotting.
    """
    from ..plotting.plotting_generation import generate_plot
    return generate_plot

def get_search_dirs(args):
    """
    Returns the search directories for show mode (raw data only).
    """
    return [
        Path("data/raw_parquet"),
        Path("data/cache/csv_converted")
    ]

def count_files_by_source(args=None):
    """
    Counts Parquet files by their source prefix (yfinance, csv, polygon, binance).
    Uses get_search_dirs(args) for directory selection.
    """
    search_dirs = get_search_dirs(args) if args is not None else [
        Path("data/raw_parquet"),
        Path("data/cache/csv_converted")
    ]
    source_counts = {
        'yfinance': 0,
        'csv': 0,
        'polygon': 0,
        'binance': 0,
        'exrate': 0,
        'other': 0,
        'csv_converted_count': 0
    }
    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        for item in search_dir.iterdir():
            if item.is_file() and item.suffix == '.parquet':
                filename_lower = item.name.lower()
                if filename_lower.startswith('yfinance_'):
                    source_counts['yfinance'] += 1
                elif filename_lower.startswith('csv_'):
                    source_counts['csv'] += 1
                    if 'csv_converted' in str(search_dir).lower():
                        source_counts['csv_converted_count'] += 1
                elif 'csv_converted' in str(search_dir).lower():
                    source_counts['csv'] += 1
                    source_counts['csv_converted_count'] += 1
                elif filename_lower.startswith('polygon_'):
                    source_counts['polygon'] += 1
                elif filename_lower.startswith('binance_'):
                    source_counts['binance'] += 1
                elif filename_lower.startswith('exrate_'):
                    source_counts['exrate'] += 1
                else:
                    source_counts['other'] += 1
    return source_counts

def get_parquet_metadata(file_path: Path) -> dict:
    """
    Reads metadata (row count, columns, first/last row with all fields) from a Parquet file.
    """
    metadata = {'num_rows': -1, 'columns': [], 'first_row': None, 'last_row': None, 'first_date': None, 'last_date': None}
    try:
        parquet_file = pq.ParquetFile(file_path)
        metadata['num_rows'] = parquet_file.metadata.num_rows
        metadata['columns'] = parquet_file.schema.names
        if metadata['num_rows'] > 0:
            df_head = pd.read_parquet(file_path).head(1)
            if not df_head.empty:
                metadata['first_row'] = df_head.iloc[0]
                metadata['first_date'] = df_head.index[0] if isinstance(df_head.index, pd.DatetimeIndex) else df_head.iloc[0, 0]
            if metadata['num_rows'] > 1:
                df_tail = pd.read_parquet(file_path).tail(1)
                if not df_tail.empty:
                    metadata['last_row'] = df_tail.iloc[0]
                    metadata['last_date'] = df_tail.index[0] if isinstance(df_tail.index, pd.DatetimeIndex) else df_tail.iloc[0, 0]
            elif metadata['num_rows'] == 1:
                metadata['last_row'] = metadata['first_row']
                metadata['last_date'] = metadata['first_date']
    except Exception as e:
        print(f"Warning: Could not read metadata for {file_path.name}. Error: {e}", file=sys.stderr)
    return metadata

def _get_relevant_columns_for_rule(rule_name: str, all_columns=None) -> list:
    """
    Returns the relevant columns to output for the given rule,
    according to clarified user logic.
    """
    base_cols = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'HL', 'Pressure', 'PV']
    rule_aliases_map = {
        'PHLD': 'Predict_High_Low_Direction',
        'PV': 'Pressure_Vector',
        'SR': 'Support_Resistants',
        'AUTO': 'Auto_Display_All'
    }
    rule_name_upper = rule_name.upper() if rule_name else ''
    canonical_rule = rule_aliases_map.get(rule_name_upper, rule_name)

    if canonical_rule in ['Auto_Display_All']:
        # For AUTO rule, return all columns available
        if all_columns:
            # Ensure datetime column is first, if present
            datetime_cols = [col for col in all_columns if col.lower() in ['datetime', 'date', 'time', 'timestamp']]
            # Include all schema columns from parquet file, especially looking for prediction columns
            prediction_cols = [col for col in all_columns if any(pred.lower() in col.lower()
                              for pred in ['predicted', 'pressure', 'vector', 'signal', 'direction'])]
            # Other numeric columns
            other_cols = [col for col in all_columns if col not in datetime_cols and col not in prediction_cols]

            print(f"AUTO mode columns detection: datetime={datetime_cols}, predictions={prediction_cols}, other={len(other_cols)}")

            # Return all columns in the right order
            return datetime_cols + prediction_cols + other_cols
        return base_cols
    elif canonical_rule in ['Predict_High_Low_Direction']:
        return base_cols + ['PPrice1', 'PPrice2', 'Direction']
    elif canonical_rule in ['Pressure_Vector']:
        return base_cols + ['PPrice1', 'Direction']
    elif canonical_rule in ['Support_Resistants']:
        return base_cols + ['PPrice1', 'PPrice2']
    elif canonical_rule == 'PV_HighLow':
        return base_cols + ['PPrice1', 'PPrice2']
    else:
        return base_cols + ['PPrice1', 'PPrice2', 'Direction']

def _print_indicator_result(df, rule_name, datetime_column=None):
    """
    Prints a DataFrame with only the relevant columns for the rule.
    Always includes DateTime.
    """
    df_to_show = df.copy()
    if datetime_column and datetime_column in df_to_show.columns:
        pass
    elif isinstance(df_to_show.index, pd.DatetimeIndex):
        df_to_show['DateTime'] = df_to_show.index
        datetime_column = 'DateTime'
    elif 'DateTime' in df_to_show.columns:
        datetime_column = 'DateTime'
    elif 'datetime' in df_to_show.columns:
        df_to_show['DateTime'] = df_to_show['datetime']
        datetime_column = 'DateTime'
    else:
        df_to_show['DateTime'] = df_to_show.index
        datetime_column = 'DateTime'

    # Handle AUTO rule separately - show all columns
    if rule_name and rule_name.upper() == 'AUTO':
        # Get all columns to show
        columns_to_show = list(df_to_show.columns)
        print(f"\n=== AUTO DISPLAY MODE: ALL COLUMNS === ({df_to_show.shape[0]} rows in selected range)")
        print(f"Displaying all {len(columns_to_show)} columns from the file.")
    else:
        # For other rules, get specific columns based on the rule
        columns_to_show = _get_relevant_columns_for_rule(rule_name, all_columns=df_to_show.columns)
        print(f"\n=== CALCULATED INDICATOR DATA === ({df_to_show.shape[0]} rows in selected range)")

    columns_to_show_existing = [col for col in columns_to_show if col in df_to_show.columns]
    row_count = df_to_show.shape[0]

    # Limit to first 100 rows
    if row_count > 100:
        df_to_show = df_to_show.head(100)
        print("(Showing only the first 100 rows)")

    if columns_to_show_existing:
        print(df_to_show[columns_to_show_existing].to_string(index=False))
    else:
        print("No relevant columns found in DataFrame to display.")

def _extract_datetime_filter_args(args):
    """
    Utility to extract start/end from both short (--start/--end) and long (--show-start/--show-end) flags.
    """
    start = getattr(args, 'start', None) or getattr(args, 'show_start', None)
    end = getattr(args, 'end', None) or getattr(args, 'show_end', None)
    return start, end

def _filter_dataframe_by_date(df, start, end):
    """
    Filters dataframe by start/end date. Index must be DatetimeIndex or column 'DateTime'/'datetime'/'date'/'timestamp'/'index' must exist.
    """
    if df.empty:
        return df
    date_index = None
    # List of possible date column names
    # Find the first suitable column (case-insensitive)
    # If the index is called 'index' and contains dates, use it
    # If the date is in the index, use it
    # Add a date column and a row number column
    # Properly format datetime for Series and DatetimeIndex
    # Form a date column for display
    # Determine the name of the date column
    # If the date is in the index, use it
    # Add a date column and a row number column
    # Properly format datetime for Series and DatetimeIndex
    # reset_index is required so that the date is not lost
    # Diagnostics: print the list of columns and first rows
    # Add the datetime field to each dictionary
    # Determine the name of the date column
    # If none found, try any column with datetime type
    # Form the datetime
    # Remove service fields
    date_col_candidates = ['DateTime', 'datetime', 'date', 'timestamp', 'index']
    lower_cols = {col.lower(): col for col in df.columns}
    found_col = None
    for candidate in date_col_candidates:
        if candidate in df.columns:
            found_col = candidate
            break
        elif candidate.lower() in lower_cols:
            found_col = lower_cols[candidate.lower()]
            break
    # If the date is in the index, use it
    if not found_col and df.index.name and df.index.name.lower() == 'index':
        try:
            df.index = pd.to_datetime(df.index, errors='coerce')
            date_index = df.index
        except Exception:
            pass
    if isinstance(df.index, pd.DatetimeIndex):
        date_index = df.index
    elif found_col:
        df[found_col] = pd.to_datetime(df[found_col], errors='coerce')
        df.set_index(found_col, inplace=True)
        date_index = df.index
    if date_index is not None:
        start_dt = pd.to_datetime(start) if start else date_index.min()
        end_dt = pd.to_datetime(end) if end else date_index.max()
        df = df[(date_index >= start_dt) & (date_index <= end_dt)]
    return df

def _should_draw_plot(args):
    """
    Returns True if the draw flag is set and is one of supported modes or should use default.
    Always returns True for 'show' mode to enable automatic plotting.
    """
    plot_modes = {"fastest", "fast", "plt", "mpl", "mplfinance", "plotly", "seaborn", "sb", "term"}

    # If it's show mode, always allow plotting (will use default 'fastest' if not specified)
    if hasattr(args, 'mode') and args.mode == 'show':
        return True

    # Otherwise check for valid draw parameter
    return hasattr(args, "draw") and args.draw is not None and args.draw in plot_modes

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

def _configure_terminal_plotting_mode(args):
    """Configure args for terminal plotting mode based on rule and draw settings."""
    # Handle special case when rule is explicitly set to OHLCV - this means display raw candlestick chart only
    if hasattr(args, 'rule') and args.rule and args.rule.upper() == 'OHLCV':
        args.raw_plot_only = True
        args.display_candlestick_only = True  # New flag to indicate candlestick only mode
        args.rule = None  # Clear the rule to use the raw data plot path

    # Special handling for AUTO rule with terminal plotting (-d term)
    if hasattr(args, 'draw') and args.draw == 'term' and hasattr(args, 'rule') and args.rule and args.rule.upper() == 'AUTO':
        print(f"Terminal plotting mode (-d term) with AUTO rule")
        args.auto_display_mode = True  # Flag to use separate field plotting for AUTO mode
        args.rule = 'AUTO'  # Ensure rule is set properly
    # For terminal plotting mode (-d term), always use OHLCV rule by default if rule not specified
    elif hasattr(args, 'draw') and args.draw == 'term' and (not hasattr(args, 'rule') or not args.rule):
        print("Terminal plotting mode (-d term) with default OHLCV display")
        args.raw_plot_only = True
        args.display_candlestick_only = True
        args.rule = 'OHLCV'
    elif hasattr(args, 'draw') and args.draw == 'term' and hasattr(args, 'rule') and args.rule:
        print(f"Terminal plotting mode (-d term) with {args.rule} rule")
        # Don't override user-specified rule like PHLD
        if args.rule.upper() == 'OHLCV':
            args.raw_plot_only = True
            args.display_candlestick_only = True
        # Special handling for PHLD rule to store original data for comparison
        elif args.rule.upper() == 'PHLD':
            args.compare_calculated = True  # Flag to indicate we want to compare calculated vs. original
            args.force_calculate = True  # Force calculation of indicators even if they exist in the file
            print("PHLD mode with calculation and visualization of indicators")

def _handle_indicator_mode(args):
    """Handle indicator files mode ('show ind')."""
    if not args.keywords or (len(args.keywords) == 1 and args.keywords[0] == 'help'):
        show_indicator_help()
        indicator_counts = count_indicator_files()
        print("\n=== AVAILABLE INDICATOR FILES ===")
        total_indicator_files = sum(indicator_counts.values())
        if total_indicator_files == 0:
            print("No indicator files found. Use export flags (--export-parquet, --export-csv, --export-json) to create indicator files first.")
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

def _handle_help_mode(args):
    """Handle help mode when no source is specified or source is 'help'."""
    show_help()
    source_counts = count_files_by_source(args)
    print("\n=== AVAILABLE DATA FILES ===")
    total_files = sum([count for source, count in source_counts.items() if source not in ['csv_converted_count']])
    
    # Add indicator files count
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
            if source == 'csv':
                csv_converted = source_counts.get('csv_converted_count', 0)
                print(f"  - {source.capitalize()}: {count} file(s) (including {csv_converted} converted from CSV)")
            elif source == 'other':
                print(f"  - Converted from CSV: {count} file(s)")
            else:
                if source == 'other':
                    print(f"  - Converted from CSV: {count} file(s)")
                else:
                    print(f"  - {source.capitalize()}: {count} file(s)")
                    
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

def handle_show_mode(args):
    """
    Handles the 'show' mode logic: finds files, displays info, and potentially triggers plot or indicator calculation.
    Returns timing and metrics data for execution summary.
    """
    # Info message about export flags
    print("Note: Export flags (--export-parquet, --export-csv, --export-json) are only allowed in demo mode. For real data, use the recommended workflow: download/convert, show+export, then show ind.")
    # Initialize timing and metrics tracking
    metrics = _initialize_metrics()
    
    # Always use raw data directories
    search_dirs = get_search_dirs(args)

    # Configure terminal plotting mode
    _configure_terminal_plotting_mode(args)

    # Handle indicator files mode
    if args.source == 'ind':
        return _handle_indicator_mode(args)

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

    # Date filtering and indicator calculation
    if len(found_files) == 1 and hasattr(args, 'rule') and args.rule:
        try:
            # Special handling for AUTO rule
            if args.rule.upper() == 'AUTO':
                return _handle_auto_display_mode(args, found_files, metrics)

            # Normal indicator calculation for other rules
            return _handle_indicator_calculation_mode(args, found_files, metrics)
        except Exception as e:
            print(f"Error processing file: {e}")
            traceback.print_exc()
            return metrics

    # Plot chart when one file found and no indicator calculation requested
    if len(found_files) > 1:
        print("To display a chart, re-run the command with more specific keywords:")
        print(f"Example: python run_analysis.py show {args.source} <additional_keywords>")
    elif len(found_files) == 1:
        return _handle_single_file_mode(args, found_files, metrics)
    
    return metrics

def _search_files(args, search_dirs):
    """Search for files based on source and keywords."""
    print(f"Searching for '{args.source}' files with keywords: {args.keywords}...")

    search_prefix = 'yfinance' if args.source == 'yf' else args.source
    search_keywords = [k.lower() for k in args.keywords]
    found_files = []
    
    for search_dir in search_dirs:
        if not search_dir.is_dir():
            print(f"Warning: Directory not found: {search_dir}")
            continue
        for item in search_dir.iterdir():
            if item.is_file() and item.suffix == '.parquet':
                filename_lower = item.name.lower()
                if search_prefix.lower() == 'csv':
                    is_match = (filename_lower.startswith('csv_') or 'csv_converted' in str(search_dir).lower())
                else:
                    is_match = filename_lower.startswith(search_prefix.lower() + '_')
                if is_match and all(keyword in filename_lower for keyword in search_keywords):
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
        print("Single CSV file found. Will automatically open chart in browser.")
        # Flag this as a single file processing for export
        args.single_file_mode = True
        # Set default rule to OHLCV when only one file is found
        if not hasattr(args, 'rule') or not args.rule:
            args.rule = 'OHLCV'
            # Apply the same logic as explicit --rule OHLCV
            args.raw_plot_only = True
            args.display_candlestick_only = True
            args.rule = None

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
            print(f"    Rows: Could not determine")
        if len(found_files) == 1:
            print(f"    Columns ({len(file_info['columns'])}): {', '.join(file_info['columns'])}")
            first_date = None
            last_date = None
            if file_info['first_date'] is not None:
                if isinstance(file_info['first_date'], pd.Timestamp):
                    first_date = file_info['first_date'].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    first_date = str(file_info['first_date'])
            if file_info['last_date'] is not None:
                if isinstance(file_info['last_date'], pd.Timestamp):
                    last_date = file_info['last_date'].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    last_date = str(file_info['last_date'])
            if first_date and last_date and first_date != last_date:
                print(f"    Date Range: {first_date} → {last_date}")
            elif first_date:
                print(f"    Date: {first_date}")
            if file_info['first_row'] is not None:
                print(f"    First Row: ", end="")
                if isinstance(file_info['first_row'], pd.Series):
                    values = []
                    for col_name, value in file_info['first_row'].items():
                        if isinstance(value, pd.Timestamp):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        values.append(f"{col_name}={value}")
                    print(" | ".join(values))
                else:
                    print(f"{file_info['first_row']}")
            if file_info['last_row'] is not None and file_info['num_rows'] > 1:
                print(f"    Last Row:  ", end="")
                if isinstance(file_info['last_row'], pd.Series):
                    values = []
                    for col_name, value in file_info['last_row'].items():
                        if isinstance(value, pd.Timestamp):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        values.append(f"{col_name}={value}")
                    print(" | ".join(values))
                else:
                    print(f"{file_info['last_row']}")
    print("-" * 40)

def _extract_point_size(file_info):
    """Extract point size from filename or use defaults."""
    point_size = None
    if 'point' in file_info['name'].lower():
        try:
            name_parts = file_info['name'].lower().split('point_')
            if len(name_parts) > 1:
                possible_point = name_parts[1].split('_')[0]
                point_size = float(possible_point)
        except (ValueError, IndexError):
            pass
    if point_size is None:
        if 'forex' in file_info['name'].lower() or 'fx' in file_info['name'].lower():
            point_size = 0.00001
        elif 'btc' in file_info['name'].lower() or 'crypto' in file_info['name'].lower():
            point_size = 0.01
        else:
            point_size = 0.01
        print(f"Point size not found in filename, using default: {point_size}")
    return point_size

    # Continue with the rest of the function...
    # Search for files
    found_files = _search_files(args, search_dirs)
    if not found_files:
        return metrics
    
    # Configure single file mode if applicable
    _configure_single_file_mode(args, found_files)
    
    # Display file information
    _display_file_info(found_files)

def _handle_auto_display_mode(args, found_files, metrics):
    """Handle AUTO rule display mode."""
    print(f"\n=== AUTO DISPLAY MODE ===")
    print(f"Loading file data and preparing to display all columns...")
    
    # Track data loading time
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
    
    start, end = _extract_datetime_filter_args(args)
    if start or end:
        df = _filter_dataframe_by_date(df, start, end)

    point_size = _extract_point_size(found_files[0])

    # Set a special flag for AUTO mode to be used by plotting functions
    args.auto_display_mode = True
    # Set column detection flag
    args.auto_detect_columns = True

    # Print all columns in the data
    datetime_column = None
    if isinstance(df.index, pd.DatetimeIndex):
        datetime_column = df.index.name or 'datetime'
    _print_indicator_result(df, 'AUTO', datetime_column=datetime_column)

    # Plot with all columns using the new fastest_auto_plot if requested
    if _should_draw_plot(args):
        metrics = _plot_auto_display(args, df, found_files[0], metrics)

    # Update point size info for AUTO mode
    metrics["point_size"] = point_size
    metrics["estimated_point"] = True
    
    return metrics

def _plot_auto_display(args, df, file_info, metrics):
    """Handle plotting for AUTO display mode."""
    # Track plotting time
    t_plot_start = time.perf_counter()
    
    draw_method = getattr(args, 'draw', 'fastest')
    
    # Check if running in Docker and force terminal mode if needed
    import os
    IN_DOCKER = os.environ.get('DOCKER_CONTAINER', False) or os.path.exists('/.dockerenv')
    disable_docker_detection = os.environ.get('DISABLE_DOCKER_DETECTION', 'false').lower() == 'true'
    
    if IN_DOCKER and not disable_docker_detection and draw_method not in ['term']:
        print(f"Docker detected: forcing draw mode from '{draw_method}' to 'term' (terminal plotting)")
        draw_method = 'term'
    
    print(f"\nDrawing AUTO display plot with method: '{draw_method}'...")
    try:
        if draw_method == 'fastest' and plot_auto_fastest_parquet is not None:
            output_html_path = os.path.join('results', 'plots', f"auto_fastest_{file_info['name'].replace('.parquet','.html')}")
            plot_auto_fastest_parquet(
                parquet_path=str(file_info['path']),
                output_html_path=output_html_path,
                trading_rule_name='AUTO',
                title=f"AUTO Fastest Plot: {file_info['name']}"
            )
            print(f"Successfully plotted all columns from '{file_info['name']}' using 'fastest' mode (fastest_auto_plot).")
        elif draw_method in ('sb', 'seaborn') and auto_plot_from_parquet is not None:
            print(f"Using seaborn_auto_plot for '{file_info['name']}'...")
            auto_plot_from_parquet(str(file_info['path']), plot_title=f"AUTO Seaborn Plot: {file_info['name']}")
            print(f"Successfully plotted all columns from '{file_info['name']}' using seaborn.")
        elif draw_method in ('mpl', 'mplfinance') and mpl_auto_plot_from_parquet is not None:
            print(f"Using mplfinance_auto_plot for '{file_info['name']}'...")
            mpl_auto_plot_from_parquet(str(file_info['path']))
            print(f"Successfully plotted all columns from '{file_info['name']}' using mplfinance.")
        elif draw_method == 'term' and auto_plot_from_dataframe is not None:
            print(f"Using terminal auto plotting for '{file_info['name']}'...")
            plot_title = f"AUTO Terminal Plot: {file_info['name']}"

            # Check if we should use separate field plotting with dots style
            if hasattr(args, 'auto_display_mode') and args.auto_display_mode:
                # Import the specific functions for parquet and CSV plotting
                try:
                    from src.plotting.term_auto_plot import auto_plot_parquet_fields, auto_plot_csv_fields

                    # Check if we're dealing with CSV or parquet file
                    if 'csv_converted' in str(file_info['path']).lower():
                        # For CSV-converted parquet files, use the parquet function but mention CSV source
                        print(f"Using separate field plotting for CSV-converted parquet file...")
                        auto_plot_parquet_fields(str(file_info['path']), f"AUTO: {file_info['name']} (CSV Source)", style="dots")
                    else:
                        # For direct parquet files
                        print(f"Using separate field plotting for parquet file...")
                        auto_plot_parquet_fields(str(file_info['path']), f"AUTO: {file_info['name']}", style="dots")

                    print(f"Successfully plotted all fields from '{file_info['name']}' using 'dots' style with separate charts.")
                except ImportError as e:
                    print(f"Could not import separate field plotting functions: {e}")
                    # Fallback to standard auto_plot_from_dataframe
                    auto_plot_from_dataframe(df, plot_title)
                    print(f"Fallback: Successfully plotted all columns from '{file_info['name']}' using terminal mode with unified chart.")
            else:
                # Use the standard auto_plot_from_dataframe function
                auto_plot_from_dataframe(df, plot_title)
                print(f"Successfully plotted all columns from '{file_info['name']}' using terminal mode with unified chart.")
        else:
            generate_plot = import_generate_plot()
            data_info = {
                "ohlcv_df": df,
                "data_source_label": f"{file_info['name']}",
                "rows_count": len(df),
                "columns_count": len(df.columns),
                "data_size_mb": file_info['size_mb'],
                "first_date": file_info['first_date'],
                "last_date": file_info['last_date'],
                "parquet_cache_used": True,
                "parquet_cache_file": str(file_info['path']),
                "all_columns": list(df.columns)  # Pass all columns to plotting function
            }
            selected_rule = "Auto_Display_All"  # Special rule name for plotting
            point_size = _extract_point_size(file_info)
            estimated_point = True
            generate_plot(args, data_info, df, selected_rule, point_size, estimated_point)
            print(f"Successfully plotted all columns from '{file_info['name']}' using '{draw_method}' mode.")
    
        # End plotting timing
        t_plot_end = time.perf_counter()
        metrics["plot_duration"] = t_plot_end - t_plot_start
        
    except Exception as e:
        print(f"Error plotting in AUTO mode: {e}")
        traceback.print_exc()
    
    return metrics

def _handle_indicator_calculation_mode(args, found_files, metrics):
    """Handle indicator calculation for single file with rule."""
    print(f"\n=== INDICATOR CALCULATION MODE ===")
    print(f"Loading file data and calculating indicator '{args.rule}' ...")
    
    # Track data loading time
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
    
    # Apply date filtering if requested
    start, end = _extract_datetime_filter_args(args)
    if start or end:
        df = _filter_dataframe_by_date(df, start, end)
    
    # Extract point size from filename or use defaults
    point_size = _extract_point_size(found_files[0])
    
    if not hasattr(args, 'mode'):
        args.mode = 'parquet'

    try:
        # Track indicator calculation time
        t_calc_start = time.perf_counter()
        # Calculate indicators
        result_df, selected_rule = calculate_indicator(args, df, point_size)
        t_calc_end = time.perf_counter()
        metrics["calc_duration"] = t_calc_end - t_calc_start
        
        # Update point size info
        metrics["point_size"] = point_size
        metrics["estimated_point"] = True
        
        datetime_column = None
        if isinstance(result_df.index, pd.DatetimeIndex):
            datetime_column = result_df.index.name or 'datetime'
        _print_indicator_result(result_df, args.rule, datetime_column=datetime_column)
        print(f"\nIndicator '{selected_rule.name}' calculated successfully.")

        # === ДОБАВЛЕНО: Экспорт индикаторов, если указаны флаги ===
        _handle_indicator_exports(args, result_df, {
            "ohlcv_df": df,
            "data_source_label": f"{found_files[0]['name']}",
            "rows_count": len(df),
            "columns_count": len(df.columns),
            "data_size_mb": found_files[0]['size_mb'],
            "first_date": found_files[0].get('first_date', None),
            "last_date": found_files[0].get('last_date', None),
            "parquet_cache_used": True,
            "parquet_cache_file": str(found_files[0]['path'])
        }, selected_rule)
        # === КОНЕЦ ДОБАВЛЕНИЯ ===

        # Draw plot after indicator calculation only if draw flag is set to supported mode
        if _should_draw_plot(args):
            metrics = _plot_indicator_calculation_result(args, df, result_df, found_files[0], selected_rule, point_size, metrics)
                        
        return metrics
    except Exception as e:
        print(f"Error calculating indicator: {e}")
        traceback.print_exc()
        return metrics

def _plot_indicator_calculation_result(args, original_df, result_df, file_info, selected_rule, point_size, metrics):
    """Handle plotting after indicator calculation."""
    # Track plotting time
    t_plot_start = time.perf_counter()
    
    print(f"\nDrawing plot after indicator calculation with method: '{args.draw}'...")
    try:
        # For terminal mode with PHLD rule
        if args.draw == 'term' and args.rule.upper() == 'PHLD':
            if auto_plot_from_dataframe is not None:
                # Check if indicators already exist in the loaded dataframe
                indicators_exist = all(col in original_df.columns for col in ['PPrice1', 'PPrice2', 'Direction'])
                calculation_type = "PRE-CALCULATED" if indicators_exist and not args.force_calculate else "CALCULATED NOW"

                print(f"\n=== {calculation_type} PHLD INDICATORS ===")
                print(f"Using terminal auto plotting for '{file_info['name']}' with PHLD rule...")
                plot_title = f"PHLD Terminal Plot: {file_info['name']} ({calculation_type})"
                # Use the auto_plot_from_dataframe function for terminal plotting
                auto_plot_from_dataframe(result_df, plot_title)

                # Extract and plot specific indicators
                if 'PPrice1' in result_df.columns and 'PPrice2' in result_df.columns:
                    print(f"\n--- Support and Resistance Levels (PPrice1 and PPrice2) - {calculation_type} ---")
                    support_resistance_df = result_df[['Open', 'PPrice1', 'PPrice2']].tail(30)
                    auto_plot_from_dataframe(support_resistance_df, f"Support and Resistance Levels ({calculation_type})")

                # Plot Direction indicator if available
                if 'Direction' in result_df.columns:
                    print(f"\n--- Direction Indicator - {calculation_type} ---")
                    direction_df = result_df[['Direction']].tail(30)
                    auto_plot_from_dataframe(direction_df, f"Direction Indicator ({calculation_type})")

                print(f"Successfully plotted PHLD indicators from '{file_info['name']}' using terminal mode.")
                print(f"Indicator source: {calculation_type}")
            else:
                print("Error: Terminal plotting functionality not available.")
        else:
            # Use the standard plotting for other modes
            generate_plot = import_generate_plot()
            data_info = {
                "ohlcv_df": original_df,
                "data_source_label": f"{file_info['name']}",
                "rows_count": len(original_df),
                "columns_count": len(original_df.columns),
                "data_size_mb": file_info['size_mb'],
                "first_date": file_info.get('first_date', None),
                "last_date": file_info.get('last_date', None),
                "parquet_cache_used": True,
                "parquet_cache_file": str(file_info['path'])
            }
            estimated_point = True
            generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
            print(f"Successfully plotted data from '{file_info['name']}' using '{args.draw}' mode after indicator calculation.")
        
        # End plotting timing
        t_plot_end = time.perf_counter()
        metrics["plot_duration"] = t_plot_end - t_plot_start
        
    except Exception as e:
        print(f"Error plotting after indicator calculation: {e}")
        traceback.print_exc()
        
    return metrics

def _handle_single_file_mode(args, found_files, metrics):
    """Handle single file mode without indicator calculation."""
    print(f"Found one file. Loading data and preparing to display...")
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
        
        data_info = {
            "ohlcv_df": df,
            "data_source_label": f"{found_files[0]['name']}",
            "rows_count": len(df),
            "columns_count": len(df.columns),
            "data_size_mb": found_files[0]['size_mb'],
            "first_date": found_files[0]['first_date'],
            "last_date": found_files[0]['last_date'],
            "parquet_cache_used": True,
            "parquet_cache_file": str(found_files[0]['path'])
        }
        
        point_size = _extract_point_size(found_files[0])

        # Add flag for single file mode
        args.single_file_mode = True

        # Just plot raw OHLCV data without indicator calculation
        if not hasattr(args, 'rule') or not args.rule:
            metrics = _plot_raw_ohlcv_data(args, df, data_info, found_files[0], point_size, metrics)
        else:
            # Calculate indicator if rule is specified
            metrics = _calculate_and_plot_indicator(args, df, data_info, found_files[0], point_size, metrics)
            
        # Return metrics for single file processing
        return metrics
    except Exception as e:
        print(f"Error plotting file: {e}")
        traceback.print_exc()
        return metrics

def _plot_raw_ohlcv_data(args, df, data_info, file_info, point_size, metrics):
    """Plot raw OHLCV data without indicator calculation."""
    # Just plot raw OHLCV data without indicator calculation
    selected_rule = 'Raw_OHLCV_Data'  # Default name for raw data display
    estimated_point = True
    generate_plot = import_generate_plot()
    draw_method = getattr(args, 'draw', 'fastest')
    print(f"Drawing raw OHLCV data chart using method: '{draw_method}'...")
    
    # Track plotting time for raw data
    t_plot_start = time.perf_counter()
    
    generate_plot(args, data_info, df, selected_rule, point_size, estimated_point)
    print(f"Successfully plotted raw OHLCV data from '{file_info['name']}'")
    
    # End plotting timing and update metrics
    t_plot_end = time.perf_counter()
    metrics["plot_duration"] = t_plot_end - t_plot_start
    metrics["point_size"] = point_size
    metrics["estimated_point"] = estimated_point
    
    return metrics

def _calculate_and_plot_indicator(args, df, data_info, file_info, point_size, metrics):
    """Calculate indicator and plot for single file."""
    # Calculate indicator if rule is specified
    print(f"Calculating indicator '{args.rule}' for the file...")
    if not hasattr(args, 'mode'):
        args.mode = 'parquet'
    
    # Track indicator calculation time
    t_calc_start = time.perf_counter()
    result_df, selected_rule = calculate_indicator(args, df, point_size)
    t_calc_end = time.perf_counter()
    metrics["calc_duration"] = t_calc_end - t_calc_start

    # Export indicator data if requested
    _handle_indicator_exports(args, result_df, data_info, selected_rule)

    # Draw plot with indicator
    estimated_point = True
    generate_plot = import_generate_plot()
    draw_method = getattr(args, 'draw', 'fastest')
    print(f"Drawing plot with indicator using method: '{draw_method}'...")
    generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
    print(f"Successfully plotted data with indicator from '{file_info['name']}'")
    
    return metrics

def _handle_indicator_exports(args, result_df, data_info, selected_rule):
    """Handle indicator data exports if requested."""
    if hasattr(args, 'export_parquet') and args.export_parquet:
        print(f"Exporting indicator data to parquet file...")
        export_info = export_indicator_to_parquet(result_df, data_info, selected_rule, args)
        if export_info["success"]:
            print(f"Indicator data exported to: {export_info['output_file']}")
        else:
            print(f"Failed to export indicator data: {export_info['error_message']}")
    
    if hasattr(args, 'export_csv') and args.export_csv:
        print(f"Exporting indicator data to CSV file...")
        export_info = export_indicator_to_csv(result_df, data_info, selected_rule, args)
        if export_info["success"]:
            print(f"Indicator data exported to: {export_info['output_file']}")
        else:
            print(f"Failed to export indicator data: {export_info['error_message']}")
    
    if hasattr(args, 'export_json') and args.export_json:
        print(f"Exporting indicator data to JSON file...")
        export_info = export_indicator_to_json(result_df, data_info, selected_rule, args)
        if export_info["success"]:
            print(f"Indicator data exported to: {export_info['output_file']}")
        else:
            print(f"Failed to export indicator data: {export_info['error_message']}")

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

def show_indicator_help():
    """
    Displays help for the 'show ind' mode with colorful formatting.
    """
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== SHOW INDICATOR FILES HELP ==={Style.RESET_ALL}")
    print(f"The {Fore.GREEN}'show ind'{Style.RESET_ALL} mode allows you to list and inspect calculated indicator files.")
    print(f"{Fore.YELLOW}Usage:{Style.RESET_ALL} python run_analysis.py show ind [format] [keywords...] [-d backend] [--rule RULE]")

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

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Note:{Style.RESET_ALL}")
    print(f"  - {Fore.MAGENTA}Parquet files{Style.RESET_ALL} can be displayed as charts with all drawing backends")
    print(f"  - {Fore.MAGENTA}CSV and JSON files{Style.RESET_ALL} are displayed as formatted terminal output")
    print(f"  - Single parquet file will automatically open chart with specified backend")
    print(f"  - Multiple parquet files can be plotted individually when using -d flag")

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

def _handle_multiple_parquet_files(args, found_files, format_filter, metrics):
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
                single_metrics = _show_single_indicator_file(file_info, args)
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
        
        # For single file in each format, show more details
        format_files = [f for f in found_files if f['format'] == file_info['format']]
        if len(format_files) == 1:
            if file_info['format'] == 'parquet':
                metadata = get_parquet_metadata(file_info['path'])
                if metadata['num_rows'] != -1:
                    print(f"    Rows: {metadata['num_rows']:,}")
                print(f"    Columns ({len(metadata['columns'])}): {', '.join(metadata['columns'])}")
            elif file_info['format'] in ['csv', 'json']:
                # Show first few lines for CSV/JSON files
                file_metrics = _show_file_preview(file_info)
                # Update metrics for text file display
                metrics["data_fetch_duration"] += file_metrics.get("data_fetch_duration", 0)
                metrics["rows_count"] += file_metrics.get("rows_count", 0)
                if file_metrics.get("columns_count", 0) > metrics["columns_count"]:
                    metrics["columns_count"] = file_metrics.get("columns_count", 0)
                metrics["data_size_mb"] += file_metrics.get("data_size_mb", 0)

    return metrics

def handle_indicator_show_mode(args):
    """
    Handles the 'show ind' mode logic for indicator files.
    Returns timing and metrics data for execution summary.
    """
    # Initialize timing and metrics tracking
    metrics = _initialize_metrics()
    
    # Set indicator mode flag to ensure proper behavior
    args.indicator_mode = True
    
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
            single_metrics = _show_single_indicator_file(file_info, args)
        elif file_format in ['csv', 'json']:
            print(f"Single {file_format} indicator file found. Displaying content.")
            # For single CSV/JSON files, show content with date filtering if applicable
            single_metrics = _show_single_text_indicator_file(file_info, args)
        
        # Merge metrics
        for key in single_metrics:
            if key in metrics:
                metrics[key] = single_metrics[key]
        return metrics
    
    # Handle multiple parquet files with drawing backend
    handled, metrics = _handle_multiple_parquet_files(args, found_files, format_filter, metrics)
    if handled:
        return metrics
    
    # Display file list for multiple files
    return _display_indicator_file_list(found_files, metrics)

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
    
    # Apply date filtering if start/end flags are provided
    start, end = _extract_datetime_filter_args(args)
    if start or end:
        print(f"Applying date filtering to indicator data...")
        original_len = len(df)
        df = _filter_dataframe_by_date(df, start, end)
        print(f"After date filtering: {len(df)} rows remaining (from {original_len})")
    
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
    
    plot_end_time = time.time()
    metrics["plot_duration"] = plot_end_time - plot_start_time
    
    return metrics

def _show_single_indicator_file(file_info, args):
    """
    Shows a single indicator file with appropriate visualization.
    Returns timing and metrics data.
    """
    # Initialize timing and metrics tracking
    metrics = _initialize_metrics()
    
    file_path = file_info['path']
    file_format = file_info['format']
    
    if file_format == 'parquet':
        # Load parquet and show chart using the same plotting system as other commands
        try:
            # Track data loading time
            load_start_time = time.time()
            df = pd.read_parquet(file_path)
            # === ДОБАВЛЕНО: если есть колонка DateTime, делаем её индексом ===
            if 'DateTime' in df.columns:
                df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
                df = df.set_index('DateTime')
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
            
            # Handle plotting
            metrics = _plot_indicator_parquet_file(args, df, file_info, metrics)
                
        except Exception as e:
            print(f"Error loading parquet file: {e}")
            traceback.print_exc()
    
    elif file_format in ['csv', 'json']:
        # Show file content in terminal
        file_metrics = _show_file_preview(file_info)
        # Merge metrics from file preview
        for key in file_metrics:
            if key in metrics:
                metrics[key] = file_metrics[key]
    
    return metrics

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

def _show_json_dict_preview(data, metrics):
    """Display JSON dictionary data preview."""
    metrics["rows_count"] = len(data)
    metrics["columns_count"] = len(data) if data else 0
    
    print(f"{Fore.CYAN}Data structure:{Style.RESET_ALL} Dictionary with {len(data)} keys")
    if data:
        print(f"{Fore.CYAN}Keys:{Style.RESET_ALL} {', '.join(data.keys())}")
        print()
        
        # Show first few values for each key
        for key, value in list(data.items())[:5]:
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

def _show_json_list_preview(data, metrics):
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
        
        # Show first few records
        for i, record in enumerate(data[:5]):
            print(f"{Fore.GREEN}Record {i+1}:{Style.RESET_ALL}")
            if isinstance(record, dict):
                for key, value in record.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {record}")
            print()
        
        if len(data) > 5:
            print(f"{Fore.BLACK}{Style.DIM}... and {len(data) - 5} more records{Style.RESET_ALL}")
    
    return metrics

def _show_json_other_preview(data, metrics):
    """Display other JSON data types preview."""
    import json
    
    # Other data types
    metrics["rows_count"] = 1
    metrics["columns_count"] = 1
    
    print(f"{Fore.CYAN}Data type:{Style.RESET_ALL} {type(data).__name__}")
    data_str = json.dumps(data, indent=2)
    if len(data_str) > 1000:
        print(data_str[:1000] + f"\n{Fore.BLACK}{Style.DIM}... (truncated){Style.RESET_ALL}")
    else:
        print(data_str)
    
    return metrics

def _show_json_file_preview(file_path, metrics):
    """Display JSON file preview and update metrics."""
    import json
    
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

def _show_file_preview(file_info):
    """
    Shows a preview of CSV or JSON file content.
    Returns timing and metrics data.
    """
    # Initialize timing and metrics tracking
    metrics = _initialize_metrics()
    
    file_path = file_info['path']
    file_format = file_info['format']
    
    # Update file size metrics
    metrics["data_size_mb"] = file_info['size_mb']
    metrics["data_size_bytes"] = int(file_info['size_mb'] * 1024 * 1024)
    
    try:
        # Track data loading time
        load_start_time = time.time()
        
        if file_format == 'csv':
            metrics = _show_csv_file_preview(file_path, metrics)
        elif file_format == 'json':
            metrics = _show_json_file_preview(file_path, metrics)
        
        load_end_time = time.time()
        metrics["data_fetch_duration"] = load_end_time - load_start_time
                
    except Exception as e:
        print(f"Error reading {file_format} file: {e}")
        traceback.print_exc()
    
    return metrics

def _show_single_text_indicator_file(file_info, args):
    """
    Shows a single CSV or JSON indicator file with date filtering support.
    Returns timing and metrics data.
    """
    # Initialize timing and metrics tracking
    metrics = _initialize_metrics()
    
    file_path = file_info['path']
    file_format = file_info['format']
    
    # Update file size metrics
    metrics["data_size_mb"] = file_info['size_mb']
    metrics["data_size_bytes"] = int(file_info['size_mb'] * 1024 * 1024)
    
    try:
        # Track data loading time
        load_start_time = time.time()
        
        # Extract date filtering parameters
        start, end = _extract_datetime_filter_args(args)
        
        if file_format == 'csv':
            df = pd.read_csv(file_path)
            load_end_time = time.time()
            
            # Apply date filtering if requested
            if start or end:
                print(f"Applying date filtering to CSV data...")
                original_len = len(df)
                df = _filter_dataframe_by_date(df, start, end)
                print(f"After date filtering: {len(df)} rows remaining (from {original_len})")
            
            # Update metrics
            metrics["data_fetch_duration"] = load_end_time - load_start_time
            metrics["rows_count"] = len(df)
            metrics["columns_count"] = len(df.columns)
            
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== CSV INDICATOR FILE CONTENT ==={Style.RESET_ALL}")
            print(f"{Fore.CYAN}Total rows:{Style.RESET_ALL} {len(df):,}")
            print(f"{Fore.CYAN}Columns ({len(df.columns)}):{Style.RESET_ALL} {', '.join(df.columns)}")
            print()
            # List of possible date column names
            # Find the first suitable column (case-insensitive)
            # If the index is called 'index' and contains dates, use it
            # If the date is in the index, use it
            # Add a date column and a row number column
            # Properly format datetime for Series and DatetimeIndex
            # Form a date column for display
            # Determine the name of the date column
            # If the date is in the index, use it
            # Add a date column and a row number column
            # Properly format datetime for Series and DatetimeIndex
            # reset_index is required so that the date is not lost
            # Diagnostics: print the list of columns and first rows
            # Add the datetime field to each dictionary
            # Determine the name of the date column
            # If none found, try any column with datetime type
            # Form the datetime
            # Remove service fields
            date_col_candidates = ['DateTime', 'datetime', 'date', 'timestamp', 'index']
            lower_cols = {col.lower(): col for col in df.columns}
            found_col = None
            for candidate in date_col_candidates:
                if candidate in df.columns:
                    found_col = candidate
                    break
                elif candidate.lower() in lower_cols:
                    found_col = lower_cols[candidate.lower()]
                    break
            # If the date is in the index, use it
            if not found_col and df.index.name and df.index.name.lower() == 'index':
                try:
                    df.index = pd.to_datetime(df.index, errors='coerce')
                    date_index = df.index
                except Exception:
                    pass
            if isinstance(df.index, pd.DatetimeIndex):
                date_index = df.index
            elif found_col:
                df[found_col] = pd.to_datetime(df[found_col], errors='coerce')
                df.set_index(found_col, inplace=True)
                date_index = df.index
            if date_index is not None:
                start_dt = pd.to_datetime(start) if start else date_index.min()
                end_dt = pd.to_datetime(end) if end else date_index.max()
                df = df[(date_index >= start_dt) & (date_index <= end_dt)]
            # Explicitly output all records with numbers
            df_to_show = df.copy()
            df_to_show.insert(0, 'rownum', range(1, len(df_to_show)+1))
            if hasattr(df_to_show.index, 'name') and df_to_show.index.name:
                df_to_show.insert(1, 'datetime', df_to_show.index)
            print(df_to_show.to_string(index=False))
        
        elif file_format == 'json':
            import json
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
                        print(f"After date filtering: {len(df)} rows remaining (from {original_len})")
                        # reset_index is required so that the date is not lost
                        df = df.reset_index(drop=False)
                        data = df.to_dict('records')
                        # Diagnostics: print the list of columns and first rows
                        print(f"DEBUG: DataFrame columns after filtering: {list(df.columns)}")
                        print(f"DEBUG: First rows after filtering:\n{df.head()}\n")
                    else:
                        print(f"Cannot apply date filtering to this JSON structure")
                except Exception as e:
                    print(f"Warning: Could not apply date filtering to JSON: {e}")
            # Create datetime
            if isinstance(data, list) and data and isinstance(data[0], dict):
                # Determine the date column name
                date_col_candidates = ['index', 'date_str', 'DateTime', 'datetime', 'date', 'timestamp']
                # If none found, try any column with datetime type
                for rec in data:
                    found_col = None
                    for candidate in date_col_candidates:
                        if candidate in rec and rec[candidate] is not None:
                            found_col = candidate
                            break
                    # If not found, try any column with date
                    if not found_col:
                        for k, v in rec.items():
                            try:
                                if pd.notnull(v) and pd.to_datetime(v, errors='coerce') is not pd.NaT:
                                    found_col = k
                                    break
                            except Exception:
                                continue
                    # Create datetime
                    if found_col:
                        try:
                            rec['datetime'] = pd.to_datetime(rec[found_col]).strftime('%Y-%m-%d %H:%M:%S')
                        except Exception:
                            rec['datetime'] = str(rec[found_col])
                    else:
                        rec['datetime'] = None
                    # Remove service fields
                    for svc in ['index', 'date_str']:
                        if svc in rec:
                            del rec[svc]
                # Explicitly output all records with numbers
                for i, rec in enumerate(data, 1):
                    print(f"Record {i}:")
                    for k, v in rec.items():
                        print(f"  {k}: {v}")
                    print()
    
    except Exception as e:
        print(f"Error reading {file_format} file: {e}")
        traceback.print_exc()
    
    return metrics

