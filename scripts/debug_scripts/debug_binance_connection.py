# debug_binance_connection.py

"""
Standalone script to test Binance connection and data fetching using the binance_fetcher module.
Ensure BINANCE_API_KEY and BINANCE_API_SECRET are optionally set in your .env file
(though historical klines usually don't require them).
"""

import os
import sys
import traceback
from datetime import datetime, timedelta

# --- Add project root to sys.path ---
# This allows importing modules from 'src' when running this script from any directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
# -----------------------------------

# Attempt to load environment variables
try:
    from dotenv import load_dotenv
    dotenv_loaded = load_dotenv()
    if not dotenv_loaded:
        print("Warning: Could not find or load .env file. API keys must be set as environment variables if needed.")
except ImportError:
    print("Warning: python-dotenv not installed. Cannot load .env file.")
    dotenv_loaded = False


# Import logger and fetcher components within a try-except block
# to handle potential import errors gracefully in a standalone script
try:
    from src.common import logger
    from src.data.fetchers.binance_fetcher import (
        fetch_binance_data,
        BINANCE_AVAILABLE,
        BinanceAPIException,
        BinanceRequestException,
        BinanceClient # Import the actual client class for direct testing if needed
    )
except ImportError as e:
    print(f"Error importing project modules: {e}")
    print("Ensure the script is run from the project root directory containing 'src'.")
    sys.exit(1)


# --- Configuration ---
# Define parameters for the test fetch
# Use a recent, short period for a quick test
TEST_TICKER = "BTCUSDT"  # Example Ticker
TEST_INTERVAL = "M1"     # Example Interval (e.g., 'M1', 'H1', 'D1')
TEST_END_DATE = datetime.now().date()
TEST_START_DATE = TEST_END_DATE - timedelta(days=1) # Fetch 1 day of M1 data

TEST_START_STR = TEST_START_DATE.strftime('%Y-%m-%d')
TEST_END_STR = TEST_END_DATE.strftime('%Y-%m-%d')


# --- Main Execution ---
def main():
    """Main function to run the Binance connection and fetch test."""
    logger.print_info("--- Binance Connection & Fetch Debug Script ---")

    # Check if the Binance library is installed
    if not BINANCE_AVAILABLE:
        logger.print_error("Binance Connector library ('python-binance') is not installed.")
        logger.print_error("Please install it: pip install python-binance")
        sys.exit(1)
    else:
        logger.print_success("Binance Connector library found.")

    # --- Optional: Test Basic Client Initialization & Ping ---
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if api_key and api_secret:
         logger.print_info("API Key and Secret found in environment.")
         try:
              client = BinanceClient(api_key=api_key, api_secret=api_secret)
              logger.print_info("Attempting to ping Binance API...")
              ping_result = client.ping()
              # Note: ping() returns an empty dict {} on success
              logger.print_success(f"Binance API ping successful: {ping_result}")
              # Optional: Get server time
              server_time = client.get_server_time()
              server_dt = datetime.fromtimestamp(server_time['serverTime'] / 1000)
              logger.print_success(f"Binance Server Time: {server_dt}")

         except (BinanceAPIException, BinanceRequestException) as e:
              logger.print_error(f"Binance API Error during ping/time check: {e}")
         except Exception as e:
              logger.print_error(f"Unexpected error during client init/ping: {type(e).__name__}: {e}")
              logger.print_error(traceback.format_exc())
    else:
         logger.print_warning("BINANCE_API_KEY or BINANCE_API_SECRET not found. Skipping ping test.")
         logger.print_info("Proceeding with public data fetch attempt...")
    # -------------------------------------------------------


    # --- Test fetch_binance_data Function ---
    logger.print_info(f"\nAttempting to fetch data using fetch_binance_data:")
    logger.print_info(f"  Ticker:   {TEST_TICKER}")
    logger.print_info(f"  Interval: {TEST_INTERVAL}")
    logger.print_info(f"  Start:    {TEST_START_STR}")
    logger.print_info(f"  End:      {TEST_END_STR}")

    try:
        # Call the main fetch function from the fetcher module
        result = fetch_binance_data(
            ticker=TEST_TICKER,
            interval=TEST_INTERVAL,
            start_date=TEST_START_STR,
            end_date=TEST_END_STR
        )

        # Check if result is a tuple (df, metadata)
        if isinstance(result, tuple) and len(result) >= 1:
            df = result[0]  # Extract the DataFrame from the tuple
            # Process results
            if df is not None and not df.empty:
                logger.print_success(f"Successfully fetched {len(df)} rows of data.")
                logger.print_info("DataFrame Info:")
                df.info()
                logger.print_info("\nDataFrame Head:")
                print(df.head().to_string())
                logger.print_info("\nDataFrame Tail:")
                print(df.tail().to_string())
            elif df is not None and df.empty:
                logger.print_warning("Data fetch was successful, but the returned DataFrame is empty.")
                logger.print_warning("Check the date range and ticker validity for the selected period.")
            else:
                # fetch_binance_data should have logged the error already
                logger.print_error("Data fetch failed. See previous logs for details.")
        else:
            # Handle case where result is not a tuple but a direct DataFrame
            df = result
            if df is not None and not df.empty:
                logger.print_success(f"Successfully fetched {len(df)} rows of data.")
                logger.print_info("DataFrame Info:")
                df.info()
                logger.print_info("\nDataFrame Head:")
                print(df.head().to_string())
                logger.print_info("\nDataFrame Tail:")
                print(df.tail().to_string())
            elif df is not None and df.empty:
                logger.print_warning("Data fetch was successful, but the returned DataFrame is empty.")
                logger.print_warning("Check the date range and ticker validity for the selected period.")
            else:
                logger.print_error("Data fetch failed. See previous logs for details.")

    except (BinanceAPIException, BinanceRequestException) as e:
        # Catch potential API errors not caught inside fetch_binance_data (should be rare)
        logger.print_error(f"Binance API Error occurred during fetch: {e}")
        logger.print_error(traceback.format_exc())
    except ValueError as e:
        # Catch potential ValueErrors (e.g., invalid dates)
        logger.print_error(f"Input Error: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        logger.print_error(f"An unexpected error occurred: {type(e).__name__}: {e}")
        logger.print_error(traceback.format_exc())

    logger.print_info("\n--- Debug script finished ---")


# --- Script Entry Point ---
if __name__ == "__main__":
    main()

