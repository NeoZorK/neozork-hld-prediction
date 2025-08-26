#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Wave indicator fixes.
Tests the corrected Wave indicator implementation.
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

def create_test_data():
    """Create test data for Wave indicator."""
    # Create sample OHLCV data
    index = pd.date_range('2023-01-01', periods=100, freq='D')
    
    # Create trending price data
    base_price = 100
    trend = np.linspace(0, 20, 100)  # Upward trend
    noise = np.random.normal(0, 0.5, 100)
    
    df = pd.DataFrame({
        'Open': base_price + trend + noise,
        'High': base_price + trend + noise + 0.5,
        'Low': base_price + trend + noise - 0.5,
        'Close': base_price + trend + noise + 0.1,
        'Volume': np.random.randint(1000, 10000, 100)
    }, index=index)
    
    return df

class TestWaveFix:
    """Test class for Wave indicator fixes"""
    
    def test_wave_indicator(self):
        """Test the corrected Wave indicator."""
        print("🔍 Testing Wave indicator fixes...")
        
        # Create test data
        df = create_test_data()
        print(f"📊 Created test data with {len(df)} rows")
        
        # Create Wave parameters (using default values from MQ5)
        wave_params = WaveParameters(
            long1=339, fast1=10, trend1=2, tr1=ENUM_MOM_TR.TR_Fast,
            long2=22, fast2=11, trend2=4, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=22
        )
        
        print(f"⚙️  Wave parameters: {wave_params}")
        
        # Apply Wave rule
        result = apply_rule_wave(df, wave_params, price_type=PriceType.OPEN)
        print("✅ Wave indicator calculation completed successfully")
        
        # Check required columns
        required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line']
        missing_cols = [col for col in required_cols if col not in result.columns]
        
        assert not missing_cols, f"Missing columns: {missing_cols}"
        print("✅ All required columns present")
        
        # Check signal generation
        signals = result['_Signal'].dropna()
        buy_signals = (signals == 1).sum()
        sell_signals = (signals == 2).sum()
        
        print(f"📈 Buy signals: {buy_signals}")
        print(f"📉 Sell signals: {sell_signals}")
        print(f"📊 Total signals: {len(signals)}")
        
        # Check line values
        if '_Plot_Wave' in result.columns:
            wave_values = result['_Plot_Wave'].dropna()
            print(f"🌊 Wave values range: {wave_values.min():.6f} to {wave_values.max():.6f}")
            assert len(wave_values) > 0, "Wave values should not be empty"
        
        if '_Plot_FastLine' in result.columns:
            fastline_values = result['_Plot_FastLine'].dropna()
            print(f"⚡ FastLine values range: {fastline_values.min():.6f} to {fastline_values.max():.6f}")
            assert len(fastline_values) > 0, "FastLine values should not be empty"
        
        if 'MA_Line' in result.columns:
            ma_values = result['MA_Line'].dropna()
            print(f"📏 MA Line values range: {ma_values.min():.6f} to {ma_values.max():.6f}")
            assert len(ma_values) > 0, "MA Line values should not be empty"
        
        # Check color values for Wave line
        if '_Plot_Color' in result.columns:
            color_values = result['_Plot_Color'].dropna()
            unique_colors = color_values.unique()
            print(f"🎨 Wave line colors: {unique_colors}")
            print(f"   - Black (NOTRADE=0): {(color_values == 0).sum()} points")
            print(f"   - Red (BUY=1): {(color_values == 1).sum()} points")
            print(f"   - Blue (SELL=2): {(color_values == 2).sum()} points")
            
            # Check that we have valid colors
            valid_colors = {0, 1, 2}
            assert all(color in valid_colors for color in unique_colors), f"Invalid colors found: {unique_colors}"
        
        # Show sample of results
        print("\n📋 Sample results (last 10 rows):")
        sample_cols = ['Open', '_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
        available_cols = [col for col in sample_cols if col in result.columns]
        print(result[available_cols].tail(10).to_string())
        
        print("\n✅ Wave indicator test completed successfully!")


if __name__ == "__main__":
    # Run test manually
    test_instance = TestWaveFix()
    test_instance.test_wave_indicator()
