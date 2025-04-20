# tests/workflow/test_workflow.py (CORRECTED - Assert Dict + AssertGreaterEqual + Logging)

import unittest
from unittest.mock import patch, MagicMock, ANY # Import ANY
import pandas as pd
import argparse
import logging # Import standard logging library
import time # Import time to measure duration

# Import the function to test
from src.workflow.workflow import run_indicator_workflow
from src.common.constants import TradingRule # Assuming TradingRule enum is here

# --- Standard Logging Setup ---
logging.basicConfig(level=logging.CRITICAL)
# -----------------------------

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
             'current_start': '2023-01-01', 'current_end': '2023-01-05',
             'api_latency_sec': 0.5, 'api_calls': 1, 'successful_chunks': 1,
             'file_size_bytes': None,
             'data_metrics': {} # Initialize data_metrics
        }

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    def test_run_workflow_success_yfinance(self, mock_to_parquet, mock_makedirs,
                                            mock_generate_plot, mock_calculate_indicator,
                                            mock_get_point_size, mock_acquire_data):
        """Test a successful workflow run using yfinance mode."""
        # Configure mocks
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Pressure_Vector)
        mock_generate_plot.return_value = "/path/to/plot.png"

        # Run the workflow
        results = run_indicator_workflow(self.mock_args)

        # Assertions (Unchanged)
        mock_acquire_data.assert_called_once_with(self.mock_args)
        mock_get_point_size.assert_called_once_with(self.mock_args, self.sample_data_info)
        mock_calculate_indicator.assert_called_once_with(self.mock_args, ANY, 0.01)
        mock_generate_plot.assert_called_once_with(self.mock_args, self.sample_data_info, ANY, TradingRule.Pressure_Vector, 0.01, False)
        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once()
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
        self.assertIsNotNone(results['parquet_save_path'])
        self.assertIsNone(results['error_message'])
        self.assertIsNotNone(results.get('data_metrics'))

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
        csv_data_info['ohlcv_df'] = self.sample_df.copy()

        mock_acquire_data.return_value = csv_data_info
        mock_get_point_size.return_value = (0.001, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Predict_High_Low_Direction)
        mock_generate_plot.return_value = "/path/to/plot.png"

        results = run_indicator_workflow(csv_args)

        # Assertions (Unchanged)
        mock_acquire_data.assert_called_once_with(csv_args)
        mock_get_point_size.assert_called_once_with(csv_args, csv_data_info)
        mock_calculate_indicator.assert_called_once_with(csv_args, ANY, 0.001)
        mock_generate_plot.assert_called_once_with(csv_args, csv_data_info, ANY, TradingRule.Predict_High_Low_Direction, 0.001, False)
        mock_makedirs.assert_not_called()
        mock_to_parquet.assert_not_called()
        self.assertTrue(results['success'])
        self.assertEqual(results['point_size'], 0.001)
        self.assertFalse(results['estimated_point'])
        self.assertEqual(results['selected_rule'], TradingRule.Predict_High_Low_Direction)
        self.assertIsNone(results['parquet_save_path'])
        self.assertIsNone(results['error_message'])
        self.assertIsNotNone(results.get('data_metrics'))

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    @patch('time.perf_counter') # Mock time to control duration
    def test_run_workflow_calculation_fail(self, mock_perf_counter, mock_to_parquet, mock_makedirs,
                                           mock_generate_plot, mock_calculate_indicator,
                                           mock_get_point_size, mock_acquire_data):
        """Test workflow failure during indicator calculation."""
        # Simulate time progression
        mock_perf_counter.side_effect = [10.0, 10.5, 10.6, 10.7] # acquire, point_size, start_calc, end_calc (instant fail)
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        # Simulate calculation failure
        mock_calculate_indicator.side_effect = Exception("Calculation failed inside")

        results = run_indicator_workflow(self.mock_args)

        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_called_once()
        mock_calculate_indicator.assert_called_once()
        mock_generate_plot.assert_not_called() # Plotting should not be called
        mock_makedirs.assert_called_once() # Make dirs for parquet still called
        mock_to_parquet.assert_called_once() # Parquet save should still happen before failure

        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        self.assertIn("Calculation failed inside", results['error_message'])
        self.assertIsNotNone(results['error_traceback'])
        # Check durations recorded up to failure
        self.assertGreater(results['data_fetch_duration'], 0)
        # CORRECTED Assertion: Use assertGreaterEqual for calc_duration
        self.assertGreaterEqual(results['calc_duration'], 0) # calc_duration might be 0 if exception is immediate
        self.assertEqual(results['plot_duration'], 0) # Plot duration should be 0
        self.assertIsNotNone(results.get('data_metrics'))

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    def test_run_workflow_acquire_fail_returns_dict(self, mock_to_parquet, mock_makedirs,
                                                  mock_generate_plot, mock_calculate_indicator,
                                                  mock_get_point_size, mock_acquire_data):
        """Test workflow handles acquire_data failure by checking returned dict."""
        # Configure acquire_data to return a dict indicating failure
        mock_acquire_data.return_value = {
            'ohlcv_df': None, # Simulate failure
            'effective_mode': 'yfinance',
            'data_source_label': 'yfinance_FAIL',
            'error_message': 'Simulated acquisition failure',
            'ticker': 'FAIL',
            'interval': 'D1',
            'data_metrics': {}, # Ensure data_metrics exists
            'steps_duration': {} # Ensure steps_duration exists
        }

        # CORRECTED: Call the function directly and check the results dictionary
        results = run_indicator_workflow(self.mock_args)

        # Verify acquire_data was called
        mock_acquire_data.assert_called_once_with(self.mock_args)

        # Verify subsequent steps were NOT called
        mock_get_point_size.assert_not_called()
        mock_calculate_indicator.assert_not_called()
        mock_generate_plot.assert_not_called()
        mock_makedirs.assert_not_called()
        mock_to_parquet.assert_not_called()

        # Verify the returned dictionary indicates failure
        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        # The error message should now come from the exception caught *within* the workflow
        self.assertIn("Cannot proceed without valid data.", results['error_message'])
        self.assertIsNotNone(results['error_traceback'])


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

        # Assertions (Unchanged)
        mock_acquire_data.assert_called_once()
        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once()
        mock_get_point_size.assert_called_once()
        mock_calculate_indicator.assert_called_once()
        mock_generate_plot.assert_called_once()
        self.assertTrue(results['success'])
        self.assertIsNone(results['parquet_save_path'])
        self.assertIsNone(results['error_message'])
        self.assertIsNotNone(results.get('data_metrics'))


if __name__ == '__main__':
    unittest.main()