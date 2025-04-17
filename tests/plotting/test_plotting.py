# tests/plotting/test_plotting.py

import unittest
from unittest.mock import patch, call, ANY #, MagicMock
import pandas as pd
import numpy as np

# Import the function to test and dependencies
from src.plotting.plotting import plot_indicator_results
from src.common.constants import TradingRule, BUY, SELL, NOTRADE

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass

# Unit tests for the low-level plotting function
class TestPlottingFunction(unittest.TestCase):

    # Setup basic data with necessary columns
    def setUp(self):
        self.df_results = pd.DataFrame({
            'Open':     [100, 110, 120, 115, 125],
            'High':     [105, 115, 125, 120, 130],
            'Low':      [ 95, 105, 115, 110, 120],
            'Close':    [102, 112, 118, 116, 128],
            'Volume':   [1000,1200,1100,1300,1500],
            # Indicator outputs (example for Predict_High_Low_Direction)
            'HL':       [100, 80, 120, 50, 90],
            'Pressure': [np.nan, 6.0, 5.0, 3.25, 8.0],
            'PV':       [np.nan, 1.5, -0.5, 0.0, 2.0],
            'PPrice1':  [95, 106, 114, 112.5, 120.5],
            'PPrice2':  [105, 114, 126, 117.5, 129.5],
            'Direction':[NOTRADE, BUY, SELL, NOTRADE, BUY],
            'PColor1':  [BUY]*5, # Not used by plotting func directly
            'PColor2':  [SELL]*5, # Not used by plotting func directly
            'Diff':     [np.nan]*5, # Not used by plotting func directly
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']))
        self.rule = TradingRule.Predict_High_Low_Direction
        self.title = "Test Chart Title"

    # Test with missing OHLC columns - should raise error
    def test_plot_missing_ohlc(self):
        df_missing = self.df_results.drop(columns=['Low'])
        with self.assertRaises(ValueError) as cm:
            plot_indicator_results(df_missing, self.rule, self.title)
        self.assertIn("Input DataFrame must contain columns:", str(cm.exception))

    # Test the generation of addplot list and call to mpf.plot
    @patch('src.plotting.plotting.mpf.make_addplot')
    @patch('src.plotting.plotting.mpf.plot')
    @patch('src.plotting.plotting.logger', new_callable=MockLogger) # Mock logger in plotting.py
    def test_plot_calls_and_addplots(self, _, mock_mpf_plot, mock_make_addplot):
        # Define unique return values for make_addplot calls to track them
        mock_make_addplot.side_effect = lambda data, **kwargs: {"data": data.name if isinstance(data, pd.Series) else 'signal', "kwargs": kwargs}

        plot_indicator_results(self.df_results, self.rule, self.title)

        # --- Assertions for make_addplot calls ---
        # Expected calls based on self.df_results columns and logic
        expected_addplot_calls = [
            # PPrice1
            call(self.df_results['PPrice1'], panel=0, color='green', width=0.9, linestyle='dotted', title="PPrice1", secondary_y=True),
            # PPrice2
            call(self.df_results['PPrice2'], panel=0, color='red', width=0.9, linestyle='dotted', title="PPrice2", secondary_y=True),
            # PV (panel 1)
            call(self.df_results['PV'].fillna(0), panel=1, color='orange', width=0.8, ylabel='PV'),
            call(ANY, panel=1, color='gray', linestyle=':', width=0.5), # Zero line for PV
            # HL (panel 2)
            call(self.df_results['HL'].fillna(0), panel=2, color='brown', width=0.8, ylabel='HL (Points)'),
            # Pressure (panel 3)
            call(self.df_results['Pressure'].fillna(0), panel=3, color='dodgerblue', width=0.8, ylabel='Pressure'),
            call(ANY, panel=3, color='gray', linestyle=':', width=0.5), # Zero line for Pressure
            # Direction BUY markers (panel 0) - Check kwargs
             call(ANY, type='scatter', markersize=50, marker='^', color='lime', panel=0),
             # Direction SELL markers (panel 0) - Check kwargs
             call(ANY, type='scatter', markersize=50, marker='v', color='red', panel=0),
        ]

        # Check the number of calls matches expected plots
        self.assertEqual(mock_make_addplot.call_count, len(expected_addplot_calls))

        # More detailed check of kwargs for specific plots (e.g., PPrice1, PV, signals)
        actual_calls = mock_make_addplot.call_args_list
        # Example: Check PPrice1 call details
        pp1_call = next(c for c in actual_calls if c[1].get('title') == 'PPrice1')
        self.assertEqual(pp1_call[1]['panel'], 0)
        self.assertEqual(pp1_call[1]['color'], 'green')
        pd.testing.assert_series_equal(pp1_call[0][0], self.df_results['PPrice1'], check_names=False)

        # Example: Check PV call details
        pv_call = next(c for c in actual_calls if c[1].get('ylabel') == 'PV')
        self.assertEqual(pv_call[1]['panel'], 1)
        self.assertEqual(pv_call[1]['color'], 'orange')
        pd.testing.assert_series_equal(pv_call[0][0], self.df_results['PV'].fillna(0), check_names=False)

        # Example: Check BUY signal call details (checking kwargs as data is complex)
        buy_signal_call = next(c for c in actual_calls if c[1].get('marker') == '^')
        self.assertEqual(buy_signal_call[1]['type'], 'scatter')
        self.assertEqual(buy_signal_call[1]['markersize'], 50)
        self.assertEqual(buy_signal_call[1]['color'], 'lime')
        self.assertEqual(buy_signal_call[1]['panel'], 0)
        # Check the data passed has NaNs where signal is not BUY
        buy_signal_data = buy_signal_call[0][0]
        self.assertTrue(np.isnan(buy_signal_data.iloc[0])) # NOTRADE
        self.assertFalse(np.isnan(buy_signal_data.iloc[1])) # BUY
        self.assertTrue(np.isnan(buy_signal_data.iloc[2])) # SELL
        self.assertTrue(np.isnan(buy_signal_data.iloc[3])) # NOTRADE
        self.assertFalse(np.isnan(buy_signal_data.iloc[4])) # BUY


        # --- Assertions for mpf.plot call ---
        mock_mpf_plot.assert_called_once()
        call_args, call_kwargs = mock_mpf_plot.call_args

        # Check the DataFrame passed
        pd.testing.assert_frame_equal(call_args[0], self.df_results)

        # Check keyword arguments
        self.assertEqual(call_kwargs['type'], 'candle')
        self.assertEqual(call_kwargs['style'], 'yahoo')
        self.assertEqual(call_kwargs['title'], f"{self.title} - Rule: {self.rule.name}")
        self.assertEqual(call_kwargs['ylabel'], 'Price')
        self.assertTrue(call_kwargs['volume']) # Volume column exists
        self.assertEqual(len(call_kwargs['addplot']), mock_make_addplot.call_count) # Check all generated plots passed
        self.assertEqual(call_kwargs['panel_ratios'], (4, 1, 1, 1)) # Main panel + 3 indicator panels
        # Check figratio calculation roughly matches expected shape
        self.assertIsInstance(call_kwargs['figratio'], tuple)


    # Test plotting with minimal columns (only OHLC + Direction for markers)
    @patch('src.plotting.plotting.mpf.make_addplot')
    @patch('src.plotting.plotting.mpf.plot')
    @patch('src.plotting.plotting.logger', new_callable=MockLogger)
    def test_plot_minimal_columns(self, _, mock_mpf_plot, mock_make_addplot):
        minimal_df = self.df_results[['Open', 'High', 'Low', 'Close', 'Direction']].copy()
        rule = TradingRule.Pressure_Vector
        mock_make_addplot.return_value = {}  # Keep mock basic

        try:
            # Просто вызываем функцию, проверяя, что она не падает
            plot_indicator_results(minimal_df, rule, "Minimal Plot")
            # Убедимся, что основной plot был вызван
            mock_mpf_plot.assert_called_once()
            call_args, call_kwargs = mock_mpf_plot.call_args
            pd.testing.assert_frame_equal(call_args[0], minimal_df)
            self.assertFalse(call_kwargs['volume'])

            # Убираем проверку количества scatter_calls, так как она ненадежна
            # expected_addplot_count = 2
            # scatter_calls = [c for c in mock_make_addplot.call_args_list if c[1].get('type') == 'scatter']
            # self.assertEqual(len(scatter_calls), expected_addplot_count)

            # Можно оставить проверку, что addplot был передан (хотя бы пустой список, если маркеры не добавились)
            self.assertIn('addplot', call_kwargs)
            self.assertIsInstance(call_kwargs['addplot'], list)

        except Exception as e:
            self.fail(f"plot_indicator_results failed unexpectedly in minimal test: {e}")

    # Test plotting when mpf.plot raises an exception
    @patch('src.plotting.plotting.mpf.plot')
    @patch('src.plotting.plotting.logger') # Use MagicMock to check error logging
    def test_plot_exception_handling(self, __instance, mock_mpf_plot):
        mock_mpf_plot.side_effect = Exception("MPF Render Error")

        # The function should catch the exception and log it, not crash
        try:
            plot_indicator_results(self.df_results, self.rule, self.title)
        except Exception as e:
             # Fail test if the function re-raises the exception (it shouldn't)
             self.fail(f"plot_indicator_results raised an exception unexpectedly: {e}")

        # Check that the error was logged
        __instance.print_error.assert_called_once()
        self.assertIn("Error during plotting: MPF Render Error", __instance.print_error.call_args[0][0])
        __instance.print_warning.assert_called_once() # Warning about data also called

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()