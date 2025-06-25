# src/export/parquet_export.py

"""
Module for exporting indicator data to parquet files.
Handles the creation of parquet files with indicator data based on original OHLCV data.
All comments are in English.
"""

import os
import pandas as pd
from pathlib import Path
from ..common import logger


def export_indicator_to_parquet(result_df, data_info, selected_rule, args):
    """
    Exports the calculated indicator data to a parquet file.

    Creates a new parquet file based on the original data source, adding
    only necessary OHLCV and timestamp fields along with the calculated indicator values.
    The new file has the same name as the original but with the rule name as a postfix.

    In show mode, export happens only when a single file is being processed.

    Args:
        result_df (pandas.DataFrame): DataFrame containing the calculated indicator data
        data_info (dict): Information about the data source
        selected_rule (str): The trading rule used for the calculation
        args (argparse.Namespace): Command-line arguments

    Returns:
        dict: Dictionary with information about the export process
    """
    # Initialize result info
    export_info = {
        "success": False,
        "output_file": None,
        "error_message": None
    }

    # Log the mode and export flag for debugging
    logger.print_debug(f"Export called: mode={args.mode}, export_flag={getattr(args, 'export_parquet', False)}, single_file={getattr(args, 'single_file_mode', False)}")

    # Only proceed if export_parquet flag is set
    if not getattr(args, 'export_parquet', False):
        export_info["error_message"] = "Export flag not set"
        return export_info

    # Check if result_df is valid
    if result_df is None or result_df.empty:
        export_info["error_message"] = "No data to export - result DataFrame is empty"
        logger.print_error(export_info["error_message"])
        return export_info

    # Determine base filename from parquet_cache_file or create one based on ticker/interval
    original_file = data_info.get("parquet_cache_file")

    if not original_file:
        # Create a filename based on ticker and interval if no cache file exists
        if getattr(args, 'mode', None) == 'demo':
            filename = "DEMO"
        else:
            ticker = args.ticker if hasattr(args, 'ticker') and args.ticker else "UNKNOWN"
            interval = args.interval if hasattr(args, 'interval') and args.interval else "D1"
            filename = f"{ticker}_{interval}"
    else:
        original_file = Path(original_file)
        filename = original_file.stem

    # Create output directory for indicators
    output_dir = Path("data/indicators/parquet")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create the new filename with the rule postfix
    # Handle the case when selected_rule is an Enum or an object with a name attribute
    if hasattr(selected_rule, 'name'):
        rule_shortname = selected_rule.name.replace("_", "")
    else:
        rule_shortname = str(selected_rule).replace("_", "")

    output_file = output_dir / f"{filename}_{rule_shortname}.parquet"
    logger.print_debug(f"Output file will be: {output_file}")

    try:
        # Prepare the data for export
        # Select only OHLCV data and add the indicator columns
        ohlcv_columns = ['open', 'high', 'low', 'close', 'volume']

        # Ensure all OHLCV columns exist (case-insensitive)
        available_columns = [col.lower() for col in result_df.columns]

        # Map between possible column names and standardized names
        column_mapping = {
            'open': ['open', 'o'],
            'high': ['high', 'h'],
            'low': ['low', 'l'],
            'close': ['close', 'c'],
            'volume': ['volume', 'vol', 'v']
        }

        # Create a dictionary to map original column names to standardized names
        actual_columns = {}
        for std_name, possible_names in column_mapping.items():
            for col in result_df.columns:
                if col.lower() in possible_names:
                    actual_columns[std_name] = col
                    break

        # Check if we have all required columns
        for col in ohlcv_columns:
            if col not in actual_columns:
                logger.print_warning(f"Column '{col}' not found in result DataFrame")

        # Select columns to export
        export_columns = list(actual_columns.values())

        # Identify indicator columns (all columns not in OHLCV and not in the index)
        indicator_columns = [col for col in result_df.columns
                           if col not in export_columns and col not in result_df.index.names]

        export_columns.extend(indicator_columns)

        # Prepare the export DataFrame
        export_df = result_df[export_columns].copy()

        # === Date column name unification ===
        date_col_candidates = ['DateTime', 'datetime', 'Timestamp', 'timestamp', 'date', 'index']
        found_date_col = None
        for candidate in date_col_candidates:
            if candidate in export_df.columns:
                found_date_col = candidate
                break
        # If found, rename to 'DateTime'
        if found_date_col and found_date_col != 'DateTime':
            export_df.rename(columns={found_date_col: 'DateTime'}, inplace=True)
        # If index is DatetimeIndex and no 'DateTime' column exists, add it
        if isinstance(export_df.index, pd.DatetimeIndex):
            if 'DateTime' not in export_df.columns:
                export_df.insert(0, 'DateTime', export_df.index)
            export_df = export_df.reset_index(drop=True)
        # === End of block ===

        # Export to parquet
        export_df.to_parquet(output_file)

        # Update export info
        export_info["success"] = True
        export_info["output_file"] = str(output_file)
        logger.print_success(f"Indicator data exported to: {output_file}")

    except Exception as e:
        export_info["error_message"] = f"Failed to export indicator data: {str(e)}"
        logger.print_error(export_info["error_message"])

    return export_info
