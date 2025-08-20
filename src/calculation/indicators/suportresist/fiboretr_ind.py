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
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_fiboretr(df: pd.DataFrame, period: int = 20, fib_levels: list = None) -> dict[str, pd.Series]:
    """
    Calculates Fibonacci Retracement levels.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        period (int): Calculation period (default: 20)
        fib_levels (list): Fibonacci levels (default: [0.236, 0.382, 0.618])
    
    Returns:
        dict: Dictionary with Fibonacci level names as keys and Series as values
    """
    if period <= 0:
        raise ValueError("Fibonacci Retracement period must be positive")
    
    if len(df) < period:
        logger.print_warning(f"Not enough data for Fibonacci Retracement calculation. Need at least {period} points, got {len(df)}")
        # Return empty series for all levels
        result = {}
        for level in fib_levels or [0.236, 0.382, 0.618]:
            level_name = f'fib_{int(level * 1000)}'
            result[level_name] = pd.Series(index=df.index, dtype=float)
        return result
    
    high_prices = df['High']
    low_prices = df['Low']
    
    # Use default Fibonacci ratios if none provided
    if fib_levels is None:
        fib_levels = [0.236, 0.382, 0.618]
    
    # Calculate swing high and low over the period
    swing_high = high_prices.rolling(window=period).max()
    swing_low = low_prices.rolling(window=period).min()
    
    # Calculate Fibonacci retracement levels
    range_size = swing_high - swing_low
    
    # Calculate all Fibonacci levels
    result = {}
    for level in fib_levels:
        level_name = f'fib_{int(level * 1000)}'  # Convert 0.236 to fib_236
        fib_level = swing_high - (range_size * level)
        result[level_name] = fib_level
    
    return result


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
    
    # BUY signals: Price bounces from Fibonacci support levels
    # Buy when price crosses above support levels
    buy_condition_618 = (price_series > fib_618) & (price_series.shift(1) <= fib_618.shift(1))
    buy_condition_382 = (price_series > fib_382) & (price_series.shift(1) <= fib_382.shift(1))
    buy_condition_236 = (price_series > fib_236) & (price_series.shift(1) <= fib_236.shift(1))
    
    # Additional buy conditions: price near support levels with momentum
    buy_near_618 = (price_series >= fib_618 * 0.995) & (price_series <= fib_618 * 1.005) & (price_series > price_series.shift(1))
    buy_near_382 = (price_series >= fib_382 * 0.995) & (price_series <= fib_382 * 1.005) & (price_series > price_series.shift(1))
    
    buy_condition = buy_condition_618 | buy_condition_382 | buy_condition_236 | buy_near_618 | buy_near_382
    signals[buy_condition] = BUY
    
    # SELL signals: Price rejects from Fibonacci resistance levels
    # Sell when price crosses below resistance levels
    sell_condition_236 = (price_series < fib_236) & (price_series.shift(1) >= fib_236.shift(1))
    sell_condition_382 = (price_series < fib_382) & (price_series.shift(1) >= fib_382.shift(1))
    sell_condition_618 = (price_series < fib_618) & (price_series.shift(1) >= fib_618.shift(1))
    
    # Additional sell conditions: price near resistance levels with downward momentum
    sell_near_236 = (price_series >= fib_236 * 0.995) & (price_series <= fib_236 * 1.005) & (price_series < price_series.shift(1))
    sell_near_382 = (price_series >= fib_382 * 0.995) & (price_series <= fib_382 * 1.005) & (price_series < price_series.shift(1))
    
    sell_condition = sell_condition_236 | sell_condition_382 | sell_condition_618 | sell_near_236 | sell_near_382
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_fiboretr(df: pd.DataFrame, point: float, 
                        fib_levels: list = None, price_type: PriceType = PriceType.CLOSE):
    """
    Applies Fibonacci Retracement rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        fib_levels (list): Fibonacci levels (default: [0.236, 0.382, 0.618])
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
    
    # Use default Fibonacci levels if none provided
    if fib_levels is None:
        fib_levels = [0.236, 0.382, 0.618]
    
    # Calculate Fibonacci Retracement levels
    fib_levels_dict = calculate_fiboretr(df, 20, fib_levels)
    
    # Add all Fibonacci levels to DataFrame
    for level_name, level_series in fib_levels_dict.items():
        df[f'FibRetr_{level_name[4:]}'] = level_series  # Remove 'fib_' prefix
    
    # Add price type info to column name
    df['FibRetr_Price_Type'] = price_name
    
    # Get the first three levels for signal calculation (if available)
    fib_236 = fib_levels_dict.get('fib_236', pd.Series(index=df.index, dtype=float))
    fib_382 = fib_levels_dict.get('fib_382', pd.Series(index=df.index, dtype=float))
    fib_618 = fib_levels_dict.get('fib_618', pd.Series(index=df.index, dtype=float))
    
    # Calculate Fibonacci Retracement signals
    df['FibRetr_Signal'] = calculate_fiboretr_signals(price_series, fib_236, fib_382, fib_618)
    
    # Use Fibonacci levels as support and resistance
    # Support level: 61.8% retracement (or highest available level)
    support_levels = fib_618 if 'fib_618' in fib_levels_dict else fib_382
    
    # Resistance level: 23.6% retracement (or lowest available level)
    resistance_levels = fib_236 if 'fib_236' in fib_levels_dict else fib_382
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['FibRetr_Signal']
    df['Diff'] = price_series - fib_382  # Use price - 38.2% level as difference indicator
    
    return df
