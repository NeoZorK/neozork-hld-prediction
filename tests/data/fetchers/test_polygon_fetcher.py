# tests/data/fetchers/test_polygon_fetcher.py

import unittest
from unittest.mock import patch, MagicMock, call # Import call
from datetime import date

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
    from polygon.rest.models.aggs import Agg
else:
    # Create a dummy Agg that can be instantiated if lib is not installed
    class Agg:
        def __init__(self, timestamp=None, open=None, high=None, low=None, close=None, volume=None):
            self.timestamp = timestamp
            self.open = open
            self.high = high
            self.low = low
            self.close = close
            self.volume = volume

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
    # Requires mocking the client.get_ticker_details method
    @patch('src.data.fetchers.polygon_fetcher.time.sleep') # Mock sleep to speed up tests
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_success_first_try(self, MockRESTClient, _, __):
        mock_client = MockRESTClient.return_value
        # Configure get_ticker_details to succeed on the first call
        mock_client.get_ticker_details.return_value = MagicMock() # Just needs to not raise error

        client_instance = MockRESTClient() # Instance used in the function
        resolved = resolve_polygon_ticker("AAPL", client_instance)

        self.assertEqual(resolved, "AAPL")
        mock_client.get_ticker_details.assert_called_once_with("AAPL")

    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_success_currency(self, MockRESTClient, _, __):
        mock_client = MockRESTClient.return_value
        # Simulate 404 for "EURUSD", success for "C:EURUSD"
        mock_response_404 = MagicMock(status_code=404)
        mock_client.get_ticker_details.side_effect = [
            BadResponse(mock_response_404), # Raise 404 for "EURUSD"
            MagicMock()                    # Succeed for "C:EURUSD"
        ]

        client_instance = MockRESTClient()
        resolved = resolve_polygon_ticker("EURUSD", client_instance)

        self.assertEqual(resolved, "C:EURUSD")
        self.assertEqual(mock_client.get_ticker_details.call_count, 2)
        mock_client.get_ticker_details.assert_has_calls([call("EURUSD"), call("C:EURUSD")])

    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_fail_not_found(self, MockRESTClient, _, __):
        mock_client = MockRESTClient.return_value
        # Simulate 404 for all attempts
        mock_response_404 = MagicMock(status_code=404)
        mock_client.get_ticker_details.side_effect = BadResponse(mock_response_404)

        client_instance = MockRESTClient()
        resolved = resolve_polygon_ticker("NOTFOUND", client_instance)

        self.assertIsNone(resolved)
        # Check it tried all prefixes
        expected_calls = [call("NOTFOUND"), call("C:NOTFOUND"), call("X:NOTFOUND"), call("I:NOTFOUND")]
        mock_client.get_ticker_details.assert_has_calls(expected_calls)
        self.assertEqual(mock_client.get_ticker_details.call_count, 4)

    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    def test_resolve_polygon_ticker_api_error_non_404(self, MockRESTClient, _, __):
        mock_client = MockRESTClient.return_value
        # Simulate a non-404 BadResponse (e.g., 401 Unauthorized)
        mock_response_401 = MagicMock(status_code=401)
        mock_client.get_ticker_details.side_effect = BadResponse(mock_response_401)

        client_instance = MockRESTClient()
        resolved = resolve_polygon_ticker("ANYTICKER", client_instance)

        self.assertIsNone(resolved)
        # Should stop after the first error
        mock_client.get_ticker_details.assert_called_once_with("ANYTICKER")


    # --- Tests for fetch_polygon_data ---
    @patch('src.data.fetchers.polygon_fetcher.os.getenv') # Mock environment variable access
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_success_single_chunk(self, mock_resolve, MockRESTClient, mock_getenv, __):
        # Setup mocks
        mock_getenv.return_value = "fake_api_key" # Provide API key
        mock_resolve.return_value = "C:EURUSD" # Simulate resolved ticker
        mock_client_instance = MockRESTClient.return_value

        # Simulate API returning data in one go
        agg1 = Agg(timestamp=1672531200000, open=1.1, high=1.11, low=1.09, close=1.1, volume=1000)
        agg2 = Agg(timestamp=1672617600000, open=1.11, high=1.12, low=1.1, close=1.11, volume=1100)
        mock_client_instance.get_aggs.return_value = [agg1, agg2] # Return list directly

        # Call function
        start_date = "2023-01-01"
        end_date = "2023-01-02"
        result_df = fetch_polygon_data("EURUSD", "D1", start_date, end_date)

        # Assertions
        mock_getenv.assert_called_once_with("POLYGON_API_KEY")
        MockRESTClient.assert_called_once_with(api_key="fake_api_key")
        mock_resolve.assert_called_once_with("EURUSD", mock_client_instance)
        mock_client_instance.get_aggs.assert_called_once()
        # Check specific args of get_aggs if needed
        args_call = mock_client_instance.get_aggs.call_args[1] # Get keyword args
        self.assertEqual(args_call['ticker'], "C:EURUSD")
        self.assertEqual(args_call['multiplier'], 1)
        self.assertEqual(args_call['timespan'], 'day')
        self.assertEqual(args_call['from_'], date(2023, 1, 1))
        self.assertEqual(args_call['to'], date(2023, 1, 2))

        self.assertIsNotNone(result_df)
        self.assertEqual(len(result_df), 2)
        self.assertEqual(result_df.iloc[0]['Open'], 1.1)
        self.assertEqual(result_df.iloc[1]['Close'], 1.11)

    @patch('src.data.fetchers.polygon_fetcher.time.sleep') # Mock sleep for pagination test
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_success_pagination(self, mock_resolve, MockRESTClient, mock_getenv, mock_sleep, __):
        # Setup mocks
        mock_getenv.return_value = "fake_key"
        mock_resolve.return_value = "X:BTCUSD"
        mock_client_instance = MockRESTClient.return_value

        # Simulate pagination: 2 chunks then empty
        agg1 = Agg(timestamp=1711929600000, open=70000, high=70100, low=69900, close=70050, volume=10) # Apr 1 2024
        agg2 = Agg(timestamp=1712016000000, open=70050, high=70200, low=70000, close=70150, volume=11) # Apr 2 2024
        agg3 = Agg(timestamp=1712102400000, open=70150, high=70300, low=70100, close=70250, volume=12) # Apr 3 2024
        mock_client_instance.get_aggs.side_effect = [
            [agg1, agg2], # First call
            [agg3],       # Second call (assuming chunk size forces this)
            []            # Third call (empty, stops loop)
        ]

        # Call function with a range that might trigger pagination
        start_date = "2024-04-01"
        end_date = "2024-04-03"
        result_df = fetch_polygon_data("BTCUSD", "D1", start_date, end_date) # Use D1 for simplicity

        # Assertions
        self.assertIsNotNone(result_df)
        self.assertEqual(len(result_df), 3) # All aggregates combined
        self.assertEqual(mock_client_instance.get_aggs.call_count, 3) # Check pagination happened

        # Verify call arguments (especially dates)
        calls = mock_client_instance.get_aggs.call_args_list
        # Dates depend on chunk_delta, let's assume yearly for D1 triggered 2 calls
        # Check the 'from_' dates align with chunking logic
        self.assertEqual(calls[0][1]['from_'], date(2024, 4, 1))
        # The 'to' date depends on chunk_delta. If delta > 3 days, only one real call needed
        # Let's adjust the side_effect to match a monthly D1 fetch scenario
        mock_client_instance.get_aggs.side_effect = [[agg1, agg2, agg3], []]
        result_df = fetch_polygon_data("BTCUSD", "D1", start_date, end_date)
        self.assertIsNotNone(result_df)
        self.assertEqual(len(result_df), 3)
        self.assertEqual(mock_client_instance.get_aggs.call_count, 2) # 1 data + 1 empty
        calls = mock_client_instance.get_aggs.call_args_list
        self.assertEqual(calls[0][1]['from_'], date(2024, 4, 1))
        self.assertEqual(calls[0][1]['to'], date(2024, 4, 3)) # End date of range

        # Verify final DataFrame content
        self.assertEqual(result_df.iloc[0]['Open'], 70000)
        self.assertEqual(result_df.iloc[2]['Close'], 70250)
        # Check index is sorted
        self.assertTrue(result_df.index.is_monotonic_increasing)

    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_no_api_key(self, mock_resolve, MockRESTClient, mock_getenv, __):
        mock_getenv.return_value = None # Simulate missing key
        result_df = fetch_polygon_data("ANY", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        MockRESTClient.assert_not_called()
        mock_resolve.assert_not_called()

    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_resolve_fails(self, mock_resolve, MockRESTClient, mock_getenv, __):
        mock_getenv.return_value = "fake_key"
        mock_resolve.return_value = None # Simulate resolve failure
        mock_client_instance = MockRESTClient.return_value

        result_df = fetch_polygon_data("FAIL", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        mock_resolve.assert_called_once_with("FAIL", mock_client_instance)
        mock_client_instance.get_aggs.assert_not_called()

    @patch('src.data.fetchers.polygon_fetcher.time.sleep')
    @patch('src.data.fetchers.polygon_fetcher.os.getenv')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    def test_fetch_polygon_data_chunk_api_error(self, mock_resolve, MockRESTClient, mock_getenv, mock_sleep, __):
        # Setup mocks
        mock_getenv.return_value = "fake_key"
        mock_resolve.return_value = "X:BTCUSD"
        mock_client_instance = MockRESTClient.return_value

        # Simulate API error on the first chunk attempt
        mock_response_500 = MagicMock(status_code=500)
        mock_client_instance.get_aggs.side_effect = BadResponse(mock_response_500)

        # Call function
        start_date = "2024-04-01"
        end_date = "2024-04-03"
        result_df = fetch_polygon_data("BTCUSD", "D1", start_date, end_date)

        # Assertions
        self.assertIsNone(result_df) # Should fail if first chunk fails after retries
        # Check that retries happened (call_count > 1)
        self.assertGreaterEqual(mock_client_instance.get_aggs.call_count, 3) # 3 attempts per chunk


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()