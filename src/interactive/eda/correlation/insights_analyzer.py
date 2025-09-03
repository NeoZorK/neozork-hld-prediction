# -*- coding: utf-8 -*-
# src/interactive/eda/correlation/insights_analyzer.py
#!/usr/bin/env python3
"""
Insights Analyzer module.

This module provides correlation insights analysis capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class InsightsAnalyzer:
    """
    Analyzer for correlation insights analysis of financial data.
    
    Features:
    - Business insights
    - Statistical insights
    - Correlation structure insights
    - Machine learning implications
    """
    
    def __init__(self):
        """Initialize the InsightsAnalyzer."""
        pass
    
    def run_correlation_insights(self, system) -> bool:
        """
        Run correlation insights analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n💡 CORRELATION INSIGHTS ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("❌ Need at least 2 numerical columns for correlation insights.")
            return False
        
        print(f"🧠 Generating insights from correlation analysis...")
        
        # Calculate correlation matrix
        correlation_matrix = df[numeric_cols].corr()
        
        # Business insights
        print(f"\n💼 Business Insights:")
        
        # Check for financial patterns
        financial_patterns = []
        
        # Look for common financial correlations
        ohlcv_cols = [col for col in numeric_cols if col.upper() in ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'VOL']]
        if len(ohlcv_cols) >= 2:
            print(f"   • OHLCV Analysis:")
            for i, col1 in enumerate(ohlcv_cols):
                for j in range(i + 1, len(ohlcv_cols)):
                    col2 = ohlcv_cols[j]
                    corr_value = correlation_matrix.loc[col1, col2]
                    
                    if abs(corr_value) > 0.5:
                        pattern_type = "Strong" if abs(corr_value) > 0.8 else "Moderate"
                        direction = "Positive" if corr_value > 0 else "Negative"
                        print(f"     - {col1} ↔ {col2}: {corr_value:.4f} ({pattern_type} {direction})")
                        
                        # Interpret the pattern
                        if col1.upper() in ['HIGH', 'LOW'] and col2.upper() in ['HIGH', 'LOW']:
                            print(f"       → High-Low correlation suggests price volatility patterns")
                        elif col1.upper() in ['OPEN', 'CLOSE'] and col2.upper() in ['OPEN', 'CLOSE']:
                            print(f"       → Open-Close correlation indicates trend strength")
                        elif 'VOLUME' in col1.upper() or 'VOLUME' in col2.upper():
                            print(f"       → Volume correlation suggests trading activity patterns")
        
        # Statistical insights
        print(f"\n📊 Statistical Insights:")
        
        # Check for normal distribution indicators
        print(f"   • Distribution Analysis:")
        for col in numeric_cols[:3]:  # Check first 3 columns
            col_data = df[col].dropna()
            if len(col_data) > 0:
                skewness = col_data.skew()
                kurtosis = col_data.kurtosis()
                
                print(f"     - {col}:")
                print(f"       Skewness: {skewness:.4f} ({'Right-skewed' if skewness > 0.5 else 'Left-skewed' if skewness < -0.5 else 'Symmetric'})")
                print(f"       Kurtosis: {kurtosis:.4f} ({'Heavy-tailed' if kurtosis > 3 else 'Light-tailed' if kurtosis < 3 else 'Normal-tailed'})")
        
        # Correlation structure insights
        print(f"\n🔗 Correlation Structure Insights:")
        
        # Check for block diagonal patterns
        print(f"   • Matrix Structure:")
        
        # Count positive vs negative correlations
        all_correlations = []
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                all_correlations.append(correlation_matrix.iloc[i, j])
        
        positive_corr = sum(1 for x in all_correlations if x > 0.1)
        negative_corr = sum(1 for x in all_correlations if x < -0.1)
        weak_corr = sum(1 for x in all_correlations if -0.1 <= x <= 0.1)
        
        print(f"     - Positive correlations: {positive_corr} ({positive_corr/len(all_correlations)*100:.1f}%)")
        print(f"     - Negative correlations: {negative_corr} ({negative_corr/len(all_correlations)*100:.1f}%)")
        print(f"     - Weak correlations: {weak_corr} ({weak_corr/len(all_correlations)*100:.1f}%)")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        
        if positive_corr > negative_corr:
            print(f"   • Data shows predominantly positive correlations")
            print(f"   • Consider using methods that handle positive correlations well")
        elif negative_corr > positive_corr:
            print(f"   • Data shows predominantly negative correlations")
            print(f"   • Consider using methods that handle negative correlations well")
        else:
            print(f"   • Data shows balanced positive/negative correlations")
        
        if weak_corr > len(all_correlations) * 0.5:
            print(f"   • Many weak correlations suggest independent features")
            print(f"   • Good for models that assume feature independence")
        else:
            print(f"   • Strong correlations suggest feature dependencies")
            print(f"   • Consider feature selection or dimensionality reduction")
        
        # ML model implications
        print(f"\n🤖 Machine Learning Implications:")
        
        high_corr_count = sum(1 for x in all_correlations if abs(x) > 0.8)
        if high_corr_count > 0:
            print(f"   • {high_corr_count} high correlations detected (|r| > 0.8)")
            print(f"   • May cause multicollinearity in linear models")
            print(f"   • Consider: Ridge/Lasso regression, feature selection")
        else:
            print(f"   • No severe multicollinearity detected")
            print(f"   • Linear models should work well")
        
        return True
