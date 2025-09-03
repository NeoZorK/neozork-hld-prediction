# -*- coding: utf-8 -*-
# src/interactive/eda/time_series/base_time_series_analyzer.py
#!/usr/bin/env python3
"""
Base Time Series Analyzer module.

This module provides the main interface for time series analysis,
orchestrating calls to specialized analyzers.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import warnings

# Import specialized analyzers
from .gaps_analyzer import GapsAnalyzer
from .trends_analyzer import TrendsAnalyzer
from .seasonality_analyzer import SeasonalityAnalyzer
from .stationarity_analyzer import StationarityAnalyzer


class TimeSeriesAnalyzer:
    """
    Main Time Series Analyzer class that orchestrates all time series analysis operations.
    
    This class provides a unified interface for:
    - Time series gaps analysis
    - Trend analysis
    - Seasonality detection
    - Stationarity testing
    - Multi-timeframe analysis
    """
    
    def __init__(self):
        """Initialize the Time Series Analyzer with specialized analyzers."""
        self.gaps_analyzer = GapsAnalyzer()
        self.trends_analyzer = TrendsAnalyzer()
        self.seasonality_analyzer = SeasonalityAnalyzer()
        self.stationarity_analyzer = StationarityAnalyzer()
        
        # Suppress warnings for cleaner output
        warnings.filterwarnings('ignore', category=FutureWarning)
        warnings.filterwarnings('ignore', category=UserWarning)
    
    def run_time_series_analysis(self, system) -> bool:
        """
        Run comprehensive time series analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n📈 TIME SERIES ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Check if we have timestamp columns
        timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        if not timestamp_cols:
            print("❌ No timestamp columns found for time series analysis.")
            return False
        
        print(f"📊 Analyzing time series with {len(timestamp_cols)} timestamp columns...")
        
        # Run all time series analyses
        self.run_time_series_gaps_analysis(system)
        self.run_time_series_trends(system)
        self.run_time_series_seasonality(system)
        self.run_time_series_stationarity(system)
        
        return True
    
    def run_time_series_gaps_analysis(self, system) -> bool:
        """
        Run time series gaps analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.gaps_analyzer.run_time_series_gaps_analysis(system)
    
    def run_time_series_trends(self, system) -> bool:
        """
        Run time series trends analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.trends_analyzer.run_time_series_trends(system)
    
    def run_time_series_seasonality(self, system) -> bool:
        """
        Run time series seasonality analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.seasonality_analyzer.run_time_series_seasonality(system)
    
    def run_time_series_stationarity(self, system) -> bool:
        """
        Run time series stationarity analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.stationarity_analyzer.run_time_series_stationarity(system)
