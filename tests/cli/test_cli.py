# tests/cli/test_cli.py

import unittest
from unittest.mock import patch
import argparse

# Import the function to test
from src.cli.cli import parse_arguments
# Import constants needed for choices/defaults if necessary
from src.common.constants import TradingRule


# Unit tests for the command line interface setup
class TestCli(unittest.TestCase):

    # Test default arguments when only mode is provided
    @patch('sys.argv', ['run_analysis.py', 'demo'])
    def test_parse_arguments_defaults_demo(self):
        args = parse_arguments()
        self.assertEqual(args.mode, 'demo')
        # Check defaults for other args that might be accessed even in demo mode (though they shouldn't be used)
        self.assertEqual(args.rule, TradingRule.Predict_High_Low_Direction.name) # Default rule
        # Check that yfinance specific args are None or their defaults if accessed directly
        self.assertIsNone(args.ticker)
        self.assertEqual(args.interval, 'D1')
        self.assertEqual(args.period, '1y')
        self.assertIsNone(args.start)
        self.assertIsNone(args.end)
        self.assertIsNone(args.point)

    # Test yfinance mode with specific arguments
    @patch('sys.argv', [
        'run_analysis.py', 'yf',
        '--ticker', 'EURUSD=X',
        '--interval', 'H1',
        '--start', '2023-01-01',
        '--end', '2023-12-31',
        '--point', '0.0001',
        '--rule', 'PV_HighLow'
    ])
    def test_parse_arguments_yfinance_specific(self):
        args = parse_arguments()
        self.assertIn(args.mode, ['yfinance', 'yf']) # Accept both aliases
        self.assertEqual(args.ticker, 'EURUSD=X')
        self.assertEqual(args.interval, 'H1')
        self.assertEqual(args.start, '2023-01-01')
        self.assertEqual(args.end, '2023-12-31')
        self.assertEqual(args.point, 0.0001)
        self.assertEqual(args.rule, 'PV_HighLow')
        # Check that 'period' is None because start/end were used
        self.assertIsNone(args.period) # mutually exclusive group works

    # Test yfinance mode using period
    @patch('sys.argv', [
        'run_analysis.py', 'yfinance',
        '--ticker', 'AAPL',
        '--period', '6mo',
        '--rule', 'SR' # Use alias Support_Resistants
    ])
    def test_parse_arguments_yfinance_period(self):
        args = parse_arguments()
        self.assertIn(args.mode, ['yfinance', 'yf'])
        self.assertEqual(args.ticker, 'AAPL')
        self.assertEqual(args.interval, 'D1') # Default interval
        self.assertEqual(args.period, '6mo')
        self.assertEqual(args.rule, 'SR') # Check alias works
        # Check that start/end are None because period was used
        self.assertIsNone(args.start)
        self.assertIsNone(args.end)
        self.assertIsNone(args.point) # Default point

    # Test rule alias PHLD
    @patch('sys.argv', ['run_analysis.py', 'demo', '--rule', 'PHLD'])
    def test_parse_arguments_rule_alias_phld(self):
        args = parse_arguments()
        self.assertEqual(args.mode, 'demo')
        self.assertEqual(args.rule, 'PHLD') # Argument uses the alias

    # Test rule alias PV
    @patch('sys.argv', ['run_analysis.py', 'demo', '--rule', 'PV'])
    def test_parse_arguments_rule_alias_pv(self):
        args = parse_arguments()
        self.assertEqual(args.mode, 'demo')
        self.assertEqual(args.rule, 'PV')

    # Test asking for version (will raise SystemExit, which is expected)
    # We patch argparse.ArgumentParser._print_message to prevent version printing to stdout/stderr
    @patch('argparse.ArgumentParser._print_message')
    @patch('sys.argv', ['run_analysis.py', '--version'])
    def test_parse_arguments_version(self, mock_print_message):
        with self.assertRaises(SystemExit) as cm:
            parse_arguments()
        self.assertEqual(cm.exception.code, 0) # Expect clean exit (code 0) for --version

    # Test mutually exclusive group (period vs start/end) - should raise error
    @patch('sys.argv', [
        'run_analysis.py', 'yf',
        '--ticker', 'XYZ',
        '--period', '1y',
        '--start', '2023-01-01' # Cannot use both period and start
    ])
    def test_parse_arguments_mutually_exclusive_fail(self):
         # argparse raises SystemExit with code 2 on error
        with self.assertRaises(SystemExit) as cm:
            parse_arguments()
        self.assertEqual(cm.exception.code, 2)

    # Test invalid rule choice - should raise error
    @patch('sys.argv', ['run_analysis.py', 'demo', '--rule', 'INVALID_RULE'])
    def test_parse_arguments_invalid_rule(self):
        with self.assertRaises(SystemExit) as cm:
            parse_arguments()
        self.assertEqual(cm.exception.code, 2)

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()