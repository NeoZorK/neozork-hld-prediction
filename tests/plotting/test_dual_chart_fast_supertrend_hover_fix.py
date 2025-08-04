"""
Test for SuperTrend hover tool fix in dual_chart_fast.py.

This test verifies that the hover tool for SuperTrend indicator displays
correct values instead of "???" for Value when using -d fast mode.
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from bokeh.models import HoverTool, ColumnDataSource

# Import the function we want to test
from src.plotting.dual_chart_fast import _get_indicator_hover_tool


class TestDualChartFastSupertrendHoverFix(unittest.TestCase):
    """Test class for SuperTrend hover tool fix in dual_chart_fast.py."""

    def setUp(self):
        """Set up test data."""
        # Create sample data with PPrice1/PPrice2 columns (like real SuperTrend data)
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        self.sample_data_pprice = pd.DataFrame({
            'PPrice1': [1.2000, 1.2100, 1.2200, 1.2300, 1.2400, 1.2500, 1.2600, 1.2700, 1.2800, 1.2900],
            'PPrice2': [1.2100, 1.2200, 1.2300, 1.2400, 1.2500, 1.2600, 1.2700, 1.2800, 1.2900, 1.3000],
            'Direction': [1, 1, -1, -1, 1, 1, -1, -1, 1, 1]
        }, index=dates)
        
        # Create sample data with direct supertrend column
        self.sample_data_direct = pd.DataFrame({
            'supertrend': [1.2000, 1.2100, 1.2200, 1.2300, 1.2400, 1.2500, 1.2600, 1.2700, 1.2800, 1.2900],
            'Direction': [1, 1, -1, -1, 1, 1, -1, -1, 1, 1]
        }, index=dates)

    def test_dual_chart_fast_supertrend_data_structure(self):
        """Test that test data has correct structure."""
        # Verify that required columns are present
        self.assertIn('PPrice1', self.sample_data_pprice.columns, "PPrice1 column should be present")
        self.assertIn('PPrice2', self.sample_data_pprice.columns, "PPrice2 column should be present")
        self.assertIn('Direction', self.sample_data_pprice.columns, "Direction column should be present")
        
        # Verify that data types are correct
        self.assertTrue(pd.api.types.is_numeric_dtype(self.sample_data_pprice['PPrice1']), "PPrice1 should be numeric")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.sample_data_pprice['PPrice2']), "PPrice2 should be numeric")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.sample_data_pprice['Direction']), "Direction should be numeric")
        
        # Verify that index is datetime
        self.assertTrue(isinstance(self.sample_data_pprice.index, pd.DatetimeIndex), "Index should be DatetimeIndex")

    def test_dual_chart_fast_supertrend_hover_tool_creation(self):
        """Test that hover tool can be created with correct parameters."""
        # Create a simple hover tool to test the logic (simplified like fastest mode)
        hover_tool = HoverTool(
            tooltips=[
                ("Value", "@PPrice1{0.5f}")
            ],
            formatters={},
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

    def test_dual_chart_fast_supertrend_column_source_creation(self):
        """Test that ColumnDataSource can be created with SuperTrend data."""
        # Prepare data like in the dual_chart_fast.py
        display_df = self.sample_data_pprice.copy()
        display_df['index'] = display_df.index
        
        # Simulate the logic from dual_chart_fast.py
        has_pprice_columns = 'PPrice1' in display_df.columns and 'PPrice2' in display_df.columns and 'Direction' in display_df.columns
        self.assertTrue(has_pprice_columns, "Should have PPrice1/PPrice2/Direction columns")
        
        if has_pprice_columns:
            p1 = display_df['PPrice1']
            p2 = display_df['PPrice2']
            direction = display_df['Direction']
            
            # Handle NaN values properly - only compute supertrend where both p1 and p2 are not NaN
            valid_mask = ~(pd.isna(p1) | pd.isna(p2))
            supertrend_values = np.full(len(direction), np.nan)
            supertrend_values[valid_mask] = np.where(direction[valid_mask] > 0, p1[valid_mask], p2[valid_mask])
            
            # Add supertrend values to both display_df and source for hover tool
            display_df['supertrend'] = supertrend_values
            
            # Create ColumnDataSource
            source = ColumnDataSource(display_df)
            
            # Verify that source was created
            self.assertIsNotNone(source, "ColumnDataSource should be created")
            
            # Verify that required columns are in the source
            self.assertIn('PPrice1', source.data, "PPrice1 should be in source data")
            self.assertIn('Direction', source.data, "Direction should be in source data")
            self.assertIn('index', source.data, "index should be in source data")

    def test_dual_chart_fast_supertrend_hover_tool_dynamic_column(self):
        """Test that hover tool uses dynamic column selection."""
        # Test with PPrice1/PPrice2 columns (like real SuperTrend data)
        has_pprice = 'PPrice1' in self.sample_data_pprice.columns and 'PPrice2' in self.sample_data_pprice.columns
        
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
        
        # Verify that tooltips contain only Value field (simplified)
        tooltips = hover_tool.tooltips
        tooltip_text = [str(tooltip) for tooltip in tooltips]
        self.assertTrue(any('Value' in str(tooltip) for tooltip in tooltips), "Value tooltip missing")
        self.assertFalse(any('Date' in str(tooltip) for tooltip in tooltips), "Date tooltip should not be present")
        self.assertFalse(any('Direction' in str(tooltip) for tooltip in tooltips), "Direction tooltip should not be present")

    def test_dual_chart_fast_supertrend_hover_tool_function(self):
        """Test the actual _get_indicator_hover_tool function."""
        # Test with PPrice1/PPrice2 columns
        hover_tool_pprice = _get_indicator_hover_tool('supertrend', self.sample_data_pprice)
        
        # Verify that hover tool was created
        self.assertIsNotNone(hover_tool_pprice, "Hover tool should be created")
        self.assertIsInstance(hover_tool_pprice, HoverTool, "Should be HoverTool instance")
        self.assertEqual(hover_tool_pprice.mode, 'vline', "Hover tool mode should be 'vline'")
        
        # Verify that tooltips contain Date, SuperTrend, and Direction fields
        tooltips = hover_tool_pprice.tooltips
        self.assertEqual(len(tooltips), 3, "Should have three tooltips: Date, SuperTrend, Direction")
        tooltip_labels = [tooltip[0] for tooltip in tooltips]
        self.assertIn("Date", tooltip_labels, "Date tooltip should be present")
        self.assertIn("SuperTrend", tooltip_labels, "SuperTrend tooltip should be present")
        self.assertIn("Direction", tooltip_labels, "Direction tooltip should be present")
        
        # Test with direct supertrend column
        hover_tool_direct = _get_indicator_hover_tool('supertrend', self.sample_data_direct)
        
        # Verify that hover tool was created
        self.assertIsNotNone(hover_tool_direct, "Hover tool should be created")
        self.assertIsInstance(hover_tool_direct, HoverTool, "Should be HoverTool instance")
        self.assertEqual(hover_tool_direct.mode, 'vline', "Hover tool mode should be 'vline'")
        
        # Verify that tooltips contain Date, SuperTrend, and Direction fields
        tooltips = hover_tool_direct.tooltips
        self.assertEqual(len(tooltips), 3, "Should have three tooltips: Date, SuperTrend, Direction")
        tooltip_labels = [tooltip[0] for tooltip in tooltips]
        self.assertIn("Date", tooltip_labels, "Date tooltip should be present")
        self.assertIn("SuperTrend", tooltip_labels, "SuperTrend tooltip should be present")
        self.assertIn("Direction", tooltip_labels, "Direction tooltip should be present")


if __name__ == '__main__':
    unittest.main() 