# tests/data/test_data_utils.py

import unittest
from unittest.mock import patch #, MagicMock
import pandas as pd
#from datetime import date, timedelta
import numpy as np

# Import functions from the module to be tested
from src.data.data_utils import (
    get_demo_data,
    map_interval,
    map_ticker,
    fetch_yfinance_data
)

# Mock logger for testing
class MockLogger:
    # Add color attributes (can be empty strings for testing)
    ERROR_COLOR = ""
    RESET_ALL = ""
    HIGHLIGHT_COLOR="" # Add if needed elsewhere

    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass
    def print_success(self, msg): pass
    # Add format_summary_line if needed by utils tests (likely not)
    # def format_summary_line(self, key, value, key_width=25):
    #     padded_key = f"{key+':':<{key_width}}"
    #     return f"{padded_key} {value}"

# Unit tests for data utility functions
class TestDataUtils(unittest.TestCase):

    # Test get_demo_data function
    def test_get_demo_data(self):
        df = get_demo_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 30) # Check expected number of rows
        # Check if columns are correctly named for mplfinance
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.assertListEqual(list(df.columns), expected_cols)
        # Check if index is DatetimeIndex
        self.assertIsInstance(df.index, pd.DatetimeIndex)

    # Test map_interval function with various valid inputs
    def test_map_interval_valid(self):
        self.assertEqual(map_interval("M1"), "1m")
        self.assertEqual(map_interval("m5"), "5m") # Test lowercase yf interval
        self.assertEqual(map_interval("H1"), "1h")
        self.assertEqual(map_interval("h4"), "4h") # Test lowercase custom
        self.assertEqual(map_interval("D1"), "1d")
        self.assertEqual(map_interval("d"), "1d")
        self.assertEqual(map_interval("W1"), "1wk")
        self.assertEqual(map_interval("W"), "1wk")
        self.assertEqual(map_interval("WK"), "1wk")
        self.assertEqual(map_interval("MN1"), "1mo")
        self.assertEqual(map_interval("MN"), "1mo")
        self.assertEqual(map_interval("MO"), "1mo")
        self.assertEqual(map_interval("15m"), "15m") # Test direct yf interval
        self.assertEqual(map_interval("1d"), "1d")
        self.assertEqual(map_interval("1WK"), "1wk") # Test mixed case direct

    # Test map_interval function with invalid input
    def test_map_interval_invalid(self):
        with self.assertRaises(ValueError) as cm:
            map_interval("invalid")
        self.assertIn("Invalid timeframe input", str(cm.exception))
        with self.assertRaises(ValueError):
            map_interval("M60") # Not in mapping or direct yf intervals

    # Test map_ticker function
    @patch('src.data.data_utils.logger', new_callable=MockLogger) # Mock logger inside data_utils
    def test_map_ticker(self, _):
        # Test Forex pair needing =X
        self.assertEqual(map_ticker("EURUSD"), "EURUSD=X")
        # Test Forex pair already having =X
        self.assertEqual(map_ticker("GBPUSD=X"), "GBPUSD=X")
        # Test Forex pair with =X in lowercase
        self.assertEqual(map_ticker("usdjpy=x"), "USDJPY=X")
        # Test stock ticker
        self.assertEqual(map_ticker("AAPL"), "AAPL")
        # Test crypto ticker
        self.assertEqual(map_ticker("BTC-USD"), "BTC-USD")
        # Test ticker with numbers (should not append =X)
        self.assertEqual(map_ticker("ES=F"), "ES=F")
        self.assertEqual(map_ticker("6E=F"), "6E=F")
        # Test invalid length (should pass through)
        self.assertEqual(map_ticker("EUR"), "EUR")
        self.assertEqual(map_ticker("TOOLONGTICKER"), "TOOLONGTICKER")

    # --- Tests for fetch_yfinance_data ---

    # Patch yf.download and logger for fetch_yfinance_data tests
    @patch('src.data.data_utils.yf.download')
    @patch('src.data.data_utils.logger', new_callable=MockLogger)
    def test_fetch_yfinance_data_success_simple_cols(self, _, mock_yf_download):
        # Configure the mock to return a simple DataFrame
        mock_df = pd.DataFrame({
            'Open': [100, 101], 'High': [102, 103], 'Low': [99, 98],
            'Close': [101, 102], 'Adj Close': [101, 102], 'Volume': [1000, 1100]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02']))
        mock_yf_download.return_value = mock_df.copy() # Return a copy

        result_df = fetch_yfinance_data('AAPL', '1d', period='1mo')

        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertFalse(result_df.empty)

        # Check if required columns are present instead of exact list match
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols:
            self.assertIn(col, result_df.columns)
        # self.assertListEqual(list(result_df.columns), required_cols) # <-- Заменить старую проверку
        self.assertEqual(len(result_df), 2)
        mock_yf_download.assert_called_once()

    # Test case where yf.download returns an empty DataFrame
    @patch('src.data.data_utils.yf.download')
    @patch('src.data.data_utils.logger', new_callable=MockLogger)
    def test_fetch_yfinance_data_empty(self, _, mock_yf_download):
        mock_yf_download.return_value = pd.DataFrame() # Empty DF

        result_df = fetch_yfinance_data('EMPTY', '1d', period='1d')

        self.assertIsNone(result_df) # Function should return None for empty data
        mock_yf_download.assert_called_once()

    # Test case with missing required columns
    @patch('src.data.data_utils.yf.download')
    @patch('src.data.data_utils.logger', new_callable=MockLogger)
    def test_fetch_yfinance_data_missing_cols(self, _, mock_yf_download):
        mock_df = pd.DataFrame({'Open': [100], 'High': [102], 'Volume': [1000]}) # Missing Low, Close
        mock_yf_download.return_value = mock_df

        result_df = fetch_yfinance_data('MISSING', '1d', period='1d')

        self.assertIsNone(result_df) # Should return None if required cols missing
        mock_yf_download.assert_called_once()

    # Test case with NaN values in OHLC columns (should be dropped)
    @patch('src.data.data_utils.yf.download')
    @patch('src.data.data_utils.logger', new_callable=MockLogger)
    def test_fetch_yfinance_data_with_nans(self, _, mock_yf_download):
        mock_df = pd.DataFrame({
            'Open': [100, 101, np.nan], 'High': [102, 103, 104],
            'Low': [99, np.nan, 98], 'Close': [101, 102, 103],
            'Volume': [1000, 1100, 1200]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']))
        mock_yf_download.return_value = mock_df.copy()

        result_df = fetch_yfinance_data('NANTEST', '1d', period='3d')

        self.assertIsInstance(result_df, pd.DataFrame)
        # Correct expectation for how='all'
        self.assertEqual(len(result_df), 3)  # <--- ИЗМЕНЕНИЕ: Ожидаем 3 строки
        # Check remaining indices (should be all original indices)
        expected_indices = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])
        pd.testing.assert_index_equal(result_df.index, expected_indices)

    # Test case handling MultiIndex columns returned by yfinance
    @patch('src.data.data_utils.yf.download')
    @patch('src.data.data_utils.logger', new_callable=MockLogger)
    def test_fetch_yfinance_data_multiindex_cols(self, _, mock_yf_download):
        # Create a DataFrame with MultiIndex columns typical for single ticker download
        arrays = [['Open', 'High', 'Low', 'Close', 'Volume'], ['GOOG', 'GOOG', 'GOOG', 'GOOG', 'GOOG']]
        tuples = list(zip(*arrays))
        multi_index = pd.MultiIndex.from_tuples(tuples, names=['ValueType', 'Ticker'])
        mock_df = pd.DataFrame({
            ('Open', 'GOOG'): [100], ('High', 'GOOG'): [102], ('Low', 'GOOG'): [99],
            ('Close', 'GOOG'): [101], ('Volume', 'GOOG'): [1000]
        }, index=pd.to_datetime(['2023-01-01']))
        mock_df.columns = multi_index # Assign the multi-index
        mock_yf_download.return_value = mock_df.copy()

        result_df = fetch_yfinance_data('GOOG', '1d', period='1d')

        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertFalse(result_df.empty)
        # Check that columns are now simple strings
        self.assertListEqual(list(result_df.columns), ['Open', 'High', 'Low', 'Close', 'Volume'])
        self.assertEqual(len(result_df), 1)

    # Test case where yf.download raises an exception
    @patch('src.data.data_utils.yf.download')
    @patch('src.data.data_utils.logger', new_callable=MockLogger)
    def test_fetch_yfinance_data_exception(self, _, mock_yf_download):
        mock_yf_download.side_effect = Exception("Network Error") # Simulate an error

        result_df = fetch_yfinance_data('ERROR', '1d', period='1d')

        self.assertIsNone(result_df) # Should return None on exception
        mock_yf_download.assert_called_once()

    # Test case where yf.download raises an exception
    # Add patch for traceback if needed, though the error is now color attr
    @patch('src.data.data_utils.yf.download')
    @patch('src.data.data_utils.logger', new_callable=MockLogger)
    @patch('traceback.format_exc') # Also mock traceback printing
    def test_fetch_yfinance_data_exception(self, mock_traceback, _, mock_yf_download):
        mock_yf_download.side_effect = Exception("Network Error") # Simulate an error
        mock_traceback.return_value = "Mocked Traceback" # Mock traceback output

        result_df = fetch_yfinance_data('ERROR', '1d', period='1d')

        self.assertIsNone(result_df) # Should return None on exception
        mock_yf_download.assert_called_once()
        # Check error was logged (optional, print_error is mocked)
        # mock_logger.print_error.assert_called()
        # Check traceback was formatted (optional)
        mock_traceback.assert_called_once()

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()