# tests/data/test_data_acquisition.py

import unittest
from unittest.mock import patch #, MagicMock
import argparse
import pandas as pd
from datetime import date

# Import the function to test
from src.data.data_acquisition import acquire_data

# Create a dummy logger class
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass
    def print_success(self, msg): pass

# Create a dummy args namespace
def create_mock_args(mode='demo', ticker=None, interval='D1', period='1y', start=None, end=None, point=None, rule=None):
    return argparse.Namespace(
        mode=mode, ticker=ticker, interval=interval, period=period,
        start=start, end=end, point=point, rule=rule
    )

# Unit tests for the data acquisition step
class TestDataAcquisition(unittest.TestCase):

    # Patch the logger within the data_acquisition module
    @patch('src.data.data_acquisition.logger', new_callable=MockLogger)
    # Patch the functions from data_utils that acquire_data calls
    @patch('src.data.data_acquisition.get_demo_data')
    def test_acquire_data_demo_mode(self, mock_get_demo_data, _ ):
        # Setup mock for get_demo_data
        demo_df = pd.DataFrame({'Open': [1], 'High': [1.1], 'Low': [0.9], 'Close': [1], 'Volume': [100]})
        mock_get_demo_data.return_value = demo_df
        args = create_mock_args(mode='demo')

        result = acquire_data(args)

        # Assertions
        mock_get_demo_data.assert_called_once()
        self.assertIsInstance(result, dict)
        self.assertEqual(result['effective_mode'], 'demo')
        self.assertEqual(result['data_source_label'], "Demo Data")
        self.assertTrue(result['ohlcv_df'].equals(demo_df))
        self.assertIsNone(result['yf_ticker'])
        self.assertIsNone(result['yf_interval'])
        self.assertIsNone(result['current_period'])
        self.assertIsNone(result['current_start'])
        self.assertIsNone(result['current_end'])

    # Patch logger and data_utils functions for yfinance mode tests
    @patch('src.data.data_acquisition.logger', new_callable=MockLogger)
    @patch('src.data.data_acquisition.map_interval')
    @patch('src.data.data_acquisition.map_ticker')
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_acquire_data_yfinance_mode_period(self, mock_fetch_yfinance_data, mock_map_ticker, mock_map_interval, _):
        # Setup mocks
        yf_df = pd.DataFrame({'Open': [10], 'High': [11], 'Low': [9], 'Close': [10], 'Volume': [1000]})
        mock_fetch_yfinance_data.return_value = yf_df
        mock_map_interval.return_value = '1d' # Mocked mapped interval
        mock_map_ticker.return_value = 'AAPL' # Mocked mapped ticker
        args = create_mock_args(mode='yf', ticker='AAPL', period='1mo', interval='D1') # Using period

        result = acquire_data(args)

        # Assertions
        mock_map_interval.assert_called_once_with('D1')
        mock_map_ticker.assert_called_once_with('AAPL')
        mock_fetch_yfinance_data.assert_called_once_with(ticker='AAPL', interval='1d', period='1mo', start_date=None, end_date=None)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['effective_mode'], 'yfinance')
        self.assertEqual(result['data_source_label'], "AAPL")
        self.assertTrue(result['ohlcv_df'].equals(yf_df))
        self.assertEqual(result['yf_ticker'], 'AAPL')
        self.assertEqual(result['yf_interval'], '1d')
        self.assertEqual(result['current_period'], '1mo') # Check period was used
        self.assertIsNone(result['current_start'])
        self.assertIsNone(result['current_end'])

    @patch('src.data.data_acquisition.logger', new_callable=MockLogger)
    @patch('src.data.data_acquisition.map_interval')
    @patch('src.data.data_acquisition.map_ticker')
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_acquire_data_yfinance_mode_start_end(self, mock_fetch_yfinance_data, mock_map_ticker, mock_map_interval, _):
        # Setup mocks
        yf_df = pd.DataFrame({'Open': [20], 'High': [21], 'Low': [19], 'Close': [20], 'Volume': [2000]})
        mock_fetch_yfinance_data.return_value = yf_df
        mock_map_interval.return_value = '1h'
        mock_map_ticker.return_value = 'MSFT'
        # Provide start and end, period should be ignored
        args = create_mock_args(mode='yfinance', ticker='MSFT', interval='H1', start='2024-01-01', end='2024-01-31', period='ignored')

        result = acquire_data(args)

        # Assertions
        mock_map_interval.assert_called_once_with('H1')
        mock_map_ticker.assert_called_once_with('MSFT')
        mock_fetch_yfinance_data.assert_called_once_with(ticker='MSFT', interval='1h', period=None, start_date='2024-01-01', end_date='2024-01-31')
        self.assertEqual(result['effective_mode'], 'yfinance')
        self.assertEqual(result['data_source_label'], "MSFT")
        self.assertTrue(result['ohlcv_df'].equals(yf_df))
        self.assertEqual(result['yf_ticker'], 'MSFT')
        self.assertEqual(result['yf_interval'], '1h')
        self.assertEqual(result['current_start'], '2024-01-01')
        self.assertEqual(result['current_end'], '2024-01-31')
        self.assertIsNone(result['current_period'])

    # Test automatic end date when only start is provided
    @patch('src.data.data_acquisition.logger', new_callable=MockLogger)
    @patch('src.data.data_acquisition.map_interval')
    @patch('src.data.data_acquisition.map_ticker')
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_acquire_data_yfinance_mode_start_only(self, mock_fetch_yfinance_data, mock_map_ticker, mock_map_interval, _):
        yf_df = pd.DataFrame({'Open': [30], 'Close': [30]})
        mock_fetch_yfinance_data.return_value = yf_df
        mock_map_interval.return_value = '1d'
        mock_map_ticker.return_value = 'GOOG'
        args = create_mock_args(mode='yf', ticker='GOOG', interval='D1', start='2024-03-01') # Only start
        today_str = date.today().strftime('%Y-%m-%d')

        result = acquire_data(args)

        mock_fetch_yfinance_data.assert_called_once_with(ticker='GOOG', interval='1d', period=None, start_date='2024-03-01', end_date=today_str)
        self.assertEqual(result['current_start'], '2024-03-01')
        self.assertEqual(result['current_end'], today_str) # End date should be today

    # Test automatic start date when only end is provided
    @patch('src.data.data_acquisition.logger', new_callable=MockLogger)
    @patch('src.data.data_acquisition.map_interval')
    @patch('src.data.data_acquisition.map_ticker')
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_acquire_data_yfinance_mode_end_only(self, mock_fetch_yfinance_data, mock_map_ticker, mock_map_interval, _):
        yf_df = pd.DataFrame({'Open': [40], 'Close': [40]})
        mock_fetch_yfinance_data.return_value = yf_df
        mock_map_interval.return_value = '1wk'
        mock_map_ticker.return_value = 'TSLA'
        args = create_mock_args(mode='yf', ticker='TSLA', interval='W1', end='2024-04-15') # Only end
        default_start = "2000-01-01"

        result = acquire_data(args)

        mock_fetch_yfinance_data.assert_called_once_with(ticker='TSLA', interval='1wk', period=None, start_date=default_start, end_date='2024-04-15')
        self.assertEqual(result['current_start'], default_start) # Start date should be default
        self.assertEqual(result['current_end'], '2024-04-15')

    # Test yfinance mode missing ticker - should raise ValueError
    @patch('src.data.data_acquisition.logger', new_callable=MockLogger)
    def test_acquire_data_yfinance_missing_ticker(self, _):
        args = create_mock_args(mode='yf', ticker=None) # Missing ticker
        with self.assertRaises(ValueError) as cm:
            acquire_data(args)
        self.assertIn("Ticker (--ticker) is required", str(cm.exception))

    # Test yfinance mode invalid interval - map_interval should raise error (tested separately, but check propagation)
    @patch('src.data.data_acquisition.logger', new_callable=MockLogger)
    @patch('src.data.data_acquisition.map_interval')
    def test_acquire_data_yfinance_invalid_interval(self, mock_map_interval, _):
        mock_map_interval.side_effect = ValueError("Invalid interval")
        args = create_mock_args(mode='yf', ticker='ANY', interval='INVALID')
        with self.assertRaises(ValueError) as cm:
            acquire_data(args)
        self.assertIn("Invalid interval", str(cm.exception)) # Error from map_interval propagates

    # Test yfinance data fetch failure
    @patch('src.data.data_acquisition.logger', new_callable=MockLogger)
    @patch('src.data.data_acquisition.map_interval')
    @patch('src.data.data_acquisition.map_ticker')
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_acquire_data_yfinance_fetch_fail(self, mock_fetch_yfinance_data, mock_map_ticker, mock_map_interval, _):
        mock_fetch_yfinance_data.return_value = None # Simulate fetch failure
        mock_map_interval.return_value = '1d'
        mock_map_ticker.return_value = 'FAIL'
        args = create_mock_args(mode='yf', ticker='FAIL', period='1d')

        result = acquire_data(args)

        # Should still return a dict, but ohlcv_df should be None
        self.assertIsInstance(result, dict)
        self.assertIsNone(result['ohlcv_df'])
        self.assertEqual(result['effective_mode'], 'yfinance')
        self.assertEqual(result['data_source_label'], "FAIL")

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()