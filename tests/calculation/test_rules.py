# tests/calculation/test_rules.py

import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch

# Import functions and constants to test/use
from src.calculation.rules import (
    apply_rule_predict_hld,
    apply_rule_pv_highlow,
    apply_rule_support_resistants,
    apply_rule_pressure_vector,
    apply_trading_rule # Dispatcher
)
from src.common.constants import TradingRule, BUY, SELL, NOTRADE #, EMPTY_VALUE

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

    # Test apply_rule_predict_hld
    def test_apply_rule_predict_hld(self):
        df_result = apply_rule_predict_hld(self.df.copy(), self.point)

        # PPrice1 = Open - HL/2 * point
        # PPrice2 = Open + HL/2 * point
        # Direction = sign(PV)
        expected_pprice1 = pd.Series([100 - 100/2*0.1, 110 - 80/2*0.1, 120 - 120/2*0.1, 115 - 50/2*0.1, 125 - 90/2*0.1]) # [95, 106, 114, 112.5, 120.5]
        expected_pprice2 = pd.Series([100 + 100/2*0.1, 110 + 80/2*0.1, 120 + 120/2*0.1, 115 + 50/2*0.1, 125 + 90/2*0.1]) # [105, 114, 126, 117.5, 129.5]
        expected_direction = pd.Series([NOTRADE, BUY, SELL, NOTRADE, BUY]) # Based on PV sign (nan -> NOTRADE)

        pd.testing.assert_series_equal(df_result['PPrice1'], expected_pprice1, check_names=False)
        pd.testing.assert_series_equal(df_result['PPrice2'], expected_pprice2, check_names=False)
        pd.testing.assert_series_equal(df_result['Direction'], expected_direction, check_names=False)
        self.assertTrue((df_result['PColor1'] == BUY).all())
        self.assertTrue((df_result['PColor2'] == SELL).all())
        self.assertTrue(df_result['Diff'].isna().all()) # Diff should be EMPTY_VALUE (NaN)

    # Test apply_rule_pv_highlow
    def test_apply_rule_pv_highlow(self):
        df_result = apply_rule_pv_highlow(self.df.copy(), self.point)
        pv_e = 0.5 * np.log(np.pi)
        pv_term = np.power(pv_e, 3) * self.df['PV'] * self.point
        hl_term = self.df['HL'] * pv_e * self.point

        # PPrice1 = Open - (hl_term + pv_term)
        # PPrice2 = Open + (hl_term - pv_term)
        expected_pprice1 = self.df['Open'] - (hl_term + pv_term)
        expected_pprice2 = self.df['Open'] + (hl_term - pv_term)
        expected_direction = pd.Series([NOTRADE] * 5)

        # Fill NaNs resulting from pv_term NaN for comparison
        pd.testing.assert_series_equal(df_result['PPrice1'], expected_pprice1.fillna(self.df['Open']), check_names=False, check_dtype=False)
        pd.testing.assert_series_equal(df_result['PPrice2'], expected_pprice2.fillna(self.df['Open']), check_names=False, check_dtype=False)

        pd.testing.assert_series_equal(df_result['Direction'], expected_direction, check_names=False)
        self.assertTrue((df_result['PColor1'] == BUY).all())
        self.assertTrue((df_result['PColor2'] == SELL).all())
        self.assertTrue(df_result['Diff'].isna().all())

    # Test apply_rule_support_resistants
    def test_apply_rule_support_resistants(self):
        df_result = apply_rule_support_resistants(self.df.copy(), self.point)
        # Same PPrice calculation as predict_hld, but different Direction/Diff
        expected_pprice1 = pd.Series([95, 106, 114, 112.5, 120.5])
        expected_pprice2 = pd.Series([105, 114, 126, 117.5, 129.5])
        expected_direction = pd.Series([NOTRADE] * 5)

        pd.testing.assert_series_equal(df_result['PPrice1'], expected_pprice1, check_names=False)
        pd.testing.assert_series_equal(df_result['PPrice2'], expected_pprice2, check_names=False)
        pd.testing.assert_series_equal(df_result['Direction'], expected_direction, check_names=False)
        self.assertTrue((df_result['PColor1'] == BUY).all())
        self.assertTrue((df_result['PColor2'] == SELL).all())
        self.assertTrue(df_result['Diff'].isna().all())

    # Test apply_rule_pressure_vector
    def test_apply_rule_pressure_vector(self):
        df_result = apply_rule_pressure_vector(self.df.copy()) # Note: doesn't need point

        # PPrice1/2 = Open
        # PColor1/Direction = sign(PV)
        # PColor2/Diff = EMPTY
        expected_pprice1 = self.df['Open']
        expected_pprice2 = self.df['Open']
        expected_pcolor1 = pd.Series([NOTRADE, BUY, SELL, NOTRADE, BUY]) # Based on PV sign (nan -> NOTRADE)
        expected_direction = expected_pcolor1

        pd.testing.assert_series_equal(df_result['PPrice1'], expected_pprice1, check_names=False)
        pd.testing.assert_series_equal(df_result['PPrice2'], expected_pprice2, check_names=False)
        pd.testing.assert_series_equal(df_result['PColor1'], expected_pcolor1, check_names=False)
        pd.testing.assert_series_equal(df_result['Direction'], expected_direction, check_names=False)
        self.assertTrue(df_result['PColor2'].isna().all())
        self.assertTrue(df_result['Diff'].isna().all())

    # Test the dispatcher function apply_trading_rule
    @patch('src.calculation.rules.apply_rule_predict_hld')
    @patch('src.calculation.rules.apply_rule_pv_highlow')
    @patch('src.calculation.rules.apply_rule_support_resistants')
    @patch('src.calculation.rules.apply_rule_pressure_vector')
    def test_apply_trading_rule_dispatcher(self, mock_pv, mock_sr, mock_pvhl, mock_phld):
        # Test dispatching to each rule function
        df_in = self.df.copy()
        point = self.point

        apply_trading_rule(df_in, TradingRule.Predict_High_Low_Direction, point)
        mock_phld.assert_called_once_with(df_in, point=point)

        apply_trading_rule(df_in, TradingRule.PV_HighLow, point)
        mock_pvhl.assert_called_once_with(df_in, point=point)

        apply_trading_rule(df_in, TradingRule.Support_Resistants, point)
        mock_sr.assert_called_once_with(df_in, point=point)

        apply_trading_rule(df_in, TradingRule.Pressure_Vector, point) # Point is passed but ignored by func
        mock_pv.assert_called_once_with(df_in)


    # Test dispatcher with unrecognized rule (should default to Predict_High_Low_Direction)
    @patch('src.calculation.rules.logger') # Mock logger inside rules.py
    @patch('src.calculation.rules.apply_rule_predict_hld') # Mock the default rule func
    def test_apply_trading_rule_unrecognized(self, mock_default_rule_func, mock_logger):
        class UnrecognizedRule(TradingRule): # Create a dummy enum member locally
             Unknown = 99
        df_in = self.df.copy()
        point = self.point

        apply_trading_rule(df_in, UnrecognizedRule.Unknown, point)
        # Check that the default rule was called
        mock_default_rule_func.assert_called_once_with(df_in, point=point)
        # Check that a warning was logged
        mock_logger.print_warning.assert_called()

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()