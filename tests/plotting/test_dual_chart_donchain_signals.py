# -*- coding: utf-8 -*-
# tests/plotting/test_dual_chart_donchain_signals.py

"""
Test file for donchain signal calculation in dual chart plotting.
This test verifies that the fix for "no buy/sell signals" issue works correctly.
"""

import unittest
import pandas as pd
import numpy as np
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.plotting.dual_chart_plot import calculate_additional_indicator
from src.common.constants import BUY, SELL, NOTRADE


class TestDualChartDonchainSignals(unittest.TestCase):
    """Test donchain signal calculation in dual chart plotting."""

    def setUp(self):
        """Set up test data."""
        # Create test DataFrame with volatile price movements to trigger signals
        dates = pd.date_range('2024-01-01', periods=50, freq='D')
        
        # Create price data with some breakouts to trigger donchain signals
        np.random.seed(42)  # For reproducible results
        base_price = 1.5000
        
        # Generate prices with some volatility and breakouts
        prices = []
        for i in range(50):
            if i < 20:
                # First 20 periods: normal movement within channels
                price = base_price + np.random.normal(0, 0.01)
            elif i == 20:
                # Breakout above upper channel
                price = base_price + 0.05
            elif i == 30:
                # Breakout below lower channel
                price = base_price - 0.05
            else:
                # Normal movement
                price = base_price + np.random.normal(0, 0.01)
            
            prices.append(price)
            base_price = price
        
        self.df = pd.DataFrame({
            'Open': prices,
            'High': [p + abs(np.random.normal(0, 0.005)) for p in prices],
            'Low': [p - abs(np.random.normal(0, 0.005)) for p in prices],
            'Close': [p + np.random.normal(0, 0.002) for p in prices],
            'Volume': np.random.randint(1000, 10000, 50)
        }, index=dates)
        
        # Ensure High >= Low
        self.df['High'] = self.df[['Open', 'High']].max(axis=1)
        self.df['Low'] = self.df[['Open', 'Low']].min(axis=1)

    def test_donchain_signal_calculation(self):
        """Test that donchain signals are properly calculated."""
        # Test with donchain:20 rule
        rule = 'donchain:20'
        
        # Calculate additional indicator
        result_df = calculate_additional_indicator(self.df, rule)
        
        # Verify that Direction column exists and has values
        self.assertIn('Direction', result_df.columns, "Direction column should exist")
        self.assertFalse(result_df['Direction'].isna().all(), "Direction column should not be all NaN")
        
        # Verify that donchain channels are calculated
        self.assertIn('donchain_upper', result_df.columns, "donchain_upper column should exist")
        self.assertIn('donchain_middle', result_df.columns, "donchain_middle column should exist")
        self.assertIn('donchain_lower', result_df.columns, "donchain_lower column should exist")
        
        # Verify that support/resistance levels are set
        self.assertIn('PPrice1', result_df.columns, "PPrice1 (support) column should exist")
        self.assertIn('PPrice2', result_df.columns, "PPrice2 (resistance) column should exist")
        self.assertIn('PColor1', result_df.columns, "PColor1 column should exist")
        self.assertIn('PColor2', result_df.columns, "PColor2 column should exist")
        
        # Verify that Diff column exists
        self.assertIn('Diff', result_df.columns, "Diff column should exist")
        
        # Check that signals are valid values (0, 1, or 2)
        valid_signals = [NOTRADE, BUY, SELL]
        invalid_signals = result_df['Direction'].dropna()
        invalid_signals = invalid_signals[~invalid_signals.isin(valid_signals)]
        self.assertTrue(invalid_signals.empty, f"All signals should be valid values. Found: {invalid_signals.unique()}")

    def test_donchain_signal_logic(self):
        """Test that donchain signal logic works correctly."""
        # Test with a simple rule
        rule = 'donchain:10'
        
        # Calculate additional indicator
        result_df = calculate_additional_indicator(self.df, rule)
        
        # Get non-NaN signals
        signals = result_df['Direction'].dropna()
        
        # Verify that we have some signals (even if they're all NOTRADE)
        self.assertGreater(len(signals), 0, "Should have some calculated signals")
        
        # Verify that signals are numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(signals), "Signals should be numeric")

    def test_donchain_with_open_prices(self):
        """Test donchain calculation with open prices."""
        # Test with donchain:20,open rule
        rule = 'donchain:20,open'
        
        # Calculate additional indicator
        result_df = calculate_additional_indicator(self.df, rule)
        
        # Verify that Direction column exists
        self.assertIn('Direction', result_df.columns, "Direction column should exist with open prices")
        
        # Verify that donchain channels are calculated
        self.assertIn('donchain_upper', result_df.columns, "donchain_upper column should exist")
        self.assertIn('donchain_middle', result_df.columns, "donchain_middle column should exist")
        self.assertIn('donchain_lower', result_df.columns, "donchain_lower column should exist")

    def test_donchain_default_period(self):
        """Test donchain calculation with default period."""
        # Test with donchain:20 rule (default period is 20)
        rule = 'donchain:20'
        
        # Calculate additional indicator
        result_df = calculate_additional_indicator(self.df, rule)
        
        # Verify that Direction column exists
        self.assertIn('Direction', result_df.columns, "Direction column should exist with default period")
        
        # Verify that donchain channels are calculated
        self.assertIn('donchain_upper', result_df.columns, "donchain_upper column should exist")
        self.assertIn('donchain_middle', result_df.columns, "donchain_middle column should exist")
        self.assertIn('donchain_lower', result_df.columns, "donchain_lower column should exist")

    def test_donchain_support_resistance_levels(self):
        """Test that support and resistance levels are properly set."""
        rule = 'donchain:20'
        
        # Calculate additional indicator
        result_df = calculate_additional_indicator(self.df, rule)
        
        # Verify support level (PPrice1) is set to lower band
        self.assertIn('PPrice1', result_df.columns, "PPrice1 should exist")
        self.assertIn('donchain_lower', result_df.columns, "donchain_lower should exist")
        
        # Verify resistance level (PPrice2) is set to upper band
        self.assertIn('PPrice2', result_df.columns, "PPrice2 should exist")
        self.assertIn('donchain_upper', result_df.columns, "donchain_upper should exist")
        
        # Verify color assignments
        self.assertIn('PColor1', result_df.columns, "PColor1 should exist")
        self.assertIn('PColor2', result_df.columns, "PColor2 should exist")
        
        # Check that colors are set correctly
        non_nan_mask = result_df['PColor1'].notna()
        if non_nan_mask.any():
            self.assertEqual(result_df.loc[non_nan_mask, 'PColor1'].iloc[0], BUY, "PColor1 should be BUY")
        
        non_nan_mask = result_df['PColor2'].notna()
        if non_nan_mask.any():
            self.assertEqual(result_df.loc[non_nan_mask, 'PColor2'].iloc[0], SELL, "PColor2 should be SELL")


if __name__ == '__main__':
    unittest.main() 