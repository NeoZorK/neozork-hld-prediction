"""
Test for SuperTrend hover tool fix.

This test verifies that the hover tool for SuperTrend indicator displays
correct values instead of "???" for Date, SuperTrend, and Direction.
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from bokeh.models import HoverTool

# Import the function we want to test
from src.plotting.dual_chart_fast import _get_indicator_hover_tool


class TestSuperTrendHoverFix(unittest.TestCase):
    """Test class for SuperTrend hover tool fix."""

    def setUp(self):
        """Set up test data."""
        # Create sample data with PPrice1/PPrice2 columns (like real SuperTrend data)
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        self.sample_data_pprice = pd.DataFrame({
            'index': dates,
            'PPrice1': [1.200, 1.205, 1.210, 1.215, 1.220, 1.225, 1.230, 1.235, 1.240, 1.245],
            'PPrice2': [1.300, 1.305, 1.310, 1.315, 1.320, 1.325, 1.330, 1.335, 1.340, 1.345],
            'Direction': [1, 1, 1, -1, -1, -1, 1, 1, -1, -1]
        })
        
        # Create sample data with direct supertrend column
        self.sample_data_direct = pd.DataFrame({
            'index': dates,
            'supertrend': [1.200, 1.205, 1.210, 1.215, 1.220, 1.225, 1.230, 1.235, 1.240, 1.245],
            'Direction': [1, 1, 1, -1, -1, -1, 1, 1, -1, -1]
        })

    def test_supertrend_hover_with_pprice_columns(self):
        """Test that hover tool uses PPrice1 when PPrice1/PPrice2 columns are present."""
        hover_tool = _get_indicator_hover_tool('supertrend', self.sample_data_pprice)
        
        # Verify hover tool exists
        self.assertIsNotNone(hover_tool, "Hover tool not created")
        self.assertIsInstance(hover_tool, HoverTool, "Hover tool is not HoverTool instance")
        
        # Verify tooltips contain expected fields
        tooltips = hover_tool.tooltips
        tooltip_text = [str(tooltip) for tooltip in tooltips]
        
        # Should contain Date, SuperTrend, and Direction
        self.assertTrue(any('Date' in str(tooltip) for tooltip in tooltips), "Date tooltip missing")
        self.assertTrue(any('SuperTrend' in str(tooltip) for tooltip in tooltips), "SuperTrend tooltip missing")
        self.assertTrue(any('Direction' in str(tooltip) for tooltip in tooltips), "Direction tooltip missing")
        
        # Verify mode is vline (not mouse)
        self.assertEqual(hover_tool.mode, 'vline', "Hover tool mode should be 'vline'")

    def test_supertrend_hover_with_direct_supertrend_column(self):
        """Test that hover tool uses supertrend column when PPrice1/PPrice2 are not present."""
        hover_tool = _get_indicator_hover_tool('supertrend', self.sample_data_direct)
        
        # Verify hover tool exists
        self.assertIsNotNone(hover_tool, "Hover tool not created")
        self.assertIsInstance(hover_tool, HoverTool, "Hover tool is not HoverTool instance")
        
        # Verify tooltips contain expected fields
        tooltips = hover_tool.tooltips
        tooltip_text = [str(tooltip) for tooltip in tooltips]
        
        # Should contain Date, SuperTrend (using supertrend column), and Direction
        self.assertTrue(any('Date' in str(tooltip) for tooltip in tooltips), "Date tooltip missing")
        self.assertTrue(any('supertrend' in str(tooltip) for tooltip in tooltips), "supertrend tooltip missing")
        self.assertTrue(any('Direction' in str(tooltip) for tooltip in tooltips), "Direction tooltip missing")
        
        # Verify mode is vline (not mouse)
        self.assertEqual(hover_tool.mode, 'vline', "Hover tool mode should be 'vline'")

    def test_supertrend_hover_formatters(self):
        """Test that hover tool has correct formatters."""
        hover_tool = _get_indicator_hover_tool('supertrend', self.sample_data_pprice)
        
        # Verify formatters exist and are correct
        self.assertIn('@index', hover_tool.formatters, "Index formatter missing")
        self.assertEqual(hover_tool.formatters['@index'], 'datetime', "Index formatter should be 'datetime'")

    def test_supertrend_hover_no_pprice_columns(self):
        """Test that hover tool works when PPrice1/PPrice2 columns are missing."""
        # Create data without PPrice1/PPrice2 columns
        data_no_pprice = pd.DataFrame({
            'index': pd.date_range('2020-01-01', periods=5, freq='D'),
            'supertrend': [1.200, 1.205, 1.210, 1.215, 1.220],
            'Direction': [1, 1, -1, -1, 1]
        })
        
        hover_tool = _get_indicator_hover_tool('supertrend', data_no_pprice)
        
        # Verify hover tool exists
        self.assertIsNotNone(hover_tool, "Hover tool not created")
        
        # Verify tooltips contain supertrend (not PPrice1)
        tooltips = hover_tool.tooltips
        self.assertTrue(any('supertrend' in str(tooltip) for tooltip in tooltips), 
                       "Should use supertrend column when PPrice1/PPrice2 are missing")

    def test_supertrend_hover_missing_direction(self):
        """Test that hover tool works when Direction column is missing."""
        # Create data without Direction column
        data_no_direction = pd.DataFrame({
            'index': pd.date_range('2020-01-01', periods=5, freq='D'),
            'PPrice1': [1.200, 1.205, 1.210, 1.215, 1.220],
            'PPrice2': [1.300, 1.305, 1.310, 1.315, 1.320]
        })
        
        hover_tool = _get_indicator_hover_tool('supertrend', data_no_direction)
        
        # Verify hover tool exists (should still work without Direction)
        self.assertIsNotNone(hover_tool, "Hover tool should be created even without Direction column")
        
        # Verify tooltips contain Date and SuperTrend
        tooltips = hover_tool.tooltips
        self.assertTrue(any('Date' in str(tooltip) for tooltip in tooltips), "Date tooltip should be present")
        self.assertTrue(any('SuperTrend' in str(tooltip) for tooltip in tooltips), "SuperTrend tooltip should be present")


if __name__ == '__main__':
    unittest.main() 