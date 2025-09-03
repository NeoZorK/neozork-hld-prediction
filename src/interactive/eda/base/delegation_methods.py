# -*- coding: utf-8 -*-
# src/interactive/eda/base/delegation_methods.py
#!/usr/bin/env python3
"""
Delegation Methods module.

This module provides delegation methods for the EDA Analyzer.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from pathlib import Path
import warnings


class DelegationMethods:
    """
    Delegation methods for the EDA Analyzer.
    
    This class provides methods that delegate to specialized analyzers.
    """
    
    def __init__(self):
        """Initialize the DelegationMethods."""
        pass
    
    def run_summary_statistics(self, system) -> bool:
        """
        Run summary statistics.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.statistics_analyzer.run_summary_statistics(system)
    
    def run_descriptive_statistics(self, system) -> bool:
        """
        Run descriptive statistics.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.statistics_analyzer.run_descriptive_statistics(system)
    
    def run_numerical_analysis(self, system) -> bool:
        """
        Run numerical analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.statistics_analyzer.run_numerical_analysis(system)
    
    def run_categorical_analysis(self, system) -> bool:
        """
        Run categorical analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.statistics_analyzer.run_categorical_analysis(system)
    
    def run_correlation_matrix(self, system) -> bool:
        """
        Run correlation matrix analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.correlation_analyzer.run_correlation_matrix(system)
    
    def run_correlation_heatmap(self, system) -> bool:
        """
        Run correlation heatmap analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.correlation_analyzer.run_correlation_heatmap(system)
    
    def run_correlation_insights(self, system) -> bool:
        """
        Run correlation insights analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.correlation_analyzer.run_correlation_insights(system)
    
    def run_time_series_trends(self, system) -> bool:
        """
        Run time series trends analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.time_series_analyzer.run_time_series_trends(system)
    
    def run_time_series_seasonality(self, system) -> bool:
        """
        Run time series seasonality analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.time_series_analyzer.run_time_series_seasonality(system)
    
    def run_time_series_stationarity(self, system) -> bool:
        """
        Run time series stationarity analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.time_series_analyzer.run_time_series_stationarity(system)
    
    def run_feature_importance_ranking(self, system) -> bool:
        """
        Run feature importance ranking analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.feature_importance_analyzer.run_feature_importance_ranking(system)
    
    def run_feature_importance_visualization(self, system) -> bool:
        """
        Run feature importance visualization.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.feature_importance_analyzer.run_feature_importance_visualization(system)
    
    def run_feature_importance_insights(self, system) -> bool:
        """
        Run feature importance insights analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.feature_importance_analyzer.run_feature_importance_insights(system)
