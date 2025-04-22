# src/calculation/indicator.py

"""
Core logic for calculating the Pressure Vector indicator and related metrics.
Integrates core calculations and applies selected trading rules.
All comments are in English.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple # Import Tuple
import traceback # Import traceback

# Use relative imports for constants, core calculations, rules, and logger
from ..common.constants import TradingRule, EMPTY_VALUE
from ..common import logger
from .core_calculations import calculate_hl, calculate_pressure, calculate_pv
from .rules import apply_trading_rule

# Main function to calculate the indicator and apply rules
def calculate_pressure_vector(
    df: pd.DataFrame,
    point_size: float,
    rule: TradingRule,
) -> Optional[pd.DataFrame]:
    """
    Calculates HL, Pressure, PV and applies the specified trading rule.

    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data.
                           Must have 'High', 'Low', 'Close', 'Volume'.
                           Index should be DatetimeIndex.
        point_size (float): The point size of the instrument.
        rule (TradingRule): The specific trading rule enum member to apply.

    Returns:
        Optional[pd.DataFrame]: DataFrame with original OHLCV data plus calculated
                                HL, Pressure, PV, and rule-specific columns
                                (PPrice1, PPrice2, Direction, etc.), or None on failure.
    """
    if df is None or df.empty:
        logger.print_error("Input DataFrame is empty or None.")
        return None

    required_cols = ['High', 'Low', 'Close', 'Volume']
    if not all(col in df.columns for col in required_cols):
        logger.print_error(f"Input DataFrame missing required columns: {required_cols}. Found: {list(df.columns)}")
        return None

    df_calc = df.copy()

    # --- Core Calculations ---
    try:
        logger.print_debug("Calculating HL...")
        df_calc = calculate_hl(df_calc, point_size)

        logger.print_debug("Calculating Pressure...")
        df_calc = calculate_pressure(df_calc)

        logger.print_debug("Calculating PV...")
        df_calc = calculate_pv(df_calc)

    except Exception as e:
        logger.print_error(f"Error during core calculations: {type(e).__name__}: {e}")
        # Use imported traceback
        logger.print_debug(f"Traceback (core calc):\n{traceback.format_exc()}")
        # Return df with potentially partial calculations? Or None? Returning None for safety.
        return None

    # --- Apply Trading Rule ---
    logger.print_debug(f"Applying selected trading rule: {rule.name}")
    rule_output_df = apply_trading_rule(df_calc, rule, point_size)

    if rule_output_df is None:
        logger.print_error(f"Failed to apply trading rule {rule.name}. Returning core calculations only.")
        # Return df_calc which contains OHLCV + HL, Pressure, PV
        # Ensure standard output columns exist even if rule failed
        for col in ['PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']:
             if col not in df_calc:
                  df_calc[col] = EMPTY_VALUE
        return df_calc
    else:
        # --- FIX: Merge rule output using concat instead of update ---
        # Ensure index alignment before merging/joining
        if not df_calc.index.equals(rule_output_df.index):
             logger.print_warning("Index mismatch between calculation df and rule output df. Attempting reindex.")
             try:
                 rule_output_df = rule_output_df.reindex(df_calc.index)
             except Exception as e_reindex:
                 logger.print_error(f"Failed to reindex rule output: {e_reindex}. Cannot merge rule results.")
                 # Fallback to returning core calculations
                 for col in ['PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']:
                      if col not in df_calc:
                           df_calc[col] = EMPTY_VALUE
                 return df_calc

        # Use concat along columns (axis=1) to add new columns from rule output
        try:
            # Ensure no duplicate columns before concat if rule_output contains OHLCV etc.
            # Assuming rule_output_df only contains NEW columns (PPrice1 etc.)
            cols_to_add = rule_output_df.columns.difference(df_calc.columns)
            df_final = pd.concat([df_calc, rule_output_df[cols_to_add]], axis=1)
            # If rule_output_df might contain overlapping columns, handle differently:
            # df_final = pd.concat([df_calc, rule_output_df], axis=1)
            # # Optional: Handle duplicate columns if necessary (e.g., keep first, last, or error)
            # df_final = df_final.loc[:, ~df_final.columns.duplicated(keep='first')]


            logger.print_debug("Successfully merged rule results using concat.")
            # Verify columns were added
            added_cols = rule_output_df.columns
            if not all(col in df_final.columns for col in added_cols):
                 logger.print_warning(f"Not all rule output columns ({added_cols}) seem to be present after concat.")

            return df_final

        except Exception as e_concat:
             logger.print_error(f"Error concatenating rule results: {e_concat}")
             logger.print_debug(f"Traceback (concat rule):\n{traceback.format_exc()}")
             # Fallback to returning core calculations
             for col in ['PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']:
                   if col not in df_calc:
                        df_calc[col] = EMPTY_VALUE
             return df_calc
        # --- End FIX ---
