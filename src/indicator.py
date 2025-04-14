# -*- coding: utf-8 -*-
# src/indicator.py

"""
Main module for calculating the Shcherbyna Pressure Vector indicator.
Orchestrates calls to core calculations and rule-specific logic.
"""

import pandas as pd
import numpy as np
import __init__ # For version access

# Import from other modules within the src package
from .constants import TradingRule, EMPTY_VALUE
from .core_calculations import (
    calculate_hl,
    calculate_pressure,
    calculate_pv,
    calculate_lwma,
    calculate_core1,
    reverse_signal_value
)
from .rules import apply_trading_rule
from .plotting import plot_indicator_results # Import plotting function

# --- Main Calculation Orchestrator ---
def calculate_pressure_vector(
    df: pd.DataFrame,
    point: float, # Instrument's point size (e.g., 0.00001 for EURUSD)
    core_back: int = 2,
    limit: int = 1000,
    strength_back: int = 1,
    tr_num: TradingRule = TradingRule.PV_HighLow,
    pv_tp_multy: int = 10,
    reverse_signal: bool = False
) -> pd.DataFrame:
    """
    Calculates the Shcherbyna Pressure Vector indicator by orchestrating
    core calculations and applying the selected trading rule.

    Args:
        df (pd.DataFrame): Input DataFrame with 'Open', 'High', 'Low', 'Close', 'TickVolume'.
                           Index should be DateTime. Sorted ascending.
        point (float): Instrument point size. Cannot be zero.
        core_back (int): Period for CORE1 calculation. Default is 2.
        limit (int): Threshold for Tick_Volume_Limit rule. Default is 1000.
        strength_back (int): Period for LWMA (SMMA) calculation. Default is 1. Must be >= 1.
        tr_num (TradingRule): Enum selecting the calculation mode/output rule.
        pv_tp_multy (int): Multiplication factor for PV TakeProfit rules. Default is 10.
        reverse_signal (bool): Whether to reverse the final signals. Default is False.

    Returns:
        pd.DataFrame: DataFrame with original data and calculated indicator values/signals.
                      Includes 'Volume' instead of 'TickVolume'.
    """
    # --- Input Validation ---
    if not isinstance(df.index, pd.DatetimeIndex):
        print("Warning: DataFrame index is not a DatetimeIndex. Plotting might be affected.")
    required_cols = ['Open', 'High', 'Low', 'Close', 'TickVolume']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Input DataFrame must contain columns: {required_cols}")
    if point == 0:
        raise ValueError("Point size cannot be zero.")
    if strength_back < 1:
        print("Warning: strength_back < 1, LWMA will be NaN.")
        # Allow strength_back=0 or less, handled in calculate_lwma
    # core_back validation handled within calculate_core1

    # Make a copy to avoid modifying the original DataFrame
    df_out = df.copy()
    # Rename TickVolume for consistency and plotting
    df_out.rename(columns={'TickVolume': 'Volume'}, inplace=True)


    # --- Core Calculations ---
    # Shifted values needed for calculations
    high_prev = df_out['High'].shift(1)
    low_prev = df_out['Low'].shift(1)
    open_prev = df_out['Open'].shift(1)
    volume_prev = df_out['Volume'].shift(1) # Use renamed 'Volume'

    # Calculate HL
    df_out['HL'] = calculate_hl(high_prev, low_prev, point)
    hl_prev2 = df_out['HL'].shift(1) # HL from bar before previous

    # Calculate Pressure
    df_out['Pressure'] = calculate_pressure(volume_prev, hl_prev2)
    pressure_prev = df_out['Pressure'].shift(1)

    # Calculate PV
    df_out['PV'] = calculate_pv(df_out['Pressure'], pressure_prev)

    # Calculate LWMA
    df_out['LWMA'] = calculate_lwma(df_out['Open'], strength_back)

    # Calculate CORE1
    df_out['CORE1'] = calculate_core1(df_out['Open'], open_prev, core_back)


    # --- Apply Trading Rule ---
    # Initialize output columns before applying rule
    df_out['PPrice1'] = df_out['Open']
    df_out['PColor1'] = EMPTY_VALUE
    df_out['PPrice2'] = df_out['Open']
    df_out['PColor2'] = EMPTY_VALUE
    df_out['Direction'] = EMPTY_VALUE
    df_out['Diff'] = EMPTY_VALUE

    # Apply the selected rule using the dispatcher function
    df_out = apply_trading_rule(df_out, tr_num, point, limit, pv_tp_multy)


    # --- Post-processing ---
    # Forward fill NaNs created during core calculations IF NEEDED.
    # Often better to handle NaNs within specific rules or downstream logic.
    # Let's comment this out for now, as rules handle NaNs partially.
    # cols_to_ffill = ['HL', 'Pressure', 'PV', 'LWMA', 'CORE1']
    # for col in cols_to_ffill:
    #     if col in df_out.columns:
    #         df_out[col] = df_out[col].ffill()

    # Forward fill rule outputs where EMPTY_VALUE was placeholder,
    # replace final EMPTY_VALUE with NaN for clarity/plotting.
    rule_output_cols = ['PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff']
    for col in rule_output_cols:
        if col in df_out.columns:
            # Ffill might propagate signals incorrectly, use with caution
            # df_out[col] = df_out[col].ffill()
            df_out[col] = df_out[col].replace(EMPTY_VALUE, np.nan)


    # Apply Reverse Signal if requested
    if reverse_signal:
        for col in ['PColor1', 'PColor2', 'Direction']:
            if col in df_out.columns:
                df_out[col] = df_out[col].apply(lambda x: reverse_signal_value(x) if pd.notna(x) else x)


    # --- Select and return final columns ---
    # Define expected output columns
    output_columns = [
        'Open', 'High', 'Low', 'Close', 'Volume', # Original Data (Volume renamed)
        'HL', 'Pressure', 'PV', 'LWMA', 'CORE1', # Intermediate Calculations
        'PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff' # Final Outputs
    ]
    # Filter to only columns that actually exist in the DataFrame
    final_columns = [col for col in output_columns if col in df_out.columns]

    return df_out[final_columns]