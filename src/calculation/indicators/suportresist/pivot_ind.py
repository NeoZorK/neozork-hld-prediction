# -*- coding: utf-8 -*-
# src/calculation/indicators/suportresist/pivot_ind.py

"""
INDICATOR INFO:
Name: Pivot Points
Category: Support/Resistance
Description: Pivot Points. Calculates support and resistance levels based on previous day's high, low, and close.
Usage: --rule pivot() or --rule pivot(close)
Parameters: price_type
Pros: + Clear support/resistance levels, + Works in any market, + Good for day trading
Cons: - Static levels, - May not work in trending markets, - Requires previous day data
File: src/calculation/indicators/suportresist/pivot_ind.py

Pivot Points indicator calculation module.
"""

import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_pivot_points(df: pd.DataFrame, price_type: PriceType = PriceType.CLOSE) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculates Pivot Points (PP, R1, S1).
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        price_type (PriceType): Price type to use for calculation
    
    Returns:
        tuple: (pivot_point, resistance_1, support_1)
    """
    if len(df) < 2:
        logger.print_warning("Not enough data for Pivot Points calculation. Need at least 2 days of data")
        return pd.Series(index=df.index, dtype=float), pd.Series(index=df.index, dtype=float), pd.Series(index=df.index, dtype=float)
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        close_price = df['Open']
    else:  # PriceType.CLOSE
        close_price = df['Close']
    
    high_price = df['High']
    low_price = df['Low']
    
    # Get previous day's values
    prev_high = high_price.shift(1)
    prev_low = low_price.shift(1)
    prev_close = close_price.shift(1)
    
    # Calculate Pivot Point (PP)
    # PP = (Previous High + Previous Low + Previous Close) / 3
    pivot_point = (prev_high + prev_low + prev_close) / 3
    
    # Calculate Resistance 1 (R1)
    # R1 = (2 * PP) - Previous Low
    resistance_1 = (2 * pivot_point) - prev_low
    
    # Calculate Support 1 (S1)
    # S1 = (2 * PP) - Previous High
    support_1 = (2 * pivot_point) - prev_high
    
    return pivot_point, resistance_1, support_1


def calculate_pivot_signals(price_series: pd.Series, pivot_point: pd.Series, 
                           resistance_1: pd.Series, support_1: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on Pivot Points.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        pivot_point (pd.Series): Pivot Point values
        resistance_1 (pd.Series): Resistance 1 values
        support_1 (pd.Series): Support 1 values
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price bounces off support level
    buy_condition = (price_series > support_1) & (price_series.shift(1) <= support_1.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Price bounces off resistance level
    sell_condition = (price_series < resistance_1) & (price_series.shift(1) >= resistance_1.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_pivot(df: pd.DataFrame, point: float, 
                     price_type: PriceType = PriceType.CLOSE):
    """
    Applies Pivot Points rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        price_type (PriceType): Price type to use for Pivot Points calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with Pivot Points calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate Pivot Points
    pivot_point, resistance_1, support_1 = calculate_pivot_points(df, price_type)
    
    df['Pivot_PP'] = pivot_point
    df['Pivot_R1'] = resistance_1
    df['Pivot_S1'] = support_1
    
    # Add price type info to column name
    df['Pivot_Price_Type'] = price_name
    
    # Calculate Pivot Points signals
    df['Pivot_Signal'] = calculate_pivot_signals(price_series, pivot_point, resistance_1, support_1)
    
    # Calculate support and resistance levels based on Pivot Points
    # Use S1 as support and R1 as resistance
    support_levels = support_1
    resistance_levels = resistance_1
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level (S1)
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level (R1)
    df['PColor2'] = SELL
    df['Direction'] = df['Pivot_Signal']
    df['Diff'] = price_series - pivot_point  # Use price - PP as difference indicator
    
    return df
