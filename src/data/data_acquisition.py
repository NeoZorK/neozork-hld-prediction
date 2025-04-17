# src/data_acquisition.py

"""
Workflow Step 1: Handles data acquisition based on mode (demo/yfinance).
All comments are in English.
"""
from datetime import date

# Use relative imports within the src package
from ..common import logger
from .data_utils import get_demo_data, map_interval, map_ticker, fetch_yfinance_data

def acquire_data(args):
    """
    Acquires data based on args.mode.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        dict: Contains 'ohlcv_df' and metadata like 'effective_mode',
              'data_source_label', 'yf_ticker', 'yf_interval', etc.
              Returns df as None if acquisition fails.
    """
    ohlcv_df = None
    data_source_label = ""
    yf_ticker = None
    yf_interval = None
    current_period = None
    current_start = None
    current_end = None

    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    if effective_mode == 'demo':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Demo) ---")
        data_source_label = "Demo Data"
        ohlcv_df = get_demo_data()
    elif effective_mode == 'yfinance':
        logger.print_info("--- Step 1: Acquiring Data (Mode: Yahoo Finance) ---")
        if not args.ticker:
             # Raising error here stops execution early
             raise ValueError("Ticker (--ticker) is required for yfinance mode.")

        data_source_label = args.ticker
        yf_interval = map_interval(args.interval) # Raises ValueError on error
        yf_ticker = map_ticker(args.ticker)
        period_arg = args.period
        start_arg = args.start
        end_arg = args.end

        if args.start and not args.end:
            end_arg = date.today().strftime('%Y-%m-%d')
            logger.print_info(f"End date not specified, using today: {end_arg}")
        elif args.end and not args.start:
            start_arg = "2000-01-01"
            logger.print_info(f"Start date not specified, using default: {start_arg}")

        if start_arg and end_arg:
            current_start = start_arg
            current_end = end_arg
            logger.print_info(f"Fetching data for interval '{yf_interval}' from {current_start} to {current_end}")
        else:
            current_period = period_arg
            logger.print_info(f"Fetching data for interval '{yf_interval}' for period '{current_period}'")

        ohlcv_df = fetch_yfinance_data( # fetch_yfinance_data logs its own details
            ticker=yf_ticker, interval=yf_interval, period=current_period,
            start_date=current_start, end_date=current_end
        )
        # Don't raise error here if df is None, let orchestrator handle it

    # Return data and metadata
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