# tests/data/fetchers/test_yfinance_fetcher.py # CORRECTED dtype

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np # Import numpy

# Functions to test
from src.data.fetchers.yfinance_fetcher import fetch_yfinance_data, map_interval, map_ticker

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass
    def print_success(self, msg): pass

@patch('src.data.fetchers.yfinance_fetcher.logger', new_callable=MockLogger)
class TestYfinanceFetcher(unittest.TestCase):

    # --- Tests for map_interval ---
    def test_map_interval_mql_style(self, _):
        self.assertEqual(map_interval("M1"), "1m")
        self.assertEqual(map_interval("H1"), "1h")
        self.assertEqual(map_interval("D1"), "1d")
        self.assertEqual(map_interval("W1"), "1wk")
        self.assertEqual(map_interval("MN1"), "1mo")
        self.assertEqual(map_interval("M15"), "15m")
        self.assertEqual(map_interval("W"), "1wk") # Alias
        self.assertEqual(map_interval("MO"), "1mo") # Alias

    def test_map_interval_yf_style(self, _):
        self.assertEqual(map_interval("5m"), "5m")
        self.assertEqual(map_interval("1d"), "1d")
        self.assertEqual(map_interval("1wk"), "1wk")

    def test_map_interval_invalid(self, _):
        with self.assertRaises(ValueError):
            map_interval("invalid")
        with self.assertRaises(ValueError):
            map_interval("1s") # yf doesn't support seconds usually

    # --- Tests for map_ticker ---
    def test_map_ticker_forex(self, _):
        self.assertEqual(map_ticker("EURUSD"), "EURUSD=X")
        self.assertEqual(map_ticker("gbpjpy"), "GBPJPY=X")

    def test_map_ticker_non_forex(self, _):
        self.assertEqual(map_ticker("AAPL"), "AAPL")
        self.assertEqual(map_ticker("MSFT"), "MSFT")
        self.assertEqual(map_ticker("EURUSD=X"), "EURUSD=X") # Already formatted
        self.assertEqual(map_ticker("^GSPC"), "^GSPC")     # Index example

    # --- Tests for fetch_yfinance_data ---
    @patch('src.data.fetchers.yfinance_fetcher.yf.download')
    def test_fetch_yfinance_data_success_period(self, mock_yf_download, _):
        mock_df = pd.DataFrame({
            'Open': [100.0], 'High': [101.0], 'Low': [99.0], 'Close': [100.0], 'Volume': [1000.0]
        }, index=pd.to_datetime(['2023-01-01']), dtype=np.float64) # Specify dtype
        mock_yf_download.return_value = mock_df.copy()

        result_df = fetch_yfinance_data(ticker="AAPL", interval="1d", period="1d")

        mock_yf_download.assert_called_once_with(
            tickers="AAPL", period="1d", interval="1d", start=None, end=None,
            progress=True, auto_adjust=False, actions=False
        )
        self.assertIsNotNone(result_df)
        pd.testing.assert_frame_equal(result_df, mock_df)

    @patch('src.data.fetchers.yfinance_fetcher.yf.download')
    def test_fetch_yfinance_data_success_start_end(self, mock_yf_download, _):
        mock_df = pd.DataFrame({
            'Open': [200.0], 'High': [202.0], 'Low': [198.0], 'Close': [200.0], 'Volume': [2000.0]
        }, index=pd.to_datetime(['2024-02-01']), dtype=np.float64) # Specify dtype
        mock_yf_download.return_value = mock_df.copy()

        result_df = fetch_yfinance_data(ticker="MSFT", interval="1h", start_date="2024-02-01", end_date="2024-02-02")

        mock_yf_download.assert_called_once_with(
            tickers="MSFT", period=None, interval="1h", start="2024-02-01", end="2024-02-02",
            progress=True, auto_adjust=False, actions=False
        )
        self.assertIsNotNone(result_df)
        pd.testing.assert_frame_equal(result_df, mock_df)

    @patch('src.data.fetchers.yfinance_fetcher.yf.download')
    def test_fetch_yfinance_data_download_fails(self, mock_yf_download, _):
        mock_yf_download.return_value = None
        result_df = fetch_yfinance_data(ticker="FAIL", interval="1d", period="1d")
        self.assertIsNone(result_df)

        mock_yf_download.return_value = pd.DataFrame()
        result_df = fetch_yfinance_data(ticker="EMPTY", interval="1d", period="1d")
        self.assertIsNone(result_df)

    @patch('src.data.fetchers.yfinance_fetcher.yf.download')
    def test_fetch_yfinance_data_missing_columns(self, mock_yf_download, _):
        mock_df = pd.DataFrame({'Open': [100], 'volume': [1000]}, index=pd.to_datetime(['2023-01-01']))
        mock_yf_download.return_value = mock_df.copy()
        result_df = fetch_yfinance_data(ticker="BAD", interval="1d", period="1d")
        self.assertIsNone(result_df)

    @patch('src.data.fetchers.yfinance_fetcher.yf.download')
    def test_fetch_yfinance_data_multiindex_success(self, mock_yf_download, _):
        # Simulate MultiIndex columns
        cols = pd.MultiIndex.from_tuples([
             ('Open', 'AAPL'), ('High', 'AAPL'), ('Low', 'AAPL'), ('Close', 'AAPL'), ('Volume', 'AAPL')
        ])
        # Use float data in mock to avoid int64 inference
        mock_df_multi = pd.DataFrame([[100.0, 101.0, 99.0, 100.0, 1000.0]],
            index=pd.to_datetime(['2023-01-01']),
            columns=cols
        )
        mock_yf_download.return_value = mock_df_multi.copy()

        # Expected result after simplification
        expected_df = pd.DataFrame({
            'Open': [100.0], 'High': [101.0], 'Low': [99.0], 'Close': [100.0], 'Volume': [1000.0]
        }, index=pd.to_datetime(['2023-01-01']), dtype=np.float64) # CORRECTED: Specify dtype

        result_df = fetch_yfinance_data(ticker="AAPL", interval="1d", period="1d")

        self.assertIsNotNone(result_df)
        self.assertFalse(isinstance(result_df.columns, pd.MultiIndex))
        self.assertListEqual(list(result_df.columns), ['Open', 'High', 'Low', 'Close', 'Volume'])
        pd.testing.assert_frame_equal(result_df, expected_df) # Should pass now


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()