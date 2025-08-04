# -*- coding: utf-8 -*-
# src/calculation/indicators/momentum/macd_ind.py

"""
INDICATOR INFO:
Name: MACD
Category: Momentum
Description: Moving Average Convergence Divergence. Shows the relationship between two moving averages of a price.
Usage: --rule macd(12,26,9) or --rule macd(12,26,9,close)
Parameters: fast_period, slow_period, signal_period, price_type
Pros: + Identifies trend changes, + Shows momentum shifts, + Good for trend confirmation
Cons: - Lagging indicator, - Can give false signals in sideways markets, - Sensitive to parameter choice
File: src/calculation/indicators/momentum/macd_ind.py

MACD (Moving Average Convergence Divergence) indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_macd(price_series: pd.Series, fast_period: int = 12, slow_period: int = 26, 
                   signal_period: int = 9) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculates MACD (MACD line, Signal line, Histogram).
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        fast_period (int): Fast EMA period (default: 12)
        slow_period (int): Slow EMA period (default: 26)
        signal_period (int): Signal line period (default: 9)
    
    Returns:
        tuple: (macd_line, signal_line, histogram)
    """
    if fast_period <= 0 or slow_period <= 0 or signal_period <= 0:
        raise ValueError("All periods must be positive")
    
    if len(price_series) < max(fast_period, slow_period, signal_period):
        logger.print_warning(f"Not enough data for MACD calculation. Need at least {max(fast_period, slow_period, signal_period)} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float), pd.Series(index=price_series.index, dtype=float), pd.Series(index=price_series.index, dtype=float)
    
    # Calculate fast and slow EMAs
    fast_ema = price_series.ewm(span=fast_period, adjust=False).mean()
    slow_ema = price_series.ewm(span=slow_period, adjust=False).mean()
    
    # Calculate MACD line
    macd_line = fast_ema - slow_ema
    
    # Calculate signal line (EMA of MACD line)
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    
    # Calculate histogram
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def calculate_macd_signals(macd_line: pd.Series, signal_line: pd.Series, histogram: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on MACD.
    
    Args:
        macd_line (pd.Series): MACD line values
        signal_line (pd.Series): Signal line values
        histogram (pd.Series): Histogram values
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=macd_line.index)
    
    # BUY signal: MACD line crosses above signal line
    buy_condition = (macd_line > signal_line) & (macd_line.shift(1) <= signal_line.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: MACD line crosses below signal line
    sell_condition = (macd_line < signal_line) & (macd_line.shift(1) >= signal_line.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_macd(df: pd.DataFrame, point: float, 
                    macd_fast: int = 12, macd_slow: int = 26, macd_signal: int = 9,
                    price_type: PriceType = PriceType.CLOSE):
    """
    Applies MACD rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        macd_fast (int): Fast EMA period
        macd_slow (int): Slow EMA period
        macd_signal (int): Signal line period
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with MACD calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate MACD
    macd_line, signal_line, histogram = calculate_macd(price_series, macd_fast, macd_slow, macd_signal)
    
    df['MACD_Line'] = macd_line
    df['MACD_Signal'] = signal_line
    df['MACD_Histogram'] = histogram
    
    # Add price type info to column name
    df['MACD_Price_Type'] = price_name
    
    # Calculate MACD signals
    df['MACD_Trading_Signal'] = calculate_macd_signals(macd_line, signal_line, histogram)
    
    # Calculate support and resistance levels based on MACD
    # Use MACD histogram to determine volatility
    volatility_factor = 0.02 + (histogram.abs() / histogram.abs().max()) * 0.03
    
    # Support level: Open price minus volatility
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level: Open price plus volatility
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['MACD_Trading_Signal']
    df['Diff'] = histogram  # Use histogram as difference indicator
    
    return df
