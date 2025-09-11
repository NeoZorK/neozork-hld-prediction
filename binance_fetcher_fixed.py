# Fixed Binance Fetcher with proper progress bar completion

import pandas as pd
import os
import time
import traceback
import threading
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
    """ Downloads OHLCV data from Binance Spot API with pagination and tqdm progress. """
    if not BINANCE_AVAILABLE:
        logger.print_error("Binance Connector library ('python-binance') is not installed.")
        return None, {"error_message": "python-binance not installed"}

    logger.print_info(f"Attempting to fetch Binance data for: {ticker} | {interval} | {start_date} to {end_date}")
    metrics = {"total_latency_sec": 0.0, "api_calls": 0, "successful_chunks": 0, "rows_fetched": 0}

    # --- DEBUG INFORMATION ---
    logger.print_debug(f"=== BINANCE FETCHER DEBUG INFO ===")
    logger.print_debug(f"Ticker: {ticker}")
    logger.print_debug(f"Interval: {interval}")
    logger.print_debug(f"Start Date: {start_date}")
    logger.print_debug(f"End Date: {end_date}")

    # --- Map Ticker and Interval ---
    binance_ticker = map_binance_ticker(ticker)
    binance_interval_str = map_binance_interval(interval)
    if binance_interval_str is None: return None, {"error_message": f"Invalid interval: {interval}"}

    logger.print_debug(f"Binance Ticker: {binance_ticker}")
    logger.print_debug(f"Binance Interval: {binance_interval_str}")

    # --- Get API Key/Secret (Optional) ---
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret: logger.print_info("Binance API Key/Secret not found. Proceeding with public access.")

    logger.print_debug(f"API Key Available: {bool(api_key)}")
    logger.print_debug(f"API Secret Available: {bool(api_secret)}")

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

    logger.print_debug(f"Date range (ms): {start_ms} ({start_dt_obj}) to {end_ms} ({end_dt_obj})")
    logger.print_debug(f"Total duration: {end_ms - start_ms} ms")

    # --- Pagination Logic ---
    all_klines_raw = []
    limit_per_request = 1000
    current_start_ms = start_ms
    initial_start_ms = start_ms
    total_duration_ms = max(0, end_ms - initial_start_ms)
    max_attempts_per_chunk = 5
    request_delay_sec = 0.5

    # --- Calculate estimated chunks and data size ---
    estimated_rows = (end_ms - start_ms) // (1000 * 60 * 60)  # Rough estimate for hourly data
    estimated_chunks = max(1, estimated_rows // 1000)  # ~1000 rows per chunk
    estimated_data_size_kb = max(100, estimated_rows * 0.12)  # ~120 bytes per row = 0.12 KB per row

    logger.print_debug(f"Estimated rows: {estimated_rows}")
    logger.print_debug(f"Estimated chunks: {estimated_chunks}")
    logger.print_debug(f"Estimated data size: {estimated_data_size_kb:.1f}KB")

    # --- Initialize tqdm with data size progress ---
    pbar = tqdm(total=estimated_data_size_kb, unit='KB', desc=f"Fetching {binance_ticker}", leave=True, ascii=True, unit_scale=True, 
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}KB [{elapsed}<{remaining}, {rate_fmt}]')
    
    chunks_processed = 0
    total_data_loaded_kb = 0.0
    total_rows_downloaded = 0

    # --- SLOW PROGRESS UPDATER ---
    def slow_progress_updater():
        """Update progress slowly even before data is fetched"""
        nonlocal total_data_loaded_kb
        while chunks_processed == 0 and total_data_loaded_kb == 0:
            # Simulate slow progress during setup phase
            setup_progress = min(5.0, pbar.format_dict['elapsed'] * 0.5)  # Max 5KB during setup
            pbar.n = setup_progress
            pbar.set_postfix_str(f"Initializing... | {setup_progress:.1f}KB | Setup phase", refresh=True)
            pbar.refresh()
            time.sleep(0.5)
    
    # Start slow progress updater in background
    progress_thread = threading.Thread(target=slow_progress_updater, daemon=True)
    progress_thread.start()

    try:
        logger.print_debug("Starting data fetching loop...")
        
        while current_start_ms <= end_ms:
            next_chunk_start_dt = datetime.fromtimestamp(current_start_ms / 1000)
            progress_percent = (total_data_loaded_kb / estimated_data_size_kb) * 100 if estimated_data_size_kb > 0 else 0
            
            # Estimate remaining time
            if total_data_loaded_kb > 0:
                avg_speed_kb_per_sec = total_data_loaded_kb / pbar.format_dict['elapsed'] if pbar.format_dict['elapsed'] > 0 else 0
                remaining_kb = estimated_data_size_kb - total_data_loaded_kb
                eta_seconds = remaining_kb / avg_speed_kb_per_sec if avg_speed_kb_per_sec > 0 else 0
                eta_str = f"ETA: {eta_seconds:.1f}s" if eta_seconds < 60 else f"ETA: {eta_seconds/60:.1f}m"
            else:
                eta_str = "ETA: calculating..."
            
            pbar.set_postfix_str(f"Chunk {chunks_processed + 1}/{estimated_chunks} | {next_chunk_start_dt.strftime('%Y-%m-%d %H:%M')} | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows | {progress_percent:.1f}% | {eta_str}", refresh=True)
            
            # Force display update
            import sys
            sys.stdout.flush()

            attempt = 0; klines_chunk = None; success = False
            while attempt < max_attempts_per_chunk:
                attempt += 1; wait_time = 0
                
                # Show API request progress
                if attempt == 1:
                    pbar.set_postfix_str(f"Requesting chunk {chunks_processed + 1}... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    sys.stdout.flush()
                
                try:
                    start_chunk_time = time.perf_counter()
                    metrics["api_calls"] += 1
                    
                    # Show downloading progress
                    pbar.set_postfix_str(f"Downloading chunk {chunks_processed + 1}... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    sys.stdout.flush()
                    
                    # Make API call
                    klines_chunk = client.get_historical_klines(
                        symbol=binance_ticker,
                        interval=binance_interval_str,
                        start_str=current_start_ms,
                        end_str=end_ms,
                        limit=limit_per_request
                    )
                    
                    end_chunk_time = time.perf_counter(); chunk_latency = end_chunk_time - start_chunk_time
                    success = True; metrics["total_latency_sec"] += chunk_latency
                    metrics["successful_chunks"] += 1
                    
                    # Show processing progress
                    pbar.set_postfix_str(f"Processing chunk {chunks_processed + 1}... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    
                    # Add delay to make progress visible
                    time.sleep(0.2)
                    pbar.refresh()
                    break

                except (BinanceAPIException, BinanceRequestException) as e:
                    status_code = getattr(e, 'status_code', None); error_code = getattr(e, 'code', None)
                    if status_code == 429: 
                        wait_time = 60
                        if attempt < max_attempts_per_chunk: 
                            pbar.write("Warning: Rate limit likely hit. Waiting...")
                            pbar.set_postfix_str(f"Rate limited, waiting... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    elif status_code == 418: 
                        wait_time = 120
                        if attempt < max_attempts_per_chunk:
                            pbar.write("Warning: IP ban likely. Waiting...")
                            pbar.set_postfix_str(f"IP banned, waiting... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    elif error_code == -1121:
                        error_msg_text = f"Invalid symbol '{binance_ticker}'. Stopping."
                        pbar.write(f"Error: {error_msg_text}")
                        metrics["error_message"] = error_msg_text
                        return None, metrics
                    else:
                        pbar.write(f"API Error: {e}")
                        if attempt < max_attempts_per_chunk:
                            pbar.set_postfix_str(f"Retrying chunk {chunks_processed + 1} (attempt {attempt + 1})... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                except Exception as e:
                    pbar.write(f"Unexpected error: {e}")
                    pbar.write(f"Traceback:\n{traceback.format_exc()}"); break

                if wait_time > 0 and attempt < max_attempts_per_chunk: 
                    time.sleep(wait_time); 
                    continue
                if not success and wait_time == 0 and attempt < max_attempts_per_chunk: 
                    pbar.set_postfix_str(f"Retrying chunk {chunks_processed + 1} (attempt {attempt + 1})... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    time.sleep(3 * attempt); 
                    continue

            # --- After attempting a chunk ---
            if not success:
                 error_msg = f"Failed to fetch Binance chunk after {max_attempts_per_chunk} attempts."
                 pbar.write(f"Error: {error_msg} Stopping.")
                 return None, {"error_message": error_msg}

            # --- Process successful chunk ---
            if klines_chunk:
                metrics["rows_fetched"] += len(klines_chunk)
                all_klines_raw.extend(klines_chunk)
                last_kline_time_ms = klines_chunk[-1][0]
                chunks_processed += 1

                # --- Calculate actual data size loaded ---
                chunk_rows = len(klines_chunk)
                chunk_data_size_kb = chunk_rows * 0.12  # ~120 bytes per row
                total_data_loaded_kb += chunk_data_size_kb
                total_rows_downloaded += chunk_rows
                
                # Update progress bar with actual data size
                pbar.n = total_data_loaded_kb
                pbar.refresh()
                
                # Show completion status
                progress_percent = (total_data_loaded_kb / estimated_data_size_kb) * 100 if estimated_data_size_kb > 0 else 0
                pbar.set_postfix_str(f"Completed chunk {chunks_processed}/{estimated_chunks} | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows | {progress_percent:.1f}%", refresh=True)
                pbar.refresh()

                current_start_ms = last_kline_time_ms + 1
                if len(klines_chunk) < limit_per_request:
                    break
                if current_start_ms <= end_ms: 
                    pbar.set_postfix_str(f"Preparing next chunk... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    time.sleep(request_delay_sec)

    finally:
        # Stop the slow progress updater
        if 'progress_thread' in locals():
            progress_thread.join(timeout=1)
            
        # --- FIXED: Ensure progress bar shows 100% before closing ---
        # Update progress bar to show completion
        pbar.n = total_data_loaded_kb
        pbar.set_postfix_str(f"Completed: {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows | 100.0%", refresh=True)
        pbar.refresh()
        
        # Small delay to show final state
        time.sleep(0.5)
        
        # Clear the postfix message and close the bar
        pbar.set_postfix_str("")
        pbar.refresh()
        pbar.close()

    # --- Combine and Process All Fetched Data ---
    if not all_klines_raw:
        logger.print_warning(f"No Binance data returned for '{binance_ticker}'.")
        return None, {**metrics, "error_message": "No data found for the specified criteria."}
    
    # Log final download statistics
    logger.print_info(f"Successfully downloaded {total_rows_downloaded} rows ({total_data_loaded_kb:.1f}KB) from Binance.")

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
    
    # --- Final Debug Information ---
    logger.print_debug(f"=== BINANCE FETCHER COMPLETED ===")
    logger.print_debug(f"Final rows: {len(df)}")
    logger.print_debug(f"Final data size: {total_data_loaded_kb:.1f}KB")
    logger.print_debug(f"Chunks processed: {chunks_processed}")

    return df, metrics
