# src/data/fetchers/yfinance_fetcher.py # REWRITTEN WITH CHUNKS AND TQDM

"""
Contains functions related to fetching data from Yahoo Finance using yfinance.
Now implements chunking and tqdm progress bar similar to Polygon/Binance fetchers.
All comments are in English.
"""

import pandas as pd
import numpy as np
import yfinance as yf
import traceback
import time
from datetime import datetime, timedelta
from tqdm import tqdm # Import tqdm
import requests
import random
import json

# Use relative import for logger
from ...common import logger


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
        mapped_ticker = f"{ticker}=X"
        logger.print_info(f"Input ticker '{ticker_input}' matches Forex pattern, using '{mapped_ticker}'.")
        return mapped_ticker
    return ticker # Return original if no mapping applied


# --- User-Agent pool для ротации ---
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

def _create_custom_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache'
    })
    return session


def _direct_yf_api_request(ticker: str, period: str, interval: str, session: requests.Session) -> pd.DataFrame | None:
    """
    Прямой запрос к API Yahoo Finance, если yf.download не сработал.
    """
    YF_API_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"
    period_map = {
        '1d': {'range': '1d', 'interval': '1m'},
        '5d': {'range': '5d', 'interval': '15m'},
        '1mo': {'range': '1mo', 'interval': '1d'},
        '3mo': {'range': '3mo', 'interval': '1d'},
        '6mo': {'range': '6mo', 'interval': '1d'},
        '1y': {'range': '1y', 'interval': '1d'},
        '2y': {'range': '2y', 'interval': '1d'},
        '5y': {'range': '5y', 'interval': '1wk'},
        'max': {'range': 'max', 'interval': '1mo'}
    }
    interval_map = {
        '1m': '1m', '2m': '2m', '5m': '5m', '15m': '15m', '30m': '30m',
        '60m': '60m', '90m': '90m', '1h': '60m', '1d': '1d',
        '5d': '5d', '1wk': '1wk', '1mo': '1mo', '3mo': '3mo'
    }
    params = {
        'range': period_map.get(period, {}).get('range', '1mo'),
        'interval': interval_map.get(interval, '1d'),
        'includePrePost': 'false',
        'events': 'div,splits',
        'lang': 'en-US',
        'region': 'US'
    }
    url = f"{YF_API_URL}{ticker}"
    try:
        logger.print_info(f"Fallback: direct API request to {url} with params: {params}")
        response = session.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                chart_data = data['chart']['result'][0]
                timestamps = chart_data.get('timestamp', [])
                quote = chart_data.get('indicators', {}).get('quote', [{}])[0]
                if timestamps and quote and 'close' in quote:
                    df = pd.DataFrame({
                        'Open': quote.get('open', []),
                        'High': quote.get('high', []),
                        'Low': quote.get('low', []),
                        'Close': quote.get('close', []),
                        'Volume': quote.get('volume', []),
                    }, index=pd.to_datetime([datetime.fromtimestamp(ts) for ts in timestamps]))
                    logger.print_success(f"Fallback: received {len(df)} rows from direct API for {ticker}")
                    return df
                else:
                    logger.print_error(f"Fallback: No price data in response for {ticker}")
            else:
                logger.print_error(f"Fallback: Invalid API response format for {ticker}")
        else:
            logger.print_error(f"Fallback: API request failed with status {response.status_code}: {response.text}")
    except Exception as e:
        logger.print_error(f"Fallback: Error in direct API request for {ticker}: {str(e)}")
    return None


# Definition of the fetch_yfinance_data function (Chunking Implementation)
def fetch_yfinance_data(ticker: str, interval: str, period: str = None, start_date: str = None, end_date: str = None, session: requests.Session = None) -> tuple[pd.DataFrame | None, dict]:
    """
    Downloads OHLCV data from Yahoo Finance using yfinance library,
    implementing manual chunking and a tqdm progress bar.

    Args:
        ticker (str): The ticker symbol to download (will be mapped).
        interval (str): The data interval (user provided, will be mapped).
        period (str, optional): Period string. *If provided, chunking is bypassed, and a single download is attempted.*
        start_date (str, optional): The start date string (YYYY-MM-DD). Required for chunking.
        end_date (str, optional): The end date string (YYYY-MM-DD). Required for chunking.

    Returns:
        tuple[pd.DataFrame | None, dict]: A tuple containing:
            - pd.DataFrame: The downloaded and processed OHLCV data, or None on failure.
            - dict: A dictionary containing metrics ('latency_sec', 'error_message', 'api_calls', 'rows_fetched').
    """
    # Map ticker and interval first
    yf_ticker = map_yfinance_ticker(ticker)
    yf_interval = map_yfinance_interval(interval)

    logger.print_info(f"Fetching yfinance data for: {yf_ticker} (original: {ticker}) | interval: {yf_interval} (original: {interval})")
    metrics = {"latency_sec": 0.0, "error_message": None, "api_calls": 0, "rows_fetched": 0} # Initialize metrics
    all_chunk_data = [] # List to store dataframes from chunks

    if yf_interval is None: # Check if interval mapping failed
        metrics["error_message"] = f"Invalid yfinance interval provided: {interval}"
        return None, metrics

    # --- Создаём кастомную сессию, если не передана ---
    if session is None:
        session = _create_custom_session()

    # --- Handle Period Argument (Bypass Chunking) ---
    if period:
        logger.print_info(f"Period '{period}' provided, bypassing chunking and attempting single download.")
        try:
            start_time = time.perf_counter()
            df_period = yf.download(
                tickers=yf_ticker, period=period, interval=yf_interval,
                progress=False, auto_adjust=False, actions=False, ignore_tz=True,
                session=session
            )
            end_time = time.perf_counter()
            metrics["latency_sec"] = end_time - start_time
            metrics["api_calls"] = 1

            # --- Fallback: direct API if yf.download не дал данных ---
            if df_period is None or df_period.empty:
                logger.print_warning(f"No data from yf.download for period '{period}', trying direct API fallback...")
                df_period = _direct_yf_api_request(yf_ticker, period, yf_interval, session)
                if df_period is not None and not df_period.empty:
                    all_chunk_data.append(df_period)
                    metrics["rows_fetched"] = len(df_period)
                    logger.print_success(f"Fallback: direct API fetched {len(df_period)} rows.")
                else:
                    metrics["error_message"] = f"No data returned by yfinance for period '{period}'."
                    return None, metrics
            else:
                all_chunk_data.append(df_period)
                metrics["rows_fetched"] = len(df_period)
                logger.print_success(f"Single download for period '{period}' fetched {len(df_period)} rows.")

        except Exception as e:
            error_msg = f"yf.download failed for period '{period}': {type(e).__name__}: {e}"
            logger.print_error(error_msg); metrics["error_message"] = error_msg
            tb_str = traceback.format_exc(); print(f"{logger.ERROR_COLOR}Traceback:\n{tb_str}{logger.RESET_ALL}")
            return None, metrics

    # --- Handle Chunking based on Start/End Dates ---
    elif start_date and end_date:
        try:
            overall_start_dt = pd.to_datetime(start_date).tz_localize(None)
            overall_end_dt = pd.to_datetime(end_date).tz_localize(None)
            if overall_start_dt >= overall_end_dt: raise ValueError("Start date must be before end date.")
        except ValueError as e:
             metrics["error_message"] = f"Invalid start/end date format or range: {e}"
             return None, metrics

        current_start_dt = overall_start_dt
        # Define chunk size (e.g., 1 year) - might need tuning based on interval/yfinance limits
        chunk_delta = timedelta(days=365)
        total_days = max(1, (overall_end_dt - overall_start_dt).days + 1)

        logger.print_info(f"Fetching data in chunks from {start_date} to {end_date}...")

        pbar = tqdm(total=total_days, unit='day', desc=f"Fetching yfinance {yf_ticker}", leave=True, ascii=True, unit_scale=False)
        last_processed_dt = overall_start_dt - timedelta(days=1) # For accurate progress update

        try: # Wrap loop for pbar.close()
            while current_start_dt <= overall_end_dt:
                # Calculate end of the current chunk
                current_end_chunk_exclusive = min(current_start_dt + chunk_delta, overall_end_dt + timedelta(days=1)) # yf end is exclusive
                current_end_chunk_inclusive = current_end_chunk_exclusive - timedelta(days=1) # For display/logic

                # Format dates for yf.download
                chunk_start_str = current_start_dt.strftime('%Y-%m-%d')
                chunk_end_str = current_end_chunk_exclusive.strftime('%Y-%m-%d') # yf needs exclusive end

                pbar.set_postfix_str(f"Chunk: {chunk_start_str} to {current_end_chunk_inclusive.strftime('%Y-%m-%d')}", refresh=True)

                try:
                    start_chunk_time = time.perf_counter()
                    df_chunk = yf.download(
                        tickers=yf_ticker, interval=yf_interval,
                        start=chunk_start_str, end=chunk_end_str,
                        progress=False, auto_adjust=False, actions=False, ignore_tz=True,
                        session=session
                    )
                    end_chunk_time = time.perf_counter()
                    metrics["api_calls"] += 1
                    chunk_latency = end_chunk_time - start_chunk_time
                    metrics["latency_sec"] += chunk_latency # Accumulate successful latency

                    if df_chunk is not None and not df_chunk.empty:
                        # Ensure timezone naive index before appending
                        df_chunk.index = pd.to_datetime(df_chunk.index).tz_localize(None)
                        all_chunk_data.append(df_chunk)
                        metrics["rows_fetched"] += len(df_chunk)
                        # pbar.write(f" Fetched {len(df_chunk)} rows for chunk {chunk_start_str}-{chunk_end_str} ({chunk_latency:.2f}s)") # Optional info
                    else:
                         pbar.write(f" Warning: No data returned by yfinance for chunk {chunk_start_str}-{chunk_end_str}")

                    # Update progress bar based on the end date of the processed chunk
                    days_processed = (current_end_chunk_inclusive - last_processed_dt).days
                    if days_processed > 0:
                        pbar.update(days_processed)
                        last_processed_dt = current_end_chunk_inclusive

                except Exception as e:
                     error_msg = f"Failed chunk {chunk_start_str}-{chunk_end_str}: {type(e).__name__}: {e}"
                     pbar.write(f" Error: {error_msg}")
                     # Decide whether to stop or continue on chunk failure
                     # For now, let's stop to avoid partial data misleading cache
                     metrics["error_message"] = error_msg
                     tb_str = traceback.format_exc()
                     try: print(f"{logger.ERROR_COLOR}Traceback:\n{tb_str}{logger.RESET_ALL}")
                     except AttributeError: print(f"Traceback:\n{tb_str}")
                     return None, metrics # Stop and return error

                # Move to the next chunk start date
                current_start_dt = current_end_chunk_exclusive
                # Optional: Add a small delay between chunks if needed
                # time.sleep(0.1)

        finally:
             # Ensure pbar reaches 100% and closes
             remaining_days = total_days - pbar.n
             if remaining_days > 0: pbar.update(remaining_days)
             pbar.close()

    else: # Neither period nor start/end dates provided
        metrics["error_message"] = "Either --period or --start/--end must be provided for yfinance."
        return None, metrics


    # --- Combine and Process All Fetched Data ---
    if not all_chunk_data:
        final_error = metrics.get("error_message", f"No data fetched for '{yf_ticker}' with given parameters.")
        logger.print_warning(final_error)
        metrics["error_message"] = final_error
        return None, metrics

    logger.print_info(f"Combining {len(all_chunk_data)} chunk(s)...")
    try:
        df = pd.concat(all_chunk_data)
        # Ensure index is DatetimeIndex after concat
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        df.index = df.index.tz_localize(None) # Ensure naive

    except Exception as e:
         logger.print_error(f"Error combining data chunks: {e}")
         metrics["error_message"] = f"Error combining chunks: {e}"
         return None, metrics # Cannot proceed if concat fails

    # --- Final Processing (Column Renaming, Deduplication, NaN handling) ---
    logger.print_info(f"Processing combined data ({len(df)} rows initially)...")
    try:
        # Handle MultiIndex if it somehow appeared (unlikely now)
        if isinstance(df.columns, pd.MultiIndex):
             logger.print_warning("Detected unexpected MultiIndex columns after concat. Flattening.")
             df.columns = ['_'.join(map(str, col)).strip().rstrip('_') for col in df.columns.values]

        # --- Column Renaming ---
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        rename_map = {}
        current_cols = df.columns.tolist()
        for col in current_cols:
            col_str = str(col)
            found_match = False
            for req_col in required_cols:
                 # Use yf_ticker for suffix check
                 expected_prefix_ticker = f"{req_col.lower()}_{yf_ticker.lower()}"
                 if col_str.lower() == expected_prefix_ticker:
                      rename_map[col] = req_col
                      found_match = True; break
                 elif col_str.lower() == req_col.lower():
                      if col_str != req_col: rename_map[col] = req_col
                      found_match = True; break
            # if not found_match: logger.print_debug(f"Ignoring column '{col_str}'") # Less verbose
        if rename_map:
             logger.print_debug(f"Renaming columns: {rename_map}")
             df.rename(columns=rename_map, inplace=True)

        # --- Validation ---
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns after processing: {missing_cols}. Available: {list(df.columns)}")

        # --- Deduplication & NaN ---
        df.sort_index(inplace=True)
        initial_rows = len(df)
        df = df[~df.index.duplicated(keep='first')]
        rows_after_dedup = len(df)
        if initial_rows > rows_after_dedup: logger.print_debug(f"Removed {initial_rows - rows_after_dedup} duplicate rows.")

        df.dropna(subset=['Open', 'High', 'Low', 'Close'], how='any', inplace=True)
        if initial_rows > len(df) and rows_after_dedup == initial_rows : logger.print_debug(f"Dropped {initial_rows - len(df)} rows with NaNs in OHLC.")
        elif len(df) < rows_after_dedup: logger.print_debug(f"Dropped {rows_after_dedup - len(df)} rows with NaNs in OHLC.")


        if df.empty:
             raise ValueError(f"Data for '{yf_ticker}' became empty after final processing (dedup/NaN drop).")

        # --- Final Index ---
        df.index.name = 'DateTime'

        logger.print_success(f"Successfully fetched and processed {len(df)} final rows from Yahoo Finance.")
        return df, metrics

    except Exception as e:
         error_msg = f"Final processing failed for '{yf_ticker}': {type(e).__name__}: {e}"
         logger.print_error(error_msg)
         tb_str = traceback.format_exc(); print(f"{logger.ERROR_COLOR}Traceback:\n{tb_str}{logger.RESET_ALL}")
         metrics["error_message"] = error_msg
         return None, metrics # Return None on final processing error