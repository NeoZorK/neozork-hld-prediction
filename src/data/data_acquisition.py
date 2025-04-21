# src/data/data_acquisition.py (Implemented single-file Parquet caching logic)

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
from datetime import datetime, timedelta, timezone # Import timezone
# from pandas.tseries.frequencies import to_offset # Alternative for interval delta

# Use relative imports for fetchers within the same package
from .fetchers import (
    fetch_csv_data, fetch_yfinance_data, fetch_polygon_data,
    fetch_binance_data, get_demo_data
)
# Use relative import for logger
from ..common import logger

# --- Helper function to get interval delta ---
def _get_interval_delta(interval_str: str) -> pd.Timedelta | None:
    """Converts interval string (e.g., 'H1', 'D1', 'M1') to pandas Timedelta."""
    # Simple mapping for common intervals to pandas frequency strings
    simple_map = {
        'M1': '1min', 'M5': '5min', 'M15': '15min', 'M30': '30min',
        'H1': '1h', 'H4': '4h', 'D1': '1d', 'D': '1d',
        'W': '7d', 'W1': '7d', # Approximate week as 7 days for delta calculation
        # Monthly interval is tricky for precise delta, maybe handle separately or use offset
        # 'MN': '1M', 'MN1': '1M'
    }
    pd_freq = simple_map.get(interval_str, interval_str)
    try:
        # Attempt to create Timedelta directly
        delta = pd.Timedelta(pd_freq)
        # Zero delta is invalid for stepping forward/backward
        return delta if delta.total_seconds() > 0 else None
    except ValueError:
        logger.print_warning(f"Could not parse interval '{interval_str}' to Timedelta. Cannot calculate precise missing range.")
        return None

# --- Helper function for Parquet filename (Mode, Ticker, Interval based) ---
def _generate_instrument_parquet_filename(args) -> Path | None:
    """Generates the expected instrument-specific parquet filename (no dates)."""
    if args.mode not in ['yfinance', 'polygon', 'binance'] or not args.ticker:
        return None

    parquet_dir = Path("data/raw_parquet")
    try:
        # Sanitize ticker for filename
        ticker_label = str(args.ticker).replace('/', '_').replace('-', '_').replace('=','_')
        interval_label = str(args.interval)
        # Filename format: mode_ticker_interval.parquet
        filename = f"{args.mode}_{ticker_label}_{interval_label}.parquet"
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
    # --- Load environment variables ---
    dotenv_path = '.env'; load_dotenv(dotenv_path=dotenv_path)

    # --- Initialize result structure ---
    data_info = { # Default values
        "ohlcv_df": None, "ticker": args.ticker, "interval": args.interval,
        "data_source_label": "N/A", "effective_mode": args.mode,
        "yf_ticker": None, "yf_interval": None, "current_period": None,
        "current_start": args.start, "current_end": args.end,
        "file_size_bytes": None, "api_latency_sec": 0.0, # Initialize latency
        "api_calls": 0, "successful_chunks": 0, "rows_fetched": 0,
        "error_message": None, "data_metrics": {}, "parquet_cache_used": False,
        "parquet_cache_file": None # Store the cache file path used
    }
    logger.print_info(f"--- Step 1: Acquiring Data (Mode: {args.mode.capitalize()}) ---")

    df = None; metrics = {}; cached_df = None; cache_filepath = None
    fetch_ranges = [] # List of (start_dt, end_dt) tuples to fetch

    # --- Handle non-cacheable modes first ---
    if args.mode == 'demo':
        data_info["data_source_label"] = "Demo Data"; df = get_demo_data(); metrics = {}
        data_info["ohlcv_df"] = df; return data_info # Return early for demo
    elif args.mode == 'csv':
        if not args.csv_file: raise ValueError("--csv-file is required for csv mode.")
        if args.point is None: raise ValueError("--point must be provided when using csv mode.")
        data_info["data_source_label"] = args.csv_file
        df, metrics = fetch_csv_data(filepath=args.csv_file)
        data_info["ohlcv_df"] = df
        if isinstance(metrics, dict): data_info.update(metrics) # Update metrics
        return data_info # Return early for CSV

    # --- Logic for Cacheable API Modes (yfinance, polygon, binance) ---
    try:
        # --- Validate required args for API modes ---
        if not args.ticker: raise ValueError(f"--ticker is required for {args.mode} mode.")
        # For simplicity, require start/end for caching. Period-based yfinance won't use smart cache yet.
        if not args.start or not args.end:
            if args.mode in ['polygon', 'binance'] or (args.mode == 'yfinance' and not args.period):
                raise ValueError(f"--start and --end are required for {args.mode} mode when not using --period.")
            # If yfinance with period, skip caching logic for now
            logger.print_debug("Period-based yfinance request, skipping smart cache check.")
        elif args.point is None and args.mode in ['polygon', 'binance']: # yfinance estimates point later
             raise ValueError(f"--point must be provided when using {args.mode} mode.")

        # --- Parse requested dates ---
        # Use timezone-aware UTC for comparisons if possible, assuming API returns UTC
        # Or keep naive if index is naive
        req_start_dt = pd.to_datetime(args.start, errors='coerce')
        req_end_dt = pd.to_datetime(args.end, errors='coerce')
        if pd.isna(req_start_dt) or pd.isna(req_end_dt):
            raise ValueError("Invalid start or end date format. Use YYYY-MM-DD.")
        # Make dates timezone-naive for consistency with potential naive cache index
        # If APIs return TZ-aware, this needs adjustment
        req_start_dt = req_start_dt.tz_localize(None)
        req_end_dt = req_end_dt.tz_localize(None) + timedelta(days=1) - timedelta(milliseconds=1) # Make end date inclusive

        # --- Check Cache ---
        cache_filepath = _generate_instrument_parquet_filename(args)
        data_info["parquet_cache_file"] = str(cache_filepath) if cache_filepath else None

        if cache_filepath and cache_filepath.exists():
            logger.print_info(f"Found existing cache file: {cache_filepath}")
            try:
                cached_df = pd.read_parquet(cache_filepath)
                if not isinstance(cached_df.index, pd.DatetimeIndex):
                    logger.print_warning("Cache file index is not DatetimeIndex, ignoring cache.")
                    cached_df = None # Treat as no cache
                elif cached_df.empty:
                     logger.print_warning("Cache file is empty, ignoring cache.")
                     cached_df = None
                else:
                    # Ensure cache index is also naive for comparison
                    cached_df.index = cached_df.index.tz_localize(None)
                    cache_start_dt = cached_df.index.min()
                    cache_end_dt = cached_df.index.max()
                    logger.print_success(f"Loaded {len(cached_df)} rows from cache ({cache_start_dt} to {cache_end_dt}).")
                    data_info["parquet_cache_used"] = True # Mark cache as used initially
            except Exception as e:
                logger.print_warning(f"Failed to load or parse cache file {cache_filepath}: {e}")
                cached_df = None # Treat as no cache

        # --- Determine Fetch Ranges based on Cache ---
        interval_delta = _get_interval_delta(args.interval) if args.interval else None

        if cached_df is not None and interval_delta:
            # Cache exists, calculate missing ranges
            logger.print_debug(f"Request range: {req_start_dt} to {req_end_dt}")
            logger.print_debug(f"Cache range:   {cache_start_dt} to {cache_end_dt}")

            # 1. Fetch data BEFORE cache start?
            if req_start_dt < cache_start_dt:
                fetch_before_end = cache_start_dt - interval_delta
                if fetch_before_end >= req_start_dt:
                     fetch_ranges.append((req_start_dt, fetch_before_end))
                     logger.print_info(f"Will fetch missing data BEFORE cache: {req_start_dt} to {fetch_before_end}")
                else: # Requested start is within the first cached interval
                     logger.print_debug("Requested start date is within the first cached interval.")

            # 2. Fetch data AFTER cache end?
            if req_end_dt > cache_end_dt:
                fetch_after_start = cache_end_dt + interval_delta
                if fetch_after_start <= req_end_dt:
                    fetch_ranges.append((fetch_after_start, req_end_dt))
                    logger.print_info(f"Will fetch missing data AFTER cache: {fetch_after_start} to {req_end_dt}")
                else: # Requested end is within the last cached interval
                     logger.print_debug("Requested end date is within the last cached interval.")

            if not fetch_ranges:
                logger.print_info("Requested range is fully covered by cache.")

        elif args.start and args.end: # No usable cache, fetch full requested range
            fetch_ranges.append((req_start_dt, req_end_dt))
            logger.print_info(f"No cache found or usable. Fetching full range: {args.start} to {args.end}")
        elif args.mode == 'yfinance' and args.period:
             # Fallback to basic yfinance fetch if period is used (no smart cache)
             logger.print_info(f"Fetching yfinance data using period '{args.period}'.")
             df, metrics = fetch_yfinance_data(ticker=args.ticker, interval=args.interval, period=args.period)
             fetch_ranges = [] # Ensure fetch loop is skipped
        else:
             # Should not happen if arg validation is correct
             raise ValueError("Invalid combination of arguments for data fetching.")


        # --- Fetch Missing Data ---
        new_data_list = []
        combined_metrics = {"api_calls": 0, "successful_chunks": 0, "rows_fetched": 0, "total_latency_sec": 0.0}
        fetch_failed = False

        if not fetch_ranges and cached_df is None and not (args.mode == 'yfinance' and args.period):
             logger.print_warning("No data fetch ranges determined and no cache available.")
             # Allows falling through to combine step which will result in None df

        for fetch_start, fetch_end in fetch_ranges:
            fetch_start_str = fetch_start.strftime('%Y-%m-%d')
            # Ensure fetch_end is inclusive for the fetcher functions
            # Fetchers expect YYYY-MM-DD, the inclusive logic is internal to them typically
            fetch_end_str = fetch_end.strftime('%Y-%m-%d')

            logger.print_info(f"Fetching range: {fetch_start_str} to {fetch_end_str} from {args.mode}...")
            new_df_part = None; metrics_part = {}

            # Dispatch to the correct fetcher for the partial range
            try:
                if args.mode in ['yfinance', 'yf']:
                    new_df_part, metrics_part = fetch_yfinance_data(ticker=args.ticker, interval=args.interval, start_date=fetch_start_str, end_date=fetch_end_str)
                elif args.mode == 'polygon':
                    new_df_part, metrics_part = fetch_polygon_data(ticker=args.ticker, interval=args.interval, start_date=fetch_start_str, end_date=fetch_end_str)
                elif args.mode == 'binance':
                    new_df_part, metrics_part = fetch_binance_data(ticker=args.ticker, interval=args.interval, start_date=fetch_start_str, end_date=fetch_end_str)

                if new_df_part is not None and not new_df_part.empty:
                    # Ensure index is naive datetime for concatenation
                    if isinstance(new_df_part.index, pd.DatetimeIndex):
                         new_df_part.index = new_df_part.index.tz_localize(None)
                    new_data_list.append(new_df_part)
                    logger.print_success(f"Fetched {len(new_df_part)} new rows for range.")
                else:
                     logger.print_warning(f"Fetcher returned no data for range {fetch_start_str} to {fetch_end_str}.")

                # Accumulate metrics
                if isinstance(metrics_part, dict):
                    for key, value in metrics_part.items():
                        if isinstance(value, (int, float)):
                             combined_metrics[key] = combined_metrics.get(key, 0) + value
                        elif key == "error_message" and value: # Store first error encountered
                             if "error_message" not in combined_metrics: combined_metrics["error_message"] = value

            except Exception as e:
                logger.print_error(f"Failed to fetch range {fetch_start_str} to {fetch_end_str}: {e}")
                fetch_failed = True
                combined_metrics["error_message"] = f"Failed fetch for {fetch_start_str}-{fetch_end_str}: {e}"
                break # Stop fetching if one range fails

        if fetch_failed:
             logger.print_error("Aborting data acquisition due to fetch failure.")
             data_info["error_message"] = combined_metrics.get("error_message", "Fetch failed for one or more ranges.")
             # Keep potentially loaded cache, but df will be derived from it only
             new_data_list = [] # Discard any partially fetched new data

        # --- Combine Data ---
        all_dfs = [cached_df] if cached_df is not None else []
        all_dfs.extend(new_data_list)
        combined_df = None

        if all_dfs:
            logger.print_info(f"Combining {len(all_dfs)} DataFrame(s) (cache + new fetches)...")
            try:
                combined_df = pd.concat(all_dfs)
                # Ensure index is datetime after concat
                if not isinstance(combined_df.index, pd.DatetimeIndex):
                     raise TypeError("Combined DataFrame index is not DatetimeIndex.")
                # Sort and remove duplicates
                combined_df.sort_index(inplace=True)
                rows_before_dedup = len(combined_df)
                combined_df = combined_df[~combined_df.index.duplicated(keep='first')]
                rows_after_dedup = len(combined_df)
                if rows_before_dedup > rows_after_dedup:
                    logger.print_debug(f"Removed {rows_before_dedup - rows_after_dedup} duplicate rows after combining.")
                logger.print_info(f"Combined data has {rows_after_dedup} unique rows.")
            except Exception as e:
                 logger.print_error(f"Error combining cached and new data: {e}")
                 data_info["error_message"] = f"Error combining data: {e}"
                 combined_df = cached_df if cached_df is not None else None # Fallback to cache if combination fails

        # --- Save Updated Cache (if new data was fetched and combined successfully) ---
        if combined_df is not None and new_data_list and not fetch_failed: # Only save if new data added and no errors
            if cache_filepath:
                logger.print_info(f"Attempting to overwrite cache file: {cache_filepath}")
                try:
                    os.makedirs(cache_filepath.parent, exist_ok=True)
                    combined_df.to_parquet(cache_filepath, index=True, engine='pyarrow')
                    logger.print_success(f"Successfully updated cache file: {cache_filepath}")
                    data_info["parquet_save_path"] = str(cache_filepath) # Record path if saved
                except ImportError:
                     logger.print_error("Failed to save Parquet: pyarrow not installed.")
                except Exception as e:
                     logger.print_error(f"Failed to save updated cache file {cache_filepath}: {e}")
            else:
                 logger.print_warning("Could not determine cache file path, skipping save.")


        # --- Return Requested Slice ---
        if combined_df is not None:
            logger.print_info(f"Filtering combined data for requested range: {args.start} to {args.end}")
            try:
                # Ensure requested dates are compatible with index (naive vs naive)
                final_df = combined_df.loc[req_start_dt:req_end_dt].copy()
                if final_df.empty:
                     logger.print_warning("Requested date range resulted in empty slice after combining/filtering.")
                else:
                     logger.print_info(f"Final DataFrame slice has {len(final_df)} rows.")
            except KeyError:
                 logger.print_warning(f"Requested date range ({args.start} to {args.end}) not fully found in combined data. Returning available data.")
                 # Return combined df if slice fails, or decide on other behavior
                 final_df = combined_df # Or maybe return None? Let's return combined for now.
            except Exception as e:
                 logger.print_error(f"Error slicing combined DataFrame: {e}")
                 final_df = None # Return None if slicing fails badly
        else:
            final_df = None

        df = final_df # Assign the final sliced (or None) df


    except ValueError as ve: # Catch config errors from validation
        logger.print_error(f"Configuration error for mode '{args.mode}': {ve}")
        data_info["error_message"] = str(ve)
        return data_info # Return early
    except ImportError as ie: # Catch missing library errors
         logger.print_error(f"Missing library for mode '{args.mode}': {ie}")
         data_info["error_message"] = f"Missing library for {args.mode}: {ie}"; return data_info
    except Exception as e: # Catch unexpected errors during setup/logic
        logger.print_error(f"An unexpected error occurred during data acquisition setup for mode '{args.mode}': {e}")
        logger.print_error(f"Traceback:\n{traceback.format_exc()}")
        data_info["error_message"] = f"Setup error: {e}"
        # Ensure df is None and metrics reflect potential fetch attempts
        df = None
        metrics = combined_metrics if combined_metrics else {}
        metrics["error_message"] = data_info["error_message"]


    # --- Final Update of data_info ---
    data_info["ohlcv_df"] = df
    # Merge combined metrics from fetches
    if isinstance(combined_metrics, dict):
        if "total_latency_sec" in combined_metrics: data_info["api_latency_sec"] = combined_metrics["total_latency_sec"]
        if "api_calls" in combined_metrics: data_info["api_calls"] = combined_metrics["api_calls"]
        if "successful_chunks" in combined_metrics: data_info["successful_chunks"] = combined_metrics["successful_chunks"]
        if "rows_fetched" in combined_metrics: data_info["rows_fetched"] = combined_metrics["rows_fetched"]
        if "error_message" in combined_metrics and data_info["error_message"] is None: data_info["error_message"] = combined_metrics["error_message"]
        data_info["data_metrics"].update(combined_metrics)

    # Update metrics from file size if cache was used but no API call made
    if data_info["parquet_cache_used"] and data_info["api_calls"] == 0 and cache_filepath and cache_filepath.exists():
         try: data_info["file_size_bytes"] = cache_filepath.stat().st_size
         except Exception: pass


    if df is None: logger.print_warning("Data acquisition resulted in None DataFrame.")
    elif df.empty: logger.print_warning("Data acquisition resulted in an empty DataFrame.")
    else: logger.print_info(f"Data acquired successfully: {len(df)} rows for requested range.")

    return data_info