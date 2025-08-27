# -*- coding: utf-8 -*-
"""
Tests for feature engineering manager module.

This module tests the FeatureEngineeringManager class from src/interactive/feature_engineering_manager.py.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os

# Import the module to test
from src.interactive.feature_engineering_manager import FeatureEngineeringManager


class TestFeatureEngineeringManager:
    """Test FeatureEngineeringManager class."""
    
    @pytest.fixture
    def feature_engineering_manager(self):
        """Create FeatureEngineeringManager instance for testing."""
        return FeatureEngineeringManager()
    
    @pytest.fixture
    def mock_system(self):
        """Create mock system for testing."""
        system = Mock()
        system.current_data = None
        system.current_results = {}
        system.menu_manager = Mock()
        system.safe_input = Mock(return_value=None)
        return system
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = {
            'Open': np.random.uniform(100, 200, 100),
            'High': np.random.uniform(150, 250, 100),
            'Low': np.random.uniform(50, 150, 100),
            'Close': np.random.uniform(100, 200, 100),
            'Volume': np.random.uniform(1000, 10000, 100)
        }
        return pd.DataFrame(data, index=dates)
    
    def test_init(self, feature_engineering_manager):
        """Test FeatureEngineeringManager initialization."""
        assert feature_engineering_manager is not None
    
    @patch('builtins.input', side_effect=['0'])
    def test_run_feature_engineering_analysis_exit(self, mock_input, feature_engineering_manager, mock_system, capsys):
        """Test run_feature_engineering_analysis with exit option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        captured = capsys.readouterr()
        # Should not print any error messages
        assert "Invalid choice" not in captured.out
    
    @patch('builtins.input', side_effect=['1', '0'])
    @patch('src.interactive.feature_engineering_manager.FeatureEngineeringManager.generate_all_features')
    def test_run_feature_engineering_analysis_generate_features(self, mock_generate, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with generate all features option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        mock_generate.assert_called_once_with(mock_system)
    
    @patch('builtins.input', side_effect=['2', '0'])
    def test_run_feature_engineering_analysis_proprietary_features(self, mock_input, feature_engineering_manager, mock_system, capsys):
        """Test run_feature_engineering_analysis with proprietary features option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        captured = capsys.readouterr()
        assert "Coming soon!" in captured.out
    
    @patch('builtins.input', side_effect=['3', '0'])
    def test_run_feature_engineering_analysis_technical_indicators(self, mock_input, feature_engineering_manager, mock_system, capsys):
        """Test run_feature_engineering_analysis with technical indicators option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        captured = capsys.readouterr()
        assert "Coming soon!" in captured.out
    
    @patch('builtins.input', side_effect=['4', '0'])
    def test_run_feature_engineering_analysis_statistical_features(self, mock_input, feature_engineering_manager, mock_system, capsys):
        """Test run_feature_engineering_analysis with statistical features option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        captured = capsys.readouterr()
        assert "Coming soon!" in captured.out
    
    @patch('builtins.input', side_effect=['5', '0'])
    def test_run_feature_engineering_analysis_temporal_features(self, mock_input, feature_engineering_manager, mock_system, capsys):
        """Test run_feature_engineering_analysis with temporal features option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        captured = capsys.readouterr()
        assert "Coming soon!" in captured.out
    
    @patch('builtins.input', side_effect=['6', '0'])
    def test_run_feature_engineering_analysis_cross_timeframe_features(self, mock_input, feature_engineering_manager, mock_system, capsys):
        """Test run_feature_engineering_analysis with cross-timeframe features option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        captured = capsys.readouterr()
        assert "Coming soon!" in captured.out
    
    @patch('builtins.input', side_effect=['7', '0'])
    def test_run_feature_engineering_analysis_feature_selection(self, mock_input, feature_engineering_manager, mock_system, capsys):
        """Test run_feature_engineering_analysis with feature selection option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        captured = capsys.readouterr()
        assert "Coming soon!" in captured.out
    
    @patch('builtins.input', side_effect=['8', '0'])
    @patch('src.interactive.feature_engineering_manager.FeatureEngineeringManager.show_feature_summary')
    def test_run_feature_engineering_analysis_feature_summary(self, mock_summary, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with feature summary option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        mock_summary.assert_called_once_with(mock_system)
    
    @patch('builtins.input', side_effect=['9', '0'])
    def test_run_feature_engineering_analysis_invalid_choice(self, mock_input, feature_engineering_manager, mock_system, capsys):
        """Test run_feature_engineering_analysis with invalid choice."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out
    
    @patch('builtins.input', side_effect=EOFError)
    def test_run_feature_engineering_analysis_eof_error(self, mock_input, feature_engineering_manager, mock_system, capsys):
        """Test run_feature_engineering_analysis with EOFError."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out
    
    def test_generate_all_features_no_data(self, feature_engineering_manager, mock_system, capsys):
        """Test generate_all_features with no data."""
        feature_engineering_manager.generate_all_features(mock_system)
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    @patch('src.ml.feature_engineering.feature_generator.FeatureGenerator')
    @patch('src.ml.feature_engineering.feature_generator.MasterFeatureConfig')
    @patch('src.ml.feature_engineering.feature_selector.FeatureSelectionConfig')
    def test_generate_all_features_with_advanced_generator(self, mock_selection_config, mock_feature_config, mock_feature_generator, feature_engineering_manager, mock_system, sample_data, capsys):
        """Test generate_all_features with advanced feature generator."""
        mock_system.current_data = sample_data
        
        # Mock feature generator
        mock_generator_instance = Mock()
        mock_generator_instance.generate_features.return_value = sample_data
        mock_generator_instance.get_feature_summary.return_value = {'feature1': 0.8, 'feature2': 0.6}
        mock_generator_instance.get_memory_usage.return_value = {'rss': 100.5}
        mock_feature_generator.return_value = mock_generator_instance
        
        feature_engineering_manager.generate_all_features(mock_system)
        
        captured = capsys.readouterr()
        assert "GENERATING ALL FEATURES" in captured.out
        assert "Feature generation completed!" in captured.out
        
        # Check that results were saved
        assert 'feature_engineering' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('feature_engineering', 'generate_all_features')
    
    @patch('src.ml.feature_engineering.feature_generator.FeatureGenerator', side_effect=ImportError)
    def test_generate_all_features_fallback_to_basic(self, mock_feature_generator, feature_engineering_manager, mock_system, sample_data, capsys):
        """Test generate_all_features with fallback to basic features."""
        mock_system.current_data = sample_data
        
        feature_engineering_manager.generate_all_features(mock_system)
        
        captured = capsys.readouterr()
        assert "GENERATING ALL FEATURES" in captured.out
        assert "Feature engineering module not available" in captured.out
        assert "Using basic feature generation" in captured.out
        assert "Basic feature generation completed!" in captured.out
        
        # Check that results were saved
        assert 'feature_engineering' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('feature_engineering', 'generate_all_features')
    
    def test_generate_all_features_small_data_padding(self, feature_engineering_manager, mock_system, capsys):
        """Test generate_all_features with small data that needs padding."""
        # Create small dataset
        small_data = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [105, 106, 107],
            'Low': [95, 96, 97],
            'Close': [103, 104, 105],
            'Volume': [1000, 1100, 1200]
        })
        mock_system.current_data = small_data
        
        with patch('src.ml.feature_engineering.feature_generator.FeatureGenerator', side_effect=ImportError):
            feature_engineering_manager.generate_all_features(mock_system)
        
        captured = capsys.readouterr()
        assert "Warning: Data has only 3 rows" in captured.out
        assert "Padding data to 500 rows" in captured.out
        assert "Data padded to 6 rows" in captured.out  # Actual padding result
    
    def test_generate_basic_features(self, feature_engineering_manager, mock_system, sample_data, capsys):
        """Test _generate_basic_features method."""
        mock_system.current_data = sample_data
        
        feature_engineering_manager._generate_basic_features(mock_system)
        
        captured = capsys.readouterr()
        assert "Generating basic features" in captured.out
        assert "Basic feature generation completed!" in captured.out
        
        # Check that results were saved
        assert 'feature_engineering' in mock_system.current_results
        result = mock_system.current_results['feature_engineering']
        assert 'original_shape' in result
        assert 'final_shape' in result
        assert 'features_generated' in result
        assert 'generation_time' in result
        
        # Check that data was updated
        assert mock_system.current_data is not None
        assert mock_system.current_data.shape[1] > sample_data.shape[1]  # Should have more columns
    
    def test_show_feature_summary_no_results(self, feature_engineering_manager, mock_system, capsys):
        """Test show_feature_summary with no feature engineering results."""
        feature_engineering_manager.show_feature_summary(mock_system)
        captured = capsys.readouterr()
        assert "No feature engineering results available" in captured.out
    
    def test_show_feature_summary_with_dict_summary(self, feature_engineering_manager, mock_system, capsys):
        """Test show_feature_summary with dictionary feature summary."""
        mock_system.current_results = {
            'feature_engineering': {
                'feature_summary': {
                    'feature1': 0.8,
                    'feature2': 0.6,
                    'feature3': 0.4,
                    'feature4': 0.2
                }
            }
        }
        
        feature_engineering_manager.show_feature_summary(mock_system)
        
        captured = capsys.readouterr()
        assert "FEATURE SUMMARY REPORT" in captured.out
        assert "Total features: 4" in captured.out
        assert "Top 20 features by importance" in captured.out
        assert "Feature Categories" in captured.out
        
        mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('feature_engineering', 'feature_summary')
    
    def test_show_feature_summary_with_string_summary(self, feature_engineering_manager, mock_system, capsys):
        """Test show_feature_summary with string feature summary."""
        mock_system.current_results = {
            'feature_engineering': {
                'feature_summary': "Generated 10 basic features"
            }
        }
        
        feature_engineering_manager.show_feature_summary(mock_system)
        
        captured = capsys.readouterr()
        assert "FEATURE SUMMARY REPORT" in captured.out
        assert "Feature Summary: Generated 10 basic features" in captured.out
        
        mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('feature_engineering', 'feature_summary')
    
    def test_show_feature_summary_with_error(self, feature_engineering_manager, mock_system, capsys):
        """Test show_feature_summary with error handling."""
        # Create a mock that will raise an exception when accessed
        mock_feature_engineering = Mock()
        mock_feature_engineering.__getitem__ = Mock(side_effect=Exception("Test error"))
        
        mock_system.current_results = {
            'feature_engineering': mock_feature_engineering
        }
        
        feature_engineering_manager.show_feature_summary(mock_system)
        
        captured = capsys.readouterr()
        assert "Error showing feature summary" in captured.out
