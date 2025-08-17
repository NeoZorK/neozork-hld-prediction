#!/usr/bin/env python3
"""
Debug script to analyze RSI on real GBPUSD data
"""

import pandas as pd
import numpy as np
from src.calculation.indicators.trend.schr_trend_ind import calculate_rsi, PriceType

def analyze_real_data_rsi():
    """Analyze RSI on real GBPUSD data"""
    
    # Load real data
    print("Loading real GBPUSD data...")
    df = pd.read_parquet('./data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet')
    
    # Filter to recent period
    recent_df = df[df.index >= '2024-01-01'].copy()
    print(f"Analyzing {len(recent_df)} rows from 2024-01-01")
    
    # Focus on the problematic period
    focus_period = recent_df[recent_df.index >= '2025-01-01'].copy()
    print(f"Focus period: {len(focus_period)} rows from 2025-01-01")
    
    print("\n=== REAL DATA ANALYSIS ===")
    print("Open prices for 2025:")
    for date, row in focus_period.iterrows():
        print(f"{date.strftime('%Y-%m-%d')}: Open={row['Open']:.5f}")
    
    print("\n=== RSI CALCULATION ===")
    
    # Calculate RSI with period=2
    period = 2
    rsi_values = calculate_rsi(recent_df, period, PriceType.OPEN)
    
    print(f"RSI calculation for period={period}:")
    for date, rsi in zip(recent_df.index, rsi_values):
        if date >= pd.Timestamp('2025-01-01'):
            print(f"{date.strftime('%Y-%m-%d')}: RSI={rsi:.6f}")
    
    print("\n=== DETAILED RSI ANALYSIS ===")
    
    # Analyze the specific bars that generate extreme signals
    for i, (date, row) in enumerate(focus_period.iterrows()):
        if i < len(rsi_values):
            rsi = rsi_values.iloc[i]
            open_price = row['Open']
            
            print(f"\n{date.strftime('%Y-%m-%d')}:")
            print(f"  Open: {open_price:.5f}")
            print(f"  RSI: {rsi:.6f}")
            
            # Check if this is one of the first bars
            if i < period:
                print(f"  Note: This is one of the first {period} bars - RSI may be incomplete")
            
            # Analyze price changes
            if i > 0:
                prev_open = focus_period.iloc[i-1]['Open']
                change = open_price - prev_open
                print(f"  Change from previous: {change:.6f}")
                
                if change > 0:
                    print(f"  Positive change -> should contribute to gains")
                elif change < 0:
                    print(f"  Negative change -> should contribute to losses")
                else:
                    print(f"  No change -> neutral")
    
    print("\n=== COMPARISON WITH MQL5 ===")
    print("MQL5 shows: yellow, yellow, blue, blue")
    print("Python shows: red, red, blue, aqua")
    print()
    print("The issue is that Python RSI calculation generates extreme values (0.0, 100.0)")
    print("while MQL5 may use different thresholds or calculation method.")

if __name__ == "__main__":
    analyze_real_data_rsi()
