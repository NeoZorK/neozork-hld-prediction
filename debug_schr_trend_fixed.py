#!/usr/bin/env python3
"""
Debug script to test fixed SCHR_TREND indicator
"""

import pandas as pd
import numpy as np
from src.calculation.indicators.trend.schr_trend_ind import calculate_schr_trend, TradingRuleMode

def test_fixed_schr_trend():
    """Test fixed SCHR_TREND calculation"""
    
    # Create test data with known RSI values
    dates = pd.date_range('2025-01-01', periods=4, freq='M')
    
    # Test data with specific RSI values to match MQL5 behavior
    test_data = pd.DataFrame({
        'Open': [1.2500, 1.2600, 1.2700, 1.2800],
        'High': [1.2550, 1.2650, 1.2750, 1.2850],
        'Low': [1.2450, 1.2550, 1.2650, 1.2750],
        'Close': [1.2520, 1.2620, 1.2720, 1.2820],
        'Volume': [1000, 1000, 1000, 1000]
    }, index=dates)
    
    print("Test data:")
    print(test_data)
    print()
    
    # Calculate SCHR_TREND with fixed parameters
    result_tuple = calculate_schr_trend(
        df=test_data,
        period=2,
        tr_mode=TradingRuleMode.TR_Zone,
        extreme_up=95,
        extreme_down=5,
        price_type='open'
    )
    
    origin, trend, direction, signal, color, purchase_power = result_tuple
    
    print("SCHR_TREND Results:")
    print(f"Origin (RSI): {origin.values}")
    print(f"Trend: {trend.values}")
    print(f"Direction: {direction.values}")
    print(f"Signal: {signal.values}")
    print(f"Color: {color.values}")
    print()
    
    # Map values to color names
    color_names = {
        0: 'No Signal (Grey)',
        1: 'Buy (Blue)', 
        2: 'Sell (Yellow)',
        3: 'DBL Buy (Aqua)',
        4: 'DBL Sell (Red)'
    }
    
    print("Color mapping:")
    for i, (date, dir_val, col_val) in enumerate(zip(dates, direction, color)):
        print(f"{date.strftime('%Y-%m')}: Direction={dir_val} -> {color_names.get(dir_val, 'Unknown')}")
        print(f"         Color={col_val} -> {color_names.get(col_val, 'Unknown')}")
        print(f"         RSI={origin.iloc[i]:.2f}")
        print()

if __name__ == "__main__":
    test_fixed_schr_trend()
