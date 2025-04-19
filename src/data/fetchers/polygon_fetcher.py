# src/data/fetchers/polygon_fetcher.py # CORRECTED Import Statement
# -*- coding: utf-8 -*-
"""
Module for fetching historical OHLCV data from Polygon.io API.

Handles ticker resolution (Stocks, Forex, Crypto), date range chunking,
API rate limiting (429 errors) with exponential backoff, and error handling.
"""

import os
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple, List
import traceback # Import traceback for detailed error logging

import pandas as pd

# Import polygon library safely
try:
    # noinspection PyPackageRequirements
    from polygon import RESTClient
    # noinspection PyPackageRequirements
    from polygon.exceptions import BadResponse
    # noinspection PyPackageRequirements
    from polygon.rest.models import Agg
    POLYGON_AVAILABLE = True
except ImportError:
    POLYGON_AVAILABLE = False
    # Define dummy classes/exceptions if polygon is not available
    # This helps with type hinting and basic structure checks even without the lib
    class RESTClient: # type: ignore
        def __init__(self, api_key=None): pass
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): pass
        # Add dummy methods that are called if needed
        def get_ticker_details(self, ticker): raise NotImplementedError
        def get_aggs(self, **kwargs): raise NotImplementedError

    class BadResponse(Exception): # type: ignore
        response = None # Add response attribute expected by error handling

    class Agg: # type: ignore
        timestamp = None; open = None; high = None; low = None; close = None; volume = None

# ***** CORRECTED IMPORT *****
# Use the correct path relative to the src directory
from src.common.logger import log_info, log_warning, log_error, log_debug

# Constants
MAX_DATE_RANGE_YEARS = 2 # Polygon limit per request (adjust if needed)
MAX_POLYGON_LIMIT = 50000 # Max aggregates per request
MAX_ATTEMPTS_PER_CHUNK = 5 # Max retries for a single date chunk
RETRY_DELAY_SECONDS = 1.0 # Initial delay for retries

# Polygon interval mapping (Input: MQL5 or standard -> Output: Tuple[str, int])
POLYGON_INTERVAL_MAP = {
    # MQL5 Timeframes
    "M1": ("minute", 1), "M5": ("minute", 5), "M15": ("minute", 15), "M30": ("minute", 30),
    "H1": ("hour", 1), "H4": ("hour", 4),
    "D1": ("day", 1), "W1": ("week", 1), "MN1": ("month", 1),
    # Standard names (case-insensitive check done in function)
    "MINUTE": ("minute", 1), "HOUR": ("hour", 1),
    "DAY": ("day", 1), "WEEK": ("week", 1), "MONTH": ("month", 1)
}


#
# Map MQL5/standard interval strings to Polygon timespan and multiplier.
#
# Args:
#     interval (str): The interval string (e.g., "H1", "D1", "minute").
#
# Returns:
#     Optional[Tuple[str, int]]: A tuple (timespan, multiplier) or None if invalid.
#
def map_polygon_interval(interval: str) -> Optional[Tuple[str, int]]:
    """
    Maps MQL5/standard interval strings to Polygon timespan and multiplier.

    Args:
        interval (str): The interval string (e.g., "H1", "D1", "minute").

    Returns:
        Optional[Tuple[str, int]]: A tuple (timespan, multiplier) or None if invalid.
    """
    interval_upper = interval.upper()
    # Direct match for standard polygon names (allow passing through)
    if interval_upper in ["MINUTE", "HOUR", "DAY", "WEEK", "MONTH"]:
        # Default multiplier is 1 if only timespan is given
        # Check if interval string contains a multiplier (e.g., "5minute") - advanced usage
        try:
            if interval_upper[0].isdigit():
                multiplier_str = ""
                timespan_str = ""
                for char in interval_upper:
                    if char.isdigit():
                        multiplier_str += char
                    else:
                        timespan_str += char
                multiplier = int(multiplier_str)
                timespan = timespan_str.lower()
                if timespan in ["minute", "hour", "day", "week", "month"]:
                     return timespan, multiplier
                else:
                     return None # Invalid timespan part
            else:
                 # Standard name without multiplier prefix
                 return interval_upper.lower(), 1
        except ValueError:
            return None # Invalid format

    # Check MQL5 mapping
    return POLYGON_INTERVAL_MAP.get(interval.upper())


#
# Resolve the ticker string, trying different prefixes (C:, X:, I:) if initial lookup fails.
# Handles 404 errors specifically during resolution.
#
# Args:
#     ticker (str): The original ticker symbol (e.g., "AAPL", "EURUSD", "BTCUSD").
#     client (RESTClient): An authenticated Polygon RESTClient instance.
#
# Returns:
#     Optional[str]: The resolved ticker string (e.g., "AAPL", "C:EURUSD", "X:BTCUSD") or None if not found.
#
def resolve_polygon_ticker(ticker: str, client: 'RESTClient') -> Optional[str]:
    """
    Resolves the ticker string, trying different prefixes (C:, X:, I:) if initial lookup fails.
    Handles 404 errors specifically during resolution.

    Args:
        ticker (str): The original ticker symbol (e.g., "AAPL", "EURUSD", "BTCUSD").
        client (RESTClient): An authenticated Polygon RESTClient instance.

    Returns:
        Optional[str]: The resolved ticker string (e.g., "AAPL", "C:EURUSD", "X:BTCUSD") or None if not found.
    """
    if not POLYGON_AVAILABLE: # Add check if library wasn't imported
        log_error("Polygon library not available for ticker resolution.")
        return None

    prefixes_to_try = ["", "C:", "X:", "I:"] # Stocks (default), Forex, Crypto, Indices
    initial_ticker_upper = ticker.upper()

    for prefix in prefixes_to_try:
        current_ticker = f"{prefix}{initial_ticker_upper}"
        log_debug(f"Attempting to resolve Polygon ticker: {current_ticker}")
        try:
            # Use get_ticker_details or similar lightweight call to check existence
            _ = client.get_ticker_details(current_ticker)
            log_info(f"Successfully resolved Polygon ticker as: {current_ticker}")
            return current_ticker
        except BadResponse as e:
            status_code = getattr(e.response, 'status_code', None)
            if status_code == 404:
                log_debug(f"Ticker {current_ticker} not found (404), trying next prefix...")
                time.sleep(0.2) # Short delay before trying next prefix
                continue # Try next prefix
            else:
                # Handle other API errors during resolution
                err_msg = getattr(e, 'message', str(e))
                response_text = getattr(e.response, 'text', 'No response text') if hasattr(e, 'response') else 'No response'
                log_error(f"Polygon API error resolving ticker {current_ticker} (Status: {status_code}): {err_msg}. Response: {response_text}")
                return None # Stop resolution attempts on non-404 errors
        except Exception as e:
            log_error(f"Unexpected error resolving Polygon ticker {current_ticker}: {e}")
            log_debug(traceback.format_exc()) # Log full traceback for debugging
            return None # Stop resolution attempts on unexpected errors

    log_error(f"Failed to resolve Polygon ticker '{ticker}' after trying all prefixes.")
    return None


#
# Fetch historical OHLCV data from Polygon.io.
#
# Args:
#     ticker (str): The ticker symbol (e.g., "AAPL", "EURUSD", "XBTUSD").
#     interval (str): The data interval (e.g., "D1", "H1", "minute").
#     start_date_str (str): Start date in "YYYY-MM-DD" format.
#     end_date_str (str): End date in "YYYY-MM-DD" format.
#
# Returns:
#     Optional[pd.DataFrame]: DataFrame with OHLCV data indexed by Datetime, or None on failure.
#                              Columns: ['Open', 'High', 'Low', 'Close', 'Volume']
#
def fetch_polygon_data(
    ticker: str,
    interval: str,
    start_date_str: str,
    end_date_str: str
) -> Optional[pd.DataFrame]:
    """
    Fetches historical OHLCV data from Polygon.io.

    Args:
        ticker (str): The ticker symbol (e.g., "AAPL", "EURUSD", "XBTUSD").
        interval (str): The data interval (e.g., "D1", "H1", "minute").
        start_date_str (str): Start date in "YYYY-MM-DD" format.
        end_date_str (str): End date in "YYYY-MM-DD" format.

    Returns:
        Optional[pd.DataFrame]: DataFrame with OHLCV data indexed by Datetime, or None on failure.
                                 Columns: ['Open', 'High', 'Low', 'Close', 'Volume']
    """
    if not POLYGON_AVAILABLE:
        log_error("Polygon library not installed. Cannot fetch data. pip install polygon-api-client")
        return None

    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        log_error("POLYGON_API_KEY environment variable not set.")
        return None

    interval_map = map_polygon_interval(interval)
    if interval_map is None:
        log_error(f"Invalid or unsupported interval for Polygon: {interval}")
        return None
    timespan, multiplier = interval_map

    try:
        # Use context manager for the client
        with RESTClient(api_key) as client:
            # 1. Resolve Ticker
            resolved_ticker = resolve_polygon_ticker(ticker, client)
            if resolved_ticker is None:
                # Error already logged in resolve_polygon_ticker
                return None

            # 2. Prepare Dates
            try:
                overall_start_dt = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                overall_end_dt = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                log_error(f"Invalid date format. Use YYYY-MM-DD. Received: start='{start_date_str}', end='{end_date_str}'")
                return None

            if overall_start_dt > overall_end_dt:
                log_error(f"Start date ({start_date_str}) cannot be after end date ({end_date_str}).")
                return None

            log_info(f"Fetching Polygon data for {resolved_ticker} ({timespan}*{multiplier}) from {overall_start_dt} to {overall_end_dt}")

            # 3. Fetch data in chunks
            all_aggs_data: List[Agg] = []
            current_start_dt = overall_start_dt

            # --- Date Chunking Loop ---
            while current_start_dt <= overall_end_dt:
                # Calculate end date for this chunk (max ~2 years)
                # Ensure calculation doesn't create invalid date ranges
                if MAX_DATE_RANGE_YEARS <= 0: # Avoid infinite loop or errors if constant is invalid
                    log_error("Invalid MAX_DATE_RANGE_YEARS configuration.")
                    return None
                # Calculate max end date based on years, approximately
                max_chunk_end_dt = current_start_dt + timedelta(days=int(MAX_DATE_RANGE_YEARS * 365.25) -1)
                current_end_dt = min(max_chunk_end_dt, overall_end_dt)

                log_debug(f"Processing chunk: {current_start_dt} to {current_end_dt}")

                # --- Retry loop for the current date chunk ---
                attempt = 0
                chunk_data = None # Initialize/reset for this chunk iteration
                while attempt < MAX_ATTEMPTS_PER_CHUNK:
                    try:
                        # *** API CALL MOVED INSIDE RETRY LOOP ***
                        log_debug(f"Polygon API Call attempt {attempt+1}/{MAX_ATTEMPTS_PER_CHUNK} for {current_start_dt} to {current_end_dt}")
                        chunk_aggs_iter = client.get_aggs(
                            ticker=resolved_ticker,
                            multiplier=multiplier,
                            timespan=timespan,
                            from_=current_start_dt,
                            to=current_end_dt,
                            adjusted=False,
                            limit=MAX_POLYGON_LIMIT
                        )

                        # *** CONVERT ITERATOR INSIDE TRY BLOCK ***
                        chunk_data = list(chunk_aggs_iter) # Consume iterator here
                        log_debug(f"Successfully fetched {len(chunk_data)} aggregates for chunk.")
                        break # Exit retry loop on success

                    except BadResponse as e:
                        status_code = getattr(e.response, 'status_code', None)
                        if status_code == 429 and attempt < MAX_ATTEMPTS_PER_CHUNK - 1:
                            # Exponential backoff for rate limiting
                            sleep_time = RETRY_DELAY_SECONDS * (2 ** attempt)
                            log_warning(f"Polygon API rate limit (429) hit on attempt {attempt + 1}. Retrying in {sleep_time:.2f} seconds...")
                            time.sleep(sleep_time)
                            attempt += 1
                            # Continue to next attempt, API call will be re-issued
                        else:
                            # Log non-429 or final 429 error and exit fetch
                            err_msg = getattr(e, 'message', str(e))
                            response_text = getattr(e.response, 'text', 'No response text') if hasattr(e, 'response') else 'No response'
                            log_error(f"Polygon API error (Status: {status_code}) fetching chunk {current_start_dt}-{current_end_dt}: {err_msg}. Response: {response_text}")
                            return None # Exit the entire fetch function
                    except Exception as e:
                        log_error(f"Unexpected error during Polygon API call/processing for chunk {current_start_dt}-{current_end_dt}: {e}")
                        log_debug(traceback.format_exc()) # Log full traceback
                        return None # Exit fetch function
                # --- End of Retry loop ---

                if chunk_data is not None:
                    all_aggs_data.extend(chunk_data)
                else:
                    # This implies all retry attempts failed for the chunk, but no critical error returned None above.
                    log_warning(f"Failed to fetch data for chunk {current_start_dt} to {current_end_dt} after all attempts. Continuing...")
                    # Decide if fetching should continue or stop. Current logic continues.

                # Move to the next chunk start date
                current_start_dt = current_end_dt + timedelta(days=1)

                # Add delay between date range chunks if looping
                if current_start_dt <= overall_end_dt:
                    time.sleep(0.2) # Shorter delay between chunks now

            # --- End of Date Chunking loop ---

            if not all_aggs_data:
                log_warning(f"No data returned from Polygon for {ticker} between {overall_start_dt} and {overall_end_dt}.")
                return None

            # 4. Convert to DataFrame
            log_info(f"Received {len(all_aggs_data)} total aggregates from Polygon.")
            df = pd.DataFrame([{
                'DateTime': agg.timestamp,
                'Open': agg.open,
                'High': agg.high,
                'Low': agg.low,
                'Close': agg.close,
                'Volume': agg.volume
            } for agg in all_aggs_data if hasattr(agg, 'timestamp')]) # Add check for timestamp attr

            if df.empty:
                 log_warning(f"DataFrame is empty after processing Polygon aggregates.")
                 return None

            # Convert timestamp to datetime objects and set as index
            df['DateTime'] = pd.to_datetime(df['DateTime'], unit='ms')
            df.set_index('DateTime', inplace=True)

            # Ensure correct dtypes
            try:
                df = df.astype({'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': float})
            except Exception as e:
                 log_error(f"Failed to convert Polygon data columns to float: {e}")
                 log_debug(f"DataFrame before conversion error:\n{df.head()}\n{df.dtypes}")
                 return None


            # Sort by DateTime index
            df.sort_index(inplace=True)

            # Filter data strictly within the requested start/end date (inclusive)
            # Convert string dates to datetime objects for comparison
            start_datetime = datetime.strptime(start_date_str, "%Y-%m-%d")
            # For end date, include the whole day by setting time to end of day
            end_datetime = datetime.strptime(end_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999999)

            df = df[(df.index >= start_datetime) & (df.index <= end_datetime)]

            if df.empty:
                 log_warning(f"DataFrame became empty after filtering for requested date range {start_date_str} to {end_date_str}.")
                 return None

            log_info(f"Successfully created DataFrame with shape {df.shape} after date filtering.")
            return df

    except Exception as e:
        log_error(f"An unexpected error occurred during Polygon data fetch setup or final processing: {e}")
        log_debug(traceback.format_exc()) # Log full traceback
        return None

# Example usage (for testing module directly)
if __name__ == "__main__":
    # Set path to load .env file from project root assuming script is run from root
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env') # Adjust path as needed
    load_dotenv(dotenv_path=dotenv_path)
    # print(f"Attempting to load .env from: {dotenv_path}")
    # print(f"POLYGON_API_KEY loaded: {'Yes' if os.getenv('POLYGON_API_KEY') else 'No'}")


    log_info("Testing Polygon Fetcher...")

    # Test case 1: Stock data (Short range)
    aapl_df = fetch_polygon_data("AAPL", "D1", "2023-01-01", "2023-01-10")
    if aapl_df is not None:
        log_info("AAPL Data:")
        print(aapl_df.head())
        print(aapl_df.tail())
        print(f"Shape: {aapl_df.shape}")
    else:
        log_error("Failed to fetch AAPL data.")

    print("-" * 20)

    # Test case 2: Forex data (H1)
    eurusd_df = fetch_polygon_data("EURUSD", "H1", "2024-04-01", "2024-04-02")
    if eurusd_df is not None:
        log_info("EURUSD Data:")
        print(eurusd_df.head())
        print(eurusd_df.tail())
        print(f"Shape: {eurusd_df.shape}")
    else:
        log_error("Failed to fetch EURUSD data.")

    print("-" * 20)

    # Test case 3: Crypto data (M5, Short range)
    btcusd_df = fetch_polygon_data("X:BTCUSD", "M5", "2024-04-18", "2024-04-18") # Fetch for a single day
    if btcusd_df is not None:
        log_info("BTCUSD Data:")
        print(btcusd_df.head())
        print(btcusd_df.tail())
        print(f"Shape: {btcusd_df.shape}")
    else:
        log_error("Failed to fetch BTCUSD data.")

    print("-" * 20)

    # Test case 4: Invalid Ticker
    invalid_df = fetch_polygon_data("INVALIDTICKERXYZ987", "D1", "2023-01-01", "2023-01-02")
    if invalid_df is None:
        log_info("Correctly handled invalid ticker.")
    else:
        log_error("Failed to handle invalid ticker correctly.")

    print("-" * 20)

    # Test case 5: Longer range potentially requiring > 1 chunk (if MAX_DATE_RANGE_YEARS is small)
    # Set MAX_DATE_RANGE_YEARS = 1 temporarily for testing chunking if needed
    log_info("Testing longer range fetch (potential chunking)...")
    msft_long_df = fetch_polygon_data("MSFT", "D1", "2020-01-01", "2022-12-31") # 3 years
    if msft_long_df is not None:
        log_info("MSFT Long Data:")
        print(f"Shape: {msft_long_df.shape}")
        # Check start and end dates
        print(f"Start: {msft_long_df.index.min()}, End: {msft_long_df.index.max()}")
    else:
        log_error("Failed to fetch MSFT long data.")