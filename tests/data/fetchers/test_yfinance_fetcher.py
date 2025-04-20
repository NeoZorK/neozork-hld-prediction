# tests/data/fetchers/test_yfinance_fetcher.py

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

    # Test cases for map_interval function
    def test_map_interval_valid(self):
        """ Test valid user timeframe inputs for map_interval. """
        self.assertEqual(map_interval("M1"), "1m")
        self.assertEqual(map_interval("H1"), "1h")
        self.assertEqual(map_interval("D1"), "1d")
        self.assertEqual(map_interval("W1"), "1wk")
        self.assertEqual(map_interval("MN1"), "1mo")
        self.assertEqual(map_interval("15m"), "15m") # Pass through valid yf interval

    # Test case for invalid interval mapping
    def test_map_interval_invalid(self):
        """ Test invalid user timeframe input for map_interval. """
        with self.assertRaises(ValueError):
            map_interval("INVALID")

    # Test cases for map_ticker function
    def test_map_ticker_stock(self):
        """ Test stock ticker mapping (should remain unchanged). """
        self.assertEqual(map_ticker("AAPL"), "AAPL")
        self.assertEqual(map_ticker("msft"), "MSFT") # Case conversion

    # Test case for forex ticker mapping
    def test_map_ticker_forex(self):
        """ Test forex ticker mapping (should append '=X'). """
        self.assertEqual(map_ticker("EURUSD"), "EURUSD=X")
        self.assertEqual(map_ticker("gbpjpy"), "GBPJPY=X")

    # Test case for ticker with symbols (should remain unchanged)
    def test_map_ticker_with_symbols(self):
        """ Test tickers with symbols (should remain unchanged). """
        self.assertEqual(map_ticker("ES=F"), "ES=F")
        self.assertEqual(map_ticker("BTC-USD"), "BTC-USD")


    # --- Tests for fetch_yfinance_data ---

    # Test successful fetch with simple columns
    # Patch yf.download and time.perf_counter
    @patch('time.perf_counter')
    @patch('yfinance.download')
    def test_fetch_yfinance_data_success_simple(self, mock_yf_download, mock_perf_counter):
        """
        Test successful data fetching when yf.download returns simple columns.
        Verifies DataFrame structure, columns, and metrics.
        """
        # Configure mock for time.perf_counter
        mock_perf_counter.side_effect = [10.0, 12.5] # Start time, end time

        # Configure mock for yf.download to return a simple DataFrame
        mock_df = pd.DataFrame({
            'Open': [100, 101], 'High': [105, 106], 'Low': [99, 100],
            'Close': [101, 102], 'Volume': [1000, 1100], 'Adj Close': [101, 102] # Include Adj Close
        }, index=pd.to_datetime(['2023-01-01 10:00', '2023-01-01 10:01']))
        mock_df.index.name = 'Datetime' # Simulate yf index name
        mock_yf_download.return_value = mock_df

        # Call the function under test
        result = fetch_yfinance_data(ticker='AAPL', interval='1m', start_date='2023-01-01', end_date='2023-01-02')

        # Assert the result is a tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack the tuple
        df, metrics = result

        # Assert yf.download was called correctly
        mock_yf_download.assert_called_once_with(
            tickers='AAPL', period=None, interval='1m', start='2023-01-01', end='2023-01-02',
            progress=True, auto_adjust=False, actions=False
        )

        # Assert DataFrame structure and content
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 2)
        # Check columns (should include OHLCV, Adj Close should be dropped or ignored by checks)
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.assertTrue(all(col in df.columns for col in expected_cols))
        self.assertEqual(df.index.name, 'DateTime') # Check index name standardization

        # Assert metrics
        self.assertIsInstance(metrics, dict)
        self.assertIn('latency_sec', metrics)
        self.assertAlmostEqual(metrics['latency_sec'], 2.5) # 12.5 - 10.0

    # Test successful fetch with MultiIndex columns that flatten correctly
    # Patch yf.download and time.perf_counter
    @patch('time.perf_counter')
    @patch('yfinance.download')
    def test_fetch_yfinance_data_success_multiindex_flatten(self, mock_yf_download, mock_perf_counter):
        """
        Test successful fetching when yf.download returns MultiIndex columns
        that trigger the flattening logic and are correctly renamed.
        Verifies DataFrame structure, renamed columns, and metrics.
        """
        # Configure mock for time.perf_counter
        mock_perf_counter.side_effect = [20.0, 21.8] # Start time, end time

        # Configure mock for yf.download to return a MultiIndex DataFrame
        # This structure should trigger flattening because droplevel(0) would yield duplicate 'AAPL'
        columns = pd.MultiIndex.from_tuples([
            ('Adj Close', 'AAPL'), ('Close', 'AAPL'), ('High', 'AAPL'),
            ('Low', 'AAPL'), ('Open', 'AAPL'), ('Volume', 'AAPL')
        ], names=['Price', 'Ticker'])
        mock_df = pd.DataFrame({
            ('Adj Close', 'AAPL'): [150.0], ('Close', 'AAPL'): [151.0], ('High', 'AAPL'): [152.0],
            ('Low', 'AAPL'): [149.0], ('Open', 'AAPL'): [150.5], ('Volume', 'AAPL'): [2000000]
        }, index=pd.to_datetime(['2023-01-03 10:00']), columns=columns)
        mock_df.index.name = 'Datetime'
        mock_yf_download.return_value = mock_df

        # Call the function under test (provide ticker in correct case for suffix check)
        result = fetch_yfinance_data(ticker='AAPL', interval='1h', start_date='2023-01-03', end_date='2023-01-04')

        # Assert the result is a tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack the tuple
        df, metrics = result

        # Assert DataFrame structure and renamed columns
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 1)
        # Check columns were correctly flattened and renamed
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume'] # Adj Close should not be here after processing? Check fetcher logic.
        # Fetcher logic currently doesn't explicitly drop Adj Close, but it's not in required_cols.
        # Let's check if the required ones are present with standard names.
        self.assertTrue(all(col in df.columns for col in expected_cols))
        # Verify that original flattened names are gone
        self.assertNotIn('Open_AAPL', df.columns)
        self.assertEqual(df.index.name, 'DateTime')

        # Assert metrics
        self.assertIsInstance(metrics, dict)
        self.assertIn('latency_sec', metrics)
        self.assertAlmostEqual(metrics['latency_sec'], 1.8) # 21.8 - 20.0


    # Test case where yf.download returns no data
    # Patch yf.download and time.perf_counter
    @patch('time.perf_counter')
    @patch('yfinance.download')
    def test_fetch_yfinance_data_no_data(self, mock_yf_download, mock_perf_counter):
        """
        Test behavior when yf.download returns an empty DataFrame.
        Expects (None, metrics with latency).
        """
        # Configure mock for time.perf_counter
        mock_perf_counter.side_effect = [30.0, 30.5]

        # Configure mock for yf.download to return an empty DataFrame
        mock_yf_download.return_value = pd.DataFrame()

        # Call the function under test
        result = fetch_yfinance_data(ticker='NONEXISTENT', interval='1d', start_date='2023-01-01', end_date='2023-01-02')

        # Assert the result is a tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack the tuple
        df, metrics = result

        # Assert DataFrame is None
        self.assertIsNone(df)

        # Assert metrics (latency should still be calculated)
        self.assertIsInstance(metrics, dict)
        self.assertIn('latency_sec', metrics)
        self.assertAlmostEqual(metrics['latency_sec'], 0.5) # 30.5 - 30.0

    # Test case where yf.download raises an exception
    # Patch yf.download and time.perf_counter
    @patch('time.perf_counter')
    @patch('yfinance.download')
    def test_fetch_yfinance_data_exception(self, mock_yf_download, mock_perf_counter):
        """
        Test behavior when yf.download raises an exception.
        Expects (None, metrics with latency=None or 0 if exception is immediate).
        """
        # Configure mock for time.perf_counter (might only capture start time if exception is immediate)
        mock_perf_counter.side_effect = [40.0, 40.1] # Simulate quick failure

        # Configure mock for yf.download to raise an exception
        mock_yf_download.side_effect = Exception("Simulated yfinance download error")

        # Call the function under test
        result = fetch_yfinance_data(ticker='ERROR', interval='1d', start_date='2023-01-01', end_date='2023-01-02')

        # Assert the result is a tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack the tuple
        df, metrics = result

        # Assert DataFrame is None
        self.assertIsNone(df)

        # Assert metrics (latency might be calculated depending on when exception occurs)
        # The current try/except block calculates latency *after* the call, so if the call
        # raises an exception, latency might not be calculated or might be calculated based
        # on the time before the exception. Let's check if the key exists.
        self.assertIsInstance(metrics, dict)
        self.assertIn('latency_sec', metrics)
        # Depending on exact timing, latency might be None or calculated.
        # If the exception is truly immediate, start/end times might not be captured correctly.
        # For this test setup, it should calculate latency based on the mock side_effect:
        self.assertAlmostEqual(metrics['latency_sec'], 0.1)


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()