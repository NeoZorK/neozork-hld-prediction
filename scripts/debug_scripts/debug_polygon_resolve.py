# debug_polygon_resolve.py

import os
import traceback
from dotenv import load_dotenv

# Polygon specific imports
try:
    # noinspection PyUnresolvedReferences,PackageRequirements
    import polygon
    from polygon.exceptions import BadResponse
    POLYGON_AVAILABLE = True
except ImportError:
    POLYGON_AVAILABLE = False
    class BadResponse(Exception): pass
    print("ERROR: polygon-api-client library not found. Install it first.")
    exit()

# --- Load Environment Variables ---
if not load_dotenv():
    print("Warning: Could not load .env file.")

print("--- Polygon Ticker Detail Debug ---")

# --- Get API Key ---
api_key = os.getenv("POLYGON_API_KEY")
if not api_key:
    print("ERROR: POLYGON_API_KEY not found in environment variables or .env file.")
    exit()
else:
    print("POLYGON_API_KEY loaded.")

# --- Initialize Client ---
try:
    # noinspection PyUnresolvedReferences
    client = polygon.RESTClient(api_key=api_key)
    print("Polygon client initialized.")
except Exception as e:
    print(f"ERROR: Failed to initialize Polygon client: {type(e).__name__}: {e}")
    exit()

# --- Test Tickers ---
tickers_to_test = [
    'EURUSD',        # Expected to fail with 404
    'C:EURUSD',      # Expected to succeed
    'BTCUSD',        # Expected to fail with 404
    'X:BTCUSD',      # Expected to succeed
    'AAPL',          # Expected to succeed
    'INVALIDTICKER'  # Expected to fail with 404
]

print("\n--- Starting Ticker Detail Tests ---")

for ticker in tickers_to_test:
    print(f"\nTesting ticker: '{ticker}'...")
    try:
        # Attempt to get details
        details_response = client.get_ticker_details(ticker)
        # If successful (no exception)
        print(f"[SUCCESS] Found ticker '{ticker}'. Response type: {type(details_response)}")
        # Optionally print some details if needed:
        # print(f"  Name: {getattr(details_response.results, 'name', 'N/A')}")
        # print(f"  Market: {getattr(details_response.results, 'market', 'N/A')}")

    except BadResponse as e:
        print(f"[BAD RESPONSE CAUGHT] for '{ticker}'. Exception: {e}")
        # --- Try to extract details from the exception ---
        response = getattr(e, 'response', None)
        status_code = None
        if response is not None:
            print(f"  Exception has response object of type: {type(response)}")
            status_code = getattr(response, 'status_code', None)
            print(f"  Extracted status code: {status_code}")
            if status_code == 404:
                print("  STATUS IS 404 (Not Found)")
            else:
                print(f"  STATUS IS NOT 404 (or unknown)")
                # Try logging details for non-404 BadResponse
                try:
                    url = getattr(response, 'url', 'N/A')
                    print(f"    URL: {url}")
                    response_details = response.json()
                    print(f"    Details: {response_details}")
                except Exception as detail_err:
                    raw_text = getattr(response, 'text', 'N/A')
                    print(f"    Could not get details from response object: {detail_err}")
                    print(f"    Raw Response Text (truncated): {raw_text[:500]}...")
        else:
            print("  Exception did NOT contain a 'response' attribute.")

    except Exception as e:
        print(f"[UNEXPECTED EXCEPTION CAUGHT] for '{ticker}': {type(e).__name__}: {e}")
        print(f"  Traceback:\n{traceback.format_exc()}")

print("\n--- End of Ticker Detail Tests ---")