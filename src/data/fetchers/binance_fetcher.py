# NeoZorK HLD/src/data/fetchers/binance_fetcher.py (with tqdm)

"""
Contains functions related to fetching data from Binance Spot API.
Includes interval/ticker mapping and the main data download function with pagination.
"""

import pandas as pd
import os
import time # Import time
import traceback
from datetime import datetime, timedelta
from tqdm import tqdm # <--- Импортируем tqdm
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
    class BinanceClient:
        KLINE_INTERVAL_1MINUTE = '1m'; KLINE_INTERVAL_5MINUTE = '5m'; KLINE_INTERVAL_15MINUTE = '15m';
        KLINE_INTERVAL_30MINUTE = '30m'; KLINE_INTERVAL_1HOUR = '1h'; KLINE_INTERVAL_4HOUR = '4h';
        KLINE_INTERVAL_1DAY = '1d'; KLINE_INTERVAL_1WEEK = '1w'; KLINE_INTERVAL_1MONTH = '1M'
    class BinanceAPIException(Exception): pass
    class BinanceRequestException(Exception): pass


# Definition of map_binance_interval function (remains the same)
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


# Definition of map_binance_ticker function (remains the same)
def map_binance_ticker(ticker_input: str) -> str:
    """Formats ticker for Binance (uppercase, no separators)."""
    ticker = ticker_input.upper().replace('/', '').replace('-', '')
    logger.print_debug(f"Mapped ticker '{ticker_input}' to Binance format '{ticker}'")
    return ticker


# Definition of fetch_binance_data function
def fetch_binance_data(ticker: str, interval: str, start_date: str, end_date: str) -> tuple[pd.DataFrame | None, dict]:
    """
    Downloads OHLCV data from Binance Spot API for a specified date range.
    Handles pagination required by the Binance API (1000 klines limit).
    Assumes BINANCE_API_KEY and BINANCE_API_SECRET are loaded into env vars (optional).
    Returns a tuple: (DataFrame or None, metrics dictionary).
    """
    if not BINANCE_AVAILABLE:
        logger.print_error("Binance Connector library ('python-binance') is not installed.")
        return None, {}

    logger.print_info(f"Attempting to fetch Binance data for: {ticker} | interval: {interval} | start: {start_date} | end: {end_date}")
    metrics = {"total_latency_sec": 0.0}

    # --- Map Ticker and Interval ---
    binance_ticker = map_binance_ticker(ticker)
    binance_interval_str = map_binance_interval(interval)
    if binance_interval_str is None: return None, metrics

    # --- Get API Key/Secret (Optional) ---
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    # ... (logging key status) ...

    # --- Initialize Client ---
    try:
        client = BinanceClient(api_key=api_key, api_secret=api_secret)
        logger.print_debug("Binance client initialized.")
    except Exception as e:
        logger.print_error(f"Failed to initialize Binance client: {type(e).__name__}: {e}")
        return None, metrics

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
        return None, metrics

    # --- Pagination Logic for Binance get_historical_klines ---
    all_klines_raw = []
    limit_per_request = 1000
    current_start_ms = start_ms
    initial_start_ms = start_ms # <--- Сохраняем начальное время для расчета прогресса
    total_duration_ms = max(0, end_ms - initial_start_ms) # <--- Общая длительность для tqdm
    max_attempts_per_chunk = 5
    request_delay_sec = 0.15

    logger.print_info(f"Fetching Binance klines in chunks for '{binance_ticker}' ({binance_interval_str})...")

    # --- Инициализация tqdm ---
    pbar = tqdm(total=total_duration_ms, unit='ms', desc=f"Fetching {binance_ticker}", leave=True, unit_scale=False)
    last_processed_ms = initial_start_ms # Отслеживаем последнюю обработанную мс для обновления pbar

    try: # <--- Добавляем try для finally
        while current_start_ms <= end_ms:
            # logger.print_debug(f"  Fetching chunk starting from {datetime.fromtimestamp(current_start_ms / 1000)}") # Можно убрать для чистоты вывода
            attempt = 0
            chunk_latency = 0
            klines_chunk = None
            success = False # Флаг успеха для текущего чанка

            while attempt < max_attempts_per_chunk:
                attempt += 1
                wait_time = 0
                try:
                    start_chunk_time = time.perf_counter()
                    klines_chunk = client.get_historical_klines(
                        symbol=binance_ticker,
                        interval=binance_interval_str,
                        start_str=str(current_start_ms),
                        end_str=str(end_ms),
                        limit=limit_per_request
                    )
                    end_chunk_time = time.perf_counter()
                    chunk_latency = end_chunk_time - start_chunk_time
                    success = True
                    metrics["total_latency_sec"] += chunk_latency
                    logger.print_debug(f"    Chunk fetch attempt {attempt} successful ({chunk_latency:.3f} sec).")
                    break # Выход из цикла ретраев при успехе

                except (BinanceAPIException, BinanceRequestException) as e:
                    # ... (логика обработки ошибок API и ретраев остается прежней) ...
                    logger.print_error(f"    Binance API Error on chunk attempt {attempt}/{max_attempts_per_chunk}: Status={getattr(e, 'status_code', 'N/A')}, Code={getattr(e, 'code', 'N/A')}, Msg={e}")
                    status_code = getattr(e, 'status_code', None)
                    error_code = getattr(e, 'code', None)
                    if status_code == 429: wait_time = 60; logger.print_warning(...)
                    elif status_code == 418: wait_time = 120; logger.print_warning(...)
                    elif error_code == -1121:
                        logger.print_error(f"      Invalid symbol '{binance_ticker}' reported by Binance API. Stopping fetch.")
                        return None, metrics # Выход из функции
                    else:
                        logger.print_error(f"      Non-retriable or unknown API error. Skipping chunk fetch.")
                        break # Выход из цикла ретраев

                except Exception as e:
                    # ... (логика обработки неожиданных ошибок остается прежней) ...
                    logger.print_error(f"    Unexpected error during Binance chunk fetch attempt {attempt}/{max_attempts_per_chunk}: {type(e).__name__}: {e}")
                    break # Выход из цикла ретраев

                if wait_time > 0 and attempt < max_attempts_per_chunk: time.sleep(wait_time); continue
                if not success and wait_time == 0 and attempt < max_attempts_per_chunk: backoff_time = 3 * attempt; time.sleep(backoff_time); continue

            # --- После попыток получить чанк ---
            if not success:
                logger.print_error(f"Failed to fetch Binance chunk starting {datetime.fromtimestamp(current_start_ms / 1000)} after {max_attempts_per_chunk} attempts. Stopping.")
                return None, metrics # Выход, если чанк не удалось получить

            # --- Обработка успешного чанка ---
            if not klines_chunk:
                logger.print_debug("  Received empty kline chunk, assuming end of data range reached.")
                # Обновляем бар до конца перед выходом
                update_amount = total_duration_ms - pbar.n
                if update_amount > 0: pbar.update(update_amount)
                break

            all_klines_raw.extend(klines_chunk)
            # logger.print_debug(f"    Fetched {len(klines_chunk)} klines.") # Можно убрать

            last_kline_time_ms = klines_chunk[-1][0]
            # --- Обновление tqdm ---
            # Обновляем прогресс до *конца* последней свечи в чанке
            processed_up_to_ms = last_kline_time_ms
            update_amount = max(0, processed_up_to_ms - last_processed_ms) # Обновляем на дельту
            if update_amount > 0:
                pbar.update(update_amount)
                last_processed_ms = processed_up_to_ms # Обновляем последнюю обработанную точку

            # --- Готовимся к следующей итерации ---
            current_start_ms = last_kline_time_ms + 1

            if len(klines_chunk) < limit_per_request:
                 logger.print_debug("  Received less than limit, assuming end of data for range.")
                 # Обновляем бар до конца перед выходом
                 update_amount = total_duration_ms - pbar.n
                 if update_amount > 0: pbar.update(update_amount)
                 break

            if current_start_ms <= end_ms:
                 time.sleep(request_delay_sec)

    finally: # <--- Добавляем finally
        pbar.close() # <--- Гарантированно закрываем progress bar

    # --- Combine and Process All Fetched Data ---
    if not all_klines_raw:
        logger.print_warning(f"No Binance data returned for '{binance_ticker}' in the specified range {start_date} to {end_date}.")
        return None, metrics

    # logger.print_info(f"Converting {len(all_klines_raw)} raw klines to DataFrame...") # Можно убрать

    columns = [ # Полный список колонок из API
        'OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume',
        'CloseTime', 'QuoteAssetVolume', 'NumberTrades',
        'TakerBuyBaseVol', 'TakerBuyQuoteVol', 'Ignore'
    ]
    try:
        df = pd.DataFrame(all_klines_raw, columns=columns)
    except ValueError as e:
         logger.print_error(f"Error creating DataFrame from Binance data, possibly inconsistent list lengths: {e}")
         return None, metrics

    # --- Data Type Conversion and Selection ---
    df['DateTime'] = pd.to_datetime(df['OpenTime'], unit='ms', errors='coerce')
    df.dropna(subset=['DateTime'], inplace=True)
    if df.empty:
         logger.print_warning("Binance data became empty after handling DateTime errors.")
         return None, metrics
    df.set_index('DateTime', inplace=True)

    ohlcv_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in ohlcv_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(subset=['Open', 'High', 'Low', 'Close'], inplace=True) # Не дропаем по Volume

    # Переименовываем 'Volume' -> 'TickVolume' (если нужно для совместимости с CSV)
    # Оставляем оригинальный 'Volume', как возвращает API
    # df.rename(columns={'Volume': 'TickVolume'}, inplace=True)
    # ohlcv_cols = ['Open', 'High', 'Low', 'Close', 'TickVolume'] # Обновляем список, если переименовали

    df = df[ohlcv_cols] # Выбираем только нужные колонки

    initial_rows = len(df)
    df = df[~df.index.duplicated(keep='first')]
    rows_dropped = initial_rows - len(df)
    if rows_dropped > 0:
        logger.print_debug(f"Removed {rows_dropped} duplicate rows from Binance data.")

    df.sort_index(inplace=True)

    if df.empty:
        logger.print_warning(f"Binance data for '{binance_ticker}' became empty after processing.")
        return None, metrics

    logger.print_success(f"Successfully fetched and processed {len(df)} rows from Binance for '{binance_ticker}'.")
    logger.print_debug(f"Total Binance API call latency (sum of successful chunks): {metrics['total_latency_sec']:.3f} seconds")
    return df, metrics