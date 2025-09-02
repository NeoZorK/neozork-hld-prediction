# File: src/data/data_acquisition_cache.py
# -*- coding: utf-8 -*-

"""
Cache management for data acquisition.
Handles loading, saving, and managing data cache.
All comments are in English.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from ..common.logger import print_info, print_warning, print_error, print_success


def _load_cache_if_available(cache_filepath, effective_mode: str, req_start_dt) -> tuple:
    """Load cache if available and valid."""
    if not cache_filepath or not cache_filepath.exists():
        return None, {"parquet_cache_used": False}
    
    # For exrate without dates (free plan), skip cache loading
    if effective_mode == 'exrate' and req_start_dt is None:
        print_info("Exrate free plan mode: Skipping cache, fetching current data")
        return None, {"parquet_cache_used": False}
    
    print_info(f"Found existing API cache file: {cache_filepath}")
    
    try:
        cached_df = pd.read_parquet(cache_filepath)
        if not isinstance(cached_df.index, pd.DatetimeIndex) or cached_df.empty:
            print_warning("Cache file invalid. Ignoring cache.")
            return None, {"parquet_cache_used": False}
        
        if cached_df.index.tz is not None:
            cached_df.index = cached_df.index.tz_localize(None)
        
        cache_start_dt = cached_df.index.min()
        cache_end_dt = cached_df.index.max()
        
        print_success(f"Loaded {len(cached_df)} rows from cache ({cache_start_dt} to {cache_end_dt}).")
        
        cache_info = {
            "parquet_cache_used": True,
            "cache_start_dt": cache_start_dt,
            "cache_end_dt": cache_end_dt,
            "file_size_bytes": cache_filepath.stat().st_size if cache_filepath.exists() else None
        }
        
        return cached_df, cache_info
        
    except Exception as e:
        print_warning(f"Failed to load cache file {cache_filepath}: {e}")
        return None, {"parquet_cache_used": False}


def _save_updated_cache(combined_df: pd.DataFrame, cache_filepath, effective_mode: str) -> None:
    """Save updated data to cache file."""
    if not cache_filepath:
        return
    
    print_info(f"Attempting to save/overwrite API cache file: {cache_filepath}")
    
    try:
        import os
        os.makedirs(cache_filepath.parent, exist_ok=True)
        
        if combined_df.index.tz is not None:
            combined_df.index = combined_df.index.tz_localize(None)
        
        combined_df.to_parquet(cache_filepath, index=True, engine='pyarrow')
        print_success(f"Successfully saved/updated API cache file: {cache_filepath}")
        
    except ImportError:
        print_error("Failed to save Parquet: pyarrow not installed.")
    except Exception as e:
        print_error(f"Failed to save updated API cache file {cache_filepath}: {e}")


def _combine_data(cached_df, new_data_list: list) -> pd.DataFrame:
    """Combine cached and new data."""
    all_dfs = ([cached_df] if cached_df is not None else []) + new_data_list
    
    if not all_dfs:
        return None
    
    print_info(f"Combining {len(all_dfs)} DataFrame(s)...")
    
    try:
        combined_df = pd.concat(all_dfs)
        if not isinstance(combined_df.index, pd.DatetimeIndex):
            raise TypeError("Index type error after concat")
        
        if combined_df.index.tz is not None:
            combined_df.index = combined_df.index.tz_localize(None)
        
        combined_df.sort_index(inplace=True)
        
        rows_before_dedup = len(combined_df)
        combined_df = combined_df[~combined_df.index.duplicated(keep='first')]
        rows_after_dedup = len(combined_df)
        
        if rows_before_dedup > rows_after_dedup:
            from ..common.logger import print_debug
            print_debug(f"Removed {rows_before_dedup - rows_after_dedup} duplicate rows after combining.")
        
        print_info(f"Combined data has {rows_after_dedup} unique rows.")
        return combined_df
        
    except Exception as e:
        print_error(f"Error combining data: {e}")
        raise
