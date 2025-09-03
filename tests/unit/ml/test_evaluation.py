"""
Unit tests for ml.evaluation module.
"""

import pytest
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from unittest.mock import Mock

from src.ml.evaluation.base import BaseEvaluator, ModelEvaluator
from src.core.exceptions import ModelError, ValidationError


class MockEvaluator(BaseEvaluator):
    """Mock evaluator for testing."""
    
    def evaluate(self, y_true: pd.Series, y_pred: pd.Series) -> Dict[str, float]:
        """Mock implementation of evaluate."""
        return {"mock_metric": 0.85}


class TestBaseEvaluator:
    """Test cases for BaseEvaluator class."""
    
    def test_evaluator_initialization(self):
        """Test evaluator initialization."""
        config = {"test": "value"}
        evaluator = MockEvaluator("test_evaluator", config)
        
        assert evaluator.name == "test_evaluator"
        assert evaluator.config == config
        assert isinstance(evaluator, BaseEvaluator)
    
    def test_base_evaluator_abstract_method(self):
        """Test that BaseEvaluator is abstract."""
        abstract_methods = BaseEvaluator.__abstractmethods__
        assert 'evaluate' in abstract_methods


class TestModelEvaluator:
    """Test cases for ModelEvaluator class."""
    
    def test_model_evaluator_initialization(self):
        """Test model evaluator initialization."""
        config = {"test": "value"}
        evaluator = ModelEvaluator(config)
        
        assert evaluator.config == config
        assert isinstance(evaluator, ModelEvaluator)
    
    def test_evaluate_regression_metrics(self):
        """Test regression metrics evaluation."""
        evaluator = ModelEvaluator({})
        
        # Test with sample data
        y_true = pd.Series([1, 2, 3, 4, 5])
        y_pred = pd.Series([1.1, 1.9, 3.1, 3.9, 5.1])
        
        result = evaluator.evaluate(y_true, y_pred)
        
        # Should have regression metrics
        assert 'mse' in result
        assert 'mae' in result
        assert 'r2' in result
        assert isinstance(result['mse'], float)
        assert isinstance(result['mae'], float)
        assert isinstance(result['r2'], float)


__all__ = ["TestBaseEvaluator", "TestModelEvaluator"]
