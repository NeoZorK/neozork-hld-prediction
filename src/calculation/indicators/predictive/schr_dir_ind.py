# -*- coding: utf-8 -*-
# src/calculation/indicators/predictive/schr_dir_ind.py

"""
INDICATOR INFO:
Name: SCHR Direction (SCHR_DIR)
Category: Predictive
Description: Fastest Direction Showing of High and Low. Predicts price direction based on Volume Price Ratio (VPR).
Usage: --rule SCHR_DIR or --rule SCHR_DIR:95,true,true,true,2
Parameters: grow_percent, shift_external_internal, fixed_price, fake_line, strong_exceed, lines_count
Pros: + Fast direction prediction, + Volume-based analysis, + Multiple line types, + Configurable parameters
Cons: - Complex calculation, - Sensitive to parameter choice, - Requires volume data
File: src/calculation/indicators/predictive/schr_dir_ind.py

SCHR Direction indicator calculation module.
Based on MQL5 SCHR_DIR.mq5 indicator by Shcherbyna Rostyslav.
"""

import pandas as pd
import numpy as np
from typing import Optional, Union
from enum import Enum
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


class GrowPercent(Enum):
    """Enum for grow percentage values."""
    P_99 = 99
    P_95 = 95
    P_90 = 90
    P_80 = 80
    P_70 = 70
    P_60 = 60
    P_50 = 50
    P_40 = 40
    P_30 = 30
    P_20 = 20
    P_10 = 10
    P_5 = 5
    P_1 = 1


class LinesCount(Enum):
    """Enum for lines count types."""
    UPPER_LINE = 0
    LOWER_LINE = 1
    BOTH_LINES = 2


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
                             vpr_series: pd.Series, point: float, grow_percent: int,
                             shift_external_internal: bool, c_vpr: float) -> tuple[pd.Series, pd.Series]:
    """
    Calculate direction lines (High and Low).
    
    Args:
        price_series (pd.Series): Base price series (Open or Close)
        diff_series (pd.Series): Price difference series
        vpr_series (pd.Series): VPR series
        point (float): Instrument point size
        grow_percent (int): Growth percentage (1-99)
        shift_external_internal (bool): External/Internal shift mode
        c_vpr (float): VPR constant (0.5 * log(pi))
    
    Returns:
        tuple: (dir_high_series, dir_low_series)
    """
    # Calculate grow factor
    if shift_external_internal:
        grow_factor = (100 + grow_percent) / 100
    else:
        grow_factor = grow_percent / 100
    
    # Calculate direction components
    diff_term = diff_series * c_vpr * point
    vpr_term = np.power(c_vpr, 3) * vpr_series * point
    
    # Calculate direction lines
    dir_high = price_series + ((diff_term - vpr_term) * grow_factor)
    dir_low = price_series - ((diff_term + vpr_term) * grow_factor)
    
    return dir_high, dir_low


def calculate_schr_dir_signals(dir_high: pd.Series, dir_low: pd.Series, 
                              high_prices: pd.Series, low_prices: pd.Series,
                              strong_exceed: bool) -> pd.Series:
    """
    Calculate trading signals based on direction lines.
    
    Args:
        dir_high (pd.Series): Direction high values
        dir_low (pd.Series): Direction low values
        high_prices (pd.Series): Actual high prices
        low_prices (pd.Series): Actual low prices
        strong_exceed (bool): Strong exceed mode
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=dir_high.index)
    
    # Initialize previous values
    prev_high = dir_high.iloc[0] if not dir_high.empty else 0
    prev_low = dir_low.iloc[0] if not dir_low.empty else 0
    
    for i in range(1, len(dir_high)):
        current_dir_high = dir_high.iloc[i]
        current_dir_low = dir_low.iloc[i]
        current_high = high_prices.iloc[i]
        current_low = low_prices.iloc[i]
        
        # High line logic
        if strong_exceed:
            if current_dir_high > prev_high and current_dir_high > current_high:
                prev_high = current_dir_high
                signals.iloc[i] = SELL
            else:
                signals.iloc[i] = SELL
        else:
            if current_dir_high > prev_high:
                prev_high = current_dir_high
                signals.iloc[i] = SELL
            else:
                signals.iloc[i] = SELL
        
        # Low line logic
        if strong_exceed:
            if current_dir_low < prev_low and current_dir_low < current_low:
                prev_low = current_dir_low
                signals.iloc[i] = BUY
            else:
                signals.iloc[i] = BUY
        else:
            if current_dir_low < prev_low:
                prev_low = current_dir_low
                signals.iloc[i] = BUY
            else:
                signals.iloc[i] = BUY
    
    return signals


def apply_rule_schr_dir(df: pd.DataFrame, point: float,
                        grow_percent: int = 95,
                        shift_external_internal: bool = False,
                        fixed_price: bool = True,
                        fake_line: bool = False,
                        strong_exceed: bool = True,
                        lines_count: LinesCount = LinesCount.BOTH_LINES,
                        price_type: PriceType = PriceType.CLOSE) -> pd.DataFrame:
    """
    Applies SCHR Direction rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        grow_percent (int): Growth percentage (1-99, default: 95)
        shift_external_internal (bool): External/Internal shift mode (default: False)
        fixed_price (bool): Use fixed price (Open) vs Close price (default: True)
        fake_line (bool): Use current HL vs previous HL (default: False)
        strong_exceed (bool): Strong exceed mode (default: True)
        lines_count (LinesCount): Lines count type (default: BOTH_LINES)
        price_type (PriceType): Price type for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with SCHR Direction calculations and signals
    """
    # Validate grow_percent
    if not 1 <= grow_percent <= 99:
        raise ValueError("grow_percent must be between 1 and 99")
    
    # Select price series based on fixed_price and price_type
    if fixed_price:
        base_price_series = df['Open']
        price_name = "Open"
    else:
        if price_type == PriceType.OPEN:
            base_price_series = df['Open']
            price_name = "Open"
        else:
            base_price_series = df['Close']
            price_name = "Close"
    
    # Select data based on fake_line
    if fake_line:
        # Use current bar data
        high_prices = df['High']
        low_prices = df['Low']
        volume_prices = df['Volume']
    else:
        # Use previous bar data (shifted)
        high_prices = df['High'].shift(1)
        low_prices = df['Low'].shift(1)
        volume_prices = df['Volume'].shift(1)
    
    # VPR constant (0.5 * log(pi))
    c_vpr = 0.5 * np.log(np.pi)
    
    # Calculate VPR and difference
    diff_series, vpr_series = calculate_vpr(high_prices, low_prices, volume_prices, point)
    
    # Calculate direction lines
    dir_high, dir_low = calculate_direction_lines(
        base_price_series, diff_series, vpr_series, point, 
        grow_percent, shift_external_internal, c_vpr
    )
    
    # Calculate trading signals
    signals = calculate_schr_dir_signals(
        dir_high, dir_low, high_prices, low_prices, strong_exceed
    )
    
    # Create a copy to avoid SettingWithCopyWarning
    result_df = df.copy()
    
    # Set output columns based on lines_count
    if lines_count in [LinesCount.BOTH_LINES, LinesCount.UPPER_LINE]:
        result_df['SCHR_DIR_High'] = dir_high
        result_df['SCHR_DIR_High_Color'] = SELL
    else:
        result_df['SCHR_DIR_High'] = EMPTY_VALUE
        result_df['SCHR_DIR_High_Color'] = EMPTY_VALUE
    
    if lines_count in [LinesCount.BOTH_LINES, LinesCount.LOWER_LINE]:
        result_df['SCHR_DIR_Low'] = dir_low
        result_df['SCHR_DIR_Low_Color'] = BUY
    else:
        result_df['SCHR_DIR_Low'] = EMPTY_VALUE
        result_df['SCHR_DIR_Low_Color'] = EMPTY_VALUE
    
    # Set main output columns
    result_df['PPrice1'] = dir_low  # Support level (Low line)
    result_df['PColor1'] = BUY
    result_df['PPrice2'] = dir_high  # Resistance level (High line)
    result_df['PColor2'] = SELL
    result_df['Direction'] = signals
    
    # Additional SCHR_DIR specific columns
    result_df['SCHR_DIR_Diff'] = diff_series
    result_df['SCHR_DIR_VPR'] = vpr_series
    result_df['SCHR_DIR_Price_Type'] = price_name
    result_df['SCHR_DIR_Grow_Percent'] = grow_percent
    result_df['SCHR_DIR_Strong_Exceed'] = strong_exceed
    
    return result_df
