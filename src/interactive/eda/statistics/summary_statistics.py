#!/usr/bin/env python3
"""
Summary Statistics module.

This module provides summary statistics analysis capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class SummaryStatistics:
    """
    Analyzer for summary statistics of financial data.
    
    Features:
    - Overall summary
    - Data type summary
    - Numerical summary
    - Categorical summary
    - Missing values summary
    """
    
    def __init__(self):
        """Initialize the SummaryStatistics."""
        pass
    
    def run_summary_statistics(self, system) -> bool:
        """
        Run summary statistics analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n📊 SUMMARY STATISTICS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Overall summary
        print(f"📋 Overall Summary:")
        print(f"   • Total rows: {len(df):,}")
        print(f"   • Total columns: {len(df.columns)}")
        print(f"   • Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Column type summary
        dtype_counts = df.dtypes.value_counts()
        print(f"\n🏷️  Data Type Summary:")
        for dtype, count in dtype_counts.items():
            print(f"   • {dtype}: {count} columns")
        
        # Numerical summary
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"\n🔢 Numerical Columns Summary:")
            print(f"   • Count: {len(numeric_cols)}")
            print(f"   • Names: {', '.join(numeric_cols.tolist())}")
            
            # Aggregate statistics
            numeric_df = df[numeric_cols]
            print(f"   • Total sum: {numeric_df.sum().sum():,.2f}")
            print(f"   • Total mean: {numeric_df.mean().mean():.6f}")
            print(f"   • Total std: {numeric_df.std().mean():.6f}")
        
        # Categorical summary
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            print(f"\n🏷️  Categorical Columns Summary:")
            print(f"   • Count: {len(categorical_cols)}")
            print(f"   • Names: {', '.join(categorical_cols.tolist())}")
            
            # Unique values summary
            for col in categorical_cols[:3]:  # Show first 3
                unique_count = df[col].nunique()
                print(f"   • {col}: {unique_count:,} unique values")
        
        # Missing values summary
        missing_summary = df.isnull().sum()
        total_missing = missing_summary.sum()
        if total_missing > 0:
            print(f"\n⚠️  Missing Values Summary:")
            print(f"   • Total missing: {total_missing:,}")
            print(f"   • Missing percentage: {(total_missing / (len(df) * len(df.columns))) * 100:.2f}%")
            
            # Columns with most missing values
            top_missing = missing_summary[missing_summary > 0].nlargest(3)
            print(f"   • Top columns with missing values:")
            for col, missing_count in top_missing.items():
                missing_percent = (missing_count / len(df)) * 100
                print(f"     - {col}: {missing_count:,} ({missing_percent:.2f}%)")
        else:
            print(f"\n✅ No missing values found")
        
        return True
