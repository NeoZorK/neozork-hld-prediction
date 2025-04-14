# -*- coding: utf-8 -*-
# src/indicator_logic.py

'''
Project: Shcherbyna Pressure Vector Indicator
Author: Shcherbyna Rostyslav
Date: 2025-04-14
Description: This module implements the Shcherbyna Pressure Vector indicator, based on the MQL5 code.
'''

import __init__
import pandas as pd
import numpy as np
from enum import Enum # For Trading Rule Switch

# --- Define constants for signals (similar to MQL5 Enum) ---
# You can adjust these values if needed, e.g., 0, 1, -1
NOTRADE = 0.0
BUY = 1.0
SELL = 2.0
DBL_BUY = 3.0       # Not used in core calculations shown, but defined for completeness
DBL_SELL = 4.0      # Not used in core calculations shown, but defined for completeness
BUY_AND_SELL = 5.0 # Not used in core calculations shown, but defined for completeness
EMPTY_VALUE = np.nan

# --- Define Enum for Trading Rule Switch ---
class TradingRule(Enum):
    PV_HighLow = 0
    Support_Resistants = 1
    Tick_Volume_Limit = 2
    Pressure_Vector = 3
    Pressure_Vector_TakeProfit = 4
    Pressure_Vector_TakeProfit2 = 5
    Pressure_Vector_TakeProfit3 = 6
    PV_Plus_Pressure = 7
    LWMA = 8
    CORE1 = 9

# --- Helper function for reversing signals ---
def reverse_signal_value(signal):
    """Reverses BUY to SELL and vice versa."""
    if signal == BUY:
        return SELL
    elif signal == SELL:
        return BUY
    # Add DBL_BUY/DBL_SELL logic if needed later
    # elif signal == DBL_BUY:
    #     return DBL_SELL
    # elif signal == DBL_SELL:
    #     return DBL_BUY
    else:
        return signal # Keep NOTRADE as is

# --- Main Calculation Function ---
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
    Calculates the Shcherbyna Pressure Vector indicator based on MQL5 logic.

    Args:
        df (pd.DataFrame): Input DataFrame with columns 'Open', 'High', 'Low', 'Close', 'TickVolume'.
                           Index should be DateTime. Data should be sorted ascending.
        point (float): The point size of the instrument (e.g., 0.00001 or 0.001). Cannot be zero.
        core_back (int): Period for CORE1 calculation smoothing. Default is 2.
        limit (int): Threshold for Tick_Volume_Limit rule. Default is 1000.
        strength_back (int): Period for LWMA (SMMA) calculation. Default is 1. Must be >= 1.
        tr_num (TradingRule): Enum selecting the calculation mode/output rule.
        pv_tp_multy (int): Multiplication factor for PV TakeProfit rules. Default is 10.
        reverse_signal (bool): Whether to reverse the final signals. Default is False.

    Returns:
        pd.DataFrame: DataFrame with calculated indicator values and signals.
                      Original columns might be included or excluded depending on implementation details.
                      New columns include: HL, Pressure, PV, Direction, PPrice1, PColor1,
                      PPrice2, PColor2, Diff, LWMA, CORE1.
    """
    if point == 0:
        raise ValueError("Point size cannot be zero.")
    if strength_back < 1:
        raise ValueError("strength_back must be >= 1.")
    if core_back <= 1:
         # The original MQL code for CORE smoothing implies core_back > 1 for the formula used
         # Using ewm requires alpha between 0 and 1, span > 1
         # Let's adjust or raise error, adjusted approach seems more robust
         print(f"Warning: core_back <= 1 ({core_back}) is unusual for CORE smoothing, using span=2 instead.")
         core_span = 2
    else:
         # Convert period n to span for ewm: span = n (adjust=False approximates MQL recursive filter)
         # The MQL formula (_PosDiff[i+1]*(n+1) + new_val)/n is unusual
         # Let's map it approximately to standard EMA/SMMA span for ewm
         # Standard Wilder smoothing (RSI) uses span = 2*n - 1.
         # The MQL code divides by n. Let's use span = core_back for simplicity,
         # acknowledging it might not be a perfect match to the strange MQL smoothing.
         # A span of n in ewm(span=n, adjust=False) corresponds roughly to alpha = 2/(n+1)
         # The MQL formula divides by n, closer to alpha = 1/n (SMMA)
         # So, let's use span = core_back * 2 -1 for SMMA like smoothing alpha=1/n
         # Update: MQL code: prev*(n+1)/n + new/n -- this is WRONG for EMA/SMMA.
         # It should be prev*(n-1)/n + new/n for SMMA or prev*(1-alpha) + new*alpha for EMA.
         # Let's replicate the *written* calculation iteratively for CORE as ewm mapping is ambiguous.
         # We'll use ewm for LWMA/SMMA as that formula is standard SMMA.
         pass # Iterative calculation will handle core_back

    # Make a copy to avoid modifying the original DataFrame
    df_out = df.copy()

    # --- Pre-calculate shifted values for convenience ---
    # Note: MQL5's i+1 means previous bar, i+2 means bar before previous
    high_prev = df_out['High'].shift(1)
    low_prev = df_out['Low'].shift(1)
    open_curr = df_out['Open'] # MQL5 uses open[i]
    open_prev = df_out['Open'].shift(1)
    tick_volume_prev = df_out['TickVolume'].shift(1)

    # --- Calculate High-Low range (HL) ---
    # _HL[i] = (high[i + 1] - low[i + 1]) / _Point;
    # Corresponds to range of the previous bar
    df_out['HL'] = (high_prev - low_prev) / point
    # Handle cases where HL is zero to prevent division by zero later
    df_out['HL'] = df_out['HL'].replace(0, np.nan) # Mark zero HL as NaN temporarily

    # Need HL of the bar before the previous one (i+2) for Pressure calculation
    # MQL5: _HL[i+1] was calculated based on high[i+2] and low[i+2]
    hl_prev2 = df_out['HL'].shift(1) # HL calculated at i+1, based on i+2 data

    # --- Calculate Pressure ---
    # _Pressure[i] = tick_volume[i + 1] / _HL[i + 1]; (if _HL[i+1] != 0)
    # Uses tick volume of previous bar and HL of bar before previous
    df_out['Pressure'] = np.where(
        (hl_prev2.notna()) & (hl_prev2 != 0),
        tick_volume_prev / hl_prev2,
        np.nan # Use NaN if hl_prev2 is NaN or zero
    )

    # --- Calculate Pressure Vector (PV) ---
    # _PV[i] = _Pressure[i] - _Pressure[i + 1];
    pressure_prev = df_out['Pressure'].shift(1)
    df_out['PV'] = df_out['Pressure'] - pressure_prev

    # --- Calculate LWMA (using SMMA/EMA logic from MQL5 code) ---
    # _LWMA[i] = (_LWMA[i + 1] * (inp_StrengthBack - 1) + open[i]) / inp_StrengthBack;
    # This is equivalent to an SMMA with period = strength_back
    # For pandas ewm, alpha = 1 / period for SMMA
    if strength_back >= 1:
         # Use adjust=False to mimic MQL5's recursive nature starting from the first available value
        df_out['LWMA'] = df_out['Open'].ewm(alpha=1/strength_back, adjust=False).mean()
    else:
        df_out['LWMA'] = np.nan # Or handle as error

    # --- Calculate CORE1 (RSI-like, using the specific MQL5 smoothing) ---
    # This requires an iterative approach or careful vectorization due to the custom smoothing
    # and the dependency on the previous smoothed values.
    # We will initialize and then loop, which might be slow on very large data.
    # Consider Numba or Cython if performance becomes an issue here.

    df_out['PriceDiff'] = df_out['Open'] - open_prev
    df_out['PosDiff'] = np.nan
    df_out['NegDiff'] = np.nan # MQL code seems to use same smoothing for both? Very unusual. Let's replicate.

    # MQL formula: _PosDiff[i] = (_PosDiff[i+1]*(n+1) + new_val)/n  where new_val = PriceDiff > 0 ? PriceDiff : 0
    # This increases the previous average and adds the new value, divided by n. This is not standard EMA/SMMA.
    # Let's replicate iteratively, although the formula itself seems questionable for its purpose.
    # Initialize first valid value
    first_valid_index = df_out['PriceDiff'].first_valid_index()
    if first_valid_index is not None:
        pos_val_init = df_out.loc[first_valid_index, 'PriceDiff'] if df_out.loc[first_valid_index, 'PriceDiff'] > 0 else 0.0
        neg_val_init = df_out.loc[first_valid_index, 'PriceDiff'] if df_out.loc[first_valid_index, 'PriceDiff'] > 0 else 0.0 # MQL used same logic here

        df_out.loc[first_valid_index, 'PosDiff'] = pos_val_init
        df_out.loc[first_valid_index, 'NegDiff'] = neg_val_init

        # Iterative calculation (Note: slow for large data!)
        pos_diff_prev = pos_val_init
        neg_diff_prev = neg_val_init
        n = core_back # Using n directly from MQL formula

        for idx in df_out.index[df_out.index > first_valid_index]:
            price_diff_curr = df_out.loc[idx, 'PriceDiff']
            new_pos = price_diff_curr if price_diff_curr > 0.0 else 0.0
            # This line replicates the strange MQL logic for NegDiff smoothing
            new_neg = price_diff_curr if price_diff_curr > 0.0 else 0.0
            # MQL smoothing: Prev * (n+1)/n + New/n - this formula amplifies previous average - likely incorrect intent.
            # Let's assume the intent was SMMA like: Prev * (n-1)/n + New/n for alpha=1/n
            # Using the exact MQL formula: (Prev * (n+1) + New) / n
            # Update: Realized the MQL code is likely wrong. (n+1) factor looks like a typo.
            # Should probably be (n-1) for SMMA or different logic for EMA.
            # Given the uncertainty, let's use standard Wilder's smoothing (EMA with alpha=1/n)
            # which is commonly used for RSI. Span = 2*n-1
            # Reverting to try and replicate *written* MQL logic, despite potential flaws.
            # This requires access to the previous calculated value, hence the loop.
            # Let's stick to the problematic MQL formula replication for now.

            if n > 0: # Avoid division by zero if core_back is accidentally <= 0
                 # Use .loc for safe setting
                 df_out.loc[idx, 'PosDiff'] = (pos_diff_prev * (n + 1) + new_pos) / n if n > 0 else new_pos
                 df_out.loc[idx, 'NegDiff'] = (neg_diff_prev * (n + 1) + new_neg) / n if n > 0 else new_neg
            else:
                 df_out.loc[idx, 'PosDiff'] = new_pos
                 df_out.loc[idx, 'NegDiff'] = new_neg

            # Update previous values safely handling potential NaNs from calculation
            pos_diff_prev = df_out.loc[idx, 'PosDiff'] if pd.notna(df_out.loc[idx, 'PosDiff']) else pos_diff_prev
            neg_diff_prev = df_out.loc[idx, 'NegDiff'] if pd.notna(df_out.loc[idx, 'NegDiff']) else neg_diff_prev


    # Calculate CORE1 based on smoothed differences
    # MQL had the standard RSI formula commented out: 100.0 - 100.0 / (1 + _PosDiff[i] / _NegDiff[i])
    # And specific logic for zero NegDiff. Let's use the standard RSI formula based on the derived PosDiff/NegDiff.
    rs = df_out['PosDiff'] / df_out['NegDiff'].replace(0, 1e-9) # Avoid division by zero
    df_out['CORE1'] = 100.0 - (100.0 / (1.0 + rs))
    # Handle cases where NegDiff was truly zero
    df_out['CORE1'] = np.where(df_out['NegDiff'] == 0,
                               np.where(df_out['PosDiff'] != 0, 100.0, 50.0),
                               df_out['CORE1'])
    df_out['CORE1'] = df_out['CORE1'].fillna(50.0) # Default to 50 if calculation failed

    # --- Initialize output columns ---
    df_out['PPrice1'] = open_curr # Default value
    df_out['PColor1'] = NOTRADE # Default value
    df_out['PPrice2'] = open_curr # Default value
    df_out['PColor2'] = NOTRADE # Default value
    df_out['Direction'] = NOTRADE # Default value
    df_out['Diff'] = EMPTY_VALUE # Default value

    # --- Apply Trading Rule Logic ---
    # Use vectorization where possible

    # Rule: PV_HighLow
    if tr_num == TradingRule.PV_HighLow:
        pv_e = 0.5 * np.log(np.pi) # Constant value: ((0.5 * MathLog(3.14159265)));
        # MQL: plus = open[i] + ((_HL[i] * pv_e * _Point) - (MathPow(pv_e, 3) * (_PV[i] * _Point)));
        # MQL: minus = open[i] - ((_HL[i] * pv_e * _Point) + (MathPow(pv_e, 3) * (_PV[i] * _Point)));
        # Note: MQL uses _HL[i] (prev bar range) and _PV[i]
        plus = open_curr + ((df_out['HL'] * pv_e * point) - (np.power(pv_e, 3) * (df_out['PV'] * point)))
        minus = open_curr - ((df_out['HL'] * pv_e * point) + (np.power(pv_e, 3) * (df_out['PV'] * point)))
        df_out['PPrice1'] = minus
        df_out['PColor1'] = BUY
        df_out['PPrice2'] = plus
        df_out['PColor2'] = SELL
        df_out['Direction'] = NOTRADE

    # Rule: Support_Resistants
    elif tr_num == TradingRule.Support_Resistants:
        # MQL: plus = open[i] + (_HL[i] / 2 * _Point);
        # MQL: minus = open[i] - (_HL[i] / 2 * _Point);
        plus = open_curr + (df_out['HL'] / 2.0 * point)
        minus = open_curr - (df_out['HL'] / 2.0 * point)
        df_out['PPrice1'] = minus
        df_out['PColor1'] = BUY
        df_out['PPrice2'] = plus
        df_out['PColor2'] = SELL
        df_out['Direction'] = NOTRADE

    # Rule: Tick_Volume_Limit
    elif tr_num == TradingRule.Tick_Volume_Limit:
        plus = open_curr + (df_out['HL'] / 2.0 * point)
        minus = open_curr - (df_out['HL'] / 2.0 * point)
        # Condition: _HL[i] >= inp_Limit
        sell_condition = df_out['HL'] >= limit
        # Condition: _HL[i] < inp_Limit
        buy_condition = df_out['HL'] < limit

        df_out['PPrice1'] = np.where(sell_condition, plus, np.where(buy_condition, minus, open_curr))
        df_out['PColor1'] = np.where(sell_condition, SELL, np.where(buy_condition, BUY, NOTRADE))
        df_out['PPrice2'] = np.where(sell_condition, minus, np.where(buy_condition, plus, open_curr))
        df_out['PColor2'] = np.where(sell_condition, BUY, np.where(buy_condition, SELL, NOTRADE))
        df_out['Direction'] = np.where(sell_condition, SELL, np.where(buy_condition, BUY, NOTRADE))
        # Diff calculation specific to this rule in MQL
        df_out['Diff'] = np.abs(open_curr - df_out['PPrice1']) - np.abs(open_curr - df_out['PPrice2'])
        df_out.loc[~(sell_condition | buy_condition), 'Diff'] = 0 # Set Diff to 0 if no condition met

    # Rule: Pressure_Vector (Direction only)
    elif tr_num == TradingRule.Pressure_Vector:
        df_out['PPrice1'] = open_curr
        df_out['PPrice2'] = open_curr
        df_out['PColor2'] = EMPTY_VALUE
        df_out['PColor1'] = np.where(df_out['PV'] > 0, BUY, np.where(df_out['PV'] < 0, SELL, NOTRADE))
        df_out['Direction'] = np.where(df_out['PV'] > 0, BUY, np.where(df_out['PV'] < 0, SELL, NOTRADE))

    # Rule: Pressure_Vector_TakeProfit (One Side TP)
    elif tr_num == TradingRule.Pressure_Vector_TakeProfit:
        tp_offset = np.abs(df_out['PV']) * pv_tp_multy * point
        df_out['PPrice1'] = np.where(df_out['PV'] > 0, open_curr + tp_offset,
                                     np.where(df_out['PV'] < 0, open_curr - tp_offset, open_curr))
        df_out['PColor1'] = np.where(df_out['PV'] > 0, BUY, np.where(df_out['PV'] < 0, SELL, NOTRADE))
        df_out['Direction'] = df_out['PColor1']
        df_out['PPrice2'] = open_curr
        df_out['PColor2'] = EMPTY_VALUE

    # Rule: Pressure_Vector_TakeProfit2 (Two Sides TP)
    elif tr_num == TradingRule.Pressure_Vector_TakeProfit2:
        tp_offset = np.abs(df_out['PV']) * pv_tp_multy * point
        # MQL logic seems to set PPrice1/Color1 based on PV sign, then PPrice2/Color2 for opposite side
        df_out['PPrice1'] = np.where(df_out['PV'] > 0, open_curr + tp_offset, # Buy TP target if PV > 0
                                     np.where(df_out['PV'] < 0, open_curr - tp_offset, open_curr)) # Sell TP target if PV < 0
        df_out['PColor1'] = np.where(df_out['PV'] > 0, BUY, np.where(df_out['PV'] < 0, SELL, NOTRADE))

        # Note: MQL code has typos/overwrites here. Let's interpret intention:
        # If PV > 0 (Buy signal), set Price2/Color2 for Sell TP
        # If PV < 0 (Sell signal), set Price2/Color2 for Buy TP
        df_out['PPrice2'] = np.where(df_out['PV'] > 0, open_curr - tp_offset, # Sell TP target if PV > 0
                                     np.where(df_out['PV'] < 0, open_curr + tp_offset, open_curr)) # Buy TP target if PV < 0
        df_out['PColor2'] = np.where(df_out['PV'] > 0, SELL, np.where(df_out['PV'] < 0, BUY, NOTRADE))

        df_out['Direction'] = df_out['PColor1'] # Direction follows the primary signal

    # Rule: Pressure_Vector_TakeProfit3 (One Side, Right Direction - Reversed?)
    elif tr_num == TradingRule.Pressure_Vector_TakeProfit3:
        # MQL logic seems reversed compared to TakeProfit1
        tp_offset = np.abs(df_out['PV']) * pv_tp_multy * point
        df_out['PPrice1'] = np.where(df_out['PV'] > 0, open_curr + tp_offset, # Buy TP Price if PV > 0
                                     np.where(df_out['PV'] < 0, open_curr - tp_offset, open_curr)) # Sell TP Price if PV < 0
        df_out['PColor1'] = np.where(df_out['PV'] > 0, SELL, np.where(df_out['PV'] < 0, BUY, NOTRADE)) # Reversed Color!
        df_out['Direction'] = df_out['PColor1'] # Direction follows reversed color
        df_out['PPrice2'] = open_curr
        df_out['PColor2'] = EMPTY_VALUE

    # Rule: PV_Plus_Pressure
    elif tr_num == TradingRule.PV_Plus_Pressure:
        # MQL: ((fabs(_PV[i]) + (_Pressure[i]) / 2) * _Point)
        # Note: MQL uses _Pressure[i] directly
        offset = (np.abs(df_out['PV']) + df_out['Pressure'] / 2.0) * point
        df_out['PPrice1'] = np.where(df_out['PV'] > 0, open_curr + offset, # Buy TP target if PV > 0
                                     np.where(df_out['PV'] < 0, open_curr - offset, open_curr)) # Sell TP target if PV < 0
        df_out['PColor1'] = np.where(df_out['PV'] > 0, BUY, np.where(df_out['PV'] < 0, SELL, NOTRADE))

        df_out['PPrice2'] = np.where(df_out['PV'] > 0, open_curr - offset, # Sell TP target if PV > 0
                                     np.where(df_out['PV'] < 0, open_curr + offset, open_curr)) # Buy TP target if PV < 0
        df_out['PColor2'] = np.where(df_out['PV'] > 0, SELL, np.where(df_out['PV'] < 0, BUY, NOTRADE))

        df_out['Direction'] = df_out['PColor1'] # Direction follows the primary signal

    # Rule: LWMA
    elif tr_num == TradingRule.LWMA:
        df_out['PPrice1'] = df_out['LWMA']
        df_out['PPrice2'] = open_curr
        df_out['PColor2'] = EMPTY_VALUE
        lwma_prev = df_out['LWMA'].shift(1)
        df_out['PColor1'] = np.where(df_out['LWMA'] > lwma_prev, BUY,
                                     np.where(df_out['LWMA'] < lwma_prev, SELL, NOTRADE))
        df_out['Direction'] = df_out['PColor1']

    # Rule: CORE1
    elif tr_num == TradingRule.CORE1:
        df_out['PPrice1'] = df_out['CORE1'] # Plotting the CORE value itself
        df_out['PPrice2'] = open_curr
        df_out['PColor2'] = EMPTY_VALUE
        core1_prev = df_out['CORE1'].shift(1)
        df_out['PColor1'] = np.where(df_out['CORE1'] > core1_prev, BUY,
                                     np.where(df_out['CORE1'] < core1_prev, SELL, NOTRADE))
        df_out['Direction'] = df_out['PColor1']

    else: # Default case if tr_num is invalid (or map to Support_Resistants as in MQL)
        plus = open_curr + (df_out['HL'] / 2.0 * point)
        minus = open_curr - (df_out['HL'] / 2.0 * point)
        df_out['PPrice1'] = minus
        df_out['PColor1'] = BUY
        df_out['PPrice2'] = plus
        df_out['PColor2'] = SELL
        df_out['Direction'] = NOTRADE


    # --- Handle potential NaNs from calculations (like DublicateValue) ---
    # Forward fill NaNs created during calculation steps like Pressure, PV, LWMA, CORE1 etc.
    # We apply this after all rules are calculated.
    # Select columns to fill, excluding maybe price/color outputs if default is intended
    cols_to_ffill = ['HL', 'Pressure', 'PV', 'LWMA', 'CORE1', 'PosDiff', 'NegDiff']
    # Also fill the final rule outputs to propagate previous state if calculation failed
    cols_to_ffill.extend(['PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff'])

    for col in cols_to_ffill:
        if col in df_out.columns:
            df_out[col] = df_out[col].ffill()


    # --- Apply Reverse Signal if requested ---
    if reverse_signal:
        df_out['PColor1'] = df_out['PColor1'].apply(reverse_signal_value)
        df_out['PColor2'] = df_out['PColor2'].apply(reverse_signal_value)
        df_out['Direction'] = df_out['Direction'].apply(reverse_signal_value)


    # --- Select and return final columns ---
    # Choose which columns to return - depends on what's needed downstream
    output_columns = [
        'Open', 'High', 'Low', 'Close', 'TickVolume', # Original Data
        'HL', 'Pressure', 'PV', 'LWMA', 'CORE1', # Intermediate Calculations
        'PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff' # Final Outputs
    ]
    # Filter out columns that might not exist depending on the rule (e.g., Diff)
    final_columns = [col for col in output_columns if col in df_out.columns]

    return df_out[final_columns]

# --- Example Usage (requires a DataFrame 'ohlcv_df' with correct columns) ---
if __name__ == '__main__':

    # Version
    print("Pressure Vector Calculation Module", __init__.__version__)


    # This is example data - replace with your actual data loading
    data = {
        'Open': [1.1, 1.11, 1.12, 1.115, 1.125, 1.13, 1.128, 1.135, 1.14, 1.138],
        'High': [1.105, 1.115, 1.125, 1.12, 1.13, 1.135, 1.133, 1.14, 1.145, 1.142],
        'Low': [1.095, 1.105, 1.115, 1.11, 1.12, 1.125, 1.125, 1.13, 1.135, 1.136],
        'Close': [1.1, 1.11, 1.118, 1.118, 1.128, 1.128, 1.131, 1.138, 1.138, 1.14],
        'TickVolume': [1000, 1200, 1100, 1300, 1500, 1400, 1600, 1700, 1550, 1650]
    }
    # Use a DatetimeIndex
    index = pd.date_range(start='2024-01-01', periods=len(data['Open']), freq='D')
    ohlcv_df = pd.DataFrame(data, index=index)

    # Define instrument point size (EXAMPLE for EURUSD)
    instr_point = 0.00001

    # --- Calculate using default PV_HighLow rule ---
    print("--- Calculating Rule: PV_HighLow ---")
    result_df_pvhl = calculate_pressure_vector(
        df=ohlcv_df.copy(), # Pass a copy
        point=instr_point,
        tr_num=TradingRule.PV_HighLow,
        strength_back=1 # Example value
    )
    print(result_df_pvhl.tail())

    # --- Calculate using Tick_Volume_Limit rule ---
    print("\n--- Calculating Rule: Tick_Volume_Limit ---")
    result_df_tvl = calculate_pressure_vector(
        df=ohlcv_df.copy(),
        point=instr_point,
        limit=15, # Example limit based on HL points (HL calculated / point)
        tr_num=TradingRule.Tick_Volume_Limit
    )
    print(result_df_tvl.tail())

    # --- Calculate using Pressure_Vector rule ---
    print("\n--- Calculating Rule: Pressure_Vector ---")
    result_df_pv = calculate_pressure_vector(
        df=ohlcv_df.copy(),
        point=instr_point,
        tr_num=TradingRule.Pressure_Vector
    )
    print(result_df_pv.tail())

     # --- Calculate using LWMA rule ---
    print("\n--- Calculating Rule: LWMA ---")
    result_df_lwma = calculate_pressure_vector(
        df=ohlcv_df.copy(),
        point=instr_point,
        strength_back=3, # Example period
        tr_num=TradingRule.LWMA
    )
    print(result_df_lwma.tail())