# -*- coding: utf-8 -*-
# src/interactive/eda/feature_importance/insights_analyzer.py
#!/usr/bin/env python3
"""
Insights Analyzer module.

This module provides feature importance insights capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class InsightsAnalyzer:
    """
    Analyzer for feature importance insights of financial data.
    
    Features:
    - Business insights
    - Statistical insights
    - Machine learning insights
    - Data quality insights
    - Actionable recommendations
    """
    
    def __init__(self):
        """Initialize the InsightsAnalyzer."""
        pass
    
    def run_feature_importance_insights(self, system) -> bool:
        """
        Run feature importance insights analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n💡 FEATURE IMPORTANCE INSIGHTS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("❌ Need at least 2 numerical columns for feature importance insights.")
            return False
        
        print(f"🧠 Generating insights from feature importance analysis...")
        
        # 1. Business insights
        print(f"\n💼 Business Insights:")
        
        # Check for financial patterns
        ohlcv_cols = [col for col in numeric_cols if col.upper() in ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'VOL']]
        if len(ohlcv_cols) >= 2:
            print(f"   • OHLCV Feature Analysis:")
            
            # Analyze OHLCV feature importance
            for col in ohlcv_cols:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    variance = col_data.var()
                    cv = col_data.std() / abs(col_data.mean()) if col_data.mean() != 0 else 0
                    
                    print(f"     - {col}:")
                    print(f"       Variance: {variance:.6f}")
                    print(f"       CV: {cv:.4f}")
                    
                    # Interpret financial significance
                    if 'VOLUME' in col.upper():
                        if cv > 1:
                            print(f"       → High volume volatility - active trading")
                        else:
                            print(f"       → Stable volume - consistent trading")
                    elif col.upper() in ['HIGH', 'LOW']:
                        if cv > 0.1:
                            print(f"       → High price volatility - wide spreads")
                        else:
                            print(f"       → Low price volatility - tight spreads")
        
        # 2. Statistical insights
        print(f"\n📊 Statistical Insights:")
        
        # Feature diversity analysis
        feature_diversity = {}
        for col in numeric_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                # Calculate coefficient of variation
                cv = col_data.std() / abs(col_data.mean()) if col_data.mean() != 0 else 0
                feature_diversity[col] = cv
        
        if feature_diversity:
            # Find most and least diverse features
            most_diverse = max(feature_diversity, key=feature_diversity.get)
            least_diverse = min(feature_diversity, key=feature_diversity.get)
            
            print(f"   • Feature Diversity:")
            print(f"     - Most diverse: {most_diverse} (CV: {feature_diversity[most_diverse]:.4f})")
            print(f"     - Least diverse: {least_diverse} (CV: {feature_diversity[least_diverse]:.4f})")
            
            # Interpret diversity
            if feature_diversity[most_diverse] > 1:
                print(f"     - High diversity suggests strong feature discrimination")
            elif feature_diversity[most_diverse] < 0.1:
                print(f"     - Low diversity suggests weak feature discrimination")
        
        # 3. Machine learning insights
        print(f"\n🤖 Machine Learning Insights:")
        
        # Feature selection recommendations
        print(f"   • Feature Selection Recommendations:")
        
        # Check for multicollinearity
        high_corr_pairs = []
        for i, col1 in enumerate(numeric_cols):
            for j in range(i + 1, len(numeric_cols)):
                col2 = numeric_cols[j]
                corr = df[col1].corr(df[col2])
                if not pd.isna(corr) and abs(corr) > 0.9:
                    high_corr_pairs.append((col1, col2, corr))
        
        if high_corr_pairs:
            print(f"     - High multicollinearity detected:")
            for col1, col2, corr in high_corr_pairs[:3]:  # Show first 3
                print(f"       • {col1} ↔ {col2}: {corr:.4f}")
            print(f"     - Recommendation: Remove one feature from each pair")
        else:
            print(f"     - No severe multicollinearity detected")
        
        # Feature importance for different ML algorithms
        print(f"\n   • Algorithm-specific Recommendations:")
        
        # Linear models
        print(f"     - Linear Models (Linear Regression, Logistic Regression):")
        print(f"       • Prefer features with low correlation")
        print(f"       • Consider feature scaling for wide ranges")
        
        # Tree-based models
        print(f"     - Tree-based Models (Random Forest, XGBoost):")
        print(f"       • Handle non-linear relationships well")
        print(f"       • Feature scaling not required")
        
        # Neural networks
        print(f"     - Neural Networks (LSTM, RNN):")
        print(f"       • Require feature scaling")
        print(f"       • Can handle high-dimensional data")
        
        # 4. Data quality insights
        print(f"\n🔍 Data Quality Insights:")
        
        # Missing value impact on feature importance
        missing_impact = {}
        for col in numeric_cols:
            missing_pct = (df[col].isnull().sum() / len(df)) * 100
            missing_impact[col] = missing_pct
        
        if missing_impact:
            high_missing = {col: pct for col, pct in missing_impact.items() if pct > 20}
            if high_missing:
                print(f"   • High Missing Values Impact:")
                for col, pct in high_missing.items():
                    print(f"     - {col}: {pct:.1f}% missing")
                    print(f"       → May reduce feature importance")
                    print(f"       → Consider imputation or removal")
            else:
                print(f"   • Missing values are within acceptable limits")
        
        # Outlier impact
        print(f"\n   • Outlier Impact Analysis:")
        
        for col in numeric_cols[:3]:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                q75 = col_data.quantile(0.75)
                q25 = col_data.quantile(0.25)
                iqr = q75 - q25
                outlier_threshold = q75 + 1.5 * iqr
                outliers = col_data[col_data > outlier_threshold]
                
                outlier_pct = (len(outliers) / len(col_data)) * 100
                print(f"     - {col}: {outlier_pct:.1f}% outliers")
                
                if outlier_pct > 5:
                    print(f"       → High outlier percentage - consider robust methods")
                elif outlier_pct > 1:
                    print(f"       → Moderate outliers - standard methods should work")
                else:
                    print(f"       → Low outliers - clean data")
        
        # 5. Actionable recommendations
        print(f"\n💡 Actionable Recommendations:")
        
        # Based on analysis results
        print(f"   • Immediate Actions:")
        
        # Check for critical issues
        critical_issues = []
        
        if high_corr_pairs:
            critical_issues.append("Address multicollinearity")
        
        high_missing_features = [col for col, pct in missing_impact.items() if pct > 50]
        if high_missing_features:
            critical_issues.append("Remove features with >50% missing values")
        
        if critical_issues:
            for issue in critical_issues:
                print(f"     - ⚠️  {issue}")
        else:
            print(f"     - ✅ No critical issues detected")
        
        print(f"\n   • Feature Engineering Opportunities:")
        
        # Suggest feature engineering based on patterns
        if len(ohlcv_cols) >= 2:
            print(f"     - Create OHLCV ratios (High/Low, Close/Open)")
            print(f"     - Calculate price momentum features")
            print(f"     - Generate volatility indicators")
        
        # Suggest transformations
        skewed_features = [col for col in numeric_cols if abs(df[col].skew()) > 1]
        if skewed_features:
            print(f"     - Apply log transformation to: {', '.join(skewed_features[:3])}")
        
        print(f"\n   • Model Selection Guidance:")
        
        # Based on feature characteristics
        if len(high_corr_pairs) > len(numeric_cols) * 0.3:
            print(f"     - High correlation suggests: Ridge/Lasso regression")
        else:
            print(f"     - Low correlation suggests: Standard linear models")
        
        if any(df[col].skew() > 2 for col in numeric_cols):
            print(f"     - High skewness suggests: Tree-based models")
        else:
            print(f"     - Normal distributions suggest: Linear models work well")
        
        return True
