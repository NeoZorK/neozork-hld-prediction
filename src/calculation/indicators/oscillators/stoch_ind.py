# -*- coding: utf-8 -*-
# src/calculation/indicators/oscillators/stoch_ind.py

"""
INDICATOR INFO:
Name: Stochastic
Category: Oscillators
Description: Stochastic Oscillator. Measures momentum by comparing a closing price to its price range over a specific period
Usage: --rule stoch(14,3,3) or --rule stoch(14,3,3,close)
Parameters: k_period, d_period, slowing, price_type
Pros: + Identifies overbought/oversold conditions, + Shows momentum shifts, + Good for range-bound markets
Cons: - Can give false signals in trending markets, - May lag in fast markets, - Sensitive to parameter choice

Stochastic Oscillator indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_stochastic(df: pd.DataFrame, k_period: int = 14, d_period: int = 3, 
                        slowing: int = 3, price_type: PriceType = PriceType.CLOSE) -> tuple[pd.Series, pd.Series]:
    """
    Calculates the Stochastic Oscillator (%K and %D).
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        k_period (int): %K period (default: 14)
        d_period (int): %D period (default: 3)
        slowing (int): Smoothing period (default: 3)
        price_type (PriceType): Price type to use for calculation
    
    Returns:
        tuple: (%K values, %D values)
    """
    if k_period <= 0 or d_period <= 0 or slowing <= 0:
        raise ValueError("All periods must be positive")
    
    if len(df) < max(k_period, d_period, slowing):
        logger.print_warning(f"Not enough data for Stochastic calculation. Need at least {max(k_period, d_period, slowing)} points, got {len(df)}")
        return pd.Series(index=df.index, dtype=float), pd.Series(index=df.index, dtype=float)
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        close_price = df['Open']
    else:  # PriceType.CLOSE
        close_price = df['Close']
    
    high_price = df['High']
    low_price = df['Low']
    
    # Calculate %K
    lowest_low = low_price.rolling(window=k_period).min()
    highest_high = high_price.rolling(window=k_period).max()
    
    # Raw %K with protection against division by zero
    denominator = highest_high - lowest_low
    raw_k = np.where(
        denominator > 1e-10,
        ((close_price - lowest_low) / denominator) * 100,
        np.nan  # if no range, let it be NaN
    )
    # Limit values before smoothing
    raw_k = np.clip(raw_k, 0, 100)
    
    # Smooth %K
    k_percent = pd.Series(raw_k, index=df.index).rolling(window=slowing).mean()
    # Limit after smoothing
    k_percent = k_percent.clip(0, 100)
    
    # Calculate %D (SMA of %K)
    d_percent = k_percent.rolling(window=d_period).mean()
    d_percent = d_percent.clip(0, 100)
    
    return k_percent, d_percent


def calculate_stochastic_signals(k_values: pd.Series, d_values: pd.Series, 
                                overbought: float = 80, oversold: float = 20) -> pd.Series:
    """
    Calculate trading signals based on Stochastic levels.
    
    Args:
        k_values (pd.Series): %K values
        d_values (pd.Series): %D values
        overbought (float): Overbought threshold (default: 80)
        oversold (float): Oversold threshold (default: 20)
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=k_values.index)
    
    # BUY signal: %K crosses above %D from oversold levels
    buy_condition = (k_values > d_values) & (k_values.shift(1) <= d_values.shift(1)) & (k_values < oversold)
    signals[buy_condition] = BUY
    
    # SELL signal: %K crosses below %D from overbought levels
    sell_condition = (k_values < d_values) & (k_values.shift(1) >= d_values.shift(1)) & (k_values > overbought)
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_stochastic(df: pd.DataFrame, point: float, 
                          k_period: int = 14, d_period: int = 3, slowing: int = 3,
                          overbought: float = 80, oversold: float = 20,
                          price_type: PriceType = PriceType.CLOSE):
    """
    Applies Stochastic rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        k_period (int): %K period
        d_period (int): %D period
        slowing (int): Smoothing period
        overbought (float): Overbought threshold
        oversold (float): Oversold threshold
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with Stochastic calculations and signals
    """
    open_prices = df['Open']
    
    # Calculate Stochastic
    k_values, d_values = calculate_stochastic(df, k_period, d_period, slowing, price_type)
    
    # Limit values only for final DataFrame
    k_values = k_values.clip(0, 100)
    d_values = d_values.clip(0, 100)
    
    df['Stoch_K'] = k_values
    df['Stoch_D'] = d_values
    
    # Add price type info to column name
    price_name = "Open" if price_type == PriceType.OPEN else "Close"
    df['Stoch_Price_Type'] = price_name
    
    # Calculate Stochastic signals
    df['Stoch_Signal'] = calculate_stochastic_signals(k_values, d_values, overbought, oversold)
    
    # Calculate support and resistance levels based on Stochastic
    volatility_factor = 0.02  # 2% volatility assumption
    
    # Support level (when Stochastic is oversold, expect price to bounce up)
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level (when Stochastic is overbought, expect price to fall)
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['Stoch_Signal']
    df['Diff'] = k_values - d_values  # Use %K - %D as difference indicator
    
    return df
