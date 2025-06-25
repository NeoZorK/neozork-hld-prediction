# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/supertrend_ind.py

"""
INDICATOR INFO:
Name: SuperTrend
Category: Trend
Description: SuperTrend. A trend-following indicator that shows dynamic support and resistance levels.
Usage: --rule supertrend(10,3) or --rule supertrend(10,3,close)
Parameters: period, multiplier, price_type
Pros: + Shows clear trend direction, + Good for stop-loss placement, + Works in trending markets
Cons: - Can give false signals in sideways markets, - May lag in fast markets, - Sensitive to parameters
File: src/calculation/indicators/trend/supertrend_ind.py

SuperTrend indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> tuple[pd.Series, pd.Series]:
    """
    Calculates SuperTrend.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        period (int): ATR period (default: 10)
        multiplier (float): ATR multiplier (default: 3.0)
    
    Returns:
        tuple: (supertrend_values, trend_direction)
    """
    if period <= 0 or multiplier <= 0:
        raise ValueError("Period and multiplier must be positive")
    
    if len(df) < period + 1:
        logger.print_warning(f"Not enough data for SuperTrend calculation. Need at least {period + 1} points, got {len(df)}")
        return pd.Series(index=df.index, dtype=float), pd.Series(index=df.index, dtype=float)
    
    high_prices = df['High']
    low_prices = df['Low']
    close_prices = df['Close']
    
    # Calculate ATR
    tr1 = high_prices - low_prices
    tr2 = abs(high_prices - close_prices.shift(1))
    tr3 = abs(low_prices - close_prices.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    # Calculate basic upper and lower bands
    basic_upper = (high_prices + low_prices) / 2 + multiplier * atr
    basic_lower = (high_prices + low_prices) / 2 - multiplier * atr
    
    # Initialize SuperTrend
    supertrend = pd.Series(index=df.index, dtype=float)
    trend = pd.Series(index=df.index, dtype=int)  # 1 for uptrend, -1 for downtrend
    
    # Initialize first values
    supertrend.iloc[0] = basic_lower.iloc[0]
    trend.iloc[0] = 1  # Start with uptrend
    
    # Calculate SuperTrend
    for i in range(1, len(df)):
        if trend.iloc[i-1] == 1:  # Previous trend was up
            if close_prices.iloc[i] <= supertrend.iloc[i-1]:
                # Trend reverses to down
                supertrend.iloc[i] = basic_upper.iloc[i]
                trend.iloc[i] = -1
            else:
                # Trend continues up
                supertrend.iloc[i] = basic_lower.iloc[i]
                if supertrend.iloc[i] < supertrend.iloc[i-1]:
                    supertrend.iloc[i] = supertrend.iloc[i-1]
                trend.iloc[i] = 1
        else:  # Previous trend was down
            if close_prices.iloc[i] >= supertrend.iloc[i-1]:
                # Trend reverses to up
                supertrend.iloc[i] = basic_lower.iloc[i]
                trend.iloc[i] = 1
            else:
                # Trend continues down
                supertrend.iloc[i] = basic_upper.iloc[i]
                if supertrend.iloc[i] > supertrend.iloc[i-1]:
                    supertrend.iloc[i] = supertrend.iloc[i-1]
                trend.iloc[i] = -1
    
    return supertrend, trend


def calculate_supertrend_signals(price_series: pd.Series, supertrend_values: pd.Series, trend_direction: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on SuperTrend.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        supertrend_values (pd.Series): SuperTrend values
        trend_direction (pd.Series): Trend direction (1 for up, -1 for down)
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Trend changes to up
    buy_condition = (trend_direction == 1) & (trend_direction.shift(1) == -1)
    signals[buy_condition] = BUY
    
    # SELL signal: Trend changes to down
    sell_condition = (trend_direction == -1) & (trend_direction.shift(1) == 1)
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_supertrend(df: pd.DataFrame, point: float, 
                          supertrend_period: int = 10, multiplier: float = 3.0,
                          price_type: PriceType = PriceType.CLOSE):
    """
    Applies SuperTrend rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        supertrend_period (int): SuperTrend period
        multiplier (float): ATR multiplier
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with SuperTrend calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate SuperTrend
    supertrend_values, trend_direction = calculate_supertrend(df, supertrend_period, multiplier)
    
    df['SuperTrend'] = supertrend_values
    df['SuperTrend_Direction'] = trend_direction
    
    # Add price type info to column name
    df['SuperTrend_Price_Type'] = price_name
    
    # Calculate SuperTrend signals
    df['SuperTrend_Signal'] = calculate_supertrend_signals(price_series, supertrend_values, trend_direction)
    
    # Use SuperTrend as dynamic support/resistance levels
    # Support level: SuperTrend with small buffer
    support_levels = supertrend_values * 0.995  # 0.5% below SuperTrend
    
    # Resistance level: SuperTrend with small buffer
    resistance_levels = supertrend_values * 1.005  # 0.5% above SuperTrend
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['SuperTrend_Signal']
    df['Diff'] = price_series - supertrend_values  # Use price - SuperTrend as difference indicator
    
    return df
