# src/indicator_calculation.py

"""
Workflow Step 3: Calculates the indicator.
All comments are in English.
"""

import pandas as pd
# Use relative imports within the src package
from ..common import logger
from ..common.constants import TradingRule
# Import the main calculation function from indicator module
from .indicator import calculate_pressure_vector

def calculate_indicator(args, ohlcv_df: pd.DataFrame, point_size: float):
    """
    Performs indicator calculation based on selected rule.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        ohlcv_df (pd.DataFrame): DataFrame with OHLCV data.
        point_size (float): Determined point size.

    Returns:
        tuple: (result_df, selected_rule) or raises ValueError/KeyError on failure.
    """
    if ohlcv_df is None or ohlcv_df.empty:
        raise ValueError("No data available for calculation.")
    if point_size is None:
         raise ValueError("Point size is None. Cannot calculate indicator.")

    logger.print_info(f"\n--- Step 3: Calculating Indicator (Rule: {args.rule}) ---")

    # --- Rule Name Conversion ---
    rule_input_str = args.rule
    rule_aliases_map = {'PHLD': 'Predict_High_Low_Direction', 'PV': 'Pressure_Vector', 'SR': 'Support_Resistants'}
    rule_name_str = rule_aliases_map.get(rule_input_str.upper(), rule_input_str)
    try:
        selected_rule = TradingRule[rule_name_str]
        logger.print_debug(f"Mapped rule input '{args.rule}' to enum member '{selected_rule.name}'")
    except KeyError:
        available_rules = list(TradingRule.__members__.keys()) + list(rule_aliases_map.keys())
        raise ValueError(f"Invalid rule name or alias '{args.rule}'. Use one of {available_rules}")

    # --- Column Check & Rename ---
    required_cols_indicator = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in ohlcv_df.columns for col in required_cols_indicator):
        raise ValueError(f"DataFrame missing required columns: {required_cols_indicator}. Has: {ohlcv_df.columns.tolist()}")
    ohlcv_df_renamed = ohlcv_df.rename(columns={'Volume': 'TickVolume'}, errors='ignore')

    # --- Calculation Call ---
    try:
        result_df = calculate_pressure_vector(
            df=ohlcv_df_renamed.copy(),
            point=point_size,
            tr_num=TradingRule(selected_rule),
        )
    except Exception as e:
         logger.print_error(f"Exception during calculate_pressure_vector: {e}")
         import traceback
         print(traceback.format_exc())
         raise # Re-raise the exception to be caught by the main workflow

    if result_df is None or result_df.empty:
        logger.print_warning("Indicator calculation returned None or empty DataFrame.")
        # Decide if this is an error or just warning - let's treat as warning for now
        # raise ValueError("Indicator calculation returned empty result.")

    logger.print_debug("Indicator calculation finished.")

    # --- Debug Print Tail ---
    if result_df is not None and not result_df.empty:
        logger.print_debug(f"\n--- DEBUG: Result DF Tail for Rule: {selected_rule.name} ---")
        cols_to_debug = ['Open', 'PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']
        existing_cols_to_debug = [col for col in cols_to_debug if col in result_df.columns]
        if existing_cols_to_debug:
             debug_tail_str = result_df[existing_cols_to_debug].tail().to_string()
             logger.print_debug(debug_tail_str)
        else:
             logger.print_debug("No differentiating columns found for tail debug print.")
        logger.print_debug(f"--- END DEBUG ---")

    return result_df, selected_rule