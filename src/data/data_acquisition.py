# src/data/data_acquisition.py # CORRECTED v6: _get_interval_delta and fetch before cache date

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

# Use relative imports for fetchers within the same package
from .fetchers import (
    fetch_csv_data, fetch_yfinance_data, fetch_polygon_data,
    fetch_binance_data, get_demo_data
)
# Use relative import for logger
from ..common import logger

# Helper function to get interval delta
def _get_interval_delta(interval_str: str) -> pd.Timedelta | None:
    """
    Converts common interval strings (e.g., 'h1', 'D1', 'M1', 'W') to pandas Timedelta.
    Handles common variations and logs a warning for unparseable intervals.
    """
    simple_map = {
        'M1': '1min', 'M5': '5min', 'M15': '15min', 'M30': '30min',
        'H1': '1h', 'h1': '1h',
        'H4': '4h', # Note: Binance/Polygon support 4h, YF might not directly
        'D1': '1d', 'D': '1d',
        'W': '7d', 'W1': '7d', 'WK': '7d', # Map week variations to 7d
        'MN': '30d', 'MN1': '30d', 'MO': '30d' # Approximation for month delta check
    }
    # Check direct pandas frequency strings first (like '1h', '15min', '1d')
    try:
        delta = pd.Timedelta(interval_str)
        if delta.total_seconds() > 0: return delta
    except ValueError:
        pass # Not a direct pandas string, try mapping

    # Try mapping common variations
    pd_freq = simple_map.get(interval_str.upper())
    if pd_freq:
        try:
            delta = pd.Timedelta(pd_freq)
            if delta.total_seconds() > 0: return delta
        except ValueError:
            pass # Should not happen if map is correct, but handle anyway

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
        "parquet_cache_file": None, "steps_duration": {} # Initialize steps_duration
    }
    logger.print_info(f"--- Step 1: Acquiring Data (Mode: {effective_mode.capitalize()}) ---")

    df = None; metrics = {}; cached_df = None; cache_filepath = None
    fetch_ranges = []; req_start_dt = None; req_end_dt_inclusive = None # Initialize
    combined_metrics = {} # Initialize combined_metrics

    # --- Handle non-cacheable modes first ---
    if effective_mode == 'demo':
        data_info["data_source_label"] = "Demo Data"; df = get_demo_data(); metrics = {}
        data_info["ohlcv_df"] = df; return data_info # Return early
    elif effective_mode == 'csv':
        data_info["data_source_label"] = args.csv_file
        df, metrics = fetch_csv_data(filepath=args.csv_file)
        combined_metrics = metrics or {}
        # Let final update outside handle metrics

    # --- Logic for Cacheable API Modes ---
    elif effective_mode in ['yfinance', 'polygon', 'binance']:
        try:
            # --- Date Parsing & Validation ---
            is_period_request = effective_mode == 'yfinance' and args.period
            cache_start_dt = None # Initialize
            cache_end_dt = None # Initialize
            req_end_dt_input = None # Initialize for later slicing

            if not is_period_request: # Using start/end dates
                 try:
                      req_start_dt = pd.to_datetime(args.start, errors='raise').tz_localize(None)
                      req_end_dt_input = pd.to_datetime(args.end, errors='raise').tz_localize(None)
                      # For range checks and fetch logic, go slightly beyond the end date midnight
                      req_end_dt_inclusive = req_end_dt_input + timedelta(days=1) - timedelta(milliseconds=1)
                      if req_start_dt >= req_end_dt_inclusive: raise ValueError("Start date must be before end date.")
                 except Exception as date_err:
                      # Wrap original error for better context
                      raise ValueError(f"Invalid start/end date format or range: {date_err}") from date_err
            else: # Using yfinance period
                 req_start_dt, req_end_dt_inclusive = None, None

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
                        # Ensure naive index for comparison
                        cached_df.index = cached_df.index.tz_localize(None)
                        cache_start_dt = cached_df.index.min()
                        cache_end_dt = cached_df.index.max()
                        logger.print_success(f"Loaded {len(cached_df)} rows from cache ({cache_start_dt} to {cache_end_dt}).")
                        data_info["parquet_cache_used"] = True
                        cache_load_success = True
                        try: data_info["file_size_bytes"] = cache_filepath.stat().st_size
                        except Exception: pass # Ignore stat errors
                except Exception as e:
                     logger.print_warning(f"Failed to load cache file {cache_filepath}: {e}")
                     # Fallback: behave as if cache doesn't exist
                     cached_df = None; cache_load_success = False; data_info["parquet_cache_used"] = False


            # --- Determine Fetch Ranges ---
            if not is_period_request:
                interval_delta = _get_interval_delta(args.interval)
                # Need valid req_start_dt for cache logic
                if not req_start_dt: raise ValueError("Start date is required for cacheable API modes.")

                if cache_load_success and interval_delta and cache_start_dt and cache_end_dt:
                    # Fetch data before cache if needed
                    if req_start_dt < cache_start_dt:
                        fetch_before_end = cache_start_dt - interval_delta # Last timestamp needed before cache
                        if fetch_before_end >= req_start_dt:
                            # Store cache_start_dt to signal this is a "before" fetch for date calc later
                            fetch_ranges.append((req_start_dt, fetch_before_end, cache_start_dt))
                    # Fetch data after cache if needed
                    if req_end_dt_inclusive > cache_end_dt:
                        fetch_after_start = cache_end_dt + interval_delta # First timestamp needed after cache
                        if fetch_after_start <= req_end_dt_inclusive:
                            # Signal not "before" fetch using None for the third element
                             fetch_ranges.append((fetch_after_start, req_end_dt_inclusive, None))

                    if not fetch_ranges: logger.print_info("Requested range is fully covered by cache.")
                    else: logger.print_info(f"Found {len(fetch_ranges)} missing range(s) to fetch.")

                elif not cache_load_success: # No cache or read error, fetch full range
                    fetch_ranges.append((req_start_dt, req_end_dt_inclusive, None))
                    logger.print_info(f"No cache found/usable. Fetching full range: {args.start} to {args.end}")
                elif not interval_delta: # Cache loaded but couldn't get delta
                     logger.print_warning("Could not determine interval delta, cannot fetch partial data. Using cache only.")

            # --- Fetch Missing Data ---
            new_data_list = []; fetch_failed = False
            if fetch_ranges:
                data_info["data_source_label"] = args.ticker # Set label to ticker since we fetch from API
                for fetch_range_data in fetch_ranges:
                    fetch_start, fetch_end, signal_cache_start = fetch_range_data # Unpack tuple

                    fetch_start_str = fetch_start.strftime('%Y-%m-%d')
                    # *** CORRECTED DATE CALCULATION LOGIC (ensure this block is correct) ***
                    if signal_cache_start is not None: # This is the "fetch before" range
                         # End date for API call should be the day the cache starts (exclusive)
                         fetch_end_str = signal_cache_start.strftime('%Y-%m-%d')
                    else: # This is a "fetch after" or "full range" fetch
                         # End date for API call should be day after the last needed timestamp
                         fetch_end_api_call = fetch_end + timedelta(days=1) # Go one day beyond the end timestamp needed
                         fetch_end_str = fetch_end_api_call.strftime('%Y-%m-%d')

                    # Log the actual inclusive range being fetched
                    logger.print_info(f"Fetching range: {fetch_start_str} to {fetch_end.strftime('%Y-%m-%d')} from {effective_mode}... (API Call end: {fetch_end_str})")
                    new_df_part = None; metrics_part = {}
                    try:
                        if effective_mode == 'yfinance':
                            new_df_part, metrics_part = fetch_yfinance_data(ticker=args.ticker, interval=args.interval, start_date=fetch_start_str, end_date=fetch_end_str, period=None)
                        elif effective_mode == 'polygon':
                            new_df_part, metrics_part = fetch_polygon_data(ticker=args.ticker, interval=args.interval, start_date=fetch_start_str, end_date=fetch_end_str)
                        elif effective_mode == 'binance':
                            new_df_part, metrics_part = fetch_binance_data(ticker=args.ticker, interval=args.interval, start_date=fetch_start_str, end_date=fetch_end_str)

                        if new_df_part is not None and not new_df_part.empty:
                            if isinstance(new_df_part.index, pd.DatetimeIndex): new_df_part.index = new_df_part.index.tz_localize(None)
                            new_data_list.append(new_df_part); logger.print_success(f"Fetched {len(new_df_part)} new rows.")
                        else: logger.print_warning(f"No data returned for range {fetch_start_str} to {fetch_end.strftime('%Y-%m-%d')}.")
                        # Accumulate metrics
                        if isinstance(metrics_part, dict):
                            for key, value in metrics_part.items():
                                if key == "error_message" and value and "error_message" not in combined_metrics: combined_metrics["error_message"] = value # Store first error
                                elif isinstance(value, (int, float)): combined_metrics[key] = combined_metrics.get(key, 0) + value
                    except Exception as e:
                        logger.print_error(f"Failed to fetch range {fetch_start_str} to {fetch_end.strftime('%Y-%m-%d')}: {e}"); fetch_failed = True
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
                    if not isinstance(combined_df.index, pd.DatetimeIndex): raise TypeError("Index type error after concat")
                    combined_df.sort_index(inplace=True)
                    rows_before_dedup = len(combined_df)
                    # Keep first occurrence on duplicate index
                    combined_df = combined_df[~combined_df.index.duplicated(keep='first')]
                    rows_after_dedup = len(combined_df)
                    if rows_before_dedup > rows_after_dedup: logger.print_debug(f"Removed {rows_before_dedup - rows_after_dedup} duplicate rows.")
                    logger.print_info(f"Combined data has {rows_after_dedup} unique rows.")
                except Exception as e: logger.print_error(f"Error combining data: {e}"); data_info["error_message"] = f"Error combining data: {e}"; combined_df = cached_df # Fallback to cache if concat fails? Risky.

            # --- Save Updated Cache ---
            # Save if new data was fetched OR if it was a period request (to potentially overwrite stale cache)
            should_save = (new_data_list and not fetch_failed and cache_filepath) or \
                          (is_period_request and combined_df is not None and not combined_df.empty and cache_filepath)
            if should_save:
                logger.print_info(f"Attempting to save/overwrite cache file: {cache_filepath}")
                try:
                    os.makedirs(cache_filepath.parent, exist_ok=True)
                    # Ensure the combined dataframe is not None before saving
                    if combined_df is not None:
                         combined_df.to_parquet(cache_filepath, index=True, engine='pyarrow')
                         logger.print_success(f"Successfully saved/updated cache file: {cache_filepath}")
                         data_info["parquet_save_path"] = str(cache_filepath)
                    else:
                         logger.print_warning("Combined DataFrame is None, cannot save cache.")
                except ImportError: logger.print_error("Failed to save Parquet: pyarrow not installed.")
                except Exception as e: logger.print_error(f"Failed to save updated cache file {cache_filepath}: {e}")

            # --- Return Requested Slice ---
            final_df = None
            if combined_df is not None and not is_period_request: # Slice only if start/end were given
                 logger.print_info(f"Filtering combined data for requested range: {args.start} to {args.end}")
                 try:
                     # Use original start/end dates for slicing (now uses req_end_dt_input)
                     slice_start = req_start_dt # Already a timestamp
                     slice_end = req_end_dt_input # Use the parsed timestamp for end date
                     final_df = combined_df.loc[slice_start:slice_end].copy() # Slice is inclusive
                     if final_df.empty and not combined_df.loc[slice_start:slice_end].empty:
                          logger.print_warning("Copying slice resulted in empty DataFrame unexpectedly.")
                          final_df = combined_df.loc[slice_start:slice_end]

                     if final_df.empty: logger.print_warning("Requested date range resulted in empty slice.")
                     else: logger.print_info(f"Final DataFrame slice has {len(final_df)} rows.")
                 except KeyError: # Handle cases where slice dates are not in index
                      logger.print_warning(f"Requested date range {args.start}-{args.end} not fully found in combined data index. Returning empty slice.")
                      final_df = pd.DataFrame() # Return empty instead of None
                 except Exception as e:
                      logger.print_error(f"Error slicing combined DataFrame: {e}"); final_df = None
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
        data_info["api_latency_sec"] = combined_metrics.get("total_latency_sec", combined_metrics.get("latency_sec", 0.0))
        data_info["api_calls"] = combined_metrics.get("api_calls", 0)
        data_info["successful_chunks"] = combined_metrics.get("successful_chunks", 0)
        data_info["rows_fetched"] = combined_metrics.get("rows_fetched", 0)
        if "file_size_bytes" in combined_metrics: data_info["file_size_bytes"] = combined_metrics["file_size_bytes"]
        if "error_message" in combined_metrics and data_info["error_message"] is None:
            data_info["error_message"] = combined_metrics["error_message"]
        data_info["data_metrics"].update(combined_metrics)

    # Update file size metric from cache file if cache used and size not set otherwise
    if data_info["parquet_cache_used"] and data_info.get("file_size_bytes") is None and cache_filepath and cache_filepath.exists():
         try: data_info["file_size_bytes"] = cache_filepath.stat().st_size
         except Exception: pass

    # Populate counts from final df
    if df is not None and not df.empty:
        data_info["rows_count"] = len(df)
        data_info["columns_count"] = len(df.columns)
        try:
             data_info["data_size_bytes"] = df.memory_usage(deep=True).sum()
             data_info["data_size_mb"] = data_info["data_size_bytes"] / (1024 * 1024)
        except Exception: pass
    elif data_info.get("error_message") is None:
        logger.print_warning("Data acquisition resulted in None or empty DataFrame.")

    logger.print_info(f"Data acquisition finished. Cache used: {data_info['parquet_cache_used']}.")
    return data_info