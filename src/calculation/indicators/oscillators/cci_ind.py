# -*- coding: utf-8 -*-
# src/calculation/indicators/oscillators/cci_ind.py

"""
INDICATOR INFO:
Name: CCI
Category: Oscillators
Description: Commodity Channel Index. Measures the current price level relative to an average price level over a given time period
Usage: --rule cci(20,0.015) or --rule cci(20,0.015,close)
Parameters: period, constant, price_type
Pros: + Identifies cyclical trends, + Works well for commodities, + Shows overbought/oversold levels
Cons: - Can be volatile, - May give false signals in non-cyclical markets, - Requires careful parameter tuning

CCI (Commodity Channel Index) indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_cci(price_series: pd.Series, period: int = 20, constant: float = 0.015) -> pd.Series:
    """
    Calculates the Commodity Channel Index (CCI) indicator.
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        period (int): CCI calculation period (default: 20)
        constant (float): CCI constant (default: 0.015)
    
    Returns:
        pd.Series: CCI values
    """
    if period <= 0:
        raise ValueError("CCI period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"Not enough data for CCI calculation. Need at least {period} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate typical price (High + Low + Close) / 3
    # Since we only have one price series, we'll use it directly
    typical_price = price_series
    
    # Calculate simple moving average of typical price
    sma = typical_price.rolling(window=period).mean()
    
    # Calculate mean deviation
    mean_deviation = typical_price.rolling(window=period).apply(
        lambda x: np.mean(np.abs(x - x.mean())), raw=True
    )
    
    # Calculate CCI
    cci = (typical_price - sma) / (constant * mean_deviation)
    
    return cci


def calculate_cci_signals(cci_values: pd.Series, overbought: float = 100, oversold: float = -100) -> pd.Series:
    """
    Calculate trading signals based on CCI levels.
    
    Args:
        cci_values (pd.Series): CCI values
        overbought (float): Overbought threshold (default: 100)
        oversold (float): Oversold threshold (default: -100)
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=cci_values.index)
    
    # BUY signal: CCI crosses above oversold level
    buy_condition = (cci_values > oversold) & (cci_values.shift(1) <= oversold)
    signals[buy_condition] = BUY
    
    # SELL signal: CCI crosses below overbought level
    sell_condition = (cci_values < overbought) & (cci_values.shift(1) >= overbought)
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_cci(df: pd.DataFrame, point: float, 
                   cci_period: int = 20, constant: float = 0.015,
                   overbought: float = 100, oversold: float = -100,
                   price_type: PriceType = PriceType.CLOSE):
    """
    Applies CCI rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        cci_period (int): CCI calculation period
        constant (float): CCI constant
        overbought (float): Overbought threshold
        oversold (float): Oversold threshold
        price_type (PriceType): Price type to use for CCI calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with CCI calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate CCI
    df['CCI'] = calculate_cci(price_series, cci_period, constant)
    
    # Add price type info to column name
    df['CCI_Price_Type'] = price_name
    
    # Calculate CCI signals
    df['CCI_Signal'] = calculate_cci_signals(df['CCI'], overbought, oversold)
    
    # Calculate support and resistance levels based on CCI
    volatility_factor = 0.02  # 2% volatility assumption
    
    # Support level (when CCI is oversold, expect price to bounce up)
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level (when CCI is overbought, expect price to fall)
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['CCI_Signal']
    df['Diff'] = df['CCI']  # Use CCI value as difference indicator
    
    return df
