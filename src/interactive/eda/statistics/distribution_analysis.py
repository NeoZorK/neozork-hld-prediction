# -*- coding: utf-8 -*-
# src/interactive/eda/statistics/distribution_analysis.py
#!/usr/bin/env python3
"""
Distribution Analysis module.

This module provides data distribution analysis capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class DistributionAnalysis:
    """
    Analyzer for data distribution analysis of financial data.
    
    Features:
    - Distribution statistics
    - Percentiles analysis
    - Distribution characteristics
    - Shape interpretation
    """
    
    def __init__(self):
        """Initialize the DistributionAnalysis."""
        pass
    
    def run_data_distribution_analysis(self, system) -> bool:
        """
        Run data distribution analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n📊 DATA DISTRIBUTION ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("❌ No numerical columns found for distribution analysis.")
            return False
        
        print(f"📈 Analyzing distributions for {len(numeric_cols)} numerical columns...")
        
        for col in numeric_cols[:5]:  # Analyze first 5 columns
            print(f"\n📊 {col} Distribution:")
            
            # Basic distribution stats
            col_data = df[col].dropna()
            if len(col_data) == 0:
                print(f"   ⚠️  Column {col} has no valid data")
                continue
            
            # Percentiles
            percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
            percentile_values = np.percentile(col_data, percentiles)
            
            print(f"   • Percentiles:")
            for p, val in zip(percentiles, percentile_values):
                print(f"     {p}%: {val:.6f}")
            
            # Distribution characteristics
            mean_val = col_data.mean()
            std_val = col_data.std()
            skew_val = col_data.skew()
            kurt_val = col_data.kurtosis()
            
            print(f"   • Distribution characteristics:")
            print(f"     - Mean: {mean_val:.6f}")
            print(f"     - Std: {std_val:.6f}")
            print(f"     - Skewness: {skew_val:.6f}")
            print(f"     - Kurtosis: {kurt_val:.6f}")
            
            # Distribution shape interpretation
            if abs(skew_val) < 0.5:
                print(f"     - Shape: Approximately symmetric")
            elif skew_val > 0.5:
                print(f"     - Shape: Right-skewed (positive skew)")
            else:
                print(f"     - Shape: Left-skewed (negative skew)")
            
            if abs(kurt_val) < 3:
                print(f"     - Tails: Normal (mesokurtic)")
            elif kurt_val > 3:
                print(f"     - Tails: Heavy (leptokurtic)")
            else:
                print(f"     - Tails: Light (platykurtic)")
        
        return True
