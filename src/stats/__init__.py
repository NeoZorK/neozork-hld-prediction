"""
Statistics Analysis Module

This module provides comprehensive statistical analysis capabilities for financial data.
It includes descriptive statistics, distribution analysis, and data transformation features.

Modules:
- descriptive_stats: Basic statistical measures and data distribution analysis
- distribution_analysis: Normality tests, skewness, kurtosis analysis
- data_transformation: Data transformation methods (log, sqrt, box-cox, etc.)
- file_operations: File I/O operations for different data formats
- cli_interface: Command-line interface for statistical analysis
- reporting: Detailed reporting and result presentation

Usage:
    from statistics import StatisticalAnalyzer
    
    analyzer = StatisticalAnalyzer()
    results = analyzer.analyze_file("data/sample.parquet")
"""

__version__ = "1.0.0"
__author__ = "Neozork Team"

from .descriptive_stats import DescriptiveStatistics
from .distribution_analysis import DistributionAnalysis
from .data_transformation import DataTransformation
from .file_operations import StatisticsFileOperations
from .cli_interface import StatisticsCLI
from .reporting import StatisticsReporter

__all__ = [
    'DescriptiveStatistics',
    'DistributionAnalysis', 
    'DataTransformation',
    'StatisticsFileOperations',
    'StatisticsCLI',
    'StatisticsReporter'
]
