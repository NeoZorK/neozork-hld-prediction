#!/usr/bin/env python3
"""
Interactive system modules for data analysis and visualization.
"""

from .core import InteractiveSystem
from .data_manager import DataManager
from .memory_manager import MemoryManager
from .data_loader import DataLoader
from .gap_analyzer import GapAnalyzer
from .multi_timeframe_manager import MultiTimeframeManager
from .cache_manager import CacheManager
from .eda import EDAAnalyzer
from .data_fixer import DataFixer
from .plot_generator import PlotGenerator
from .html_report_generator import HTMLReportGenerator
from .menu_manager import MenuManager
from .analysis_runner import AnalysisRunner
from .feature_engineering_manager import FeatureEngineeringManager
from .visualization_manager import VisualizationManager

__all__ = [
    'InteractiveSystem',
    'DataManager',
    'MemoryManager',
    'DataLoader',
    'GapAnalyzer',
    'MultiTimeframeManager',
    'CacheManager',
    'EDAAnalyzer',
    'DataFixer',
    'PlotGenerator',
    'HTMLReportGenerator',
    'MenuManager',
    'AnalysisRunner',
    'FeatureEngineeringManager',
    'VisualizationManager'
]

__version__ = '1.0.0'
