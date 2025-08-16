#!/usr/bin/env python3
"""
Debug RSI calculation for SCHR_TREND indicator
"""

import pandas as pd
import numpy as np

def calculate_rsi(prices, period=2):
    """Calculate RSI exactly like in SCHR_TREND indicator."""
    delta = prices.diff()
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()
    
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_rsi_alternative(prices, period=2):
    """Alternative RSI calculation method."""
    delta = prices.diff()
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # Use exponential moving average instead of simple moving average
    avg_gains = gains.ewm(span=period).mean()
    avg_losses = losses.ewm(span=period).mean()
    
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    return rsi

def main():
    # Load data
    try:
        df = pd.read_parquet('./data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet')
        print(f"Data loaded: {len(df)} rows")
        print(f"Date range: {df.index[0]} to {df.index[-1]}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Calculate RSI using different methods, price types, and periods
    rsi_values_open_2 = calculate_rsi(df['Open'], period=2)
    rsi_alt_open_2 = calculate_rsi_alternative(df['Open'], period=2)
    rsi_values_close_2 = calculate_rsi(df['Close'], period=2)
    rsi_alt_close_2 = calculate_rsi_alternative(df['Close'], period=2)
    
    # Test with period 1 (like MQL5 might use)
    rsi_values_open_1 = calculate_rsi(df['Open'], period=1)
    rsi_values_close_1 = calculate_rsi(df['Close'], period=1)
    
    # Show last 20 bars with detailed analysis (Open prices, period 2)
    print("\nLast 20 bars with RSI analysis (Open prices, period 2):")
    print("Date\t\tOpen\t\tClose\t\tRSI(SMA)\tRSI(EMA)\tExpected\tColor")
    print("-" * 100)
    
    for i in range(-20, 0):
        date = df.index[i].strftime('%Y-%m-%d')
        open_price = df['Open'].iloc[i]
        close_price = df['Close'].iloc[i]
        rsi_sma = rsi_values_open_2.iloc[i]
        rsi_ema = rsi_alt_open_2.iloc[i]
        
        # Determine expected signal based on RSI (Zone mode)
        if pd.isna(rsi_sma):
            signal = "N/A"
            color = "N/A"
        elif rsi_sma > 95:
            signal = "DBL_BUY (3)"
            color = "Aqua"
        elif rsi_sma > 50:
            signal = "BUY (1)"
            color = "Blue"
        elif rsi_sma < 5:
            signal = "DBL_SELL (4)"
            color = "Red"
        else:
            signal = "SELL (2)"
            color = "Yellow"
        
        print(f'{date}\t{open_price:.5f}\t{close_price:.5f}\t{rsi_sma:.2f}\t\t{rsi_ema:.2f}\t\t{signal}\t\t{color}')
    
    print("\n" + "="*100)
    print("RSI Logic:")
    print("RSI > 95: DBL_BUY (3) - Aqua")
    print("RSI > 50: BUY (1) - Blue")
    print("RSI < 5:  DBL_SELL (4) - Red")
    print("RSI <= 50: SELL (2) - Yellow")
    print("="*100)
    
    # Test with Close prices, period 2
    print("\nLast 20 bars with RSI analysis (Close prices, period 2):")
    print("Date\t\tOpen\t\tClose\t\tRSI(SMA)\tRSI(EMA)\tExpected\tColor")
    print("-" * 100)
    
    for i in range(-20, 0):
        date = df.index[i].strftime('%Y-%m-%d')
        open_price = df['Open'].iloc[i]
        close_price = df['Close'].iloc[i]
        rsi_sma = rsi_values_close_2.iloc[i]
        rsi_ema = rsi_alt_close_2.iloc[i]
        
        # Determine expected signal based on RSI (Zone mode)
        if pd.isna(rsi_sma):
            signal = "N/A"
            color = "N/A"
        elif rsi_sma > 95:
            signal = "DBL_BUY (3)"
            color = "Aqua"
        elif rsi_sma > 50:
            signal = "BUY (1)"
            color = "Blue"
        elif rsi_sma < 5:
            signal = "DBL_SELL (4)"
            color = "Red"
        else:
            signal = "SELL (2)"
            color = "Yellow"
        
        print(f'{date}\t{open_price:.5f}\t{close_price:.5f}\t{rsi_sma:.2f}\t\t{rsi_ema:.2f}\t\t{signal}\t\t{color}')
    
    print("\n" + "="*100)
    print("Comparison (period 2):")
    print("Open prices RSI (last):", rsi_values_open_2.iloc[-1])
    print("Close prices RSI (last):", rsi_values_close_2.iloc[-1])
    print("="*100)
    
    # Test with period 1
    print("\nLast 20 bars with RSI analysis (Open prices, period 1):")
    print("Date\t\tOpen\t\tClose\t\tRSI(period1)\tExpected\tColor")
    print("-" * 100)
    
    for i in range(-20, 0):
        date = df.index[i].strftime('%Y-%m-%d')
        open_price = df['Open'].iloc[i]
        close_price = df['Close'].iloc[i]
        rsi_1 = rsi_values_open_1.iloc[i]
        
        # Determine expected signal based on RSI (Zone mode)
        if pd.isna(rsi_1):
            signal = "N/A"
            color = "N/A"
        elif rsi_1 > 95:
            signal = "DBL_BUY (3)"
            color = "Aqua"
        elif rsi_1 > 50:
            signal = "BUY (1)"
            color = "Blue"
        elif rsi_1 < 5:
            signal = "DBL_SELL (4)"
            color = "Red"
        else:
            signal = "SELL (2)"
            color = "Yellow"
        
        print(f'{date}\t{open_price:.5f}\t{close_price:.5f}\t{rsi_1:.2f}\t\t\t{signal}\t\t{color}')
    
    print("\n" + "="*100)
    print("Comparison (period 1):")
    print("Open prices RSI (last):", rsi_values_open_1.iloc[-1])
    print("Close prices RSI (last):", rsi_values_close_1.iloc[-1])
    print("="*100)
    
    # Check for potential data differences
    print("\nData Analysis:")
    print(f"Last Open price: {df['Open'].iloc[-1]:.5f}")
    print(f"Last Close price: {df['Close'].iloc[-1]:.5f}")
    print(f"Last High price: {df['High'].iloc[-1]:.5f}")
    print(f"Last Low price: {df['Low'].iloc[-1]:.5f}")
    
    # Check if there are any NaN values in RSI
    nan_count = rsi_values_open_2.isna().sum() # Changed to rsi_values_open_2 for consistency
    print(f"NaN values in RSI: {nan_count}")
    
    # Check RSI range
    print(f"RSI range: {rsi_values_open_2.min():.2f} to {rsi_values_open_2.max():.2f}") # Changed to rsi_values_open_2 for consistency

    print("="*100)
    
    # Test with different extreme points
    print("\nTesting with different extreme points:")
    print("Standard: >95 = DBL_BUY, <5 = DBL_SELL")
    print("Alternative 1: >90 = DBL_BUY, <10 = DBL_SELL")
    print("Alternative 2: >80 = DBL_BUY, <20 = DBL_SELL")
    print("-" * 100)
    
    # Test last few bars with different extreme points
    print("Last 5 bars with different extreme points:")
    print("Date\t\tRSI\t\tStd(95/5)\tAlt1(90/10)\tAlt2(80/20)")
    print("-" * 100)
    
    for i in range(-5, 0):
        date = df.index[i].strftime('%Y-%m-%d')
        rsi = rsi_values_open_2.iloc[i]
        
        if pd.isna(rsi):
            std_signal = "N/A"
            alt1_signal = "N/A"
            alt2_signal = "N/A"
        else:
            # Standard (95/5)
            if rsi > 95:
                std_signal = "DBL_BUY(3)"
            elif rsi > 50:
                std_signal = "BUY(1)"
            elif rsi < 5:
                std_signal = "DBL_SELL(4)"
            else:
                std_signal = "SELL(2)"
            
            # Alternative 1 (90/10)
            if rsi > 90:
                alt1_signal = "DBL_BUY(3)"
            elif rsi > 50:
                alt1_signal = "BUY(1)"
            elif rsi < 10:
                alt1_signal = "DBL_SELL(4)"
            else:
                alt1_signal = "SELL(2)"
            
            # Alternative 2 (80/20)
            if rsi > 80:
                alt2_signal = "DBL_BUY(3)"
            elif rsi > 50:
                alt2_signal = "BUY(1)"
            elif rsi < 20:
                alt2_signal = "DBL_SELL(4)"
            else:
                alt2_signal = "SELL(2)"
        
        print(f'{date}\t{rsi:.2f}\t\t{std_signal}\t\t{alt1_signal}\t\t{alt2_signal}')
    
    print("\n" + "="*100)
    print("Hypothesis: MQL5 might use different extreme points!")
    print("If MQL5 uses 80/20 instead of 95/5, then:")
    print("RSI = 100.00 → RSI > 80 → DBL_BUY(3) - Aqua")
    print("But if MQL5 uses different logic, we need to investigate further")
    print("="*100)

if __name__ == "__main__":
    main()
