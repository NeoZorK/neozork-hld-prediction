# src/export/json_export.py

"""
Module for exporting indicator data to JSON files.
Handles the creation of JSON files with indicator data based on original OHLCV data.
All comments are in English.
"""

import os
import pandas as pd
import json
from pathlib import Path
from src.common import logger


def export_indicator_to_json(result_df, data_info, selected_rule, args):
    """
    Exports the calculated indicator data to a JSON file.

    Creates a new JSON file in the data/indicators/json directory based on the 
    original data source, adding only necessary OHLCV and timestamp fields 
    along with the calculated indicator values.

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
    logger.print_debug(f"JSON Export called: mode={args.mode}, export_flag={getattr(args, 'export_json', False)}")

    # Only proceed if export_json flag is set
    if not getattr(args, 'export_json', False):
        export_info["error_message"] = "Export JSON flag not set"
        return export_info

    # Check if result_df is valid
    if result_df is None or result_df.empty:
        export_info["error_message"] = "No data to export - result DataFrame is empty"
        logger.print_error(export_info["error_message"])
        return export_info

    # Determine base filename from data_info or create one based on ticker/interval
    original_file = data_info.get("parquet_cache_file") or data_info.get("csv_file")

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

    # Create output directory
    output_dir = Path("data/indicators/json")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create the filename with the rule postfix
    if hasattr(selected_rule, 'name'):
        rule_shortname = selected_rule.name.replace("_", "")
    else:
        rule_shortname = str(selected_rule).replace("_", "")

    output_file = output_dir / f"{filename}_{rule_shortname}.json"
    logger.print_debug(f"JSON Output file will be: {output_file}")

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

        # Add timestamp column if it's in the index
        if isinstance(export_df.index, pd.DatetimeIndex):
            export_df = export_df.reset_index()

        # Convert DataFrame to JSON
        # Use 'records' orientation for a list of dictionaries format
        # Handle NaN values and datetime serialization
        json_data = export_df.to_json(orient='records', date_format='iso', default_handler=str)
        
        # Parse and re-serialize with proper indentation for readability
        parsed_data = json.loads(json_data)
        
        # Export to JSON with pretty formatting
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=2, ensure_ascii=False)

        # Update export info
        export_info["success"] = True
        export_info["output_file"] = str(output_file)
        logger.print_success(f"Indicator data exported to JSON: {output_file}")

    except Exception as e:
        export_info["error_message"] = f"Failed to export indicator data to JSON: {str(e)}"
        logger.print_error(export_info["error_message"])

    return export_info
