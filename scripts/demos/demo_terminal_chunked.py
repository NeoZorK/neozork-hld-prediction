#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# scripts/demos/demo_terminal_chunked.py

"""
Demo script for PHLD terminal chunked plotting functionality.
Shows how to use the enhanced terminal mode with automatic chunking for PHLD rule.
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from plotting.term_chunked_plot import plot_chunked_terminal


def create_sample_data(rows=1000):
    """Create sample OHLCV data for demonstration."""
    print(f"Creating sample data with {rows} rows...")
    
    # Create date range
    dates = pd.date_range('2023-01-01', periods=rows, freq='1h')
    
    # Create OHLCV data
    base_price = 100.0
    data = []
    
    for i in range(rows):
        # Simulate price movement
        change = np.random.normal(0, 0.5)
        base_price += change
        
        # Create OHLC
        open_price = base_price
        high_price = base_price + abs(np.random.normal(0, 0.3))
        low_price = base_price - abs(np.random.normal(0, 0.3))
        close_price = base_price + np.random.normal(0, 0.2)
        
        # Ensure OHLC relationship
        high_price = max(high_price, open_price, close_price)
        low_price = min(low_price, open_price, close_price)
        
        # Volume
        volume = np.random.randint(1000, 10000)
        
        data.append({
            'Open': open_price,
            'High': high_price,
            'Low': low_price,
            'Close': close_price,
            'Volume': volume
        })
    
    df = pd.DataFrame(data, index=dates)
    print(f"Created sample data: {len(df)} rows, {len(df.columns)} columns")
    return df


def create_indicator_data(df):
    """Add PHLD indicator columns to the DataFrame."""
    print("Adding PHLD indicator columns...")
    
    # Add PHLD-specific indicators
    df['PPrice1'] = df['Low'] * 0.95  # Support Channel
    df['PPrice2'] = df['High'] * 1.05  # Resistance Channel
    df['Direction'] = np.random.choice([0, 1, 2], len(df))  # NOTRADE, BUY, SELL
    
    print(f"Added PHLD indicator columns: {list(df.columns)}")
    return df


def demo_phld_mode(df):
    """Demonstrate PHLD mode."""
    print("\n" + "="*60)
    print("DEMO: PHLD MODE (Predict High Low Direction)")
    print("="*60)
    print("Shows channels and buy/sell signals")
    print("Two channels with trading signals")
    print("="*60)
    
    try:
        plot_chunked_terminal(df, 'PHLD', 'Demo PHLD Mode', style="matrix")
        print("✅ PHLD mode completed successfully!")
    except Exception as e:
        print(f"❌ Error in PHLD mode: {e}")


def main():
    """Main demo function."""
    print("🚀 PHLD TERMINAL CHUNKED PLOTTING DEMO")
    print("="*60)
    print("This demo showcases the enhanced terminal mode with automatic chunking")
    print("PHLD rule visualization optimized for terminal display")
    print("="*60)
    
    # Create sample data
    df = create_sample_data(1000)
    df = create_indicator_data(df)
    
    print(f"\n📊 Sample data created:")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Date range: {df.index[0]} to {df.index[-1]}")
    print(f"   Price range: {df['Low'].min():.2f} - {df['High'].max():.2f}")
    
    # Run PHLD demo
    demo_phld_mode(df)
    
    print("\n" + "="*60)
    print("🎉 PHLD DEMO COMPLETED!")
    print("="*60)
    print("Key features demonstrated:")
    print("✅ Automatic chunking for optimal viewing")
    print("✅ PHLD-specific visualizations")
    print("✅ Interactive navigation between chunks")
    print("✅ Comprehensive statistics for each chunk")
    print("✅ Support for PHLD trading rule")
    print("="*60)
    print("\nTo use in your own analysis:")
    print("python run_analysis.py show csv your_file.csv -d term --rule PHLD")
    print("="*60)


if __name__ == "__main__":
    main() 