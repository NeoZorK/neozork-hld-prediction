# File: src/data/data_acquisition.py
# -*- coding: utf-8 -*-

"""
Handles the overall data acquisition process by dispatching to specific fetchers based on mode.
Checks for existing single Parquet cache_manager file per instrument and fetches only missing data.
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
# Use relative import for logger functions
from ..common.logger import print_info, print_warning, print_error, print_debug, print_success  # Added print_success


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
    if effective_mode not in ['yfinance', 'polygon', 'binance'] or not args.ticker:
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
    CSV data uses a separate cache_manager mechanism within fetch_csv_data.

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

        elif effective_mode in ['yfinance', 'polygon', 'binance']:
            is_period_request = effective_mode == 'yfinance' and args.period
            cache_start_dt = None;
            cache_end_dt = None;
            req_end_dt_input = None

            if not is_period_request:
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
                print_info(f"Found existing API cache_manager file: {cache_filepath}")
                try:
                    cached_df = pd.read_parquet(cache_filepath)
                    if not isinstance(cached_df.index, pd.DatetimeIndex) or cached_df.empty:
                        print_warning("Cache file invalid. Ignoring cache_manager.")
                        cached_df = None
                    else:
                        if cached_df.index.tz is not None: cached_df.index = cached_df.index.tz_localize(None)
                        cache_start_dt = cached_df.index.min();
                        cache_end_dt = cached_df.index.max()
                        print_success(f"Loaded {len(cached_df)} rows from cache_manager ({cache_start_dt} to {cache_end_dt}).")
                        data_info["parquet_cache_used"] = True;
                        cache_load_success = True
                        try:
                            data_info["file_size_bytes"] = cache_filepath.stat().st_size
                        except Exception:
                            pass
                except Exception as e:
                    print_warning(f"Failed to load cache_manager file {cache_filepath}: {e}")
                    cached_df = None;
                    cache_load_success = False;
                    data_info["parquet_cache_used"] = False

            if not is_period_request:
                interval_delta = _get_interval_delta(args.interval)
                if not req_start_dt: raise ValueError("Start date is required for cacheable API modes.")

                if cache_load_success and interval_delta and cache_start_dt and cache_end_dt:
                    if req_start_dt < cache_start_dt:
                        # Inclusive end timestamp for this fetch range
                        fetch_before_end = cache_start_dt - interval_delta
                        if fetch_before_end >= req_start_dt:
                            fetch_ranges.append((req_start_dt, fetch_before_end, cache_start_dt))
                    if req_end_dt_inclusive > cache_end_dt:
                        # Inclusive start timestamp for this fetch range
                        fetch_after_start = cache_end_dt + interval_delta
                        if fetch_after_start <= req_end_dt_inclusive:
                            # End timestamp is the overall required inclusive end
                            fetch_ranges.append((fetch_after_start, req_end_dt_inclusive, None))
                    if not fetch_ranges:
                        print_info("Requested range is fully covered by cache_manager.")
                    else:
                        print_info(f"Found {len(fetch_ranges)} missing range(s) to fetch.")
                elif not cache_load_success:
                    fetch_ranges.append((req_start_dt, req_end_dt_inclusive, None))
                    print_info(f"No cache_manager found/usable. Fetching full range: {args.start} to {args.end}")
                elif not interval_delta:
                    print_warning("Could not determine interval delta, cannot fetch partial data. Using cache_manager only.")

            new_data_list = [];
            fetch_failed = False
            temp_metrics = {}

            if fetch_ranges:
                data_info["data_source_label"] = args.ticker
                for fetch_range_data in fetch_ranges:
                    fetch_start, fetch_end, signal_cache_start = fetch_range_data  # fetch_end is the last timestamp to INCLUDE
                    fetch_start_str = fetch_start.strftime('%Y-%m-%d')
                    fetch_end_str = ""  # Initialize

                    # Calculate the API end date string (needs to be exclusive / day after last included)
                    if signal_cache_start is not None:  # Fetching BEFORE cache_manager
                        # API call end date should be the day the cache_manager starts (exclusive)
                        fetch_end_api_call_dt = signal_cache_start.normalize()  # Start of the day cache_manager begins
                        fetch_end_str = fetch_end_api_call_dt.strftime('%Y-%m-%d')
                    else:  # Fetching AFTER cache_manager or FULL range
                        # --- CORRECTED LOGIC ---
                        # API end date needs to cover the *entire* last day included in fetch_end.
                        # Add 1 day to the last included timestamp's date for the API call end date string.
                        fetch_end_api_call_dt = fetch_end.normalize() + timedelta(days=1)
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

                    if fetch_func:
                        try:
                            # --- Refactored Fetch Call ---
                            call_kwargs = {
                                'ticker': args.ticker,
                                'interval': args.interval,
                                'start_date': fetch_start_str,
                                'end_date': fetch_end_str  # Use calculated exclusive end date string
                            }
                            if effective_mode == 'yfinance':
                                call_kwargs['period'] = None

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

                            if isinstance(metrics_part, dict):
                                for key, value in metrics_part.items():
                                    if key == "error_message" and value and "error_message" not in temp_metrics:
                                        temp_metrics["error_message"] = value
                                    elif isinstance(value, (int, float)):
                                        temp_metrics[key] = temp_metrics.get(key, 0) + value
                        except Exception as e:
                            error_msg = f"Failed fetch range {fetch_start_str}-{fetch_end_str}: {e}"
                            print_error(error_msg);
                            fetch_failed = True
                            temp_metrics["error_message"] = error_msg
                            print_error("Traceback:")
                            traceback.print_exc()
                            break
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
                print_info("Using only data from cache_manager.")
                data_info["data_source_label"] = args.ticker
            else:
                print_warning("No data fetching triggered.")

            if fetch_failed:
                final_error_msg = combined_metrics.get("error_message",
                                                       "Aborting data acquisition due to fetch failure.")
                print_error(final_error_msg)
                data_info["error_message"] = final_error_msg;
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
                except Exception as e:
                    print_error(f"Error combining data: {e}");
                    data_info["error_message"] = f"Error combining data: {e}"
                    combined_df = None;
                    raise

                    # --- Save Updated API Cache ---
            should_save = (new_data_list and not fetch_failed and cache_filepath) or \
                          (is_period_request and combined_df is not None and not combined_df.empty and cache_filepath)
            if should_save:
                print_info(f"Attempting to save/overwrite API cache_manager file: {cache_filepath}")
                try:
                    os.makedirs(cache_filepath.parent, exist_ok=True)
                    if combined_df is not None:
                        if combined_df.index.tz is not None: combined_df.index = combined_df.index.tz_localize(None)
                        combined_df.to_parquet(cache_filepath, index=True, engine='pyarrow')
                        print_success(
                            f"Successfully saved/updated API cache_manager file: {cache_filepath}")  # Use print_success
                        data_info["parquet_save_path"] = str(cache_filepath)
                    else:
                        print_warning("Combined DataFrame is None, cannot save API cache_manager.")
                except ImportError:
                    print_error("Failed to save Parquet: pyarrow not installed.")
                except Exception as e:
                    print_error(f"Failed to save updated API cache_manager file {cache_filepath}: {e}")

            # --- Return Requested Slice ---
            final_df = None
            if combined_df is not None and not is_period_request:
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