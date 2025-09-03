# -*- coding: utf-8 -*-
# src/interactive/eda/correlation/base_correlation_analyzer.py
#!/usr/bin/env python3
"""
Base Correlation Analyzer module.

This module provides the main interface for correlation analysis,
orchestrating calls to specialized analyzers.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import warnings

# Import specialized analyzers
from .matrix_analyzer import MatrixAnalyzer
from .heatmap_analyzer import HeatmapAnalyzer
from .insights_analyzer import InsightsAnalyzer


class CorrelationAnalyzer:
    """
    Main Correlation Analyzer class that orchestrates all correlation analysis operations.
    
    This class provides a unified interface for:
    - Correlation matrix analysis
    - Correlation heatmap generation
    - Correlation insights and interpretation
    - Multi-timeframe correlation analysis
    """
    
    def __init__(self):
        """Initialize the Correlation Analyzer with specialized analyzers."""
        self.matrix_analyzer = MatrixAnalyzer()
        self.heatmap_analyzer = HeatmapAnalyzer()
        self.insights_analyzer = InsightsAnalyzer()
        
        # Suppress warnings for cleaner output
        warnings.filterwarnings('ignore', category=FutureWarning)
        warnings.filterwarnings('ignore', category=UserWarning)
    
    def run_correlation_analysis(self, system) -> bool:
        """
        Run comprehensive correlation analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🔗 CORRELATION ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Check if we have enough numerical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            print("❌ Need at least 2 numerical columns for correlation analysis.")
            return False
        
        print(f"📊 Analyzing correlations between {len(numeric_cols)} numerical columns...")
        
        # Run all correlation analyses
        self.run_correlation_matrix(system)
        self.run_correlation_heatmap(system)
        self.run_correlation_insights(system)
        
        return True
    
    def run_correlation_matrix(self, system) -> bool:
        """
        Run correlation matrix analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.matrix_analyzer.run_correlation_matrix(system)
    
    def run_correlation_heatmap(self, system) -> bool:
        """
        Run correlation heatmap analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.heatmap_analyzer.run_correlation_heatmap(system)
    
    def run_correlation_insights(self, system) -> bool:
        """
        Run correlation insights analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.insights_analyzer.run_correlation_insights(system)
