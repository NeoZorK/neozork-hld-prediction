# -*- coding: utf-8 -*-
"""
EDA Analysis module for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive exploratory data analysis tools.
"""

from .data_quality_analyzer import DataQualityAnalyzer
from .statistical_analyzer import StatisticalAnalyzer
from .visualization_analyzer import VisualizationAnalyzer
from .report_generator import ReportGenerator

class EDAAnalyzer:
    """Main EDA analyzer class."""
    def __init__(self):
        self.data_quality = DataQualityAnalyzer()
        self.statistical = StatisticalAnalyzer()
        self.visualization = VisualizationAnalyzer()
        self.report_generator = ReportGenerator()

__all__ = [
    'EDAAnalyzer',
    'DataQualityAnalyzer',
    'StatisticalAnalyzer',
    'VisualizationAnalyzer',
    'ReportGenerator'
]
