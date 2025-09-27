# -*- coding: utf-8 -*-
"""
Tests for deployment functionality.

This module provides tests for model export, retraining, and drift monitoring.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import json
from unittest.mock import Mock, patch
import os

from ..deployment import GluonExporter, AutoRetrainer, DriftMonitor
from ..config import GluonConfig, ExperimentConfig


class TestDeployment:
    """Test deployment functionality."""
    
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
    def mock_predictor(self):
        """Create mock predictor for testing."""
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor:
            mock_predictor_instance = Mock()
            mock_predictor_instance.problem_type = 'regression'
            mock_predictor_instance.eval_metric = 'rmse'
            mock_predictor_instance.path = 'test_path'
            mock_predictor_instance.feature_importance.return_value = pd.DataFrame({
                'importance': [0.5, 0.3, 0.2]
            })
            mock_predictor_instance.leaderboard.return_value = pd.DataFrame({
                'model': ['model1', 'model2'],
                'score': [0.8, 0.7]
            })
            yield mock_predictor_instance
    
    def test_exporter_initialization(self):
        """Test GluonExporter initialization."""
        exporter = GluonExporter()
        assert exporter is not None
    
    def test_model_export_pickle(self, mock_predictor):
        """Test model export in pickle format."""
        exporter = GluonExporter()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            export_paths = exporter.export(mock_predictor, temp_dir, ['pickle'])
            
            assert 'pickle' in export_paths
            assert Path(export_paths['pickle']).exists()
    
    def test_model_export_json(self, mock_predictor):
        """Test model export in JSON format."""
        exporter = GluonExporter()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            export_paths = exporter.export(mock_predictor, temp_dir, ['json'])
            
            assert 'json' in export_paths
            assert Path(export_paths['json']).exists()
            
            # Check JSON content
            with open(export_paths['json'], 'r') as f:
                json_data = json.load(f)
            
            assert 'model_type' in json_data
            assert 'problem_type' in json_data
            assert 'feature_importance' in json_data
    
    def test_walk_forward_export(self, mock_predictor):
        """Test export for walk forward analysis."""
        exporter = GluonExporter()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            export_paths = exporter.export_for_walk_forward(mock_predictor, temp_dir)
            
            assert 'pickle' in export_paths
            assert 'json' in export_paths
            assert 'config' in export_paths
            
            # Check config file
            with open(export_paths['config'], 'r') as f:
                config_data = json.load(f)
            
            assert 'model_type' in config_data
            assert 'compatible_with' in config_data
            assert 'walk_forward' in config_data['compatible_with']
    
    def test_monte_carlo_export(self, mock_predictor):
        """Test export for Monte Carlo analysis."""
        exporter = GluonExporter()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            export_paths = exporter.export_for_monte_carlo(mock_predictor, temp_dir)
            
            assert 'pickle' in export_paths
            assert 'json' in export_paths
            assert 'config' in export_paths
            
            # Check config file
            with open(export_paths['config'], 'r') as f:
                config_data = json.load(f)
            
            assert 'model_type' in config_data
            assert 'compatible_with' in config_data
            assert 'monte_carlo' in config_data['compatible_with']
            assert config_data['supports_probability'] is True
    
    def test_deployment_package_creation(self, mock_predictor):
        """Test complete deployment package creation."""
        exporter = GluonExporter()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            export_paths = exporter.create_deployment_package(mock_predictor, temp_dir)
            
            assert 'pickle' in export_paths
            assert 'json' in export_paths
            assert 'config' in export_paths
            assert 'requirements' in export_paths
            assert 'readme' in export_paths
            
            # Check requirements file
            with open(export_paths['requirements'], 'r') as f:
                requirements = f.read()
            
            assert 'autogluon.tabular' in requirements
            assert 'pandas' in requirements
            assert 'numpy' in requirements
    
    def test_retrainer_initialization(self):
        """Test AutoRetrainer initialization."""
        retrainer = AutoRetrainer()
        
        assert retrainer.retrain_threshold == 0.1
        assert retrainer.min_samples == 100
        assert retrainer.max_retrain_frequency == 7
        assert retrainer.last_retrain is None
    
    def test_retrain_decision_logic(self):
        """Test retrain decision logic."""
        retrainer = AutoRetrainer()
        
        # Test with good performance (no degradation)
        should_retrain = retrainer.should_retrain(0.8, 0.8, 150)
        # With good performance and no degradation, should not retrain
        assert not should_retrain
        
        # Test with performance degradation
        should_retrain = retrainer.should_retrain(0.6, 0.8, 150)
        assert should_retrain
        
        # Test with insufficient data
        should_retrain = retrainer.should_retrain(0.6, 0.8, 50)
        assert not should_retrain
    
    def test_model_retraining(self, sample_data, mock_predictor):
        """Test model retraining."""
        retrainer = AutoRetrainer()
        config = GluonConfig()
        
        with patch('autogluon.tabular.TabularPredictor') as mock_predictor_class:
            # Mock new predictor
            new_predictor = Mock()
            mock_predictor_class.return_value = new_predictor
            new_predictor.fit.return_value = new_predictor
            
            # Retrain model
            retrained_predictor = retrainer.retrain(
                mock_predictor, sample_data, 'target', config
            )
            
            # Check that new predictor was created and trained
            mock_predictor_class.assert_called_once()
            new_predictor.fit.assert_called_once()
            assert retrained_predictor == new_predictor
    
    def test_incremental_retraining(self, sample_data, mock_predictor):
        """Test incremental retraining."""
        retrainer = AutoRetrainer()
        
        # Mock incremental retraining
        mock_predictor.fit.return_value = mock_predictor
        
        # Perform incremental retraining
        updated_predictor = retrainer.incremental_retrain(
            mock_predictor, sample_data, 'target'
        )
        
        # Check that fit was called
        mock_predictor.fit.assert_called_once()
        assert updated_predictor == mock_predictor
    
    def test_retrain_scheduling(self, mock_predictor):
        """Test retrain scheduling."""
        retrainer = AutoRetrainer()
        
        # Test daily schedule
        schedule_config = retrainer.schedule_retrain(mock_predictor, "daily")
        
        assert schedule_config['schedule'] == 'daily'
        assert schedule_config['enabled'] is True
        assert 'next_retrain' in schedule_config
    
    def test_retrain_status(self):
        """Test retrain status retrieval."""
        retrainer = AutoRetrainer()
        
        status = retrainer.get_retrain_status()
        
        assert 'last_retrain' in status
        assert 'retrain_threshold' in status
        assert 'min_samples' in status
        assert 'max_retrain_frequency' in status
        assert 'ready_for_retrain' in status
    
    def test_drift_monitor_initialization(self):
        """Test DriftMonitor initialization."""
        monitor = DriftMonitor()
        
        assert monitor.drift_threshold == 0.1
        assert monitor.psi_threshold == 0.2
        assert monitor.performance_threshold == 0.05
        assert monitor.baseline_data is None
        assert monitor.baseline_performance is None
    
    def test_baseline_setting(self, sample_data):
        """Test baseline data setting."""
        monitor = DriftMonitor()
        
        monitor.set_baseline(sample_data, 0.8)
        
        assert monitor.baseline_data is not None
        assert monitor.baseline_performance == 0.8
        assert len(monitor.baseline_data) == len(sample_data)
    
    def test_drift_detection(self, sample_data, mock_predictor):
        """Test drift detection."""
        monitor = DriftMonitor()
        
        # Set baseline
        monitor.set_baseline(sample_data, 0.8)
        
        # Test with similar data (no drift)
        similar_data = sample_data.copy()
        drift_results = monitor.check_drift(mock_predictor, similar_data)
        
        assert 'drift_detected' in drift_results
        assert 'feature_drift' in drift_results
        assert 'psi_scores' in drift_results
        assert 'recommendations' in drift_results
    
    def test_feature_drift_detection(self, sample_data):
        """Test feature drift detection."""
        monitor = DriftMonitor()
        
        # Set baseline
        monitor.set_baseline(sample_data)
        
        # Create data with drift
        drifted_data = sample_data.copy()
        drifted_data['feature_1'] = drifted_data['feature_1'] * 2  # Scale change
        
        drift_results = monitor.check_drift(Mock(), drifted_data)
        
        assert 'feature_drift' in drift_results
        assert 'psi_scores' in drift_results
    
    def test_psi_calculation(self, sample_data):
        """Test PSI calculation."""
        monitor = DriftMonitor()
        
        # Test with identical data (PSI should be 0)
        psi_score = monitor._calculate_psi(sample_data['feature_1'], sample_data['feature_1'])
        assert psi_score == 0.0
        
        # Test with different data
        different_data = sample_data['feature_1'] * 2
        psi_score = monitor._calculate_psi(sample_data['feature_1'], different_data)
        assert psi_score > 0.0
    
    def test_drift_summary(self, sample_data, mock_predictor):
        """Test drift summary generation."""
        monitor = DriftMonitor()
        
        # Set baseline
        monitor.set_baseline(sample_data, 0.8)
        
        # Check drift
        drift_results = monitor.check_drift(mock_predictor, sample_data)
        
        # Get summary
        summary = monitor.get_drift_summary(drift_results)
        
        assert 'drift_detected' in summary
        assert 'high_psi_features' in summary
        assert 'recommendations' in summary
        assert 'monitoring_status' in summary
    
    def test_performance_drift_detection(self, sample_data, mock_predictor):
        """Test performance drift detection."""
        monitor = DriftMonitor()
        
        # Set baseline
        monitor.set_baseline(sample_data, 0.8)
        
        # Mock performance degradation
        mock_predictor.predict.return_value = pd.Series([1, 2, 3])
        
        # Test performance drift
        performance_drift = monitor._check_performance_drift(mock_predictor, sample_data)
        
        # Should not detect drift with good performance
        assert isinstance(performance_drift, bool)
    
    def test_error_handling(self):
        """Test error handling in deployment components."""
        exporter = GluonExporter()
        
        # Test with invalid predictor
        with pytest.raises((TypeError, ValueError, AttributeError)):
            exporter.export(None, "invalid_path", ['pickle'])
        
        # Test with invalid export path
        with pytest.raises(Exception):
            exporter.export(Mock(), "/nonexistent/path", ['pickle'])
    
    def test_memory_efficiency(self, sample_data):
        """Test memory efficiency of deployment components."""
        monitor = DriftMonitor()
        
        # Test with large dataset
        large_data = pd.concat([sample_data] * 10)  # 10x larger
        
        # Should handle large datasets efficiently
        monitor.set_baseline(large_data)
        
        # Check drift detection with large data
        drift_results = monitor.check_drift(Mock(), large_data)
        
        assert 'drift_detected' in drift_results
        assert 'feature_drift' in drift_results
