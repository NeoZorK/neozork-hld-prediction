# -*- coding: utf-8 -*-
# src/indicator.py

"""
Main module for calculating the Shcherbyna Pressure Vector indicator.
Orchestrates calls to core calculations and rule-specific logic.
"""

import pandas as pd
import numpy as np

# Use relative imports within the src package
from ..common import logger
from ..common.constants import TradingRule, EMPTY_VALUE
from .core_calculations import (
    calculate_hl, calculate_pressure, calculate_pv
)
from .rules import apply_trading_rule

# --- Main Calculation Orchestrator ---
def calculate_pressure_vector(
    df: pd.DataFrame,
    point: float, # Instrument's point size (e.g., 0.00001 for EURUSD)
    tr_num: TradingRule = TradingRule.PV_HighLow,
) -> pd.DataFrame:
    """
    Calculates the Shcherbyna Pressure Vector indicator by orchestrating
    core calculations and applying the selected trading rule.

    Args:
        df (pd.DataFrame): Input DataFrame with 'Open', 'High', 'Low', 'Close', 'TickVolume'.
                           Index should be DateTime. Sorted ascending.
        point (float): Instrument point size. Cannot be zero.
        tr_num (TradingRule): Enum selecting the calculation mode/output rule.

    Returns:
        pd.DataFrame: DataFrame with original data and calculated indicator values/signals.
                      Includes 'Volume' instead of 'TickVolume'.
    """
    # --- Input Validation ---
    if not isinstance(df.index, pd.DatetimeIndex):
        logger.print_warning("Warning: DataFrame index is not a DatetimeIndex. Plotting might be affected.")
    required_cols = ['Open', 'High', 'Low', 'Close', 'TickVolume']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Input DataFrame must contain columns: {required_cols}")
    if point == 0:
        raise ValueError("Point size cannot be zero.")

    # Make a copy to avoid modifying the original DataFrame
    df_out = df.copy()

    # Handle duplicate indices that can cause reindexing errors
    if df_out.index.duplicated().any():
        logger.print_warning(f"Warning: Found {df_out.index.duplicated().sum()} duplicate indices. Removing duplicates to prevent calculation errors.")
        # Keep the first occurrence of each duplicate index
        df_out = df_out[~df_out.index.duplicated(keep='first')]

    # Rename TickVolume for consistency and plotting
    df_out.rename(columns={'TickVolume': 'Volume'}, inplace=True, errors='ignore')


    # --- Core Calculations ---
    # Shifted values needed for calculations
    high_prev = df_out['High'].shift(1)
    low_prev = df_out['Low'].shift(1)
    volume_prev = df_out['Volume'].shift(1) # Use renamed 'Volume'

    # Calculate HL
    df_out['HL'] = calculate_hl(high_prev, low_prev, point)
    hl_prev2 = df_out['HL'].shift(1) # HL from bar before previous

    # Calculate Pressure
    df_out['Pressure'] = calculate_pressure(volume_prev, hl_prev2)
    pressure_prev = df_out['Pressure'].shift(1)

    # Calculate PV
    df_out['PV'] = calculate_pv(df_out['Pressure'], pressure_prev)


    # --- Apply Trading Rule ---
    # Initialize output columns before applying rule
    df_out['PPrice1'] = df_out['Open']
    df_out['PColor1'] = EMPTY_VALUE
    df_out['PPrice2'] = df_out['Open']
    df_out['PColor2'] = EMPTY_VALUE
    df_out['Direction'] = EMPTY_VALUE
    df_out['Diff'] = EMPTY_VALUE

    # Apply the selected rule using the dispatcher function
    df_out = apply_trading_rule(df_out, tr_num, point)


    # --- Post-processing ---
    # Forward fill NaNs created during core calculations IF NEEDED.
    # Often better to handle NaNs within specific rules or downstream logic.
    # Let's comment this out for now, as rules handle NaNs partially.
    # cols_to_ffill = ['HL', 'Pressure', 'PV']
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


    # --- Select and return final columns ---
    # Define expected output columns
    output_columns = [
        'Open', 'High', 'Low', 'Close', 'Volume',                       # Original Data (Volume renamed)
        'HL', 'Pressure', 'PV',                                         # Intermediate Calculations
        'PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff' # Final Outputs
    ]
    # Filter to only columns that actually exist in the DataFrame
    final_columns = [col for col in output_columns if col in df_out.columns]

    return df_out[final_columns]