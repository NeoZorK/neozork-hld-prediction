# File: src/data/data_acquisition_csv.py
# -*- coding: utf-8 -*-

"""
CSV data processing for data acquisition.
Handles CSV folder and single file processing.
All comments are in English.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any
from ..common.logger import print_info, print_warning, print_error, print_success


def _process_csv_folder(args, data_info: dict) -> dict:
    """Process CSV folder mode."""
    from .csv_folder_processor import process_csv_folder
    
    data_info["data_source_label"] = f"CSV Folder: {args.csv_folder}"
    print_info(f"Processing CSV folder: {args.csv_folder}")
    
    try:
        folder_df, folder_metrics = process_csv_folder(
            folder_path=args.csv_folder,
            interval=args.interval
        )
        
        if folder_df is not None and not folder_df.empty:
            if isinstance(folder_df.index, pd.DatetimeIndex):
                if folder_df.index.tz is not None:
                    folder_df.index = folder_df.index.tz_localize(None)
            data_info["ohlcv_df"] = folder_df
            data_info["data_metrics"].update(folder_metrics or {})
            print_success(f"Successfully processed CSV folder with {len(folder_df)} rows.")
        else:
            data_info["ohlcv_df"] = pd.DataFrame()
            print_warning("CSV folder processing returned empty DataFrame.")
            
    except Exception as e:
        error_msg = f"Error processing CSV folder {args.csv_folder}: {e}"
        print_error(error_msg)
        data_info["error_message"] = error_msg
        data_info["ohlcv_df"] = pd.DataFrame()
    
    return data_info


def _process_csv_single(args, data_info: dict) -> dict:
    """Process single CSV file mode."""
    from .fetchers import fetch_csv_data
    
    data_info["data_source_label"] = f"CSV File: {args.csv_file}"
    print_info(f"Processing single CSV file: {args.csv_file}")
    
    try:
        csv_df, csv_metrics = fetch_csv_data(
            file_path=args.csv_file,
            interval=args.interval
        )
        
        if csv_df is not None and not csv_df.empty:
            if isinstance(csv_df.index, pd.DatetimeIndex):
                if csv_df.index.tz is not None:
                    csv_df.index = csv_df.index.tz_localize(None)
            data_info["ohlcv_df"] = csv_df
            data_info["data_metrics"].update(csv_metrics or {})
            print_success(f"Successfully processed CSV file with {len(csv_df)} rows.")
        else:
            data_info["ohlcv_df"] = pd.DataFrame()
            print_warning("CSV file processing returned empty DataFrame.")
            
    except Exception as e:
        error_msg = f"Error processing CSV file {args.csv_file}: {e}"
        print_error(error_msg)
        data_info["error_message"] = error_msg
        data_info["ohlcv_df"] = pd.DataFrame()
    
    return data_info
