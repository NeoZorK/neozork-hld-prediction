# tests/calculation/test_indicator_calculation.py # MODIFIED - Fixed logger mocking and assertion

import unittest
from unittest.mock import patch #, MagicMock, ANY
import argparse
import pandas as pd
# Remove io import if mock_stdout test is removed or refactored
# import io
import numpy as np # Keep numpy if needed for test data setup

# Import the function to test
from src.calculation.indicator_calculation import calculate_indicator
# Import dependencies to mock or use
from src.common.constants import TradingRule

# No longer need MockLogger if we patch methods directly

# Create a dummy args namespace helper function
# *** FIX: Added 'mode' with a default value ***
def create_mock_args(rule='PHLD', mode='demo'): # Add mode with default
    # Include other args if calculate_indicator starts checking them
    return argparse.Namespace(rule=rule, mode=mode) # Add mode here


# Unit tests for the indicator calculation workflow step
class TestIndicatorCalculationStep(unittest.TestCase):

    # Setup basic data
    def setUp(self):
        # Reduced size for simplicity, ensure enough data for calculations if needed
        self.ohlcv_df = pd.DataFrame({
            'Open':     [100, 110, 120, 130],
            'High':     [105, 115, 125, 135],
            'Low':      [ 95, 105, 115, 125],
            'Close':    [102, 112, 118, 128],
            'Volume':   [1000, 1200, 1100, 1300],
            # Add original MQL5 columns needed for validation test
            'pressure':        [10.1, 10.2, 10.3, 10.4],
            'pressure_vector': [ 0.1, -0.1,  0.2, -0.2],
            'predicted_low':   [ 98,  108,  118, 128],
            'predicted_high':  [103,  113,  123, 133]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']))
        self.point_size = 0.1

    # Test successful calculation with a valid rule alias
    # Patch only the necessary dependency for this test
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_success_alias(self, mock_calc_pv_func):
        args = create_mock_args(rule='PHLD') # Uses alias, mode='demo' default
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
    def test_calculate_indicator_success_direct_name(self, mock_calc_pv_func):
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
    def test_calculate_indicator_invalid_rule(self):
        args = create_mock_args(rule='InvalidRuleName') # mode='demo' default
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, self.ohlcv_df, self.point_size)
        self.assertIn("Invalid rule name or alias 'InvalidRuleName'", str(cm.exception))

    # Test with missing required columns in input DataFrame
    def test_calculate_indicator_missing_columns(self):
        args = create_mock_args() # mode='demo' default
        df_missing = self.ohlcv_df.drop(columns=['High'])
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, df_missing, self.point_size)
        # *** FIX: Update assertion string to match actual error ***
        self.assertIn("DataFrame missing required columns for calculation:", str(cm.exception))
        self.assertIn("'High'", str(cm.exception))

    # Test with None DataFrame input
    def test_calculate_indicator_none_dataframe(self):
        args = create_mock_args() # mode='demo' default
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, None, self.point_size) # type: ignore
        self.assertIn("No data available for calculation", str(cm.exception))

    # Test with empty DataFrame input
    def test_calculate_indicator_empty_dataframe(self):
        args = create_mock_args() # mode='demo' default
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, pd.DataFrame(), self.point_size)
        self.assertIn("No data available for calculation", str(cm.exception))

    # Test with None point size input
    def test_calculate_indicator_none_point_size(self):
        args = create_mock_args() # mode='demo' default
        with self.assertRaises(ValueError) as cm:
            calculate_indicator(args, self.ohlcv_df, None) # type: ignore
        self.assertIn("Point size is None", str(cm.exception))

    # Test when calculation function itself raises an error
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_calc_exception(self, mock_calc_pv_func):
        args = create_mock_args() # mode='demo' default
        mock_calc_pv_func.side_effect = RuntimeError("Calculation failed inside")

        with self.assertRaises(RuntimeError) as cm:
            calculate_indicator(args, self.ohlcv_df, self.point_size)
        self.assertIn("Calculation failed inside", str(cm.exception))

    # Test when calculation function returns None
    # *** FIX: Patch logger.print_warning directly ***
    @patch('src.calculation.indicator_calculation.logger.print_warning')
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_calc_returns_none(self, mock_calc_pv_func, mock_print_warning): # mock is now specific method
        args = create_mock_args() # mode='demo' default
        mock_calc_pv_func.return_value = None

        result_df, selected_rule = calculate_indicator(args, self.ohlcv_df, self.point_size)

        self.assertIsNone(result_df)
        self.assertEqual(selected_rule, TradingRule.Predict_High_Low_Direction)
        # *** FIX: Assert on the specific mocked method ***
        mock_print_warning.assert_called_once_with("Indicator calculation returned None or empty DataFrame.")

    # Test when calculation function returns empty
    # *** FIX: Patch logger.print_warning directly ***
    @patch('src.calculation.indicator_calculation.logger.print_warning')
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_calc_returns_empty(self, mock_calc_pv_func, mock_print_warning): # mock is specific method
        args = create_mock_args(rule='Pressure_Vector') # mode='demo' default
        mock_calc_pv_func.return_value = pd.DataFrame()

        result_df, selected_rule = calculate_indicator(args, self.ohlcv_df, self.point_size)

        self.assertTrue(result_df.empty)
        self.assertEqual(selected_rule, TradingRule.Pressure_Vector)
        # *** FIX: Assert on the specific mocked method ***
        mock_print_warning.assert_called_once_with("Indicator calculation returned None or empty DataFrame.")

    # Test validation logic execution in CSV mode
    # *** FIX: Patch specific logger methods needed ***
    @patch('src.calculation.indicator_calculation.logger.print_info')
    @patch('numpy.isclose', return_value=np.array([True])) # Keep isclose mock simple
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_csv_validation_called(self, mock_calc_pv_func, mock_isclose, mock_print_info):
        # Create args for CSV mode
        args = create_mock_args(mode='csv') # Set mode to CSV
        mock_result_df = self.ohlcv_df.copy() # Use existing df structure
        mock_result_df['Pressure'] = 10.1 # Ensure calc columns exist
        mock_result_df['PV'] = 0.1
        mock_calc_pv_func.return_value = mock_result_df

        calculate_indicator(args, self.ohlcv_df, self.point_size)

        # Assert that validation info was printed via the mocked print_info
        # Check if ANY call to print_info contains the expected string
        # *** FIX: Check call_args_list on the mocked method ***
        found_header = False
        found_pressure = False
        for call_args in mock_print_info.call_args_list:
            log_message = call_args[0][0] # First positional argument of the call
            if "--- Indicator Calculation Validation (CSV Mode) ---" in log_message:
                found_header = True
            if "Pressure Comparison:" in log_message:
                found_pressure = True
        self.assertTrue(found_header, "Validation header log not found")
        self.assertTrue(found_pressure, "Pressure comparison log not found")
        # Check isclose was called
        self.assertTrue(mock_isclose.called)


    # Test debug print output
    # *** FIX: Patch logger.print_debug directly ***
    @patch('src.calculation.indicator_calculation.logger.print_debug')
    @patch('src.calculation.indicator_calculation.calculate_pressure_vector')
    def test_calculate_indicator_debug_print(self, mock_calc_pv_func, mock_print_debug):
        args = create_mock_args() # mode='demo' default
        mock_result_df = pd.DataFrame({
            'Open': [100, 110], 'PPrice1': [99, 109], 'PPrice2': [101, 111],
            'Direction': [1.0, 0.0], 'PColor1': [1.0, 1.0], 'PColor2': [2.0, 2.0]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02']))
        mock_calc_pv_func.return_value = mock_result_df

        calculate_indicator(args, self.ohlcv_df.head(2), self.point_size)

        # Check if print_debug was called with the expected strings
        # *** FIX: Check call_args_list on the mocked method ***
        debug_log_calls = [str(c.args[0]) for c in mock_print_debug.call_args_list] # Extract first arg from calls
        self.assertTrue(any("DEBUG: Result DF Tail for Rule:" in call for call in debug_log_calls), "Debug tail header not logged")
        self.assertTrue(any("--- END DEBUG ---" in call for call in debug_log_calls), "Debug tail footer not logged")
        self.assertTrue(any("PPrice1" in call for call in debug_log_calls), "PPrice1 column not found in debug log")

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()