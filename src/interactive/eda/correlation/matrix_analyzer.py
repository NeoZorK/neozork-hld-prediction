#!/usr/bin/env python3
"""
Matrix Analyzer module.

This module provides correlation matrix analysis capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class MatrixAnalyzer:
    """
    Analyzer for correlation matrix analysis of financial data.
    
    Features:
    - Correlation matrix calculation
    - Strong correlation detection
    - Moderate correlation detection
    - Correlation summary statistics
    """
    
    def __init__(self):
        """Initialize the MatrixAnalyzer."""
        pass
    
    def run_correlation_matrix(self, system) -> bool:
        """
        Run correlation matrix analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🔗 CORRELATION MATRIX ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("❌ Need at least 2 numerical columns for correlation matrix.")
            return False
        
        print(f"📊 Correlation matrix for {len(numeric_cols)} numerical columns:")
        
        # Calculate correlation matrix
        correlation_matrix = df[numeric_cols].corr()
        
        # Display correlation matrix
        print(f"\n📈 Correlation Matrix:")
        print(correlation_matrix.round(4))
        
        # Find strongest correlations
        print(f"\n🔍 Strongest Correlations (|r| > 0.7):")
        strong_correlations = []
        
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                col1 = numeric_cols[i]
                col2 = numeric_cols[j]
                corr_value = correlation_matrix.iloc[i, j]
                
                if abs(corr_value) > 0.7:
                    strong_correlations.append((col1, col2, corr_value))
        
        if strong_correlations:
            # Sort by absolute correlation value
            strong_correlations.sort(key=lambda x: abs(x[2]), reverse=True)
            
            for col1, col2, corr_value in strong_correlations[:10]:  # Show top 10
                strength = "Very Strong" if abs(corr_value) > 0.9 else "Strong"
                direction = "Positive" if corr_value > 0 else "Negative"
                print(f"   • {col1} ↔ {col2}: {corr_value:.4f} ({strength} {direction})")
        else:
            print("   • No strong correlations found (|r| > 0.7)")
        
        # Find moderate correlations
        print(f"\n🔍 Moderate Correlations (0.3 < |r| ≤ 0.7):")
        moderate_correlations = []
        
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                col1 = numeric_cols[i]
                col2 = numeric_cols[j]
                corr_value = correlation_matrix.iloc[i, j]
                
                if 0.3 < abs(corr_value) <= 0.7:
                    moderate_correlations.append((col1, col2, corr_value))
        
        if moderate_correlations:
            # Sort by absolute correlation value
            moderate_correlations.sort(key=lambda x: abs(x[2]), reverse=True)
            
            for col1, col2, corr_value in moderate_correlations[:10]:  # Show top 10
                direction = "Positive" if corr_value > 0 else "Negative"
                print(f"   • {col1} ↔ {col2}: {corr_value:.4f} (Moderate {direction})")
        else:
            print("   • No moderate correlations found (0.3 < |r| ≤ 0.7)")
        
        # Correlation summary statistics
        print(f"\n📊 Correlation Summary:")
        all_correlations = []
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                all_correlations.append(correlation_matrix.iloc[i, j])
        
        all_correlations = np.array(all_correlations)
        print(f"   • Total correlation pairs: {len(all_correlations)}")
        print(f"   • Mean absolute correlation: {np.abs(all_correlations).mean():.4f}")
        print(f"   • Correlation range: [{all_correlations.min():.4f}, {all_correlations.max():.4f}]")
        print(f"   • Positive correlations: {(all_correlations > 0).sum()} ({(all_correlations > 0).mean() * 100:.1f}%)")
        print(f"   • Negative correlations: {(all_correlations < 0).sum()} ({(all_correlations < 0).mean() * 100:.1f}%)")
        
        return True
