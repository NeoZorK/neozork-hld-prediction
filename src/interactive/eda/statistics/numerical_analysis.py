#!/usr/bin/env python3
"""
Numerical Analysis module.

This module provides numerical analysis capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class NumericalAnalysis:
    """
    Analyzer for numerical analysis of financial data.
    
    Features:
    - Basic numerical properties
    - Statistical measures
    - Variability measures
    - Shape measures
    - Range and percentiles
    """
    
    def __init__(self):
        """Initialize the NumericalAnalysis."""
        pass
    
    def run_numerical_analysis(self, system) -> bool:
        """
        Run numerical analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🔢 NUMERICAL ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("❌ No numerical columns found for numerical analysis.")
            return False
        
        print(f"📊 Analyzing {len(numeric_cols)} numerical columns...")
        
        for col in numeric_cols[:5]:  # Analyze first 5 columns
            print(f"\n🔢 {col} Analysis:")
            
            col_data = df[col].dropna()
            if len(col_data) == 0:
                print(f"   ⚠️  Column {col} has no valid data")
                continue
            
            # Basic numerical properties
            print(f"   • Basic Properties:")
            print(f"     - Data type: {df[col].dtype}")
            print(f"     - Non-null count: {len(col_data):,}")
            print(f"     - Null count: {df[col].isnull().sum():,}")
            
            # Statistical measures
            print(f"   • Statistical Measures:")
            print(f"     - Sum: {col_data.sum():,.6f}")
            print(f"     - Mean: {col_data.mean():.6f}")
            print(f"     - Median: {col_data.median():.6f}")
            print(f"     - Mode: {col_data.mode().iloc[0] if len(col_data.mode()) > 0 else 'N/A'}")
            
            # Variability measures
            print(f"   • Variability Measures:")
            print(f"     - Variance: {col_data.var():.6f}")
            print(f"     - Standard deviation: {col_data.std():.6f}")
            print(f"     - Coefficient of variation: {(col_data.std() / col_data.mean()) * 100:.2f}%")
            
            # Shape measures
            print(f"   • Shape Measures:")
            print(f"     - Skewness: {col_data.skew():.6f}")
            print(f"     - Kurtosis: {col_data.kurtosis():.6f}")
            
            # Range and percentiles
            print(f"   • Range and Percentiles:")
            print(f"     - Range: {col_data.max() - col_data.min():.6f}")
            print(f"     - 25th percentile: {col_data.quantile(0.25):.6f}")
            print(f"     - 75th percentile: {col_data.quantile(0.75):.6f}")
            print(f"     - Interquartile range: {col_data.quantile(0.75) - col_data.quantile(0.25):.6f}")
        
        return True
