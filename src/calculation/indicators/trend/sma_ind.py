# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/sma_ind.py

"""
INDICATOR INFO:
Name: SMA
Category: Trend
Description: Simple Moving Average. A type of moving average that gives equal weight to all prices in the calculation period.
Usage: --rule sma:20,close or --rule sma:20,open
Parameters: period, price_type
Pros: + Simple and easy to understand, + Smooths out price noise, + Good for trend identification
Cons: - Can lag behind price changes, - May give false signals in volatile markets, - Equal weight may not reflect recent market conditions

SMA (Simple Moving Average) indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_sma(price_series: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculates the Simple Moving Average (SMA).
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        period (int): SMA calculation period (default: 20)
    
    Returns:
        pd.Series: SMA values
    """
    if period <= 0:
        raise ValueError("SMA period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"Not enough data for SMA calculation. Need at least {period} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate SMA using pandas rolling mean
    sma = price_series.rolling(window=period, min_periods=period).mean()
    
    return sma


def calculate_sma_signals(price_series: pd.Series, sma_values: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on price vs SMA.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        sma_values (pd.Series): SMA values
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price crosses above SMA
    buy_condition = (price_series > sma_values) & (price_series.shift(1) <= sma_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Price crosses below SMA
    sell_condition = (price_series < sma_values) & (price_series.shift(1) >= sma_values.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_sma(df: pd.DataFrame, point: float, 
                   sma_period: int = 20, price_type: PriceType = PriceType.CLOSE):
    """
    Applies SMA rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        sma_period (int): SMA calculation period
        price_type (PriceType): Price type to use for SMA calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with SMA calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate SMA
    df['SMA'] = calculate_sma(price_series, sma_period)
    
    # Add price type info to column name
    df['SMA_Price_Type'] = price_name
    
    # Calculate SMA signals
    df['SMA_Signal'] = calculate_sma_signals(price_series, df['SMA'])
    
    # Calculate support and resistance levels based on SMA
    # Use SMA as dynamic support/resistance
    sma_values = df['SMA']
    
    # Support level: SMA with small buffer
    support_levels = sma_values * 0.995  # 0.5% below SMA
    
    # Resistance level: SMA with small buffer
    resistance_levels = sma_values * 1.005  # 0.5% above SMA
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['SMA_Signal']
    df['Diff'] = price_series - sma_values  # Use price - SMA as difference indicator
    
    return df
