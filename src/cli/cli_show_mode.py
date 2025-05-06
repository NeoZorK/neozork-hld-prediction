# -*- coding: utf-8 -*-
# src/core/cli_show_mode.py

import os
from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd
import sys
import traceback

# Import for indicator calculation; fallback for different relative import
try:
    from src.calculation.indicator_calculation import calculate_indicator
except ImportError:
    from src.calculation.indicator_calculation import calculate_indicator

def show_help():
    """
    Displays help for the 'show' mode.
    """
    print("\n=== SHOW MODE HELP ===")
    print("The 'show' mode allows you to list and inspect cached data files.")
    print("Usage: python run_analysis.py show <source> [keywords...]")
    print("\nAvailable sources:")
    print("  - csv: Converted CSV data files")
    print("  - yfinance/yf: Yahoo Finance data files")
    print("  - polygon: Polygon.io API data files")
    print("  - binance: Binance API data files")
    print("\nExamples:")
    print("  python run_analysis.py show                  # Show statistics for all sources")
    print("  python run_analysis.py show yf               # List all Yahoo Finance files")
    print("  python run_analysis.py show yf aapl          # List YF files containing 'aapl'")
    print("  python run_analysis.py show binance btc MN1  # List Binance files with 'btc' and timeframe 'MN1'")
    print("\nDate filtering:")
    print("  --start, --end or --show-start, --show-end for date range filtering.")

def import_generate_plot():
    """
    Dynamically imports the generate_plot function for plotting.
    """
    from ..plotting.plotting_generation import generate_plot
    return generate_plot

SEARCH_DIRS = [
    Path("data/raw_parquet"),
    Path("data/cache/csv_converted")
]

def count_files_by_source():
    """
    Counts Parquet files by their source prefix (yfinance, csv, polygon, binance).
    """
    source_counts = {
        'yfinance': 0,
        'csv': 0,
        'polygon': 0,
        'binance': 0,
        'other': 0,
        'csv_converted_count': 0
    }
    for search_dir in SEARCH_DIRS:
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

def _get_relevant_columns_for_rule(rule_name: str) -> list:
    """
    Returns the relevant columns to output for the given rule,
    according to clarified user logic.
    """
    base_cols = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'HL', 'Pressure', 'PV']
    rule_aliases_map = {
        'PHLD': 'Predict_High_Low_Direction',
        'PV': 'Pressure_Vector',
        'SR': 'Support_Resistants'
    }
    rule_name_upper = rule_name.upper()
    canonical_rule = rule_aliases_map.get(rule_name_upper, rule_name)
    if canonical_rule in ['Predict_High_Low_Direction']:
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
    columns_to_show = _get_relevant_columns_for_rule(rule_name)
    columns_to_show_existing = [col for col in columns_to_show if col in df_to_show.columns]
    row_count = df_to_show.shape[0]
    print(f"\n=== CALCULATED INDICATOR DATA === ({row_count} rows in selected range)")
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
    Filters dataframe by start/end date. Index must be DatetimeIndex or column 'DateTime'/'datetime' must exist.
    """
    if df.empty:
        return df
    date_index = None
    if isinstance(df.index, pd.DatetimeIndex):
        date_index = df.index
    elif 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
        df.set_index('DateTime', inplace=True)
        date_index = df.index
    elif 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        df.set_index('datetime', inplace=True)
        date_index = df.index
    if date_index is not None:
        start_dt = pd.to_datetime(start) if start else date_index.min()
        end_dt = pd.to_datetime(end) if end else date_index.max()
        df = df[(date_index >= start_dt) & (date_index <= end_dt)]
    return df

def _should_draw_plot(args):
    """
    Returns True if the draw flag is set and is one of supported modes.
    """
    plot_modes = {"fastest", "fast", "plt", "mpl", "mplfinance", "plotly", "seaborn", "sb"}
    return hasattr(args, "draw") and args.draw is not None and args.draw in plot_modes

def handle_show_mode(args):
    """
    Handles the 'show' mode logic: finds files, displays info, and potentially triggers plot or indicator calculation.
    """
    if not args.source or args.source == 'help':
        show_help()
        source_counts = count_files_by_source()
        print("\n=== AVAILABLE DATA FILES ===")
        total_files = sum([count for source, count in source_counts.items() if source not in ['csv_converted_count']])
        if total_files == 0:
            print("No data files found. Use other modes to download or import data first.")
            print("\nTo convert a CSV file, use the 'csv' mode:")
            print("  python run_analysis.py csv --csv-file path/to/data.csv --point 0.01")
            return
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
        print("\nTo view specific files, use: python run_analysis.py show <source> [keywords...]")
        return

    print(f"Searching for '{args.source}' files with keywords: {args.keywords}...")

    search_prefix = 'yfinance' if args.source == 'yf' else args.source
    search_keywords = [k.lower() for k in args.keywords]
    found_files = []
    for search_dir in SEARCH_DIRS:
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
    if not found_files:
        return
    elif len(found_files) == 1:
        print("Single CSV file found. Will automatically open chart in browser.")

    found_files.sort(key=lambda x: x['name'])
    print("-" * 40)
    for idx, file_info in enumerate(found_files):
        metadata = get_parquet_metadata(file_info['path'])
        file_info.update(metadata)
        print(f"[{idx}] {file_info['name']}")
        print(f"    Size: {file_info['size_mb']:.3f} MB")
        if metadata['num_rows'] != -1:
            print(f"    Rows: {file_info['num_rows']:,}")
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

    # Date filtering and indicator calculation
    if len(found_files) == 1 and hasattr(args, 'rule') and args.rule:
        try:
            print(f"\n=== INDICATOR CALCULATION MODE ===")
            print(f"Loading file data and calculating indicator '{args.rule}' ...")
            df = pd.read_parquet(found_files[0]['path'])
            start, end = _extract_datetime_filter_args(args)
            if start or end:
                df = _filter_dataframe_by_date(df, start, end)
            point_size = None
            if 'point' in found_files[0]['name'].lower():
                try:
                    name_parts = found_files[0]['name'].lower().split('point_')
                    if len(name_parts) > 1:
                        possible_point = name_parts[1].split('_')[0]
                        point_size = float(possible_point)
                except (ValueError, IndexError):
                    pass
            if point_size is None:
                if 'forex' in found_files[0]['name'].lower() or 'fx' in found_files[0]['name'].lower():
                    point_size = 0.00001
                elif 'btc' in found_files[0]['name'].lower() or 'crypto' in found_files[0]['name'].lower():
                    point_size = 0.01
                else:
                    point_size = 0.01
                print(f"Point size not found in filename, using default: {point_size}")
            if not hasattr(args, 'mode'):
                args.mode = 'parquet'
            result_df, selected_rule = calculate_indicator(args, df, point_size)
            datetime_column = None
            if isinstance(result_df.index, pd.DatetimeIndex):
                datetime_column = result_df.index.name or 'datetime'
            _print_indicator_result(result_df, args.rule, datetime_column=datetime_column)
            print(f"\nIndicator '{selected_rule.name}' calculated and shown above.")
            # Draw plot after indicator calculation only if draw flag is set to supported mode
            if _should_draw_plot(args):
                print(f"\nDrawing plot after indicator calculation with method: '{args.draw}'...")
                try:
                    generate_plot = import_generate_plot()
                    data_info = {
                        "ohlcv_df": df,
                        "data_source_label": f"Parquet file: {found_files[0]['name']}",
                        "rows_count": len(df),
                        "columns_count": len(df.columns),
                        "data_size_mb": found_files[0]['size_mb'],
                        "first_date": found_files[0]['first_date'],
                        "last_date": found_files[0]['last_date'],
                        "parquet_cache_used": True,
                        "parquet_cache_file": str(found_files[0]['path'])
                    }
                    estimated_point = True
                    generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
                    print(f"Successfully plotted data from '{found_files[0]['name']}' using '{args.draw}' mode after indicator calculation.")
                except Exception as e:
                    print(f"Error plotting after indicator calculation: {e}")
                    traceback.print_exc()
            return
        except Exception as e:
            print(f"Error calculating indicator: {e}")
            traceback.print_exc()
            return

    # Plot chart when one file found and no indicator calculation requested
    if len(found_files) > 1:
        print("To display a chart, re-run the command with more specific keywords:")
        print(f"Example: python run_analysis.py show {args.source} <additional_keywords>")
    elif len(found_files) == 1:
        # Only plot if draw flag is specified and is supported
        if not _should_draw_plot(args):
            return
        print(f"Found one file. Triggering plot with method: '{args.draw}'...")
        print(f"Loading file data and triggering plot with method: '{args.draw}'...")
        try:
            df = pd.read_parquet(found_files[0]['path'])
            data_info = {
                "ohlcv_df": df,
                "data_source_label": f"Parquet file: {found_files[0]['name']}",
                "rows_count": len(df),
                "columns_count": len(df.columns),
                "data_size_mb": found_files[0]['size_mb'],
                "first_date": found_files[0]['first_date'],
                "last_date": found_files[0]['last_date'],
                "parquet_cache_used": True,
                "parquet_cache_file": str(found_files[0]['path'])
            }
            point_size = None
            if 'point' in found_files[0]['name'].lower():
                try:
                    name_parts = found_files[0]['name'].lower().split('point_')
                    if len(name_parts) > 1:
                        possible_point = name_parts[1].split('_')[0]
                        point_size = float(possible_point)
                except (ValueError, IndexError):
                    pass
            if point_size is None:
                if 'forex' in found_files[0]['name'].lower() or 'fx' in found_files[0]['name'].lower():
                    point_size = 0.00001
                elif 'btc' in found_files[0]['name'].lower() or 'crypto' in found_files[0]['name'].lower():
                    point_size = 0.01
                else:
                    point_size = 0.01
                print(f"Point size not found in filename, using default: {point_size}")
            generate_plot = import_generate_plot()
            result_df = None
            selected_rule = args.rule if hasattr(args, 'rule') else 'Predict_High_Low_Direction'
            estimated_point = True
            generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
            print(f"Successfully plotted data from '{found_files[0]['name']}' using '{args.draw}' mode")
        except Exception as e:
            print(f"Error plotting file: {e}")
            traceback.print_exc()