# -*- coding: utf-8 -*-
# src/calculation/indicators/probability/montecarlo_ind.py

"""
INDICATOR INFO:
Name: Monte Carlo
Category: Probability
Description: Monte Carlo Simulation. Uses random sampling to estimate probability distributions of price movements.
Usage: --rule montecarlo(1000,20) or --rule montecarlo(1000,20,close)
Parameters: simulations, period, price_type
Pros: + Provides probability estimates, + Based on statistical methods, + Good for risk assessment
Cons: - Computationally intensive, - Results may vary, - Requires sufficient historical data
File: src/calculation/indicators/probability/montecarlo_ind.py

Monte Carlo indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_montecarlo(price_series: pd.Series, simulations: int = 1000, period: int = 20) -> pd.Series:
    """
    Calculates Monte Carlo simulation results.
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        simulations (int): Number of simulations (default: 1000)
        period (int): Forecast period (default: 20)
    
    Returns:
        pd.Series: Monte Carlo forecast values
    """
    if simulations <= 0 or period <= 0:
        raise ValueError("Simulations and period must be positive")
    
    if len(price_series) < 10:
        logger.print_warning(f"Not enough data for Monte Carlo calculation. Need at least 10 points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate returns
    returns = price_series.pct_change(fill_method=None).dropna()
    
    if len(returns) < 5:
        logger.print_warning("Not enough return data for Monte Carlo simulation")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate mean and standard deviation of returns
    mean_return = returns.mean()
    std_return = returns.std()
    
    # Initialize result series
    mc_forecast = pd.Series(index=price_series.index, dtype=float)
    
    # For each point, run Monte Carlo simulation
    for i in range(period, len(price_series)):
        current_price = price_series.iloc[i-1]
        
        # Run simulations
        simulated_prices = []
        for _ in range(simulations):
            # Generate random returns
            random_returns = np.random.normal(mean_return, std_return, period)
            # Calculate simulated price
            simulated_price = current_price * np.prod(1 + random_returns)
            simulated_prices.append(simulated_price)
        
        # Use median of simulations as forecast
        mc_forecast.iloc[i] = np.median(simulated_prices)
    
    return mc_forecast


def calculate_montecarlo_signal_line(mc_forecast: pd.Series, signal_period: int = 9) -> pd.Series:
    """
    Calculate signal line for Monte Carlo (EMA of forecast).
    
    Args:
        mc_forecast (pd.Series): Monte Carlo forecast values
        signal_period (int): Period for signal line EMA
    
    Returns:
        pd.Series: Signal line values
    """
    if signal_period <= 0:
        raise ValueError("Signal period must be positive")
    
    # Calculate EMA of the forecast
    signal_line = mc_forecast.ewm(span=signal_period, adjust=False).mean()
    return signal_line


def calculate_montecarlo_histogram(mc_forecast: pd.Series, signal_line: pd.Series) -> pd.Series:
    """
    Calculate histogram for Monte Carlo (difference between forecast and signal line).
    
    Args:
        mc_forecast (pd.Series): Monte Carlo forecast values
        signal_line (pd.Series): Signal line values
    
    Returns:
        pd.Series: Histogram values
    """
    histogram = mc_forecast - signal_line
    return histogram


def calculate_montecarlo_confidence_bands(mc_forecast: pd.Series, confidence_level: float = 0.95) -> tuple[pd.Series, pd.Series]:
    """
    Calculate confidence bands for Monte Carlo forecast.
    
    Args:
        mc_forecast (pd.Series): Monte Carlo forecast values
        confidence_level (float): Confidence level (0.95 = 95%)
    
    Returns:
        tuple[pd.Series, pd.Series]: Upper and lower confidence bands
    """
    # Calculate rolling standard deviation of forecast changes
    forecast_changes = mc_forecast.pct_change().rolling(window=20, min_periods=5).std()
    
    # Calculate confidence interval
    z_score = 1.96  # For 95% confidence level
    confidence_interval = z_score * forecast_changes * mc_forecast
    
    upper_band = mc_forecast + confidence_interval
    lower_band = mc_forecast - confidence_interval
    
    return upper_band, lower_band


def calculate_montecarlo_signals(price_series: pd.Series, mc_forecast: pd.Series, signal_line: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on Monte Carlo forecast and signal line.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        mc_forecast (pd.Series): Monte Carlo forecast values
        signal_line (pd.Series): Signal line values
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Forecast crosses above signal line and price is below forecast
    buy_condition = (mc_forecast > signal_line) & (mc_forecast.shift(1) <= signal_line.shift(1)) & (price_series < mc_forecast)
    signals[buy_condition] = BUY
    
    # SELL signal: Forecast crosses below signal line and price is above forecast
    sell_condition = (mc_forecast < signal_line) & (mc_forecast.shift(1) >= signal_line.shift(1)) & (price_series > mc_forecast)
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_montecarlo(df: pd.DataFrame, point: float, 
                          simulations: int = 1000, period: int = 20,
                          price_type: PriceType = PriceType.CLOSE):
    """
    Applies Monte Carlo rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        simulations (int): Number of simulations
        period (int): Forecast period
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with Monte Carlo calculations and signals
    """
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate Monte Carlo forecast
    df['MonteCarlo'] = calculate_montecarlo(price_series, simulations, period)
    
    # Calculate signal line (EMA of forecast)
    df['MonteCarlo_Signal'] = calculate_montecarlo_signal_line(df['MonteCarlo'], signal_period=9)
    
    # Calculate histogram
    df['MonteCarlo_Histogram'] = calculate_montecarlo_histogram(df['MonteCarlo'], df['MonteCarlo_Signal'])
    
    # Calculate confidence bands
    df['MonteCarlo_Upper'], df['MonteCarlo_Lower'] = calculate_montecarlo_confidence_bands(df['MonteCarlo'])
    
    # Add price type info to column name
    df['MonteCarlo_Price_Type'] = price_name
    
    # Calculate Monte Carlo signals
    df['MonteCarlo_Signal_Line'] = calculate_montecarlo_signals(price_series, df['MonteCarlo'], df['MonteCarlo_Signal'])
    
    # Calculate support and resistance levels based on Monte Carlo
    mc_forecast = df['MonteCarlo']
    
    # Support level: Lower confidence band
    support_levels = df['MonteCarlo_Lower']
    
    # Resistance level: Upper confidence band
    resistance_levels = df['MonteCarlo_Upper']
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['MonteCarlo_Signal_Line']
    df['Diff'] = price_series - mc_forecast  # Use price - forecast as difference indicator
    
    return df
