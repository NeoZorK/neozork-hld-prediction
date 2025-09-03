# -*- coding: utf-8 -*-
# src/interactive/eda/feature_importance/__init__.py
#!/usr/bin/env python3
"""
Feature Importance Analysis package.

This package provides comprehensive feature importance analysis capabilities
for financial data including ranking, visualization, and insights.
"""

from .base_feature_importance_analyzer import FeatureImportanceAnalyzer
from .ranking_analyzer import RankingAnalyzer
from .visualization_analyzer import VisualizationAnalyzer
from .insights_analyzer import InsightsAnalyzer

__all__ = [
    'FeatureImportanceAnalyzer',
    'RankingAnalyzer',
    'VisualizationAnalyzer',
    'InsightsAnalyzer'
]

# Version info
__version__ = "1.0.0"
