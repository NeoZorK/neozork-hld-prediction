# -*- coding: utf-8 -*-
# src/calculation/indicators/oscillators/rsi_ind_calc.py

"""
RSI (Relative Strength Index) indicator calculation module.
Implements RSI calculation with configurable period, overbought/oversold levels, and price type selection.
All comments and texts in English.

INDICATOR INFO:
Name: RSI (Relative Strength Index)
Category: Oscillators
Description: Measures the speed and magnitude of price changes to identify overbought/oversold conditions
Usage: --rule rsi(14,70,30,open) or --rule rsi(14,70,30,close)
Parameters: period, overbought_level, oversold_level, price_type
Pros: + Identifies overbought/oversold conditions, + Simple to interpret, + Widely used
Cons: - Can give false signals in trending markets, - Lagging indicator
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
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


def calculate_rsi_levels(open_prices: pd.Series, rsi_values: pd.Series, 
                        overbought: float = 70, oversold: float = 30) -> tuple[pd.Series, pd.Series]:
    """
    Calculates support and resistance levels based on RSI.
    
    Args:
        open_prices (pd.Series): Opening prices
        rsi_values (pd.Series): RSI values
        overbought (float): Overbought threshold
        oversold (float): Oversold threshold
    
    Returns:
        tuple: (support_levels, resistance_levels)
    """
    # Calculate price volatility as percentage of open price
    # Use a simple approach: when RSI is extreme, expect price reversal
    volatility_factor = 0.02  # 2% volatility assumption
    
    # Support level (when RSI is oversold, expect price to bounce up)
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level (when RSI is overbought, expect price to fall)
    resistance_levels = open_prices * (1 + volatility_factor)
    
    return support_levels, resistance_levels


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
    df['RSI'] = calculate_rsi(price_series, rsi_period)
    
    # Add price type info to column name
    df['RSI_Price_Type'] = price_name
    
    # Calculate RSI signals
    df['RSI_Signal'] = calculate_rsi_signals(df['RSI'], overbought, oversold)
    
    # Calculate support and resistance levels
    support_levels, resistance_levels = calculate_rsi_levels(
        open_prices, df['RSI'], overbought, oversold
    )
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['RSI_Signal']
    df['Diff'] = df['RSI']  # Use RSI value as difference indicator
    
    return df


def apply_rule_rsi_momentum(df: pd.DataFrame, point: float, 
                           rsi_period: int = 14, overbought: float = 70, oversold: float = 30,
                           price_type: PriceType = PriceType.CLOSE):
    """
    Applies RSI momentum rule logic - focuses on RSI direction changes.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        rsi_period (int): RSI calculation period
        overbought (float): Overbought threshold
        oversold (float): Oversold threshold
        price_type (PriceType): Price type to use for RSI calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with RSI momentum calculations and signals
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
    df['RSI'] = calculate_rsi(price_series, rsi_period)
    df['RSI_Price_Type'] = price_name
    
    # Calculate RSI momentum (change in RSI)
    df['RSI_Momentum'] = df['RSI'].diff()
    
    # Calculate signals based on momentum and levels
    signals = pd.Series(NOTRADE, index=df.index)
    
    # BUY: RSI rising from oversold levels
    buy_condition = (df['RSI'] > oversold) & (df['RSI_Momentum'] > 0) & (df['RSI'].shift(1) <= oversold)
    signals[buy_condition] = BUY
    
    # SELL: RSI falling from overbought levels
    sell_condition = (df['RSI'] < overbought) & (df['RSI_Momentum'] < 0) & (df['RSI'].shift(1) >= overbought)
    signals[sell_condition] = SELL
    
    df['RSI_Signal'] = signals
    
    # Calculate dynamic levels based on RSI momentum
    momentum_factor = df['RSI_Momentum'].abs() / 100  # Normalize momentum
    volatility_factor = 0.02 + momentum_factor * 0.03  # Dynamic volatility
    
    # Support and resistance levels
    support_levels = open_prices * (1 - volatility_factor)
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels
    df['PColor2'] = SELL
    df['Direction'] = df['RSI_Signal']
    df['Diff'] = df['RSI_Momentum']
    
    return df


def apply_rule_rsi_divergence(df: pd.DataFrame, point: float, 
                             rsi_period: int = 14, overbought: float = 70, oversold: float = 30,
                             price_type: PriceType = PriceType.CLOSE):
    """
    Applies RSI divergence rule logic - detects price/RSI divergences.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        rsi_period (int): RSI calculation period
        overbought (float): Overbought threshold
        oversold (float): Oversold threshold
        price_type (PriceType): Price type to use for RSI calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with RSI divergence calculations and signals
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
    df['RSI'] = calculate_rsi(price_series, rsi_period)
    df['RSI_Price_Type'] = price_name
    
    # Calculate price and RSI highs/lows for divergence detection
    price_highs = df['High'].rolling(window=5, center=True).max()
    price_lows = df['Low'].rolling(window=5, center=True).min()
    rsi_highs = df['RSI'].rolling(window=5, center=True).max()
    rsi_lows = df['RSI'].rolling(window=5, center=True).min()
    
    # Detect divergences (simplified approach)
    signals = pd.Series(NOTRADE, index=df.index)
    
    # Bearish divergence: Price making higher highs, RSI making lower highs
    bearish_divergence = (price_highs > price_highs.shift(5)) & (rsi_highs < rsi_highs.shift(5))
    signals[bearish_divergence] = SELL
    
    # Bullish divergence: Price making lower lows, RSI making higher lows
    bullish_divergence = (price_lows < price_lows.shift(5)) & (rsi_lows > rsi_lows.shift(5))
    signals[bullish_divergence] = BUY
    
    # Add signals based on overbought/oversold levels (like regular RSI)
    # SELL signal when RSI is overbought
    signals[df['RSI'] >= overbought] = SELL
    
    # BUY signal when RSI is oversold
    signals[df['RSI'] <= oversold] = BUY
    
    df['RSI_Signal'] = signals
    
    # Calculate levels based on divergence strength
    divergence_strength = (df['RSI'] - 50).abs() / 50  # How far from neutral
    volatility_factor = 0.02 + divergence_strength * 0.04
    
    support_levels = open_prices * (1 - volatility_factor)
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels
    df['PColor2'] = SELL
    df['Direction'] = df['RSI_Signal']
    df['Diff'] = divergence_strength
    
    return df 