#!/usr/bin/env python3
"""Test script to explore plotext candlestick functionality."""

import plotext as plt
import pandas as pd
import numpy as np

# Create sample OHLC data
dates = pd.date_range('2024-01-01', periods=20, freq='D')
np.random.seed(42)

# Generate realistic OHLC data
base_price = 100
prices = [base_price]
for _ in range(19):
    change = np.random.normal(0, 2)
    prices.append(max(50, prices[-1] + change))

data = []
for i, price in enumerate(prices):
    # Generate OHLC for each day
    volatility = np.random.uniform(0.5, 3.0)
    high = price + np.random.uniform(0, volatility)
    low = price - np.random.uniform(0, volatility)
    close = np.random.uniform(low, high)
    
    data.append({
        'Date': dates[i],
        'Open': price,
        'High': high,
        'Low': low,
        'Close': close,
        'Volume': np.random.randint(1000, 10000)
    })

df = pd.DataFrame(data)

print("Sample OHLC data:")
print(df.head())
print()

# Test candlestick function
print("Testing candlestick function...")
try:
    plt.clear_data()
    plt.clear_figure()
    
    # Try different ways to call candlestick
    print("Method 1: Using lists...")
    dates_num = list(range(len(df)))
    opens = df['Open'].tolist()
    highs = df['High'].tolist()
    lows = df['Low'].tolist()
    closes = df['Close'].tolist()
    
    plt.candlestick(dates_num, opens, highs, lows, closes)
    plt.title("Candlestick Chart Test")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.theme('dark')
    plt.plot_size(100, 25)
    
    print("Displaying candlestick chart...")
    plt.show()
    
except Exception as e:
    print(f"Error with candlestick function: {e}")
    print(f"Exception type: {type(e).__name__}")

# Test other advanced features
print("\nTesting other plotext features...")

try:
    plt.clear_data()
    plt.clear_figure()
    
    # Test stacked bar for volume
    plt.subplot(2, 1, 1)
    plt.candlestick(dates_num, opens, highs, lows, closes)
    plt.title("Price Chart")
    
    plt.subplot(2, 1, 2)
    plt.bar(dates_num, df['Volume'].tolist(), color='blue')
    plt.title("Volume")
    
    plt.show()
    
except Exception as e:
    print(f"Error with subplots: {e}")

# Test available themes and styling
print("\nTesting themes...")
for theme in ['dark', 'matrix', 'elegant', 'retro']:
    try:
        plt.clear_data()
        plt.clear_figure()
        plt.theme(theme)
        plt.plot(dates_num[:5], closes[:5], color='green', marker='o')
        plt.title(f"Theme: {theme}")
        plt.plot_size(60, 10)
        plt.show()
        print(f"✓ Theme {theme} works")
    except Exception as e:
        print(f"✗ Theme {theme} failed: {e}")
