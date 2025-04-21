# src/data/data_acquisition.py (Added Parquet caching logic)

"""
Handles the overall data acquisition process by dispatching to specific fetchers based on mode.
All comments are in English.
"""
import os
import traceback
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path # Use pathlib for cleaner path joining

# Use relative imports for fetchers within the same package
from .fetchers import (
    fetch_csv_data, fetch_yfinance_data, fetch_polygon_data,
    fetch_binance_data, get_demo_data
)
# Use relative import for logger
from ..common import logger

# --- Helper function for Parquet filename ---
def _generate_parquet_filename(args) -> Path | None:
    """Generates the expected parquet filename based on args."""
    # Caching only applies to API modes with specific identifiers
    if args.mode not in ['yfinance', 'polygon', 'binance'] or not args.ticker:
        return None

    # Use required args for these modes
    if args.mode in ['polygon', 'binance'] and (not args.start or not args.end):
         logger.print_debug(f"Cannot generate cache filename for {args.mode} without start/end dates.")
         return None
    # For yfinance, allow period OR start/end
    if args.mode == 'yfinance' and not args.period and (not args.start or not args.end):
         logger.print_debug("Cannot generate cache filename for yfinance without period or start/end dates.")
         return None


    parquet_dir = Path("data/raw_parquet")
    try:
        # Sanitize ticker for filename
        ticker_label = str(args.ticker).replace('/', '_').replace('-', '_').replace('=','_')
        interval_label = str(args.interval)

        # Determine date part based on available args
        if args.start and args.end:
            date_part = f"{args.start}_{args.end}"
        elif args.period:
             # Note: Cache filename based on period might not perfectly match
             # data fetched if yfinance adjusts dates, but it's the best we can do.
             date_part = f"period_{args.period}"
        else:
            date_part = "unknown_range" # Fallback

        filename = f"{args.mode}_{ticker_label}_{interval_label}_{date_part}.parquet"
        filepath = parquet_dir / filename
        return filepath
    except Exception as e:
        logger.print_warning(f"Error generating parquet filename: {e}")
        return None


# Definition of acquire_data function
def acquire_data(args) -> dict:
    """
    Acquires OHLCV data based on the specified mode and arguments.
    Checks for existing Parquet cache before fetching from APIs.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        dict: A dictionary containing the DataFrame ('ohlcv_df') and acquisition metrics.
              Returns {'ohlcv_df': None} on failure.
    """
    # --- Load environment variables ---
    dotenv_path = '.env'
    if os.path.exists(dotenv_path): load_dotenv(dotenv_path=dotenv_path); logger.print_debug(".env file loaded.")
    else: logger.print_debug(".env file not found, proceeding without it.")

    # Initialize result structure
    data_info = { # Default values
        "ohlcv_df": None, "ticker": args.ticker, "interval": args.interval,
        "data_source_label": "N/A", "effective_mode": args.mode,
        "yf_ticker": None, "yf_interval": None, "current_period": None,
        "current_start": args.start, "current_end": args.end,
        "file_size_bytes": None, "api_latency_sec": None,
        "api_calls": None, "successful_chunks": None, "rows_fetched": None,
        "error_message": None, "data_metrics": {}, "parquet_cache_used": False
    }

    logger.print_info(f"--- Step 1: Acquiring Data (Mode: {args.mode.capitalize()}) ---")

    df = None
    metrics = {}
    cache_filepath = None

    # --- Attempt to load from Parquet cache for API modes ---
    if args.mode in ['yfinance', 'polygon', 'binance']:
        cache_filepath = _generate_parquet_filename(args)
        if cache_filepath and cache_filepath.exists():
            logger.print_info(f"Found existing Parquet file: {cache_filepath}")
            try:
                logger.print_info("Attempting to load data from cache...")
                df = pd.read_parquet(cache_filepath)
                logger.print_success(f"Successfully loaded {len(df)} rows from Parquet cache.")
                data_info["data_source_label"] = str(cache_filepath) # Update source label
                data_info["parquet_cache_used"] = True
                # Populate some basic metrics from loaded df
                data_info["rows_fetched"] = len(df)
                try: # Safely get file size
                     data_info["file_size_bytes"] = cache_filepath.stat().st_size
                except Exception: pass # Ignore if stat fails

            except Exception as e:
                logger.print_warning(f"Failed to load data from Parquet cache ({cache_filepath}): {e}")
                logger.print_info("Proceeding to fetch data from API...")
                df = None # Ensure df is None if cache loading fails
                data_info["parquet_cache_used"] = False
        else:
            logger.print_info("No suitable Parquet cache file found. Fetching from API...")

    # --- Fetch from source ONLY if not loaded from cache ---
    if not data_info["parquet_cache_used"]:
        try:
            # --- Dispatch based on mode ---
            if args.mode == 'demo':
                data_info["data_source_label"] = "Demo Data"
                df = get_demo_data(); metrics = {}
            elif args.mode == 'csv':
                if not args.csv_file: raise ValueError("--csv-file is required for csv mode.")
                if args.point is None: raise ValueError("--point must be provided when using csv mode.")
                data_info["data_source_label"] = args.csv_file
                df, metrics = fetch_csv_data(filepath=args.csv_file)
            elif args.mode in ['yfinance', 'yf']:
                if not args.ticker: raise ValueError("--ticker is required for yfinance mode.")
                data_info["data_source_label"] = args.ticker; data_info["yf_ticker"] = args.ticker
                data_info["yf_interval"] = args.interval; data_info["current_period"] = args.period
                df, metrics = fetch_yfinance_data(ticker=args.ticker, interval=args.interval, period=args.period, start_date=args.start, end_date=args.end)
            elif args.mode == 'polygon':
                if not args.ticker: raise ValueError("--ticker is required for polygon mode.")
                if not args.start or not args.end: raise ValueError("--start and --end are required for polygon mode.")
                if args.point is None: raise ValueError("--point must be provided when using polygon mode.")
                data_info["data_source_label"] = args.ticker
                df, metrics = fetch_polygon_data(ticker=args.ticker, interval=args.interval, start_date=args.start, end_date=args.end)
            elif args.mode == 'binance':
                if not args.ticker: raise ValueError("--ticker is required for binance mode.")
                if not args.start or not args.end: raise ValueError("--start and --end are required for binance mode.")
                if args.point is None: raise ValueError("--point must be provided when using binance mode.")
                data_info["data_source_label"] = args.ticker
                df, metrics = fetch_binance_data(ticker=args.ticker, interval=args.interval, start_date=args.start, end_date=args.end)
            else:
                raise ValueError(f"Invalid mode specified: {args.mode}")

        except ValueError as ve:
            logger.print_error(f"Configuration error for mode '{args.mode}': {ve}"); data_info["error_message"] = str(ve); return data_info
        except ImportError as ie:
             logger.print_error(f"Missing library for mode '{args.mode}': {ie}"); data_info["error_message"] = f"Missing library for {args.mode}: {ie}"; return data_info
        except Exception as e:
            logger.print_error(f"An unexpected error occurred during data acquisition for mode '{args.mode}': {e}"); logger.print_error(f"Traceback:\n{traceback.format_exc()}")
            data_info["error_message"] = f"Fetch error: {e}"; metrics = metrics or {}; metrics["error_message"] = data_info["error_message"]

    # --- Post-fetch/load processing ---
    data_info["ohlcv_df"] = df
    if isinstance(metrics, dict): # Merge metrics safely
        # ... (mapping logic as before) ...
        if "total_latency_sec" in metrics: data_info["api_latency_sec"] = metrics["total_latency_sec"]
        elif "latency_sec" in metrics: data_info["api_latency_sec"] = metrics["latency_sec"]
        # ... other metric mappings ...
        if "error_message" in metrics and data_info["error_message"] is None: data_info["error_message"] = metrics["error_message"]
        data_info["data_metrics"].update(metrics)

    if df is None: logger.print_warning("Data acquisition resulted in None DataFrame.")
    elif df.empty: logger.print_warning("Data acquisition resulted in an empty DataFrame.")
    else: logger.print_info(f"Data acquired successfully: {len(df)} rows.")

    return data_info