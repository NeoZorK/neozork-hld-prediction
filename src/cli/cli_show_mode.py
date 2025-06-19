# -*- coding: utf-8 -*-
# src/cli/cli_show_mode.py

"""
Refactored CLI show mode with modular structure.
This is the main entry point that delegates to specialized modules.
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
from .cli_show_indicators import handle_indicator_mode
from .cli_show_common import _initialize_metrics

def handle_show_mode(args):
    """
    Main entry point for show mode - delegates to appropriate handlers.
    """
    # Handle indicator files mode
    if hasattr(args, 'source') and args.source == 'ind':
        return handle_indicator_mode(args)
    
    # For other modes, use the original logic from cli_show_mode_new
    from .cli_show_mode_new import handle_show_mode as handle_original_show_mode
    return handle_original_show_mode(args)

# Keep backward compatibility
show_mode_handler = handle_show_mode

# Functions needed for backward compatibility and tests
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

def import_generate_plot():
    """
    Dynamically imports the generate_plot function for plotting.
    """
    try:
        from ..plotting.plotting_generation import generate_plot
        return generate_plot
    except ImportError:
        return None

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
    Returns the relevant columns to output for the given rule.
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
        if all_columns:
            datetime_cols = [col for col in all_columns if col.lower() in ['datetime', 'date', 'time', 'timestamp']]
            prediction_cols = [col for col in all_columns if any(pred.lower() in col.lower()
                              for pred in ['predicted', 'pressure', 'vector', 'signal', 'direction'])]
            other_cols = [col for col in all_columns if col not in datetime_cols and col not in prediction_cols]
            return datetime_cols + prediction_cols + other_cols
        return base_cols
    elif canonical_rule in ['Predict_High_Low_Direction']:
        return base_cols + ['PPrice1', 'PPrice2', 'Direction']
    elif canonical_rule in ['Pressure_Vector']:
        return base_cols
    elif canonical_rule in ['Support_Resistants']:
        return base_cols + ['PPrice1', 'PColor1', 'PPrice2', 'PColor2']
    else:
        return base_cols

def _print_indicator_result(df, rule_name, datetime_column=None):
    """
    Prints the indicator calculation result with proper formatting.
    """
    print(f"Calculated indicator: {rule_name}")
    print(f"DataFrame shape: {df.shape}")
    if not df.empty:
        print("First few rows:")
        print(df.head())
    else:
        print("No data to display")

def _should_draw_plot(args):
    """
    Determines if a plot should be drawn based on args.
    """
    return hasattr(args, "draw") and args.draw is not None

def _configure_terminal_plotting_mode(args):
    """
    Configures terminal plotting mode if needed.
    """
    if hasattr(args, "draw") and args.draw == "term":
        os.environ["MPLBACKEND"] = "Agg"
