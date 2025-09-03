#!/usr/bin/env python3
"""
Missing Values Analyzer module.

This module provides comprehensive missing values analysis capabilities
for financial data including pattern detection and recommendations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class MissingValuesAnalyzer:
    """
    Analyzer for missing values in financial data.
    
    Features:
    - Missing values summary
    - Column-wise analysis
    - Row-wise analysis
    - Pattern correlation analysis
    - Missing value types
    - Recommendations
    """
    
    def __init__(self):
        """Initialize the MissingValuesAnalyzer."""
        pass
    
    def run_missing_values_analysis(self, system) -> bool:
        """
        Run missing values analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n❓ MISSING VALUES ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        print(f"📊 Analyzing missing values for {len(df.columns)} columns...")
        
        # Overall missing values summary
        missing_summary = df.isnull().sum()
        total_missing = missing_summary.sum()
        total_cells = df.shape[0] * df.shape[1]
        
        print(f"\n📋 Missing Values Summary:")
        print(f"   • Total cells: {total_cells:,}")
        print(f"   • Missing cells: {total_missing:,}")
        print(f"   • Missing percentage: {(total_missing / total_cells) * 100:.2f}%")
        
        if total_missing == 0:
            print("✅ No missing values found in the dataset")
            return True
        
        # Missing values by column
        print(f"\n📊 Missing Values by Column:")
        
        # Sort by missing count
        missing_by_column = missing_summary[missing_summary > 0].sort_values(ascending=False)
        
        for col, missing_count in missing_by_column.head(10).items():  # Show top 10
            missing_percentage = (missing_count / len(df)) * 100
            print(f"   • {col}: {missing_count:,} missing ({missing_percentage:.2f}%)")
            
            # Categorize missing severity
            if missing_percentage > 50:
                print(f"     → Critical: More than 50% missing")
            elif missing_percentage > 20:
                print(f"     → High: 20-50% missing")
            elif missing_percentage > 5:
                print(f"     → Moderate: 5-20% missing")
            else:
                print(f"     → Low: Less than 5% missing")
        
        # Missing values by row
        print(f"\n📊 Missing Values by Row:")
        
        missing_by_row = df.isnull().sum(axis=1)
        rows_with_missing = missing_by_row[missing_by_row > 0]
        
        if len(rows_with_missing) > 0:
            print(f"   • Rows with missing values: {len(rows_with_missing):,}")
            print(f"   • Max missing per row: {rows_with_missing.max()}")
            print(f"   • Mean missing per row: {rows_with_missing.mean():.2f}")
            
            # Distribution of missing values per row
            missing_distribution = missing_by_row.value_counts().sort_index()
            print(f"   • Missing values distribution per row:")
            for missing_count, row_count in missing_distribution.head(10).items():
                print(f"     - {missing_count} missing: {row_count:,} rows")
        
        # Pattern analysis
        print(f"\n🔍 Missing Values Pattern Analysis:")
        
        # Check for systematic patterns
        if len(missing_by_column) > 1:
            # Create missing value matrix
            missing_matrix = df.isnull().astype(int)
            
            # Check for correlated missing patterns
            missing_correlations = missing_matrix.corr()
            
            # Find high correlations
            high_corr_pairs = []
            for i in range(len(missing_correlations.columns)):
                for j in range(i + 1, len(missing_correlations.columns)):
                    col1 = missing_correlations.columns[i]
                    col2 = missing_correlations.columns[j]
                    corr_val = missing_correlations.iloc[i, j]
                    
                    if corr_val > 0.7:  # High correlation threshold
                        high_corr_pairs.append((col1, col2, corr_val))
            
            if high_corr_pairs:
                print(f"   • Correlated missing patterns detected:")
                for col1, col2, corr_val in high_corr_pairs[:5]:  # Show first 5
                    print(f"     - {col1} ↔ {col2}: {corr_val:.4f}")
                print(f"     → Suggests systematic data collection issues")
            else:
                print(f"   • No strong missing value pattern correlations")
        
        # Missing value types
        print(f"\n🔍 Missing Value Types:")
        
        # Check for different types of missing values
        missing_types = {}
        
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check for string representations of missing values
                unique_vals = df[col].value_counts()
                missing_strings = [val for val in unique_vals.index if str(val).lower() in ['nan', 'none', 'null', 'na', '']]
                
                if missing_strings:
                    missing_types[col] = missing_strings
        
        if missing_types:
            print(f"   • String missing values detected:")
            for col, missing_strings in missing_types.items():
                print(f"     - {col}: {missing_strings}")
            print(f"     → These should be converted to proper NaN values")
        else:
            print(f"   • No string missing values detected")
        
        # Recommendations
        print(f"\n💡 Missing Values Handling Recommendations:")
        
        print(f"   • Immediate Actions:")
        
        # Critical columns
        critical_cols = missing_by_column[missing_by_column > len(df) * 0.5]
        if len(critical_cols) > 0:
            print(f"     - Remove columns with >50% missing: {', '.join(critical_cols.index.tolist())}")
        
        # High missing columns
        high_missing_cols = missing_by_column[(missing_by_column > len(df) * 0.2) & (missing_by_column <= len(df) * 0.5)]
        if len(high_missing_cols) > 0:
            print(f"     - Develop imputation strategy for: {', '.join(high_missing_cols.index.tolist())}")
        
        print(f"\n   • Imputation Strategies:")
        print(f"     - Numerical columns: Mean, median, or forward/backward fill")
        print(f"     - Categorical columns: Mode or most frequent value")
        print(f"     - Time series: Forward fill or interpolation")
        print(f"     - Advanced: KNN imputation, multiple imputation")
        
        print(f"\n   • Prevention Strategies:")
        print(f"     - Investigate data collection process")
        print(f"     - Implement data validation at source")
        print(f"     - Set up monitoring for missing value patterns")
        
        return True
