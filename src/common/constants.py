# -*- coding: utf-8 -*-
# src/constants.py

"""
Constants and enumerations used in the indicator calculations.
"""

import numpy as np
from enum import Enum

# --- Define constants for signals ---
NOTRADE = 0.0
BUY = 1.0
SELL = 2.0
DBL_BUY = 3.0       # Not used in core calculations shown, but defined for completeness
DBL_SELL = 4.0      # Not used in core calculations shown, but defined for completeness
BUY_AND_SELL = 5.0 # Not used in core calculations shown, but defined for completeness
EMPTY_VALUE = np.nan

# --- Define Enum for Trading Rule Switch ---
class TradingRule(Enum):
    PV_HighLow = 0
    Support_Resistants = 1
    Pressure_Vector = 2
    Predict_High_Low_Direction = 3
    OHLCV = 4  # Raw OHLCV data without indicator calculation
    AUTO = 5  # Auto mode for automatic columns selection based on data availability
    RSI = 6  # RSI indicator with overbought/oversold signals
    RSI_Momentum = 7  # RSI momentum-based signals
    RSI_Divergence = 8  # RSI divergence detection
    # New indicators with price_type support
    CCI = 9  # Commodity Channel Index
    Stochastic = 10  # Stochastic Oscillator
    EMA = 11  # Exponential Moving Average
    SMA = 12  # Simple Moving Average
    Bollinger_Bands = 13  # Bollinger Bands
    ATR = 14  # Average True Range
    VWAP = 15  # Volume Weighted Average Price
    Pivot_Points = 16  # Pivot Points
    # Momentum indicators
    MACD = 17  # Moving Average Convergence Divergence
    StochOscillator = 18  # Stochastic Oscillator (momentum)
    # Predictive indicators
    HMA = 19  # Hull Moving Average
    TSForecast = 20  # Time Series Forecast
    # Probability indicators
    MonteCarlo = 21  # Monte Carlo Simulation
    Kelly = 22  # Kelly Criterion
    # Sentiment indicators
    FearGreed = 23  # Fear & Greed Index
    COT = 24  # Commitment of Traders
    PutCallRatio = 25  # Put/Call Ratio
    # Support/Resistance indicators
    Donchain = 26  # Donchian Channel
    FiboRetr = 27  # Fibonacci Retracement
    # Volume indicators
    OBV = 28  # On Balance Volume
    # Volatility indicators
    StDev = 29  # Standard Deviation
    # Trend indicators
    ADX = 30  # Average Directional Index
    SAR = 31  # Parabolic SAR
    SuperTrend = 32  # SuperTrend
    Wave = 33 # Wave
