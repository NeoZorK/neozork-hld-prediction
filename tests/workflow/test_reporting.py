# tests/workflow/test_reporting.py

"""
Unit tests for the reporting module functions.
All comments are in English.
"""

import unittest
from unittest.mock import patch, MagicMock, call # Import call

# Adjust the import path based on the project structure
from src.workflow.reporting import print_summary

# Definition of the TestReporting class
class TestReporting(unittest.TestCase):
    """
    Test suite for the print_summary function.
    """

    # --- Helper to create mock args ---
    def create_mock_args(self, mode='demo', rule='Predict_High_Low_Direction', **kwargs):
        """ Creates a mock args object for testing print_summary. """
        args = MagicMock()
        args.mode = mode
        args.rule = rule
        # Add other args potentially used by print_summary if any
        args.__dict__.update(kwargs)
        return args

    # --- Helper to create a base results dict ---
    def create_base_results(self, effective_mode, success=True):
         """ Creates a base results dictionary for testing print_summary. """
         return {
             "success": success,
             "effective_mode": effective_mode,
             "data_source_label": f"Source_{effective_mode}",
             "yf_ticker": "MOCK_YF" if effective_mode == 'yfinance' else None,
             "yf_interval": "1d_map" if effective_mode == 'yfinance' else None,
             "current_start": "2023-01-01",
             "current_end": "2023-01-05",
             "current_period": None,
             "point_size": 0.01,
             "estimated_point": False,
             "data_size_mb": 1.234,
             "data_size_bytes": 1234 * 1024 * 1024,
             "rows_count": 100,
             "columns_count": 6,
             "file_size_bytes": None, # Default to None
             "api_latency_sec": None, # Default to None
             "parquet_save_path": None, # Default to None
             "data_fetch_duration": 0.5,
             "calc_duration": 0.2,
             "plot_duration": 0.3,
             "error_message": "Sample Error" if not success else None,
         }

    # Patch the logger used within reporting module
    @patch('src.workflow.reporting.logger')
    def test_print_summary_csv_success(self, mock_logger):
        """ Test print_summary output for a successful CSV run. """
        args = self.create_mock_args(mode='csv')
        results = self.create_base_results('csv')
        # Add CSV specific metrics
        results['file_size_bytes'] = 20480 # 20 KB example
        results['data_source_label'] = 'path/to/my.csv'

        print_summary(results, 1.0, args) # total_duration = 1.0

        # Get all arguments passed to print_info
        call_args_list = [c.args[0] for c in mock_logger.print_info.call_args_list if c.args]
        full_output = "\n".join(call_args_list)
        # print(f"\n--- CSV Output ---:\n{full_output}\n------------") # For debugging test

        # Check for specific lines containing new metrics
        self.assertTrue(any("Data Source:" in line and "path/to/my.csv" in line for line in call_args_list))
        self.assertTrue(any("Input File Size:" in line and "0.020 MB" in line and "20,480 bytes" in line for line in call_args_list))
        self.assertTrue(any("DataFrame Shape:" in line and "100 rows, 6 columns" in line for line in call_args_list))
        self.assertTrue(any("Memory Usage:" in line and "1.234 MB" in line for line in call_args_list))
        # Check that API specific lines are NOT present
        self.assertFalse(any("Latency:" in line for line in call_args_list))
        self.assertFalse(any("Saved Raw Data:" in line for line in call_args_list))
        # Check total time
        self.assertTrue(any("Total Execution Time:" in line and "1.000 seconds" in line for line in call_args_list))
        # Check no error printed by logger
        mock_logger.print_error.assert_not_called()

    @patch('src.workflow.reporting.logger')
    def test_print_summary_yfinance_success_saved(self, mock_logger):
        """ Test print_summary output for a successful YFinance run with parquet save. """
        args = self.create_mock_args(mode='yfinance', interval='H4') # Match interval for label
        results = self.create_base_results('yfinance')
        # Add API specific metrics
        results['api_latency_sec'] = 1.456
        results['parquet_save_path'] = 'data/raw_parquet/yfinance_MOCK_YF_1d_map_2023-01-01_2023-01-05.parquet'
        results['yf_interval'] = "4h" # Set mapped interval used in output

        print_summary(results, 2.0, args)

        call_args_list = [c.args[0] for c in mock_logger.print_info.call_args_list if c.args]
        # print(f"\n--- YF Output ---:\n{'\n'.join(call_args_list)}\n------------") # Debugging

        self.assertTrue(any("Data Source:" in line and "Source_yfinance" in line for line in call_args_list))
        # Check yfinance specific info
        self.assertTrue(any("Ticker:" in line and "MOCK_YF" in line for line in call_args_list))
        self.assertTrue(any("Interval Requested:" in line and "H4 (mapped to 4h)" in line for line in call_args_list))
        # Check standard metrics
        self.assertTrue(any("DataFrame Shape:" in line and "100 rows, 6 columns" in line for line in call_args_list))
        self.assertTrue(any("Memory Usage:" in line and "1.234 MB" in line for line in call_args_list))
        # Check API specific metrics
        self.assertTrue(any("yf.download Latency:" in line and "1.456 seconds" in line for line in call_args_list))
        self.assertTrue(any("Saved Raw Data:" in line and results['parquet_save_path'] in line for line in call_args_list))
        # Check that CSV specific lines are NOT present
        self.assertFalse(any("Input File Size:" in line for line in call_args_list))
        # Check total time
        self.assertTrue(any("Total Execution Time:" in line and "2.000 seconds" in line for line in call_args_list))
        mock_logger.print_error.assert_not_called()

    @patch('src.workflow.reporting.logger')
    def test_print_summary_polygon_success_no_save(self, mock_logger):
        """ Test print_summary output for a successful Polygon run where parquet save failed. """
        args = self.create_mock_args(mode='polygon')
        results = self.create_base_results('polygon')
        # Add API specific metrics, but parquet path is None
        results['api_latency_sec'] = 5.8
        results['parquet_save_path'] = None

        print_summary(results, 7.0, args)

        call_args_list = [c.args[0] for c in mock_logger.print_info.call_args_list if c.args]

        self.assertTrue(any("API Chunks Total Latency:" in line and "5.800 seconds" in line for line in call_args_list))
        # Check that parquet path line is NOT present
        self.assertFalse(any("Saved Raw Data:" in line for line in call_args_list))
        # Check other standard lines are present
        self.assertTrue(any("DataFrame Shape:" in line for line in call_args_list))
        self.assertTrue(any("Total Execution Time:" in line and "7.000 seconds" in line for line in call_args_list))
        mock_logger.print_error.assert_not_called()

    @patch('src.workflow.reporting.logger')
    def test_print_summary_failure(self, mock_logger):
        """ Test print_summary output when workflow failed. """
        args = self.create_mock_args(mode='binance')
        # Simulate failure, some metrics might still be populated before failure
        results = self.create_base_results('binance', success=False)
        results['rows_count'] = 0
        results['columns_count'] = 0
        results['data_size_mb'] = 0.0
        results['data_size_bytes'] = 0
        results['api_latency_sec'] = 0.1 # Latency might exist if fetch started
        results['error_message'] = "API Key Invalid"

        print_summary(results, 0.2, args)

        call_args_list_info = [c.args[0] for c in mock_logger.print_info.call_args_list if c.args]
        call_args_list_error = [c.args[0] for c in mock_logger.print_error.call_args_list if c.args]

        # Check that essential info is still printed
        self.assertTrue(any("Data Source:" in line for line in call_args_list_info))
        self.assertTrue(any("Rule Applied:" in line for line in call_args_list_info))
        # Check metrics that might have values are printed
        self.assertTrue(any("Memory Usage:" in line and "0.000 MB" in line for line in call_args_list_info))
        self.assertTrue(any("API Chunks Total Latency:" in line and "0.100 seconds" in line for line in call_args_list_info))
        # Check things that shouldn't be present
        self.assertFalse(any("DataFrame Shape:" in line and "rows" in line for line in call_args_list_info)) # Shape is 0x0
        self.assertFalse(any("Saved Raw Data:" in line for line in call_args_list_info))

        # Check that the final error message *is* printed by logger.print_error
        self.assertTrue(any("Workflow failed: API Key Invalid" in line for line in call_args_list_error))


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()