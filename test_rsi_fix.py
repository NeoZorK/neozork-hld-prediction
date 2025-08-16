#!/usr/bin/env python3
"""
Test the fixed RSI calculation function
"""

import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from calculation.indicators.trend.schr_trend_ind import calculate_rsi, PriceType

def test_rsi_fix():
    """Test the fixed RSI calculation"""
    
    print("=== TESTING FIXED RSI CALCULATION ===")
    
    # Create test data similar to the problematic period
    test_data = pd.DataFrame({
        'Open': [1.27189, 1.25125, 1.22820, 1.25810, 1.29178],
        'Close': [1.25119, 1.23879, 1.25770, 1.29164, 1.33782]
    }, index=pd.to_datetime(['2024-12-01', '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01']))
    
    print("Test data:")
    for idx, row in test_data.iterrows():
        print(f"{idx.strftime('%Y-%m-%d')}: Open={row['Open']:.5f}, Close={row['Close']:.5f}")
    
    print("\nCalculating RSI with period=2...")
    
    # Calculate RSI using the fixed function
    rsi_values = calculate_rsi(test_data, period=2, price_type=PriceType.OPEN)
    
    print("\nRSI Results:")
    for idx, rsi in rsi_values.items():
        print(f"{idx.strftime('%Y-%m-%d')}: RSI = {rsi:.6f}")
    
    # Check the specific problematic values
    print("\n=== ANALYSIS ===")
    
    # 2025-01-01: Should be > 50 (Sell) not 0 (DBL Sell)
    rsi_2025_01 = rsi_values.loc['2025-01-01']
    print(f"2025-01-01: RSI = {rsi_2025_01:.6f}")
    if rsi_2025_01 > 50:
        print("  ✓ RSI > 50 → Will show Sell (Yellow) like MQL5")
    else:
        print("  ❌ RSI <= 50 → Will show DBL Sell (Red) - WRONG!")
    
    # 2025-02-01: Should be > 50 (Sell) not 0 (DBL Sell)
    rsi_2025_02 = rsi_values.loc['2025-02-01']
    print(f"2025-02-01: RSI = {rsi_2025_02:.6f}")
    if rsi_2025_02 > 50:
        print("  ✓ RSI > 50 → Will show Sell (Yellow) like MQL5")
    else:
        print("  ❌ RSI <= 50 → Will show DBL Sell (Red) - WRONG!")
    
    # 2025-03-01: Should be > 50 (Buy) - this was working
    rsi_2025_03 = rsi_values.loc['2025-03-01']
    print(f"2025-03-01: RSI = {rsi_2025_03:.6f}")
    if rsi_2025_03 > 50:
        print("  ✓ RSI > 50 → Will show Buy (Blue) like MQL5")
    else:
        print("  ❌ RSI <= 50 → Will show wrong signal")
    
    # 2025-04-01: Should be > 95 (DBL Buy) - this was working
    rsi_2025_04 = rsi_values.loc['2025-04-01']
    print(f"2025-04-01: RSI = {rsi_2025_04:.6f}")
    if rsi_2025_04 > 95:
        print("  ✓ RSI > 50 → Will show DBL Buy (Aqua) like MQL5")
    else:
        print("  ❌ RSI <= 95 → Will show wrong signal")

if __name__ == "__main__":
    test_rsi_fix()
