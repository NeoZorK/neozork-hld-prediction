# tests/utils/test_point_size_determination.py # MODIFIED

import unittest
from unittest.mock import patch #, MagicMock
import argparse
import pandas as pd # Keep import if needed for data_info

# Import the function to test
from src.utils.point_size_determination import get_point_size

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass

# Create a dummy args namespace helper function
# Ensure it can accept all relevant args, though only 'point' is checked here
def create_mock_args(point=None, **other_args):
    # Only 'point' argument is directly checked by get_point_size logic itself
    # but the args object is passed through, so allow others
    namespace = argparse.Namespace(point=point)
    # Add any other default args needed if the function under test accesses them
    # For get_point_size, currently only args.point is directly accessed.
    for key, value in other_args.items():
        setattr(namespace, key, value)
    return namespace

# Unit tests for the point size determination step
# Patch logger for the whole class
@patch('src.utils.point_size_determination.logger', new_callable=MockLogger)
class TestPointSizeDetermination(unittest.TestCase):

    # --- Existing Tests for Demo and Yfinance ---
    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_demo_mode(self, mock_determine_point_size, _):
        args = create_mock_args()
        data_info = {"ohlcv_df": pd.DataFrame({'Close': [1]}), "effective_mode": "demo", "yf_ticker": None}
        point_size, estimated_point = get_point_size(args, data_info)
        self.assertEqual(point_size, 0.00001)
        self.assertFalse(estimated_point)
        mock_determine_point_size.assert_not_called()

    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_yfinance_user_provided(self, mock_determine_point_size, _):
        user_point = 0.001
        args = create_mock_args(point=user_point)
        data_info = {"ohlcv_df": pd.DataFrame({'Close': [100]}), "effective_mode": "yfinance", "yf_ticker": "AAPL"}
        point_size, estimated_point = get_point_size(args, data_info)
        self.assertEqual(point_size, user_point)
        self.assertFalse(estimated_point)
        mock_determine_point_size.assert_not_called()

    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_yfinance_estimated_success(self, mock_determine_point_size, _):
        estimated_point_val = 0.01
        mock_determine_point_size.return_value = estimated_point_val
        args = create_mock_args()
        data_info = {"ohlcv_df": pd.DataFrame({'Close': [100]}), "effective_mode": "yfinance", "yf_ticker": "MSFT"}
        point_size, estimated_point = get_point_size(args, data_info)
        self.assertEqual(point_size, estimated_point_val)
        self.assertTrue(estimated_point)
        mock_determine_point_size.assert_called_once_with("MSFT")

    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_yfinance_estimated_fail(self, mock_determine_point_size, _):
        mock_determine_point_size.return_value = None
        args = create_mock_args()
        data_info = {"ohlcv_df": pd.DataFrame({'Close': [100]}), "effective_mode": "yfinance", "yf_ticker": "UNKNOWN"}
        with self.assertRaises(ValueError) as cm: get_point_size(args, data_info)
        self.assertIn("Automatic point size estimation failed", str(cm.exception))
        mock_determine_point_size.assert_called_once_with("UNKNOWN")

    def test_get_point_size_yfinance_no_data(self, _):
        args = create_mock_args()
        data_info = {"ohlcv_df": None, "effective_mode": "yfinance", "yf_ticker": "NODATA"}
        with self.assertRaises(ValueError) as cm: get_point_size(args, data_info)
        self.assertIn("Cannot determine point size without valid data", str(cm.exception))

    def test_get_point_size_yfinance_empty_data(self, _):
        args = create_mock_args()
        data_info = {"ohlcv_df": pd.DataFrame(), "effective_mode": "yfinance", "yf_ticker": "EMPTYDATA"}
        with self.assertRaises(ValueError) as cm: get_point_size(args, data_info)
        self.assertIn("Cannot determine point size without valid data", str(cm.exception))

    def test_get_point_size_yfinance_invalid_user_point(self, _):
        args = create_mock_args(point=-0.001)
        data_info = {"ohlcv_df": pd.DataFrame({'Close': [100]}), "effective_mode": "yfinance", "yf_ticker": "AAPL"}
        with self.assertRaises(ValueError) as cm: get_point_size(args, data_info)
        self.assertIn("Provided point size (--point) must be positive", str(cm.exception))

    # --- NEW Tests for CSV Mode ---

    @patch('src.utils.point_size_determination.determine_point_size') # Still need to patch this even if not called
    def test_get_point_size_csv_mode_point_provided(self, mock_determine_point_size, _):
        user_point = 0.01
        args = create_mock_args(point=user_point) # User provides point
        data_info = {
            "ohlcv_df": pd.DataFrame({'Close': [100]}), # Dummy df
            "effective_mode": "csv", # Set mode to csv
            "yf_ticker": None # Not relevant for csv
        }
        point_size, estimated_point = get_point_size(args, data_info)

        # Assertions
        self.assertEqual(point_size, user_point)
        self.assertFalse(estimated_point)
        mock_determine_point_size.assert_not_called() # Estimation func shouldn't be called

    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_csv_mode_point_missing(self, mock_determine_point_size, _):
        args = create_mock_args(point=None) # Point NOT provided
        data_info = {"ohlcv_df": pd.DataFrame({'Close': [100]}), "effective_mode": "csv"}

        # Assertions
        with self.assertRaises(ValueError) as cm:
            get_point_size(args, data_info)
        self.assertIn("must be provided when using csv mode", str(cm.exception))
        mock_determine_point_size.assert_not_called()

    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_csv_mode_point_invalid(self, mock_determine_point_size, _):
        args_zero = create_mock_args(point=0) # Zero point
        args_neg = create_mock_args(point=-0.01) # Negative point
        data_info = {"ohlcv_df": pd.DataFrame({'Close': [100]}), "effective_mode": "csv"}

        # Assertions for zero point
        with self.assertRaises(ValueError) as cm_zero:
            get_point_size(args_zero, data_info)
        self.assertIn("must be positive", str(cm_zero.exception))

        # Assertions for negative point
        with self.assertRaises(ValueError) as cm_neg:
            get_point_size(args_neg, data_info)
        self.assertIn("must be positive", str(cm_neg.exception))
        mock_determine_point_size.assert_not_called()


    # --- NEW Tests for Polygon Mode ---

    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_polygon_mode_point_provided(self, mock_determine_point_size, _):
        user_point = 0.00001
        args = create_mock_args(point=user_point)
        data_info = {
            "ohlcv_df": pd.DataFrame({'Close': [1.1]}),
            "effective_mode": "polygon", # Set mode to polygon
            "yf_ticker": None
        }
        point_size, estimated_point = get_point_size(args, data_info)

        # Assertions
        self.assertEqual(point_size, user_point)
        self.assertFalse(estimated_point)
        mock_determine_point_size.assert_not_called()

    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_polygon_mode_point_missing(self, mock_determine_point_size, _):
        args = create_mock_args(point=None)
        data_info = {"ohlcv_df": pd.DataFrame({'Close': [1.1]}), "effective_mode": "polygon"}

        # Assertions
        with self.assertRaises(ValueError) as cm:
            get_point_size(args, data_info)
        self.assertIn("must be provided when using polygon mode", str(cm.exception))
        mock_determine_point_size.assert_not_called()

    @patch('src.utils.point_size_determination.determine_point_size')
    def test_get_point_size_polygon_mode_point_invalid(self, mock_determine_point_size, _):
        args_zero = create_mock_args(point=0)
        args_neg = create_mock_args(point=-0.00001)
        data_info = {"ohlcv_df": pd.DataFrame({'Close': [1.1]}), "effective_mode": "polygon"}

        # Assertions for zero point
        with self.assertRaises(ValueError) as cm_zero:
            get_point_size(args_zero, data_info)
        self.assertIn("must be positive", str(cm_zero.exception))

        # Assertions for negative point
        with self.assertRaises(ValueError) as cm_neg:
            get_point_size(args_neg, data_info)
        self.assertIn("must be positive", str(cm_neg.exception))
        mock_determine_point_size.assert_not_called()


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()