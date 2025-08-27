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

# Import the module to test
from src.ml.feature_engineering.base_feature_generator import (
    BaseFeatureGenerator, 
    FeatureConfig,
    BUY, SELL, NOTRADE
)


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


class ConcreteFeatureGenerator(BaseFeatureGenerator):
    """Concrete implementation of BaseFeatureGenerator for testing."""
    
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate simple features for testing."""
        if not self.validate_data(df):
            return df
        
        df_features = df.copy()
        
        # Add simple features
        if 'Close' in df.columns:
            df_features['close_ma_5'] = df['Close'].rolling(window=5).mean()
            df_features['close_ma_10'] = df['Close'].rolling(window=10).mean()
            self.features_generated += 2
            self.feature_names.extend(['close_ma_5', 'close_ma_10'])
        
        return df_features
    
    def get_feature_names(self) -> list:
        """Get list of generated feature names."""
        return self.feature_names


class TestBaseFeatureGenerator:
    """Test BaseFeatureGenerator class."""
    
    @pytest.fixture
    def feature_config(self):
        """Create FeatureConfig instance for testing."""
        return FeatureConfig()
    
    @pytest.fixture
    def feature_generator(self, feature_config):
        """Create ConcreteFeatureGenerator instance for testing."""
        return ConcreteFeatureGenerator(config=feature_config)
    
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
    
    def test_init_with_config(self, feature_config):
        """Test BaseFeatureGenerator initialization with config."""
        generator = ConcreteFeatureGenerator(config=feature_config)
        assert generator.config == feature_config
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
    
    def test_init_without_config(self):
        """Test BaseFeatureGenerator initialization without config."""
        generator = ConcreteFeatureGenerator()
        assert generator.config is not None
        assert isinstance(generator.config, FeatureConfig)
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
    
    def test_validate_data_none(self, feature_generator):
        """Test validate_data with None data."""
        result = feature_generator.validate_data(None)
        assert result is False
    
    def test_validate_data_empty(self, feature_generator):
        """Test validate_data with empty DataFrame."""
        result = feature_generator.validate_data(pd.DataFrame())
        assert result is False
    
    def test_validate_data_insufficient_rows(self, feature_generator):
        """Test validate_data with insufficient data rows."""
        data = pd.DataFrame({
            'Open': [100] * 10,
            'High': [150] * 10,
            'Low': [50] * 10,
            'Close': [120] * 10
        })
        result = feature_generator.validate_data(data)
        assert result is False
    
    def test_validate_data_valid(self, feature_generator, sample_data):
        """Test validate_data with valid data."""
        # Ensure sample_data has enough rows for validation
        if len(sample_data) < 500:
            # Extend the data to meet minimum requirements
            extended_data = sample_data.copy()
            while len(extended_data) < 500:
                extended_data = pd.concat([extended_data, sample_data], ignore_index=True)
            result = feature_generator.validate_data(extended_data)
        else:
            result = feature_generator.validate_data(sample_data)
        assert result is True
    
    def test_handle_missing_values_forward_fill(self, feature_generator, sample_data):
        """Test handle_missing_values with forward fill method."""
        # Add some NaN values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Close')] = np.nan
        
        result = feature_generator.handle_missing_values(sample_data, method='forward_fill')
        
        assert isinstance(result, pd.DataFrame)
        assert not result['Close'].isna().any()
    
    def test_handle_missing_values_backward_fill(self, feature_generator, sample_data):
        """Test handle_missing_values with backward fill method."""
        # Add some NaN values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Close')] = np.nan
        
        result = feature_generator.handle_missing_values(sample_data, method='backward_fill')
        
        assert isinstance(result, pd.DataFrame)
        assert not result['Close'].isna().any()
    
    def test_handle_missing_values_interpolate(self, feature_generator, sample_data):
        """Test handle_missing_values with interpolate method."""
        # Add some NaN values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Close')] = np.nan
        
        result = feature_generator.handle_missing_values(sample_data, method='interpolate')
        
        assert isinstance(result, pd.DataFrame)
        assert not result['Close'].isna().any()
    
    def test_handle_missing_values_unknown_method(self, feature_generator, sample_data):
        """Test handle_missing_values with unknown method."""
        # Add some NaN values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Close')] = np.nan
        
        result = feature_generator.handle_missing_values(sample_data, method='unknown_method')
        
        assert isinstance(result, pd.DataFrame)
        # Should return cleaned data (not original) due to dropna()
        assert not result.equals(sample_data)
        assert not result['Close'].isna().any()
    
    def test_calculate_returns_valid(self, feature_generator, sample_data):
        """Test calculate_returns with valid data."""
        result = feature_generator.calculate_returns(sample_data, price_col='Close')
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert pd.isna(result.iloc[0])  # First value should be NaN (no previous value)
        assert not result.iloc[1:].isna().all()  # Other values should not be all NaN
    
    def test_calculate_returns_invalid_column(self, feature_generator, sample_data):
        """Test calculate_returns with invalid price column."""
        result = feature_generator.calculate_returns(sample_data, price_col='InvalidColumn')
        
        assert isinstance(result, pd.Series)
        assert result.empty or result.dtype == float
    
    def test_calculate_log_returns_valid(self, feature_generator, sample_data):
        """Test calculate_log_returns with valid data."""
        result = feature_generator.calculate_log_returns(sample_data, price_col='Close')
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert pd.isna(result.iloc[0])  # First value should be NaN (no previous value)
        assert not result.iloc[1:].isna().all()  # Other values should not be all NaN
    
    def test_calculate_log_returns_invalid_column(self, feature_generator, sample_data):
        """Test calculate_log_returns with invalid price column."""
        result = feature_generator.calculate_log_returns(sample_data, price_col='InvalidColumn')
        
        assert isinstance(result, pd.Series)
        assert result.empty or result.dtype == float
    

    
    def test_generate_features_abstract(self):
        """Test that BaseFeatureGenerator cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseFeatureGenerator()
    
    def test_generate_features_concrete(self, feature_generator, sample_data):
        """Test generate_features with concrete implementation."""
        result = feature_generator.generate_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) > len(sample_data.columns)
        assert 'close_ma_5' in result.columns
        assert 'close_ma_10' in result.columns
        assert feature_generator.features_generated == 2
        assert len(feature_generator.feature_names) == 2
    
    def test_generate_features_invalid_data(self, feature_generator):
        """Test generate_features with invalid data."""
        invalid_data = pd.DataFrame({'Open': [1, 2, 3]})  # Missing required columns
        result = feature_generator.generate_features(invalid_data)
        
        assert result.equals(invalid_data)  # Should return original data unchanged
        assert feature_generator.features_generated == 0
    
    def test_get_feature_names(self, feature_generator, sample_data):
        """Test get_feature_names method."""
        # Generate some features first
        feature_generator.generate_features(sample_data)
        
        feature_names = feature_generator.get_feature_names()
        
        assert isinstance(feature_names, list)
        assert len(feature_names) == 2
        assert 'close_ma_5' in feature_names
        assert 'close_ma_10' in feature_names
    
    def test_log_feature_generation(self, feature_generator):
        """Test log_feature_generation method."""
        feature_generator.log_feature_generation('test_feature', importance=0.8)
        
        assert feature_generator.feature_importance['test_feature'] == 0.8
        assert 'test_feature' in feature_generator.feature_names
        assert feature_generator.features_generated == 1
    
    def test_log_feature_generation_no_importance(self, feature_generator):
        """Test log_feature_generation method without importance."""
        feature_generator.log_feature_generation('test_feature')
        
        assert feature_generator.feature_importance['test_feature'] == 0.5  # Default importance
        assert 'test_feature' in feature_generator.feature_names
        assert feature_generator.features_generated == 1
    
    def test_get_feature_importance(self, feature_generator):
        """Test get_feature_importance method."""
        # Add some features with importance
        feature_generator.log_feature_generation('feature_1', importance=0.8)
        feature_generator.log_feature_generation('feature_2', importance=0.6)
        
        importance = feature_generator.get_feature_importance()
        
        assert isinstance(importance, dict)
        assert importance['feature_1'] == 0.8
        assert importance['feature_2'] == 0.6
    
    def test_get_feature_importance(self, feature_generator):
        """Test get_feature_importance method."""
        # Add some features with importance
        feature_generator.log_feature_generation('feature_1', importance=0.8)
        feature_generator.log_feature_generation('feature_2', importance=0.6)
        
        importance = feature_generator.get_feature_importance()
        
        assert isinstance(importance, dict)
        assert importance['feature_1'] == 0.8
        assert importance['feature_2'] == 0.6
    
    def test_str_representation(self, feature_generator):
        """Test string representation."""
        feature_generator.features_generated = 5
        
        result = str(feature_generator)
        
        assert "ConcreteFeatureGenerator" in result
        assert "features_generated=5" in result
    
    def test_repr_representation(self, feature_generator):
        """Test detailed string representation."""
        feature_generator.features_generated = 5
        
        result = repr(feature_generator)
        
        assert "ConcreteFeatureGenerator" in result
        assert "config=" in result
        assert "features_generated=5" in result
    
    def test_constants(self):
        """Test trading signal constants."""
        assert BUY == 1
        assert SELL == -1
        assert NOTRADE == 0
    
    def test_validate_data_missing_columns(self, feature_generator):
        """Test validate_data with missing required columns."""
        data = pd.DataFrame({'Open': [1, 2, 3]})  # Missing High, Low, Close
        result = feature_generator.validate_data(data)
        assert result is False
    
    def test_handle_missing_values_no_nan(self, feature_generator, sample_data):
        """Test handle_missing_values with no NaN values."""
        result = feature_generator.handle_missing_values(sample_data, method='forward_fill')
        
        assert isinstance(result, pd.DataFrame)
        assert result.equals(sample_data)  # Should return unchanged data
    
    def test_calculate_returns_zero_price(self, feature_generator, sample_data):
        """Test calculate_returns with zero price values."""
        sample_data.loc[0, 'Close'] = 0
        sample_data.loc[1, 'Close'] = 100
        
        result = feature_generator.calculate_returns(sample_data, price_col='Close')
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert pd.isna(result.iloc[0])  # First value should be NaN
        assert pd.isna(result.iloc[1])  # Second value should be NaN due to division by zero
    
    def test_calculate_log_returns_zero_price(self, feature_generator, sample_data):
        """Test calculate_log_returns with zero price values."""
        sample_data.loc[0, 'Close'] = 0
        sample_data.loc[1, 'Close'] = 100
        
        result = feature_generator.calculate_log_returns(sample_data, price_col='Close')
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert pd.isna(result.iloc[0])  # First value should be NaN
        assert pd.isna(result.iloc[1])  # Second value should be NaN due to log(0)
    
    def test_multiple_feature_generation(self, feature_generator, sample_data):
        """Test multiple feature generation calls."""
        # First generation
        result1 = feature_generator.generate_features(sample_data)
        features_generated_1 = feature_generator.features_generated
        
        # Second generation
        result2 = feature_generator.generate_features(sample_data)
        features_generated_2 = feature_generator.features_generated
        
        assert features_generated_2 == features_generated_1 * 2
        assert len(result2.columns) > len(result1.columns)
    
    def test_feature_importance_accumulation(self, feature_generator):
        """Test feature importance accumulation."""
        # Add features with different importance levels
        feature_generator.log_feature_generation('feature_1', importance=0.8)
        feature_generator.log_feature_generation('feature_2', importance=0.6)
        feature_generator.log_feature_generation('feature_3', importance=0.9)
        
        importance = feature_generator.get_feature_importance()
        
        assert len(importance) == 3
        assert importance['feature_1'] == 0.8
        assert importance['feature_2'] == 0.6
        assert importance['feature_3'] == 0.9
        assert feature_generator.features_generated == 3
