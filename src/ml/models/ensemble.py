"""
Ensemble Models Implementation

This module provides ensemble model implementations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sklearn.ensemble import VotingClassifier, VotingRegressor

from .base import BaseMLModel
from ...core.exceptions import ModelError, ValidationError


class EnsembleModel(BaseMLModel):
    """
    Ensemble model that combines multiple base models.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ensemble model.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("ensemble_model", config)
        self.base_models = []
        self.ensemble_type = config.get("ensemble_type", "voting")
        self.voting_type = config.get("voting_type", "soft")
    
    def add_model(self, model: BaseMLModel, name: str) -> None:
        """
        Add a base model to the ensemble.
        
        Args:
            model: Base model to add
            name: Name for the model in ensemble
        """
        self.base_models.append((name, model))
        self.logger.debug(f"Added model {name} to ensemble")
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Train the ensemble model.
        
        Args:
            X: Feature data
            y: Target data
        """
        self.validate_training_data(X, y)
        
        if not self.base_models:
            raise ModelError("No base models added to ensemble")
        
        try:
            # Train each base model
            for name, model in self.base_models:
                model.train(X, y)
                self.logger.debug(f"Trained base model {name}")
            
            self.is_trained = True
            self.logger.info(f"Trained ensemble with {len(self.base_models)} models")
            
        except Exception as e:
            raise ModelError(f"Ensemble training failed: {e}")
    
    def predict(self, X: pd.DataFrame) -> pd.Series:
        """
        Make ensemble predictions.
        
        Args:
            X: Feature data
            
        Returns:
            Ensemble predictions
        """
        if not self.is_trained:
            raise ModelError("Ensemble must be trained before prediction")
        
        try:
            # Get predictions from all base models
            predictions = []
            for name, model in self.base_models:
                pred = model.predict(X)
                predictions.append(pred)
            
            # Combine predictions (simple averaging for now)
            ensemble_pred = pd.concat(predictions, axis=1).mean(axis=1)
            
            self.logger.debug(f"Made ensemble predictions using {len(self.base_models)} models")
            return ensemble_pred
            
        except Exception as e:
            raise ModelError(f"Ensemble prediction failed: {e}")
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """
        Evaluate ensemble performance.
        
        Args:
            X: Feature data
            y: True values
            
        Returns:
            Dictionary containing evaluation metrics
        """
        predictions = self.predict(X)
        
        # Basic evaluation metrics
        mse = np.mean((y - predictions) ** 2)
        mae = np.mean(np.abs(y - predictions))
        
        # Individual model performances
        individual_metrics = {}
        for name, model in self.base_models:
            try:
                individual_metrics[name] = model.evaluate(X, y)
            except Exception as e:
                self.logger.warning(f"Could not evaluate model {name}: {e}")
        
        return {
            'ensemble_mse': mse,
            'ensemble_mae': mae,
            'individual_models': individual_metrics
        }


__all__ = ["EnsembleModel"]
