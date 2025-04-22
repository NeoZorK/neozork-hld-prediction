# src/calculation/core_calculations.py

"""
Core calculation functions for HL (High-Low), Pressure, and PV (Pressure Vector).
These functions operate directly on DataFrame columns.
All comments are in English.
"""

import pandas as pd
import numpy as np
from typing import Optional

# Use relative imports for constants and logger
from ..common.constants import EMPTY_VALUE
from ..common import logger

# Function to calculate High - Low range in points
# *** CORRECTED: Added point_size argument ***
def calculate_hl(df: pd.DataFrame, point_size: float) -> pd.DataFrame:
    """
    Calculates the High-Low range (HL) in points.

    Args:
        df (pd.DataFrame): DataFrame containing 'High' and 'Low' columns.
        point_size (float): The point size of the instrument.

    Returns:
        pd.DataFrame: DataFrame with an added 'HL' column (High-Low in points).
                      Returns original df if point_size is invalid or columns are missing.
    """
    if 'High' not in df.columns or 'Low' not in df.columns:
        logger.print_error("Missing 'High' or 'Low' column for HL calculation.")
        # Add empty HL column if missing? Or return df as is? Returning as is for now.
        if 'HL' not in df.columns:
             df['HL'] = EMPTY_VALUE
        return df

    if point_size is None or point_size <= 0:
         logger.print_error(f"Invalid point_size ({point_size}) for HL calculation. Cannot divide by zero or negative.")
         if 'HL' not in df.columns:
              df['HL'] = EMPTY_VALUE
         return df # Return df without calculating HL

    # Calculate HL in points
    try:
        # Ensure High and Low are numeric
        high_numeric = pd.to_numeric(df['High'], errors='coerce')
        low_numeric = pd.to_numeric(df['Low'], errors='coerce')
        # Calculate the difference, handle potential NaNs from coercion
        hl_diff = high_numeric - low_numeric
        # Divide by point size, handle potential division by zero (already checked point_size > 0)
        # Replace NaN results with EMPTY_VALUE
        df['HL'] = (hl_diff / point_size).replace([np.inf, -np.inf], np.nan).fillna(EMPTY_VALUE)
    except Exception as e:
         logger.print_error(f"Error calculating HL: {e}")
         if 'HL' not in df.columns:
              df['HL'] = EMPTY_VALUE

    return df


# Function to calculate Pressure
def calculate_pressure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Pressure = Volume / HL of the previous bar.

    Args:
        df (pd.DataFrame): DataFrame containing 'Volume' and 'HL' columns.

    Returns:
        pd.DataFrame: DataFrame with an added 'Pressure' column.
    """
    if 'Volume' not in df.columns or 'HL' not in df.columns:
        logger.print_error("Missing 'Volume' or 'HL' column for Pressure calculation.")
        if 'Pressure' not in df.columns:
             df['Pressure'] = EMPTY_VALUE
        return df

    try:
        # Ensure Volume and HL are numeric
        volume_numeric = pd.to_numeric(df['Volume'], errors='coerce')
        hl_numeric = pd.to_numeric(df['HL'], errors='coerce')

        # Shift HL to get the previous bar's HL
        hl_prev = hl_numeric.shift(1)

        # Calculate Pressure: Volume / HL_previous
        # Use np.divide to handle division by zero gracefully (results in inf)
        with np.errstate(divide='ignore', invalid='ignore'): # Suppress warnings
             pressure = np.divide(volume_numeric, hl_prev)

        # Replace inf/-inf/nan resulting from division by zero or NaN inputs
        df['Pressure'] = pd.Series(pressure, index=df.index).replace([np.inf, -np.inf], np.nan).fillna(EMPTY_VALUE)

    except Exception as e:
         logger.print_error(f"Error calculating Pressure: {e}")
         if 'Pressure' not in df.columns:
              df['Pressure'] = EMPTY_VALUE

    return df


# Function to calculate Pressure Vector (PV)
def calculate_pv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates PV = Pressure - Pressure of the previous bar.

    Args:
        df (pd.DataFrame): DataFrame containing the 'Pressure' column.

    Returns:
        pd.DataFrame: DataFrame with an added 'PV' column.
    """
    if 'Pressure' not in df.columns:
        logger.print_error("Missing 'Pressure' column for PV calculation.")
        if 'PV' not in df.columns:
             df['PV'] = EMPTY_VALUE
        return df

    try:
        # Ensure Pressure is numeric
        pressure_numeric = pd.to_numeric(df['Pressure'], errors='coerce')

        # Calculate PV using diff() which calculates the difference with the previous row
        # fillna(EMPTY_VALUE) handles the first row which will have NaN after diff()
        df['PV'] = pressure_numeric.diff().fillna(EMPTY_VALUE)

    except Exception as e:
         logger.print_error(f"Error calculating PV: {e}")
         if 'PV' not in df.columns:
              df['PV'] = EMPTY_VALUE

    return df

