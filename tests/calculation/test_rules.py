# tests/calculation/test_rules.py

import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch , MagicMock

# Import functions and constants to test/use
from src.calculation.rules import (
    apply_trading_rule, # Dispatcher
    RULE_DISPATCHER
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


    # Test the dispatcher function
    def test_dispatcher_calls_correct_function(self):
        df_in = self.df.copy()
        point = self.point

        # Create mock functions for each rule
        mock_phld = MagicMock(name='mock_phld')
        mock_pvhl = MagicMock(name='mock_pvhl')
        mock_sr = MagicMock(name='mock_sr')
        mock_pv = MagicMock(name='mock_pv')

        # Patch the RULE_DISPATCHER to use our mocks
        with patch.dict(RULE_DISPATCHER, {
            TradingRule.Predict_High_Low_Direction: mock_phld,
            TradingRule.PV_HighLow: mock_pvhl,
            TradingRule.Support_Resistants: mock_sr,
            TradingRule.Pressure_Vector: mock_pv,
        }):
            # Call the dispatcher with different rules
            apply_trading_rule(df_in, TradingRule.Predict_High_Low_Direction, point)
            apply_trading_rule(df_in, TradingRule.PV_HighLow, point)
            apply_trading_rule(df_in, TradingRule.Support_Resistants, point)
            apply_trading_rule(df_in, TradingRule.Pressure_Vector, point)

        # Check that each rule function was called with the correct arguments
        mock_phld.assert_called_once_with(df_in, point=point)
        mock_pvhl.assert_called_once_with(df_in, point=point)
        mock_sr.assert_called_once_with(df_in, point=point)
        mock_pv.assert_called_once_with(df_in, point=point)

    # Test dispatcher with unrecognized rule (should default to Predict_High_Low_Direction)
    @patch('src.calculation.rules.logger')  # Mock logger inside rules.py
    def test_apply_trading_rule_unrecognized_value(self, mock_logger):
        invalid_rule_value = 99
        df_in = self.df.copy()
        point = self.point

        # Mock the default rule function
        original_default_func = RULE_DISPATCHER[TradingRule.Predict_High_Low_Direction]
        mock_default_rule_func = MagicMock()
        RULE_DISPATCHER[TradingRule.Predict_High_Low_Direction] = mock_default_rule_func

        try:
            apply_trading_rule(df_in, invalid_rule_value, point)
            mock_default_rule_func.assert_called_once_with(df_in, point=point)
            mock_logger.print_warning.assert_called()
        except Exception as e:
            self.fail(f"apply_trading_rule raised an exception unexpectedly: {e}")
        finally:
            RULE_DISPATCHER[TradingRule.Predict_High_Low_Direction] = original_default_func


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()