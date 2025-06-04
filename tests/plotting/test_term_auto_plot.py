# tests/plotting/test_term_auto_plot.py
"""
Tests for terminal auto plot functionality.
These tests verify that terminal-based auto plotting works correctly.
"""
import unittest
import pandas as pd
import numpy as np
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the src directory to the path so we can import modules from there
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.constants import TradingRule
from src.plotting.term_auto_plot import auto_plot_from_parquet, _determine_chart_type, _plot_series_in_terminal

class TestTermAutoPlot(unittest.TestCase):
    """Test cases for terminal auto plot functionality."""

    def setUp(self):
        """Set up test data."""
        # Create a test DataFrame with various column types
        self.test_data = pd.DataFrame({
            'DateTime': pd.date_range('2023-01-01', periods=50),
            'Open': np.random.rand(50) * 100 + 100,
            'High': np.random.rand(50) * 100 + 110,
            'Low': np.random.rand(50) * 100 + 90,
            'Close': np.random.rand(50) * 100 + 100,
            'Volume': np.random.randint(1000, 10000, 50),
            'RSI': np.random.rand(50) * 100,
            'SMA': np.random.rand(50) * 100 + 100,
            'Direction': np.random.choice([0, 1, -1], 50),
            'Signal': np.random.rand(50) * 2 - 1,
            'PPrice1': np.random.rand(50) * 100 + 105,
            'PPrice2': np.random.rand(50) * 100 + 95,
            'Pressure': np.random.rand(50) * 2 - 1,
            'HL': np.random.rand(50) * 10 - 5,
            'CustomMetric1': np.random.rand(50) * 100,
            'CustomMetric2': np.random.rand(50) * 100
        })

        # Set DateTime as index
        self.test_data.set_index('DateTime', inplace=True)

        # Define test parquet file path
        self.test_file = Path("tests/plotting/test_data_auto.parquet")
        os.makedirs(self.test_file.parent, exist_ok=True)

        # Save test data to parquet
        self.test_data.to_parquet(self.test_file)

    def tearDown(self):
        """Clean up after tests."""
        # Remove test parquet file if it exists
        if self.test_file.exists():
            self.test_file.unlink()

    @patch('plotext.show')
    def test_determine_chart_type(self, mock_show):
        """Test the chart type determination logic."""
        # Binary/categorical data should return 'bar'
        binary_series = pd.Series([0, 1, 0, 1, 0], name='Direction')
        self.assertEqual(_determine_chart_type(binary_series), 'bar')

        # Volume data should return 'bar'
        volume_series = pd.Series(np.random.randint(1000, 10000, 10), name='Volume')
        self.assertEqual(_determine_chart_type(volume_series), 'bar')

        # Continuous data should return 'line'
        continuous_series = pd.Series(np.random.rand(10) * 100, name='Price')
        self.assertEqual(_determine_chart_type(continuous_series), 'line')

    @patch('plotext.show')
    @patch('plotext.plot')
    @patch('plotext.clear_data')
    def test_plot_series_in_terminal(self, mock_clear_data, mock_plot, mock_show):
        """Test plotting a single series in the terminal."""
        x_data = list(range(5))
        x_labels = ['01-01', '01-02', '01-03', '01-04', '01-05']

        # Test with price data
        price_series = pd.Series([100, 101, 102, 101, 103], name='Close')
        result = _plot_series_in_terminal(price_series, x_data, x_labels, 1)
        self.assertTrue(result)
        mock_clear_data.assert_called()
        mock_plot.assert_called()
        mock_show.assert_called()

        # Test with empty series
        empty_series = pd.Series([np.nan, np.nan, np.nan], name='Empty')
        result = _plot_series_in_terminal(empty_series, x_data, x_labels, 1)
        self.assertFalse(result)

    @patch('plotext.show')
    def test_auto_plot_from_parquet(self, mock_show):
        """Test auto plotting from a parquet file."""
        with patch('src.plotting.term_auto_plot._plot_series_in_terminal', return_value=True) as mock_plot_series:
            # Test with valid parquet file
            result = auto_plot_from_parquet(str(self.test_file))
            self.assertTrue(result)

            # Verify that all non-OHLCV columns are plotted
            expected_calls = len(self.test_data.columns) - 5  # Exclude OHLCV
            self.assertGreaterEqual(mock_plot_series.call_count, expected_calls)

    @patch('plotext.show')
    def test_auto_plot_large_dataset(self, mock_show):
        """Test auto plotting with a large dataset (should be truncated)."""
        # Create large test data
        large_data = pd.DataFrame({
            'DateTime': pd.date_range('2023-01-01', periods=200),
            'Open': np.random.rand(200) * 100 + 100,
            'High': np.random.rand(200) * 100 + 110,
            'Low': np.random.rand(200) * 100 + 90,
            'Close': np.random.rand(200) * 100 + 100,
            'Volume': np.random.randint(1000, 10000, 200),
            'CustomMetric': np.random.rand(200) * 100
        })
        large_data.set_index('DateTime', inplace=True)

        # Save to parquet
        large_file = Path("tests/plotting/test_large_data.parquet")
        os.makedirs(large_file.parent, exist_ok=True)
        large_data.to_parquet(large_file)

        try:
            with patch('src.plotting.term_auto_plot._plot_series_in_terminal', return_value=True) as mock_plot_series:
                result = auto_plot_from_parquet(str(large_file))
                self.assertTrue(result)

                # Verify the dataset was truncated to max_points (80)
                args, _ = mock_plot_series.call_args
                self.assertEqual(len(args[1]), 80)  # x_data should be truncated to 80 points
        finally:
            # Clean up
            if large_file.exists():
                large_file.unlink()

    @patch('plotext.show')
    def test_auto_plot_handles_errors(self, mock_show):
        """Test that auto_plot_from_parquet handles errors gracefully."""
        # Test with non-existent file
        with patch('src.common.logger.print_error') as mock_print_error:
            result = auto_plot_from_parquet("non_existent_file.parquet")
            self.assertFalse(result)
            mock_print_error.assert_called()

    @patch('plotext.show')
    def test_auto_plot_with_title(self, mock_show):
        """Test auto plotting with a custom title."""
        with patch('builtins.print') as mock_print:
            result = auto_plot_from_parquet(str(self.test_file), plot_title="Custom Title")
            self.assertTrue(result)

            # Verify custom title was used
            title_call = False
            for call in mock_print.call_args_list:
                if call[0] and "Custom Title" in str(call[0][0]):
                    title_call = True
                    break
            self.assertTrue(title_call)

if __name__ == '__main__':
    unittest.main()
