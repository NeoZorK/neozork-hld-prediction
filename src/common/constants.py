# src/common/constants.py

"""
Defines constants used throughout the application, including trading rules,
signal values, and valid data source identifiers.
All comments are in English.
"""

from enum import Enum, auto
import numpy as np # <-- Import numpy

# --- Trading Rules Enum ---
# Defines the different calculation/trading rules available.
class TradingRule(Enum):
    Predict_High_Low_Direction = auto() # Original complex rule
    Pressure_Vector = auto()           # Simpler rule focusing on PV
    Support_Resistants = auto()        # Rule based on S/R levels (potentially derived from PV/Pressure)
    # Add other rules here if needed

# --- Signal Values ---
# Standardized values for trade direction signals.
BUY = 1.0
SELL = 2.0
NOTRADE = 0.0

# --- Placeholder for Empty/Missing Numerical Values ---
EMPTY_VALUE = np.nan # <-- Define EMPTY_VALUE as NaN

# --- Valid Data Sources for API Cache ---
# Used by cache_manager and potentially CLI to validate source names.
# Excludes 'csv' and 'demo' as they have different caching mechanisms or no cache.
VALID_DATA_SOURCES = ['yfinance', 'polygon', 'binance']

# --- Other Constants ---
# Example: Default number of rows for demo data
DEFAULT_DEMO_ROWS = 30

# Example: Default colors (though plotting logic might override)
DEFAULT_PPRICE1_COLOR = 'lime'
DEFAULT_PPRICE2_COLOR = 'red'

