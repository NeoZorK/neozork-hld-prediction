"""
Regression Models Implementation

This module provides regression model implementations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from .base import BaseMLModel
from ...core.exceptions import ModelError, ValidationError


class LinearRegressionModel(BaseMLModel):
    """
    Linear Regression model.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Linear Regression model.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("linear_regression", config)
        self.model = LinearRegression()
    
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
            y: True values
            
        Returns:
            Dictionary containing evaluation metrics
        """
        predictions = self.predict(X)
        
        mse = mean_squared_error(y, predictions)
        mae = mean_absolute_error(y, predictions)
        r2 = r2_score(y, predictions)
        
        return {
            'mse': mse,
            'rmse': np.sqrt(mse),
            'mae': mae,
            'r2': r2
        }


class RandomForestRegressorModel(BaseMLModel):
    """
    Random Forest regression model.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Random Forest model.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("random_forest_regressor", config)
        self.model = RandomForestRegressor(
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
            y: True values
            
        Returns:
            Dictionary containing evaluation metrics
        """
        predictions = self.predict(X)
        
        mse = mean_squared_error(y, predictions)
        mae = mean_absolute_error(y, predictions)
        r2 = r2_score(y, predictions)
        
        # Feature importance
        feature_importance = pd.Series(
            self.model.feature_importances_,
            index=X.columns
        ).sort_values(ascending=False)
        
        return {
            'mse': mse,
            'rmse': np.sqrt(mse),
            'mae': mae,
            'r2': r2,
            'feature_importance': feature_importance.to_dict()
        }


__all__ = ["LinearRegressionModel", "RandomForestRegressorModel"]
