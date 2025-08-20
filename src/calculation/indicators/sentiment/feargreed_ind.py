# -*- coding: utf-8 -*-
# src/calculation/indicators/sentiment/feargreed_ind.py

"""
INDICATOR INFO:
Name: Fear & Greed
Category: Sentiment
Description: Fear & Greed Index. Measures market sentiment based on volatility, momentum, and other factors.
Usage: --rule feargreed(14) or --rule feargreed(14,close)
Parameters: period, price_type
Pros: + Measures market sentiment, + Good for contrarian signals, + Helps identify extremes
Cons: - May lag market moves, - Subjective interpretation, - Can give false signals in trending markets
File: src/calculation/indicators/sentiment/feargreed_ind.py

Fear & Greed indicator calculation module.
"""

import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_feargreed(price_series: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculates Fear & Greed Index values.
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        period (int): Calculation period (default: 14)
    
    Returns:
        pd.Series: Fear & Greed Index values (0-100)
    """
    if period <= 0:
        raise ValueError("Fear & Greed period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"[FearGreed] Not enough data: need at least {period} rows, got {len(price_series)}. Returning all NaN.")
        return pd.Series([np.nan]*len(price_series), index=price_series.index, dtype=float)
    
    # Calculate price changes
    price_changes = price_series.pct_change()
    
    feargreed_values = pd.Series([np.nan]*len(price_series), index=price_series.index, dtype=float)
    
    for i in range(period, len(price_series)):
        window = price_changes.iloc[i-period+1:i+1].dropna()
        if len(window) < period-1:
            continue
        # Calculate volatility (standard deviation)
        volatility = window.std()
        
        # Calculate momentum (average return)
        momentum = window.mean()
        
        # Calculate market strength (ratio of positive to negative days)
        positive_days = len(window[window > 0])
        negative_days = len(window[window < 0])
        total_days = len(window)
        
        if total_days > 0:
            strength = positive_days / total_days
        else:
            strength = 0.5
        
        # Combine factors into Fear & Greed Index
        # Higher volatility = more fear
        # Higher momentum = more greed
        # Higher strength = more greed
        
        # Normalize volatility (0-1 scale)
        vol_factor = min(1.0, volatility * 10)  # Scale volatility
        
        # Normalize momentum (-1 to 1 scale)
        mom_factor = np.tanh(momentum * 10)  # Use tanh to bound momentum
        
        # Combine factors
        fear_factor = (vol_factor + (1 - strength)) / 2
        greed_factor = (mom_factor + strength) / 2
        
        # Calculate final index (0-100)
        feargreed_index = (greed_factor - fear_factor + 1) * 50
        feargreed_index = max(0, min(100, feargreed_index))
        
        feargreed_values.iloc[i] = feargreed_index
    
    return feargreed_values


def calculate_feargreed_signals(feargreed_values: pd.Series, 
                               fear_threshold: float = 40, greed_threshold: float = 60) -> pd.Series:
    """
    Calculate trading signals based on Fear & Greed Index.
    
    Args:
        feargreed_values (pd.Series): Fear & Greed Index values
        fear_threshold (float): Fear threshold for buy signal (default: 40)
        greed_threshold (float): Greed threshold for sell signal (default: 60)
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=feargreed_values.index)
    
    # BUY signal: Extreme fear (contrarian)
    buy_condition = (feargreed_values < fear_threshold) & (feargreed_values > feargreed_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Extreme greed (contrarian)
    sell_condition = (feargreed_values > greed_threshold) & (feargreed_values < feargreed_values.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_feargreed(df: pd.DataFrame, point: float, 
                         feargreed_period: int = 14, fear_threshold: float = 40, greed_threshold: float = 60,
                         price_type: PriceType = PriceType.CLOSE):
    """
    Applies Fear & Greed rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        feargreed_period (int): Fear & Greed calculation period
        fear_threshold (float): Fear threshold for buy signal
        greed_threshold (float): Greed threshold for sell signal
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with Fear & Greed calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate Fear & Greed Index
    df['FearGreed'] = calculate_feargreed(price_series, feargreed_period)
    
    # Add price type info to column name
    df['FearGreed_Price_Type'] = price_name
    
    # Calculate Fear & Greed signals
    df['FearGreed_Signal'] = calculate_feargreed_signals(df['FearGreed'], fear_threshold, greed_threshold)
    
    # Calculate support and resistance levels based on Fear & Greed Index
    feargreed_values = df['FearGreed']
    
    # Use sentiment to determine volatility
    # Higher fear = higher volatility expectation
    volatility_factor = 0.02 + (feargreed_values / 100) * 0.03
    
    # Support level: Open price minus volatility
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level: Open price plus volatility
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['FearGreed_Signal']
    df['Diff'] = feargreed_values - 50  # Use deviation from neutral (50) as difference indicator
    
    return df
