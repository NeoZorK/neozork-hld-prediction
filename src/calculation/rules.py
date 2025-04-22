# src/calculation/rules.py

"""
Implements different trading rule calculations based on core indicator values.
All comments are in English.
"""
import traceback

import pandas as pd
import numpy as np
from typing import Dict, Callable, Optional # Import Optional

# Use relative imports for constants and logger
from ..common.constants import TradingRule, BUY, SELL, NOTRADE, EMPTY_VALUE
from ..common import logger

# --- Rule Implementation Functions ---

# Placeholder/Example function for Predict_High_Low_Direction
def apply_rule_predict_hld(df: pd.DataFrame, point_size: float) -> pd.DataFrame:
    """
    Applies the 'Predict_High_Low_Direction' rule.
    Calculates PPrice1, PPrice2 based on Open +/- HL/2 * point_size.
    Generates a simple alternating Buy/Sell direction signal.

    Args:
        df (pd.DataFrame): DataFrame containing 'Open', 'HL'.
        point_size (float): The point size of the instrument.

    Returns:
        pd.DataFrame: DataFrame with added 'PPrice1', 'PPrice2', 'Direction',
                      'PColor1', 'PColor2' columns.
    """
    logger.print_debug("Applying rule: Predict_High_Low_Direction")
    df_res = df.copy()

    # Ensure HL is numeric and handle potential NaNs from calculation
    hl_numeric = pd.to_numeric(df_res['HL'], errors='coerce').fillna(0) # Fill NaN HL with 0 for calculation

    # Calculate PPrice1 and PPrice2
    # This formula might differ from the original MQL5 logic for these levels
    df_res['PPrice1'] = df_res['Open'] - (hl_numeric / 2 * point_size)
    df_res['PPrice2'] = df_res['Open'] + (hl_numeric / 2 * point_size)

    # --- Simple Direction Logic (Example) ---
    # This is a placeholder and likely needs to be replaced with actual logic
    # based on PV, Pressure, or other factors if available.
    # For now, let's create a simple alternating signal for demonstration.
    signal = np.resize([BUY, SELL], len(df_res)) # Simple alternating Buy/Sell
    # Set first signal based on some condition? Or start fixed?
    # Let's make it NOTRADE for the first row where calculations might be incomplete
    if len(signal) > 0:
        signal[0] = NOTRADE
    df_res['Direction'] = signal
    # --- End Simple Direction Logic ---

    # Add color columns (assuming fixed colors for this rule for now)
    df_res['PColor1'] = BUY # Example: Lime for PPrice1
    df_res['PColor2'] = SELL # Example: Red for PPrice2

    # Ensure specific columns exist, adding them with EMPTY_VALUE if not
    for col in ['PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']:
         if col not in df_res:
              df_res[col] = EMPTY_VALUE

    return df_res[['PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']]


# Placeholder/Example function for Pressure_Vector rule
def apply_rule_pressure_vector(df: pd.DataFrame, point_size: float) -> pd.DataFrame:
    """
    Applies the 'Pressure_Vector' rule (Placeholder).
    This rule might focus solely on PV signals or simple thresholds.

    Args:
        df (pd.DataFrame): DataFrame potentially containing 'PV'.
        point_size (float): The point size (may not be used directly here).

    Returns:
        pd.DataFrame: DataFrame with added 'Direction' column (and others if needed).
    """
    logger.print_debug("Applying rule: Pressure_Vector (Placeholder)")
    df_res = df.copy()

    # --- Example Logic: Signal based on PV sign ---
    if 'PV' in df_res.columns:
        pv_numeric = pd.to_numeric(df_res['PV'], errors='coerce').fillna(0)
        df_res['Direction'] = np.where(pv_numeric > 0, BUY, np.where(pv_numeric < 0, SELL, NOTRADE))
    else:
        logger.print_warning("PV column not found for Pressure_Vector rule. Setting Direction to NOTRADE.")
        df_res['Direction'] = NOTRADE
    # --- End Example Logic ---

    # Ensure specific columns exist, adding them with EMPTY_VALUE if not
    for col in ['PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']:
         if col not in df_res:
              df_res[col] = EMPTY_VALUE # Add placeholder columns if missing

    # Return only the columns relevant to this rule's output
    return df_res[['PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']]


# Placeholder/Example function for Support_Resistants rule
def apply_rule_support_resistants(df: pd.DataFrame, point_size: float) -> pd.DataFrame:
    """
    Applies the 'Support_Resistants' rule (Placeholder).
    This rule might calculate S/R levels based on Pressure, PV, or price action.

    Args:
        df (pd.DataFrame): DataFrame potentially containing 'Pressure', 'PV', OHLC.
        point_size (float): The point size.

    Returns:
        pd.DataFrame: DataFrame with added 'PPrice1' (Support?), 'PPrice2' (Resistance?),
                      'Direction' columns.
    """
    logger.print_debug("Applying rule: Support_Resistants (Placeholder)")
    df_res = df.copy()

    # --- Example Logic: Placeholder S/R ---
    # Replace with actual S/R calculation logic
    df_res['PPrice1'] = df_res['Low'].rolling(window=5).min() # Example: 5-period low as support
    df_res['PPrice2'] = df_res['High'].rolling(window=5).max() # Example: 5-period high as resistance
    df_res['Direction'] = NOTRADE # Example: No direction signal from S/R levels alone
    # --- End Example Logic ---

    # Ensure specific columns exist, adding them with EMPTY_VALUE if not
    for col in ['PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']:
         if col not in df_res:
              df_res[col] = EMPTY_VALUE

    return df_res[['PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']]


# --- Rule Dispatcher ---

# Dictionary mapping TradingRule enum members to their implementation functions
# *** CORRECTED: Removed reference to non-existent PV_HighLow ***
RULE_IMPLEMENTATIONS: Dict[TradingRule, Callable[[pd.DataFrame, float], pd.DataFrame]] = {
    TradingRule.Predict_High_Low_Direction: apply_rule_predict_hld,
    TradingRule.Pressure_Vector: apply_rule_pressure_vector,
    TradingRule.Support_Resistants: apply_rule_support_resistants,
    # Add mappings for other rules if defined in TradingRule Enum
}


# Main function to apply the selected trading rule
def apply_trading_rule(df: pd.DataFrame, rule: TradingRule, point_size: float) -> Optional[pd.DataFrame]:
    """
    Applies the specified trading rule function to the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing necessary columns (OHLC, PV, Pressure, etc.).
        rule (TradingRule): The enum member representing the rule to apply.
        point_size (float): The instrument's point size.

    Returns:
        Optional[pd.DataFrame]: DataFrame with added columns based on the rule
                                ('PPrice1', 'PPrice2', 'Direction', etc.), or None if rule not found.
    """
    rule_function = RULE_IMPLEMENTATIONS.get(rule)

    if rule_function:
        logger.print_debug(f"Found implementation for rule: {rule.name}")
        try:
            # Apply the selected rule function
            rule_output_df = rule_function(df, point_size)
            # Ensure the output is a DataFrame
            if not isinstance(rule_output_df, pd.DataFrame):
                 logger.print_error(f"Rule function {rule.name} did not return a DataFrame.")
                 return None
            # Ensure expected output columns exist, even if filled with NaN/EMPTY_VALUE
            expected_cols = ['PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']
            for col in expected_cols:
                 if col not in rule_output_df.columns:
                      logger.print_warning(f"Rule '{rule.name}' output missing column '{col}'. Adding with empty values.")
                      rule_output_df[col] = EMPTY_VALUE

            return rule_output_df[expected_cols] # Return only the standard output columns

        except Exception as e:
            logger.print_error(f"Error applying rule '{rule.name}': {type(e).__name__}: {e}")
            logger.print_debug(f"Traceback (apply rule):\n{traceback.format_exc()}")
            return None # Return None on error during rule application
    else:
        logger.print_error(f"No implementation found for trading rule: {rule.name}")
        return None # Return None if no function is mapped to the rule

