"""
Unit tests for ml.training module.
"""

import pytest
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from unittest.mock import Mock

from src.ml.training.base import BaseTrainer, SimpleTrainer
from src.core.exceptions import ModelError, ValidationError


class MockTrainer(BaseTrainer):
    """Mock trainer for testing."""
    
    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series) -> Any:
        """Mock implementation of train_model."""
        return Mock()
    
    def split_data(self, data: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Mock implementation of split_data."""
        X = data.drop(columns=[target_column])
        y = data[target_column]
        return X, X, y, y


class TestBaseTrainer:
    """Test cases for BaseTrainer class."""
    
    def test_trainer_initialization(self):
        """Test trainer initialization."""
        config = {"test": "value"}
        trainer = MockTrainer("test_trainer", config)
        
        assert trainer.name == "test_trainer"
        assert trainer.config == config
        assert isinstance(trainer, BaseTrainer)
    
    def test_base_trainer_abstract_methods(self):
        """Test that BaseTrainer is abstract."""
        abstract_methods = BaseTrainer.__abstractmethods__
        assert 'train_model' in abstract_methods


class TestSimpleTrainer:
    """Test cases for SimpleTrainer class."""
    
    def test_simple_trainer_initialization(self):
        """Test simple trainer initialization."""
        config = {"test": "value"}
        trainer = SimpleTrainer(config)
        
        assert trainer.config == config
        assert isinstance(trainer, SimpleTrainer)
    
    def test_split_data(self):
        """Test data splitting."""
        trainer = SimpleTrainer({})
        
        # Test with sample data
        test_data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50],
            'target': [0, 1, 0, 1, 0]
        })
        
        X_train, X_test, y_train, y_test = trainer.split_data(test_data, 'target')
        
        # Should have correct shapes
        assert len(X_train) > 0
        assert len(X_test) > 0
        assert len(y_train) > 0
        assert len(y_test) > 0
        assert 'target' not in X_train.columns
        assert 'target' not in X_test.columns


__all__ = ["TestBaseTrainer", "TestSimpleTrainer"]
