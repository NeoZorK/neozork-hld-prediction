# src/data/fetchers/yfinance_fetcher.py # CORRECTED COLUMN RENAMING

"""
Contains functions related to fetching data from Yahoo Finance using yfinance.
Includes interval mapping and the main data download function.
All comments are in English.
"""

import pandas as pd
import numpy as np
import yfinance as yf
import traceback
import time
from ...common import logger # Relative import


# Definition of the map_yfinance_interval function (using yfinance name convention)
def map_yfinance_interval(tf_input: str) -> str | None:
    """Maps user-friendly timeframe input to yfinance interval string."""
    tf_input_upper = tf_input.upper()
    # Map common inputs to valid yfinance intervals
    mapping = {
        "M1": "1m", "M5": "5m", "M15": "15m", "M30": "30m",
        "H1": "1h", "H4": "4h", # Note: yfinance doesn't have '4h', largest intraday < 1d is '1h' or '90m'
        "D1": "1d", "D": "1d",
        "W1": "1wk", "W": "1wk", "WK": "1wk", "MN1": "1mo",
        "MN": "1mo", "MO": "1mo"
    }
    # List of intervals generally accepted by yfinance download
    valid_yf_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]

    if tf_input_upper == "H4":
        logger.print_warning("yfinance does not support 'H4' interval directly. Using '1h' instead.")
        return "1h"

    if tf_input_upper in mapping:
        mapped_interval = mapping[tf_input_upper]
        # Further check if the mapped interval is generally valid
        if mapped_interval in valid_yf_intervals:
             return mapped_interval
        else:
             logger.print_error(f"Mapped interval '{mapped_interval}' from '{tf_input}' is not a standard yfinance interval.")
             return None
    elif tf_input.lower() in valid_yf_intervals:
        return tf_input.lower() # Already a valid interval
    else:
        logger.print_error(f"Invalid or unsupported yfinance timeframe input: '{tf_input}'. Valid examples: {valid_yf_intervals}")
        return None # Return None for invalid input


# Definition of the map_yfinance_ticker function (using yfinance name convention)
# Optional: Adds standard suffixes for common yfinance ticker patterns (e.g., Forex).
def map_yfinance_ticker(ticker_input: str) -> str:
    """ Maps user-provided ticker to a potentially yfinance-specific format (optional). """
    ticker = ticker_input.upper()
    # Example: Auto-append '=X' for assumed Forex pairs
    if len(ticker) == 6 and '=' not in ticker and '-' not in ticker and ticker.isalpha():
        logger.print_info(f"Assuming '{ticker}' is Forex, checking '{ticker}=X'.")
        # Ideally, we'd verify with yf.Ticker(f"{ticker}=X").info here, but that's slow.
        # For now, we just append based on pattern. User should verify tickers.
        return f"{ticker}=X"
    return ticker


# Definition of the fetch_yfinance_data function
# MODIFIED: Corrected column handling after MultiIndex flattening
def fetch_yfinance_data(ticker: str, interval: str, period: str = None, start_date: str = None, end_date: str = None) -> tuple[pd.DataFrame | None, dict]:
    """
    Downloads OHLCV data from Yahoo Finance using yfinance library.
    Handles MultiIndex columns returned by yfinance and validates essential columns.
    Measures the download latency and propagates error messages.

    Args:
        ticker (str): The ticker symbol to download (should be yfinance compatible).
        interval (str): The data interval (should be mapped to yfinance format).
        period (str, optional): The period string (e.g., '1y', '6mo'). Defaults to None.
        start_date (str, optional): The start date string (YYYY-MM-DD). Defaults to None.
        end_date (str, optional): The end date string (YYYY-MM-DD). Defaults to None.

    Returns:
        tuple[pd.DataFrame | None, dict]: A tuple containing:
            - pd.DataFrame: The downloaded and processed OHLCV data, or None on failure.
            - dict: A dictionary containing metrics ('latency_sec', 'error_message').
    """
    logger.print_info(f"Attempting to fetch yfinance data for: {ticker} | interval: {interval} | period: {period} | start: {start_date} | end: {end_date}")
    metrics = {"latency_sec": 0.0, "error_message": None} # Initialize error_message
    df = None
    yf_interval = map_yfinance_interval(interval)
    if yf_interval is None: # Check if mapping failed
        metrics["error_message"] = f"Invalid yfinance interval provided: {interval}"
        return None, metrics

    # Ensure end_date is adjusted correctly if provided (fetch needs day *after* target end)
    end_date_adjusted = None
    if end_date:
        try:
            end_dt = pd.to_datetime(end_date)
            # Add one day to include the end date in yfinance fetch logic
            end_date_adjusted = (end_dt + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        except ValueError:
             metrics["error_message"] = f"Invalid end_date format: {end_date}"
             return None, metrics

    try:
        # Measure latency of the download call
        start_time = time.perf_counter()
        df = yf.download(
            tickers=ticker, period=period, interval=yf_interval,
            start=start_date, end=end_date_adjusted, # Use adjusted end date here
            progress=True, auto_adjust=False, actions=False, # Keep standard settings
            ignore_tz=True # Typically safer for OHLCV consistency
        )
        end_time = time.perf_counter()
        metrics["latency_sec"] = end_time - start_time
        logger.print_debug(f"yf.download call took: {metrics['latency_sec']:.3f} seconds")

        # --- Post-download checks ---
        if df is None or df.empty:
            # Check if yfinance logged errors (often available in stderr or captured logs)
            # We don't have direct access here, rely on df being empty as indicator
            warning_msg = f"No yfinance data returned for '{ticker}' with specified parameters."
            logger.print_warning(warning_msg)
            metrics["error_message"] = warning_msg # Set error message
            return None, metrics

        # --- Handle Columns ---
        if isinstance(df.columns, pd.MultiIndex):
             # This shouldn't happen with auto_adjust=False, actions=False
             logger.print_warning("Detected unexpected MultiIndex columns with auto_adjust=False. Attempting to handle by flattening.")
             # Basic flatten strategy
             df.columns = ['_'.join(map(str, col)).strip().rstrip('_') for col in df.columns.values]

        # --- Column Renaming and Validation --- (REVISED LOGIC)
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        rename_map = {}
        current_cols = df.columns.tolist() # Get current column names

        logger.print_debug(f"Original columns from yf.download: {current_cols}")

        # Iterate through current columns to build the rename map
        for col in current_cols:
            col_str = str(col) # Ensure it's a string
            # Check if column starts with a required name (case insensitive) + '_' + ticker
            # Example: 'Open_AAPL', 'close_AAPL', 'Volume_AAPL'
            found_match = False
            for req_col in required_cols:
                # Check for pattern like "Open_TICKER" or "close_TICKER"
                # Match case-insensitively
                expected_prefix = f"{req_col.lower()}_{ticker.lower()}" # e.g., open_aapl
                if col_str.lower() == expected_prefix: # Exact match needed here
                    rename_map[col] = req_col # Map 'open_aapl' to 'Open'
                    found_match = True
                    break
                # Check for pattern like "Open" or "close" (case insensitive)
                elif col_str.lower() == req_col.lower():
                     if col_str != req_col: # Only rename if case differs
                          rename_map[col] = req_col # Map 'open' to 'Open'
                     found_match = True
                     break # Found standard name (case-insensitive), no need to check other req_cols

            if not found_match:
                logger.print_debug(f"Ignoring column '{col_str}' during required OHLCV renaming.")


        if rename_map:
             logger.print_debug(f"Renaming columns for standardization: {rename_map}")
             df.rename(columns=rename_map, inplace=True)
        else:
            logger.print_debug("No columns needed renaming based on detected patterns.")


        # Check for missing required columns *AFTER* potential renaming
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            error_msg = f"Data for '{ticker}' missing required columns after processing: {missing_cols}. Available columns: {list(df.columns)}"
            logger.print_error(error_msg)
            metrics["error_message"] = error_msg
            return None, metrics # Return error

        # --- Post-processing ---
        # Drop rows with NaNs in essential OHLC columns
        initial_rows = len(df)
        df.dropna(subset=['Open', 'High', 'Low', 'Close'], how='any', inplace=True)
        rows_dropped = initial_rows - len(df)
        if rows_dropped > 0: logger.print_debug(f"Dropped {rows_dropped} rows with NaNs in OHLC columns.")

        if df.empty:
             warning_msg = f"Data for '{ticker}' became empty after removing NaN rows."
             logger.print_warning(warning_msg)
             metrics["error_message"] = warning_msg
             return None, metrics

        # Ensure index is DatetimeIndex and named 'DateTime'
        df.index.name = 'DateTime'

        logger.print_success(f"Successfully fetched and processed {len(df)} rows from Yahoo Finance.")
        return df, metrics

    # --- Catch ALL exceptions during fetch/process ---
    except Exception as e:
        error_type = type(e).__name__
        # Extract specific yfinance error message if possible
        yf_error_msg = str(e)
        # Example: Check for common yfinance error patterns if needed here

        error_msg = f"yf.download or processing failed: {error_type}: {yf_error_msg}"
        logger.print_error(error_msg)
        tb_str = traceback.format_exc()
        try: print(f"{logger.ERROR_COLOR}Traceback:\n{tb_str}{logger.RESET_ALL}")
        except AttributeError: print(f"Traceback:\n{tb_str}")
        metrics["error_message"] = error_msg # Ensure error message is set
        return None, metrics