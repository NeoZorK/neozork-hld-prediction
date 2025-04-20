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
    POLYGON_AVAILABLE, BadResponse # Import exception for mocking
)

# Mock Agg class if polygon library is not available
if not POLYGON_AVAILABLE:
    class Agg: # Dummy class
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    # Define BadResponse if not imported
    class BadResponse(Exception):
        def __init__(self, message="Mock BadResponse", response=None):
            super().__init__(message)
            self.response = response

# --- Helper function to create mock Agg objects ---
def create_mock_agg(timestamp_ms, o, h, l, c, v):
    """ Creates a mock Agg object for testing. """
    agg = MagicMock(spec=Agg) # Use MagicMock to allow attribute assignment
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
    # Add url attribute for logging within the fetcher
    response.url = f"mock_url_status_{status_code}"
    return response


# Definition of the TestPolygonFetcher class
@unittest.skipIf(not POLYGON_AVAILABLE, "Polygon library not installed, skipping tests")
class TestPolygonFetcher(unittest.TestCase):
    """
    Test suite for Polygon.io related functions. Requires polygon-api-client.
    """

    # Test cases for map_polygon_interval function
    def test_map_polygon_interval_valid(self):
        """ Test valid user timeframe inputs for map_polygon_interval. """
        self.assertEqual(map_polygon_interval("M1"), ("minute", 1))
        self.assertEqual(map_polygon_interval("H1"), ("hour", 1))
        self.assertEqual(map_polygon_interval("D1"), ("day", 1))
        self.assertEqual(map_polygon_interval("W1"), ("week", 1))
        self.assertEqual(map_polygon_interval("MN1"), ("month", 1))
        self.assertEqual(map_polygon_interval("day"), ("day", 1)) # Pass through

    # Test case for invalid interval mapping
    def test_map_polygon_interval_invalid(self):
        """ Test invalid user timeframe input for map_polygon_interval. """
        self.assertIsNone(map_polygon_interval("INVALID"))


    # --- Tests for resolve_polygon_ticker ---
    # Patch RESTClient for these tests
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None) # Patch sleep within resolve
    def test_resolve_polygon_ticker_success(self, mock_sleep, mock_rest_client_class):
        """ Test successful ticker resolution. """
        mock_client_instance = mock_rest_client_class.return_value
        # Configure get_ticker_details to succeed on the first try
        mock_client_instance.get_ticker_details.return_value = MagicMock() # Simulate success

        resolved = resolve_polygon_ticker("AAPL", mock_client_instance)
        self.assertEqual(resolved, "AAPL")
        mock_client_instance.get_ticker_details.assert_called_once_with("AAPL")

    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_success_prefix(self, mock_sleep, mock_rest_client_class):
        """ Test successful ticker resolution using a prefix. """
        mock_client_instance = mock_rest_client_class.return_value
        # Configure get_ticker_details to fail on first, succeed on second (C: prefix)
        mock_response_404 = create_mock_response(404)
        mock_client_instance.get_ticker_details.side_effect = [
            BadResponse("Not Found", response=mock_response_404), # Fail for "EURUSD"
            MagicMock() # Succeed for "C:EURUSD"
        ]

        resolved = resolve_polygon_ticker("EURUSD", mock_client_instance)
        self.assertEqual(resolved, "C:EURUSD")
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 2)
        mock_client_instance.get_ticker_details.assert_has_calls([
            call("EURUSD"), call("C:EURUSD")
        ])

    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_not_found(self, mock_sleep, mock_rest_client_class):
        """ Test ticker resolution when ticker is not found with any prefix. """
        mock_client_instance = mock_rest_client_class.return_value
        # Configure get_ticker_details to raise 404 for all attempts
        mock_response_404 = create_mock_response(404)
        mock_client_instance.get_ticker_details.side_effect = BadResponse("Not Found", response=mock_response_404)

        resolved = resolve_polygon_ticker("NONEXISTENT", mock_client_instance)
        self.assertIsNone(resolved)
        # Called for NONEXISTENT, C:NONEXISTENT, X:NONEXISTENT, I:NONEXISTENT
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 4)

    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('time.sleep', return_value=None)
    def test_resolve_polygon_ticker_api_error(self, mock_sleep, mock_rest_client_class):
        """ Test ticker resolution when a non-404 API error occurs. """
        mock_client_instance = mock_rest_client_class.return_value
        # Configure get_ticker_details to raise a 500 error
        mock_response_500 = create_mock_response(500, text_data="Internal Server Error")
        mock_client_instance.get_ticker_details.side_effect = BadResponse("Server Error", response=mock_response_500)

        resolved = resolve_polygon_ticker("ANYTICKER", mock_client_instance)
        self.assertIsNone(resolved)
        mock_client_instance.get_ticker_details.assert_called_once_with("ANYTICKER")


    # --- Tests for fetch_polygon_data ---

    # Patch os.getenv, polygon.RESTClient, resolve_polygon_ticker, time.sleep, time.perf_counter
    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None) # Patch sleep in fetch_polygon_data
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_success_single_chunk(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        """
        Test successful fetch when data fits in a single chunk.
        Verifies DataFrame, metrics (latency).
        """
        # --- Mock Configuration ---
        mock_getenv.return_value = "FAKE_API_KEY" # Mock API key
        mock_resolve_ticker.return_value = "T:AAPL" # Mock successful resolution
        mock_client_instance = mock_rest_client_class.return_value

        # Mock data returned by get_aggs (single chunk)
        mock_aggs_list = [
            create_mock_agg(1672578000000, 130, 131, 129, 130.5, 10000), # 2023-01-01 10:00:00
            create_mock_agg(1672578060000, 130.5, 132, 130, 131.5, 12000) # 2023-01-01 10:01:00
        ]
        mock_client_instance.get_aggs.return_value = iter(mock_aggs_list) # Return iterator

        # Mock time.perf_counter for latency calculation
        mock_perf_counter.side_effect = [50.0, 50.8] # Start and end time for the single get_aggs call

        # --- Call Function Under Test ---
        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")

        # --- Assertions ---
        # Check result tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack
        df, metrics = result

        # Check client initialization and ticker resolution
        mock_getenv.assert_called_with("POLYGON_API_KEY")
        mock_rest_client_class.assert_called_once_with(api_key="FAKE_API_KEY")
        mock_resolve_ticker.assert_called_once_with("AAPL", mock_client_instance)

        # Check get_aggs call
        mock_client_instance.get_aggs.assert_called_once_with(
            ticker="T:AAPL", multiplier=1, timespan="minute",
            from_=date(2023, 1, 1), to=date(2023, 1, 1),
            adjusted=False, limit=50000
        )

        # Check DataFrame
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 2)
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.assertListEqual(df.columns.tolist(), expected_cols)
        self.assertIsInstance(df.index, pd.DatetimeIndex)

        # Check Metrics
        self.assertIsInstance(metrics, dict)
        self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.8) # 50.8 - 50.0

    # Patch os.getenv, polygon.RESTClient, resolve_polygon_ticker, time.sleep, time.perf_counter
    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_pagination(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        """
        Test successful fetch requiring pagination (multiple chunks).
        Verifies combined DataFrame and summed latency.
        """
        # --- Mock Configuration ---
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:GE"
        mock_client_instance = mock_rest_client_class.return_value

        # Mock data returned by get_aggs (two chunks for minute data over >30 days)
        mock_aggs_chunk1 = [create_mock_agg(1672578000000, 10, 11, 9, 10.5, 1000)] # 2023-01-01
        mock_aggs_chunk2 = [create_mock_agg(1675256400000, 11, 12, 10, 11.5, 1500)] # 2023-02-01
        # Simulate get_aggs returning different lists on subsequent calls
        mock_client_instance.get_aggs.side_effect = [iter(mock_aggs_chunk1), iter(mock_aggs_chunk2)]

        # Mock time.perf_counter for two successful chunks
        mock_perf_counter.side_effect = [
            60.0, 60.5, # Chunk 1 start, end
            61.0, 61.7  # Chunk 2 start, end (assuming 0.5s sleep mock doesn't affect perf_counter)
        ]

        # --- Call Function Under Test ---
        # Use dates requiring > 1 chunk for minute data (e.g., > 30 days apart)
        result = fetch_polygon_data(ticker="GE", interval="M1", start_date="2023-01-01", end_date="2023-02-01")

        # --- Assertions ---
        # Check result tuple
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result

        # Check get_aggs calls (called twice)
        self.assertEqual(mock_client_instance.get_aggs.call_count, 2)
        calls = [
            call(ticker="T:GE", multiplier=1, timespan="minute", from_=date(2023, 1, 1), to=date(2023, 1, 31), adjusted=False, limit=50000), # Chunk 1 (Jan)
            call(ticker="T:GE", multiplier=1, timespan="minute", from_=date(2023, 2, 1), to=date(2023, 2, 1), adjusted=False, limit=50000)  # Chunk 2 (Feb 1st)
        ]
        mock_client_instance.get_aggs.assert_has_calls(calls)

        # Check DataFrame (combined from both chunks)
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 2) # 1 row from chunk1 + 1 row from chunk2

        # Check Metrics (latency should be summed)
        self.assertIsInstance(metrics, dict)
        self.assertIn("total_latency_sec", metrics)
        expected_latency = (60.5 - 60.0) + (61.7 - 61.0) # Latency chunk 1 + Latency chunk 2
        self.assertAlmostEqual(metrics["total_latency_sec"], expected_latency)


    # Patch os.getenv, polygon.RESTClient, resolve_polygon_ticker, time.sleep, time.perf_counter
    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_api_error_retry_fail(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        """
        Test API error (e.g., 429 rate limit) that fails after retries.
        Expects (None, metrics with partial latency if any attempt measured).
        """
        # --- Mock Configuration ---
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:MSFT"
        mock_client_instance = mock_rest_client_class.return_value

        # Mock get_aggs to raise 429 (rate limit) repeatedly
        mock_response_429 = create_mock_response(429)
        mock_client_instance.get_aggs.side_effect = BadResponse("Rate limit", response=mock_response_429)

        # Mock time.perf_counter - it won't get to the 'end' time in this case
        mock_perf_counter.side_effect = [
             70.0, # Attempt 1 start
             70.1, # Attempt 2 start (after sleep)
             70.2  # Attempt 3 start (after sleep)
        ]

        # --- Call Function Under Test ---
        result = fetch_polygon_data(ticker="MSFT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")

        # --- Assertions ---
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result

        # Check DataFrame is None
        self.assertIsNone(df)

        # Check get_aggs was called multiple times (default 3 attempts)
        self.assertEqual(mock_client_instance.get_aggs.call_count, 3)

        # Check Metrics (latency should be 0 as no chunk succeeded)
        self.assertIsInstance(metrics, dict)
        self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    # Patch os.getenv, polygon.RESTClient, resolve_polygon_ticker, time.sleep, time.perf_counter
    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_api_error_non_retriable(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker, mock_sleep, mock_perf_counter):
        """
        Test API error that is not retried (e.g., 500).
        Expects (None, metrics with 0 latency).
        """
        # --- Mock Configuration ---
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = "T:IBM"
        mock_client_instance = mock_rest_client_class.return_value

        # Mock get_aggs to raise 500 error on first attempt
        mock_response_500 = create_mock_response(500)
        mock_client_instance.get_aggs.side_effect = BadResponse("Server Error", response=mock_response_500)

        mock_perf_counter.side_effect = [80.0] # Only start time is relevant

        # --- Call Function Under Test ---
        result = fetch_polygon_data(ticker="IBM", interval="M1", start_date="2023-01-01", end_date="2023-01-01")

        # --- Assertions ---
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        mock_client_instance.get_aggs.assert_called_once() # Called only once
        self.assertIsInstance(metrics, dict)
        self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    # Patch os.getenv
    def test_fetch_polygon_data_no_api_key(self, mock_getenv):
        """ Test behavior when POLYGON_API_KEY is not set. """
        mock_getenv.return_value = None # Simulate missing key
        result = fetch_polygon_data(ticker="AAPL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        self.assertEqual(metrics, {}) # Should return empty metrics dict early

    # Patch os.getenv, polygon.RESTClient, resolve_polygon_ticker
    @patch('src.data.fetchers.polygon_fetcher.resolve_polygon_ticker')
    @patch('src.data.fetchers.polygon_fetcher.polygon.RESTClient')
    @patch('os.getenv')
    def test_fetch_polygon_data_ticker_resolve_fails(self, mock_getenv, mock_rest_client_class, mock_resolve_ticker):
        """ Test behavior when ticker resolution fails. """
        mock_getenv.return_value = "FAKE_API_KEY"
        mock_resolve_ticker.return_value = None # Simulate resolution failure
        mock_client_instance = mock_rest_client_class.return_value

        result = fetch_polygon_data(ticker="FAIL", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        mock_resolve_ticker.assert_called_once_with("FAIL", mock_client_instance)
        self.assertEqual(metrics, {"total_latency_sec": 0.0}) # Returns initialized metrics


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()