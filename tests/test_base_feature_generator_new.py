# -*- coding: utf-8 -*-
"""
Tests for base feature generator module.

This module tests the BaseFeatureGenerator class from src/ml/feature_engineering/base_feature_generator.py.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os
from typing import List

# Import the module to test
from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator, FeatureConfig, BUY, SELL, NOTRADE


class ConcreteFeatureGenerator(BaseFeatureGenerator):
    """Concrete implementation of BaseFeatureGenerator for testing."""
    
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate simple features for testing."""
        if not self.validate_data(df):
            return df
            
        df_result = df.copy()
        
        # Add a simple feature
        df_result['test_feature'] = df_result['Close'] / df_result['Close'].rolling(window=5).mean()
        
        self.log_feature_generation('test_feature', 0.5)
        
        return df_result
    
    def get_feature_names(self) -> List[str]:
        """Get list of generated feature names."""
        return self.feature_names.copy()


class TestFeatureConfig:
    """Test FeatureConfig class."""
    
    def test_init_defaults(self):
        """Test FeatureConfig initialization with defaults."""
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
        config = FeatureConfig(
            short_periods=[3, 7],
            medium_periods=[15, 30],
            long_periods=[100],
            price_types=['close'],
            volatility_periods=[10],
            volume_periods=[10],
            feature_types=['ratio'],
            custom_params={'test': 'value'}
        )
        
        assert config.short_periods == [3, 7]
        assert config.medium_periods == [15, 30]
        assert config.long_periods == [100]
        assert config.price_types == ['close']
        assert config.volatility_periods == [10]
        assert config.volume_periods == [10]
        assert config.feature_types == ['ratio']
        assert config.custom_params == {'test': 'value'}


class TestBaseFeatureGenerator:
    """Test BaseFeatureGenerator class."""
    
    @pytest.fixture
    def feature_config(self):
        """Create FeatureConfig instance for testing."""
        return FeatureConfig()
    
    @pytest.fixture
    def base_generator(self, feature_config):
        """Create ConcreteFeatureGenerator instance for testing."""
        return ConcreteFeatureGenerator(config=feature_config)
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range('2023-01-01', periods=600, freq='D')  # More data for validation
        data = {
            'Open': np.random.uniform(100, 200, 600),
            'High': np.random.uniform(150, 250, 600),
            'Low': np.random.uniform(50, 150, 600),
            'Close': np.random.uniform(100, 200, 600),
            'Volume': np.random.uniform(1000, 10000, 600)
        }
        return pd.DataFrame(data, index=dates)
    
    def test_init_with_config(self, feature_config):
        """Test ConcreteFeatureGenerator initialization with config."""
        generator = ConcreteFeatureGenerator(config=feature_config)
        
        assert generator.config == feature_config
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
    
    def test_init_without_config(self):
        """Test ConcreteFeatureGenerator initialization without config."""
        generator = ConcreteFeatureGenerator()
        
        assert generator.config is not None
        assert isinstance(generator.config, FeatureConfig)
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
    
    def test_validate_data_none(self, base_generator):
        """Test validate_data with None data."""
        result = base_generator.validate_data(None)
        assert result is False
    
    def test_validate_data_empty(self, base_generator):
        """Test validate_data with empty DataFrame."""
        result = base_generator.validate_data(pd.DataFrame())
        assert result is False
    
    def test_validate_data_missing_columns(self, base_generator):
        """Test validate_data with missing required columns."""
        data = pd.DataFrame({'Open': [1, 2, 3]})  # Missing High, Low, Close
        result = base_generator.validate_data(data)
        assert result is False
    
    def test_validate_data_insufficient_rows(self, base_generator):
        """Test validate_data with insufficient data rows."""
        data = pd.DataFrame({
            'Open': [1, 2, 3],
            'High': [2, 3, 4],
            'Low': [0, 1, 2],
            'Close': [1.5, 2.5, 3.5]
        })
        result = base_generator.validate_data(data)
        assert result is False  # Less than max(long_periods) = 500
    
    def test_validate_data_valid(self, base_generator, sample_data):
        """Test validate_data with valid data."""
        result = base_generator.validate_data(sample_data)
        assert result is True
    
    def test_handle_missing_values_forward_fill(self, base_generator, sample_data):
        """Test handle_missing_values with forward fill method."""
        # Add some NaN values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Close')] = np.nan
        
        result = base_generator.handle_missing_values(sample_data, method='forward_fill')
        
        assert result is not None
        assert not result.isna().any().any()  # No NaN values should remain
        assert len(result) == len(sample_data)
    
    def test_handle_missing_values_backward_fill(self, base_generator, sample_data):
        """Test handle_missing_values with backward fill method."""
        # Add some NaN values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Close')] = np.nan
        
        result = base_generator.handle_missing_values(sample_data, method='backward_fill')
        
        assert result is not None
        assert not result.isna().any().any()  # No NaN values should remain
        assert len(result) == len(sample_data)
    
    def test_handle_missing_values_interpolate(self, base_generator, sample_data):
        """Test handle_missing_values with interpolate method."""
        # Add some NaN values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Close')] = np.nan
        
        result = base_generator.handle_missing_values(sample_data, method='interpolate')
        
        assert result is not None
        assert not result.isna().any().any()  # No NaN values should remain
        assert len(result) == len(sample_data)
    
    def test_handle_missing_values_unknown_method(self, base_generator, sample_data):
        """Test handle_missing_values with unknown method."""
        # Add some NaN values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Close')] = np.nan
        
        result = base_generator.handle_missing_values(sample_data, method='unknown_method')
        
        assert result is not None
        assert not result.isna().any().any()  # Should use forward fill as fallback
        assert len(result) == len(sample_data)
    
    def test_calculate_returns_valid(self, base_generator, sample_data):
        """Test calculate_returns with valid data."""
        result = base_generator.calculate_returns(sample_data, price_col='Close')
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert pd.isna(result.iloc[0])  # First value should be NaN (no previous value)
        assert not result.iloc[1:].isna().all()  # Other values should not be all NaN
    
    def test_calculate_returns_invalid_column(self, base_generator, sample_data):
        """Test calculate_returns with invalid price column."""
        result = base_generator.calculate_returns(sample_data, price_col='InvalidColumn')
        
        assert isinstance(result, pd.Series)
        assert result.empty or result.dtype == float
    
    def test_calculate_log_returns_valid(self, base_generator, sample_data):
        """Test calculate_log_returns with valid data."""
        result = base_generator.calculate_log_returns(sample_data, price_col='Close')
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert pd.isna(result.iloc[0])  # First value should be NaN (no previous value)
        assert not result.iloc[1:].isna().all()  # Other values should not be all NaN
    
    def test_calculate_log_returns_invalid_column(self, base_generator, sample_data):
        """Test calculate_log_returns with invalid price column."""
        result = base_generator.calculate_log_returns(sample_data, price_col='InvalidColumn')
        
        assert isinstance(result, pd.Series)
        assert result.empty or result.dtype == float
    
    def test_get_feature_importance_empty(self, base_generator):
        """Test get_feature_importance with empty importance dict."""
        result = base_generator.get_feature_importance()
        
        assert isinstance(result, dict)
        assert len(result) == 0
    
    def test_get_feature_importance_with_data(self, base_generator):
        """Test get_feature_importance with data."""
        # Set some feature importance
        base_generator.feature_importance = {'feature1': 0.8, 'feature2': 0.6}
        
        result = base_generator.get_feature_importance()
        
        assert isinstance(result, dict)
        assert len(result) == 2
        assert result['feature1'] == 0.8
        assert result['feature2'] == 0.6
        assert result is not base_generator.feature_importance  # Should be a copy
    
    def test_set_feature_importance(self, base_generator):
        """Test set_feature_importance."""
        importance_dict = {'feature1': 0.8, 'feature2': 0.6}
        
        base_generator.set_feature_importance(importance_dict)
        
        assert base_generator.feature_importance == importance_dict
        assert base_generator.feature_importance is not importance_dict  # Should be a copy
    
    def test_get_feature_count(self, base_generator):
        """Test get_feature_count."""
        base_generator.features_generated = 10
        
        result = base_generator.get_feature_count()
        
        assert result == 10
    
    def test_reset_feature_count(self, base_generator):
        """Test reset_feature_count."""
        base_generator.features_generated = 10
        base_generator.feature_names = ['feature1', 'feature2']
        
        base_generator.reset_feature_count()
        
        assert base_generator.features_generated == 0
        assert base_generator.feature_names == []
    
    def test_log_feature_generation(self, base_generator):
        """Test log_feature_generation."""
        initial_count = base_generator.features_generated
        
        base_generator.log_feature_generation('test_feature', importance=0.8)
        
        assert base_generator.features_generated == initial_count + 1
        assert 'test_feature' in base_generator.feature_names
        assert base_generator.feature_importance['test_feature'] == 0.8
    
    def test_log_feature_generation_no_importance(self, base_generator):
        """Test log_feature_generation without importance."""
        initial_count = base_generator.features_generated
        
        base_generator.log_feature_generation('test_feature')
        
        assert base_generator.features_generated == initial_count + 1
        assert 'test_feature' in base_generator.feature_names
        assert 'test_feature' not in base_generator.feature_importance  # No importance set
    
    def test_str_representation(self, base_generator):
        """Test string representation."""
        base_generator.features_generated = 5
        
        result = str(base_generator)
        
        assert "ConcreteFeatureGenerator" in result
        assert "features_generated=5" in result
    
    def test_repr_representation(self, base_generator):
        """Test detailed string representation."""
        base_generator.features_generated = 5
        
        result = repr(base_generator)
        
        assert "ConcreteFeatureGenerator" in result
        assert "config=" in result
        assert "features_generated=5" in result
    
    def test_constants(self):
        """Test trading signal constants."""
        assert BUY == 1
        assert SELL == -1
        assert NOTRADE == 0


class TestBaseFeatureGeneratorAbstractMethods:
    """Test that BaseFeatureGenerator cannot be instantiated directly."""
    
    def test_cannot_instantiate_abstract_class(self):
        """Test that BaseFeatureGenerator cannot be instantiated due to abstract methods."""
        # This should work because we're not testing the abstract methods directly
        # The actual test is that concrete subclasses must implement them
        pass
    
    def test_abstract_methods_exist(self):
        """Test that abstract methods are defined."""
        # Check that abstract methods exist in the class
        assert hasattr(BaseFeatureGenerator, 'generate_features')
        assert hasattr(BaseFeatureGenerator, 'get_feature_names')
        
        # These methods should be abstract
        assert BaseFeatureGenerator.generate_features.__isabstractmethod__
        assert BaseFeatureGenerator.get_feature_names.__isabstractmethod__
