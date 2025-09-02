# File: src/data/data_acquisition_ranges.py
# -*- coding: utf-8 -*-

"""
Range determination for data acquisition.
Handles determining which data ranges need to be fetched.
All comments are in English.
"""

import pandas as pd
from datetime import timedelta
from typing import List, Tuple, Optional
from ..common.logger import print_info, print_warning


def _determine_fetch_ranges(req_start_dt, req_end_dt_inclusive, cache_info: dict, interval: str) -> list:
    """Determine which ranges need to be fetched."""
    if not cache_info.get("parquet_cache_used"):
        return [(req_start_dt, req_end_dt_inclusive, None)]
    
    from .data_acquisition_utils import _get_interval_delta
    interval_delta = _get_interval_delta(interval)
    if not interval_delta:
        print_warning("Could not determine interval delta, cannot fetch partial data. Using cache only.")
        return []
    
    cache_start_dt = cache_info.get("cache_start_dt")
    cache_end_dt = cache_info.get("cache_end_dt")
    
    if not cache_start_dt or not cache_end_dt:
        return [(req_start_dt, req_end_dt_inclusive, None)]
    
    fetch_ranges = []
    
    # Check if we need to fetch before cache
    if req_start_dt < cache_start_dt:
        fetch_before_end = cache_start_dt - interval_delta
        if fetch_before_end >= req_start_dt:
            fetch_ranges.append((req_start_dt, fetch_before_end, cache_start_dt))
    
    # Check if we need to fetch after cache
    if req_end_dt_inclusive > cache_end_dt:
        fetch_after_start = cache_end_dt + interval_delta
        if fetch_after_start <= req_end_dt_inclusive:
            fetch_ranges.append((fetch_after_start, req_end_dt_inclusive, None))
    
    if not fetch_ranges:
        print_info("Requested range is fully covered by cache.")
    else:
        print_info(f"Found {len(fetch_ranges)} missing range(s) to fetch.")
    
    return fetch_ranges


def _get_final_data_slice(combined_df: pd.DataFrame, req_start_dt, req_end_dt_inclusive, 
                          effective_mode: str, args) -> pd.DataFrame:
    """Get final data slice for the requested range."""
    if combined_df is None:
        return None
    
    # Special handling for exrate mode
    if effective_mode == 'exrate':
        if hasattr(args, 'start') and args.start and hasattr(args, 'end') and args.end:
            from ..common.logger import print_info
            print_info("Exchange Rate API: Returning historical data for requested range")
            try:
                slice_start = req_start_dt
                slice_end = req_start_dt + timedelta(days=1) - timedelta(milliseconds=1)
                final_df = combined_df.loc[slice_start:slice_end].copy()
            except Exception as e:
                from ..common.logger import print_warning
                print_warning(f"Date slicing failed for exrate: {e}")
                final_df = combined_df.copy()
        else:
            from ..common.logger import print_info
            print_info("Exchange Rate API: Returning current exchange rate data")
            final_df = combined_df.copy()
    else:
        from ..common.logger import print_info, print_warning
        print_info(f"Filtering combined data for requested range: {args.start} to {args.end}")
        try:
            slice_start = req_start_dt
            slice_end = req_start_dt + timedelta(days=1) - timedelta(milliseconds=1)
            final_df = combined_df.loc[slice_start:slice_end].copy()
            
            if final_df.empty and not combined_df.loc[slice_start:slice_end].empty:
                print_warning("Copying slice resulted in empty DataFrame unexpectedly. Using view.")
                final_df = combined_df.loc[slice_start:slice_end]
            
            if final_df.empty:
                print_warning(f"Requested range {args.start}-{args.end} resulted in empty slice.")
            else:
                print_info(f"Final DataFrame slice has {len(final_df)} rows.")
                
        except KeyError:
            print_warning(f"Requested date range {args.start}-{args.end} not found in index. Returning empty slice.")
            final_df = pd.DataFrame()
        except Exception as e:
            from ..common.logger import print_error
            print_error(f"Error slicing combined DataFrame: {e}")
            final_df = None
    
    return final_df
