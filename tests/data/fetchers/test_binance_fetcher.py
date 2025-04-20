# tests/data/fetchers/test_binance_fetcher.py

"""
Unit tests for the Binance data fetcher and related utility functions.
All comments are in English.
"""

import unittest
import pandas as pd
import os
import time
from unittest.mock import patch, MagicMock, call
from datetime import datetime

# Adjust the import path based on the project structure
from src.data.fetchers.binance_fetcher import (
    fetch_binance_data, map_binance_interval, map_binance_ticker,
    BINANCE_AVAILABLE, BinanceAPIException, BinanceRequestException # Import exceptions
)

# Define dummy exceptions if binance is not installed
if not BINANCE_AVAILABLE:
    class BinanceAPIException(Exception):
        def __init__(self, status_code, code, message):
            self.status_code = status_code
            self.code = code
            super().__init__(message)
    class BinanceRequestException(Exception): pass


# --- Helper function to create mock kline data ---
def create_mock_kline(timestamp_ms, o, h, l, c, v):
    """ Creates a mock kline list matching Binance API structure. """
    # Structure: [OpenTime, Open, High, Low, Close, Volume, CloseTime, QuoteAssetVolume, NumberTrades, TakerBuyBaseVol, TakerBuyQuoteVol, Ignore]
    return [timestamp_ms, str(o), str(h), str(l), str(c), str(v), timestamp_ms + 59999, '1000.0', 10, '50.0', '500.0', '0']


# Definition of the TestBinanceFetcher class
@unittest.skipIf(not BINANCE_AVAILABLE, "python-binance library not installed, skipping tests")
class TestBinanceFetcher(unittest.TestCase):
    """
    Test suite for Binance related functions. Requires python-binance.
    """

    # Test cases for map_binance_interval function
    def test_map_binance_interval_valid(self):
        """ Test valid user timeframe inputs for map_binance_interval. """
        from binance.client import Client as BinanceClient # Import only if available
        self.assertEqual(map_binance_interval("M1"), BinanceClient.KLINE_INTERVAL_1MINUTE)
        self.assertEqual(map_binance_interval("H1"), BinanceClient.KLINE_INTERVAL_1HOUR)
        self.assertEqual(map_binance_interval("D1"), BinanceClient.KLINE_INTERVAL_1DAY)
        self.assertEqual(map_binance_interval("W1"), BinanceClient.KLINE_INTERVAL_1WEEK)
        self.assertEqual(map_binance_interval("MN1"), BinanceClient.KLINE_INTERVAL_1MONTH)
        self.assertEqual(map_binance_interval("15m"), "15m") # Pass through

    # Test case for invalid interval mapping
    def test_map_binance_interval_invalid(self):
        """ Test invalid user timeframe input for map_binance_interval. """
        self.assertIsNone(map_binance_interval("INVALID"))

    # Test cases for map_binance_ticker function
    def test_map_binance_ticker(self):
        """ Test ticker formatting for Binance. """
        self.assertEqual(map_binance_ticker("BTC/USDT"), "BTCUSDT")
        self.assertEqual(map_binance_ticker("eth-usdt"), "ETHUSDT")
        self.assertEqual(map_binance_ticker("AdaUsdt"), "ADAUSDT")


    # --- Tests for fetch_binance_data ---

    # Patch os.getenv, binance.Client, time.sleep, time.perf_counter
    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None) # Patch sleep in fetch_binance_data
    @patch('src.data.fetchers.binance_fetcher.BinanceClient') # Patch client class
    @patch('os.getenv')
    def test_fetch_binance_data_success_single_chunk(self, mock_getenv, mock_binance_client_class, mock_sleep, mock_perf_counter):
        """
        Test successful fetch when data fits in a single chunk.
        Verifies DataFrame, metrics (latency).
        """
        # --- Mock Configuration ---
        # Mock getenv to simulate key presence (optional, as fetcher handles missing keys)
        mock_getenv.side_effect = lambda key: "FAKE_KEY" if key == "BINANCE_API_KEY" else "FAKE_SECRET" if key == "BINANCE_API_SECRET" else None
        mock_client_instance = mock_binance_client_class.return_value
        mock_get_klines = mock_client_instance.get_historical_klines

        # Mock data returned by get_historical_klines (single chunk)
        mock_klines_list = [
            create_mock_kline(1672531200000, 40000, 40100, 39900, 40050, 100), # 2023-01-01 00:00:00 UTC
            create_mock_kline(1672531260000, 40050, 40150, 40000, 40100, 120)  # 2023-01-01 00:01:00 UTC
        ]
        mock_get_klines.return_value = mock_klines_list

        # Mock time.perf_counter for latency calculation
        mock_perf_counter.side_effect = [100.0, 100.9] # Start and end time for the single get_historical_klines call

        # --- Call Function Under Test ---
        result = fetch_binance_data(ticker="BTCUSDT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")

        # --- Assertions ---
        # Check result tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack
        df, metrics = result

        # Check client initialization
        mock_binance_client_class.assert_called_once_with(api_key="FAKE_KEY", api_secret="FAKE_SECRET")

        # Check get_historical_klines call
        start_ts = int(datetime.strptime("2023-01-01", '%Y-%m-%d').timestamp() * 1000)
        # End timestamp is end_date + 1 day - 1 millisecond
        end_ts = int(datetime.strptime("2023-01-02", '%Y-%m-%d').timestamp() * 1000) - 1
        mock_get_klines.assert_called_once_with(
            symbol="BTCUSDT", interval="1m",
            start_str=str(start_ts), end_str=str(end_ts), limit=1000
        )

        # Check DataFrame
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 2)
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.assertListEqual(df.columns.tolist(), expected_cols)
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertEqual(df.index.name, 'DateTime')

        # Check Metrics
        self.assertIsInstance(metrics, dict)
        self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.9) # 100.9 - 100.0

    # Patch os.getenv, binance.Client, time.sleep, time.perf_counter
    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_pagination(self, mock_getenv, mock_binance_client_class, mock_sleep, mock_perf_counter):
        """
        Test successful fetch requiring pagination (multiple chunks).
        Verifies combined DataFrame and summed latency.
        """
        # --- Mock Configuration ---
        mock_getenv.side_effect = lambda key: None # Simulate no keys
        mock_client_instance = mock_binance_client_class.return_value
        mock_get_klines = mock_client_instance.get_historical_klines

        # Mock data spanning multiple chunks (Binance limit is 1000)
        # Chunk 1: Returns 2 klines, last timestamp determines next start
        mock_klines_chunk1 = [
            create_mock_kline(1672531200000, 40000, 40100, 39900, 40050, 100), # 2023-01-01 00:00:00
            create_mock_kline(1672531260000, 40050, 40150, 40000, 40100, 120)  # 2023-01-01 00:01:00
        ]
        # Chunk 2: Returns 1 kline, last timestamp + 1ms is used for next potential call
        mock_klines_chunk2 = [
             create_mock_kline(1672531320000, 40100, 40200, 40050, 40150, 110)  # 2023-01-01 00:02:00
        ]
        # Chunk 3: Returns empty list, stopping pagination
        mock_klines_chunk3 = []
        mock_get_klines.side_effect = [mock_klines_chunk1, mock_klines_chunk2, mock_klines_chunk3]

        # Mock time.perf_counter for two successful chunks
        mock_perf_counter.side_effect = [
            110.0, 110.6, # Chunk 1 start, end
            111.0, 111.5  # Chunk 2 start, end (Chunk 3 returns empty, no timing needed)
        ]

        # --- Call Function Under Test ---
        result = fetch_binance_data(ticker="ETHUSDT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")

        # --- Assertions ---
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result

        # Check get_historical_klines calls (called 3 times)
        self.assertEqual(mock_get_klines.call_count, 3)
        start_ts_req1 = 1672531200000 # Initial start
        end_ts_req = int(datetime.strptime("2023-01-02", '%Y-%m-%d').timestamp() * 1000) - 1 # Overall end for all calls
        start_ts_req2 = mock_klines_chunk1[-1][0] + 1 # Start for chunk 2
        start_ts_req3 = mock_klines_chunk2[-1][0] + 1 # Start for chunk 3

        calls = [
            call(symbol="ETHUSDT", interval="1m", start_str=str(start_ts_req1), end_str=str(end_ts_req), limit=1000),
            call(symbol="ETHUSDT", interval="1m", start_str=str(start_ts_req2), end_str=str(end_ts_req), limit=1000),
            call(symbol="ETHUSDT", interval="1m", start_str=str(start_ts_req3), end_str=str(end_ts_req), limit=1000),
        ]
        mock_get_klines.assert_has_calls(calls)

        # Check DataFrame (combined from chunks 1 and 2)
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 3) # 2 rows from chunk1 + 1 row from chunk2

        # Check Metrics (latency should be summed for successful chunks)
        self.assertIsInstance(metrics, dict)
        self.assertIn("total_latency_sec", metrics)
        expected_latency = (110.6 - 110.0) + (111.5 - 111.0) # Latency chunk 1 + Latency chunk 2
        self.assertAlmostEqual(metrics["total_latency_sec"], expected_latency)


    # Patch os.getenv, binance.Client, time.sleep, time.perf_counter
    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_api_error_429_retry_fail(self, mock_getenv, mock_binance_client_class, mock_sleep, mock_perf_counter):
        """
        Test API error 429 (rate limit) that fails after retries.
        Expects (None, metrics with 0 latency).
        """
        # --- Mock Configuration ---
        mock_getenv.side_effect = lambda key: None
        mock_client_instance = mock_binance_client_class.return_value
        mock_get_klines = mock_client_instance.get_historical_klines

        # Mock get_klines to raise 429 repeatedly
        mock_get_klines.side_effect = BinanceAPIException(status_code=429, code=-1003, message="Rate limit exceeded")

        # Mock time.perf_counter - may not capture end times if exception is immediate within the call
        mock_perf_counter.side_effect = [120.0, 120.1, 120.2, 120.3, 120.4] # Start times for attempts

        # --- Call Function Under Test ---
        result = fetch_binance_data(ticker="ADAUSDT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")

        # --- Assertions ---
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        # Check get_klines called multiple times (default 5 attempts)
        self.assertEqual(mock_get_klines.call_count, 5)
        # Check Metrics (latency should be 0 as no chunk succeeded)
        self.assertIsInstance(metrics, dict)
        self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    # Patch os.getenv, binance.Client, time.sleep, time.perf_counter
    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_api_error_other(self, mock_getenv, mock_binance_client_class, mock_sleep, mock_perf_counter):
        """
        Test other non-retriable API error (e.g., invalid symbol).
        Expects (None, metrics with 0 latency).
        """
         # --- Mock Configuration ---
        mock_getenv.side_effect = lambda key: None
        mock_client_instance = mock_binance_client_class.return_value
        mock_get_klines = mock_client_instance.get_historical_klines

        # Mock get_klines to raise invalid symbol error
        mock_get_klines.side_effect = BinanceAPIException(status_code=400, code=-1121, message="Invalid symbol.")

        mock_perf_counter.side_effect = [130.0] # Only start time relevant

        # --- Call Function Under Test ---
        result = fetch_binance_data(ticker="INVALID", interval="M1", start_date="2023-01-01", end_date="2023-01-01")

         # --- Assertions ---
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        # Check get_klines called once
        mock_get_klines.assert_called_once()
        # Check Metrics (latency should be 0)
        self.assertIsInstance(metrics, dict)
        self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    # Test invalid date format
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    def test_fetch_binance_data_invalid_date(self, mock_binance_client_class):
        """ Test providing an invalid date format. """
        result = fetch_binance_data(ticker="BTCUSDT", interval="M1", start_date="01/01/2023", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        self.assertEqual(metrics, {"total_latency_sec": 0.0}) # Returns initialized metrics


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()