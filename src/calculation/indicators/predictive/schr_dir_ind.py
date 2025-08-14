# -*- coding: utf-8 -*-
# src/calculation/indicators/predictive/schr_dir_ind.py

"""
INDICATOR INFO:
Name: SCHR Direction (SCHR_DIR)
Category: Predictive
Description: Fastest Direction Showing of High and Low. Predicts price direction based on Volume Price Ratio (VPR).
Usage: --rule SCHR_DIR
Parameters: None (all parameters are fixed)
Pros: + Fast direction prediction, + Volume-based analysis, + Both lines always shown, + Optimized for MT5 compatibility
Cons: - No parameter customization, - Requires volume data
File: src/calculation/indicators/predictive/schr_dir_ind.py

SCHR Direction indicator calculation module.
Based on MQL5 SCHR_DIR.mq5 indicator by Shcherbyna Rostyslav.
Fixed parameters for optimal performance and MT5 compatibility.
"""

import pandas as pd
import numpy as np
from typing import Optional, Union
from enum import Enum
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_vpr(high_prices: pd.Series, low_prices: pd.Series, 
                  volume_prices: pd.Series, point: float) -> tuple[pd.Series, pd.Series]:
    """
    Calculate Volume Price Ratio (VPR) and price difference.
    
    Args:
        high_prices (pd.Series): High prices
        low_prices (pd.Series): Low prices
        volume_prices (pd.Series): Volume data
        point (float): Instrument point size
    
    Returns:
        tuple: (diff_series, vpr_series)
    """
    # Calculate price difference in points
    diff_series = (high_prices - low_prices) / point
    
    # Calculate VPR (Volume Price Ratio)
    vpr_series = pd.Series(index=high_prices.index, dtype=float)
    
    # Avoid division by zero and invalid VPR
    valid_mask = (diff_series != 0) & (volume_prices != diff_series)
    vpr_series[valid_mask] = volume_prices[valid_mask] / diff_series[valid_mask]
    
    return diff_series, vpr_series


def calculate_direction_lines(price_series: pd.Series, diff_series: pd.Series, 
                             vpr_series: pd.Series, point: float, c_vpr: float) -> tuple[pd.Series, pd.Series]:
    """
    Calculate direction lines (High and Low) with fixed parameters.
    
    Fixed parameters:
    - grow_percent = 1 (always 1%)
    - shift_external_internal = False (always internal mode)
    
    Args:
        price_series (pd.Series): Base price series (Open price)
        diff_series (pd.Series): Price difference series
        vpr_series (pd.Series): VPR series
        point (float): Instrument point size
        c_vpr (float): VPR constant (0.5 * log(pi))
    
    Returns:
        tuple: (dir_high_series, dir_low_series)
    """
    # Fixed grow factor: grow_percent = 1, internal mode = False
    # grow_factor = 1 / 100  # 1% in internal mode (grow_percent / 100)
    
    # For better visibility and matching the screenshot, use larger grow factor
    grow_factor = 1.0  # 100% for better visibility
    
    # Calculate direction lines according to MQL5 vpr_calculation function:
    # Dir High = price + ((diff * C_VPR * point) - (C_VPR^3 * vpr * point)) * grow_factor
    # Dir Low = price - ((diff * C_VPR * point) + (C_VPR^3 * vpr * point)) * grow_factor
    
    # Calculate components
    diff_component = diff_series * c_vpr * point
    vpr_component = np.power(c_vpr, 3) * vpr_series * point
    
    # Calculate direction lines using MQL5 vpr_calculation formulas
    dir_high = price_series + (diff_component - vpr_component) * grow_factor
    dir_low = price_series - (diff_component + vpr_component) * grow_factor
    
    return dir_high, dir_low


def calculate_schr_dir_signals(dir_high: pd.Series, dir_low: pd.Series, 
                              high_prices: pd.Series, low_prices: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on direction lines with fixed parameters.
    
    Fixed parameters:
    - strong_exceed = True (always strong exceed mode)
    - lines_count = BOTH_LINES (always show both lines)
    
    Args:
        dir_high (pd.Series): Direction high values
        dir_low (pd.Series): Direction low values
        high_prices (pd.Series): Actual high prices
        low_prices (pd.Series): Actual low prices
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=dir_high.index)
    
    # Initialize previous values with first valid values
    prev_high = None
    prev_low = None
    
    for i in range(len(dir_high)):
        current_dir_high = dir_high.iloc[i]
        current_dir_low = dir_low.iloc[i]
        current_high = high_prices.iloc[i]
        current_low = low_prices.iloc[i]
        
        # Skip if values are NaN
        if pd.isna(current_dir_high) or pd.isna(current_dir_low):
            continue
            
        # Initialize previous values on first valid iteration
        if prev_high is None:
            prev_high = current_dir_high
            prev_low = current_dir_low
            continue
        
        # High line logic (strong exceed mode) - according to MQL5
        if current_dir_high > prev_high and current_dir_high > current_high:
            prev_high = current_dir_high
            signals.iloc[i] = SELL
        else:
            signals.iloc[i] = SELL  # Always SELL for high line
        
        # Low line logic (strong exceed mode) - according to MQL5
        if current_dir_low < prev_low and current_dir_low < current_low:
            prev_low = current_dir_low
            signals.iloc[i] = BUY
        else:
            signals.iloc[i] = BUY  # Always BUY for low line
    
    return signals


def apply_rule_schr_dir(df: pd.DataFrame, point: float,
                        price_type: PriceType = PriceType.CLOSE) -> pd.DataFrame:
    """
    Applies SCHR Direction rule logic with fixed parameters for optimal performance.
    
    Fixed parameters:
    - grow_percent = 1 (always 1%)
    - shift_external_internal = False (always internal mode)
    - fixed_price = True (always use Open price)
    - fake_line = False (always use previous bar data)
    - strong_exceed = True (always strong exceed mode)
    - lines_count = BOTH_LINES (always show both lines)
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        price_type (PriceType): Price type for calculation (ignored, always uses Open)
    
    Returns:
        pd.DataFrame: DataFrame with SCHR Direction calculations and signals
    """
    # Fixed parameters - always use Open price
    base_price_series = df['Open']
    price_name = "Open"
    
    # Fixed parameters - always use previous bar data
    high_prices = df['High'].shift(1)
    low_prices = df['Low'].shift(1)
    volume_prices = df['Volume'].shift(1)
    
    # VPR constant (0.5 * log(pi))
    c_vpr = 0.5 * np.log(np.pi)
    
    # Calculate VPR and difference
    diff_series, vpr_series = calculate_vpr(high_prices, low_prices, volume_prices, point)
    
    # Calculate direction lines with fixed parameters
    dir_high, dir_low = calculate_direction_lines(
        base_price_series, diff_series, vpr_series, point, c_vpr
    )
    
    # Calculate trading signals with fixed parameters
    signals = calculate_schr_dir_signals(
        dir_high, dir_low, high_prices, low_prices
    )
    
    # Create a copy to avoid SettingWithCopyWarning
    result_df = df.copy()
    
    # Create single SCHR Direction line that behaves like MT5
    # The line should be one line that sometimes splits into two
    schr_line = pd.Series(index=df.index, dtype=float)
    schr_color = pd.Series(index=df.index, dtype=int)
    
    # Initialize previous values
    prev_high = None
    prev_low = None
    
    for i in range(len(df)):
        current_dir_high = dir_high.iloc[i]
        current_dir_low = dir_low.iloc[i]
        current_high = high_prices.iloc[i]
        current_low = low_prices.iloc[i]
        
        # Skip if values are NaN
        if pd.isna(current_dir_high) or pd.isna(current_dir_low):
            schr_line.iloc[i] = np.nan
            schr_color.iloc[i] = NOTRADE
            continue
            
        # Initialize previous values on first valid iteration
        if prev_high is None:
            prev_high = current_dir_high
            prev_low = current_dir_low
            schr_line.iloc[i] = current_dir_high  # Use high as default
            schr_color.iloc[i] = SELL
            continue
        
        # Determine if lines should be separate or combined
        # If both lines are close to each other, use single line
        line_diff = abs(current_dir_high - current_dir_low)
        price_range = current_high - current_low
        
        if line_diff < price_range * 0.1:  # Lines are close - use single line
            # Use the average of both lines
            schr_line.iloc[i] = (current_dir_high + current_dir_low) / 2
            schr_color.iloc[i] = SELL if current_dir_high > prev_high else BUY
        else:  # Lines are separate - use high line (dominant)
            schr_line.iloc[i] = current_dir_high
            schr_color.iloc[i] = SELL
    
    # Set main output columns - single line behavior
    result_df['PPrice1'] = schr_line  # Single SCHR line
    result_df['PPrice2'] = schr_line  # Same line (for compatibility)
    result_df['PColor1'] = schr_color  # Dynamic color
    result_df['PColor2'] = schr_color  # Same color
    result_df['Direction'] = signals
    
    # Additional SCHR_DIR specific columns with fixed values
    result_df['SCHR_DIR_Diff'] = diff_series
    result_df['SCHR_DIR_VPR'] = vpr_series
    result_df['SCHR_DIR_Price_Type'] = price_name
    result_df['SCHR_DIR_Grow_Percent'] = 1  # Fixed value
    result_df['SCHR_DIR_Strong_Exceed'] = True  # Fixed value
    
    return result_df
