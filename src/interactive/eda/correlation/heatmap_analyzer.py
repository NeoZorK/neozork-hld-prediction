# -*- coding: utf-8 -*-
# src/interactive/eda/correlation/heatmap_analyzer.py
#!/usr/bin/env python3
"""
Heatmap Analyzer module.

This module provides correlation heatmap analysis capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class HeatmapAnalyzer:
    """
    Analyzer for correlation heatmap analysis of financial data.
    
    Features:
    - Heatmap pattern analysis
    - Feature clustering detection
    - Multicollinearity check
    - Feature importance by correlation
    """
    
    def __init__(self):
        """Initialize the HeatmapAnalyzer."""
        pass
    
    def run_correlation_heatmap(self, system) -> bool:
        """
        Run correlation heatmap analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🔥 CORRELATION HEATMAP ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("❌ Need at least 2 numerical columns for correlation heatmap.")
            return False
        
        print(f"📊 Generating correlation heatmap for {len(numeric_cols)} numerical columns...")
        
        # Calculate correlation matrix
        correlation_matrix = df[numeric_cols].corr()
        
        # Analyze heatmap patterns
        print(f"\n🔍 Heatmap Pattern Analysis:")
        
        # Check for clustering
        print(f"   • Matrix size: {correlation_matrix.shape[0]} × {correlation_matrix.shape[1]}")
        
        # Find highly correlated feature groups
        print(f"\n🔗 Highly Correlated Feature Groups:")
        
        # Use a threshold to find clusters
        threshold = 0.8
        clusters = []
        used_cols = set()
        
        for i, col1 in enumerate(numeric_cols):
            if col1 in used_cols:
                continue
                
            cluster = [col1]
            used_cols.add(col1)
            
            for j, col2 in enumerate(numeric_cols):
                if col2 in used_cols:
                    continue
                    
                if abs(correlation_matrix.iloc[i, j]) > threshold:
                    cluster.append(col2)
                    used_cols.add(col2)
            
            if len(cluster) > 1:
                clusters.append(cluster)
        
        if clusters:
            for i, cluster in enumerate(clusters):
                print(f"   • Cluster {i+1}: {', '.join(cluster)}")
                print(f"     - Size: {len(cluster)} features")
                print(f"     - Average correlation: {np.mean([correlation_matrix.loc[c1, c2] for c1 in cluster for c2 in cluster if c1 != c2]):.4f}")
        else:
            print(f"   • No highly correlated feature clusters found (threshold: {threshold})")
        
        # Check for multicollinearity
        print(f"\n⚠️  Multicollinearity Check:")
        high_corr_pairs = []
        
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                col1 = numeric_cols[i]
                col2 = numeric_cols[j]
                corr_value = correlation_matrix.iloc[i, j]
                
                if abs(corr_value) > 0.95:
                    high_corr_pairs.append((col1, col2, corr_value))
        
        if high_corr_pairs:
            print(f"   • High multicollinearity detected (|r| > 0.95):")
            for col1, col2, corr_value in high_corr_pairs:
                print(f"     - {col1} ↔ {col2}: {corr_value:.4f}")
            print(f"   • Recommendation: Consider removing one of these highly correlated features")
        else:
            print(f"   • No severe multicollinearity detected (|r| ≤ 0.95)")
        
        # Feature importance based on correlation
        print(f"\n🎯 Feature Importance by Correlation:")
        
        # Calculate average absolute correlation for each feature
        feature_importance = []
        for col in numeric_cols:
            avg_abs_corr = np.abs(correlation_matrix[col]).mean()
            feature_importance.append((col, avg_abs_corr))
        
        # Sort by importance
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        for i, (col, importance) in enumerate(feature_importance[:5]):  # Show top 5
            print(f"   • {i+1}. {col}: {importance:.4f}")
        
        return True
