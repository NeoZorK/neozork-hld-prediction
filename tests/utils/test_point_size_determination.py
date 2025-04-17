# tests/utils/test_point_size_determination.py

import unittest
from unittest.mock import patch #, MagicMock
import argparse
import pandas as pd

# Import the function to test
from src.utils.point_size_determination import get_point_size

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass

# Create a dummy args namespace
def create_mock_args(point=None):
    # Only need 'point' argument for this module's tests
    return argparse.Namespace(point=point)

# Unit tests for the point size determination step
class TestPointSizeDetermination(unittest.TestCase):

    # Patch the logger and the determine_point_size utility function
    @patch('src.utils.point_size_determination.logger', new_callable=MockLogger)
    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_demo_mode(self, mock_determine_point_size, _):
        args = create_mock_args() # Point not provided
        # data_info for demo mode
        data_info = {
            "ohlcv_df": pd.DataFrame({'Close': [1]}), # Needs some df
            "effective_mode": "demo",
            "yf_ticker": None
        }
        point_size, estimated_point = get_point_size(args, data_info)

        # Assertions
        self.assertEqual(point_size, 0.00001) # Fixed demo point size
        self.assertFalse(estimated_point)
        mock_determine_point_size.assert_not_called() # Estimation func shouldn't be called

    @patch('src.utils.point_size_determination.logger', new_callable=MockLogger)
    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_yfinance_user_provided(self, mock_determine_point_size, _):
        user_point = 0.001
        args = create_mock_args(point=user_point) # User provides point
        data_info = {
            "ohlcv_df": pd.DataFrame({'Close': [100]}),
            "effective_mode": "yfinance",
            "yf_ticker": "AAPL"
        }
        point_size, estimated_point = get_point_size(args, data_info)

        # Assertions
        self.assertEqual(point_size, user_point)
        self.assertFalse(estimated_point)
        mock_determine_point_size.assert_not_called() # Estimation func shouldn't be called

    @patch('src.utils.point_size_determination.logger', new_callable=MockLogger)
    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_yfinance_estimated_success(self, mock_determine_point_size, _):
        estimated_point_val = 0.01
        mock_determine_point_size.return_value = estimated_point_val # Simulate successful estimation
        args = create_mock_args() # Point not provided
        data_info = {
            "ohlcv_df": pd.DataFrame({'Close': [100]}),
            "effective_mode": "yfinance",
            "yf_ticker": "MSFT"
        }
        point_size, estimated_point = get_point_size(args, data_info)

        # Assertions
        self.assertEqual(point_size, estimated_point_val)
        self.assertTrue(estimated_point)
        mock_determine_point_size.assert_called_once_with("MSFT") # Check estimation was called with ticker

    @patch('src.utils.point_size_determination.logger', new_callable=MockLogger)
    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_yfinance_estimated_fail(self, mock_determine_point_size, _):
        mock_determine_point_size.return_value = None # Simulate estimation failure
        args = create_mock_args() # Point not provided
        data_info = {
            "ohlcv_df": pd.DataFrame({'Close': [100]}),
            "effective_mode": "yfinance",
            "yf_ticker": "UNKNOWN"
        }

        # Assertions
        with self.assertRaises(ValueError) as cm:
            get_point_size(args, data_info)
        self.assertIn("Automatic point size estimation failed", str(cm.exception))
        mock_determine_point_size.assert_called_once_with("UNKNOWN")

    @patch('src.utils.point_size_determination.logger', new_callable=MockLogger)
    def test_get_point_size_yfinance_no_data(self, _):
        args = create_mock_args() # Point not provided
        data_info = {
            "ohlcv_df": None, # No DataFrame provided
            "effective_mode": "yfinance",
            "yf_ticker": "NODATA"
        }

        # Assertions
        with self.assertRaises(ValueError) as cm:
            get_point_size(args, data_info)
        self.assertIn("Cannot determine point size without valid data", str(cm.exception))

    @patch('src.utils.point_size_determination.logger', new_callable=MockLogger)
    def test_get_point_size_yfinance_empty_data(self, _):
        args = create_mock_args() # Point not provided
        data_info = {
            "ohlcv_df": pd.DataFrame(), # Empty DataFrame
            "effective_mode": "yfinance",
            "yf_ticker": "EMPTYDATA"
        }

        # Assertions
        with self.assertRaises(ValueError) as cm:
            get_point_size(args, data_info)
        self.assertIn("Cannot determine point size without valid data", str(cm.exception))

    @patch('src.utils.point_size_determination.logger', new_callable=MockLogger)
    def test_get_point_size_yfinance_invalid_user_point(self, _):
        args = create_mock_args(point=-0.001) # Invalid point provided
        data_info = {
            "ohlcv_df": pd.DataFrame({'Close': [100]}),
            "effective_mode": "yfinance",
            "yf_ticker": "AAPL"
        }

        # Assertions
        with self.assertRaises(ValueError) as cm:
            get_point_size(args, data_info)
        self.assertIn("Provided point size (--point) must be positive", str(cm.exception))

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()