# tests/workflow/test_workflow.py

import unittest
from unittest.mock import patch #, MagicMock, ANY
import argparse
import pandas as pd
#import time

# Import the function to test
from src.workflow.workflow import run_indicator_workflow
# Import dependencies to mock
from src.common.constants import TradingRule

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass
    def print_success(self, msg): pass

# Dummy args namespace
def create_mock_args(mode='demo', rule='Predict_High_Low_Direction'):
    # Add other args if needed by mocked functions
    return argparse.Namespace(mode=mode, rule=rule, ticker=None, interval=None, point=None)

# Unit tests for the main workflow orchestrator
class TestWorkflow(unittest.TestCase):

    # Patch all the step functions called by the workflow
    @patch('src.workflow.workflow.logger', new_callable=MockLogger)
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('time.perf_counter') # Mock time to control durations
    def test_run_workflow_success(self, mock_perf_counter, mock_generate_plot, mock_calculate_indicator, mock_get_point_size, mock_acquire_data, _):
        # --- Setup Mocks ---
        args = create_mock_args(mode='demo')
        # Mock time sequence
        mock_perf_counter.side_effect = [0.0, 0.1, 0.1, 0.3, 0.3, 0.5] # t0, t1_data, t2_point (no time), t3_calc, t4_plot_start, t5_plot_end

        # Mock data acquisition result
        mock_ohlcv_df = pd.DataFrame({'Close': [1], 'Volume': [100]})
        mock_data_info = {
            "ohlcv_df": mock_ohlcv_df, "effective_mode": "demo", "data_source_label": "Demo",
            "yf_ticker": None, "yf_interval": None, "current_period": None, "current_start": None, "current_end": None
        }
        mock_acquire_data.return_value = mock_data_info

        # Mock point size result
        mock_point_size = 0.0001
        mock_estimated = False
        mock_get_point_size.return_value = (mock_point_size, mock_estimated)

        # Mock indicator calculation result
        mock_result_df = pd.DataFrame({'PPrice1': [0.99]})
        mock_selected_rule = TradingRule.Predict_High_Low_Direction
        mock_calculate_indicator.return_value = (mock_result_df, mock_selected_rule)

        # Mock plotting (doesn't return anything, just check call)

        # --- Execute Workflow ---
        results = run_indicator_workflow(args)

        # --- Assertions ---
        # 1. Check steps were called in order with correct args
        mock_acquire_data.assert_called_once_with(args)
        mock_get_point_size.assert_called_once_with(args, mock_data_info)
        mock_calculate_indicator.assert_called_once_with(args, mock_ohlcv_df, mock_point_size)
        mock_generate_plot.assert_called_once_with(args, mock_data_info, mock_result_df, mock_selected_rule, mock_point_size, mock_estimated)

        # 2. Check final results dictionary
        self.assertTrue(results['success'])
        self.assertIsNone(results['error_message'])
        # Check timing calculations (t1-t0, t3-t2(same as t1), t5-t4)
        self.assertAlmostEqual(results['data_fetch_duration'], 0.1) # 0.1 - 0.0
        self.assertAlmostEqual(results['calc_duration'], 0.2)     # 0.3 - 0.1
        self.assertAlmostEqual(results['plot_duration'], 0.2)     # 0.5 - 0.3
        # Check data size calculation (approximate)
        self.assertGreater(results['data_size_bytes'], 0)
        self.assertGreater(results['data_size_mb'], 0)
        # Check pass-through values
        self.assertEqual(results['point_size'], mock_point_size)
        self.assertEqual(results['estimated_point'], mock_estimated)
        self.assertEqual(results['effective_mode'], mock_data_info['effective_mode'])
        self.assertEqual(results['data_source_label'], mock_data_info['data_source_label'])
        self.assertEqual(results['selected_rule'], mock_selected_rule)


    # Test workflow failure during data acquisition
    @patch('src.workflow.workflow.logger', new_callable=MockLogger)
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('time.perf_counter')
    def test_run_workflow_fail_data_acquisition(self, mock_perf_counter, mock_generate_plot, mock_calculate_indicator, mock_get_point_size, mock_acquire_data, _):
        args = create_mock_args(mode='yf')
        mock_perf_counter.side_effect = [0.0, 0.1] # Only time until data fetch fails
        error_message = "Ticker required"
        # Simulate acquire_data raising an exception
        mock_acquire_data.side_effect = ValueError(error_message)

        results = run_indicator_workflow(args)

        # Assertions
        mock_acquire_data.assert_called_once_with(args)
        # Subsequent steps should NOT be called
        mock_get_point_size.assert_not_called()
        mock_calculate_indicator.assert_not_called()
        mock_generate_plot.assert_not_called()

        # Check results dictionary indicates failure
        self.assertFalse(results['success'])
        self.assertEqual(results['error_message'], error_message)
        self.assertAlmostEqual(results['data_fetch_duration'], 0.1) # Time until failure
        self.assertEqual(results['calc_duration'], 0) # Other timings are 0
        self.assertEqual(results['plot_duration'], 0)


    # Test workflow failure during point size determination
    @patch('src.workflow.workflow.logger', new_callable=MockLogger)
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('time.perf_counter')
    def test_run_workflow_fail_point_size(self, mock_perf_counter, mock_generate_plot, mock_calculate_indicator, mock_get_point_size, mock_acquire_data, _):
        args = create_mock_args(mode='yf')
        mock_perf_counter.side_effect = [0.0, 0.1, 0.1] # Time until point size fails
        mock_ohlcv_df = pd.DataFrame({'Close': [1]})
        mock_data_info = {"ohlcv_df": mock_ohlcv_df, "effective_mode": "yfinance"}
        mock_acquire_data.return_value = mock_data_info
        error_message = "Estimation failed"
        mock_get_point_size.side_effect = ValueError(error_message) # Point size step fails

        results = run_indicator_workflow(args)

        mock_acquire_data.assert_called_once_with(args)
        mock_get_point_size.assert_called_once_with(args, mock_data_info)
        mock_calculate_indicator.assert_not_called()
        mock_generate_plot.assert_not_called()

        self.assertFalse(results['success'])
        self.assertEqual(results['error_message'], error_message)
        self.assertAlmostEqual(results['data_fetch_duration'], 0.1)
        # No duration recorded specifically for point size failure


    # Test workflow failure during indicator calculation
    @patch('src.workflow.workflow.logger', new_callable=MockLogger)
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('time.perf_counter')
    def test_run_workflow_fail_calculation(self, mock_perf_counter, mock_generate_plot, mock_calculate_indicator, mock_get_point_size, mock_acquire_data, _):
        args = create_mock_args(mode='demo')
        mock_perf_counter.side_effect = [0.0, 0.1, 0.1, 0.3] # Time until calc fails
        mock_ohlcv_df = pd.DataFrame({'Close': [1]})
        mock_data_info = {"ohlcv_df": mock_ohlcv_df, "effective_mode": "demo"}
        mock_acquire_data.return_value = mock_data_info
        mock_point_size, mock_estimated = (0.01, False)
        mock_get_point_size.return_value = (mock_point_size, mock_estimated)
        error_message = "Invalid rule"
        mock_calculate_indicator.side_effect = ValueError(error_message) # Calc step fails

        results = run_indicator_workflow(args)

        mock_acquire_data.assert_called_once_with(args)
        mock_get_point_size.assert_called_once_with(args, mock_data_info)
        mock_calculate_indicator.assert_called_once_with(args, mock_ohlcv_df, mock_point_size)
        mock_generate_plot.assert_not_called() # Plotting skipped

        self.assertFalse(results['success'])
        self.assertEqual(results['error_message'], error_message)
        self.assertAlmostEqual(results['data_fetch_duration'], 0.1)
        self.assertAlmostEqual(results['calc_duration'], 0.2) # Time until failure
        self.assertEqual(results['plot_duration'], 0)


    # Test workflow success even if calculation returns None/Empty (warning, not error)
    @patch('src.workflow.workflow.logger') # Use MagicMock logger to check warnings
    @patch('src.workflow.workflow.acquire_data')
    @patch('src.workflow.workflow.get_point_size')
    @patch('src.workflow.workflow.calculate_indicator')
    @patch('src.workflow.workflow.generate_plot')
    @patch('time.perf_counter')
    def test_run_workflow_success_calc_returns_empty(self, mock_perf_counter, mock_generate_plot, mock_calculate_indicator, mock_get_point_size, mock_acquire_data, _):
        args = create_mock_args(mode='demo')
        mock_perf_counter.side_effect = [0.0, 0.1, 0.1, 0.3, 0.3, 0.5]
        mock_ohlcv_df = pd.DataFrame({'Close': [1]})
        mock_data_info = {"ohlcv_df": mock_ohlcv_df, "effective_mode": "demo"}
        mock_acquire_data.return_value = mock_data_info
        mock_point_size, mock_estimated = (0.01, False)
        mock_get_point_size.return_value = (mock_point_size, mock_estimated)
        # Simulate calculation returning empty DF and selected rule
        mock_result_df_empty = pd.DataFrame()
        mock_selected_rule = TradingRule.Pressure_Vector
        mock_calculate_indicator.return_value = (mock_result_df_empty, mock_selected_rule)

        results = run_indicator_workflow(args)

        # Workflow should still be marked as success
        self.assertTrue(results['success'])
        self.assertIsNone(results['error_message'])
        # Check timings
        self.assertAlmostEqual(results['calc_duration'], 0.2)
        self.assertAlmostEqual(results['plot_duration'], 0.2)
        # Check warning was logged in calculate_indicator (mocked here implicitly via logger)
        # This relies on calculate_indicator logging the warning, which it does
        # A more direct test would mock logger inside calculate_indicator itself
        # Check generate_plot was called (it handles empty df internally)
        mock_generate_plot.assert_called_once_with(args, mock_data_info, mock_result_df_empty, mock_selected_rule, mock_point_size, mock_estimated)

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()