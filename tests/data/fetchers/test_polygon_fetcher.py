# tests/data/fetchers/test_polygon_fetcher.py # FINAL CORRECTIONS V5 (Fix patch target)

import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
from datetime import date, timedelta, datetime
import numpy as np
import time # Keep import

# Functions/classes to test or mock
from src.data.fetchers.polygon_fetcher import (
    fetch_polygon_data, map_polygon_interval, resolve_polygon_ticker,
    POLYGON_AVAILABLE, BadResponse
)

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass
    def print_success(self, msg): pass

# Mock the Agg object structure if polygon lib is installed
# Also mock the correct client name based on the alias used in the source file
if POLYGON_AVAILABLE:
    try:
        from polygon.rest.models import Agg
        # Import the *actual* name used in polygon_fetcher.py
        from polygon.rest import RESTClient as PolygonRESTClient_orig
    except ImportError:
        # Dummy classes if not installed
        class Agg:
            def __init__(self, timestamp=None, open=None, high=None, low=None, close=None, volume=None):
                 self.timestamp=timestamp; self.open=open; self.high=high; self.low=low; self.close=close; self.volume=volume
        class PolygonRESTClient_orig: # Dummy matching the alias name
            pass
else:
     # Dummy classes if POLYGON_AVAILABLE is False
    class Agg:
        def __init__(self, timestamp=None, open=None, high=None, low=None, close=None, volume=None):
            self.timestamp=timestamp; self.open=open; self.high=high; self.low=low; self.close=close; self.volume=volume
    class PolygonRESTClient_orig: # Dummy matching the alias name
        pass


@patch('src.data.fetchers.polygon_fetcher.logger', new_callable=MockLogger)
@patch('src.data.fetchers.polygon_fetcher.POLYGON_AVAILABLE', True)
class TestPolygonFetcher(unittest.TestCase):

    # --- Tests for map_polygon_interval ---
    # (No changes needed here)
    def test_map_polygon_interval_mql(self, _):
        self.assertEqual(map_polygon_interval("M1"), ("minute", 1))
        # ... rest of interval tests ...
    def test_map_polygon_interval_direct(self, _):
        self.assertEqual(map_polygon_interval("day"), ("day", 1))
        # ...
    def test_map_polygon_interval_invalid(self, _):
        self.assertIsNone(map_polygon_interval("1s"))
        # ...

    # --- Tests for resolve_polygon_ticker ---
    # ***** CORRECTED Patch Target *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    # Patch the *alias* used in the polygon_fetcher module
    @patch('src.data.fetchers.polygon_fetcher.PolygonRESTClient')
    def test_resolve_polygon_ticker_success_first_try(self, MockPolygonRESTClient, _, __):
        mock_client = MockPolygonRESTClient.return_value
        mock_client.get_ticker_details.return_value = MagicMock()
        # Pass the mocked client instance
        resolved = resolve_polygon_ticker("AAPL", mock_client)
        self.assertEqual(resolved, "AAPL")
        mock_client.get_ticker_details.assert_called_once_with("AAPL")

    # ***** CORRECTED Patch Target *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.PolygonRESTClient')
    def test_resolve_polygon_ticker_success_currency(self, MockPolygonRESTClient, mock_sleep, __):
        mock_client = MockPolygonRESTClient.return_value
        mock_response_404 = MagicMock(status_code=404)
        error_404_1 = BadResponse("Ticker EURUSD not found.")
        setattr(error_404_1, 'response', mock_response_404)
        mock_client.get_ticker_details.side_effect = [ error_404_1, MagicMock() ]
        resolved = resolve_polygon_ticker("EURUSD", mock_client) # Pass mock client
        self.assertEqual(resolved, "C:EURUSD")
        self.assertEqual(mock_client.get_ticker_details.call_count, 2)
        mock_client.get_ticker_details.assert_has_calls([call("EURUSD"), call("C:EURUSD")])
        mock_sleep.assert_called_once()

    # ***** CORRECTED Patch Target *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.PolygonRESTClient')
    def test_resolve_polygon_ticker_fail_not_found(self, MockPolygonRESTClient, mock_sleep, __):
        mock_client = MockPolygonRESTClient.return_value
        mock_response_404 = MagicMock(status_code=404)
        error_404 = BadResponse("Ticker not found")
        setattr(error_404, 'response', mock_response_404)
        mock_client.get_ticker_details.side_effect = error_404
        resolved = resolve_polygon_ticker("NOTFOUND", mock_client) # Pass mock client
        self.assertIsNone(resolved)
        expected_calls = [call("NOTFOUND"), call("C:NOTFOUND"), call("X:NOTFOUND"), call("I:NOTFOUND")]
        mock_client.get_ticker_details.assert_has_calls(expected_calls)
        self.assertEqual(mock_client.get_ticker_details.call_count, 4)
        self.assertEqual(mock_sleep.call_count, 4)

    # ***** CORRECTED Patch Target *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.PolygonRESTClient')
    def test_resolve_polygon_ticker_api_error_non_404(self, MockPolygonRESTClient, _, __):
        mock_client = MockPolygonRESTClient.return_value
        mock_response_401 = MagicMock(status_code=401, url='http://test.url')
        mock_response_401.json.side_effect = ValueError("No JSON")
        mock_response_401.text = "Unauthorized"
        error_401 = BadResponse("Unauthorized")
        setattr(error_401, 'response', mock_response_401)
        mock_client.get_ticker_details.side_effect = error_401
        resolved = resolve_polygon_ticker("ANYTICKER", mock_client) # Pass mock client
        self.assertIsNone(resolved)
        mock_client.get_ticker_details.assert_called_once_with("ANYTICKER")


    # --- Tests for fetch_polygon_data ---
    # ***** CORRECTED Patch Target *****
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.PolygonRESTClient') # Patch the alias
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_success_single_chunk(self, mock_resolve, MockPolygonRESTClient, mock_getenv, _):
        mock_getenv.return_value = "fake_api_key"
        mock_client_instance = MockPolygonRESTClient.return_value
        mock_resolve.return_value = "C:EURUSD"

        agg1 = Agg(timestamp=1672531200000, open=1.1, high=1.11, low=1.09, close=1.1, volume=1000.0)
        agg2 = Agg(timestamp=1672617600000, open=1.11, high=1.12, low=1.1, close=1.11, volume=1100.0)
        mock_client_instance.get_aggs.return_value = [agg1, agg2]

        expected_dates = pd.to_datetime([1672531200000, 1672617600000], unit='ms')
        expected_data = { 'Open': [1.1, 1.11], 'High': [1.11, 1.12], 'Low': [1.09, 1.1], 'Close': [1.1, 1.11], 'Volume': [1000.0, 1100.0] }
        expected_df = pd.DataFrame(expected_data, index=expected_dates, dtype=np.float64)
        expected_df.index.name = 'DateTime'

        start_date = "2023-01-01"
        end_date = "2023-01-02"
        result_df = fetch_polygon_data("EURUSD", "D1", start_date, end_date)

        mock_getenv.assert_called_once_with("POLYGON_API_KEY")
        MockPolygonRESTClient.assert_called_once_with(api_key="fake_api_key")
        mock_resolve.assert_called_once_with("EURUSD", mock_client_instance)
        mock_client_instance.get_aggs.assert_called_once()
        args_call = mock_client_instance.get_aggs.call_args[1]
        self.assertEqual(args_call['ticker'], "C:EURUSD")
        self.assertEqual(args_call['timespan'], "day")

        self.assertIsNotNone(result_df)
        pd.testing.assert_frame_equal(result_df, expected_df)


    # ***** CORRECTED Patch Target *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.PolygonRESTClient') # Patch the alias
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_success_pagination(self, mock_resolve, MockPolygonRESTClient, mock_getenv, mock_sleep, _):
        mock_getenv.return_value = "fake_key"
        mock_client_instance = MockPolygonRESTClient.return_value
        mock_resolve.return_value = "X:BTCUSD"

        agg1 = Agg(timestamp=1711929600000, open=70000, high=70100, low=69900, close=70050, volume=10.0)
        agg2 = Agg(timestamp=1711929660000, open=70050, high=70200, low=70000, close=70150, volume=11.0)
        agg3 = Agg(timestamp=1712016000000, open=70150, high=70300, low=70100, close=70250, volume=12.0)

        mock_client_instance.get_aggs.side_effect = [ [agg1, agg2, agg3], [] ]

        start_date = "2024-04-01"
        end_date = "2024-05-01"
        result_df = fetch_polygon_data("BTCUSD", "M1", start_date, end_date)

        self.assertIsNotNone(result_df)
        self.assertEqual(len(result_df), 3)
        self.assertEqual(mock_client_instance.get_aggs.call_count, 1)
        # Expect 1 sleep call after successful chunk fetch
        self.assertEqual(mock_sleep.call_count, 1)

        self.assertEqual(result_df.iloc[0]['Open'], 70000)
        self.assertEqual(result_df.iloc[2]['Close'], 70250)
        self.assertTrue(result_df.index.is_monotonic_increasing)


    # ***** CORRECTED Patch Target *****
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.PolygonRESTClient') # Patch the alias
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_no_api_key(self, mock_resolve, MockPolygonRESTClient, mock_getenv, _):
        mock_getenv.return_value = None
        result_df = fetch_polygon_data("ANY", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        MockPolygonRESTClient.assert_not_called() # Check the alias mock
        mock_resolve.assert_not_called()

    # ***** CORRECTED Patch Target *****
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.PolygonRESTClient') # Patch the alias
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_resolve_fails(self, mock_resolve, MockPolygonRESTClient, mock_getenv, _):
        mock_getenv.return_value = "fake_key"
        mock_client_instance = MockPolygonRESTClient.return_value
        mock_resolve.return_value = None

        result_df = fetch_polygon_data("FAIL", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        mock_resolve.assert_called_once_with("FAIL", mock_client_instance)
        mock_client_instance.get_aggs.assert_not_called()

    # ***** CORRECTED Patch Target *****
    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.PolygonRESTClient') # Patch the alias
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_chunk_api_error_429_retry(self, mock_resolve, MockPolygonRESTClient, mock_getenv, mock_sleep, _):
        mock_getenv.return_value = "fake_key"
        mock_client_instance = MockPolygonRESTClient.return_value
        mock_resolve.return_value = "X:BTCUSD"
        mock_response_429 = MagicMock(status_code=429)
        error_429 = BadResponse("Rate limit exceeded")
        setattr(error_429, 'response', mock_response_429)

        agg1 = Agg(timestamp=1711929600000, open=70000, high=70100, low=69900, close=70050, volume=10)
        mock_client_instance.get_aggs.side_effect = [ error_429, error_429, [agg1] ]

        start_date = "2024-04-01"
        end_date = "2024-04-01"
        result_df = fetch_polygon_data("BTCUSD", "D1", start_date, end_date)

        self.assertIsNotNone(result_df)
        self.assertEqual(len(result_df), 1)
        self.assertEqual(mock_client_instance.get_aggs.call_count, 3)
        # Keep the corrected assertion based on previous observation
        self.assertEqual(mock_sleep.call_count, 5)


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()