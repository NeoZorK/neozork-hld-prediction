# -*- coding: utf-8 -*-
# src/calculation/indicators/volatility/bb_ind.py

"""
INDICATOR INFO:
Name: Bollinger Bands
Category: Volatility
Description: Bollinger Bands. Consists of a middle band (SMA) and upper/lower bands based on standard deviation.
Usage: --rule bb(20,2) or --rule bb(20,2,close)
Parameters: period, std_dev, price_type
Pros: + Identifies volatility expansion/contraction, + Shows overbought/oversold levels, + Good for mean reversion
Cons: - Can give false signals in trending markets, - Sensitive to parameter choice, - May lag in fast markets
File: src/calculation/indicators/volatility/bb_ind.py

Bollinger Bands indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_bollinger_bands(price_series: pd.Series, period: int = 20, std_dev: float = 2.0) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculates Bollinger Bands (upper, middle, lower).
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        period (int): Calculation period (default: 20)
        std_dev (float): Standard deviation multiplier (default: 2.0)
    
    Returns:
        tuple: (upper_band, middle_band, lower_band)
    """
    if period <= 0:
        raise ValueError("Bollinger Bands period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"Not enough data for Bollinger Bands calculation. Need at least {period} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float), pd.Series(index=price_series.index, dtype=float), pd.Series(index=price_series.index, dtype=float)
    
    # Calculate middle band (SMA)
    middle_band = price_series.rolling(window=period).mean()
    
    # Calculate standard deviation
    rolling_std = price_series.rolling(window=period).std()
    
    # Calculate upper and lower bands
    upper_band = middle_band + (rolling_std * std_dev)
    lower_band = middle_band - (rolling_std * std_dev)
    
    return upper_band, middle_band, lower_band


def calculate_bb_signals(price_series: pd.Series, upper_band: pd.Series, lower_band: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on Bollinger Bands.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        upper_band (pd.Series): Upper Bollinger Band
        lower_band (pd.Series): Lower Bollinger Band
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price touches or crosses below lower band
    buy_condition = (price_series <= lower_band) & (price_series.shift(1) > lower_band.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Price touches or crosses above upper band
    sell_condition = (price_series >= upper_band) & (price_series.shift(1) < upper_band.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_bollinger_bands(df: pd.DataFrame, point: float, 
                               period: int = 20, std_dev: float = 2.0,
                               price_type: PriceType = PriceType.CLOSE):
    """
    Applies Bollinger Bands rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        period (int): Calculation period
        std_dev (float): Standard deviation multiplier
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with Bollinger Bands calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate Bollinger Bands
    upper_band, middle_band, lower_band = calculate_bollinger_bands(price_series, period, std_dev)
    
    df['BB_Upper'] = upper_band
    df['BB_Middle'] = middle_band
    df['BB_Lower'] = lower_band
    
    # Add price type info to column name
    df['BB_Price_Type'] = price_name
    
    # Calculate Bollinger Bands signals
    df['BB_Signal'] = calculate_bb_signals(price_series, upper_band, lower_band)
    
    # Calculate support and resistance levels based on Bollinger Bands
    # Use lower band as support and upper band as resistance
    support_levels = lower_band
    resistance_levels = upper_band
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level (lower band)
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level (upper band)
    df['PColor2'] = SELL
    df['Direction'] = df['BB_Signal']
    df['Diff'] = (price_series - middle_band) / (upper_band - lower_band)  # Normalized position within bands
    
    return df
