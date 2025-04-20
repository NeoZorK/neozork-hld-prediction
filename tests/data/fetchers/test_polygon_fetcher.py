# tests/data/fetchers/test_polygon_fetcher.py

import unittest # <-- ADDED THIS LINE
from unittest.mock import patch, MagicMock, call, ANY
import pandas as pd
import time
import os
from datetime import datetime

# Attempt to import polygon and set a flag
try:
    import polygon
    from polygon.exceptions import BadResponse, NoResultsError
    POLYGON_AVAILABLE = True
except ImportError:
    POLYGON_AVAILABLE = False
    # Define dummy exceptions if polygon is not installed
    class BadResponse(Exception): pass
    class NoResultsError(Exception): pass

from src.data.fetchers.polygon_fetcher import fetch_polygon_data, resolve_polygon_ticker
from src.common.logger import print_info, print_warning, print_error, print_debug

# --- Helper function ---

# Function to create a mock Aggregate object
def create_mock_agg(timestamp, open_val, high_val, low_val, close_val, volume_val):
    # Creates a MagicMock object that behaves like a Polygon Aggregate object
    agg = MagicMock()
    agg.timestamp = timestamp # Milliseconds
    agg.open = open_val
    agg.high = high_val
    agg.low = low_val
    agg.close = close_val
    agg.volume = volume_val
    return agg

# --- Constants for conditional skip ---
# Decorator to skip tests if polygon is not installed

# --- Callable for time.perf_counter mock ---

# Class to mock time.perf_counter, simulating time increments
class MockTimer:
    # Simulates time.perf_counter for testing durations
    def __init__(self):
        self.current_time = 0.0
        self.increment = 0.1 # Default increment

    def __call__(self):
        # Returns the current time and increments it for the next call
        now = self.current_time
        self.current_time += self.increment
        return now

    def reset(self, start_time=0.0, increment=0.1):
        # Resets the timer's state for a new test
        self.current_time = start_time
        self.increment = increment

# Decorator to skip tests if polygon library is not available
@unittest.skipIf(not POLYGON_AVAILABLE, "Polygon library not installed, skipping tests")
class TestPolygonFetcher(unittest.TestCase):

    # Test case for successful ticker resolution (e.g., AAPL)
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_success_stock(self, mock_rest_client_class):
        # Tests successful resolution of a standard stock ticker.
        mock_client_instance = mock_rest_client_class.return_value
        mock_client_instance.get_ticker_details.return_value = MagicMock(ticker='AAPL') # Simulate successful details fetch
        print_debug(f"Attempting to get details for ticker: AAPL")

        resolved_ticker = resolve_polygon_ticker("AAPL", mock_client_instance)
        print_info(f"Resolved 'AAPL' to Polygon ticker: '{resolved_ticker}'")
        self.assertEqual(resolved_ticker, "AAPL")
        mock_client_instance.get_ticker_details.assert_called_once_with("AAPL")

    # Test case for successful ticker resolution (e.g., EURUSD)
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_success_forex(self, mock_rest_client_class):
        # Tests successful resolution of a Forex pair ticker.
        mock_client_instance = mock_rest_client_class.return_value
        # Simulate failure for stock, success for Forex (C:)
        mock_client_instance.get_ticker_details.side_effect = [
            BadResponse("Ticker Not Found", response=MagicMock(status_code=404)), # For "EURUSD"
            MagicMock(ticker='C:EURUSD') # For "C:EURUSD"
        ]

        print_debug(f"Attempting to get details for ticker: EURUSD")
        resolved_ticker = resolve_polygon_ticker("EURUSD", mock_client_instance)
        print_info(f"Resolved 'EURUSD' to Polygon ticker: '{resolved_ticker}'")
        self.assertEqual(resolved_ticker, "C:EURUSD")
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 2)
        mock_client_instance.get_ticker_details.assert_has_calls([call("EURUSD"), call("C:EURUSD")])

    # Test case for unsuccessful ticker resolution
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_not_found(self, mock_rest_client_class):
        # Tests scenario where the ticker cannot be resolved using common prefixes.
        mock_client_instance = mock_rest_client_class.return_value
        # Simulate 404 Not Found for all common prefixes
        mock_client_instance.get_ticker_details.side_effect = BadResponse("Ticker Not Found", response=MagicMock(status_code=404))

        resolved_ticker = resolve_polygon_ticker("NONEXISTENT", mock_client_instance)
        self.assertIsNone(resolved_ticker)
        # Check it tried Stock, Forex, Crypto, Index prefixes
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 4)
        mock_client_instance.get_ticker_details.assert_has_calls([
            call("NONEXISTENT"),
            call("C:NONEXISTENT"),
            call("X:NONEXISTENT"),
            call("I:NONEXISTENT")
        ], any_order=False)

    # Test case for API error during ticker resolution (non-404)
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_api_error(self, mock_rest_client_class):
        # Tests handling of non-404 API errors during ticker resolution.
        mock_client_instance = mock_rest_client_class.return_value
        # Simulate a 500 Server Error
        mock_response = MagicMock(status_code=500, url="mock_url_status_500")
        mock_response.json.return_value = {"error": "Server Error"}
        mock_client_instance.get_ticker_details.side_effect = BadResponse("Server Error", response=mock_response)

        resolved_ticker = resolve_polygon_ticker("ANYTICKER", mock_client_instance)
        self.assertIsNone(resolved_ticker)
        mock_client_instance.get_ticker_details.assert_called_once_with("ANYTICKER")

    # Test case for successful data fetch in a single chunk
    # Use new_callable to get a fresh timer instance for each test
    @patch('time.perf_counter', new_callable=MockTimer)
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_success_single_chunk(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        # Tests successful data retrieval within a single API call chunk.
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:AAPL"
        mock_client_instance = mock_rest_client_class.return_value
        mock_aggs_list = [ create_mock_agg(1672578000000, 130, 131, 129, 130.5, 10000) ]
        mock_client_instance.get_aggs.return_value = iter(mock_aggs_list)
        # Configure timer increment for this call
        mock_perf_counter.reset(start_time=50.0, increment=0.8)

        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 1)
        # FIX: Assert correct latency based on increment
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.8)
        # Verify perf_counter was called twice (start and end)
        # self.assertEqual(mock_perf_counter.call_count, 2) # <-- PREVIOUSLY REMOVED/COMMENTED OUT

        mock_client_instance.get_aggs.assert_called_once_with(
            ticker="T:AAPL",
            multiplier=1,
            timespan='minute',
            from_='2023-01-01',
            to='2023-01-01',
            adjusted=True,
            limit=50000
        )
        self.assertEqual(metrics['api_calls'], 1)
        self.assertEqual(metrics['successful_chunks'], 1)

    # Test case for successful data fetch with pagination
    @patch('time.perf_counter', new_callable=MockTimer)
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_pagination(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        # Tests successful data retrieval spanning multiple monthly chunks (pagination).
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:GE"
        mock_client_instance = mock_rest_client_class.return_value
        # Simulate two chunks of data
        mock_aggs_chunk1 = [create_mock_agg(1673784000000, 10, 11, 9, 10.5, 5000)] # Jan 15th
        mock_aggs_chunk2 = [create_mock_agg(1675341600000, 12, 13, 11, 12.5, 6000)] # Feb 2nd
        mock_client_instance.get_aggs.side_effect = [iter(mock_aggs_chunk1), iter(mock_aggs_chunk2)]
        # Configure timer: 0.7s for first chunk, 0.9s for second
        mock_perf_counter.reset(start_time=100.0, increment=0.7) # Initial increment for first call duration
        def perf_counter_side_effect():
            # Custom logic for perf_counter mock during pagination
            val = mock_perf_counter() # Use the MockTimer's logic
            # After the first chunk is processed, change increment for the second chunk
            if mock_client_instance.get_aggs.call_count >= 1:
                 mock_perf_counter.increment = 0.9
            return val
        mock_perf_counter.side_effect = perf_counter_side_effect # Use the custom side effect

        result = fetch_polygon_data(ticker="GE", interval="M1", start_date="2023-01-01", end_date="2023-02-01")
        df, metrics = result
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 2)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.7 + 0.9) # Sum of increments
        self.assertEqual(mock_client_instance.get_aggs.call_count, 2) # Check pagination occurred
        self.assertEqual(metrics['api_calls'], 2)
        self.assertEqual(metrics['successful_chunks'], 2)

    # Test case for API error with retry logic (HTTP 429)
    @patch('time.perf_counter', new_callable=MockTimer)
    @patch('time.sleep', return_value=None) # Mock sleep to avoid delays
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_api_error_retry_fail(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        # Tests the retry mechanism for rate limit errors (429).
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:MSFT"
        mock_client_instance = mock_rest_client_class.return_value
        # Simulate rate limit error on all attempts
        mock_response_429 = MagicMock(status_code=429, url="mock_url_status_429")
        mock_client_instance.get_aggs.side_effect = BadResponse("Rate Limit", response=mock_response_429)
        mock_perf_counter.reset(start_time=200.0, increment=0.1) # Consistent small increment

        result = fetch_polygon_data(ticker="MSFT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNone(df)
        # Check that it retried 3 times (initial call + 2 retries)
        self.assertEqual(mock_client_instance.get_aggs.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2) # Should have slept twice
        self.assertEqual(metrics['api_calls'], 3)
        self.assertEqual(metrics['successful_chunks'], 0)
        self.assertIsNotNone(metrics.get("error_message"))
        self.assertIn("Failed to fetch chunk", metrics["error_message"])

    # Test case for non-retriable API error (e.g., 404)
    @patch('time.perf_counter', new_callable=MockTimer)
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_api_error_non_retriable(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        # Tests handling of non-retriable API errors (e.g., 404 Not Found).
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:FAIL"
        mock_client_instance = mock_rest_client_class.return_value
        # Simulate a 404 Not Found error
        mock_response_404 = MagicMock(status_code=404, url="mock_url_status_404")
        mock_client_instance.get_aggs.side_effect = BadResponse("Not Found", response=mock_response_404)
        mock_perf_counter.reset(start_time=300.0, increment=0.2)

        result = fetch_polygon_data(ticker="FAIL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNone(df)
        mock_client_instance.get_aggs.assert_called_once() # Should not retry on 404
        mock_sleep.assert_not_called()
        self.assertEqual(metrics['api_calls'], 1)
        self.assertEqual(metrics['successful_chunks'], 0)
        self.assertIsNotNone(metrics.get("error_message"))
        self.assertIn("Non-retriable Polygon API Error", metrics["error_message"])

    # Test case for unexpected error during fetch
    @patch('time.perf_counter', new_callable=MockTimer)
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_unexpected_error(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        # Tests handling of unexpected exceptions during data fetching.
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:IBM"
        mock_client_instance = mock_rest_client_class.return_value
        # Simulate an unexpected error (e.g., network issue, parsing error)
        mock_client_instance.get_aggs.side_effect = ValueError("Unexpected parsing error")
        mock_perf_counter.reset(start_time=400.0, increment=0.1)

        result = fetch_polygon_data(ticker="IBM", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNone(df)
        mock_client_instance.get_aggs.assert_called_once() # Only the first attempt
        mock_sleep.assert_not_called() # Should not retry on ValueError
        self.assertEqual(metrics['api_calls'], 1)
        self.assertEqual(metrics['successful_chunks'], 0)
        self.assertIsNotNone(metrics.get("error_message"))
        self.assertIn("UNEXPECTED ERROR DURING POLYGON CHUNK FETCH", metrics["error_message"])
        self.assertIn("ValueError: Unexpected parsing error", metrics["error_traceback"])

    # Test case for NoResultsError from Polygon
    @patch('time.perf_counter', new_callable=MockTimer)
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_no_results(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        # Tests handling of Polygon's specific NoResultsError.
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:EMPTY"
        mock_client_instance = mock_rest_client_class.return_value
        # Simulate NoResultsError
        mock_client_instance.get_aggs.side_effect = NoResultsError("No results found for query.")
        mock_perf_counter.reset(start_time=500.0, increment=0.3)

        result = fetch_polygon_data(ticker="EMPTY", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        # Should return an empty DataFrame and success status, but log a warning
        self.assertIsNotNone(df)
        self.assertTrue(df.empty)
        mock_client_instance.get_aggs.assert_called_once()
        mock_sleep.assert_not_called()
        self.assertEqual(metrics['api_calls'], 1)
        self.assertEqual(metrics['successful_chunks'], 1) # Treated as success (fetched nothing)
        self.assertEqual(metrics['rows_fetched'], 0)
        self.assertIsNone(metrics.get("error_message")) # No error reported

    # Test case when API key is missing
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_no_api_key(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep):
        # Tests the behavior when the POLYGON_API_KEY environment variable is not set.
        mock_getenv.return_value = None # Simulate missing API key

        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNone(df)
        mock_rest_client_class.assert_not_called() # Client should not be initialized
        mock_resolve_ticker.assert_not_called()
        self.assertIsNotNone(metrics.get("error_message"))
        self.assertIn("POLYGON_API_KEY not found", metrics["error_message"])

    # Test case for invalid date format
    @patch('os.getenv', return_value="FAKE_KEY")
    def test_fetch_polygon_data_invalid_dates(self, mock_getenv):
        # Tests input validation for date formats.
        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="01/01/2023", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNone(df)
        self.assertIn("Invalid date format", metrics.get("error_message", ""))

        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="2023-01-01", end_date="01/01/2023")
        df, metrics = result
        self.assertIsNone(df)
        self.assertIn("Invalid date format", metrics.get("error_message", ""))

    # Test case for invalid interval/timespan format
    @patch('os.getenv', return_value="FAKE_KEY")
    def test_fetch_polygon_data_invalid_interval(self, mock_getenv):
        # Tests input validation for the interval/timespan format.
        result = fetch_polygon_data(ticker="AAPL", interval="INVALID", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNone(df)
        self.assertIn("Invalid Polygon timeframe input", metrics.get("error_message", ""))

    # Test case when ticker resolution fails
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker', return_value=None) # Simulate failure
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv', return_value="FAKE_KEY")
    def test_fetch_polygon_data_resolve_fails(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep):
        # Tests the scenario where ticker resolution returns None.
        result = fetch_polygon_data(ticker="UNKNOWN", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNone(df)
        mock_resolve_ticker.assert_called_once()
        mock_rest_client_class.return_value.get_aggs.assert_not_called() # get_aggs should not be called
        self.assertIn("Could not resolve ticker", metrics.get("error_message", ""))

if __name__ == '__main__':
    unittest.main()