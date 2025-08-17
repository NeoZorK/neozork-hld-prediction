#!/usr/bin/env python3
"""
Debug script to analyze RSI calculations and compare with MQL5
"""

import pandas as pd
import numpy as np
from src.calculation.indicators.trend.schr_trend_ind import calculate_rsi, PriceType

def analyze_rsi_calculation():
    """Analyze RSI calculation step by step"""
    
    # Create test data that should generate specific RSI values
    dates = pd.date_range('2025-01-01', periods=10, freq='D')
    
    # Test data with specific patterns
    test_data = pd.DataFrame({
        'Open': [1.2500, 1.2600, 1.2700, 1.2800, 1.2900, 1.3000, 1.3100, 1.3200, 1.3300, 1.3400],
        'High': [1.2550, 1.2650, 1.2750, 1.2850, 1.2950, 1.3050, 1.3150, 1.3250, 1.3350, 1.3450],
        'Low': [1.2450, 1.2550, 1.2650, 1.2750, 1.2850, 1.2950, 1.3050, 1.3150, 1.3250, 1.3350],
        'Close': [1.2520, 1.2620, 1.2720, 1.2820, 1.2920, 1.3020, 1.3120, 1.3220, 1.3320, 1.3420],
        'Volume': [1000] * 10
    }, index=dates)
    
    print("Test data:")
    print(test_data)
    print()
    
    # Calculate RSI step by step
    period = 2
    prices = test_data['Open']
    
    print(f"RSI calculation for period={period}:")
    print("Step-by-step analysis:")
    
    for i in range(1, len(prices)):
        # Calculate price changes
        delta = prices.iloc[i] - prices.iloc[i-1]
        
        # Calculate gains and losses
        gains = max(delta, 0)
        losses = max(-delta, 0)
        
        print(f"Bar {i}: Open={prices.iloc[i]:.5f}, Change={delta:.5f}, Gains={gains:.5f}, Losses={losses:.5f}")
    
    print()
    
    # Calculate RSI using our function
    rsi_values = calculate_rsi(test_data, period, PriceType.OPEN)
    
    print("RSI values:")
    for i, (date, rsi) in enumerate(zip(dates, rsi_values)):
        print(f"{date.strftime('%Y-%m-%d')}: RSI={rsi:.6f}")
    
    print()
    
    # Analyze why we get extreme values
    print("Analysis of extreme RSI values:")
    for i, rsi in enumerate(rsi_values):
        if rsi == 0.0 or rsi > 99.0:
            print(f"Bar {i}: RSI={rsi:.6f} - EXTREME VALUE")
            if i > 0:
                prev_open = prices.iloc[i-1]
                curr_open = prices.iloc[i]
                change = curr_open - prev_open
                print(f"  Open change: {prev_open:.5f} -> {curr_open:.5f} = {change:.5f}")
                
                # Check if this is the first few bars
                if i < period + 1:
                    print(f"  This is one of the first {period + 1} bars - RSI calculation may be incomplete")
    
    print()
    
    # Test with different periods
    print("Testing different RSI periods:")
    for test_period in [1, 2, 3, 5]:
        test_rsi = calculate_rsi(test_data, test_period, PriceType.OPEN)
        print(f"Period {test_period}: RSI values = {[f'{r:.2f}' for r in test_rsi]}")
    
    print()
    
    # Check if the issue is with the RSI calculation or the signal logic
    print("Signal logic test:")
    extreme_up = 95
    extreme_down = 5
    
    for i, rsi in enumerate(rsi_values):
        if pd.isna(rsi):
            continue
            
        # Apply Zone TR logic
        if rsi > 50:
            if rsi > extreme_up:
                signal = "DBL_BUY (Aqua)"
            else:
                signal = "BUY (Blue)"
        else:
            if rsi < extreme_down:
                signal = "DBL_SELL (Red)"
            else:
                signal = "SELL (Yellow)"
        
        print(f"Bar {i}: RSI={rsi:.2f} -> {signal}")

if __name__ == "__main__":
    analyze_rsi_calculation()
