#!/usr/bin/env python3
"""
Script to check PutCallRatio values for different periods
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from src.calculation.indicators.sentiment.putcallratio_ind import apply_rule_putcallratio

def main():
    # Load mn1 data
    data_path = "data/CSVExport_GBPUSD_PERIOD_MN1.parquet."
    if not os.path.exists(data_path):
        print(f"Data file not found: {data_path}")
        return
    
    df = pd.read_parquet(data_path)
    print(f"Loaded data: {len(df)} rows")
    print(f"Columns: {list(df.columns)}")
    
    point = 0.01  # Default point size
    
    # Test different periods
    periods = [5, 10, 20, 50, 100]
    
    for period in periods:
        print(f"\n=== Testing period {period} ===")
        result = apply_rule_putcallratio(df.copy(), point, putcall_period=period)
        
        # Get PutCallRatio values
        putcall_values = result['PutCallRatio'].dropna()
        signals = result['PutCallRatio_Signal'].dropna()
        
        print(f"PutCallRatio values: {len(putcall_values)} valid")
        print(f"Range: {putcall_values.min():.2f} - {putcall_values.max():.2f}")
        print(f"Mean: {putcall_values.mean():.2f}")
        print(f"Std: {putcall_values.std():.2f}")
        
        # Count signals
        buy_signals = np.sum(signals == 1)
        sell_signals = np.sum(signals == 2)
        no_trade = np.sum(signals == 0)
        
        print(f"Signals: {len(signals)} total")
        print(f"  Buy: {buy_signals}")
        print(f"  Sell: {sell_signals}")
        print(f"  No Trade: {no_trade}")
        
        # Show first few values
        print(f"First 5 PutCallRatio values: {putcall_values.head().values}")
        print(f"First 5 signals: {signals.head().values}")

if __name__ == "__main__":
    main() 