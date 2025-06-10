# src/data/fetchers/polygon_fetcher.py

"""
Contains functions related to fetching data from Polygon.io API.
Includes interval mapping, ticker resolution, and the main data download function with pagination.
"""

import pandas as pd
import os
import time # Import time
import traceback
from datetime import datetime, timedelta
from ...common import logger # Relative import
from tqdm import tqdm # Import tqdm
# Need to import MaxRetryError
from urllib3.exceptions import MaxRetryError

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
    valid_polygon_timespans = ['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']

    if tf_input_upper in mapping:
        return mapping[tf_input_upper]
    elif tf_input.lower() in valid_polygon_timespans:
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

    for potential_ticker in tickers_to_try:
        try:
            logger.print_debug(f"Attempting to get details for ticker: {potential_ticker}")
            # Increase delay significantly BEFORE the call
            logger.print_debug("Waiting 1.1 seconds before ticker details request to avoid rate limit...")
            time.sleep(1.1) # Increased delay to > 1 second
            client.get_ticker_details(potential_ticker)
            logger.print_success(f"Resolved '{user_ticker}' to Polygon ticker: '{potential_ticker}'")
            return potential_ticker # Found it!

        except MaxRetryError as e: # Catch the specific MaxRetryError
            logger.print_error(f"Rate limit error (Max Retries Exceeded) resolving ticker '{potential_ticker}': {e}")
            logger.print_error("Likely hit Polygon API rate limit (e.g., 5 requests/minute). Stopping resolution attempt.")
            return None # Stop trying if rate limit hit hard

        except BadResponse as e:
            logger.print_debug(f"Caught BadResponse for {potential_ticker}. Exception: {e}")
            is_not_found = False
            status_code = None
            response = getattr(e, 'response', None)
            if response is not None:
                status_code = getattr(response, 'status_code', None)

            if status_code == 404:
                is_not_found = True
            else: # Check message as fallback
                try:
                    # Handle potential JSONDecodeError if response text isn't valid JSON
                    if response is not None and response.text:
                        error_msg_upper = str(response.text).upper() # Use response.text if available
                    else:
                        error_msg_upper = str(e).upper() # Fallback to exception string

                    if '"STATUS":"NOT_FOUND"' in error_msg_upper or 'TICKER NOT FOUND' in error_msg_upper:
                        logger.print_debug("Detected 'NOT_FOUND' in exception message/text as fallback.")
                        is_not_found = True
                except Exception as str_err:
                    logger.print_warning(f"Could not analyze BadResponse exception/text for 'NOT_FOUND': {str_err}")


            logger.print_debug(f"Extracted status code: {status_code}, Determined Not Found: {is_not_found}")

            if is_not_found:
                logger.print_debug(f"Ticker format '{potential_ticker}' not found. Trying next format...")
                continue # Continue to the next iteration of the loop
            else:
                # For any other BadResponse error (e.g., 401, 429, 5xx)
                logger.print_error(f"Non-404 Polygon API Error or unrecognized error format for '{potential_ticker}': Status={status_code}, Error={e}")
                # Log details if possible
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


# Definition of fetch_polygon_data function (with pagination and tqdm)
# noinspection PyUnresolvedReferences
# MODIFIED: Added tqdm progress bar
def fetch_polygon_data(ticker: str, interval: str, start_date: str, end_date: str) -> tuple[pd.DataFrame | None, dict]:
    """
    Downloads OHLCV data from Polygon.io REST API for a specified date range,
    handling pagination by fetching data in chunks and showing progress with tqdm.
    Attempts to automatically resolve the user-provided ticker.
    Assumes POLYGON_API_KEY is already loaded.
    Returns a tuple: (DataFrame or None, metrics dictionary).
    """
    if not POLYGON_AVAILABLE:
        logger.print_error("Polygon API client library ('polygon-api-client') is not installed.")
        return None, {"error_message": "polygon-api-client not installed"}

    logger.print_info(f"Attempting to fetch Polygon.io data for user ticker: {ticker} | interval: {interval}")
    # Initialize metrics
    metrics = {"total_latency_sec": 0.0, "api_calls": 0, "successful_chunks": 0, "rows_fetched": 0}

    # --- Get API Key and Initialize Client ---
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        logger.print_error("POLYGON_API_KEY not found in environment variables.")
        return None, {"error_message": "POLYGON_API_KEY not found"}
    try:
        client = polygon.RESTClient(api_key=api_key)
        logger.print_debug("Polygon client initialized.")
    except Exception as e:
        logger.print_error(f"Failed to initialize Polygon client: {type(e).__name__}: {e}")
        return None, {"error_message": f"Client init failed: {e}"}

    # --- Resolve Ticker ---
    resolve_start_time = time.perf_counter()
    resolved_ticker = resolve_polygon_ticker(ticker, client)
    resolve_end_time = time.perf_counter()
    # Add resolve latency to metrics if desired
    metrics["resolve_latency_sec"] = resolve_end_time - resolve_start_time
    logger.print_debug(f"Ticker resolution took: {metrics['resolve_latency_sec']:.3f} seconds")
    if not resolved_ticker:
        # Include ticker in the error message for clarity
        return None, {**metrics, "error_message": f"Could not resolve ticker '{ticker}'"}

    # --- Map Interval ---
    interval_map = map_polygon_interval(interval)
    if interval_map is None: return None, {**metrics, "error_message": f"Invalid interval: {interval}"}
    timespan, multiplier = interval_map

    # --- Convert Dates ---
    try:
        overall_start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
        overall_end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        error_msg = f"Invalid date format for start_date ('{start_date}') or end_date ('{end_date}'). Use<x_bin_880>-MM-DD."
        logger.print_error(error_msg)
        return None, {**metrics, "error_message": error_msg}

    # --- Pagination Logic ---
    all_aggs_data = []
    current_start_dt = overall_start_dt

    logger.print_info(f"Fetching Polygon data in chunks for '{resolved_ticker}' ({timespan} x{multiplier}) from {overall_start_dt} to {overall_end_dt}...")

    # Chunk size determination (remains the same)
    if timespan == 'minute': chunk_delta = timedelta(days=30); chunk_label = "monthly"
    elif timespan == 'hour': chunk_delta = timedelta(days=180); chunk_label = "semi-annual"
    else: chunk_delta = timedelta(days=365 * 2); chunk_label = "2-year" # Includes day, week, month etc.

    max_attempts_per_chunk = 3
    request_delay_sec = 0.21 # Be slightly above 5 req/sec limit (1/5 = 0.2)

    # --- Initialize tqdm ---
    total_days = max(1, (overall_end_dt - overall_start_dt).days + 1)
    pbar = tqdm(total=total_days, unit='day', desc=f"Fetching Polygon {resolved_ticker}", leave=True, ascii=True, unit_scale=False)
    # Track the last date successfully processed for accurate progress update
    last_processed_dt = overall_start_dt - timedelta(days=1) # Initialize to day before start

    try: # Wrap the main loop in try...finally for pbar.close()
        while current_start_dt <= overall_end_dt:
            current_end_chunk = min(current_start_dt + chunk_delta, overall_end_dt)
            # Update pbar postfix before fetching the chunk
            pbar.set_postfix_str(f"Chunk: {current_start_dt} to {current_end_chunk}", refresh=True)

            attempt = 0
            success = False
            chunk_data = [] # Initialize chunk_data for the loop

            while attempt < max_attempts_per_chunk and not success:
                attempt += 1
                metrics["api_calls"] += 1 # Increment API calls on each attempt
                chunk_latency = 0 # Track latency for this specific attempt
                try:
                    # Make the API call for the chunk
                    start_chunk_time = time.perf_counter()
                    # Use limit=50000 to maximize data per request
                    # noinspection PyTypeChecker
                    chunk_aggs_iter = client.get_aggs(
                        ticker=resolved_ticker,
                        multiplier=multiplier,
                        timespan=timespan,
                        from_=current_start_dt,
                        to=current_end_chunk,
                        adjusted=True, # Keep adjusted=True default
                        limit=50000
                    )
                    # Consume the iterator to get the list of aggregates
                    chunk_data = list(chunk_aggs_iter) # type: list[Agg]
                    end_chunk_time = time.perf_counter()
                    chunk_latency = end_chunk_time - start_chunk_time
                    metrics["total_latency_sec"] += chunk_latency # Add successful fetch latency

                    # Check if 50k limit was hit
                    if len(chunk_data) == 50000:
                        # Use pbar.write for warnings inside the loop
                        pbar.write(f"    Warning: Chunk {current_start_dt}-{current_end_chunk} hit the 50k bar limit. Data might be incomplete if actual bars exceed limit for this chunk delta.")

                    # Format data immediately
                    formatted_chunk_data = [
                        {'DateTime': pd.to_datetime(getattr(agg, 'timestamp', None), unit='ms', errors='coerce'),
                         'Open': getattr(agg, 'open', None), 'High': getattr(agg, 'high', None),
                         'Low': getattr(agg, 'low', None), 'Close': getattr(agg, 'close', None),
                         'Volume': getattr(agg, 'volume', None)}
                        for agg in chunk_data
                    ]
                    all_aggs_data.extend(formatted_chunk_data)
                    metrics["rows_fetched"] += len(formatted_chunk_data) # Update rows fetched count
                    success = True # Mark chunk as successful
                    metrics["successful_chunks"] += 1 # Increment successful chunks only on success

                except BadResponse as e:
                    # Log API errors using pbar.write
                    pbar.write(f"    API Error chunk {current_start_dt}-{current_end_chunk} (Attempt {attempt}/{max_attempts_per_chunk}): {e}")
                    response = getattr(e, 'response', None)
                    status_code = None
                    wait_time = 0
                    if response is not None: status_code = getattr(response, 'status_code', None)

                    # NEW: Check for NOT_AUTHORIZED specifically
                    is_not_authorized = False
                    try:
                        if response is not None and response.text:
                            error_text = response.text
                            if '"status":"NOT_AUTHORIZED"' in error_text or "plan doesn't include this data" in error_text:
                                is_not_authorized = True
                    except Exception:
                        pass # Ignore errors checking the text

                    if is_not_authorized:
                         pbar.write(f"      Authorization Error (HTTP {status_code}): Your plan likely doesn't support '{timespan}' timeframe. Skipping chunk.")
                         break # Break inner retry loop, skip this chunk

                    elif status_code == 429: # Rate limit
                        wait_time = 60 # Wait a minute
                        pbar.write(f"      Rate limit likely hit (HTTP {status_code}). Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue # Continue to next attempt in the inner loop
                    else:
                        # Use pbar.write for non-retriable errors
                        pbar.write(f"      Non-retriable API error (HTTP {status_code}). Logging details and skipping chunk.")
                        if response is not None:
                            try: response_details = response.json(); pbar.write(f"      Details: {response_details}")
                            except Exception: raw_text = getattr(response, 'text', 'N/A'); pbar.write(f"      Raw Response Text (truncated): {raw_text[:500]}...")
                        break # Break inner retry loop for this chunk

                # noinspection PyBroadException
                except Exception as e:
                    # Log unexpected errors more verbosely using pbar.write
                    pbar.write(f"\n--- UNEXPECTED ERROR DURING POLYGON CHUNK FETCH ---")
                    pbar.write(f"Chunk: {current_start_dt}-{current_end_chunk} (Attempt {attempt}/{max_attempts_per_chunk})")
                    pbar.write(f"Ticker: '{resolved_ticker}', Error: {type(e).__name__}: {e}")
                    pbar.write("--- TRACEBACK START ---")
                    # Use pbar.write for traceback too (might be long)
                    pbar.write(traceback.format_exc())
                    pbar.write("--- TRACEBACK END ---")
                    pbar.write(f"    Skipping chunk due to unexpected error.")
                    break # Break inner retry loop

                # Backoff only if an error occurred (and not authorization error) and more retries are left
                if not success and attempt < max_attempts_per_chunk:
                    backoff_time = 5 * attempt
                    # Use pbar.write for retry info
                    pbar.write(f"    Retrying chunk in {backoff_time} seconds...")
                    time.sleep(backoff_time) # Simple exponential backoff

            # --- After attempting a chunk ---
            if not success:
                # Check if the loop was broken due to authorization error, don't return error if so
                if 'is_not_authorized' in locals() and is_not_authorized:
                    pbar.write(f"    Skipping chunk {current_start_dt}-{current_end_chunk} due to authorization error.")
                else:
                    # If failed for other reasons after retries
                    error_msg = f"Failed to fetch chunk {current_start_dt}-{current_end_chunk} after {max_attempts_per_chunk} attempts. Stopping data retrieval."
                    # Use pbar.write for the final error message before returning
                    pbar.write(f"Error: {error_msg}")
                    return None, {**metrics, "error_message": error_msg} # Stop fetching if a chunk fails repeatedly

            # Update progress bar based on the successfully processed chunk end date only if success
            if success:
                days_processed = (current_end_chunk - last_processed_dt).days
                if days_processed > 0:
                    pbar.update(days_processed)
                    last_processed_dt = current_end_chunk

            # Move to the next chunk start date regardless of success/skip
            current_start_dt = current_end_chunk + timedelta(days=1)
            if current_start_dt <= overall_end_dt: # Only sleep if there are more chunks
                time.sleep(request_delay_sec) # Be polite between chunk requests

    finally:
        # Clear postfix and ensure the bar reaches 100% on completion or error
        pbar.set_postfix_str("")
        remaining_days = total_days - pbar.n
        if remaining_days > 0:
            pbar.update(remaining_days)
        pbar.close() # Close the progress bar


    # --- Combine and Process All Fetched Data ---
    if not all_aggs_data:
        logger.print_warning(f"No Polygon data returned for '{resolved_ticker}' in the specified range {overall_start_dt} to {overall_end_dt} after chunking.")
        # Return None df but keep metrics
        final_error_message = metrics.get("error_message") # Keep previous error if fetch failed
        if not final_error_message: final_error_message = "No data found for the specified criteria."
        return None, {**metrics, "error_message": final_error_message}


    logger.print_info(f"Combining {len(all_aggs_data)} bars from all chunks...")
    df = pd.DataFrame(all_aggs_data)

    # --- Post-processing ---
    df.dropna(subset=['DateTime'], inplace=True)
    if df.empty:
        logger.print_warning(f"Polygon data became empty after handling potential DateTime errors.")
        return None, metrics # Return None df and metrics
    df.set_index('DateTime', inplace=True)

    initial_rows = len(df)
    df = df[~df.index.duplicated(keep='first')]
    rows_dropped = initial_rows - len(df)
    if rows_dropped > 0:
        logger.print_debug(f"Removed {rows_dropped} duplicate rows based on DateTime index.")

    df.sort_index(inplace=True)

    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        logger.print_error(f"Polygon data is missing required columns after processing: {missing_cols}. Columns found: {list(df.columns)}")
        return None, metrics # Return None df and metrics

    # Convert columns to numeric, coercing errors AFTER combining all chunks
    for col in required_cols:
         if col in df.columns: # Check column exists before conversion
              df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(subset=required_cols, inplace=True)
    if df.empty:
        logger.print_warning(f"Polygon data for '{resolved_ticker}' became empty after removing NaN rows.")
        return None, metrics # Return None df and metrics

    logger.print_success(f"Successfully fetched and processed {len(df)} rows from Polygon.io for '{resolved_ticker}'.")
    logger.print_debug(f"Total Polygon API call latency (sum of successful chunks): {metrics['total_latency_sec']:.3f} seconds")
    # Return DataFrame and metrics
    return df, metrics