# -*- coding: utf-8 -*-
# src/ml/feature_engineering/__init__.py

"""
Feature Engineering module for NeoZork HLD Prediction.

This module provides comprehensive feature engineering capabilities:
- Automatic generation of 100+ technical indicators as features
- Proprietary PHLD and Wave indicator features
- Multi-timeframe feature analysis
- Statistical and temporal feature creation
- Feature selection and importance analysis
"""

from .feature_generator import FeatureGenerator
from .technical_features import TechnicalFeatureGenerator
from .statistical_features import StatisticalFeatureGenerator
from .temporal_features import TemporalFeatureGenerator
from .cross_timeframe_features import CrossTimeframeFeatureGenerator
from .feature_selector import FeatureSelector
from .proprietary_features import ProprietaryFeatureGenerator

__all__ = [
    'FeatureGenerator',
    'TechnicalFeatureGenerator', 
    'StatisticalFeatureGenerator',
    'TemporalFeatureGenerator',
    'CrossTimeframeFeatureGenerator',
    'FeatureSelector',
    'ProprietaryFeatureGenerator'
]
