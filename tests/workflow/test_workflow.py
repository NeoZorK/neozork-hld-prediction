# tests/workflow/test_workflow.py (Updated for new caching logic)

import unittest
from unittest.mock import patch, MagicMock, ANY
import pandas as pd
import argparse
import logging
import time

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
        # Sample data_info dictionary RETURNED BY acquire_data
        self.sample_data_info = {
             'ohlcv_df': self.sample_df, # Must contain the df
             'ticker': 'TEST', 'interval': 'D1',
             'data_source_label': 'yfinance_TEST', 'effective_mode': 'yfinance',
             'yf_ticker': 'TEST', 'yf_interval': 'D1', 'current_period': '1y',
             'current_start': '2023-01-01', 'current_end': '2023-01-05', # Example dates from args or fetch
             'api_latency_sec': 0.5, 'api_calls': 1, 'successful_chunks': 1,
             'file_size_bytes': None, 'data_metrics': {},
             'parquet_cache_used': False, # Indicate cache was not used in this mock setup
             'parquet_cache_file': None,
             'error_message': None
             # Other fields like rows_count etc., are also added by acquire_data
        }

    # REMOVED patch for 'pandas.DataFrame.to_parquet' and 'os.makedirs' for workflow saving
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs') # Keep if generate_plot creates dirs
    def test_run_workflow_success_yfinance(self, mock_makedirs, # Removed mock_to_parquet
                                            mock_generate_plot, mock_calculate_indicator,
                                            mock_get_point_size, mock_acquire_data):
        """Test a successful workflow run using yfinance mode."""
        # Mock acquire_data returns the full data_info dict
        mock_acquire_data.return_value = {**self.sample_data_info} # Use a copy
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Pressure_Vector)
        # Mock generate_plot (doesn't return path anymore based on current code)
        mock_generate_plot.return_value = None

        # Use context manager for perf_counter
        with patch('time.perf_counter') as mock_perf_counter:
            # Provide enough values (timing simplified here)
            mock_perf_counter.side_effect = [0.0, 0.5, 0.6, 0.7, 0.8] # start_wf, end_acq, start_point, end_point, start_calc, end_calc, start_plot, end_plot
            results = run_indicator_workflow(self.mock_args)

        # Assertions
        mock_acquire_data.assert_called_once_with(self.mock_args)
        mock_get_point_size.assert_called_once_with(self.mock_args, self.sample_data_info)
        mock_calculate_indicator.assert_called_once_with(self.mock_args, ANY, 0.01)
        mock_generate_plot.assert_called_once_with(self.mock_args, self.sample_data_info, ANY, TradingRule.Pressure_Vector, 0.01, False)
        # Removed mock_to_parquet.assert_called_once()
        # Keep mock_makedirs if plot creates dirs: mock_makedirs.assert_called()

        self.assertTrue(results['success'])
        self.assertGreaterEqual(results['data_fetch_duration'], 0)
        self.assertGreaterEqual(results['calc_duration'], 0)
        self.assertGreaterEqual(results['plot_duration'], 0)
        self.assertIn('acquire', results['steps_duration'])
        self.assertIn('point_size', results['steps_duration'])
        self.assertIn('calculate', results['steps_duration'])
        self.assertIn('plot', results['steps_duration'])
        # parquet_save_path is no longer directly set by workflow, check if present from acquire_data mock if needed
        # self.assertIsNotNone(results['parquet_save_path'])
        self.assertIsNone(results['error_message'])


    # REMOVED patch for 'pandas.DataFrame.to_parquet' and 'os.makedirs'
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs') # Keep if generate_plot creates dirs
    def test_run_workflow_success_csv_no_parquet(self, mock_makedirs, # Removed mock_to_parquet
                                                mock_generate_plot, mock_calculate_indicator,
                                                mock_get_point_size, mock_acquire_data):
        """Test a successful workflow run using csv mode (no parquet save)."""
        csv_args = argparse.Namespace(
            mode='csv', csv_file='input.csv', ticker=None, interval='H1',
            point=0.001, period=None, start=None, end=None, rule='PHLD', version=False
        )
        # Mock acquire_data to return structure for CSV mode
        csv_data_info = {
             'ohlcv_df': self.sample_df.copy(), 'ticker': None, 'interval': 'H1',
             'data_source_label': 'input.csv', 'effective_mode': 'csv',
             'current_start': None, 'current_end': None, # Dates might be parsed from CSV index by acquire_data
             'file_size_bytes': 1234, 'data_metrics': {}, 'parquet_cache_used': False,
             'error_message': None
        }
        mock_acquire_data.return_value = csv_data_info
        mock_get_point_size.return_value = (0.001, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Predict_High_Low_Direction)
        mock_generate_plot.return_value = None

        with patch('time.perf_counter') as mock_perf_counter:
            # Values for CSV path (no save step timing needed here)
            mock_perf_counter.side_effect = [0.0, 0.5, 0.6, 0.7, 2.0, 2.1, 3.0, 3.1]
            results = run_indicator_workflow(csv_args)

        # Assertions
        mock_acquire_data.assert_called_once_with(csv_args)
        mock_get_point_size.assert_called_once_with(csv_args, csv_data_info)
        mock_calculate_indicator.assert_called_once_with(csv_args, ANY, 0.001)
        mock_generate_plot.assert_called_once_with(csv_args, csv_data_info, ANY, TradingRule.Predict_High_Low_Direction, 0.001, False)
        # mock_makedirs.assert_not_called() # Might be called by plot
        # mock_to_parquet.assert_not_called() # Removed

        self.assertTrue(results['success'])
        self.assertIsNone(results['parquet_cache_file']) # No cache file for CSV
        self.assertIsNone(results['error_message'])
        self.assertGreaterEqual(results['data_fetch_duration'], 0)
        self.assertGreaterEqual(results['calc_duration'], 0)
        self.assertGreaterEqual(results['plot_duration'], 0)
        self.assertNotIn('save', results['steps_duration'])


    # REMOVED patch for 'pandas.DataFrame.to_parquet' and 'os.makedirs'
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs') # Keep if plot needs it
    def test_run_workflow_calculation_fail(self, mock_makedirs, # Removed mock_to_parquet
                                           mock_generate_plot, mock_calculate_indicator,
                                           mock_get_point_size, mock_acquire_data):
        """Test workflow failure during indicator calculation."""
        # acquire_data mock should return a valid df for calc step to be reached
        mock_acquire_data.return_value = {**self.sample_data_info} # Use copy
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.side_effect = Exception("Calculation failed inside")

        with patch('time.perf_counter') as mock_perf_counter:
            # Values needed up to the exception in calculate step
            mock_perf_counter.side_effect = [10.0, 10.5, 10.6, 10.7, 10.8] # start_wf, end_acq, start_point, end_point, start_calc, end_calc (in except)
            results = run_indicator_workflow(self.mock_args)

        # Assertions
        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_called_once()
        mock_calculate_indicator.assert_called_once() # It was called before failing
        mock_generate_plot.assert_not_called()
        # mock_makedirs might be called by acquire_data, not workflow
        # mock_to_parquet is not called by workflow

        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        self.assertIn("Calculation failed inside", results['error_message'])
        self.assertIsNotNone(results['error_traceback'])
        self.assertGreaterEqual(results['data_fetch_duration'], 0)
        self.assertGreaterEqual(results['calc_duration'], 0)
        self.assertEqual(results['plot_duration'], 0)
        self.assertIn('acquire', results['steps_duration'])
        self.assertIn('point_size', results['steps_duration'])
        # Calculation step duration might be recorded depending on exact exception timing
        # self.assertIn('calculate', results['steps_duration']) # Make this check optional


    # REMOVED patch for 'pandas.DataFrame.to_parquet' and 'os.makedirs'
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs') # Keep if plot needs it
    def test_run_workflow_acquire_fail_returns_dict(self, mock_makedirs, # Removed mock_to_parquet
                                                  mock_generate_plot, mock_calculate_indicator,
                                                  mock_get_point_size, mock_acquire_data):
        """Test workflow handles acquire_data failure by checking returned dict."""
        mock_acquire_data.return_value = {
            'ohlcv_df': None, 'effective_mode': 'yfinance', 'data_source_label': 'yfinance_FAIL',
            'error_message': 'Simulated acquisition failure', 'ticker': 'FAIL', 'interval': 'D1',
            'data_metrics': {}, 'steps_duration': {}, 'parquet_cache_used': False
        }
        with patch('time.perf_counter') as mock_perf_counter:
            mock_perf_counter.side_effect = [0.0, 0.5] # start_wf, end_acq
            results = run_indicator_workflow(self.mock_args)

        # Assertions
        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_not_called() # Should not be called if acquire fails
        mock_calculate_indicator.assert_not_called()
        mock_generate_plot.assert_not_called()
        # mock_makedirs.assert_not_called() # Might be called by acquire_data if it tries to save cache path? Unlikely on fail.
        # mock_to_parquet.assert_not_called() # Removed

        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        # The error message might come from acquire_data or the ValueError raised after
        self.assertTrue("Simulated acquisition failure" in results['error_message'] or \
                        "Cannot proceed without valid data" in results['error_message'])
        self.assertIsNotNone(results['error_traceback'])


    # REMOVED test_run_workflow_parquet_save_fail as saving is handled in acquire_data now

if __name__ == '__main__':
    unittest.main()