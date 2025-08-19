# -*- coding: utf-8 -*-
# src/calculation/indicators/volatility/atr_ind.py

"""
INDICATOR INFO:
Name: ATR
Category: Volatility
Description: Average True Range. Measures market volatility by decomposing the entire range of an asset price for that period.
Usage: --rule atr(14) or --rule atr(14,close)
Parameters: period, price_type
Pros: + Measures true volatility, + Works in any market, + Good for stop loss placement
Cons: - Lagging indicator, - May not work well in low volatility, - Requires careful interpretation
File: src/calculation/indicators/volatility/atr_ind.py

ATR (Average True Range) indicator calculation module.
"""

import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
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


def calculate_atr_signals(atr_values: pd.Series, atr_prev: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on ATR changes.
    
    Args:
        atr_values (pd.Series): Current ATR values
        atr_prev (pd.Series): Previous ATR values
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=atr_values.index)
    
    # BUY signal: ATR increasing (volatility expanding)
    buy_condition = (atr_values > atr_prev) & (atr_values > atr_values.rolling(window=20).mean())
    signals[buy_condition] = BUY
    
    # SELL signal: ATR decreasing (volatility contracting)
    sell_condition = (atr_values < atr_prev) & (atr_values < atr_values.rolling(window=20).mean())
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_atr(df: pd.DataFrame, point: float, 
                   atr_period: int = 14, price_type: PriceType = PriceType.CLOSE):
    """
    Applies ATR rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        atr_period (int): ATR calculation period
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with ATR calculations and signals
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
    
    # Calculate ATR signals
    df['ATR_Signal'] = calculate_atr_signals(df['ATR'], df['ATR'].shift(1))
    
    # Calculate support and resistance levels based on ATR
    # Use ATR to set dynamic support/resistance levels
    atr_values = df['ATR']
    
    # Support level: Open price minus ATR
    support_levels = open_prices - atr_values
    
    # Resistance level: Open price plus ATR
    resistance_levels = open_prices + atr_values
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['ATR_Signal']
    df['Diff'] = df['ATR']  # Use ATR value as difference indicator
    
    return df
