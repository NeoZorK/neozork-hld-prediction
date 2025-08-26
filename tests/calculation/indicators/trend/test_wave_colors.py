#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Wave indicator colors.
Tests that Wave line shows correct colors: Black (NOTRADE=0), Red (BUY=1), Blue (SELL=2)
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import pandas as pd
import numpy as np
import pytest
from src.calculation.indicators.trend.wave_ind import (
    apply_rule_wave, WaveParameters, ENUM_MOM_TR, ENUM_GLOBAL_TR
)
from src.calculation.indicators.base_indicator import PriceType

def create_test_data_with_trends():
    """Create test data that generates both BUY and SELL signals."""
    # Create sample OHLCV data with alternating trends
    index = pd.date_range('2023-01-01', periods=200, freq='D')
    
    # Create data with alternating trends to generate both BUY and SELL signals
    base_price = 100
    trend1 = np.linspace(0, 10, 100)  # First upward trend
    trend2 = np.linspace(10, -5, 100)  # Then downward trend
    
    trend = np.concatenate([trend1, trend2])
    noise = np.random.normal(0, 0.3, 200)
    
    df = pd.DataFrame({
        'Open': base_price + trend + noise,
        'High': base_price + trend + noise + 0.5,
        'Low': base_price + trend + noise - 0.5,
        'Close': base_price + trend + noise + 0.1,
        'Volume': np.random.randint(1000, 10000, 200)
    }, index=index)
    
    return df

class TestWaveColors:
    """Test class for Wave indicator colors"""
    
    def test_wave_colors(self):
        """Test that Wave indicator shows correct colors."""
        print("🎨 Testing Wave indicator colors...")
        
        # Create test data
        df = create_test_data_with_trends()
        print(f"📊 Created test data with {len(df)} rows")
        
        # Create Wave parameters with shorter periods to generate more signals
        wave_params = WaveParameters(
            long1=50, fast1=10, trend1=2, tr1=ENUM_MOM_TR.TR_Fast,
            long2=25, fast2=8, trend2=2, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=10
        )
        
        print(f"⚙️  Wave parameters: {wave_params}")
        
        # Apply Wave rule
        result = apply_rule_wave(df, wave_params, price_type=PriceType.OPEN)
        print("✅ Wave indicator calculation completed successfully")
        
        # Check color values for Wave line
        assert '_Plot_Color' in result.columns, "Wave color column not found"
        
        color_values = result['_Plot_Color'].dropna()
        unique_colors = sorted(color_values.unique())
        print(f"🎨 Wave line colors found: {unique_colors}")
        
        for color in unique_colors:
            count = (color_values == color).sum()
            if color == 0:
                print(f"   - Black (NOTRADE=0): {count} points")
            elif color == 1:
                print(f"   - Red (BUY=1): {count} points")
            elif color == 2:
                print(f"   - Blue (SELL=2): {count} points")
            else:
                print(f"   - Unknown color ({color}): {count} points")
        
        # Check that we have all expected colors
        expected_colors = {0, 1, 2}
        assert set(unique_colors) == expected_colors, f"Missing colors: {expected_colors - set(unique_colors)}"
        print("✅ All expected colors present: Black, Red, Blue")
        
        # Check signal generation
        signals = result['_Signal'].dropna()
        buy_signals = (signals == 1).sum()
        sell_signals = (signals == 2).sum()
        
        print(f"\n📈 Buy signals (_Signal=1): {buy_signals}")
        print(f"📉 Sell signals (_Signal=2): {sell_signals}")
        print(f"📊 Total signals: {len(signals)}")
        
        # Show sample of results
        print("\n📋 Sample results (last 10 rows):")
        sample_cols = ['Open', '_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
        available_cols = [col for col in sample_cols if col in result.columns]
        print(result[available_cols].tail(10).to_string())
        
        print("\n✅ Wave colors test completed successfully!")


if __name__ == "__main__":
    # Run test manually
    test_instance = TestWaveColors()
    test_instance.test_wave_colors()
