# -*- coding: utf-8 -*-
"""
Feature Engineering module for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive feature engineering tools.
"""

from .technical_indicators import TechnicalIndicators
from .premium_indicators import PremiumIndicators
from .statistical_features import StatisticalFeatures
from .temporal_features import TemporalFeatures
from .cross_timeframe_features import CrossTimeframeFeatures
from .feature_selector import FeatureSelector

class FeatureEngineer:
    """Main feature engineering class."""
    def __init__(self):
        self.technical_indicators = TechnicalIndicators()
        self.premium_indicators = PremiumIndicators()
        self.statistical_features = StatisticalFeatures()
        self.temporal_features = TemporalFeatures()
        self.cross_timeframe_features = CrossTimeframeFeatures()
        self.feature_selector = FeatureSelector()

__all__ = [
    'FeatureEngineer',
    'TechnicalIndicators',
    'PremiumIndicators',
    'StatisticalFeatures',
    'TemporalFeatures',
    'CrossTimeframeFeatures',
    'FeatureSelector'
]
