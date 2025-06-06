#!/usr/bin/env python3
"""
Demo script showcasing terminal plotting capabilities with larger dataset
"""

import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_terminal_plotting():
    """Demonstrate terminal plotting with mn1.csv dataset"""
    
    print("=" * 70)
    print("🚀 TERMINAL PLOTTING DEMO - LARGER DATASET")
    print("=" * 70)
    
    try:
        from plotting.plotting import plot_indicator_results
        from common.constants import TradingRule
        
        # Load larger dataset
        df = pd.read_csv('data/mn1.csv')
        print(f"✓ Loaded MN1 data: {len(df)} rows")
        print(f"✓ Columns: {list(df.columns)}")
        
        # Show first few rows of data
        print(f"\n📊 First 3 rows of data:")
        print(df.head(3).to_string())
        
        # Take a sample for better visualization (terminal has limited space)
        df_sample = df.tail(10)  # Last 10 rows for recent data
        print(f"\n📈 Using last {len(df_sample)} rows for visualization...")
        
        # Demo 1: PHLD plotting with larger dataset
        print(f"\n1. 📊 PHLD Terminal Plot Demo...")
        result = plot_indicator_results(
            df_sample, 
            TradingRule.Predict_High_Low_Direction, 
            title="📈 MN1 Data - PHLD Analysis (Recent 10 bars)", 
            mode="term"
        )
        
        print(f"\n" + "="*70)
        print("✅ TERMINAL PLOTTING DEMO COMPLETED SUCCESSFULLY!")
        print("💡 Terminal plots work great for:")
        print("   - SSH/Remote terminal sessions")
        print("   - Docker containers without GUI")
        print("   - Quick data visualization in CLI")
        print("   - Automated reporting and monitoring")
        print("="*70)
        
    except Exception as e:
        print(f"✗ Error in demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_terminal_plotting()
