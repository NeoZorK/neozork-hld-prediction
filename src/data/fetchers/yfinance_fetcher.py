# src/data/fetchers/yfinance_fetcher.py # CORRECTED MultiIndex/Column Handling

"""
Contains functions related to fetching data from Yahoo Finance using yfinance.
Includes interval/ticker mapping and the main data download function.
"""

import pandas as pd
import numpy as np
import yfinance as yf
import traceback
from ...common import logger # Relative import


# Definition of the map_interval function (specific to yfinance)
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

    if tf_input_upper in mapping:
        return mapping[tf_input_upper]
    elif tf_input.lower() in valid_yf_intervals:
        return tf_input.lower()
    else:
        raise ValueError(f"Invalid yfinance timeframe input: '{tf_input}'. Use M1, H1, D1, W1, MN1 or yfinance intervals like '1h', '1d', '1wk', '1mo'.")


# Definition of the map_ticker function (specific to yfinance)
def map_ticker(ticker_input: str) -> str:
    """Optional: Adds standard suffixes for common yfinance ticker patterns (e.g., Forex)."""
    ticker = ticker_input.upper()
    if len(ticker) == 6 and '=' not in ticker and '-' not in ticker and all(c.isalpha() for c in ticker):
        logger.print_info(f"Assuming '{ticker}' is Forex, appending '=X'. -> '{ticker}=X'")
        return f"{ticker}=X"
    return ticker


# Definition of the fetch_yfinance_data function
def fetch_yfinance_data(ticker: str, interval: str, period: str = None, start_date: str = None, end_date: str = None) -> pd.DataFrame | None:
    """
    Downloads OHLCV data from Yahoo Finance using yfinance library.
    Handles MultiIndex columns returned by yfinance and validates essential columns.
    """
    logger.print_info(f"Attempting to fetch yfinance data for: {ticker} | interval: {interval} | period: {period} | start: {start_date} | end: {end_date}")

    try:
        df = yf.download(
            tickers=ticker, period=period, interval=interval, start=start_date, end=end_date,
            progress=True, auto_adjust=False, actions=False
        )

        if df is None or df.empty:
            logger.print_warning(f"No yfinance data returned for '{ticker}' with specified parameters.")
            return None

        # --- CORRECTED: MultiIndex Handling ---
        if isinstance(df.columns, pd.MultiIndex):
            logger.print_debug("Detected MultiIndex columns from yfinance. Simplifying...")
            original_cols = df.columns
            try:
                 # Try dropping the first level (often Ticker name for single download)
                 # Or the second level (often attribute name if structure is different)
                 # Let's try dropping level 0 first
                 simplified_cols = df.columns.droplevel(0)
                 if not simplified_cols.has_duplicates: # Check if dropping worked meaningfully
                      df.columns = simplified_cols
                      logger.print_debug(f"Dropped level 0. Simplified columns: {list(df.columns)}")
                 else:
                      # Try dropping level 1 if level 0 didn't work well
                      simplified_cols = df.columns.droplevel(1)
                      if not simplified_cols.has_duplicates:
                           df.columns = simplified_cols
                           logger.print_debug(f"Dropped level 1. Simplified columns: {list(df.columns)}")
                      else:
                           # Fallback to flattening if droplevel fails
                           logger.print_warning("Droplevel failed to simplify uniquely. Attempting to flatten MultiIndex...")
                           df.columns = ['_'.join(map(str, col)).strip().rstrip('_') for col in original_cols.values]
                           logger.print_debug(f"Flattened columns: {list(df.columns)}")
            except Exception as multi_index_error:
                 logger.print_error(f"Failed during MultiIndex simplification: {multi_index_error}")
                 logger.print_error(f"Original MultiIndex columns were: {original_cols}")
                 # Attempt final fallback flatten on error
                 try:
                      logger.print_warning("Attempting final flatten MultiIndex fallback...")
                      df.columns = ['_'.join(map(str, col)).strip().rstrip('_') for col in original_cols.values]
                      logger.print_debug(f"Flattened columns: {list(df.columns)}")
                 except Exception as flatten_error:
                       logger.print_error(f"Final fallback flatten MultiIndex failed: {flatten_error}")
                       return None # Give up

        # --- CORRECTED: Column Renaming and Validation ---
        # Standardize column names to PascalCase (Open, High, Low, Close, Volume) case-insensitively
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        rename_map = {}
        current_cols_lower_map = {c.lower(): c for c in df.columns} # Map lower case name to original name

        for req_col in required_cols:
             req_col_lower = req_col.lower()
             if req_col_lower in current_cols_lower_map:
                  original_case_col = current_cols_lower_map[req_col_lower]
                  if original_case_col != req_col: # If case differs
                       rename_map[original_case_col] = req_col
             #else:
                 # If required column (lower case) is not found at all
                 # Handled by the missing check below

        if rename_map:
             logger.print_debug(f"Renaming columns for case consistency: {rename_map}")
             df.rename(columns=rename_map, inplace=True)

        # Check for required columns *after* potential renaming
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.print_error(f"Downloaded data for '{ticker}' is missing required columns after processing: {missing_cols}. Available columns: {list(df.columns)}")
            return None
        # --- END Column Renaming and Validation ---

        # Drop rows with NaNs in essential OHLC columns
        initial_rows = len(df)
        try:
            df.dropna(subset=['Open', 'High', 'Low', 'Close'], how='any', inplace=True) # Use 'any' to drop if any OHLC is NaN
        except KeyError as ke:
            logger.print_error(f"KeyError during dropna, columns might not be as expected: {ke}")
            return None
        rows_dropped = initial_rows - len(df)
        if rows_dropped > 0:
            logger.print_debug(f"Dropped {rows_dropped} rows with NaNs in any OHLC column.")

        if df.empty:
            logger.print_warning(f"Data for '{ticker}' became empty after removing NaN rows.")
            return None

        # Ensure index is DatetimeIndex
        if not isinstance(df.index, pd.DatetimeIndex):
             logger.print_warning(f"Index for {ticker} is not DatetimeIndex. Type: {type(df.index)}")
             try:
                  df.index = pd.to_datetime(df.index)
                  logger.print_info("Converted index to DatetimeIndex.")
             except Exception as idx_err:
                  logger.print_error(f"Failed to convert index to DatetimeIndex: {idx_err}")
                  return None


        logger.print_success(f"Successfully fetched and validated {len(df)} rows from Yahoo Finance.")
        return df

    except Exception as e:
        logger.print_error(f"\n--- ERROR DOWNLOADING/PROCESSING YFINANCE ---")
        logger.print_error(f"An unexpected error occurred for ticker '{ticker}': {type(e).__name__}: {e}")
        tb_str = traceback.format_exc()
        try: print(f"{logger.ERROR_COLOR}Traceback:\n{tb_str}{logger.RESET_ALL}")
        except AttributeError: print(f"Traceback:\n{tb_str}")
        logger.print_error(f"--- END YFINANCE ERROR ---")
        return None