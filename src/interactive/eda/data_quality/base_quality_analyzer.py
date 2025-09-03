# -*- coding: utf-8 -*-
# src/interactive/eda/data_quality/base_quality_analyzer.py
#!/usr/bin/env python3
"""
Base Data Quality Analyzer module.

This module provides the main interface for data quality analysis,
orchestrating calls to specialized analyzers.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import warnings

# Import specialized analyzers
from .nan_analyzer import NanAnalyzer
from .outlier_analyzer import OutlierAnalyzer
from .data_type_analyzer import DataTypeAnalyzer
from .missing_values_analyzer import MissingValuesAnalyzer
from .consistency_analyzer import ConsistencyAnalyzer


class DataQualityAnalyzer:
    """
    Main Data Quality Analyzer class that orchestrates all quality analysis operations.
    
    This class provides a unified interface for:
    - Comprehensive data quality check
    - NaN analysis
    - Outlier analysis
    - Data type analysis
    - Missing values analysis
    - Data consistency check
    """
    
    def __init__(self):
        """Initialize the Data Quality Analyzer with specialized analyzers."""
        self.nan_analyzer = NanAnalyzer()
        self.outlier_analyzer = OutlierAnalyzer()
        self.data_type_analyzer = DataTypeAnalyzer()
        self.missing_values_analyzer = MissingValuesAnalyzer()
        self.consistency_analyzer = ConsistencyAnalyzer()
        
        # Suppress warnings for cleaner output
        warnings.filterwarnings('ignore', category=FutureWarning)
        warnings.filterwarnings('ignore', category=UserWarning)
    
    def run_comprehensive_data_quality_check(self, system) -> bool:
        """
        Run comprehensive data quality check.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🔍 COMPREHENSIVE DATA QUALITY CHECK")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        print(f"📊 Running comprehensive data quality check on {df.shape[0]:,} rows × {df.shape[1]} columns...")
        
        # Run all data quality analyses
        self.run_nan_analysis(system)
        self.run_outlier_analysis(system)
        self.run_data_type_analysis(system)
        self.run_missing_values_analysis(system)
        self.run_data_consistency_check(system)
        
        # Overall quality score
        print(f"\n🎯 OVERALL DATA QUALITY SCORE")
        print("-" * 50)
        
        # Calculate quality metrics
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        quality_score = ((total_cells - missing_cells) / total_cells) * 100
        
        print(f"📊 Data Quality Metrics:")
        print(f"   • Total cells: {total_cells:,}")
        print(f"   • Missing cells: {missing_cells:,}")
        print(f"   • Quality score: {quality_score:.2f}%")
        
        # Quality assessment
        if quality_score >= 95:
            print(f"   • Assessment: Excellent data quality")
        elif quality_score >= 90:
            print(f"   • Assessment: Good data quality")
        elif quality_score >= 80:
            print(f"   • Assessment: Acceptable data quality")
        elif quality_score >= 70:
            print(f"   • Assessment: Poor data quality - needs attention")
        else:
            print(f"   • Assessment: Very poor data quality - immediate action required")
        
        return True
    
    def run_nan_analysis(self, system) -> bool:
        """
        Run NaN analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.nan_analyzer.run_nan_analysis(system)
    
    def run_outlier_analysis(self, system) -> bool:
        """
        Run outlier analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.outlier_analyzer.run_outlier_analysis(system)
    
    def run_data_type_analysis(self, system) -> bool:
        """
        Run data type analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.data_type_analyzer.run_data_type_analysis(system)
    
    def run_missing_values_analysis(self, system) -> bool:
        """
        Run missing values analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.missing_values_analyzer.run_missing_values_analysis(system)
    
    def run_data_consistency_check(self, system) -> bool:
        """
        Run data consistency check.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.consistency_analyzer.run_data_consistency_check(system)
