#!/usr/bin/env python3
"""
Base Feature Importance Analyzer module.

This module provides the main interface for feature importance analysis,
orchestrating calls to specialized analyzers.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import warnings

# Import specialized analyzers
from .ranking_analyzer import RankingAnalyzer
from .visualization_analyzer import VisualizationAnalyzer
from .insights_analyzer import InsightsAnalyzer


class FeatureImportanceAnalyzer:
    """
    Main Feature Importance Analyzer class that orchestrates all feature importance analysis operations.
    
    This class provides a unified interface for:
    - Feature importance ranking
    - Feature importance visualization
    - Feature importance insights
    - Comprehensive feature importance analysis
    """
    
    def __init__(self):
        """Initialize the Feature Importance Analyzer with specialized analyzers."""
        self.ranking_analyzer = RankingAnalyzer()
        self.visualization_analyzer = VisualizationAnalyzer()
        self.insights_analyzer = InsightsAnalyzer()
        
        # Suppress warnings for cleaner output
        warnings.filterwarnings('ignore', category=FutureWarning)
        warnings.filterwarnings('ignore', category=UserWarning)
    
    def run_feature_importance_analysis(self, system) -> bool:
        """
        Run comprehensive feature importance analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🎯 FEATURE IMPORTANCE ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Check if we have enough numerical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            print("❌ Need at least 2 numerical columns for feature importance analysis.")
            return False
        
        print(f"📊 Analyzing feature importance for {len(numeric_cols)} numerical columns...")
        
        # Run all feature importance analyses
        self.run_feature_importance_ranking(system)
        self.run_feature_importance_visualization(system)
        self.run_feature_importance_insights(system)
        
        return True
    
    def run_feature_importance_ranking(self, system) -> bool:
        """
        Run feature importance ranking analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.ranking_analyzer.run_feature_importance_ranking(system)
    
    def run_feature_importance_visualization(self, system) -> bool:
        """
        Run feature importance visualization analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.visualization_analyzer.run_feature_importance_visualization(system)
    
    def run_feature_importance_insights(self, system) -> bool:
        """
        Run feature importance insights analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.insights_analyzer.run_feature_importance_insights(system)
