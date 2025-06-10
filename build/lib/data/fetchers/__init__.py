# -*- coding: utf-8 -*-
# src/data/fetchers/__init__.py

"""
Initializes the fetchers package and exposes the main data fetching functions
and necessary mapping utilities for use by data_acquisition.
"""

# Import the main fetch function from each module
from .csv_fetcher import fetch_csv_data
from .demo_fetcher import get_demo_data
from .yfinance_fetcher import fetch_yfinance_data
from .polygon_fetcher import fetch_polygon_data
from .binance_fetcher import fetch_binance_data

# Import specific mapping functions needed by data_acquisition.py
from .yfinance_fetcher import map_yfinance_interval, map_yfinance_ticker

# Define what symbols are exported when 'from .fetchers import *' is used
# (Good practice, though we use direct imports in data_acquisition)
__all__ = [
    'fetch_csv_data',
    'get_demo_data',
    'fetch_yfinance_data',
    'fetch_polygon_data',
    'fetch_binance_data',
    # *** FIX: Update __all__ with the new names ***
    'map_yfinance_interval',  # For yfinance
    'map_yfinance_ticker',    # For yfinance
]