# Improved Binance Fetcher with Debug Information and Slow Progress Updates

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

def fetch_binance_data(ticker, interval, start_date, end_date, api_key=None, api_secret=None):
    """
    Fetch historical klines data from Binance Spot API with improved progress tracking.
    
    Args:
        ticker: Trading pair symbol (e.g., 'ETHUSDT')
        interval: Time interval (e.g., 'H1', 'M1', 'D1')
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        api_key: Binance API key (optional)
        api_secret: Binance API secret (optional)
    
    Returns:
        tuple: (DataFrame, metrics_dict) or (None, error_dict)
    """
    
    if not BINANCE_AVAILABLE:
        error_msg = "Binance library not available. Install with: pip install python-binance"
        logger.print_error(error_msg)
        return None, {"error_message": error_msg}
    
    # Debug information
    logger.print_debug(f"=== BINANCE FETCHER DEBUG INFO ===")
    logger.print_debug(f"Ticker: {ticker}")
    logger.print_debug(f"Interval: {interval}")
    logger.print_debug(f"Start Date: {start_date}")
    logger.print_debug(f"End Date: {end_date}")
    logger.print_debug(f"API Key Available: {bool(api_key)}")
    logger.print_debug(f"API Secret Available: {bool(api_secret)}")
    
    # Map interval to Binance format
    interval_mapping = {
        'M1': BinanceClient.KLINE_INTERVAL_1MINUTE,
        'M5': BinanceClient.KLINE_INTERVAL_5MINUTE,
        'M15': BinanceClient.KLINE_INTERVAL_15MINUTE,
        'M30': BinanceClient.KLINE_INTERVAL_30MINUTE,
        'H1': BinanceClient.KLINE_INTERVAL_1HOUR,
        'H4': BinanceClient.KLINE_INTERVAL_4HOUR,
        'D1': BinanceClient.KLINE_INTERVAL_1DAY,
        'W1': BinanceClient.KLINE_INTERVAL_1WEEK,
        'MN1': BinanceClient.KLINE_INTERVAL_1MONTH
    }
    
    binance_interval = interval_mapping.get(interval)
    if not binance_interval:
        error_msg = f"Unsupported interval: {interval}. Supported: {list(interval_mapping.keys())}"
        logger.print_error(error_msg)
        return None, {"error_message": error_msg}
    
    # Map ticker to Binance format
    binance_ticker = ticker.upper()
    logger.print_debug(f"Mapped ticker '{ticker}' to Binance format '{binance_ticker}'")
    
    # Initialize Binance client
    try:
        if api_key and api_secret:
            client = BinanceClient(api_key, api_secret)
            logger.print_debug("Using authenticated Binance client")
        else:
            client = BinanceClient()
            logger.print_debug("Using public Binance client (no API key)")
    except Exception as e:
        error_msg = f"Failed to initialize Binance client: {e}"
        logger.print_error(error_msg)
        return None, {"error_message": error_msg}
    
    # Convert dates to milliseconds
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        start_ms = int(start_dt.timestamp() * 1000)
        end_ms = int(end_dt.timestamp() * 1000)
        logger.print_debug(f"Date range (ms): {start_ms} to {end_ms}")
        logger.print_debug(f"Date range (human): {start_dt} to {end_dt}")
    except ValueError:
        error_msg = f"Invalid date format for start_date ('{start_date}') or end_date ('{end_date}'). Use YYYY-MM-DD."
        logger.print_error(error_msg)
        return None, {"error_message": error_msg}
    
    # Calculate estimated data size and chunks
    total_duration_ms = max(0, end_ms - start_ms)
    estimated_rows = total_duration_ms // (1000 * 60 * 60)  # Rough estimate for hourly data
    estimated_chunks = max(1, estimated_rows // 1000)  # ~1000 rows per chunk
    estimated_data_size_kb = max(100, estimated_rows * 0.12)  # ~120 bytes per row = 0.12 KB per row
    
    logger.print_debug(f"Estimated rows: {estimated_rows}")
    logger.print_debug(f"Estimated chunks: {estimated_chunks}")
    logger.print_debug(f"Estimated data size: {estimated_data_size_kb:.1f}KB")
    
    # Initialize progress tracking
    all_klines_raw = []
    limit_per_request = 1000
    current_start_ms = start_ms
    initial_start_ms = start_ms
    max_attempts_per_chunk = 5
    request_delay_sec = 0.5
    
    # Initialize progress bar with slow updates
    pbar = tqdm(total=estimated_data_size_kb, unit='KB', desc=f"Fetching {binance_ticker}", leave=True, ascii=True, unit_scale=True, 
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}KB [{elapsed}<{remaining}, {rate_fmt}]')
    
    chunks_processed = 0
    total_data_loaded_kb = 0.0
    total_rows_downloaded = 0
    
    # Add slow progress updates before API calls
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
            
            # Update progress bar with detailed information
            pbar.set_postfix_str(f"Chunk {chunks_processed + 1}/{estimated_chunks} | {next_chunk_start_dt.strftime('%Y-%m-%d %H:%M')} | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows | {progress_percent:.1f}% | {eta_str}", refresh=True)
            
            # Force display update
            import sys
            sys.stdout.flush()
            
            # API call logic with retries
            attempt = 0
            klines_chunk = None
            success = False
            
            while attempt < max_attempts_per_chunk:
                attempt += 1
                wait_time = 0
                
                # Show API request progress
                if attempt == 1:
                    pbar.set_postfix_str(f"Requesting chunk {chunks_processed + 1}... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    sys.stdout.flush()
                
                try:
                    start_chunk_time = time.perf_counter()
                    
                    # Make API call
                    klines_chunk = client.get_historical_klines(
                        symbol=binance_ticker,
                        interval=binance_interval,
                        start_str=current_start_ms,
                        end_str=end_ms,
                        limit=limit_per_request
                    )
                    
                    end_chunk_time = time.perf_counter()
                    chunk_latency = end_chunk_time - start_chunk_time
                    success = True
                    
                    # Show processing progress
                    pbar.set_postfix_str(f"Processing chunk {chunks_processed + 1}... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    
                    # Add delay to make progress visible
                    time.sleep(0.2)
                    pbar.refresh()
                    break
                    
                except (BinanceAPIException, BinanceRequestException) as e:
                    status_code = getattr(e, 'status_code', None)
                    error_code = getattr(e, 'code', None)
                    
                    if status_code == 429:  # Rate limit
                        wait_time = 60
                        if attempt < max_attempts_per_chunk:
                            pbar.write("Warning: Rate limit hit. Waiting...")
                            pbar.set_postfix_str(f"Rate limited, waiting... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    elif status_code == 418:  # IP ban
                        wait_time = 120
                        if attempt < max_attempts_per_chunk:
                            pbar.write("Warning: IP ban detected. Waiting...")
                            pbar.set_postfix_str(f"IP banned, waiting... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    elif error_code == -1121:  # Invalid symbol
                        error_msg_text = f"Invalid symbol '{binance_ticker}'. Stopping."
                        pbar.write(f"Error: {error_msg_text}")
                        return None, {"error_message": error_msg_text}
                    else:
                        pbar.write(f"API Error: {e}")
                        if attempt < max_attempts_per_chunk:
                            pbar.set_postfix_str(f"Retrying chunk {chunks_processed + 1} (attempt {attempt + 1})... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                
                if wait_time > 0 and attempt < max_attempts_per_chunk:
                    time.sleep(wait_time)
                    continue
                if not success and wait_time == 0 and attempt < max_attempts_per_chunk:
                    pbar.set_postfix_str(f"Retrying chunk {chunks_processed + 1} (attempt {attempt + 1})... | {total_data_loaded_kb:.1f}KB | {total_rows_downloaded} rows", refresh=True)
                    time.sleep(3 * attempt)
                    continue
            
            # Handle failed chunk
            if not success:
                error_msg = f"Failed to fetch Binance chunk after {max_attempts_per_chunk} attempts."
                pbar.write(f"Error: {error_msg} Stopping.")
                return None, {"error_message": error_msg}
            
            # Process successful chunk
            if klines_chunk:
                all_klines_raw.extend(klines_chunk)
                last_kline_time_ms = klines_chunk[-1][0]
                chunks_processed += 1
                
                # Calculate actual data size loaded
                chunk_rows = len(klines_chunk)
                chunk_data_size_kb = chunk_rows * 0.12  # ~120 bytes per row
                total_data_loaded_kb += chunk_data_size_kb
                total_rows_downloaded += chunk_rows
                
                # Update progress bar
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
        
        # Clear the postfix message and close the bar
        pbar.set_postfix_str("")
        pbar.n = total_data_loaded_kb
        pbar.refresh()
        pbar.close()
    
    # Process final data
    if not all_klines_raw:
        logger.print_warning(f"No Binance data returned for '{binance_ticker}'.")
        return None, {"error_message": "No data found for the specified criteria."}
    
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
    
    # Return success metrics
    metrics = {
        "rows_fetched": len(df),
        "api_calls": chunks_processed,
        "successful_chunks": chunks_processed,
        "total_latency_sec": 0,  # Will be calculated in main function
        "data_size_kb": total_data_loaded_kb,
        "total_rows_downloaded": total_rows_downloaded
    }
    
    logger.print_debug(f"=== BINANCE FETCHER COMPLETED ===")
    logger.print_debug(f"Final rows: {len(df)}")
    logger.print_debug(f"Final data size: {total_data_loaded_kb:.1f}KB")
    logger.print_debug(f"Chunks processed: {chunks_processed}")
    
    return df, metrics
