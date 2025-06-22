# -*- coding: utf-8 -*-
# src/calculation/indicators/sentiment/putcallratio_ind.py

"""
INDICATOR INFO:
Name: Put/Call Ratio
Category: Sentiment
Description: Put/Call Ratio. Measures the ratio of put options to call options to gauge market sentiment.
Usage: --rule putcallratio(20) or --rule putcallratio(20,close)
Parameters: period, price_type
Pros: + Shows options sentiment, + Good contrarian indicator, + Based on actual trading activity
Cons: - May lag price action, - Requires options data, - Can be manipulated
File: src/calculation/indicators/sentiment/putcallratio_ind.py

Put/Call Ratio indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_putcallratio(price_series: pd.Series, volume_series: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculates Put/Call Ratio-like sentiment values based on price and volume patterns.
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        volume_series (pd.Series): Series of volumes
        period (int): Calculation period (default: 20)
    
    Returns:
        pd.Series: Put/Call Ratio sentiment values
    """
    if period <= 0:
        raise ValueError("Put/Call Ratio period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"Not enough data for Put/Call Ratio calculation. Need at least {period} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate price changes
    price_changes = price_series.pct_change().dropna()
    
    if len(price_changes) < period:
        logger.print_warning("Not enough price change data for Put/Call Ratio calculation")
        return pd.Series(index=price_series.index, dtype=float)
    
    putcall_values = pd.Series(index=price_series.index, dtype=float)
    
    for i in range(period, len(price_changes)):
        # Get window of data
        price_window = price_changes.iloc[i-period:i]
        volume_window = volume_series.iloc[i-period:i]
        
        # Reset indices to avoid alignment issues in boolean indexing
        price_window = price_window.reset_index(drop=True)
        volume_window = volume_window.reset_index(drop=True)
        
        # Calculate bearish vs bullish volume
        bearish_volume = volume_window[price_window < 0].sum()
        bullish_volume = volume_window[price_window > 0].sum()
        
        # Calculate put/call ratio (bearish/bullish)
        if bullish_volume > 0:
            putcall_ratio = bearish_volume / bullish_volume
        else:
            putcall_ratio = 1.0  # Neutral if no bullish volume
        
        # Normalize ratio to sentiment scale
        # Higher ratio = more bearish sentiment
        # Lower ratio = more bullish sentiment
        
        # Convert to 0-100 scale where 50 is neutral
        sentiment = 50 + (1 - putcall_ratio) * 25  # Scale the ratio
        sentiment = max(0, min(100, sentiment))
        
        putcall_values.iloc[i] = sentiment
    
    return putcall_values


def calculate_putcallratio_signals(putcall_values: pd.Series, 
                                  bullish_threshold: float = 60, bearish_threshold: float = 40) -> pd.Series:
    """
    Calculate trading signals based on Put/Call Ratio sentiment.
    
    Args:
        putcall_values (pd.Series): Put/Call Ratio sentiment values
        bullish_threshold (float): Bullish threshold for buy signal (default: 60)
        bearish_threshold (float): Bearish threshold for sell signal (default: 40)
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=putcall_values.index)
    
    # BUY signal: Low put/call ratio (bullish sentiment)
    buy_condition = (putcall_values > bullish_threshold) & (putcall_values > putcall_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: High put/call ratio (bearish sentiment)
    sell_condition = (putcall_values < bearish_threshold) & (putcall_values < putcall_values.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_putcallratio(df: pd.DataFrame, point: float, 
                            putcall_period: int = 20, bullish_threshold: float = 60, bearish_threshold: float = 40,
                            price_type: PriceType = PriceType.CLOSE):
    """
    Applies Put/Call Ratio rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        putcall_period (int): Put/Call Ratio calculation period
        bullish_threshold (float): Bullish threshold for buy signal
        bearish_threshold (float): Bearish threshold for sell signal
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with Put/Call Ratio calculations and signals
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
    
    # Calculate Put/Call Ratio sentiment
    df['PutCallRatio'] = calculate_putcallratio(price_series, volume_series, putcall_period)
    
    # Add price type info to column name
    df['PutCallRatio_Price_Type'] = price_name
    
    # Calculate Put/Call Ratio signals
    df['PutCallRatio_Signal'] = calculate_putcallratio_signals(df['PutCallRatio'], bullish_threshold, bearish_threshold)
    
    # Calculate support and resistance levels based on Put/Call Ratio sentiment
    putcall_values = df['PutCallRatio']
    
    # Use sentiment to determine volatility
    # Higher sentiment extremes = higher volatility expectation
    volatility_factor = 0.02 + abs(putcall_values - 50) / 100 * 0.03
    
    # Support level: Open price minus volatility
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level: Open price plus volatility
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['PutCallRatio_Signal']
    df['Diff'] = putcall_values - 50  # Use deviation from neutral (50) as difference indicator
    
    return df
