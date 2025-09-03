#!/usr/bin/env python3
"""
Data Quality Analysis package.

This package provides comprehensive data quality analysis capabilities
for financial data including NaN analysis, outliers, data types,
missing values, and consistency checks.
"""

from .base_quality_analyzer import DataQualityAnalyzer
from .nan_analyzer import NanAnalyzer
from .outlier_analyzer import OutlierAnalyzer
from .data_type_analyzer import DataTypeAnalyzer
from .missing_values_analyzer import MissingValuesAnalyzer
from .consistency_analyzer import ConsistencyAnalyzer

__all__ = [
    'DataQualityAnalyzer',
    'NanAnalyzer',
    'OutlierAnalyzer',
    'DataTypeAnalyzer',
    'MissingValuesAnalyzer',
    'ConsistencyAnalyzer'
]

# Version info
__version__ = "1.0.0"
