# tests/data/test_data_acquisition.py # MODIFIED

import unittest
from unittest.mock import patch # Import MagicMock if needed later
import argparse
import pandas as pd


# Import the function to test
from src.data.data_acquisition import acquire_data
# Import the functions that acquire_data will call, for patching
# These imports might seem unused but are needed targets for patch



# Create a dummy logger class
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass
    def print_success(self, msg): pass

# Create a dummy args namespace helper function
# Added csv_file argument
def create_mock_args(mode='demo', ticker=None, interval='D1', period='1y',
                     start=None, end=None, point=None, rule=None, csv_file=None): # Added csv_file
    return argparse.Namespace(
        mode=mode, ticker=ticker, interval=interval, period=period,
        start=start, end=end, point=point, rule=rule, csv_file=csv_file # Added csv_file
    )

# Unit tests for the data acquisition step
# Patch the logger for the whole class
@patch('src.data.data_acquisition.logger', new_callable=MockLogger)
class TestDataAcquisition(unittest.TestCase):

    # Patch the specific functions called by acquire_data for each test method

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
        # Assert other mode specific keys are None
        self.assertIsNone(result['yf_ticker'])
        self.assertIsNone(result['yf_interval'])
        self.assertIsNone(result['current_period'])
        self.assertIsNone(result['current_start'])
        self.assertIsNone(result['current_end'])

    # --- Tests for yfinance mode (keep existing ones) ---
    @patch('src.data.data_acquisition.map_interval')
    @patch('src.data.data_acquisition.map_ticker')
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_acquire_data_yfinance_mode_period(self, mock_fetch_yfinance_data, mock_map_ticker, mock_map_interval, _):
        yf_df = pd.DataFrame({'Open': [10]}) # Simplified df
        mock_fetch_yfinance_data.return_value = yf_df
        mock_map_interval.return_value = '1d'
        mock_map_ticker.return_value = 'AAPL'
        args = create_mock_args(mode='yf', ticker='AAPL', period='1mo', interval='D1')

        result = acquire_data(args)

        mock_map_interval.assert_called_once_with('D1')
        mock_map_ticker.assert_called_once_with('AAPL')
        mock_fetch_yfinance_data.assert_called_once_with(ticker='AAPL', interval='1d', period='1mo', start_date=None, end_date=None)
        self.assertEqual(result['effective_mode'], 'yfinance')
        self.assertEqual(result['data_source_label'], "AAPL")
        self.assertTrue(result['ohlcv_df'].equals(yf_df))
        self.assertEqual(result['yf_ticker'], 'AAPL')
        self.assertEqual(result['yf_interval'], '1d')
        self.assertEqual(result['current_period'], '1mo')
        self.assertIsNone(result['current_start'])
        self.assertIsNone(result['current_end'])

    @patch('src.data.data_acquisition.map_interval')
    @patch('src.data.data_acquisition.map_ticker')
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_acquire_data_yfinance_mode_start_end(self, mock_fetch_yfinance_data, mock_map_ticker, mock_map_interval, _):
        yf_df = pd.DataFrame({'Open': [20]})
        mock_fetch_yfinance_data.return_value = yf_df
        mock_map_interval.return_value = '1h'
        mock_map_ticker.return_value = 'MSFT'
        args = create_mock_args(mode='yfinance', ticker='MSFT', interval='H1', start='2024-01-01', end='2024-01-31')

        result = acquire_data(args)

        mock_fetch_yfinance_data.assert_called_once_with(ticker='MSFT', interval='1h', period=None, start_date='2024-01-01', end_date='2024-01-31')
        self.assertEqual(result['effective_mode'], 'yfinance')
        self.assertEqual(result['current_start'], '2024-01-01')
        self.assertEqual(result['current_end'], '2024-01-31')
        self.assertIsNone(result['current_period'])

    # ... (keep other existing yfinance tests: start_only, end_only, missing_ticker, invalid_interval, fetch_fail) ...
    @patch('src.data.data_acquisition.map_interval')
    @patch('src.data.data_acquisition.map_ticker')
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_acquire_data_yfinance_fetch_fail(self, mock_fetch_yfinance_data, mock_map_ticker, mock_map_interval, _):
        mock_fetch_yfinance_data.return_value = None # Simulate failure
        mock_map_interval.return_value = '1d'
        mock_map_ticker.return_value = 'FAIL'
        args = create_mock_args(mode='yf', ticker='FAIL', period='1d')

        result = acquire_data(args)

        self.assertIsInstance(result, dict)
        self.assertIsNone(result['ohlcv_df']) # Check DF is None on failure
        self.assertEqual(result['effective_mode'], 'yfinance')


    # --- NEW Test for CSV Mode ---
    @patch('src.data.data_acquisition.fetch_csv_data') # Patch the target function
    def test_acquire_data_csv_mode(self, mock_fetch_csv_data, _):
        # Setup mock for fetch_csv_data
        csv_df = pd.DataFrame({'Open': [1.1], 'Volume': [1000]}) # Example structure
        mock_fetch_csv_data.return_value = csv_df
        csv_path = "data/my_test.csv"
        args = create_mock_args(mode='csv', csv_file=csv_path) # Set mode and file path

        result = acquire_data(args)

        # Assertions
        mock_fetch_csv_data.assert_called_once_with(filepath=csv_path) # Check called correctly
        self.assertIsInstance(result, dict)
        self.assertEqual(result['effective_mode'], 'csv')
        self.assertEqual(result['data_source_label'], csv_path) # Label should be filename
        self.assertTrue(result['ohlcv_df'].equals(csv_df))
        # Assert yfinance specific keys are None
        self.assertIsNone(result['yf_ticker'])
        self.assertIsNone(result['yf_interval'])
        self.assertIsNone(result['current_period'])
        self.assertIsNone(result['current_start'])
        self.assertIsNone(result['current_end'])

    # --- NEW Test for Polygon Mode ---
    @patch('src.data.data_acquisition.fetch_polygon_data') # Patch the target function
    def test_acquire_data_polygon_mode(self, mock_fetch_polygon_data, _):
        # Setup mock for fetch_polygon_data
        poly_df = pd.DataFrame({'Open': [100], 'Volume': [5000]}) # Example structure
        mock_fetch_polygon_data.return_value = poly_df
        args = create_mock_args(
            mode='polygon',
            ticker='AAPL',
            interval='D1',
            start='2024-01-01',
            end='2024-01-10'
            # point argument is handled in get_point_size, not needed here
        )

        result = acquire_data(args)

        # Assertions
        mock_fetch_polygon_data.assert_called_once_with(
            ticker='AAPL',
            interval='D1',
            start_date='2024-01-01',
            end_date='2024-01-10'
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(result['effective_mode'], 'polygon')
        self.assertEqual(result['data_source_label'], 'AAPL') # Label should be ticker
        self.assertTrue(result['ohlcv_df'].equals(poly_df))
        # Assert yfinance specific keys are None (or check relevant polygon keys if added)
        self.assertIsNone(result['yf_ticker'])
        self.assertIsNone(result['yf_interval'])
        self.assertIsNone(result['current_period']) # Polygon used start/end
        self.assertEqual(result['current_start'], '2024-01-01') # Check start/end are stored
        self.assertEqual(result['current_end'], '2024-01-10')


    # --- NEW Test for CSV Mode Fetch Failure ---
    @patch('src.data.data_acquisition.fetch_csv_data')
    def test_acquire_data_csv_fetch_fail(self, mock_fetch_csv_data, _):
        mock_fetch_csv_data.return_value = None # Simulate failure
        csv_path = "data/my_fail.csv"
        args = create_mock_args(mode='csv', csv_file=csv_path)

        result = acquire_data(args)

        mock_fetch_csv_data.assert_called_once_with(filepath=csv_path)
        self.assertIsInstance(result, dict)
        self.assertIsNone(result['ohlcv_df']) # Check DF is None
        self.assertEqual(result['effective_mode'], 'csv')

    # --- NEW Test for Polygon Mode Fetch Failure ---
    @patch('src.data.data_acquisition.fetch_polygon_data')
    def test_acquire_data_polygon_fetch_fail(self, mock_fetch_polygon_data, _):
        mock_fetch_polygon_data.return_value = None # Simulate failure
        args = create_mock_args(mode='polygon', ticker='FAIL', interval='D1', start='2024-01-01', end='2024-01-10')

        result = acquire_data(args)

        mock_fetch_polygon_data.assert_called_once_with(ticker='FAIL', interval='D1', start_date='2024-01-01', end_date='2024-01-10')
        self.assertIsInstance(result, dict)
        self.assertIsNone(result['ohlcv_df']) # Check DF is None
        self.assertEqual(result['effective_mode'], 'polygon')


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()