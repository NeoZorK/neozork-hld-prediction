# tests/workflow/test_workflow.py (CORRECTED - Perf Counter Values + Assert Order)

import unittest
from unittest.mock import patch, MagicMock, ANY
import pandas as pd
import argparse
import logging
import time # Import time

# Import the function to test
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
            'Open': [100, 110, 120, 130],
            'High': [105, 115, 125, 135],
            'Low': [95, 105, 115, 125],
            'Close': [102, 112, 122, 132],
            'Volume': [1000, 1100, 1200, 1300]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']))
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
             'data_metrics': {}
        }

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    @patch('time.perf_counter') # Ensure time is mocked if durations are checked precisely
    def test_run_workflow_success_yfinance(self, mock_perf_counter, mock_to_parquet, mock_makedirs,
                                            mock_generate_plot, mock_calculate_indicator,
                                            mock_get_point_size, mock_acquire_data):
        """Test a successful workflow run using yfinance mode."""
        # Provide enough mock time values for all steps
        mock_perf_counter.side_effect = [0.0, 0.5, 0.6, 0.7, 2.0, 2.1, 3.0, 3.1] # start, end_acq, end_point, end_save, start_calc, end_calc, start_plot, end_plot
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Pressure_Vector)
        mock_generate_plot.return_value = "/path/to/plot.png"

        results = run_indicator_workflow(self.mock_args)

        # Assertions (Unchanged structure, but mock_perf_counter affects durations)
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
        # Check durations based on mock_perf_counter values
        self.assertAlmostEqual(results['data_fetch_duration'], 0.5) # 0.5 - 0.0
        self.assertAlmostEqual(results['calc_duration'], 0.1) # 2.1 - 2.0
        self.assertAlmostEqual(results['plot_duration'], 0.1) # 3.1 - 3.0
        self.assertIn('acquire', results['steps_duration'])
        self.assertAlmostEqual(results['steps_duration']['acquire'], 0.5)
        self.assertIn('point_size', results['steps_duration'])
        self.assertAlmostEqual(results['steps_duration']['point_size'], 0.1) # 0.6 - 0.5
        self.assertIn('save', results['steps_duration'])
        self.assertAlmostEqual(results['steps_duration']['save'], 0.1) # 0.7 - 0.6
        self.assertIn('calculate', results['steps_duration'])
        self.assertAlmostEqual(results['steps_duration']['calculate'], 0.1) # 2.1 - 2.0
        self.assertIn('plot', results['steps_duration'])
        self.assertAlmostEqual(results['steps_duration']['plot'], 0.1) # 3.1 - 3.0

        self.assertIsNotNone(results['parquet_save_path'])
        self.assertIsNone(results['error_message'])
        self.assertIsNotNone(results.get('data_metrics'))

    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    @patch('time.perf_counter')
    def test_run_workflow_success_csv_no_parquet(self, mock_perf_counter, mock_to_parquet, mock_makedirs,
                                                mock_generate_plot, mock_calculate_indicator,
                                                mock_get_point_size, mock_acquire_data):
        """Test a successful workflow run using csv mode (no parquet save)."""
        # Provide enough mock time values
        mock_perf_counter.side_effect = [0.0, 0.5, 0.6, 0.7, 2.0, 2.1, 3.0, 3.1]
        csv_args = argparse.Namespace(
            mode='csv', csv_file='input.csv', ticker=None, interval='H1',
            point=0.001, period=None, start=None, end=None, rule='PHLD', version=False
        )
        csv_data_info = self.sample_data_info.copy()
        csv_data_info['effective_mode'] = 'csv'
        csv_data_info['data_source_label'] = 'input.csv'
        # csv_data_info['point'] = 0.001 # point is derived now
        csv_data_info['ohlcv_df'] = self.sample_df.copy()

        mock_acquire_data.return_value = csv_data_info
        mock_get_point_size.return_value = (0.001, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Predict_High_Low_Direction)
        mock_generate_plot.return_value = "/path/to/plot.png"

        results = run_indicator_workflow(csv_args)

        # Assertions (Unchanged structure)
        mock_acquire_data.assert_called_once_with(csv_args)
        mock_get_point_size.assert_called_once_with(csv_args, csv_data_info)
        mock_calculate_indicator.assert_called_once_with(csv_args, ANY, 0.001)
        mock_generate_plot.assert_called_once_with(csv_args, csv_data_info, ANY, TradingRule.Predict_High_Low_Direction, 0.001, False)
        mock_makedirs.assert_not_called() # No save for csv
        mock_to_parquet.assert_not_called() # No save for csv
        self.assertTrue(results['success'])
        self.assertEqual(results['point_size'], 0.001)
        self.assertFalse(results['estimated_point'])
        self.assertEqual(results['selected_rule'], TradingRule.Predict_High_Low_Direction)
        self.assertIsNone(results['parquet_save_path'])
        self.assertIsNone(results['error_message'])
        self.assertIsNotNone(results.get('data_metrics'))
        # Check durations (save step should be missing or zero)
        self.assertAlmostEqual(results['data_fetch_duration'], 0.5)
        self.assertAlmostEqual(results['calc_duration'], 0.1)
        self.assertAlmostEqual(results['plot_duration'], 0.1)
        self.assertNotIn('save', results['steps_duration']) # Save step shouldn't run for CSV


    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    @patch('time.perf_counter')
    def test_run_workflow_calculation_fail(self, mock_perf_counter, mock_to_parquet, mock_makedirs,
                                           mock_generate_plot, mock_calculate_indicator,
                                           mock_get_point_size, mock_acquire_data):
        """Test workflow failure during indicator calculation."""
        # CORRECTED: Provide 5 time values for steps up to and including the except block
        mock_perf_counter.side_effect = [10.0, 10.5, 10.6, 10.7, 10.8] # start_wf, end_acq, end_point, end_save, start_calc, end_calc (in except)
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.side_effect = Exception("Calculation failed inside")

        results = run_indicator_workflow(self.mock_args)

        # Assertions
        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_called_once()
        # CORRECTED: Assert save was called before checking calc
        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once()
        # Now assert calculate_indicator was called (should pass now)
        mock_calculate_indicator.assert_called_once()
        mock_generate_plot.assert_not_called()

        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        self.assertIn("Calculation failed inside", results['error_message'])
        self.assertIsNotNone(results['error_traceback'])
        # Check durations
        self.assertAlmostEqual(results['data_fetch_duration'], 0.5) # 10.5 - 10.0
        self.assertAlmostEqual(results['calc_duration'], 0.1) # 10.8 - 10.7 (start_calc=10.7, end_calc_in_except=10.8)
        self.assertEqual(results['plot_duration'], 0)
        self.assertIsNotNone(results.get('data_metrics'))
        # Check steps_duration timing
        self.assertAlmostEqual(results['steps_duration']['acquire'], 0.5) # 10.5 - 10.0
        self.assertAlmostEqual(results['steps_duration']['point_size'], 0.1) # 10.6 - 10.5
        self.assertAlmostEqual(results['steps_duration']['save'], 0.1) # 10.7 - 10.6
        self.assertAlmostEqual(results['steps_duration']['calculate'], 0.1) # 10.8 - 10.7


    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    @patch('time.perf_counter')
    def test_run_workflow_acquire_fail_returns_dict(self, mock_perf_counter, mock_to_parquet, mock_makedirs,
                                                  mock_generate_plot, mock_calculate_indicator,
                                                  mock_get_point_size, mock_acquire_data):
        """Test workflow handles acquire_data failure by checking returned dict."""
        mock_perf_counter.side_effect = [0.0, 0.5] # start_wf, end_acq (where failure happens)
        mock_acquire_data.return_value = {
            'ohlcv_df': None,
            'effective_mode': 'yfinance',
            'data_source_label': 'yfinance_FAIL',
            'error_message': 'Simulated acquisition failure',
            'ticker': 'FAIL',
            'interval': 'D1',
            'data_metrics': {},
            'steps_duration': {}
        }

        # CORRECTED: Call function and check results dict, not exception
        results = run_indicator_workflow(self.mock_args)

        # Assertions
        mock_acquire_data.assert_called_once_with(self.mock_args)
        mock_get_point_size.assert_not_called()
        mock_calculate_indicator.assert_not_called()
        mock_generate_plot.assert_not_called()
        mock_makedirs.assert_not_called()
        mock_to_parquet.assert_not_called()
        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        self.assertIn("Cannot proceed without valid data.", results['error_message']) # Error generated by workflow
        self.assertIsNotNone(results['error_traceback'])
        # Check duration only for acquire step
        self.assertAlmostEqual(results['data_fetch_duration'], 0.5)
        self.assertEqual(results['calc_duration'], 0)
        self.assertEqual(results['plot_duration'], 0)
        self.assertAlmostEqual(results['steps_duration']['acquire'], 0.5)


    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    @patch('time.perf_counter')
    def test_run_workflow_parquet_save_fail(self, mock_perf_counter, mock_to_parquet, mock_makedirs,
                                          mock_generate_plot, mock_calculate_indicator,
                                          mock_get_point_size, mock_acquire_data):
        """Test workflow continues even if parquet saving fails."""
        # Provide enough mock time values
        mock_perf_counter.side_effect = [0.0, 0.5, 0.6, 0.7, 2.0, 2.1, 3.0, 3.1]
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Pressure_Vector)
        mock_generate_plot.return_value = "/path/to/plot.png"
        # Simulate parquet write failure
        mock_to_parquet.side_effect = Exception("Simulated Parquet write error (e.g., disk full)")

        results = run_indicator_workflow(self.mock_args)

        # Assertions (Unchanged structure)
        mock_acquire_data.assert_called_once()
        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once()
        mock_get_point_size.assert_called_once()
        mock_calculate_indicator.assert_called_once()
        mock_generate_plot.assert_called_once()
        self.assertTrue(results['success']) # Overall workflow succeeded
        self.assertIsNone(results['parquet_save_path']) # Path should be None
        self.assertIsNone(results['error_message']) # No critical error
        self.assertIsNotNone(results.get('data_metrics'))


if __name__ == '__main__':
    unittest.main()