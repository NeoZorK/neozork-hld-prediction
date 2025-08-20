#!/usr/bin/env python3
"""
Debug script to check Wave indicator columns and signal generation.
"""

import pandas as pd
import numpy as np
from src.calculation.indicators.trend.wave_ind import (
    apply_rule_wave, WaveParameters, ENUM_MOM_TR, ENUM_GLOBAL_TR
)
from src.calculation.indicators.base_indicator import PriceType
from src.common.constants import BUY, SELL, NOTRADE

def debug_wave_columns():
    """Debug the Wave indicator columns and signal generation."""
    
    # Load test data
    df = pd.read_parquet('data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet')
    print(f"Loaded data: {len(df)} rows")
    print(f"Original columns: {list(df.columns)}")
    print()
    
    # Create Wave parameters for the specific command
    wave_params = WaveParameters(
        long1=339,
        fast1=10,
        trend1=2,
        tr1=ENUM_MOM_TR.TR_Fast,
        long2=22,
        fast2=11,
        trend2=4,
        tr2=ENUM_MOM_TR.TR_Fast,
        global_tr=ENUM_GLOBAL_TR.G_TR_PRIME,
        sma_period=10
    )
    
    print("Wave Parameters:")
    print(f"  long1: {wave_params.long1}")
    print(f"  fast1: {wave_params.fast1}")
    print(f"  trend1: {wave_params.trend1}")
    print(f"  tr1: {wave_params.tr1}")
    print(f"  long2: {wave_params.long2}")
    print(f"  fast2: {wave_params.fast2}")
    print(f"  trend2: {wave_params.trend2}")
    print(f"  tr2: {wave_params.tr2}")
    print(f"  global_tr: {wave_params.global_tr}")
    print(f"  sma_period: {wave_params.sma_period}")
    print()
    
    # Apply Wave indicator with CLOSE price type
    result_df = apply_rule_wave(df, wave_params, PriceType.CLOSE)
    
    print("Wave Indicator Results:")
    print(f"Result columns: {list(result_df.columns)}")
    print()
    
    # Check all signal-related columns
    signal_columns = [col for col in result_df.columns if any(keyword in col.lower() for keyword in ['signal', 'direction', 'color', 'wave'])]
    print("Signal-related columns:")
    for col in signal_columns:
        unique_values = result_df[col].value_counts()
        print(f"  {col}: {dict(unique_values)}")
    print()
    
    # Check specific columns that should contain signals
    important_columns = ['_Signal', '_Direction', '_Plot_Color', 'Wave1', 'Wave2']
    print("Important signal columns:")
    for col in important_columns:
        if col in result_df.columns:
            unique_values = result_df[col].value_counts()
            print(f"  {col}: {dict(unique_values)}")
        else:
            print(f"  {col}: NOT FOUND")
    print()
    
    # Check if there are any non-zero signals
    if '_Signal' in result_df.columns:
        non_zero_signals = result_df[result_df['_Signal'] != NOTRADE]
        print(f"Non-zero signals in _Signal: {len(non_zero_signals)}")
        if len(non_zero_signals) > 0:
            print("Sample non-zero signals:")
            print(non_zero_signals[['_Signal', '_Direction', '_Plot_Color']].head())
    print()
    
    # Check wave calculations
    if 'wave1' in result_df.columns and 'wave2' in result_df.columns:
        print("Wave calculations:")
        print(f"  wave1 range: {result_df['wave1'].min():.6f} to {result_df['wave1'].max():.6f}")
        print(f"  wave2 range: {result_df['wave2'].min():.6f} to {result_df['wave2'].max():.6f}")
        print(f"  wave1 non-null: {result_df['wave1'].notna().sum()}")
        print(f"  wave2 non-null: {result_df['wave2'].notna().sum()}")
    print()
    
    # Check fastline calculations
    if 'fastline1' in result_df.columns and 'fastline2' in result_df.columns:
        print("Fastline calculations:")
        print(f"  fastline1 range: {result_df['fastline1'].min():.6f} to {result_df['fastline1'].max():.6f}")
        print(f"  fastline2 range: {result_df['fastline2'].min():.6f} to {result_df['fastline2'].max():.6f}")
        print(f"  fastline1 non-null: {result_df['fastline1'].notna().sum()}")
        print(f"  fastline2 non-null: {result_df['fastline2'].notna().sum()}")
    print()
    
    # Show sample data
    print("Sample data (last 5 rows):")
    sample_cols = ['Close', 'wave1', 'fastline1', 'wave2', 'fastline2', '_Signal', '_Direction', '_Plot_Color']
    available_cols = [col for col in sample_cols if col in result_df.columns]
    print(result_df[available_cols].tail())

if __name__ == "__main__":
    debug_wave_columns()
