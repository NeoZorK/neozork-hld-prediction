#!/usr/bin/env python3
"""
EDA (Exploratory Data Analysis) package.

This package provides comprehensive data analysis capabilities including:
- Basic statistics and data quality checks
- Duplicates analysis and fixing
- Time series analysis
- Correlation analysis
- Feature importance analysis
- Data visualization
"""

from .base import EDAAnalyzer
from .duplicates import DuplicatesAnalyzer
from .statistics import StatisticsAnalyzer
from .correlation import CorrelationAnalyzer
from .time_series import TimeSeriesAnalyzer
from .feature_importance import FeatureImportanceAnalyzer
from .data_quality import DataQualityAnalyzer

__all__ = [
    'EDAAnalyzer',
    'DuplicatesAnalyzer', 
    'StatisticsAnalyzer',
    'CorrelationAnalyzer',
    'TimeSeriesAnalyzer',
    'FeatureImportanceAnalyzer',
    'DataQualityAnalyzer'
]

# Version info
__version__ = "2.0.0"
