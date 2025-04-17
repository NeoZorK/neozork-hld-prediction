# src/data_utils.py

"""
Utility functions for fetching and preparing data (demo or yfinance).
All comments are in English.
"""
import pandas as pd
import yfinance as yf
import time
from datetime import date, timedelta

# Assuming logger is imported if used
from . import logger

def get_demo_data() -> pd.DataFrame:
    """Returns the demonstration DataFrame."""
    print("[Info] Generating demo data...")
    # Simulate a short delay for "loading"
    time.sleep(0.5)
    # Demo data definition (same as before)
    data = {
        'Open': [1.1, 1.11, 1.12, 1.115, 1.125, 1.13, 1.128, 1.135, 1.14, 1.138,
                 1.142, 1.145, 1.140, 1.135, 1.130, 1.132, 1.138, 1.145, 1.148, 1.150,
                 1.152, 1.155, 1.153, 1.158, 1.160, 1.157, 1.162, 1.165, 1.163, 1.160],
        'High': [1.105, 1.115, 1.125, 1.12, 1.13, 1.135, 1.133, 1.14, 1.145, 1.142,
                 1.146, 1.148, 1.143, 1.139, 1.136, 1.137, 1.142, 1.150, 1.152, 1.155,
                 1.156, 1.159, 1.158, 1.161, 1.163, 1.160, 1.165, 1.168, 1.166, 1.164],
        'Low': [1.095, 1.105, 1.115, 1.11, 1.12, 1.125, 1.125, 1.13, 1.135, 1.136,
                1.140, 1.142, 1.138, 1.133, 1.128, 1.130, 1.135, 1.143, 1.146, 1.148,
                1.150, 1.152, 1.151, 1.155, 1.157, 1.154, 1.159, 1.161, 1.160, 1.158],
        'Close': [1.1, 1.11, 1.118, 1.118, 1.128, 1.128, 1.131, 1.138, 1.138, 1.14,
                  1.145, 1.141, 1.136, 1.131, 1.131, 1.136, 1.144, 1.149, 1.151, 1.149,
                  1.155, 1.154, 1.157, 1.160, 1.159, 1.158, 1.163, 1.164, 1.161, 1.159],
        'Volume': [1000, 1200, 1100, 1300, 1500, 1400, 1600, 1700, 1550, 1650,
                   1750, 1800, 1600, 1900, 2000, 1850, 1950, 2100, 2050, 2200,
                   2150, 2250, 2100, 2300, 2400, 2350, 2450, 2500, 2400, 2300]
    }
    start_date_idx = date.today() - timedelta(days=len(data['Open'])-1)
    index = pd.date_range(start=start_date_idx, periods=len(data['Open']), freq='D')
    df = pd.DataFrame(data, index=index)

    # Rename columns for mplfinance compatibility
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    return df

def map_interval(tf_input: str) -> str:
    """Maps user-friendly timeframe input to yfinance interval string."""
    tf_input_upper = tf_input.upper()

    # Mapping from user input (like M1, D1) to yfinance interval (like 1m, 1d)
    mapping = {
        "M1": "1m", "M5": "5m", "M15": "15m", "M30": "30m",
        "H1": "1h", "H4": "4h",
        "D1": "1d", "D": "1d",
        "W1": "1wk", "W": "1wk", "WK": "1wk",
        "MN1": "1mo", "MN": "1mo", "MO": "1mo"
    }
    # Valid intervals directly accepted by yfinance
    valid_yf_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]

    if tf_input_upper in mapping:
        return mapping[tf_input_upper]
    elif tf_input.lower() in valid_yf_intervals:
         # Allow direct use of yfinance intervals
         return tf_input.lower()
    else:
        raise ValueError(f"Invalid timeframe input: '{tf_input}'. Use formats like 'M1', 'H1', 'D1', 'W1', 'MN1' or yfinance intervals like '1m', '1h', '1d', '1wk', '1mo'.")

def map_ticker(ticker_input: str) -> str:
    """Optional: Adds standard suffixes for common yfinance ticker patterns."""
    ticker = ticker_input.upper()

    # Example: Add '=X' for 6-char currency pairs without a suffix
    if len(ticker) == 6 and '=' not in ticker and '-' not in ticker:
         is_likely_forex = all(c.isalpha() for c in ticker)
         if is_likely_forex:
             logger.print_info(f"[Info] Assuming '{ticker}' is Forex, appending '=X'. -> '{ticker}=X'")
             return f"{ticker}=X"

    # Return the ticker as is if no rules matched
    return ticker


def fetch_yfinance_data(ticker: str, interval: str, period: str = None, start_date: str = None, end_date: str = None) -> pd.DataFrame | None:
    """Downloads data from Yahoo Finance, handles MultiIndex columns, and validates."""
    logger.print_info(f"Attempting to fetch data for ticker: {ticker} | interval: {interval}")
    try:
        df = yf.download(
            tickers=ticker, # Single ticker string
            period=period,
            interval=interval,
            start=start_date,
            end=end_date,
            progress=True,
            auto_adjust=False,
            actions=False,
            # group_by='ticker' # Often forces MultiIndex, good practice for consistency
        )

        if df is None or df.empty:
            logger.print_warning(f"No data returned for ticker '{ticker}' with specified parameters.")
            return None

        # --- Handle Potential MultiIndex Columns ---
        # Check if columns are MultiIndex (returned when downloading single ticker sometimes)
        if isinstance(df.columns, pd.MultiIndex):
            logger.print_debug("Detected MultiIndex columns. Simplifying by dropping ticker level...")
            # Assuming the structure is (ValueType, Ticker) like ('Open', 'GOOG')
            # Drop the second level (Ticker) to get simple column names ('Open', 'High', ...)
            # Check number of levels first to be safe
            if df.columns.nlevels > 1:
                 original_cols = df.columns # Keep original for potential debug messages
                 try:
                     df.columns = df.columns.droplevel(1) # Drop the ticker level (level 1)
                     logger.print_debug(f"Simplified columns: {df.columns.tolist()}")
                 except Exception as multi_index_error:
                     logger.print_error(f"Failed to simplify MultiIndex columns: {multi_index_error}")
                     logger.print_error(f"Original MultiIndex columns were: {original_cols}")
                     return None # Cannot proceed if columns aren't simplified
            else:
                 # Handle cases where it's MultiIndex but only one level? Unlikely but possible.
                 logger.print_warning("MultiIndex detected but only one level found. Attempting basic flatten.")
                 try:
                    df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
                 except Exception as flatten_error:
                    logger.print_error(f"Failed to flatten unusual MultiIndex: {flatten_error}")
                    return None

        # --- Validate Columns and Data (using potentially simplified column names) ---
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.print_warning(f"Downloaded data for '{ticker}' is missing required columns: {missing_cols}. Available columns after potential simplification: {df.columns.tolist()}")
            return None # Return None if essential columns are missing

        # --- Drop Rows with NaNs in essential price columns ---
        # Now this should work because columns are simple strings
        initial_rows = len(df)
        try:
            # Use standard OHLC column names here
            df.dropna(subset=['Open', 'High', 'Low', 'Close'], how='all', inplace=True)
        except KeyError as ke:
            # This shouldn't happen if the check above passed, but as a safeguard
            logger.print_error(f"KeyError during dropna, columns might not be simplified correctly: {ke}")
            logger.print_error(f"Columns at time of dropna: {df.columns.tolist()}")
            return None

        rows_dropped = initial_rows - len(df)
        if rows_dropped > 0:
             logger.print_debug(f"Dropped {rows_dropped} rows with NaNs in OHLC columns.")

        if df.empty:
            logger.print_warning(f"Data for '{ticker}' became empty after removing NaN rows.")
            return None

        logger.print_success(f"Successfully fetched and validated {len(df)} rows.")
        return df

    except Exception as e:
        # General exception handler
        logger.print_error(f"\n--- ERROR DOWNLOADING/PROCESSING ---")
        logger.print_error(f"An unexpected error occurred for ticker '{ticker}': {type(e).__name__}: {e}")
        import traceback
        # Print traceback with error color
        print(f"{logger.ERROR_COLOR}Traceback:\n{traceback.format_exc()}{logger.RESET_ALL}")
        logger.print_error(f"--- END ERROR ---")
        return None