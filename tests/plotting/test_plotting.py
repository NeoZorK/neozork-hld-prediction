# tests/plotting/test_plotting.py

import unittest
from unittest.mock import patch, call, ANY #, MagicMock
import pandas as pd
import numpy as np

# Import the function to test and dependencies
from src.plotting.plotting import plot_indicator_results
from src.common.constants import TradingRule, BUY, SELL, NOTRADE
from src.plotting.fastest_plot import plot_indicator_results_fastest

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

    # Test with missing OHLC columns - should log error and return None
    def test_plot_missing_ohlc(self):
        df_missing = self.df_results.drop(columns=['Low'])
        with patch('src.plotting.plotting.logger') as mock_logger:
            result = plot_indicator_results(df_missing, self.rule, self.title)
            self.assertIsNone(result)
            mock_logger.print_error.assert_called_once()
            error_msg = mock_logger.print_error.call_args[0][0]
            self.assertIn("must contain columns", error_msg)

    # Test the generation of addplot list and call to mpf.plot
    @patch('src.plotting.plotting.mpf.make_addplot')
    @patch('src.plotting.plotting.mpf.plot')
    @patch('src.plotting.plotting.logger', new_callable=MockLogger) # Mock logger in plotting.py
    def test_plot_calls_and_addplots(self, _, mock_mpf_plot, mock_make_addplot):

        # Mock the make_addplot function to track calls
        self.assertTrue('Low' in self.df_results.columns)
        self.assertTrue('High' in self.df_results.columns)

        # Define unique return values for make_addplot calls to track them
        mock_make_addplot.side_effect = lambda data, **kwargs: {"data": data.name if isinstance(data, pd.Series) else 'signal', "kwargs": kwargs}

        # Call the function to test, specifying the mplfinance branch
        # Call the function to test, specifying the mplfinance mode
        plot_indicator_results(self.df_results, self.rule, self.title, mode="mplfinance")
        # Check that make_addplot was called the expected number of times
        self.assertEqual(mock_make_addplot.call_count, 9)

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
        # wait green color for PPrice1
        self.assertEqual(pp1_call[1]['color'], 'lime')
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
        self.assertEqual(call_kwargs['panel_ratios'], (4, 1, 1, 1, 0.8))
        # Check figratio calculation roughly matches expected shape
        self.assertIsInstance(call_kwargs['figratio'], tuple)

    # Test plotting with minimal columns (only OHLC + Direction for markers)
    @patch('src.plotting.mplfinance_plot.mpf.make_addplot')
    @patch('src.plotting.mplfinance_plot.mpf.plot')
    @patch('src.plotting.plotting.logger', new_callable=MockLogger)
    def test_plot_minimal_columns(self, _, mock_mpf_plot, mock_make_addplot):
        minimal_df = self.df_results[['Open', 'High', 'Low', 'Close', 'Direction']].copy()
        rule = TradingRule.Pressure_Vector
        mock_make_addplot.return_value = {}  # Keep mock basic

        try:
            # Call the function with minimal data, specifying mplfinance mode
            plot_indicator_results(minimal_df, rule, "Minimal Plot", mode="mplfinance")
            call_args, call_kwargs = mock_mpf_plot.call_args
            pd.testing.assert_frame_equal(call_args[0], minimal_df)
            self.assertFalse(call_kwargs['volume'])
            self.assertIn('addplot', call_kwargs)
            self.assertIsInstance(call_kwargs['addplot'], list)

        except Exception as e:
            self.fail(f"plot_indicator_results failed unexpectedly in minimal test: {e}")

    # Test plotting when mpf.plot raises an exception
    @patch('src.plotting.plotting.mpf.plot')
    @patch('src.plotting.plotting.logger')
    def test_plot_exception_handling(self, mock_logger, mock_mpf_plot):
        mock_mpf_plot.side_effect = Exception("MPF Render Error")

        print(f"DEBUG: Type of mock_logger in test_plot_exception_handling: {type(mock_logger)}")

        # Call the function to test, specifying the mplfinance branch
        # Call the function to test, specifying the mplfinance mode
        plot_indicator_results(self.df_results, self.rule, self.title, mode="mplfinance")
        # Сheck that the logger's print_error method was called
        mock_logger.print_error.assert_called_once()
        error_call_args = mock_logger.print_error.call_args[0]
        self.assertIn("Error during mplfinance plotting: MPF Render Error", error_call_args[0])
        mock_logger.print_warning.assert_called_once()

    # Test the mode parameter for fastest mode
    @patch('src.plotting.plotting.plot_indicator_results_fastest')
    @patch('src.plotting.plotting.logger')
    def test_plot_fastest_mode(self, mock_logger, mock_fastest_plot):
        """Test that plot_indicator_results correctly calls plot_indicator_results_fastest when mode='fastest'"""
        # Call the function with fastest mode
        result = plot_indicator_results(
            self.df_results, self.rule, self.title, 
            mode="fastest", data_source="demo", 
            output_path="results/test_fastest_plot.html"
        )
        
        # Check logger was called with the correct message
        mock_logger.print_info.assert_called_with("Using 'fastest' mode (Plotly + Dask + Datashader) for plotting...")
        
        # Check the fastest plot function was called with the correct parameters
        mock_fastest_plot.assert_called_once()
        call_args = mock_fastest_plot.call_args
        
        # Check that the first positional arg is the dataframe
        pd.testing.assert_frame_equal(call_args[0][0], self.df_results)
        # Check that the second positional arg is the rule
        self.assertEqual(call_args[0][1], self.rule)
        # Check the keyword arguments
        self.assertEqual(call_args[1]['title'], self.title)
        self.assertEqual(call_args[1]['data_source'], "demo")
        self.assertEqual(call_args[1]['output_path'], "results/test_fastest_plot.html")
        self.assertEqual(call_args[1]['mode'], "fastest")
        
        # Check that the function returns None as expected
        self.assertIsNone(result)

    # Test error handling for fastest mode
    @patch('src.plotting.plotting.plot_indicator_results_fastest')
    @patch('src.plotting.plotting.plot_indicator_results_plotly')
    @patch('src.plotting.plotting.logger')
    def test_plot_fastest_mode_error_handling(self, mock_logger, mock_plotly_plot, mock_fastest_plot):
        """Test that plot_indicator_results handles errors in fastest mode and falls back to plotly"""
        # Set up the fastest plot function to raise an exception
        mock_fastest_plot.side_effect = Exception("Fastest plot error")
        mock_plotly_plot.return_value = "Plotly plot result"
        
        # Call the function with fastest mode
        result = plot_indicator_results(
            self.df_results, self.rule, self.title, 
            mode="fastest", data_source="demo"
        )
        
        # Check that the error was logged
        mock_logger.print_error.assert_called_once()
        self.assertIn("Error in plot_indicator_results with mode='fastest'", 
                      mock_logger.print_error.call_args[0][0])
        
        # Check that the fallback warning was logged
        mock_logger.print_warning.assert_called_once()
        self.assertEqual("Falling back to 'plotly' mode due to error...", 
                       mock_logger.print_warning.call_args[0][0])
        
        # Check that the plotly plot function was called as a fallback
        mock_plotly_plot.assert_called_once()
        # Check that the function returns the plotly result
        self.assertEqual(result, "Plotly plot result")

    # Test large dataset handling with fastest mode
    @patch('src.plotting.plotting.plot_indicator_results_fastest')
    @patch('src.plotting.plotting.logger')
    def test_plot_fastest_mode_large_dataset(self, mock_logger, mock_fastest_plot):
        """Test that plot_indicator_results correctly handles large datasets with fastest mode"""
        # Create a large dataset by repeating the existing one
        large_df = pd.concat([self.df_results] * 1000, ignore_index=True)
        # Reset the index to be datetime
        large_df.index = pd.date_range(start='2023-01-01', periods=len(large_df), freq='h')
        
        # Call the function with fastest mode
        result = plot_indicator_results(
            large_df, self.rule, "Large Dataset Test", 
            mode="fastest", data_source="demo"
        )
        
        # Check the fastest plot function was called with the large dataframe
        mock_fastest_plot.assert_called_once()
        call_args = mock_fastest_plot.call_args
        self.assertEqual(len(call_args[0][0]), 5000)  # Check dataframe size
        
        # Verify the function returns None
        self.assertIsNone(result)

    # Test integration of different modes in the plotting workflow
    @patch('src.plotting.plotting.plot_indicator_results_fastest')
    @patch('src.plotting.plotting.plot_indicator_results_fast')
    @patch('src.plotting.plotting.plot_indicator_results_plotly')
    @patch('src.plotting.plotting.plot_indicator_results_mplfinance')
    @patch('src.plotting.plotting.logger')
    def test_plot_mode_integration(self, mock_logger, mock_mpl, mock_plotly, mock_fast, mock_fastest):
        """Test that plot_indicator_results correctly routes to different plotting functions based on mode"""
        # Set return values for the mocked functions
        mock_plotly.return_value = "Plotly result"
        mock_mpl.return_value = "MPL result"
        
        # Test fastest mode
        result_fastest = plot_indicator_results(self.df_results, self.rule, self.title, mode="fastest")
        mock_fastest.assert_called_once()
        self.assertIsNone(result_fastest)
        mock_fastest.reset_mock()
        
        # Test fast mode
        result_fast = plot_indicator_results(self.df_results, self.rule, self.title, mode="fast")
        mock_fast.assert_called_once()
        self.assertIsNone(result_fast)
        mock_fast.reset_mock()
        
        # Test plotly mode
        result_plotly = plot_indicator_results(self.df_results, self.rule, self.title, mode="plotly")
        mock_plotly.assert_called_once()
        self.assertEqual(result_plotly, "Plotly result")
        mock_plotly.reset_mock()
        
        # Test plt alias for plotly
        result_plt = plot_indicator_results(self.df_results, self.rule, self.title, mode="plt")
        mock_plotly.assert_called_once()
        self.assertEqual(result_plt, "Plotly result")
        mock_plotly.reset_mock()
        
        # Test mplfinance mode
        result_mpl = plot_indicator_results(self.df_results, self.rule, self.title, mode="mplfinance")
        mock_mpl.assert_called_once()
        self.assertEqual(result_mpl, "MPL result")
        mock_mpl.reset_mock()
        
        # Test mpl alias for mplfinance
        result_mpl_alias = plot_indicator_results(self.df_results, self.rule, self.title, mode="mpl")
        mock_mpl.assert_called_once()
        self.assertEqual(result_mpl_alias, "MPL result")

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()
