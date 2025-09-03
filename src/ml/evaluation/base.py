"""
Base Evaluation Components

This module provides base classes for model evaluation.
"""

import pandas as pd
from typing import Dict, Any, Optional, List
import numpy as np
from abc import ABC, abstractmethod
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ...core.base import BaseComponent
from ...core.exceptions import ModelError, ValidationError


class BaseEvaluator(BaseComponent, ABC):
    """
    Base class for model evaluation components.
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize evaluator.
        
        Args:
            name: Name of the evaluator
            config: Configuration dictionary
        """
        super().__init__(name, config)
        self.metrics = config.get("metrics", ["mse", "mae", "r2"])
    
    @abstractmethod
    def evaluate(self, y_true: pd.Series, y_pred: pd.Series) -> Dict[str, Any]:
        """
        Evaluate predictions.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary containing evaluation metrics
        """
        pass
    
    def validate_data(self, y_true: pd.Series, y_pred: pd.Series) -> None:
        """
        Validate evaluation data.
        
        Args:
            y_true: True values
            y_pred: Predicted values
        """
        if y_true.empty or y_pred.empty:
            raise ValidationError("Evaluation data cannot be empty")
        
        if len(y_true) != len(y_pred):
            raise ValidationError("True and predicted values must have same length")


class ModelEvaluator(BaseEvaluator):
    """
    Standard model evaluator for regression tasks.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize model evaluator.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("model_evaluator", config)
    
    def evaluate(self, y_true: pd.Series, y_pred: pd.Series) -> Dict[str, Any]:
        """
        Evaluate regression predictions.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary containing evaluation metrics
        """
        self.validate_data(y_true, y_pred)
        
        results = {}
        
        # Calculate standard regression metrics
        if "mse" in self.metrics:
            results["mse"] = mean_squared_error(y_true, y_pred)
        
        if "rmse" in self.metrics:
            results["rmse"] = np.sqrt(mean_squared_error(y_true, y_pred))
        
        if "mae" in self.metrics:
            results["mae"] = mean_absolute_error(y_true, y_pred)
        
        if "r2" in self.metrics:
            results["r2"] = r2_score(y_true, y_pred)
        
        # Additional metrics
        if "mape" in self.metrics:
            # Mean Absolute Percentage Error
            results["mape"] = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        self.logger.debug(f"Evaluated predictions with {len(self.metrics)} metrics")
        return results


__all__ = ["BaseEvaluator", "ModelEvaluator"]
