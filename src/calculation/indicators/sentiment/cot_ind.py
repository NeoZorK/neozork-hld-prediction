# -*- coding: utf-8 -*-
# src/calculation/indicators/sentiment/cot_ind.py

"""
INDICATOR INFO:
Name: COT
Category: Sentiment
Description: Commitment of Traders. Analyzes futures market positioning to gauge market sentiment.
Usage: --rule cot(20) or --rule cot(20,close)
Parameters: period, price_type
Pros: + Shows institutional sentiment, + Good for trend confirmation, + Based on actual positions
Cons: - Weekly data only, - May lag price action, - Requires futures data
File: src/calculation/indicators/sentiment/cot_ind.py

COT (Commitment of Traders) indicator calculation module.
"""

import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_cot(price_series: pd.Series, volume_series: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculates COT-like sentiment values based on price and volume.
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        volume_series (pd.Series): Series of volumes
        period (int): Calculation period (default: 20)
    
    Returns:
        pd.Series: COT sentiment values
    """
    if period <= 0:
        raise ValueError("COT period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"Not enough data for COT calculation. Need at least {period} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate price changes
    price_changes = price_series.pct_change().dropna()
    
    if len(price_changes) < period:
        logger.print_warning("Not enough price change data for COT calculation")
        return pd.Series(index=price_series.index, dtype=float)
    
    cot_values = pd.Series(index=price_series.index, dtype=float)
    
    for i in range(period, len(price_changes)):
        # Get window of data
        price_window = price_changes.iloc[i-period:i]
        volume_window = volume_series.iloc[i-period:i]
        
        # Calculate volume-weighted price changes
        if volume_window.sum() > 0:
            vwap_change = (price_window * volume_window).sum() / volume_window.sum()
        else:
            vwap_change = price_window.mean()
        
        # Calculate volume momentum
        volume_momentum = volume_window.pct_change().mean()
        
        # Calculate price momentum
        price_momentum = price_window.mean()
        
        # Combine factors into COT sentiment
        # Higher volume + positive price change = bullish sentiment
        # Higher volume + negative price change = bearish sentiment
        
        sentiment = (price_momentum + vwap_change + volume_momentum) / 3
        
        # Normalize to 0-100 scale
        cot_index = (np.tanh(sentiment * 5) + 1) * 50
        cot_values.iloc[i] = cot_index
    
    return cot_values


def calculate_cot_signals(cot_values: pd.Series, 
                         bullish_threshold: float = 70, bearish_threshold: float = 30) -> pd.Series:
    """
    Calculate trading signals based on COT sentiment.
    
    Args:
        cot_values (pd.Series): COT sentiment values
        bullish_threshold (float): Bullish threshold for buy signal (default: 70)
        bearish_threshold (float): Bearish threshold for sell signal (default: 30)
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=cot_values.index)
    
    # BUY signal: Strong bullish sentiment
    buy_condition = (cot_values > bullish_threshold) & (cot_values > cot_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Strong bearish sentiment
    sell_condition = (cot_values < bearish_threshold) & (cot_values < cot_values.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_cot(df: pd.DataFrame, point: float, 
                   cot_period: int = 20, bullish_threshold: float = 70, bearish_threshold: float = 30,
                   price_type: PriceType = PriceType.CLOSE):
    """
    Applies COT rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        cot_period (int): COT calculation period
        bullish_threshold (float): Bullish threshold for buy signal
        bearish_threshold (float): Bearish threshold for sell signal
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with COT calculations and signals
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
    
    # Calculate COT sentiment
    df['COT'] = calculate_cot(price_series, volume_series, cot_period)
    
    # Add price type info to column name
    df['COT_Price_Type'] = price_name
    
    # Calculate COT signals
    df['COT_Signal'] = calculate_cot_signals(df['COT'], bullish_threshold, bearish_threshold)
    
    # Calculate support and resistance levels based on COT sentiment
    cot_values = df['COT']
    
    # Use sentiment to determine volatility
    # Higher sentiment extremes = higher volatility expectation
    volatility_factor = 0.02 + abs(cot_values - 50) / 100 * 0.03
    
    # Support level: Open price minus volatility
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level: Open price plus volatility
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['COT_Signal']
    df['Diff'] = cot_values - 50  # Use deviation from neutral (50) as difference indicator
    
    return df
