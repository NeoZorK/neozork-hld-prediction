#!/usr/bin/env python3
"""
Correlation Analysis package.

This module provides comprehensive correlation analysis capabilities
for financial time series data including correlation matrices,
heatmaps, and insights.
"""

from .base_correlation_analyzer import CorrelationAnalyzer
from .matrix_analyzer import MatrixAnalyzer
from .heatmap_analyzer import HeatmapAnalyzer
from .insights_analyzer import InsightsAnalyzer

__all__ = [
    'CorrelationAnalyzer',
    'MatrixAnalyzer',
    'HeatmapAnalyzer',
    'InsightsAnalyzer'
]

# Version info
__version__ = "1.0.0"
