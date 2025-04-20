# tests/workflow/test_workflow.py

"""
Unit tests for the main workflow execution logic.
All comments are in English.
"""

import unittest
import pandas as pd
import os # Import os
from unittest.mock import patch, MagicMock, ANY # Import ANY

# Adjust the import path based on the project structure
from src.workflow.workflow import run_indicator_workflow

# Definition of the TestWorkflow class
class TestWorkflow(unittest.TestCase):
    """
    Test suite for the run_indicator_workflow function.
    """

    # --- Helper to create mock args ---
    def create_mock_args(self, mode='demo', **kwargs):
        """ Creates a mock args object for testing. """
        args = MagicMock()
        args.mode = mode
        args.ticker = 'TEST'
        args.interval = 'D1'
        args.start = '2023-01-01'
        args.end = '2023-01-05'
        args.period = None
        args.csv_file = None
        args.rule = 'Predict_High_Low_Direction'
        args.point = 0.01
        args.no_plot = False
        args.__dict__.update(kwargs)
        return args

    # --- Helper to create a base mock return for acquire_data ---
    def create_base_acquire_data_return(self, effective_mode, ohlcv_df=None, metrics=None):
        """ Creates a base dictionary mimicking acquire_data return value. """
        base_return = {
            "ohlcv_df": ohlcv_df if ohlcv_df is not None else pd.DataFrame({'Close': [100, 101, 102]}, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])),
            "effective_mode": effective_mode,
            "data_source_label": "MockSource",
            "yf_ticker": "MOCK" if effective_mode == 'yfinance' else None,
            "yf_interval": "1d" if effective_mode == 'yfinance' else None,
            "current_period": None,
            "current_start": "2023-01-01",
            "current_end": "2023-01-05",
            "file_size_bytes": None,
            "api_latency_sec": None,
        }
        if metrics:
            base_return.update(metrics) # Add specific metrics passed
        return base_return

    # --- Patch all external dependencies for the workflow ---
    # Note: Patching pandas DataFrame methods requires careful targetting if the instance is created inside
    # We patch where the functions are *looked up*
    @patch('src.workflow.workflow.generate_plot')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.os.makedirs') # Patch os.makedirs
    @patch('pandas.DataFrame.to_parquet')      # Patch DataFrame method where it's defined
    def test_run_workflow_success_api_mode_saves_parquet(self, mock_to_parquet, mock_makedirs, mock_acquire_data, mock_get_point_size, mock_calc_indicator, mock_generate_plot):
        """
        Test successful workflow run for an API mode (e.g., yfinance).
        Verifies calculation of metrics and that Parquet saving is attempted.
        """
        # --- Mock Configuration ---
        args = self.create_mock_args(mode='yfinance', ticker='API_TICKER')
        mock_df = pd.DataFrame({'Close': [1, 2, 3, 4]}, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']))
        mock_metrics = {"api_latency_sec": 1.23}
        acquire_return = self.create_base_acquire_data_return('yfinance', mock_df, mock_metrics)
        mock_acquire_data.return_value = acquire_return

        # Mock downstream steps return values
        mock_get_point_size.return_value = (0.01, False) # point_size, estimated_point
        mock_calc_indicator.return_value = (mock_df.copy(), args.rule) # result_df, selected_rule

        # --- Run Workflow ---
        workflow_results = run_indicator_workflow(args)

        # --- Assertions ---
        # Check main success flag and downstream calls
        self.assertTrue(workflow_results['success'])
        mock_acquire_data.assert_called_once_with(args)
        mock_get_point_size.assert_called_once_with(args, acquire_return)
        mock_calc_indicator.assert_called_once_with(args, ANY, 0.01) # ANY for df check
        mock_generate_plot.assert_called_once_with(args, acquire_return, ANY, args.rule, 0.01, False) # ANY for result_df check

        # Check calculated metrics
        self.assertEqual(workflow_results['rows_count'], 4)
        self.assertEqual(workflow_results['columns_count'], 1) # Only 'Close' column in mock_df
        self.assertGreater(workflow_results['data_size_bytes'], 0)
        self.assertGreater(workflow_results['data_size_mb'], 0)

        # Check propagated metrics
        self.assertIsNone(workflow_results['file_size_bytes'])
        self.assertEqual(workflow_results['api_latency_sec'], 1.23)

        # Check Parquet saving calls
        mock_makedirs.assert_called_once_with("data/raw_parquet", exist_ok=True)
        # Construct expected filename based on mocks
        expected_filename = "yfinance_API_TICKER_D1_2023-01-01_2023-01-05.parquet"
        expected_filepath = os.path.join("data/raw_parquet", expected_filename)
        # Assert to_parquet was called on the correct DataFrame instance with correct path
        # ANY is used for the dataframe instance check as it's created within the function scope sort of
        mock_to_parquet.assert_called_once()
        call_args, call_kwargs = mock_to_parquet.call_args
        self.assertEqual(call_args[0], expected_filepath) # Check the path argument
        self.assertEqual(call_kwargs.get('index'), True) # Check index=True
        self.assertEqual(call_kwargs.get('engine'), 'pyarrow') # Check engine

        # Check result dictionary path
        self.assertEqual(workflow_results['parquet_save_path'], expected_filepath)


    @patch('src.workflow.workflow.generate_plot')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    def test_run_workflow_success_csv_mode_no_parquet(self, mock_to_parquet, mock_makedirs, mock_acquire_data, mock_get_point_size, mock_calc_indicator, mock_generate_plot):
        """
        Test successful workflow run for CSV mode.
        Verifies metrics and ensures Parquet saving is NOT attempted.
        """
        # --- Mock Configuration ---
        args = self.create_mock_args(mode='csv', csv_file='data.csv')
        mock_df = pd.DataFrame({'Close': [50, 55]}, index=pd.to_datetime(['2023-02-01', '2023-02-02']))
        mock_metrics = {"file_size_bytes": 1024}
        acquire_return = self.create_base_acquire_data_return('csv', mock_df, mock_metrics)
        mock_acquire_data.return_value = acquire_return
        mock_get_point_size.return_value = (0.1, False)
        mock_calc_indicator.return_value = (mock_df.copy(), args.rule)

        # --- Run Workflow ---
        workflow_results = run_indicator_workflow(args)

        # --- Assertions ---
        self.assertTrue(workflow_results['success'])
        # Check calculated metrics
        self.assertEqual(workflow_results['rows_count'], 2)
        self.assertEqual(workflow_results['columns_count'], 1)
        # Check propagated metrics
        self.assertEqual(workflow_results['file_size_bytes'], 1024)
        self.assertIsNone(workflow_results['api_latency_sec'])

        # Check Parquet saving NOT called
        mock_makedirs.assert_not_called()
        mock_to_parquet.assert_not_called()
        self.assertIsNone(workflow_results['parquet_save_path'])

    @patch('src.workflow.workflow.generate_plot')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    def test_run_workflow_acquire_fail_no_parquet(self, mock_to_parquet, mock_makedirs, mock_acquire_data, mock_get_point_size, mock_calc_indicator, mock_generate_plot):
        """
        Test workflow when data acquisition fails (returns None df).
        Verifies downstream steps are not called and Parquet saving is not attempted.
        """
         # --- Mock Configuration ---
        args = self.create_mock_args(mode='yfinance')
        # Simulate acquire_data returning None df but potentially some metrics
        acquire_return = self.create_base_acquire_data_return('yfinance', ohlcv_df=None, metrics={"api_latency_sec": 0.1})
        mock_acquire_data.return_value = acquire_return

        # --- Run Workflow ---
        workflow_results = run_indicator_workflow(args)

        # --- Assertions ---
        self.assertFalse(workflow_results['success'])
        self.assertIsNotNone(workflow_results['error_message'])
        self.assertIn("Cannot proceed without valid data", workflow_results['error_message'])

        # Check downstream steps NOT called
        mock_get_point_size.assert_not_called()
        mock_calc_indicator.assert_not_called()
        mock_generate_plot.assert_not_called()

        # Check Parquet saving NOT called
        mock_makedirs.assert_not_called()
        mock_to_parquet.assert_not_called()
        self.assertIsNone(workflow_results['parquet_save_path'])

        # Check metrics that were calculated before failure
        self.assertEqual(workflow_results['rows_count'], 0) # Based on None df
        self.assertEqual(workflow_results['columns_count'], 0)
        self.assertEqual(workflow_results['data_size_bytes'], 0)
        self.assertEqual(workflow_results['api_latency_sec'], 0.1) # Propagated metric still present

    @patch('src.workflow.workflow.generate_plot')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.os.makedirs')
    @patch('pandas.DataFrame.to_parquet')
    def test_run_workflow_parquet_save_fails(self, mock_to_parquet, mock_makedirs, mock_acquire_data, mock_get_point_size, mock_calc_indicator, mock_generate_plot):
        """
        Test workflow when saving to Parquet fails with an exception.
        Workflow should still succeed overall, but path should be None.
        """
        # --- Mock Configuration ---
        args = self.create_mock_args(mode='polygon')
        mock_df = pd.DataFrame({'Close': [1, 2]})
        acquire_return = self.create_base_acquire_data_return('polygon', mock_df, metrics={"api_latency_sec": 0.5})
        mock_acquire_data.return_value = acquire_return
        mock_get_point_size.return_value = (1.0, False)
        mock_calc_indicator.return_value = (mock_df.copy(), args.rule)

        # Configure to_parquet mock to raise an error
        mock_to_parquet.side_effect = Exception("Simulated Parquet write error (e.g., disk full)")

        # --- Run Workflow ---
        workflow_results = run_indicator_workflow(args)

        # --- Assertions ---
        # Workflow should still be marked as successful (saving is best-effort?)
        # Or decide if save failure should make overall workflow fail? Currently, it doesn't.
        self.assertTrue(workflow_results['success'])
        self.assertIsNone(workflow_results['error_message']) # No workflow-stopping error

        # Check Parquet saving was attempted
        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once()

        # Check result dictionary path is None due to error
        self.assertIsNone(workflow_results['parquet_save_path'])

        # Check other steps were still called
        mock_calc_indicator.assert_called_once()
        mock_generate_plot.assert_called_once()


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()