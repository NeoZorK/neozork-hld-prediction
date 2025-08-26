# -*- coding: utf-8 -*-
# src/ml/feature_engineering/feature_selector.py

"""
Feature selector for NeoZorK HLD Prediction.

This module provides intelligent feature selection and optimization
to reduce dimensionality and improve ML model performance.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from dataclasses import dataclass
from sklearn.feature_selection import (
    SelectKBest, f_regression, mutual_info_regression,
    SelectFromModel, RFE
)
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
import warnings

from .logger import logger

# Suppress sklearn warnings
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')


@dataclass
class FeatureSelectionConfig:
    """Configuration for feature selection."""
    
    # Selection methods
    methods: List[str] = None
    
    # Maximum number of features to select
    max_features: int = 200
    
    # Minimum importance threshold
    min_importance: float = 0.3
    
    # Correlation threshold for removing highly correlated features
    correlation_threshold: float = 0.95
    
    # Cross-validation folds for model-based selection
    cv_folds: int = 5
    
    # Random state for reproducibility
    random_state: int = 42
    
    def __post_init__(self):
        """Set default values if not provided."""
        if self.methods is None:
            self.methods = ['correlation', 'importance', 'mutual_info', 'lasso']


class FeatureSelector:
    """
    Intelligent feature selector for ML trading features.
    
    This class provides multiple feature selection methods to optimize
    the feature set for ML models.
    """
    
    def __init__(self, config: FeatureSelectionConfig = None):
        """
        Initialize the feature selector.
        
        Args:
            config: Configuration for feature selection
        """
        self.config = config or FeatureSelectionConfig()
        self.selected_features = []
        self.feature_scores = {}
        self.correlation_matrix = None
        
    def select_features(self, X: pd.DataFrame, feature_importance: Dict[str, float], 
                       max_features: int = None) -> List[str]:
        """
        Select the best features using multiple methods.
        
        Args:
            X: Feature matrix
            feature_importance: Dictionary of feature importance scores
            max_features: Maximum number of features to select
            
        Returns:
            List of selected feature names
        """
        if max_features is None:
            max_features = self.config.max_features
            
        logger.print_info(f"Starting feature selection from {len(X.columns)} features")
        
        # Initialize feature scores
        self.feature_scores = {feature: 0.0 for feature in X.columns}
        
        # Apply different selection methods
        for method in self.config.methods:
            try:
                if method == 'correlation':
                    self._apply_correlation_selection(X)
                elif method == 'importance':
                    self._apply_importance_selection(feature_importance)
                elif method == 'mutual_info':
                    self._apply_mutual_info_selection(X)
                elif method == 'lasso':
                    self._apply_lasso_selection(X)
                elif method == 'random_forest':
                    self._apply_random_forest_selection(X)
                    
            except Exception as e:
                logger.print_warning(f"Error applying {method} selection: {e}")
                continue
                
        # Normalize and combine scores
        self._normalize_scores()
        
        # Select top features
        selected_features = self._select_top_features(max_features)
        
        logger.print_info(f"Selected {len(selected_features)} features after selection")
        
        return selected_features
    
    def _apply_correlation_selection(self, X: pd.DataFrame):
        """Apply correlation-based feature selection."""
        try:
            # Calculate correlation matrix
            self.correlation_matrix = X.corr().abs()
            
            # Find highly correlated feature pairs
            high_corr_pairs = []
            for i in range(len(self.correlation_matrix.columns)):
                for j in range(i+1, len(self.correlation_matrix.columns)):
                    if self.correlation_matrix.iloc[i, j] > self.config.correlation_threshold:
                        high_corr_pairs.append((
                            self.correlation_matrix.columns[i],
                            self.correlation_matrix.columns[j],
                            self.correlation_matrix.iloc[i, j]
                        ))
                        
            # Penalize highly correlated features
            for feature1, feature2, corr in high_corr_pairs:
                if feature1 in self.feature_scores and feature2 in self.feature_scores:
                    # Reduce score for both features
                    penalty = corr * 0.5
                    self.feature_scores[feature1] -= penalty
                    self.feature_scores[feature2] -= penalty
                    
            logger.print_info(f"Applied correlation selection, found {len(high_corr_pairs)} high-correlation pairs")
            
        except Exception as e:
            logger.print_error(f"Error in correlation selection: {e}")
    
    def _apply_importance_selection(self, feature_importance: Dict[str, float]):
        """Apply importance-based feature selection."""
        try:
            for feature, importance in feature_importance.items():
                if feature in self.feature_scores:
                    # Add importance score
                    self.feature_scores[feature] += importance
                    
            logger.print_info("Applied importance-based selection")
            
        except Exception as e:
            logger.print_error(f"Error in importance selection: {e}")
    
    def _apply_mutual_info_selection(self, X: pd.DataFrame):
        """Apply mutual information-based feature selection."""
        try:
            # Create target variable (price changes)
            y = X['Close'].pct_change().fillna(0) if 'Close' in X.columns else pd.Series(0, index=X.index)
            
            # Remove non-numeric columns and target
            X_numeric = X.select_dtypes(include=[np.number])
            if 'Close' in X_numeric.columns:
                X_numeric = X_numeric.drop(columns=['Close'])
                
            if len(X_numeric.columns) == 0:
                return
                
            # Calculate mutual information
            try:
                mi_scores = mutual_info_regression(X_numeric.fillna(0), y, random_state=self.config.random_state)
                mi_dict = dict(zip(X_numeric.columns, mi_scores))
                
                # Add mutual information scores
                for feature, mi_score in mi_dict.items():
                    if feature in self.feature_scores:
                        self.feature_scores[feature] += mi_score
                        
                logger.print_info("Applied mutual information selection")
                
            except Exception as e:
                logger.print_warning(f"Mutual information calculation failed: {e}")
                
        except Exception as e:
            logger.print_error(f"Error in mutual information selection: {e}")
    
    def _apply_lasso_selection(self, X: pd.DataFrame):
        """Apply Lasso-based feature selection."""
        try:
            # Create target variable
            y = X['Close'].pct_change().fillna(0) if 'Close' in X.columns else pd.Series(0, index=X.index)
            
            # Remove non-numeric columns and target
            X_numeric = X.select_dtypes(include=[np.number])
            if 'Close' in X_numeric.columns:
                X_numeric = X_numeric.drop(columns=['Close'])
                
            if len(X_numeric.columns) == 0:
                return
                
            # Standardize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_numeric.fillna(0))
            
            # Apply Lasso
            try:
                lasso = LassoCV(cv=self.config.cv_folds, random_state=self.config.random_state)
                lasso.fit(X_scaled, y)
                
                # Get feature importance from Lasso coefficients
                lasso_importance = np.abs(lasso.coef_)
                lasso_dict = dict(zip(X_numeric.columns, lasso_importance))
                
                # Add Lasso scores
                for feature, lasso_score in lasso_dict.items():
                    if feature in self.feature_scores:
                        self.feature_scores[feature] += lasso_score
                        
                logger.print_info("Applied Lasso-based selection")
                
            except Exception as e:
                logger.print_warning(f"Lasso calculation failed: {e}")
                
        except Exception as e:
            logger.print_error(f"Error in Lasso selection: {e}")
    
    def _apply_random_forest_selection(self, X: pd.DataFrame):
        """Apply Random Forest-based feature selection."""
        try:
            # Create target variable
            y = X['Close'].pct_change().fillna(0) if 'Close' in X.columns else pd.Series(0, index=X.index)
            
            # Remove non-numeric columns and target
            X_numeric = X.select_dtypes(include=[np.number])
            if 'Close' in X_numeric.columns:
                X_numeric = X_numeric.drop(columns=['Close'])
                
            if len(X_numeric.columns) == 0:
                return
                
            # Apply Random Forest
            try:
                rf = RandomForestRegressor(
                    n_estimators=100,
                    random_state=self.config.random_state,
                    n_jobs=-1
                )
                rf.fit(X_numeric.fillna(0), y)
                
                # Get feature importance
                rf_importance = rf.feature_importances_
                rf_dict = dict(zip(X_numeric.columns, rf_importance))
                
                # Add Random Forest scores
                for feature, rf_score in rf_dict.items():
                    if feature in self.feature_scores:
                        self.feature_scores[feature] += rf_score
                        
                logger.print_info("Applied Random Forest-based selection")
                
            except Exception as e:
                logger.print_warning(f"Random Forest calculation failed: {e}")
                
        except Exception as e:
            logger.print_error(f"Error in Random Forest selection: {e}")
    
    def _normalize_scores(self):
        """Normalize feature scores to 0-1 range."""
        try:
            if not self.feature_scores:
                return
                
            # Get min and max scores
            min_score = min(self.feature_scores.values())
            max_score = max(self.feature_scores.values())
            
            if max_score > min_score:
                # Normalize to 0-1 range
                for feature in self.feature_scores:
                    self.feature_scores[feature] = (self.feature_scores[feature] - min_score) / (max_score - min_score)
            else:
                # All scores are the same, set to 0.5
                for feature in self.feature_scores:
                    self.feature_scores[feature] = 0.5
                    
        except Exception as e:
            logger.print_error(f"Error normalizing scores: {e}")
    
    def _select_top_features(self, max_features: int) -> List[str]:
        """Select top features based on scores."""
        try:
            # Sort features by score
            sorted_features = sorted(
                self.feature_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Select top features
            selected_features = []
            for feature, score in sorted_features:
                if len(selected_features) >= max_features:
                    break
                    
                # Check minimum importance threshold
                if score >= self.config.min_importance:
                    selected_features.append(feature)
                    
            return selected_features
            
        except Exception as e:
            logger.print_error(f"Error selecting top features: {e}")
            return []
    
    def get_feature_scores(self) -> Dict[str, float]:
        """Get feature selection scores."""
        return self.feature_scores.copy()
    
    def get_correlation_matrix(self) -> Optional[pd.DataFrame]:
        """Get correlation matrix if available."""
        return self.correlation_matrix.copy() if self.correlation_matrix is not None else None
    
    def export_selection_report(self, output_path: str = None) -> str:
        """
        Export feature selection report.
        
        Args:
            output_path: Path to save the report (optional)
            
        Returns:
            Path to the saved report
        """
        try:
            if output_path is None:
                output_path = f"logs/feature_selection_report_{int(time.time())}.txt"
                
            # Ensure directory exists
            import os
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("NEOZORk HLD PREDICTION - FEATURE SELECTION REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                # Configuration
                f.write("Configuration:\n")
                f.write(f"  Methods: {', '.join(self.config.methods)}\n")
                f.write(f"  Max Features: {self.config.max_features}\n")
                f.write(f"  Min Importance: {self.config.min_importance}\n")
                f.write(f"  Correlation Threshold: {self.config.correlation_threshold}\n\n")
                
                # Feature scores
                f.write("Feature Selection Scores:\n")
                sorted_scores = sorted(
                    self.feature_scores.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                
                for i, (feature, score) in enumerate(sorted_scores, 1):
                    f.write(f"  {i:3d}. {feature:<40} {score:.4f}\n")
                    
                f.write("\n")
                
                # Selected features
                f.write(f"Selected Features ({len(self.selected_features)}):\n")
                for feature in self.selected_features:
                    score = self.feature_scores.get(feature, 0.0)
                    f.write(f"  {feature:<50} {score:.4f}\n")
                    
            logger.print_success(f"Feature selection report exported to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.print_error(f"Error exporting feature selection report: {e}")
            return ""
    
    def __str__(self) -> str:
        """String representation of the feature selector."""
        return f"FeatureSelector(methods={len(self.config.methods)}, selected={len(self.selected_features)})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"FeatureSelector(config={self.config}, "
                f"selected_features={len(self.selected_features)}, "
                f"methods={self.config.methods})")
