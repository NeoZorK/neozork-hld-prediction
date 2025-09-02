# File: src/data/data_acquisition_processing.py
# -*- coding: utf-8 -*-

"""
Data processing logic for data acquisition.
Handles specific processing modes and data flow.
All comments are in English.
"""

import pandas as pd
from datetime import timedelta
from typing import Dict, Tuple
from ..common.logger import print_info, print_warning, print_error, print_success
from .data_acquisition_csv import _process_csv_folder, _process_csv_single
from .data_acquisition_cache import _load_cache_if_available, _save_updated_cache, _combine_data
from .data_acquisition_ranges import _determine_fetch_ranges, _get_final_data_slice


def _process_demo_data(data_info: dict) -> dict:
    """Process demo data mode."""
    from .fetchers import get_demo_data
    
    data_info["data_source_label"] = "Demo Data"
    df = get_demo_data()
    data_info["ohlcv_df"] = df
    return data_info


def _process_csv_data(args, data_info: dict) -> dict:
    """Process CSV data mode."""
    if hasattr(args, 'csv_folder') and args.csv_folder:
        return _process_csv_folder(args, data_info)
    else:
        return _process_csv_single(args, data_info)


def _process_api_data(args, data_info: dict, effective_mode: str) -> dict:
    """Process API data modes (yfinance, polygon, binance, exrate)."""
    is_period_request = effective_mode == 'yfinance' and args.period
    
    if is_period_request:
        return _process_period_request(args, data_info, effective_mode)
    else:
        return _process_date_range_request(args, data_info, effective_mode)


def _process_period_request(args, data_info: dict, effective_mode: str) -> dict:
    """Process period-based requests (yfinance only)."""
    from .fetchers import fetch_yfinance_data
    
    data_info["data_source_label"] = args.ticker
    print_info(f"Fetching yfinance data using period '{args.period}'.")
    
    fetched_period_df, metrics_period = fetch_yfinance_data(
        ticker=args.ticker, interval=args.interval, period=args.period,
        start_date=None, end_date=None
    )
    
    if fetched_period_df is not None and not fetched_period_df.empty:
        if isinstance(fetched_period_df.index, pd.DatetimeIndex):
            if fetched_period_df.index.tz is not None:
                fetched_period_df.index = fetched_period_df.index.tz_localize(None)
        data_info["ohlcv_df"] = fetched_period_df
        data_info["data_metrics"].update(metrics_period or {})
    else:
        data_info["ohlcv_df"] = pd.DataFrame()
    
    return data_info


def _process_date_range_request(args, data_info: dict, effective_mode: str) -> dict:
    """Process date range-based requests."""
    try:
        # Parse dates
        req_start_dt, req_end_dt_inclusive = _parse_date_range(args, effective_mode)
        
        # Generate cache filepath
        from .data_acquisition_utils import _generate_instrument_parquet_filename
        cache_filepath = _generate_instrument_parquet_filename(args)
        data_info["parquet_cache_file"] = str(cache_filepath) if cache_filepath else None
        
        # Load cache if available
        cached_df, cache_info = _load_cache_if_available(cache_filepath, effective_mode, req_start_dt)
        data_info.update(cache_info)
        
        # Determine fetch ranges
        fetch_ranges = _determine_fetch_ranges(
            req_start_dt, req_end_dt_inclusive, cache_info, args.interval
        )
        
        # Fetch new data
        new_data_list, fetch_metrics = _fetch_new_data(
            args, effective_mode, fetch_ranges, req_start_dt
        )
        
        # Combine data
        combined_df = _combine_data(cached_df, new_data_list)
        
        # Save updated cache
        if combined_df is not None and not combined_df.empty:
            _save_updated_cache(combined_df, cache_filepath, effective_mode)
        
        # Return final slice
        final_df = _get_final_data_slice(
            combined_df, req_start_dt, req_end_dt_inclusive, effective_mode, args
        )
        
        data_info["ohlcv_df"] = final_df
        data_info["data_metrics"].update(fetch_metrics)
        
        return data_info
        
    except Exception as e:
        print_error(f"Error processing date range request: {e}")
        data_info["error_message"] = str(e)
        return data_info


def _parse_date_range(args, effective_mode: str) -> tuple:
    """Parse start and end dates from arguments."""
    if effective_mode == 'exrate':
        # For exrate, dates are optional
        has_dates = hasattr(args, 'start') and hasattr(args, 'end') and args.start and args.end
        
        if has_dates:
            try:
                req_start_dt = pd.to_datetime(args.start, errors='raise').tz_localize(None)
                req_end_dt_input = pd.to_datetime(args.end, errors='raise').tz_localize(None)
                req_end_dt_api_buffer = req_end_dt_input + timedelta(days=1)
                req_end_dt_inclusive = req_end_dt_api_buffer - timedelta(milliseconds=1)
                
                if req_start_dt >= req_end_dt_api_buffer:
                    raise ValueError("Start date must be before end date.")
                    
                return req_start_dt, req_end_dt_inclusive
            except Exception as date_err:
                raise ValueError(f"Invalid start/end date format or range: {date_err}") from date_err
        else:
            # Free plan: no dates needed
            return None, None
    else:
        # Other modes require dates
        try:
            req_start_dt = pd.to_datetime(args.start, errors='raise').tz_localize(None)
            req_end_dt_input = pd.to_datetime(args.end, errors='raise').tz_localize(None)
            req_end_dt_api_buffer = req_end_dt_input + timedelta(days=1)
            req_end_dt_inclusive = req_end_dt_api_buffer - timedelta(milliseconds=1)
            
            if req_start_dt >= req_end_dt_api_buffer:
                raise ValueError("Start date must be before end date.")
                
            return req_start_dt, req_end_dt_inclusive
        except Exception as date_err:
            raise ValueError(f"Invalid start/end date format or range: {date_err}") from date_err


def _fetch_new_data(args, effective_mode: str, fetch_ranges: list, req_start_dt) -> tuple:
    """Fetch new data for the specified ranges."""
    new_data_list = []
    fetch_metrics = {}
    
    # Special case for exrate free plan
    if effective_mode == 'exrate' and req_start_dt is None:
        return _fetch_exrate_current_data(args, new_data_list, fetch_metrics)
    
    if not fetch_ranges:
        return new_data_list, fetch_metrics
    
    # Fetch data for each range
    for fetch_range_data in fetch_ranges:
        fetch_start, fetch_end, signal_cache_start = fetch_range_data
        
        # Calculate API call dates
        fetch_start_str = fetch_start.strftime('%Y-%m-%d')
        if signal_cache_start is not None:
            fetch_end_api_call_dt = signal_cache_start.normalize()
            fetch_end_str = fetch_end_api_call_dt.strftime('%Y-%m-%d')
        else:
            fetch_end_api_call_dt = fetch_end.normalize() + timedelta(days=1)
            fetch_end_str = fetch_end_api_call_dt.strftime('%Y-%m-%d')
        
        print_info(
            f"Fetching range: {fetch_start.strftime('%Y-%m-%d %H:%M:%S')} to "
            f"{fetch_end.strftime('%Y-%m-%d %H:%M:%S')} from {effective_mode}... "
            f"(API Call: {fetch_start_str} to {fetch_end_str})"
        )
        
        # Fetch data
        new_df_part, metrics_part = _fetch_single_range(
            args, effective_mode, fetch_start_str, fetch_end_str
        )
        
        if new_df_part is not None and not new_df_part.empty:
            if isinstance(new_df_part.index, pd.DatetimeIndex):
                if new_df_part.index.tz is not None:
                    new_df_part.index = new_df_part.index.tz_localize(None)
            new_data_list.append(new_df_part)
            print_success(f"Fetched {len(new_df_part)} new rows.")
        else:
            print_warning(f"No data returned for range {fetch_start_str} to {fetch_end_str}.")
        
        # Update metrics
        if isinstance(metrics_part, dict):
            for key, value in metrics_part.items():
                if key == "error_message" and value and "error_message" not in fetch_metrics:
                    fetch_metrics["error_message"] = value
                elif isinstance(value, (int, float)):
                    fetch_metrics[key] = fetch_metrics.get(key, 0) + value
    
    return new_data_list, fetch_metrics


def _fetch_exrate_current_data(args, new_data_list: list, fetch_metrics: dict) -> tuple:
    """Fetch current exchange rate data for free plan."""
    from .fetchers import fetch_exrate_data
    
    print_info("Fetching current exchange rate data...")
    
    try:
        new_df_part, metrics_part = fetch_exrate_data(
            ticker=args.ticker,
            interval=args.interval,
            start_date=None,
            end_date=None
        )
        
        if new_df_part is not None and not new_df_part.empty:
            if isinstance(new_df_part.index, pd.DatetimeIndex):
                if new_df_part.index.tz is not None:
                    new_df_part.index = new_df_part.index.tz_localize(None)
            new_data_list.append(new_df_part)
            print_success(f"Fetched {len(new_df_part)} current exchange rate.")
            fetch_metrics.update(metrics_part)
        else:
            print_warning("No current exchange rate data returned.")
            fetch_metrics.update(metrics_part)
            
    except Exception as e:
        print_error(f"Failed to fetch current exchange rate: {e}")
        fetch_metrics["error_message"] = str(e)
    
    return new_data_list, fetch_metrics


def _fetch_single_range(args, effective_mode: str, fetch_start_str: str, fetch_end_str: str) -> tuple:
    """Fetch data for a single time range."""
    from .fetchers import (
        fetch_yfinance_data, fetch_polygon_data, 
        fetch_binance_data, fetch_exrate_data
    )
    
    fetch_func = None
    if effective_mode == 'yfinance':
        fetch_func = fetch_yfinance_data
    elif effective_mode == 'polygon':
        fetch_func = fetch_polygon_data
    elif effective_mode == 'binance':
        fetch_func = fetch_binance_data
    elif effective_mode == 'exrate':
        fetch_func = fetch_exrate_data
    
    if not fetch_func:
        print_error(f"Internal error: No fetch function defined for mode {effective_mode}")
        return None, {"error_message": f"No fetch function for mode {effective_mode}"}
    
    try:
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
            if hasattr(args, 'start') and args.start and hasattr(args, 'end') and args.end:
                call_kwargs['start_date'] = fetch_start_str
                call_kwargs['end_date'] = fetch_end_str
            else:
                call_kwargs['start_date'] = None
                call_kwargs['end_date'] = None
        else:
            # polygon, binance require dates
            call_kwargs['start_date'] = fetch_start_str
            call_kwargs['end_date'] = fetch_end_str
        
        return fetch_func(**call_kwargs)
        
    except Exception as e:
        error_msg = f"Failed fetch range {fetch_start_str}-{fetch_end_str}: {e}"
        print_error(error_msg)
        print_error("Traceback:")
        import traceback
        traceback.print_exc()
        return None, {"error_message": error_msg}
