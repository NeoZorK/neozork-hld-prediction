# src/data_acquisition.py

"""
Workflow Step 1: Handles data acquisition based on mode (demo/yfinance/csv).
All comments are in English.
"""
from datetime import date
# ADDED pathlib for potential path handling, though not strictly needed here yet


# Use relative imports within the src package
from ..common import logger
# Import fetch_csv_data along with others
from .data_utils import get_demo_data, map_interval, map_ticker, fetch_yfinance_data, fetch_csv_data # ADDED fetch_csv_data


# Definition of the acquire_data function
def acquire_data(args):
    """
    Acquires data based on args.mode (demo, yfinance, csv).

    Args:
        args (argparse.Namespace): Parsed command-line arguments from cli.py.

    Returns:
        dict: Contains 'ohlcv_df' (DataFrame or None) and metadata like 'effective_mode',
              'data_source_label', 'yf_ticker', 'yf_interval', etc.
    """
    # Initialize variables to store results and metadata
    ohlcv_df = None # Will hold the main OHLCV DataFrame
    data_source_label = "" # A label identifying the data source (e.g., ticker, filename)
    yf_ticker = None # Yahoo Finance specific ticker
    yf_interval = None # Yahoo Finance specific interval
    current_period = None # Period used for yfinance fetch (e.g., '1y')
    current_start = None # Start date used for yfinance fetch
    current_end = None # End date used for yfinance fetch

    # Determine the effective mode, handling 'yf' as an alias for 'yfinance'
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    # --- Demo Mode ---
    # Handles the case when mode is 'demo'
    if effective_mode == 'demo':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Demo) ---")
        # Sets the label for demo data.
        data_source_label = "Demo Data"
        # Calls the function to generate demo data.
        ohlcv_df = get_demo_data()

    # --- CSV Mode --- ADDED THIS BLOCK
    # Handles the case when mode is 'csv'
    elif effective_mode == 'csv':
        logger.print_info("--- Step 1: Acquiring Data (Mode: CSV File) ---")
        # NOTE: The CLI should have already checked that args.csv_file exists for this mode.
        # Sets the data source label to the provided CSV file path.
        data_source_label = args.csv_file # Use the filename as the label
        # Calls the new function to fetch data from the specified CSV file.
        ohlcv_df = fetch_csv_data(filepath=args.csv_file)
        # If fetch_csv_data returns None, ohlcv_df will be None, handled later.

    # --- Yahoo Finance Mode ---
    # Handles the case when mode is 'yfinance'
    elif effective_mode == 'yfinance':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Yahoo Finance) ---")
        # Checks if the required ticker argument was provided.
        if not args.ticker:
             # Raising error here stops execution early if ticker is missing for yfinance.
             raise ValueError("Ticker (--ticker) is required for yfinance mode.")

        # Sets the label to the ticker symbol.
        data_source_label = args.ticker
        # Maps the user-friendly interval (e.g., 'D1') to the yfinance format (e.g., '1d').
        yf_interval = map_interval(args.interval) # Raises ValueError on invalid input
        # Maps the user-provided ticker to a potentially modified yfinance ticker (e.g., adding '=X').
        yf_ticker = map_ticker(args.ticker)
        # Gets period, start, and end date arguments from the parsed arguments.
        period_arg = args.period
        start_arg = args.start
        end_arg = args.end

        # Handles logic if only start date or only end date is provided.
        # If start is given but end is missing, set end to today.
        if args.start and not args.end:
            end_arg = date.today().strftime('%Y-%m-%d')
            logger.print_info(f"End date not specified, using today: {end_arg}")
        # If end is given but start is missing, set start to a default past date.
        elif args.end and not args.start:
            # Default start date if only end date is provided.
            start_arg = "2000-01-01"
            logger.print_info(f"Start date not specified, using default: {start_arg}")

        # Determines whether to use period or start/end dates for the API call.
        # If both start and end dates are determined, use them.
        if start_arg and end_arg:
            current_start = start_arg
            current_end = end_arg
            # Logs the parameters being used for fetching.
            logger.print_info(f"Fetching data for interval '{yf_interval}' from {current_start} to {current_end}")
        # Otherwise, use the period argument.
        else:
            current_period = period_arg
            # Logs the parameters being used for fetching.
            logger.print_info(f"Fetching data for interval '{yf_interval}' for period '{current_period}'")

        # Calls the function to fetch data from Yahoo Finance.
        # fetch_yfinance_data handles its own internal logging and error reporting.
        ohlcv_df = fetch_yfinance_data(
            ticker=yf_ticker, interval=yf_interval, period=current_period,
            start_date=current_start, end_date=current_end
        )
        # Don't raise error here if df is None, let the main workflow handle None DataFrame.

    # --- Return Results ---
    # Collects all relevant data and metadata into a dictionary.
    # Returns the dictionary containing the DataFrame (or None) and all metadata.
    return {
        "ohlcv_df": ohlcv_df, # The acquired DataFrame (or None if failed)
        "effective_mode": effective_mode, # The mode used ('demo', 'csv', 'yfinance')
        "data_source_label": data_source_label, # Identifier for the source (ticker, filename, 'Demo Data')
        # --- yfinance specific metadata (will be None for other modes) ---
        "yf_ticker": yf_ticker, # Ticker used for yfinance
        "yf_interval": yf_interval, # Interval used for yfinance
        "current_period": current_period, # Period used for yfinance
        "current_start": current_start, # Start date used for yfinance
        "current_end": current_end, # End date used for yfinance
        # --- Add specific metadata for other modes if needed in the future ---
    }