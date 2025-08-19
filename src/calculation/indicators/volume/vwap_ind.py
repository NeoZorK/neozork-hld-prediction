# -*- coding: utf-8 -*-
# src/calculation/indicators/volume/vwap_ind.py

"""
INDICATOR INFO:
Name: VWAP
Category: Volume
Description: Volume Weighted Average Price. Calculates the average price weighted by volume.
Usage: --rule vwap() or --rule vwap(close)
Parameters: price_type
Pros: + Reflects true market price, + Good for institutional trading, + Shows fair value
Cons: - Resets daily, - May not work for all timeframes, - Requires volume data
File: src/calculation/indicators/volume/vwap_ind.py

VWAP (Volume Weighted Average Price) indicator calculation module.
"""

import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_vwap(df: pd.DataFrame, price_type: PriceType = PriceType.CLOSE) -> pd.Series:
    """
    Calculates the Volume Weighted Average Price (VWAP).
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        price_type (PriceType): Price type to use for calculation
    
    Returns:
        pd.Series: VWAP values
    """
    if len(df) < 1:
        logger.print_warning("Not enough data for VWAP calculation")
        return pd.Series(index=df.index, dtype=float)
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
    else:  # PriceType.CLOSE
        price_series = df['Close']
    
    volume = df['Volume']
    
    # Calculate typical price (can be customized based on price_type)
    typical_price = price_series
    
    # Calculate VWAP
    # VWAP = Σ(Price × Volume) / Σ(Volume)
    cumulative_pv = (typical_price * volume).cumsum()
    cumulative_volume = volume.cumsum()
    
    vwap = cumulative_pv / cumulative_volume
    
    return vwap


def calculate_vwap_signals(price_series: pd.Series, vwap_values: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on price vs VWAP.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        vwap_values (pd.Series): VWAP values
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price crosses above VWAP
    buy_condition = (price_series > vwap_values) & (price_series.shift(1) <= vwap_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Price crosses below VWAP
    sell_condition = (price_series < vwap_values) & (price_series.shift(1) >= vwap_values.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_vwap(df: pd.DataFrame, point: float, 
                    price_type: PriceType = PriceType.CLOSE):
    """
    Applies VWAP rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        price_type (PriceType): Price type to use for VWAP calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with VWAP calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate VWAP
    df['VWAP'] = calculate_vwap(df, price_type)
    
    # Add price type info to column name
    df['VWAP_Price_Type'] = price_name
    
    # Calculate VWAP signals
    df['VWAP_Signal'] = calculate_vwap_signals(price_series, df['VWAP'])
    
    # Calculate support and resistance levels based on VWAP
    vwap_values = df['VWAP']
    
    # Support level: VWAP with small buffer
    support_levels = vwap_values * 0.995  # 0.5% below VWAP
    
    # Resistance level: VWAP with small buffer
    resistance_levels = vwap_values * 1.005  # 0.5% above VWAP
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['VWAP_Signal']
    df['Diff'] = price_series - vwap_values  # Use price - VWAP as difference indicator
    
    return df
