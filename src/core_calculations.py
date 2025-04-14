# -*- coding: utf-8 -*-
# src/core_calculations.py

"""
Core calculation functions for the Shcherbyna Pressure Vector indicator components.
"""

import pandas as pd
import numpy as np
from .constants import BUY, SELL # Import from constants within the same package

# --- Helper function for reversing signals ---
def reverse_signal_value(signal):
    """Reverses BUY to SELL and vice versa."""
    if signal == BUY:
        return SELL
    elif signal == SELL:
        return BUY
    else:
        return signal # Keep NOTRADE etc. as is

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

def calculate_lwma(open_series: pd.Series, period: int) -> pd.Series:
    """Calculates LWMA (using SMMA logic) with the specified period."""
    if period < 1:
        # raise ValueError("LWMA period must be >= 1.")
        print(f"Warning: LWMA period ({period}) < 1, returning NaNs.")
        return pd.Series(np.nan, index=open_series.index)
    # SMMA alpha = 1 / period
    # Use adjust=False to mimic MQL5's recursive nature
    lwma = open_series.ewm(alpha=1/period, adjust=False).mean()
    return lwma

def calculate_core1(open_series: pd.Series, open_prev: pd.Series, period: int) -> pd.Series:
    """
    Calculates CORE1 using the specific MQL5-like iterative smoothing.
    Note: The MQL smoothing formula `Prev * (n+1)/n + New/n` is unusual and likely
    differs from standard EMA/SMMA/Wilder's smoothing. This function attempts
    to replicate the *written* MQL logic.
    """
    if period <= 0:
        # raise ValueError("CORE1 period must be > 0.")
         print(f"Warning: CORE1 period ({period}) <= 0, using period=1 and standard RSI logic.")
         # Fallback to a standard RSI-like calculation if period is invalid?
         # Or just return NaN? Let's try standard RSI for period=1 for now.
         delta = open_series.diff()
         gain = delta.where(delta > 0, 0).fillna(0)
         loss = -delta.where(delta < 0, 0).fillna(0)
         avg_gain = gain.ewm(com=1 - 1, min_periods=1, adjust=False).mean() # Alpha=1/(N) -> com=N-1; N=1 -> com=0 -> alpha=1
         avg_loss = loss.ewm(com=1 - 1, min_periods=1, adjust=False).mean()
         rs = avg_gain / avg_loss.replace(0, 1e-9)
         core1 = 100.0 - (100.0 / (1.0 + rs))
         return core1.fillna(50.0) # Fill initial NaNs


    price_diff = open_series - open_prev
    pos_diff_series = pd.Series(np.nan, index=open_series.index)
    neg_diff_series = pd.Series(np.nan, index=open_series.index) # MQL used same logic

    first_valid_index = price_diff.first_valid_index()
    pos_diff_prev = np.nan
    neg_diff_prev = np.nan
    n = period # Use n directly from MQL formula

    if first_valid_index is not None:
        price_diff_first = price_diff.loc[first_valid_index]
        if pd.notna(price_diff_first):
            pos_val_init = price_diff_first if price_diff_first > 0.0 else 0.0
            neg_val_init = price_diff_first if price_diff_first > 0.0 else 0.0 # MQL logic
            pos_diff_series.loc[first_valid_index] = pos_val_init
            neg_diff_series.loc[first_valid_index] = neg_val_init
            pos_diff_prev = pos_val_init
            neg_diff_prev = neg_val_init

            # Iterative calculation
            for idx in open_series.index[open_series.index > first_valid_index]:
                price_diff_curr = price_diff.loc[idx]

                if pd.isna(price_diff_curr):
                    pos_diff_series.loc[idx] = pos_diff_prev
                    neg_diff_series.loc[idx] = neg_diff_prev
                    continue

                new_pos = price_diff_curr if price_diff_curr > 0.0 else 0.0
                new_neg = price_diff_curr if price_diff_curr > 0.0 else 0.0 # MQL logic

                current_pos = pos_diff_prev # Default to previous if calculation fails
                current_neg = neg_diff_prev

                # Apply MQL smoothing: Prev * (n+1)/n + New/n
                if pd.notna(pos_diff_prev):
                    current_pos = (pos_diff_prev * (n + 1) + new_pos) / n
                else:
                    current_pos = new_pos # Initialize if previous was NaN

                if pd.notna(neg_diff_prev):
                    current_neg = (neg_diff_prev * (n + 1) + new_neg) / n
                else:
                    current_neg = new_neg # Initialize

                pos_diff_series.loc[idx] = current_pos
                neg_diff_series.loc[idx] = current_neg

                # Update previous values for the next iteration
                pos_diff_prev = current_pos
                neg_diff_prev = current_neg


    # Calculate CORE1 based on smoothed differences (Standard RSI formula part)
    rs = pos_diff_series / neg_diff_series.replace(0, 1e-9)
    core1 = 100.0 - (100.0 / (1.0 + rs))
    # Handle cases where NegDiff was truly zero
    core1 = np.where(neg_diff_series == 0,
                     np.where(pos_diff_series != 0, 100.0, 50.0),
                     core1)
    # Fill remaining NaNs (e.g., at the start) with 50.0
    core1 = pd.Series(core1, index=open_series.index).fillna(50.0)

    return core1