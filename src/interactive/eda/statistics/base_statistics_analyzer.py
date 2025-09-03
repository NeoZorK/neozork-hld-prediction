# -*- coding: utf-8 -*-
# src/interactive/eda/statistics/base_statistics_analyzer.py
#!/usr/bin/env python3
"""
Base Statistics Analyzer module.

This module provides the main interface for statistical analysis,
orchestrating calls to specialized analyzers.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import warnings

# Import specialized analyzers
from .basic_statistics import BasicStatistics
from .distribution_analysis import DistributionAnalysis
from .summary_statistics import SummaryStatistics
from .descriptive_statistics import DescriptiveStatistics
from .numerical_analysis import NumericalAnalysis
from .categorical_analysis import CategoricalAnalysis


class StatisticsAnalyzer:
    """
    Main Statistics Analyzer class that orchestrates all statistical analysis operations.
    
    This class provides a unified interface for:
    - Basic statistics
    - Data distribution analysis
    - Summary statistics
    - Descriptive statistics
    - Numerical analysis
    - Categorical analysis
    """
    
    def __init__(self):
        """Initialize the Statistics Analyzer with specialized analyzers."""
        self.basic_statistics = BasicStatistics()
        self.distribution_analysis = DistributionAnalysis()
        self.summary_statistics = SummaryStatistics()
        self.descriptive_statistics = DescriptiveStatistics()
        self.numerical_analysis = NumericalAnalysis()
        self.categorical_analysis = CategoricalAnalysis()
        
        # Suppress warnings for cleaner output
        warnings.filterwarnings('ignore', category=FutureWarning)
        warnings.filterwarnings('ignore', category=UserWarning)
    
    def run_basic_statistics(self, system) -> bool:
        """
        Run basic statistics analysis on the loaded data.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.basic_statistics.run_basic_statistics(system)
    
    def run_data_distribution_analysis(self, system) -> bool:
        """
        Run data distribution analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.distribution_analysis.run_data_distribution_analysis(system)
    
    def run_summary_statistics(self, system) -> bool:
        """
        Run summary statistics analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.summary_statistics.run_summary_statistics(system)
    
    def run_descriptive_statistics(self, system) -> bool:
        """
        Run descriptive statistics analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.descriptive_statistics.run_descriptive_statistics(system)
    
    def run_numerical_analysis(self, system) -> bool:
        """
        Run numerical analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.numerical_analysis.run_numerical_analysis(system)
    
    def run_categorical_analysis(self, system) -> bool:
        """
        Run categorical analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.categorical_analysis.run_categorical_analysis(system)
