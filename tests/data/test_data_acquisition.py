# tests/data/test_data_acquisition.py # UPDATED PATCH TARGETS

import unittest
from unittest.mock import patch #, MagicMock # Import MagicMock
import argparse
import pandas as pd


# Import the function to test
from src.data.data_acquisition import acquire_data
# Import functions for type hinting or direct use if necessary,
# but patching targets will be within data_acquisition's scope
# from src.data.fetchers import get_demo_data, fetch_csv_data # etc.


# Create a dummy logger class
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass
    def print_success(self, msg): pass

# Create a dummy args namespace helper function
def create_mock_args(mode='demo', ticker=None, interval='D1', period='1y',
                     start=None, end=None, point=None, rule=None, csv_file=None):
    return argparse.Namespace(
        mode=mode, ticker=ticker, interval=interval, period=period,
        start=start, end=end, point=point, rule=rule, csv_file=csv_file
    )

# Unit tests for the data acquisition step
# Patch the logger for the whole class
@patch('src.data.data_acquisition.logger', new_callable=MockLogger)
class TestDataAcquisition(unittest.TestCase):

    # Patch the specific fetcher functions *where they are looked up by acquire_data*

    # --- Demo Mode Test ---
    @patch('src.data.data_acquisition.get_demo_data') # Patch lookup within acquire_data
    def test_acquire_data_demo_mode(self, mock_get_demo_data, _ ):
        demo_df = pd.DataFrame({'Open': [1], 'High': [1.1], 'Low': [0.9], 'Close': [1], 'Volume': [100]})
        mock_get_demo_data.return_value = demo_df
        args = create_mock_args(mode='demo')
        result = acquire_data(args)
        mock_get_demo_data.assert_called_once()
        self.assertEqual(result['effective_mode'], 'demo')
        self.assertTrue(result['ohlcv_df'].equals(demo_df))
        # ... other demo assertions ...

    # --- CSV Mode Test ---
    @patch('src.data.data_acquisition.fetch_csv_data') # Patch lookup within acquire_data
    def test_acquire_data_csv_mode(self, mock_fetch_csv_data, _):
        csv_df = pd.DataFrame({'Open': [1.1], 'Volume': [1000]})
        mock_fetch_csv_data.return_value = csv_df
        csv_path = "data/my_test.csv"
        args = create_mock_args(mode='csv', csv_file=csv_path)
        result = acquire_data(args)
        mock_fetch_csv_data.assert_called_once_with(filepath=csv_path)
        self.assertEqual(result['effective_mode'], 'csv')
        self.assertTrue(result['ohlcv_df'].equals(csv_df))
        # ... other csv assertions ...

    # --- YFinance Mode Tests ---
    @patch('src.data.data_acquisition.fetch_yfinance_data') # Patch lookup
    @patch('src.data.data_acquisition.map_ticker')         # Patch lookup
    @patch('src.data.data_acquisition.map_interval')        # Patch lookup
    def test_acquire_data_yfinance_mode_period(self, mock_map_interval, mock_map_ticker, mock_fetch_yfinance_data, _):
        yf_df = pd.DataFrame({'Open': [10]})
        mock_fetch_yfinance_data.return_value = yf_df
        mock_map_interval.return_value = '1d'
        mock_map_ticker.return_value = 'AAPL'
        args = create_mock_args(mode='yf', ticker='AAPL', period='1mo', interval='D1')
        result = acquire_data(args)
        mock_map_interval.assert_called_once_with('D1')
        mock_map_ticker.assert_called_once_with('AAPL')
        mock_fetch_yfinance_data.assert_called_once_with(ticker='AAPL', interval='1d', period='1mo', start_date=None, end_date=None)
        self.assertEqual(result['effective_mode'], 'yfinance')
        self.assertTrue(result['ohlcv_df'].equals(yf_df))
        # ... other yf period assertions ...

    @patch('src.data.data_acquisition.fetch_yfinance_data') # Patch lookup
    @patch('src.data.data_acquisition.map_ticker')         # Patch lookup
    @patch('src.data.data_acquisition.map_interval')        # Patch lookup
    def test_acquire_data_yfinance_mode_start_end(self, mock_map_interval, mock_map_ticker, mock_fetch_yfinance_data, _):
        yf_df = pd.DataFrame({'Open': [20]})
        mock_fetch_yfinance_data.return_value = yf_df
        mock_map_interval.return_value = '1h'
        mock_map_ticker.return_value = 'MSFT'
        args = create_mock_args(mode='yfinance', ticker='MSFT', interval='H1', start='2024-01-01', end='2024-01-31')
        result = acquire_data(args)
        mock_fetch_yfinance_data.assert_called_once_with(ticker='MSFT', interval='1h', period=None, start_date='2024-01-01', end_date='2024-01-31')
        self.assertEqual(result['effective_mode'], 'yfinance')
        # ... other yf start/end assertions ...

    @patch('src.data.data_acquisition.fetch_yfinance_data') # Patch lookup
    @patch('src.data.data_acquisition.map_ticker')         # Patch lookup
    @patch('src.data.data_acquisition.map_interval')        # Patch lookup
    def test_acquire_data_yfinance_fetch_fail(self, mock_map_interval, mock_map_ticker, mock_fetch_yfinance_data, _):
        mock_fetch_yfinance_data.return_value = None # Simulate failure
        mock_map_interval.return_value = '1d'
        mock_map_ticker.return_value = 'FAIL'
        args = create_mock_args(mode='yf', ticker='FAIL', period='1d')
        result = acquire_data(args)
        self.assertIsNone(result['ohlcv_df'])
        self.assertEqual(result['effective_mode'], 'yfinance')

    # --- Polygon Mode Test ---
    @patch('src.data.data_acquisition.fetch_polygon_data') # Patch lookup within acquire_data
    def test_acquire_data_polygon_mode(self, mock_fetch_polygon_data, _):
        poly_df = pd.DataFrame({'Open': [100], 'Volume': [5000]})
        mock_fetch_polygon_data.return_value = poly_df
        args = create_mock_args(
            mode='polygon', ticker='AAPL', interval='D1',
            start='2024-01-01', end='2024-01-10'
        )
        result = acquire_data(args)
        mock_fetch_polygon_data.assert_called_once_with(
            ticker='AAPL', interval='D1',
            start_date='2024-01-01', end_date='2024-01-10'
        )
        self.assertEqual(result['effective_mode'], 'polygon')
        self.assertTrue(result['ohlcv_df'].equals(poly_df))
        # ... other polygon assertions ...

    # --- Binance Mode Test ---
    @patch('src.data.data_acquisition.fetch_binance_data') # Patch lookup within acquire_data
    def test_acquire_data_binance_mode(self, mock_fetch_binance_data, _):
        binance_df = pd.DataFrame({'Open': [30000], 'Volume': [100]})
        mock_fetch_binance_data.return_value = binance_df
        args = create_mock_args(
            mode='binance', ticker='BTCUSDT', interval='H1',
            start='2024-04-01', end='2024-04-05'
        )
        result = acquire_data(args)
        mock_fetch_binance_data.assert_called_once_with(
            ticker='BTCUSDT', interval='H1',
            start_date='2024-04-01', end_date='2024-04-05'
        )
        self.assertEqual(result['effective_mode'], 'binance')
        self.assertTrue(result['ohlcv_df'].equals(binance_df))
        # ... other binance assertions ...

    # --- Failure Tests ---
    @patch('src.data.data_acquisition.fetch_csv_data')
    def test_acquire_data_csv_fetch_fail(self, mock_fetch_csv_data, _):
        mock_fetch_csv_data.return_value = None
        args = create_mock_args(mode='csv', csv_file="fail.csv")
        result = acquire_data(args)
        self.assertIsNone(result['ohlcv_df'])
        self.assertEqual(result['effective_mode'], 'csv')

    @patch('src.data.data_acquisition.fetch_polygon_data')
    def test_acquire_data_polygon_fetch_fail(self, mock_fetch_polygon_data, _):
        mock_fetch_polygon_data.return_value = None
        args = create_mock_args(mode='polygon', ticker='FAIL', interval='D1', start='2024-01-01', end='2024-01-10')
        result = acquire_data(args)
        self.assertIsNone(result['ohlcv_df'])
        self.assertEqual(result['effective_mode'], 'polygon')

    @patch('src.data.data_acquisition.fetch_binance_data')
    def test_acquire_data_binance_fetch_fail(self, mock_fetch_binance_data, _):
        mock_fetch_binance_data.return_value = None
        args = create_mock_args(mode='binance', ticker='FAIL', interval='D1', start='2024-01-01', end='2024-01-10')
        result = acquire_data(args)
        self.assertIsNone(result['ohlcv_df'])
        self.assertEqual(result['effective_mode'], 'binance')


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()