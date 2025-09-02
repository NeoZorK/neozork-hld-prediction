# File: src/data/data_acquisition_utils.py
# -*- coding: utf-8 -*-

"""
Utility functions for data acquisition process.
Includes interval parsing, filename generation, and CSV processing helpers.
All comments are in English.
"""

import pandas as pd
from pathlib import Path
from ..common.logger import print_info, print_warning, print_error, print_success


def _get_interval_delta(interval_str: str) -> pd.Timedelta | None:
    """
    Converts common interval strings (e.g., 'h1', 'D1', 'M1', 'W') to pandas Timedelta.
    Handles common variations and logs a warning for unparseable intervals.
    """
    try:
        delta = pd.Timedelta(interval_str)
        if delta.total_seconds() > 0:
            return delta
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
            if delta.total_seconds() > 0:
                return delta
        except ValueError:
            pass

    print_warning(f"Could not parse interval '{interval_str}' to Timedelta. Cache delta logic may be affected.")
    return None


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


def _process_csv_folder(args, data_info: dict) -> dict:
    """Process CSV folder with multiple files."""
    from src.data.csv_folder_processor import process_csv_folder
    
    data_info["data_source_label"] = f"CSV Folder: {args.csv_folder}"
    
    # Determine export formats
    export_formats = []
    if getattr(args, 'export_parquet', False):
        export_formats.append('parquet')
    if getattr(args, 'export_csv', False):
        export_formats.append('csv')
    if getattr(args, 'export_json', False):
        export_formats.append('json')
    
    # Process the folder
    folder_results = process_csv_folder(
        folder_path=args.csv_folder,
        point_size=args.point,
        rule=getattr(args, 'rule', 'OHLCV'),
        draw_mode=getattr(args, 'draw', None),
        export_formats=export_formats if export_formats else None,
        mask=getattr(args, 'csv_mask', None)
    )
    
    # Store folder processing results
    data_info["folder_processing_results"] = folder_results
    data_info["files_processed"] = folder_results.get('files_processed', 0)
    data_info["files_failed"] = folder_results.get('files_failed', 0)
    data_info["total_processing_time"] = folder_results.get('total_time', 0)
    data_info["total_size_mb"] = folder_results.get('total_size_mb', 0)
    
    # For folder processing, we don't return a single DataFrame
    # Instead, we return success status and processing results
    if folder_results.get('success', False):
        data_info["success"] = True
        # Create a dummy DataFrame for compatibility
        import pandas as pd
        df = pd.DataFrame({'dummy': [1]})
        data_info["ohlcv_df"] = df
    else:
        error_msg = f"Failed to process CSV folder: {args.csv_folder}"
        raise ValueError(error_msg)
    
    return data_info


def _process_csv_single(args, data_info: dict) -> dict:
    """Process single CSV file."""
    from .fetchers import fetch_csv_data
    
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
            data_info["file_size_bytes"] = Path(args.csv_file).stat().st_size
        except Exception:
            pass
    
    data_info["ohlcv_df"] = df
    return data_info


def _process_api_data(args, data_info: dict, effective_mode: str) -> dict:
    """Process API data modes - placeholder for future refactoring."""
    # This function is a placeholder for future refactoring
    # Currently handled in the core module
    pass


def _update_data_info_metrics(data_info: dict, combined_metrics: dict, cache_filepath: Path = None) -> None:
    """Update data_info with metrics and final statistics."""
    if isinstance(combined_metrics, dict):
        api_latency = combined_metrics.get("total_latency_sec", combined_metrics.get("latency_sec", 0.0))
        data_info["api_latency_sec"] = api_latency if api_latency is not None else 0.0
        data_info["api_calls"] = combined_metrics.get("api_calls", 0)
        data_info["successful_chunks"] = combined_metrics.get("successful_chunks", 0)
        data_info["rows_fetched"] = combined_metrics.get("rows_fetched", 0)
        
        if "file_size_bytes" in combined_metrics:
            data_info["file_size_bytes"] = combined_metrics["file_size_bytes"]
        
        if "error_message" in combined_metrics and data_info["error_message"] is None:
            data_info["error_message"] = combined_metrics["error_message"]
        
        data_info["data_metrics"].update(combined_metrics)

    # Update cache file size if available
    if data_info["parquet_cache_used"] and data_info.get("file_size_bytes") is None and cache_filepath and cache_filepath.exists():
        try:
            data_info["file_size_bytes"] = cache_filepath.stat().st_size
        except Exception:
            pass

    # Update DataFrame statistics
    df = data_info.get("ohlcv_df")
    if df is not None and not df.empty:
        data_info["rows_count"] = len(df)
        data_info["columns_count"] = len(df.columns)
        
        try:
            data_info["data_size_bytes"] = df.memory_usage(deep=True).sum()
            data_info["data_size_mb"] = data_info["data_size_bytes"] / (1024 * 1024)
        except Exception as mem_err:
            print_warning(f"Could not calculate DataFrame memory usage: {mem_err}")
            data_info["data_size_bytes"] = -1
            data_info["data_size_mb"] = -1.0
    elif data_info.get("error_message") is None:
        print_warning("Data acquisition resulted in None or empty DataFrame.")


def _validate_dataframe(df: pd.DataFrame, context: str = "") -> bool:
    """Validate DataFrame for common issues."""
    if df is None:
        print_error(f"{context}: DataFrame is None")
        return False
    
    if df.empty:
        print_warning(f"{context}: DataFrame is empty")
        return False
    
    if not isinstance(df.index, pd.DatetimeIndex):
        print_warning(f"{context}: DataFrame index is not DatetimeIndex")
        return False
    
    return True


def _clean_dataframe_index(df: pd.DataFrame) -> pd.DataFrame:
    """Clean DataFrame index by removing timezone info if present."""
    if df is not None and not df.empty and isinstance(df.index, pd.DatetimeIndex):
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
            # print_debug("Removed timezone info from DataFrame index")
    
    return df


def _get_dataframe_summary(df: pd.DataFrame) -> dict:
    """Get summary statistics for DataFrame."""
    if df is None or df.empty:
        return {"rows": 0, "columns": 0, "memory_mb": 0.0}
    
    try:
        memory_bytes = df.memory_usage(deep=True).sum()
        memory_mb = memory_bytes / (1024 * 1024)
        
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "memory_mb": memory_mb,
            "dtypes": df.dtypes.to_dict()
        }
    except Exception as e:
        print_warning(f"Could not get DataFrame summary: {e}")
        return {"rows": len(df), "columns": len(df.columns), "memory_mb": -1.0}


def _log_dataframe_info(df: pd.DataFrame, context: str = "") -> None:
    """Log information about DataFrame."""
    if df is None:
        print_info(f"{context}: DataFrame is None")
        return
    
    if df.empty:
        print_info(f"{context}: DataFrame is empty")
        return
    
    summary = _get_dataframe_summary(df)
    print_info(f"{context}: {summary['rows']} rows, {summary['columns']} columns, "
               f"{summary['memory_mb']:.2f} MB")
    
    if isinstance(df.index, pd.DatetimeIndex):
        print_info(f"{context}: Index range: {df.index.min()} to {df.index.max()}")
        print_info(f"{context}: Index frequency: {df.index.freq}")
