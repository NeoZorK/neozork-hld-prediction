# -*- coding: utf-8 -*-
# src/interactive/eda/statistics/__init__.py
#!/usr/bin/env python3
"""
Statistics Analysis package.

This module provides comprehensive statistical analysis capabilities
for financial time series data including basic statistics, distributions,
and numerical/categorical analysis.
"""

from .base_statistics_analyzer import StatisticsAnalyzer
from .basic_statistics import BasicStatistics
from .distribution_analysis import DistributionAnalysis
from .summary_statistics import SummaryStatistics
from .descriptive_statistics import DescriptiveStatistics
from .numerical_analysis import NumericalAnalysis
from .categorical_analysis import CategoricalAnalysis

__all__ = [
    'StatisticsAnalyzer',
    'BasicStatistics',
    'DistributionAnalysis',
    'SummaryStatistics',
    'DescriptiveStatistics',
    'NumericalAnalysis',
    'CategoricalAnalysis'
]

# Version info
__version__ = "1.0.0"
