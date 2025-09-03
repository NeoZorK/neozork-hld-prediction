# -*- coding: utf-8 -*-
# src/interactive/eda/statistics/descriptive_statistics.py
#!/usr/bin/env python3
"""
Descriptive Statistics module.

This module provides descriptive statistics analysis capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class DescriptiveStatistics:
    """
    Analyzer for descriptive statistics of financial data.
    
    Features:
    - Central tendency measures
    - Dispersion measures
    - Percentiles analysis
    - Extremes analysis
    """
    
    def __init__(self):
        """Initialize the DescriptiveStatistics."""
        pass
    
    def run_descriptive_statistics(self, system) -> bool:
        """
        Run descriptive statistics analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n📊 DESCRIPTIVE STATISTICS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("❌ No numerical columns found for descriptive analysis.")
            return False
        
        print(f"📈 Descriptive statistics for {len(numeric_cols)} numerical columns:")
        
        # Create comprehensive descriptive statistics
        desc_stats = df[numeric_cols].describe(percentiles=[0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95])
        
        for col in numeric_cols[:5]:  # Show first 5 columns
            print(f"\n📊 {col}:")
            col_stats = desc_stats[col]
            
            # Central tendency
            print(f"   • Central Tendency:")
            print(f"     - Count: {col_stats['count']:,}")
            print(f"     - Mean: {col_stats['mean']:.6f}")
            print(f"     - Median (50%): {col_stats['50%']:.6f}")
            
            # Dispersion
            print(f"   • Dispersion:")
            print(f"     - Std: {col_stats['std']:.6f}")
            print(f"     - Variance: {col_stats['std']**2:.6f}")
            print(f"     - Range: {col_stats['max'] - col_stats['min']:.6f}")
            print(f"     - IQR: {col_stats['75%'] - col_stats['25%']:.6f}")
            
            # Percentiles
            print(f"   • Percentiles:")
            print(f"     - 5%: {col_stats['5%']:.6f}")
            print(f"     - 10%: {col_stats['10%']:.6f}")
            print(f"     - 25%: {col_stats['25%']:.6f}")
            print(f"     - 75%: {col_stats['75%']:.6f}")
            print(f"     - 90%: {col_stats['90%']:.6f}")
            print(f"     - 95%: {col_stats['95%']:.6f}")
            
            # Extremes
            print(f"   • Extremes:")
            print(f"     - Min: {col_stats['min']:.6f}")
            print(f"     - Max: {col_stats['max']:.6f}")
        
        return True
