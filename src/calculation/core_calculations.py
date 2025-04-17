# -*- coding: utf-8 -*-
# src/core_calculations.py

"""
Core calculation functions for the Shcherbyna Pressure Vector indicator components.
"""

import pandas as pd
import numpy as np

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

    # Select only calculated (not NA)
    pressure = np.where(
        (tick_volume_prev.notna()) & (hl_prev2_numeric.notna()),
        tick_volume_prev / hl_prev2_numeric,
        np.nan
    )
    return pd.Series(pressure, index=tick_volume_prev.index)

def calculate_pv(pressure: pd.Series, pressure_prev: pd.Series) -> pd.Series:
    """Calculates the Pressure Vector (PV)."""
    pv = pressure - pressure_prev
    return pv
