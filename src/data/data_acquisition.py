# File: src/data/data_acquisition.py
# -*- coding: utf-8 -*-

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
from typing import List, Tuple

# Use relative imports for fetchers within the same package
from .fetchers import (
    fetch_csv_data, fetch_yfinance_data, fetch_polygon_data,
    fetch_binance_data, get_demo_data, fetch_exrate_data
)
# Use relative import for logger functions
from ..common.logger import print_info, print_warning, print_error, print_debug, print_success  # Added print_success


# Helper function to detect gaps in full requested range (including missing data outside cache)
def _detect_full_range_gaps(cached_df: pd.DataFrame, req_start_dt: pd.Timestamp, req_end_dt: pd.Timestamp, 
                           cache_start_dt: pd.Timestamp, cache_end_dt: pd.Timestamp, 
                           interval_delta: pd.Timedelta) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
    """
    Detect gaps in the full requested range, including missing data outside the cache.
    Returns a list of (gap_start, gap_end) tuples.
    """
    gaps = []
    
    # Check for gaps before cache starts
    if req_start_dt < cache_start_dt:
        gap_start = req_start_dt
        gap_end = cache_start_dt - interval_delta
        if gap_end > gap_start:
            gaps.append((gap_start, gap_end))
            print_debug(f"Gap before cache: {gap_start} to {gap_end} (duration: {gap_end - gap_start})")
    
    # Check for gaps after cache ends
    if req_end_dt > cache_end_dt:
        gap_start = cache_end_dt + interval_delta
        gap_end = req_end_dt
        if gap_end > gap_start:
            gaps.append((gap_start, gap_end))
            print_debug(f"Gap after cache: {gap_start} to {gap_end} (duration: {gap_end - gap_start})")
    
    # Check for gaps within cache (if cache exists)
    if cached_df is not None and not cached_df.empty:
        cache_gaps = _detect_data_gaps(cached_df, cache_start_dt, cache_end_dt, interval_delta)
        for gap_start, gap_end in cache_gaps:
            # Only include gaps that overlap with requested range
            if gap_start <= req_end_dt and gap_end >= req_start_dt:
                # Adjust gap boundaries to fit within requested range
                adjusted_start = max(gap_start, req_start_dt)
                adjusted_end = min(gap_end, req_end_dt)
                if adjusted_end > adjusted_start:
                    gaps.append((adjusted_start, adjusted_end))
    
    return gaps

# Helper function to detect gaps in cached data
def _detect_data_gaps(df: pd.DataFrame, start_dt: pd.Timestamp, end_dt: pd.Timestamp, interval_delta: pd.Timedelta) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
    """
    Detect gaps in cached data within the requested range.
    Returns a list of (gap_start, gap_end) tuples.
    """
    gaps = []
    
    # Filter data to the requested range
    filtered_df = df[(df.index >= start_dt) & (df.index <= end_dt)]
    
    if len(filtered_df) < 2:
        return gaps
    
    # Calculate expected time differences
    time_diffs = filtered_df.index.to_series().diff()
    
    # Define what constitutes a gap (more than 1.5x the expected interval for M15)
    # This will catch gaps of 30+ minutes for M15 data
    gap_threshold = interval_delta * 1.5
    
    # Find gaps
    gap_indices = time_diffs[time_diffs > gap_threshold]
    
    for timestamp, diff in gap_indices.items():
        # Calculate gap start and end
        gap_start = timestamp - diff + interval_delta
        gap_end = timestamp - interval_delta
        
        # Only include gaps that are within our requested range
        if gap_start >= start_dt and gap_end <= end_dt and gap_end > gap_start:
            gaps.append((gap_start, gap_end))
            print_debug(f"Gap detected: {gap_start} to {gap_end} (duration: {diff})")
    
    # Also check for large gaps that might span multiple days
    # This is a more aggressive check for major data gaps
    if len(filtered_df) > 0:
        # Check if we have data for each month in the range
        current_date = start_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = end_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        while current_date <= end_date:
            month_start = current_date
            month_end = (current_date + pd.DateOffset(months=1)) - pd.Timedelta(minutes=15)
            
            # Check if we have data for this month
            month_data = filtered_df[(filtered_df.index >= month_start) & (filtered_df.index <= month_end)]
            
            # If we have very little data for a month (less than 10% of expected), consider it a gap
            expected_rows_per_month = (month_end - month_start).total_seconds() / (interval_delta.total_seconds())
            if len(month_data) < expected_rows_per_month * 0.1:
                if len(month_data) > 0:
                    # Find the actual data range in this month
                    actual_start = month_data.index.min()
                    actual_end = month_data.index.max()
                    
                    # Check for gaps before and after the actual data
                    if actual_start > month_start + interval_delta:
                        gap_start = month_start
                        gap_end = actual_start - interval_delta
                        if gap_end > gap_start:
                            gaps.append((gap_start, gap_end))
                            print_debug(f"Large gap detected: {gap_start} to {gap_end} (month: {current_date.strftime('%Y-%m')})")
                    
                    if actual_end < month_end - interval_delta:
                        gap_start = actual_end + interval_delta
                        gap_end = month_end
                        if gap_end > gap_start:
                            gaps.append((gap_start, gap_end))
                            print_debug(f"Large gap detected: {gap_start} to {gap_end} (month: {current_date.strftime('%Y-%m')})")
                else:
                    # No data at all for this month - add the entire month as a gap
                    gap_start = month_start
                    gap_end = month_end
                    if gap_end > gap_start:
                        gaps.append((gap_start, gap_end))
                        print_debug(f"Complete month gap detected: {gap_start} to {gap_end} (month: {current_date.strftime('%Y-%m')})")
            
            current_date += pd.DateOffset(months=1)
    
    return gaps

# Helper function to get interval delta
def _get_interval_delta(interval_str: str) -> pd.Timedelta | None:
    """
    Converts common interval strings (e.g., 'h1', 'D1', 'M1', 'W') to pandas Timedelta.
    Handles common variations and logs a warning for unparseable intervals.
    """
    try:
        delta = pd.Timedelta(interval_str)
        if delta.total_seconds() > 0: return delta
    except ValueError:
        pass

    simple_map = {
        'M1': '1min', 'M5': '5min', 'M15': '15min', 'M30': '30min',
        'H1': '1h', 'h1': '1h', 'H4': '4h',
        'D1': '1d', 'D': '1d', 'W': '7d', 'W1': '7d', 'WK': '7d',
        'MN': '30d', 'MN1': '30d', 'MO': '30d'
    }
    pd_freq = simple_map.get(str(interval_str).upper())
    if pd_freq:
        try:
            delta = pd.Timedelta(pd_freq)
            if delta.total_seconds() > 0: return delta
        except ValueError:
            pass

    print_warning(f"Could not parse interval '{interval_str}' to Timedelta. Cache delta logic may be affected.")
    return None


# Helper function for Parquet filename
def _generate_instrument_parquet_filename(args) -> Path | None:
    """Generates the expected instrument-specific parquet filename (no dates)."""
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode
    if effective_mode not in ['yfinance', 'polygon', 'binance', 'exrate'] or not args.ticker:
        return None
    parquet_dir = Path("data/raw_parquet")
    try:
        ticker_label = str(args.ticker).replace('/', '_').replace('-', '_').replace('=', '_').replace(':', '_')
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
    Uses a single Parquet file per instrument for caching API data, fetching only missing data.
    CSV data uses a separate cache mechanism within fetch_csv_data.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        dict: A dictionary containing the DataFrame ('ohlcv_df') and acquisition metrics.
              Returns dict with 'error_message' on failure.
    """
    dotenv_path = '.env';
    load_dotenv(dotenv_path=dotenv_path)
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    data_info = {
        "ohlcv_df": None, "ticker": args.ticker, "interval": args.interval,
        "data_source_label": "N/A", "effective_mode": effective_mode,
        "yf_ticker": None, "yf_interval": None, "current_period": args.period,
        "current_start": args.start, "current_end": args.end,
        "file_size_bytes": None, "api_latency_sec": 0.0,
        "api_calls": 0, "successful_chunks": 0, "rows_fetched": 0,
        "error_message": None, "data_metrics": {}, "parquet_cache_used": False,
        "parquet_cache_file": None, "steps_duration": {}
    }
    print_info(f"--- Step 1: Acquiring Data (Mode: {effective_mode.capitalize()}) ---")

    df = None;
    metrics = {};
    cached_df = None;
    cache_filepath = None
    fetch_ranges = [];
    req_start_dt = None;
    req_end_dt_inclusive = None
    combined_metrics = {}

    try:
        if effective_mode == 'demo':
            data_info["data_source_label"] = "Demo Data";
            df = get_demo_data();
            combined_metrics = {}
            data_info["ohlcv_df"] = df;
            return data_info

        elif effective_mode == 'csv':
            # Handle single CSV file
            if args.csv_file:
                data_info["data_source_label"] = args.csv_file
                csv_column_mapping = {
                    'Open': 'Open,', 'High': 'High,', 'Low': 'Low,',
                    'Close': 'Close,', 'Volume': 'TickVolume,'
                }
                csv_datetime_column = 'DateTime,'
                df = fetch_csv_data(
                    file_path=args.csv_file, ohlc_columns=csv_column_mapping,
                    datetime_column=csv_datetime_column, skiprows=1, separator=','
                )
                if df is None or df.empty:
                    error_msg = f"Failed to read or process CSV file: {args.csv_file}. Check logs for details."
                    raise ValueError(error_msg)
                if args.csv_file and Path(args.csv_file).exists():
                    try:
                        combined_metrics["file_size_bytes"] = Path(args.csv_file).stat().st_size
                    except Exception:
                        pass
                combined_metrics["api_latency_sec"] = 0.0;
                combined_metrics["api_calls"] = 0
                data_info["ohlcv_df"] = df
            
            # Handle CSV folder batch processing
            elif args.csv_folder:
                from .batch_csv_processor import process_csv_folder
                data_info["data_source_label"] = f"Batch CSV folder: {args.csv_folder}"
                
                # Process the entire folder
                batch_results = process_csv_folder(args)
                
                # Update data_info with batch processing results
                data_info.update(batch_results)
                
                # For batch processing, we don't return a single DataFrame
                # Instead, we indicate that this was a batch operation
                data_info["batch_processing"] = True
                data_info["ohlcv_df"] = None  # No single DataFrame for batch processing
                
                # Set success based on batch results
                if not batch_results["success"]:
                    error_msg = f"Batch CSV processing failed. {len(batch_results['error_messages'])} errors occurred."
                    raise ValueError(error_msg)

        elif effective_mode in ['yfinance', 'polygon', 'binance', 'exrate']:
            is_period_request = effective_mode == 'yfinance' and args.period
            cache_start_dt = None;
            cache_end_dt = None;
            req_end_dt_input = None

            # Special handling for exrate mode: dates are optional
            if effective_mode == 'exrate':
                # For exrate, start/end dates are optional (free plan = current only, paid plan = historical)
                has_dates = hasattr(args, 'start') and hasattr(args, 'end') and args.start and args.end
                is_period_request = False  # Exrate doesn't use period
                
                if has_dates:
                    try:
                        req_start_dt = pd.to_datetime(args.start, errors='raise').tz_localize(None)
                        req_end_dt_input = pd.to_datetime(args.end, errors='raise').tz_localize(None)
                        # Calculate the end timestamp for API calls (usually needs day after)
                        req_end_dt_api_buffer = req_end_dt_input + timedelta(days=1)
                        # Calculate the actual last timestamp needed (inclusive) for internal checks
                        req_end_dt_inclusive = req_end_dt_api_buffer - timedelta(milliseconds=1)
                        if req_start_dt >= req_end_dt_api_buffer: raise ValueError("Start date must be before end date.")
                    except Exception as date_err:
                        raise ValueError(f"Invalid start/end date format or range: {date_err}") from date_err
                else:
                    # Free plan: no dates needed, will fetch current data
                    req_start_dt, req_end_dt_inclusive = None, None
            elif not is_period_request:
                try:
                    req_start_dt = pd.to_datetime(args.start, errors='raise').tz_localize(None)
                    req_end_dt_input = pd.to_datetime(args.end, errors='raise').tz_localize(None)
                    # Calculate the end timestamp for API calls (usually needs day after)
                    req_end_dt_api_buffer = req_end_dt_input + timedelta(days=1)
                    # Calculate the actual last timestamp needed (inclusive) for internal checks
                    req_end_dt_inclusive = req_end_dt_api_buffer - timedelta(milliseconds=1)
                    if req_start_dt >= req_end_dt_api_buffer: raise ValueError("Start date must be before end date.")
                except Exception as date_err:
                    raise ValueError(f"Invalid start/end date format or range: {date_err}") from date_err
            else:
                req_start_dt, req_end_dt_inclusive = None, None

            cache_filepath = _generate_instrument_parquet_filename(args)
            data_info["parquet_cache_file"] = str(cache_filepath) if cache_filepath else None
            cache_load_success = False

            if cache_filepath and cache_filepath.exists() and not is_period_request:
                # For exrate without dates (free plan), skip cache loading as we always want current data
                if effective_mode == 'exrate' and req_start_dt is None:
                    print_info("Exrate free plan mode: Skipping cache, fetching current data")
                    cached_df = None
                    cache_load_success = False
                else:
                    print_info(f"Found existing API cache file: {cache_filepath}")
                    try:
                        cached_df = pd.read_parquet(cache_filepath)
                        if not isinstance(cached_df.index, pd.DatetimeIndex) or cached_df.empty:
                            print_warning("Cache file invalid. Ignoring cache.")
                            cached_df = None
                        else:
                            if cached_df.index.tz is not None: cached_df.index = cached_df.index.tz_localize(None)
                            cache_start_dt = cached_df.index.min();
                            cache_end_dt = cached_df.index.max()
                            print_success(f"Loaded {len(cached_df)} rows from cache ({cache_start_dt} to {cache_end_dt}).")
                            data_info["parquet_cache_used"] = True;
                            cache_load_success = True
                            try:
                                data_info["file_size_bytes"] = cache_filepath.stat().st_size
                            except Exception:
                                pass
                    except Exception as e:
                        print_warning(f"Failed to load cache file {cache_filepath}: {e}")
                        cached_df = None;
                        cache_load_success = False;
                        data_info["parquet_cache_used"] = False

            if not is_period_request:
                interval_delta = _get_interval_delta(args.interval)
                # Special handling for exrate without dates (free plan)
                if effective_mode == 'exrate' and req_start_dt is None:
                    # For free plan exrate, we don't need date validation or cache checking
                    pass
                elif not req_start_dt:
                    raise ValueError("Start date is required for cacheable API modes.")

                if cache_load_success and interval_delta and cache_start_dt and cache_end_dt:
                    # Check for future dates - allow fetching up to requested date
                    current_time = pd.Timestamp.now(tz='UTC').tz_localize(None)
                    if req_start_dt > current_time:
                        print_warning(f"Requested start date {req_start_dt} is in the future. No data available.")
                        fetch_ranges = []  # No need to fetch future data
                    elif req_end_dt_inclusive > current_time:
                        print_info(f"Requested end date {req_end_dt_inclusive} is in the future. Will attempt to fetch up to requested date.")
                        # Keep the requested end date for gap detection, but limit actual API calls to current time
                        # This allows gap detection to work properly for the full requested range
                        # The actual API calls will be limited by the fetcher functions
                    
                    # Check for gaps in the full requested range (including missing data outside cache)
                    if cached_df is not None and not cached_df.empty:
                        print_info("Checking for gaps in full requested range...")
                        # Use the new function to detect gaps in the full range
                        all_gaps = _detect_full_range_gaps(cached_df, req_start_dt, req_end_dt_inclusive, 
                                                         cache_start_dt, cache_end_dt, interval_delta)
                        
                        if all_gaps:
                            print_info(f"Found {len(all_gaps)} gaps in full requested range. Will fetch missing data.")
                            # Add gap ranges to fetch_ranges
                            for gap_start, gap_end in all_gaps:
                                fetch_ranges.append((gap_start, gap_end, None))
                        else:
                            print_info("No significant gaps found in full requested range.")
                    else:
                        # No cache available, will fetch full range
                        print_info("No cache available, will fetch full requested range.")
                    
                    # Special handling for future dates: if requested end date is in the future,
                    # we need to check if we have data up to current time and mark the remaining
                    # period as a gap that will be filled when data becomes available
                    if req_end_dt_inclusive > current_time:
                        print_info(f"Requested end date {req_end_dt_inclusive} is in the future.")
                        print_info("Will fetch available data up to current time and note the remaining gap.")
                        # The gap detection above should have already identified this gap
                    
                    # Note: Gap detection and range fetching is now handled by _detect_full_range_gaps above
                    if not fetch_ranges:
                        print_info("Requested range is fully covered by cache.")
                    else:
                        print_info(f"Found {len(fetch_ranges)} missing range(s) to fetch.")
                elif not cache_load_success:
                    fetch_ranges.append((req_start_dt, req_end_dt_inclusive, None))
                    print_info(f"No cache found/usable. Fetching full range: {args.start} to {args.end}")
                elif not interval_delta:
                    print_warning("Could not determine interval delta, cannot fetch partial data. Using cache only.")

            new_data_list = [];
            fetch_failed = False
            temp_metrics = {}

            # Special case for exrate free plan: always fetch current data even without ranges
            if effective_mode == 'exrate' and req_start_dt is None:
                data_info["data_source_label"] = args.ticker
                print_info("Fetching current exchange rate data...")
                
                fetch_func = fetch_exrate_data
                try:
                    call_kwargs = {
                        'ticker': args.ticker,
                        'interval': args.interval,
                        'start_date': None,
                        'end_date': None
                    }
                    
                    new_df_part, metrics_part = fetch_func(**call_kwargs)
                    
                    if new_df_part is not None and not new_df_part.empty:
                        if isinstance(new_df_part.index, pd.DatetimeIndex):
                            if new_df_part.index.tz is not None:
                                new_df_part.index = new_df_part.index.tz_localize(None)
                        new_data_list.append(new_df_part);
                        print_success(f"Fetched {len(new_df_part)} current exchange rate.")
                        temp_metrics.update(metrics_part)
                    else:
                        print_warning("No current exchange rate data returned.")
                        fetch_failed = True
                        temp_metrics.update(metrics_part)
                except Exception as e:
                    print_error(f"Failed to fetch current exchange rate: {e}")
                    fetch_failed = True
                    temp_metrics["error_message"] = str(e)
            elif fetch_ranges:
                data_info["data_source_label"] = args.ticker
                for fetch_range_data in fetch_ranges:
                    fetch_start, fetch_end, signal_cache_start = fetch_range_data  # fetch_end is the last timestamp to INCLUDE
                    fetch_start_str = fetch_start.strftime('%Y-%m-%d')
                    fetch_end_str = ""  # Initialize

                    # Calculate the API end date string (needs to be exclusive / day after last included)
                    if signal_cache_start is not None:  # Fetching BEFORE cache
                        # API call end date should be the day the cache starts (exclusive)
                        fetch_end_api_call_dt = signal_cache_start.normalize()  # Start of the day cache begins
                        fetch_end_str = fetch_end_api_call_dt.strftime('%Y-%m-%d')
                    else:  # Fetching AFTER cache or FULL range
                        # --- CORRECTED LOGIC ---
                        # API end date needs to cover the *entire* last day included in fetch_end.
                        # Add 1 day to the last included timestamp's date for the API call end date string.
                        fetch_end_api_call_dt = fetch_end.normalize() + timedelta(days=1)
                        # Allow fetching up to requested date, even if it's in the future
                        # The actual API fetcher will handle the limitation to current time if needed
                        fetch_end_str = fetch_end_api_call_dt.strftime('%Y-%m-%d')
                        # --- END CORRECTION ---

                    # Log the actual inclusive range and the API call range
                    print_info(
                        f"Fetching range: {fetch_start.strftime('%Y-%m-%d %H:%M:%S')} to {fetch_end.strftime('%Y-%m-%d %H:%M:%S')} from {effective_mode}... (API Call: {fetch_start_str} to {fetch_end_str})")

                    new_df_part = None;
                    metrics_part = {}
                    fetch_func = None
                    if effective_mode == 'yfinance':
                        fetch_func = fetch_yfinance_data
                    elif effective_mode == 'polygon':
                        fetch_func = fetch_polygon_data
                    elif effective_mode == 'binance':
                        fetch_func = fetch_binance_data
                    elif effective_mode == 'exrate':
                        fetch_func = fetch_exrate_data

                    if fetch_func:
                        try:
                            # --- Refactored Fetch Call ---
                            call_kwargs = {
                                'ticker': args.ticker,
                                'interval': args.interval,
                            }
                            
                            # Handle date parameters based on mode
                            if effective_mode == 'yfinance':
                                call_kwargs['start_date'] = fetch_start_str
                                call_kwargs['end_date'] = fetch_end_str
                                call_kwargs['period'] = None
                            elif effective_mode == 'exrate':
                                # For exrate, only pass dates if they were provided by user
                                if hasattr(args, 'start') and args.start and hasattr(args, 'end') and args.end:
                                    call_kwargs['start_date'] = fetch_start_str
                                    call_kwargs['end_date'] = fetch_end_str
                                else:
                                    # Free plan mode - current data only
                                    call_kwargs['start_date'] = None
                                    call_kwargs['end_date'] = None
                            else:
                                # polygon, binance require dates
                                call_kwargs['start_date'] = fetch_start_str
                                call_kwargs['end_date'] = fetch_end_str

                            new_df_part, metrics_part = fetch_func(**call_kwargs)
                            # --- End Refactored Fetch Call ---

                            if new_df_part is not None and not new_df_part.empty:
                                if isinstance(new_df_part.index, pd.DatetimeIndex):
                                    if new_df_part.index.tz is not None:
                                        new_df_part.index = new_df_part.index.tz_localize(None)
                                new_data_list.append(new_df_part);
                                print_success(f"Fetched {len(new_df_part)} new rows.")  # Use print_success
                            else:
                                print_warning(f"No data returned for range {fetch_start_str} to {fetch_end_str}.")
                                # Check if this is due to unavailable historical data
                                if effective_mode == 'binance':
                                    print_info("This might be because:")
                                    print_info("1. The trading pair was not available during this time period")
                                    print_info("2. The requested date range is in the future")
                                    print_info("3. The exchange was not operational during this time")
                                    # Don't treat this as a fatal error, continue with available data

                            if isinstance(metrics_part, dict):
                                for key, value in metrics_part.items():
                                    if key == "error_message" and value and "error_message" not in temp_metrics:
                                        temp_metrics["error_message"] = value
                                    elif isinstance(value, (int, float)):
                                        temp_metrics[key] = temp_metrics.get(key, 0) + value
                        except Exception as e:
                            error_msg = f"Failed fetch range {fetch_start_str}-{fetch_end_str}: {e}"
                            print_error(error_msg);
                            # Don't break the entire process for individual range failures
                            # Just log the error and continue with other ranges
                            temp_metrics["error_message"] = error_msg
                            print_error("Traceback:")
                            traceback.print_exc()
                            # Continue with next range instead of breaking
                            continue
                    else:
                        print_error(f"Internal error: No fetch function defined for mode {effective_mode}")
                        fetch_failed = True;
                        break

                combined_metrics.update(temp_metrics)

            elif is_period_request:
                data_info["data_source_label"] = args.ticker
                print_info(f"Fetching yfinance data using period '{args.period}'.")
                fetched_period_df, metrics_period = fetch_yfinance_data(
                    ticker=args.ticker, interval=args.interval, period=args.period,
                    start_date=None, end_date=None
                )
                combined_metrics = metrics_period or {}
                cached_df = None
                if fetched_period_df is not None and not fetched_period_df.empty:
                    if isinstance(fetched_period_df.index, pd.DatetimeIndex):
                        if fetched_period_df.index.tz is not None:
                            fetched_period_df.index = fetched_period_df.index.tz_localize(None)
                    new_data_list = [fetched_period_df]
                else:
                    new_data_list = []
            elif cache_load_success:
                print_info("Using only data from cache.")
                data_info["data_source_label"] = args.ticker
            else:
                print_warning("No data fetching triggered.")

            if fetch_failed:
                final_error_msg = combined_metrics.get("error_message",
                                                       "Aborting data acquisition due to fetch failure.")
                print_error(final_error_msg)
                data_info["error_message"] = final_error_msg;
                new_data_list = []
            elif combined_metrics.get("error_message") and not new_data_list:
                # If we have error messages but no new data, it's not necessarily a failure
                # if we have cached data available
                if cached_df is not None and not cached_df.empty:
                    print_warning("Some data ranges failed to fetch, but using available cached data.")
                    data_info["error_message"] = combined_metrics.get("error_message")
                else:
                    # No cached data and no new data - this is a real failure
                    print_error("No data available from any source.")
                    data_info["error_message"] = combined_metrics.get("error_message")
                    new_data_list = []

            # --- Combine Data ---
            all_dfs = ([cached_df] if cached_df is not None else []) + new_data_list
            combined_df = None
            if all_dfs:
                print_info(f"Combining {len(all_dfs)} DataFrame(s)...")
                try:
                    combined_df = pd.concat(all_dfs)
                    if not isinstance(combined_df.index, pd.DatetimeIndex): raise TypeError(
                        "Index type error after concat")
                    if combined_df.index.tz is not None: combined_df.index = combined_df.index.tz_localize(None)
                    combined_df.sort_index(inplace=True)
                    rows_before_dedup = len(combined_df)
                    combined_df = combined_df[~combined_df.index.duplicated(keep='first')]
                    rows_after_dedup = len(combined_df)
                    if rows_before_dedup > rows_after_dedup: print_debug(
                        f"Removed {rows_before_dedup - rows_after_dedup} duplicate rows after combining.")
                    print_info(f"Combined data has {rows_after_dedup} unique rows.")
                    
                    # After combining data, check if we still have gaps for future dates
                    if req_end_dt_inclusive > current_time and combined_df is not None and not combined_df.empty:
                        current_data_end = combined_df.index.max()
                        if current_data_end < req_end_dt_inclusive:
                            remaining_gap_days = (req_end_dt_inclusive - current_data_end).days
                            print_info(f"Data loaded up to {current_data_end}. Remaining gap: {remaining_gap_days} days until {req_end_dt_inclusive}")
                            print_info("This gap will be filled when future data becomes available.")
                            
                except Exception as e:
                    print_error(f"Error combining data: {e}");
                    data_info["error_message"] = f"Error combining data: {e}"
                    combined_df = None;
                    raise

                    # --- Save Updated API Cache ---
            should_save = (new_data_list and not fetch_failed and cache_filepath) or \
                          (is_period_request and combined_df is not None and not combined_df.empty and cache_filepath)
            if should_save:
                print_info(f"Attempting to save/overwrite API cache file: {cache_filepath}")
                try:
                    os.makedirs(cache_filepath.parent, exist_ok=True)
                    if combined_df is not None:
                        if combined_df.index.tz is not None: combined_df.index = combined_df.index.tz_localize(None)
                        combined_df.to_parquet(cache_filepath, index=True, engine='pyarrow')
                        print_success(
                            f"Successfully saved/updated API cache file: {cache_filepath}")  # Use print_success
                        data_info["parquet_save_path"] = str(cache_filepath)
                    else:
                        print_warning("Combined DataFrame is None, cannot save API cache.")
                except ImportError:
                    print_error("Failed to save Parquet: pyarrow not installed.")
                except Exception as e:
                    print_error(f"Failed to save updated API cache file {cache_filepath}: {e}")

            # --- Return Requested Slice ---
            final_df = None
            if combined_df is not None and not is_period_request:
                # Special handling for exrate mode: check if historical data was requested
                if effective_mode == 'exrate':
                    if hasattr(args, 'start') and args.start and hasattr(args, 'end') and args.end:
                        print_info("Exchange Rate API: Returning historical data for requested range")
                        try:
                            slice_start = req_start_dt
                            slice_end = req_end_dt_input
                            # Perform slice using loc, which is inclusive for Timestamps
                            final_df = combined_df.loc[slice_start:slice_end].copy()
                        except Exception as e:
                            print_warning(f"Date slicing failed for exrate: {e}")
                            final_df = combined_df.copy()
                    else:
                        print_info("Exchange Rate API: Returning current exchange rate data")
                        final_df = combined_df.copy()
                else:
                    print_info(f"Filtering combined data for requested range: {args.start} to {args.end}")
                    try:
                        slice_start = req_start_dt
                        slice_end = req_end_dt_input
                        # Perform slice using loc, which is inclusive for Timestamps
                        final_df = combined_df.loc[slice_start:slice_end].copy()
                        # Check copy validity, fallback to view if needed
                        if final_df.empty and not combined_df.loc[slice_start:slice_end].empty:
                            print_warning("Copying slice resulted in empty DataFrame unexpectedly. Using view.")
                            final_df = combined_df.loc[slice_start:slice_end]

                        if final_df.empty:
                            print_warning(f"Requested range {args.start}-{args.end} resulted in empty slice.")
                        else:
                            print_info(f"Final DataFrame slice has {len(final_df)} rows.")
                    except KeyError:
                        print_warning(
                            f"Requested date range {args.start}-{args.end} not found in index. Returning empty slice.")
                        final_df = pd.DataFrame()
                    except Exception as e:
                        print_error(f"Error slicing combined DataFrame: {e}");
                        final_df = None
                        data_info["error_message"] = f"Error slicing data: {e}"
            elif combined_df is not None and is_period_request:
                final_df = combined_df

            df = final_df  # Final assignment for API modes

    except ValueError as ve:
        print_error(f"Configuration error: {ve}"); data_info["error_message"] = str(ve)
    except ImportError as ie:
        print_error(f"Missing library: {ie}"); data_info["error_message"] = str(ie); raise  # Re-raise import error
    except Exception as e:
        print_error(f"Unexpected error in acquire_data: {e}");
        print_error("Traceback:")
        traceback.print_exc()
        data_info["error_message"] = str(e)
        df = None

        # --- Final Update of data_info ---
    data_info["ohlcv_df"] = df
    if isinstance(combined_metrics, dict):
        api_latency = combined_metrics.get("total_latency_sec", combined_metrics.get("latency_sec", 0.0))
        data_info["api_latency_sec"] = api_latency if api_latency is not None else 0.0
        data_info["api_calls"] = combined_metrics.get("api_calls", 0)
        data_info["successful_chunks"] = combined_metrics.get("successful_chunks", 0)
        data_info["rows_fetched"] = combined_metrics.get("rows_fetched", 0)
        if "file_size_bytes" in combined_metrics: data_info["file_size_bytes"] = combined_metrics["file_size_bytes"]
        if "error_message" in combined_metrics and data_info["error_message"] is None:
            data_info["error_message"] = combined_metrics["error_message"]
        data_info["data_metrics"].update(combined_metrics)

    if data_info["parquet_cache_used"] and data_info.get(
            "file_size_bytes") is None and cache_filepath and cache_filepath.exists():
        try:
            data_info["file_size_bytes"] = cache_filepath.stat().st_size
        except Exception:
            pass

    if df is not None and not df.empty:
        data_info["rows_count"] = len(df)
        data_info["columns_count"] = len(df.columns)
        try:
            data_info["data_size_bytes"] = df.memory_usage(deep=True).sum()
            data_info["data_size_mb"] = data_info["data_size_bytes"] / (1024 * 1024)
        except Exception as mem_err:
            print_warning(f"Could not calculate DataFrame memory usage: {mem_err}")
            data_info["data_size_bytes"] = -1;
            data_info["data_size_mb"] = -1.0
    elif data_info.get("error_message") is None:
        print_warning("Data acquisition resulted in None or empty DataFrame.")

    print_info(
        f"Data acquisition finished. Cache used: {data_info['parquet_cache_used']}. Error: {data_info['error_message'] or 'None'}")
    return data_info