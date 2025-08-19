# -*- coding: utf-8 -*-
# src/calculation/indicators/probability/kelly_ind.py

"""
INDICATOR INFO:
Name: Kelly Criterion
Category: Probability
Description: Kelly Criterion. Calculates optimal position size based on win probability and risk/reward ratio.
Usage: --rule kelly(20) or --rule kelly(20,close)
Parameters: period, price_type
Pros: + Optimizes position sizing, + Based on mathematical principles, + Good for risk management
Cons: - Requires accurate probability estimates, - May suggest large positions, - Sensitive to parameter choice
File: src/calculation/indicators/probability/kelly_ind.py

Kelly Criterion indicator calculation module.
"""

import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_kelly(price_series: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculates Kelly Criterion values.
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        period (int): Calculation period (default: 20)
    
    Returns:
        pd.Series: Kelly Criterion values
    """
    if period <= 0:
        raise ValueError("Kelly period must be positive")
    
    if len(price_series) < period + 1:
        logger.print_warning(f"Not enough data for Kelly calculation. Need at least {period + 1} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate price changes
    price_changes = price_series.pct_change(fill_method=None).dropna()
    
    if len(price_changes) < period:
        logger.print_warning("Not enough price change data for Kelly calculation")
        return pd.Series(index=price_series.index, dtype=float)
    
    kelly_values = pd.Series(index=price_series.index, dtype=float)
    
    for i in range(period, len(price_changes)):
        # Get window of price changes
        window = price_changes.iloc[i-period:i]
        
        # Calculate wins and losses
        wins = window[window > 0]
        losses = window[window < 0]
        
        if len(wins) == 0 or len(losses) == 0:
            kelly_values.iloc[i] = 0.0
            continue
        
        # Calculate win probability
        win_prob = len(wins) / len(window)
        
        # Calculate average win and loss
        avg_win = wins.mean()
        avg_loss = abs(losses.mean())
        
        # Kelly formula: f = (bp - q) / b
        # where: b = odds received, p = probability of win, q = probability of loss
        if avg_loss > 0:
            b = avg_win / avg_loss  # odds received
            p = win_prob
            q = 1 - p
            
            kelly_fraction = (b * p - q) / b
            # Cap Kelly fraction to reasonable range (0 to 0.25)
            kelly_fraction = max(0, min(0.25, kelly_fraction))
            kelly_values.iloc[i] = kelly_fraction
        else:
            kelly_values.iloc[i] = 0.0
    
    return kelly_values


def calculate_kelly_signals(kelly_values: pd.Series, threshold: float = 0.1) -> pd.Series:
    """
    Calculate trading signals based on Kelly Criterion.
    
    Args:
        kelly_values (pd.Series): Kelly Criterion values
        threshold (float): Minimum Kelly fraction for signal (default: 0.1)
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=kelly_values.index)
    
    # BUY signal: Kelly fraction above threshold and increasing
    buy_condition = (kelly_values > threshold) & (kelly_values > kelly_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Kelly fraction below threshold and decreasing
    sell_condition = (kelly_values < threshold) & (kelly_values < kelly_values.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_kelly(df: pd.DataFrame, point: float, 
                     kelly_period: int = 20, threshold: float = 0.1,
                     price_type: PriceType = PriceType.CLOSE):
    """
    Applies Kelly Criterion rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        kelly_period (int): Kelly calculation period
        threshold (float): Minimum Kelly fraction for signal
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with Kelly Criterion calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate Kelly Criterion
    df['Kelly'] = calculate_kelly(price_series, kelly_period)
    
    # Add price type info to column name
    df['Kelly_Price_Type'] = price_name
    
    # Calculate Kelly signals
    df['Kelly_Signal'] = calculate_kelly_signals(df['Kelly'], threshold)
    
    # Calculate support and resistance levels based on Kelly Criterion
    kelly_values = df['Kelly']
    
    # Use Kelly fraction to determine volatility
    volatility_factor = 0.02 + kelly_values * 0.1  # Base 2% + Kelly adjustment
    
    # Support level: Open price minus volatility
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level: Open price plus volatility
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['Kelly_Signal']
    df['Diff'] = kelly_values  # Use Kelly fraction as difference indicator
    
    return df
