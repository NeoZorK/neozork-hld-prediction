# -*- coding: utf-8 -*-
# src/calculation/indicators/volume/obv_ind.py

"""
INDICATOR INFO:
Name: OBV
Category: Volume
Description: On Balance Volume. Measures buying and selling pressure using volume and price changes.
Usage: --rule obv(20) or --rule obv(20,close)
Parameters: period, price_type
Pros: + Shows volume flow, + Confirms price trends, + Good for divergence analysis
Cons: - Can be noisy, - May lag price action, - Requires volume data
File: src/calculation/indicators/volume/obv_ind.py

OBV (On Balance Volume) indicator calculation module.
"""

import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_obv(price_series: pd.Series, volume_series: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculates On Balance Volume (OBV).
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        volume_series (pd.Series): Series of volumes
        period (int): Smoothing period (default: 20)
    
    Returns:
        pd.Series: OBV values
    """
    if period <= 0:
        raise ValueError("OBV period must be positive")
    
    if len(price_series) < 2:
        logger.print_warning("Not enough data for OBV calculation. Need at least 2 points")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate price changes
    price_changes = price_series.pct_change(fill_method=None).dropna()
    
    if len(price_changes) < 1:
        logger.print_warning("Not enough price change data for OBV calculation")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Initialize OBV
    obv = pd.Series(index=price_series.index, dtype=float)
    obv.iloc[0] = volume_series.iloc[0]  # Start with first volume
    
    # Calculate OBV
    for i in range(1, len(price_series)):
        if price_series.iloc[i] > price_series.iloc[i-1]:
            # Price up, add volume
            obv.iloc[i] = obv.iloc[i-1] + volume_series.iloc[i]
        elif price_series.iloc[i] < price_series.iloc[i-1]:
            # Price down, subtract volume
            obv.iloc[i] = obv.iloc[i-1] - volume_series.iloc[i]
        else:
            # Price unchanged, keep previous OBV
            obv.iloc[i] = obv.iloc[i-1]
    
    # Apply smoothing if period > 1
    if period > 1:
        obv = obv.rolling(window=period).mean()
    
    return obv


def calculate_obv_signals(obv_values: pd.Series, price_series: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on OBV divergence and momentum.
    
    Args:
        obv_values (pd.Series): OBV values
        price_series (pd.Series): Price series (Open or Close)
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=obv_values.index)
    
    # Calculate OBV momentum
    obv_momentum = obv_values.pct_change(fill_method=None)
    price_momentum = price_series.pct_change(fill_method=None)
    
    # BUY signal: OBV increasing and price momentum positive
    buy_condition = (obv_momentum > 0) & (price_momentum > 0) & (obv_momentum > obv_momentum.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: OBV decreasing and price momentum negative
    sell_condition = (obv_momentum < 0) & (price_momentum < 0) & (obv_momentum < obv_momentum.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_obv(df: pd.DataFrame, point: float, 
                   obv_period: int = 20, price_type: PriceType = PriceType.CLOSE):
    """
    Applies OBV rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        obv_period (int): OBV smoothing period
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with OBV calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Use volume data
    volume_series = df['Volume']
    
    # Calculate OBV
    df['OBV'] = calculate_obv(price_series, volume_series, obv_period)
    
    # Add price type info to column name
    df['OBV_Price_Type'] = price_name
    
    # Calculate OBV signals
    df['OBV_Signal'] = calculate_obv_signals(df['OBV'], price_series)
    
    # Calculate support and resistance levels based on OBV
    obv_values = df['OBV']
    
    # Use OBV momentum to determine volatility
    obv_momentum = obv_values.pct_change(fill_method=None).abs()
    volatility_factor = 0.02 + obv_momentum * 0.1  # Base 2% + OBV momentum adjustment
    
    # Support level: Open price minus volatility
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level: Open price plus volatility
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['OBV_Signal']
    df['Diff'] = obv_momentum  # Use OBV momentum as difference indicator
    
    return df
