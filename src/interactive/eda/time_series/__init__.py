# -*- coding: utf-8 -*-
# src/interactive/eda/time_series/__init__.py
#!/usr/bin/env python3
"""
Time Series Analysis package.

This package provides comprehensive time series analysis capabilities
for financial data including gaps analysis, trends, seasonality,
and stationarity.
"""

from .base_time_series_analyzer import TimeSeriesAnalyzer
from .gaps_analyzer import GapsAnalyzer
from .trends_analyzer import TrendsAnalyzer
from .seasonality_analyzer import SeasonalityAnalyzer
from .stationarity_analyzer import StationarityAnalyzer

__all__ = [
    'TimeSeriesAnalyzer',
    'GapsAnalyzer',
    'TrendsAnalyzer',
    'SeasonalityAnalyzer',
    'StationarityAnalyzer'
]

# Version info
__version__ = "1.0.0"
