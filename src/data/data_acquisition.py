# File: src/data/data_acquisition.py
# (Includes corrections for calling fetch_csv_data with specific mappings)

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
from ..common.logger import print_info, print_warning, print_error, print_debug, print_success  # Use print_* functions

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
        # Attempt to create Timedelta directly
        delta = pd.Timedelta(interval_str)
        if delta.total_seconds() > 0: return delta
    except ValueError:
        # Not a direct pandas string, try mapping
        pass

    # Try mapping common variations
    pd_freq = simple_map.get(interval_str.upper())
    if pd_freq:
        try:
             # Attempt Timedelta from mapped frequency string
            delta = pd.Timedelta(pd_freq)
            if delta.total_seconds() > 0: return delta
        except ValueError:
            # Should not happen if map is correct, but handle anyway
            pass

    print_warning(f"Could not parse interval '{interval_str}' to Timedelta. Cache delta logic may be affected.")
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
        print_warning(f"Error generating instrument parquet filename: {e}")
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
              Returns dict with 'error_message' on failure.
    """
    # Load environment variables if needed by fetchers
    dotenv_path = '.env'; load_dotenv(dotenv_path=dotenv_path)
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode # Normalize mode

    # Initialize the dictionary to store results and info
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
    print_info(f"--- Step 1: Acquiring Data (Mode: {effective_mode.capitalize()}) ---")

    df = None; metrics = {}; cached_df = None; cache_filepath = None
    fetch_ranges = []; req_start_dt = None; req_end_dt_inclusive = None # Initialize
    combined_metrics = {} # Initialize combined_metrics

    try:
        # --- Handle non-cacheable modes first ---
        if effective_mode == 'demo':
            data_info["data_source_label"] = "Demo Data"; df = get_demo_data(); metrics = {}
            data_info["ohlcv_df"] = df; return data_info # Return early for demo

        elif effective_mode == 'csv':
            data_info["data_source_label"] = args.csv_file

            # --- CORRECTED CALL TO fetch_csv_data ---
            # Define the mapping based on the actual CSV header from mql5_feed/...
            # Note the trailing commas and TickVolume
            csv_column_mapping = {
                'Open': 'Open,',
                'High': 'High,',
                'Low': 'Low,',
                'Close': 'Close,',
                'Volume': 'TickVolume,' # Map standard 'Volume' to CSV's 'TickVolume,'
            }
            # Define the datetime column name from CSV
            csv_datetime_column = 'DateTime,'

            # Call fetch_csv_data with explicit mappings and skiprows
            # It now returns only the DataFrame, or an empty DataFrame on error
            df = fetch_csv_data(
                file_path=args.csv_file,
                ohlc_columns=csv_column_mapping,
                datetime_column=csv_datetime_column,
                skiprows=1,  # Skip the first info line before the header
                separator=',' # Explicitly state separator
                # Note: Metrics dict is not returned by the modified fetch_csv_data
            )
            # --- END CORRECTION ---

            # Check if df is empty (indicating an error during fetch)
            if df.empty:
                 # Attempt to get a more specific error message if possible, otherwise use generic
                 # (Currently, fetch_csv_data logs errors but returns empty df, needs refinement to pass error msg back)
                 raise ValueError(f"Failed to read or process CSV file: {args.csv_file}. Check logs for details.")

            # Populate some basic metrics for CSV mode
            combined_metrics = {}
            if args.csv_file and Path(args.csv_file).exists():
                try:
                    combined_metrics["file_size_bytes"] = Path(args.csv_file).stat().st_size
                except Exception:
                    pass # Ignore stat errors
            # No API latency/calls for CSV
            combined_metrics["api_latency_sec"] = 0.0
            combined_metrics["api_calls"] = 0

        # --- Logic for Cacheable API Modes ---
        elif effective_mode in ['yfinance', 'polygon', 'binance']:
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
                      # IMPORTANT: Add 1 full day to end date input for inclusive behavior for API calls
                      # For slicing later, we use req_end_dt_input directly
                      req_end_dt_api = req_end_dt_input + timedelta(days=1)
                      # For internal check, use milliseconds before the next day starts
                      req_end_dt_inclusive = req_end_dt_api - timedelta(milliseconds=1)

                      if req_start_dt >= req_end_dt_api: raise ValueError("Start date must be before end date.")
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
                print_info(f"Found existing cache file: {cache_filepath}")
                try:
                    cached_df = pd.read_parquet(cache_filepath)
                    if not isinstance(cached_df.index, pd.DatetimeIndex) or cached_df.empty:
                        print_warning("Cache file invalid (no DatetimeIndex or empty). Ignoring cache.")
                        cached_df = None
                    else:
                        # Ensure naive index for comparison
                        if cached_df.index.tz is not None:
                             cached_df.index = cached_df.index.tz_localize(None)
                        cache_start_dt = cached_df.index.min()
                        cache_end_dt = cached_df.index.max()
                        print_success(f"Loaded {len(cached_df)} rows from cache ({cache_start_dt} to {cache_end_dt}).")
                        data_info["parquet_cache_used"] = True
                        cache_load_success = True
                        try: data_info["file_size_bytes"] = cache_filepath.stat().st_size
                        except Exception: pass # Ignore stat errors
                except Exception as e:
                     print_warning(f"Failed to load cache file {cache_filepath}: {e}")
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
                            # API end date should be the day *before* cache starts
                            fetch_ranges.append((req_start_dt, fetch_before_end, cache_start_dt))
                    # Fetch data after cache if needed
                    if req_end_dt_inclusive > cache_end_dt:
                        fetch_after_start = cache_end_dt + interval_delta # First timestamp needed after cache
                        if fetch_after_start <= req_end_dt_inclusive:
                            # Signal not "before" fetch using None for the third element
                             fetch_ranges.append((fetch_after_start, req_end_dt_inclusive, None))

                    if not fetch_ranges: print_info("Requested range is fully covered by cache.")
                    else: print_info(f"Found {len(fetch_ranges)} missing range(s) to fetch.")

                elif not cache_load_success: # No cache or read error, fetch full range
                    fetch_ranges.append((req_start_dt, req_end_dt_inclusive, None))
                    print_info(f"No cache found/usable. Fetching full range: {args.start} to {args.end}")
                elif not interval_delta: # Cache loaded but couldn't get delta
                     print_warning("Could not determine interval delta, cannot fetch partial data. Using cache only.")

            # --- Fetch Missing Data ---
            new_data_list = []; fetch_failed = False
            temp_metrics = {} # Temp dict to aggregate metrics from multiple fetches

            if fetch_ranges:
                data_info["data_source_label"] = args.ticker # Set label to ticker since we fetch from API
                for fetch_range_data in fetch_ranges:
                    fetch_start, fetch_end, signal_cache_start = fetch_range_data # Unpack tuple

                    fetch_start_str = fetch_start.strftime('%Y-%m-%d')
                    # Determine the correct END DATE STRING for the API call
                    if signal_cache_start is not None: # This is the "fetch before" range
                         # API call should end *before* the cache starts.
                         # Use the day *before* the cache start date.
                         fetch_end_api_call_dt = signal_cache_start - timedelta(days=1)
                         fetch_end_str = fetch_end_api_call_dt.strftime('%Y-%m-%d')
                    else: # This is a "fetch after" or "full range" fetch
                         # API call end date should be the actual END date requested by user.
                         # req_end_dt_input holds the user's requested end date (inclusive)
                         fetch_end_str = req_end_dt_input.strftime('%Y-%m-%d')

                    # Log the actual inclusive range being fetched for user understanding
                    print_info(f"Fetching range: {fetch_start_str} to {fetch_end.strftime('%Y-%m-%d')} from {effective_mode}... (API Call: {fetch_start_str} to {fetch_end_str})")

                    new_df_part = None; metrics_part = {}
                    fetch_func = None
                    if effective_mode == 'yfinance': fetch_func = fetch_yfinance_data
                    elif effective_mode == 'polygon': fetch_func = fetch_polygon_data
                    elif effective_mode == 'binance': fetch_func = fetch_binance_data

                    if fetch_func:
                         try:
                             # Call the appropriate fetcher
                             new_df_part, metrics_part = fetch_func(
                                 ticker=args.ticker,
                                 interval=args.interval,
                                 start_date=fetch_start_str,
                                 end_date=fetch_end_str # Pass API end date string
                                 # Yfinance needs special handling if 'period' was used (not here)
                                 # For yfinance, pass period=None explicitly if start/end used
                                 **({'period': None} if effective_mode == 'yfinance' else {})
                             )

                             if new_df_part is not None and not new_df_part.empty:
                                 # Ensure index is naive datetime
                                 if isinstance(new_df_part.index, pd.DatetimeIndex):
                                     if new_df_part.index.tz is not None:
                                         new_df_part.index = new_df_part.index.tz_localize(None)
                                 new_data_list.append(new_df_part); print_success(f"Fetched {len(new_df_part)} new rows.")
                             else: print_warning(f"No data returned for range {fetch_start_str} to {fetch_end_str}.")

                             # Accumulate metrics safely
                             if isinstance(metrics_part, dict):
                                 for key, value in metrics_part.items():
                                     if key == "error_message" and value and "error_message" not in temp_metrics:
                                         temp_metrics["error_message"] = value # Store first error
                                     elif isinstance(value, (int, float)):
                                         temp_metrics[key] = temp_metrics.get(key, 0) + value
                         except Exception as e:
                              error_msg = f"Failed fetch range {fetch_start_str}-{fetch_end_str}: {e}"
                              print_error(error_msg); fetch_failed = True
                              # Store the critical error message
                              temp_metrics["error_message"] = error_msg
                              # Print traceback for unexpected errors during fetch call
                              print_error("Traceback:")
                              traceback.print_exc()
                              break # Stop fetching on error
                    else:
                         print_error(f"Internal error: No fetch function defined for mode {effective_mode}")
                         fetch_failed = True; break

                # After loop, merge collected metrics into combined_metrics
                combined_metrics.update(temp_metrics)

            elif is_period_request: # Handle yfinance period request (no caching attempt)
                 data_info["data_source_label"] = args.ticker
                 print_info(f"Fetching yfinance data using period '{args.period}'.")
                 fetched_period_df, metrics_period = fetch_yfinance_data(
                     ticker=args.ticker, interval=args.interval, period=args.period,
                     start_date=None, end_date=None # Explicitly None when period is used
                     )
                 combined_metrics = metrics_period or {} # Use metrics from this call
                 cached_df = None # Ensure no accidental merge with old cache
                 if fetched_period_df is not None and not fetched_period_df.empty:
                     # Ensure index is naive datetime
                     if isinstance(fetched_period_df.index, pd.DatetimeIndex):
                         if fetched_period_df.index.tz is not None:
                              fetched_period_df.index = fetched_period_df.index.tz_localize(None)
                     new_data_list = [fetched_period_df] # Treat fetched data as "new"
                 else: new_data_list = [] # No data fetched for period
            elif cache_load_success: # Loaded from cache, nothing to fetch
                 print_info("Using only data from cache.")
                 data_info["data_source_label"] = args.ticker # Set label to ticker even if from cache
            else: # Catchall: No cache, no period, no fetch ranges determined (should be rare)
                 print_warning("No data fetching triggered (no cache, no API fetch needed/possible).")


            if fetch_failed:
                 # Use the error stored in combined_metrics if available
                 final_error_msg = combined_metrics.get("error_message", "Aborting data acquisition due to fetch failure.")
                 print_error(final_error_msg)
                 data_info["error_message"] = final_error_msg; new_data_list = []

            # --- Combine Data ---
            all_dfs = ([cached_df] if cached_df is not None else []) + new_data_list
            combined_df = None
            if all_dfs:
                print_info(f"Combining {len(all_dfs)} DataFrame(s)...")
                try:
                    combined_df = pd.concat(all_dfs)
                    if not isinstance(combined_df.index, pd.DatetimeIndex): raise TypeError("Index type error after concat")
                    # Ensure naive index after concat
                    if combined_df.index.tz is not None: combined_df.index = combined_df.index.tz_localize(None)
                    combined_df.sort_index(inplace=True)
                    rows_before_dedup = len(combined_df)
                    # Keep first occurrence on duplicate index
                    combined_df = combined_df[~combined_df.index.duplicated(keep='first')]
                    rows_after_dedup = len(combined_df)
                    if rows_before_dedup > rows_after_dedup: print_debug(f"Removed {rows_before_dedup - rows_after_dedup} duplicate rows after combining.")
                    print_info(f"Combined data has {rows_after_dedup} unique rows.")
                except Exception as e:
                    print_error(f"Error combining data: {e}")
                    data_info["error_message"] = f"Error combining data: {e}"
                    # Decide fallback: use only cache? or fail? Let's fail for safety.
                    combined_df = None
                    raise # Re-raise the concatenation error

            # --- Save Updated Cache ---
            # Save if new data was fetched successfully OR if it was a period request (to potentially overwrite stale cache)
            should_save = (new_data_list and not fetch_failed and cache_filepath) or \
                          (is_period_request and combined_df is not None and not combined_df.empty and cache_filepath)
            if should_save:
                print_info(f"Attempting to save/overwrite cache file: {cache_filepath}")
                try:
                    os.makedirs(cache_filepath.parent, exist_ok=True)
                    # Ensure the combined dataframe is not None before saving
                    if combined_df is not None:
                         # Double check index is naive before saving
                         if combined_df.index.tz is not None: combined_df.index = combined_df.index.tz_localize(None)
                         combined_df.to_parquet(cache_filepath, index=True, engine='pyarrow')
                         print_success(f"Successfully saved/updated cache file: {cache_filepath}")
                         data_info["parquet_save_path"] = str(cache_filepath)
                    else:
                         print_warning("Combined DataFrame is None, cannot save cache.")
                except ImportError: print_error("Failed to save Parquet: pyarrow not installed.")
                except Exception as e: print_error(f"Failed to save updated cache file {cache_filepath}: {e}")

            # --- Return Requested Slice ---
            final_df = None
            if combined_df is not None and not is_period_request: # Slice only if start/end were given
                 print_info(f"Filtering combined data for requested range: {args.start} to {args.end}")
                 try:
                     # Use original start/end date objects for slicing
                     slice_start = req_start_dt # This is tz-naive
                     slice_end = req_end_dt_input # This is tz-naive and represents the END of the requested day
                     # Slicing with pandas loc is inclusive for both start and end when using timestamps
                     final_df = combined_df.loc[slice_start:slice_end].copy()
                     if final_df.empty and not combined_df.loc[slice_start:slice_end].empty:
                          print_warning("Copying slice resulted in empty DataFrame unexpectedly.")
                          final_df = combined_df.loc[slice_start:slice_end] # Fallback to view if copy fails

                     if final_df.empty: print_warning(f"Requested date range {args.start}-{args.end} resulted in empty slice from combined data.")
                     else: print_info(f"Final DataFrame slice has {len(final_df)} rows.")
                 except KeyError: # Handle cases where slice dates are not in index
                      print_warning(f"Requested date range {args.start}-{args.end} not fully found in combined data index. Returning empty slice.")
                      final_df = pd.DataFrame() # Return empty instead of None
                 except Exception as e:
                      print_error(f"Error slicing combined DataFrame: {e}"); final_df = None
                      data_info["error_message"] = f"Error slicing data: {e}" # Store slicing error
            elif combined_df is not None and is_period_request: # For period request, return the whole fetched df
                final_df = combined_df

            df = final_df # Final assignment for API modes

    # --- General Exception Handling ---
    # Catch errors from date parsing, invalid config, or unexpected issues
    except ValueError as ve: print_error(f"Configuration error: {ve}"); data_info["error_message"] = str(ve)
    except ImportError as ie: print_error(f"Missing library: {ie}"); data_info["error_message"] = str(ie)
    except Exception as e:
        # Catch any other unexpected errors during the process
        print_error(f"Unexpected error in acquire_data: {e}");
        # Use print_error for traceback as logger isn't setup here
        print_error("Traceback:")
        traceback.print_exc()
        data_info["error_message"] = str(e)
        df = None # Ensure df is None on unexpected error


    # --- Final Update of data_info ---
    # Assign the final DataFrame (could be None or empty if errors occurred)
    data_info["ohlcv_df"] = df

    # Merge combined metrics collected during API calls or from CSV fetch
    if isinstance(combined_metrics, dict):
        # Normalize latency key (some fetchers use 'total_latency_sec', others 'latency_sec')
        api_latency = combined_metrics.get("total_latency_sec", combined_metrics.get("latency_sec", 0.0))
        data_info["api_latency_sec"] = api_latency if api_latency is not None else 0.0

        data_info["api_calls"] = combined_metrics.get("api_calls", 0)
        data_info["successful_chunks"] = combined_metrics.get("successful_chunks", 0)
        data_info["rows_fetched"] = combined_metrics.get("rows_fetched", 0)
        if "file_size_bytes" in combined_metrics: data_info["file_size_bytes"] = combined_metrics["file_size_bytes"]
        # If an error wasn't caught by main try/except, use one from metrics if present
        if "error_message" in combined_metrics and data_info["error_message"] is None:
            data_info["error_message"] = combined_metrics["error_message"]
        # Store all collected metrics within data_metrics for potential detailed reporting
        data_info["data_metrics"].update(combined_metrics)

    # Update file size metric from cache file if cache was used and size not set otherwise
    if data_info["parquet_cache_used"] and data_info.get("file_size_bytes") is None and cache_filepath and cache_filepath.exists():
         try: data_info["file_size_bytes"] = cache_filepath.stat().st_size
         except Exception: pass

    # Populate counts and size from final df if available
    if df is not None and not df.empty:
        data_info["rows_count"] = len(df)
        data_info["columns_count"] = len(df.columns)
        try:
             # Calculate memory usage
             data_info["data_size_bytes"] = df.memory_usage(deep=True).sum()
             data_info["data_size_mb"] = data_info["data_size_bytes"] / (1024 * 1024)
        except Exception as mem_err:
             print_warning(f"Could not calculate DataFrame memory usage: {mem_err}")
             data_info["data_size_bytes"] = -1
             data_info["data_size_mb"] = -1.0
    elif data_info.get("error_message") is None:
        # If no specific error was recorded, but df is None/empty, log a warning
        print_warning("Data acquisition resulted in None or empty DataFrame.")
        # Optionally set a generic error message here if df is unexpectedly None/empty
        # data_info["error_message"] = "Acquisition finished with no data."

    print_info(f"Data acquisition finished. Cache used: {data_info['parquet_cache_used']}. Error: {data_info['error_message'] or 'None'}")
    return data_info # Return the populated dictionary