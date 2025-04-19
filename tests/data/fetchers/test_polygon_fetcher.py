# tests/data/fetchers/test_polygon_fetcher.py # FINAL CORRECTIONS

import unittest
from unittest.mock import patch, MagicMock, call # Import call
import pandas as pd
from datetime import date, timedelta
import numpy as np # Import numpy

# Functions/classes to test or mock
from src.data.fetchers.polygon_fetcher import (
    fetch_polygon_data, map_polygon_interval, resolve_polygon_ticker,
    POLYGON_AVAILABLE, BadResponse # Import exception
)

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass
    def print_success(self, msg): pass

# Mock the Agg object structure if polygon lib is installed
if POLYGON_AVAILABLE:
    try:
        from polygon.rest.models.aggs import Agg
    except ImportError:
        class Agg: # Dummy
            def __init__(self, timestamp=None, open=None, high=None, low=None, close=None, volume=None):
                 self.timestamp=timestamp; self.open=open; self.high=high; self.low=low; self.close=close; self.volume=volume
else:
    class Agg: # Dummy
        def __init__(self, timestamp=None, open=None, high=None, low=None, close=None, volume=None):
            self.timestamp=timestamp; self.open=open; self.high=high; self.low=low; self.close=close; self.volume=volume

@patch('src.data.fetchers.polygon_fetcher.logger', new_callable=MockLogger)
@patch('src.data.fetchers.polygon_fetcher.POLYGON_AVAILABLE', True) # Assume library is available for tests
class TestPolygonFetcher(unittest.TestCase):

    # --- Tests for map_polygon_interval ---
    def test_map_polygon_interval_mql(self, _):
        self.assertEqual(map_polygon_interval("M1"), ("minute", 1))
        self.assertEqual(map_polygon_interval("H4"), ("hour", 4))
        self.assertEqual(map_polygon_interval("D1"), ("day", 1))
        self.assertEqual(map_polygon_interval("W"), ("week", 1))

    def test_map_polygon_interval_direct(self, _):
        self.assertEqual(map_polygon_interval("day"), ("day", 1))
        self.assertEqual(map_polygon_interval("minute"), ("minute", 1))

    def test_map_polygon_interval_invalid(self, _):
        self.assertIsNone(map_polygon_interval("1s"))
        self.assertIsNone(map_polygon_interval("invalid"))

    # --- Tests for resolve_polygon_ticker ---
    @patch('src.data.fetchers.polygon_fetcher.time.sleep') # Mock sleep to speed up tests
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_success_first_try(self, MockRESTClient, _, __):
        mock_client = MockRESTClient.return_value
        mock_client.get_ticker_details.return_value = MagicMock()
        client_instance = MockRESTClient()
        resolved = resolve_polygon_ticker("AAPL", client_instance)
        self.assertEqual(resolved, "AAPL")
        mock_client.get_ticker_details.assert_called_once_with("AAPL")

    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_success_currency(self, MockRESTClient, mock_sleep, __):
        mock_client = MockRESTClient.return_value
        # CORRECTED: Simulate 404 using BadResponse with message and mock response
        mock_response_404 = MagicMock(status_code=404)
        error_404 = BadResponse("Ticker not found") # Pass message
        setattr(error_404, 'response', mock_response_404) # Set attribute

        mock_client.get_ticker_details.side_effect = [
            error_404,      # Raise 404 for "EURUSD"
            MagicMock()     # Succeed for "C:EURUSD"
        ]
        client_instance = MockRESTClient()
        resolved = resolve_polygon_ticker("EURUSD", client_instance)
        self.assertEqual(resolved, "C:EURUSD") # Should now resolve correctly
        self.assertEqual(mock_client.get_ticker_details.call_count, 2)
        mock_client.get_ticker_details.assert_has_calls([call("EURUSD"), call("C:EURUSD")])
        mock_sleep.assert_called_once()

    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_fail_not_found(self, MockRESTClient, mock_sleep, __):
        mock_client = MockRESTClient.return_value
        # CORRECTED: Simulate 404
        mock_response_404 = MagicMock(status_code=404)
        error_404 = BadResponse("Ticker not found")
        setattr(error_404, 'response', mock_response_404)
        mock_client.get_ticker_details.side_effect = error_404

        client_instance = MockRESTClient()
        resolved = resolve_polygon_ticker("NOTFOUND", client_instance)
        self.assertIsNone(resolved)
        expected_calls = [call("NOTFOUND"), call("C:NOTFOUND"), call("X:NOTFOUND"), call("I:NOTFOUND")]
        mock_client.get_ticker_details.assert_has_calls(expected_calls) # Should now try all
        self.assertEqual(mock_client.get_ticker_details.call_count, 4)
        self.assertEqual(mock_sleep.call_count, 4)


    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_api_error_non_404(self, MockRESTClient, _, __):
        mock_client = MockRESTClient.return_value
        # CORRECTED: Simulate a non-404 BadResponse
        mock_response_401 = MagicMock(status_code=401, url='http://test.url')
        mock_response_401.json.side_effect = ValueError("No JSON")
        mock_response_401.text = "Unauthorized"
        error_401 = BadResponse("Unauthorized")
        setattr(error_401, 'response', mock_response_401)
        mock_client.get_ticker_details.side_effect = error_401

        client_instance = MockRESTClient()
        resolved = resolve_polygon_ticker("ANYTICKER", client_instance)
        self.assertIsNone(resolved)
        mock_client.get_ticker_details.assert_called_once_with("ANYTICKER")


    # --- Tests for fetch_polygon_data ---
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_success_single_chunk(self, mock_resolve, MockRESTClient, mock_getenv, __):
        mock_getenv.return_value = "fake_api_key"
        mock_resolve.return_value = "C:EURUSD"
        mock_client_instance = MockRESTClient.return_value
        agg1 = Agg(timestamp=1672531200000, open=1.1, high=1.11, low=1.09, close=1.1, volume=1000.0)
        agg2 = Agg(timestamp=1672617600000, open=1.11, high=1.12, low=1.1, close=1.11, volume=1100.0)
        mock_client_instance.get_aggs.return_value = [agg1, agg2]

        expected_dates = pd.to_datetime([1672531200000, 1672617600000], unit='ms', name='DateTime') # Set name
        expected_data = { 'Open': [1.1, 1.11], 'High': [1.11, 1.12], 'Low': [1.09, 1.1], 'Close': [1.1, 1.11], 'Volume': [1000.0, 1100.0] }
        expected_df = pd.DataFrame(expected_data, index=expected_dates, dtype=np.float64)
        expected_df.index.name = 'DateTime' # CORRECTED: Set index name

        start_date = "2023-01-01"
        end_date = "2023-01-02"
        result_df = fetch_polygon_data("EURUSD", "D1", start_date, end_date)

        mock_getenv.assert_called_once_with("POLYGON_API_KEY")
        MockRESTClient.assert_called_once_with(api_key="fake_api_key")
        mock_resolve.assert_called_once_with("EURUSD", mock_client_instance)
        mock_client_instance.get_aggs.assert_called_once()
        args_call = mock_client_instance.get_aggs.call_args[1]
        self.assertEqual(args_call['ticker'], "C:EURUSD")

        self.assertIsNotNone(result_df)
        pd.testing.assert_frame_equal(result_df, expected_df) # Should pass now


    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_success_pagination(self, mock_resolve, MockRESTClient, mock_getenv, mock_sleep, __):
        mock_getenv.return_value = "fake_key"
        mock_resolve.return_value = "X:BTCUSD"
        mock_client_instance = MockRESTClient.return_value
        agg1 = Agg(timestamp=1711929600000, open=70000, high=70100, low=69900, close=70050, volume=10.0)
        agg2 = Agg(timestamp=1712016000000, open=70050, high=70200, low=70000, close=70150, volume=11.0)
        agg3 = Agg(timestamp=1712102400000, open=70150, high=70300, low=70100, close=70250, volume=12.0)
        # CORRECTED: side_effect to simulate multiple non-empty chunks
        mock_client_instance.get_aggs.side_effect = [
            [agg1],       # Call 1
            [agg2, agg3], # Call 2
            []            # Call 3 (empty)
        ]

        start_date = "2024-04-01"
        # CORRECTED: Extend end date to ensure multiple chunks are possible with default delta
        end_date = "2024-04-05"
        result_df = fetch_polygon_data("BTCUSD", "D1", start_date, end_date)

        self.assertIsNotNone(result_df)
        self.assertEqual(len(result_df), 3) # Expect all 3 rows
        self.assertEqual(mock_client_instance.get_aggs.call_count, 3) # 2 data + 1 empty
        self.assertEqual(mock_sleep.call_count, 2) # Slept between successful chunk calls

        self.assertEqual(result_df.iloc[0]['Open'], 70000)
        self.assertEqual(result_df.iloc[2]['Close'], 70250)
        self.assertTrue(result_df.index.is_monotonic_increasing)


    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_no_api_key(self, mock_resolve, MockRESTClient, mock_getenv, __):
        mock_getenv.return_value = None
        result_df = fetch_polygon_data("ANY", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        MockRESTClient.assert_not_called()
        mock_resolve.assert_not_called()

    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_resolve_fails(self, mock_resolve, MockRESTClient, mock_getenv, __):
        mock_getenv.return_value = "fake_key"
        mock_resolve.return_value = None
        mock_client_instance = MockRESTClient.return_value

        result_df = fetch_polygon_data("FAIL", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        mock_resolve.assert_called_once_with("FAIL", mock_client_instance)
        mock_client_instance.get_aggs.assert_not_called()

    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_chunk_api_error_429_retry(self, mock_resolve, MockRESTClient, mock_getenv, mock_sleep, __):
        mock_getenv.return_value = "fake_key"
        mock_resolve.return_value = "X:BTCUSD"
        mock_client_instance = MockRESTClient.return_value
        # CORRECTED: Simulate 429 error correctly
        mock_response_429 = MagicMock(status_code=429)
        error_429 = BadResponse("Rate limit")
        setattr(error_429, 'response', mock_response_429)

        agg1 = Agg(timestamp=1711929600000, open=70000, high=70100, low=69900, close=70050, volume=10)
        mock_client_instance.get_aggs.side_effect = [
            error_429, # First attempt fails (429)
            error_429, # Second attempt fails (429)
            [agg1],    # Third attempt succeeds
            []         # Next chunk is empty
        ]

        start_date = "2024-04-01"
        end_date = "2024-04-01"
        result_df = fetch_polygon_data("BTCUSD", "D1", start_date, end_date)

        self.assertIsNotNone(result_df)
        self.assertEqual(len(result_df), 1)
        # CORRECTED: Check call count (2 fails + 1 success for first chunk + 1 empty call)
        self.assertEqual(mock_client_instance.get_aggs.call_count, 4)
        # Check sleeps (1 after each 429 + 1 between successful chunk fetches)
        self.assertEqual(mock_sleep.call_count, 3)

# Allow running tests directly
if __name__ == '__main__':
    unittest.main()