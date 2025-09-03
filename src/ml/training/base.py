"""
Base Training Components

This module provides base classes for model training.
"""

import pandas as pd
from typing import Dict, Any, Optional, Tuple
import numpy as np
from abc import ABC, abstractmethod
from sklearn.model_selection import train_test_split

from ...core.base import BaseComponent
from ...core.exceptions import ModelError, ValidationError


class BaseTrainer(BaseComponent, ABC):
    """
    Base class for model training components.
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize trainer.
        
        Args:
            name: Name of the trainer
            config: Configuration dictionary
        """
        super().__init__(name, config)
        self.test_size = config.get("test_size", 0.2)
        self.random_state = config.get("random_state", 42)
        self.validation_split = config.get("validation_split", 0.2)
    
    @abstractmethod
    def train_model(self, model: Any, X: pd.DataFrame, y: pd.Series) -> Any:
        """
        Train a model.
        
        Args:
            model: Model to train
            X: Feature data
            y: Target data
            
        Returns:
            Trained model
        """
        pass
    
    def split_data(self, X: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Split data into training and testing sets.
        
        Args:
            X: Feature data
            y: Target data
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        return train_test_split(
            X, y, 
            test_size=self.test_size, 
            random_state=self.random_state
        )


class SimpleTrainer(BaseTrainer):
    """
    Simple model trainer.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize simple trainer.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("simple_trainer", config)
    
    def train_model(self, model: Any, X: pd.DataFrame, y: pd.Series) -> Any:
        """
        Train a model using simple fit method.
        
        Args:
            model: Model to train
            X: Feature data
            y: Target data
            
        Returns:
            Trained model
        """
        if X.empty or y.empty:
            raise ValidationError("Training data cannot be empty")
        
        if len(X) != len(y):
            raise ValidationError("Feature and target data must have same length")
        
        try:
            model.fit(X, y)
            self.logger.info(f"Trained model on {len(X)} samples")
            return model
        except Exception as e:
            raise ModelError(f"Training failed: {e}")


__all__ = ["BaseTrainer", "SimpleTrainer"]
