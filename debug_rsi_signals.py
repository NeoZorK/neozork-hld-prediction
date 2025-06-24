#!/usr/bin/env python3
"""
Debug script to analyze RSI signals and understand why strategy parameters don't affect results.
"""

import pandas as pd
import numpy as np
from src.calculation.indicator_calculation import calculate_indicator
from src.calculation.trading_metrics import calculate_trading_metrics
from src.common.constants import BUY, SELL, NOTRADE

def analyze_rsi_signals():
    """Analyze RSI signals and trading metrics."""
    
    # Load data
    df = pd.read_parquet('data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet')
    print(f"Original data shape: {df.shape}")
    print(f"Original columns: {df.columns.tolist()}")
    
    # Calculate RSI indicator
    result_df = calculate_indicator(df, 'rsi:14,30,70,open', point_size=0.01)
    print(f"\nAfter RSI calculation shape: {result_df.shape}")
    print(f"New columns: {result_df.columns.tolist()}")
    
    # Analyze Direction signals
    direction_counts = result_df['Direction'].value_counts().sort_index()
    print(f"\nDirection signal counts:")
    for value, count in direction_counts.items():
        signal_type = "NOTRADE" if value == 0 else "BUY" if value == 1 else "SELL"
        percentage = (count / len(result_df)) * 100
        print(f"  {value} ({signal_type}): {count} times ({percentage:.1f}%)")
    
    # Calculate metrics with different strategy parameters
    print(f"\n=== Trading Metrics Analysis ===")
    
    # Strategy 1: 1,5,0.07
    metrics1 = calculate_trading_metrics(
        result_df, 
        lot_size=1.0, 
        risk_reward_ratio=5.0, 
        fee_per_trade=0.07
    )
    
    # Strategy 2: 1,1,0.07  
    metrics2 = calculate_trading_metrics(
        result_df, 
        lot_size=1.0, 
        risk_reward_ratio=1.0, 
        fee_per_trade=0.07
    )
    
    print(f"\nStrategy 1 (1,5,0.07):")
    print(f"  Buy signals: {metrics1.get('buy_count', 0)}")
    print(f"  Sell signals: {metrics1.get('sell_count', 0)}")
    print(f"  Total trades: {metrics1.get('total_trades', 0)}")
    print(f"  Win ratio: {metrics1.get('win_ratio', 0):.1f}%")
    print(f"  Profit factor: {metrics1.get('profit_factor', 0):.2f}")
    print(f"  Net return: {metrics1.get('net_return', 0):.2f}%")
    print(f"  Strategy efficiency: {metrics1.get('strategy_efficiency', 0):.1f}%")
    
    print(f"\nStrategy 2 (1,1,0.07):")
    print(f"  Buy signals: {metrics2.get('buy_count', 0)}")
    print(f"  Sell signals: {metrics2.get('sell_count', 0)}")
    print(f"  Total trades: {metrics2.get('total_trades', 0)}")
    print(f"  Win ratio: {metrics2.get('win_ratio', 0):.1f}%")
    print(f"  Profit factor: {metrics2.get('profit_factor', 0):.2f}")
    print(f"  Net return: {metrics2.get('net_return', 0):.2f}%")
    print(f"  Strategy efficiency: {metrics2.get('strategy_efficiency', 0):.1f}%")
    
    # Check if metrics are identical
    identical = True
    for key in ['buy_count', 'sell_count', 'total_trades', 'win_ratio', 'profit_factor', 'net_return', 'strategy_efficiency']:
        if abs(metrics1.get(key, 0) - metrics2.get(key, 0)) > 0.001:
            identical = False
            print(f"  DIFFERENCE in {key}: {metrics1.get(key, 0)} vs {metrics2.get(key, 0)}")
    
    if identical:
        print(f"\n⚠️  WARNING: All metrics are identical! This suggests:")
        print(f"   1. Very few trading signals (mostly NOTRADE)")
        print(f"   2. Strategy parameters don't affect the calculation")
        print(f"   3. The RSI indicator may need parameter tuning")
    
    # Show some actual trades
    print(f"\n=== Sample Trading Signals ===")
    signals_df = result_df[result_df['Direction'] != 0].copy()
    if len(signals_df) > 0:
        print(f"Found {len(signals_df)} trading signals:")
        for idx, row in signals_df.head(10).iterrows():
            signal_type = "BUY" if row['Direction'] == 1 else "SELL"
            print(f"  {idx}: {signal_type} at {row['Open']:.5f}")
    else:
        print("No trading signals found!")
    
    # Analyze RSI values
    if 'RSI' in result_df.columns:
        print(f"\n=== RSI Analysis ===")
        rsi_values = result_df['RSI'].dropna()
        print(f"RSI range: {rsi_values.min():.1f} - {rsi_values.max():.1f}")
        print(f"RSI mean: {rsi_values.mean():.1f}")
        print(f"RSI std: {rsi_values.std():.1f}")
        
        # Check oversold/overbought conditions
        oversold_count = (rsi_values < 30).sum()
        overbought_count = (rsi_values > 70).sum()
        print(f"Oversold (<30): {oversold_count} times")
        print(f"Overbought (>70): {overbought_count} times")

if __name__ == "__main__":
    analyze_rsi_signals() 