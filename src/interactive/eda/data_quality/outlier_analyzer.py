# -*- coding: utf-8 -*-
# src/interactive/eda/data_quality/outlier_analyzer.py
#!/usr/bin/env python3
"""
Outlier Analyzer module.

This module provides comprehensive outlier analysis capabilities
for financial data using multiple detection methods.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class OutlierAnalyzer:
    """
    Analyzer for outliers in financial data.
    
    Features:
    - IQR method outliers
    - Z-score method outliers
    - Modified Z-score method outliers
    - Method comparison
    - Recommendations
    """
    
    def __init__(self):
        """Initialize the OutlierAnalyzer."""
        pass
    
    def run_outlier_analysis(self, system) -> bool:
        """
        Run outlier analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🔍 OUTLIER ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("❌ No numerical columns found for outlier analysis.")
            return False
        
        print(f"📊 Analyzing outliers in {len(numeric_cols)} numerical columns...")
        
        # Multiple outlier detection methods
        outlier_methods = {}
        
        # 1. IQR method
        print(f"\n📏 IQR Method Outliers:")
        iqr_outliers = {}
        
        for col in numeric_cols[:5]:  # Analyze first 5 columns
            col_data = df[col].dropna()
            if len(col_data) > 0:
                q75 = col_data.quantile(0.75)
                q25 = col_data.quantile(0.25)
                iqr = q75 - q25
                
                lower_bound = q25 - 1.5 * iqr
                upper_bound = q75 + 1.5 * iqr
                
                outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                outlier_count = len(outliers)
                outlier_percentage = (outlier_count / len(col_data)) * 100
                
                iqr_outliers[col] = {
                    'count': outlier_count,
                    'percentage': outlier_percentage,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
                
                print(f"   • {col}: {outlier_count:,} outliers ({outlier_percentage:.2f}%)")
                print(f"     - Bounds: [{lower_bound:.6f}, {upper_bound:.6f}]")
                
                if outlier_percentage > 10:
                    print(f"     → High outlier percentage - investigate data quality")
                elif outlier_percentage > 5:
                    print(f"       → Moderate outliers - consider treatment")
                else:
                    print(f"     → Low outliers - acceptable")
        
        outlier_methods['iqr'] = iqr_outliers
        
        # 2. Z-score method
        print(f"\n📊 Z-Score Method Outliers:")
        zscore_outliers = {}
        
        for col in numeric_cols[:5]:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                z_scores = np.abs((col_data - col_data.mean()) / col_data.std())
                outliers = col_data[z_scores > 3]  # 3 standard deviations
                outlier_count = len(outliers)
                outlier_percentage = (outlier_count / len(col_data)) * 100
                
                zscore_outliers[col] = {
                    'count': outlier_count,
                    'percentage': outlier_percentage
                }
                
                print(f"   • {col}: {outlier_count:,} outliers ({outlier_percentage:.2f}%)")
        
        outlier_methods['zscore'] = zscore_outliers
        
        # 3. Modified Z-score method (more robust)
        print(f"\n🔄 Modified Z-Score Method Outliers:")
        modified_zscore_outliers = {}
        
        for col in numeric_cols[:5]:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                median = col_data.median()
                mad = np.median(np.abs(col_data - median))
                
                if mad != 0:
                    modified_z_scores = np.abs(0.6745 * (col_data - median) / mad)
                    outliers = col_data[modified_z_scores > 3.5]
                    outlier_count = len(outliers)
                    outlier_percentage = (outlier_count / len(col_data)) * 100
                    
                    modified_zscore_outliers[col] = {
                        'count': outlier_count,
                        'percentage': outlier_percentage
                    }
                    
                    print(f"   • {col}: {outlier_count:,} outliers ({outlier_percentage:.2f}%)")
        
        outlier_methods['modified_zscore'] = modified_zscore_outliers
        
        # Outlier summary and recommendations
        print(f"\n📋 OUTLIER SUMMARY:")
        
        # Compare methods
        for col in numeric_cols[:3]:
            print(f"\n   • {col} Outlier Comparison:")
            
            if col in iqr_outliers:
                iqr_count = iqr_outliers[col]['count']
                print(f"     - IQR method: {iqr_count:,} outliers")
            
            if col in zscore_outliers:
                zscore_count = zscore_outliers[col]['count']
                print(f"     - Z-score method: {zscore_count:,} outliers")
            
            if col in modified_zscore_outliers:
                modified_count = modified_zscore_outliers[col]['count']
                print(f"     - Modified Z-score: {modified_count:,} outliers")
        
        # Recommendations
        print(f"\n💡 Outlier Handling Recommendations:")
        
        print(f"   • Detection Method:")
        print(f"     - IQR: Good for non-normal distributions")
        print(f"     - Z-score: Good for normal distributions")
        print(f"     - Modified Z-score: Most robust to extreme values")
        
        print(f"   • Treatment Strategies:")
        print(f"     - Remove outliers if they represent errors")
        print(f"     - Cap outliers at reasonable bounds")
        print(f"     - Use robust statistical methods")
        print(f"     - Investigate outlier causes")
        
        return True
