#!/usr/bin/env python3
"""
Visualization Analyzer module.

This module provides feature importance visualization capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class VisualizationAnalyzer:
    """
    Analyzer for feature importance visualization of financial data.
    
    Features:
    - Feature distribution analysis
    - Feature comparison analysis
    - Feature importance patterns
    - Visualization recommendations
    """
    
    def __init__(self):
        """Initialize the VisualizationAnalyzer."""
        pass
    
    def run_feature_importance_visualization(self, system) -> bool:
        """
        Run feature importance visualization analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n📊 FEATURE IMPORTANCE VISUALIZATION")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("❌ Need at least 2 numerical columns for feature importance visualization.")
            return False
        
        print(f"📊 Generating visualization insights for {len(numeric_cols)} features...")
        
        # 1. Feature distribution analysis
        print(f"\n📈 Feature Distribution Analysis:")
        
        for col in numeric_cols[:3]:  # Analyze first 3 columns
            print(f"\n📊 {col} Distribution:")
            
            col_data = df[col].dropna()
            if len(col_data) == 0:
                print(f"   ⚠️  No valid data for {col}")
                continue
            
            # Distribution characteristics
            print(f"   • Basic Statistics:")
            print(f"     - Count: {len(col_data):,}")
            print(f"     - Mean: {col_data.mean():.6f}")
            print(f"     - Median: {col_data.median():.6f}")
            print(f"     - Std: {col_data.std():.6f}")
            print(f"     - Min: {col_data.min():.6f}")
            print(f"     - Max: {col_data.max():.6f}")
            
            # Distribution shape
            skewness = col_data.skew()
            kurtosis = col_data.kurtosis()
            
            print(f"   • Distribution Shape:")
            print(f"     - Skewness: {skewness:.4f}")
            print(f"     - Kurtosis: {kurtosis:.4f}")
            
            # Interpret skewness
            if abs(skewness) < 0.5:
                print(f"     - Shape: Approximately symmetric")
            elif skewness > 0.5:
                print(f"     - Shape: Right-skewed (positive skew)")
            else:
                print(f"     - Shape: Left-skewed (negative skew)")
            
            # Interpret kurtosis
            if abs(kurtosis) < 3:
                print(f"     - Tails: Normal (mesokurtic)")
            elif kurtosis > 3:
                print(f"     - Tails: Heavy (leptokurtic)")
            else:
                print(f"     - Tails: Light (platykurtic)")
            
            # Percentiles for visualization reference
            percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
            percentile_values = np.percentile(col_data, percentiles)
            
            print(f"   • Key Percentiles:")
            for p, val in zip(percentiles, percentile_values):
                print(f"     - {p}%: {val:.6f}")
        
        # 2. Feature comparison analysis
        print(f"\n🔍 Feature Comparison Analysis:")
        
        # Compare top features
        if len(numeric_cols) >= 2:
            top_features = numeric_cols[:3]  # Compare first 3 features
            
            print(f"   • Comparing {len(top_features)} top features:")
            
            for i, col1 in enumerate(top_features):
                for j in range(i + 1, len(top_features)):
                    col2 = top_features[j]
                    
                    # Calculate correlation
                    corr = df[col1].corr(df[col2])
                    if not pd.isna(corr):
                        print(f"     - {col1} ↔ {col2}: {corr:.4f}")
                        
                        # Interpret correlation
                        if abs(corr) > 0.8:
                            print(f"       → Very strong correlation")
                        elif abs(corr) > 0.6:
                            print(f"       → Strong correlation")
                        elif abs(corr) > 0.4:
                            print(f"       → Moderate correlation")
                        elif abs(corr) > 0.2:
                            print(f"       → Weak correlation")
                        else:
                            print(f"       → Very weak correlation")
            
            # Feature scaling comparison
            print(f"\n   • Feature Scaling Comparison:")
            
            for col in top_features:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    # Z-score scaling reference
                    z_score_range = (col_data.max() - col_data.min()) / col_data.std()
                    print(f"     - {col}: Range/Std = {z_score_range:.2f}")
                    
                    if z_score_range > 10:
                        print(f"       → Wide range - consider scaling")
                    elif z_score_range < 2:
                        print(f"       → Narrow range - may need expansion")
                    else:
                        print(f"       → Moderate range - scaling optional")
        
        # 3. Feature importance patterns
        print(f"\n🎯 Feature Importance Patterns:")
        
        # Check for feature groups
        feature_groups = {}
        
        # Group by correlation patterns
        correlation_threshold = 0.7
        for col1 in numeric_cols:
            if col1 not in [item for sublist in feature_groups.values() for item in sublist]:
                group = [col1]
                
                for col2 in numeric_cols:
                    if col1 != col2 and col2 not in [item for sublist in feature_groups.values() for item in sublist]:
                        corr = df[col1].corr(df[col2])
                        if not pd.isna(corr) and abs(corr) > correlation_threshold:
                            group.append(col2)
                
                if len(group) > 1:
                    feature_groups[f"Group_{len(feature_groups)+1}"] = group
        
        if feature_groups:
            print(f"   • Feature Groups Detected:")
            for group_name, features in feature_groups.items():
                print(f"     - {group_name}: {', '.join(features)}")
                print(f"       → Size: {len(features)} features")
                
                # Calculate group importance
                group_importance = 0
                for feature in features:
                    if feature in df.columns:
                        col_data = df[feature].dropna()
                        if len(col_data) > 0:
                            group_importance += col_data.var()
                
                print(f"       → Group importance: {group_importance:.6f}")
        else:
            print(f"   • No strong feature groups detected (correlation threshold: {correlation_threshold})")
        
        # 4. Visualization recommendations
        print(f"\n💡 Visualization Recommendations:")
        
        # Based on data characteristics
        for col in numeric_cols[:3]:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                print(f"   • {col}:")
                
                # Distribution type recommendation
                if abs(col_data.skew()) > 1:
                    print(f"     - Use log scale or transformation for skewed data")
                
                if col_data.nunique() < 20:
                    print(f"     - Consider histogram or bar chart (discrete-like data)")
                else:
                    print(f"     - Use density plot or histogram (continuous data)")
                
                # Outlier detection
                q75 = col_data.quantile(0.75)
                q25 = col_data.quantile(0.25)
                iqr = q75 - q25
                outlier_threshold = q75 + 1.5 * iqr
                outliers = col_data[col_data > outlier_threshold]
                
                if len(outliers) > 0:
                    print(f"     - {len(outliers)} outliers detected - consider box plot")
        
        return True
