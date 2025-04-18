# src/calculation/indicator_calculation.py # MODIFIED

"""
Workflow Step 3: Calculates the indicator and optionally validates against CSV data.
All comments are in English.
"""

import pandas as pd
import numpy as np # Added for comparison
# Use relative imports within the src package
from ..common import logger
from ..common.constants import TradingRule
# Import the main calculation function from indicator module
from .indicator import calculate_pressure_vector


# Definition of the calculate_indicator function
def calculate_indicator(args, ohlcv_df: pd.DataFrame, point_size: float):
    """
    Performs indicator calculation based on selected rule.
    If mode is 'csv', also compares calculated Pressure and PV against
    'pressure' and 'pressure_vector' columns from the input CSV.

    Args:
        args (argparse.Namespace): Parsed command-line arguments (must contain 'mode').
        ohlcv_df (pd.DataFrame): DataFrame with OHLCV data. Should contain
                                 'pressure' and 'pressure_vector' if mode is 'csv'
                                 for validation.
        point_size (float): Determined point size.

    Returns:
        tuple: (result_df, selected_rule) containing calculated indicator values.
               Raises ValueError/KeyError on critical failure.
    """
    # --- Input Validation ---
    # Checks if the input DataFrame is valid.
    if ohlcv_df is None or ohlcv_df.empty:
        raise ValueError("No data available for calculation.")
    # Checks if a valid point size was determined.
    if point_size is None:
         raise ValueError("Point size is None. Cannot calculate indicator.")

    logger.print_info(f"\n--- Step 3: Calculating Indicator (Rule: {args.rule}) ---")

    # --- Rule Name Conversion ---
    # Converts rule alias (e.g., 'PHLD') or name to TradingRule enum member.
    rule_input_str = args.rule
    # Defines a dictionary mapping aliases to full rule names.
    rule_aliases_map = {'PHLD': 'Predict_High_Low_Direction', 'PV': 'Pressure_Vector', 'SR': 'Support_Resistants'}
    # Gets the full rule name, using alias map or the input directly.
    rule_name_str = rule_aliases_map.get(rule_input_str.upper(), rule_input_str)
    try:
        # Tries to get the TradingRule enum member corresponding to the name.
        selected_rule = TradingRule[rule_name_str]
        logger.print_debug(f"Mapped rule input '{args.rule}' to enum member '{selected_rule.name}'")
    # Catches error if the rule name is invalid.
    except KeyError:
        # Lists all valid rule names and aliases for the error message.
        available_rules = list(TradingRule.__members__.keys()) + list(rule_aliases_map.keys())
        raise ValueError(f"Invalid rule name or alias '{args.rule}'. Use one of {available_rules}")

    # --- Column Check & Rename for Calculation ---
    # Defines essential columns needed for the indicator calculation function.
    required_cols_indicator = ['Open', 'High', 'Low', 'Close', 'Volume']
    # Checks if all required columns exist in the input DataFrame.
    if not all(col in ohlcv_df.columns for col in required_cols_indicator):
        # Raises error if required columns are missing.
        raise ValueError(f"DataFrame missing required columns for calculation: {required_cols_indicator}. Has: {ohlcv_df.columns.tolist()}")

    # Rename 'Volume' to 'TickVolume' as expected by calculate_pressure_vector
    # Creates a new DataFrame with 'Volume' possibly renamed to 'TickVolume'.
    # errors='ignore' prevents error if 'Volume' column doesn't exist (shouldn't happen due to check above).
    # A copy is made implicitly here because rename returns a new DF unless inplace=True is used.
    ohlcv_df_calc_input = ohlcv_df.rename(columns={'Volume': 'TickVolume'}, errors='ignore')

    # Store original MQL5 results before calculation if mode is csv
    # Initializes variables for storing original MQL5 values.
    pressure_mql5 = None
    pv_mql5 = None
    # Checks if the mode is 'csv' to attempt storing original values for comparison.
    if args.mode == 'csv':
        logger.print_debug("CSV mode: Attempting to store original 'pressure' and 'pressure_vector' columns for validation.")
        # Checks if the expected MQL5 columns exist in the original DataFrame.
        if 'pressure' in ohlcv_df.columns and 'pressure_vector' in ohlcv_df.columns:
            # Copies the original MQL5 columns into separate Series objects.
            pressure_mql5 = ohlcv_df['pressure'].copy()
            pv_mql5 = ohlcv_df['pressure_vector'].copy()
            logger.print_debug("Successfully stored original MQL5 columns.")
        else:
            # Logs a warning if the MQL5 columns needed for validation are missing.
            logger.print_warning("Columns 'pressure' or 'pressure_vector' not found in CSV for validation.")


    # --- Calculation Call ---
    # Executes the main indicator calculation function.
    try:
        # Passes a copy of the potentially renamed DataFrame to avoid modifying the original used for validation.
        result_df = calculate_pressure_vector(
            df=ohlcv_df_calc_input.copy(), # Use the renamed df, pass a copy
            point=point_size,
            tr_num=selected_rule, # Pass the enum member directly
        )
    # Catches any exceptions during the calculation.
    except Exception as e:
         logger.print_error(f"Exception during calculate_pressure_vector: {e}")
         import traceback
         # Prints the full traceback if an error occurs.
         print(traceback.format_exc())
         # Re-raises the exception to be handled by the main workflow.
         raise

    # --- Post-Calculation Checks ---
    # Checks if the calculation returned a valid DataFrame.
    if result_df is None or result_df.empty:
        logger.print_warning("Indicator calculation returned None or empty DataFrame.")
        # Optional: Could raise an error here, but currently treated as a warning.
        # raise ValueError("Indicator calculation returned empty result.")

    logger.print_debug("Indicator calculation finished.")


    # --- Validation Against CSV (if applicable) --- ADDED THIS BLOCK ---
    # Checks if running in CSV mode and if original MQL5 data was stored.
    if args.mode == 'csv' and pressure_mql5 is not None and pv_mql5 is not None and result_df is not None and not result_df.empty:
        logger.print_info("\n--- Indicator Calculation Validation (CSV Mode) ---")
        logger.print_info("Comparing Python results ('Pressure', 'PV') against CSV columns ('pressure', 'pressure_vector')...")

        validation_summary = [] # To store validation messages

        # Check if calculated columns exist
        # Checks if the Python-calculated columns exist in the result DataFrame.
        if 'Pressure' in result_df.columns and 'PV' in result_df.columns:
            # Extract calculated series
            # Extracts the Python-calculated Series.
            pressure_py = result_df['Pressure']
            pv_py = result_df['PV']

            # Align indexes (important if calculation dropped/added rows, though unlikely here)
            # Aligns the MQL5 and Python Series based on their DateTimeIndex. 'inner' join keeps only matching dates.
            pressure_mql5_aligned, pressure_py_aligned = pressure_mql5.align(pressure_py, join='inner')
            pv_mql5_aligned, pv_py_aligned = pv_mql5.align(pv_py, join='inner')

            # Define tolerance for float comparison
            # Sets the absolute and relative tolerances for comparing floating-point numbers.
            atol = 1e-6
            rtol = 1e-6

            # Compare Pressure
            # Compares the aligned Pressure series using numpy.isclose.
            # equal_nan=True treats NaN values in both series at the same position as equal.
            pressure_matches = np.isclose(pressure_mql5_aligned, pressure_py_aligned, atol=atol, rtol=rtol, equal_nan=True)
            # Calculates the number of mismatches.
            pressure_mismatches = len(pressure_matches) - np.sum(pressure_matches)
            # Calculates correlation between the two series.
            pressure_corr = pressure_mql5_aligned.corr(pressure_py_aligned)
            # Calculates the mean absolute difference.
            pressure_mad = (pressure_mql5_aligned - pressure_py_aligned).abs().mean()
            # Appends comparison results for Pressure to the summary list.
            validation_summary.append("Pressure Comparison:")
            validation_summary.append(f"  - Mismatches (atol={atol}): {pressure_mismatches} / {len(pressure_matches)} ({pressure_mismatches/len(pressure_matches)*100:.2f}%)")
            validation_summary.append(f"  - Correlation: {pressure_corr:.6f}")
            validation_summary.append(f"  - Mean Absolute Difference: {pressure_mad:.6f}")

            # Compare PV (Pressure Vector)
            # Compares the aligned PV series.
            pv_matches = np.isclose(pv_mql5_aligned, pv_py_aligned, atol=atol, rtol=rtol, equal_nan=True)
            # Calculates PV mismatches.
            pv_mismatches = len(pv_matches) - np.sum(pv_matches)
            # Calculates PV correlation.
            pv_corr = pv_mql5_aligned.corr(pv_py_aligned)
            # Calculates PV mean absolute difference.
            pv_mad = (pv_mql5_aligned - pv_py_aligned).abs().mean()
            # Appends comparison results for PV to the summary list.
            validation_summary.append("PV (Pressure Vector) Comparison:")
            validation_summary.append(f"  - Mismatches (atol={atol}): {pv_mismatches} / {len(pv_matches)} ({pv_mismatches/len(pv_matches)*100:.2f}%)")
            validation_summary.append(f"  - Correlation: {pv_corr:.6f}")
            validation_summary.append(f"  - Mean Absolute Difference: {pv_mad:.6f}")

            # Optionally print first few mismatches for debugging
            # Finds the indices where Pressure values don't match.
            pressure_mismatch_indices = pressure_mql5_aligned.index[~pressure_matches]
            # Checks if there are any Pressure mismatches.
            if not pressure_mismatch_indices.empty:
                 # Logs a sample of the first 5 Pressure mismatches.
                 validation_summary.append("Sample Pressure Mismatches (Index, MQL5, Python):")
                 # Creates a DataFrame showing the mismatching values.
                 diff_df_p = pd.DataFrame({
                     'MQL5': pressure_mql5_aligned.loc[pressure_mismatch_indices[:5]],
                     'Python': pressure_py_aligned.loc[pressure_mismatch_indices[:5]]
                 })
                 validation_summary.append(diff_df_p.to_string())

            # Finds the indices where PV values don't match.
            pv_mismatch_indices = pv_mql5_aligned.index[~pv_matches]
            # Checks if there are any PV mismatches.
            if not pv_mismatch_indices.empty:
                 # Logs a sample of the first 5 PV mismatches.
                 validation_summary.append("Sample PV Mismatches (Index, MQL5, Python):")
                 # Creates a DataFrame showing the mismatching values.
                 diff_df_pv = pd.DataFrame({
                     'MQL5': pv_mql5_aligned.loc[pv_mismatch_indices[:5]],
                     'Python': pv_py_aligned.loc[pv_mismatch_indices[:5]]
                 })
                 validation_summary.append(diff_df_pv.to_string())

        else:
             # Logs a warning if the Python-calculated columns are missing.
             validation_summary.append("Warning: Calculated 'Pressure' or 'PV' columns not found in result_df. Cannot perform validation.")

        # Prints the collected validation summary messages.
        for line in validation_summary:
             logger.print_info(line)
        logger.print_info("--- End Validation ---")
    # End of validation block

    # --- Debug Print Tail ---
    # Prints the tail of the result DataFrame for debugging purposes.
    if result_df is not None and not result_df.empty:
        logger.print_debug(f"\n--- DEBUG: Result DF Tail for Rule: {selected_rule.name} ---")
        # Defines columns typically generated by rules, for debugging output.
        cols_to_debug = ['Open', 'PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']
        # Filters the debug columns to only those that actually exist in the result DataFrame.
        existing_cols_to_debug = [col for col in cols_to_debug if col in result_df.columns]
        # Checks if any relevant columns for debugging were found.
        if existing_cols_to_debug:
             # Converts the tail of the selected columns to a string for logging.
             debug_tail_str = result_df[existing_cols_to_debug].tail().to_string()
             logger.print_debug(debug_tail_str)
        else:
             logger.print_debug("No differentiating rule output columns found for tail debug print.")
        logger.print_debug(f"--- END DEBUG ---")

    # Returns the DataFrame containing the calculation results and the selected rule enum member.
    return result_df, selected_rule