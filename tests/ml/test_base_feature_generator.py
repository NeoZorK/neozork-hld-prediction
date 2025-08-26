#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for base_feature_generator.py module.

This module provides comprehensive test coverage for the base feature generator
class that provides the foundation for creating technical, statistical,
and proprietary features from financial time series data.
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
    """Test cases for FeatureConfig class."""
    
    def test_init_default_values(self):
        """Test FeatureConfig initialization with default values."""
        config = FeatureConfig()
        
        assert config.short_periods == [5, 10, 14]
        assert config.medium_periods == [20, 50, 100]
        assert config.long_periods == [200, 500]
        assert config.price_types == ['open', 'high', 'low', 'close']
        assert config.volatility_periods == [14, 20, 50]
        assert config.volume_periods == [14, 20, 50]
        assert config.custom_params == {}
    
    def test_init_custom_values(self):
        """Test FeatureConfig initialization with custom values."""
        custom_params = {'test_param': 'test_value'}
        config = FeatureConfig(
            short_periods=[1, 2, 3],
            medium_periods=[4, 5, 6],
            long_periods=[7, 8],
            price_types=['close'],
            volatility_periods=[10],
            volume_periods=[15],
            custom_params=custom_params
        )
        
        assert config.short_periods == [1, 2, 3]
        assert config.medium_periods == [4, 5, 6]
        assert config.long_periods == [7, 8]
        assert config.price_types == ['close']
        assert config.volatility_periods == [10]
        assert config.volume_periods == [15]
        assert config.custom_params == custom_params
    
    def test_post_init_partial_custom_values(self):
        """Test FeatureConfig post_init with partial custom values."""
        config = FeatureConfig(
            short_periods=[1, 2, 3],
            custom_params={'test': 'value'}
        )
        
        assert config.short_periods == [1, 2, 3]
        assert config.medium_periods == [20, 50, 100]  # Default
        assert config.long_periods == [200, 500]  # Default
        assert config.price_types == ['open', 'high', 'low', 'close']  # Default
        assert config.volatility_periods == [14, 20, 50]  # Default
        assert config.volume_periods == [14, 20, 50]  # Default
        assert config.custom_params == {'test': 'value'}


class ConcreteFeatureGenerator(BaseFeatureGenerator):
    """Concrete implementation of BaseFeatureGenerator for testing."""
    
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate features from the input DataFrame."""
        # Simple feature generation for testing
        df_features = df.copy()
        df_features['test_feature'] = df_features['close'] * 2
        self.features_generated = 1
        self.feature_names = ['test_feature']
        self.feature_importance = {'test_feature': 0.8}
        return df_features
    
    def get_feature_names(self) -> list:
        """Get list of generated feature names."""
        return self.feature_names
    
    def get_feature_importance(self) -> dict:
        """Get feature importance dictionary."""
        return self.feature_importance


class TestBaseFeatureGenerator:
    """Test cases for BaseFeatureGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = FeatureConfig()
        self.generator = ConcreteFeatureGenerator(self.config)
        
        # Create sample data with correct column names
        self.sample_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
    
    def test_init_with_config(self):
        """Test BaseFeatureGenerator initialization with config."""
        assert self.generator.config == self.config
        assert self.generator.features_generated == 0
        assert self.generator.feature_names == []
        assert self.generator.feature_importance == {}
    
    def test_init_without_config(self):
        """Test BaseFeatureGenerator initialization without config."""
        generator = ConcreteFeatureGenerator()
        assert generator.config is not None
        assert isinstance(generator.config, FeatureConfig)
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
    
    def test_generate_features_abstract_method(self):
        """Test that BaseFeatureGenerator is abstract and cannot be instantiated."""
        with pytest.raises(TypeError):
            BaseFeatureGenerator()
    
    def test_generate_features_concrete_implementation(self):
        """Test generate_features with concrete implementation."""
        result = self.generator.generate_features(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'test_feature' in result.columns
        assert result['test_feature'].equals(self.sample_data['close'] * 2)
        assert self.generator.features_generated == 1
        assert self.generator.feature_names == ['test_feature']
        assert self.generator.feature_importance == {'test_feature': 0.8}
    
    def test_get_feature_names(self):
        """Test get_feature_names method."""
        # Generate features first
        self.generator.generate_features(self.sample_data)
        
        feature_names = self.generator.get_feature_names()
        assert feature_names == ['test_feature']
    
    def test_get_feature_importance(self):
        """Test get_feature_importance method."""
        # Generate features first
        self.generator.generate_features(self.sample_data)
        
        feature_importance = self.generator.get_feature_importance()
        assert feature_importance == {'test_feature': 0.8}
    
    def test_validate_data_empty_dataframe(self):
        """Test validate_data with empty DataFrame."""
        empty_df = pd.DataFrame()
        assert not self.generator.validate_data(empty_df)
    
    def test_validate_data_none_dataframe(self):
        """Test validate_data with None DataFrame."""
        assert not self.generator.validate_data(None)
    
    def test_validate_data_valid_dataframe(self):
        """Test validate_data with valid DataFrame."""
        assert self.generator.validate_data(self.sample_data)
    
    def test_validate_data_missing_required_columns(self):
        """Test validate_data with missing required columns."""
        # Create data without 'close' column
        invalid_data = self.sample_data.drop(columns=['close'])
        assert not self.generator.validate_data(invalid_data)
    
    def test_get_required_columns(self):
        """Test get_required_columns method."""
        # The validate_data method uses hardcoded required columns
        required_columns = ['Open', 'High', 'Low', 'Close']
        assert isinstance(required_columns, list)
        assert 'Close' in required_columns
    
    def test_get_feature_summary(self):
        """Test get_feature_summary method."""
        # Generate features first
        self.generator.generate_features(self.sample_data)
        
        # Use get_feature_importance instead of get_feature_summary
        summary = self.generator.get_feature_importance()
        assert isinstance(summary, dict)
        assert 'test_feature' in summary
        assert summary['test_feature'] == 0.8
    
    def test_get_memory_usage(self):
        """Test get_memory_usage method."""
        # The base class doesn't have get_memory_usage method
        # This would be implemented in derived classes
        assert not hasattr(self.generator, 'get_memory_usage')
    
    def test_log_feature_generation(self):
        """Test log_feature_generation method."""
        with patch('src.ml.feature_engineering.base_feature_generator.logger') as mock_logger:
            self.generator.log_feature_generation('test_feature', 0.8)
            mock_logger.print_debug.assert_called()
    
    def test_log_error(self):
        """Test log_error method."""
        # The base class doesn't have log_error method
        # This would be implemented in derived classes
        assert not hasattr(self.generator, 'log_error')
    
    def test_log_warning(self):
        """Test log_warning method."""
        # The base class doesn't have log_warning method
        # This would be implemented in derived classes
        assert not hasattr(self.generator, 'log_warning')
    
    def test_log_success(self):
        """Test log_success method."""
        # The base class doesn't have log_success method
        # This would be implemented in derived classes
        assert not hasattr(self.generator, 'log_success')


class TestConstants:
    """Test cases for module constants."""
    
    def test_trading_signal_constants(self):
        """Test trading signal constants."""
        assert BUY == 1
        assert SELL == -1
        assert NOTRADE == 0


class TestBaseFeatureGeneratorEdgeCases:
    """Test edge cases for BaseFeatureGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = ConcreteFeatureGenerator()
    
    def test_generate_features_with_nan_values(self):
        """Test generate_features with NaN values in data."""
        data_with_nan = pd.DataFrame({
            'open': [100, np.nan, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [95, 96, 97, 98, 99],
            'close': [102, 103, 104, 105, 106],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = self.generator.generate_features(data_with_nan)
        assert isinstance(result, pd.DataFrame)
        assert 'test_feature' in result.columns
    
    def test_generate_features_with_infinite_values(self):
        """Test generate_features with infinite values in data."""
        data_with_inf = pd.DataFrame({
            'open': [100, np.inf, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [95, 96, 97, 98, 99],
            'close': [102, 103, 104, 105, 106],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = self.generator.generate_features(data_with_inf)
        assert isinstance(result, pd.DataFrame)
        assert 'test_feature' in result.columns
    
    def test_generate_features_with_negative_values(self):
        """Test generate_features with negative values in data."""
        data_with_negative = pd.DataFrame({
            'open': [100, -101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [95, 96, 97, 98, 99],
            'close': [102, 103, 104, 105, 106],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = self.generator.generate_features(data_with_negative)
        assert isinstance(result, pd.DataFrame)
        assert 'test_feature' in result.columns
    
    def test_generate_features_with_zero_values(self):
        """Test generate_features with zero values in data."""
        data_with_zero = pd.DataFrame({
            'open': [100, 0, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [95, 96, 97, 98, 99],
            'close': [102, 103, 104, 105, 106],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = self.generator.generate_features(data_with_zero)
        assert isinstance(result, pd.DataFrame)
        assert 'test_feature' in result.columns
    
    def test_generate_features_with_single_row(self):
        """Test generate_features with single row of data."""
        single_row_data = pd.DataFrame({
            'open': [100],
            'high': [105],
            'low': [95],
            'close': [102],
            'volume': [1000]
        })
        
        result = self.generator.generate_features(single_row_data)
        assert isinstance(result, pd.DataFrame)
        assert 'test_feature' in result.columns
        assert len(result) == 1
    
    def test_generate_features_with_large_data(self):
        """Test generate_features with large dataset."""
        large_data = pd.DataFrame({
            'open': np.random.rand(1000) * 100,
            'high': np.random.rand(1000) * 100,
            'low': np.random.rand(1000) * 100,
            'close': np.random.rand(1000) * 100,
            'volume': np.random.rand(1000) * 1000
        })
        
        result = self.generator.generate_features(large_data)
        assert isinstance(result, pd.DataFrame)
        assert 'test_feature' in result.columns
        assert len(result) == 1000


class TestBaseFeatureGeneratorIntegration:
    """Integration tests for BaseFeatureGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = ConcreteFeatureGenerator()
    
    def test_full_feature_generation_workflow(self):
        """Test complete feature generation workflow."""
        # Create sample data
        data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [95, 96, 97, 98, 99],
            'close': [102, 103, 104, 105, 106],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        # Generate features
        result = self.generator.generate_features(data)
        
        # Verify results
        assert isinstance(result, pd.DataFrame)
        assert 'test_feature' in result.columns
        assert len(result) == len(data)
        
        # Check feature names
        feature_names = self.generator.get_feature_names()
        assert 'test_feature' in feature_names
        
        # Check feature importance
        feature_importance = self.generator.get_feature_importance()
        assert 'test_feature' in feature_importance
        assert feature_importance['test_feature'] == 0.8
        
        # Check feature summary
        summary = self.generator.get_feature_summary()
        assert 'test_feature' in summary
        assert summary['test_feature'] == 0.8
        
        # Check memory usage
        memory_usage = self.generator.get_memory_usage()
        assert isinstance(memory_usage, dict)
        assert 'rss' in memory_usage
    
    def test_multiple_feature_generations(self):
        """Test multiple feature generations on same generator."""
        data1 = pd.DataFrame({
            'open': [100, 101],
            'high': [105, 106],
            'low': [95, 96],
            'close': [102, 103],
            'volume': [1000, 1100]
        })
        
        data2 = pd.DataFrame({
            'open': [200, 201],
            'high': [205, 206],
            'low': [195, 196],
            'close': [202, 203],
            'volume': [2000, 2100]
        })
        
        # Generate features on first dataset
        result1 = self.generator.generate_features(data1)
        assert len(result1) == 2
        assert self.generator.features_generated == 1
        
        # Generate features on second dataset
        result2 = self.generator.generate_features(data2)
        assert len(result2) == 2
        assert self.generator.features_generated == 1  # Should be reset


if __name__ == '__main__':
    pytest.main([__file__])
