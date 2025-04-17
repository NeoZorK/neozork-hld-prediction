# tests/plotting/test_plotting_generation.py

import unittest
from unittest.mock import patch, MagicMock
import argparse
import pandas as pd

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
    def test_generate_plot_success(self, mock_plot_indicator_results, mock_logger):
        generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, self.point_size, self.estimated_point)

        # Check if the core plotting function was called
        mock_plot_indicator_results.assert_called_once()
        call_args, call_kwargs = mock_plot_indicator_results.call_args

        # Check the arguments passed to the core plotting function
        pd.testing.assert_frame_equal(call_args[0], self.result_df) # DataFrame
        self.assertEqual(call_args[1], self.selected_rule) # Rule
        # Check title construction
        expected_title = f"{self.data_info['data_source_label']} | {self.args.interval} | Rule: {self.selected_rule.name}"
        self.assertEqual(call_kwargs['title'], expected_title)

    # Test plot generation with estimated point size (title should reflect it)
    @patch('src.plotting.plotting_generation.logger', new_callable=MockLogger)
    @patch('src.plotting.plotting_generation.plot_indicator_results')
    def test_generate_plot_estimated_point(self, mock_plot_indicator_results, mock_logger):
        estimated_point = True
        point_size_small = 0.00001 # Should use .8f format
        generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, point_size_small, estimated_point)

        mock_plot_indicator_results.assert_called_once()
        call_kwargs = mock_plot_indicator_results.call_args[1]
        # Check title includes estimated point size formatted correctly
        expected_title_part = f" | Est. Point: {point_size_small:.8f}"
        self.assertIn(expected_title_part, call_kwargs['title'])

        # Test with larger point size format
        mock_plot_indicator_results.reset_mock()
        point_size_large = 0.01 # Should use .2f format
        generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, point_size_large, estimated_point)
        expected_title_part_large = f" | Est. Point: {point_size_large:.2f}"
        self.assertIn(expected_title_part_large, mock_plot_indicator_results.call_args[1]['title'])


    # Test skipping plot when result_df is None
    @patch('src.plotting.plotting_generation.logger') # Use MagicMock logger
    @patch('src.plotting.plotting_generation.plot_indicator_results')
    def test_generate_plot_skip_none_df(self, mock_plot_indicator_results, mock_logger_instance):
        generate_plot(self.args, self.data_info, None, self.selected_rule, self.point_size, self.estimated_point)

        # Check plotting function was NOT called
        mock_plot_indicator_results.assert_not_called()
        # Check info message was logged
        mock_logger_instance.print_info.assert_called_with("Skipping plotting as no valid calculation results are available.")

    # Test skipping plot when result_df is empty
    @patch('src.plotting.plotting_generation.logger')
    @patch('src.plotting.plotting_generation.plot_indicator_results')
    def test_generate_plot_skip_empty_df(self, mock_plot_indicator_results, mock_logger_instance):
        empty_df = pd.DataFrame()
        generate_plot(self.args, self.data_info, empty_df, self.selected_rule, self.point_size, self.estimated_point)

        # Check plotting function was NOT called
        mock_plot_indicator_results.assert_not_called()
        # Check info message was logged
        mock_logger_instance.print_info.assert_called_with("Skipping plotting as no valid calculation results are available.")

    # Test when selected_rule is None (should log warning and skip plotting)
    @patch('src.plotting.plotting_generation.logger')
    @patch('src.plotting.plotting_generation.plot_indicator_results')
    def test_generate_plot_none_rule(self, mock_plot_indicator_results, mock_logger_instance):
        generate_plot(self.args, self.data_info, self.result_df, None, self.point_size, self.estimated_point)

        # Check plotting function was NOT called
        mock_plot_indicator_results.assert_not_called()
        # Check warning message was logged
        mock_logger_instance.print_warning.assert_called_with("No valid rule selected, cannot generate plot accurately.")


    # Test when core plotting function raises an exception
    @patch('src.plotting.plotting_generation.logger')
    @patch('src.plotting.plotting_generation.plot_indicator_results')
    @patch('traceback.format_exc') # Mock traceback printing
    def test_generate_plot_exception_handling(self, mock_traceback, mock_plot_indicator_results, mock_logger_instance):
        error_message = "Core plot failed"
        mock_plot_indicator_results.side_effect = Exception(error_message)
        mock_traceback.return_value = "Traceback details here" # Mock traceback output

        # The function should catch the exception, log it, and not re-raise
        try:
            generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, self.point_size, self.estimated_point)
        except Exception as e:
            self.fail(f"generate_plot raised an exception unexpectedly: {e}")

        # Check error was logged
        mock_logger_instance.print_error.assert_called_once()
        self.assertIn(f"An error occurred during plotting:{error_message}", mock_logger_instance.print_error.call_args[0][0])
        # Check traceback was printed (or attempted to be printed via format_exc)
        mock_traceback.assert_called_once()


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()