# NeoZorK HLD/test_polygon_connection.py

import os
import sys
import pandas as pd
#import json
from datetime import date, timedelta
from dotenv import load_dotenv
# Import the RESTClient from the polygon package
# Note: The package installed is polygon-api-client, but it's imported as 'polygon'
# noinspection PackageRequirements
# 2 Week Warnings -> simply Ignore this!!!
import polygon
from polygon.exceptions import BadResponse

# Load environment variables from .env file
# Loads environment variables from a .env file if it exists.
if not load_dotenv():
    print("[Warning] Could not load .env file. Assuming keys are set as environment variables.")

print("--- Testing Polygon.io API Connection ---")

# Get API key from environment variables
# Retrieves the Polygon API key from environment variables.
api_key = os.getenv("POLYGON_API_KEY")

# --- Check if API Key Exists ---
# Checks if the API key was successfully retrieved.
if not api_key:
    print("\n[Error] POLYGON_API_KEY not found.")
    print("Please ensure it is set in your .env file or environment variables.")
    sys.exit(1) # Exit if key is missing

print("Successfully loaded POLYGON_API_KEY (key is kept hidden).")

# --- Initialize Polygon REST Client ---
# Creates a REST API client instance using the loaded API key.
try:
    client = polygon.RESTClient(api_key=api_key)
    print("\nPolygon API client initialized successfully.")
except Exception as e:
     print(f"\n[Error] Failed to initialize Polygon client: {type(e).__name__}: {e}")
     sys.exit(1)

# --- Make a Test API Call (Get Aggregates) ---
# Define parameters for the test call
# Sets the stock ticker symbol for the test request.
test_ticker = "AAPL"
# Sets the multiplier for the timespan (e.g., 1 for 1 day).
multiplier = 1
# Sets the timespan (e.g., 'day', 'hour', 'minute').
timespan = "day"
# Calculates the end date (today).
end_date = date.today()
# Calculates the start date (5 days ago).
start_date = end_date - timedelta(days=5)

print(f"\nAttempting to fetch '{multiplier} {timespan}' aggregates for '{test_ticker}'")
print(f"From: {start_date} To: {end_date}")

try:
    # Executes the get_aggs API request.
    # This function often returns a generator or an iterator.
    aggs_response = client.get_aggs(
        ticker=test_ticker,
        multiplier=multiplier,
        timespan=timespan,
        from_=start_date,
        to=end_date,
        # limit=5 # Optionally limit the number of results directly
    )

    # Convert iterator/generator to list to easily check/print
    # Converts the response iterator to a list to make it easier to work with.
    aggs_list = list(aggs_response)

    # Checks if the list of aggregates is empty.
    if not aggs_list:
         print("\n[Success] API request successful, but no aggregates returned for the specified period.")
    else:
        print(f"\n[Success] API request successful! Received {len(aggs_list)} aggregate bar(s).")
        print("\nFirst few aggregate bars:")
        # Iterates through the first 5 aggregates (or fewer if less were returned).
        for i, agg in enumerate(aggs_list[:5]):
            # Converts the timestamp (likely Unix ms) to a readable datetime object.
            ts_readable = pd.to_datetime(agg.timestamp, unit='ms') if hasattr(agg, 'timestamp') else 'N/A'
            # Prints details for each aggregate bar. Uses getattr for safe access to attributes.
            print(
                f"  - Timestamp: {ts_readable}, "
                f"Open: {getattr(agg, 'open', 'N/A')}, "
                f"High: {getattr(agg, 'high', 'N/A')}, "
                f"Low: {getattr(agg, 'low', 'N/A')}, "
                f"Close: {getattr(agg, 'close', 'N/A')}, "
                f"Volume: {getattr(agg, 'volume', 'N/A')}"
            )

    # Optionally, you can convert the list of aggregates to a DataFrame for easier manipulation.
except BadResponse as e:
    # Handles specific API errors returned by Polygon (e.g., bad key, rate limit).
    print(f"\n[Error] Polygon API Error: {e}")
    # Tries to get specific details from the error if available.
    print(f"  URL: {getattr(e, 'response', {}).get('url', 'N/A')}")
    print(f"  Status Code: {getattr(e, 'status_code', 'N/A')}")
    # Consider printing response text if helpful and available: print(f"  Response Text: {getattr(e, 'response', {}).get('text', 'N/A')}")
# General exceptions
except Exception as e:
    # Catches any other unexpected errors.
    print(f"\n[Error] An unexpected error occurred: {type(e).__name__}: {e}")
    import traceback
    # Prints the full traceback for debugging.
    traceback.print_exc()

print(f"\n--- End of Polygon Test ---")