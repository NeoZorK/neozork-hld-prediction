# src/calculation/indicator_calculation.py

"""
Wrapper function for the main indicator calculation logic.
Handles calling the core calculation and potentially validation steps.
All comments are in English.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict # Import Dict

# Use relative imports for constants, logger, and core indicator function
from ..common.constants import TradingRule, EMPTY_VALUE
from ..common import logger
from .indicator import calculate_pressure_vector

# Definition of the main calculation wrapper function
# *** CORRECTED: Added data_info argument ***
def calculate_indicator(
    df: pd.DataFrame,
    rule: TradingRule,
    point_size: float,
    data_info: Dict # <-- Added data_info argument
) -> Optional[pd.DataFrame]:
    """
    Calculates the indicator and performs validation if applicable (e.g., CSV mode).

    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data.
        rule (TradingRule): The trading rule enum member to apply.
        point_size (float): The instrument's point size.
        data_info (Dict): Dictionary containing metadata about the data source,
                          used here to check if mode is 'csv' for validation.

    Returns:
        Optional[pd.DataFrame]: DataFrame with calculated results, or None on failure.
    """
    if df is None or df.empty:
        logger.print_error("Input DataFrame is empty in calculate_indicator.")
        return None

    logger.print_debug("Starting indicator calculation...")
    # Call the core function that calculates PV and applies rules
    result_df = calculate_pressure_vector(df, point_size, rule)

    if result_df is None:
        logger.print_error("Core indicator calculation failed.")
        return None

    # --- Validation specific to CSV mode ---
    # Check if running in CSV mode and if validation columns exist
    if data_info.get('mode') == 'csv':
        logger.print_info("Running in CSV mode, performing validation...")
        required_validation_cols = ['pressure', 'pressure_vector', 'predicted_low', 'predicted_high']
        # Check which validation columns are actually present in the original CSV data (now in result_df)
        validation_cols_present = [col for col in required_validation_cols if col in result_df.columns]

        if not validation_cols_present:
             logger.print_warning("No validation columns (pressure, pressure_vector, predicted_low, predicted_high) found in CSV data for comparison.")
        else:
             logger.print_debug(f"Validation columns found: {validation_cols_present}")
             validation_results = {}

             # Validate Pressure
             if 'Pressure' in result_df.columns and 'pressure' in validation_cols_present:
                 # Ensure both columns are numeric, fillna for comparison
                 calc_pressure = pd.to_numeric(result_df['Pressure'], errors='coerce').fillna(0)
                 csv_pressure = pd.to_numeric(result_df['pressure'], errors='coerce').fillna(0)
                 mae_pressure = (calc_pressure - csv_pressure).abs().mean()
                 validation_results['Pressure MAE'] = mae_pressure
                 logger.print_debug(f"Pressure vs csv_pressure MAE: {mae_pressure:.6f}")
             else:
                  logger.print_warning("Could not validate Pressure (missing calculated 'Pressure' or original 'pressure' column).")


             # Validate PV (Pressure Vector)
             if 'PV' in result_df.columns and 'pressure_vector' in validation_cols_present:
                 # Ensure both columns are numeric, fillna for comparison
                 calc_pv = pd.to_numeric(result_df['PV'], errors='coerce').fillna(0)
                 csv_pv = pd.to_numeric(result_df['pressure_vector'], errors='coerce').fillna(0)
                 mae_pv = (calc_pv - csv_pv).abs().mean()
                 validation_results['PV MAE'] = mae_pv
                 logger.print_debug(f"PV vs csv_pressure_vector MAE: {mae_pv:.6f}")
             else:
                  logger.print_warning("Could not validate PV (missing calculated 'PV' or original 'pressure_vector' column).")


             # Validate Predicted Prices (PPrice1/PPrice2 vs predicted_low/predicted_high)
             # Note: This validation might show differences due to potential formula discrepancies
             # between MQL5 export and current Python rule implementation.
             rule_needs_price_validation = rule in [TradingRule.Predict_High_Low_Direction, TradingRule.Support_Resistants]

             if rule_needs_price_validation:
                  # Validate PPrice1 vs predicted_low
                  if 'PPrice1' in result_df.columns and 'predicted_low' in validation_cols_present:
                       calc_pp1 = pd.to_numeric(result_df['PPrice1'], errors='coerce').fillna(EMPTY_VALUE) # Use EMPTY_VALUE (nan)
                       csv_plow = pd.to_numeric(result_df['predicted_low'], errors='coerce').fillna(EMPTY_VALUE)
                       # Calculate MAE only where both are not NaN
                       valid_mask = ~np.isnan(calc_pp1) & ~np.isnan(csv_plow)
                       if valid_mask.any():
                            mae_pp1 = (calc_pp1[valid_mask] - csv_plow[valid_mask]).abs().mean()
                            validation_results['PPrice1 vs PredLow MAE'] = mae_pp1
                            logger.print_debug(f"PPrice1 vs csv_predicted_low MAE: {mae_pp1:.6f}")
                       else:
                            logger.print_warning("Not enough valid data points to compare PPrice1 and predicted_low.")
                  else:
                       logger.print_warning("Could not validate PPrice1 (missing calculated 'PPrice1' or original 'predicted_low' column).")


                  # Validate PPrice2 vs predicted_high
                  if 'PPrice2' in result_df.columns and 'predicted_high' in validation_cols_present:
                       calc_pp2 = pd.to_numeric(result_df['PPrice2'], errors='coerce').fillna(EMPTY_VALUE)
                       csv_phigh = pd.to_numeric(result_df['predicted_high'], errors='coerce').fillna(EMPTY_VALUE)
                       valid_mask = ~np.isnan(calc_pp2) & ~np.isnan(csv_phigh)
                       if valid_mask.any():
                            mae_pp2 = (calc_pp2[valid_mask] - csv_phigh[valid_mask]).abs().mean()
                            validation_results['PPrice2 vs PredHigh MAE'] = mae_pp2
                            logger.print_debug(f"PPrice2 vs csv_predicted_high MAE: {mae_pp2:.6f}")
                       else:
                            logger.print_warning("Not enough valid data points to compare PPrice2 and predicted_high.")
                  else:
                       logger.print_warning("Could not validate PPrice2 (missing calculated 'PPrice2' or original 'predicted_high' column).")

             # Store validation results in data_info for potential summary display
             if validation_results:
                  data_info['validation_results'] = validation_results
                  logger.print_info("Validation Results (CSV Mode):")
                  for key, value in validation_results.items():
                       print(f"  - {key}: {value:.6f}") # Print summary to console
                  # Add a note about potential PPrice discrepancies
                  if rule_needs_price_validation and ('PPrice1 vs PredLow MAE' in validation_results or 'PPrice2 vs PredHigh MAE' in validation_results):
                       logger.print_warning("Note: PPrice1/PPrice2 MAE might be non-zero due to differences between Python rule logic and MQL5 export formulas used for 'predicted_low'/'predicted_high'.")


    # Return the DataFrame with all calculations and rule outputs
    return result_df
