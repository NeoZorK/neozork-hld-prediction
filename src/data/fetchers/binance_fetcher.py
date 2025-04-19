# src/data/fetchers/binance_fetcher.py # CORRECTED

"""
Contains functions related to fetching data from Binance Spot API.
Includes interval/ticker mapping and the main data download function with pagination.
"""

import pandas as pd
import os
import time
import traceback
from datetime import datetime, timedelta
from ...common import logger # Relative import

# Binance specific imports and checks
try:
    # noinspection PyPackageRequirements
    from binance.client import Client as BinanceClient
    # noinspection PyPackageRequirements
    from binance.exceptions import BinanceAPIException, BinanceRequestException
    BINANCE_AVAILABLE = True
except ImportError:
    BINANCE_AVAILABLE = False
    # Define dummy classes if binance is not installed
    class BinanceClient: # Dummy class for type hinting when lib not installed
        # Define constants used in mapping to avoid NameError if lib missing
        KLINE_INTERVAL_1MINUTE = '1m'
        KLINE_INTERVAL_5MINUTE = '5m'
        KLINE_INTERVAL_15MINUTE = '15m'
        KLINE_INTERVAL_30MINUTE = '30m'
        KLINE_INTERVAL_1HOUR = '1h'
        KLINE_INTERVAL_4HOUR = '4h'
        KLINE_INTERVAL_1DAY = '1d'
        KLINE_INTERVAL_1WEEK = '1w'
        KLINE_INTERVAL_1MONTH = '1M'
        # Add other intervals if map_binance_interval uses them

    class BinanceAPIException(Exception): pass
    class BinanceRequestException(Exception): pass


# Definition of map_binance_interval function
def map_binance_interval(tf_input: str) -> str | None:
    """Maps user-friendly timeframe to Binance KLINE_INTERVAL_* constant string."""
    # Note: Uses constants defined even in the dummy class if import fails
    tf_input_upper = tf_input.upper()
    mapping = {
        "M1": BinanceClient.KLINE_INTERVAL_1MINUTE,
        "M5": BinanceClient.KLINE_INTERVAL_5MINUTE,
        "M15": BinanceClient.KLINE_INTERVAL_15MINUTE,
        "M30": BinanceClient.KLINE_INTERVAL_30MINUTE,
        "H1": BinanceClient.KLINE_INTERVAL_1HOUR,
        "H4": BinanceClient.KLINE_INTERVAL_4HOUR,
        "D1": BinanceClient.KLINE_INTERVAL_1DAY,
        "D": BinanceClient.KLINE_INTERVAL_1DAY,
        "W1": BinanceClient.KLINE_INTERVAL_1WEEK,
        "W": BinanceClient.KLINE_INTERVAL_1WEEK,
        "WK": BinanceClient.KLINE_INTERVAL_1WEEK,
        "MN1": BinanceClient.KLINE_INTERVAL_1MONTH,
        "MN": BinanceClient.KLINE_INTERVAL_1MONTH,
        "MO": BinanceClient.KLINE_INTERVAL_1MONTH,
    }
    # Check against known valid intervals (even if lib not installed)
    # This list should ideally be comprehensive based on python-binance constants
    valid_binance_intervals = [
        '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'
    ]

    if tf_input_upper in mapping:
        return mapping[tf_input_upper]
    elif tf_input in valid_binance_intervals:
        return tf_input
    else:
        logger.print_error(f"Invalid Binance timeframe input: '{tf_input}'. Use M1, H1, D1 etc. or Binance intervals like '1m', '1h', '1d'.")
        return None


# Definition of map_binance_ticker function
def map_binance_ticker(ticker_input: str) -> str:
    """Formats ticker for Binance (uppercase, no separators)."""
    ticker = ticker_input.upper().replace('/', '').replace('-', '')
    logger.print_debug(f"Mapped ticker '{ticker_input}' to Binance format '{ticker}'")
    return ticker


# Definition of fetch_binance_data function
def fetch_binance_data(ticker: str, interval: str, start_date: str, end_date: str) -> pd.DataFrame | None:
    """
    Downloads OHLCV data from Binance Spot API for a specified date range.
    Handles pagination required by the Binance API (1000 klines limit).
    Assumes BINANCE_API_KEY and BINANCE_API_SECRET are loaded into env vars (optional).
    """
    if not BINANCE_AVAILABLE:
        logger.print_error("Binance Connector library ('python-binance') is not installed.")
        return None

    logger.print_info(f"Attempting to fetch Binance data for: {ticker} | interval: {interval} | start: {start_date} | end: {end_date}")

    # --- Map Ticker and Interval ---
    binance_ticker = map_binance_ticker(ticker)
    binance_interval = map_binance_interval(interval)
    if binance_interval is None:
        return None # Error already logged

    # --- Get API Key/Secret (Optional for public data) ---
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        logger.print_info("Binance API Key/Secret not found in environment. Proceeding with public access.")
    else:
        logger.print_debug("Binance API Key/Secret found.")

    # --- Initialize Client --- CORRECTED BLOCK ---
    try:
        # Initialize client *after* availability check and getting keys.
        # Pass keys even if they are None; library handles it for public endpoints.
        client = BinanceClient(api_key=api_key, api_secret=api_secret)
        logger.print_debug("Binance client initialized.")
        # Optional: Test connection if keys are provided
        # if api_key and api_secret:
        #     client.ping()
        #     logger.print_debug("Binance API ping successful.")
    except Exception as e:
        logger.print_error(f"Failed to initialize Binance client: {type(e).__name__}: {e}")
        return None
    # --- END CORRECTED BLOCK ---

    # --- Convert Dates to Milliseconds Timestamps ---
    try:
        start_dt_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt_obj = datetime.strptime(end_date, '%Y-%m-%d')
        end_dt_inclusive = end_dt_obj + timedelta(days=1) - timedelta(milliseconds=1)
        start_ms = int(start_dt_obj.timestamp() * 1000)
        end_ms = int(end_dt_inclusive.timestamp() * 1000)
        logger.print_debug(f"Binance date range (ms): {start_ms} ({start_dt_obj}) to {end_ms} ({end_dt_inclusive})")
    except ValueError:
        logger.print_error(f"Invalid date format for start_date ('{start_date}') or end_date ('{end_date}'). Use YYYY-MM-DD.")
        return None

    # --- Pagination Logic for Binance get_historical_klines ---
    all_klines_raw = []
    limit_per_request = 1000 # Binance API limit
    current_start_ms = start_ms
    max_attempts_per_chunk = 5
    request_delay_sec = 0.2 # Small delay between successful requests

    logger.print_info(f"Fetching Binance klines in chunks for '{binance_ticker}' ({binance_interval})...")

    while current_start_ms <= end_ms:
        logger.print_debug(f"  Fetching chunk starting from {datetime.fromtimestamp(current_start_ms / 1000)}")
        attempt = 0
        success = False
        klines_chunk = None

        while attempt < max_attempts_per_chunk and not success:
            attempt += 1
            try:
                # Now this call should resolve correctly if client was initialized
                klines_chunk = client.get_historical_klines(
                    symbol=binance_ticker,
                    interval=binance_interval,
                    start_str=str(current_start_ms),
                    end_str=str(end_ms), # Pass overall end time to potentially limit last chunk
                    limit=limit_per_request
                )
                success = True # Mark successful if no exception

            except (BinanceAPIException, BinanceRequestException) as e:
                logger.print_error(f"    Binance API Error on chunk attempt {attempt}/{max_attempts_per_chunk}: Status={getattr(e, 'status_code', 'N/A')}, Code={getattr(e, 'code', 'N/A')}, Msg={e}")
                status_code = getattr(e, 'status_code', None)
                error_code = getattr(e, 'code', None)
                #wait_time = 0
                if status_code == 429: # Rate limit
                    wait_time = 60
                    logger.print_warning(f"      Rate limit likely hit (HTTP {status_code}). Waiting {wait_time} seconds before retry...")
                elif status_code == 418: # IP Ban
                    wait_time = 120
                    logger.print_warning(f"      IP ban likely (HTTP {status_code}). Waiting {wait_time} seconds before retry...")
                elif error_code == -1121: # Invalid symbol
                     logger.print_error(f"      Invalid symbol '{binance_ticker}' reported by Binance API. Stopping fetch.")
                     return None # Cannot recover from invalid symbol
                else: # Other API errors
                    logger.print_error(f"      Non-retriable or unknown API error. Skipping chunk fetch.")
                    break # Break inner retry loop

                if wait_time > 0:
                    time.sleep(wait_time)
                    continue # Go to next attempt without breaking

                # If we didn't continue or return, break the retry loop
                break

            # noinspection PyBroadException
            except Exception as e:
                logger.print_error(f"    Unexpected error during Binance chunk fetch attempt {attempt}/{max_attempts_per_chunk}: {type(e).__name__}: {e}")
                logger.print_error(f"Traceback:\n{traceback.format_exc()}")
                logger.print_error(f"    Skipping chunk fetch due to unexpected error.")
                break # Break inner retry loop

            if not success and attempt < max_attempts_per_chunk:
                logger.print_info(f"    Retrying chunk in {3 * attempt} seconds...")
                time.sleep(3 * attempt) # Simple backoff

        # --- After attempting a chunk ---
        if not success:
            logger.print_error(f"Failed to fetch Binance chunk starting {datetime.fromtimestamp(current_start_ms / 1000)} after {max_attempts_per_chunk} attempts. Stopping.")
            return None # Stop fetching if a chunk fails

        if not klines_chunk: # If chunk is empty, we've reached the end of the specified range
            logger.print_debug("  Received empty kline chunk, assuming end of data range reached.")
            break

        all_klines_raw.extend(klines_chunk)
        logger.print_debug(f"    Fetched {len(klines_chunk)} klines.")

        # Update start time for the next chunk
        last_kline_time_ms = klines_chunk[-1][0] # Open time of the last kline
        current_start_ms = last_kline_time_ms + 1 # Start next request just after the last one

        # Break if the last chunk was smaller than the limit (means we got all remaining data)
        if len(klines_chunk) < limit_per_request:
             logger.print_debug("  Received less than limit, assuming end of data for range.")
             break

        # Be polite to the API
        time.sleep(request_delay_sec)

    # --- Combine and Process All Fetched Data ---
    if not all_klines_raw:
        logger.print_warning(f"No Binance data returned for '{binance_ticker}' in the specified range {start_date} to {end_date}.")
        return None

    logger.print_info(f"Converting {len(all_klines_raw)} raw klines to DataFrame...")

    # Define columns based on Binance documentation
    columns = [
        'OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume',
        'CloseTime', 'QuoteAssetVolume', 'NumberTrades',
        'TakerBuyBaseVol', 'TakerBuyQuoteVol', 'Ignore'
    ]
    df = pd.DataFrame(all_klines_raw, columns=columns)

    # --- Data Type Conversion and Selection ---
    df['DateTime'] = pd.to_datetime(df['OpenTime'], unit='ms', errors='coerce')
    df.dropna(subset=['DateTime'], inplace=True)
    if df.empty:
         logger.print_warning("Binance data became empty after handling DateTime errors.")
         return None
    df.set_index('DateTime', inplace=True)

    # Convert essential columns to numeric
    ohlcv_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in ohlcv_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with NaN in OHLC columns (Volume can sometimes be 0)
    df.dropna(subset=['Open', 'High', 'Low', 'Close'], inplace=True)

    # Select and rename standard columns (already matches required names)
    df = df[ohlcv_cols]

    # Remove duplicates (shouldn't occur with proper pagination)
    initial_rows = len(df)
    df = df[~df.index.duplicated(keep='first')]
    rows_dropped = initial_rows - len(df)
    if rows_dropped > 0:
        logger.print_debug(f"Removed {rows_dropped} duplicate rows from Binance data.")

    # Sort index (should be sorted, but enforce)
    df.sort_index(inplace=True)

    if df.empty:
        logger.print_warning(f"Binance data for '{binance_ticker}' became empty after processing.")
        return None

    logger.print_success(f"Successfully fetched and processed {len(df)} rows from Binance for '{binance_ticker}'.")
    return df