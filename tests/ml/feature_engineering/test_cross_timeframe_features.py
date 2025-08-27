# -*- coding: utf-8 -*-
"""
Tests for cross timeframe features module.

This module tests the CrossTimeframeFeatureGenerator class from src/ml/feature_engineering/cross_timeframe_features.py.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os

# Import the module to test
from src.ml.feature_engineering.cross_timeframe_features import (
    CrossTimeframeFeatureGenerator, 
    CrossTimeframeFeatureConfig
)


class TestCrossTimeframeFeatureConfig:
    """Test CrossTimeframeFeatureConfig class."""
    
    def test_init_defaults(self):
        """Test CrossTimeframeFeatureConfig initialization with defaults."""
        config = CrossTimeframeFeatureConfig()
        
        assert config.timeframes == ['1m', '5m', '15m', '1h', '4h', '1d']
        assert config.aggregation_methods == ['mean', 'std', 'min', 'max', 'last']
        assert config.feature_types == ['ratio', 'difference', 'momentum', 'volatility']
        assert config.lookback_periods == [5, 10, 20, 50]
        assert config.short_periods == [5, 10, 14]
        assert config.medium_periods == [20, 50, 100]
        assert config.long_periods == [200, 500]
    
    def test_init_custom_values(self):
        """Test CrossTimeframeFeatureConfig initialization with custom values."""
        config = CrossTimeframeFeatureConfig(
            timeframes=['1m', '5m'],
            aggregation_methods=['mean', 'std'],
            feature_types=['ratio'],
            lookback_periods=[10, 20],
            short_periods=[3, 7],
            medium_periods=[15, 30],
            long_periods=[100],
            price_types=['close'],
            volatility_periods=[10],
            volume_periods=[10],
            custom_params={'test': 'value'}
        )
        
        assert config.timeframes == ['1m', '5m']
        assert config.aggregation_methods == ['mean', 'std']
        assert config.feature_types == ['ratio']
        assert config.lookback_periods == [10, 20]
        assert config.short_periods == [3, 7]
        assert config.medium_periods == [15, 30]
        assert config.long_periods == [100]
        assert config.price_types == ['close']
        assert config.volatility_periods == [10]
        assert config.volume_periods == [10]
        assert config.custom_params == {'test': 'value'}


class TestCrossTimeframeFeatureGenerator:
    """Test CrossTimeframeFeatureGenerator class."""
    
    @pytest.fixture
    def feature_config(self):
        """Create CrossTimeframeFeatureConfig instance for testing."""
        return CrossTimeframeFeatureConfig()
    
    @pytest.fixture
    def feature_generator(self, feature_config):
        """Create CrossTimeframeFeatureGenerator instance for testing."""
        return CrossTimeframeFeatureGenerator(config=feature_config)
    
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
    
    def test_init(self, feature_generator, feature_config):
        """Test CrossTimeframeFeatureGenerator initialization."""
        assert feature_generator.config == feature_config
        assert feature_generator.features_generated == 0
        assert feature_generator.feature_names == []
        assert feature_generator.feature_importance == {}
        assert feature_generator.ratio_features == []
        assert feature_generator.difference_features == []
        assert feature_generator.momentum_features == []
        assert feature_generator.volatility_features == []
    
    def test_get_required_columns(self, feature_generator):
        """Test get_required_columns method."""
        required_columns = feature_generator.get_required_columns()
        assert required_columns == ['Open', 'High', 'Low', 'Close']
    
    def test_validate_data_none(self, feature_generator):
        """Test validate_data with None data."""
        result = feature_generator.validate_data(None)
        assert result is False
    
    def test_validate_data_empty(self, feature_generator):
        """Test validate_data with empty DataFrame."""
        result = feature_generator.validate_data(pd.DataFrame())
        assert result is False
    
    def test_validate_data_missing_columns(self, feature_generator):
        """Test validate_data with missing required columns."""
        data = pd.DataFrame({'Open': [1, 2, 3]})  # Missing High, Low, Close
        result = feature_generator.validate_data(data)
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
        result = feature_generator.validate_data(sample_data)
        assert result is True
    
    def test_generate_features_no_validation(self, feature_generator):
        """Test generate_features with invalid data."""
        data = pd.DataFrame({'Open': [1, 2, 3]})  # Invalid data
        result = feature_generator.generate_features(data)
        assert result.equals(data)  # Should return original data unchanged
    
    def test_generate_features_ratio_only(self, feature_generator, sample_data):
        """Test generate_features with ratio features only."""
        feature_generator.config.feature_types = ['ratio']
        result = feature_generator.generate_features(sample_data)
        
        assert len(result.columns) > len(sample_data.columns)
        assert feature_generator.features_generated > 0
        assert len(feature_generator.ratio_features) > 0
    
    def test_generate_features_difference_only(self, feature_generator, sample_data):
        """Test generate_features with difference features only."""
        feature_generator.config.feature_types = ['difference']
        result = feature_generator.generate_features(sample_data)
        
        assert len(result.columns) > len(sample_data.columns)
        assert feature_generator.features_generated > 0
        assert len(feature_generator.difference_features) > 0
    
    def test_generate_features_momentum_only(self, feature_generator, sample_data):
        """Test generate_features with momentum features only."""
        feature_generator.config.feature_types = ['momentum']
        result = feature_generator.generate_features(sample_data)
        
        assert len(result.columns) > len(sample_data.columns)
        assert feature_generator.features_generated > 0
        assert len(feature_generator.momentum_features) > 0
    
    def test_generate_features_volatility_only(self, feature_generator, sample_data):
        """Test generate_features with volatility features only."""
        feature_generator.config.feature_types = ['volatility']
        result = feature_generator.generate_features(sample_data)
        
        assert len(result.columns) > len(sample_data.columns)
        assert feature_generator.features_generated > 0
        assert len(feature_generator.volatility_features) > 0
    
    def test_generate_features_all_types(self, feature_generator, sample_data):
        """Test generate_features with all feature types."""
        result = feature_generator.generate_features(sample_data)
        
        assert len(result.columns) > len(sample_data.columns)
        assert feature_generator.features_generated > 0
        assert len(feature_generator.ratio_features) > 0
        assert len(feature_generator.difference_features) > 0
        assert len(feature_generator.momentum_features) > 0
        assert len(feature_generator.volatility_features) > 0
    
    def test_generate_ratio_features(self, feature_generator, sample_data):
        """Test _generate_ratio_features method."""
        result = feature_generator._generate_ratio_features(sample_data)
        
        assert len(result.columns) >= len(sample_data.columns)
        # Check if ratio features were generated
        if hasattr(feature_generator, 'ratio_features'):
            assert len(feature_generator.ratio_features) >= 0
    
    def test_generate_ratio_features_exception(self, feature_generator, sample_data):
        """Test _generate_ratio_features with exception."""
        # Mock logger to avoid print output during test
        with patch('src.ml.feature_engineering.cross_timeframe_features.logger'):
            # Create data that will cause an exception
            small_data = sample_data.iloc[:5]  # Too small for some calculations
            result = feature_generator._generate_ratio_features(small_data)
            assert isinstance(result, pd.DataFrame)
    
    def test_generate_difference_features(self, feature_generator, sample_data):
        """Test _generate_difference_features method."""
        result = feature_generator._generate_difference_features(sample_data)
        
        assert len(result.columns) > len(sample_data.columns)
        assert len(feature_generator.difference_features) > 0
    
    def test_generate_difference_features_exception(self, feature_generator, sample_data):
        """Test _generate_difference_features with exception."""
        with patch('src.ml.feature_engineering.cross_timeframe_features.logger'):
            small_data = sample_data.iloc[:5]
            result = feature_generator._generate_difference_features(small_data)
            assert isinstance(result, pd.DataFrame)
    
    def test_generate_momentum_features(self, feature_generator, sample_data):
        """Test _generate_momentum_features method."""
        result = feature_generator._generate_momentum_features(sample_data)
        
        assert len(result.columns) > len(sample_data.columns)
        assert len(feature_generator.momentum_features) > 0
    
    def test_generate_momentum_features_exception(self, feature_generator, sample_data):
        """Test _generate_momentum_features with exception."""
        with patch('src.ml.feature_engineering.cross_timeframe_features.logger'):
            small_data = sample_data.iloc[:5]
            result = feature_generator._generate_momentum_features(small_data)
            assert isinstance(result, pd.DataFrame)
    
    def test_generate_volatility_features(self, feature_generator, sample_data):
        """Test _generate_volatility_features method."""
        result = feature_generator._generate_volatility_features(sample_data)
        
        assert len(result.columns) > len(sample_data.columns)
        assert len(feature_generator.volatility_features) > 0
    
    def test_generate_volatility_features_exception(self, feature_generator, sample_data):
        """Test _generate_volatility_features with exception."""
        with patch('src.ml.feature_engineering.cross_timeframe_features.logger'):
            small_data = sample_data.iloc[:5]
            result = feature_generator._generate_volatility_features(small_data)
            assert isinstance(result, pd.DataFrame)
    
    def test_calculate_cross_timeframe_ratio(self, feature_generator, sample_data):
        """Test _calculate_cross_timeframe_ratio method."""
        result = feature_generator._calculate_cross_timeframe_ratio(sample_data, 'Close', 10)
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
    
    def test_calculate_cross_timeframe_ratio_invalid_column(self, feature_generator, sample_data):
        """Test _calculate_cross_timeframe_ratio with invalid column."""
        result = feature_generator._calculate_cross_timeframe_ratio(sample_data, 'InvalidColumn', 10)
        assert isinstance(result, pd.Series)
        assert result.empty
    
    def test_calculate_cross_timeframe_difference(self, feature_generator, sample_data):
        """Test _calculate_cross_timeframe_difference method."""
        result = feature_generator._calculate_cross_timeframe_difference(sample_data, 'Close', 10)
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
    
    def test_calculate_cross_timeframe_difference_invalid_column(self, feature_generator, sample_data):
        """Test _calculate_cross_timeframe_difference with invalid column."""
        result = feature_generator._calculate_cross_timeframe_difference(sample_data, 'InvalidColumn', 10)
        assert isinstance(result, pd.Series)
        assert result.empty
    
    def test_calculate_cross_timeframe_momentum(self, feature_generator, sample_data):
        """Test _calculate_cross_timeframe_momentum method."""
        result = feature_generator._calculate_cross_timeframe_momentum(sample_data, 'Close', 10)
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
    
    def test_calculate_cross_timeframe_momentum_invalid_column(self, feature_generator, sample_data):
        """Test _calculate_cross_timeframe_momentum with invalid column."""
        result = feature_generator._calculate_cross_timeframe_momentum(sample_data, 'InvalidColumn', 10)
        assert isinstance(result, pd.Series)
        assert result.empty
    
    def test_calculate_cross_timeframe_volatility(self, feature_generator, sample_data):
        """Test _calculate_cross_timeframe_volatility method."""
        result = feature_generator._calculate_cross_timeframe_volatility(sample_data, 'Close', 10)
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
    
    def test_calculate_cross_timeframe_volatility_invalid_column(self, feature_generator, sample_data):
        """Test _calculate_cross_timeframe_volatility with invalid column."""
        result = feature_generator._calculate_cross_timeframe_volatility(sample_data, 'InvalidColumn', 10)
        assert isinstance(result, pd.Series)
        assert result.empty
    
    def test_resample_data_empty(self, feature_generator):
        """Test _resample_data with empty DataFrame."""
        result = feature_generator._resample_data(pd.DataFrame(), '1H')
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    def test_resample_data_no_datetime_index(self, feature_generator, sample_data):
        """Test _resample_data with non-datetime index."""
        data = sample_data.reset_index(drop=True)  # Remove datetime index
        result = feature_generator._resample_data(data, '1H')
        assert result.equals(data)
    
    def test_resample_data_success(self, feature_generator, sample_data):
        """Test _resample_data with valid data."""
        result = feature_generator._resample_data(sample_data, '1H')
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
    
    def test_resample_data_exception(self, feature_generator, sample_data):
        """Test _resample_data with exception."""
        with patch('pandas.DataFrame.resample', side_effect=Exception("Test error")):
            with patch('src.ml.feature_engineering.cross_timeframe_features.logger'):
                result = feature_generator._resample_data(sample_data, '1H')
                assert result.equals(sample_data)
    
    def test_aggregate_data_empty(self, feature_generator):
        """Test _aggregate_data with empty DataFrame."""
        result = feature_generator._aggregate_data(pd.DataFrame(), 'mean', 5)
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    def test_aggregate_data_mean(self, feature_generator, sample_data):
        """Test _aggregate_data with mean method."""
        result = feature_generator._aggregate_data(sample_data, 'mean', 5)
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
    
    def test_aggregate_data_std(self, feature_generator, sample_data):
        """Test _aggregate_data with std method."""
        result = feature_generator._aggregate_data(sample_data, 'std', 5)
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
    
    def test_aggregate_data_min(self, feature_generator, sample_data):
        """Test _aggregate_data with min method."""
        result = feature_generator._aggregate_data(sample_data, 'min', 5)
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
    
    def test_aggregate_data_max(self, feature_generator, sample_data):
        """Test _aggregate_data with max method."""
        result = feature_generator._aggregate_data(sample_data, 'max', 5)
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
    
    def test_aggregate_data_last(self, feature_generator, sample_data):
        """Test _aggregate_data with last method."""
        result = feature_generator._aggregate_data(sample_data, 'last', 5)
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
    
    def test_aggregate_data_unknown_method(self, feature_generator, sample_data):
        """Test _aggregate_data with unknown method."""
        with patch('src.ml.feature_engineering.cross_timeframe_features.logger'):
            result = feature_generator._aggregate_data(sample_data, 'unknown', 5)
            assert result.equals(sample_data)
    
    def test_aggregate_data_exception(self, feature_generator, sample_data):
        """Test _aggregate_data with exception."""
        with patch('pandas.DataFrame.rolling', side_effect=Exception("Test error")):
            with patch('src.ml.feature_engineering.cross_timeframe_features.logger'):
                result = feature_generator._aggregate_data(sample_data, 'mean', 5)
                assert result.equals(sample_data)
    
    @patch('psutil.Process')
    def test_get_memory_usage(self, mock_process, feature_generator):
        """Test get_memory_usage method."""
        mock_process.return_value.memory_info.return_value.rss = 1024 * 1024  # 1MB
        
        result = feature_generator.get_memory_usage()
        
        assert isinstance(result, dict)
        assert 'config_size' in result
        assert 'features_generated' in result
        assert 'feature_names_count' in result
        assert 'ratio_features_count' in result
        assert 'difference_features_count' in result
        assert 'momentum_features_count' in result
        assert 'volatility_features_count' in result
        assert 'rss' in result
    
    def test_get_feature_names(self, feature_generator):
        """Test get_feature_names method."""
        # Add some features
        feature_generator.ratio_features = ['ratio_1', 'ratio_2']
        feature_generator.difference_features = ['diff_1']
        feature_generator.momentum_features = ['momentum_1', 'momentum_2', 'momentum_3']
        feature_generator.volatility_features = ['vol_1']
        
        result = feature_generator.get_feature_names()
        
        assert isinstance(result, list)
        assert len(result) == 7
        assert 'ratio_1' in result
        assert 'ratio_2' in result
        assert 'diff_1' in result
        assert 'momentum_1' in result
        assert 'momentum_2' in result
        assert 'momentum_3' in result
        assert 'vol_1' in result
    
    def test_get_feature_categories(self, feature_generator):
        """Test get_feature_categories method."""
        # Add some features
        feature_generator.ratio_features = ['ratio_1', 'ratio_2']
        feature_generator.difference_features = ['diff_1']
        feature_generator.momentum_features = ['momentum_1']
        feature_generator.volatility_features = ['vol_1']
        
        result = feature_generator.get_feature_categories()
        
        assert isinstance(result, dict)
        assert 'ratio' in result
        assert 'difference' in result
        assert 'momentum' in result
        assert 'volatility' in result
        assert 'all' in result
        assert result['ratio'] == ['ratio_1', 'ratio_2']
        assert result['difference'] == ['diff_1']
        assert result['momentum'] == ['momentum_1']
        assert result['volatility'] == ['vol_1']
        assert len(result['all']) == 5
