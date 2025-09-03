# -*- coding: utf-8 -*-
# src/interactive/eda/base/base_analyzer.py
#!/usr/bin/env python3
"""
Base EDA Analyzer module.

This module provides the main interface for all EDA operations,
delegating specific analysis tasks to specialized analyzer classes.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from pathlib import Path
import warnings

# Import specialized analyzers
from ..duplicates import DuplicatesAnalyzer
from ..statistics import StatisticsAnalyzer
from ..correlation import CorrelationAnalyzer
from ..time_series import TimeSeriesAnalyzer
from ..feature_importance import FeatureImportanceAnalyzer
from ..data_quality import DataQualityAnalyzer

# Import base classes
from .core_methods import CoreMethods
from .delegation_methods import DelegationMethods


class EDAAnalyzer(CoreMethods, DelegationMethods):
    """
    Main EDA Analyzer class that orchestrates all analysis operations.
    
    This class provides a unified interface for:
    - Basic statistics and data quality checks
    - Duplicates analysis and fixing
    - Time series analysis
    - Correlation analysis
    - Feature importance analysis
    """
    
    def __init__(self):
        """Initialize the EDA Analyzer with specialized analyzers."""
        self.duplicates_analyzer = DuplicatesAnalyzer()
        self.statistics_analyzer = StatisticsAnalyzer()
        self.correlation_analyzer = CorrelationAnalyzer()
        self.time_series_analyzer = TimeSeriesAnalyzer()
        self.feature_importance_analyzer = FeatureImportanceAnalyzer()
        self.data_quality_analyzer = DataQualityAnalyzer()
        
        # Suppress warnings for cleaner output
        warnings.filterwarnings('ignore', category=FutureWarning)
        warnings.filterwarnings('ignore', category=UserWarning)
    
    def run_basic_statistics(self, system) -> bool:
        """
        Run basic statistics analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.statistics_analyzer.run_basic_statistics(system)
    
    def run_duplicates_analysis(self, system) -> bool:
        """
        Run duplicates analysis with fixing option.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.duplicates_analyzer.run_duplicates_analysis(system)
    
    def run_correlation_analysis(self, system) -> bool:
        """
        Run correlation analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.correlation_analyzer.run_correlation_analysis(system)
    
    def run_time_series_analysis(self, system) -> bool:
        """
        Run time series analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.time_series_analyzer.run_time_series_analysis(system)
    
    def run_feature_importance_analysis(self, system) -> bool:
        """
        Run feature importance analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.feature_importance_analyzer.run_feature_importance_analysis(system)
    
    def run_comprehensive_data_quality_check(self, system) -> bool:
        """
        Run comprehensive data quality check.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.data_quality_analyzer.run_comprehensive_data_quality_check(system)
