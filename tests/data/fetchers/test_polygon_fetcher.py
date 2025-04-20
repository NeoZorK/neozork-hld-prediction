# tests/data/fetchers/test_polygon_fetcher.py (Исправления v2)

"""
Unit tests for the Polygon.io data fetcher and related utility functions.
All comments are in English.
"""

import unittest
import pandas as pd
import os
import time
from unittest.mock import patch, MagicMock, PropertyMock, call
from datetime import date

# Adjust the import path based on the project structure
from src.data.fetchers.polygon_fetcher import (
    fetch_polygon_data, map_polygon_interval, resolve_polygon_ticker,
    POLYGON_AVAILABLE
)

# --- Import or define exceptions correctly ---
try:
    from polygon.exceptions import BadResponse
    # Check how BadResponse is typically instantiated or used in the library
    # Often, it's caught and attributes like .response or .status_code are checked.
    # For mocking side_effect, raising a custom exception might be simpler if
    # the exact signature is tricky. Let's try creating a mock that *acts like* BadResponse.
    class MockBadResponse(Exception):
        def __init__(self, message="Mock BadResponse", status_code=500, response=None):
            super().__init__(message)
            self.response = response if response else create_mock_response(status_code, text_data=message)
            # Ensure status_code is accessible if needed by fetcher code
            if hasattr(self.response, 'status_code'):
                 self.status_code = self.response.status_code
            else:
                 self.status_code = status_code


except ImportError:
    POLYGON_AVAILABLE = False
    class MockBadResponse(Exception): # Use same mock structure if library absent
        def __init__(self, message="Mock BadResponse", status_code=500, response=None):
            super().__init__(message)
            self.response = response if response else create_mock_response(status_code, text_data=message)
            if hasattr(self.response, 'status_code'):
                 self.status_code = self.response.status_code
            else:
                 self.status_code = status_code


# --- Import or define Agg correctly ---
try:
    from polygon.rest.models.aggs import Agg
except ImportError:
    class Agg: pass # Dummy class

# --- Helper function to create mock Agg objects ---
def create_mock_agg(timestamp_ms, o, h, l, c, v):
    """ Creates a mock Agg object for testing. """
    agg = MagicMock() # REMOVED spec=Agg
    agg.timestamp = timestamp_ms; agg.open = o; agg.high = h; agg.low = l; agg.close = c; agg.volume = v
    return agg

# --- Helper function to create a mock Response ---
def create_mock_response(status_code, json_data=None, text_data=""):
    """ Creates a mock Response object for BadResponse exception """
    response = MagicMock(); response.status_code = status_code
    if json_data is not None: response.json.return_value = json_data
    response.text = text_data; response.url = f"mock_url_status_{status_code}"
    return response


# Definition of the TestPolygonFetcher class
@unittest.skipIf(not POLYGON_AVAILABLE, "Polygon library not installed, skipping tests")
class TestPolygonFetcher(unittest.TestCase):
    """ Test suite for Polygon.io related functions. Requires polygon-api-client. """

    # Interval mapping tests (No changes)
    def test_map_polygon_interval_valid(self):
        self.assertEqual(map_polygon_interval("M1"), ("minute", 1))
        self.assertEqual(map_polygon_interval("H1"), ("hour", 1))
        self.assertEqual(map_polygon_interval("day"), ("day", 1))
    def test_map_polygon_interval_invalid(self):
        self.assertIsNone(map_polygon_interval("INVALID"))


    # Ticker resolution tests (Use MockBadResponse)
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_success(self, mock_sleep, mock_rest_client_class):
        mock_client_instance = mock_rest_client_class.return_value
        mock_client_instance.get_ticker_details.return_value = MagicMock()
        resolved = resolve_polygon_ticker("AAPL", mock_client_instance)
        self.assertEqual(resolved, "AAPL")
        mock_client_instance.get_ticker_details.assert_called_once_with("AAPL")

    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_success_prefix(self, mock_sleep, mock_rest_client_class):
        mock_client_instance = mock_rest_client_class.return_value
        mock_response_404 = create_mock_response(404)
        # FIX: Use MockBadResponse
        bad_response_404 = MockBadResponse("Ticker Not Found", status_code=404, response=mock_response_404)
        mock_client_instance.get_ticker_details.side_effect = [bad_response_404, MagicMock()]
        resolved = resolve_polygon_ticker("EURUSD", mock_client_instance)
        self.assertEqual(resolved, "C:EURUSD")
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 2)

    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_not_found(self, mock_sleep, mock_rest_client_class):
        mock_client_instance = mock_rest_client_class.return_value
        mock_response_404 = create_mock_response(404)
        # FIX: Use MockBadResponse
        bad_response_404 = MockBadResponse("Ticker Not Found", status_code=404, response=mock_response_404)
        mock_client_instance.get_ticker_details.side_effect = bad_response_404
        resolved = resolve_polygon_ticker("NONEXISTENT", mock_client_instance)
        self.assertIsNone(resolved)
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 4)

    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_api_error(self, mock_sleep, mock_rest_client_class):
        mock_client_instance = mock_rest_client_class.return_value
        mock_response_500 = create_mock_response(500, text_data="Internal Server Error")
        # FIX: Use MockBadResponse
        bad_response_500 = MockBadResponse("Server Error", status_code=500, response=mock_response_500)
        mock_client_instance.get_ticker_details.side_effect = bad_response_500
        resolved = resolve_polygon_ticker("ANYTICKER", mock_client_instance)
        self.assertIsNone(resolved)
        mock_client_instance.get_ticker_details.assert_called_once_with("ANYTICKER")


    # --- Tests for fetch_polygon_data ---

    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_success_single_chunk(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:AAPL"
        mock_client_instance = mock_rest_client_class.return_value
        mock_aggs_list = [ create_mock_agg(1672578000000, 130, 131, 129, 130.5, 10000) ]
        mock_client_instance.get_aggs.return_value = iter(mock_aggs_list)
        # FIX: Provide more values for perf_counter just in case
        mock_perf_counter.side_effect = [50.0, 50.8, 51.0, 51.2] # Extra values shouldn't hurt
        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        # FIX: Assertion should check df is not None AFTER checking result tuple
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 1) # Only 1 mock agg now
        self.assertIsInstance(metrics, dict); self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.8)

    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_pagination(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:GE"
        mock_client_instance = mock_rest_client_class.return_value
        mock_aggs_chunk1 = [create_mock_agg(1672578000000, 10, 11, 9, 10.5, 1000)] # Jan 1st
        mock_aggs_chunk2 = [create_mock_agg(1675256400000, 11, 12, 10, 11.5, 1500)] # Feb 1st
        mock_client_instance.get_aggs.side_effect = [iter(mock_aggs_chunk1), iter(mock_aggs_chunk2)]
        mock_perf_counter.side_effect = [60.0, 60.5, 61.0, 61.7, 62.0, 62.1] # Provide plenty
        # Use dates Jan 1st to Feb 1st to force 2 chunks for 'minute' timespan
        result = fetch_polygon_data(ticker="GE", interval="M1", start_date="2023-01-01", end_date="2023-02-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        # FIX: Assert call count is 2
        self.assertEqual(mock_client_instance.get_aggs.call_count, 2)
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 2)
        self.assertIsInstance(metrics, dict); self.assertIn("total_latency_sec", metrics)
        expected_latency = (60.5 - 60.0) + (61.7 - 61.0)
        self.assertAlmostEqual(metrics["total_latency_sec"], expected_latency)


    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_api_error_retry_fail(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:MSFT"
        mock_client_instance = mock_rest_client_class.return_value
        mock_response_429 = create_mock_response(429)
        # FIX: Use MockBadResponse
        bad_response_429 = MockBadResponse("Rate Limit", status_code=429, response=mock_response_429)
        mock_client_instance.get_aggs.side_effect = bad_response_429
        # FIX: Ensure enough values for 3 attempts (start each time)
        mock_perf_counter.side_effect = [70.0, 70.1, 70.2, 70.3, 70.4]
        result = fetch_polygon_data(ticker="MSFT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        # FIX: Assert call count is 3 (should retry 3 times on 429)
        self.assertEqual(mock_client_instance.get_aggs.call_count, 3)
        self.assertIsInstance(metrics, dict); self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_api_error_non_retriable(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:IBM"
        mock_client_instance = mock_rest_client_class.return_value
        mock_response_500 = create_mock_response(500)
        # FIX: Use MockBadResponse
        bad_response_500 = MockBadResponse("Server Error", status_code=500, response=mock_response_500)
        mock_client_instance.get_aggs.side_effect = bad_response_500
        # FIX: Provide at least 2 values for start/end potential
        mock_perf_counter.side_effect = [80.0, 80.1]
        result = fetch_polygon_data(ticker="IBM", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        mock_client_instance.get_aggs.assert_called_once()
        self.assertIsInstance(metrics, dict); self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    # FIX: Add mock_getenv argument
    @patch('os.getenv')
    def test_fetch_polygon_data_no_api_key(self, mock_getenv):
        """ Test behavior when POLYGON_API_KEY is not set. """
        mock_getenv.return_value = None
        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        # FIX: Assert against expected initial metrics, not empty dict
        self.assertEqual(metrics, {"total_latency_sec": 0.0})

    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_ticker_resolve_fails(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker):
        # This test seems correct already
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = None
        mock_client_instance = mock_rest_client_class.return_value
        result = fetch_polygon_data(ticker="FAIL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        mock_resolve_ticker.assert_called_once_with("FAIL", mock_client_instance)
        self.assertEqual(metrics, {"total_latency_sec": 0.0})


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()