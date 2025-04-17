# tests/calculation/test_rules.py

import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch

# Import functions and constants to test/use
from src.calculation.rules import (
    apply_trading_rule # Dispatcher
)
from src.common.constants import TradingRule #, BUY, SELL, NOTRADE #, EMPTY_VALUE

# Unit tests for rule application functions
class TestRules(unittest.TestCase):

    # Setup sample data for tests
    def setUp(self):
        self.df = pd.DataFrame({
            'Open':     [100, 110, 120, 115, 125],
            'High':     [105, 115, 125, 120, 130], # Not directly used by rules, but good context
            'Low':      [ 95, 105, 115, 110, 120], # Not directly used by rules
            'Close':    [102, 112, 118, 116, 128], # Not directly used by rules
            'Volume':   [1000,1200,1100,1300,1500],# Not directly used by rules
            # Required inputs for rules (typically calculated in indicator.py first)
            'HL':       pd.Series([100, 80, 120, 50, 90], dtype=float),  # HL in points
            'PV':       pd.Series([np.nan, 1.5, -0.5, 0.0, 2.0], dtype=float), # Pressure Vector
        })
        self.point = 0.1

    @patch('src.calculation.rules.apply_rule_predict_hld', autospec=True)
    def test_dispatcher_calls_predict_hld(self, mock_rule_func):
        df_in = self.df.copy()
        point = self.point
        apply_trading_rule(df_in, TradingRule.Predict_High_Low_Direction, point)
        mock_rule_func.assert_called_once_with(df_in, point=point)

    @patch('src.calculation.rules.apply_rule_pv_highlow', autospec=True)
    def test_dispatcher_calls_pv_highlow(self, mock_rule_func):
        df_in = self.df.copy()
        point = self.point
        apply_trading_rule(df_in, TradingRule.PV_HighLow, point)
        mock_rule_func.assert_called_once_with(df_in, point=point)

    @patch('src.calculation.rules.apply_rule_support_resistants', autospec=True)
    def test_dispatcher_calls_support_resistants(self, mock_rule_func):
        df_in = self.df.copy()
        point = self.point
        apply_trading_rule(df_in, TradingRule.Support_Resistants, point)
        mock_rule_func.assert_called_once_with(df_in, point=point)

    @patch('src.calculation.rules.apply_rule_pressure_vector', autospec=True)
    def test_dispatcher_calls_pressure_vector(self, mock_rule_func):
        df_in = self.df.copy()
        point = self.point
        apply_trading_rule(df_in, TradingRule.Pressure_Vector, point)
        # Pressure_Vector rule function doesn't take point
        mock_rule_func.assert_called_once_with(df_in)

    # Test dispatcher with unrecognized rule (should default to Predict_High_Low_Direction)
    @patch('src.calculation.rules.logger')  # Mock logger inside rules.py
    @patch('src.calculation.rules.apply_rule_predict_hld')  # Mock the default rule func
    def test_apply_trading_rule_unrecognized_value(self, mock_default_rule_func, mock_logger):
        # Pass an integer value that is not a valid TradingRule member value
        invalid_rule_value = 99
        df_in = self.df.copy()
        point = self.point

        # Ensure the function doesn't crash and calls the default
        try:
            # We expect apply_trading_rule to handle the invalid enum value gracefully
            # by defaulting to Predict_High_Low_Direction
            apply_trading_rule(df_in, invalid_rule_value, point)  # Pass invalid value directly
        except Exception as e:
            self.fail(f"apply_trading_rule raised an exception unexpectedly for invalid value: {e}")

        # Check that the default rule was called
        mock_default_rule_func.assert_called_once_with(df_in, point=point)
        # Check that a warning was logged
        mock_logger.print_warning.assert_called()

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()