# tests/workflow/test_reporting.py

import unittest
from unittest.mock import patch, MagicMock
import datetime
import argparse # Import argparse to simulate Namespace

from src.workflow.reporting import print_summary
from src.common.constants import TradingRule # Make sure TradingRule is imported

# Sample results dictionary structure for testing
MOCK_BASE_RESULTS = {
    "status": "Success",
    "mode": "demo",
    "ticker": "DemoTicker",
    "interval": "D1",
    "rule": TradingRule.Pressure_Vector, # Valid member
    "point_size": 0.0001,
    "estimated_point": True,
    "csv_file_path": None,
    "total_duration_sec": 10.5,
    "steps_duration": {"acquire": 2.1, "point_size": 0.2, "calculate": 5.0, "plot": 3.2},
    "data_metrics": {"rows": 100, "cols": 6, "memory_mb": 0.1, "start": "2023-01-01", "end": "2023-04-10"},
    "validation_metrics": None,
    "plot_file_path": "/path/to/plot.png",
    "parquet_file_path": "/path/to/data.parquet",
    "api_latency_sec": 1.5,
    "api_calls": 5,
    "successful_chunks": 5,
    "error_message": None,
    "error_traceback": None
}

class TestReporting(unittest.TestCase):

    # Helper to extract log messages
    def _extract_log_args(self, mock_logger):
        """Extracts the first string argument from mock logger calls."""
        log_args = []
        for call_item in mock_logger.call_args_list:
            if call_item.args: # Check if there are positional arguments
                log_args.append(str(call_item.args[0]))
        return log_args

    # Helper to create mock args based on results
    def _create_mock_args(self, results):
         # Simulates the args namespace needed by print_summary
         mock_args = argparse.Namespace()
         mock_args.mode = results.get("mode")
         mock_args.ticker = results.get("ticker")
         mock_args.interval = results.get("interval")
         mock_args.rule = results.get("rule").name # Pass rule name string if needed, or enum itself
         mock_args.csv_file = results.get("csv_file_path")
         # Add other args if print_summary uses them
         return mock_args

    @patch('src.common.logger.print_error')
    @patch('src.common.logger.print_info')
    def test_print_summary_csv_success(self, mock_print_info, mock_print_error):
        """Test print_summary output for a successful CSV run."""
        mock_results = MOCK_BASE_RESULTS.copy()
        mock_results.update({
            "mode": "csv",
            "ticker": None, # Usually None for CSV
            "interval": "H1",
            "rule": TradingRule.Predict_High_Low_Direction, # Overrides base rule for this specific test
            "point_size": 0.01,
            "estimated_point": False,
            "csv_file_path": "data/test.csv",
            "total_duration_sec": 5.123,
            "steps_duration": {"acquire": 1.2, "point_size": 0.1, "calculate": 2.5, "plot": 1.323},
            "data_metrics": {"rows": 1000, "cols": 15, "memory_mb": 1.5, "start": "2023-01-01", "end": "2023-01-10"},
            "validation_metrics": {"pressure_match": 0.99, "pv_match": 0.98, "phl_match": 0.75, "rows_compared": 998},
            "plot_file_path": "plots/plot_test_h1.png",
            "parquet_file_path": None, # No parquet for CSV mode typically
            "api_latency_sec": None,
            "api_calls": None,
            "successful_chunks": None,
        })
        # Create mock args
        mock_args = self._create_mock_args(mock_results)

        # FIX: Call print_summary with all required arguments
        print_summary(mock_results, mock_results['total_duration_sec'], mock_args)

        # Extract log arguments
        call_args_list_info = self._extract_log_args(mock_print_info)
        call_args_list_error = self._extract_log_args(mock_print_error)

        # --- Assertions (remain the same) ---
        self.assertTrue(any("--- Run Summary ---" in line for line in call_args_list_info))
        self.assertTrue(any("Status: Success" in line for line in call_args_list_info))
        self.assertTrue(any("Mode: csv" in line for line in call_args_list_info))
        self.assertTrue(any("CSV File: data/test.csv" in line for line in call_args_list_info))
        self.assertTrue(any("Interval: H1" in line for line in call_args_list_info))
        self.assertTrue(any("Trading Rule: Predict_High_Low_Direction" in line for line in call_args_list_info))
        self.assertTrue(any("Point Size: 0.01" in line for line in call_args_list_info))
        self.assertTrue(any("Data Rows: 1000" in line for line in call_args_list_info))
        self.assertTrue(any("Validation Pressure Match:" in line and "99.00%" in line for line in call_args_list_info))
        self.assertTrue(any("Validation PV Match:" in line and "98.00%" in line for line in call_args_list_info))
        self.assertTrue(any("Validation PHL Match:" in line and "75.00%" in line for line in call_args_list_info))
        self.assertTrue(any("Plot saved to:" in line and "plots/plot_test_h1.png" in line for line in call_args_list_info))
        self.assertFalse(any("Raw data saved to:" in line for line in call_args_list_info)) # No parquet expected
        self.assertFalse(any("API" in line for line in call_args_list_info)) # No API metrics expected

        # Assert that print_error was NOT called
        mock_print_error.assert_not_called()
        self.assertEqual(len(call_args_list_error), 0)

    @patch('src.common.logger.print_error')
    @patch('src.common.logger.print_info')
    def test_print_summary_yfinance_success_saved(self, mock_print_info, mock_print_error):
        """Test print_summary output for a successful YFinance run with parquet save."""
        mock_results = MOCK_BASE_RESULTS.copy()
        mock_results.update({
            "mode": "yfinance",
            "ticker": "AAPL",
            "interval": "1d",
            "rule": TradingRule.Pressure_Vector, # Uses base rule Pressure_Vector now
            "parquet_file_path": "data/raw_parquet/yfinance_AAPL_1d.parquet",
            "api_latency_sec": 0.85,
            "api_calls": 1,
             "successful_chunks": 1,
             "validation_metrics": None, # No validation for API modes usually
             "plot_file_path": "plots/yfinance_AAPL_1d_plot.png",
             "total_duration_sec": 9.876, # Give a specific duration
        })
        mock_results["data_metrics"]["source"] = "Source_yfinance" # Add source for API modes
        # Create mock args
        mock_args = self._create_mock_args(mock_results)

        # FIX: Call print_summary with all required arguments
        print_summary(mock_results, mock_results['total_duration_sec'], mock_args)

        # Extract log arguments
        call_args_list_info = self._extract_log_args(mock_print_info)
        call_args_list_error = self._extract_log_args(mock_print_error)

        # --- Assertions (remain the same) ---
        self.assertTrue(any("--- Run Summary ---" in line for line in call_args_list_info))
        self.assertTrue(any("Status: Success" in line for line in call_args_list_info))
        self.assertTrue(any("Mode: yfinance" in line for line in call_args_list_info))
        self.assertTrue(any("Ticker: AAPL" in line for line in call_args_list_info))
        self.assertTrue(any("Interval: 1d" in line for line in call_args_list_info))
        self.assertTrue(any("Trading Rule: Pressure_Vector" in line for line in call_args_list_info))
        self.assertTrue(any("Point Size: 0.0001 (Estimated)" in line for line in call_args_list_info))
        self.assertTrue(any("Data Source: Source_yfinance" in line for line in call_args_list_info)) # Check source added
        self.assertTrue(any("API Call Latency:" in line and "0.850 seconds" in line for line in call_args_list_info))
        self.assertTrue(any("API Calls Made: 1" in line for line in call_args_list_info))
        self.assertFalse(any("Validation" in line for line in call_args_list_info)) # No validation expected
        self.assertTrue(any("Plot saved to:" in line and "plots/yfinance_AAPL_1d_plot.png" in line for line in call_args_list_info))
        self.assertTrue(any("Raw data saved to:" in line and "data/raw_parquet/yfinance_AAPL_1d.parquet" in line for line in call_args_list_info))

        # Assert that print_error was NOT called
        mock_print_error.assert_not_called()
        self.assertEqual(len(call_args_list_error), 0)

    @patch('src.common.logger.print_error')
    @patch('src.common.logger.print_info')
    def test_print_summary_polygon_success_no_save(self, mock_print_info, mock_print_error):
        """Test print_summary output for a successful Polygon run where parquet save failed."""
        mock_results = MOCK_BASE_RESULTS.copy()
        mock_results.update({
            "mode": "polygon",
            "ticker": "MSFT",
            "interval": "M1",
            "rule": TradingRule.PV_HighLow, # Overrides base rule
            "parquet_file_path": None, # Simulate parquet save failure
            "api_latency_sec": 5.8,
            "api_calls": 12,
            "successful_chunks": 10, # Example: some chunks might fail but overall success
            "validation_metrics": None,
            "plot_file_path": None, # Simulate plot failure maybe
            "total_duration_sec": 15.2, # Give a specific duration
        })
        mock_results["data_metrics"]["source"] = "Source_polygon"
        # Create mock args
        mock_args = self._create_mock_args(mock_results)

        # FIX: Call print_summary with all required arguments
        print_summary(mock_results, mock_results['total_duration_sec'], mock_args)

        # Extract log arguments
        call_args_list_info = self._extract_log_args(mock_print_info)
        call_args_list_error = self._extract_log_args(mock_print_error)

        # --- Assertions (remain the same) ---
        self.assertTrue(any("--- Run Summary ---" in line for line in call_args_list_info))
        self.assertTrue(any("Status: Success" in line for line in call_args_list_info))
        self.assertTrue(any("Mode: polygon" in line for line in call_args_list_info))
        self.assertTrue(any("Ticker: MSFT" in line for line in call_args_list_info))
        self.assertTrue(any("Interval: M1" in line for line in call_args_list_info))
        self.assertTrue(any("Trading Rule: PV_HighLow" in line for line in call_args_list_info))
        self.assertTrue(any("Point Size: 0.0001 (Estimated)" in line for line in call_args_list_info))
        self.assertTrue(any("Data Source: Source_polygon" in line for line in call_args_list_info))
        self.assertTrue(any("API Chunks Total Latency:" in line and "5.800 seconds" in line for line in call_args_list_info))
        self.assertTrue(any("API Calls Made: 12" in line for line in call_args_list_info))
        self.assertTrue(any("API Chunks Successful: 10" in line for line in call_args_list_info))
        self.assertFalse(any("Validation" in line for line in call_args_list_info))
        self.assertFalse(any("Plot saved to:" in line for line in call_args_list_info)) # No plot expected
        self.assertFalse(any("Raw data saved to:" in line for line in call_args_list_info)) # No parquet expected

        # Assert that print_error was NOT called
        mock_print_error.assert_not_called()
        self.assertEqual(len(call_args_list_error), 0)


    @patch('src.common.logger.print_error')
    @patch('src.common.logger.print_info')
    def test_print_summary_failure(self, mock_print_info, mock_print_error):
        """Test print_summary output when workflow failed."""
        mock_results = MOCK_BASE_RESULTS.copy()
        mock_results.update({
            "status": "Failed",
            "mode": "binance",
            "ticker": "BTCUSDT",
            "interval": "1h",
            "rule": TradingRule.Pressure_Vector, # Use valid base rule
            "error_message": "API key invalid",
            "error_traceback": "Traceback:\n...",
            "total_duration_sec": 1.2, # Use this duration
            "steps_duration": {"acquire": 1.2}, # Only acquire step ran
            "plot_file_path": None,
            "parquet_file_path": None,
            "validation_metrics": None,
            "api_latency_sec": None,
            "api_calls": 1,
            "successful_chunks": 0,
        })
        # Ensure data_metrics exists, even if minimal, for source lookup
        if "data_metrics" not in mock_results or not mock_results["data_metrics"]:
             mock_results["data_metrics"] = {}
        mock_results["data_metrics"]["source"] = "Source_binance" # Add source if missing

        # Create mock args
        mock_args = self._create_mock_args(mock_results)

        # FIX: Call print_summary with all required arguments
        print_summary(mock_results, mock_results['total_duration_sec'], mock_args)

        # Extract log arguments
        call_args_list_info = self._extract_log_args(mock_print_info)
        call_args_list_error = self._extract_log_args(mock_print_error)

        # --- Assertions (remain the same) ---
        # Check that basic info is still printed
        self.assertTrue(any("--- Run Summary ---" in line for line in call_args_list_info))
        self.assertTrue(any("Mode: binance" in line for line in call_args_list_info))
        self.assertTrue(any("Ticker: BTCUSDT" in line for line in call_args_list_info))
        self.assertTrue(any("Interval: 1h" in line for line in call_args_list_info))
        # Check status is Failed and error is printed to error log
        self.assertTrue(any("Status: Failed" in line for line in call_args_list_error))
        self.assertTrue(any("Error Message: API key invalid" in line for line in call_args_list_error))
        self.assertTrue(any("Traceback:" in line for line in call_args_list_error))
        # Check total duration printed to info log
        self.assertTrue(any("Total Duration:" in line and "1.200 sec" in line for line in call_args_list_info))
        # Check only acquire step duration is printed
        self.assertTrue(any("Acquire Data Duration:" in line and "1.200 sec" in line for line in call_args_list_info))
        self.assertFalse(any("Calculate Indicator Duration:" in line for line in call_args_list_info))


if __name__ == '__main__':
    unittest.main()