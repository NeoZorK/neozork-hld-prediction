# -*- coding: utf-8 -*-
# src/calculation/indicators/oscillators/rsi_ind.py

"""
INDICATOR INFO:
Name: RSI
Category: Oscillators
Description: Relative Strength Index. Measures the speed and magnitude of price changes to identify overbought/oversold conditions.
Usage: --rule rsi(14,70,30,open) or --rule rsi(14,70,30,close)
Parameters: period, overbought_level, oversold_level, price_type
Pros: + Identifies overbought/oversold conditions, + Simple to interpret, + Widely used
Cons: - Can give false signals in trending markets, - Lagging indicator

RSI (Relative Strength Index) indicator module.
Implements RSI calculation with configurable period, overbought/oversold levels, and price type selection.
All comments and texts in English.
"""

import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from enum import Enum


class PriceType(Enum):
    """Enum for price type selection in RSI calculations."""
    OPEN = "open"
    CLOSE = "close"


def calculate_rsi(price_series: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculates the Relative Strength Index (RSI) indicator.
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        period (int): RSI calculation period (default: 14)
    
    Returns:
        pd.Series: RSI values between 0 and 100
    """
    if period <= 0:
        raise ValueError("RSI period must be positive")
    
    if len(price_series) < period + 1:
        logger.print_warning(f"Not enough data for RSI calculation. Need at least {period + 1} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate price changes
    delta = price_series.diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # Calculate average gains and losses using exponential moving average
    avg_gains = gains.ewm(span=period, adjust=False).mean()
    avg_losses = losses.ewm(span=period, adjust=False).mean()
    
    # Calculate RS and RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_rsi_signals(rsi_values: pd.Series, overbought: float = 70, oversold: float = 30) -> pd.Series:
    """
    Calculates trading signals based on RSI overbought/oversold levels.
    
    Args:
        rsi_values (pd.Series): RSI values
        overbought (float): Overbought threshold (default: 70)
        oversold (float): Oversold threshold (default: 30)
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=rsi_values.index)
    
    # SELL signal when RSI is overbought
    signals[rsi_values >= overbought] = SELL
    
    # BUY signal when RSI is oversold
    signals[rsi_values <= oversold] = BUY
    
    return signals


def apply_rule_rsi(df: pd.DataFrame, point: float, 
                   rsi_period: int = 14, overbought: float = 70, oversold: float = 30,
                   price_type: PriceType = PriceType.CLOSE):
    """
    Applies RSI rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        rsi_period (int): RSI calculation period
        overbought (float): Overbought threshold
        oversold (float): Oversold threshold
        price_type (PriceType): Price type to use for RSI calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with RSI calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate RSI
    df.loc[:, 'RSI'] = calculate_rsi(price_series, rsi_period)
    
    # Add price type info to column name
    df.loc[:, 'RSI_Price_Type'] = price_name
    
    # Calculate RSI signals
    df.loc[:, 'RSI_Signal'] = calculate_rsi_signals(df['RSI'], overbought, oversold)
    
    # Calculate support and resistance levels based on RSI
    volatility_factor = 0.02  # 2% volatility assumption
    
    # Support level (when RSI is oversold, expect price to bounce up)
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level (when RSI is overbought, expect price to fall)
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df.loc[:, 'PPrice1'] = support_levels  # Support level
    df.loc[:, 'PColor1'] = BUY
    df.loc[:, 'PPrice2'] = resistance_levels  # Resistance level
    df.loc[:, 'PColor2'] = SELL
    df.loc[:, 'Direction'] = df['RSI_Signal']
    df.loc[:, 'Diff'] = df['RSI']  # Use RSI value as difference indicator
    
    return df
