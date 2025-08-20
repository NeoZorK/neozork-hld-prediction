# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/adx_ind.py

"""
INDICATOR INFO:
Name: ADX
Category: Trend
Description: Average Directional Index. Measures the strength of a trend regardless of direction.
Usage: --rule adx(14) or --rule adx(14,close)
Parameters: period, price_type
Pros: + Measures trend strength, + Works in all markets, + Good for trend confirmation
Cons: - Lagging indicator, - May give false signals in choppy markets, - Requires trend identification
File: src/calculation/indicators/trend/adx_ind.py

ADX (Average Directional Index) indicator calculation module.
"""

import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_adx(df: pd.DataFrame, period: int = 14) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculates ADX (ADX, +DI, -DI).
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        period (int): ADX calculation period (default: 14)
    
    Returns:
        tuple: (adx_values, plus_di, minus_di)
    """
    if period <= 0:
        raise ValueError("ADX period must be positive")
    
    if len(df) < period + 1:
        logger.print_warning(f"Not enough data for ADX calculation. Need at least {period + 1} points, got {len(df)}")
        return pd.Series(index=df.index, dtype=float), pd.Series(index=df.index, dtype=float), pd.Series(index=df.index, dtype=float)
    
    high_prices = df['High']
    low_prices = df['Low']
    close_prices = df['Close']
    
    # Calculate True Range (TR)
    tr1 = high_prices - low_prices
    tr2 = abs(high_prices - close_prices.shift(1))
    tr3 = abs(low_prices - close_prices.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Calculate Directional Movement
    up_move = high_prices - high_prices.shift(1)
    down_move = low_prices.shift(1) - low_prices
    
    # +DM and -DM
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
    
    # Smooth TR, +DM, -DM
    tr_smooth = tr.rolling(window=period).mean()
    plus_dm_smooth = pd.Series(plus_dm, index=df.index).rolling(window=period).mean()
    minus_dm_smooth = pd.Series(minus_dm, index=df.index).rolling(window=period).mean()
    
    # Calculate +DI and -DI
    plus_di = 100 * (plus_dm_smooth / tr_smooth)
    minus_di = 100 * (minus_dm_smooth / tr_smooth)
    
    # Calculate DX
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    
    # Calculate ADX
    adx = dx.rolling(window=period).mean()
    
    return adx, plus_di, minus_di


def calculate_adx_signals(adx_values: pd.Series, plus_di: pd.Series, minus_di: pd.Series,
                         adx_threshold: float = 25) -> pd.Series:
    """
    Calculate trading signals based on ADX and DI values.
    
    Args:
        adx_values (pd.Series): ADX values
        plus_di (pd.Series): +DI values
        minus_di (pd.Series): -DI values
        adx_threshold (float): ADX threshold for trend strength (default: 25)
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=adx_values.index)
    
    # BUY signal: Strong trend (+DI > -DI) and ADX above threshold
    buy_condition = (plus_di > minus_di) & (adx_values > adx_threshold) & (plus_di > plus_di.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Strong trend (-DI > +DI) and ADX above threshold
    sell_condition = (minus_di > plus_di) & (adx_values > adx_threshold) & (minus_di > minus_di.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_adx(df: pd.DataFrame, point: float, 
                   adx_period: int = 14, adx_threshold: float = 25,
                   price_type: PriceType = PriceType.CLOSE):
    """
    Applies ADX rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        adx_period (int): ADX calculation period
        adx_threshold (float): ADX threshold for trend strength
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with ADX calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate ADX
    adx_values, plus_di, minus_di = calculate_adx(df, adx_period)
    
    df['ADX'] = adx_values
    df['ADX_PlusDI'] = plus_di
    df['ADX_MinusDI'] = minus_di
    
    # Add price type info to column name
    df['ADX_Price_Type'] = price_name
    
    # Calculate ADX signals
    df['ADX_Signal'] = calculate_adx_signals(adx_values, plus_di, minus_di, adx_threshold)
    
    # Calculate support and resistance levels based on ADX
    # Use ADX strength to determine volatility
    volatility_factor = 0.02 + (adx_values / 100) * 0.03  # Base 2% + ADX adjustment
    
    # Support level: Open price minus volatility
    support_levels = open_prices * (1 - volatility_factor)
    
    # Resistance level: Open price plus volatility
    resistance_levels = open_prices * (1 + volatility_factor)
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['ADX_Signal']
    df['Diff'] = plus_di - minus_di  # Use DI difference as difference indicator
    
    return df
