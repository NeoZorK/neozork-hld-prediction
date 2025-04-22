# src/data/data_acquisition.py

"""
Handles data acquisition from various sources based on command-line arguments.
Manages fetching data using appropriate fetcher functions and basic processing.
All comments are in English.
"""

import pandas as pd
from typing import Tuple, Dict, Optional
import traceback # Import traceback

# Use relative imports for fetchers and logger
# --- CORRECTED Import name for demo data function ---
from .fetchers import (
    get_demo_data, # Corrected name
    fetch_csv_data,
    fetch_yfinance_data,
    fetch_polygon_data,
    fetch_binance_data
)
from ..common import logger

# Main data acquisition function
def acquire_data(args) -> Tuple[Optional[pd.DataFrame], Dict]:
    """
    Acquires data based on the specified mode in args.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        Tuple[Optional[pd.DataFrame], Dict]:
            - DataFrame containing the acquired data (OHLCV).
            - Dictionary containing metadata about the data source.
              Returns (None, data_info) if data acquisition fails.
    """
    # Normalize mode 'yf' to 'yfinance'
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode
    logger.print_info(f"--- Step 1: Acquiring Data (Mode: {effective_mode.capitalize()}) ---")

    df: Optional[pd.DataFrame] = None
    # Initialize data_info with mode, potentially updated by fetchers
    data_info: Dict = {'mode': effective_mode, 'data_source_label': 'Unknown'}

    try:
        if effective_mode == 'demo':
            logger.print_info("Generating demo data...")
            # --- CORRECTED function call ---
            # fetch_demo_data likely returns only the DataFrame
            df = get_demo_data() # Corrected function call
            # Set data_info specifically for demo mode
            data_info['data_source_label'] = 'Demo Data'
            data_info['interval'] = 'D1' # Assuming demo data is daily
            data_info['ticker'] = 'DEMO_EURUSD' # Example ticker
            # Point size for demo is handled in workflow step 2

        elif effective_mode == 'csv':
            if not args.csv_file or args.point is None:
                 logger.print_error("CSV file path (--csv-file) and point size (--point) are required for CSV mode.")
                 return None, data_info # Return None df and basic data_info
            # fetch_csv_data should return df and specific info
            df, csv_info = fetch_csv_data(args.csv_file, args.point)
            data_info.update(csv_info) # Merge csv specific info

        elif effective_mode == 'yfinance':
            if not args.ticker:
                 logger.print_error("Ticker (--ticker) is required for yfinance mode.")
                 return None, data_info
            # Determine date range parameters
            start_date = args.start
            end_date = args.end
            period = args.period
            # fetch_yfinance_data should return df and specific info
            df, yf_info = fetch_yfinance_data(args.ticker, args.interval, start_date, end_date, period)
            data_info.update(yf_info)

        elif effective_mode == 'polygon':
            if not args.ticker or not args.start or not args.end or args.point is None:
                 logger.print_error("Ticker, start date, end date, and point size are required for Polygon mode.")
                 return None, data_info
            # fetch_polygon_data should return df and specific info
            df, poly_info = fetch_polygon_data(args.ticker, args.interval, args.start, args.end)
            data_info.update(poly_info)
            # Add required point size info
            data_info['point_size'] = args.point
            data_info['estimated_point'] = False


        elif effective_mode == 'binance':
            if not args.ticker or not args.start or not args.end or args.point is None:
                 logger.print_error("Ticker, start date, end date, and point size are required for Binance mode.")
                 return None, data_info
            # fetch_binance_data should return df and specific info
            df, binance_info = fetch_binance_data(args.ticker, args.interval, args.start, args.end)
            data_info.update(binance_info)
            # Add required point size info
            data_info['point_size'] = args.point
            data_info['estimated_point'] = False

        else:
            # This case should ideally not be reached due to CLI validation
            logger.print_error(f"Unsupported mode encountered in acquire_data: {effective_mode}")
            return None, data_info

        # --- Final check and return ---
        if df is None:
            logger.print_warning(f"Data acquisition for mode '{effective_mode}' returned no data.")
        elif df.empty:
             logger.print_warning(f"Data acquisition for mode '{effective_mode}' returned an empty DataFrame.")
        else:
             logger.print_success(f"Data acquired successfully for mode '{effective_mode}'. Rows: {len(df)}")
             # Ensure index is datetime
             if not isinstance(df.index, pd.DatetimeIndex):
                  logger.print_warning("Index is not DatetimeIndex. Attempting conversion.")
                  try:
                       df.index = pd.to_datetime(df.index)
                  except Exception as e:
                       logger.print_error(f"Failed to convert index to DatetimeIndex: {e}. Plotting might fail.")

        # Always return df and data_info (even if df is None)
        return df, data_info

    except Exception as e:
        logger.print_error(f"An error occurred during data acquisition (Mode: {effective_mode}): {type(e).__name__}: {e}")
        # Use imported traceback
        logger.print_debug(f"Traceback (acquire_data):\n{traceback.format_exc()}")
        # Return None df and the current state of data_info on error
        return None, data_info
