# src/data/data_acquisition.py

"""
Handles the overall data acquisition process by dispatching to specific fetchers based on mode.
Checks for existing single Parquet cache file per instrument and fetches only missing data.
All comments are in English.
"""
import os
import traceback
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone
# from pandas.tseries.frequencies import to_offset

# Use relative imports for fetchers within the same package
from .fetchers import (
    fetch_csv_data, fetch_yfinance_data, fetch_polygon_data,
    fetch_binance_data, get_demo_data
)
# Use relative import for logger
from ..common import logger

# Helper function to get interval delta
def _get_interval_delta(interval_str: str) -> pd.Timedelta | None:
    """Converts interval string (e.g., 'H1', 'D1', 'M1') to pandas Timedelta."""
    simple_map = {
        'M1': '1min', 'M5': '5min', 'M15': '15min', 'M30': '30min',
        'H1': '1h', 'H4': '4h', 'D1': '1d', 'D': '1d',
        'W': '7d', 'W1': '7d',
        'MN': '30d', 'MN1': '30d' # Approximation for month delta check
    }
    pd_freq = simple_map.get(interval_str.upper(), interval_str) # Use upper for mapping keys
    try:
        delta = pd.Timedelta(pd_freq)
        # Return None if delta is zero or negative (invalid interval for delta logic)
        return delta if delta.total_seconds() > 0 else None
    except ValueError:
        logger.print_warning(f"Could not parse interval '{interval_str}' to Timedelta. Cache delta logic may be affected.")
        return None # Return None if parsing fails

# Helper function for Parquet filename (Mode, Ticker, Interval based)
def _generate_instrument_parquet_filename(args) -> Path | None:
    """Generates the expected instrument-specific parquet filename (no dates)."""
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode # Normalize mode
    if effective_mode not in ['yfinance', 'polygon', 'binance'] or not args.ticker:
        return None

    parquet_dir = Path("data/raw_parquet")
    try:
        # Sanitize ticker: replace common problematic characters
        ticker_label = str(args.ticker).replace('/', '_').replace('-', '_').replace('=','_').replace(':','_')
        interval_label = str(args.interval)
        filename = f"{effective_mode}_{ticker_label}_{interval_label}.parquet"
        filepath = parquet_dir / filename
        return filepath
    except Exception as e:
        logger.print_warning(f"Error generating instrument parquet filename: {e}")
        return None

# Definition of acquire_data function
def acquire_data(args) -> dict:
    """
    Acquires OHLCV data based on the specified mode and arguments.
    Uses a single Parquet file per instrument for caching, fetching only missing data.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        dict: A dictionary containing the DataFrame ('ohlcv_df') and acquisition metrics.
    """
    dotenv_path = '.env'; load_dotenv(dotenv_path=dotenv_path)
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode # Normalize mode

    data_info = {
        "ohlcv_df": None, "ticker": args.ticker, "interval": args.interval,
        "data_source_label": "N/A", "effective_mode": effective_mode, # Use normalized mode
        "yf_ticker": None, "yf_interval": None, "current_period": args.period,
        "current_start": args.start, "current_end": args.end,
        "file_size_bytes": None, "api_latency_sec": 0.0,
        "api_calls": 0, "successful_chunks": 0, "rows_fetched": 0,
        "error_message": None, "data_metrics": {}, "parquet_cache_used": False,
        "parquet_cache_file": None
    }
    logger.print_info(f"--- Step 1: Acquiring Data (Mode: {effective_mode.capitalize()}) ---")

    df = None; metrics = {}; cached_df = None; cache_filepath = None
    fetch_ranges = []; req_start_dt = None; req_end_dt_inclusive = None # Initialize
    combined_metrics = {} # *** FIX: Initialize combined_metrics here ***

    # --- Handle non-cacheable modes first ---
    if effective_mode == 'demo':
        data_info["data_source_label"] = "Demo Data"; df = get_demo_data(); metrics = {}
        data_info["ohlcv_df"] = df; return data_info
    elif effective_mode == 'csv':
        # Validation now happens in cli.py
        data_info["data_source_label"] = args.csv_file
        df, metrics = fetch_csv_data(filepath=args.csv_file)
        data_info["ohlcv_df"] = df
        combined_metrics = metrics or {} # Assign to combined_metrics
        if isinstance(metrics, dict): data_info["data_metrics"].update(metrics) # Update metrics
        if "file_size_bytes" in data_info["data_metrics"]: data_info["file_size_bytes"] = data_info["data_metrics"]["file_size_bytes"]
        # Need to populate other fields from combined_metrics at the end
        # return data_info # Don't return early, let final update happen

    # --- Logic for Cacheable API Modes ---
    elif effective_mode in ['yfinance', 'polygon', 'binance']:
        try:
            # --- Date Parsing (moved from cli, handles period vs start/end) ---
            is_period_request = effective_mode == 'yfinance' and args.period
            if not is_period_request: # Using start/end dates
                 try:
                      req_start_dt = pd.to_datetime(args.start, errors='raise').tz_localize(None)
                      # Fetch up to the *beginning* of the day *after* end_date to be inclusive for daily/longer intervals
                      req_end_dt_inclusive = pd.to_datetime(args.end, errors='raise').tz_localize(None) + timedelta(days=1) - timedelta(milliseconds=1)
                      if req_start_dt >= req_end_dt_inclusive: raise ValueError("Start date must be before end date.")
                 except Exception as date_err:
                      raise ValueError(f"Invalid start/end date format or range: {date_err}")
            else: # Using yfinance period
                 req_start_dt, req_end_dt_inclusive = None, None # Mark as period request

            # --- Check Cache ---
            cache_filepath = _generate_instrument_parquet_filename(args)
            data_info["parquet_cache_file"] = str(cache_filepath) if cache_filepath else None
            cache_load_success = False

            if cache_filepath and cache_filepath.exists() and not is_period_request:
                logger.print_info(f"Found existing cache file: {cache_filepath}")
                try:
                    cached_df = pd.read_parquet(cache_filepath)
                    if not isinstance(cached_df.index, pd.DatetimeIndex) or cached_df.empty:
                        logger.print_warning("Cache file invalid (no DatetimeIndex or empty). Ignoring cache.")
                        cached_df = None
                    else:
                        cached_df.index = cached_df.index.tz_localize(None) # Ensure naive index
                        cache_start_dt = cached_df.index.min()
                        cache_end_dt = cached_df.index.max()
                        logger.print_success(f"Loaded {len(cached_df)} rows from cache ({cache_start_dt} to {cache_end_dt}).")
                        data_info["parquet_cache_used"] = True
                        cache_load_success = True
                        try: data_info["file_size_bytes"] = cache_filepath.stat().st_size
                        except Exception: pass
                except Exception as e: logger.print_warning(f"Failed to load cache file {cache_filepath}: {e}")

            # --- Determine Fetch Ranges ---
            if not is_period_request: # Only determine fetch ranges if start/end provided
                interval_delta = _get_interval_delta(args.interval)
                if cache_load_success and interval_delta:
                    # Fetch data before cache if needed
                    if req_start_dt < cache_start_dt:
                        fetch_before_end = cache_start_dt - interval_delta # Fetch up to the bar *before* cache starts
                        if fetch_before_end >= req_start_dt:
                            fetch_ranges.append((req_start_dt, fetch_before_end))
                    # Fetch data after cache if needed
                    if req_end_dt_inclusive > cache_end_dt:
                        fetch_after_start = cache_end_dt + interval_delta # Fetch from the bar *after* cache ends
                        if fetch_after_start <= req_end_dt_inclusive:
                             fetch_ranges.append((fetch_after_start, req_end_dt_inclusive))

                    if not fetch_ranges: logger.print_info("Requested range is fully covered by cache.")
                    else: logger.print_info(f"Found {len(fetch_ranges)} missing range(s) to fetch.")

                elif not cache_load_success: # No cache, fetch full range
                    fetch_ranges.append((req_start_dt, req_end_dt_inclusive))
                    logger.print_info(f"No cache found/usable. Fetching full range: {args.start} to {args.end}")
                elif not interval_delta: # Cache loaded but couldn't get delta
                     logger.print_warning("Could not determine interval delta, cannot fetch partial data. Using cache only.")
                     # Proceed with only cached_df

            # --- Fetch Missing Data ---
            new_data_list = []; fetch_failed = False
            if fetch_ranges:
                data_info["data_source_label"] = args.ticker # Set label to ticker since we fetch from API
                for fetch_start, fetch_end in fetch_ranges:
                    fetch_start_str = fetch_start.strftime('%Y-%m-%d')
                    # For fetch_end, we need the end date string for the API call
                    # Add back the millisecond we subtracted earlier, then format
                    fetch_end_inclusive = fetch_end + timedelta(milliseconds=1)
                    fetch_end_str = fetch_end_inclusive.strftime('%Y-%m-%d')

                    logger.print_info(f"Fetching range: {fetch_start_str} to {fetch_end_str} from {effective_mode}...")
                    new_df_part = None; metrics_part = {}
                    try:
                        if effective_mode == 'yfinance':
                            # Pass period=None when using start/end
                            new_df_part, metrics_part = fetch_yfinance_data(ticker=args.ticker, interval=args.interval, start_date=fetch_start_str, end_date=fetch_end_str, period=None)
                        elif effective_mode == 'polygon':
                            new_df_part, metrics_part = fetch_polygon_data(ticker=args.ticker, interval=args.interval, start_date=fetch_start_str, end_date=fetch_end_str)
                        elif effective_mode == 'binance':
                            new_df_part, metrics_part = fetch_binance_data(ticker=args.ticker, interval=args.interval, start_date=fetch_start_str, end_date=fetch_end_str)

                        if new_df_part is not None and not new_df_part.empty:
                            if isinstance(new_df_part.index, pd.DatetimeIndex): new_df_part.index = new_df_part.index.tz_localize(None)
                            new_data_list.append(new_df_part); logger.print_success(f"Fetched {len(new_df_part)} new rows.")
                        else: logger.print_warning(f"No data returned for range {fetch_start_str} to {fetch_end_str}.")
                        # Accumulate metrics
                        if isinstance(metrics_part, dict):
                            for key, value in metrics_part.items():
                                if key == "error_message" and value and "error_message" not in combined_metrics: combined_metrics["error_message"] = value # Store first error
                                elif isinstance(value, (int, float)): combined_metrics[key] = combined_metrics.get(key, 0) + value
                                # Optionally accumulate other metrics if needed
                    except Exception as e:
                        logger.print_error(f"Failed to fetch range {fetch_start_str} to {fetch_end_str}: {e}"); fetch_failed = True
                        combined_metrics["error_message"] = f"Failed fetch: {e}"; break # Stop fetching on error
            elif is_period_request: # Handle yfinance period request (no caching attempt)
                 data_info["data_source_label"] = args.ticker
                 logger.print_info(f"Fetching yfinance data using period '{args.period}'.")
                 fetched_period_df, metrics_period = fetch_yfinance_data(ticker=args.ticker, interval=args.interval, period=args.period)
                 combined_metrics = metrics_period or {} # Use metrics from this call
                 cached_df = None # Ensure no accidental merge with old cache
                 if fetched_period_df is not None and not fetched_period_df.empty:
                     if isinstance(fetched_period_df.index, pd.DatetimeIndex): fetched_period_df.index = fetched_period_df.index.tz_localize(None)
                     new_data_list = [fetched_period_df] # Treat fetched data as "new" for combination logic
                 else: new_data_list = []
            elif cache_load_success: # Loaded from cache, nothing to fetch
                 logger.print_info("Using only data from cache.")
                 data_info["data_source_label"] = args.ticker # Set label to ticker even if from cache

            if fetch_failed: logger.print_error("Aborting data acquisition due to fetch failure."); data_info["error_message"] = combined_metrics.get("error_message"); new_data_list = []

            # --- Combine Data ---
            all_dfs = ([cached_df] if cached_df is not None else []) + new_data_list
            combined_df = None
            if all_dfs:
                logger.print_info(f"Combining {len(all_dfs)} DataFrame(s)...")
                try:
                    combined_df = pd.concat(all_dfs)
                    if not isinstance(combined_df.index, pd.DatetimeIndex): raise TypeError("Index type error")
                    combined_df.sort_index(inplace=True)
                    rows_before_dedup = len(combined_df)
                    combined_df = combined_df[~combined_df.index.duplicated(keep='first')]
                    rows_after_dedup = len(combined_df)
                    if rows_before_dedup > rows_after_dedup: logger.print_debug(f"Removed {rows_before_dedup - rows_after_dedup} duplicate rows.")
                    logger.print_info(f"Combined data has {rows_after_dedup} unique rows.")
                except Exception as e: logger.print_error(f"Error combining data: {e}"); data_info["error_message"] = f"Error combining data: {e}"; combined_df = cached_df # Fallback

            # --- Save Updated Cache ---
            if combined_df is not None and new_data_list and not fetch_failed and cache_filepath:
                logger.print_info(f"Attempting to overwrite cache file: {cache_filepath}")
                try:
                    os.makedirs(cache_filepath.parent, exist_ok=True)
                    combined_df.to_parquet(cache_filepath, index=True, engine='pyarrow')
                    logger.print_success(f"Successfully updated cache file: {cache_filepath}")
                    data_info["parquet_save_path"] = str(cache_filepath)
                except ImportError: logger.print_error("Failed to save Parquet: pyarrow not installed.")
                except Exception as e: logger.print_error(f"Failed to save updated cache file {cache_filepath}: {e}")

            # --- Return Requested Slice ---
            final_df = None
            if combined_df is not None and not is_period_request: # Slice only if start/end were given
                logger.print_info(f"Filtering combined data for requested range: {args.start} to {args.end}")
                try:
                    # Use original start/end dates for slicing
                    slice_start = pd.to_datetime(args.start).tz_localize(None)
                    slice_end = pd.to_datetime(args.end).tz_localize(None)
                    # Slice inclusive of both start and end dates
                    final_df = combined_df.loc[slice_start:slice_end].copy()
                    if final_df.empty: logger.print_warning("Requested date range resulted in empty slice.")
                    else: logger.print_info(f"Final DataFrame slice has {len(final_df)} rows.")
                except Exception as e: logger.print_error(f"Error slicing combined DataFrame: {e}"); final_df = None
            elif combined_df is not None and is_period_request: # For period request, return the whole fetched df
                final_df = combined_df

            df = final_df # Final assignment

        except ValueError as ve: logger.print_error(f"Config error: {ve}"); data_info["error_message"] = str(ve)
        except ImportError as ie: logger.print_error(f"Missing library: {ie}"); data_info["error_message"] = str(ie)
        except Exception as e: logger.print_error(f"Unexpected error in acquire_data: {e}"); logger.print_error(f"Traceback:\n{traceback.format_exc()}"); data_info["error_message"] = str(e)

    # --- Final Update of data_info ---
    data_info["ohlcv_df"] = df
    # Merge combined metrics collected during API calls or from CSV fetch
    if isinstance(combined_metrics, dict):
        if "latency_sec" in combined_metrics: data_info["api_latency_sec"] = combined_metrics["latency_sec"]
        if "total_latency_sec" in combined_metrics: data_info["api_latency_sec"] = combined_metrics["total_latency_sec"] # Polygon/Binance use this
        if "api_calls" in combined_metrics: data_info["api_calls"] = combined_metrics["api_calls"]
        if "successful_chunks" in combined_metrics: data_info["successful_chunks"] = combined_metrics["successful_chunks"]
        if "rows_fetched" in combined_metrics: data_info["rows_fetched"] = combined_metrics["rows_fetched"]
        if "file_size_bytes" in combined_metrics: data_info["file_size_bytes"] = combined_metrics["file_size_bytes"] # From CSV
        # Ensure error message is updated if fetch failed and no other error occurred
        if "error_message" in combined_metrics and data_info["error_message"] is None:
            data_info["error_message"] = combined_metrics["error_message"]
        data_info["data_metrics"].update(combined_metrics)

    # Update metrics from file size if cache was used but no API call made
    if data_info["parquet_cache_used"] and combined_metrics.get("api_calls", 0) == 0 and cache_filepath and cache_filepath.exists():
         try: data_info["file_size_bytes"] = cache_filepath.stat().st_size
         except Exception: pass

    # Populate counts from final df
    if df is not None and not df.empty:
        data_info["rows_count"] = len(df)
        data_info["columns_count"] = len(df.columns)
        try:
             data_info["data_size_bytes"] = df.memory_usage(deep=True).sum()
             data_info["data_size_mb"] = data_info["data_size_bytes"] / (1024 * 1024)
        except Exception: pass # Ignore memory calculation errors
    elif data_info.get("error_message") is None: # Only warn if no error message already set
        logger.print_warning("Data acquisition resulted in None or empty DataFrame.")

    logger.print_info(f"Data acquisition finished. Cache used: {data_info['parquet_cache_used']}.")
    return data_info