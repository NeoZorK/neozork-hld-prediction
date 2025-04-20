# tests/data/test_data_acquisition.py

"""
Unit tests for the data_acquisition module.
All comments are in English.
"""

import unittest
import pandas as pd
from unittest.mock import patch, MagicMock, ANY # Import ANY for flexible matching

# Adjust the import path based on the project structure
from src.data.data_acquisition import acquire_data

# Definition of the TestDataAcquisition class
class TestDataAcquisition(unittest.TestCase):
    """
    Test suite for the acquire_data function.
    """

    # --- Helper to create mock args ---
    def create_mock_args(self, mode, **kwargs):
        """ Creates a mock args object for testing. """
        args = MagicMock()
        args.mode = mode
        # Set defaults for potentially missing args to avoid AttributeError
        args.csv_file = None
        args.ticker = None
        args.interval = 'D1' # Default interval
        args.start = None
        args.end = None
        args.period = '1y' # Default period for yfinance if start/end not set
        # Update with provided kwargs
        args.__dict__.update(kwargs)
        return args

    # --- Helper to create a simple mock DataFrame ---
    def create_simple_mock_df(self):
        """ Creates a basic DataFrame for mocking fetcher returns. """
        return pd.DataFrame({'Close': [100, 101]}, index=pd.to_datetime(['2023-01-01', '2023-01-02']))

    # --- Test cases for each mode ---

    # Test demo mode
    # Patch the specific function imported into data_acquisition
    @patch('src.data.data_acquisition.get_demo_data')
    @patch('src.data.data_acquisition.load_dotenv', return_value=True) # Mock dotenv loading
    def test_acquire_data_demo(self, mock_dotenv, mock_get_demo):
        """ Test acquire_data in 'demo' mode. """
        args = self.create_mock_args(mode='demo')
        mock_df = self.create_simple_mock_df()
        # Demo fetcher still returns only DataFrame
        mock_get_demo.return_value = mock_df

        result = acquire_data(args)

        # Assert correct fetcher was called
        mock_get_demo.assert_called_once()
        # Assert results dictionary content
        self.assertEqual(result['effective_mode'], 'demo')
        self.assertEqual(result['data_source_label'], 'Demo Data')
        pd.testing.assert_frame_equal(result['ohlcv_df'], mock_df)
        # Check that metrics are None (as demo doesn't provide them)
        self.assertIsNone(result.get('file_size_bytes'))
        self.assertIsNone(result.get('api_latency_sec'))

    # Test CSV mode
    # Patch the specific function imported into data_acquisition
    @patch('src.data.data_acquisition.fetch_csv_data')
    @patch('src.data.data_acquisition.load_dotenv', return_value=True)
    def test_acquire_data_csv_success(self, mock_dotenv, mock_fetch_csv):
        """ Test acquire_data in 'csv' mode with successful fetch. """
        csv_path = "fake/path/data.csv"
        args = self.create_mock_args(mode='csv', csv_file=csv_path)
        mock_df = self.create_simple_mock_df()
        mock_metrics = {"file_size_bytes": 5120} # Example metric
        # Configure mock fetcher to return tuple
        mock_fetch_csv.return_value = (mock_df, mock_metrics)

        result = acquire_data(args)

        # Assert correct fetcher was called
        mock_fetch_csv.assert_called_once_with(filepath=csv_path)
        # Assert results dictionary content
        self.assertEqual(result['effective_mode'], 'csv')
        self.assertEqual(result['data_source_label'], csv_path)
        pd.testing.assert_frame_equal(result['ohlcv_df'], mock_df)
        # Check metrics are correctly propagated
        self.assertEqual(result.get('file_size_bytes'), 5120)
        self.assertIsNone(result.get('api_latency_sec')) # Latency not applicable to CSV

    # Test CSV mode fetcher failure
    @patch('src.data.data_acquisition.fetch_csv_data')
    @patch('src.data.data_acquisition.load_dotenv', return_value=True)
    def test_acquire_data_csv_failure(self, mock_dotenv, mock_fetch_csv):
        """ Test acquire_data in 'csv' mode when fetcher returns None. """
        csv_path = "fake/path/bad_data.csv"
        args = self.create_mock_args(mode='csv', csv_file=csv_path)
        # Configure mock fetcher to return None tuple (e.g., file not found)
        mock_fetch_csv.return_value = (None, {"file_size_bytes": None}) # Or just None

        result = acquire_data(args)

        mock_fetch_csv.assert_called_once_with(filepath=csv_path)
        self.assertEqual(result['effective_mode'], 'csv')
        self.assertIsNone(result['ohlcv_df'])
        # Check metrics (file size might be None if file not found)
        self.assertIsNone(result.get('file_size_bytes'))
        self.assertIsNone(result.get('api_latency_sec'))


    # Test Yfinance mode
    # Patch the specific functions imported into data_acquisition
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    @patch('src.data.data_acquisition.map_interval')
    @patch('src.data.data_acquisition.map_ticker')
    @patch('src.data.data_acquisition.load_dotenv', return_value=True)
    def test_acquire_data_yfinance_success(self, mock_dotenv, mock_map_ticker, mock_map_interval, mock_fetch_yf):
        """ Test acquire_data in 'yfinance' mode with successful fetch. """
        args = self.create_mock_args(mode='yfinance', ticker='AAPL', interval='H1', start='2023-01-01', end='2023-01-05')
        mock_df = self.create_simple_mock_df()
        mock_metrics = {"latency_sec": 1.5} # Example metric from yf fetcher
        # Configure mocks
        mock_map_ticker.return_value = 'AAPL' # Assume ticker mapping returns same
        mock_map_interval.return_value = '1h' # Assume interval mapping
        mock_fetch_yf.return_value = (mock_df, mock_metrics)

        result = acquire_data(args)

        # Assert mocks called
        mock_map_ticker.assert_called_once_with('AAPL')
        mock_map_interval.assert_called_once_with('H1')
        mock_fetch_yf.assert_called_once_with(
            ticker='AAPL', interval='1h', period=None, # period is None because start/end are set
            start_date='2023-01-01', end_date='2023-01-05'
        )
        # Assert results dictionary content
        self.assertEqual(result['effective_mode'], 'yfinance')
        self.assertEqual(result['data_source_label'], 'AAPL')
        pd.testing.assert_frame_equal(result['ohlcv_df'], mock_df)
        # Check metrics are correctly propagated
        self.assertEqual(result.get('api_latency_sec'), 1.5)
        self.assertIsNone(result.get('file_size_bytes')) # File size not applicable


    # Test Polygon mode
    # Patch the specific function imported into data_acquisition
    @patch('src.data.data_acquisition.fetch_polygon_data')
    @patch('src.data.data_acquisition.load_dotenv', return_value=True)
    def test_acquire_data_polygon_success(self, mock_dotenv, mock_fetch_polygon):
        """ Test acquire_data in 'polygon' mode with successful fetch. """
        args = self.create_mock_args(mode='polygon', ticker='T:MSFT', interval='hour', start='2023-02-01', end='2023-02-02')
        mock_df = self.create_simple_mock_df()
        mock_metrics = {"total_latency_sec": 3.2} # Example metric from polygon fetcher
        # Configure mock fetcher to return tuple
        mock_fetch_polygon.return_value = (mock_df, mock_metrics)

        result = acquire_data(args)

        # Assert correct fetcher was called
        mock_fetch_polygon.assert_called_once_with(
            ticker='T:MSFT', interval='hour', start_date='2023-02-01', end_date='2023-02-02'
        )
        # Assert results dictionary content
        self.assertEqual(result['effective_mode'], 'polygon')
        self.assertEqual(result['data_source_label'], 'T:MSFT')
        pd.testing.assert_frame_equal(result['ohlcv_df'], mock_df)
        # Check metrics are correctly propagated
        self.assertEqual(result.get('api_latency_sec'), 3.2) # Uses the 'total_latency_sec' value
        self.assertIsNone(result.get('file_size_bytes'))


    # Test Binance mode
    # Patch the specific function imported into data_acquisition
    @patch('src.data.data_acquisition.fetch_binance_data')
    @patch('src.data.data_acquisition.load_dotenv', return_value=True)
    def test_acquire_data_binance_success(self, mock_dotenv, mock_fetch_binance):
        """ Test acquire_data in 'binance' mode with successful fetch. """
        args = self.create_mock_args(mode='binance', ticker='BTCUSDT', interval='M15', start='2023-03-10', end='2023-03-11')
        mock_df = self.create_simple_mock_df()
        mock_metrics = {"total_latency_sec": 2.8} # Example metric from binance fetcher
        # Configure mock fetcher to return tuple
        mock_fetch_binance.return_value = (mock_df, mock_metrics)

        result = acquire_data(args)

        # Assert correct fetcher was called
        mock_fetch_binance.assert_called_once_with(
            ticker='BTCUSDT', interval='M15', start_date='2023-03-10', end_date='2023-03-11'
        )
        # Assert results dictionary content
        self.assertEqual(result['effective_mode'], 'binance')
        self.assertEqual(result['data_source_label'], 'BTCUSDT')
        pd.testing.assert_frame_equal(result['ohlcv_df'], mock_df)
        # Check metrics are correctly propagated
        self.assertEqual(result.get('api_latency_sec'), 2.8) # Uses the 'total_latency_sec' value
        self.assertIsNone(result.get('file_size_bytes'))


    # Test missing required argument for a mode (e.g., ticker for yfinance)
    # No mocks needed as it should fail before calling fetcher
    @patch('src.data.data_acquisition.load_dotenv', return_value=True)
    def test_acquire_data_missing_arg(self, mock_dotenv):
        """ Test acquire_data raises ValueError if a required arg is missing. """
        args = self.create_mock_args(mode='yfinance', ticker=None) # Missing ticker
        with self.assertRaisesRegex(ValueError, "--ticker is required for yfinance mode."):
            acquire_data(args)

        args_csv = self.create_mock_args(mode='csv', csv_file=None) # Missing csv_file
        with self.assertRaisesRegex(ValueError, "--csv-file is required for csv mode."):
            acquire_data(args_csv)


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()