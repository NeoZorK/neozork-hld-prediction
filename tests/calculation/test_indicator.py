# tests/calculation/test_indicator.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

# Import the main function to test
from src.calculation.indicator import calculate_pressure_vector
# Import dependencies to mock or use
from src.common.constants import TradingRule, BUY, SELL, NOTRADE, EMPTY_VALUE
from src.calculation import core_calculations, rules

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass

# Unit tests for the main indicator calculation orchestrator
class TestIndicatorCalculation(unittest.TestCase):

    # Basic setup with required columns
    def setUp(self):
        self.df_input = pd.DataFrame({
            'Open':     [100, 110, 120, 115, 125],
            'High':     [105, 115, 125, 120, 130],
            'Low':      [ 95, 105, 115, 110, 120],
            'Close':    [102, 112, 118, 116, 128],
            'TickVolume':[1000,1200,1100,1300,1500], # Input column name
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']))
        self.point = 0.1

    # Test with invalid input DataFrame (missing columns)
    @patch('src.calculation.indicator.logger', new_callable=MockLogger)
    def test_calculate_pv_missing_columns(self, mock_logger):
        df_missing = self.df_input.drop(columns=['Low', 'TickVolume'])
        with self.assertRaises(ValueError) as cm:
            calculate_pressure_vector(df_missing, self.point, TradingRule.Predict_High_Low_Direction)
        self.assertIn("Input DataFrame must contain columns:", str(cm.exception))

    # Test with zero point size
    @patch('src.calculation.indicator.logger', new_callable=MockLogger)
    def test_calculate_pv_zero_point(self, mock_logger):
        with self.assertRaises(ValueError) as cm:
            calculate_pressure_vector(self.df_input, 0, TradingRule.Predict_High_Low_Direction)
        self.assertIn("Point size cannot be zero", str(cm.exception))

    # Test calculation flow with Predict_High_Low_Direction rule
    # Mock the core calculation and rule application steps to verify interaction
    @patch('src.calculation.indicator.logger', new_callable=MockLogger)
    @patch('src.calculation.indicator.calculate_hl')
    @patch('src.calculation.indicator.calculate_pressure')
    @patch('src.calculation.indicator.calculate_pv')
    @patch('src.calculation.indicator.apply_trading_rule')
    def test_calculate_pv_flow_predict_hld(self, mock_apply_rule, mock_calc_pv, mock_calc_pressure, mock_calc_hl, mock_logger):
        # --- Setup Mocks ---
        # Make mock functions return series with correct index and some dummy data
        mock_hl = pd.Series([100, 80, 120, 50, 90], index=self.df_input.index, dtype=float)
        mock_pressure = pd.Series([np.nan, 6.0, 5.0, 3.25, 8.0], index=self.df_input.index, dtype=float)
        mock_pv = pd.Series([np.nan, np.nan, -1.0, -1.75, 4.75], index=self.df_input.index, dtype=float)
        mock_calc_hl.return_value = mock_hl
        mock_calc_pressure.return_value = mock_pressure
        mock_calc_pv.return_value = mock_pv

        # Mock apply_trading_rule to return a DataFrame with expected rule outputs
        # Create a base DF with intermediate calcs + initial rule outputs
        df_intermediate = self.df_input.rename(columns={'TickVolume': 'Volume'})
        df_intermediate['HL'] = mock_hl
        df_intermediate['Pressure'] = mock_pressure
        df_intermediate['PV'] = mock_pv
        df_intermediate['PPrice1'] = df_intermediate['Open']
        df_intermediate['PColor1'] = EMPTY_VALUE
        df_intermediate['PPrice2'] = df_intermediate['Open']
        df_intermediate['PColor2'] = EMPTY_VALUE
        df_intermediate['Direction'] = EMPTY_VALUE
        df_intermediate['Diff'] = EMPTY_VALUE

        # Simulate rule application modifying the df_intermediate
        df_rule_applied = df_intermediate.copy()
        df_rule_applied['PPrice1'] = pd.Series([95, 106, 114, 112.5, 120.5], index=self.df_input.index)
        df_rule_applied['PPrice2'] = pd.Series([105, 114, 126, 117.5, 129.5], index=self.df_input.index)
        df_rule_applied['Direction'] = pd.Series([NOTRADE, BUY, SELL, SELL, BUY], index=self.df_input.index) # Example based on mocked PV
        df_rule_applied['PColor1'] = BUY
        df_rule_applied['PColor2'] = SELL
        mock_apply_rule.return_value = df_rule_applied # Return the modified DF

        # --- Execute Function ---
        rule_to_test = TradingRule.Predict_High_Low_Direction
        result_df = calculate_pressure_vector(self.df_input, self.point, rule_to_test)

        # --- Assertions ---
        # 1. Check if core calculations were called correctly
        #    Need access to the shifted series used internally
        high_prev = self.df_input['High'].shift(1)
        low_prev = self.df_input['Low'].shift(1)
        volume_prev = self.df_input['TickVolume'].shift(1) # Original name before rename
        hl_prev2 = mock_hl.shift(1) # HL as calculated
        pressure_prev = mock_pressure.shift(1) # Pressure as calculated

        mock_calc_hl.assert_called_once()
        # Need to compare series properly in call assertion
        pd.testing.assert_series_equal(mock_calc_hl.call_args[0][0], high_prev, check_names=False)
        pd.testing.assert_series_equal(mock_calc_hl.call_args[0][1], low_prev, check_names=False)
        self.assertEqual(mock_calc_hl.call_args[0][2], self.point)

        mock_calc_pressure.assert_called_once()
        pd.testing.assert_series_equal(mock_calc_pressure.call_args[0][0], volume_prev, check_names=False)
        pd.testing.assert_series_equal(mock_calc_pressure.call_args[0][1], hl_prev2, check_names=False)

        mock_calc_pv.assert_called_once()
        pd.testing.assert_series_equal(mock_calc_pv.call_args[0][0], mock_pressure, check_names=False)
        pd.testing.assert_series_equal(mock_calc_pv.call_args[0][1], pressure_prev, check_names=False)

        # 2. Check if apply_trading_rule was called correctly
        mock_apply_rule.assert_called_once()
        # The first arg to apply_trading_rule is the DataFrame *after* core calcs were added
        # Check if the DataFrame passed to the rule function had the core calc columns
        call_df = mock_apply_rule.call_args[0][0]
        self.assertIn('HL', call_df.columns)
        self.assertIn('Pressure', call_df.columns)
        self.assertIn('PV', call_df.columns)
        pd.testing.assert_series_equal(call_df['HL'], mock_hl)
        # Check other args
        self.assertEqual(mock_apply_rule.call_args[0][1], rule_to_test)
        self.assertEqual(mock_apply_rule.call_args[0][2], self.point)


        # 3. Check final output DataFrame structure and content
        expected_cols = [
            'Open', 'High', 'Low', 'Close', 'Volume', # Original renamed
            'HL', 'Pressure', 'PV',                  # Intermediate
            'PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff' # Final Outputs
        ]
        self.assertListEqual(list(result_df.columns), expected_cols)
        self.assertEqual(result_df.shape[0], self.df_input.shape[0])

        # Verify specific values from the mocked rule application (after NaN replacement)
        pd.testing.assert_series_equal(result_df['PPrice1'], df_rule_applied['PPrice1'], check_names=False)
        pd.testing.assert_series_equal(result_df['Direction'], df_rule_applied['Direction'], check_names=False)
        pd.testing.assert_series_equal(result_df['PV'], mock_pv, check_names=False) # Check intermediate is preserved
        self.assertTrue(result_df['Diff'].isna().all()) # Check EMPTY_VALUE became NaN

    # Test index type warning
    @patch('src.calculation.indicator.logger') # Patch logger directly this time
    def test_calculate_pv_non_datetime_index(self, mock_logger_instance):
        df_non_dt_index = self.df_input.reset_index() # Use default integer index
        # Ensure required columns still exist after reset_index
        df_non_dt_index.rename(columns={'index': 'DateTime'}, inplace=True) # Keep a time col, just not index

        # Use real calculations this time, just check the warning
        result_df = calculate_pressure_vector(df_non_dt_index, self.point, TradingRule.Support_Resistants)

        self.assertIsInstance(result_df, pd.DataFrame) # Should still calculate
        mock_logger_instance.print_warning.assert_called_once()
        self.assertIn("index is not a DatetimeIndex", mock_logger_instance.print_warning.call_args[0][0])


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()