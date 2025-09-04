"""
Classification Models Implementation

This module provides classification model implementations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from .base import BaseMLModel
from ...core.exceptions import ModelError, ValidationError


class LogisticRegressionModel(BaseMLModel):
    """
    Logistic Regression classification model.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Logistic Regression model.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("logistic_regression", config)
        self.model = LogisticRegression(
            random_state=config.get("random_state", 42),
            max_iter=config.get("max_iter", 1000)
        )
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Train the model.
        
        Args:
            X: Feature data
            y: Target data
        """
        self.validate_training_data(X, y)
        
        try:
            self.model.fit(X, y)
            self.is_trained = True
            self.logger.info(f"Trained {self.name} on {len(X)} samples")
        except Exception as e:
            raise ModelError(f"Training failed: {e}")
    
    def predict(self, X: pd.DataFrame) -> pd.Series:
        """
        Make predictions.
        
        Args:
            X: Feature data
            
        Returns:
            Predictions
        """
        if not self.is_trained:
            raise ModelError("Model must be trained before prediction")
        
        try:
            predictions = self.model.predict(X)
            return pd.Series(predictions, index=X.index)
        except Exception as e:
            raise ModelError(f"Prediction failed: {e}")
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """
        Evaluate model performance.
        
        Args:
            X: Feature data
            y: True labels
            
        Returns:
            Dictionary containing evaluation metrics
        """
        predictions = self.predict(X)
        
        accuracy = accuracy_score(y, predictions)
        report = classification_report(y, predictions, output_dict=True)
        
        return {
            'accuracy': accuracy,
            'classification_report': report
        }


class RandomForestClassifierModel(BaseMLModel):
    """
    Random Forest classification model.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Random Forest model.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("random_forest_classifier", config)
        self.model = RandomForestClassifier(
            n_estimators=config.get("n_estimators", 100),
            random_state=config.get("random_state", 42),
            max_depth=config.get("max_depth", None)
        )
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Train the model.
        
        Args:
            X: Feature data
            y: Target data
        """
        self.validate_training_data(X, y)
        
        try:
            self.model.fit(X, y)
            self.is_trained = True
            self.logger.info(f"Trained {self.name} on {len(X)} samples")
        except Exception as e:
            raise ModelError(f"Training failed: {e}")
    
    def predict(self, X: pd.DataFrame) -> pd.Series:
        """
        Make predictions.
        
        Args:
            X: Feature data
            
        Returns:
            Predictions
        """
        if not self.is_trained:
            raise ModelError("Model must be trained before prediction")
        
        try:
            predictions = self.model.predict(X)
            return pd.Series(predictions, index=X.index)
        except Exception as e:
            raise ModelError(f"Prediction failed: {e}")
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """
        Evaluate model performance.
        
        Args:
            X: Feature data
            y: True labels
            
        Returns:
            Dictionary containing evaluation metrics
        """
        predictions = self.predict(X)
        
        accuracy = accuracy_score(y, predictions)
        report = classification_report(y, predictions, output_dict=True)
        
        # Feature importance
        feature_importance = pd.Series(
            self.model.feature_importances_,
            index=X.columns
        ).sort_values(ascending=False)
        
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'feature_importance': feature_importance.to_dict()
        }


__all__ = ["LogisticRegressionModel", "RandomForestClassifierModel"]
