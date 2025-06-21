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
