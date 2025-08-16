#!/usr/bin/env python3
"""
Debug RSI calculation in Python SCHR_TREND indicator
Compare with expected MQL5 behavior
"""

import pandas as pd
import numpy as np

def calculate_rsi_manual(prices, period=2):
    """Manual RSI calculation to debug the issue"""
    
    if len(prices) < period + 1:
        print(f"Not enough data: {len(prices)} < {period + 1}")
        return pd.Series([np.nan] * len(prices), index=prices.index)
    
    # Calculate price changes
    delta = prices.diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    print(f"Price changes (first 5): {delta.head().tolist()}")
    print(f"Gains (first 5): {gains.head().tolist()}")
    print(f"Losses (first 5): {losses.head().tolist()}")
    
    # Calculate average gains and losses
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()
    
    print(f"Average gains (first 5): {avg_gains.head().tolist()}")
    print(f"Average losses (first 5): {avg_losses.head().tolist()}")
    
    # Calculate RS and RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    
    print(f"RS (first 5): {rs.head().tolist()}")
    print(f"RSI (first 5): {rsi.head().tolist()}")
    
    return rsi

def debug_rsi_issue():
    """Debug RSI calculation issue"""
    
    print("=== DEBUGGING RSI CALCULATION ISSUE ===")
    
    # Load data
    print("\nLoading data...")
    df = pd.read_parquet('./data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet')
    
    # Focus on the problematic period
    focus_df = df[df.index >= '2024-12-01'].copy()
    print(f"Focus period: {len(focus_df)} rows from {focus_df.index[0]} to {focus_df.index[-1]}")
    
    # Show the data
    print("\n=== DATA FOR RSI CALCULATION ===")
    for idx, row in focus_df.iterrows():
        print(f"{idx.strftime('%Y-%m-%d')}: Open={row['Open']:.5f}, Close={row['Close']:.5f}")
    
    # Calculate RSI manually
    print("\n=== MANUAL RSI CALCULATION ===")
    print("Using Open prices (as in MQL5)")
    
    open_prices = focus_df['Open']
    rsi_values = calculate_rsi_manual(open_prices, period=2)
    
    print(f"\nFinal RSI values:")
    for idx, rsi in rsi_values.items():
        print(f"{idx.strftime('%Y-%m-%d')}: RSI = {rsi:.6f}")
    
    # Check for NaN values
    print(f"\nNaN values in RSI: {rsi_values.isna().sum()}")
    print(f"Zero values in RSI: {(rsi_values == 0).sum()}")
    
    # Analyze the issue
    print("\n=== ANALYSIS ===")
    print("Problem: RSI = 0.000000 for 2025-01 and 2025-02")
    print("This causes Python to show DBL Sell (Red) instead of Sell (Yellow)")
    print("")
    print("Expected behavior (MQL5):")
    print("- 2025-01: RSI should be > 50 → Sell (Yellow)")
    print("- 2025-02: RSI should be > 50 → Sell (Yellow)")
    print("- 2025-03: RSI = 56.47 → Buy (Blue) ✓")
    print("- 2025-04: RSI = 100.00 → DBL Buy (Aqua)")
    print("")
    print("Python behavior:")
    print("- 2025-01: RSI = 0.00 → DBL Sell (Red) ❌")
    print("- 2025-02: RSI = 0.00 → DBL Sell (Red) ❌")
    print("- 2025-03: RSI = 56.47 → Buy (Blue) ✓")
    print("- 2025-04: RSI = 100.00 → DBL Buy (Aqua) ✓")
    
    # Check if there's a division by zero issue
    print("\n=== POTENTIAL ISSUES ===")
    print("1. Division by zero in RSI calculation")
    print("2. Insufficient data for period=2")
    print("3. NaN handling in rolling window")
    print("4. Price data quality issues")

if __name__ == "__main__":
    debug_rsi_issue()
