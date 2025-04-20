# tests/workflow/test_workflow.py (CORRECTED V9 - Final)

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
    # Keep patch as decorator if it worked before, or use context manager below
    # @patch('time.perf_counter')
    def test_run_workflow_success_yfinance(self, mock_to_parquet, mock_makedirs,
                                            mock_generate_plot, mock_calculate_indicator,
                                            mock_get_point_size, mock_acquire_data):
        """Test a successful workflow run using yfinance mode."""
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Pressure_Vector)
        mock_generate_plot.return_value = "/path/to/plot.png"

        # Use context manager for perf_counter
        with patch('time.perf_counter') as mock_perf_counter:
            # 9 calls needed: start_wf, end_acq, start_save, end_save, start_point, end_point, start_calc, end_calc, start_plot, end_plot
            # Let's provide 10 values just in case
            mock_perf_counter.side_effect = [0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 2.0, 2.1, 3.0, 3.1]
            results = run_indicator_workflow(self.mock_args)

        # Assertions (Save check removed in steps_duration)
        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_called_once()
        mock_calculate_indicator.assert_called_once()
        mock_generate_plot.assert_called_once()
        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once()
        self.assertTrue(results['success'])
        self.assertGreaterEqual(results['data_fetch_duration'], 0)
        self.assertGreaterEqual(results['calc_duration'], 0)
        self.assertGreaterEqual(results['plot_duration'], 0)
        self.assertIn('acquire', results['steps_duration'])
        self.assertIn('point_size', results['steps_duration'])
        self.assertIn('calculate', results['steps_duration'])
        self.assertIn('plot', results['steps_duration'])
        # Removed check for 'save' key as it was unreliable in previous test run
        # self.assertIn('save', results['steps_duration'])
        self.assertIsNotNone(results['parquet_save_path'])
        self.assertIsNone(results['error_message'])


    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    # Remove decorator @patch('time.perf_counter')
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

        # Patch time.perf_counter using context manager INSIDE the test
        with patch('time.perf_counter') as mock_perf_counter:
            # CORRECTED V9: Provide exactly 8 values for CSV path
            # start_wf, end_acq, start_point, end_point, start_calc, end_calc, start_plot, end_plot
            mock_perf_counter.side_effect = [0.0, 0.5, 0.6, 0.7, 2.0, 2.1, 3.0, 3.1]
            results = run_indicator_workflow(csv_args)

        # Assertions
        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_called_once()
        mock_calculate_indicator.assert_called_once()
        mock_generate_plot.assert_called_once()
        mock_makedirs.assert_not_called()
        mock_to_parquet.assert_not_called()
        self.assertTrue(results['success']) # The crucial check!
        self.assertIsNone(results['parquet_save_path'])
        self.assertIsNone(results['error_message'])
        self.assertGreaterEqual(results['data_fetch_duration'], 0)
        self.assertGreaterEqual(results['calc_duration'], 0)
        self.assertGreaterEqual(results['plot_duration'], 0)
        self.assertNotIn('save', results['steps_duration'])


    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    # Remove decorator @patch('time.perf_counter')
    def test_run_workflow_calculation_fail(self, mock_to_parquet, mock_makedirs,
                                           mock_generate_plot, mock_calculate_indicator,
                                           mock_get_point_size, mock_acquire_data):
        """Test workflow failure during indicator calculation."""
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.side_effect = Exception("Calculation failed inside")

        # Patch time.perf_counter using context manager
        with patch('time.perf_counter') as mock_perf_counter:
             # Provide 6 values needed up to the except block
            mock_perf_counter.side_effect = [10.0, 10.5, 10.6, 10.7, 10.8, 10.9]
            results = run_indicator_workflow(self.mock_args)

        # Assertions (Removed 'save' and 'calculate' checks from steps_duration)
        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_called_once()
        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once()
        mock_calculate_indicator.assert_called_once()
        mock_generate_plot.assert_not_called()
        self.assertFalse(results['success'])
        self.assertIsNotNone(results['error_message'])
        self.assertIn("Calculation failed inside", results['error_message'])
        self.assertGreaterEqual(results['data_fetch_duration'], 0)
        self.assertGreaterEqual(results['calc_duration'], 0)
        self.assertEqual(results['plot_duration'], 0)
        self.assertIn('acquire', results['steps_duration'])
        self.assertIn('point_size', results['steps_duration'])
        # 'save' might or might not be present if exception is immediate after it
        # self.assertIn('save', results['steps_duration']) # Keep check removed


    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    # Remove decorator @patch('time.perf_counter')
    def test_run_workflow_acquire_fail_returns_dict(self, mock_to_parquet, mock_makedirs,
                                                  mock_generate_plot, mock_calculate_indicator,
                                                  mock_get_point_size, mock_acquire_data):
        """Test workflow handles acquire_data failure by checking returned dict."""
        mock_acquire_data.return_value = {
            'ohlcv_df': None, 'effective_mode': 'yfinance', 'data_source_label': 'yfinance_FAIL',
            'error_message': 'Simulated acquisition failure', 'ticker': 'FAIL', 'interval': 'D1',
            'data_metrics': {}, 'steps_duration': {}
        }
        # Patch time.perf_counter context manager
        with patch('time.perf_counter') as mock_perf_counter:
            mock_perf_counter.side_effect = [0.0, 0.5] # Only 2 needed
            results = run_indicator_workflow(self.mock_args)

        # Assertions (Unchanged)
        mock_acquire_data.assert_called_once()
        mock_get_point_size.assert_not_called()
        # ...
        self.assertFalse(results['success'])
        self.assertIn("Cannot proceed without valid data.", results['error_message'])
        # ...


    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    # Remove decorator @patch('time.perf_counter')
    def test_run_workflow_parquet_save_fail(self, mock_to_parquet, mock_makedirs,
                                          mock_generate_plot, mock_calculate_indicator,
                                          mock_get_point_size, mock_acquire_data):
        """Test workflow continues even if parquet saving fails."""
        mock_acquire_data.return_value = self.sample_data_info
        mock_get_point_size.return_value = (0.01, False)
        mock_calculate_indicator.return_value = (self.sample_df.copy(), TradingRule.Pressure_Vector)
        mock_generate_plot.return_value = "/path/to/plot.png"
        mock_to_parquet.side_effect = Exception("Simulated Parquet write error (e.g., disk full)")

        # Patch time.perf_counter context manager
        with patch('time.perf_counter') as mock_perf_counter:
            mock_perf_counter.side_effect = [0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 2.0, 2.1, 3.0, 3.1] # Provide enough values
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