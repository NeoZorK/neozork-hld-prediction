# -*- coding: utf-8 -*-
"""
Tests for model training functionality.

This module provides tests for the AutoGluon trainer, predictor, and evaluator.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import os

from ..models import GluonTrainer, GluonPredictor, GluonEvaluator
from ..config import GluonConfig, ExperimentConfig


class TestModelTraining:
    """Test model training functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        np.random.seed(42)
        n_samples = 100
        
        data = pd.DataFrame({
            'feature_1': np.random.randn(n_samples),
            'feature_2': np.random.randn(n_samples),
            'feature_3': np.random.randn(n_samples),
            'target': np.random.randn(n_samples)
        })
        
        # Add datetime index
        data.index = pd.date_range('2023-01-01', periods=n_samples, freq='D')
        
        return data
    
    @pytest.fixture
    def gluon_config(self):
        """Create test configuration."""
        return GluonConfig(
            time_limit=60,  # Short time for testing
            presets=['medium_quality_faster_train']
        )
    
    @pytest.fixture
    def experiment_config(self):
        """Create test experiment configuration."""
        return ExperimentConfig(
            experiment_name="test_experiment",
            target_column="target",
            problem_type="regression",
            time_limit=60
        )
    
    def test_trainer_initialization(self, gluon_config, experiment_config):
        """Test GluonTrainer initialization."""
        trainer = GluonTrainer(gluon_config, experiment_config)
        
        assert trainer.config == gluon_config
        assert trainer.experiment_config == experiment_config
        assert trainer.predictor is None
    
    def test_model_training(self, sample_data, gluon_config, experiment_config):
        """Test model training."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            mock_predictor_instance.fit.return_value = mock_predictor_instance
            
            trainer = GluonTrainer(gluon_config, experiment_config)
            
            # Train model
            predictor = trainer.train(sample_data, 'target')
            
            # Check that fit was called
            mock_predictor_instance.fit.assert_called_once()
            assert predictor == mock_predictor_instance
    
    def test_model_training_with_validation(self, sample_data, gluon_config, experiment_config):
        """Test model training with validation data."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            mock_predictor_instance.fit.return_value = mock_predictor_instance
            
            trainer = GluonTrainer(gluon_config, experiment_config)
            
            # Split data
            train_data = sample_data.iloc[:60]
            val_data = sample_data.iloc[60:80]
            
            # Train model with validation
            predictor = trainer.train(train_data, 'target', val_data)
            
            # Check that fit was called with validation data
            mock_predictor_instance.fit.assert_called_once()
            call_args = mock_predictor_instance.fit.call_args
            assert 'val_data' in call_args[1]
    
    def test_leaderboard_retrieval(self, gluon_config, experiment_config):
        """Test leaderboard retrieval."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            mock_predictor_instance.fit.return_value = mock_predictor_instance
            mock_predictor_instance.leaderboard.return_value = pd.DataFrame({
                'model': ['model1', 'model2'],
                'score': [0.8, 0.7]
            })
            
            trainer = GluonTrainer(gluon_config, experiment_config)
            trainer.predictor = mock_predictor_instance
            
            # Get leaderboard
            leaderboard = trainer.get_leaderboard()
            
            assert isinstance(leaderboard, pd.DataFrame)
            assert 'model' in leaderboard.columns
            assert 'score' in leaderboard.columns
    
    def test_feature_importance_retrieval(self, gluon_config, experiment_config):
        """Test feature importance retrieval."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            mock_predictor_instance.fit.return_value = mock_predictor_instance
            mock_predictor_instance.feature_importance.return_value = pd.DataFrame({
                'importance': [0.5, 0.3, 0.2],
                'feature': ['feature_1', 'feature_2', 'feature_3']
            })
            
            trainer = GluonTrainer(gluon_config, experiment_config)
            trainer.predictor = mock_predictor_instance
            
            # Get feature importance
            importance = trainer.get_feature_importance()
            
            assert isinstance(importance, pd.DataFrame)
            assert 'importance' in importance.columns
    
    def test_model_info_retrieval(self, gluon_config, experiment_config):
        """Test model information retrieval."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            mock_predictor_instance.fit.return_value = mock_predictor_instance
            mock_predictor_instance.info.return_value = {'model_type': 'test'}
            
            trainer = GluonTrainer(gluon_config, experiment_config)
            trainer.predictor = mock_predictor_instance
            
            # Get model info
            info = trainer.get_model_info()
            
            assert isinstance(info, dict)
            assert 'model_type' in info
    
    def test_predictor_initialization(self):
        """Test GluonPredictor initialization."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            mock_predictor_instance = Mock()
            
            predictor = GluonPredictor(mock_predictor_instance)
            
            assert predictor.predictor == mock_predictor_instance
    
    def test_prediction(self, sample_data):
        """Test prediction functionality."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor_instance.predict.return_value = pd.Series([1, 2, 3])
            
            predictor = GluonPredictor(mock_predictor_instance)
            
            # Make predictions
            test_data = sample_data.iloc[:10]
            predictions = predictor.predict(test_data)
            
            # Check results
            assert isinstance(predictions, pd.DataFrame)
            assert 'predictions' in predictions.columns
            assert len(predictions) == len(test_data)
    
    def test_probability_prediction(self, sample_data):
        """Test probability prediction functionality."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor_instance.predict_proba.return_value = pd.DataFrame({
                'class_0': [0.3, 0.4, 0.5],
                'class_1': [0.7, 0.6, 0.5]
            })
            
            predictor = GluonPredictor(mock_predictor_instance)
            
            # Make probability predictions
            test_data = sample_data.iloc[:10]
            proba_predictions = predictor.predict_proba(test_data)
            
            # Check results
            assert isinstance(proba_predictions, pd.DataFrame)
            assert len(proba_predictions) == len(test_data)
    
    def test_prediction_with_confidence(self, sample_data):
        """Test prediction with confidence intervals."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor_instance.predict.return_value = pd.Series([1, 2, 3])
            mock_predictor_instance.predict_proba.return_value = pd.DataFrame({
                'class_0': [0.3, 0.4, 0.5],
                'class_1': [0.7, 0.6, 0.5]
            })
            
            predictor = GluonPredictor(mock_predictor_instance)
            
            # Make predictions with confidence
            test_data = sample_data.iloc[:10]
            predictions = predictor.predict_with_confidence(test_data)
            
            # Check results
            assert isinstance(predictions, pd.DataFrame)
            assert 'predictions' in predictions.columns
            assert 'confidence' in predictions.columns
            assert len(predictions) == len(test_data)
    
    def test_batch_prediction(self, sample_data):
        """Test batch prediction functionality."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor_instance.predict.return_value = pd.Series([1, 2, 3])
            
            predictor = GluonPredictor(mock_predictor_instance)
            
            # Make batch predictions
            test_data = sample_data.iloc[:50]  # Larger dataset
            predictions = predictor.batch_predict(test_data, batch_size=10)
            
            # Check results
            assert isinstance(predictions, pd.DataFrame)
            assert 'predictions' in predictions.columns
            assert len(predictions) == len(test_data)
    
    def test_evaluator_initialization(self):
        """Test GluonEvaluator initialization."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            mock_predictor_instance = Mock()
            
            evaluator = GluonEvaluator(mock_predictor_instance)
            
            assert evaluator.predictor == mock_predictor_instance
    
    def test_model_evaluation(self, sample_data):
        """Test model evaluation."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor_instance.predict.return_value = pd.Series([1, 2, 3])
            mock_predictor_instance.evaluate.return_value = {'rmse': 0.5}
            mock_predictor_instance.feature_importance.return_value = pd.DataFrame({
                'importance': [0.5, 0.3, 0.2]
            })
            mock_predictor_instance.leaderboard.return_value = pd.DataFrame({
                'model': ['model1', 'model2'],
                'score': [0.8, 0.7]
            })
            
            evaluator = GluonEvaluator(mock_predictor_instance)
            
            # Evaluate model
            test_data = sample_data.iloc[:20]
            results = evaluator.evaluate(test_data, 'target')
            
            # Check results
            assert 'predictions' in results
            assert 'metrics' in results
            assert 'performance' in results
            assert 'feature_importance' in results
            assert 'model_leaderboard' in results
    
    def test_cross_validation(self, sample_data):
        """Test cross-validation."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor_instance.evaluate_cv.return_value = {'cv_score': 0.8}
            
            evaluator = GluonEvaluator(mock_predictor_instance)
            
            # Perform cross-validation
            cv_results = evaluator.cross_validate(sample_data, 'target', cv_folds=3)
            
            # Check results
            assert isinstance(cv_results, dict)
            assert 'cv_score' in cv_results
    
    def test_model_comparison(self, sample_data):
        """Test model comparison."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor_instance.predict.return_value = pd.Series([1, 2, 3])
            mock_predictor_instance.leaderboard.return_value = pd.DataFrame({
                'model': ['model1', 'model2'],
                'score': [0.8, 0.7]
            })
            
            evaluator = GluonEvaluator(mock_predictor_instance)
            
            # Compare models
            test_data = sample_data.iloc[:20]
            comparison_results = evaluator.compare_models(test_data, 'target')
            
            # Check results
            assert 'model_predictions' in comparison_results
            assert 'model_metrics' in comparison_results
            assert 'leaderboard' in comparison_results
    
    def test_metrics_calculation(self, sample_data):
        """Test metrics calculation."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor_instance.problem_type = 'regression'
            
            evaluator = GluonEvaluator(mock_predictor_instance)
            
            # Test regression metrics
            y_true = pd.Series([1, 2, 3, 4, 5])
            y_pred = pd.Series([1.1, 2.1, 2.9, 4.1, 4.9])
            
            metrics = evaluator._calculate_metrics(y_true, y_pred)
            
            assert 'mse' in metrics
            assert 'rmse' in metrics
            assert 'mae' in metrics
            assert 'r2' in metrics
    
    def test_classification_metrics(self, sample_data):
        """Test classification metrics calculation."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor_instance.problem_type = 'binary'
            
            evaluator = GluonEvaluator(mock_predictor_instance)
            
            # Test classification metrics
            y_true = pd.Series([0, 1, 0, 1, 0])
            y_pred = pd.Series([0, 1, 0, 1, 1])
            
            metrics = evaluator._calculate_metrics(y_true, y_pred)
            
            assert 'accuracy' in metrics
            assert 'classification_report' in metrics
    
    def test_error_handling(self):
        """Test error handling in model training."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor to raise an error
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            mock_predictor_instance.fit.side_effect = Exception("Training failed")
            
            trainer = GluonTrainer(GluonConfig(), ExperimentConfig())
            
            # Should handle training errors gracefully
            with pytest.raises(Exception):
                trainer.train(pd.DataFrame(), 'target')
    
    def test_empty_data_handling(self):
        """Test handling of empty data."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            
            trainer = GluonTrainer(GluonConfig(), ExperimentConfig())
            
            # Test with empty data
            empty_data = pd.DataFrame()
            
            with pytest.raises(Exception):
                trainer.train(empty_data, 'target')
