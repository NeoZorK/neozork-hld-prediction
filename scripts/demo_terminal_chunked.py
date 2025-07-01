#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# scripts/demo_terminal_chunked.py

"""
Demo script for the new terminal chunked plotting functionality.
Shows how to use the enhanced terminal mode with automatic chunking for different rules.
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
    """Add indicator columns to the DataFrame."""
    print("Adding indicator columns...")
    
    # Add some basic indicators
    df['RSI'] = np.random.uniform(0, 100, len(df))
    df['PV'] = np.random.uniform(-1, 1, len(df))
    df['PPrice1'] = df['Low'] * 0.95  # Support
    df['PPrice2'] = df['High'] * 1.05  # Resistance
    df['Direction'] = np.random.choice([0, 1, 2], len(df))  # NOTRADE, BUY, SELL
    df['RSI_Momentum'] = np.random.uniform(-5, 5, len(df))
    df['Diff'] = np.random.uniform(0, 1, len(df))
    
    print(f"Added indicator columns: {list(df.columns)}")
    return df


def demo_ohlcv_mode(df):
    """Demonstrate OHLCV mode."""
    print("\n" + "="*60)
    print("DEMO: OHLCV MODE")
    print("="*60)
    print("Shows OHLC candlestick charts + separate volume charts")
    print("Data is automatically split into optimal chunks")
    print("="*60)
    
    try:
        plot_chunked_terminal(df, 'OHLCV', 'Demo OHLCV Mode', style="matrix")
        print("✅ OHLCV mode completed successfully!")
    except Exception as e:
        print(f"❌ Error in OHLCV mode: {e}")


def demo_auto_mode(df):
    """Demonstrate AUTO mode."""
    print("\n" + "="*60)
    print("DEMO: AUTO MODE")
    print("="*60)
    print("Shows each field on separate charts")
    print("Perfect for exploring all available data")
    print("="*60)
    
    try:
        plot_chunked_terminal(df, 'AUTO', 'Demo AUTO Mode', style="dots")
        print("✅ AUTO mode completed successfully!")
    except Exception as e:
        print(f"❌ Error in AUTO mode: {e}")


def demo_pv_mode(df):
    """Demonstrate PV mode."""
    print("\n" + "="*60)
    print("DEMO: PV MODE (Pressure Vector)")
    print("="*60)
    print("Shows Pressure Vector with buy/sell signals")
    print("Includes support/resistance lines and trading signals")
    print("="*60)
    
    try:
        plot_chunked_terminal(df, 'PV', 'Demo PV Mode', style="matrix")
        print("✅ PV mode completed successfully!")
    except Exception as e:
        print(f"❌ Error in PV mode: {e}")


def demo_sr_mode(df):
    """Demonstrate SR mode."""
    print("\n" + "="*60)
    print("DEMO: SR MODE (Support/Resistance)")
    print("="*60)
    print("Shows Support/Resistance lines")
    print("Two lines without signals for clean analysis")
    print("="*60)
    
    try:
        plot_chunked_terminal(df, 'SR', 'Demo SR Mode', style="matrix")
        print("✅ SR mode completed successfully!")
    except Exception as e:
        print(f"❌ Error in SR mode: {e}")


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


def demo_rsi_modes(df):
    """Demonstrate RSI modes."""
    print("\n" + "="*60)
    print("DEMO: RSI MODES")
    print("="*60)
    print("Shows RSI calculations with different variants")
    print("Includes momentum and divergence analysis")
    print("="*60)
    
    rsi_rules = [
        ('rsi(14,70,30,close)', 'Basic RSI'),
        ('rsi_mom(14,70,30,open)', 'RSI Momentum'),
        ('rsi_div(20,80,20,close)', 'RSI Divergence')
    ]
    
    for rule, description in rsi_rules:
        print(f"\n--- {description} ---")
        try:
            plot_chunked_terminal(df, rule, f'Demo {description}', style="matrix")
            print(f"✅ {description} completed successfully!")
        except Exception as e:
            print(f"❌ Error in {description}: {e}")


def main():
    """Main demo function."""
    print("🚀 TERMINAL CHUNKED PLOTTING DEMO")
    print("="*60)
    print("This demo showcases the enhanced terminal mode with automatic chunking")
    print("Each rule type has a specific visualization optimized for terminal display")
    print("="*60)
    
    # Create sample data
    df = create_sample_data(1000)
    df = create_indicator_data(df)
    
    print(f"\n📊 Sample data created:")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Date range: {df.index[0]} to {df.index[-1]}")
    print(f"   Price range: {df['Low'].min():.2f} - {df['High'].max():.2f}")
    
    # Run demos
    demo_ohlcv_mode(df)
    demo_auto_mode(df)
    demo_pv_mode(df)
    demo_sr_mode(df)
    demo_phld_mode(df)
    demo_rsi_modes(df)
    
    print("\n" + "="*60)
    print("🎉 DEMO COMPLETED!")
    print("="*60)
    print("Key features demonstrated:")
    print("✅ Automatic chunking for optimal viewing")
    print("✅ Rule-specific visualizations")
    print("✅ Interactive navigation between chunks")
    print("✅ Comprehensive statistics for each chunk")
    print("✅ Support for all trading rules")
    print("✅ RSI variants with parameterized rules")
    print("="*60)
    print("\nTo use in your own analysis:")
    print("python run_analysis.py show csv your_file.csv -d term --rule OHLCV")
    print("python run_analysis.py show csv your_file.csv -d term --rule rsi:14,70,30,close")
    print("="*60)


if __name__ == "__main__":
    main() 