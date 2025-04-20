# src/data/data_acquisition.py # REFACTORED IMPORTS

"""
Workflow Step 1: Handles data acquisition based on mode (demo/yfinance/csv/polygon/binance).
Imports fetchers from the 'fetchers' subpackage.
All comments are in English.
"""

from dotenv import load_dotenv

# Use relative imports within the src package
from ..common import logger
# Import functions from the fetchers subpackage via its __init__.py
from .fetchers import (
    get_demo_data,
    fetch_csv_data,
    fetch_yfinance_data,
    map_interval, map_ticker, # YFinance specific utils needed here
    fetch_polygon_data,
    fetch_binance_data
)


# Definition of the acquire_data function
def acquire_data(args):
    """
    Acquires data based on args.mode by calling the appropriate fetcher.
    Loads environment variables from .env file at the beginning.

    Args:
        args (argparse.Namespace): Parsed command-line arguments from cli.py.

    Returns:
        dict: Contains 'ohlcv_df' (DataFrame or None) and metadata including fetcher metrics.
    """
    # --- Load Environment Variables ---
    dotenv_loaded = load_dotenv()
    if not dotenv_loaded:
         logger.print_warning("Could not find or load .env file. API keys must be set as environment variables.")
    # -----------------------------------------

    # Initialize variables
    ohlcv_df = None
    data_source_label = ""
    yf_ticker = None
    yf_interval = None
    current_period = None
    current_start = args.start
    current_end = args.end
    fetcher_metrics = {} # Initialize dictionary for fetcher metrics

    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    # --- Select Fetcher based on Mode ---
    if effective_mode == 'demo':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Demo) ---")
        data_source_label = "Demo Data"
        ohlcv_df = get_demo_data()
        # Demo has no specific fetcher metrics like latency or file size
        fetcher_metrics = {"latency_sec": None, "file_size_bytes": None}

    elif effective_mode == 'csv':
        logger.print_info("--- Step 1: Acquiring Data (Mode: CSV File) ---")
        if not args.csv_file: raise ValueError("--csv-file is required for csv mode.")
        data_source_label = args.csv_file
        result_tuple = fetch_csv_data(filepath=args.csv_file)
        if result_tuple: ohlcv_df, fetcher_metrics = result_tuple
        else: ohlcv_df, fetcher_metrics = None, {}
        # fetcher_metrics now contains 'file_size_bytes'

    elif effective_mode == 'polygon':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Polygon.io) ---")
        if not args.ticker or not args.start or not args.end: raise ValueError("--ticker, --start, and --end are required for polygon mode.")
        data_source_label = args.ticker
        # MODIFIED: Expect tuple (df, metrics)
        result_tuple = fetch_polygon_data(
            ticker=args.ticker,
            interval=args.interval,
            start_date=current_start,
            end_date=current_end
        )
        if result_tuple: ohlcv_df, fetcher_metrics = result_tuple
        else: ohlcv_df, fetcher_metrics = None, {}
        # fetcher_metrics now contains 'total_latency_sec'
        yf_ticker = None; yf_interval = None; current_period = None # Clear yf vars

    elif effective_mode == 'yfinance':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Yahoo Finance) ---")
        if not args.ticker: raise ValueError("--ticker is required for yfinance mode.")
        data_source_label = args.ticker
        try: yf_interval = map_interval(args.interval)
        except ValueError as e: logger.print_error(f"Failed to map yfinance interval: {e}"); raise
        yf_ticker = map_ticker(args.ticker)
        period_arg = args.period

        # MODIFIED: Expect tuple (df, metrics)
        result_tuple = None
        if current_start and current_end:
             logger.print_info(f"Fetching yfinance data for interval '{yf_interval}' from {current_start} to {current_end}")
             current_period = None
             result_tuple = fetch_yfinance_data(
                ticker=yf_ticker, interval=yf_interval, period=None,
                start_date=current_start, end_date=current_end
             )
        elif period_arg:
             current_period = period_arg; current_start = None; current_end = None
             logger.print_info(f"Fetching yfinance data for interval '{yf_interval}' for period '{current_period}'")
             result_tuple = fetch_yfinance_data(
                ticker=yf_ticker, interval=yf_interval, period=current_period,
                start_date=None, end_date=None
             )
        else:
             current_period = period_arg if period_arg else args.period
             current_start = None; current_end = None
             logger.print_info(f"Fetching yfinance data for interval '{yf_interval}' for default period '{current_period}'")
             result_tuple = fetch_yfinance_data(
                 ticker=yf_ticker, interval=yf_interval, period=current_period,
                 start_date=None, end_date=None
             )

        if result_tuple: ohlcv_df, fetcher_metrics = result_tuple
        else: ohlcv_df, fetcher_metrics = None, {}
        # fetcher_metrics now contains 'latency_sec'

    elif effective_mode == 'binance':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Binance) ---")
        if not args.ticker or not args.start or not args.end: raise ValueError("--ticker, --start, and --end are required for binance mode.")
        data_source_label = args.ticker
        # MODIFIED: Expect tuple (df, metrics)
        result_tuple = fetch_binance_data(
            ticker=args.ticker,
            interval=args.interval,
            start_date=current_start,
            end_date=current_end
        )
        if result_tuple: ohlcv_df, fetcher_metrics = result_tuple
        else: ohlcv_df, fetcher_metrics = None, {}
        # fetcher_metrics now contains 'total_latency_sec'
        yf_ticker = None; yf_interval = None; current_period = None # Clear yf vars

    # --- Return Results ---
    results = {
        "ohlcv_df": ohlcv_df,
        "effective_mode": effective_mode,
        "data_source_label": data_source_label,
        "yf_ticker": yf_ticker,
        "yf_interval": yf_interval,
        "current_period": current_period,
        "current_start": current_start,
        "current_end": current_end,
    }
    # Use a consistent key for latency in the final results, e.g., 'api_latency_sec'
    # Handle different keys returned by fetchers ('latency_sec' vs 'total_latency_sec')
    latency_value = fetcher_metrics.get("latency_sec") or fetcher_metrics.get("total_latency_sec")
    results["api_latency_sec"] = latency_value
    # Add other metrics like file size
    results["file_size_bytes"] = fetcher_metrics.get("file_size_bytes")

    return results