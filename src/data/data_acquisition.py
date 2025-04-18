# src/data_acquisition.py # MODIFIED

"""
Workflow Step 1: Handles data acquisition based on mode (demo/yfinance/csv/polygon).
All comments are in English.
"""

from dotenv import load_dotenv # ADDED import

# Use relative imports within the src package
from ..common import logger
# Import all fetch functions
from .data_utils import (
    get_demo_data, map_interval, map_ticker, fetch_yfinance_data, fetch_csv_data,
    fetch_polygon_data
)


# Definition of the acquire_data function
def acquire_data(args):
    """
    Acquires data based on args.mode (demo, yfinance, csv, polygon).
    Loads environment variables from .env file at the beginning.

    Args:
        args (argparse.Namespace): Parsed command-line arguments from cli.py.

    Returns:
        dict: Contains 'ohlcv_df' (DataFrame or None) and metadata like 'effective_mode',
              'data_source_label', 'yf_ticker', 'yf_interval', etc.
    """
    # --- Load Environment Variables --- ADDED ---
    # Load variables from .env file into environment. Should be called early.
    # Returns True if .env was found and loaded, False otherwise.
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
    current_start = None
    current_end = None

    # Determine effective mode, handling 'yf' alias
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    # --- Demo Mode ---
    if effective_mode == 'demo':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Demo) ---")
        data_source_label = "Demo Data"
        ohlcv_df = get_demo_data()

    # --- CSV Mode ---
    elif effective_mode == 'csv':
        logger.print_info("--- Step 1: Acquiring Data (Mode: CSV File) ---")
        data_source_label = args.csv_file
        ohlcv_df = fetch_csv_data(filepath=args.csv_file)

    # --- Polygon.io Mode ---
    elif effective_mode == 'polygon':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Polygon.io) ---")
        data_source_label = args.ticker
        current_start = args.start
        current_end = args.end
        # fetch_polygon_data will now find the key in the already loaded environment
        ohlcv_df = fetch_polygon_data(
            ticker=args.ticker,
            interval=args.interval,
            start_date=args.start,
            end_date=args.end
        )
        yf_ticker = None
        yf_interval = None
        current_period = None

    # --- Yahoo Finance Mode ---
    elif effective_mode == 'yfinance':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Yahoo Finance) ---")
        data_source_label = args.ticker
        try:
            yf_interval = map_interval(args.interval)
        except ValueError as e:
             logger.print_error(f"Failed to map yfinance interval: {e}")
             raise
        yf_ticker = map_ticker(args.ticker)
        period_arg = args.period
        start_arg = args.start
        end_arg = args.end
        if args.start and args.end:
             current_start = args.start
             current_end = args.end
             logger.print_info(f"Fetching yfinance data for interval '{yf_interval}' from {current_start} to {current_end}")
        else:
             current_period = period_arg
             logger.print_info(f"Fetching yfinance data for interval '{yf_interval}' for period '{current_period}'")
        ohlcv_df = fetch_yfinance_data(
            ticker=yf_ticker, interval=yf_interval, period=current_period,
            start_date=current_start, end_date=current_end
        )

    # --- Return Results ---
    return {
        "ohlcv_df": ohlcv_df,
        "effective_mode": effective_mode,
        "data_source_label": data_source_label,
        "yf_ticker": yf_ticker,
        "yf_interval": yf_interval,
        "current_period": current_period,
        "current_start": current_start,
        "current_end": current_end,
    }