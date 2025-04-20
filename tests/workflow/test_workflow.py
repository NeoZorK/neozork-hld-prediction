# tests/workflow/test_workflow.py (CORRECTED - Use assertRaisesRegex)

import unittest
from unittest.mock import patch, MagicMock, ANY # Import ANY
import pandas as pd
import argparse

# Import the function to test
from src.workflow.workflow import run_indicator_workflow
from src.common.constants import TradingRule # Assuming TradingRule enum is here

# Disable logging for tests unless explicitly needed
from src.common import logger
logger.set_level(logger.logging.CRITICAL)
# logger.set_level(logger.logging.DEBUG) # Uncomment for debugging

class TestWorkflow(unittest.TestCase):

    def setUp(self):
        """Common setup for tests."""
        self.mock_args = argparse.Namespace(
            mode='yfinance',
            ticker='TEST',
            interval='D1',
            point=None,
            period='1y',
            start=None,
            end=None,
            rule='Pressure_Vector', # Use string representation
            csv_file=None,
            version=False
        )
        # Sample DataFrame
        self.sample_df = pd.DataFrame({
            'Open': [100, 110, 120, 130],
            'High': [105, 115, 125, 135],
            'Low': [95, 105, 115, 125],
            'Close': [102, 112, 122, 132],
            'Volume': [1000, 1100, 1200, 1300]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']))
        # Sample data_info dictionary returned by acquire_data
        self.sample_data_info = {
             'ohlcv_df': self.sample_df,
             'ticker': 'TEST',
             'interval': 'D1',
             'data_source_label': 'yfinance_TEST',
             'effective_mode': 'yfinance',
             'yf_ticker': 'TEST', 'yf_interval': 'D1', 'current_period': '1y',
             'current_start': '2023-01-01', 'current_end': '2023-01-05', # Example dates
             'api_latency_sec': 0.5, 'api_calls': 1, 'successful_chunks': 1,
             'file_size_bytes': None,
        }

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs') # Mock file system operations
    @patch('pandas.DataFrame.to_parquet') # Mock parquet writing
    def test_run_workflow_success_yfinance(self, mock_to_parquet, mock_makedirs,
                                            mock_generate_plot, mock_calculate_indicator,
                                            mock_get_point_size, mock_acquire_data):
        """Test a successful workflow run using yfinance mode."""
        # Configure mocks
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False) # point_size, estimated
        # Simulate calculate_indicator returning the df and the selected rule enum
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Pressure_Vector) # Return df and rule
        mock_generate_plot.return_value = "/path/to/plot.png" # Simulate plot path return

        # Run the workflow
        results = run_indicator_workflow(self.mock_args)

        # Assertions
        mock_acquire_data.assert_called_once_with(self.mock_args)
        mock_get_point_size.assert_called_once_with(self.mock_args, self.sample_data_info)
        # Check calculate_indicator call - Use ANY for the df copy
        mock_calculate_indicator.assert_called_once_with(self.mock_args, ANY, 0.01)
        # Check generate_plot call - Use ANY for the result_df
        mock_generate_plot.assert_called_once_with(self.mock_args, self.sample_data_info, ANY, TradingRule.Pressure_Vector, 0.01, False)

        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once() # Check if parquet saving was attempted

        self.assertTrue(results['success'])
        self.assertEqual(results['point_size'], 0.01)
        self.assertFalse(results['estimated_point'])
        self.assertEqual(results['selected_rule'], TradingRule.Pressure_Vector)
        self.assertGreater(results['data_fetch_duration'], 0)
        self.assertGreater(results['calc_duration'], 0)
        self.assertGreater(results['plot_duration'], 0)
        self.assertIn('acquire', results['steps_duration'])
        self.assertIn('point_size', results['steps_duration'])
        self.assertIn('calculate', results['steps_duration'])
        self.assertIn('plot', results['steps_duration'])
        self.assertIsNotNone(results['parquet_save_path']) # Check path was set
        self.assertIsNone(results['error_message'])

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    def test_run_workflow_success_csv_no_parquet(self, mock_to_parquet, mock_makedirs,
                                                mock_generate_plot, mock_calculate_indicator,
                                                mock_get_point_size, mock_acquire_data):
        """Test a successful workflow run using csv mode (no parquet save)."""
        csv_args = argparse.Namespace(
            mode='csv', csv_file='input.csv', ticker=None, interval='H1',
            point=0.001, period=None, start=None, end=None, rule='PHLD', version=False
        )
        csv_data_info = self.sample_data_info.copy()
        csv_data_info['effective_mode'] = 'csv'
        csv_data_info['data_source_label'] = 'input.csv'
        csv_data_info['point'] = 0.001 # Match args
        csv_data_info['ohlcv_df'] = self.sample_df.copy()


        mock_acquire_data.return_value = csv_data_info
        mock_get_point_size.return_value = (0.001, False) # Point provided in args
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Predict_High_Low_Direction)
        mock_generate_plot.return_value = "/path/to/plot.png"

        results = run_indicator_workflow(csv_args)

        mock_acquire_data.assert_called_once_with(csv_args)
        mock_get_point_size.assert_called_once_with(csv_args, csv_data_info)
        mock_calculate_indicator.assert_called_once_with(csv_args, ANY, 0.001)
        mock_generate_plot.assert_called_once_with(csv_args, csv_data_info, ANY, TradingRule.Predict_High_Low_Direction, 0.001, False)

        mock_makedirs.assert_not_called() # Should not be called for csv mode
        mock_to_parquet.assert_not_called() # Should not be called for csv mode

        self.assertTrue(results['success'])
        self.assertEqual(results['point_size'], 0.001)
        self.assertFalse(results['estimated_point'])
        self.assertEqual(results['selected_rule'], TradingRule.Predict_High_Low_Direction)
        self.assertIsNone(results['parquet_save_path']) # No parquet path for csv
        self.assertIsNone(results['error_message'])

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    def test_run_workflow_calculation_fail(self, mock_to_parquet, mock_makedirs,
                                           mock_generate_plot, mock_calculate_indicator,
                                           mock_get_point_size, mock_acquire_data):
        """Test workflow failure during indicator calculation."""
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        # Simulate calculation failure
        mock_calculate_indicator.side_effect = Exception("Calculation failed inside")

        results = run_indicator_workflow(self.mock_args)

        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_called_once()
        mock_calculate_indicator.assert_called_once()
        mock_generate_plot.assert_not_called() # Plotting should not be called
        mock_to_parquet.assert_called_once() # Parquet save should still happen before failure

        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        self.assertIn("Calculation failed inside", results['error_message'])
        self.assertIsNotNone(results['error_traceback'])
        # Check durations recorded up to failure
        self.assertGreater(results['data_fetch_duration'], 0)
        self.assertGreater(results['calc_duration'], 0) # Calc duration is measured even if it fails
        self.assertEqual(results['plot_duration'], 0) # Plot duration should be 0


    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    def test_run_workflow_acquire_fail_no_parquet(self, mock_to_parquet, mock_makedirs,
                                               mock_generate_plot, mock_calculate_indicator,
                                               mock_get_point_size, mock_acquire_data):
        """Test workflow when data acquisition fails (returns None df)."""
        # ** CORRECTED Mock Return Value **
        mock_acquire_data.return_value = {
            'ohlcv_df': None, # Simulate failure
            'effective_mode': 'yfinance', # Still provide mode
             'data_source_label': 'yfinance_FAIL',
             'error_message': 'Simulated acquisition failure', # Optional error from acquire
             # Other potential keys that might be returned even on failure
             'ticker': 'FAIL',
             'interval': 'D1',
        }

        # ** CORRECTED Assertion - Use assertRaisesRegex **
        with self.assertRaisesRegex(ValueError, "Cannot proceed without valid data"):
             run_indicator_workflow(self.mock_args)

        # Get results by calling again outside context manager (if needed, but test is about exception)
        # Alternatively, check logs or don't check results dict if exception is the main point
        # results = run_indicator_workflow(self.mock_args) # This would raise again

        # Verify mocks were called/not called appropriately
        mock_acquire_data.assert_called_once_with(self.mock_args)
        mock_get_point_size.assert_not_called()
        mock_calculate_indicator.assert_not_called()
        mock_generate_plot.assert_not_called()
        mock_makedirs.assert_not_called()
        mock_to_parquet.assert_not_called()

        # If you still want to check the returned dict (less ideal when expecting exceptions):
        # Need to wrap the call in try/except within the test to capture results dict
        try:
            results = run_indicator_workflow(self.mock_args)
        except ValueError as e:
            # Simulate how the main script might catch and store the error
            results = {'success': False, 'error_message': str(e)} # simplified

        self.assertFalse(results.get('success', True)) # Check success flag if checking dict
        self.assertIn("Cannot proceed without valid data", results.get('error_message', ''))


    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    def test_run_workflow_parquet_save_fail(self, mock_to_parquet, mock_makedirs,
                                          mock_generate_plot, mock_calculate_indicator,
                                          mock_get_point_size, mock_acquire_data):
        """Test workflow continues even if parquet saving fails."""
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Pressure_Vector)
        mock_generate_plot.return_value = "/path/to/plot.png"
        # Simulate parquet write failure
        mock_to_parquet.side_effect = Exception("Simulated Parquet write error (e.g., disk full)")

        # Run the workflow - should NOT raise an exception, just log error
        results = run_indicator_workflow(self.mock_args)

        # Assertions
        mock_acquire_data.assert_called_once()
        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once() # Saving was attempted
        mock_get_point_size.assert_called_once()
        mock_calculate_indicator.assert_called_once()
        mock_generate_plot.assert_called_once() # Workflow should continue to plot

        self.assertTrue(results['success']) # Overall workflow succeeded
        self.assertIsNone(results['parquet_save_path']) # Path should be None due to save failure
        self.assertIsNone(results['error_message']) # No critical error message for workflow


if __name__ == '__main__':
    unittest.main()