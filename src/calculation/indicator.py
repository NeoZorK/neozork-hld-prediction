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
    price_type: str = 'close',
    **kwargs
) -> pd.DataFrame:
    """
    Calculates the Shcherbyna Pressure Vector indicator by orchestrating
    core calculations and applying the selected trading rule.

    Args:
        df (pd.DataFrame): Input DataFrame with 'Open', 'High', 'Low', 'Close', 'TickVolume'.
                           Index should be DateTime. Sorted ascending.
        point (float): Instrument point size. Cannot be zero.
        tr_num (TradingRule): Enum selecting the calculation mode/output rule.
        price_type (str): Price type for RSI calculations ('open' or 'close').
        **kwargs: Additional parameters for specific indicators

    Returns:
        pd.DataFrame: DataFrame with original data and calculated indicator values/signals.
                      Includes 'Volume' instead of 'TickVolume'.
    """
    # --- Input Validation ---
    if not isinstance(df.index, pd.DatetimeIndex):
        logger.print_warning("Warning: DataFrame index is not a DatetimeIndex. Plotting might be affected.")
    
    # Check for required columns - handle both Volume and TickVolume
    base_cols = ['Open', 'High', 'Low', 'Close']
    volume_cols = ['Volume', 'TickVolume']
    
    if not all(col in df.columns for col in base_cols):
        raise ValueError(f"Input DataFrame must contain columns: {base_cols}")
    
    # Check if at least one volume column exists
    if not any(col in df.columns for col in volume_cols):
        raise ValueError(f"Input DataFrame must contain either 'Volume' or 'TickVolume' column")
    
    if point == 0:
        raise ValueError("Point size cannot be zero.")

    # Make a copy to avoid modifying the original DataFrame
    df_out = df.copy()

    # Handle duplicate indices that can cause reindexing errors
    if df_out.index.duplicated().any():
        logger.print_warning(f"Warning: Found {df_out.index.duplicated().sum()} duplicate indices. Removing duplicates to prevent calculation errors.")
        # Keep the first occurrence of each duplicate index
        df_out = df_out[~df_out.index.duplicated(keep='first')]

    # Ensure Volume column exists for consistency
    if 'Volume' not in df_out.columns and 'TickVolume' in df_out.columns:
        df_out.rename(columns={'TickVolume': 'Volume'}, inplace=True)
    elif 'TickVolume' not in df_out.columns and 'Volume' in df_out.columns:
        # Volume already exists, no need to rename
        pass
    else:
        # Both exist, prefer Volume
        if 'TickVolume' in df_out.columns:
            df_out.drop(columns=['TickVolume'], inplace=True)


    # --- Core Calculations ---
    # Only calculate HL, Pressure, PV for non-RSI rules
    if tr_num not in [TradingRule.RSI, TradingRule.RSI_Momentum, TradingRule.RSI_Divergence]:
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

    # Apply the selected rule using the dispatcher function with additional parameters
    df_out = apply_trading_rule(df_out, tr_num, point, price_type, **kwargs)


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
    
    # Add RSI-specific columns for RSI rules
    if tr_num in [TradingRule.RSI, TradingRule.RSI_Momentum, TradingRule.RSI_Divergence]:
        rsi_columns = ['RSI', 'RSI_Signal', 'RSI_Price_Type']
        if tr_num == TradingRule.RSI_Momentum:
            rsi_columns.append('RSI_Momentum')
        output_columns.extend(rsi_columns)
    
    # Add CCI-specific columns for CCI rules
    if tr_num == TradingRule.CCI:
        cci_columns = ['CCI', 'CCI_Signal', 'CCI_Price_Type']
        output_columns.extend(cci_columns)
    
    # Add Stochastic-specific columns for Stochastic rules
    if tr_num == TradingRule.Stochastic:
        stoch_columns = ['Stoch_K', 'Stoch_D', 'Stoch_Signal', 'Stoch_Price_Type']
        output_columns.extend(stoch_columns)
    
    # Add EMA-specific columns for EMA rules
    if tr_num == TradingRule.EMA:
        ema_columns = ['EMA', 'EMA_Signal', 'EMA_Price_Type']
        output_columns.extend(ema_columns)
    
    # Add Bollinger Bands-specific columns for BB rules
    if tr_num == TradingRule.Bollinger_Bands:
        bb_columns = ['BB_Upper', 'BB_Middle', 'BB_Lower', 'BB_Signal', 'BB_Price_Type']
        output_columns.extend(bb_columns)
    
    # Add ATR-specific columns for ATR rules
    if tr_num == TradingRule.ATR:
        atr_columns = ['ATR', 'ATR_Signal', 'ATR_Price_Type']
        output_columns.extend(atr_columns)
    
    # Add VWAP-specific columns for VWAP rules
    if tr_num == TradingRule.VWAP:
        vwap_columns = ['VWAP', 'VWAP_Signal', 'VWAP_Price_Type']
        output_columns.extend(vwap_columns)
    
    # Add Pivot Points-specific columns for Pivot rules
    if tr_num == TradingRule.Pivot_Points:
        pivot_columns = ['Pivot_PP', 'Pivot_R1', 'Pivot_S1', 'Pivot_Signal', 'Pivot_Price_Type']
        output_columns.extend(pivot_columns)
    
    # Add PutCallRatio-specific columns for PutCallRatio rules
    if tr_num == TradingRule.PutCallRatio:
        putcall_columns = ['PutCallRatio', 'PutCallRatio_Signal', 'PutCallRatio_Price_Type']
        output_columns.extend(putcall_columns)
    
    # Add COT-specific columns for COT rules
    if tr_num == TradingRule.COT:
        cot_columns = ['COT', 'COT_Signal', 'COT_Price_Type']
        output_columns.extend(cot_columns)
    
    # Add MACD-specific columns for MACD rules
    if tr_num == TradingRule.MACD:
        macd_columns = ['MACD_Line', 'MACD_Signal', 'MACD_Histogram', 'MACD_Price_Type']
        output_columns.extend(macd_columns)
    
    # Add HMA-specific columns for HMA rules
    if tr_num == TradingRule.HMA:
        hma_columns = ['HMA', 'HMA_Signal', 'HMA_Price_Type']
        output_columns.extend(hma_columns)
    
    # Add TSF-specific columns for TSF rules
    if tr_num == TradingRule.TSForecast:
        tsf_columns = ['TSForecast', 'TSForecast_Signal', 'TSForecast_Price_Type']
        output_columns.extend(tsf_columns)
    
    # Filter to only columns that actually exist in the DataFrame
    final_columns = [col for col in output_columns if col in df_out.columns]

    return df_out[final_columns]