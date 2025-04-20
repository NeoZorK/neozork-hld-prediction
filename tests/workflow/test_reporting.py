# tests/workflow/test_reporting.py (CORRECTED - Key and Value Fixes)

import unittest
from unittest.mock import patch, MagicMock # Removed ANY as it wasn't used here
import argparse # Import argparse to simulate Namespace

from src.workflow.reporting import print_summary
from src.common.constants import TradingRule # Make sure TradingRule is imported

# Sample results dictionary structure for testing
MOCK_BASE_RESULTS = {
    "success": True, # Changed from status
    "mode": "demo",
    "ticker": "DemoTicker",
    "interval": "D1",
    "rule": TradingRule.Pressure_Vector, # Valid member
    "point_size": 0.0001,
    "estimated_point": True,
    "csv_file_path": None,
    # Removed total_duration_sec from here, it's passed separately
    "steps_duration": {"acquire": 2.1, "point_size": 0.2, "calculate": 5.0, "plot": 3.2},
    "data_metrics": {"rows": 100, "cols": 6, "memory_mb": 0.1, "start": "2023-01-01", "end": "2023-04-10"},
    "validation_metrics": None,
    "plot_file_path": "/path/to/plot.png",
    "parquet_save_path": "/path/to/data.parquet", # CORRECTED Key
    "api_latency_sec": 1.5,
    "api_calls": 5,
    "successful_chunks": 5,
    "error_message": None,
    "error_traceback": None,
    # Added fields used in print_summary
    "effective_mode": "demo",
    "data_source_label": "Demo Data",
    "yf_ticker": None,
    "yf_interval": None,
    "current_period": None,
    "current_start": "2023-01-01",
    "current_end": "2023-04-10",
    "data_fetch_duration": 2.1,
    "calc_duration": 5.0,
    "plot_duration": 3.2,
    "data_size_mb": 0.1,
    "data_size_bytes": 102400,
    "rows_count": 100,
    "columns_count": 6,
    "file_size_bytes": None,
    "selected_rule": TradingRule.Pressure_Vector, # Add selected rule
}

class TestReporting(unittest.TestCase):

    # Helper to extract log messages - CORRECTED V2
    def _extract_log_args(self, mock_logger):
        """Extracts the first string argument from mock logger calls."""
        log_args = []
        # Access call_args_list from the mock object itself
        for call_item in mock_logger.call_args_list:
            # Ensure there are positional arguments and the first one is a string
            if call_item.args and isinstance(call_item.args[0], str):
                log_args.append(call_item.args[0])
            # Check if the first argument is a list/tuple (from logger formatting)
            elif call_item.args and isinstance(call_item.args[0], (list, tuple)) and len(call_item.args[0]) > 0:
                 log_args.append(str(call_item.args[0][0])) # Assume first element is the message
            elif call_item.args: # Fallback for unexpected arg types
                log_args.append(str(call_item.args[0]))

        return log_args

    # Helper to create mock args based on results
    def _create_mock_args(self, results):
         """ Simulates the args namespace needed by print_summary """
         mock_args = argparse.Namespace()
         mock_args.mode = results.get("mode")
         mock_args.ticker = results.get("ticker")
         mock_args.interval = results.get("interval")
         # Pass rule name string if needed, or enum itself - depends on how print_summary uses it
         # Let's pass the name as it's likely used for display
         selected_rule = results.get("selected_rule", results.get("rule")) # Use selected_rule if available
         mock_args.rule = selected_rule.name if isinstance(selected_rule, TradingRule) else str(selected_rule)
         mock_args.csv_file = results.get("csv_file_path")
         # Add other args if print_summary uses them
         return mock_args

    @patch('src.common.logger.print_error')
    @patch('src.common.logger.print_info')
    def test_print_summary_csv_success(self, mock_print_info, mock_print_error):
        """Test print_summary output for a successful CSV run."""
        mock_results = MOCK_BASE_RESULTS.copy()
        mock_results.update({
            "success": True,
            "mode": "csv",
            "effective_mode": "csv",
            "ticker": None,
            "interval": "H1",
            "rule": TradingRule.Predict_High_Low_Direction,
            "selected_rule": TradingRule.Predict_High_Low_Direction, # Match rule
            "point_size": 0.01,
            "estimated_point": False,
            "csv_file_path": "data/test.csv",
            "data_source_label": "data/test.csv",
            # "total_duration_sec": 5.123, # Passed separately
            "steps_duration": {"acquire": 1.2, "point_size": 0.1, "calculate": 2.5, "plot": 1.323},
            "data_fetch_duration": 1.2, # Match step duration
            "calc_duration": 2.5,
            "plot_duration": 1.323,
            "data_metrics": {"rows": 1000, "cols": 15, "memory_mb": 1.5, "start": "2023-01-01", "end": "2023-01-10"},
            "rows_count": 1000, "columns_count": 15, "data_size_mb": 1.5, "data_size_bytes": 1572864,
            "validation_metrics": {"pressure_match": 0.99, "pv_match": 0.98, "phl_match": 0.75, "rows_compared": 998},
            "plot_file_path": "plots/plot_test_h1.png",
            "parquet_save_path": None, # CORRECTED Key
            "api_latency_sec": None,
            "api_calls": None,
            "successful_chunks": None,
            "file_size_bytes": 1600000, # Example file size
        })
        mock_total_duration = 5.123 # Define total duration
        mock_args = self._create_mock_args(mock_results)

        print_summary(mock_results, mock_total_duration, mock_args)

        call_args_list_info = self._extract_log_args(mock_print_info)
        call_args_list_error = self._extract_log_args(mock_print_error)

        # --- Assertions --- # Updated to check for key strings
        self.assertTrue(any("--- Execution Summary ---" in line for line in call_args_list_info), "Summary header missing")
        # self.assertTrue(any("Status: Success" in line for line in call_args_list_info)) # Status not printed directly
        self.assertTrue(any("Data Source:" in line and "data/test.csv" in line for line in call_args_list_info), "CSV File path missing")
        self.assertTrue(any("Rule Applied:" in line and "Predict_High_Low_Direction" in line for line in call_args_list_info), "Rule missing")
        self.assertTrue(any("Point Size Used:" in line and "0.01" in line and "Estimated" not in line for line in call_args_list_info), "Point size incorrect")
        self.assertTrue(any("DataFrame Shape:" in line and "1000 rows, 15 columns" in line for line in call_args_list_info), "Shape incorrect")
        # Validation metrics are not directly printed in the current print_summary, checked elsewhere if needed
        # self.assertTrue(any("Validation Pressure Match:" in line and "99.00%" in line for line in call_args_list_info))
        # self.assertTrue(any("Validation PV Match:" in line and "98.00%" in line for line in call_args_list_info))
        # self.assertTrue(any("Validation PHL Match:" in line and "75.00%" in line for line in call_args_list_info))
        # Plot path not printed directly
        # self.assertTrue(any("Plot saved to:" in line and "plots/plot_test_h1.png" in line for line in call_args_list_info))
        self.assertFalse(any("Saved Raw Data:" in line for line in call_args_list_info), "Parquet path incorrectly shown")
        self.assertFalse(any("API" in line for line in call_args_list_info), "API metrics incorrectly shown")
        self.assertTrue(any("Total Execution Time:" in line and "5.123 sec" in line for line in call_args_list_info), "Total duration missing")

        mock_print_error.assert_not_called()

    @patch('src.common.logger.print_error')
    @patch('src.common.logger.print_info')
    def test_print_summary_yfinance_success_saved(self, mock_print_info, mock_print_error):
        """Test print_summary output for a successful YFinance run with parquet save."""
        mock_results = MOCK_BASE_RESULTS.copy()
        mock_results.update({
            "success": True,
            "mode": "yfinance",
            "effective_mode": "yfinance",
            "ticker": "AAPL",
            "data_source_label": "AAPL",
            "interval": "1d",
            "yf_interval": "1d", # Add mapped interval
            "selected_rule": TradingRule.Pressure_Vector,
            "parquet_save_path": "data/raw_parquet/yfinance_AAPL_1d.parquet", # CORRECTED Key
            "api_latency_sec": 0.85,
            "api_calls": 1,
            "successful_chunks": 1,
            "validation_metrics": None,
            "plot_file_path": "plots/yfinance_AAPL_1d_plot.png",
            "data_fetch_duration": 0.9,
            "calc_duration": 1.5,
            "plot_duration": 0.8,
            "data_metrics": {"rows": 100, "cols": 6, "memory_mb": 0.1, "start": "2023-01-01", "end": "2023-04-10", "source": "Source_yfinance"},
        })
        mock_total_duration = 9.876
        mock_args = self._create_mock_args(mock_results)

        print_summary(mock_results, mock_total_duration, mock_args)

        call_args_list_info = self._extract_log_args(mock_print_info)

        self.assertTrue(any("--- Execution Summary ---" in line for line in call_args_list_info))
        self.assertTrue(any("Data Source:" in line and "AAPL" in line for line in call_args_list_info))
        # self.assertTrue(any("Ticker:" in line and "AAPL" in line for line in call_args_list_info)) # Ticker not printed if same as source
        self.assertTrue(any("Interval Requested:" in line and "1d (mapped to 1d)" in line for line in call_args_list_info))
        self.assertTrue(any("Rule Applied:" in line and "Pressure_Vector" in line for line in call_args_list_info))
        self.assertTrue(any("Point Size Used:" in line and "0.0001" in line and "(Estimated)" in line for line in call_args_list_info))
        # self.assertTrue(any("Data Source:" in line and "Source_yfinance" in line for line in call_args_list_info)) # Source printed earlier
        self.assertTrue(any("yf.download Latency:" in line and "0.850 seconds" in line for line in call_args_list_info))
        # self.assertTrue(any("API Calls Made: 1" in line for line in call_args_list_info)) # Calls/Chunks not printed
        self.assertFalse(any("Validation" in line for line in call_args_list_info))
        # self.assertTrue(any("Plot saved to:" in line and "plots/yfinance_AAPL_1d_plot.png" in line for line in call_args_list_info)) # Plot path not printed
        # ** CORRECTED Assertion **
        self.assertTrue(any("Saved Raw Data:" in line and "data/raw_parquet/yfinance_AAPL_1d.parquet" in line for line in call_args_list_info), "Parquet save path missing from summary")
        self.assertTrue(any("Total Execution Time:" in line and "9.876 sec" in line for line in call_args_list_info))
        mock_print_error.assert_not_called()

    @patch('src.common.logger.print_error')
    @patch('src.common.logger.print_info')
    def test_print_summary_polygon_success_no_save(self, mock_print_info, mock_print_error):
        """Test print_summary output for a successful Polygon run where parquet save failed."""
        mock_results = MOCK_BASE_RESULTS.copy()
        mock_results.update({
            "success": True,
            "mode": "polygon",
            "effective_mode": "polygon",
            "ticker": "MSFT",
            "data_source_label": "MSFT",
            "interval": "M1",
            "selected_rule": TradingRule.PV_HighLow,
            "parquet_save_path": None, # Simulate parquet save failure (Key Corrected)
            "api_latency_sec": 5.8,
            "api_calls": 12,
            "successful_chunks": 10,
            "validation_metrics": None,
            "plot_file_path": None,
            "data_fetch_duration": 6.0,
            "calc_duration": 2.0,
            "plot_duration": 0.0, # No plot
             "data_metrics": {"rows": 100, "cols": 6, "memory_mb": 0.1, "start": "2023-01-01", "end": "2023-04-10", "source": "Source_polygon"},
        })
        mock_total_duration = 15.2
        mock_args = self._create_mock_args(mock_results)

        print_summary(mock_results, mock_total_duration, mock_args)

        call_args_list_info = self._extract_log_args(mock_print_info)

        self.assertTrue(any("--- Execution Summary ---" in line for line in call_args_list_info))
        self.assertTrue(any("Data Source:" in line and "MSFT" in line for line in call_args_list_info))
        self.assertTrue(any("Rule Applied:" in line and "PV_HighLow" in line for line in call_args_list_info))
        self.assertTrue(any("Point Size Used:" in line and "0.0001" in line and "(Estimated)" in line for line in call_args_list_info))
        # self.assertTrue(any("Data Source:" in line and "Source_polygon" in line for line in call_args_list_info))
        self.assertTrue(any("API Chunks Total Latency:" in line and "5.800 seconds" in line for line in call_args_list_info))
        # self.assertTrue(any("API Calls Made: 12" in line for line in call_args_list_info)) # Not printed
        # self.assertTrue(any("API Chunks Successful: 10" in line for line in call_args_list_info)) # Not printed
        self.assertFalse(any("Validation" in line for line in call_args_list_info))
        # self.assertFalse(any("Plot saved to:" in line for line in call_args_list_info)) # Plot path not printed
        self.assertFalse(any("Saved Raw Data:" in line for line in call_args_list_info)) # No parquet path
        self.assertTrue(any("Total Execution Time:" in line and "15.200 sec" in line for line in call_args_list_info))
        mock_print_error.assert_not_called()


    @patch('src.common.logger.print_error')
    @patch('src.common.logger.print_info')
    def test_print_summary_failure(self, mock_print_info, mock_print_error):
        """Test print_summary output when workflow failed."""
        mock_results = MOCK_BASE_RESULTS.copy()
        mock_results.update({
            "success": False, # Workflow failed
            "mode": "binance",
            "effective_mode": "binance",
            "ticker": "BTCUSDT",
            "data_source_label": "BTCUSDT",
            "interval": "1h",
            "selected_rule": TradingRule.Pressure_Vector, # Use valid base rule
            "error_message": "API key invalid",
            "error_traceback": "Traceback:\n...",
            "data_fetch_duration": 1.2, # Only acquire step ran
            "calc_duration": 0.0, # ** CORRECTED: Explicitly add 0.0 **
            "plot_duration": 0.0, # Add plot duration as 0.0 as well
            "steps_duration": {"acquire": 1.2},
            "plot_file_path": None,
            "parquet_save_path": None, # CORRECTED Key
            "validation_metrics": None,
            "api_latency_sec": None,
            "api_calls": 1,
            "successful_chunks": 0,
            "data_metrics": {"source": "Source_binance"}, # Minimal metrics
        })
        mock_total_duration = 1.2
        mock_args = self._create_mock_args(mock_results)

        print_summary(mock_results, mock_total_duration, mock_args)

        call_args_list_info = self._extract_log_args(mock_print_info)
        call_args_list_error = self._extract_log_args(mock_print_error)

        # --- Assertions ---
        self.assertTrue(any("--- Execution Summary ---" in line for line in call_args_list_info))
        self.assertTrue(any("Data Source:" in line and "BTCUSDT" in line for line in call_args_list_info))
        # Check status is Failed and error is printed to error log
        # Status not printed directly, but error message is
        self.assertTrue(any("Workflow failed: API key invalid" in line for line in call_args_list_error))
        # Traceback not printed directly by print_summary
        # self.assertTrue(any("Traceback:" in line for line in call_args_list_error))

        # Check total duration printed to info log
        self.assertTrue(any("Total Execution Time:" in line and "1.200 sec" in line for line in call_args_list_info))
        # Check only acquire step duration is printed
        self.assertTrue(any("Data Fetch/Load Time:" in line and "1.200 sec" in line for line in call_args_list_info))
        # ** CORRECTED Assertion **
        self.assertTrue(any("Indicator Calc Time:" in line and "0.000 sec" in line for line in call_args_list_info), "Calc time 0.000s missing in failure summary")
        self.assertTrue(any("Plot Generation Time:" in line and "0.000 sec" in line for line in call_args_list_info), "Plot time 0.000s missing in failure summary")


if __name__ == '__main__':
    unittest.main()