#!/usr/bin/env python3
"""
Categorical Analysis module.

This module provides categorical analysis capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class CategoricalAnalysis:
    """
    Analyzer for categorical analysis of financial data.
    
    Features:
    - Basic categorical properties
    - Value distribution
    - Top values analysis
    - Cardinality analysis
    - Missing value analysis
    """
    
    def __init__(self):
        """Initialize the CategoricalAnalysis."""
        pass
    
    def run_categorical_analysis(self, system) -> bool:
        """
        Run categorical analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🏷️  CATEGORICAL ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        if len(categorical_cols) == 0:
            print("❌ No categorical columns found for categorical analysis.")
            return False
        
        print(f"📊 Analyzing {len(categorical_cols)} categorical columns...")
        
        for col in categorical_cols[:5]:  # Analyze first 5 columns
            print(f"\n🏷️  {col} Analysis:")
            
            col_data = df[col].dropna()
            if len(col_data) == 0:
                print(f"   ⚠️  Column {col} has no valid data")
                continue
            
            # Basic categorical properties
            print(f"   • Basic Properties:")
            print(f"     - Data type: {df[col].dtype}")
            print(f"     - Non-null count: {len(col_data):,}")
            print(f"     - Null count: {df[col].isnull().sum():,}")
            print(f"     - Unique values: {col_data.nunique():,}")
            
            # Value counts
            value_counts = col_data.value_counts()
            print(f"   • Value Distribution:")
            print(f"     - Most common value: '{value_counts.index[0]}' ({value_counts.iloc[0]:,} times)")
            print(f"     - Least common value: '{value_counts.index[-1]}' ({value_counts.iloc[-1]:,} times)")
            
            # Show top values
            top_values = value_counts.head(5)
            print(f"   • Top 5 Values:")
            for value, count in top_values.items():
                percentage = (count / len(col_data)) * 100
                print(f"     - '{value}': {count:,} ({percentage:.2f}%)")
            
            # Cardinality analysis
            unique_count = col_data.nunique()
            total_count = len(col_data)
            cardinality_ratio = unique_count / total_count if total_count > 0 else 0
            
            print(f"   • Cardinality Analysis:")
            print(f"     - Cardinality ratio: {cardinality_ratio:.4f}")
            if cardinality_ratio < 0.01:
                print(f"     - Type: Low cardinality (good for encoding)")
            elif cardinality_ratio < 0.1:
                print(f"     - Type: Medium cardinality (moderate encoding)")
            else:
                print(f"     - Type: High cardinality (consider feature engineering)")
            
            # Missing value analysis
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                missing_percentage = (missing_count / len(df)) * 100
                print(f"   • Missing Value Analysis:")
                print(f"     - Missing count: {missing_count:,}")
                print(f"     - Missing percentage: {missing_percentage:.2f}%")
                
                if missing_percentage > 50:
                    print(f"     - Warning: High missing percentage - consider dropping")
                elif missing_percentage > 20:
                    print(f"     - Note: Moderate missing percentage - consider imputation")
                else:
                    print(f"     - Acceptable missing percentage")
        
        return True
