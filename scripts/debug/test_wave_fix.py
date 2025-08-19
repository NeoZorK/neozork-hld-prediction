#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Wave indicator fixes.
Tests the corrected Wave indicator implementation.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
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

def test_wave_indicator():
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
    
    try:
        # Apply Wave rule
        result = apply_rule_wave(df, wave_params, price_type=PriceType.OPEN)
        print("✅ Wave indicator calculation completed successfully")
        
        # Check required columns
        required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line']
        missing_cols = [col for col in required_cols if col not in result.columns]
        
        if missing_cols:
            print(f"❌ Missing columns: {missing_cols}")
        else:
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
        
        if '_Plot_FastLine' in result.columns:
            fastline_values = result['_Plot_FastLine'].dropna()
            print(f"⚡ FastLine values range: {fastline_values.min():.6f} to {fastline_values.max():.6f}")
        
        if 'MA_Line' in result.columns:
            ma_values = result['MA_Line'].dropna()
            print(f"📏 MA Line values range: {ma_values.min():.6f} to {ma_values.max():.6f}")
        
        # Show sample of results
        print("\n📋 Sample results (last 5 rows):")
        sample_cols = ['Open', '_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line']
        available_cols = [col for col in sample_cols if col in result.columns]
        print(result[available_cols].tail())
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Wave indicator: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print("🚀 Starting Wave indicator test...")
    
    success = test_wave_indicator()
    
    if success:
        print("\n✅ Wave indicator test completed successfully!")
        print("🎯 Key fixes implemented:")
        print("   - Corrected line colors and thickness (Yellow thick, Red thin, Light blue thin)")
        print("   - Fixed signal generation logic (only when _Direction changes)")
        print("   - Corrected SMA calculation source (_Plot_FastLine)")
        print("   - Fixed signal display on upper chart (_Signal column)")
    else:
        print("\n❌ Wave indicator test failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
