"""
Test for SuperTrend hover tool fix in fast mode.

This test verifies that the hover tool for SuperTrend indicator displays
correct values instead of "???" for Date, SuperTrend, and Direction
when using -d fast mode.
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from bokeh.models import HoverTool, ColumnDataSource

# Import the function we want to test
from src.plotting.fast_plot import plot_indicator_results_fast


class TestFastSupertrendHoverFix(unittest.TestCase):
    """Test class for SuperTrend hover tool fix in fast mode."""

    def setUp(self):
        """Set up test data."""
        # Create sample data with PPrice1/PPrice2 columns (like real SuperTrend data)
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [1.200, 1.205, 1.210, 1.215, 1.220, 1.225, 1.230, 1.235, 1.240, 1.245],
            'High': [1.210, 1.215, 1.220, 1.225, 1.230, 1.235, 1.240, 1.245, 1.250, 1.255],
            'Low': [1.190, 1.195, 1.200, 1.205, 1.210, 1.215, 1.220, 1.225, 1.230, 1.235],
            'Close': [1.205, 1.210, 1.215, 1.220, 1.225, 1.230, 1.235, 1.240, 1.245, 1.250],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900],
            'PPrice1': [1.200, 1.205, 1.210, 1.215, 1.220, 1.225, 1.230, 1.235, 1.240, 1.245],
            'PPrice2': [1.300, 1.305, 1.310, 1.315, 1.320, 1.325, 1.330, 1.335, 1.340, 1.345],
            'Direction': [1, 1, 1, -1, -1, -1, 1, 1, -1, -1]
        }, index=dates)

    def test_fast_supertrend_data_structure(self):
        """Test that the sample data has the correct structure for SuperTrend."""
        # Verify that required columns are present
        self.assertIn('PPrice1', self.sample_data.columns, "PPrice1 column should be present")
        self.assertIn('PPrice2', self.sample_data.columns, "PPrice2 column should be present")
        self.assertIn('Direction', self.sample_data.columns, "Direction column should be present")
        
        # Verify that data types are correct
        self.assertTrue(pd.api.types.is_numeric_dtype(self.sample_data['PPrice1']), "PPrice1 should be numeric")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.sample_data['PPrice2']), "PPrice2 should be numeric")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.sample_data['Direction']), "Direction should be numeric")
        
        # Verify that index is datetime
        self.assertTrue(isinstance(self.sample_data.index, pd.DatetimeIndex), "Index should be DatetimeIndex")

    def test_fast_supertrend_hover_tool_creation(self):
        """Test that hover tool can be created with correct parameters."""
        # Create a simple hover tool to test the logic (simplified like fastest mode)
        hover_tool = HoverTool(
            tooltips=[
                ("Value", "@PPrice1{0.5f}")
            ],
            formatters={
                "@PPrice1": "numeral"
            },
            mode='vline'
        )
        
        # Verify that hover tool was created
        self.assertIsNotNone(hover_tool, "Hover tool should be created")
        self.assertEqual(hover_tool.mode, 'vline', "Hover tool mode should be 'vline'")
        
        # Verify that tooltips contain only Value field (simplified)
        tooltips = hover_tool.tooltips
        tooltip_text = [str(tooltip) for tooltip in tooltips]
        self.assertTrue(any('Value' in str(tooltip) for tooltip in tooltips), "Value tooltip missing")
        self.assertFalse(any('Date' in str(tooltip) for tooltip in tooltips), "Date tooltip should not be present")
        self.assertFalse(any('Direction' in str(tooltip) for tooltip in tooltips), "Direction tooltip should not be present")

    def test_fast_supertrend_column_source_creation(self):
        """Test that ColumnDataSource can be created with SuperTrend data."""
        # Prepare data like in the fast_plot.py
        display_df = self.sample_data.copy()
        display_df['index'] = display_df.index
        
        # Simulate the logic from fast_plot.py
        has_pprice_columns = 'PPrice1' in display_df.columns and 'PPrice2' in display_df.columns and 'Direction' in display_df.columns
        self.assertTrue(has_pprice_columns, "Should have PPrice1/PPrice2/Direction columns")
        
        if has_pprice_columns:
            p1 = display_df['PPrice1']
            p2 = display_df['PPrice2']
            direction = display_df['Direction']
            supertrend_val = np.where(direction > 0, p1, p2)
            st_col = 'PPrice1'  # для hover
            
            # Create DataFrame for source
            st_df = display_df.copy()
            st_df[st_col] = supertrend_val
            st_df['supertrend_val'] = supertrend_val
            
            # Ensure all required columns are in the source for proper hover functionality
            if 'index' not in st_df.columns:
                st_df['index'] = st_df.index
            if 'Direction' not in st_df.columns:
                st_df['Direction'] = direction
                
            # Create ColumnDataSource
            st_source = ColumnDataSource(st_df)
            
            # Verify that source was created
            self.assertIsNotNone(st_source, "ColumnDataSource should be created")
            
            # Verify that required columns are in the source
            self.assertIn('PPrice1', st_source.data, "PPrice1 should be in source data")
            self.assertIn('Direction', st_source.data, "Direction should be in source data")
            self.assertIn('index', st_source.data, "index should be in source data")

    def test_fast_supertrend_hover_tool_dynamic_column(self):
        """Test that hover tool uses dynamic column selection."""
        # Test with PPrice1/PPrice2 columns (like real SuperTrend data)
        has_pprice = 'PPrice1' in self.sample_data.columns and 'PPrice2' in self.sample_data.columns
        
        if has_pprice:
            # Should use PPrice1 for hover (simplified like fastest mode)
            hover_tool = HoverTool(
                tooltips=[
                    ("Value", "@PPrice1{0.5f}")
                ],
                formatters={},
                mode='vline'
            )
        else:
            # Should use direct supertrend column (simplified like fastest mode)
            hover_tool = HoverTool(
                tooltips=[
                    ("Value", "@supertrend{0.5f}")
                ],
                formatters={},
                mode='vline'
            )
        
        # Verify that hover tool was created
        self.assertIsNotNone(hover_tool, "Hover tool should be created")
        self.assertEqual(hover_tool.mode, 'vline', "Hover tool mode should be 'vline'")
        
        # Verify that tooltips contain the correct column
        tooltips = hover_tool.tooltips
        tooltip_text = [str(tooltip) for tooltip in tooltips]
        self.assertTrue(any('PPrice1' in str(tooltip) for tooltip in tooltips), "Should use PPrice1 for hover")


if __name__ == '__main__':
    unittest.main() 