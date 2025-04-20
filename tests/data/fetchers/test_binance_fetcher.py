# tests/data/fetchers/test_binance_fetcher.py (Исправления v6)

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
    # Define a mock class based on the error message demanding positional args
    # status_code and text
    class MockBinanceAPIException(Exception): # Inherit from Base Exception
        def __init__(self, status_code, text, code=None, message=None): # Match positional from error msg
            self.status_code = status_code
            self.text = text
            self.code = code
            # Construct a meaningful message for super()
            msg = message or f"Mock Binance Error: Status={status_code}, Text='{text}', Code={code}"
            super().__init__(msg)

except ImportError:
    BINANCE_AVAILABLE = False
    # Dummy needs similar structure if used
    class MockBinanceAPIException(Exception):
         def __init__(self, status_code, text, code=None, message=None):
             self.status_code = status_code
             self.text = text
             self.code = code
             msg = message or f"Mock Binance Error: Status={status_code}, Text='{text}', Code={code}"
             super().__init__(msg)
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

    # Test cases for map_binance_interval function (No changes)
    def test_map_binance_interval_valid(self):
        from binance.client import Client as BinanceClient
        self.assertEqual(map_binance_interval("M1"), BinanceClient.KLINE_INTERVAL_1MINUTE)
        self.assertEqual(map_binance_interval("H1"), BinanceClient.KLINE_INTERVAL_1HOUR)
        self.assertEqual(map_binance_interval("15m"), "15m")
    def test_map_binance_interval_invalid(self):
        self.assertIsNone(map_binance_interval("INVALID"))

    # Test cases for map_binance_ticker function (No changes)
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
        mock_klines_list = [ create_mock_kline(1672531200000+i*60000, 40000+i, 40100+i, 39900+i, 40050+i, 100+i) for i in range(2) ] # 2 items < 1000 limit
        mock_get_klines.return_value = mock_klines_list
        mock_perf_counter.side_effect = [100.0, 100.9]
        result = fetch_binance_data(ticker="BTCUSDT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        start_ts = int(datetime.strptime("2023-01-01", '%Y-%m-%d').timestamp() * 1000)
        end_ts = int(datetime.strptime("2023-01-02", '%Y-%m-%d').timestamp() * 1000) - 1
        # FIX: Assert interval using the mapped string '1m'
        mock_get_klines.assert_called_once_with(
            symbol="BTCUSDT", interval='1m', # USE STRING
            start_str=str(start_ts), end_str=str(end_ts), limit=1000
        )
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 2)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.9)

    @patch('time.perf_counter')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_pagination(self, mock_getenv, mock_binance_client_class, mock_sleep, mock_perf_counter):
        mock_getenv.side_effect = lambda key: None
        mock_client_instance = mock_binance_client_class.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        ts_start = 1672531200000
        # Chunk 1 returns exactly 1000 items
        mock_klines_chunk1 = [create_mock_kline(ts_start + i*60000, 40000+i, 40100+i, 39900+i, 40050+i, 100+i) for i in range(1000)]
        last_ts_chunk1 = mock_klines_chunk1[-1][0]
        # Chunk 2 returns 1 item (less than limit)
        mock_klines_chunk2 = [create_mock_kline(last_ts_chunk1 + 60000, 41000, 41100, 40900, 41050, 150)]
        mock_get_klines.side_effect = [mock_klines_chunk1, mock_klines_chunk2]
        mock_perf_counter.side_effect = [110.0, 112.6, 113.0, 113.5]
        result = fetch_binance_data(ticker="ETHUSDT", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        df, metrics = result
        self.assertEqual(mock_get_klines.call_count, 2)
        start_ts_req1 = 1672531200000
        end_ts_req = int(datetime.strptime("2023-01-02", '%Y-%m-%d').timestamp() * 1000) - 1
        start_ts_req2 = last_ts_chunk1 + 1
        calls = [
            # FIX: Check interval using string '1m'
            call(symbol="ETHUSDT", interval='1m', start_str=str(start_ts_req1), end_str=str(end_ts_req), limit=1000),
            call(symbol="ETHUSDT", interval='1m', start_str=str(start_ts_req2), end_str=str(end_ts_req), limit=1000),
        ]
        mock_get_klines.assert_has_calls(calls, any_order=False) # Check calls in order
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 1001)
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
        # FIX: Instantiate MockBinanceAPIException based on error message
        # Pass positional status_code, text
        error_instance = MockBinanceAPIException(status_code=429, text="Rate limit exceeded", code=-1003)
        mock_get_klines.side_effect = error_instance
        mock_perf_counter.side_effect = [120.0, 120.1, 120.2, 120.3, 120.4, 120.5]
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
        # FIX: Instantiate MockBinanceAPIException correctly
        error_instance = MockBinanceAPIException(status_code=400, text="Invalid symbol.", code=-1121)
        mock_get_klines.side_effect = error_instance
        mock_perf_counter.side_effect = [130.0, 130.1]
        result = fetch_binance_data(ticker="INVALID", interval="M1", start_date="2023-01-01", end_date="2023-01-01")
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        mock_get_klines.assert_called_once()
        self.assertIsInstance(metrics, dict); self.assertIn("total_latency_sec", metrics)
        self.assertAlmostEqual(metrics["total_latency_sec"], 0.0)

    # Test invalid date format (No changes)
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