# tests/data/fetchers/test_polygon_fetcher.py

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
    # Try importing the real exception first
    from polygon.exceptions import BadResponse
except ImportError:
    # Define dummy if library not installed
    class BadResponse(Exception):
        def __init__(self, message="Mock BadResponse", response=None):
            # Make dummy accept response for compatibility with fetcher code logging it
            super().__init__(message)
            self.response = response

# --- Import or define Agg correctly ---
try:
    from polygon.rest.models.aggs import Agg
except ImportError:
    # Dummy class for Agg if library not installed
    # Don't use spec in MagicMock if using this dummy
    class Agg:
        pass # Minimal definition is enough if spec is not used

# --- Helper function to create mock Agg objects ---
def create_mock_agg(timestamp_ms, o, h, l, c, v):
    """ Creates a mock Agg object for testing. """
    agg = MagicMock() # REMOVED spec=Agg for broader compatibility
    agg.timestamp = timestamp_ms
    agg.open = o
    agg.high = h
    agg.low = l
    agg.close = c
    agg.volume = v
    return agg

# --- Helper function to create a mock Response for BadResponse ---
def create_mock_response(status_code, json_data=None, text_data=""):
    """ Creates a mock Response object for BadResponse exception """
    response = MagicMock()
    response.status_code = status_code
    if json_data is not None:
        response.json.return_value = json_data
    response.text = text_data
    response.url = f"mock_url_status_{status_code}"
    return response


# Definition of the TestPolygonFetcher class
@unittest.skipIf(not POLYGON_AVAILABLE, "Polygon library not installed, skipping tests")
class TestPolygonFetcher(unittest.TestCase):
    """
    Test suite for Polygon.io related functions. Requires polygon-api-client.
    """

    # Test cases for map_polygon_interval function (No changes needed)
    def test_map_polygon_interval_valid(self):
        self.assertEqual(map_polygon_interval("M1"), ("minute", 1))
        self.assertEqual(map_polygon_interval("H1"), ("hour", 1))
        self.assertEqual(map_polygon_interval("day"), ("day", 1))
    def test_map_polygon_interval_invalid(self):
        self.assertIsNone(map_polygon_interval("INVALID"))


    # --- Tests for resolve_polygon_ticker (Correct BadResponse instantiation) ---
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
        # FIX: Instantiate BadResponse correctly (assuming it takes message and optional response)
        # Or just pass the message string if that's how the library expects it.
        # Let's try passing the response object directly to the real exception if possible,
        # or stick to the message for the dummy. Assuming message only for dummy now.
        # If using real library, check its init signature. Let's assume message is enough for now.
        bad_response_404 = BadResponse(f"Ticker Not Found (mock response status {mock_response_404.status_code})")
        # Add the response attribute manually if needed by the fetcher code that catches it
        bad_response_404.response = mock_response_404

        mock_client_instance.get_ticker_details.side_effect = [
            bad_response_404, # Fail for "EURUSD"
            MagicMock()       # Succeed for "C:EURUSD"
        ]
        resolved = resolve_polygon_ticker("EURUSD", mock_client_instance)
        self.assertEqual(resolved, "C:EURUSD")
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 2)

    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_not_found(self, mock_sleep, mock_rest_client_class):
        mock_client_instance = mock_rest_client_class.return_value
        mock_response_404 = create_mock_response(404)
        # FIX: Instantiate BadResponse correctly
        bad_response_404 = BadResponse(f"Ticker Not Found (mock response status {mock_response_404.status_code})")
        bad_response_404.response = mock_response_404
        mock_client_instance.get_ticker_details.side_effect = bad_response_404

        resolved = resolve_polygon_ticker("NONEXISTENT", mock_client_instance)
        self.assertIsNone(resolved)
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 4)

    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_api_error(self, mock_sleep, mock_rest_client_class):
        mock_client_instance = mock_rest_client_class.return_value
        mock_response_500 = create_mock_response(500, text_data="Internal Server Error")
        # FIX: Instantiate BadResponse correctly
        bad_response_500 = BadResponse(f"Server Error (mock response status {mock_response_500.status_code})")
        bad_response_500.response = mock_response_500
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
        mock_aggs_list = [
            create_mock_agg(1672578000000, 130, 131, 129, 130.5, 10000),
            create_mock_agg(1672578060000, 130.5, 132, 130, 131.5, 12000)
        ]
        mock_client_instance.get_aggs.return_value = iter(mock_aggs_list)
        mock_perf_counter.side_effect = [50.0, 50.8]
        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 2)
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
        mock_aggs_chunk1 = [create_mock_agg(1672578000000, 10, 11, 9, 10.5, 1000)]
        mock_aggs_chunk2 = [create_mock_agg(1675256400000, 11, 12, 10, 11.5, 1500)]
        # FIX: Need to simulate returning 50000 items in first chunk to force pagination if chunk_delta is large
        # Let's refine this test - assume minute data over 2 days WILL require > 1 chunk based on date logic
        mock_client_instance.get_aggs.side_effect = [iter(mock_aggs_chunk1), iter(mock_aggs_chunk2)]
        mock_perf_counter.side_effect = [60.0, 60.5, 61.0, 61.7]
        # Use dates forcing 2 chunks for minute data (e.g., 2 days)
        result = fetch_polygon_data(ticker="GE", interval="M1", start_date="2023-01-01", end_date="2023-01-02") # Use 2 days
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        # Check get_aggs called twice for the two days (assuming minute timespan chunking logic works per day here)
        # The chunk delta is 30 days for minute, so 2 days should fit in ONE chunk.
        # Let's adjust the dates to force pagination based on the 30-day chunk delta
        # Test Jan 1st to Feb 1st
        mock_client_instance.get_aggs.reset_mock() # Reset from previous call
        mock_client_instance.get_aggs.side_effect = [iter(mock_aggs_chunk1), iter(mock_aggs_chunk2)] # Reset side effect
        mock_perf_counter.side_effect = [60.0, 60.5, 61.0, 61.7] # Reset perf counter mock
        result = fetch_polygon_data(ticker="GE", interval="M1", start_date="2023-01-01", end_date="2023-02-01")

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
        # FIX: Instantiate BadResponse correctly
        bad_response_429 = BadResponse(f"Rate Limit (mock response status {mock_response_429.status_code})")
        bad_response_429.response = mock_response_429
        mock_client_instance.get_aggs.side_effect = bad_response_429
        mock_perf_counter.side_effect = [70.0, 70.1, 70.2]
        result = fetch_polygon_data(ticker="MSFT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
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
        # FIX: Instantiate BadResponse correctly
        bad_response_500 = BadResponse(f"Server Error (mock response status {mock_response_500.status_code})")
        bad_response_500.response = mock_response_500
        mock_client_instance.get_aggs.side_effect = bad_response_500
        mock_perf_counter.side_effect = [80.0]
        result = fetch_polygon_data(ticker="IBM", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        mock_client_instance.get_aggs.assert_called_once()
        self.assertIsInstance(metrics, dict); self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    # Patch os.getenv - FIX: Add mock_getenv argument to method signature
    @patch('os.getenv')
    def test_fetch_polygon_data_no_api_key(self, mock_getenv):
        """ Test behavior when POLYGON_API_KEY is not set. """
        mock_getenv.return_value = None
        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        self.assertEqual(metrics, {})

    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_ticker_resolve_fails(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker):
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