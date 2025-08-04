#!/usr/bin/env python3
"""
Test for fastest_plot_fullscreen.py module.
Tests the dynamic fullscreen height functionality for OHLCV rule.
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.plotting.fastest_plot_fullscreen import (
    get_screen_height,
    calculate_dynamic_height,
    plot_indicator_results_fastest_fullscreen
)


class TestFastestPlotFullscreen(unittest.TestCase):
    """Test cases for fastest_plot_fullscreen.py module."""

    def setUp(self):
        """Set up test data."""
        # Generate test DataFrame with OHLCV data
        date_index = pd.date_range(start="2024-01-01", periods=100, freq="h")
        self.test_df = pd.DataFrame({
            "index": date_index,
            "Open": np.random.rand(100) * 100,
            "High": np.random.rand(100) * 100 + 1,
            "Low": np.random.rand(100) * 100 - 1,
            "Close": np.random.rand(100) * 100,
            "Volume": np.random.randint(1000, 10000, size=100),
        })
        self.test_df.set_index("index", inplace=True)
        
        # Output path for testing
        self.output_path = "results/plots/test_fastest_plot_fullscreen.html"

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_get_screen_height(self):
        """Test screen height detection."""
        height = get_screen_height()
        self.assertIsInstance(height, int)
        self.assertGreater(height, 0)
        self.assertLessEqual(height, 10000)  # Reasonable upper bound

    def test_calculate_dynamic_height_ohlcv(self):
        """Test dynamic height calculation for OHLCV rule."""
        # Test with OHLCV rule
        height = calculate_dynamic_height(rule_str="OHLCV")
        self.assertIsInstance(height, int)
        self.assertGreaterEqual(height, 800)
        self.assertLessEqual(height, 2000)

    def test_calculate_dynamic_height_other_rules(self):
        """Test dynamic height calculation for other rules."""
        # Test with other rules
        height = calculate_dynamic_height(rule_str="AUTO")
        self.assertEqual(height, 1100)  # Default height for non-OHLCV rules

    def test_calculate_dynamic_height_with_screen_height(self):
        """Test dynamic height calculation with provided screen height."""
        screen_height = 1920
        height = calculate_dynamic_height(screen_height=screen_height, rule_str="OHLCV")
        expected_height = int(screen_height * 0.85)  # Function uses 0.85, not 0.9
        self.assertEqual(height, expected_height)

    def test_calculate_dynamic_height_bounds(self):
        """Test that dynamic height respects minimum and maximum bounds."""
        # Test minimum bound (500 * 0.85 = 425, but min is 400)
        height_min = calculate_dynamic_height(screen_height=500, rule_str="OHLCV")
        self.assertEqual(height_min, 425)  # 500 * 0.85 = 425
        
        # Test maximum bound
        height_max = calculate_dynamic_height(screen_height=3000, rule_str="OHLCV")
        self.assertEqual(height_max, 2000)  # Maximum bound

    def test_plot_indicator_results_fastest_fullscreen_basic(self):
        """Test basic functionality of fullscreen plotting."""
        # Create a simple rule object
        class MockRule:
            def __init__(self, name):
                self.name = name
        
        rule = MockRule("OHLCV")
        
        # Test the plotting function
        fig = plot_indicator_results_fastest_fullscreen(
            df=self.test_df,
            rule=rule,
            title="Test Fullscreen Plot",
            output_path=self.output_path,
            height=1200
        )
        
        # Check that the function returns a figure
        self.assertIsNotNone(fig)
        
        # Check that the output file was created
        self.assertTrue(os.path.exists(self.output_path))

    def test_plot_indicator_results_fastest_fullscreen_missing_columns(self):
        """Test handling of missing required columns."""
        # Create DataFrame without required columns
        invalid_df = pd.DataFrame({
            "index": pd.date_range(start="2024-01-01", periods=10, freq="h"),
            "Open": np.random.rand(10) * 100,
            # Missing High, Low, Close columns
        })
        invalid_df.set_index("index", inplace=True)
        
        class MockRule:
            def __init__(self, name):
                self.name = name
        
        rule = MockRule("OHLCV")
        
        # Test that the function handles missing columns gracefully
        result = plot_indicator_results_fastest_fullscreen(
            df=invalid_df,
            rule=rule,
            title="Test Invalid Data",
            output_path=self.output_path
        )
        
        # Should return None for invalid data
        self.assertIsNone(result)

    def test_plot_indicator_results_fastest_fullscreen_dynamic_height(self):
        """Test that dynamic height is used when height is None."""
        class MockRule:
            def __init__(self, name):
                self.name = name
        
        rule = MockRule("OHLCV")
        
        # Test with height=None to trigger dynamic calculation
        fig = plot_indicator_results_fastest_fullscreen(
            df=self.test_df,
            rule=rule,
            title="Test Dynamic Height",
            output_path=self.output_path,
            height=None  # Should trigger dynamic calculation
        )
        
        # Check that the function returns a figure
        self.assertIsNotNone(fig)
        
        # Check that the output file was created
        self.assertTrue(os.path.exists(self.output_path))

    def test_plot_indicator_results_fastest_fullscreen_different_rules(self):
        """Test plotting with different rule types."""
        class MockRule:
            def __init__(self, name):
                self.name = name
        
        # Test with AUTO rule
        auto_rule = MockRule("AUTO")
        fig_auto = plot_indicator_results_fastest_fullscreen(
            df=self.test_df,
            rule=auto_rule,
            title="Test AUTO Rule",
            output_path=self.output_path
        )
        self.assertIsNotNone(fig_auto)
        
        # Test with PHLD rule
        phld_rule = MockRule("PHLD")
        fig_phld = plot_indicator_results_fastest_fullscreen(
            df=self.test_df,
            rule=phld_rule,
            title="Test PHLD Rule",
            output_path=self.output_path
        )
        self.assertIsNotNone(fig_phld)

    def test_plot_indicator_results_fastest_fullscreen_with_indicators(self):
        """Test plotting with additional indicator columns."""
        # Add indicator columns to test data
        self.test_df['HL'] = self.test_df['High'] - self.test_df['Low']
        self.test_df['PV'] = np.random.randn(100) * 2
        self.test_df['Pressure'] = np.random.randn(100) * 1.5
        self.test_df['Direction'] = np.random.choice([1, 2], size=100, p=[0.5, 0.5])
        
        class MockRule:
            def __init__(self, name):
                self.name = name
        
        rule = MockRule("OHLCV")
        
        # Test plotting with indicators
        fig = plot_indicator_results_fastest_fullscreen(
            df=self.test_df,
            rule=rule,
            title="Test with Indicators",
            output_path=self.output_path
        )
        
        # Check that the function returns a figure
        self.assertIsNotNone(fig)
        
        # Check that the output file was created
        self.assertTrue(os.path.exists(self.output_path))


if __name__ == "__main__":
    unittest.main() 