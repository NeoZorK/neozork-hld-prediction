# -*- coding: utf-8 -*-
# src/interactive/eda/base/core_methods.py
#!/usr/bin/env python3
"""
Core Methods module.

This module provides core analysis methods for the EDA Analyzer.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from pathlib import Path
import warnings


class CoreMethods:
    """
    Core analysis methods for the EDA Analyzer.
    
    This class provides the main analysis methods that are used
    by the EDAAnalyzer class.
    """
    
    def __init__(self):
        """Initialize the CoreMethods."""
        pass
    
    def run_time_series_gaps_analysis(self, system) -> bool:
        """
        Run time series gaps analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.time_series_analyzer.run_time_series_gaps_analysis(system)
    
    def run_nan_analysis(self, system) -> bool:
        """
        Run NaN analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.data_quality_analyzer.run_nan_analysis(system)
    
    def run_outlier_analysis(self, system) -> bool:
        """
        Run outlier analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.data_quality_analyzer.run_outlier_analysis(system)
    
    def run_data_type_analysis(self, system) -> bool:
        """
        Run data type analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.data_quality_analyzer.run_data_type_analysis(system)
    
    def run_missing_values_analysis(self, system) -> bool:
        """
        Run missing values analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.data_quality_analyzer.run_missing_values_analysis(system)
    
    def run_data_consistency_check(self, system) -> bool:
        """
        Run data consistency check.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.data_quality_analyzer.run_data_consistency_check(system)
    
    def run_data_distribution_analysis(self, system) -> bool:
        """
        Run data distribution analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return system.statistics_analyzer.run_data_distribution_analysis(system)
