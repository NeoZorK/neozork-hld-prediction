# -*- coding: utf-8 -*-
"""
Integration tests for AutoGluon wrapper.

This module provides comprehensive integration tests for the AutoGluon wrapper.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os
from unittest.mock import Mock, patch

# Import the main wrapper
from ..gluon import GluonAutoML
from ..config import GluonConfig, ExperimentConfig


class TestGluonIntegration:
    """Test AutoGluon integration."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        np.random.seed(42)
        n_samples = 1000
        
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
    
    @pytest.fixture
    def temp_data_dir(self, sample_data):
        """Create temporary data directory with sample files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create parquet file
            parquet_path = Path(temp_dir) / "test_data.parquet"
            sample_data.to_parquet(parquet_path)
            
            # Create CSV file
            csv_path = Path(temp_dir) / "test_data.csv"
            sample_data.to_csv(csv_path)
            
            yield temp_dir
    
    @pytest.mark.skip(reason="AutoGluon not available")
    def test_gluon_initialization(self, gluon_config, experiment_config):
        """Test GluonAutoML initialization."""
        with patch('autogluon.tabular.TabularPredictor'):
            gluon = GluonAutoML(experiment_config=experiment_config.to_dict())
            
            assert gluon.config is not None
            assert gluon.experiment_config is not None
            assert gluon.data_loader is not None
            assert gluon.preprocessor is not None
    
    def test_data_loading(self, temp_data_dir, sample_data):
        """Test data loading functionality."""
        with patch('autogluon.tabular.TabularPredictor'):
            gluon = GluonAutoML()
            gluon.experiment_config.data_path = temp_data_dir
            
            # Test loading specific file
            loaded_data = gluon.load_data(f"{temp_data_dir}/test_data.parquet")
            
            assert not loaded_data.empty
            assert len(loaded_data) == len(sample_data)
            assert list(loaded_data.columns) == list(sample_data.columns)
    
    def test_data_discovery(self, temp_data_dir):
        """Test data file discovery."""
        with patch('autogluon.tabular.TabularPredictor'):
            gluon = GluonAutoML()
            gluon.experiment_config.data_path = temp_data_dir
            
            # Test file discovery
            files = gluon.data_loader.discover_data_files()
            
            assert len(files) >= 2  # At least parquet and CSV
            assert any('test_data.parquet' in str(f) for f in files)
            assert any('test_data.csv' in str(f) for f in files)
    
    def test_time_series_split(self, sample_data):
        """Test time series splitting."""
        with patch('autogluon.tabular.TabularPredictor'):
            gluon = GluonAutoML()
            
            train, val, test = gluon.create_time_series_split(sample_data)
            
            # Check split ratios
            total_len = len(sample_data)
            assert len(train) == int(total_len * 0.6)
            assert len(val) == int(total_len * 0.2)
            assert len(test) == int(total_len * 0.2)
            
            # Check chronological order
            assert train.index.max() <= val.index.min()
            assert val.index.max() <= test.index.min()
    
    def test_data_summary(self, sample_data):
        """Test data summary generation."""
        with patch('autogluon.tabular.TabularPredictor'):
            gluon = GluonAutoML()
            
            summary = gluon.get_data_summary(sample_data)
            
            assert 'shape' in summary
            assert 'columns' in summary
            assert 'dtypes' in summary
            assert 'missing_values' in summary
            assert 'quality_issues' in summary
            assert 'is_ready_for_gluon' in summary
    
    @pytest.mark.skip(reason="AutoGluon not available")
    def test_model_training(self, sample_data):
        """Test model training."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            mock_predictor_instance.fit.return_value = mock_predictor_instance
            mock_predictor_instance.predict.return_value = pd.Series([1, 2, 3])
            mock_predictor_instance.evaluate.return_value = {'rmse': 0.5}
            
            gluon = GluonAutoML()
            
            # Split data
            train, val, test = gluon.create_time_series_split(sample_data)
            
            # Train model
            gluon.train_models(train, 'target', val)
            
            # Check that fit was called
            mock_predictor_instance.fit.assert_called_once()
    
    @pytest.mark.skip(reason="AutoGluon not available")
    def test_model_evaluation(self, sample_data):
        """Test model evaluation."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            mock_predictor_instance.fit.return_value = mock_predictor_instance
            mock_predictor_instance.predict.return_value = pd.Series([1, 2, 3])
            mock_predictor_instance.evaluate.return_value = {'rmse': 0.5}
            mock_predictor_instance.feature_importance.return_value = pd.DataFrame({
                'importance': [0.5, 0.3, 0.2]
            })
            mock_predictor_instance.leaderboard.return_value = pd.DataFrame({
                'model': ['model1', 'model2'],
                'score': [0.8, 0.7]
            })
            
            gluon = GluonAutoML()
            
            # Split data
            train, val, test = gluon.create_time_series_split(sample_data)
            
            # Train model
            gluon.train_models(train, 'target', val)
            
            # Evaluate model
            results = gluon.evaluate_models(test, 'target')
            
            # Check results
            assert 'predictions' in results
            assert 'metrics' in results
            assert 'performance' in results
            assert 'feature_importance' in results
            assert 'value_scores' in results
    
    def test_model_export(self, sample_data):
        """Test model export."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            mock_predictor_instance.fit.return_value = mock_predictor_instance
            mock_predictor_instance.predict.return_value = pd.Series([1, 2, 3])
            
            gluon = GluonAutoML()
            
            # Split data
            train, val, test = gluon.create_time_series_split(sample_data)
            
            # Train model
            gluon.train_models(train, 'target', val)
            
            # Test export
            with tempfile.TemporaryDirectory() as temp_dir:
                export_paths = gluon.export_models(temp_dir)
                
                assert isinstance(export_paths, dict)
                assert len(export_paths) > 0
    
    def test_drift_monitoring(self, sample_data):
        """Test drift monitoring."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            mock_predictor_instance.fit.return_value = mock_predictor_instance
            mock_predictor_instance.predict.return_value = pd.Series([1, 2, 3])
            
            gluon = GluonAutoML()
            
            # Split data
            train, val, test = gluon.create_time_series_split(sample_data)
            
            # Train model
            gluon.train_models(train, 'target', val)
            
            # Test drift monitoring
            drift_results = gluon.monitor_drift(test)
            
            assert 'drift_detected' in drift_results
            assert 'feature_drift' in drift_results
            assert 'psi_scores' in drift_results
            assert 'recommendations' in drift_results
    
    def test_model_summary(self, sample_data):
        """Test model summary generation."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            # Mock the predictor
            mock_predictor_instance = Mock()
            mock_predictor.return_value = mock_predictor_instance
            mock_predictor_instance.fit.return_value = mock_predictor_instance
            mock_predictor_instance.predict.return_value = pd.Series([1, 2, 3])
            mock_predictor_instance.info.return_value = {'model_type': 'test'}
            mock_predictor_instance.feature_importance.return_value = pd.DataFrame({
                'importance': [0.5, 0.3, 0.2]
            })
            mock_predictor_instance.leaderboard.return_value = pd.DataFrame({
                'model': ['model1', 'model2'],
                'score': [0.8, 0.7]
            })
            
            gluon = GluonAutoML()
            
            # Split data
            train, val, test = gluon.create_time_series_split(sample_data)
            
            # Train model
            gluon.train_models(train, 'target', val)
            
            # Test model summary
            summary = gluon.get_model_summary()
            
            assert 'model_info' in summary
            assert 'feature_importance' in summary
            assert 'leaderboard' in summary
            assert 'config' in summary
            assert 'experiment_config' in summary
    
    def test_error_handling(self):
        """Test error handling."""
        # Test with invalid data path
        with patch('autogluon.tabular.TabularPredictor'):
            gluon = GluonAutoML()
            gluon.experiment_config.data_path = "/nonexistent/path"
            
            # Should handle gracefully
            data = gluon.load_data()
            assert data.empty
    
    def test_configuration_loading(self):
        """Test configuration loading."""
        with patch('autogluon.tabular.TabularPredictor'):
            # Test default configuration
            gluon = GluonAutoML()
            assert gluon.config is not None
            
            # Test custom configuration
            custom_config = {
                'experiment_name': 'custom_test',
                'target_column': 'custom_target',
                'time_limit': 120
            }
            
            gluon_custom = GluonAutoML(experiment_config=custom_config)
            assert gluon_custom.experiment_config.experiment_name == 'custom_test'
            assert gluon_custom.experiment_config.target_column == 'custom_target'
            assert gluon_custom.experiment_config.time_limit == 120
