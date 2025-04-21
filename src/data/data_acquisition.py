# src/data/data_acquisition.py

"""
Handles the overall data acquisition process by dispatching to specific fetchers based on mode.
All comments are in English.
"""
import os
import traceback
from dotenv import load_dotenv
import pandas as pd # Keep pandas import

# Use relative imports for fetchers within the same package
from .fetchers import (
    fetch_csv_data, fetch_yfinance_data, fetch_polygon_data,
    fetch_binance_data, get_demo_data
)
# Use relative import for logger
from ..common import logger

# Definition of acquire_data function
def acquire_data(args) -> dict:
    """
    Acquires OHLCV data based on the specified mode and arguments.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        dict: A dictionary containing the DataFrame ('ohlcv_df') and acquisition metrics.
              Returns {'ohlcv_df': None} on failure.
    """
    # --- Load environment variables ---
    dotenv_path = '.env'
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        logger.print_debug(".env file loaded.")
    else:
        logger.print_debug(".env file not found, proceeding without it.")

    # Initialize result structure
    data_info = {
        "ohlcv_df": None, "ticker": args.ticker, "interval": args.interval,
        "data_source_label": "N/A", "effective_mode": args.mode,
        "yf_ticker": None, "yf_interval": None, "current_period": None,
        "current_start": args.start, "current_end": args.end,
        "file_size_bytes": None, "api_latency_sec": None,
        "api_calls": None, "successful_chunks": None, "rows_fetched": None,
        "error_message": None, "data_metrics": {}
    }

    logger.print_info(f"--- Step 1: Acquiring Data (Mode: {args.mode.capitalize()}) ---")

    df = None # Initialize df
    metrics = {} # Initialize metrics

    # --- No tqdm wrapper here ---
    try:
        # --- Dispatch based on mode ---
        if args.mode == 'demo':
            data_info["data_source_label"] = "Demo Data"
            df = get_demo_data() # Demo returns only df
            metrics = {} # No specific metrics for demo

        elif args.mode == 'csv':
            if not args.csv_file: raise ValueError("--csv-file is required for csv mode.")
            if args.point is None: raise ValueError("--point must be provided when using csv mode.") # Check point for CSV
            data_info["data_source_label"] = args.csv_file
            # CSV fetcher returns df, metrics tuple
            df, metrics = fetch_csv_data(filepath=args.csv_file)

        elif args.mode in ['yfinance', 'yf']:
            if not args.ticker: raise ValueError("--ticker is required for yfinance mode.")
            data_info["data_source_label"] = args.ticker
            data_info["yf_ticker"] = args.ticker # Store original ticker for estimation
            data_info["yf_interval"] = args.interval
            data_info["current_period"] = args.period
            # Yfinance fetcher returns df, metrics tuple
            df, metrics = fetch_yfinance_data(
                ticker=args.ticker, interval=args.interval, period=args.period,
                start_date=args.start, end_date=args.end
            )

        elif args.mode == 'polygon':
            if not args.ticker: raise ValueError("--ticker is required for polygon mode.")
            if not args.start or not args.end: raise ValueError("--start and --end are required for polygon mode.")
            if args.point is None: raise ValueError("--point must be provided when using polygon mode.") # Check point for Polygon
            data_info["data_source_label"] = args.ticker
            # Polygon fetcher returns df, metrics tuple
            df, metrics = fetch_polygon_data(
                ticker=args.ticker, interval=args.interval,
                start_date=args.start, end_date=args.end
            )

        elif args.mode == 'binance':
            if not args.ticker: raise ValueError("--ticker is required for binance mode.")
            if not args.start or not args.end: raise ValueError("--start and --end are required for binance mode.")
            if args.point is None: raise ValueError("--point must be provided when using binance mode.") # Check point for Binance
            data_info["data_source_label"] = args.ticker
            # Binance fetcher returns df, metrics tuple
            df, metrics = fetch_binance_data(
                ticker=args.ticker, interval=args.interval,
                start_date=args.start, end_date=args.end
            )
        else:
            # This case should ideally be caught by argparse choices
            raise ValueError(f"Invalid mode specified: {args.mode}")

    except ValueError as ve:
        logger.print_error(f"Configuration error for mode '{args.mode}': {ve}")
        data_info["error_message"] = str(ve)
        # Return immediately on config error before fetchers are called
        return data_info
    except ImportError as ie:
         logger.print_error(f"Missing library for mode '{args.mode}': {ie}")
         data_info["error_message"] = f"Missing library for {args.mode}: {ie}"
         return data_info # Return on import error
    except Exception as e:
        # Catch potential errors during the fetcher call itself
        logger.print_error(f"An unexpected error occurred during data acquisition for mode '{args.mode}': {e}")
        logger.print_error(f"Traceback:\n{traceback.format_exc()}")
        data_info["error_message"] = f"Fetch error: {e}"
        # df remains None
        metrics = metrics or {} # Ensure metrics is a dict even if fetch failed early
        metrics["error_message"] = data_info["error_message"] # Add error to metrics too


    # --- Post-fetch processing ---
    data_info["ohlcv_df"] = df
    # Merge fetched metrics into data_info, prioritizing fetched values
    if isinstance(metrics, dict):
        # Map specific metric names if needed
        if "file_size_bytes" in metrics: data_info["file_size_bytes"] = metrics["file_size_bytes"]
        # Use 'total_latency_sec' if available, else 'latency_sec'
        if "total_latency_sec" in metrics: data_info["api_latency_sec"] = metrics["total_latency_sec"]
        elif "latency_sec" in metrics: data_info["api_latency_sec"] = metrics["latency_sec"]
        if "api_calls" in metrics: data_info["api_calls"] = metrics["api_calls"]
        if "successful_chunks" in metrics: data_info["successful_chunks"] = metrics["successful_chunks"]
        if "rows_fetched" in metrics: data_info["rows_fetched"] = metrics["rows_fetched"]
        if "error_message" in metrics: # Propagate error from fetcher if not already set
             if data_info["error_message"] is None: data_info["error_message"] = metrics["error_message"]
        # Store the raw metrics dict as well
        data_info["data_metrics"].update(metrics)


    if df is None: logger.print_warning("Data acquisition resulted in None DataFrame.")
    elif df.empty: logger.print_warning("Data acquisition resulted in an empty DataFrame.")
    else: logger.print_info(f"Data acquired successfully: {len(df)} rows.")

    return data_info