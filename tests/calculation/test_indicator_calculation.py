# tests/calculation/test_indicator_calculation.py # MODIFIED

import unittest
from unittest.mock import patch # Import ANY if needed for call matching
import argparse
import pandas as pd
import numpy as np # Import numpy if needed for creating test data

# Import the function to test
from src.calculation.indicator_calculation import calculate_indicator
# Import dependencies to mock or use
from src.common.constants import TradingRule

# Dummy logger class
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass
    def print_success(self, msg): pass

# Create a dummy args namespace
# *** FIX: Added 'mode' with a default value ***
def create_mock_args(rule='PHLD', mode='demo'): # Add mode with default
    return argparse.Namespace(rule=rule, mode=mode) # Add mode here

# Unit tests for the indicator calculation workflow step
# Patch logger for the whole class
@patch('src.calculation.indicator_calculation.logger', new_callable=MockLogger)
class TestIndicatorCalculationStep(unittest.TestCase):

    # Setup basic data
    def setUp(self):
        # Basic OHLCV data for testing calculation calls
        self.ohlcv_df = pd.DataFrame({
            'Open':     [100, 110, 120, 130],
            'High':     [105, 115, 125, 135],
            'Low':      [ 95, 105, 115, 125],
            'Close':    [102, 112, 118, 128],
            'Volume':   [1000, 1200, 1100, 1300], # Input name from data acquisition
            # Add original MQL5 columns needed for validation test (if we add one)
            'pressure':        [10.1, 10.2, 10.3, 10.4],
            'pressure_vector': [ 0.1, -0.1,  0.2, -0.2],
            'predicted_low':   [ 98,  108,  118, 128],
            'predicted_high':  [103,  113,  123, 133]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']))
        self.point_size = 0.1

    # Test successful calculation with a valid rule alias
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_success_alias(self, mock_calc_pv_func, _):
        # Args will have mode='demo' by default from create_mock_args
        args = create_mock_args(rule='PHLD') # Use alias
        expected_rule_enum = TradingRule.Predict_High_Low_Direction
        mock_result_df = pd.DataFrame({'Close': [102, 112, 118, 128]})
        mock_calc_pv_func.return_value = mock_result_df

        result_df, selected_rule = calculate_indicator(args, self.ohlcv_df, self.point_size)

        self.assertTrue(result_df.equals(mock_result_df))
        self.assertEqual(selected_rule, expected_rule_enum)
        mock_calc_pv_func.assert_called_once()
        call_args = mock_calc_pv_func.call_args[1]
        call_df = call_args['df']
        self.assertIn('TickVolume', call_df.columns)
        self.assertNotIn('Volume', call_df.columns)
        self.assertEqual(call_args['point'], self.point_size)
        self.assertEqual(call_args['tr_num'], expected_rule_enum)


    # Test successful calculation with a direct enum name
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_success_direct_name(self, mock_calc_pv_func, _):
        rule_name = 'PV_HighLow'
        args = create_mock_args(rule=rule_name) # mode='demo' default
        expected_rule_enum = TradingRule.PV_HighLow
        mock_result_df = pd.DataFrame({'Close': [1, 2, 3, 4]})
        mock_calc_pv_func.return_value = mock_result_df

        result_df, selected_rule = calculate_indicator(args, self.ohlcv_df, self.point_size)

        self.assertTrue(result_df.equals(mock_result_df))
        self.assertEqual(selected_rule, expected_rule_enum)
        mock_calc_pv_func.assert_called_once()
        self.assertEqual(mock_calc_pv_func.call_args[1]['tr_num'], expected_rule_enum)

    # Test with invalid rule name
    def test_calculate_indicator_invalid_rule(self, _):
        args = create_mock_args(rule='InvalidRuleName') # mode='demo' default
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, self.ohlcv_df, self.point_size)
        self.assertIn("Invalid rule name or alias 'InvalidRuleName'", str(cm.exception))

    # Test with missing required columns in input DataFrame
    def test_calculate_indicator_missing_columns(self, _):
        args = create_mock_args() # mode='demo' default
        df_missing = self.ohlcv_df.drop(columns=['High']) # Drop 'High' for test
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, df_missing, self.point_size)
        # *** FIX: Update assertion string to match actual error ***
        self.assertIn("DataFrame missing required columns for calculation:", str(cm.exception))
        self.assertIn("'High'", str(cm.exception)) # Check specific missing col is mentioned

    # Test with None DataFrame input
    def test_calculate_indicator_none_dataframe(self, _):
        args = create_mock_args() # mode='demo' default
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, None, self.point_size) # type: ignore
        self.assertIn("No data available for calculation", str(cm.exception))

    # Test with empty DataFrame input
    def test_calculate_indicator_empty_dataframe(self, _):
        args = create_mock_args() # mode='demo' default
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, pd.DataFrame(), self.point_size)
        self.assertIn("No data available for calculation", str(cm.exception))

    # Test with None point size input
    def test_calculate_indicator_none_point_size(self, _):
        args = create_mock_args() # mode='demo' default
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, self.ohlcv_df, None) # type: ignore
        self.assertIn("Point size is None", str(cm.exception))

    # Test when calculation function itself raises an error
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_calc_exception(self, mock_calc_pv_func, _):
        args = create_mock_args() # mode='demo' default
        mock_calc_pv_func.side_effect = RuntimeError("Calculation failed inside")

        with self.assertRaises(RuntimeError) as cm: # Should re-raise the original exception
            calculate_indicator(args, self.ohlcv_df, self.point_size)
        self.assertIn("Calculation failed inside", str(cm.exception))

    # Test when calculation function returns None or empty (should log warning but not fail step)
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_calc_returns_none(self, mock_calc_pv_func, mock_logger_instance):
        args = create_mock_args() # mode='demo' default
        mock_calc_pv_func.return_value = None # Simulate calculation returning None

        result_df, selected_rule = calculate_indicator(args, self.ohlcv_df, self.point_size)

        self.assertIsNone(result_df)
        self.assertEqual(selected_rule, TradingRule.Predict_High_Low_Direction) # Should still return selected rule
        # Check logger warning
        mock_logger_instance.print_warning.assert_called_with("Indicator calculation returned None or empty DataFrame.")

    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_calc_returns_empty(self, mock_calc_pv_func, mock_logger_instance):
        args = create_mock_args(rule='Pressure_Vector') # mode='demo' default
        mock_calc_pv_func.return_value = pd.DataFrame() # Simulate calculation returning empty DF

        result_df, selected_rule = calculate_indicator(args, self.ohlcv_df, self.point_size)

        self.assertTrue(result_df.empty)
        self.assertEqual(selected_rule, TradingRule.Pressure_Vector)
        mock_logger_instance.print_warning.assert_called_with("Indicator calculation returned None or empty DataFrame.")
        # Check debug print is not attempted for empty df
        debug_calls = [c for c in mock_logger_instance.print_debug.call_args_list if "DEBUG: Result DF Tail" in str(c)]
        self.assertEqual(len(debug_calls), 0)

    # Test validation logic execution in CSV mode (optional, can be expanded)
    @patch('numpy.isclose') # Mock isclose to avoid float precision issues in test setup
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_csv_validation_called(self, mock_calc_pv_func, mock_isclose, mock_logger_instance):
        # Create args for CSV mode
        args = create_mock_args(mode='csv')
        # Mock result includes Pressure and PV columns
        mock_result_df = self.ohlcv_df.copy()
        mock_result_df['Pressure'] = 10 # Dummy calculated data
        mock_result_df['PV'] = 0.5    # Dummy calculated data
        mock_calc_pv_func.return_value = mock_result_df
        # Mock isclose to always return True for simplicity in this test
        mock_isclose.return_value = np.array([True] * len(self.ohlcv_df))

        # Input DataFrame already has MQL5 columns from setUp
        calculate_indicator(args, self.ohlcv_df, self.point_size)

        # Assert that validation info was printed (check for specific log messages)
        log_calls = [str(c) for c in mock_logger_instance.print_info.call_args_list]
        self.assertTrue(any("--- Indicator Calculation Validation (CSV Mode) ---" in call for call in log_calls))
        self.assertTrue(any("Pressure Comparison:" in call for call in log_calls))
        self.assertTrue(any("PV (Pressure Vector) Comparison:" in call for call in log_calls))
        # Check isclose was called (might need more specific arg checking if needed)
        self.assertTrue(mock_isclose.called)


    # Test debug print output (Modified slightly for better mocking check)
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_debug_print(self, mock_calc_pv_func, mock_logger_instance):
        args = create_mock_args() # mode='demo' default
        mock_result_df = pd.DataFrame({
            'Open': [100, 110], 'PPrice1': [99, 109], 'PPrice2': [101, 111],
            'Direction': [1.0, 0.0], 'PColor1': [1.0, 1.0], 'PColor2': [2.0, 2.0]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02'])) # Need index for tail()
        mock_calc_pv_func.return_value = mock_result_df

        calculate_indicator(args, self.ohlcv_df.head(2), self.point_size) # Use head(2) to match mock result size

        # Check if print_debug was called with the expected header/footer
        debug_calls_str = "\n".join([str(c) for c in mock_logger_instance.print_debug.call_args_list])
        self.assertIn("DEBUG: Result DF Tail for Rule:", debug_calls_str)
        self.assertIn("--- END DEBUG ---", debug_calls_str)
        self.assertIn("PPrice1", debug_calls_str) # Check if expected col name is in the logged string


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()