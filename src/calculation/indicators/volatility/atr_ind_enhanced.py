# -*- coding: utf-8 -*-
# src/calculation/indicators/volatility/atr_ind_enhanced.py

"""
INDICATOR INFO:
Name: ATR Enhanced
Category: Volatility
Description: Enhanced Average True Range with period-sensitive signal generation.
Usage: --rule atr:period or --rule atr:period,price_type
Parameters: period, price_type
Pros: + Measures true volatility, + Period-sensitive signals, + Better signal differentiation
Cons: - Lagging indicator, - May not work well in low volatility, - Requires careful interpretation
File: src/calculation/indicators/volatility/atr_ind_enhanced.py

Enhanced ATR (Average True Range) indicator calculation module with improved signal generation.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_true_range(df: pd.DataFrame) -> pd.Series:
    """
    Calculates True Range for ATR calculation.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
    
    Returns:
        pd.Series: True Range values
    """
    high = df['High']
    low = df['Low']
    close_prev = df['Close'].shift(1)
    
    # True Range is the greatest of:
    # 1. Current High - Current Low
    # 2. |Current High - Previous Close|
    # 3. |Current Low - Previous Close|
    
    tr1 = high - low
    tr2 = np.abs(high - close_prev)
    tr3 = np.abs(low - close_prev)
    
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    return true_range


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculates the Average True Range (ATR).
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        period (int): ATR calculation period (default: 14)
    
    Returns:
        pd.Series: ATR values
    """
    if period <= 0:
        raise ValueError("ATR period must be positive")
    
    if len(df) < period + 1:
        logger.print_warning(f"Not enough data for ATR calculation. Need at least {period + 1} points, got {len(df)}")
        return pd.Series(index=df.index, dtype=float)
    
    # Calculate True Range
    true_range = calculate_true_range(df)
    
    # Calculate ATR using exponential moving average
    atr = true_range.ewm(span=period, adjust=False).mean()
    
    return atr


def calculate_atr_signals_enhanced(atr_values: pd.Series, atr_period: int) -> pd.Series:
    """
    Calculate enhanced trading signals based on ATR with period-sensitive logic.
    
    Args:
        atr_values (pd.Series): Current ATR values
        atr_period (int): ATR period used for calculation
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=atr_values.index)
    
    # Calculate dynamic thresholds based on ATR period
    # Shorter periods = more sensitive, longer periods = less sensitive
    sensitivity_factor = max(1, 20 / atr_period)  # Higher for shorter periods
    
    # Calculate rolling statistics with period-dependent windows
    short_window = max(5, atr_period // 3)
    long_window = max(20, atr_period * 2)
    
    atr_short_ma = atr_values.rolling(window=short_window).mean()
    atr_long_ma = atr_values.rolling(window=long_window).mean()
    atr_std = atr_values.rolling(window=atr_period).std()
    
    # Calculate ATR change rate
    atr_change = atr_values.pct_change()
    atr_change_ma = atr_change.rolling(window=short_window).mean()
    
    # Enhanced BUY signals with period sensitivity
    buy_conditions = [
        # ATR increasing above short-term average
        (atr_values > atr_short_ma * (1 + 0.1 * sensitivity_factor)),
        # ATR change rate is positive
        (atr_change_ma > 0),
        # ATR is above long-term average
        (atr_values > atr_long_ma),
        # Volatility is expanding
        (atr_values > atr_values.shift(1))
    ]
    
    # Enhanced SELL signals with period sensitivity
    sell_conditions = [
        # ATR decreasing below short-term average
        (atr_values < atr_short_ma * (1 - 0.1 * sensitivity_factor)),
        # ATR change rate is negative
        (atr_change_ma < 0),
        # ATR is below long-term average
        (atr_values < atr_long_ma),
        # Volatility is contracting
        (atr_values < atr_values.shift(1))
    ]
    
    # Apply conditions with different weights based on period
    if atr_period <= 20:
        # Short period: more sensitive to immediate changes
        buy_signal = sum(buy_conditions) >= 2  # Need at least 2 conditions
        sell_signal = sum(sell_conditions) >= 2
    elif atr_period <= 50:
        # Medium period: balanced sensitivity
        buy_signal = sum(buy_conditions) >= 3  # Need at least 3 conditions
        sell_signal = sum(sell_conditions) >= 3
    else:
        # Long period: less sensitive, more conservative
        buy_signal = sum(buy_conditions) >= 4  # Need all conditions
        sell_signal = sum(sell_conditions) >= 4
    
    # Apply signals
    signals[buy_signal] = BUY
    signals[sell_signal] = SELL
    
    return signals


def apply_rule_atr_enhanced(df: pd.DataFrame, point: float, 
                           atr_period: int = 14, price_type: PriceType = PriceType.CLOSE):
    """
    Applies enhanced ATR rule logic with period-sensitive signal generation.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        atr_period (int): ATR calculation period
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with enhanced ATR calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate ATR
    df['ATR'] = calculate_atr(df, atr_period)
    
    # Add price type info to column name
    df['ATR_Price_Type'] = price_name
    
    # Calculate enhanced ATR signals with period sensitivity
    df['ATR_Signal'] = calculate_atr_signals_enhanced(df['ATR'], atr_period)
    
    # Calculate support and resistance levels based on ATR
    # Use ATR to set dynamic support/resistance levels
    atr_values = df['ATR']
    
    # Support level: Open price minus ATR (adjusted by period sensitivity)
    sensitivity_factor = max(1, 20 / atr_period)
    support_levels = open_prices - (atr_values * sensitivity_factor)
    
    # Resistance level: Open price plus ATR (adjusted by period sensitivity)
    resistance_levels = open_prices + (atr_values * sensitivity_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['ATR_Signal']
    df['Diff'] = df['ATR']  # Use ATR value as difference indicator
    
    return df 