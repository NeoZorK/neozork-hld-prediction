# src/data/fetchers/polygon_fetcher.py

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
    # noinspection PyUnresolvedReferences,PackageRequirements
    import polygon
    from polygon.exceptions import BadResponse
    try:
        # noinspection PyUnresolvedReferences
        from polygon.rest.models.aggs import Agg
    except ImportError:
        Agg = object # Dummy type if model not found
    POLYGON_AVAILABLE = True
except ImportError:
    POLYGON_AVAILABLE = False
    # Define dummy classes if polygon is not installed
    class BadResponse(Exception): pass
    # noinspection PyPep8Naming
    class RESTClient: pass
    Agg = object # Dummy type


# Definition of map_polygon_interval function
def map_polygon_interval(tf_input: str) -> tuple[str, int] | None:
    """Maps user-friendly timeframe to Polygon.io timespan and multiplier."""
    tf_input_upper = tf_input.upper()
    mapping = {
        "M1": ("minute", 1), "M5": ("minute", 5), "M15": ("minute", 15), "M30": ("minute", 30),
        "H1": ("hour", 1), "H4": ("hour", 4), "D1": ("day", 1), "D": ("day", 1),
        "W1": ("week", 1), "W": ("week", 1), "WK": ("week", 1), "MN1": ("month", 1),
        "MN": ("month", 1), "MO": ("month", 1)
    }
    # Polygon also supports 'quarter', 'year' directly
    valid_polygon_timespans = ['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']

    if tf_input_upper in mapping:
        return mapping[tf_input_upper]
    elif tf_input.lower() in valid_polygon_timespans:
        # If user enters 'day', 'week' etc., assume multiplier is 1
        return tf_input.lower(), 1
    else:
        logger.print_error(f"Invalid Polygon timeframe input: '{tf_input}'. Use formats like M1, H1, D1 or Polygon timespans.")
        return None


# Definition of resolve_polygon_ticker function
# noinspection PyUnresolvedReferences
def resolve_polygon_ticker(user_ticker: str, client: polygon.RESTClient) -> str | None:
    """
    Uses Polygon API get_ticker_details to find the canonical ticker by trying common prefixes.
    Includes robust check for 404 / "NOT_FOUND" errors and adds delay for rate limiting.
    """
    search_term = user_ticker.upper()
    logger.print_info(f"Resolving Polygon ticker for: '{search_term}'...")

    tickers_to_try = [
        search_term,           # Try exact match first (e.g., AAPL)
        f"C:{search_term}",    # Try Currency prefix
        f"X:{search_term}",    # Try Crypto prefix
        f"I:{search_term}",    # Try Index prefix
    ]
    wait_seconds_on_404 = 15 # Wait N seconds after a 404 to avoid rapid checks

    for potential_ticker in tickers_to_try:
        try:
            logger.print_debug(f"Attempting to get details for ticker: {potential_ticker}")
            # This call will raise BadResponse on 404 or other API errors
            client.get_ticker_details(potential_ticker)
            logger.print_success(f"Resolved '{user_ticker}' to Polygon ticker: '{potential_ticker}'")
            return potential_ticker # Found it!

        except BadResponse as e:
            logger.print_debug(f"Caught BadResponse for {potential_ticker}. Exception: {e}")
            is_not_found = False
            status_code = None
            response = getattr(e, 'response', None)
            if response is not None:
                status_code = getattr(response, 'status_code', None)

            # Check if it's definitely a 404 or contains "NOT_FOUND"
            if status_code == 404:
                is_not_found = True
            else:
                try:
                    error_msg_upper = str(e).upper()
                    if '"STATUS":"NOT_FOUND"' in error_msg_upper or 'TICKER NOT FOUND' in error_msg_upper:
                        logger.print_debug("Detected 'NOT_FOUND' in exception message as fallback.")
                        is_not_found = True
                except Exception as str_err:
                    logger.print_warning(f"Could not analyze BadResponse exception string for 'NOT_FOUND': {str_err}")

            logger.print_debug(f"Extracted status code: {status_code}, Determined Not Found: {is_not_found}")

            if is_not_found:
                logger.print_debug(f"Ticker format '{potential_ticker}' not found. Adding delay before trying next format...")
                logger.print_info(f"Rate limit precaution: waiting for {wait_seconds_on_404} seconds...")
                time.sleep(wait_seconds_on_404)
                continue # Continue to the next iteration of the loop
            else:
                # For any other BadResponse error (e.g., 401, 429, 5xx)
                logger.print_error(f"Non-404 Polygon API Error or unrecognized error format for '{potential_ticker}': {e}")
                if response is not None:
                    url = getattr(response, 'url', 'N/A'); status_code_display = status_code if status_code else 'N/A'
                    logger.print_error(f"  URL: {url}"); logger.print_error(f"  Status Code: {status_code_display}")
                    try: response_details = response.json(); logger.print_error(f"  Details: {response_details}")
                    except Exception: raw_text = getattr(response, 'text', 'N/A'); logger.print_error(f"  Raw Response Text (truncated): {raw_text[:500]}...")
                else: logger.print_error("  (Could not retrieve response details from exception object)")
                logger.print_error("Stopping ticker resolution attempt due to non-404/unknown API error.")
                return None

        # noinspection PyBroadException
        except Exception as e:
            logger.print_error(f"Unexpected error resolving ticker '{potential_ticker}': {type(e).__name__}: {e}")
            logger.print_error(f"Traceback:\n{traceback.format_exc()}")
            return None

    # If loop completes without finding a valid ticker
    logger.print_warning(f"Could not resolve user ticker '{user_ticker}' using common formats (Stock, C:, X:, I:).")
    return None


# Definition of fetch_polygon_data function (with pagination)
# noinspection PyUnresolvedReferences
def fetch_polygon_data(ticker: str, interval: str, start_date: str, end_date: str) -> pd.DataFrame | None:
    """
    Downloads OHLCV data from Polygon.io REST API for a specified date range,
    handling pagination by fetching data in chunks (e.g., monthly for M1, yearly otherwise).
    Attempts to automatically resolve the user-provided ticker to the canonical Polygon ticker.
    Assumes POLYGON_API_KEY is already loaded into environment variables.
    """
    if not POLYGON_AVAILABLE:
        logger.print_error("Polygon API client library ('polygon-api-client') is not installed.")
        return None

    logger.print_info(f"Attempting to fetch Polygon.io data for user ticker: {ticker} | interval: {interval}")

    # --- Get API Key and Initialize Client ---
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        logger.print_error("POLYGON_API_KEY not found in environment variables.")
        return None
    try:
        client = polygon.RESTClient(api_key=api_key)
        logger.print_debug("Polygon client initialized.")
    except Exception as e:
        logger.print_error(f"Failed to initialize Polygon client: {type(e).__name__}: {e}")
        return None

    # --- Resolve Ticker ---
    resolved_ticker = resolve_polygon_ticker(ticker, client)
    if not resolved_ticker:
        return None # Error already logged

    # --- Map Interval ---
    interval_map = map_polygon_interval(interval)
    if interval_map is None: return None # Error already logged
    timespan, multiplier = interval_map

    # --- Convert Dates ---
    try:
        overall_start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
        overall_end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        logger.print_error(f"Invalid date format for start_date ('{start_date}') or end_date ('{end_date}'). Use YYYY-MM-DD.")
        return None

    # --- Pagination Logic ---
    all_aggs_data = []
    current_start_dt = overall_start_dt

    logger.print_info(f"Fetching Polygon data in chunks for '{resolved_ticker}' ({timespan} x{multiplier}) from {overall_start_dt} to {overall_end_dt}...")

    # Determine chunk size based on interval to avoid 50k limit
    if timespan == 'minute':
        chunk_delta = timedelta(days=30) # Approx 1 month chunks for minute data
        chunk_label = "monthly"
    elif timespan == 'hour':
        chunk_delta = timedelta(days=180) # Approx 6 month chunks for hourly data
        chunk_label = "semi-annual"
    else: # day, week, month, quarter, year
        chunk_delta = timedelta(days=365 * 2) # 2-year chunks for daily or larger
        chunk_label = "2-year"

    max_attempts_per_chunk = 3 # Max retries for a single chunk
    request_delay_sec = 0.5 # Small delay between requests to be polite

    while current_start_dt <= overall_end_dt:
        # Calculate end date for the current chunk (inclusive for Polygon 'to')
        current_end_chunk = min(current_start_dt + chunk_delta, overall_end_dt)

        logger.print_info(f"  Fetching {chunk_label} chunk: {current_start_dt} to {current_end_chunk}")

        #chunk_aggs_iter = None
        attempt = 0
        success = False
        while attempt < max_attempts_per_chunk and not success:
            attempt += 1
            try:
                 # Make the API call for the chunk
                 # Use limit=50000 to maximize data per request
                 # noinspection PyTypeChecker
                 chunk_aggs_iter = client.get_aggs(
                     ticker=resolved_ticker,
                     multiplier=multiplier,
                     timespan=timespan,
                     from_=current_start_dt,
                     to=current_end_chunk,
                     adjusted=False, # Keep raw OHLCV
                     limit=50000
                 )

                 # Consume the iterator to get the list of aggregates
                 chunk_data = list(chunk_aggs_iter) # type: list[Agg]

                 if len(chunk_data) == 50000:
                     logger.print_warning(f"    Chunk {current_start_dt}-{current_end_chunk} hit the 50k bar limit. Data might be incomplete if actual bars exceed limit for this chunk delta.")

                 # Format data immediately
                 formatted_chunk_data = [
                     {'DateTime': pd.to_datetime(getattr(agg, 'timestamp', None), unit='ms', errors='coerce'), # Added getattr safety
                      'Open': getattr(agg, 'open', None),
                      'High': getattr(agg, 'high', None),
                      'Low': getattr(agg, 'low', None),
                      'Close': getattr(agg, 'close', None),
                      'Volume': getattr(agg, 'volume', None)}
                     for agg in chunk_data
                 ]
                 all_aggs_data.extend(formatted_chunk_data)
                 logger.print_debug(f"    Fetched {len(formatted_chunk_data)} bars for chunk.")
                 success = True # Mark chunk as successful

            except BadResponse as e:
                logger.print_error(f"    Polygon API Error on chunk {current_start_dt}-{current_end_chunk} (Attempt {attempt}/{max_attempts_per_chunk}): {e}")
                response = getattr(e, 'response', None)
                status_code = None
                if response is not None: status_code = getattr(response, 'status_code', None)

                if status_code == 429: # Rate limit
                    wait_time = 60 # Wait a minute
                    logger.print_warning(f"      Rate limit likely hit (HTTP {status_code}). Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    # Continue to next attempt in the inner loop
                else:
                    logger.print_error(f"      Non-retriable API error (HTTP {status_code}). Logging details and skipping chunk.")
                    if response is not None:
                        try: response_details = response.json(); logger.print_error(f"      Details: {response_details}")
                        except Exception: raw_text = getattr(response, 'text', 'N/A'); logger.print_error(f"      Raw Response Text (truncated): {raw_text[:500]}...")
                    break # Break inner retry loop for this chunk

            # noinspection PyBroadException
            except Exception as e:
                logger.print_error(f"\n--- UNEXPECTED ERROR DURING POLYGON CHUNK FETCH ---")
                logger.print_error("--- TRACEBACK START ---")
                traceback.print_exc()
                logger.print_error("--- TRACEBACK END ---")
                logger.print_error(f"Chunk: {current_start_dt}-{current_end_chunk} (Attempt {attempt}/{max_attempts_per_chunk})")
                logger.print_error(f"Ticker: '{resolved_ticker}', Error: {type(e).__name__}: {e}")
                logger.print_error(f"Traceback:\n{traceback.format_exc()}")
                logger.print_error(f"--- END POLYGON CHUNK ERROR ---")
                logger.print_error(f"    Skipping chunk due to unexpected error.")
                break # Break inner retry loop

            if not success and attempt < max_attempts_per_chunk:
                logger.print_info(f"    Retrying chunk in {5 * attempt} seconds...")
                time.sleep(5 * attempt) # Simple exponential backoff

        # --- After attempting a chunk ---
        if not success:
            logger.print_error(f"Failed to fetch chunk {current_start_dt}-{current_end_chunk} after {max_attempts_per_chunk} attempts. Stopping data retrieval.")
            return None # Stop fetching if a chunk fails repeatedly

        # Move to the next chunk start date (day after the current chunk ended)
        current_start_dt = current_end_chunk + timedelta(days=1)
        time.sleep(request_delay_sec) # Be polite between chunk requests


    # --- Combine and Process All Fetched Data ---
    if not all_aggs_data:
        logger.print_warning(f"No Polygon data returned for '{resolved_ticker}' in the specified range {overall_start_dt} to {overall_end_dt} after chunking.")
        return None

    logger.print_info(f"Combining {len(all_aggs_data)} bars from all chunks...")
    df = pd.DataFrame(all_aggs_data)

    # --- Post-processing ---
    df.dropna(subset=['DateTime'], inplace=True) # Drop rows where timestamp conversion failed
    if df.empty:
        logger.print_warning(f"Polygon data became empty after handling potential DateTime errors.")
        return None
    df.set_index('DateTime', inplace=True)

    # Remove duplicates (can happen if chunks overlap slightly or API returns dupes)
    initial_rows = len(df)
    df = df[~df.index.duplicated(keep='first')]
    rows_dropped = initial_rows - len(df)
    if rows_dropped > 0:
        logger.print_debug(f"Removed {rows_dropped} duplicate rows based on DateTime index.")

    # Sort by index to ensure chronological order
    df.sort_index(inplace=True)

    # Check required columns
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        logger.print_error(f"Polygon data is missing required columns after processing: {missing_cols}. Columns found: {list(df.columns)}")
        return None

    # Convert columns to numeric, coercing errors
    for col in required_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')


    # Drop rows with NaN in essential OHLCV columns
    df.dropna(subset=required_cols, inplace=True)
    if df.empty:
        logger.print_warning(f"Polygon data for '{resolved_ticker}' became empty after removing NaN rows.")
        return None

    logger.print_success(f"Successfully fetched and processed {len(df)} rows from Polygon.io for '{resolved_ticker}' using chunking.")
    return df