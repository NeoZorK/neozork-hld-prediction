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
from . import  logger

# Helper to safely get series or default
def _get_series(df, col_name, default_val=0):
    if col_name in df.columns:
        return df[col_name].fillna(default_val)
    return pd.Series(default_val, index=df.index)

# Predict High/Low Direction
def apply_rule_predict_hld(df: pd.DataFrame, point: float):
    """
    Combines Support/Resistants levels with Pressure Vector direction.
    Calculates PPrice1/2 based on Open +/- HL/2.
    Calculates Direction based on PV sign.
    """
    open_curr = _get_series(df, 'Open')
    hl_val = _get_series(df, 'HL') # HL in points
    pv_val = _get_series(df, 'PV') # Original PV

    # --- Calculate PPrice1/PPrice2 (from Support_Resistants) ---
    hl_term = hl_val / 2.0 * point # HL in price units
    df['PPrice1'] = open_curr - hl_term
    df['PPrice2'] = open_curr + hl_term
    # Assign colors like Support_Resistants
    df['PColor1'] = BUY
    df['PColor2'] = SELL

    # --- Calculate Direction (from Pressure_Vector) ---
    df['Direction'] = np.where(pv_val > 0, BUY, np.where(pv_val < 0, SELL, NOTRADE))

    # --- Set other outputs ---
    df['Diff'] = EMPTY_VALUE # Not calculated for this rule

    return df

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


# --- Rule Dispatcher ---
# Maps TradingRule enum to the corresponding function
RULE_DISPATCHER = {
    TradingRule.PV_HighLow: apply_rule_pv_highlow,
    TradingRule.Support_Resistants: apply_rule_support_resistants,
    TradingRule.Pressure_Vector: apply_rule_pressure_vector,
    TradingRule.Predict_High_Low_Direction: apply_rule_predict_hld,
}

def apply_trading_rule(df: pd.DataFrame, rule: TradingRule, point: float) -> pd.DataFrame:
    """
    Applies the selected trading rule logic to the DataFrame.
    Simplified signature again.
    """
    if rule not in RULE_DISPATCHER:
        logger.print_warning(f"TradingRule '{rule.name}' not recognized or removed. Applying default (Predict_High_Low_Direction).")
        # Use default rule if not recognized
        rule_func = RULE_DISPATCHER[TradingRule.Predict_High_Low_Direction]
        return rule_func(df, point=point)

    rule_func = RULE_DISPATCHER[rule]

    # Check if the rule requires point
    if rule in [TradingRule.PV_HighLow, TradingRule.Support_Resistants, TradingRule.Predict_High_Low_Direction]:
         return rule_func(df, point=point)
    elif rule == TradingRule.Pressure_Vector:
        return rule_func(df)
    else:
        # Fallback
        logger.print_warning(f"Rule '{rule.name}' dispatcher logic needs update or rule is unsupported.")
        try:
             return rule_func(df)
        except TypeError:
             logger.print_error(f"Rule function for {rule.name} likely requires arguments (e.g., point). Cannot execute.")
             return df
