# tests/plotting/test_plotting_generation.py # CORRECTED v2: Assertions

import unittest
from unittest.mock import patch, ANY # Import ANY
import argparse
import pandas as pd
import traceback # Import traceback

# Import the function to test and dependencies
from src.plotting.plotting_generation import generate_plot
from src.common.constants import TradingRule

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass

# Dummy args namespace
def create_mock_args(interval='D1'):
    return argparse.Namespace(interval=interval)

# Unit tests for the plotting generation workflow step
class TestPlottingGenerationStep(unittest.TestCase):

    # Setup basic data
    def setUp(self):
        self.args = create_mock_args(interval='H4')
        self.data_info = {
            'data_source_label': 'EURUSD=X',
            'effective_mode': 'yfinance',
            'yf_ticker': 'EURUSD=X' # Used if point estimated
        }
        self.result_df = pd.DataFrame({'Close': [1.1, 1.2, 1.15]}) # Dummy DF
        self.selected_rule = TradingRule.Predict_High_Low_Direction
        self.point_size = 0.0001
        self.estimated_point = False

    # Test successful plot generation
    @patch('src.plotting.plotting_generation.logger', new_callable=MockLogger)
    @patch('src.plotting.plotting_generation.plot_indicator_results') # Mock the actual plotting function
    def test_generate_plot_success(self, mock_plot_indicator_results, _):
        generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, self.point_size, self.estimated_point)

        mock_plot_indicator_results.assert_called_once()
        call_args, call_kwargs = mock_plot_indicator_results.call_args

        pd.testing.assert_frame_equal(call_args[0], self.result_df) # DataFrame (pos arg 0)
        self.assertEqual(call_args[1], self.selected_rule) # Rule (pos arg 1)
        # Check title construction (pos arg 2)
        # *** FIX: Expect correct precision based on code logic (8 for < 0.001) ***
        expected_title = f"{self.data_info['data_source_label']} | {self.args.interval} | Point: {self.point_size:.8f}"
        self.assertEqual(call_args[2], expected_title)


    # Test plot generation with estimated point size (title should reflect it)
    @patch('src.plotting.plotting_generation.logger', new_callable=MockLogger)
    @patch('src.plotting.plotting_generation.plot_indicator_results')
    def test_generate_plot_estimated_point(self, mock_plot_indicator_results, _):
        estimated_point = True
        point_size_small = 0.00001 # Precision 8
        generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, point_size_small, estimated_point)

        mock_plot_indicator_results.assert_called_once()
        call_args, _ = mock_plot_indicator_results.call_args
        # *** FIX: Expect correct precision based on code logic (8) ***
        expected_title_part = f" | Point: {point_size_small:.8f} (Est.)"
        self.assertIn(expected_title_part, call_args[2])

        # Test with larger point size format
        mock_plot_indicator_results.reset_mock()
        point_size_large = 0.01 # Precision 4
        generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, point_size_large, estimated_point)
        # *** FIX: Expect correct precision based on code logic (4) ***
        expected_title_part_large = f" | Point: {point_size_large:.4f} (Est.)"
        # Check positional argument for title
        self.assertIn(expected_title_part_large, mock_plot_indicator_results.call_args[0][2])


    # Test skipping plot when result_df is None
    @patch('src.plotting.plotting_generation.logger')
    @patch('src.plotting.plotting_generation.plot_indicator_results')
    def test_generate_plot_skip_none_df(self, mock_plot_indicator_results, mock_logger):
        generate_plot(self.args, self.data_info, None, self.selected_rule, self.point_size, self.estimated_point)
        mock_plot_indicator_results.assert_not_called()
        mock_logger.print_info.assert_called_with("Skipping plotting as no valid calculation results are available.")

    # Test skipping plot when result_df is empty
    @patch('src.plotting.plotting_generation.logger')
    @patch('src.plotting.plotting_generation.plot_indicator_results')
    def test_generate_plot_skip_empty_df(self, mock_plot_indicator_results, mock_logger):
        empty_df = pd.DataFrame()
        generate_plot(self.args, self.data_info, empty_df, self.selected_rule, self.point_size, self.estimated_point)
        mock_plot_indicator_results.assert_not_called()
        mock_logger.print_info.assert_called_with("Skipping plotting as no valid calculation results are available.")

    # Test when selected_rule is None
    @patch('src.plotting.plotting_generation.logger')
    @patch('src.plotting.plotting_generation.plot_indicator_results')
    def test_generate_plot_none_rule(self, mock_plot_indicator_results, mock_logger):
        generate_plot(self.args, self.data_info, self.result_df, None, self.point_size, self.estimated_point)
        mock_plot_indicator_results.assert_not_called()
        mock_logger.print_warning.assert_called_with("No valid rule selected, cannot generate plot accurately.")


    # Test when core plotting function raises an exception
    @patch('src.plotting.plotting_generation.logger')
    @patch('src.plotting.plotting_generation.plot_indicator_results')
    @patch('traceback.format_exc')
    def test_generate_plot_exception_handling(self, mock_traceback, mock_plot_indicator_results, mock_logger):
        error_message = "Core plot failed"
        mock_plot_indicator_results.side_effect = Exception(error_message)
        mock_traceback.return_value = "Traceback details here"

        try:
            generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, self.point_size, self.estimated_point)
        except Exception as e:
            self.fail(f"generate_plot raised an exception unexpectedly: {e}")

        mock_logger.print_error.assert_called_once()
        # *** FIX: Expect exception type AND message in the logged string ***
        expected_log_message = f"An error occurred during plotting: Exception: {error_message}"
        actual_call_args = mock_logger.print_error.call_args[0]
        # Use assertIn to be less brittle about exact surrounding text
        self.assertIn(expected_log_message, actual_call_args[0])
        mock_traceback.assert_called_once()


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()