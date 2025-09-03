# -*- coding: utf-8 -*-
# src/interactive/eda/statistics/basic_statistics.py
#!/usr/bin/env python3
"""
Basic Statistics module.

This module provides basic statistical analysis capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class BasicStatistics:
    """
    Analyzer for basic statistics of financial data.
    
    Features:
    - Dataset overview
    - Basic information
    - Summary statistics
    - Categorical analysis
    - Missing values
    - Data quality indicators
    """
    
    def __init__(self):
        """Initialize the BasicStatistics."""
        pass
    
    def run_basic_statistics(self, system) -> bool:
        """
        Run basic statistics analysis on the loaded data.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n📊 BASIC STATISTICS ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        print(f"📋 Dataset Overview:")
        print(f"   • Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"   • Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print(f"   • Data types: {df.dtypes.nunique()} unique types")
        
        # Basic info
        print(f"\n📊 Basic Information:")
        print(f"   • Columns: {', '.join(df.columns.tolist())}")
        print(f"   • Index type: {type(df.index).__name__}")
        print(f"   • Range: {df.index.min()} to {df.index.max()}" if hasattr(df.index, 'min') else "   • Index: Custom")
        
        # Summary statistics
        print(f"\n📈 Summary Statistics:")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            summary_stats = df[numeric_cols].describe()
            print(f"   • Numerical columns: {len(numeric_cols)}")
            for col in numeric_cols[:5]:  # Show first 5 columns
                col_stats = summary_stats[col]
                print(f"     {col}:")
                print(f"       - Count: {col_stats['count']:,}")
                print(f"       - Mean: {col_stats['mean']:.6f}")
                print(f"       - Std: {col_stats['std']:.6f}")
                print(f"       - Min: {col_stats['min']:.6f}")
                print(f"       - 25%: {col_stats['25%']:.6f}")
                print(f"       - 50%: {col_stats['50%']:.6f}")
                print(f"       - 75%: {col_stats['75%']:.6f}")
                print(f"       - Max: {col_stats['max']:.6f}")
        else:
            print("   • No numerical columns found")
        
        # Categorical analysis
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            print(f"\n🏷️  Categorical Analysis:")
            print(f"   • Categorical columns: {len(categorical_cols)}")
            for col in categorical_cols[:3]:  # Show first 3 columns
                unique_vals = df[col].nunique()
                print(f"     {col}: {unique_vals:,} unique values")
                if unique_vals <= 10:
                    value_counts = df[col].value_counts().head(5)
                    print(f"       Top values: {dict(value_counts)}")
        
        # Missing values
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            print(f"\n⚠️  Missing Values:")
            for col, missing_count in missing_data[missing_data > 0].items():
                missing_percent = (missing_count / len(df)) * 100
                print(f"   • {col}: {missing_count:,} ({missing_percent:.2f}%)")
        else:
            print(f"\n✅ No missing values found")
        
        # Data quality indicators
        print(f"\n🔍 Data Quality Indicators:")
        print(f"   • Duplicate rows: {df.duplicated().sum():,}")
        print(f"   • Unique rows: {df.drop_duplicates().shape[0]:,}")
        
        # Memory optimization suggestions
        print(f"\n💡 Memory Optimization Suggestions:")
        for col in df.columns:
            col_dtype = df[col].dtype
            if col_dtype == 'object':
                print(f"   • {col}: Consider converting to category if low cardinality")
            elif col_dtype == 'float64':
                print(f"   • {col}: Consider converting to float32 if precision allows")
            elif col_dtype == 'int64':
                print(f"   • {col}: Consider converting to int32 if range allows")
        
        return True
