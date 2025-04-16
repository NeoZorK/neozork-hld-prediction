# src/utils.py

"""
General utility functions, including point size estimation.
All comments are in English.
"""
import pandas as pd
import numpy as np
from . import logger

def determine_point_size(ticker: str, df: pd.DataFrame) -> float:
    """Estimates the instrument's point size based on ticker and price data."""
    logger.print_info("[Info] Estimating point size...")
    ticker_upper = ticker.upper()

    # 1. Forex Heuristic (ticker ends with =X)
    if ticker_upper.endswith("=X"):
        logger.print_info("[Info] Ticker ends with '=X', assuming Forex point size: 0.00001")
        return 0.00001

    # 2. Calculate minimum non-zero High-Low difference
    min_hl_diff = np.nan
    if 'High' in df.columns and 'Low' in df.columns and not df.empty:
        # Ensure columns are numeric, coercing errors
        high_numeric = pd.to_numeric(df['High'], errors='coerce')
        low_numeric = pd.to_numeric(df['Low'], errors='coerce')
        if high_numeric.notna().any() and low_numeric.notna().any():
            hl_diff = (high_numeric - low_numeric).abs()
            # Replace 0 with NaN before finding the minimum non-zero difference
            min_hl_diff = hl_diff.replace(0, np.nan).min()
        else:
             logger.print_warning("[Warning] Could not calculate H-L difference due to non-numeric data.")


    if pd.notna(min_hl_diff) and min_hl_diff > 1e-12: # Check > 0 with tolerance
        logger.print_debug(f"[Debug] Minimum non-zero H-L difference: {min_hl_diff:.8f}")
        # 3. Estimate based on order of magnitude of min H-L difference
        log_diff = np.log10(min_hl_diff)
        # Estimate point size as 10^(floor(log10(min_diff)) - 1), ensuring reasonable bounds
        # Example: min_diff=0.00015 -> log=-3.8 -> floor=-4 -> point=10^-5
        # Example: min_diff=0.05    -> log=-1.3 -> floor=-2 -> point=10^-3 (adjust to 0.01)
        # Example: min_diff=0.5     -> log=-0.3 -> floor=-1 -> point=10^-2 (adjust to 0.1 or 0.01?)

        # Heuristic adjustment based on typical market conventions
        if log_diff < -2.5: # Likely Forex or similar high precision (e.g., < 0.003)
            estimated_point = 10**(np.floor(log_diff) - 1)
            estimated_point = max(0.000001, estimated_point) # Ensure minimum
            logger.print_info(f"[Info] Low H-L diff suggests high precision, estimating point size: {estimated_point:.8f}")
            # Refine for common 5-decimal Forex
            if -6 < log_diff < -3.5: estimated_point=0.00001

        elif log_diff < -0.5: # Likely stocks, indices, crypto (e.g., < 0.3)
            estimated_point = 0.01
            logger.print_info(f"[Info] Moderate H-L diff suggests stock/index/crypto precision, estimating point size: {estimated_point:.2f}")
        else: # Larger differences
             estimated_point = 0.1 if log_diff < 1.5 else 1.0
             logger.print_info(f"[Info] Large H-L diff, estimating point size: {estimated_point:.1f}")

        # Safety check for extremely small values
        return max(estimated_point, 1e-8)


    # 4. Fallback / Default if estimation failed
    print("[Warning] Could not reliably estimate point size from H-L difference. Falling back to default: 0.01")
    return 0.01

# Example: If you move reverse_signal_value here from core_calculations.py
# from .constants import BUY, SELL # Use relative import within src
# def reverse_signal_value(signal):
#     """Reverses BUY to SELL and vice versa."""
#     # ... implementation ...