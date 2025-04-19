# src/data/fetchers/yfinance_fetcher.py

"""
Contains functions related to fetching data from Yahoo Finance using yfinance.
Includes interval/ticker mapping and the main data download function.
"""

import pandas as pd
import yfinance as yf
import traceback
from ...common import logger # Relative import


# Definition of the map_interval function (specific to yfinance)
def map_interval(tf_input: str) -> str:
    """Maps user-friendly timeframe input to yfinance interval string."""
    tf_input_upper = tf_input.upper()
    # Mapping from MQL5 style to yfinance style
    mapping = {
        "M1": "1m", "M5": "5m", "M15": "15m", "M30": "30m",
        "H1": "1h", "H4": "4h", "D1": "1d", "D": "1d",
        "W1": "1wk", "W": "1wk", "WK": "1wk", "MN1": "1mo",
        "MN": "1mo", "MO": "1mo"
    }
    # Also accept valid yfinance intervals directly
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
    # Simple check for 6-letter Forex pairs (like EURUSD)
    if len(ticker) == 6 and '=' not in ticker and '-' not in ticker and all(c.isalpha() for c in ticker):
        logger.print_info(f"Assuming '{ticker}' is Forex, appending '=X'. -> '{ticker}=X'")
        return f"{ticker}=X"
    # Add other potential mappings here (e.g., indices)
    # Example: if ticker == 'SPX': return '^GSPC'
    return ticker


# Definition of the fetch_yfinance_data function
def fetch_yfinance_data(ticker: str, interval: str, period: str = None, start_date: str = None, end_date: str = None) -> pd.DataFrame | None:
    """
    Downloads OHLCV data from Yahoo Finance using yfinance library.
    Handles MultiIndex columns returned by yfinance and validates essential columns.

    Args:
        ticker (str): Ticker symbol recognized by Yahoo Finance (e.g., "AAPL", "EURUSD=X").
        interval (str): Data interval string compatible with yfinance (e.g., "1d", "1h", "1m").
        period (str, optional): Duration string (e.g., "1y", "6mo", "max"). Used if start_date/end_date are None.
        start_date (str, optional): Start date in 'YYYY-MM-DD' format.
        end_date (str, optional): End date in 'YYYY-MM-DD' format.
        If period is specified, start_date/end_date are ignored by yfinance.

    Returns:
        pd.DataFrame | None: DataFrame with OHLCV data and DatetimeIndex, or None on failure.
    """
    logger.print_info(f"Attempting to fetch yfinance data for: {ticker} | interval: {interval} | period: {period} | start: {start_date} | end: {end_date}")

    try:
        # Download data using yfinance
        df = yf.download(
            tickers=ticker,
            period=period,
            interval=interval,
            start=start_date,
            end=end_date,
            progress=True,      # Show progress bar
            auto_adjust=False,  # Keep OHLC separate, don't auto adjust for splits/dividends here
            actions=False       # Don't download actions like dividends/splits
        )

        # --- Post-Download Processing ---
        if df is None or df.empty:
            logger.print_warning(f"No yfinance data returned for '{ticker}' with specified parameters.")
            return None

        # Handle potential MultiIndex columns (common when downloading multiple tickers, but can happen for one)
        if isinstance(df.columns, pd.MultiIndex):
            logger.print_debug("Detected MultiIndex columns from yfinance. Simplifying...")
            if df.columns.nlevels > 1:
                original_cols = df.columns
                try:
                    # Drop the upper level (usually 'Attributes') and keep the lower ('Ticker')
                    df.columns = df.columns.droplevel(0) # Or use droplevel(1) depending on structure
                    logger.print_debug(f"Simplified columns: {list(df.columns)}")
                except Exception as multi_index_error:
                    logger.print_error(f"Failed to simplify MultiIndex columns: {multi_index_error}")
                    logger.print_error(f"Original MultiIndex columns were: {original_cols}")
                    # Attempt flattening as fallback
                    try:
                         logger.print_warning("Attempting to flatten MultiIndex as fallback...")
                         df.columns = ['_'.join(map(str, col)).strip() for col in original_cols.values]
                         logger.print_debug(f"Flattened columns: {list(df.columns)}")
                    except Exception as flatten_error:
                         logger.print_error(f"Failed to flatten MultiIndex: {flatten_error}")
                         return None # Give up if flattening fails
            else:
                # Handle single-level MultiIndex (less common)
                logger.print_warning("Single-level MultiIndex detected. Flattening...")
                try:
                    df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
                except Exception as flatten_error:
                    logger.print_error(f"Failed to flatten unusual MultiIndex: {flatten_error}")
                    return None

        # Ensure required columns are present after potential simplification
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.print_warning(f"Downloaded data for '{ticker}' is missing required columns: {missing_cols}. Available columns: {list(df.columns)}")
            # Try to find alternative names (case variations) - less reliable
            # Example: if 'volume' in df.columns and 'Volume' not in df.columns: df.rename(columns={'volume':'Volume'}, inplace=True)
            # Recalculate missing after trying alternatives
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                 logger.print_error(f"Still missing required columns after checks: {missing_cols}")
                 return None

        # Drop rows where essential OHLC data might be missing (e.g., market holidays)
        initial_rows = len(df)
        try:
            df.dropna(subset=['Open', 'High', 'Low', 'Close'], how='all', inplace=True)
        except KeyError as ke:
            logger.print_error(f"KeyError during dropna, columns might not be as expected: {ke}")
            logger.print_error(f"Columns at time of dropna: {list(df.columns)}")
            return None
        rows_dropped = initial_rows - len(df)
        if rows_dropped > 0:
            logger.print_debug(f"Dropped {rows_dropped} rows with NaNs in OHLC columns.")

        if df.empty:
            logger.print_warning(f"Data for '{ticker}' became empty after removing NaN rows.")
            return None

        # Ensure index is DatetimeIndex
        if not isinstance(df.index, pd.DatetimeIndex):
             logger.print_warning(f"Index for {ticker} is not DatetimeIndex. Type: {type(df.index)}")
             # Attempt conversion if possible, otherwise return None or raise error
             try:
                  df.index = pd.to_datetime(df.index)
                  logger.print_info("Converted index to DatetimeIndex.")
             except Exception as idx_err:
                  logger.print_error(f"Failed to convert index to DatetimeIndex: {idx_err}")
                  return None


        logger.print_success(f"Successfully fetched and validated {len(df)} rows from Yahoo Finance.")
        return df

    # noinspection PyBroadException
    except Exception as e:
        logger.print_error(f"\n--- ERROR DOWNLOADING/PROCESSING YFINANCE ---")
        logger.print_error(f"An unexpected error occurred for ticker '{ticker}': {type(e).__name__}: {e}")
        tb_str = traceback.format_exc()
        # Print traceback using logger colors if available
        try: print(f"{logger.ERROR_COLOR}Traceback:\n{tb_str}{logger.RESET_ALL}")
        except AttributeError: print(f"Traceback:\n{tb_str}") # Fallback if logger colors fail
        logger.print_error(f"--- END YFINANCE ERROR ---")
        return None