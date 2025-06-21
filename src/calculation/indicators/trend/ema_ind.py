# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/ema_ind.py

"""
INDICATOR INFO:
Name: EMA
Category: Trend
Description: Exponential Moving Average. A type of moving average that gives more weight to recent prices.
Usage: --rule ema(20) or --rule ema(20,close)
Parameters: period, price_type
Pros: + Responds quickly to price changes, + Reduces lag compared to SMA, + Good for trend identification
Cons: - Can be more volatile, - May give false signals in choppy markets, - Sensitive to parameter choice

EMA (Exponential Moving Average) indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_ema(price_series: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculates the Exponential Moving Average (EMA).
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        period (int): EMA calculation period (default: 20)
    
    Returns:
        pd.Series: EMA values
    """
    if period <= 0:
        raise ValueError("EMA period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"Not enough data for EMA calculation. Need at least {period} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate EMA using pandas ewm
    ema = price_series.ewm(span=period, adjust=False).mean()
    
    return ema


def calculate_ema_signals(price_series: pd.Series, ema_values: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on price vs EMA.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        ema_values (pd.Series): EMA values
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price crosses above EMA
    buy_condition = (price_series > ema_values) & (price_series.shift(1) <= ema_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Price crosses below EMA
    sell_condition = (price_series < ema_values) & (price_series.shift(1) >= ema_values.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_ema(df: pd.DataFrame, point: float, 
                   ema_period: int = 20, price_type: PriceType = PriceType.CLOSE):
    """
    Applies EMA rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        ema_period (int): EMA calculation period
        price_type (PriceType): Price type to use for EMA calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with EMA calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate EMA
    df['EMA'] = calculate_ema(price_series, ema_period)
    
    # Add price type info to column name
    df['EMA_Price_Type'] = price_name
    
    # Calculate EMA signals
    df['EMA_Signal'] = calculate_ema_signals(price_series, df['EMA'])
    
    # Calculate support and resistance levels based on EMA
    # Use EMA as dynamic support/resistance
    ema_values = df['EMA']
    
    # Support level: EMA with small buffer
    support_levels = ema_values * 0.995  # 0.5% below EMA
    
    # Resistance level: EMA with small buffer
    resistance_levels = ema_values * 1.005  # 0.5% above EMA
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['EMA_Signal']
    df['Diff'] = price_series - ema_values  # Use price - EMA as difference indicator
    
    return df
