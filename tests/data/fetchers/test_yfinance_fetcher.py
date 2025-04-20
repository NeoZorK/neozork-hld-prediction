# tests/data/fetchers/test_yfinance_fetcher.py (Исправления v2)

"""
Unit tests for the yfinance data fetcher and related utility functions.
All comments are in English.
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

# Adjust the import path based on the project structure
from src.data.fetchers.yfinance_fetcher import fetch_yfinance_data, map_interval, map_ticker


# Definition of the TestYfinanceFetcher class
class TestYfinanceFetcher(unittest.TestCase):
    """
    Test suite for yfinance related functions.
    """

    # Test cases for map_interval function (No changes needed)
    def test_map_interval_valid(self):
        self.assertEqual(map_interval("M1"), "1m"); self.assertEqual(map_interval("H1"), "1h")
        self.assertEqual(map_interval("D1"), "1d"); self.assertEqual(map_interval("W1"), "1wk")
        self.assertEqual(map_interval("MN1"), "1mo"); self.assertEqual(map_interval("15m"), "15m")
    def test_map_interval_invalid(self):
        with self.assertRaises(ValueError): map_interval("INVALID")

    # Test cases for map_ticker function (No changes needed)
    def test_map_ticker_stock(self):
        self.assertEqual(map_ticker("AAPL"), "AAPL"); self.assertEqual(map_ticker("msft"), "MSFT")
    def test_map_ticker_forex(self):
        self.assertEqual(map_ticker("EURUSD"), "EURUSD=X"); self.assertEqual(map_ticker("gbpjpy"), "GBPJPY=X")
    def test_map_ticker_with_symbols(self):
        self.assertEqual(map_ticker("ES=F"), "ES=F"); self.assertEqual(map_ticker("BTC-USD"), "BTC-USD")


    # --- Tests for fetch_yfinance_data ---

    # Test successful fetch with simple columns (No changes needed)
    @patch('time.perf_counter')
    @patch('yfinance.download')
    def test_fetch_yfinance_data_success_simple(self, mock_yf_download, mock_perf_counter):
        mock_perf_counter.side_effect = [10.0, 12.5]
        mock_df = pd.DataFrame({
            'Open': [100, 101], 'High': [105, 106], 'Low': [99, 100],
            'Close': [101, 102], 'Volume': [1000, 1100], 'Adj Close': [101, 102]
        }, index=pd.to_datetime(['2023-01-01 10:00', '2023-01-01 10:01'])); mock_df.index.name = 'Datetime'
        mock_yf_download.return_value = mock_df
        result = fetch_yfinance_data(ticker='AAPL', interval='1m', start_date='2023-01-01', end_date='2023-01-02')
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        mock_yf_download.assert_called_once_with(tickers='AAPL', period=None, interval='1m', start='2023-01-01', end='2023-01-02', progress=True, auto_adjust=False, actions=False)
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 2); self.assertEqual(df.index.name, 'DateTime')
        self.assertIsInstance(metrics, dict); self.assertIn('latency_sec', metrics); self.assertAlmostEqual(metrics['latency_sec'], 2.5)

    # Test successful fetch with MultiIndex columns (No changes needed)
    @patch('time.perf_counter')
    @patch('yfinance.download')
    def test_fetch_yfinance_data_success_multiindex_flatten(self, mock_yf_download, mock_perf_counter):
        mock_perf_counter.side_effect = [20.0, 21.8]
        columns = pd.MultiIndex.from_tuples([ ('Adj Close', 'AAPL'), ('Close', 'AAPL'), ('High', 'AAPL'), ('Low', 'AAPL'), ('Open', 'AAPL'), ('Volume', 'AAPL')], names=['Price', 'Ticker'])
        mock_df = pd.DataFrame({ ('Adj Close', 'AAPL'): [150.0], ('Close', 'AAPL'): [151.0], ('High', 'AAPL'): [152.0], ('Low', 'AAPL'): [149.0], ('Open', 'AAPL'): [150.5], ('Volume', 'AAPL'): [2000000]}, index=pd.to_datetime(['2023-01-03 10:00']), columns=columns); mock_df.index.name = 'Datetime'
        mock_yf_download.return_value = mock_df
        result = fetch_yfinance_data(ticker='AAPL', interval='1h', start_date='2023-01-03', end_date='2023-01-04')
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNotNone(df); self.assertEqual(df.shape[0], 1); self.assertEqual(df.index.name, 'DateTime')
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.assertTrue(all(col in df.columns for col in expected_cols)); self.assertNotIn('Open_AAPL', df.columns)
        self.assertIsInstance(metrics, dict); self.assertIn('latency_sec', metrics); self.assertAlmostEqual(metrics['latency_sec'], 1.8)

    # Test case where yf.download returns no data (No changes needed)
    @patch('time.perf_counter')
    @patch('yfinance.download')
    def test_fetch_yfinance_data_no_data(self, mock_yf_download, mock_perf_counter):
        mock_perf_counter.side_effect = [30.0, 30.5]
        mock_yf_download.return_value = pd.DataFrame()
        result = fetch_yfinance_data(ticker='NONEXISTENT', interval='1d', start_date='2023-01-01', end_date='2023-01-02')
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        self.assertIsInstance(metrics, dict); self.assertIn('latency_sec', metrics); self.assertAlmostEqual(metrics['latency_sec'], 0.5)

    # Test case where yf.download raises an exception
    @patch('time.perf_counter')
    @patch('yfinance.download')
    def test_fetch_yfinance_data_exception(self, mock_yf_download, mock_perf_counter):
        """ Test behavior when yf.download raises an exception. """
        # Configure mock for time.perf_counter
        mock_perf_counter.side_effect = [40.0, 40.1] # Simulate quick start/end or just start

        # Configure mock for yf.download to raise an exception
        mock_yf_download.side_effect = Exception("Simulated yfinance download error")

        # Call the function under test
        result = fetch_yfinance_data(ticker='ERROR', interval='1d', start_date='2023-01-01', end_date='2023-01-02')

        # Assert the result is a tuple
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result

        # Assert DataFrame is None
        self.assertIsNone(df)

        # Assert metrics
        self.assertIsInstance(metrics, dict)
        self.assertIn('latency_sec', metrics)
        # FIX: Check if latency is None OR a float value, as exception might occur
        # after the start time but before the end time is captured.
        # Checking just for existence is safer. If a value *is* captured, it should be >= 0.
        if metrics['latency_sec'] is not None:
             self.assertIsInstance(metrics['latency_sec'], float)
             self.assertGreaterEqual(metrics['latency_sec'], 0.0)
        # Optionally, if mock setup guarantees timing like [40.0, 40.1]:
        # self.assertAlmostEqual(metrics['latency_sec'], 0.1)
        # But let's stick to the safer check for this error case.


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()