# Enhanced Binance Fetcher with Small Chunks and Detailed Progress Control

import pandas as pd
import os
import time
import traceback
import signal
from datetime import datetime, timedelta
from tqdm import tqdm
from src.common import logger

# Binance specific imports and checks
try:
    from binance.client import Client as BinanceClient
    from binance.exceptions import BinanceAPIException, BinanceRequestException
    BINANCE_AVAILABLE = True
except ImportError:
    BINANCE_AVAILABLE = False
    class BinanceClient:
        KLINE_INTERVAL_1MINUTE = '1m'; KLINE_INTERVAL_5MINUTE = '5m'; KLINE_INTERVAL_15MINUTE = '15m';
        KLINE_INTERVAL_30MINUTE = '30m'; KLINE_INTERVAL_1HOUR = '1h'; KLINE_INTERVAL_4HOUR = '4h';
        KLINE_INTERVAL_1DAY = '1d'; KLINE_INTERVAL_1WEEK = '1w'; KLINE_INTERVAL_1MONTH = '1M'
    class BinanceAPIException(Exception): pass
    class BinanceRequestException(Exception): pass

# Global flag for graceful shutdown during data fetching
shutdown_requested = False

def check_shutdown_requested():
    """Check if a shutdown signal has been received during data fetching."""
    return shutdown_requested

def signal_handler(signum, frame):
    """Handle CTRL+C gracefully during data fetching."""
    global shutdown_requested
    if not shutdown_requested:
        shutdown_requested = True
        logger.print_info("🛑 Shutdown requested during data fetching... Please wait for current chunk to complete.")
    else:
        logger.print_info("⚠️  Force exit requested during data fetching.")
        raise KeyboardInterrupt("Force exit requested")

def map_binance_interval(tf_input: str) -> str | None:
    """Maps timeframe input to Binance interval string."""
    mapping = {
        'M1': BinanceClient.KLINE_INTERVAL_1MINUTE, 'M5': BinanceClient.KLINE_INTERVAL_5MINUTE,
        'M15': BinanceClient.KLINE_INTERVAL_15MINUTE, 'M30': BinanceClient.KLINE_INTERVAL_30MINUTE,
        'H1': BinanceClient.KLINE_INTERVAL_1HOUR, 'H4': BinanceClient.KLINE_INTERVAL_4HOUR,
        'D1': BinanceClient.KLINE_INTERVAL_1DAY, 'W1': BinanceClient.KLINE_INTERVAL_1WEEK, 'MN1': BinanceClient.KLINE_INTERVAL_1MONTH
    }
    valid_binance_intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
    tf_input_upper = tf_input.upper()
    if tf_input_upper in mapping: return mapping[tf_input_upper]
    elif tf_input in valid_binance_intervals: return tf_input
    else:
        logger.print_error(f"Invalid Binance timeframe input: '{tf_input}'. Use M1, H1, D1 etc. or Binance intervals like '1m', '1h', '1d'.")
        return None

def map_binance_ticker(ticker_input: str) -> str:
    """Formats ticker for Binance (uppercase, no separators)."""
    ticker = ticker_input.upper().replace('/', '').replace('-', '')
    logger.print_debug(f"Mapped ticker '{ticker_input}' to Binance format '{ticker}'")
    return ticker

def fetch_binance_data(ticker: str, interval: str, start_date: str, end_date: str) -> tuple[pd.DataFrame | None, dict]:
    """ Downloads OHLCV data from Binance Spot API with small chunks and detailed progress control. """
    global shutdown_requested
    shutdown_requested = False  # Reset shutdown flag for new fetch
    
    # Register signal handler for graceful shutdown during data fetching
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
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
        start_ms = int(start_dt_obj.timestamp() * 1000)
        end_ms = int(end_dt_obj.timestamp() * 1000)
    except ValueError:
        error_msg = f"Invalid date format for start_date ('{start_date}') or end_date ('{end_date}'). Use YYYY-MM-DD."
        logger.print_error(error_msg)
        return None, {"error_message": error_msg}

    # --- Enhanced Chunking Logic ---
    all_klines_raw = []
    
    # Determine optimal chunk size based on interval
    interval_minutes = {
        '1m': 1, '3m': 3, '5m': 5, '15m': 15, '30m': 30,
        '1h': 60, '2h': 120, '4h': 240, '6h': 360, '8h': 480, '12h': 720,
        '1d': 1440, '3d': 4320, '1w': 10080, '1M': 43200
    }
    
    interval_min = interval_minutes.get(binance_interval_str, 60)
    
    # Calculate chunk size based on time duration (max 1000 records per API call)
    max_records_per_chunk = 1000  # Binance API limit
    # Use time-based chunking: each chunk covers 1000 records worth of time
    chunk_duration_ms = max_records_per_chunk * interval_min * 60 * 1000  # Convert to milliseconds
    
    # Calculate total chunks needed
    total_duration_ms = end_ms - start_ms
    total_chunks = max(1, (total_duration_ms + chunk_duration_ms - 1) // chunk_duration_ms)  # Ceiling division
    
    # Estimate total data size
    estimated_rows = total_duration_ms // (interval_min * 60 * 1000)
    estimated_data_size_kb = max(100, estimated_rows * 0.12)  # ~120 bytes per row
    
    logger.print_debug(f"Total chunks needed: {total_chunks}")
    logger.print_debug(f"Estimated rows: {estimated_rows}")
    logger.print_debug(f"Estimated data size: {estimated_data_size_kb:.1f}KB")

    # --- Initialize Progress Bar (only one, no stuck progress bar) ---
    pbar = tqdm(
        total=total_chunks, 
        unit='chunks', 
        desc=f"Fetching {binance_ticker}", 
        leave=True, 
        ascii=True, 
        unit_scale=False,
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} chunks [{elapsed}<{remaining}, {rate_fmt}] {postfix}'
    )
    
    chunks_processed = 0
    total_data_loaded_kb = 0.0
    total_rows_downloaded = 0
    current_start_ms = start_ms
    max_attempts_per_chunk = 3
    request_delay_sec = 0.3

    try:
        while current_start_ms < end_ms:
            # Check for shutdown request before processing each chunk
            if check_shutdown_requested():
                logger.print_info("🛑 Shutdown requested during data fetching. Stopping gracefully...")
                pbar.close()
                return None, {**metrics, "error_message": "Shutdown requested by user"}
            
            # Calculate current chunk end time
            current_chunk_end_ms = min(current_start_ms + chunk_duration_ms, end_ms)
            
            # Show detailed progress information
            chunk_start_dt = datetime.fromtimestamp(current_start_ms / 1000)
            chunk_end_dt = datetime.fromtimestamp(current_chunk_end_ms / 1000)
            
            # Calculate progress percentage
            progress_percent = (chunks_processed / total_chunks) * 100 if total_chunks > 0 else 0
            
            # Update progress bar with detailed information
            pbar.set_postfix_str(
                f"Chunk {chunks_processed + 1}/{total_chunks} | "
                f"{chunk_start_dt.strftime('%Y-%m-%d %H:%M')} to {chunk_end_dt.strftime('%Y-%m-%d %H:%M')} | "
                f"{total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows | {progress_percent:.1f}%"
            )
            
            # Force display update
            import sys
            sys.stdout.flush()

            # --- API Call with Retry Logic ---
            attempt = 0
            klines_chunk = None
            success = False
            
            while attempt < max_attempts_per_chunk:
                # Check for shutdown request before each retry attempt
                if check_shutdown_requested():
                    logger.print_info("🛑 Shutdown requested during chunk retry. Stopping gracefully...")
                    pbar.close()
                    return None, {**metrics, "error_message": "Shutdown requested by user"}
                
                attempt += 1
                wait_time = 0
                
                try:
                    start_chunk_time = time.perf_counter()
                    metrics["api_calls"] += 1
                    
                    # Make API call with small chunk
                    klines_chunk = client.get_historical_klines(
                        symbol=binance_ticker,
                        interval=binance_interval_str,
                        start_str=current_start_ms,
                        end_str=current_chunk_end_ms,
                        limit=max_records_per_chunk
                    )
                    
                    end_chunk_time = time.perf_counter()
                    chunk_latency = end_chunk_time - start_chunk_time
                    success = True
                    metrics["total_latency_sec"] += chunk_latency
                    metrics["successful_chunks"] += 1
                    break

                except (BinanceAPIException, BinanceRequestException) as e:
                    status_code = getattr(e, 'status_code', None)
                    error_code = getattr(e, 'code', None)
                    
                    if status_code == 429:  # Rate limit
                        wait_time = 60
                        if attempt < max_attempts_per_chunk:
                            pbar.write("Warning: Rate limit hit. Waiting...")
                    elif status_code == 418:  # IP ban
                        wait_time = 120
                        if attempt < max_attempts_per_chunk:
                            pbar.write("Warning: IP ban detected. Waiting...")
                    elif error_code == -1121:  # Invalid symbol
                        error_msg_text = f"Invalid symbol '{binance_ticker}'. Stopping."
                        pbar.write(f"Error: {error_msg_text}")
                        metrics["error_message"] = error_msg_text
                        return None, metrics
                    else:
                        pbar.write(f"API Error: {e}")
                except KeyboardInterrupt:
                    logger.print_info("🛑 KeyboardInterrupt received during data fetching. Stopping gracefully...")
                    pbar.close()
                    return None, {**metrics, "error_message": "Interrupted by user"}
                except Exception as e:
                    pbar.write(f"Unexpected error: {e}")
                    pbar.write(f"Traceback:\n{traceback.format_exc()}")
                    break

                if wait_time > 0 and attempt < max_attempts_per_chunk:
                    time.sleep(wait_time)
                    continue
                if not success and wait_time == 0 and attempt < max_attempts_per_chunk:
                    time.sleep(2 * attempt)  # Exponential backoff
                    continue

            # --- Handle Failed Chunk ---
            if not success:
                error_msg = f"Failed to fetch Binance chunk {chunks_processed + 1} after {max_attempts_per_chunk} attempts."
                pbar.write(f"Error: {error_msg} Stopping.")
                return None, {"error_message": error_msg}

            # --- Process Successful Chunk ---
            if klines_chunk:
                metrics["rows_fetched"] += len(klines_chunk)
                all_klines_raw.extend(klines_chunk)
                chunks_processed += 1

                # Calculate actual data size loaded
                chunk_rows = len(klines_chunk)
                chunk_data_size_kb = chunk_rows * 0.12  # ~120 bytes per row
                total_data_loaded_kb += chunk_data_size_kb
                total_rows_downloaded += chunk_rows
                
                # Update progress bar
                pbar.update(1)  # Increment by 1 chunk
                
                # Show completion status
                progress_percent = (chunks_processed / total_chunks) * 100 if total_chunks > 0 else 0
                pbar.set_postfix_str(
                    f"Completed chunk {chunks_processed}/{total_chunks} | "
                    f"{total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows | {progress_percent:.1f}%"
                )
                pbar.refresh()

                # Move to next chunk
                if len(klines_chunk) < max_records_per_chunk:
                    # Last chunk or no more data
                    break
                
                current_start_ms = current_chunk_end_ms
                
                # Small delay between chunks
                if current_start_ms < end_ms:
                    time.sleep(request_delay_sec)

    except KeyboardInterrupt:
        logger.print_info("🛑 KeyboardInterrupt received during main data fetching loop. Stopping gracefully...")
        pbar.close()
        return None, {**metrics, "error_message": "Interrupted by user"}
    finally:
        # --- Ensure progress bar shows 100% before closing ---
        pbar.n = total_chunks
        pbar.set_postfix_str(f"Completed: {total_chunks}/{total_chunks} chunks | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows | 100.0%")
        pbar.refresh()
        time.sleep(0.5)
        pbar.close()

    # --- Combine and Process All Fetched Data ---
    if not all_klines_raw:
        logger.print_warning(f"No Binance data returned for '{binance_ticker}'.")
        return None, {**metrics, "error_message": "No data found for the specified criteria."}
    
    # Log final download statistics
    logger.print_info(f"Successfully downloaded {total_rows_downloaded} rows ({total_data_loaded_kb:.1f}KB) from Binance in {chunks_processed} chunks.")

    # Convert to DataFrame
    columns = [
        'OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume',
        'CloseTime', 'QuoteAssetVolume', 'NumberTrades',
        'TakerBuyBaseVol', 'TakerBuyQuoteVol', 'Ignore'
    ]
    
    try:
        df = pd.DataFrame(all_klines_raw, columns=columns)
    except ValueError as e:
        logger.print_error(f"Error creating DataFrame from Binance data: {e}")
        return None, {"error_message": str(e)}
    
    # Process DataFrame
    df['DateTime'] = pd.to_datetime(df['OpenTime'], unit='ms', errors='coerce')
    df.dropna(subset=['DateTime'], inplace=True)
    if df.empty:
        logger.print_warning("Binance data empty after DateTime conversion.")
        return None, {"error_message": "No valid data after processing"}
    
    df.set_index('DateTime', inplace=True)
    
    ohlcv_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in ohlcv_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.dropna(subset=['Open', 'High', 'Low', 'Close'], inplace=True)
    df = df[ohlcv_cols]
    
    # Remove duplicates and sort
    initial_rows = len(df)
    df = df[~df.index.duplicated(keep='first')]
    rows_dropped = initial_rows - len(df)
    if rows_dropped > 0:
        logger.print_debug(f"Removed {rows_dropped} duplicate rows.")
    
    df.sort_index(inplace=True)
    if df.empty:
        logger.print_warning("Binance data empty after processing.")
        return None, {"error_message": "No valid data after processing"}

    return df, metrics