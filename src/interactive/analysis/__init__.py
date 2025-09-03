# -*- coding: utf-8 -*-
# src/interactive/analysis/__init__.py
"""
Analysis and processing components for interactive analysis.

This module provides:
- Data analysis execution
- Feature engineering
- Statistical analysis
- Data quality assessment
"""

from .analysis_runner import AnalysisRunner
from .feature_engineering_manager import FeatureEngineeringManager

__all__ = [
    'AnalysisRunner',
    'FeatureEngineeringManager'
]
