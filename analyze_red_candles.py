#!/usr/bin/env python3
"""
Analyze red candles (DBL Sell) in SCHR_TREND indicator
Find why there are so many red candles and fix the algorithm
"""

import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from calculation.indicators.trend.schr_trend_ind import calculate_schr_trend, TradingRuleMode

def analyze_red_candles():
    """Analyze why there are so many red candles in SCHR_TREND"""
    
    print("=== ANALYZING RED CANDLES IN SCHR_TREND ===")
    
    # Load data
    print("Loading data...")
    df = pd.read_parquet('./data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet')
    
    # Calculate SCHR_TREND
    print("Calculating SCHR_TREND with parameters: 2,zone,95,5,open")
    
    result_tuple = calculate_schr_trend(
        df=df,
        period=2,
        tr_mode=TradingRuleMode.TR_Zone,
        extreme_up=95,
        extreme_down=5,
        price_type='open'
    )
    
    # Unpack results
    origin, trend, direction, signal, color, purchase_power = result_tuple
    
    # Create DataFrame
    result_df = pd.DataFrame({
        'schr_trend_origin': origin,
        'schr_trend': trend,
        'schr_trend_direction': direction,
        'schr_trend_signal': signal,
        'schr_trend_color': color,
        'schr_trend_purchase_power': purchase_power
    }, index=df.index)
    
    # Analyze color distribution
    print("\n=== COLOR DISTRIBUTION ANALYSIS ===")
    
    color_counts = result_df['schr_trend_color'].value_counts().sort_index()
    print("Color distribution:")
    color_names = {0: 'No Signal (Grey)', 1: 'Buy (Blue)', 2: 'Sell (Yellow)', 
                   3: 'DBL Buy (Aqua)', 4: 'DBL Sell (Red)'}
    
    for color_val, count in color_counts.items():
        color_name = color_names.get(color_val, f'Unknown ({color_val})')
        percentage = (count / len(result_df)) * 100
        print(f"  {color_name}: {count} ({percentage:.1f}%)")
    
    # Analyze RSI values that lead to red candles
    print("\n=== RSI ANALYSIS FOR RED CANDLES ===")
    
    red_candles = result_df[result_df['schr_trend_color'] == 4]
    print(f"Total red candles (DBL Sell): {len(red_candles)}")
    
    if len(red_candles) > 0:
        print("\nRSI values for red candles:")
        print(f"  Min RSI: {red_candles['schr_trend_origin'].min():.6f}")
        print(f"  Max RSI: {red_candles['schr_trend_origin'].max():.6f}")
        print(f"  Mean RSI: {red_candles['schr_trend_origin'].mean():.6f}")
        
        # Show some examples
        print("\nExamples of red candles:")
        for i, (idx, row) in enumerate(red_candles.head(10).iterrows()):
            print(f"  {idx.strftime('%Y-%m-%d')}: RSI = {row['schr_trend_origin']:.6f}")
            if i >= 9:  # Show only first 10
                break
    
    # Analyze extreme RSI values
    print("\n=== EXTREME RSI VALUES ANALYSIS ===")
    
    extreme_low = result_df[result_df['schr_trend_origin'] < 5]
    extreme_high = result_df[result_df['schr_trend_origin'] > 95]
    
    print(f"RSI < 5 (extreme down): {len(extreme_low)} candles")
    print(f"RSI > 95 (extreme up): {len(extreme_high)} candles")
    
    # Check if RSI = 0 is causing issues
    rsi_zero = result_df[result_df['schr_trend_origin'] == 0]
    print(f"RSI = 0: {len(rsi_zero)} candles")
    
    if len(rsi_zero) > 0:
        print("RSI = 0 candles:")
        for idx, row in rsi_zero.head(5).iterrows():
            print(f"  {idx.strftime('%Y-%m-%d')}: Color = {row['schr_trend_color']}")
    
    # Compare with MQL5 expected behavior
    print("\n=== COMPARISON WITH MQL5 EXPECTED BEHAVIOR ===")
    print("MQL5 typically shows:")
    print("  - RSI > 50: Buy (Blue)")
    print("  - RSI < 50: Sell (Yellow)")
    print("  - RSI > 95: DBL Buy (Aqua) - only for very strong signals")
    print("  - RSI < 5: DBL Sell (Red) - only for very strong signals")
    
    print("\nPython currently shows:")
    print(f"  - DBL Sell (Red): {len(red_candles)} candles ({len(red_candles)/len(result_df)*100:.1f}%)")
    print("  - This suggests the algorithm is too aggressive in detecting extreme signals")
    
    # Recommendations
    print("\n=== RECOMMENDATIONS ===")
    print("1. Check if RSI calculation is correct")
    print("2. Verify extreme thresholds (5 and 95)")
    print("3. Ensure RSI = 0 is handled properly")
    print("4. Compare with MQL5 iRSI() function behavior")
    print("5. Consider adjusting the extreme_down threshold")

if __name__ == "__main__":
    analyze_red_candles()
