"""
Unit tests for ML models in ML module.

This module tests the machine learning model implementations.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

from src.ml.models.base import BaseMLModel


class MockMLModel(BaseMLModel):
    """Mock ML model for testing."""
    
    def _create_model(self):
        """Create a mock model."""
        return Mock()
    
    def _validate_features(self, features: pd.DataFrame) -> bool:
        """Validate features."""
        return isinstance(features, pd.DataFrame) and len(features) > 0
    
    def _train_model(self, features: pd.DataFrame, targets: pd.Series):
        """Mock training."""
        self.model.fit(features, targets)
    
    def _make_predictions(self, features: pd.DataFrame):
        """Mock predictions."""
        return self.model.predict(features)
    
    def _calculate_metrics(self, targets: pd.Series, predictions) -> dict:
        """Mock metrics calculation."""
        return {"accuracy": 0.85, "precision": 0.82, "recall": 0.78}


class TestBaseMLModel:
    """Test cases for BaseMLModel class."""
    
    def test_init(self):
        """Test BaseMLModel initialization."""
        model = MockMLModel("test_model")
        
        assert model.name == "test_model"
        assert model.model is None
        assert model.is_trained is False
        assert model.training_history == []
        assert model.feature_names == []
        assert model.target_name == ""
        assert model.model_type == "MockMLModel"
    
    def test_init_with_config(self):
        """Test BaseMLModel initialization with config."""
        config = {"param1": "value1", "param2": 42}
        model = MockMLModel("test_model", config)
        
        assert model.config == config
    
    def test_train_success(self):
        """Test successful model training."""
        model = MockMLModel("test_model")
        
        # Mock the model's fit method
        model.model = Mock()
        model.model.fit = Mock()
        
        features = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
        targets = pd.Series([0, 1, 0], name="target")
        
        result = model.train({"features": features, "targets": targets})
        
        assert result is True
        assert model.is_trained is True
        assert len(model.training_history) == 1
        assert model.feature_names == ["feature1", "feature2"]
        assert model.target_name == "target"
    
    def test_train_invalid_data_format(self):
        """Test training with invalid data format."""
        model = MockMLModel("test_model")
        
        with pytest.raises(Exception):
            model.train("invalid_data")
    
    def test_train_missing_features(self):
        """Test training with missing features."""
        model = MockMLModel("test_model")
        
        with pytest.raises(Exception):
            model.train({"targets": pd.Series([0, 1, 0])})
    
    def test_train_missing_targets(self):
        """Test training with missing targets."""
        model = MockMLModel("test_model")
        
        with pytest.raises(Exception):
            model.train({"features": pd.DataFrame({"f1": [1, 2, 3]})})
    
    def test_train_validation_failure(self):
        """Test training with validation failure."""
        model = MockMLModel("test_model")
        
        # Override validation to fail
        model._validate_features = Mock(return_value=False)
        
        with pytest.raises(Exception):
            model.train({"features": pd.DataFrame(), "targets": pd.Series()})
    
    def test_predict_not_trained(self):
        """Test prediction without training."""
        model = MockMLModel("test_model")
        
        with pytest.raises(Exception):
            model.predict(pd.DataFrame({"f1": [1, 2, 3]}))
    
    def test_predict_success(self):
        """Test successful prediction."""
        model = MockMLModel("test_model")
        
        # Train the model first
        model.model = Mock()
        model.model.fit = Mock()
        model.model.predict = Mock(return_value=np.array([0, 1, 0]))
        
        features = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
        targets = pd.Series([0, 1, 0], name="target")
        
        model.train({"features": features, "targets": targets})
        
        # Now test prediction
        test_features = pd.DataFrame({"feature1": [4, 5], "feature2": [7, 8]})
        predictions = model.predict(test_features)
        
        assert predictions is not None
        model.model.predict.assert_called_once()
    
    def test_predict_validation_failure(self):
        """Test prediction with validation failure."""
        model = MockMLModel("test_model")
        
        # Train the model first
        model.model = Mock()
        model.model.fit = Mock()
        
        features = pd.DataFrame({"feature1": [1, 2, 3]})
        targets = pd.Series([0, 1, 0])
        
        model.train({"features": features, "targets": targets})
        
        # Override validation to fail for prediction
        model._validate_features = Mock(return_value=False)
        
        with pytest.raises(Exception):
            model.predict(pd.DataFrame())
    
    def test_evaluate_success(self):
        """Test successful model evaluation."""
        model = MockMLModel("test_model")
        
        # Train the model first
        model.model = Mock()
        model.model.fit = Mock()
        model.model.predict = Mock(return_value=np.array([0, 1, 0]))
        
        features = pd.DataFrame({"feature1": [1, 2, 3]})
        targets = pd.Series([0, 1, 0])
        
        model.train({"features": features, "targets": targets})
        
        # Test evaluation
        test_data = {"features": features, "targets": targets}
        metrics = model.evaluate(test_data)
        
        assert isinstance(metrics, dict)
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
    
    def test_evaluate_not_trained(self):
        """Test evaluation without training."""
        model = MockMLModel("test_model")
        
        with pytest.raises(Exception):
            model.evaluate({"features": pd.DataFrame(), "targets": pd.Series()})
    
    def test_evaluate_invalid_data_format(self):
        """Test evaluation with invalid data format."""
        model = MockMLModel("test_model")
        
        # Train the model first
        model.model = Mock()
        model.model.fit = Mock()
        
        features = pd.DataFrame({"feature1": [1, 2, 3]})
        targets = pd.Series([0, 1, 0])
        
        model.train({"features": features, "targets": targets})
        
        with pytest.raises(Exception):
            model.evaluate("invalid_data")
    
    def test_save_model_success(self):
        """Test successful model saving."""
        model = MockMLModel("test_model")
        
        # Train the model first
        model.model = Mock()
        model.model.fit = Mock()
        
        features = pd.DataFrame({"feature1": [1, 2, 3]})
        targets = pd.Series([0, 1, 0])
        
        model.train({"features": features, "targets": targets})
        
        # Test saving
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "test_model.joblib")
            result = model.save_model(model_path)
            
            assert result is True
            assert os.path.exists(model_path)
            assert os.path.exists(model_path.replace('.joblib', '_metadata.json'))
    
    def test_save_model_not_trained(self):
        """Test saving untrained model."""
        model = MockMLModel("test_model")
        
        with pytest.raises(Exception):
            model.save_model("test.joblib")
    
    def test_load_model_success(self):
        """Test successful model loading."""
        model = MockMLModel("test_model")
        
        # Train and save the model first
        model.model = Mock()
        model.model.fit = Mock()
        
        features = pd.DataFrame({"feature1": [1, 2, 3]})
        targets = pd.Series([0, 1, 0])
        
        model.train({"features": features, "targets": targets})
        
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "test_model.joblib")
            model.save_model(model_path)
            
            # Create new model and load
            new_model = MockMLModel("new_model")
            result = new_model.load_model(model_path)
            
            assert result is True
            assert new_model.is_trained is True
            assert new_model.feature_names == ["feature1"]
            assert new_model.target_name == "target"
    
    def test_load_model_file_not_found(self):
        """Test loading non-existent model."""
        model = MockMLModel("test_model")
        
        with pytest.raises(Exception):
            model.load_model("non_existent.joblib")
    
    def test_get_model_info(self):
        """Test getting model information."""
        model = MockMLModel("test_model")
        
        info = model.get_model_info()
        
        assert isinstance(info, dict)
        assert info["name"] == "test_model"
        assert info["model_type"] == "MockMLModel"
        assert info["is_trained"] is False
        assert info["feature_names"] == []
        assert info["target_name"] == ""
        assert info["training_history"] == []
        assert "created_at" in info
        assert "parameters" in info


class TestMLModelIntegration:
    """Test cases for ML model integration."""
    
    def test_model_lifecycle(self):
        """Test complete model lifecycle."""
        model = MockMLModel("test_model")
        
        # Create training data
        features = pd.DataFrame({
            "feature1": np.random.randn(100),
            "feature2": np.random.randn(100),
            "feature3": np.random.randn(100)
        })
        targets = pd.Series(np.random.randint(0, 2, 100), name="target")
        
        # Train
        assert model.train({"features": features, "targets": targets}) is True
        
        # Predict
        test_features = features.head(10)
        predictions = model.predict(test_features)
        assert len(predictions) == 10
        
        # Evaluate
        test_data = {"features": features.tail(20), "targets": targets.tail(20)}
        metrics = model.evaluate(test_data)
        assert isinstance(metrics, dict)
        
        # Save and load
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "test_model.joblib")
            assert model.save_model(model_path) is True
            
            new_model = MockMLModel("new_model")
            assert new_model.load_model(model_path) is True
            assert new_model.is_trained is True
