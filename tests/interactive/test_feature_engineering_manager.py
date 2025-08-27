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
        system.current_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        system.current_results = {}
        system.menu_manager = Mock()
        system.safe_input = Mock(return_value=None)
        return system
    
    @pytest.fixture
    def mock_system_no_data(self):
        """Create mock system without data for testing."""
        system = Mock()
        system.current_data = None
        system.current_results = {}
        system.menu_manager = Mock()
        system.safe_input = Mock(return_value=None)
        return system
    
    def test_init(self, feature_engineering_manager):
        """Test FeatureEngineeringManager initialization."""
        assert feature_engineering_manager is not None
    
    @patch('builtins.input', side_effect=['0'])
    def test_run_feature_engineering_analysis_exit(self, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with exit option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        mock_system.menu_manager.print_feature_engineering_menu.assert_called_once()
    
    @patch('builtins.input', side_effect=['1', '0'])
    def test_run_feature_engineering_analysis_generate_all_features(self, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with generate all features option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        assert mock_system.menu_manager.print_feature_engineering_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['2', '0'])
    def test_run_feature_engineering_analysis_proprietary_features(self, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with proprietary features option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        assert mock_system.menu_manager.print_feature_engineering_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['3', '0'])
    def test_run_feature_engineering_analysis_technical_indicators(self, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with technical indicators option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        assert mock_system.menu_manager.print_feature_engineering_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['4', '0'])
    def test_run_feature_engineering_analysis_statistical_features(self, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with statistical features option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        assert mock_system.menu_manager.print_feature_engineering_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['5', '0'])
    def test_run_feature_engineering_analysis_temporal_features(self, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with temporal features option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        assert mock_system.menu_manager.print_feature_engineering_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['6', '0'])
    def test_run_feature_engineering_analysis_cross_timeframe_features(self, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with cross timeframe features option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        assert mock_system.menu_manager.print_feature_engineering_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['7', '0'])
    def test_run_feature_engineering_analysis_feature_selection(self, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with feature selection option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        assert mock_system.menu_manager.print_feature_engineering_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['8', '0'])
    def test_run_feature_engineering_analysis_feature_summary(self, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with feature summary option."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        assert mock_system.menu_manager.print_feature_engineering_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['9', '0'])
    def test_run_feature_engineering_analysis_invalid_choice(self, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with invalid choice."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        assert mock_system.menu_manager.print_feature_engineering_menu.call_count == 2
    
    @patch('builtins.input', side_effect=EOFError)
    def test_run_feature_engineering_analysis_eof(self, mock_input, feature_engineering_manager, mock_system):
        """Test run_feature_engineering_analysis with EOFError."""
        feature_engineering_manager.run_feature_engineering_analysis(mock_system)
        mock_system.menu_manager.print_feature_engineering_menu.assert_called_once()
    
    def test_generate_all_features_no_data(self, feature_engineering_manager, mock_system_no_data):
        """Test generate_all_features with no data."""
        feature_engineering_manager.generate_all_features(mock_system_no_data)
    
    @patch('src.interactive.feature_engineering_manager.FeatureGenerator')
    @patch('src.interactive.feature_engineering_manager.MasterFeatureConfig')
    @patch('src.interactive.feature_engineering_manager.FeatureSelectionConfig')
    def test_generate_all_features_with_advanced_generator(self, mock_selection_config, mock_feature_config, mock_feature_generator, feature_engineering_manager, mock_system):
        """Test generate_all_features with advanced feature generator."""
        # Mock the feature generator
        mock_generator_instance = Mock()
        mock_generator_instance.generate_features.return_value = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106],
            'Volume': [1000, 1100, 1200, 1300, 1400],
            'feature_1': [0.1, 0.2, 0.3, 0.4, 0.5],
            'feature_2': [0.6, 0.7, 0.8, 0.9, 1.0]
        })
        mock_generator_instance.get_feature_summary.return_value = {'feature_1': 0.8, 'feature_2': 0.6}
        mock_generator_instance.get_memory_usage.return_value = {'rss': 100.5}
        mock_feature_generator.return_value = mock_generator_instance
        
        feature_engineering_manager.generate_all_features(mock_system)
        
        assert 'feature_engineering' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('feature_engineering', 'generate_all_features')
    
    @patch('src.interactive.feature_engineering_manager.FeatureGenerator', side_effect=ImportError)
    def test_generate_all_features_import_error(self, mock_feature_generator, feature_engineering_manager, mock_system):
        """Test generate_all_features with import error."""
        feature_engineering_manager.generate_all_features(mock_system)
        
        assert 'feature_engineering' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('feature_engineering', 'generate_all_features')
    
    def test_generate_all_features_exception(self, feature_engineering_manager, mock_system):
        """Test generate_all_features with exception."""
        mock_system.current_data.shape = (100, 5)  # Small dataset
        feature_engineering_manager.generate_all_features(mock_system)
        
        assert 'feature_engineering' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('feature_engineering', 'generate_all_features')
    
    def test_generate_all_features_small_dataset(self, feature_engineering_manager, mock_system):
        """Test generate_all_features with small dataset that needs padding."""
        mock_system.current_data.shape = (100, 5)  # Small dataset
        feature_engineering_manager.generate_all_features(mock_system)
        
        assert 'feature_engineering' in mock_system.current_results
        assert mock_system.current_data.shape[0] >= 500  # Should be padded
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('feature_engineering', 'generate_all_features')
    
    def test_generate_basic_features(self, feature_engineering_manager, mock_system):
        """Test _generate_basic_features method."""
        original_shape = mock_system.current_data.shape
        feature_engineering_manager._generate_basic_features(mock_system)
        
        assert 'feature_engineering' in mock_system.current_results
        assert mock_system.current_data.shape[1] > original_shape[1]  # Should have more columns
        assert mock_system.current_results['feature_engineering']['features_generated'] > 0
    
    def test_generate_basic_features_with_ohlcv(self, feature_engineering_manager, mock_system):
        """Test _generate_basic_features method with OHLCV data."""
        # Ensure we have OHLCV columns
        mock_system.current_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        original_shape = mock_system.current_data.shape
        feature_engineering_manager._generate_basic_features(mock_system)
        
        assert 'feature_engineering' in mock_system.current_results
        assert mock_system.current_data.shape[1] > original_shape[1]  # Should have more columns
        assert 'price_range' in mock_system.current_data.columns
        assert 'body_size' in mock_system.current_data.columns
    
    def test_show_feature_summary_no_results(self, feature_engineering_manager, mock_system):
        """Test show_feature_summary with no feature engineering results."""
        feature_engineering_manager.show_feature_summary(mock_system)
    
    def test_show_feature_summary_with_dict_summary(self, feature_engineering_manager, mock_system):
        """Test show_feature_summary with dictionary feature summary."""
        mock_system.current_results['feature_engineering'] = {
            'feature_summary': {
                'feature_1': 0.8,
                'feature_2': 0.6,
                'feature_3': 0.4,
                'feature_4': 0.2
            }
        }
        
        feature_engineering_manager.show_feature_summary(mock_system)
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('feature_engineering', 'feature_summary')
    
    def test_show_feature_summary_with_string_summary(self, feature_engineering_manager, mock_system):
        """Test show_feature_summary with string feature summary."""
        mock_system.current_results['feature_engineering'] = {
            'feature_summary': "Generated 10 basic features"
        }
        
        feature_engineering_manager.show_feature_summary(mock_system)
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('feature_engineering', 'feature_summary')
    
    def test_show_feature_summary_exception(self, feature_engineering_manager, mock_system):
        """Test show_feature_summary with exception."""
        mock_system.current_results['feature_engineering'] = {
            'feature_summary': {'feature_1': 0.8}
        }
        mock_system.menu_manager.mark_menu_as_used.side_effect = Exception("Test error")
        
        feature_engineering_manager.show_feature_summary(mock_system)
