# src/data_utils.py # MODIFIED AGAIN TO FIX WARNINGS

"""
Utility functions for fetching and preparing data (demo, yfinance, csv, polygon).
All comments are in English.
"""
import pandas as pd
import yfinance as yf
import time
from datetime import date, timedelta, datetime
from pathlib import Path
import numpy as np
import os
#from dotenv import load_dotenv
#import json # Added import for json

# Polygon specific imports
# Note: Requires 'polygon-api-client' installed
try:
    # noinspection PackageRequirements
    import polygon # type: ignore
    from polygon.exceptions import BadResponse # type: ignore
    # Attempt to import the Agg type for type hinting
    try:
        from polygon.rest.models.aggs import Agg # type: ignore
    except ImportError:
        # Fallback if structure changed or type hint isn't critical
        Agg = object # Use generic object if Agg cannot be imported
    POLYGON_AVAILABLE = True
except ImportError:
    POLYGON_AVAILABLE = False
    # Define dummy classes if polygon is not installed to avoid NameErrors later
    class BadResponse(Exception): pass
    class RESTClient: pass
    Agg = object


# Use relative import for the logger within the src package
from ..common import logger


# ---------------------------------------------------------------------------- #
#                             CSV Data Functions                               #
# ---------------------------------------------------------------------------- #

def fetch_csv_data(filepath: str) -> pd.DataFrame | None:
    """
    Reads historical OHLCV and indicator data from a specified CSV file.
    """
    logger.print_debug(f"Attempting to read CSV file: {filepath}")
    file_path_obj = Path(filepath)
    if not file_path_obj.is_file():
        logger.print_error(f"CSV file not found at path: {file_path_obj}")
        return None

    try:
        df = pd.read_csv(file_path_obj, sep=',', header=1, skipinitialspace=True, low_memory=False)
        if df.empty:
            logger.print_warning(f"CSV file is empty: {filepath}")
            return None

        original_columns = df.columns.tolist()
        cleaned_columns = [str(col).strip().rstrip(',') for col in original_columns]
        df.columns = cleaned_columns
        logger.print_debug(f"Original CSV columns: {original_columns}")
        logger.print_debug(f"Cleaned CSV columns: {cleaned_columns}")

        unnamed_cols = [col for col in df.columns if col == '' or 'Unnamed' in col]
        if unnamed_cols:
            logger.print_debug(f"Dropping unnamed/empty columns: {unnamed_cols}")
            df.drop(columns=unnamed_cols, inplace=True, errors='ignore')

        if 'DateTime' not in df.columns:
            logger.print_error("Mandatory 'DateTime' column not found in CSV.")
            return None
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y.%m.%d %H:%M', errors='coerce')
        rows_before_dropna = len(df)
        df.dropna(subset=['DateTime'], inplace=True)
        rows_after_dropna = len(df)
        if rows_before_dropna > rows_after_dropna:
            logger.print_warning(f"Dropped {rows_before_dropna - rows_after_dropna} rows with invalid DateTime format.")
        if df.empty:
            logger.print_warning("DataFrame became empty after removing rows with invalid dates.")
            return None
        df.set_index('DateTime', inplace=True)

        df.rename(columns={'TickVolume': 'Volume'}, inplace=True, errors='ignore')

        for col in df.columns:
             df[col] = pd.to_numeric(df[col], errors='coerce')

        inf_mask = np.isinf(df.select_dtypes(include=[np.number]))
        if inf_mask.any().any():
            logger.print_warning("Replacing infinite values (inf, -inf) with NaN.")
            df.replace([np.inf, -np.inf], np.nan, inplace=True)

        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.print_error(f"CSV data is missing required columns after processing: {missing_cols}")
            # Use list() for safety with potential list assignment earlier
            logger.print_error(f"Available columns: {list(df.columns)}")
            return None

        logger.print_info(f"Successfully read and processed {len(df)} rows from {filepath}")
        return df

    except FileNotFoundError:
        logger.print_error(f"CSV file not found at path: {file_path_obj}")
        return None
    except pd.errors.EmptyDataError:
        logger.print_error(f"CSV file is empty: {filepath}")
        return None
    except pd.errors.ParserError as e:
        logger.print_error(f"Failed to parse CSV file: {filepath} - Error: {e}")
        return None
    except KeyError as e:
         logger.print_error(f"Missing expected column during processing: {e} in file {filepath}")
         return None
    except Exception as e:
        logger.print_error(f"An unexpected error occurred while processing CSV {filepath}: {type(e).__name__}: {e}")
        return None

# ---------------------------------------------------------------------------- #
#                             Demo Data Functions                              #
# ---------------------------------------------------------------------------- #
def get_demo_data() -> pd.DataFrame:
    """Returns the demonstration DataFrame."""
    logger.print_info("Generating demo data...")
    time.sleep(0.5)
    data = {
        'Open': [1.1, 1.11, 1.12, 1.115, 1.125, 1.13, 1.128, 1.135, 1.14, 1.138, 1.142, 1.145, 1.140, 1.135, 1.130, 1.132, 1.138, 1.145, 1.148, 1.150, 1.152, 1.155, 1.153, 1.158, 1.160, 1.157, 1.162, 1.165, 1.163, 1.160],
        'High': [1.105, 1.115, 1.125, 1.12, 1.13, 1.135, 1.133, 1.14, 1.145, 1.142, 1.146, 1.148, 1.143, 1.139, 1.136, 1.137, 1.142, 1.150, 1.152, 1.155, 1.156, 1.159, 1.158, 1.161, 1.163, 1.160, 1.165, 1.168, 1.166, 1.164],
        'Low': [1.095, 1.105, 1.115, 1.11, 1.12, 1.125, 1.125, 1.13, 1.135, 1.136, 1.140, 1.142, 1.138, 1.133, 1.128, 1.130, 1.135, 1.143, 1.146, 1.148, 1.150, 1.152, 1.151, 1.155, 1.157, 1.154, 1.159, 1.161, 1.160, 1.158],
        'Close': [1.1, 1.11, 1.118, 1.118, 1.128, 1.128, 1.131, 1.138, 1.138, 1.14, 1.145, 1.141, 1.136, 1.131, 1.131, 1.136, 1.144, 1.149, 1.151, 1.149, 1.155, 1.154, 1.157, 1.160, 1.159, 1.158, 1.163, 1.164, 1.161, 1.159],
        'Volume': [1000, 1200, 1100, 1300, 1500, 1400, 1600, 1700, 1550, 1650, 1750, 1800, 1600, 1900, 2000, 1850, 1950, 2100, 2050, 2200, 2150, 2250, 2100, 2300, 2400, 2350, 2450, 2500, 2400, 2300]
    }
    start_date_idx = date.today() - timedelta(days=len(data['Open'])-1)
    index = pd.date_range(start=start_date_idx, periods=len(data['Open']), freq='D')
    df = pd.DataFrame(data, index=index)
    return df

# ---------------------------------------------------------------------------- #
#                         Yahoo Finance Data Functions                         #
# ---------------------------------------------------------------------------- #
def map_interval(tf_input: str) -> str:
    """Maps user-friendly timeframe input to yfinance interval string."""
    tf_input_upper = tf_input.upper()
    mapping = {"M1": "1m", "M5": "5m", "M15": "15m", "M30": "30m", "H1": "1h", "H4": "4h", "D1": "1d", "D": "1d", "W1": "1wk", "W": "1wk", "WK": "1wk", "MN1": "1mo", "MN": "1mo", "MO": "1mo"}
    valid_yf_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
    if tf_input_upper in mapping: return mapping[tf_input_upper]
    elif tf_input.lower() in valid_yf_intervals: return tf_input.lower()
    else: raise ValueError(f"Invalid yfinance timeframe input: '{tf_input}'. Use M1, H1, D1, W1, MN1 or yfinance intervals.")

def map_ticker(ticker_input: str) -> str:
    """Optional: Adds standard suffixes for common yfinance ticker patterns."""
    ticker = ticker_input.upper()
    if len(ticker) == 6 and '=' not in ticker and '-' not in ticker and all(c.isalpha() for c in ticker):
        logger.print_info(f"Assuming '{ticker}' is Forex, appending '=X'. -> '{ticker}=X'")
        return f"{ticker}=X"
    return ticker

def fetch_yfinance_data(ticker: str, interval: str, period: str = None, start_date: str = None, end_date: str = None) -> pd.DataFrame | None:
    """Downloads data from Yahoo Finance, handles MultiIndex columns, and validates."""
    logger.print_info(f"Attempting to fetch yfinance data for: {ticker} | interval: {interval}")
    try:
        df = yf.download(tickers=ticker, period=period, interval=interval, start=start_date, end=end_date, progress=True, auto_adjust=False, actions=False)
        if df is None or df.empty:
            logger.print_warning(f"No yfinance data returned for '{ticker}' with specified parameters.")
            return None
        if isinstance(df.columns, pd.MultiIndex):
            logger.print_debug("Detected MultiIndex columns from yfinance. Simplifying...")
            if df.columns.nlevels > 1:
                 #original_cols = df.columns
                 try: df.columns = df.columns.droplevel(1)
                 except Exception as multi_index_error: logger.print_error(f"Failed to simplify yfinance MultiIndex columns: {multi_index_error}"); return None
            else:
                 logger.print_warning("Single-level MultiIndex detected. Flattening.")
                 try: df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
                 except Exception as flatten_error: logger.print_error(f"Failed to flatten unusual yfinance MultiIndex: {flatten_error}"); return None
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            # Use list() for safety
            logger.print_warning(f"yfinance data for '{ticker}' missing required columns: {missing_cols}. Available: {list(df.columns)}")
            return None
        initial_rows = len(df)
        try: df.dropna(subset=['Open', 'High', 'Low', 'Close'], how='all', inplace=True)
        except KeyError as ke:
             # Use list() for safety
             logger.print_error(f"KeyError during dropna for yfinance data: {ke}. Columns: {list(df.columns)}")
             return None
        rows_dropped = initial_rows - len(df)
        if rows_dropped > 0: logger.print_debug(f"Dropped {rows_dropped} yfinance rows with NaNs in OHLC columns.")
        if df.empty: logger.print_warning(f"yfinance data for '{ticker}' became empty after removing NaN rows."); return None
        logger.print_success(f"Successfully fetched and validated {len(df)} yfinance rows.")
        return df
    except Exception as e:
        logger.print_error(f"\n--- ERROR DOWNLOADING/PROCESSING YFINANCE ---")
        logger.print_error(f"An unexpected error occurred for ticker '{ticker}': {type(e).__name__}: {e}")
        import traceback
        tb_str = traceback.format_exc()
        try: print(f"{logger.ERROR_COLOR}Traceback:\n{tb_str}{logger.RESET_ALL}")
        except AttributeError: print(f"Traceback:\n{tb_str}")
        logger.print_error(f"--- END YFINANCE ERROR ---")
        return None

# ---------------------------------------------------------------------------- #
#                           Polygon.io Data Functions                          #
# ---------------------------------------------------------------------------- #
def map_polygon_interval(tf_input: str) -> tuple[str, int] | None:
    """Maps user-friendly timeframe to Polygon.io timespan and multiplier."""
    tf_input_upper = tf_input.upper()
    mapping = {"M1": ("minute", 1), "M5": ("minute", 5), "M15": ("minute", 15), "M30": ("minute", 30), "H1": ("hour", 1), "H4": ("hour", 4), "D1": ("day", 1), "D": ("day", 1), "W1": ("week", 1), "W": ("week", 1), "WK": ("week", 1), "MN1": ("month", 1), "MN": ("month", 1), "MO": ("month", 1)}
    valid_polygon_timespans = ['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']
    if tf_input_upper in mapping: return mapping[tf_input_upper]
    elif tf_input.lower() in valid_polygon_timespans: return tf_input.lower(), 1
    else: logger.print_error(f"Invalid Polygon timeframe input: '{tf_input}'. Use formats like M1, H1, D1 etc."); return None

def map_polygon_ticker(ticker_input: str) -> str:
    """Adjusts ticker format for Polygon.io (e.g., adds 'X:' for Forex/Crypto)."""
    ticker = ticker_input.upper()
    if '.' not in ticker and ':' not in ticker and '-' not in ticker:
        logger.print_info(f"Assuming '{ticker}' is Forex/Crypto, prepending 'X:'. -> 'X:{ticker}'")
        return f"X:{ticker}"
    return ticker

# Fetches aggregate bars (OHLCV) data from Polygon.io API.
def fetch_polygon_data(ticker: str, interval: str, start_date: str, end_date: str) -> pd.DataFrame | None:
    """
    Downloads OHLCV data from Polygon.io REST API for a specified date range.
    Assumes POLYGON_API_KEY is already loaded into environment variables.

    Args:
        ticker (str): The ticker symbol to fetch (e.g., 'AAPL', 'EURUSD').
        interval (str): The timeframe interval (e.g., 'D1', 'H1', 'M1').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame | None: DataFrame with OHLCV data and DatetimeIndex, or None on failure.
                              Standard columns: Open, High, Low, Close, Volume.
    """
    if not POLYGON_AVAILABLE:
        logger.print_error("Polygon API client library ('polygon-api-client') is not installed. Cannot fetch Polygon data.")
        return None

    logger.print_info(f"Attempting to fetch Polygon.io data for: {ticker} | interval: {interval}")

    # --- Get API Key from environment ---
    # Environment should be loaded by the calling function (e.g., acquire_data)
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        # This error message remains, but load_dotenv() call is removed
        logger.print_error("POLYGON_API_KEY not found in environment variables.")
        return None
    # --- REMOVED load_dotenv() call from here ---

    # Map interval and ticker
    interval_map = map_polygon_interval(interval)
    if interval_map is None: return None
    timespan, multiplier = interval_map
    mapped_ticker = map_polygon_ticker(ticker)

    # Convert dates
    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        logger.print_error(f"Invalid date format for start_date ('{start_date}') or end_date ('{end_date}'). Use YYYY-MM-DD.")
        return None

    # Initialize client
    try:
        client = polygon.RESTClient(api_key=api_key)
    except Exception as e:
        logger.print_error(f"Failed to initialize Polygon client: {type(e).__name__}: {e}")
        return None

    # Fetch data
    try:
        logger.print_info(f"Requesting aggregates for {mapped_ticker} ({timespan} x{multiplier}) from {start_date_obj} to {end_date_obj}")
        aggs_iter = client.get_aggs(
            ticker=mapped_ticker, multiplier=multiplier, timespan=timespan,
            from_=start_date_obj, to=end_date_obj, adjusted=False, limit=50000
        )

        agg_data = [
            {'DateTime': pd.to_datetime(agg.timestamp, unit='ms') if hasattr(agg, 'timestamp') else None,
             'Open': getattr(agg, 'open', None), 'High': getattr(agg, 'high', None),
             'Low': getattr(agg, 'low', None), 'Close': getattr(agg, 'close', None),
             'Volume': getattr(agg, 'volume', None)}
            for agg in aggs_iter
        ]

        if not agg_data:
            logger.print_warning(f"No Polygon data returned for '{mapped_ticker}' in the specified range.")
            return None

        df = pd.DataFrame(agg_data)
        df.dropna(subset=['DateTime'], inplace=True)
        if df.empty:
             logger.print_warning(f"Polygon data became empty after handling potential DateTime errors.")
             return None
        df.set_index('DateTime', inplace=True)

        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
             logger.print_error(f"Polygon data is missing required columns: {missing_cols}. Columns found: {list(df.columns)}")
             return None

        df.dropna(subset=required_cols, inplace=True)
        if df.empty:
             logger.print_warning(f"Polygon data for '{mapped_ticker}' became empty after removing NaN rows.")
             return None

        logger.print_success(f"Successfully fetched and processed {len(df)} rows from Polygon.io.")
        if len(agg_data) == 50000: logger.print_warning("Reached Polygon API limit (50k bars). Result may be incomplete. Pagination not implemented.")
        return df

    except BadResponse as e:
        # ... (Error handling for BadResponse remains the same) ...
        logger.print_error(f"Polygon API Error: {e}")
        response = getattr(e, 'response', None)
        if response is not None:
            url = getattr(response, 'url', 'N/A')
            status_code = getattr(response, 'status_code', 'N/A')
            logger.print_error(f"  URL: {url}")
            logger.print_error(f"  Status Code: {status_code}")
            try:
                response_details = response.json()
                logger.print_error(f"  Details: {response_details}")
            except Exception as e:
                 raw_text = getattr(response, 'text', 'N/A')
                 logger.print_error(f"An unexpected error occurred for ticker : {type(e).__name__}: {e}")
                 logger.print_error(f"  Raw Response Text (truncated): {raw_text[:500]}...")
        else:
             logger.print_error("  (Could not retrieve response details from exception)")
        return None
    # noinspection PyBroadException
    except Exception as e:
        # ... (Error handling for general Exception remains the same) ...
        logger.print_error(f"\n--- ERROR FETCHING/PROCESSING POLYGON ---")
        logger.print_error(f"An unexpected error occurred for ticker '{ticker}': {type(e).__name__}: {e}")
        import traceback
        tb_str = traceback.format_exc()
        try: print(f"{logger.ERROR_COLOR}Traceback:\n{tb_str}{logger.RESET_ALL}")
        except AttributeError: print(f"Traceback:\n{tb_str}")
        logger.print_error(f"--- END POLYGON ERROR ---")
        return None
