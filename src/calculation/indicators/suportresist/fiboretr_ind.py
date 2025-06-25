# -*- coding: utf-8 -*-
# src/calculation/indicators/suportresist/fiboretr_ind.py

"""
INDICATOR INFO:
Name: Fibonacci Retracement
Category: Support/Resistance
Description: Fibonacci Retracement. Uses Fibonacci ratios to identify potential support and resistance levels.
Usage: --rule fiboretr(20) or --rule fiboretr(20,close)
Parameters: period, price_type
Pros: + Based on mathematical principles, + Widely recognized levels, + Good for trend analysis
Cons: - Subjective swing point selection, - May not work in all markets, - Requires trend identification
File: src/calculation/indicators/suportresist/fiboretr_ind.py

Fibonacci Retracement indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_fiboretr(df: pd.DataFrame, period: int = 20) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculates Fibonacci Retracement levels.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        period (int): Calculation period (default: 20)
    
    Returns:
        tuple: (fib_236, fib_382, fib_618)
    """
    if period <= 0:
        raise ValueError("Fibonacci Retracement period must be positive")
    
    if len(df) < period:
        logger.print_warning(f"Not enough data for Fibonacci Retracement calculation. Need at least {period} points, got {len(df)}")
        return pd.Series(index=df.index, dtype=float), pd.Series(index=df.index, dtype=float), pd.Series(index=df.index, dtype=float)
    
    high_prices = df['High']
    low_prices = df['Low']
    
    # Fibonacci ratios
    fib_236 = 0.236
    fib_382 = 0.382
    fib_618 = 0.618
    
    # Calculate swing high and low over the period
    swing_high = high_prices.rolling(window=period).max()
    swing_low = low_prices.rolling(window=period).min()
    
    # Calculate Fibonacci retracement levels
    range_size = swing_high - swing_low
    
    # 23.6% retracement
    fib_236_level = swing_high - (range_size * fib_236)
    
    # 38.2% retracement
    fib_382_level = swing_high - (range_size * fib_382)
    
    # 61.8% retracement
    fib_618_level = swing_high - (range_size * fib_618)
    
    return fib_236_level, fib_382_level, fib_618_level


def calculate_fiboretr_signals(price_series: pd.Series, fib_236: pd.Series, fib_382: pd.Series, fib_618: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on Fibonacci Retracement levels.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        fib_236 (pd.Series): 23.6% Fibonacci level
        fib_382 (pd.Series): 38.2% Fibonacci level
        fib_618 (pd.Series): 61.8% Fibonacci level
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price bounces from Fibonacci support levels
    buy_condition = ((price_series > fib_618) & (price_series.shift(1) <= fib_618.shift(1))) | \
                   ((price_series > fib_382) & (price_series.shift(1) <= fib_382.shift(1)))
    signals[buy_condition] = BUY
    
    # SELL signal: Price rejects from Fibonacci resistance levels
    sell_condition = ((price_series < fib_236) & (price_series.shift(1) >= fib_236.shift(1))) | \
                    ((price_series < fib_382) & (price_series.shift(1) >= fib_382.shift(1)))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_fiboretr(df: pd.DataFrame, point: float, 
                        fiboretr_period: int = 20, price_type: PriceType = PriceType.CLOSE):
    """
    Applies Fibonacci Retracement rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        fiboretr_period (int): Fibonacci Retracement period
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with Fibonacci Retracement calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate Fibonacci Retracement levels
    fib_236, fib_382, fib_618 = calculate_fiboretr(df, fiboretr_period)
    
    df['FibRetr_236'] = fib_236
    df['FibRetr_382'] = fib_382
    df['FibRetr_618'] = fib_618
    
    # Add price type info to column name
    df['FibRetr_Price_Type'] = price_name
    
    # Calculate Fibonacci Retracement signals
    df['FibRetr_Signal'] = calculate_fiboretr_signals(price_series, fib_236, fib_382, fib_618)
    
    # Use Fibonacci levels as support and resistance
    # Support level: 61.8% retracement
    support_levels = fib_618
    
    # Resistance level: 23.6% retracement
    resistance_levels = fib_236
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['FibRetr_Signal']
    df['Diff'] = price_series - fib_382  # Use price - 38.2% level as difference indicator
    
    return df
