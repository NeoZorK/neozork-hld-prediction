# -*- coding: utf-8 -*-
# src/calculation/indicators/suportresist/donchain_ind.py

"""
INDICATOR INFO:
Name: Donchian Channel
Category: Support/Resistance
Description: Donchian Channel. Shows the highest high and lowest low over a specified period.
Usage: --rule donchain(20) or --rule donchain(20,close)
Parameters: period, price_type
Pros: + Shows clear support/resistance levels, + Good for breakout trading, + Simple to understand
Cons: - Lagging indicator, - May give false breakouts, - Sensitive to period choice
File: src/calculation/indicators/suportresist/donchain_ind.py

Donchian Channel indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_donchain(df: pd.DataFrame, period: int = 20) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculates Donchian Channel (Upper, Middle, Lower).
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        period (int): Channel period (default: 20)
    
    Returns:
        tuple: (upper_band, middle_band, lower_band)
    """
    if period <= 0:
        raise ValueError("Donchian Channel period must be positive")
    
    if len(df) < period:
        logger.print_warning(f"Not enough data for Donchian Channel calculation. Need at least {period} points, got {len(df)}")
        return pd.Series(index=df.index, dtype=float), pd.Series(index=df.index, dtype=float), pd.Series(index=df.index, dtype=float)
    
    high_prices = df['High']
    low_prices = df['Low']
    
    # Calculate upper band (highest high)
    upper_band = high_prices.rolling(window=period).max()
    
    # Calculate lower band (lowest low)
    lower_band = low_prices.rolling(window=period).min()
    
    # Calculate middle band (average of upper and lower)
    middle_band = (upper_band + lower_band) / 2
    
    return upper_band, middle_band, lower_band


def calculate_donchain_signals(price_series: pd.Series, upper_band: pd.Series, lower_band: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on Donchian Channel breakouts.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        upper_band (pd.Series): Upper Donchian band
        lower_band (pd.Series): Lower Donchian band
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price breaks above upper band
    buy_condition = (price_series > upper_band) & (price_series.shift(1) <= upper_band.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Price breaks below lower band
    sell_condition = (price_series < lower_band) & (price_series.shift(1) >= lower_band.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_donchain(df: pd.DataFrame, point: float, 
                        donchain_period: int = 20, price_type: PriceType = PriceType.CLOSE):
    """
    Applies Donchian Channel rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        donchain_period (int): Donchian Channel period
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with Donchian Channel calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate Donchian Channel
    upper_band, middle_band, lower_band = calculate_donchain(df, donchain_period)
    
    df['Donchain_Upper'] = upper_band
    df['Donchain_Middle'] = middle_band
    df['Donchain_Lower'] = lower_band
    
    # Add price type info to column name
    df['Donchain_Price_Type'] = price_name
    
    # Calculate Donchian Channel signals
    df['Donchain_Signal'] = calculate_donchain_signals(price_series, upper_band, lower_band)
    
    # Use Donchian Channel bands as support and resistance levels
    # Support level: Lower band
    support_levels = lower_band
    
    # Resistance level: Upper band
    resistance_levels = upper_band
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['Donchain_Signal']
    df['Diff'] = price_series - middle_band  # Use price - middle band as difference indicator
    
    return df
