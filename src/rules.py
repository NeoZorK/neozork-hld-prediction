# -*- coding: utf-8 -*-
# src/rules.py

"""
Functions implementing the specific logic for each TradingRule.
Each function updates the DataFrame with rule-specific outputs
(PPrice1, PColor1, PPrice2, PColor2, Direction, Diff).
"""

import pandas as pd
import numpy as np
from .constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE

# Helper to safely get series or default
def _get_series(df, col_name, default_val=0):
    if col_name in df.columns:
        return df[col_name].fillna(default_val)
    return pd.Series(default_val, index=df.index)

def apply_rule_pv_highlow(df: pd.DataFrame, point: float):
    """Applies PV_HighLow rule logic."""
    open_curr = _get_series(df, 'Open')
    hl_val = _get_series(df, 'HL')
    pv_val = _get_series(df, 'PV')
    pv_e = 0.5 * np.log(np.pi) # approx 0.57236

    pv_term = np.power(pv_e, 3) * pv_val * point
    hl_term = hl_val * pv_e * point

    df['PPrice1'] = open_curr - (hl_term + pv_term)
    df['PColor1'] = BUY
    df['PPrice2'] = open_curr + (hl_term - pv_term)
    df['PColor2'] = SELL
    df['Direction'] = NOTRADE
    df['Diff'] = EMPTY_VALUE
    return df

def apply_rule_support_resistants(df: pd.DataFrame, point: float):
    """Applies Support_Resistants rule logic."""
    open_curr = _get_series(df, 'Open')
    hl_val = _get_series(df, 'HL')
    hl_term = hl_val / 2.0 * point

    df['PPrice1'] = open_curr - hl_term
    df['PColor1'] = BUY
    df['PPrice2'] = open_curr + hl_term
    df['PColor2'] = SELL
    df['Direction'] = NOTRADE
    df['Diff'] = EMPTY_VALUE
    return df

def apply_rule_tick_volume_limit(df: pd.DataFrame, point: float, limit: int):
    """Applies Tick_Volume_Limit rule logic."""
    open_curr = _get_series(df, 'Open')
    hl_val = _get_series(df, 'HL')
    hl_term = hl_val / 2.0 * point
    plus = open_curr + hl_term
    minus = open_curr - hl_term

    sell_condition = hl_val >= limit
    buy_condition = hl_val < limit

    df['PPrice1'] = np.where(sell_condition, plus, np.where(buy_condition, minus, open_curr))
    df['PColor1'] = np.where(sell_condition, SELL, np.where(buy_condition, BUY, NOTRADE))
    df['PPrice2'] = np.where(sell_condition, minus, np.where(buy_condition, plus, open_curr))
    df['PColor2'] = np.where(sell_condition, BUY, np.where(buy_condition, SELL, NOTRADE))
    df['Direction'] = np.where(sell_condition, SELL, np.where(buy_condition, BUY, NOTRADE))

    diff_term1 = np.abs(open_curr - _get_series(df, 'PPrice1', default_val=open_curr))
    diff_term2 = np.abs(open_curr - _get_series(df, 'PPrice2', default_val=open_curr))
    df['Diff'] = np.where(sell_condition | buy_condition, diff_term1 - diff_term2, 0)
    return df

def apply_rule_pressure_vector(df: pd.DataFrame):
    """Applies Pressure_Vector rule logic."""
    open_curr = _get_series(df, 'Open')
    pv_val = _get_series(df, 'PV')

    df['PPrice1'] = open_curr
    df['PPrice2'] = open_curr
    df['PColor1'] = np.where(pv_val > 0, BUY, np.where(pv_val < 0, SELL, NOTRADE))
    df['PColor2'] = EMPTY_VALUE
    df['Direction'] = df['PColor1']
    df['Diff'] = EMPTY_VALUE
    return df

def apply_rule_pressure_vector_tp(df: pd.DataFrame, point: float, pv_tp_multy: int):
    """Applies Pressure_Vector_TakeProfit rule logic."""
    open_curr = _get_series(df, 'Open')
    pv_val = _get_series(df, 'PV')
    tp_offset = np.abs(pv_val) * pv_tp_multy * point

    df['PPrice1'] = np.where(pv_val > 0, open_curr + tp_offset,
                             np.where(pv_val < 0, open_curr - tp_offset, open_curr))
    df['PColor1'] = np.where(pv_val > 0, BUY, np.where(pv_val < 0, SELL, NOTRADE))
    df['Direction'] = df['PColor1']
    df['PPrice2'] = open_curr
    df['PColor2'] = EMPTY_VALUE
    df['Diff'] = EMPTY_VALUE
    return df

def apply_rule_pressure_vector_tp2(df: pd.DataFrame, point: float, pv_tp_multy: int):
    """Applies Pressure_Vector_TakeProfit2 rule logic."""
    open_curr = _get_series(df, 'Open')
    pv_val = _get_series(df, 'PV')
    tp_offset = np.abs(pv_val) * pv_tp_multy * point

    df['PColor1'] = np.where(pv_val > 0, BUY, np.where(pv_val < 0, SELL, NOTRADE))
    df['PPrice1'] = np.where(pv_val > 0, open_curr + tp_offset,
                             np.where(pv_val < 0, open_curr - tp_offset, open_curr))
    df['PColor2'] = np.where(pv_val > 0, SELL, np.where(pv_val < 0, BUY, NOTRADE))
    df['PPrice2'] = np.where(pv_val > 0, open_curr - tp_offset,
                             np.where(pv_val < 0, open_curr + tp_offset, open_curr))
    df['Direction'] = df['PColor1']
    df['Diff'] = EMPTY_VALUE
    return df

def apply_rule_pressure_vector_tp3(df: pd.DataFrame, point: float, pv_tp_multy: int):
    """Applies Pressure_Vector_TakeProfit3 rule logic."""
    open_curr = _get_series(df, 'Open')
    pv_val = _get_series(df, 'PV')
    tp_offset = np.abs(pv_val) * pv_tp_multy * point

    df['PPrice1'] = np.where(pv_val > 0, open_curr + tp_offset,
                             np.where(pv_val < 0, open_curr - tp_offset, open_curr))
    df['PColor1'] = np.where(pv_val > 0, SELL, np.where(pv_val < 0, BUY, NOTRADE)) # Reversed Color!
    df['Direction'] = df['PColor1']
    df['PPrice2'] = open_curr
    df['PColor2'] = EMPTY_VALUE
    df['Diff'] = EMPTY_VALUE
    return df

def apply_rule_pv_plus_pressure(df: pd.DataFrame, point: float):
    """Applies PV_Plus_Pressure rule logic."""
    open_curr = _get_series(df, 'Open')
    pv_val = _get_series(df, 'PV')
    pressure_val = _get_series(df, 'Pressure')
    offset = (np.abs(pv_val) + pressure_val / 2.0) * point

    df['PColor1'] = np.where(pv_val > 0, BUY, np.where(pv_val < 0, SELL, NOTRADE))
    df['PPrice1'] = np.where(pv_val > 0, open_curr + offset,
                             np.where(pv_val < 0, open_curr - offset, open_curr))
    df['PColor2'] = np.where(pv_val > 0, SELL, np.where(pv_val < 0, BUY, NOTRADE))
    df['PPrice2'] = np.where(pv_val > 0, open_curr - offset,
                             np.where(pv_val < 0, open_curr + offset, open_curr))
    df['Direction'] = df['PColor1']
    df['Diff'] = EMPTY_VALUE
    return df

def apply_rule_lwma(df: pd.DataFrame):
    """Applies LWMA rule logic."""
    open_curr = _get_series(df, 'Open')
    lwma_val = _get_series(df, 'LWMA', default_val=np.nan) # Keep NaN default for LWMA
    lwma_prev = lwma_val.shift(1).fillna(lwma_val) # Handle start NaN

    df['PPrice1'] = lwma_val # Plot LWMA line itself
    df['PPrice2'] = open_curr # No second price line
    df['PColor1'] = np.where(lwma_val > lwma_prev, BUY,
                             np.where(lwma_val < lwma_prev, SELL, NOTRADE))
    df['PColor2'] = EMPTY_VALUE
    df['Direction'] = df['PColor1']
    df['Diff'] = EMPTY_VALUE
    return df

def apply_rule_core1(df: pd.DataFrame):
    """Applies CORE1 rule logic."""
    open_curr = _get_series(df, 'Open')
    core1_val = _get_series(df, 'CORE1', default_val=50.0) # Default CORE1 is 50
    core1_prev = core1_val.shift(1).fillna(core1_val) # Handle start NaN

    df['PPrice1'] = core1_val # Plotting the CORE value itself (expected in separate panel)
    df['PPrice2'] = open_curr
    df['PColor1'] = np.where(core1_val > core1_prev, BUY,
                             np.where(core1_val < core1_prev, SELL, NOTRADE))
    df['PColor2'] = EMPTY_VALUE
    df['Direction'] = df['PColor1']
    df['Diff'] = EMPTY_VALUE
    return df

# --- Rule Dispatcher ---
# Maps TradingRule enum to the corresponding function
RULE_DISPATCHER = {
    TradingRule.PV_HighLow: apply_rule_pv_highlow,
    TradingRule.Support_Resistants: apply_rule_support_resistants,
    TradingRule.Tick_Volume_Limit: apply_rule_tick_volume_limit,
    TradingRule.Pressure_Vector: apply_rule_pressure_vector,
    TradingRule.Pressure_Vector_TakeProfit: apply_rule_pressure_vector_tp,
    TradingRule.Pressure_Vector_TakeProfit2: apply_rule_pressure_vector_tp2,
    TradingRule.Pressure_Vector_TakeProfit3: apply_rule_pressure_vector_tp3,
    TradingRule.PV_Plus_Pressure: apply_rule_pv_plus_pressure,
    TradingRule.LWMA: apply_rule_lwma,
    TradingRule.CORE1: apply_rule_core1,
}

def apply_trading_rule(df: pd.DataFrame, rule: TradingRule, point: float, limit: int, pv_tp_multy: int) -> pd.DataFrame:
    """
    Applies the selected trading rule logic to the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing Open prices and calculated core indicators (HL, PV, Pressure, LWMA, CORE1).
        rule (TradingRule): The rule to apply.
        point (float): Instrument point size.
        limit (int): Limit parameter for Tick_Volume_Limit rule.
        pv_tp_multy (int): Multiplier for PV TakeProfit rules.

    Returns:
        pd.DataFrame: DataFrame with added/updated rule-specific columns.
    """
    if rule not in RULE_DISPATCHER:
        print(f"Warning: TradingRule '{rule.name}' not recognized. Applying default (Support_Resistants).")
        rule_func = RULE_DISPATCHER[TradingRule.Support_Resistants]
        # Pass only relevant args for the default
        return rule_func(df, point=point)

    rule_func = RULE_DISPATCHER[rule]

    # Pass arguments based on the specific rule's needs
    # This could be improved with more sophisticated argument handling if rules diverge more
    if rule == TradingRule.Tick_Volume_Limit:
        return rule_func(df, point=point, limit=limit)
    elif rule in [TradingRule.Pressure_Vector_TakeProfit,
                  TradingRule.Pressure_Vector_TakeProfit2,
                  TradingRule.Pressure_Vector_TakeProfit3]:
        return rule_func(df, point=point, pv_tp_multy=pv_tp_multy)
    elif rule in [TradingRule.PV_HighLow,
                  TradingRule.Support_Resistants,
                  TradingRule.PV_Plus_Pressure]:
         return rule_func(df, point=point)
    else: # Pressure_Vector, LWMA, CORE1 don't need extra params here
        return rule_func(df)