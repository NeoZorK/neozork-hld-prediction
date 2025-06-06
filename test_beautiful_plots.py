#!/usr/bin/env python3
"""Simple test for beautiful terminal plotting."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np

# Test basic plotext candlestick functionality
print("Testing basic plotext candlestick...")

try:
    import plotext as plt
    
    # Simple test data
    dates = [1, 2, 3, 4, 5]
    data = {
        'Open': [100, 102, 104, 106, 108],
        'High': [105, 107, 108, 110, 112],
        'Low': [98, 101, 102, 104, 106],
        'Close': [102, 104, 106, 108, 110]
    }
    
    plt.clear_data()
    plt.clear_figure()
    plt.candlestick(dates, data)
    plt.title("🎨 Beautiful Candlestick Chart Test")
    plt.theme('matrix')
    plt.plot_size(100, 20)
    plt.show()
    
    print("✓ Basic candlestick test successful!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test our enhanced terminal plotting
print("\nTesting enhanced terminal plotting...")

try:
    from plotting.term_plot import plot_indicator_results_term
    from common.constants import TradingRule
    
    # Create test DataFrame
    np.random.seed(42)
    
    data = []
    for i in range(15):
        price = 100 + i * 0.5 + np.random.normal(0, 1)
        high = price + np.random.uniform(0.5, 2.0)
        low = price - np.random.uniform(0.5, 2.0)
        close = np.random.uniform(low, high)
        
        data.append({
            'Open': price,
            'High': high,
            'Low': low,
            'Close': close,
            'Volume': np.random.randint(1000, 5000),
            'HL': high - low,
            'Pressure': np.random.uniform(-1, 1),
            'PV': np.random.uniform(-2, 2),
            'Direction': np.random.choice([1, -1, 0], p=[0.3, 0.3, 0.4])
        })
    
    df = pd.DataFrame(data)
    print(f"Created test DataFrame with {len(df)} rows")
    
    # Test different trading rules
    print("\n1. Testing Predict_High_Low_Direction mode...")
    plot_indicator_results_term(df, TradingRule.Predict_High_Low_Direction, "🚀 Beautiful PHLD Chart")
    
    print("\n2. Testing Pressure_Vector mode...")  
    plot_indicator_results_term(df, TradingRule.Pressure_Vector, "💨 Beautiful PV Chart")
    
    print("\n3. Testing AUTO mode...")
    plot_indicator_results_term(df, TradingRule.AUTO, "🎨 Beautiful AUTO Chart")
    
    print("✓ All enhanced terminal plotting tests successful!")
    
except Exception as e:
    print(f"✗ Error in enhanced plotting: {e}")
    import traceback
    traceback.print_exc()
