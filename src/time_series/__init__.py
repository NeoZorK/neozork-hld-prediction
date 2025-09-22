"""
Time Series Analysis Module

This module provides comprehensive time series analysis capabilities for financial data,
including stationarity analysis, seasonality detection, and financial features analysis.

Main Components:
- Stationarity Analysis: ADF tests, critical values, stationarity recommendations
- Seasonality Detection: Day-of-week, monthly, and cyclical patterns
- Financial Features: Price range, price changes, volatility analysis
- Data Transformation: Time series specific transformations

Usage:
    from src.time_series import TimeSeriesAnalyzer
    
    analyzer = TimeSeriesAnalyzer()
    results = analyzer.analyze_file('data.parquet', analysis_options)
"""

__version__ = "1.0.0"
__author__ = "Neozork Team"

# Import main classes
from .file_operations import TimeSeriesFileOperations
from .cli_interface import TimeSeriesCLI
from .stationarity_analysis import StationarityAnalysis
from .seasonality_detection import SeasonalityDetection
from .financial_features import FinancialFeatures
from .data_transformation import TimeSeriesDataTransformation
from .reporting import TimeSeriesReporter
from .color_utils import ColorUtils
from .progress_tracker import ProgressTracker, ProgressBar, ColumnProgressTracker

__all__ = [
    'TimeSeriesFileOperations',
    'TimeSeriesCLI', 
    'StationarityAnalysis',
    'SeasonalityDetection',
    'FinancialFeatures',
    'TimeSeriesDataTransformation',
    'TimeSeriesReporter',
    'ColorUtils',
    'ProgressTracker',
    'ProgressBar',
    'ColumnProgressTracker'
]
