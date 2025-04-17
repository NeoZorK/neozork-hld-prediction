# tests/workflow/test_reporting.py

import unittest
from unittest.mock import patch #, MagicMock, call
import argparse

# Import the function to test
from src.workflow.reporting import print_summary

# Dummy logger to check calls
class MockLogger:
    def __init__(self):
        self.calls = []

    def print_info(self, msg):
        self.calls.append(('info', msg))

    def print_warning(self, msg):
        self.calls.append(('warning', msg))

    def print_error(self, msg):
        self.calls.append(('error', msg))

    # Helper to format summary line similar to the real logger for assertion checks
    def format_summary_line(self, key, value, key_width=25):
        padded_key = f"{key+':':<{key_width}}"
        return f"{padded_key} {value}" # Simplified version without colors for test comparison

# Dummy args namespace
def create_mock_args(mode='demo', rule='TestRule', interval='D1', ticker=None, point=None, start=None, end=None, period=None):
    return argparse.Namespace(
        mode=mode, rule=rule, interval=interval, ticker=ticker, point=point,
        start=start, end=end, period=period
    )

# Unit tests for the summary reporting function
class TestReporting(unittest.TestCase):

    # Test summary print for demo mode success
    @patch('src.workflow.reporting.logger', new_callable=MockLogger)
    def test_print_summary_demo_success(self, mock_logger):
        args = create_mock_args(mode='demo', rule='Predict_High_Low_Direction')
        results = {
            "success": True, "data_fetch_duration": 0.1, "data_size_mb": 0.05, "data_size_bytes": 51200,
            "calc_duration": 0.2, "plot_duration": 0.3, "point_size": 0.00001, "estimated_point": False,
            "data_source_label": "Demo Data", "yf_ticker": None, "yf_interval": None, "current_period": None,
            "current_start": None, "current_end": None, "selected_rule": args.rule, "error_message": None,
            "effective_mode": "demo"
        }
        total_duration = 0.6

        print_summary(results, total_duration, args)

        # Check the sequence and content of logger calls (simplified check)
        log_messages = [c[1] for c in mock_logger.calls if c[0] == 'info'] # Get only info messages

        self.assertIn("\n--- Execution Summary ---", log_messages[0])
        self.assertIn(mock_logger.format_summary_line("Data Source:", 'Demo'), log_messages[1])
        self.assertIn(mock_logger.format_summary_line("Rule Applied:", args.rule), log_messages[2])
        # Check Point Size formatting (using .8f for small demo point)
        self.assertIn(mock_logger.format_summary_line("Point Size Used:", f"{results['point_size']:.8f}"), log_messages[3])
        self.assertIn(mock_logger.format_summary_line("Data Size:", f"{results['data_size_mb']:.3f} MB ({results['data_size_bytes']:,} bytes)"), log_messages[5]) # Index 5 after separator
        self.assertIn(mock_logger.format_summary_line("Data Fetch/Load Time:", f"{results['data_fetch_duration']:.3f} seconds"), log_messages[6])
        self.assertIn(mock_logger.format_summary_line("Indicator Calc Time:", f"{results['calc_duration']:.3f} seconds"), log_messages[7])
        self.assertIn(mock_logger.format_summary_line("Plotting Time:", f"{results['plot_duration']:.3f} seconds"), log_messages[8])
        self.assertIn(mock_logger.format_summary_line("Total Execution Time:", f"{total_duration:.3f} seconds"), log_messages[10]) # Index 10 after separator
        self.assertIn("--- End Summary ---", log_messages[11])

        # Ensure no error message was printed for success case
        error_calls = [c for c in mock_logger.calls if c[0] == 'error']
        self.assertEqual(len(error_calls), 0)
        # Ensure no yfinance specific warning printed for demo mode
        warning_calls = [c for c in mock_logger.calls if c[0] == 'warning']
        self.assertEqual(len(warning_calls), 0)


    # Test summary print for yfinance mode success with period and estimated point
    @patch('src.workflow.reporting.logger', new_callable=MockLogger)
    def test_print_summary_yfinance_period_estimated(self, mock_logger):
        args = create_mock_args(mode='yf', rule='PV_HighLow', ticker='EURUSD=X', interval='H1', period='3mo')
        results = {
            "success": True, "data_fetch_duration": 0.5, "data_size_mb": 1.2, "data_size_bytes": 1258291,
            "calc_duration": 1.1, "plot_duration": 0.8, "point_size": 0.00001, "estimated_point": True, # Estimated point
            "data_source_label": args.ticker, "yf_ticker": "EURUSD=X", "yf_interval": "1h", # Mapped interval
            "current_period": args.period, "current_start": None, "current_end": None,
            "selected_rule": args.rule, "error_message": None, "effective_mode": "yfinance"
        }
        total_duration = 2.4

        print_summary(results, total_duration, args)

        # Check the sequence and content of logger calls
        log_messages_info = [c[1] for c in mock_logger.calls if c[0] == 'info']
        log_messages_warning = [c[1] for c in mock_logger.calls if c[0] == 'warning']

        self.assertIn(mock_logger.format_summary_line("Data Source:", args.ticker), log_messages_info[1])
        self.assertIn(mock_logger.format_summary_line("Rule Applied:", args.rule), log_messages_info[2])
        # Check yfinance specific lines
        self.assertIn("--- YFinance Data Note: Volume might be zero/missing for Forex/Indices ---", log_messages_warning[0]) # Warning present
        self.assertIn(mock_logger.format_summary_line("Ticker:", results['yf_ticker']), log_messages_info[3])
        self.assertIn(mock_logger.format_summary_line("Interval Requested:", f"{args.interval} (mapped to {results['yf_interval']})"), log_messages_info[4])
        self.assertIn(mock_logger.format_summary_line("Period:", results['current_period']), log_messages_info[5]) # Period shown
        # Check Point Size formatting with "(Estimated)" flag
        self.assertIn(mock_logger.format_summary_line("Point Size Used:", f"{results['point_size']:.8f} (Estimated)"), log_messages_info[6])
        self.assertIn(mock_logger.format_summary_line("Total Execution Time:", f"{total_duration:.3f} seconds"), log_messages_info[12]) # Adjusted index


    # Test summary print for yfinance mode success with start/end and provided point
    @patch('src.workflow.reporting.logger', new_callable=MockLogger)
    def test_print_summary_yfinance_start_end_provided_point(self, mock_logger):
        args = create_mock_args(mode='yfinance', rule='Support_Resistants', ticker='AAPL', interval='D1',
                                start='2024-01-01', end='2024-03-31', point=0.01) # Provided point
        results = {
            "success": True, "data_fetch_duration": 0.6, "data_size_mb": 0.8, "data_size_bytes": 838860,
            "calc_duration": 0.4, "plot_duration": 0.5, "point_size": args.point, "estimated_point": False, # Provided point
            "data_source_label": args.ticker, "yf_ticker": "AAPL", "yf_interval": "1d",
            "current_period": None, "current_start": args.start, "current_end": args.end, # Start/End used
            "selected_rule": args.rule, "error_message": None, "effective_mode": "yfinance"
        }
        total_duration = 1.5

        print_summary(results, total_duration, args)

        log_messages_info = [c[1] for c in mock_logger.calls if c[0] == 'info']
        log_messages_warning = [c[1] for c in mock_logger.calls if c[0] == 'warning']

        self.assertIn(mock_logger.format_summary_line("Data Source:", args.ticker), log_messages_info[1])
        self.assertIn("--- YFinance Data Note: Volume might be zero/missing for Forex/Indices ---", log_messages_warning[0])
        self.assertIn(mock_logger.format_summary_line("Ticker:", results['yf_ticker']), log_messages_info[3])
        self.assertIn(mock_logger.format_summary_line("Interval Requested:", f"{args.interval} (mapped to {results['yf_interval']})"), log_messages_info[4])
        # Check Date Range is shown instead of Period
        self.assertIn(mock_logger.format_summary_line("Date Range:", f"{results['current_start']} to {results['current_end']}"), log_messages_info[5])
        # Check Point Size formatting without "(Estimated)" flag (using .2f for 0.01)
        self.assertIn(mock_logger.format_summary_line("Point Size Used:", f"{results['point_size']:.2f}"), log_messages_info[6])


    # Test summary print for workflow failure
    @patch('src.workflow.reporting.logger', new_callable=MockLogger)
    def test_print_summary_failure(self, mock_logger):
        args = create_mock_args(mode='yf', rule='Predict_High_Low_Direction', ticker='FAIL', interval='D1')
        error_msg = "Data acquisition failed"
        results = {
            "success": False, # Failure flag
            "data_fetch_duration": 0.1, "data_size_mb": 0, "data_size_bytes": 0, # No data size
            "calc_duration": 0, "plot_duration": 0, "point_size": None, "estimated_point": False, # No point size
            "data_source_label": args.ticker, "yf_ticker": "FAIL", "yf_interval": "1d",
            "current_period": args.period, "current_start": None, "current_end": None,
            "selected_rule": args.rule, "error_message": error_msg, # Error message present
            "effective_mode": "yfinance"
        }
        total_duration = 0.15

        print_summary(results, total_duration, args)

        log_messages_info = [c[1] for c in mock_logger.calls if c[0] == 'info']
        log_messages_error = [c[1] for c in mock_logger.calls if c[0] == 'error']

        # Check Point Size shows N/A with reason
        self.assertIn(mock_logger.format_summary_line("Point Size Used:", "N/A (Data load failed)"), log_messages_info[6])
        # Check timings might be zero
        self.assertIn(mock_logger.format_summary_line("Indicator Calc Time:", f"{results['calc_duration']:.3f} seconds"), log_messages_info[8])

        # Check error message is printed at the end
        self.assertEqual(len(log_messages_error), 1)
        self.assertIn(f"Workflow failed: {error_msg}", log_messages_error[0])

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()