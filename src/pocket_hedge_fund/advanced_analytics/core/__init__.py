"""
Core Analytics Components

This module contains the fundamental analytics components:
- AnalyticsEngine: Main orchestrator for analytics operations
- DataProcessor: Handles data cleaning, transformation, and preparation
- FeatureEngineer: Creates and manages features for ML models
- InsightGenerator: Generates actionable insights from analytics results
"""

from .analytics_engine import AnalyticsEngine
from .data_processor import DataProcessor
from .feature_engineer import FeatureEngineer
from .insight_generator import InsightGenerator

__all__ = [
    "AnalyticsEngine",
    "DataProcessor",
    "FeatureEngineer", 
    "InsightGenerator"
]
