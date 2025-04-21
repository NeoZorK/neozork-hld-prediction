# tests/workflow/test_workflow.py # CORRECTED v2: More time values for mocks

import unittest
from unittest.mock import patch, MagicMock, ANY
import pandas as pd
import argparse
import logging
import time # Import time

# Import components, use try-except for robustness
try:
    from src.workflow.workflow import run_indicator_workflow
    from src.common.constants import TradingRule
except ImportError:
    # Fallback for running script directly
    from src.workflow.workflow import run_indicator_workflow
    from src.common.constants import TradingRule


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
            rule='Pressure_Vector',
            csv_file=None,
            version=False
        )
        self.sample_df = pd.DataFrame({
            'Open': [100, 110, 120, 130], 'High': [105, 115, 125, 135],
            'Low': [95, 105, 115, 125], 'Close': [102, 112, 122, 132],
            'Volume': [1000, 1100, 1200, 1300]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']))
        self.sample_df.index.name = 'DateTime' # Ensure index name is set
        # Sample data_info dictionary RETURNED BY acquire_data
        self.sample_data_info = {
             'ohlcv_df': self.sample_df.copy(), # Must contain the df
             'ticker': 'TEST', 'interval': 'D1',
             'data_source_label': 'yfinance_TEST', 'effective_mode': 'yfinance',
             'yf_ticker': 'TEST', 'yf_interval': 'D1', 'current_period': '1y',
             'current_start': None, 'current_end': None, # Example dates from args or fetch
             'api_latency_sec': 0.5, 'api_calls': 1, 'successful_chunks': 1,
             'file_size_bytes': None, 'data_metrics': {},
             'parquet_cache_used': False, # Indicate cache was not used in this mock setup
             'parquet_cache_file': '/fake/path/yfinance_TEST_D1.parquet', # Example path
             'error_message': None,
             'rows_count': len(self.sample_df), 'columns_count': len(self.sample_df.columns),
             'data_size_mb': 0.01
        }

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs') # Keep if generate_plot creates dirs
    @patch('src.workflow.workflow.logger') # Mock logger inside workflow
    def test_run_workflow_success_yfinance(self, mock_logger, mock_makedirs,
                                            mock_generate_plot, mock_calculate_indicator,
                                            mock_get_point_size, mock_acquire_data):
        """Test a successful workflow run using yfinance mode."""
        mock_acquire_data.return_value = {**self.sample_data_info}
        mock_get_point_size.return_value = (0.01, False) # point_size, estimated_flag
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Pressure_Vector)
        mock_generate_plot.return_value = None # generate_plot returns None

        with patch('time.perf_counter') as mock_perf_counter:
            # *** FIX: Provide enough time values (10 needed for success path) ***
            mock_perf_counter.side_effect = [0.0, 0.5, 0.55, 0.6, 0.65, 0.8, 0.85, 1.5, 1.55, 1.6]
            results = run_indicator_workflow(self.mock_args)

        # Assertions
        mock_acquire_data.assert_called_once_with(self.mock_args)
        mock_get_point_size.assert_called_once_with(self.mock_args, self.sample_data_info)
        pd.testing.assert_frame_equal(mock_calculate_indicator.call_args[0][1], self.sample_df)
        self.assertEqual(mock_calculate_indicator.call_args[0][2], 0.01) # point_size
        mock_calculate_indicator.assert_called_once_with(self.mock_args, ANY, 0.01)
        pd.testing.assert_frame_equal(mock_generate_plot.call_args[0][2], self.sample_df)
        mock_generate_plot.assert_called_once_with(self.mock_args, self.sample_data_info, ANY, TradingRule.Pressure_Vector, 0.01, False)
        self.assertTrue(results['success'])
        self.assertGreaterEqual(results['data_fetch_duration'], 0)
        self.assertGreaterEqual(results['calc_duration'], 0)
        self.assertGreaterEqual(results['plot_duration'], 0)
        self.assertIn('acquire', results['steps_duration']); self.assertIn('point_size', results['steps_duration'])
        self.assertIn('calculate', results['steps_duration']); self.assertIn('plot', results['steps_duration'])
        self.assertIsNone(results['error_message'])

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('src.workflow.workflow.logger') # Mock logger inside workflow
    def test_run_workflow_success_csv_no_parquet(self, mock_logger, mock_makedirs,
                                                mock_generate_plot, mock_calculate_indicator,
                                                mock_get_point_size, mock_acquire_data):
        """Test a successful workflow run using csv mode (no parquet save)."""
        csv_args = argparse.Namespace(
            mode='csv', csv_file='input.csv', ticker=None, interval='H1',
            point=0.001, period=None, start=None, end=None, rule='PHLD', version=False
        )
        csv_data_info = {
             'ohlcv_df': self.sample_df.copy(), 'ticker': None, 'interval': 'H1',
             'data_source_label': 'input.csv', 'effective_mode': 'csv',
             'current_start': None, 'current_end': None,
             'file_size_bytes': 1234, 'data_metrics': {}, 'parquet_cache_used': False,
             'error_message': None, 'rows_count': len(self.sample_df), 'columns_count': len(self.sample_df.columns),
             'data_size_mb': 0.01
        }
        mock_acquire_data.return_value = csv_data_info
        mock_get_point_size.return_value = (0.001, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Predict_High_Low_Direction)
        mock_generate_plot.return_value = None

        with patch('time.perf_counter') as mock_perf_counter:
            # *** FIX: Provide enough time values (10 needed for success path) ***
            mock_perf_counter.side_effect = [0.0, 0.5, 0.55, 0.6, 0.65, 0.8, 0.85, 1.5, 1.55, 1.6]
            results = run_indicator_workflow(csv_args)

        # Assertions
        mock_acquire_data.assert_called_once_with(csv_args)
        mock_get_point_size.assert_called_once_with(csv_args, csv_data_info)
        pd.testing.assert_frame_equal(mock_calculate_indicator.call_args[0][1], self.sample_df)
        mock_calculate_indicator.assert_called_once_with(csv_args, ANY, 0.001)
        pd.testing.assert_frame_equal(mock_generate_plot.call_args[0][2], self.sample_df)
        mock_generate_plot.assert_called_once_with(csv_args, csv_data_info, ANY, TradingRule.Predict_High_Low_Direction, 0.001, False)
        self.assertTrue(results['success'])
        self.assertIsNone(results['parquet_cache_file']) # No cache file for CSV
        self.assertIsNone(results['error_message'])
        self.assertGreaterEqual(results['data_fetch_duration'], 0); self.assertGreaterEqual(results['calc_duration'], 0)
        self.assertGreaterEqual(results['plot_duration'], 0)
        self.assertIn('acquire', results['steps_duration']); self.assertIn('point_size', results['steps_duration'])
        self.assertIn('calculate', results['steps_duration']); self.assertIn('plot', results['steps_duration'])
        self.assertNotIn('save', results['steps_duration']) # No save step

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('src.workflow.workflow.logger')
    @patch('traceback.format_exc')
    def test_run_workflow_calculation_fail(self, mock_traceback, mock_logger, mock_makedirs,
                                           mock_generate_plot, mock_calculate_indicator,
                                           mock_get_point_size, mock_acquire_data):
        """Test workflow failure during indicator calculation."""
        mock_acquire_data.return_value = {**self.sample_data_info}
        mock_get_point_size.return_value = (0.01, False)
        calc_error_msg = "Calculation failed inside"
        mock_calculate_indicator.side_effect = RuntimeError(calc_error_msg)
        mock_traceback.return_value = "Mocked Traceback"

        with patch('time.perf_counter') as mock_perf_counter:
            # *** FIX: Provide enough values for path ending in except block (8 needed) ***
            mock_perf_counter.side_effect = [10.0, 10.5, 10.55, 10.6, 10.65, 10.8, 10.85, 10.9]
            results = run_indicator_workflow(self.mock_args)

        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_called_once()
        mock_calculate_indicator.assert_called_once()
        mock_generate_plot.assert_not_called()
        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        self.assertEqual(calc_error_msg, results['error_message'])
        self.assertEqual("Mocked Traceback", results['error_traceback'])
        self.assertGreater(mock_logger.print_error.call_count, 0)

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('src.workflow.workflow.logger')
    @patch('traceback.format_exc')
    def test_run_workflow_acquire_fail_returns_dict(self, mock_traceback, mock_logger, mock_makedirs,
                                                  mock_generate_plot, mock_calculate_indicator,
                                                  mock_get_point_size, mock_acquire_data):
        """Test workflow handles acquire_data failure by checking returned dict."""
        acquire_fail_msg = 'Simulated acquisition failure'
        mock_acquire_data.return_value = {
            'ohlcv_df': None, 'effective_mode': 'yfinance', 'data_source_label': 'yfinance_FAIL',
            'error_message': acquire_fail_msg, 'ticker': 'FAIL', 'interval': 'D1',
            'data_metrics': {}, 'parquet_cache_used': False, 'steps_duration': {} # Add steps_duration
        }
        mock_traceback.return_value = "Mocked Traceback"

        with patch('time.perf_counter') as mock_perf_counter:
             # *** FIX: Provide enough values for path ending in except block after acquire (5 needed) ***
            mock_perf_counter.side_effect = [0.0, 0.5, 0.55, 0.6, 0.7] # start_wf, end_acq, t_except(after value error check), print_error, end_wf
            results = run_indicator_workflow(self.mock_args)

        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_not_called()
        mock_calculate_indicator.assert_not_called()
        mock_generate_plot.assert_not_called()
        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        # Check the error message raised by the workflow itself
        self.assertEqual(acquire_fail_msg, results['error_message'])
        self.assertEqual("Mocked Traceback", results['error_traceback'])
        self.assertGreater(mock_logger.print_error.call_count, 0)


if __name__ == '__main__':
    unittest.main()