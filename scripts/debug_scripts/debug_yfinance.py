# debug_yfinance.py
import yfinance as yf
import pandas as pd
import json
import time
import requests

ticker = 'AAPL'
period = '1mo'
interval = '1d'

print(f"--- Minimal YFinance Test ---")
print(f"Attempting to download: Ticker={ticker}, Period={period}, Interval={interval}")

try:
    # Set display options for pandas DataFrame
    pd.set_option('display.max_rows', 10)
    pd.set_option('display.max_columns', 10)
    yf.set_tz_cache_location(".yf_cache") # Set cache location for yfinance

    # Skip ticker validation step that triggers 429 errors
    # and directly try to download the data
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            data = yf.download(
                tickers=ticker,
                period=period,
                interval=interval,
                progress=True,
                auto_adjust=True,  # Changed to True for better compatibility
                prepost=False,
                actions=False,
                ignore_tz=True,    # Ignore timezone issues
                threads=False      # Single-threaded for better reliability
            )

            if data is None or data.empty:
                print("\n[Error] yf.download returned None or empty DataFrame.")
            else:
                print(f"\n[Success] Downloaded {len(data)} rows.")
                print("First 5 rows:")
                print(data.head())
                print("\nLast 5 rows:")
                print(data.tail())
                print("\nColumns:", data.columns.tolist())
                required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                missing_cols = [col for col in required_cols if col not in data.columns]
                if missing_cols:
                    print(f"\n[Warning] Missing required columns: {missing_cols}")
                else:
                    print(f"\n[Info] All required columns present.")
            # If we got here, no need to retry
            break

        except requests.exceptions.HTTPError as e:
            if "429" in str(e):
                print(f"[Rate Limit] Attempt {attempt+1}/{max_retries}: Too many requests (HTTP 429)")
                if attempt < max_retries - 1:
                    print(f"Waiting {retry_delay} seconds before retrying...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print("Maximum retries reached. Could not download data due to rate limiting.")
            else:
                # Re-raise if it's not a rate limit error
                raise
        except json.decoder.JSONDecodeError:
            print(f"Failed to get ticker '{ticker}' reason: JSON decode error - API may be temporarily unavailable")
            print("\n[Error] yf.download returned None or empty DataFrame.")
            break
        except KeyError:
            print(f"Failed to get ticker '{ticker}' reason: Invalid ticker symbol or no data available")
            print("\n[Error] yf.download returned None or empty DataFrame.")
            break

except Exception as e:
    print(f"\n--- ERROR ---")
    print(f"An exception occurred during yf.download:")
    print(f"Exception Type: {type(e).__name__}")
    print(f"Exception Details: {e}")
    # Suppress full traceback for cleaner output
    print(f"--- END ERROR ---")

print(f"\n--- End of Test ---")