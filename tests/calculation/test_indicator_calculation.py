# tests/calculation/test_indicator_calculation.py

import unittest
from unittest.mock import patch #, MagicMock, ANY
import argparse
import pandas as pd
import io
#import numpy as np

# Import the function to test
from src.calculation.indicator_calculation import calculate_indicator
# Import dependencies to mock or use
from src.common.constants import TradingRule

# Create a dummy args namespace
def create_mock_args(rule='PHLD'): # Default to an alias
    return argparse.Namespace(rule=rule)

# Unit tests for the indicator calculation workflow step
class TestIndicatorCalculationStep(unittest.TestCase):

    # Setup basic data
    def setUp(self):
        self.ohlcv_df = pd.DataFrame({
            'Open':     [100, 110, 120],
            'High':     [105, 115, 125],
            'Low':      [ 95, 105, 115],
            'Close':    [102, 112, 118],
            'Volume':   [1000,1200,1100], # Input name from data acquisition
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']))
        self.point_size = 0.1

    # Test successful calculation with a valid rule alias
    @patch('src.calculation.indicator_calculation.logger')
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_success_alias(self, mock_calc_pv_func, _):
        args = create_mock_args(rule='PHLD') # Use alias
        expected_rule_enum = TradingRule.Predict_High_Low_Direction
        # Mock the main calculation function to return a dummy DataFrame
        mock_result_df = pd.DataFrame({'Close': [102, 112, 118]}) # Dummy result
        mock_calc_pv_func.return_value = mock_result_df

        result_df, selected_rule = calculate_indicator(args, self.ohlcv_df, self.point_size)

        # Assertions
        self.assertTrue(result_df.equals(mock_result_df))
        self.assertEqual(selected_rule, expected_rule_enum)

        # Check that the main calculation function was called correctly
        mock_calc_pv_func.assert_called_once()
        call_args = mock_calc_pv_func.call_args[1] # Keyword arguments
        call_df = call_args['df']
        # Verify input DataFrame had 'Volume' renamed to 'TickVolume' before passing
        self.assertIn('TickVolume', call_df.columns)
        self.assertNotIn('Volume', call_df.columns)
        # Check other arguments passed to the main function
        self.assertEqual(call_args['point'], self.point_size)
        self.assertEqual(call_args['tr_num'], expected_rule_enum)


    # Test successful calculation with a direct enum name
    @patch('src.calculation.indicator_calculation.logger')
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_success_direct_name(self, mock_calc_pv_func, _):
        rule_name = 'PV_HighLow'
        args = create_mock_args(rule=rule_name)
        expected_rule_enum = TradingRule.PV_HighLow
        mock_result_df = pd.DataFrame({'Close': [1, 2, 3]})
        mock_calc_pv_func.return_value = mock_result_df

        result_df, selected_rule = calculate_indicator(args, self.ohlcv_df, self.point_size)

        self.assertTrue(result_df.equals(mock_result_df))
        self.assertEqual(selected_rule, expected_rule_enum)
        mock_calc_pv_func.assert_called_once()
        self.assertEqual(mock_calc_pv_func.call_args[1]['tr_num'], expected_rule_enum)

    # Test with invalid rule name
    @patch('src.calculation.indicator_calculation.logger')
    def test_calculate_indicator_invalid_rule(self, _):
        args = create_mock_args(rule='InvalidRuleName')
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, self.ohlcv_df, self.point_size)
        self.assertIn("Invalid rule name or alias 'InvalidRuleName'", str(cm.exception))

    # Test with missing required columns in input DataFrame
    @patch('src.calculation.indicator_calculation.logger')
    def test_calculate_indicator_missing_columns(self, _):
        args = create_mock_args()
        df_missing = self.ohlcv_df.drop(columns=['High'])
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, df_missing, self.point_size)
        self.assertIn("DataFrame missing required columns:", str(cm.exception))
        self.assertIn("'High'", str(cm.exception)) # Check specific missing col

    # Test with None DataFrame input
    @patch('src.calculation.indicator_calculation.logger')
    def test_calculate_indicator_none_dataframe(self, _):
        args = create_mock_args()
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, None, self.point_size) # type: ignore
        self.assertIn("No data available for calculation", str(cm.exception))

    # Test with empty DataFrame input
    @patch('src.calculation.indicator_calculation.logger')
    def test_calculate_indicator_empty_dataframe(self, _):
        args = create_mock_args()
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, pd.DataFrame(), self.point_size)
        self.assertIn("No data available for calculation", str(cm.exception))

    # Test with None point size input
    @patch('src.calculation.indicator_calculation.logger')
    def test_calculate_indicator_none_point_size(self, _):
        args = create_mock_args()
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, self.ohlcv_df, None) # type: ignore
        self.assertIn("Point size is None", str(cm.exception))

    # Test when calculation function itself raises an error
    @patch('src.calculation.indicator_calculation.logger')
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_calc_exception(self, mock_calc_pv_func, _):
        args = create_mock_args()
        mock_calc_pv_func.side_effect = RuntimeError("Calculation failed inside")

        with self.assertRaises(RuntimeError) as cm: # Should re-raise the original exception
            calculate_indicator(args, self.ohlcv_df, self.point_size)
        self.assertIn("Calculation failed inside", str(cm.exception))

    # Test when calculation function returns None or empty (should log warning but not fail step)
    @patch('src.calculation.indicator_calculation.logger') # Use MagicMock for logger to check calls
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_calc_returns_none(self, mock_calc_pv_func, __instance):
        args = create_mock_args()
        mock_calc_pv_func.return_value = None # Simulate calculation returning None

        result_df, selected_rule = calculate_indicator(args, self.ohlcv_df, self.point_size)

        self.assertIsNone(result_df)
        self.assertEqual(selected_rule, TradingRule.Predict_High_Low_Direction) # Should still return selected rule
        __instance.print_warning.assert_called_once_with("Indicator calculation returned None or empty DataFrame.")

    @patch('src.calculation.indicator_calculation.logger')
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_calc_returns_empty(self, mock_calc_pv_func, __instance):
        args = create_mock_args(rule='Pressure_Vector')
        mock_calc_pv_func.return_value = pd.DataFrame() # Simulate calculation returning empty DF

        result_df, selected_rule = calculate_indicator(args, self.ohlcv_df, self.point_size)

        self.assertTrue(result_df.empty)
        self.assertEqual(selected_rule, TradingRule.Pressure_Vector)
        __instance.print_warning.assert_called_once_with("Indicator calculation returned None or empty DataFrame.")
        # Check debug print is not attempted for empty df
        debug_calls = [call for call in __instance.print_debug.call_args_list if "DEBUG: Result DF Tail" in str(call)]
        self.assertEqual(len(debug_calls), 0)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    # Mock the logger to capture print statements
    def test_calculate_indicator_debug_print(self, mock_calc_pv_func, mock_stdout):
        args = create_mock_args()
        mock_result_df = pd.DataFrame({
            'Open': [100, 110], 'PPrice1': [99, 109], 'PPrice2': [101, 111],
            'Direction': [1.0, 0.0], 'PColor1': [1.0, 1.0], 'PColor2': [2.0, 2.0]
        })
        mock_calc_pv_func.return_value = mock_result_df

        try:
            calculate_indicator(args, self.ohlcv_df, self.point_size)
            output = mock_stdout.getvalue()
            lines_with_debug = [line for line in output.splitlines() if "Debug: " in line]
            self.assertTrue(len(lines_with_debug) > 0,
                            "No 'Debug: ' prefix found in stdout, logger.print_debug likely wasn't called.")

        except Exception as e:
            self.fail(f"calculate_indicator failed unexpectedly during logging test: {e}")

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()