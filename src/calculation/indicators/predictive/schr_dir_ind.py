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
                             vpr_series: pd.Series, point: float, c_vpr: float,
                             grow_percent: float = 95.0, shift_external_internal: bool = False) -> tuple[pd.Series, pd.Series]:
    """
    Calculate direction lines (High and Low) according to MQL5 algorithm.
    
    Args:
        price_series (pd.Series): Base price series (Open price)
        diff_series (pd.Series): Price difference series
        vpr_series (pd.Series): VPR series
        point (float): Instrument point size
        c_vpr (float): VPR constant (0.5 * log(pi))
        grow_percent (float): Growth percentage (default 95%)
        shift_external_internal (bool): External/Internal mode (default False)
    
    Returns:
        tuple: (dir_high_series, dir_low_series)
    """
    # Calculate grow factor based on MQL5 logic
    if not shift_external_internal:
        grow_factor = grow_percent / 100.0  # Internal mode
    else:
        grow_factor = (100.0 + grow_percent) / 100.0  # External mode
    
    # Calculate components according to MQL5 formulas
    diff_component = diff_series * c_vpr * point
    vpr_component = np.power(c_vpr, 3) * vpr_series * point
    
    # Calculate direction lines using exact MQL5 formulas
    # Dir High = price + ((diff * C_VPR * point) - (C_VPR^3 * vpr * point)) * grow_factor
    # Dir Low = price - ((diff * C_VPR * point) + (C_VPR^3 * vpr * point)) * grow_factor
    dir_high = price_series + (diff_component - vpr_component) * grow_factor
    dir_low = price_series - (diff_component + vpr_component) * grow_factor
    
    return dir_high, dir_low


def calculate_schr_dir_lines(dir_high: pd.Series, dir_low: pd.Series, 
                            high_prices: pd.Series, low_prices: pd.Series,
                            strong_exceed: bool = True) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Calculate SCHR Direction lines with proper High and Low line logic.
    
    Args:
        dir_high (pd.Series): Calculated direction high values
        dir_low (pd.Series): Calculated direction low values
        high_prices (pd.Series): Actual high prices
        low_prices (pd.Series): Actual low prices
        strong_exceed (bool): Strong exceed mode (default True)
    
    Returns:
        tuple: (high_line, high_color, low_line, low_color)
    """
    high_line = pd.Series(index=dir_high.index, dtype=float)
    high_color = pd.Series(index=dir_high.index, dtype=int)
    low_line = pd.Series(index=dir_low.index, dtype=float)
    low_color = pd.Series(index=dir_low.index, dtype=int)
    
    # Initialize previous values
    prev_high = None
    prev_low = None
    
    for i in range(len(dir_high)):
        current_dir_high = dir_high.iloc[i]
        current_dir_low = dir_low.iloc[i]
        current_high = high_prices.iloc[i]
        current_low = low_prices.iloc[i]
        
        # Skip if values are NaN
        if pd.isna(current_dir_high) or pd.isna(current_dir_low):
            high_line.iloc[i] = np.nan
            high_color.iloc[i] = NOTRADE
            low_line.iloc[i] = np.nan
            low_color.iloc[i] = NOTRADE
            continue
            
        # Initialize previous values on first valid iteration
        if prev_high is None:
            prev_high = current_dir_high
            prev_low = current_dir_low
            high_line.iloc[i] = current_dir_high
            high_color.iloc[i] = SELL
            low_line.iloc[i] = current_dir_low
            low_color.iloc[i] = BUY
            continue
        
        # High line logic according to MQL5
        if strong_exceed:
            # Strong exceed mode: must exceed both previous high and current high
            if current_dir_high > prev_high and current_dir_high > current_high:
                prev_high = current_dir_high
                high_line.iloc[i] = current_dir_high
                high_color.iloc[i] = SELL
            else:
                high_line.iloc[i] = prev_high
                high_color.iloc[i] = SELL
        else:
            # Weak exceed mode: only need to exceed previous high
            if current_dir_high > prev_high:
                prev_high = current_dir_high
                high_line.iloc[i] = current_dir_high
                high_color.iloc[i] = SELL
            else:
                high_line.iloc[i] = prev_high
                high_color.iloc[i] = SELL
        
        # Low line logic according to MQL5
        if strong_exceed:
            # Strong exceed mode: must be below both previous low and current low
            if current_dir_low < prev_low and current_dir_low < current_low:
                prev_low = current_dir_low
                low_line.iloc[i] = current_dir_low
                low_color.iloc[i] = BUY
            else:
                low_line.iloc[i] = prev_low
                low_color.iloc[i] = BUY
        else:
            # Weak exceed mode: only need to be below previous low
            if current_dir_low < prev_low:
                prev_low = current_dir_low
                low_line.iloc[i] = current_dir_low
                low_color.iloc[i] = BUY
            else:
                low_line.iloc[i] = prev_low
                low_color.iloc[i] = BUY
    
    return high_line, high_color, low_line, low_color


def calculate_schr_dir_signals(high_line: pd.Series, low_line: pd.Series, 
                              open_prices: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on SCHR Direction lines.
    
    Trading Rule:
    - BUY if open price higher than both (high and low) lines
    - SELL if open price lower than both (high and low) lines
    - NOTRADE otherwise
    
    Args:
        high_line (pd.Series): High line values
        low_line (pd.Series): Low line values
        open_prices (pd.Series): Open prices
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=high_line.index)
    
    for i in range(len(high_line)):
        if pd.isna(high_line.iloc[i]) or pd.isna(low_line.iloc[i]):
            continue
            
        open_price = open_prices.iloc[i]
        high_val = high_line.iloc[i]
        low_val = low_line.iloc[i]
        
        # BUY signal: open price higher than both lines
        if open_price > high_val and open_price > low_val:
            signals.iloc[i] = BUY
        # SELL signal: open price lower than both lines
        elif open_price < high_val and open_price < low_val:
            signals.iloc[i] = SELL
        # NOTRADE: open price between the lines
    
    return signals


def apply_rule_schr_dir(df: pd.DataFrame, point: float,
                        price_type: PriceType = PriceType.CLOSE,
                        grow_percent: float = 1.0) -> pd.DataFrame:
    """
    Applies SCHR Direction rule logic with configurable grow percentage.
    
    Parameters:
    - grow_percent: Growth percentage for line calculation (1-95, default 1)
    - shift_external_internal = False (internal mode)
    - fixed_price = True (always use Open price)
    - fake_line = False (always use previous bar data)
    - strong_exceed = True (always strong exceed mode)
    - lines_count = BothLines (always show both lines)
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        price_type (PriceType): Price type for calculation (ignored, always uses Open)
        grow_percent (float): Growth percentage (1-95, default 1)
    
    Returns:
        pd.DataFrame: DataFrame with SCHR Direction calculations and signals
    """
    # Validate grow_percent parameter
    if not (1.0 <= grow_percent <= 95.0):
        raise ValueError(f"grow_percent must be between 1.0 and 95.0, got: {grow_percent}")
    
    # Fixed parameters - always use Open price
    base_price_series = df['Open']
    price_name = "Open"
    
    # Fixed parameters - always use previous bar data (fake_line = False)
    high_prices = df['High'].shift(1)
    low_prices = df['Low'].shift(1)
    volume_prices = df['Volume'].shift(1)
    
    # VPR constant (0.5 * log(pi))
    c_vpr = 0.5 * np.log(np.pi)
    
    # Calculate VPR and difference
    diff_series, vpr_series = calculate_vpr(high_prices, low_prices, volume_prices, point)
    
    # Calculate direction lines with configurable grow percentage
    dir_high, dir_low = calculate_direction_lines(
        base_price_series, diff_series, vpr_series, point, c_vpr,
        grow_percent=grow_percent, shift_external_internal=False
    )
    
    # Calculate SCHR Direction lines with proper High and Low logic
    high_line, high_color, low_line, low_color = calculate_schr_dir_lines(
        dir_high, dir_low, high_prices, low_prices, strong_exceed=True
    )
    
    # Calculate trading signals
    signals = calculate_schr_dir_signals(high_line, low_line, base_price_series)
    
    # Create a copy to avoid SettingWithCopyWarning
    result_df = df.copy()
    
    # Set main output columns - two separate lines for dual chart
    result_df['PPrice1'] = high_line  # High line
    result_df['PPrice2'] = low_line   # Low line
    result_df['PColor1'] = high_color  # High line color
    result_df['PColor2'] = low_color   # Low line color
    result_df['Direction'] = signals
    
    # Additional SCHR_DIR specific columns with configurable values
    result_df['SCHR_DIR_Diff'] = diff_series
    result_df['SCHR_DIR_VPR'] = vpr_series
    result_df['SCHR_DIR_Price_Type'] = price_name
    result_df['SCHR_DIR_Grow_Percent'] = grow_percent  # Configurable value
    result_df['SCHR_DIR_Strong_Exceed'] = True  # Fixed value
    result_df['SCHR_DIR_Shift_External_Internal'] = False  # Fixed value
    
    return result_df
