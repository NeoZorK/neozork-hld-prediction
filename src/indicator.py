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


# --- Example Usage Block ---
if __name__ == '__main__':

    # Version
    print("Pressure Vector Calculation Module", __init__.__version__)

    # Example data
    data = {
        'Open': [1.1, 1.11, 1.12, 1.115, 1.125, 1.13, 1.128, 1.135, 1.14, 1.138,
                 1.142, 1.145, 1.140, 1.135, 1.130, 1.132, 1.138, 1.145, 1.148, 1.150],
        'High': [1.105, 1.115, 1.125, 1.12, 1.13, 1.135, 1.133, 1.14, 1.145, 1.142,
                 1.146, 1.148, 1.143, 1.139, 1.136, 1.137, 1.142, 1.150, 1.152, 1.155],
        'Low': [1.095, 1.105, 1.115, 1.11, 1.12, 1.125, 1.125, 1.13, 1.135, 1.136,
                1.140, 1.142, 1.138, 1.133, 1.128, 1.130, 1.135, 1.143, 1.146, 1.148],
        'Close': [1.1, 1.11, 1.118, 1.118, 1.128, 1.128, 1.131, 1.138, 1.138, 1.14,
                  1.145, 1.141, 1.136, 1.131, 1.131, 1.136, 1.144, 1.149, 1.151, 1.149],
        'TickVolume': [1000, 1200, 1100, 1300, 1500, 1400, 1600, 1700, 1550, 1650,
                       1750, 1800, 1600, 1900, 2000, 1850, 1950, 2100, 2050, 2200]
    }
    index = pd.date_range(start='2024-01-01', periods=len(data['Open']), freq='D')
    ohlcv_df = pd.DataFrame(data, index=index)

    instr_point = 0.00001

    # --- Test Rule 1: PV_HighLow ---
    print("--- Calculating Rule: PV_HighLow ---")
    rule_to_test = TradingRule.PV_HighLow
    result_df_1 = calculate_pressure_vector(
        df=ohlcv_df.copy(),
        point=instr_point,
        core_back=5, strength_back=3,
        tr_num=rule_to_test
    )
    print(result_df_1.tail())
    plot_indicator_results(result_df_1, rule=rule_to_test, title="PV HighLow Rule Results")

    # --- Test Rule 2: Pressure_Vector ---
    print("\n--- Calculating Rule: Pressure_Vector ---")
    rule_to_test = TradingRule.Pressure_Vector
    result_df_2 = calculate_pressure_vector(
        df=ohlcv_df.copy(),
        point=instr_point,
        core_back=5, strength_back=3,
        tr_num=rule_to_test
    )
    print(result_df_2.tail())
    plot_indicator_results(result_df_2, rule=rule_to_test, title="Pressure Vector Rule Results")

    # --- Test Rule 3: CORE1 ---
    print("\n--- Calculating Rule: CORE1 ---")
    rule_to_test = TradingRule.CORE1
    result_df_3 = calculate_pressure_vector(
        df=ohlcv_df.copy(),
        point=instr_point,
        core_back=14, strength_back=3,
        tr_num=rule_to_test
    )
    print(result_df_3.tail())
    plot_indicator_results(result_df_3, rule=rule_to_test, title="CORE1 Rule Results")