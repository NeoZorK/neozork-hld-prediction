# -*- coding: utf-8 -*-
# src/calculation/indicators/predictive/hma_ind.py

"""
INDICATOR INFO:
Name: HMA
Category: Predictive
Description: Hull Moving Average. A type of moving average that reduces lag while maintaining smoothness.
Usage: --rule hma(20) or --rule hma(20,close)
Parameters: period, price_type
Pros: + Reduces lag compared to traditional MAs, + Maintains smoothness, + Good for trend identification
Cons: - Can be more volatile, - May give false signals in choppy markets, - Sensitive to parameter choice
File: src/calculation/indicators/predictive/hma_ind.py

HMA (Hull Moving Average) indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_hma(price_series: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculates the Hull Moving Average (HMA).
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        period (int): HMA calculation period (default: 20)
    
    Returns:
        pd.Series: HMA values
    """
    if period <= 0:
        raise ValueError("HMA period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"Not enough data for HMA calculation. Need at least {period} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate WMA with period/2
    half_period = int(period / 2)
    wma1 = price_series.rolling(window=half_period).apply(
        lambda x: np.average(x, weights=np.arange(1, len(x) + 1)), raw=True
    )
    
    # Calculate WMA with period
    wma2 = price_series.rolling(window=period).apply(
        lambda x: np.average(x, weights=np.arange(1, len(x) + 1)), raw=True
    )
    
    # Calculate raw HMA
    raw_hma = 2 * wma1 - wma2
    
    # Calculate final HMA using WMA with sqrt(period)
    sqrt_period = int(np.sqrt(period))
    hma = raw_hma.rolling(window=sqrt_period).apply(
        lambda x: np.average(x, weights=np.arange(1, len(x) + 1)), raw=True
    )
    
    return hma


def calculate_hma_signals(price_series: pd.Series, hma_values: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on price vs HMA.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        hma_values (pd.Series): HMA values
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price crosses above HMA
    buy_condition = (price_series > hma_values) & (price_series.shift(1) <= hma_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Price crosses below HMA
    sell_condition = (price_series < hma_values) & (price_series.shift(1) >= hma_values.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_hma(df: pd.DataFrame, point: float, 
                   hma_period: int = 20, price_type: PriceType = PriceType.CLOSE):
    """
    Applies HMA rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        hma_period (int): HMA calculation period
        price_type (PriceType): Price type to use for HMA calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with HMA calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate HMA
    df['HMA'] = calculate_hma(price_series, hma_period)
    
    # Add price type info to column name
    df['HMA_Price_Type'] = price_name
    
    # Calculate HMA signals
    df['HMA_Signal'] = calculate_hma_signals(price_series, df['HMA'])
    
    # Calculate support and resistance levels based on HMA
    # Use HMA as dynamic support/resistance
    hma_values = df['HMA']
    
    # Support level: HMA with small buffer
    support_levels = hma_values * 0.995  # 0.5% below HMA
    
    # Resistance level: HMA with small buffer
    resistance_levels = hma_values * 1.005  # 0.5% above HMA
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['HMA_Signal']
    df['Diff'] = price_series - hma_values  # Use price - HMA as difference indicator
    
    return df
