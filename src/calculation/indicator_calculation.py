# -*- coding: utf-8 -*-
# src/calculation/indicator_calculation.py

"""
Workflow Step 3: Calculates the indicator and optionally validates against CSV data.
All comments are in English.
"""

import pandas as pd
import numpy as np # Added for comparison
# Use relative imports within the src package
from ..common import logger
from ..common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
# Import the main calculation function from indicator module
from .indicator import calculate_pressure_vector
from ..cli.cli import parse_indicator_parameters

# Definition of the calculate_indicator function
def calculate_indicator(args, ohlcv_df: pd.DataFrame, point_size: float):
    """
    Performs indicator calculation based on selected rule.
    If mode is 'csv', also compares calculated Pressure/PV and potentially
    PPrice1/PPrice2 against corresponding columns from the input CSV.

    Args:
        args (argparse.Namespace): Parsed command-line arguments (must contain 'mode').
        ohlcv_df (pd.DataFrame): DataFrame with OHLCV data. Should contain relevant
                                 MQL5 columns if mode is 'csv' for validation.
        point_size (float): Determined point size.

    Returns:
        tuple: (result_df, selected_rule) containing calculated indicator values.
               Raises ValueError/KeyError on critical failure.
    """
    # Parse indicator parameters if provided in format 'indicator:param1,param2,param3,param4'
    rule_input_str = args.rule
    indicator_params = {}
    original_rule_with_params = rule_input_str  # Store original rule with parameters
    
    if ':' in rule_input_str:
        indicator_name, indicator_params = parse_indicator_parameters(rule_input_str)
        # Update the rule name to the parsed indicator name (всегда в верхнем регистре)
        rule_input_str = indicator_name.upper()
    
    # Store original rule with parameters for display purposes
    setattr(args, 'original_rule_with_params', original_rule_with_params)
    
    # Map rule aliases to full names
    rule_aliases_map = {
        'PHLD': 'Predict_High_Low_Direction', 
        'PV': 'Pressure_Vector', 
        'SR': 'Support_Resistants',
        'RSI': 'RSI',
        'RSI_MOM': 'RSI_Momentum',
        'RSI_DIV': 'RSI_Divergence',
        'RSI_MOMENTUM': 'RSI_Momentum',
        'RSI_DIVERGENCE': 'RSI_Divergence',
        'CCI': 'CCI',
        'STOCH': 'Stochastic',
        'EMA': 'EMA',
        'BB': 'Bollinger_Bands',
        'ATR': 'ATR',
        'VWAP': 'VWAP',
        'PIVOT': 'Pivot_Points',
        # Momentum indicators
        'MACD': 'MACD',
        'STOCHOSC': 'StochOscillator',
        'STOCHOSCILLATOR': 'StochOscillator',
        # Predictive indicators
        'HMA': 'HMA',
        'TSF': 'TSForecast',
        # Probability indicators
        'MC': 'MonteCarlo',
        'MONTE': 'MonteCarlo',
        'KELLY': 'Kelly',
        # Sentiment indicators
        'FG': 'FearGreed',
        'COT': 'COT',
            'PCR': 'PutCallRatio',
    'PUTCALLRATIO': 'PutCallRatio',
    'putcallratio': 'PutCallRatio',
        # Support/Resistance indicators
        'DONCHAIN': 'Donchain',
        'FIBO': 'FiboRetr',
        # Volume indicators
        'OBV': 'OBV',
        # Volatility indicators
        'STDEV': 'StDev',
        # Trend indicators
        'ADX': 'ADX',
        'SAR': 'SAR',
        'SUPERTREND': 'SuperTrend'
    }
    rule_name_str = rule_aliases_map.get(rule_input_str.upper(), rule_input_str)
    try:
        selected_rule = TradingRule[rule_name_str]
    except KeyError:
        available_rules = list(TradingRule.__members__.keys()) + list(rule_aliases_map.keys()) + ['putcallratio']
        raise ValueError(f"Invalid rule name or alias '{args.rule}'. Use one of {available_rules}")

    # --- Column Check & Rename for Calculation ---
    if ohlcv_df is None:
        raise ValueError("No data available for calculation")
    
    required_cols_indicator = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in ohlcv_df.columns for col in required_cols_indicator):
        raise ValueError(f"DataFrame missing required columns for calculation: {required_cols_indicator}. Has: {ohlcv_df.columns.tolist()}")

    ohlcv_df_calc_input = ohlcv_df.rename(columns={'Volume': 'TickVolume'}, errors='ignore')

    # Store original MQL5 results before calculation if mode is csv
    pressure_mql5 = None
    pv_mql5 = None
    # ADDED: Store predicted low/high from MQL5 CSV
    pred_low_mql5 = None
    pred_high_mql5 = None
    if args.mode == 'csv':
        # Store Pressure/PV
        if 'pressure' in ohlcv_df.columns and 'pressure_vector' in ohlcv_df.columns:
            pressure_mql5 = ohlcv_df['pressure'].copy()
            pv_mql5 = ohlcv_df['pressure_vector'].copy()
        # Store predicted_low/predicted_high
        if 'predicted_low' in ohlcv_df.columns and 'predicted_high' in ohlcv_df.columns:
             pred_low_mql5 = ohlcv_df['predicted_low'].copy()
             pred_high_mql5 = ohlcv_df['predicted_high'].copy()


    # --- Calculation Call ---
    result_df = None  # Initialize result_df
    try:
        # Special handling for OHLCV rule - don't calculate indicators, just return raw data
        if selected_rule == TradingRule.OHLCV:
            # Return the original dataframe without calculations
            # Add original rule with parameters to the rule object for display
            setattr(selected_rule, 'original_rule_with_params', original_rule_with_params)
            return ohlcv_df.copy(), selected_rule
        
        # Special handling for AUTO rule - calculate indicators but return all columns for display
        if selected_rule == TradingRule.AUTO:
            result_df = calculate_pressure_vector(
                df=ohlcv_df_calc_input.copy(),
                point=point_size,
                tr_num=selected_rule,
                price_type=getattr(args, 'price_type', 'close'),
            )
            # For AUTO mode, preserve all original columns if they exist in CSV mode
            if args.mode == 'csv':
                # Merge original extra columns (like predicted_high, predicted_low, etc.) back into result
                extra_cols = [col for col in ohlcv_df.columns 
                             if col not in ['Open', 'High', 'Low', 'Close', 'Volume', 'TickVolume']]
                for col in extra_cols:
                    if col not in result_df.columns:
                        result_df[col] = ohlcv_df[col]
            # Add original rule with parameters to the rule object for display
            setattr(selected_rule, 'original_rule_with_params', original_rule_with_params)
            return result_df, selected_rule

        # Apply indicator parameters if provided
        price_type = indicator_params.get('price_type', getattr(args, 'price_type', 'close'))
        
        # Create a modified args object with indicator parameters
        modified_args = args
        for param_name, param_value in indicator_params.items():
            setattr(modified_args, param_name, param_value)
        
        result_df = calculate_pressure_vector(
            df=ohlcv_df_calc_input.copy(),
            point=point_size,
            tr_num=selected_rule,
            **indicator_params
        )
        
        # Add original rule with parameters to the rule object for display
        setattr(selected_rule, 'original_rule_with_params', original_rule_with_params)
        
    except Exception as e:
        logger.print_error(f"Calculation failed: {e}")
        result_df = None

    # --- Post-Calculation Checks ---
    if result_df is None or result_df.empty:
        logger.print_warning("Indicator calculation returned None or empty DataFrame.")
        return None, selected_rule

    # --- Validation Against CSV (if applicable) --- MODIFIED BLOCK ---
    if args.mode == 'csv' and result_df is not None and not result_df.empty:
        validation_summary = []
        atol = 1e-6 # Absolute tolerance for float comparison
        rtol = 1e-6 # Relative tolerance for float comparison

        # --- Compare Pressure / PV (Always attempt if columns exist) ---
        if pressure_mql5 is not None and pv_mql5 is not None and 'Pressure' in result_df.columns and 'PV' in result_df.columns:
            pressure_py = result_df['Pressure']
            pv_py = result_df['PV']
            pressure_mql5_aligned, pressure_py_aligned = pressure_mql5.align(pressure_py, join='inner')
            pv_mql5_aligned, pv_py_aligned = pv_mql5.align(pv_py, join='inner')

            # Compare Pressure
            pressure_matches = np.isclose(pressure_mql5_aligned, pressure_py_aligned, atol=atol, rtol=rtol, equal_nan=True)
            pressure_mismatches = len(pressure_matches) - np.sum(pressure_matches)
            pressure_corr = pressure_mql5_aligned.corr(pressure_py_aligned) if len(pressure_mql5_aligned.dropna()) > 1 else np.nan
            pressure_mad = (pressure_mql5_aligned - pressure_py_aligned).abs().mean()
            validation_summary.append("Pressure Comparison:")
            validation_summary.append(f"  - Mismatches (atol={atol}): {pressure_mismatches} / {len(pressure_matches)} ({pressure_mismatches/len(pressure_matches)*100:.2f}%)")
            validation_summary.append(f"  - Correlation: {pressure_corr:.6f}")
            validation_summary.append(f"  - Mean Absolute Difference: {pressure_mad:.6f}")

            # Compare PV (Pressure Vector)
            pv_matches = np.isclose(pv_mql5_aligned, pv_py_aligned, atol=atol, rtol=rtol, equal_nan=True)
            pv_mismatches = len(pv_matches) - np.sum(pv_matches)
            pv_corr = pv_mql5_aligned.corr(pv_py_aligned) if len(pv_mql5_aligned.dropna()) > 1 else np.nan
            pv_mad = (pv_mql5_aligned - pv_py_aligned).abs().mean()
            validation_summary.append("PV (Pressure Vector) Comparison:")
            validation_summary.append(f"  - Mismatches (atol={atol}): {pv_mismatches} / {len(pv_matches)} ({pv_mismatches/len(pv_matches)*100:.2f}%)")
            validation_summary.append(f"  - Correlation: {pv_corr:.6f}")
            validation_summary.append(f"  - Mean Absolute Difference: {pv_mad:.6f}")
        else:
             validation_summary.append("Warning: Could not perform Pressure/PV validation (missing columns in CSV or calculation results).")

        # --- Compare Predicted Low/High (Only for relevant rules) --- ADDED THIS SECTION ---
        # Checks if the current rule is one that calculates predicted levels and if MQL5/Python columns exist.
        if selected_rule in [TradingRule.Predict_High_Low_Direction, TradingRule.Support_Resistants]:
            validation_summary.append(f"Predicted Low/High Comparison (Rule: {selected_rule.name}):")
            # Checks required columns existence for this specific comparison.
            if pred_low_mql5 is not None and pred_high_mql5 is not None and \
               'PPrice1' in result_df.columns and 'PPrice2' in result_df.columns:

                # Extract Python predicted levels
                pred_low_py = result_df['PPrice1'] # Assuming PPrice1 corresponds to predicted low
                pred_high_py = result_df['PPrice2'] # Assuming PPrice2 corresponds to predicted high

                # Align series
                pred_low_mql5_aligned, pred_low_py_aligned = pred_low_mql5.align(pred_low_py, join='inner')
                pred_high_mql5_aligned, pred_high_py_aligned = pred_high_mql5.align(pred_high_py, join='inner')

                # Compare Predicted Low (MQL5 predicted_low vs Python PPrice1)
                low_matches = np.isclose(pred_low_mql5_aligned, pred_low_py_aligned, atol=atol, rtol=rtol, equal_nan=True)
                low_mismatches = len(low_matches) - np.sum(low_matches)
                low_corr = pred_low_mql5_aligned.corr(pred_low_py_aligned) if len(pred_low_mql5_aligned.dropna()) > 1 else np.nan
                low_mad = (pred_low_mql5_aligned - pred_low_py_aligned).abs().mean()
                validation_summary.append("  Predicted Low Comparison (CSV 'predicted_low' vs Python 'PPrice1'):")
                validation_summary.append(f"    - Mismatches (atol={atol}): {low_mismatches} / {len(low_matches)} ({low_mismatches/len(low_matches)*100:.2f}%)")
                validation_summary.append(f"    - Correlation: {low_corr:.6f}")
                validation_summary.append(f"    - Mean Absolute Difference: {low_mad:.6f}")

                # Compare Predicted High (MQL5 predicted_high vs Python PPrice2)
                high_matches = np.isclose(pred_high_mql5_aligned, pred_high_py_aligned, atol=atol, rtol=rtol, equal_nan=True)
                high_mismatches = len(high_matches) - np.sum(high_matches)
                high_corr = pred_high_mql5_aligned.corr(pred_high_py_aligned) if len(pred_high_mql5_aligned.dropna()) > 1 else np.nan
                high_mad = (pred_high_mql5_aligned - pred_high_py_aligned).abs().mean()
                validation_summary.append("  Predicted High Comparison (CSV 'predicted_high' vs Python 'PPrice2'):")
                validation_summary.append(f"    - Mismatches (atol={atol}): {high_mismatches} / {len(high_matches)} ({high_mismatches/len(high_matches)*100:.2f}%)")
                validation_summary.append(f"    - Correlation: {high_corr:.6f}")
                validation_summary.append(f"    - Mean Absolute Difference: {high_mad:.6f}")

                # Optionally print first few mismatches for Low prediction
                low_mismatch_indices = pred_low_mql5_aligned.index[~low_matches]
                if not low_mismatch_indices.empty:
                    validation_summary.append("    Sample Low Mismatches (Index, MQL5_pred_low, Python_PPrice1):")
                    diff_df_low = pd.DataFrame({
                        'MQL5': pred_low_mql5_aligned.loc[low_mismatch_indices[:5]],
                        'Python': pred_low_py_aligned.loc[low_mismatch_indices[:5]]
                    })
                    validation_summary.append(diff_df_low.to_string())

                 # Optionally print first few mismatches for High prediction
                high_mismatch_indices = pred_high_mql5_aligned.index[~high_matches]
                if not high_mismatch_indices.empty:
                     validation_summary.append("    Sample High Mismatches (Index, MQL5_pred_high, Python_PPrice2):")
                     diff_df_high = pd.DataFrame({
                         'MQL5': pred_high_mql5_aligned.loc[high_mismatch_indices[:5]],
                         'Python': pred_high_py_aligned.loc[high_mismatch_indices[:5]]
                     })
                     validation_summary.append(diff_df_high.to_string())

            else:
                validation_summary.append("Warning: Could not perform Predicted Low/High validation (missing columns in CSV or calculation results).")
        # End of Predicted Low/High comparison section

        # Print the complete validation summary
        for line in validation_summary:
            logger.print_info(line)
    # End of validation block

    # --- Debug Print Tail ---
    if result_df is not None and not result_df.empty:
        cols_to_debug = ['Open', 'PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']
        existing_cols_to_debug = [col for col in cols_to_debug if col in result_df.columns]
        if existing_cols_to_debug:
            logger.print_debug(f"Result DF Tail for Rule {selected_rule.name}:")
            logger.print_debug(result_df[existing_cols_to_debug].tail().to_string())
        else:
            logger.print_debug(f"No debug columns found for Rule {selected_rule.name}")

    return result_df, selected_rule

