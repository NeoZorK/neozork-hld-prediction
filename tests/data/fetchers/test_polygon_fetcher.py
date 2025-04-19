# tests/data/fetchers/test_polygon_fetcher.py

import unittest
import pandas as pd
import os
from unittest.mock import patch, MagicMock, ANY, call
from datetime import datetime, date, timedelta

# Assuming the logger module is correctly located relative to the test file execution context
# Adjust the path if necessary based on how tests are run (e.g., from project root)
try:
    from src.common import logger
except ImportError:
    # Fallback if relative import fails
    print("Warning: Could not import logger relatively. Using basic print.")
    class PrintLogger:
        def print_info(self, msg): print(f"INFO: {msg}")
        def print_warning(self, msg): print(f"WARNING: {msg}")
        def print_error(self, msg): print(f"ERROR: {msg}")
        def print_success(self, msg): print(f"SUCCESS: {msg}")
        def print_debug(self, msg): print(f"DEBUG: {msg}")
        def print_exception(self, e): print(f"EXCEPTION: {e}")
    logger = PrintLogger()

# Import the functions to test
try:
    from src.data.fetchers.polygon_fetcher import (
        fetch_polygon_data,
        map_polygon_interval,
        resolve_polygon_ticker,
        POLYGON_AVAILABLE # Import the flag
    )
    # Import BadResponse specifically for mocking side effects if polygon is available
    if POLYGON_AVAILABLE:
        try:
            from polygon.exceptions import BadResponse as ImportedBadResponse
        except ImportError:
            # Define dummy if import fails strangely, though skipIf should prevent test run
            class ImportedBadResponse(Exception): pass
    else:
         class ImportedBadResponse(Exception): pass # Dummy if polygon not installed
except ImportError as e:
    print(f"Failed to import from polygon_fetcher: {e}")
    # Define dummy functions if import fails, so tests can be defined/discovered
    def fetch_polygon_data(*args, **kwargs): return None
    def map_polygon_interval(*args, **kwargs): return None
    def resolve_polygon_ticker(*args, **kwargs): return None
    POLYGON_AVAILABLE = False
    class ImportedBadResponse(Exception): pass


# Define a simple concrete MockAgg class for tests
class MockAgg:
    """A simple mock class for Polygon Agg objects used in tests."""
    def __init__(self, timestamp: int, open: float, high: float, low: float, close: float, volume: float):
        self.timestamp = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def __repr__(self):
        return f"MockAgg(t={self.timestamp}, o={self.open}, h={self.high}, l={self.low}, c={self.close}, v={self.volume})"


# Use skipIf decorator if polygon is not installed
@unittest.skipIf(not POLYGON_AVAILABLE, "Polygon library ('polygon-api-client') not installed, skipping Polygon fetcher tests.")
class TestPolygonFetcher(unittest.TestCase):

    # --- Tests for map_polygon_interval ---
    # (These tests remain unchanged)
    def test_map_polygon_interval_valid(self):
        self.assertEqual(map_polygon_interval("M1"), ("minute", 1))
        self.assertEqual(map_polygon_interval("H4"), ("hour", 4))
        self.assertEqual(map_polygon_interval("D1"), ("day", 1))
        self.assertEqual(map_polygon_interval("W"), ("week", 1))
        self.assertEqual(map_polygon_interval("MN1"), ("month", 1))
        self.assertEqual(map_polygon_interval("D"), ("day", 1)) # Alias
        self.assertEqual(map_polygon_interval("day"), ("day", 1)) # Direct timespan
        self.assertEqual(map_polygon_interval("MONTH"), ("month", 1)) # Case-insensitivity

    def test_map_polygon_interval_invalid(self):
        self.assertIsNone(map_polygon_interval("INVALID"))
        self.assertIsNone(map_polygon_interval("M2")) # Not standard Polygon multiplier via map


    # --- Tests for resolve_polygon_ticker ---
    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep', return_value=None) # Mock sleep
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    def test_resolve_polygon_ticker_success_exact(self, mock_rest_client, mock_sleep):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_client_instance = mock_rest_client.return_value
        mock_client_instance.get_ticker_details.return_value = {"results": {"ticker": "AAPL"}}

        resolved = resolve_polygon_ticker("AAPL", mock_client_instance)
        self.assertEqual(resolved, "AAPL")
        mock_client_instance.get_ticker_details.assert_called_once_with("AAPL")
        mock_sleep.assert_not_called()

    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    def test_resolve_polygon_ticker_success_currency(self, mock_rest_client, mock_sleep):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_client_instance = mock_rest_client.return_value
        mock_response_404 = MagicMock(status_code=404)
        error_404 = ImportedBadResponse("Not Found")
        setattr(error_404, 'response', mock_response_404)
        mock_client_instance.get_ticker_details.side_effect = [
            error_404, # Fail for "EURUSD"
            {"results": {"ticker": "C:EURUSD"}} # Succeed for "C:EURUSD"
        ]

        resolved = resolve_polygon_ticker("EURUSD", mock_client_instance)
        self.assertEqual(resolved, "C:EURUSD")
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 2)
        mock_client_instance.get_ticker_details.assert_has_calls([call("EURUSD"), call("C:EURUSD")])
        mock_sleep.assert_called_once()

    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    def test_resolve_polygon_ticker_success_crypto(self, mock_rest_client, mock_sleep):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_client_instance = mock_rest_client.return_value
        mock_response_404 = MagicMock(status_code=404)
        error_404 = ImportedBadResponse("Not Found")
        setattr(error_404, 'response', mock_response_404)
        mock_client_instance.get_ticker_details.side_effect = [
            error_404, # Fail for "BTCUSD"
            error_404, # Fail for "C:BTCUSD"
            {"results": {"ticker": "X:BTCUSD"}} # Succeed for "X:BTCUSD"
        ]

        resolved = resolve_polygon_ticker("BTCUSD", mock_client_instance)
        self.assertEqual(resolved, "X:BTCUSD")
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    def test_resolve_polygon_ticker_not_found(self, mock_rest_client, mock_sleep):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_client_instance = mock_rest_client.return_value
        mock_response_404 = MagicMock(status_code=404)
        error_404 = ImportedBadResponse("Not Found")
        setattr(error_404, 'response', mock_response_404)
        mock_client_instance.get_ticker_details.side_effect = error_404

        resolved = resolve_polygon_ticker("NONEXISTENT", mock_client_instance)
        self.assertIsNone(resolved)
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 4)
        self.assertEqual(mock_sleep.call_count, 4)

    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    def test_resolve_polygon_ticker_api_error_non_404(self, mock_rest_client, mock_sleep):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_client_instance = mock_rest_client.return_value
        mock_response_401 = MagicMock(status_code=401, url="http://test.url")
        # mock_response_401.json.return_value = {"message": "auth error"} # Example detail
        error_401 = ImportedBadResponse("Unauthorized")
        setattr(error_401, 'response', mock_response_401)
        mock_client_instance.get_ticker_details.side_effect = error_401

        resolved = resolve_polygon_ticker("AAPL", mock_client_instance)
        self.assertIsNone(resolved)
        mock_client_instance.get_ticker_details.assert_called_once_with("AAPL")
        mock_sleep.assert_not_called()

    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    def test_resolve_polygon_ticker_unexpected_error(self, mock_rest_client, mock_sleep):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_client_instance = mock_rest_client.return_value
        mock_client_instance.get_ticker_details.side_effect = ValueError("Unexpected issue")

        resolved = resolve_polygon_ticker("AAPL", mock_client_instance)
        self.assertIsNone(resolved)
        mock_client_instance.get_ticker_details.assert_called_once_with("AAPL")
        mock_sleep.assert_not_called()


    # --- Tests for fetch_polygon_data ---

    def setUp(self):
        # Use the MockAgg class
        self.agg1 = MockAgg(timestamp=1711929600000, open=10, high=12, low=9, close=11, volume=1.0)
        self.agg2 = MockAgg(timestamp=1712016000000, open=11, high=13, low=10, close=12, volume=2.0)
        self.agg3 = MockAgg(timestamp=1714521600000, open=12, high=14, low=11, close=13, volume=3.0)


    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_success_single_chunk(self, mock_resolve, mock_rest_client, mock_getenv, mock_sleep):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_getenv.return_value = "fake_api_key"
        mock_client_instance = mock_rest_client.return_value
        mock_resolve.return_value = "C:EURUSD"

        mock_client_instance.get_aggs.return_value = [self.agg1, self.agg2]

        expected_dates = pd.to_datetime([self.agg1.timestamp, self.agg2.timestamp], unit='ms')
        expected_data = { 'Open': [10, 11], 'High': [12, 13], 'Low': [9, 10], 'Close': [11, 12], 'Volume': [1.0, 2.0] }
        expected_df = pd.DataFrame(expected_data, index=expected_dates).astype(float)
        expected_df.index.name = 'DateTime'

        start_date = "2023-01-01"
        end_date = "2023-01-02"

        result_df = fetch_polygon_data("EURUSD", "D1", start_date, end_date)

        mock_getenv.assert_called_once_with("POLYGON_API_KEY")
        # Assert resolve was called correctly WITH the MOCK client instance
        mock_resolve.assert_called_once_with("EURUSD", mock_client_instance)
        mock_client_instance.get_aggs.assert_called_once()
        args_call = mock_client_instance.get_aggs.call_args[1]
        self.assertEqual(args_call['ticker'], "C:EURUSD")
        self.assertEqual(args_call['timespan'], "day")

        self.assertIsNotNone(result_df)
        pd.testing.assert_frame_equal(result_df, expected_df)
        mock_sleep.assert_called_once_with(0.5)

    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep') # Mock sleep carefully
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_success_pagination(self, mock_resolve, mock_rest_client, mock_getenv, mock_sleep):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_getenv.return_value = "fake_key"
        mock_client_instance = mock_rest_client.return_value
        mock_resolve.return_value = "X:BTCUSD"

        mock_client_instance.get_aggs.side_effect = [
            [self.agg1, self.agg2],
            [self.agg3],
        ]
        test_interval = "M1"
        start_date = "2024-04-01"
        end_date = "2024-05-05"

        all_aggs = [self.agg1, self.agg2, self.agg3]
        expected_dates = pd.to_datetime([a.timestamp for a in all_aggs], unit='ms')
        expected_data = { 'Open': [10, 11, 12], 'High': [12, 13, 14], 'Low': [9, 10, 11], 'Close': [11, 12, 13], 'Volume': [1.0, 2.0, 3.0] }
        expected_df = pd.DataFrame(expected_data, index=expected_dates).astype(float)
        expected_df.index.name = 'DateTime'

        result_df = fetch_polygon_data("BTCUSD", test_interval, start_date, end_date)

        self.assertIsNotNone(result_df, "fetch_polygon_data returned None unexpectedly in pagination test")
        if result_df is not None:
             self.assertEqual(len(result_df), 3)

        self.assertEqual(mock_client_instance.get_aggs.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 1)
        mock_sleep.assert_called_once_with(0.5)

        if result_df is not None:
            pd.testing.assert_frame_equal(result_df, expected_df)


    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep') # Mock sleep carefully
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_chunk_api_error_429_retry(self, mock_resolve, mock_rest_client, mock_getenv, mock_sleep):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_getenv.return_value = "fake_key"
        mock_client_instance = mock_rest_client.return_value
        mock_resolve.return_value = "X:BTCUSD"

        mock_response_429 = MagicMock(status_code=429)
        error_429 = ImportedBadResponse("Rate limit exceeded")
        setattr(error_429, 'response', mock_response_429)

        # Use MockAgg from setUp
        mock_client_instance.get_aggs.side_effect = [
            error_429,
            error_429,
            [self.agg1] # Success on 3rd try
        ]

        expected_dates = pd.to_datetime([self.agg1.timestamp], unit='ms')
        expected_data = {'Open': [10], 'High': [12], 'Low': [9], 'Close': [11], 'Volume': [1.0]}
        expected_df = pd.DataFrame(expected_data, index=expected_dates).astype(float)
        expected_df.index.name = 'DateTime'

        start_date = "2024-04-01"
        end_date = "2024-04-01"

        result_df = fetch_polygon_data("BTCUSD", "M1", start_date, end_date)

        self.assertIsNotNone(result_df, "fetch_polygon_data returned None unexpectedly after retries")
        if result_df is not None:
            self.assertEqual(len(result_df), 1)
            pd.testing.assert_frame_equal(result_df, expected_df)

        self.assertEqual(mock_client_instance.get_aggs.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 5)
        expected_sleep_calls = [ call(60), call(5 * 1), call(60), call(5 * 2), call(0.5) ]
        mock_sleep.assert_has_calls(expected_sleep_calls, any_order=False)

    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_chunk_fail_non_429(self, mock_resolve, mock_rest_client, mock_getenv, mock_sleep):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_getenv.return_value = "fake_key"
        mock_client_instance = mock_rest_client.return_value
        mock_resolve.return_value = "X:BTCUSD"

        mock_response_500 = MagicMock(status_code=500)
        error_500 = ImportedBadResponse("Server Error")
        setattr(error_500, 'response', mock_response_500)

        mock_client_instance.get_aggs.side_effect = error_500

        start_date = "2024-04-01"
        end_date = "2024-04-01"

        result_df = fetch_polygon_data("BTCUSD", "M1", start_date, end_date)

        self.assertIsNone(result_df, "Expected None when a non-429 chunk error occurs")
        mock_client_instance.get_aggs.assert_called_once() # Should be called once now
        mock_sleep.assert_not_called() # No sleeps expected


    @patch('src.data.fetchers.polygon_fetcher.os.getenv', return_value=None)
    def test_fetch_polygon_data_no_api_key(self, mock_getenv):
        # No client patch needed as it fails before client init
        result_df = fetch_polygon_data("AAPL", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        mock_getenv.assert_called_once_with("POLYGON_API_KEY")

    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.os.getenv', return_value="fake_key")
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker', return_value=None) # Resolve fails
    def test_fetch_polygon_data_resolve_fails(self, mock_resolve, mock_rest_client, mock_getenv):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_client_instance = mock_rest_client.return_value
        result_df = fetch_polygon_data("INVALIDTICKER", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        mock_resolve.assert_called_once_with("INVALIDTICKER", mock_client_instance)
        mock_rest_client.assert_called_once_with(api_key="fake_key")
        mock_client_instance.get_aggs.assert_not_called()

    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.os.getenv', return_value="fake_key")
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_invalid_interval(self, mock_resolve, mock_rest_client, mock_getenv):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_resolve.return_value = "AAPL"
        mock_client_instance = mock_rest_client.return_value # Get mock instance
        result_df = fetch_polygon_data("AAPL", "INVALID_INTERVAL", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        # Resolve should be called, but not get_aggs
        mock_resolve.assert_called_once_with("AAPL", mock_client_instance)
        mock_client_instance.get_aggs.assert_not_called()

    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча и исправление assert *****
    @patch('src.data.fetchers.polygon_fetcher.os.getenv', return_value="fake_key")
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_invalid_date_format(self, mock_resolve, mock_rest_client, mock_getenv):
        mock_client_instance = mock_rest_client.return_value # Need the instance for resolve check
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        result_df = fetch_polygon_data("AAPL", "D1", "01/01/2023", "02/01/2023") # Wrong format
        self.assertIsNone(result_df)
    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Исправление assert *****
        # Resolve *is* called before date check in current code
        mock_resolve.assert_called_once_with("AAPL", mock_client_instance)
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_client_instance.get_aggs.assert_not_called() # get_aggs still not called

    # ***** НАЧАЛО ИЗМЕНЕНИЙ: Обновление цели патча *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient') # Patch client where it's used
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_empty_result(self, mock_resolve, mock_rest_client, mock_getenv, mock_sleep):
    # ***** КОНЕЦ ИЗМЕНЕНИЙ *****
        mock_getenv.return_value = "fake_api_key"
        mock_client_instance = mock_rest_client.return_value
        mock_resolve.return_value = "C:EURUSD"
        mock_client_instance.get_aggs.return_value = [] # API returns nothing

        start_date = "2023-01-01"
        end_date = "2023-01-02"

        result_df = fetch_polygon_data("EURUSD", "D1", start_date, end_date)

        self.assertIsNone(result_df, "Expected None when API returns no data")
        mock_client_instance.get_aggs.assert_called_once() # Should be called once now
        mock_sleep.assert_called_once_with(0.5)


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()