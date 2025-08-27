"""
Interactive System Package for NeoZorK HLD Prediction

This package provides an interactive interface for the entire system,
including EDA, Feature Engineering, and other capabilities.
"""

from .core import InteractiveSystem
from .menu_manager import MenuManager
from .data_manager import DataManager
from .analysis_runner import AnalysisRunner
from .visualization_manager import VisualizationManager
from .feature_engineering_manager import FeatureEngineeringManager

__all__ = [
    'InteractiveSystem',
    'MenuManager', 
    'DataManager',
    'AnalysisRunner',
    'VisualizationManager',
    'FeatureEngineeringManager'
]

__version__ = '1.0.0'
