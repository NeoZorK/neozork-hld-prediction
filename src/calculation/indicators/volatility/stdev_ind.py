# -*- coding: utf-8 -*-
# src/calculation/indicators/volatility/stdev_ind.py

"""
INDICATOR INFO:
Name: Standard Deviation
Category: Volatility
Description: Standard Deviation. Measures price volatility using statistical standard deviation.
Usage: --rule stdev(20) or --rule stdev(20,close)
Parameters: period, price_type
Pros: + Measures true volatility, + Based on statistics, + Good for risk assessment
Cons: - Assumes normal distribution, - May not capture extreme events, - Sensitive to period choice
File: src/calculation/indicators/volatility/stdev_ind.py

Standard Deviation indicator calculation module.
"""

import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_stdev(price_series: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculates Standard Deviation of price changes.
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        period (int): Calculation period (default: 20)
    
    Returns:
        pd.Series: Standard Deviation values
    """
    if period <= 0:
        raise ValueError("Standard Deviation period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"Not enough data for Standard Deviation calculation. Need at least {period} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate price changes
    price_changes = price_series.pct_change().dropna()
    
    if len(price_changes) < period:
        logger.print_warning("Not enough price change data for Standard Deviation calculation")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate rolling standard deviation
    stdev_values = price_changes.rolling(window=period).std()
    
    return stdev_values


def calculate_stdev_signals(stdev_values: pd.Series, price_series: pd.Series,
                           high_volatility_threshold: float = 0.02, low_volatility_threshold: float = 0.005) -> pd.Series:
    """
    Calculate trading signals based on Standard Deviation volatility levels.
    
    Args:
        stdev_values (pd.Series): Standard Deviation values
        price_series (pd.Series): Price series (Open or Close)
        high_volatility_threshold (float): High volatility threshold (default: 0.02)
        low_volatility_threshold (float): Low volatility threshold (default: 0.005)
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=stdev_values.index)
    
    # Calculate price momentum
    price_momentum = price_series.pct_change()
    
    # BUY signal: Low volatility and positive momentum (breakout potential)
    buy_condition = (stdev_values < low_volatility_threshold) & (price_momentum > 0) & (price_momentum > price_momentum.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: High volatility and negative momentum (panic selling)
    sell_condition = (stdev_values > high_volatility_threshold) & (price_momentum < 0) & (price_momentum < price_momentum.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_stdev(df: pd.DataFrame, point: float, 
                     stdev_period: int = 20, high_volatility_threshold: float = 0.02, low_volatility_threshold: float = 0.005,
                     price_type: PriceType = PriceType.CLOSE):
    """
    Applies Standard Deviation rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        stdev_period (int): Standard Deviation period
        high_volatility_threshold (float): High volatility threshold
        low_volatility_threshold (float): Low volatility threshold
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with Standard Deviation calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate Standard Deviation
    df['StDev'] = calculate_stdev(price_series, stdev_period)
    
    # Add price type info to column name
    df['StDev_Price_Type'] = price_name
    
    # Calculate Standard Deviation signals
    df['StDev_Signal'] = calculate_stdev_signals(df['StDev'], price_series, high_volatility_threshold, low_volatility_threshold)
    
    # Calculate support and resistance levels based on Standard Deviation
    stdev_values = df['StDev']
    
    # Use Standard Deviation directly as volatility factor
    volatility_factor = stdev_values * 2  # Scale the standard deviation
    
    # Support level: Open price minus volatility
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level: Open price plus volatility
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['StDev_Signal']
    df['Diff'] = stdev_values  # Use Standard Deviation as difference indicator
    
    return df
