# NeoZorK HLD/test_oanda_connection.py

import os
import sys
import json # To pretty-print the API response
from dotenv import load_dotenv # Import only load_dotenv
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
from oandapyV20.exceptions import V20Error

# Load environment variables from .env file in the project root
# load_dotenv() now searches for the .env file automatically.
# It returns True if a .env file was found and loaded, False otherwise.
if not load_dotenv():
    # Checks if loading the .env file failed (e.g., file not found).
    print("[Warning] Could not load .env file. Assuming keys are set as environment variables.")

print("--- Testing Oanda V20 API Connection ---")

# Get credentials from environment variables
# Retrieves the API token from environment variables.
api_token = os.getenv("OANDA_API_TOKEN")
# Retrieves the Account ID from environment variables.
account_id = os.getenv("OANDA_ACCOUNT_ID")

# --- Check if Credentials Exist ---
# Checks if both the token and account ID were successfully retrieved.
if not api_token:
    print("\n[Error] OANDA_API_TOKEN not found.")
    print("Please ensure it is set in your .env file or environment variables.")
    sys.exit(1) # Exit if token is missing

if not account_id:
    print("\n[Error] OANDA_ACCOUNT_ID not found.")
    print("Please ensure it is set in your .env file or environment variables.")
    sys.exit(1) # Exit if account ID is missing

print(f"Successfully loaded OANDA_ACCOUNT_ID: ...{account_id[-4:]}") # Print last 4 chars for confirmation
print("OANDA_API_TOKEN loaded (token is kept hidden).")

# --- Connect to Oanda API (Practice environment by default) ---
# Define the API environment ('practice' or 'live'). Recommend starting with 'practice'.
oanda_environment = "practice"
# Creates an API client instance using the loaded token and specified environment.
api = oandapyV20.API(environment=oanda_environment, access_token=api_token)

print(f"\nAttempting to connect to Oanda {oanda_environment} environment...")

# --- Make a Test API Call (Get Account Summary) ---
# Creates a request object for the Account Summary endpoint using the loaded account ID.
r = accounts.AccountSummary(accountID=account_id)

try:
    # Executes the API request.
    response = api.request(r)
    print("\n[Success] API request successful!")
    print("\nAccount Summary Response:")
    # Prints the API response in a nicely formatted JSON structure.
    # indent=2 makes the JSON output readable.
    print(json.dumps(response, indent=2))

except V20Error as err:
    # Catches specific errors from the oandapyV20 library.
    print(f"\n[Error] Oanda V20 API Error: {err}")
    print(f"HTTP status code: {getattr(err, 'code', 'N/A')}") # Display HTTP status code if available
    # If response body is available in error, print it
    error_body = getattr(err, 'msg', '{}')
    try:
        # Attempt to pretty-print the error message body if it's JSON
        print("Error Body:")
        print(json.dumps(json.loads(error_body), indent=2))
    except json.JSONDecodeError:
         # Otherwise, print the raw message
        print(f"Raw Error Message: {error_body}")

except Exception as e:
    # Catches any other unexpected errors during the API call.
    print(f"\n[Error] An unexpected error occurred: {type(e).__name__}: {e}")
    import traceback
    # Prints the full traceback for debugging general errors.
    traceback.print_exc()

print(f"\n--- End of Oanda Test ---")