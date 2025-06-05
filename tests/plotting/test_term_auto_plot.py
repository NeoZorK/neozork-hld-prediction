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
from unittest.mock import patch, MagicMock, call, ANY
from pathlib import Path

# Add the src directory to the path so we can import modules from there
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.constants import TradingRule
from src.plotting.term_auto_plot import auto_plot_from_parquet, auto_plot_from_dataframe

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
    @patch('builtins.print')
    def test_auto_plot_from_parquet_basic(self, mock_print, mock_show):
        """Test basic auto plotting from a parquet file."""
        # Test with valid parquet file and AUTO rule
        auto_plot_from_parquet(str(self.test_file), "AUTO")
        
        # Verify that plotext.show was called (indicating charts were generated)
        self.assertTrue(mock_show.called)
        
        # Check that some output was printed
        self.assertTrue(mock_print.called)

    @patch('plotext.show')
    @patch('builtins.print')
    def test_auto_plot_from_dataframe(self, mock_print, mock_show):
        """Test auto plotting from DataFrame."""
        auto_plot_from_dataframe(self.test_data)
        
        # Verify that plotext.show was called
        self.assertTrue(mock_show.called)
        
        # Check that some output was printed
        self.assertTrue(mock_print.called)

    @patch('builtins.print')
    def test_auto_plot_with_nonexistent_file(self, mock_print):
        """Test that auto_plot_from_parquet handles non-existent files gracefully."""
        auto_plot_from_parquet("non_existent_file.parquet", "AUTO")
        
        # Should print error message about file not found
        print_calls = [str(call) for call in mock_print.call_args_list]
        file_not_found = any("not found" in call or "File not found" in call for call in print_calls)
        self.assertTrue(file_not_found)

    @patch('plotext.show')
    @patch('builtins.print')
    def test_auto_plot_with_empty_dataframe(self, mock_print, mock_show):
        """Test auto plotting with empty DataFrame."""
        empty_df = pd.DataFrame()
        empty_file = Path("tests/plotting/test_empty_data.parquet")
        os.makedirs(empty_file.parent, exist_ok=True)
        
        try:
            empty_df.to_parquet(empty_file)
            auto_plot_from_parquet(str(empty_file), "AUTO")
            
            # Should print message about empty DataFrame
            print_calls = [str(call) for call in mock_print.call_args_list]
            empty_msg = any("Empty" in call for call in print_calls)
            self.assertTrue(empty_msg)
        finally:
            if empty_file.exists():
                empty_file.unlink()

    @patch('plotext.show')
    @patch('builtins.print') 
    def test_auto_plot_with_custom_title(self, mock_print, mock_show):
        """Test auto plotting with custom title."""
        custom_title = "Custom Test Title"
        auto_plot_from_parquet(str(self.test_file), "AUTO", custom_title)
        
        # Verify that the custom title appears in the output
        print_calls = [str(call) for call in mock_print.call_args_list]
        title_found = any(custom_title in call for call in print_calls)
        self.assertTrue(title_found)

    @patch('plotext.show')
    @patch('plotext.plot')
    @patch('plotext.scatter')
    @patch('plotext.bar')
    def test_auto_plot_calls_plotext_functions(self, mock_bar, mock_scatter, mock_plot, mock_show):
        """Test that auto plotting calls appropriate plotext functions."""
        auto_plot_from_parquet(str(self.test_file), "AUTO")
        
        # At least one of the plotting functions should be called
        plotting_called = mock_plot.called or mock_scatter.called or mock_bar.called
        self.assertTrue(plotting_called)
        
        # Show should definitely be called
        self.assertTrue(mock_show.called)

if __name__ == '__main__':
    unittest.main()
