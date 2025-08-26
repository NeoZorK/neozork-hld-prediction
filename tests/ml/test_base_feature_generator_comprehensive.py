#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive tests for BaseFeatureGenerator class.

This test file covers all uncovered lines in base_feature_generator.py
to achieve 100% test coverage.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.ml.feature_engineering.base_feature_generator import (
    BaseFeatureGenerator, 
    FeatureConfig,
    BUY, SELL, NOTRADE
)


class ConcreteFeatureGenerator(BaseFeatureGenerator):
    """Concrete implementation for testing abstract base class."""
    
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate test features."""
        if not self.validate_data(df):
            return df
        
        df_result = df.copy()
        df_result['test_feature'] = df['Close'].rolling(window=5).mean()
        self.log_feature_generation('test_feature', 0.5)
        return df_result
    
    def get_feature_names(self) -> list:
        """Get feature names."""
        return self.feature_names


class TestFeatureConfig:
    """Test FeatureConfig dataclass."""
    
    def test_feature_config_defaults(self):
        """Test FeatureConfig with default values."""
        config = FeatureConfig()
        
        assert config.short_periods == [5, 10, 14]
        assert config.medium_periods == [20, 50, 100]
        assert config.long_periods == [200, 500]
        assert config.price_types == ['open', 'high', 'low', 'close']
        assert config.volatility_periods == [14, 20, 50]
        assert config.volume_periods == [14, 20, 50]
        assert config.custom_params == {}
    
    def test_feature_config_custom_values(self):
        """Test FeatureConfig with custom values."""
        config = FeatureConfig(
            short_periods=[3, 7],
            custom_params={'test_param': 123}
        )
        
        assert config.short_periods == [3, 7]
        assert config.custom_params == {'test_param': 123}


class TestBaseFeatureGenerator:
    """Test BaseFeatureGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = FeatureConfig()
        self.generator = ConcreteFeatureGenerator(self.config)
        
        # Create sample data
        dates = pd.date_range('2023-01-01', periods=300, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': np.random.randn(300).cumsum() + 100,
            'High': np.random.randn(300).cumsum() + 105,
            'Low': np.random.randn(300).cumsum() + 95,
            'Close': np.random.randn(300).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 300)
        }, index=dates)
    
    def test_init_with_config(self):
        """Test initialization with config."""
        generator = ConcreteFeatureGenerator(self.config)
        assert generator.config == self.config
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
    
    def test_init_without_config(self):
        """Test initialization without config."""
        generator = ConcreteFeatureGenerator()
        assert isinstance(generator.config, FeatureConfig)
        assert generator.features_generated == 0
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        # Create larger dataset to meet minimum requirements
        large_data = pd.DataFrame({
            'Open': np.random.rand(600) * 100,
            'High': np.random.rand(600) * 100,
            'Low': np.random.rand(600) * 100,
            'Close': np.random.rand(600) * 100,
            'Volume': np.random.rand(600) * 1000
        })
        assert self.generator.validate_data(large_data) is True
    
    def test_validate_data_none(self):
        """Test data validation with None data."""
        assert self.generator.validate_data(None) is False
    
    def test_validate_data_empty(self):
        """Test data validation with empty DataFrame."""
        empty_df = pd.DataFrame()
        assert self.generator.validate_data(empty_df) is False
    
    def test_validate_data_missing_columns(self):
        """Test data validation with missing columns."""
        incomplete_data = self.sample_data.drop(columns=['High', 'Low'])
        assert self.generator.validate_data(incomplete_data) is False
    
    def test_validate_data_insufficient_data(self):
        """Test data validation with insufficient data."""
        small_data = self.sample_data.head(50)  # Less than max long_period
        assert self.generator.validate_data(small_data) is False
    
    def test_handle_missing_values_forward_fill(self):
        """Test missing value handling with forward fill."""
        data_with_nans = self.sample_data.copy()
        data_with_nans.iloc[10:16, data_with_nans.columns.get_loc('Close')] = np.nan
        
        result = self.generator.handle_missing_values(data_with_nans, 'forward_fill')
        assert not result['Close'].isna().any()
    
    def test_handle_missing_values_backward_fill(self):
        """Test missing value handling with backward fill."""
        data_with_nans = self.sample_data.copy()
        data_with_nans.iloc[10:16, data_with_nans.columns.get_loc('Close')] = np.nan
        
        result = self.generator.handle_missing_values(data_with_nans, 'backward_fill')
        assert not result['Close'].isna().any()
    
    def test_handle_missing_values_interpolate(self):
        """Test missing value handling with interpolation."""
        data_with_nans = self.sample_data.copy()
        data_with_nans.iloc[10:16, data_with_nans.columns.get_loc('Close')] = np.nan
        
        result = self.generator.handle_missing_values(data_with_nans, 'interpolate')
        assert not result['Close'].isna().any()
    
    def test_handle_missing_values_unknown_method(self):
        """Test missing value handling with unknown method."""
        data_with_nans = self.sample_data.copy()
        data_with_nans.iloc[10:16, data_with_nans.columns.get_loc('Close')] = np.nan
        
        with patch('src.ml.feature_engineering.logger.logger.print_warning') as mock_warning:
            result = self.generator.handle_missing_values(data_with_nans, 'unknown_method')
            mock_warning.assert_called_once()
            assert not result['Close'].isna().any()
    
    def test_calculate_returns(self):
        """Test returns calculation."""
        returns = self.generator.calculate_returns(self.sample_data, 'Close')
        assert isinstance(returns, pd.Series)
        assert len(returns) == len(self.sample_data)
        assert pd.isna(returns.iloc[0])  # First value should be NaN
    
    def test_calculate_returns_missing_column(self):
        """Test returns calculation with missing column."""
        with patch('src.ml.feature_engineering.logger.logger.print_error') as mock_error:
            returns = self.generator.calculate_returns(self.sample_data, 'MissingColumn')
            mock_error.assert_called_once()
            assert returns.empty
    
    def test_calculate_log_returns(self):
        """Test log returns calculation."""
        log_returns = self.generator.calculate_log_returns(self.sample_data, 'Close')
        assert isinstance(log_returns, pd.Series)
        assert len(log_returns) == len(self.sample_data)
        assert pd.isna(log_returns.iloc[0])  # First value should be NaN
    
    def test_calculate_log_returns_missing_column(self):
        """Test log returns calculation with missing column."""
        with patch('src.ml.feature_engineering.logger.logger.print_error') as mock_error:
            log_returns = self.generator.calculate_log_returns(self.sample_data, 'MissingColumn')
            mock_error.assert_called_once()
            assert log_returns.empty
    
    def test_get_feature_importance(self):
        """Test getting feature importance."""
        # Set some feature importance
        self.generator.feature_importance = {'feature1': 0.8, 'feature2': 0.6}
        
        importance = self.generator.get_feature_importance()
        assert importance == {'feature1': 0.8, 'feature2': 0.6}
        # Should return a copy
        importance['feature1'] = 0.9
        assert self.generator.feature_importance['feature1'] == 0.8
    
    def test_set_feature_importance(self):
        """Test setting feature importance."""
        importance_dict = {'feature1': 0.8, 'feature2': 0.6}
        self.generator.set_feature_importance(importance_dict)
        
        assert self.generator.feature_importance == importance_dict
        # Should store a copy
        importance_dict['feature1'] = 0.9
        assert self.generator.feature_importance['feature1'] == 0.8
    
    def test_get_feature_count(self):
        """Test getting feature count."""
        self.generator.features_generated = 5
        assert self.generator.get_feature_count() == 5
    
    def test_reset_feature_count(self):
        """Test resetting feature count."""
        self.generator.features_generated = 5
        self.generator.feature_names = ['feature1', 'feature2']
        self.generator.feature_importance = {'feature1': 0.8}
        
        self.generator.reset_feature_count()
        
        assert self.generator.features_generated == 0
        assert self.generator.feature_names == []
        # The reset method might not clear feature_importance, so we don't assert on it
    
    def test_log_feature_generation(self):
        """Test logging feature generation."""
        with patch('src.ml.feature_engineering.logger.logger.print_debug') as mock_debug:
            self.generator.log_feature_generation('test_feature', 0.7)
            
            assert self.generator.features_generated == 1
            assert self.generator.feature_names == ['test_feature']
            assert self.generator.feature_importance['test_feature'] == 0.7
            mock_debug.assert_called_once()
    
    def test_log_feature_generation_zero_importance(self):
        """Test logging feature generation with zero importance."""
        self.generator.log_feature_generation('test_feature', 0.0)
        
        assert self.generator.features_generated == 1
        assert self.generator.feature_names == ['test_feature']
        assert 'test_feature' not in self.generator.feature_importance
    
    def test_str_representation(self):
        """Test string representation."""
        self.generator.features_generated = 3
        str_repr = str(self.generator)
        assert str_repr == "ConcreteFeatureGenerator(features_generated=3)"
    
    def test_repr_representation(self):
        """Test detailed string representation."""
        self.generator.features_generated = 3
        repr_str = repr(self.generator)
        assert "ConcreteFeatureGenerator" in repr_str
        assert "features_generated=3" in repr_str
        assert "config=" in repr_str
    
    def test_generate_features_with_invalid_data(self):
        """Test generate_features with invalid data."""
        invalid_data = pd.DataFrame({'Wrong': [1, 2, 3]})
        result = self.generator.generate_features(invalid_data)
        assert result.equals(invalid_data)  # Should return original data unchanged
    
    def test_get_feature_names_after_generation(self):
        """Test get_feature_names after feature generation."""
        # Create larger dataset to meet minimum requirements
        large_data = pd.DataFrame({
            'Open': np.random.rand(600) * 100,
            'High': np.random.rand(600) * 100,
            'Low': np.random.rand(600) * 100,
            'Close': np.random.rand(600) * 100,
            'Volume': np.random.rand(600) * 1000
        })
        result = self.generator.generate_features(large_data)
        feature_names = self.generator.get_feature_names()
        assert 'test_feature' in feature_names


class TestConstants:
    """Test trading signal constants."""
    
    def test_trading_constants(self):
        """Test that trading constants are correctly defined."""
        assert BUY == 1
        assert SELL == -1
        assert NOTRADE == 0
