# -*- coding: utf-8 -*-
# src/calculation/core_calculations.py

"""
Core calculation functions for the Shcherbyna Pressure Vector indicator components.
"""

import pandas as pd
import numpy as np

# Import logger for error reporting
try:
    from src.common import logger
except ImportError:
    # Fallback for direct imports
    try:
        from common import logger
    except ImportError:
        # Define a minimal logger if all imports fail
        class MinimalLogger:
            @staticmethod
            def print_warning(msg): print(f"WARNING: {msg}")
        logger = MinimalLogger()

# --- Core Calculation Functions ---

def calculate_hl(high_prev: pd.Series, low_prev: pd.Series, point: float) -> pd.Series:
    """Calculates High-Low range in points for the previous bar."""
    if point == 0:
        raise ValueError("Point size cannot be zero.")
    hl = (high_prev - low_prev) / point
    hl = hl.fillna(0) # Fill initial NaNs (due to shift) with 0
    # hl = hl.replace(0, np.nan) # Option: replace 0 with NaN if needed downstream
    return hl

def calculate_pressure(tick_volume_prev: pd.Series, hl_prev2: pd.Series) -> pd.Series:
    """Calculates Pressure based on previous volume and HL of bar before previous."""
    # Ensure hl_prev2 is numeric and handle potential division by zero
    hl_prev2_numeric = pd.to_numeric(hl_prev2, errors='coerce').replace(0, np.nan)

    # Convert Series to simple numpy arrays for safer operations
    try:
        # Extract values as 1D arrays
        tick_vol_values = np.ravel(tick_volume_prev.values)
        hl_values = np.ravel(hl_prev2_numeric.values)

        # Ensure equal lengths by truncating to minimum length
        min_length = min(len(tick_vol_values), len(hl_values))
        tick_vol_values = tick_vol_values[:min_length]
        hl_values = hl_values[:min_length]

        # Calculate pressure safely with numpy
        pressure_values = np.zeros_like(tick_vol_values, dtype=float)

        # Set to NaN by default
        pressure_values.fill(np.nan)

        # Find valid indices where we can calculate
        valid_indices = ~np.isnan(tick_vol_values) & ~np.isnan(hl_values) & (hl_values != 0)

        # Calculate only for valid indices
        if np.any(valid_indices):
            pressure_values[valid_indices] = tick_vol_values[valid_indices] / hl_values[valid_indices]

        # Create a Series with the calculated values
        return pd.Series(
            pressure_values,
            index=tick_volume_prev.index[:min_length] if min_length < len(tick_volume_prev.index) else tick_volume_prev.index
        )
    except Exception as e:
        # Fallback to simpler method if something goes wrong
        logger.print_warning(f"Fallback calculation for pressure: {str(e)}")
        # Use simple Series division with NaN handling
        return tick_volume_prev / hl_prev2_numeric

def calculate_pv(pressure: pd.Series, pressure_prev: pd.Series) -> pd.Series:
    """Calculates the Pressure Vector (PV)."""
    pv = pressure - pressure_prev
    return pv
