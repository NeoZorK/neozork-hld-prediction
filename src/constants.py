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
    Tick_Volume_Limit = 2
    Pressure_Vector = 3
    Pressure_Vector_TakeProfit = 4
    Pressure_Vector_TakeProfit2 = 5
    Pressure_Vector_TakeProfit3 = 6
    PV_Plus_Pressure = 7
    LWMA = 8
    CORE1 = 9