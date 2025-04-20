# src/data/fetchers/yfinance_fetcher.py

"""
Contains functions related to fetching data from Yahoo Finance using yfinance.
Includes interval/ticker mapping and the main data download function.
All comments are in English.
"""

import pandas as pd
import numpy as np
import yfinance as yf
import traceback
import time
from ...common import logger # Relative import


# Definition of the map_interval function
# ... (код map_interval остается без изменений) ...
def map_interval(tf_input: str) -> str:
    """Maps user-friendly timeframe input to yfinance interval string."""
    tf_input_upper = tf_input.upper()
    mapping = {
        "M1": "1m", "M5": "5m", "M15": "15m", "M30": "30m",
        "H1": "1h", "H4": "4h", "D1": "1d", "D": "1d",
        "W1": "1wk", "W": "1wk", "WK": "1wk", "MN1": "1mo",
        "MN": "1mo", "MO": "1mo"
    }
    valid_yf_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
    if tf_input_upper in mapping: return mapping[tf_input_upper]
    elif tf_input.lower() in valid_yf_intervals: return tf_input.lower()
    else:
        logger.print_error(f"Invalid yfinance timeframe input: '{tf_input}'.")
        raise ValueError(f"Invalid yfinance timeframe input: '{tf_input}'.")


# Definition of the map_ticker function
# ... (код map_ticker остается без изменений) ...
def map_ticker(ticker_input: str) -> str:
    """Optional: Adds standard suffixes for common yfinance ticker patterns (e.g., Forex)."""
    ticker = ticker_input.upper()
    if len(ticker) == 6 and '=' not in ticker and '-' not in ticker and ticker.isalpha():
        logger.print_info(f"Assuming '{ticker}' is Forex, appending '=X'. -> '{ticker}=X'")
        return f"{ticker}=X"
    return ticker


# Definition of the fetch_yfinance_data function
# MODIFIED: Corrected column handling after MultiIndex flattening
def fetch_yfinance_data(ticker: str, interval: str, period: str = None, start_date: str = None, end_date: str = None) -> tuple[pd.DataFrame | None, dict]:
    """
    Downloads OHLCV data from Yahoo Finance using yfinance library.
    Handles MultiIndex columns returned by yfinance and validates essential columns.
    Measures the download latency.

    Args:
        ticker (str): The ticker symbol to download.
        interval (str): The data interval (already mapped to yfinance format).
        period (str, optional): The period string (e.g., '1y', '6mo'). Defaults to None.
        start_date (str, optional): The start date string (YYYY-MM-DD). Defaults to None.
        end_date (str, optional): The end date string (YYYY-MM-DD). Defaults to None.

    Returns:
        tuple[pd.DataFrame | None, dict]: A tuple containing:
            - pd.DataFrame: The downloaded and processed OHLCV data, or None on failure.
            - dict: A dictionary containing metrics, including 'latency_sec'.
    """
    logger.print_info(f"Attempting to fetch yfinance data for: {ticker} | interval: {interval} | period: {period} | start: {start_date} | end: {end_date}")
    metrics = {"latency_sec": None}
    df = None

    try:
        # Measure latency of the download call
        start_time = time.perf_counter()
        df = yf.download(
            tickers=ticker, period=period, interval=interval, start=start_date, end=end_date,
            progress=True, auto_adjust=False, actions=False,
        )
        end_time = time.perf_counter()
        metrics["latency_sec"] = end_time - start_time
        logger.print_debug(f"yf.download call took: {metrics['latency_sec']:.3f} seconds")

        if df is None or df.empty:
            logger.print_warning(f"No yfinance data returned for '{ticker}' with specified parameters.")
            return None, metrics

        # Flag to track if columns were flattened
        columns_were_flattened = False

        # Handle MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            logger.print_debug("Detected MultiIndex columns from yfinance. Simplifying...")
            original_cols = df.columns
            try:
                 # Try dropping level 0 first
                 simplified_cols = df.columns.droplevel(0)
                 if not simplified_cols.has_duplicates:
                      df.columns = simplified_cols
                      logger.print_debug(f"Dropped level 0. Simplified columns: {list(df.columns)}")
                 else:
                      # Fallback to flattening if droplevel creates duplicates
                      logger.print_warning("Droplevel(0) created duplicate columns. Attempting to flatten MultiIndex...")
                      df.columns = ['_'.join(map(str, col)).strip().rstrip('_') for col in original_cols.values]
                      logger.print_debug(f"Flattened columns: {list(df.columns)}")
                      columns_were_flattened = True # Mark that flattening occurred
            except Exception as multi_index_error:
                 logger.print_error(f"Failed during MultiIndex simplification: {multi_index_error}")
                 # Attempt final fallback flatten
                 try:
                      logger.print_warning("Attempting final flatten MultiIndex fallback...")
                      df.columns = ['_'.join(map(str, col)).strip().rstrip('_') for col in original_cols.values]
                      logger.print_debug(f"Flattened columns: {list(df.columns)}")
                      columns_were_flattened = True # Mark that flattening occurred
                 except Exception as flatten_error:
                       logger.print_error(f"Final fallback flatten MultiIndex failed: {flatten_error}")
                       return None, metrics

        # --- Column Renaming and Validation ---
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        rename_map = {}

        # Build map based on current columns (which might be flattened)
        current_cols = df.columns.tolist()
        ticker_suffix = f"_{ticker}" # Check for suffix like _AAPL

        for col in current_cols:
            # Case 1: Flattened columns like 'Open_AAPL'
            if columns_were_flattened and col.endswith(ticker_suffix):
                base_name = col[:-len(ticker_suffix)] # Get 'Open' from 'Open_AAPL'
                if base_name in required_cols:
                    rename_map[col] = base_name # Map 'Open_AAPL' to 'Open'
            # Case 2: Simple columns that need case correction (e.g., 'open' -> 'Open')
            elif col.capitalize() in required_cols and col != col.capitalize():
                 rename_map[col] = col.capitalize()
            # Case 3: Already correct standard columns (Open, High, etc.) - no rename needed
            elif col in required_cols:
                 pass # Already correct
            # Case 4: Other columns like 'Adj Close' or 'Adj Close_AAPL' - ignore for renaming map
            else:
                 logger.print_debug(f"Ignoring column '{col}' during required OHLCV renaming.")


        if rename_map:
             logger.print_debug(f"Renaming columns for standardization: {rename_map}")
             df.rename(columns=rename_map, inplace=True)

        # Check for missing required columns *AFTER* potential renaming
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.print_error(f"Downloaded data for '{ticker}' is missing required columns after processing: {missing_cols}. Available columns: {list(df.columns)}")
            return None, metrics

        # --- Post-processing ---
        # Drop rows with NaNs in essential OHLC columns
        initial_rows = len(df)
        try:
            # We know required_cols exist now due to the check above
            df.dropna(subset=['Open', 'High', 'Low', 'Close'], how='any', inplace=True)
        except KeyError as ke:
            # Should not happen if the check passed, but keep as safeguard
            logger.print_error(f"KeyError during dropna, columns might not be as expected: {ke}")
            return None, metrics
        rows_dropped = initial_rows - len(df)
        if rows_dropped > 0:
            logger.print_debug(f"Dropped {rows_dropped} rows with NaNs in any OHLC column.")

        if df.empty:
            logger.print_warning(f"Data for '{ticker}' became empty after removing NaN rows.")
            return None, metrics

        # Ensure index is DatetimeIndex and named 'DateTime'
        if not isinstance(df.index, pd.DatetimeIndex):
             logger.print_warning(f"Index for {ticker} is not DatetimeIndex. Type: {type(df.index)}. Attempting conversion.")
             try:
                  df.index = pd.to_datetime(df.index)
                  df.index.name = 'DateTime'
                  logger.print_info("Converted index to DatetimeIndex.")
             except Exception as idx_err:
                  logger.print_error(f"Failed to convert index to DatetimeIndex: {idx_err}")
                  return None, metrics
        else:
            df.index.name = 'DateTime'

        logger.print_success(f"Successfully fetched and validated {len(df)} rows from Yahoo Finance.")
        # Return DataFrame and metrics
        return df, metrics

    except Exception as e:
        # Log detailed error information
        logger.print_error(f"\n--- ERROR DOWNLOADING/PROCESSING YFINANCE ---")
        logger.print_error(f"An unexpected error occurred for ticker '{ticker}': {type(e).__name__}: {e}")
        tb_str = traceback.format_exc()
        try: print(f"{logger.ERROR_COLOR}Traceback:\n{tb_str}{logger.RESET_ALL}")
        except AttributeError: print(f"Traceback:\n{tb_str}")
        logger.print_error(f"--- END YFINANCE ERROR ---")
        return None, metrics