# NeoZorK HLD/src/data/fetchers/binance_fetcher.py (Using pbar.write)

"""
Contains functions related to fetching data from Binance Spot API.
Includes interval/ticker mapping and the main data download function with pagination.
All comments are in English.
"""

import pandas as pd
import os
import time
import traceback
from datetime import datetime, timedelta
from tqdm import tqdm # Import tqdm
from src.common import logger # Absolute import

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
    class BinanceClient:
        KLINE_INTERVAL_1MINUTE = '1m'; KLINE_INTERVAL_5MINUTE = '5m'; KLINE_INTERVAL_15MINUTE = '15m';
        KLINE_INTERVAL_30MINUTE = '30m'; KLINE_INTERVAL_1HOUR = '1h'; KLINE_INTERVAL_4HOUR = '4h';
        KLINE_INTERVAL_1DAY = '1d'; KLINE_INTERVAL_1WEEK = '1w'; KLINE_INTERVAL_1MONTH = '1M'
    class BinanceAPIException(Exception): pass
    class BinanceRequestException(Exception): pass


# Definition of map_binance_interval function
def map_binance_interval(tf_input: str) -> str | None:
    """Maps user-friendly timeframe to Binance KLINE_INTERVAL_* constant string."""
    tf_input_upper = tf_input.upper()
    mapping = {
        "M1": BinanceClient.KLINE_INTERVAL_1MINUTE, "M5": BinanceClient.KLINE_INTERVAL_5MINUTE,
        "M15": BinanceClient.KLINE_INTERVAL_15MINUTE, "M30": BinanceClient.KLINE_INTERVAL_30MINUTE,
        "H1": BinanceClient.KLINE_INTERVAL_1HOUR, "H4": BinanceClient.KLINE_INTERVAL_4HOUR,
        "D1": BinanceClient.KLINE_INTERVAL_1DAY, "D": BinanceClient.KLINE_INTERVAL_1DAY,
        "W1": BinanceClient.KLINE_INTERVAL_1WEEK, "W": BinanceClient.KLINE_INTERVAL_1WEEK, "WK": BinanceClient.KLINE_INTERVAL_1WEEK,
        "MN1": BinanceClient.KLINE_INTERVAL_1MONTH, "MN": BinanceClient.KLINE_INTERVAL_1MONTH, "MO": BinanceClient.KLINE_INTERVAL_1MONTH,
    }
    valid_binance_intervals = [
        '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'
    ]
    if tf_input_upper in mapping: return mapping[tf_input_upper]
    elif tf_input in valid_binance_intervals: return tf_input
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
def fetch_binance_data(ticker: str, interval: str, start_date: str, end_date: str) -> tuple[pd.DataFrame | None, dict]:
    """ Downloads OHLCV data from Binance Spot API with pagination and tqdm progress. """
    if not BINANCE_AVAILABLE:
        logger.print_error("Binance Connector library ('python-binance') is not installed.")
        return None, {"error_message": "python-binance not installed"}

    logger.print_info(f"Attempting to fetch Binance data for: {ticker} | {interval} | {start_date} to {end_date}")
    metrics = {"total_latency_sec": 0.0, "api_calls": 0, "successful_chunks": 0, "rows_fetched": 0}

    # --- Map Ticker and Interval ---
    binance_ticker = map_binance_ticker(ticker)
    binance_interval_str = map_binance_interval(interval)
    if binance_interval_str is None: return None, {"error_message": f"Invalid interval: {interval}"}

    # --- Get API Key/Secret (Optional) ---
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret: logger.print_info("Binance API Key/Secret not found. Proceeding with public access.")

    # --- Initialize Client ---
    try:
        client = BinanceClient(api_key=api_key, api_secret=api_secret)
    except Exception as e:
        logger.print_error(f"Failed to initialize Binance client: {e}")
        return None, {"error_message": f"Client init failed: {e}"}

    # --- Convert Dates to Milliseconds Timestamps ---
    try:
        start_dt_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt_obj = datetime.strptime(end_date, '%Y-%m-%d')
        end_dt_inclusive = end_dt_obj + timedelta(days=1) - timedelta(milliseconds=1)
        start_ms = int(start_dt_obj.timestamp() * 1000)
        end_ms = int(end_dt_inclusive.timestamp() * 1000)
        logger.print_debug(f"Binance date range (ms): {start_ms} ({start_dt_obj}) to {end_ms} ({end_dt_inclusive})")
    except ValueError:
        error_msg = f"Invalid date format for start_date ('{start_date}') or end_date ('{end_date}'). Use YYYY-MM-DD."
        logger.print_error(error_msg)
        return None, {"error_message": error_msg}

    # --- Pagination Logic ---
    all_klines_raw = []
    limit_per_request = 1000
    current_start_ms = start_ms
    initial_start_ms = start_ms
    total_duration_ms = max(0, end_ms - initial_start_ms)
    max_attempts_per_chunk = 5
    request_delay_sec = 0.1 # Reduced delay slightly

    # --- Initialize tqdm ---
    pbar = tqdm(total=total_duration_ms, unit='ms', desc=f"Fetching {binance_ticker}", leave=True, ascii=True, unit_scale=False)
    last_processed_ms = initial_start_ms

    try:
        while current_start_ms <= end_ms:
            # Minimal logging before attempt
            next_chunk_start_dt = datetime.fromtimestamp(current_start_ms / 1000)
            pbar.set_postfix_str(f"Next chunk: {next_chunk_start_dt.strftime('%Y-%m-%d %H:%M')}", refresh=True) # Update postfix instead of writing

            attempt = 0; klines_chunk = None; success = False
            while attempt < max_attempts_per_chunk:
                attempt += 1; wait_time = 0
                try:
                    start_chunk_time = time.perf_counter()
                    metrics["api_calls"] += 1
                    klines_chunk = client.get_historical_klines(
                        symbol=binance_ticker,
                        interval=binance_interval_str,
                        start_str=str(current_start_ms),
                        end_str=str(end_ms),
                        limit=limit_per_request
                    )
                    end_chunk_time = time.perf_counter(); chunk_latency = end_chunk_time - start_chunk_time
                    success = True; metrics["total_latency_sec"] += chunk_latency
                    metrics["successful_chunks"] += 1
                    break # Exit retry loop

                except (BinanceAPIException, BinanceRequestException) as e:
                    # Use pbar.write for errors to print above the bar
                    pbar.write(f"Error: API Error attempt {attempt}/{max_attempts_per_chunk}: Status={getattr(e, 'status_code', 'N/A')}, Code={getattr(e, 'code', 'N/A')}, Msg={e}")
                    status_code = getattr(e, 'status_code', None); error_code = getattr(e, 'code', None)
                    if status_code == 429: 
                        wait_time = 60
                        if attempt < max_attempts_per_chunk: 
                            pbar.write("Warning: Rate limit likely hit. Waiting...")
                    elif status_code == 418: 
                        wait_time = 120
                        if attempt < max_attempts_per_chunk:
                            pbar.write("Warning: IP ban likely. Waiting...")
                    elif error_code == -1121:
                        # Use pbar.write for the specific error
                        error_msg_text = f"Invalid symbol '{binance_ticker}'. Stopping."
                        pbar.write(f"Error: {error_msg_text}")
                        metrics["error_message"] = error_msg_text  # Store specific error message
                        return None, metrics  # Return immediately for invalid symbol
                    else: pbar.write("Error: Non-retriable/unknown API error."); break
                except Exception as e:
                    pbar.write(f"Error: Unexpected error attempt {attempt}/{max_attempts_per_chunk}: {type(e).__name__}: {e}")
                    pbar.write(f"Traceback:\n{traceback.format_exc()}"); break

                if wait_time > 0 and attempt < max_attempts_per_chunk: time.sleep(wait_time); continue
                if not success and wait_time == 0 and attempt < max_attempts_per_chunk: time.sleep(3 * attempt); continue

            # --- After attempting a chunk ---
            if not success:
                 error_msg = f"Failed to fetch Binance chunk after {max_attempts_per_chunk} attempts."
                 pbar.write(f"Error: {error_msg} Stopping.")
                 return None, {**metrics, "error_message": error_msg}

            if not klines_chunk: break # Exit outer loop if empty chunk received

            metrics["rows_fetched"] += len(klines_chunk)
            all_klines_raw.extend(klines_chunk)
            last_kline_time_ms = klines_chunk[-1][0]

            # --- Update tqdm ---
            processed_up_to_ms = last_kline_time_ms
            update_amount = max(0, processed_up_to_ms - last_processed_ms)
            if update_amount > 0: pbar.update(update_amount); last_processed_ms = processed_up_to_ms

            current_start_ms = last_kline_time_ms + 1
            if len(klines_chunk) < limit_per_request: break
            if current_start_ms <= end_ms: time.sleep(request_delay_sec)

    finally:
        # Clear the postfix message and close the bar
        pbar.set_postfix_str("")
        # Update pbar to 100% if loop finished early/normally
        final_update = total_duration_ms - pbar.n
        if final_update > 0: pbar.update(final_update)
        pbar.close()

    # --- Combine and Process All Fetched Data ---
    if not all_klines_raw:
        logger.print_warning(f"No Binance data returned for '{binance_ticker}'.")
        return None, {**metrics, "error_message": "No data found for the specified criteria."}

    # logger.print_info(f"Converting {len(all_klines_raw)} raw klines to DataFrame...")

    columns = [
        'OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume',
        'CloseTime', 'QuoteAssetVolume', 'NumberTrades',
        'TakerBuyBaseVol', 'TakerBuyQuoteVol', 'Ignore'
    ]
    try: df = pd.DataFrame(all_klines_raw, columns=columns)
    except ValueError as e:
         logger.print_error(f"Error creating DataFrame from Binance data: {e}"); return None, metrics

    # --- Data Type Conversion and Selection ---
    df['DateTime'] = pd.to_datetime(df['OpenTime'], unit='ms', errors='coerce')
    df.dropna(subset=['DateTime'], inplace=True)
    if df.empty: logger.print_warning("Binance data empty after DateTime conversion."); return None, metrics
    df.set_index('DateTime', inplace=True)

    ohlcv_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in ohlcv_cols: df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=['Open', 'High', 'Low', 'Close'], inplace=True)
    df = df[ohlcv_cols]

    # ... (duplicate removal, sorting) ...
    initial_rows = len(df)
    df = df[~df.index.duplicated(keep='first')]
    rows_dropped = initial_rows - len(df)
    if rows_dropped > 0: logger.print_debug(f"Removed {rows_dropped} duplicate rows.")
    df.sort_index(inplace=True)
    if df.empty: logger.print_warning("Binance data empty after processing."); return None, metrics


    logger.print_success(f"Successfully fetched and processed {len(df)} rows from Binance.")
    # logger.print_debug(f"Total Binance API call latency (sum of successful chunks): {metrics['total_latency_sec']:.3f} seconds")
    return df, metrics