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
    BINANCE_AVAILABLE
)

# Import or define exceptions correctly
try:
    from binance.exceptions import BinanceAPIException, BinanceRequestException
except ImportError:
    BINANCE_AVAILABLE = False
    class BinanceAPIException(Exception):
         # FIX: Update dummy to match expected signature based on usage
         def __init__(self, message, status_code=None):
             self.status_code = status_code
             # Add code attribute if the fetcher code uses it
             self.code = None # Example if fetcher checks e.g., e.code == -1121
             super().__init__(message)
    class BinanceRequestException(Exception): pass


# --- Helper function to create mock kline data ---
def create_mock_kline(timestamp_ms, o, h, l, c, v):
    """ Creates a mock kline list matching Binance API structure. """
    return [timestamp_ms, str(o), str(h), str(l), str(c), str(v), timestamp_ms + 59999, '1000.0', 10, '50.0', '500.0', '0']


# Definition of the TestBinanceFetcher class
@unittest.skipIf(not BINANCE_AVAILABLE, "python-binance library not installed, skipping tests")
class TestBinanceFetcher(unittest.TestCase):
    """
    Test suite for Binance related functions. Requires python-binance.
    """

    # Test cases for map_binance_interval function (No changes needed)
    def test_map_binance_interval_valid(self):
        from binance.client import Client as BinanceClient # Import only if available
        self.assertEqual(map_binance_interval("M1"), BinanceClient.KLINE_INTERVAL_1MINUTE)
        self.assertEqual(map_binance_interval("H1"), BinanceClient.KLINE_INTERVAL_1HOUR)
        self.assertEqual(map_binance_interval("15m"), "15m") # Pass through
    def test_map_binance_interval_invalid(self):
        self.assertIsNone(map_binance_interval("INVALID"))

    # Test cases for map_binance_ticker function (No changes needed)
    def test_map_binance_ticker(self):
        self.assertEqual(map_binance_ticker("BTC/USDT"), "BTCUSDT")
        self.assertEqual(map_binance_ticker("eth-usdt"), "ETHUSDT")
        self.assertEqual(map_binance_ticker("AdaUsdt"), "ADAUSDT")


    # --- Tests for fetch_binance_data ---

    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_success_single_chunk(self, mock_getenv, mock_binance_client_class, mock_sleep, mock_perf_counter):
        mock_getenv.side_effect = lambda key: "FAKE_KEY" if key == "BINANCE_API_KEY" else "FAKE_SECRET" if key == "BINANCE_API_SECRET" else None
        mock_client_instance = mock_binance_client_class.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        mock_klines_list = [
            create_mock_kline(1672531200000, 40000, 40100, 39900, 40050, 100),
            create_mock_kline(1672531260000, 40050, 40150, 40000, 40100, 120)
        ]
        mock_get_klines.return_value = mock_klines_list
        mock_perf_counter.side_effect = [100.0, 100.9]
        result = fetch_binance_data(ticker="BTCUSDT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        mock_binance_client_class.assert_called_once_with(api_key="FAKE_KEY", api_secret="FAKE_SECRET")
        start_ts = int(datetime.strptime("2023-01-01", '%Y-%m-%d').timestamp() * 1000)
        end_ts = int(datetime.strptime("2023-01-02", '%Y-%m-%d').timestamp() * 1000) - 1
        # FIX: Assert interval using the mapped string '1m'
        mock_get_klines.assert_called_once_with(
            symbol="BTCUSDT", interval='1m', # Use string '1m'
            start_str=str(start_ts), end_str=str(end_ts), limit=1000
        )
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 2)
        self.assertIsInstance(metrics, dict); self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.9)

    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_pagination(self, mock_getenv, mock_binance_client_class, mock_sleep, mock_perf_counter):
        mock_getenv.side_effect = lambda key: None
        mock_client_instance = mock_binance_client_class.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        # FIX: Simulate first chunk returning full limit to trigger pagination
        mock_klines_chunk1 = [create_mock_kline(1672531200000 + i*60000, 40000+i, 40100+i, 39900+i, 40050+i, 100+i) for i in range(1000)] # 1000 items
        mock_klines_chunk2 = [create_mock_kline(mock_klines_chunk1[-1][0] + 60000, 41000, 41100, 40900, 41050, 150)] # 1 item in second chunk
        mock_get_klines.side_effect = [mock_klines_chunk1, mock_klines_chunk2] # Only two calls needed now
        mock_perf_counter.side_effect = [110.0, 112.6, 113.0, 113.5] # Timing for 2 calls
        result = fetch_binance_data(ticker="ETHUSDT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        # FIX: Expect only 2 calls now
        self.assertEqual(mock_get_klines.call_count, 2)
        start_ts_req1 = 1672531200000
        end_ts_req = int(datetime.strptime("2023-01-02", '%Y-%m-%d').timestamp() * 1000) - 1
        start_ts_req2 = mock_klines_chunk1[-1][0] + 1
        calls = [
            call(symbol="ETHUSDT", interval='1m', start_str=str(start_ts_req1), end_str=str(end_ts_req), limit=1000),
            call(symbol="ETHUSDT", interval='1m', start_str=str(start_ts_req2), end_str=str(end_ts_req), limit=1000),
        ]
        mock_get_klines.assert_has_calls(calls)
        # FIX: Expect 1001 rows
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 1001)
        self.assertIsInstance(metrics, dict); self.assertIn("total_latency_sec", metrics)
        expected_latency = (112.6 - 110.0) + (113.5 - 113.0)
        self.assertAlmostEqual(metrics["total_latency_sec"], expected_latency)

    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_api_error_429_retry_fail(self, mock_getenv, mock_binance_client_class, mock_sleep, mock_perf_counter):
        mock_getenv.side_effect = lambda key: None
        mock_client_instance = mock_binance_client_class.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        # FIX: Instantiate BinanceAPIException correctly (message only, maybe status_code)
        # Check python-binance docs for exact signature, let's assume message & status_code
        mock_get_klines.side_effect = BinanceAPIException(status_code=429, message="Rate limit exceeded")
        mock_perf_counter.side_effect = [120.0, 120.1, 120.2, 120.3, 120.4]
        result = fetch_binance_data(ticker="ADAUSDT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        self.assertEqual(mock_get_klines.call_count, 5)
        self.assertIsInstance(metrics, dict); self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_api_error_other(self, mock_getenv, mock_binance_client_class, mock_sleep, mock_perf_counter):
        mock_getenv.side_effect = lambda key: None
        mock_client_instance = mock_binance_client_class.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        # FIX: Instantiate BinanceAPIException correctly
        # Let's add the 'code' attribute manually if the fetcher checks it
        error_instance = BinanceAPIException(status_code=400, message="Invalid symbol.")
        error_instance.code = -1121 # Add code if checked in fetcher
        mock_get_klines.side_effect = error_instance
        mock_perf_counter.side_effect = [130.0]
        result = fetch_binance_data(ticker="INVALID", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        mock_get_klines.assert_called_once()
        self.assertIsInstance(metrics, dict); self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    # Test invalid date format (No changes needed)
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    def test_fetch_binance_data_invalid_date(self, mock_binance_client_class):
        result = fetch_binance_data(ticker="BTCUSDT", interval="M1", start_date="01/01/2023", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        self.assertEqual(metrics, {"total_latency_sec": 0.0})


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()