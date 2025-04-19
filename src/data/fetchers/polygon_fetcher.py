# src/data/fetchers/polygon_fetcher.py # Added Debug Logging

"""
Contains functions related to fetching data from Polygon.io API.
Includes interval mapping, ticker resolution, and the main data download function with pagination.
"""

import pandas as pd
import os
import time
import traceback
from datetime import datetime, timedelta
from ...common import logger # Relative import

# Polygon specific imports and checks
try:
    import polygon
    from polygon.exceptions import BadResponse
    try: from polygon.rest.models.aggs import Agg
    except ImportError: Agg = object
    POLYGON_AVAILABLE = True
except ImportError:
    POLYGON_AVAILABLE = False
    class BadResponse(Exception): pass
    class RESTClient: pass
    Agg = object


# map_polygon_interval (no changes needed)
def map_polygon_interval(tf_input: str) -> tuple[str, int] | None:
    tf_input_upper = tf_input.upper()
    mapping = { "M1": ("minute", 1), "M5": ("minute", 5), "M15": ("minute", 15), "M30": ("minute", 30), "H1": ("hour", 1), "H4": ("hour", 4), "D1": ("day", 1), "D": ("day", 1), "W1": ("week", 1), "W": ("week", 1), "WK": ("week", 1), "MN1": ("month", 1), "MN": ("month", 1), "MO": ("month", 1) }
    valid_polygon_timespans = ['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']
    if tf_input_upper in mapping: return mapping[tf_input_upper]
    elif tf_input.lower() in valid_polygon_timespans: return tf_input.lower(), 1
    else: logger.print_error(f"Invalid Polygon timeframe input: '{tf_input}'. Use formats like M1, H1, D1 or Polygon timespans."); return None


# resolve_polygon_ticker (no changes needed from previous version)
def resolve_polygon_ticker(user_ticker: str, client: polygon.RESTClient) -> str | None:
    search_term = user_ticker.upper()
    logger.print_info(f"Resolving Polygon ticker for: '{search_term}'...")
    tickers_to_try = [ search_term, f"C:{search_term}", f"X:{search_term}", f"I:{search_term}" ]
    wait_seconds_on_404 = 15
    for potential_ticker in tickers_to_try:
        try:
            logger.print_debug(f"Attempting to get details for ticker: {potential_ticker}")
            client.get_ticker_details(potential_ticker)
            logger.print_success(f"Resolved '{user_ticker}' to Polygon ticker: '{potential_ticker}'")
            return potential_ticker
        except BadResponse as e:
            logger.print_debug(f"Caught BadResponse for {potential_ticker}. Exception: {e}")
            is_not_found = False; status_code = None
            response = getattr(e, 'response', None)
            if response is not None: status_code = getattr(response, 'status_code', None)
            if status_code == 404: is_not_found = True
            else:
                try:
                    error_msg_upper = str(e).upper()
                    if '"STATUS":"NOT_FOUND"' in error_msg_upper or 'TICKER NOT FOUND' in error_msg_upper: is_not_found = True
                except Exception as str_err: logger.print_warning(f"Could not analyze BadResponse exception string for 'NOT_FOUND': {str_err}")
            logger.print_debug(f"Extracted status code: {status_code}, Determined Not Found: {is_not_found}")
            if is_not_found:
                logger.print_debug(f"Ticker format '{potential_ticker}' not found. Adding delay...")
                time.sleep(wait_seconds_on_404); continue
            else:
                logger.print_error(f"Non-404 Polygon API Error for '{potential_ticker}': {e}")
                if response is not None:
                    url = getattr(response, 'url', 'N/A'); status_code_display = status_code if status_code else 'N/A'
                    logger.print_error(f"  URL: {url}"); logger.print_error(f"  Status Code: {status_code_display}")
                    try: response_details = response.json(); logger.print_error(f"  Details: {response_details}")
                    except Exception: raw_text = getattr(response, 'text', 'N/A'); logger.print_error(f"  Raw Response Text (truncated): {raw_text[:500]}...")
                else: logger.print_error("  (Could not retrieve response details from exception object)")
                logger.print_error("Stopping ticker resolution attempt.")
                return None
        except Exception as e:
            logger.print_error(f"Unexpected error resolving ticker '{potential_ticker}': {type(e).__name__}: {e}")
            logger.print_error(f"Traceback:\n{traceback.format_exc()}")
            return None
    logger.print_warning(f"Could not resolve user ticker '{user_ticker}' using common formats."); return None


# fetch_polygon_data (Added debug logging in pagination loop)
def fetch_polygon_data(ticker: str, interval: str, start_date: str, end_date: str) -> pd.DataFrame | None:
    if not POLYGON_AVAILABLE: logger.print_error("'polygon-api-client' not installed."); return None
    logger.print_info(f"Attempting to fetch Polygon.io data for user ticker: {ticker} | interval: {interval}")
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key: logger.print_error("POLYGON_API_KEY not found in environment variables."); return None
    try: client = polygon.RESTClient(api_key=api_key); logger.print_debug("Polygon client initialized.")
    except Exception as e: logger.print_error(f"Failed to initialize Polygon client: {type(e).__name__}: {e}"); return None
    resolved_ticker = resolve_polygon_ticker(ticker, client)
    if not resolved_ticker: return None
    interval_map = map_polygon_interval(interval)
    if interval_map is None: return None
    timespan, multiplier = interval_map
    try:
        overall_start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
        overall_end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError: logger.print_error(f"Invalid date format. Use YYYY-MM-DD."); return None

    all_aggs_data = []; current_start_dt = overall_start_dt
    logger.print_info(f"Fetching Polygon data in chunks for '{resolved_ticker}' ({timespan} x{multiplier}) from {overall_start_dt} to {overall_end_dt}...")
    if timespan == 'minute': chunk_delta = timedelta(days=30); chunk_label = "monthly"
    elif timespan == 'hour': chunk_delta = timedelta(days=180); chunk_label = "semi-annual"
    else: chunk_delta = timedelta(days=365 * 2); chunk_label = "2-year"
    max_attempts_per_chunk = 3; request_delay_sec = 0.5

    loop_counter = 0 # DEBUG
    while current_start_dt <= overall_end_dt:
        loop_counter += 1 # DEBUG
        current_end_chunk = min(current_start_dt + chunk_delta, overall_end_dt)
        logger.print_info(f"  Fetching {chunk_label} chunk #{loop_counter}: {current_start_dt} to {current_end_chunk}") # DEBUG Added loop counter

        chunk_aggs_iter = None; attempt = 0; success = False
        while attempt < max_attempts_per_chunk and not success:
            attempt += 1
            try:
                 chunk_aggs_iter = client.get_aggs( ticker=resolved_ticker, multiplier=multiplier, timespan=timespan, from_=current_start_dt, to=current_end_chunk, adjusted=False, limit=50000 )
                 chunk_data = list(chunk_aggs_iter)
                 if len(chunk_data) == 50000: logger.print_warning(f"    Chunk {current_start_dt}-{current_end_chunk} hit the 50k bar limit.")
                 formatted_chunk_data = [ {'DateTime': pd.to_datetime(getattr(agg, 'timestamp', None), unit='ms', errors='coerce'), 'Open': getattr(agg, 'open', None), 'High': getattr(agg, 'high', None), 'Low': getattr(agg, 'low', None), 'Close': getattr(agg, 'close', None), 'Volume': getattr(agg, 'volume', None)} for agg in chunk_data ]
                 all_aggs_data.extend(formatted_chunk_data)
                 logger.print_debug(f"    Fetched {len(formatted_chunk_data)} bars for chunk.")
                 success = True
            except BadResponse as e:
                logger.print_error(f"    Polygon API Error on chunk (Attempt {attempt}/{max_attempts_per_chunk}): {e}")
                response = getattr(e, 'response', None); status_code = None
                if response is not None: status_code = getattr(response, 'status_code', None)
                if status_code == 429: wait_time = 60; logger.print_warning(f"      Rate limit hit. Waiting {wait_time}s..."); time.sleep(wait_time)
                else: logger.print_error(f"      Non-retriable API error (HTTP {status_code}). Skipping chunk."); break
            except Exception as e: logger.print_error(f"    Unexpected error during chunk fetch: {type(e).__name__}: {e}"); traceback.print_exc(); break
            if not success and attempt < max_attempts_per_chunk: logger.print_info(f"    Retrying chunk in {5 * attempt} seconds..."); time.sleep(5 * attempt)

        if not success: logger.print_error(f"Failed to fetch chunk {current_start_dt}-{current_end_chunk} after {max_attempts_per_chunk} attempts."); return None
        current_start_dt = current_end_chunk + timedelta(days=1)
        logger.print_debug(f"    Next chunk will start from: {current_start_dt}") # DEBUG
        if current_start_dt > overall_end_dt: logger.print_debug("    End date reached.") # DEBUG
        time.sleep(request_delay_sec)

    if not all_aggs_data: logger.print_warning(f"No Polygon data returned for '{resolved_ticker}' in range after chunking."); return None
    logger.print_info(f"Combining {len(all_aggs_data)} bars from all chunks...")
    df = pd.DataFrame(all_aggs_data)
    df.dropna(subset=['DateTime'], inplace=True)
    if df.empty: logger.print_warning(f"Data became empty after handling DateTime errors."); return None
    df.set_index('DateTime', inplace=True)
    initial_rows = len(df)
    df = df[~df.index.duplicated(keep='first')]
    rows_dropped = initial_rows - len(df)
    if rows_dropped > 0: logger.print_debug(f"Removed {rows_dropped} duplicate rows based on DateTime index.")
    df.sort_index(inplace=True)
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols: logger.print_error(f"Data missing required columns after processing: {missing_cols}. Found: {list(df.columns)}"); return None
    for col in required_cols: df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=required_cols, inplace=True)
    if df.empty: logger.print_warning(f"Data for '{resolved_ticker}' became empty after removing NaN rows."); return None
    logger.print_success(f"Successfully fetched and processed {len(df)} rows from Polygon.io for '{resolved_ticker}' using chunking.")
    return df