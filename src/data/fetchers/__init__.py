# src/data/fetchers/__init__.py

"""
Makes data fetching functions available for import.
"""

# Import functions from specific fetcher modules
from .demo_fetcher import get_demo_data # Correct function name
from .csv_fetcher import fetch_csv_data
from .yfinance_fetcher import fetch_yfinance_data
from .polygon_fetcher import fetch_polygon_data
from .binance_fetcher import fetch_binance_data

# Define __all__ to control what `from src.data.fetchers import *` imports
# and to clearly state the public interface of this package.
__all__ = [
    'get_demo_data', # Correct function name
    'fetch_csv_data',
    'fetch_yfinance_data',
    'fetch_polygon_data',
    'fetch_binance_data',
]
