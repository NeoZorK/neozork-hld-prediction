# -*- coding: utf-8 -*-
# src/rules.py

"""
Functions implementing the specific logic for each TradingRule.
Each function updates the DataFrame with rule-specific outputs
(PPrice1, PColor1, PPrice2, PColor2, Direction, Diff).
"""
from typing import Any

import pandas as pd
import numpy as np
from ..common import logger
from ..common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE


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

def apply_trading_rule(df: pd.DataFrame, rule: TradingRule | Any, point: float) -> pd.DataFrame: # Allow Any type hint for rule
    """
    Applies the selected trading rule logic to the DataFrame.
    Simplified signature again.
    """
    selected_rule = None # Keep track of the potentially valid rule
    is_valid_rule = False

    # Check if the rule is a valid TradingRule member
    if isinstance(rule, TradingRule):
         selected_rule = rule
         if rule in RULE_DISPATCHER:
             is_valid_rule = True
             rule_func = RULE_DISPATCHER[rule]
         else:
             # It's a TradingRule instance but not in dispatcher (e.g., future rule)
             pass # is_valid_rule remains False

    # If not a valid rule instance or not in dispatcher, try default and log warning
    if not is_valid_rule:
         # Log warning - use repr(rule) for safety as it might not have .name
         logger.print_warning(
             f"TradingRule {repr(rule)} not recognized or supported. "
             f"Applying default ({TradingRule.Predict_High_Low_Direction.name})."
         )
         selected_rule = TradingRule.Predict_High_Low_Direction # Use default rule enum
         rule_func = RULE_DISPATCHER[selected_rule]

    # --- Now apply the selected or default rule function ---
    if selected_rule in [TradingRule.PV_HighLow, TradingRule.Support_Resistants, TradingRule.Predict_High_Low_Direction]:
         return rule_func(df, point=point)
    elif selected_rule == TradingRule.Pressure_Vector:
         return rule_func(df)
    else:
         # Fallback for rules potentially added later that might need different args
         logger.print_warning(f"Rule '{selected_rule.name}' dispatcher logic needs update or rule is unsupported.")
         try:
              # Try calling without args first, maybe it's simple
              return rule_func(df)
         except TypeError:
              # If it fails, try with point (common case)
              try:
                  return rule_func(df, point=point)
              except Exception as e:
                  logger.print_error(f"Failed to execute rule function for {selected_rule.name}: {e}")
                  return df # Return original df on error