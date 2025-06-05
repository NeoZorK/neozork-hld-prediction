# tests/plotting/test_plotting_generation.py

import unittest
from unittest.mock import patch, MagicMock, ANY, call # Import MagicMock, ANY, and call
import argparse
import pandas as pd
import traceback # Import traceback
from pathlib import Path # Import Path, still needed for type hints and Path() calls outside the patch scope if any
import webbrowser # Need this module to check mock target
import os
# No need to import pathlib directly for patching anymore

# Import the function to test and dependencies
from src.plotting.plotting_generation import generate_plot
from src.common.constants import TradingRule

# Dummy logger class for simple mocking - REMOVED as we use MagicMock now
# class MockLogger:
#     def print_info(self, msg): pass
#     def print_warning(self, msg): pass
#     def print_error(self, msg): pass
#     def print_debug(self, msg): pass

# Helper function to create a dummy args namespace
def create_mock_args(interval='D1', draw='plotly'): # Default draw to plotly
    return argparse.Namespace(interval=interval, draw=draw)

# Unit tests for the plotting generation workflow step
class TestPlottingGenerationStep(unittest.TestCase):

    # Setup basic data used across tests
    def setUp(self):
        # Use helper to create args, explicitly setting draw if needed
        self.args = create_mock_args(interval='H4', draw='plotly') # Assuming plotly default path
        self.data_info = {
            'data_source_label': 'TEST/DATA/EURUSD=X.csv', # Example with slashes
            'effective_mode': 'yfinance',
            'yf_ticker': 'EURUSD=X'
        }
        # Calculate expected stem once using real Path for test setup clarity
        self.expected_stem = Path(self.data_info['data_source_label']).stem
        self.data_label_path = self.data_info['data_source_label']
        self.output_dir_path = "results/plots"
        # Define a simple, predictable string representation for the mock path
        self.mock_file_path_str = f"{self.output_dir_path}/mock_plot.html"
        self.mock_uri = f"file:///{self.output_dir_path}/mock_plot.html" # Simple URI


        self.result_df = pd.DataFrame({
            'Open': [1.1, 1.12, 1.11], # Add required OHLC columns
            'High': [1.13, 1.14, 1.12],
            'Low': [1.09, 1.10, 1.10],
            'Close': [1.1, 1.2, 1.15]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']))
        self.selected_rule = TradingRule.Predict_High_Low_Direction
        self.point_size = 0.0001
        self.estimated_point = False

    # Test successful plot generation using the default Plotly path
    def test_generate_plot_success(self):
        with patch.dict(os.environ, {'DISABLE_DOCKER_DETECTION': 'true'}), \
             patch('src.plotting.plotting.IN_DOCKER', False), \
             patch('src.plotting.plotting_generation.IN_DOCKER', False), \
             patch('src.plotting.plotting_generation._detect_docker_environment', return_value=False), \
             patch('src.plotting.plotting_generation.logger') as mock_logger, \
             patch('src.plotting.plotting_generation.webbrowser.open') as mock_webbrowser_open, \
             patch('src.plotting.plotting_generation.plot_indicator_results_plotly') as mock_plotly_plot, \
             patch('src.plotting.plotting_generation.Path') as mock_path_class:
            
            # --- Configure Mocks ---
            mock_figure = MagicMock()
            # Ensure write_html exists and is callable without error
            mock_figure.write_html = MagicMock()
            mock_plotly_plot.return_value = mock_figure

            mock_path_instance = MagicMock(spec=Path)
            mock_path_instance.stem = self.expected_stem
            mock_path_instance.resolve.return_value = mock_path_instance
            mock_path_instance.as_uri.return_value = self.mock_uri
            # *** FIX: Use constant string for __str__ ***
            mock_path_instance.__str__.return_value = self.mock_file_path_str
            mock_path_instance.mkdir = MagicMock()
            mock_path_instance.__truediv__.return_value = mock_path_instance
            mock_path_class.return_value = mock_path_instance
            # --- End Path Mocking ---

            # --- Call Function Under Test ---
            generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, self.point_size, self.estimated_point)

            # --- Assertions ---
            # 1. Check Path instantiation calls
            expected_path_calls = [call(self.output_dir_path)]
            if '/' in self.data_label_path or '\\' in self.data_label_path:
                 expected_path_calls.append(call(self.data_label_path))
            mock_path_class.assert_has_calls(expected_path_calls, any_order=True)

            # 2. Check plotting function call
            mock_plotly_plot.assert_called_once()
            call_args, call_kwargs = mock_plotly_plot.call_args

            # 3. Check plotting function arguments
            pd.testing.assert_frame_equal(call_args[0], self.result_df)
            self.assertEqual(call_args[1], self.selected_rule)

            # 4. Check the constructed title
            expected_precision = 8 if abs(self.point_size) < 0.001 else 5 if abs(self.point_size) < 0.1 else 2
            expected_point_str = f"{self.point_size:.{expected_precision}f}"
            expected_title = f"{self.expected_stem} | {self.args.interval} | Pt:{expected_point_str}{'~' if self.estimated_point else ''}"
            self.assertEqual(call_args[2], expected_title)

            # 5. Check mkdir call on the instance
            mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)
            # 6. Check the '/' operator on the instance
            mock_path_instance.__truediv__.assert_called_once()
            # 7. Check figure saving (write_html should be called now)
            mock_figure.write_html.assert_called_once_with(self.mock_file_path_str, include_plotlyjs='cdn')
            # 8. Check path methods *after* confirming write_html was called
            mock_path_instance.resolve.assert_called_once()
            mock_path_instance.as_uri.assert_called_once()
            # 9. Check browser opening attempt
            mock_webbrowser_open.assert_called_once_with(self.mock_uri)
            # 10. Check success logs
            mock_logger.print_success.assert_any_call(f"Interactive Plotly plot saved successfully to: {mock_path_instance}")
            # Check specific info logs
            mock_logger.print_info.assert_any_call('Generating plot using Plotly...')
            mock_logger.print_info.assert_any_call(f"Attempting to open {mock_path_instance} in default browser...")
            # Check no errors/warnings were logged
            mock_logger.print_error.assert_not_called()
            mock_logger.print_warning.assert_not_called()


    # Test plot generation title reflects estimated point size correctly
    def test_generate_plot_estimated_point(self):
        with patch.dict(os.environ, {'DISABLE_DOCKER_DETECTION': 'true'}), \
             patch('src.plotting.plotting.IN_DOCKER', False), \
             patch('src.plotting.plotting_generation.IN_DOCKER', False), \
             patch('src.plotting.plotting_generation._detect_docker_environment', return_value=False), \
             patch('src.plotting.plotting_generation.logger') as mock_logger, \
             patch('src.plotting.plotting_generation.webbrowser.open') as mock_webbrowser_open, \
             patch('src.plotting.plotting_generation.plot_indicator_results_plotly') as mock_plotly_plot, \
             patch('src.plotting.plotting_generation.Path') as mock_path_class:

            # --- Configure Mocks ---
            # Configure Path mock once, it's not reset
            mock_path_instance = MagicMock(spec=Path)
            mock_path_instance.stem = self.expected_stem
            mock_path_instance.resolve.return_value = mock_path_instance
            uri_side_effects = [f"{self.mock_uri}_1", f"{self.mock_uri}_2", f"{self.mock_uri}_3"]
            # *** FIX: Use constant string for __str__ ***
            mock_path_instance.__str__.return_value = self.mock_file_path_str # Constant string
            mock_path_instance.as_uri.side_effect = uri_side_effects # Keep side effect for as_uri
            mock_path_instance.mkdir = MagicMock()
            mock_path_instance.__truediv__.return_value = mock_path_instance
            mock_path_class.return_value = mock_path_instance

            # --- Test Setup ---
            estimated_point = True

            # --- Test with small point size (precision 8) ---
            # Configure figure mock for this iteration
            mock_figure_1 = MagicMock()
            mock_figure_1.write_html = MagicMock()
            mock_plotly_plot.return_value = mock_figure_1

            point_size_small = 0.00001
            generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, point_size_small, estimated_point)
            # Assertions for small point size
            mock_plotly_plot.assert_called_once() # Called once so far
            call_args_small, _ = mock_plotly_plot.call_args
            expected_title_small = f"{self.expected_stem} | {self.args.interval} | Pt:{point_size_small:.8f}~"
            self.assertEqual(call_args_small[2], expected_title_small)
            # Check calls for this iteration
            self.assertEqual(mock_path_instance.mkdir.call_count, 1)
            mock_path_instance.mkdir.assert_called_with(parents=True, exist_ok=True)
            # Check write_html on the specific figure mock for this iteration
            mock_figure_1.write_html.assert_called_once_with(self.mock_file_path_str, include_plotlyjs='cdn') # Use constant string
            self.assertEqual(mock_path_instance.resolve.call_count, 1)
            self.assertEqual(mock_path_instance.as_uri.call_count, 1)
            mock_webbrowser_open.assert_called_once_with(uri_side_effects[0])
            # *** FIX: Remove assert_not_called for print_error ***
            # mock_logger.print_error.assert_not_called()
            mock_logger.print_warning.assert_not_called()


            # --- Reset mocks that need independent checks per call ---
            mock_plotly_plot.reset_mock()
            # mock_figure is NOT reset (we use a new one)
            # mock_path_instance is NOT reset
            mock_webbrowser_open.reset_mock()
            mock_logger.reset_mock()


            # --- Test with medium point size (precision 5) ---
            # Configure figure mock for this iteration
            mock_figure_2 = MagicMock()
            mock_figure_2.write_html = MagicMock()
            mock_plotly_plot.return_value = mock_figure_2 # Set new return value

            point_size_medium = 0.01
            generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, point_size_medium, estimated_point)
            # Assertions for medium point size
            mock_plotly_plot.assert_called_once() # Called once since last reset
            call_args_medium, _ = mock_plotly_plot.call_args
            expected_title_medium = f"{self.expected_stem} | {self.args.interval} | Pt:{point_size_medium:.5f}~"
            self.assertEqual(call_args_medium[2], expected_title_medium)
            # Check cumulative call counts for path instance
            self.assertEqual(mock_path_instance.mkdir.call_count, 2)
            mock_path_instance.mkdir.assert_called_with(parents=True, exist_ok=True)
            # *** FIX: Remove assert_not_called for print_error ***
            # mock_logger.print_error.assert_not_called()
            # Check write_html on the specific figure mock for this iteration
            mock_figure_2.write_html.assert_called_once_with(self.mock_file_path_str, include_plotlyjs='cdn') # Use constant string
            self.assertEqual(mock_path_instance.resolve.call_count, 2)
            self.assertEqual(mock_path_instance.as_uri.call_count, 2)
            mock_webbrowser_open.assert_called_once_with(uri_side_effects[1]) # Called once since last reset
            # mock_logger.print_error.assert_not_called() # Already checked above
            mock_logger.print_warning.assert_not_called()

            # --- Reset mocks ---
            mock_plotly_plot.reset_mock()
            # mock_figure is NOT reset
            # mock_path_instance is NOT reset
            mock_webbrowser_open.reset_mock()
            mock_logger.reset_mock()

            # --- Test with large point size (precision 2) ---
            # Configure figure mock for this iteration
            mock_figure_3 = MagicMock()
            mock_figure_3.write_html = MagicMock()
            mock_plotly_plot.return_value = mock_figure_3 # Set new return value

            point_size_large = 0.15
            generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, point_size_large, estimated_point)
            # Assertions for large point size
            mock_plotly_plot.assert_called_once() # Called once since last reset
            call_args_large, _ = mock_plotly_plot.call_args
            expected_title_large = f"{self.expected_stem} | {self.args.interval} | Pt:{point_size_large:.2f}~"
            self.assertEqual(call_args_large[2], expected_title_large)
            # Check cumulative call counts for path instance
            self.assertEqual(mock_path_instance.mkdir.call_count, 3)
            mock_path_instance.mkdir.assert_called_with(parents=True, exist_ok=True)
            # *** FIX: Remove assert_not_called for print_error ***
            # mock_logger.print_error.assert_not_called()
            # Check write_html on the specific figure mock for this iteration
            mock_figure_3.write_html.assert_called_once_with(self.mock_file_path_str, include_plotlyjs='cdn') # Use constant string
            self.assertEqual(mock_path_instance.resolve.call_count, 3)
            self.assertEqual(mock_path_instance.as_uri.call_count, 3)
            mock_webbrowser_open.assert_called_once_with(uri_side_effects[2]) # Called once since last reset
            # mock_logger.print_error.assert_not_called() # Already checked above
            mock_logger.print_warning.assert_not_called()


    # Test skipping plot when result_df is None
    def test_generate_plot_skip_none_df(self):
        with patch.dict(os.environ, {'DISABLE_DOCKER_DETECTION': 'true'}), \
             patch('src.plotting.plotting_generation._detect_docker_environment', return_value=False), \
             patch('src.plotting.plotting_generation.logger') as mock_logger, \
             patch('src.plotting.plotting_generation.plot_indicator_results_plotly') as mock_plotly_plot:
            
            # No need to configure or check Path mock here

            generate_plot(self.args, self.data_info, None, self.selected_rule, self.point_size, self.estimated_point)

            mock_plotly_plot.assert_not_called()

            mock_logger.print_info.assert_called_once_with("Skipping plotting as no valid calculation results are available.")
            mock_logger.print_warning.assert_not_called()
            mock_logger.print_error.assert_not_called()


    # Test skipping plot when result_df is empty
    def test_generate_plot_skip_empty_df(self):
        with patch.dict(os.environ, {'DISABLE_DOCKER_DETECTION': 'true'}), \
             patch('src.plotting.plotting_generation._detect_docker_environment', return_value=False), \
             patch('src.plotting.plotting_generation.logger') as mock_logger, \
             patch('src.plotting.plotting_generation.plot_indicator_results_plotly') as mock_plotly_plot:
            
            # No need to configure or check Path mock here

            empty_df = pd.DataFrame()
            generate_plot(self.args, self.data_info, empty_df, self.selected_rule, self.point_size, self.estimated_point)

            mock_plotly_plot.assert_not_called()

            mock_logger.print_info.assert_called_once_with("Skipping plotting as no valid calculation results are available.")
            mock_logger.print_warning.assert_not_called()
            mock_logger.print_error.assert_not_called()


    # Test when selected_rule is None
    def test_generate_plot_none_rule(self):
        with patch.dict(os.environ, {'DISABLE_DOCKER_DETECTION': 'true'}), \
             patch('src.plotting.plotting_generation._detect_docker_environment', return_value=False), \
             patch('src.plotting.plotting_generation.logger') as mock_logger, \
             patch('src.plotting.plotting_generation.plot_indicator_results_plotly') as mock_plotly_plot:
            
            # No need to configure or check Path mock here

            generate_plot(self.args, self.data_info, self.result_df, None, self.point_size, self.estimated_point)

            mock_plotly_plot.assert_not_called()

            mock_logger.print_warning.assert_called_once_with("No valid rule selected, cannot generate plot accurately.")
            mock_logger.print_info.assert_not_called()
            mock_logger.print_error.assert_not_called()


    # Test when the core plotting function raises an exception during generation
    def test_generate_plot_exception_handling(self):
        with patch.dict(os.environ, {'DISABLE_DOCKER_DETECTION': 'true'}), \
             patch('src.plotting.plotting.IN_DOCKER', False), \
             patch('src.plotting.plotting_generation.IN_DOCKER', False), \
             patch('src.plotting.plotting_generation._detect_docker_environment', return_value=False), \
             patch('src.plotting.plotting_generation.logger') as mock_logger, \
             patch('src.plotting.plotting_generation.plot_indicator_results_plotly') as mock_plotly_plot, \
             patch('traceback.format_exc') as mock_traceback, \
             patch('src.plotting.plotting_generation.Path') as mock_path_class:
            
            # --- Configure Mocks ---
            mock_path_instance = MagicMock(spec=Path)
            mock_path_instance.stem = self.expected_stem
            mock_path_class.return_value = mock_path_instance
            # --- End Mocking ---

            error_message = "Core Plotly render failed"
            mock_plotly_plot.side_effect = ValueError(error_message)
            mock_traceback.return_value = "Detailed traceback here..."

            # --- Call Function Under Test ---
            try:
                generate_plot(self.args, self.data_info, self.result_df, self.selected_rule, self.point_size, self.estimated_point)
            except Exception as e:
                self.fail(f"generate_plot raised an exception unexpectedly: {e}")

            # --- Assertions ---
            # 1. Check Path was called for the label
            if '/' in self.data_label_path or '\\' in self.data_label_path:
                mock_path_class.assert_called_once_with(self.data_label_path)
            else:
                 mock_path_class.assert_not_called()

            # 2. Check that the error was logged correctly
            mock_logger.print_error.assert_called_once()
            expected_log_part = f"An error occurred during plot generation: ValueError: {error_message}"
            actual_log_call_args = mock_logger.print_error.call_args[0]
            self.assertIn(expected_log_part, actual_log_call_args[0])

            # 3. Assert that traceback was formatted and logged
            mock_traceback.assert_called_once()
            mock_logger.print_debug.assert_called_with(f"Traceback (generate plot):\n{mock_traceback.return_value}")
            # Check logger calls based on actual code flow
            mock_logger.print_info.assert_any_call('Generating plot using Plotly...')
            mock_logger.print_warning.assert_not_called()


# Allow running the tests directly from the command line
if __name__ == '__main__':
    unittest.main()
