# -*- coding: utf-8 -*-
# src/interactive/eda/data_quality/nan_analyzer.py
#!/usr/bin/env python3
"""
NaN Analyzer module.

This module provides comprehensive NaN analysis capabilities
for financial data including pattern detection and recommendations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class NanAnalyzer:
    """
    Analyzer for NaN values in financial data.
    
    Features:
    - NaN pattern detection
    - Column-wise analysis
    - Row-wise analysis
    - Pattern correlation analysis
    - Recommendations
    """
    
    def __init__(self):
        """Initialize the NanAnalyzer."""
        pass
    
    def run_nan_analysis(self, system) -> bool:
        """
        Run NaN analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n❌ NaN ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Check for NaN values
        nan_counts = df.isnull().sum()
        total_nans = nan_counts.sum()
        
        if total_nans == 0:
            print("✅ No NaN values found in the dataset")
            return True
        
        print(f"⚠️  Found {total_nans:,} NaN values across the dataset")
        
        # Analyze NaN patterns by column
        print(f"\n📊 NaN Analysis by Column:")
        
        # Sort columns by NaN count
        nan_by_column = nan_counts[nan_counts > 0].sort_values(ascending=False)
        
        for col, nan_count in nan_by_column.head(10).items():  # Show top 10
            nan_percentage = (nan_count / len(df)) * 100
            print(f"   • {col}: {nan_count:,} NaNs ({nan_percentage:.2f}%)")
            
            # Categorize NaN severity
            if nan_percentage > 50:
                print(f"     → Critical: More than 50% missing - consider removing column")
            elif nan_percentage > 20:
                print(f"     → High: 20-50% missing - needs imputation strategy")
            elif nan_percentage > 5:
                print(f"     → Moderate: 5-20% missing - consider imputation")
            else:
                print(f"     → Low: Less than 5% missing - acceptable")
        
        # Analyze NaN patterns by row
        print(f"\n📊 NaN Analysis by Row:")
        
        nan_by_row = df.isnull().sum(axis=1)
        rows_with_nans = nan_by_row[nan_by_row > 0]
        
        if len(rows_with_nans) > 0:
            print(f"   • Rows with NaNs: {len(rows_with_nans):,}")
            print(f"   • Max NaNs per row: {rows_with_nans.max()}")
            print(f"   • Mean NaNs per row: {rows_with_nans.mean():.2f}")
            
            # Find rows with most NaNs
            worst_rows = nan_by_row.nlargest(5)
            print(f"   • Rows with most NaNs:")
            for idx, nan_count in worst_rows.items():
                print(f"     - Row {idx}: {nan_count} NaNs")
        
        # Pattern analysis
        print(f"\n🔍 NaN Pattern Analysis:")
        
        # Check for systematic patterns
        if len(nan_by_column) > 1:
            # Check if NaN patterns are correlated
            nan_matrix = df.isnull().astype(int)
            nan_correlations = nan_matrix.corr()
            
            # Find columns with correlated NaN patterns
            high_nan_corr = []
            for i in range(len(nan_correlations.columns)):
                for j in range(i + 1, len(nan_correlations.columns)):
                    col1 = nan_correlations.columns[i]
                    col2 = nan_correlations.columns[j]
                    corr_val = nan_correlations.iloc[i, j]
                    
                    if corr_val > 0.7:  # High correlation threshold
                        high_nan_corr.append((col1, col2, corr_val))
            
            if high_nan_corr:
                print(f"   • Correlated NaN patterns detected:")
                for col1, col2, corr_val in high_nan_corr[:5]:  # Show first 5
                    print(f"     - {col1} ↔ {col2}: {corr_val:.4f}")
                print(f"     → Suggests systematic data collection issues")
            else:
                print(f"   • No strong NaN pattern correlations detected")
        
        # Recommendations
        print(f"\n💡 NaN Handling Recommendations:")
        
        if total_nans > 0:
            print(f"   • Immediate Actions:")
            
            # Critical columns
            critical_cols = nan_by_column[nan_by_column > len(df) * 0.5]
            if len(critical_cols) > 0:
                print(f"     - Remove columns with >50% NaNs: {', '.join(critical_cols.index.tolist())}")
            
            # High missing columns
            high_missing_cols = nan_by_column[(nan_by_column > len(df) * 0.2) & (nan_by_column <= len(df) * 0.5)]
            if len(high_missing_cols) > 0:
                print(f"     - Develop imputation strategy for: {', '.join(high_missing_cols.index.tolist())}")
            
            print(f"   • Imputation Strategies:")
            print(f"     - Numerical columns: Mean, median, or forward/backward fill")
            print(f"     - Categorical columns: Mode or most frequent value")
            print(f"     - Time series: Forward fill or interpolation")
        
        return True
