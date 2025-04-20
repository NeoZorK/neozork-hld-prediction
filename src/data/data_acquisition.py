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


# Definition of the acquire_data function (logic remains the same)
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
    # Initialize dictionary for fetcher metrics
    fetcher_metrics = {}

    # Determine effective mode, handling 'yf' alias
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    # --- Select Fetcher based on Mode ---
    if effective_mode == 'demo':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Demo) ---")
        data_source_label = "Demo Data"
        ohlcv_df = get_demo_data() # Call demo fetcher
        # No specific fetcher metrics for demo

    elif effective_mode == 'csv':
        logger.print_info("--- Step 1: Acquiring Data (Mode: CSV File) ---")
        if not args.csv_file:
             # This should be caught by CLI, but double-check
             logger.print_error("--csv-file is required for csv mode.")
             raise ValueError("--csv-file is required for csv mode.")
        data_source_label = args.csv_file
        # MODIFIED: Expect tuple (df, metrics)
        result_tuple = fetch_csv_data(filepath=args.csv_file)
        if result_tuple:
             ohlcv_df, fetcher_metrics = result_tuple
        else: # Handle case where fetcher returns None directly on major error
             ohlcv_df, fetcher_metrics = None, {}
        # fetcher_metrics will contain 'file_size_bytes' if successful

    elif effective_mode == 'polygon':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Polygon.io) ---")
        if not args.ticker or not args.start or not args.end:
             logger.print_error("--ticker, --start, and --end are required for polygon mode.")
             raise ValueError("--ticker, --start, and --end are required for polygon mode.")
        data_source_label = args.ticker
        # TODO (Next Step): Modify fetch_polygon_data to return (df, metrics)
        # For now, assume it just returns df
        ohlcv_df = fetch_polygon_data( # Call polygon fetcher
            ticker=args.ticker,
            interval=args.interval,
            start_date=current_start,
            end_date=current_end
        )
        # Placeholder for future metrics
        fetcher_metrics = {"latency_sec": None}
        yf_ticker = None; yf_interval = None; current_period = None # Clear yf vars

    elif effective_mode == 'yfinance':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Yahoo Finance) ---")
        if not args.ticker:
            logger.print_error("--ticker is required for yfinance mode.")
            raise ValueError("--ticker is required for yfinance mode.")
        data_source_label = args.ticker
        try:
            yf_interval = map_interval(args.interval) # Use imported map_interval
        except ValueError as e:
            logger.print_error(f"Failed to map yfinance interval: {e}")
            raise
        yf_ticker = map_ticker(args.ticker) # Use imported map_ticker
        period_arg = args.period

        # TODO (Next Step): Modify fetch_yfinance_data to return (df, metrics)
        # For now, assume it just returns df
        if current_start and current_end:
             logger.print_info(f"Fetching yfinance data for interval '{yf_interval}' from {current_start} to {current_end}")
             current_period = None
             ohlcv_df = fetch_yfinance_data( # Call yfinance fetcher
                ticker=yf_ticker, interval=yf_interval, period=None,
                start_date=current_start, end_date=current_end
             )
        elif period_arg:
             current_period = period_arg
             current_start = None; current_end = None
             logger.print_info(f"Fetching yfinance data for interval '{yf_interval}' for period '{current_period}'")
             ohlcv_df = fetch_yfinance_data( # Call yfinance fetcher
                ticker=yf_ticker, interval=yf_interval, period=current_period,
                start_date=None, end_date=None
             )
        else:
             current_period = period_arg if period_arg else args.period # Use default if None
             current_start = None; current_end = None
             logger.print_info(f"Fetching yfinance data for interval '{yf_interval}' for default period '{current_period}'")
             ohlcv_df = fetch_yfinance_data( # Call yfinance fetcher
                 ticker=yf_ticker, interval=yf_interval, period=current_period,
                 start_date=None, end_date=None
             )
        # Placeholder for future metrics
        fetcher_metrics = {"latency_sec": None}


    elif effective_mode == 'binance':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Binance) ---")
        if not args.ticker or not args.start or not args.end:
             logger.print_error("--ticker, --start, and --end are required for binance mode.")
             raise ValueError("--ticker, --start, and --end are required for binance mode.")
        data_source_label = args.ticker
        # TODO (Next Step): Modify fetch_binance_data to return (df, metrics)
        # For now, assume it just returns df
        ohlcv_df = fetch_binance_data( # Call binance fetcher
            ticker=args.ticker,
            interval=args.interval,
            start_date=current_start,
            end_date=current_end
        )
        # Placeholder for future metrics
        fetcher_metrics = {"latency_sec": None}
        yf_ticker = None; yf_interval = None; current_period = None # Clear yf vars

    # --- Return Results ---
    # Combine base info with metrics from the fetcher
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
    # Add metrics collected by the fetcher
    results.update(fetcher_metrics) # Adds keys like 'file_size_bytes', 'latency_sec' etc.

    return results