# -*- coding: utf-8 -*-
# src/interactive/eda/feature_importance/ranking_analyzer.py
#!/usr/bin/env python3
"""
Ranking Analyzer module.

This module provides feature importance ranking capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class RankingAnalyzer:
    """
    Analyzer for feature importance ranking of financial data.
    
    Features:
    - Variance-based importance
    - Correlation-based importance
    - Statistical importance measures
    - Range-based importance
    - Combined importance score
    """
    
    def __init__(self):
        """Initialize the RankingAnalyzer."""
        pass
    
    def run_feature_importance_ranking(self, system) -> bool:
        """
        Run feature importance ranking analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🏆 FEATURE IMPORTANCE RANKING")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("❌ Need at least 2 numerical columns for feature importance ranking.")
            return False
        
        print(f"📊 Ranking {len(numeric_cols)} features by importance...")
        
        # Multiple importance metrics
        importance_metrics = {}
        
        # 1. Variance-based importance
        print(f"\n📊 Variance-based Importance:")
        variance_importance = {}
        for col in numeric_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                variance = col_data.var()
                variance_importance[col] = variance
        
        if variance_importance:
            # Sort by variance
            sorted_variance = sorted(variance_importance.items(), key=lambda x: x[1], reverse=True)
            
            for i, (col, var) in enumerate(sorted_variance[:5]):  # Top 5
                print(f"   {i+1}. {col}: {var:.6f}")
        
        # 2. Correlation-based importance
        print(f"\n🔗 Correlation-based Importance:")
        correlation_importance = {}
        
        # Calculate average absolute correlation for each feature
        for col in numeric_cols:
            correlations = []
            for other_col in numeric_cols:
                if col != other_col:
                    corr = df[col].corr(df[other_col])
                    if not pd.isna(corr):
                        correlations.append(abs(corr))
            
            if correlations:
                avg_corr = np.mean(correlations)
                correlation_importance[col] = avg_corr
        
        if correlation_importance:
            # Sort by average correlation
            sorted_correlation = sorted(correlation_importance.items(), key=lambda x: x[1], reverse=True)
            
            for i, (col, corr) in enumerate(sorted_correlation[:5]):  # Top 5
                print(f"   {i+1}. {col}: {corr:.4f}")
        
        # 3. Statistical importance (coefficient of variation)
        print(f"\n📈 Statistical Importance (Coefficient of Variation):")
        cv_importance = {}
        
        for col in numeric_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                mean_val = col_data.mean()
                std_val = col_data.std()
                
                if mean_val != 0:
                    cv = std_val / abs(mean_val)
                    cv_importance[col] = cv
        
        if cv_importance:
            # Sort by coefficient of variation
            sorted_cv = sorted(cv_importance.items(), key=lambda x: x[1], reverse=True)
            
            for i, (col, cv) in enumerate(sorted_cv[:5]):  # Top 5
                print(f"   {i+1}. {col}: {cv:.4f}")
        
        # 4. Range-based importance
        print(f"\n📏 Range-based Importance:")
        range_importance = {}
        
        for col in numeric_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                data_range = col_data.max() - col_data.min()
                range_importance[col] = data_range
        
        if range_importance:
            # Sort by range
            sorted_range = sorted(range_importance.items(), key=lambda x: x[1], reverse=True)
            
            for i, (col, data_range) in enumerate(sorted_range[:5]):  # Top 5
                print(f"   {i+1}. {col}: {data_range:.6f}")
        
        # 5. Combined importance score
        print(f"\n🎯 Combined Importance Score:")
        
        # Normalize and combine all metrics
        combined_scores = {}
        
        for col in numeric_cols:
            scores = []
            
            # Normalize variance score
            if col in variance_importance:
                norm_var = (variance_importance[col] - min(variance_importance.values())) / (max(variance_importance.values()) - min(variance_importance.values()))
                scores.append(norm_var)
            
            # Normalize correlation score
            if col in correlation_importance:
                norm_corr = (correlation_importance[col] - min(correlation_importance.values())) / (max(correlation_importance.values()) - min(correlation_importance.values()))
                scores.append(norm_corr)
            
            # Normalize CV score
            if col in cv_importance:
                norm_cv = (cv_importance[col] - min(cv_importance.values())) / (max(cv_importance.values()) - min(cv_importance.values()))
                scores.append(norm_cv)
            
            # Normalize range score
            if col in range_importance:
                norm_range = (range_importance[col] - min(range_importance.values())) / (max(range_importance.values()) - min(range_importance.values()))
                scores.append(norm_range)
            
            if scores:
                combined_scores[col] = np.mean(scores)
        
        if combined_scores:
            # Sort by combined score
            sorted_combined = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
            
            print(f"   🏆 Top Features by Combined Importance:")
            for i, (col, score) in enumerate(sorted_combined[:10]):  # Top 10
                print(f"   {i+1}. {col}: {score:.4f}")
        
        # Store importance metrics for other methods
        importance_metrics['variance'] = variance_importance
        importance_metrics['correlation'] = correlation_importance
        importance_metrics['cv'] = cv_importance
        importance_metrics['range'] = range_importance
        importance_metrics['combined'] = combined_scores
        
        return True
