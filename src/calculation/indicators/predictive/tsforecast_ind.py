# -*- coding: utf-8 -*-
# src/calculation/indicators/predictive/tsforecast_ind.py

"""
INDICATOR INFO:
Name: Time Series Forecast
Category: Predictive
Description: Time Series Forecast. Uses linear regression to predict future price movements.
Usage: --rule tsforecast(14) or --rule tsforecast(14,close)
Parameters: period, price_type
Pros: + Provides price predictions, + Based on statistical methods, + Good for trend analysis
Cons: - Assumes linear relationships, - May not work in volatile markets, - Requires stable trends
File: src/calculation/indicators/predictive/tsforecast_ind.py

Time Series Forecast indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_tsforecast(price_series: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculates Time Series Forecast using linear regression.
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        period (int): Forecast period (default: 14)
    
    Returns:
        pd.Series: Forecast values
    """
    if period <= 0:
        raise ValueError("TSForecast period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"Not enough data for TSForecast calculation. Need at least {period} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    forecast_values = pd.Series(index=price_series.index, dtype=float)
    
    for i in range(period, len(price_series)):
        # Get the window of data
        window = price_series.iloc[i-period:i]
        
        # Create time index for regression
        x = np.arange(len(window))
        y = window.values
        
        # Simple linear regression
        if len(y) > 1:
            slope, intercept = np.polyfit(x, y, 1)
            # Forecast next value
            forecast = slope * len(window) + intercept
            forecast_values.iloc[i] = forecast
        else:
            forecast_values.iloc[i] = y[0] if len(y) == 1 else np.nan
    
    return forecast_values


def calculate_tsforecast_signals(price_series: pd.Series, forecast_values: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on price vs forecast.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        forecast_values (pd.Series): Forecast values
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price is below forecast (expecting rise)
    buy_condition = (price_series < forecast_values) & (forecast_values > forecast_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Price is above forecast (expecting fall)
    sell_condition = (price_series > forecast_values) & (forecast_values < forecast_values.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_tsforecast(df: pd.DataFrame, point: float, 
                          tsforecast_period: int = 14, price_type: PriceType = PriceType.CLOSE):
    """
    Applies Time Series Forecast rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        tsforecast_period (int): Forecast period
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with TSForecast calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate TSForecast
    df['TSForecast'] = calculate_tsforecast(price_series, tsforecast_period)
    
    # Add price type info to column name
    df['TSForecast_Price_Type'] = price_name
    
    # Calculate TSForecast signals
    df['TSForecast_Signal'] = calculate_tsforecast_signals(price_series, df['TSForecast'])
    
    # Calculate support and resistance levels based on TSForecast
    forecast_values = df['TSForecast']
    
    # Support level: Forecast with small buffer
    support_levels = forecast_values * 0.995  # 0.5% below forecast
    
    # Resistance level: Forecast with small buffer
    resistance_levels = forecast_values * 1.005  # 0.5% above forecast
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['TSForecast_Signal']
    df['Diff'] = price_series - forecast_values  # Use price - forecast as difference indicator
    
    return df
