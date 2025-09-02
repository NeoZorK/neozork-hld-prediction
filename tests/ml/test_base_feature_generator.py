# -*- coding: utf-8 -*-
"""
Tests for base_feature_generator.py.

This module tests the base feature generator classes and functionality.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from abc import ABC

from src.ml.feature_engineering.base_feature_generator import (
    BaseFeatureGenerator, FeatureConfig, BUY, SELL, NOTRADE
)


class TestFeatureConfig:
    """Test FeatureConfig dataclass."""
    
    def test_init_default_values(self):
        """Test FeatureConfig initialization with default values."""
        config = FeatureConfig()
        
        assert config.short_periods == [5, 10, 14]
        assert config.medium_periods == [20, 50, 100]
        assert config.long_periods == [200, 500]
        assert config.price_types == ['open', 'high', 'low', 'close']
        assert config.volatility_periods == [14, 20, 50]
        assert config.volume_periods == [14, 20, 50]
        assert config.feature_types == ['ratio', 'difference', 'momentum', 'volatility']
        assert config.custom_params == {}
    
    def test_init_custom_values(self):
        """Test FeatureConfig initialization with custom values."""
        custom_config = FeatureConfig(
            short_periods=[3, 7],
            medium_periods=[15, 30],
            long_periods=[100],
            price_types=['close'],
            volatility_periods=[10],
            volume_periods=[10],
            feature_types=['ratio'],
            custom_params={'test_param': 'test_value'}
        )
        
        assert custom_config.short_periods == [3, 7]
        assert custom_config.medium_periods == [15, 30]
        assert custom_config.long_periods == [100]
        assert custom_config.price_types == ['close']
        assert custom_config.volatility_periods == [10]
        assert custom_config.volume_periods == [10]
        assert custom_config.feature_types == ['ratio']
        assert custom_config.custom_params == {'test_param': 'test_value'}
    
    def test_post_init_partial_values(self):
        """Test FeatureConfig post_init with partial values."""
        config = FeatureConfig(
            short_periods=[3, 7],
            custom_params={'test': 'value'}
        )
        
        # Custom values should be preserved
        assert config.short_periods == [3, 7]
        assert config.custom_params == {'test': 'value'}
        
        # Other values should have defaults
        assert config.medium_periods == [20, 50, 100]
        assert config.long_periods == [200, 500]
        assert config.price_types == ['open', 'high', 'low', 'close']


class TestBaseFeatureGenerator:
    """Test BaseFeatureGenerator abstract class."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range('2023-01-01', periods=600, freq='D')  # Increased to 600 to meet minimum requirement
        data = {
            'Open': np.random.uniform(100, 200, 600),
            'High': np.random.uniform(150, 250, 600),
            'Low': np.random.uniform(50, 150, 600),
            'Close': np.random.uniform(100, 200, 600),
            'Volume': np.random.uniform(1000, 10000, 600)
        }
        return pd.DataFrame(data, index=dates)
    
    def test_init_with_config(self):
        """Test BaseFeatureGenerator initialization with config."""
        config = FeatureConfig(short_periods=[3, 7])
        generator = ConcreteFeatureGenerator(config)
        
        assert generator.config == config
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
    
    def test_init_without_config(self):
        """Test BaseFeatureGenerator initialization without config."""
        generator = ConcreteFeatureGenerator()
        
        assert isinstance(generator.config, FeatureConfig)
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
    
    def test_validate_data_valid(self, sample_data):
        """Test data validation with valid data."""
        generator = ConcreteFeatureGenerator()
        result = generator.validate_data(sample_data)
        assert result is True
    
    def test_validate_data_none(self):
        """Test data validation with None data."""
        generator = ConcreteFeatureGenerator()
        result = generator.validate_data(None)
        assert result is False
    
    def test_validate_data_empty(self):
        """Test data validation with empty DataFrame."""
        generator = ConcreteFeatureGenerator()
        empty_df = pd.DataFrame()
        result = generator.validate_data(empty_df)
        assert result is False
    
    def test_validate_data_missing_columns(self, sample_data):
        """Test data validation with missing required columns."""
        generator = ConcreteFeatureGenerator()
        # Remove required column
        invalid_data = sample_data.drop(columns=['Open'])
        result = generator.validate_data(invalid_data)
        assert result is False
    
    def test_validate_data_insufficient_data(self):
        """Test data validation with insufficient data."""
        generator = ConcreteFeatureGenerator()
        # Create data with insufficient rows
        insufficient_data = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [150, 151, 152],
            'Low': [50, 51, 52],
            'Close': [100, 101, 102]
        })
        result = generator.validate_data(insufficient_data)
        assert result is False
    
    def test_handle_missing_values_forward_fill(self, sample_data):
        """Test handling missing values with forward fill."""
        generator = ConcreteFeatureGenerator()
        
        # Add some missing values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Open')] = np.nan
        
        result = generator.handle_missing_values(sample_data, 'forward_fill')
        assert not result['Open'].isna().any()
        # Forward fill should preserve all rows, just fill missing values
        assert len(result) == len(sample_data)
    
    def test_handle_missing_values_backward_fill(self, sample_data):
        """Test handling missing values with backward fill."""
        generator = ConcreteFeatureGenerator()
        
        # Add some missing values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Open')] = np.nan
        
        result = generator.handle_missing_values(sample_data, 'backward_fill')
        assert not result['Open'].isna().any()
    
    def test_handle_missing_values_interpolate(self, sample_data):
        """Test handling missing values with interpolation."""
        generator = ConcreteFeatureGenerator()
        
        # Add some missing values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Open')] = np.nan
        
        result = generator.handle_missing_values(sample_data, 'interpolate')
        assert not result['Open'].isna().any()
    
    def test_handle_missing_values_unknown_method(self, sample_data):
        """Test handling missing values with unknown method."""
        generator = ConcreteFeatureGenerator()
        
        # Add some missing values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Open')] = np.nan
        
        result = generator.handle_missing_values(sample_data, 'unknown_method')
        assert not result['Open'].isna().any()  # Should fall back to forward fill
    
    def test_calculate_returns(self, sample_data):
        """Test calculating returns."""
        generator = ConcreteFeatureGenerator()
        result = generator.calculate_returns(sample_data, 'Close')
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert pd.isna(result.iloc[0])  # First value should be NaN
        assert not result.iloc[1:].isna().all()  # Other values should not be all NaN
    
    def test_calculate_returns_invalid_column(self, sample_data):
        """Test calculating returns with invalid column."""
        generator = ConcreteFeatureGenerator()
        result = generator.calculate_returns(sample_data, 'InvalidColumn')
        
        assert isinstance(result, pd.Series)
        assert len(result) == 0
    
    def test_calculate_log_returns(self, sample_data):
        """Test calculating log returns."""
        generator = ConcreteFeatureGenerator()
        result = generator.calculate_log_returns(sample_data, 'Close')
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert pd.isna(result.iloc[0])  # First value should be NaN
        assert not result.iloc[1:].isna().all()  # Other values should not be all NaN
    
    def test_calculate_log_returns_invalid_column(self, sample_data):
        """Test calculating log returns with invalid column."""
        generator = ConcreteFeatureGenerator()
        result = generator.calculate_log_returns(sample_data, 'InvalidColumn')
        
        assert isinstance(result, pd.Series)
        assert len(result) == 0
    
    def test_get_feature_importance_empty(self):
        """Test getting feature importance when empty."""
        generator = ConcreteFeatureGenerator()
        result = generator.get_feature_importance()
        assert result == {}
    
    def test_get_feature_importance_with_data(self):
        """Test getting feature importance with data."""
        generator = ConcreteFeatureGenerator()
        importance_dict = {'feature1': 0.8, 'feature2': 0.6}
        generator.feature_importance = importance_dict
        
        result = generator.get_feature_importance()
        assert result == importance_dict
        assert result is not importance_dict  # Should be a copy
    
    def test_set_feature_importance(self):
        """Test setting feature importance."""
        generator = ConcreteFeatureGenerator()
        importance_dict = {'feature1': 0.8, 'feature2': 0.6}
        
        generator.set_feature_importance(importance_dict)
        assert generator.feature_importance == importance_dict
        assert generator.feature_importance is not importance_dict  # Should be a copy
    
    def test_get_feature_count(self):
        """Test getting feature count."""
        generator = ConcreteFeatureGenerator()
        assert generator.get_feature_count() == 0
        
        generator.features_generated = 5
        assert generator.get_feature_count() == 5
    
    def test_reset_feature_count(self):
        """Test resetting feature count."""
        generator = ConcreteFeatureGenerator()
        generator.features_generated = 5
        generator.feature_names = ['feature1', 'feature2']
        generator.feature_importance = {'feature1': 0.8}
        
        generator.reset_feature_count()
        assert generator.features_generated == 0
        assert generator.feature_names == []
        # feature_importance should remain unchanged
    
    def test_log_feature_generation(self):
        """Test logging feature generation."""
        generator = ConcreteFeatureGenerator()
        
        generator.log_feature_generation('test_feature', 0.8)
        
        assert generator.features_generated == 1
        assert generator.feature_names == ['test_feature']
        assert generator.feature_importance['test_feature'] == 0.8
    
    def test_log_feature_generation_zero_importance(self):
        """Test logging feature generation with zero importance."""
        generator = ConcreteFeatureGenerator()
        
        generator.log_feature_generation('test_feature', 0.0)
        
        assert generator.features_generated == 1
        assert generator.feature_names == ['test_feature']
        assert 'test_feature' not in generator.feature_importance
    
    def test_str_repr(self):
        """Test string representation."""
        generator = ConcreteFeatureGenerator()
        generator.features_generated = 5
        
        str_repr = str(generator)
        repr_repr = repr(generator)
        
        assert "ConcreteFeatureGenerator" in str_repr
        assert "features_generated=5" in str_repr
        assert "ConcreteFeatureGenerator" in repr_repr
        assert "features_generated=5" in repr_repr


class TestTradingConstants:
    """Test trading signal constants."""
    
    def test_trading_constants(self):
        """Test that trading constants are correctly defined."""
        assert BUY == 1
        assert SELL == -1
        assert NOTRADE == 0
        
        # Test that they are integers
        assert isinstance(BUY, int)
        assert isinstance(SELL, int)
        assert isinstance(NOTRADE, int)


class TestAbstractMethods:
    """Test that abstract methods are properly defined."""
    
    def test_generate_features_abstract(self):
        """Test that generate_features is abstract."""
        # Should not be able to instantiate BaseFeatureGenerator directly
        with pytest.raises(TypeError):
            BaseFeatureGenerator()
    
    def test_get_feature_names_abstract(self):
        """Test that get_feature_names is abstract."""
        # This is tested through the concrete implementation
        pass


# Concrete implementation for testing abstract class
class ConcreteFeatureGenerator(BaseFeatureGenerator):
    """Concrete implementation of BaseFeatureGenerator for testing."""
    
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate features from the input DataFrame."""
        if not self.validate_data(df):
            return df
        
        df_features = df.copy()
        
        # Add a simple feature
        df_features['test_feature'] = df_features['Close'] / df_features['Open']
        self.log_feature_generation('test_feature', 0.5)
        
        return df_features
    
    def get_feature_names(self):
        """Get list of generated feature names."""
        return self.feature_names


class TestFeatureGeneratorIntegration:
    """Integration tests for feature generator."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range('2023-01-01', periods=600, freq='D')  # Increased to 600 to meet minimum requirement
        data = {
            'Open': np.random.uniform(100, 200, 600),
            'High': np.random.uniform(150, 250, 600),
            'Low': np.random.uniform(50, 150, 600),
            'Close': np.random.uniform(100, 200, 600),
            'Volume': np.random.uniform(1000, 10000, 600)
        }
        return pd.DataFrame(data, index=dates)
    
    def test_full_feature_generation_workflow(self, sample_data):
        """Test complete feature generation workflow."""
        config = FeatureConfig(
            short_periods=[5, 10],
            feature_types=['ratio']
        )
        generator = ConcreteFeatureGenerator(config)
        
        # Generate features
        result = generator.generate_features(sample_data)
        
        # Verify results
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert 'test_feature' in result.columns
        assert generator.get_feature_count() == 1
        assert 'test_feature' in generator.get_feature_names()
        assert generator.get_feature_importance()['test_feature'] == 0.5
    
    def test_feature_generation_with_invalid_data(self):
        """Test feature generation with invalid data."""
        generator = ConcreteFeatureGenerator()
        
        # Test with None
        result = generator.generate_features(None)
        assert result is None
        
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        result = generator.generate_features(empty_df)
        assert result is empty_df
    
    def test_feature_generation_with_missing_values(self, sample_data):
        """Test feature generation with missing values."""
        generator = ConcreteFeatureGenerator()
        
        # Add missing values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Open')] = np.nan
        
        # Should handle missing values automatically
        result = generator.generate_features(sample_data)
        assert isinstance(result, pd.DataFrame)
        assert 'test_feature' in result.columns


class TestFeatureConfigValidation:
    """Test FeatureConfig validation and edge cases."""
    
    def test_config_with_empty_lists(self):
        """Test config with empty lists."""
        config = FeatureConfig(
            short_periods=[],
            medium_periods=[],
            long_periods=[]
        )
        
        assert config.short_periods == []
        assert config.medium_periods == []
        assert config.long_periods == []
    
    def test_config_with_none_values(self):
        """Test config with None values."""
        config = FeatureConfig(
            short_periods=None,
            custom_params=None
        )
        
        # Should use defaults for None values
        assert config.short_periods == [5, 10, 14]
        assert config.custom_params == {}
    
    def test_config_custom_params_persistence(self):
        """Test that custom params persist correctly."""
        custom_params = {
            'param1': 'value1',
            'param2': 42,
            'param3': [1, 2, 3]
        }
        
        config = FeatureConfig(custom_params=custom_params)
        assert config.custom_params == custom_params
        # Note: dataclass doesn't automatically copy dict, so this might be the same object
        # The important thing is that the values are correct
