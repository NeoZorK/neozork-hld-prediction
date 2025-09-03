"""
Unit tests for ml.pipeline module.
"""

import pytest
import pandas as pd
import numpy as np
from typing import Dict, Any
from unittest.mock import Mock

from src.ml.pipeline.base import BaseMLPipeline
from src.core.exceptions import ModelError, ValidationError


class TestBaseMLPipeline:
    """Test cases for BaseMLPipeline class."""
    
    def test_pipeline_initialization(self):
        """Test pipeline initialization."""
        config = {"test": "value"}
        pipeline = BaseMLPipeline("test_pipeline", config)
        
        assert pipeline.name == "test_pipeline"
        assert pipeline.config == config
        assert isinstance(pipeline, BaseMLPipeline)
    
    def test_set_feature_engineer(self):
        """Test setting feature engineer."""
        pipeline = BaseMLPipeline("test", {})
        mock_engineer = Mock()
        
        pipeline.set_feature_engineer(mock_engineer)
        
        assert pipeline.feature_engineer == mock_engineer
    
    def test_set_model(self):
        """Test setting model."""
        pipeline = BaseMLPipeline("test", {})
        mock_model = Mock()
        
        pipeline.set_model(mock_model)
        
        assert pipeline.model == mock_model
    
    def test_set_evaluator(self):
        """Test setting evaluator."""
        pipeline = BaseMLPipeline("test", {})
        mock_evaluator = Mock()
        
        pipeline.set_evaluator(mock_evaluator)
        
        assert pipeline.evaluator == mock_evaluator
    
    def test_fit_pipeline(self):
        """Test pipeline fitting."""
        pipeline = BaseMLPipeline("test", {})
        
        # Mock components
        mock_engineer = Mock()
        mock_engineer.create_features.return_value = pd.DataFrame({'feature': [1, 2, 3]})
        
        mock_model = Mock()
        mock_model.train.return_value = True
        
        pipeline.set_feature_engineer(mock_engineer)
        pipeline.set_model(mock_model)
        
        # Test data
        test_data = pd.DataFrame({'price': [1, 2, 3]})
        
        result = pipeline.fit(test_data)
        
        assert result is True
        mock_engineer.create_features.assert_called_once()
        mock_model.train.assert_called_once()
    
    def test_predict_pipeline(self):
        """Test pipeline prediction."""
        pipeline = BaseMLPipeline("test", {})
        
        # Mock components
        mock_engineer = Mock()
        mock_engineer.create_features.return_value = pd.DataFrame({'feature': [1, 2, 3]})
        
        mock_model = Mock()
        mock_model.predict.return_value = np.array([0.5, 0.7, 0.9])
        
        pipeline.set_feature_engineer(mock_engineer)
        pipeline.set_model(mock_model)
        
        # Test data
        test_data = pd.DataFrame({'price': [1, 2, 3]})
        
        result = pipeline.predict(test_data)
        
        assert len(result) == 3
        mock_engineer.create_features.assert_called_once()
        mock_model.predict.assert_called_once()


__all__ = ["TestBaseMLPipeline"]
