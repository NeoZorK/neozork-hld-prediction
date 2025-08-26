#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for BaseFeatureGenerator class.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch

from src.ml.feature_engineering.base_feature_generator import (
    BaseFeatureGenerator, 
    FeatureConfig, 
    BUY, 
    SELL, 
    NOTRADE
)


class TestFeatureConfig:
    """Test FeatureConfig dataclass."""
    
    def test_default_values(self):
        """Test default values are set correctly."""
        config = FeatureConfig()
        
        assert config.short_periods == [5, 10, 14]
        assert config.medium_periods == [20, 50, 100]
        assert config.long_periods == [200, 500]
        assert config.price_types == ['open', 'high', 'low', 'close']
        assert config.volatility_periods == [14, 20, 50]
        assert config.volume_periods == [14, 20, 50]
        assert config.custom_params == {}
    
    def test_custom_values(self):
        """Test custom values are preserved."""
        custom_config = FeatureConfig(
            short_periods=[3, 7],
            custom_params={'test': 'value'}
        )
        
        assert custom_config.short_periods == [3, 7]
        assert custom_config.custom_params == {'test': 'value'}
        # Default values should still be set
        assert custom_config.medium_periods == [20, 50, 100]


class TestBaseFeatureGenerator:
    """Test BaseFeatureGenerator abstract class."""
    
    def test_constants(self):
        """Test trading signal constants."""
        assert BUY == 1
        assert SELL == -1
        assert NOTRADE == 0
    
    def test_initialization(self):
        """Test initialization with default config."""
        generator = MockBaseFeatureGenerator()
        
        assert generator.config is not None
        assert isinstance(generator.config, FeatureConfig)
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
    
    def test_initialization_with_custom_config(self):
        """Test initialization with custom config."""
        custom_config = FeatureConfig(short_periods=[3, 7])
        generator = MockBaseFeatureGenerator(config=custom_config)
        
        assert generator.config.short_periods == [3, 7]
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        generator = MockBaseFeatureGenerator()
        # Create enough data to pass validation (need at least 500 rows)
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 500),
            'High': np.random.uniform(200, 300, 500),
            'Low': np.random.uniform(50, 100, 500),
            'Close': np.random.uniform(100, 200, 500)
        })
        
        assert generator.validate_data(df) is True
    
    def test_validate_data_none(self):
        """Test data validation with None data."""
        generator = MockBaseFeatureGenerator()
        
        assert generator.validate_data(None) is False
    
    def test_validate_data_empty(self):
        """Test data validation with empty DataFrame."""
        generator = MockBaseFeatureGenerator()
        df = pd.DataFrame()
        
        assert generator.validate_data(df) is False
    
    def test_validate_data_missing_columns(self):
        """Test data validation with missing required columns."""
        generator = MockBaseFeatureGenerator()
        df = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [105, 106, 107]
            # Missing 'Low' and 'Close'
        })
        
        assert generator.validate_data(df) is False
    
    def test_validate_data_insufficient_data(self):
        """Test data validation with insufficient data."""
        generator = MockBaseFeatureGenerator()
        df = pd.DataFrame({
            'Open': [100, 101],  # Only 2 rows, need at least 200
            'High': [105, 106],
            'Low': [95, 96],
            'Close': [103, 104]
        })
        
        assert generator.validate_data(df) is False
    
    def test_handle_missing_values_forward_fill(self):
        """Test handling missing values with forward fill."""
        generator = MockBaseFeatureGenerator()
        df = pd.DataFrame({
            'Open': [100, np.nan, 102],
            'High': [105, 106, np.nan]
        })
        
        result = generator.handle_missing_values(df, 'forward_fill')
        
        assert not result.isna().any().any()
        assert result.iloc[1]['Open'] == 100  # Forward filled
        assert result.iloc[2]['High'] == 106  # Forward filled
    
    def test_handle_missing_values_backward_fill(self):
        """Test handling missing values with backward fill."""
        generator = MockBaseFeatureGenerator()
        df = pd.DataFrame({
            'Open': [np.nan, 101, 102],
            'High': [105, np.nan, 107]
        })
        
        result = generator.handle_missing_values(df, 'backward_fill')
        
        assert not result.isna().any().any()
        assert result.iloc[0]['Open'] == 101  # Backward filled
        assert result.iloc[1]['High'] == 107  # Backward filled
    
    def test_handle_missing_values_interpolate(self):
        """Test handling missing values with interpolation."""
        generator = MockBaseFeatureGenerator()
        df = pd.DataFrame({
            'Open': [100, np.nan, 102],
            'High': [105, np.nan, 107]
        })
        
        result = generator.handle_missing_values(df, 'interpolate')
        
        assert not result.isna().any().any()
        assert result.iloc[1]['Open'] == 101  # Interpolated
        assert result.iloc[1]['High'] == 106  # Interpolated
    
    def test_handle_missing_values_unknown_method(self):
        """Test handling missing values with unknown method."""
        generator = MockBaseFeatureGenerator()
        df = pd.DataFrame({
            'Open': [100, np.nan, 102]
        })
        
        result = generator.handle_missing_values(df, 'unknown_method')
        
        assert not result.isna().any().any()
        # Should fall back to forward fill
    
    def test_calculate_returns(self):
        """Test calculating returns."""
        generator = MockBaseFeatureGenerator()
        df = pd.DataFrame({
            'Close': [100, 105, 102, 108]
        })
        
        returns = generator.calculate_returns(df, 'Close')
        
        # Test that returns are calculated correctly (allow for floating point precision)
        assert pd.isna(returns.iloc[0])  # First value should be NaN
        assert abs(returns.iloc[1] - 0.05) < 1e-10  # Second value should be 0.05
        assert abs(returns.iloc[2] - (-0.02857142857142858)) < 1e-10  # Third value
        assert abs(returns.iloc[3] - 0.05882352941176472) < 1e-10  # Fourth value
    
    def test_calculate_returns_missing_column(self):
        """Test calculating returns with missing column."""
        generator = MockBaseFeatureGenerator()
        df = pd.DataFrame({
            'Open': [100, 105, 102]
        })
        
        returns = generator.calculate_returns(df, 'Close')
        
        assert returns.empty
        assert returns.dtype == float
    
    def test_calculate_log_returns(self):
        """Test calculating log returns."""
        generator = MockBaseFeatureGenerator()
        df = pd.DataFrame({
            'Close': [100, 105, 102, 108]
        })
        
        log_returns = generator.calculate_log_returns(df, 'Close')
        
        expected = pd.Series([np.nan, np.log(105/100), np.log(102/105), np.log(108/102)], name='Close')
        pd.testing.assert_series_equal(log_returns, expected, check_names=False)
    
    def test_calculate_log_returns_missing_column(self):
        """Test calculating log returns with missing column."""
        generator = MockBaseFeatureGenerator()
        df = pd.DataFrame({
            'Open': [100, 105, 102]
        })
        
        log_returns = generator.calculate_log_returns(df, 'Close')
        
        assert log_returns.empty
        assert log_returns.dtype == float
    
    def test_get_feature_importance(self):
        """Test getting feature importance."""
        generator = MockBaseFeatureGenerator()
        generator.feature_importance = {'feature1': 0.8, 'feature2': 0.6}
        
        importance = generator.get_feature_importance()
        
        assert importance == {'feature1': 0.8, 'feature2': 0.6}
        # Should return a copy
        importance['feature1'] = 0.9
        assert generator.feature_importance['feature1'] == 0.8
    
    def test_set_feature_importance(self):
        """Test setting feature importance."""
        generator = MockBaseFeatureGenerator()
        importance_dict = {'feature1': 0.8, 'feature2': 0.6}
        
        generator.set_feature_importance(importance_dict)
        
        assert generator.feature_importance == importance_dict
        # Should store a copy
        importance_dict['feature1'] = 0.9
        assert generator.feature_importance['feature1'] == 0.8
    
    def test_get_feature_count(self):
        """Test getting feature count."""
        generator = MockBaseFeatureGenerator()
        generator.features_generated = 5
        
        count = generator.get_feature_count()
        
        assert count == 5
    
    def test_reset_feature_count(self):
        """Test resetting feature count."""
        generator = MockBaseFeatureGenerator()
        generator.features_generated = 5
        generator.feature_names = ['feature1', 'feature2']
        
        generator.reset_feature_count()
        
        assert generator.features_generated == 0
        assert generator.feature_names == []
    
    @patch('src.ml.feature_engineering.base_feature_generator.logger')
    def test_log_feature_generation(self, mock_logger):
        """Test logging feature generation."""
        generator = MockBaseFeatureGenerator()
        
        generator.log_feature_generation('test_feature', 0.8)
        
        assert generator.features_generated == 1
        assert generator.feature_names == ['test_feature']
        assert generator.feature_importance['test_feature'] == 0.8
        mock_logger.print_debug.assert_called_once()
    
    @patch('src.ml.feature_engineering.base_feature_generator.logger')
    def test_log_feature_generation_zero_importance(self, mock_logger):
        """Test logging feature generation with zero importance."""
        generator = MockBaseFeatureGenerator()
        
        generator.log_feature_generation('test_feature', 0.0)
        
        assert generator.features_generated == 1
        assert generator.feature_names == ['test_feature']
        assert 'test_feature' not in generator.feature_importance
        mock_logger.print_debug.assert_called_once()
    
    def test_str_representation(self):
        """Test string representation."""
        generator = MockBaseFeatureGenerator()
        generator.features_generated = 5
        
        result = str(generator)
        
        assert result == "MockBaseFeatureGenerator(features_generated=5)"
    
    def test_repr_representation(self):
        """Test detailed string representation."""
        generator = MockBaseFeatureGenerator()
        generator.features_generated = 5
        
        result = repr(generator)
        
        assert "MockBaseFeatureGenerator" in result
        assert "features_generated=5" in result
        assert "config=" in result


class MockBaseFeatureGenerator(BaseFeatureGenerator):
    """Mock implementation of BaseFeatureGenerator for testing."""
    
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Mock implementation of generate_features."""
        if not self.validate_data(df):
            return df
        
        df_features = df.copy()
        df_features['mock_feature'] = df_features['Close'] * 0.1
        self.log_feature_generation('mock_feature', 0.5)
        return df_features
    
    def get_feature_names(self) -> list:
        """Mock implementation of get_feature_names."""
        return self.feature_names.copy()


if __name__ == "__main__":
    pytest.main([__file__])
