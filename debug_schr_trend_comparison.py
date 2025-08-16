#!/usr/bin/env python3
"""
Debug script to compare Python and MQL5 SCHR_TREND indicator results
Focus on the period 2025.01-2025.04 where differences are observed
"""

import pandas as pd
import numpy as np
from src.calculation.indicators.trend.schr_trend_ind import calculate_schr_trend, TradingRuleMode

def debug_schr_trend_comparison():
    """Debug SCHR_TREND calculation differences between Python and MQL5"""
    
    # Load data
    print("Loading data...")
    df = pd.read_parquet('./data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet')
    
    # Filter to recent period for detailed analysis
    recent_df = df[df.index >= '2024-01-01'].copy()
    print(f"Analyzing {len(recent_df)} rows from 2024-01-01")
    
    # Calculate SCHR_TREND with same parameters as MQL5
    print("Calculating SCHR_TREND with parameters: 2,zone,95,5,open")
    print(f"tr_mode: {TradingRuleMode.TR_Zone} (Zone mode)")
    
    # Parameters: period=2, tr_mode=3 (TR_Zone), extreme_up=95, extreme_down=5, price_type='open'
    result_tuple = calculate_schr_trend(
        df=recent_df,
        period=2,
        tr_mode=TradingRuleMode.TR_Zone,  # Use numeric value 3
        extreme_up=95,
        extreme_down=5,
        price_type='open'
    )
    
    # Unpack the tuple: (origin, trend, direction, signal, color, purchase_power)
    origin, trend, direction, signal, color, purchase_power = result_tuple
    
    # Create a DataFrame with the results
    result_df = pd.DataFrame({
        'schr_trend_origin': origin,
        'schr_trend': trend,
        'schr_trend_direction': direction,
        'schr_trend_signal': signal,
        'schr_trend_color': color,
        'schr_trend_purchase_power': purchase_power
    }, index=recent_df.index)
    
    # Focus on the problematic period
    focus_period = result_df[result_df.index >= '2025-01-01'].copy()
    
    print("\n=== DETAILED ANALYSIS OF 2025.01-2025.04 PERIOD ===")
    print("Python SCHR_TREND Results:")
    
    for idx, row in focus_period.iterrows():
        direction_val = row['schr_trend_direction']
        color_val = row['schr_trend_color']
        signal_val = row['schr_trend_signal']
        origin_val = row['schr_trend_origin']
        trend_val = row['schr_trend']
        
        # Map direction to color name
        color_name = {
            0: 'No Signal (Grey)',
            1: 'Buy (Blue)', 
            2: 'Sell (Yellow)',
            3: 'DBL Buy (Aqua)',
            4: 'DBL Sell (Red)'
        }.get(direction_val, f'Unknown ({direction_val})')
        
        print(f"{idx.strftime('%Y-%m-%d')}:")
        print(f"  Direction: {direction_val} -> {color_name}")
        print(f"  Color: {color_val}")
        print(f"  Signal: {signal_val}")
        print(f"  Origin: {origin_val:.6f}" if isinstance(origin_val, (int, float)) else f"  Origin: {origin_val}")
        print(f"  Trend: {trend_val:.6f}" if isinstance(trend_val, (int, float)) else f"  Trend: {trend_val}")
        print("")
    
    # Analyze RSI calculation
    print("\n=== RSI CALCULATION ANALYSIS ===")
    
    # Get the last few rows for RSI analysis
    last_rows = recent_df.tail(10)
    
    for idx, row in last_rows.iterrows():
        open_price = row['Open']
        close_price = row['Close']
        
        print(f"{idx.strftime('%Y-%m-%d')}: Open={open_price:.5f}, Close={close_price:.5f}")
    
    # Check if there are any NaN or extreme values
    print("\n=== DATA QUALITY CHECK ===")
    
    # Check for NaN values in key columns
    nan_check = result_df[['schr_trend_direction', 'schr_trend_color', 'schr_trend_signal']].isna().sum()
    print(f"NaN values in key columns: {nan_check.to_dict()}")
    
    # Check for extreme values
    direction_stats = result_df['schr_trend_direction'].describe()
    print(f"Direction statistics: {direction_stats.to_dict()}")
    
    # Check if there are any unexpected values
    unique_directions = result_df['schr_trend_direction'].unique()
    print(f"Unique direction values: {sorted(unique_directions)}")
    
    print("\n=== COMPARISON WITH MQL5 EXPECTED VALUES ===")
    print("MQL5 shows: yellow, yellow, blue, blue")
    print("Python shows: red, red, blue, aqua")
    print("")
    print("Key differences:")
    print("1. 2025-01: MQL5=Yellow(Sell), Python=Red(DBL Sell)")
    print("2. 2025-02: MQL5=Yellow(Sell), Python=Red(DBL Sell)")
    print("3. 2025-03: MQL5=Blue(Buy), Python=Blue(Buy) ✓")
    print("4. 2025-04: MQL5=Blue(Buy), Python=Aqua(DBL Buy)")
    print("")
    print("This suggests Python is more aggressive in signal generation")
    print("Python shows DBL signals where MQL5 shows regular signals")

if __name__ == "__main__":
    debug_schr_trend_comparison()
