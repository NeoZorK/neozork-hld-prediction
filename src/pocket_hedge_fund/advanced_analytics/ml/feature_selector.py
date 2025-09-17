"""
Feature Selector for advanced analytics.

This module provides feature selection functionality for machine learning models.
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
import logging

logger = logging.getLogger(__name__)


class FeatureSelector:
    """Feature selector for machine learning models."""
    
    def __init__(self, method: str = 'mutual_info', k: int = 10):
        """Initialize feature selector."""
        self.method = method
        self.k = k
        self.selected_features: List[str] = []
        self.feature_scores: Dict[str, float] = {}
        self.logger = logger
    
    def select_features(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Select best features based on the specified method."""
        try:
            if self.method == 'mutual_info':
                selector = SelectKBest(score_func=mutual_info_regression, k=self.k)
            elif self.method == 'f_regression':
                selector = SelectKBest(score_func=f_regression, k=self.k)
            elif self.method == 'random_forest':
                return self._select_with_random_forest(X, y)
            else:
                raise ValueError(f"Unknown method: {self.method}")
            
            selector.fit(X, y)
            selected_indices = selector.get_support(indices=True)
            self.selected_features = [X.columns[i] for i in selected_indices]
            
            # Store feature scores
            if hasattr(selector, 'scores_'):
                self.feature_scores = {
                    X.columns[i]: selector.scores_[i] 
                    for i in selected_indices
                }
            
            self.logger.info(f"Selected {len(self.selected_features)} features using {self.method}")
            return self.selected_features
            
        except Exception as e:
            self.logger.error(f"Error selecting features: {e}")
            return []
    
    def _select_with_random_forest(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Select features using Random Forest feature importance."""
        try:
            rf = RandomForestRegressor(n_estimators=100, random_state=42)
            rf.fit(X, y)
            
            # Get feature importance
            importance_scores = rf.feature_importances_
            feature_importance = dict(zip(X.columns, importance_scores))
            
            # Sort by importance and select top k
            sorted_features = sorted(
                feature_importance.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            self.selected_features = [feat[0] for feat in sorted_features[:self.k]]
            self.feature_scores = dict(sorted_features[:self.k])
            
            self.logger.info(f"Selected {len(self.selected_features)} features using Random Forest")
            return self.selected_features
            
        except Exception as e:
            self.logger.error(f"Error with Random Forest feature selection: {e}")
            return []
    
    def get_feature_scores(self) -> Dict[str, float]:
        """Get feature importance scores."""
        return self.feature_scores.copy()
    
    def get_selected_features(self) -> List[str]:
        """Get list of selected features."""
        return self.selected_features.copy()
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform data to include only selected features."""
        if not self.selected_features:
            self.logger.warning("No features selected. Returning original data.")
            return X
        
        try:
            return X[self.selected_features]
        except KeyError as e:
            self.logger.error(f"Error transforming data: {e}")
            return X
    
    def fit_transform(self, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        """Fit selector and transform data."""
        self.select_features(X, y)
        return self.transform(X)
    
    def get_feature_ranking(self) -> List[Tuple[str, float]]:
        """Get features ranked by importance."""
        if not self.feature_scores:
            return []
        
        return sorted(
            self.feature_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
