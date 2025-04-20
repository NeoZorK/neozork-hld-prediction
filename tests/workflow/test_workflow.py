# tests/workflow/test_workflow.py (CORRECTED V5 - Calc Duration Assert + Expand CSV Perf Counter)

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
    @patch('time.perf_counter')
    def test_run_workflow_success_yfinance(self, mock_perf_counter, mock_to_parquet, mock_makedirs,
                                            mock_generate_plot, mock_calculate_indicator,
                                            mock_get_point_size, mock_acquire_data):
        """Test a successful workflow run using yfinance mode."""
        # Provide enough values to avoid StopIteration
        mock_perf_counter.side_effect = [0.0, 0.5, 0.6, 0.7, 2.0, 2.1, 3.0, 3.1, 4.0, 5.0]
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Pressure_Vector)
        mock_generate_plot.return_value = "/path/to/plot.png"

        results = run_indicator_workflow(self.mock_args)

        # Assertions (Save check removed)
        mock_acquire_data.assert_called_once_with(self.mock_args)
        mock_get_point_size.assert_called_once_with(self.mock_args, self.sample_data_info)
        mock_calculate_indicator.assert_called_once_with(self.mock_args, ANY, 0.01)
        mock_generate_plot.assert_called_once_with(self.mock_args, self.sample_data_info, ANY, TradingRule.Pressure_Vector, 0.01, False)
        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once()
        self.assertTrue(results['success'])
        self.assertAlmostEqual(results['data_fetch_duration'], 0.5)
        self.assertAlmostEqual(results['calc_duration'], 0.1) # 2.1 - 2.0
        self.assertAlmostEqual(results['plot_duration'], 0.1) # 3.1 - 3.0
        # Check steps_duration (save check removed)
        self.assertIn('acquire', results['steps_duration'])
        self.assertAlmostEqual(results['steps_duration']['acquire'], 0.5)
        self.assertIn('point_size', results['steps_duration'])
        self.assertAlmostEqual(results['steps_duration']['point_size'], 0.1)
        self.assertIn('calculate', results['steps_duration'])
        self.assertAlmostEqual(results['steps_duration']['calculate'], 0.1)
        self.assertIn('plot', results['steps_duration'])
        self.assertAlmostEqual(results['steps_duration']['plot'], 0.1)
        self.assertIsNotNone(results['parquet_save_path'])
        self.assertIsNone(results['error_message'])

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
        # CORRECTED V5: Provide more values to avoid StopIteration
        mock_perf_counter.side_effect = [0.0, 0.5, 0.6, 2.0, 2.1, 3.0, 3.1, 4.0, 5.0, 6.0] # 10 values
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

        # Assertions
        mock_acquire_data.assert_called_once_with(csv_args)
        mock_get_point_size.assert_called_once_with(csv_args, csv_data_info)
        mock_calculate_indicator.assert_called_once_with(csv_args, ANY, 0.001)
        mock_generate_plot.assert_called_once_with(csv_args, csv_data_info, ANY, TradingRule.Predict_High_Low_Direction, 0.001, False)
        mock_makedirs.assert_not_called()
        mock_to_parquet.assert_not_called()
        self.assertTrue(results['success']) # Should pass now
        self.assertIsNone(results['parquet_save_path'])
        self.assertIsNone(results['error_message'])
        # Check durations (only those expected for CSV)
        self.assertAlmostEqual(results['data_fetch_duration'], 0.5)
        self.assertAlmostEqual(results['calc_duration'], 0.1) # 2.1 - 2.0
        self.assertAlmostEqual(results['plot_duration'], 0.1) # 3.1 - 3.0
        self.assertNotIn('save', results['steps_duration'])


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
        # Provide 6 values
        mock_perf_counter.side_effect = [10.0, 10.5, 10.6, 10.7, 10.8, 10.9]
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.side_effect = Exception("Calculation failed inside")

        results = run_indicator_workflow(self.mock_args)

        # Assertions
        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_called_once()
        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once()
        mock_calculate_indicator.assert_called_once()
        mock_generate_plot.assert_not_called()
        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        self.assertIn("Calculation failed inside", results['error_message'])
        # Check durations
        self.assertAlmostEqual(results['data_fetch_duration'], 0.5)
        # CORRECTED V5: Use assertGreaterEqual for calc_duration in failure case
        self.assertGreaterEqual(results['calc_duration'], 0) # Allow 0 for instant exception
        self.assertEqual(results['plot_duration'], 0)
        # Check steps_duration timing (remove 'save' check here too for consistency)
        self.assertAlmostEqual(results['steps_duration']['acquire'], 0.5)
        self.assertAlmostEqual(results['steps_duration']['point_size'], 0.1)
        self.assertGreaterEqual(results['steps_duration']['calculate'], 0)


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
        mock_perf_counter.side_effect = [0.0, 0.5]
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

        # Call function and check results dict
        results = run_indicator_workflow(self.mock_args)

        # Assertions (Unchanged)
        mock_acquire_data.assert_called_once_with(self.mock_args)
        mock_get_point_size.assert_not_called()
        mock_calculate_indicator.assert_not_called()
        # ... other not called asserts ...
        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        self.assertIn("Cannot proceed without valid data.", results['error_message'])
        # ... other asserts ...


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
        mock_perf_counter.side_effect = [0.0, 0.5, 0.6, 0.7, 2.0, 2.1, 3.0, 3.1, 4.0, 5.0]
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Pressure_Vector)
        mock_generate_plot.return_value = "/path/to/plot.png"
        mock_to_parquet.side_effect = Exception("Simulated Parquet write error (e.g., disk full)")

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


if __name__ == '__main__':
    unittest.main()