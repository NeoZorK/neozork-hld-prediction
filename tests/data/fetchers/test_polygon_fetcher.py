# tests/data/fetchers/test_polygon_fetcher.py (Исправления v6)

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
# Try importing the real exception to use its type for patching and isinstance checks
try:
    from polygon.exceptions import BadResponse as PolygonBadResponse
    BaseBadResponseException = PolygonBadResponse # Use real type if available
except ImportError:
    POLYGON_AVAILABLE = False
    # Define dummy if library not installed
    class BaseBadResponseException(Exception):
        def __init__(self, message="Mock BadResponse", response=None):
             super().__init__(message)
             self.response = response if response else create_mock_response(500)
             self.status_code = getattr(self.response, 'status_code', 500)
    PolygonBadResponse = BaseBadResponseException # Use dummy as the target for patching


# --- Import or define Agg correctly ---
try:
    from polygon.rest.models.aggs import Agg
except ImportError:
    class Agg: pass

# --- Helper function to create mock Agg objects ---
def create_mock_agg(timestamp_ms, o, h, l, c, v):
    agg = MagicMock()
    agg.timestamp = timestamp_ms; agg.open = o; agg.high = h; agg.low = l; agg.close = c; agg.volume = v
    return agg

# --- Helper function to create a mock Response ---
def create_mock_response(status_code, json_data=None, text_data=""):
    response = MagicMock(); response.status_code = status_code
    if json_data is not None: response.json.return_value = json_data
    response.text = text_data; response.url = f"mock_url_status_{status_code}"
    return response


# Definition of the TestPolygonFetcher class
# Ensure tests are skipped if the library isn't actually available
@unittest.skipIf(not POLYGON_AVAILABLE, "Polygon library not installed, skipping tests")
class TestPolygonFetcher(unittest.TestCase):
    """ Test suite for Polygon.io related functions. Requires polygon-api-client. """

    # Interval mapping tests (No changes)
    def test_map_polygon_interval_valid(self): self.assertEqual(map_polygon_interval("M1"), ("minute", 1))
    def test_map_polygon_interval_invalid(self): self.assertIsNone(map_polygon_interval("INVALID"))

    # --- Ticker resolution tests (Patch PolygonBadResponse where it's used) ---
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_success(self, mock_sleep, mock_rest_client_class):
        mock_client_instance = mock_rest_client_class.return_value
        mock_client_instance.get_ticker_details.return_value = MagicMock()
        resolved = resolve_polygon_ticker("AAPL", mock_client_instance)
        self.assertEqual(resolved, "AAPL")
        mock_client_instance.get_ticker_details.assert_called_once_with("AAPL")

    # Patch the actual exception where it's imported/used in the fetcher module
    @patch('src.data.fetchers.polygon_fetcher.BadResponse', new=BaseBadResponseException) # Patch the base class (real or dummy)
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_success_prefix(self, mock_sleep, mock_rest_client_class, mock_bad_response_class):
        mock_client_instance = mock_rest_client_class.return_value
        mock_response_404 = create_mock_response(404)
        # Create instance of the patched exception
        error_instance = BaseBadResponseException("Ticker Not Found")
        error_instance.response = mock_response_404 # Add attributes needed by the code
        error_instance.status_code = 404

        mock_client_instance.get_ticker_details.side_effect = [ error_instance, MagicMock() ]
        resolved = resolve_polygon_ticker("EURUSD", mock_client_instance)
        # FIX: Assert result
        self.assertEqual(resolved, "C:EURUSD")
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 2)

    @patch('src.data.fetchers.polygon_fetcher.BadResponse', new=BaseBadResponseException) # Patch the base class
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_not_found(self, mock_sleep, mock_rest_client_class, mock_bad_response_class):
        mock_client_instance = mock_rest_client_class.return_value
        mock_response_404 = create_mock_response(404)
        # FIX: Raise the exception instance repeatedly using lambda
        def raise_404(*args, **kwargs):
             err = BaseBadResponseException("Ticker Not Found")
             err.response = mock_response_404
             err.status_code = 404
             raise err
        mock_client_instance.get_ticker_details.side_effect = raise_404
        resolved = resolve_polygon_ticker("NONEXISTENT", mock_client_instance)
        self.assertIsNone(resolved)
        # FIX: Assert call count is 4
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 4)

    @patch('src.data.fetchers.polygon_fetcher.BadResponse', new=BaseBadResponseException) # Patch the base class
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_api_error(self, mock_sleep, mock_rest_client_class, mock_bad_response_class):
        mock_client_instance = mock_rest_client_class.return_value
        mock_response_500 = create_mock_response(500, text_data="Internal Server Error")
        # FIX: Raise the exception instance
        error_instance = BaseBadResponseException("Server Error")
        error_instance.response = mock_response_500
        error_instance.status_code = 500
        mock_client_instance.get_ticker_details.side_effect = error_instance
        resolved = resolve_polygon_ticker("ANYTICKER", mock_client_instance)
        self.assertIsNone(resolved)
        mock_client_instance.get_ticker_details.assert_called_once_with("ANYTICKER")


    # --- Tests for fetch_polygon_data (Fix perf_counter side_effects, latency asserts, call counts) ---

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
        # FIX: Set side_effect precisely for this test
        mock_perf_counter.side_effect = [50.0, 50.8]
        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 1)
        # FIX: Assert correct latency
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.8) # 50.8 - 50.0

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
        # FIX: Provide exactly 4 values for 2 successful fetches
        mock_perf_counter.side_effect = [60.0, 60.5, # Chunk 1 = 0.5s
                                         61.0, 61.7] # Chunk 2 = 0.7s
        result = fetch_polygon_data(ticker="GE", interval="M1", start_date="2023-01-01", end_date="2023-02-01")
        df, metrics = result
        self.assertEqual(mock_client_instance.get_aggs.call_count, 2)
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 2)
        # FIX: Assert correct summed latency
        expected_latency = (60.5 - 60.0) + (61.7 - 61.0) # 0.5 + 0.7 = 1.2
        self.assertAlmostEqual(metrics["total_latency_sec"], expected_latency)

    # Patch BadResponse where it's used in the fetcher
    @patch('src.data.fetchers.polygon_fetcher.BadResponse', new=BaseBadResponseException)
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
        # FIX: Raise exception instance repeatedly using lambda
        def raise_429(*args, **kwargs):
             err = BaseBadResponseException("Rate Limit")
             err.response = mock_response_429
             err.status_code = 429
             raise err
        mock_client_instance.get_aggs.side_effect = raise_429
        # FIX: perf_counter only called at start of each attempt? No, fetcher calls before try.
        # Provide start/end pairs for *potential* success, although none occur.
        # The latency calculation won't happen anyway. Provide enough values.
        mock_perf_counter.side_effect = [70.0, 70.1, 70.2, 70.3, 70.4, 70.5] # 3 attempts start/end
        result = fetch_polygon_data(ticker="MSFT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNone(df)
        # FIX: Assert call count is 3
        self.assertEqual(mock_client_instance.get_aggs.call_count, 3)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    @patch('src.data.fetchers.polygon_fetcher.BadResponse', new=BaseBadResponseException)
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
        # FIX: Raise exception instance
        error_instance = BaseBadResponseException("Server Error")
        error_instance.response = mock_response_500
        error_instance.status_code = 500
        mock_client_instance.get_aggs.side_effect = error_instance
        # FIX: Provide only 2 values for the single failed attempt start/end
        mock_perf_counter.side_effect = [80.0, 80.1]
        result = fetch_polygon_data(ticker="IBM", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNone(df)
        # FIX: Assert call count is 1
        mock_client_instance.get_aggs.assert_called_once()
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    @patch('os.getenv')
    def test_fetch_polygon_data_no_api_key(self, mock_getenv):
        mock_getenv.return_value = None
        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNone(df)
        self.assertEqual(metrics, {"total_latency_sec": 0.0}) # Initialized metrics

    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_ticker_resolve_fails(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker):
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = None
        mock_client_instance = mock_rest_client_class.return_value
        result = fetch_polygon_data(ticker="FAIL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertIsNone(df)
        mock_resolve_ticker.assert_called_once_with("FAIL", mock_client_instance)
        self.assertEqual(metrics, {"total_latency_sec": 0.0})


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()