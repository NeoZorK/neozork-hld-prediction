# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/sar_ind.py

"""
INDICATOR INFO:
Name: SAR
Category: Trend
Description: Parabolic SAR. Shows potential reversal points in price trends.
Usage: --rule sar(0.02,0.2) or --rule sar(0.02,0.2,close)
Parameters: acceleration, maximum, price_type
Pros: + Shows trend reversals, + Good for stop-loss placement, + Works in trending markets
Cons: - Can give false signals in sideways markets, - May lag in fast markets, - Sensitive to parameters
File: src/calculation/indicators/trend/sar_ind.py

SAR (Parabolic SAR) indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_sar(df: pd.DataFrame, acceleration: float = 0.02, maximum: float = 0.2) -> pd.Series:
    """
    Calculates Parabolic SAR.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        acceleration (float): Acceleration factor (default: 0.02)
        maximum (float): Maximum acceleration (default: 0.2)
    
    Returns:
        pd.Series: SAR values
    """
    if acceleration <= 0 or maximum <= 0:
        raise ValueError("Acceleration and maximum must be positive")
    
    if len(df) < 2:
        logger.print_warning("Not enough data for SAR calculation. Need at least 2 points")
        return pd.Series(index=df.index, dtype=float)
    
    high_prices = df['High']
    low_prices = df['Low']
    
    # Initialize SAR
    sar = pd.Series(index=df.index, dtype=float)
    ep = pd.Series(index=df.index, dtype=float)  # Extreme Point
    af = pd.Series(index=df.index, dtype=float)  # Acceleration Factor
    trend = pd.Series(index=df.index, dtype=int)  # 1 for uptrend, -1 for downtrend
    
    # Initialize first values
    sar.iloc[0] = low_prices.iloc[0]
    ep.iloc[0] = high_prices.iloc[0]
    af.iloc[0] = acceleration
    trend.iloc[0] = 1  # Start with uptrend
    
    # Calculate SAR
    for i in range(1, len(df)):
        if trend.iloc[i-1] == 1:  # Uptrend
            # Check if trend continues
            if high_prices.iloc[i] > ep.iloc[i-1]:
                # Trend continues
                ep.iloc[i] = high_prices.iloc[i]
                af.iloc[i] = min(af.iloc[i-1] + acceleration, maximum)
                trend.iloc[i] = 1
            else:
                # Trend reverses
                ep.iloc[i] = low_prices.iloc[i]
                af.iloc[i] = acceleration
                trend.iloc[i] = -1
            
            # Calculate SAR for uptrend
            sar.iloc[i] = sar.iloc[i-1] + af.iloc[i-1] * (ep.iloc[i-1] - sar.iloc[i-1])
            
            # SAR should not be above the previous low
            if sar.iloc[i] > low_prices.iloc[i-1]:
                sar.iloc[i] = low_prices.iloc[i-1]
            
            # SAR should not be above the current low
            if sar.iloc[i] > low_prices.iloc[i]:
                sar.iloc[i] = low_prices.iloc[i]
                
        else:  # Downtrend
            # Check if trend continues
            if low_prices.iloc[i] < ep.iloc[i-1]:
                # Trend continues
                ep.iloc[i] = low_prices.iloc[i]
                af.iloc[i] = min(af.iloc[i-1] + acceleration, maximum)
                trend.iloc[i] = -1
            else:
                # Trend reverses
                ep.iloc[i] = high_prices.iloc[i]
                af.iloc[i] = acceleration
                trend.iloc[i] = 1
            
            # Calculate SAR for downtrend
            sar.iloc[i] = sar.iloc[i-1] + af.iloc[i-1] * (ep.iloc[i-1] - sar.iloc[i-1])
            
            # SAR should not be below the previous high
            if sar.iloc[i] < high_prices.iloc[i-1]:
                sar.iloc[i] = high_prices.iloc[i-1]
            
            # SAR should not be below the current high
            if sar.iloc[i] < high_prices.iloc[i]:
                sar.iloc[i] = high_prices.iloc[i]
    
    return sar


def calculate_sar_signals(price_series: pd.Series, sar_values: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on SAR.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        sar_values (pd.Series): SAR values
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price crosses above SAR
    buy_condition = (price_series > sar_values) & (price_series.shift(1) <= sar_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Price crosses below SAR
    sell_condition = (price_series < sar_values) & (price_series.shift(1) >= sar_values.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_sar(df: pd.DataFrame, point: float, 
                   sar_acceleration: float = 0.02, sar_maximum: float = 0.2,
                   price_type: PriceType = PriceType.CLOSE):
    """
    Applies SAR rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        sar_acceleration (float): Acceleration factor
        sar_maximum (float): Maximum acceleration
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with SAR calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate SAR
    df['SAR'] = calculate_sar(df, sar_acceleration, sar_maximum)
    
    # Add price type info to column name
    df['SAR_Price_Type'] = price_name
    
    # Calculate SAR signals
    df['SAR_Signal'] = calculate_sar_signals(price_series, df['SAR'])
    
    # Use SAR as dynamic support/resistance levels
    sar_values = df['SAR']
    
    # Support level: SAR with small buffer
    support_levels = sar_values * 0.995  # 0.5% below SAR
    
    # Resistance level: SAR with small buffer
    resistance_levels = sar_values * 1.005  # 0.5% above SAR
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['SAR_Signal']
    df['Diff'] = price_series - sar_values  # Use price - SAR as difference indicator
    
    return df
