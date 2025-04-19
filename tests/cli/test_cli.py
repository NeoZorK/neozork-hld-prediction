# tests/cli/test_cli.py # ADDED BINANCE TESTS

import unittest
from unittest.mock import patch
#import argparse

# Import the function to test
from src.cli.cli import parse_arguments
# Import constants needed for choices/defaults if necessary
from src.common.constants import TradingRule
from src import __version__ # Import version to check output

# Unit tests for the command line interface setup
class TestCli(unittest.TestCase):

    # Test default arguments when only mode is provided
    @patch('sys.argv', ['run_analysis.py', 'demo'])
    def test_parse_arguments_defaults_demo(self):
        args = parse_arguments()
        self.assertEqual(args.mode, 'demo')
        self.assertEqual(args.rule, TradingRule.Predict_High_Low_Direction.name)
        self.assertIsNone(args.ticker)
        self.assertEqual(args.interval, 'D1')
        self.assertEqual(args.period, '1y') # Default from argparse
        self.assertIsNone(args.start)
        self.assertIsNone(args.end)
        self.assertIsNone(args.point)
        self.assertIsNone(args.csv_file)

    # Test yfinance mode with specific arguments
    @patch('sys.argv', [
        'run_analysis.py', 'yf',
        '--ticker', 'EURUSD=X', '--interval', 'H1',
        '--start', '2023-01-01', '--end', '2023-12-31',
        '--point', '0.0001', '--rule', 'PV_HighLow'
    ])
    def test_parse_arguments_yfinance_specific(self):
        args = parse_arguments()
        self.assertIn(args.mode, ['yfinance', 'yf'])
        self.assertEqual(args.ticker, 'EURUSD=X')
        self.assertEqual(args.interval, 'H1')
        self.assertEqual(args.start, '2023-01-01')
        self.assertEqual(args.end, '2023-12-31')
        self.assertEqual(args.point, 0.0001)
        self.assertEqual(args.rule, 'PV_HighLow')
        self.assertIsNone(args.period) # Period should be None if start/end used

    # Test yfinance mode using period
    @patch('sys.argv', [
        'run_analysis.py', 'yfinance',
        '--ticker', 'AAPL', '--period', '6mo', '--rule', 'SR'
    ])
    def test_parse_arguments_yfinance_period(self):
        args = parse_arguments()
        self.assertIn(args.mode, ['yfinance', 'yf'])
        self.assertEqual(args.ticker, 'AAPL')
        self.assertEqual(args.interval, 'D1') # Default interval
        self.assertEqual(args.period, '6mo')
        self.assertEqual(args.rule, 'SR')
        self.assertIsNone(args.start)
        self.assertIsNone(args.end)
        self.assertIsNone(args.point)

    # --- CSV Mode Tests ---
    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-file', 'mydata.csv', '--point', '0.1'])
    def test_parse_arguments_csv_success(self):
        args = parse_arguments()
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_file, 'mydata.csv')
        self.assertEqual(args.point, 0.1)
        self.assertEqual(args.rule, TradingRule.Predict_High_Low_Direction.name) # Default rule

    @patch('sys.argv', ['run_analysis.py', 'csv', '--point', '0.1']) # Missing csv-file
    def test_parse_arguments_csv_fail_no_file(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2) # argparse error exit code

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-file', 'mydata.csv']) # Missing point
    def test_parse_arguments_csv_fail_no_point(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)

    # --- Polygon Mode Tests ---
    @patch('sys.argv', ['run_analysis.py', 'polygon', '--ticker', 'MSFT', '--start', '2024-01-01', '--end', '2024-02-01', '--point', '0.01'])
    def test_parse_arguments_polygon_success(self):
        args = parse_arguments()
        self.assertEqual(args.mode, 'polygon')
        self.assertEqual(args.ticker, 'MSFT')
        self.assertEqual(args.start, '2024-01-01')
        self.assertEqual(args.end, '2024-02-01')
        self.assertEqual(args.point, 0.01)

    @patch('sys.argv', ['run_analysis.py', 'polygon', '--start', '2024-01-01', '--end', '2024-02-01', '--point', '0.01']) # Missing ticker
    def test_parse_arguments_polygon_fail_no_ticker(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)

    @patch('sys.argv', ['run_analysis.py', 'polygon', '--ticker', 'MSFT', '--end', '2024-02-01', '--point', '0.01']) # Missing start
    def test_parse_arguments_polygon_fail_no_start(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)

    @patch('sys.argv', ['run_analysis.py', 'polygon', '--ticker', 'MSFT', '--start', '2024-01-01', '--point', '0.01']) # Missing end
    def test_parse_arguments_polygon_fail_no_end(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)

    @patch('sys.argv', ['run_analysis.py', 'polygon', '--ticker', 'MSFT', '--start', '2024-01-01', '--end', '2024-02-01']) # Missing point
    def test_parse_arguments_polygon_fail_no_point(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)


    # --- Binance Mode Tests --- ADDED SECTION ---
    @patch('sys.argv', ['run_analysis.py', 'binance', '--ticker', 'BTCUSDT', '--start', '2024-04-01', '--end', '2024-04-10', '--point', '0.01', '--interval', 'M1'])
    def test_parse_arguments_binance_success(self):
        args = parse_arguments()
        self.assertEqual(args.mode, 'binance')
        self.assertEqual(args.ticker, 'BTCUSDT')
        self.assertEqual(args.start, '2024-04-01')
        self.assertEqual(args.end, '2024-04-10')
        self.assertEqual(args.point, 0.01)
        self.assertEqual(args.interval, 'M1') # Check non-default interval

    @patch('sys.argv', ['run_analysis.py', 'binance', '--start', '2024-04-01', '--end', '2024-04-10', '--point', '0.01']) # Missing ticker
    def test_parse_arguments_binance_fail_no_ticker(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)

    @patch('sys.argv', ['run_analysis.py', 'binance', '--ticker', 'BTCUSDT', '--end', '2024-04-10', '--point', '0.01']) # Missing start
    def test_parse_arguments_binance_fail_no_start(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)

    @patch('sys.argv', ['run_analysis.py', 'binance', '--ticker', 'BTCUSDT', '--start', '2024-04-01', '--point', '0.01']) # Missing end
    def test_parse_arguments_binance_fail_no_end(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)

    @patch('sys.argv', ['run_analysis.py', 'binance', '--ticker', 'BTCUSDT', '--start', '2024-04-01', '--end', '2024-04-10']) # Missing point
    def test_parse_arguments_binance_fail_no_point(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)
    # --- END ADDED SECTION ---


    # --- General Argument Tests ---
    @patch('sys.argv', ['run_analysis.py', 'demo', '--rule', 'PHLD'])
    def test_parse_arguments_rule_alias_phld(self):
        args = parse_arguments()
        self.assertEqual(args.rule, 'PHLD')

    @patch('sys.argv', ['run_analysis.py', 'demo', '--rule', 'PV'])
    def test_parse_arguments_rule_alias_pv(self):
        args = parse_arguments()
        self.assertEqual(args.rule, 'PV')

    # Test asking for version
    @patch('argparse.ArgumentParser._print_message') # Mock print_message to suppress output
    @patch('sys.argv', ['run_analysis.py', '--version'])
    def test_parse_arguments_version(self, mock_print_message):
        with self.assertRaises(SystemExit) as cm:
            parse_arguments()
        self.assertEqual(cm.exception.code, 0) # Expect clean exit (code 0)
        # Check that the correct version string was prepared for printing
        # This checks the internal mechanism of action='version'
        call_args = mock_print_message.call_args[0] # Get positional arguments of the call
        self.assertIn(f'{__version__}', call_args[1]) # Check version string is in the message


    # Test mutually exclusive group (period vs start/end) for yfinance
    @patch('sys.argv', [
        'run_analysis.py', 'yf', '--ticker', 'XYZ', '--period', '1y', '--start', '2023-01-01'
    ])
    def test_parse_arguments_mutually_exclusive_fail(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)

    # Test invalid rule choice
    @patch('sys.argv', ['run_analysis.py', 'demo', '--rule', 'INVALID_RULE'])
    def test_parse_arguments_invalid_rule(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)

    # Test invalid mode choice
    @patch('sys.argv', ['run_analysis.py', 'invalid_mode'])
    def test_parse_arguments_invalid_mode(self):
        with self.assertRaises(SystemExit) as cm: parse_arguments()
        self.assertEqual(cm.exception.code, 2)


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()