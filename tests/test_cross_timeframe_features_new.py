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
from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator, CrossTimeframeFeatureConfig


class TestCrossTimeframeFeatureConfig:
    """Test CrossTimeframeFeatureConfig class."""
    
    def test_init_defaults(self):
        """Test CrossTimeframeFeatureConfig initialization with defaults."""
        config = CrossTimeframeFeatureConfig()
        
        # Check inherited defaults
        assert config.short_periods == [5, 10, 14]
        assert config.medium_periods == [20, 50, 100]
        assert config.long_periods == [200, 500]
        assert config.price_types == ['open', 'high', 'low', 'close']
        assert config.volatility_periods == [14, 20, 50]
        assert config.volume_periods == [14, 20, 50]
        assert config.feature_types == ['ratio', 'difference', 'momentum', 'volatility']
        assert config.custom_params == {}
        
        # Check cross-timeframe specific defaults
        assert config.timeframes == ['1m', '5m', '15m', '1h', '4h', '1d']
        assert config.aggregation_methods == ['mean', 'std', 'min', 'max', 'last']
        assert config.lookback_periods == [5, 10, 20, 50]
    
    def test_init_custom_values(self):
        """Test CrossTimeframeFeatureConfig initialization with custom values."""
        config = CrossTimeframeFeatureConfig(
            timeframes=['1h', '1d'],
            aggregation_methods=['mean', 'std'],
            lookback_periods=[10, 20],
            feature_types=['ratio'],
            short_periods=[5],
            medium_periods=[20],
            long_periods=[100]
        )
        
        assert config.timeframes == ['1h', '1d']
        assert config.aggregation_methods == ['mean', 'std']
        assert config.lookback_periods == [10, 20]
        assert config.feature_types == ['ratio']
        assert config.short_periods == [5]
        assert config.medium_periods == [20]
        assert config.long_periods == [100]


class TestCrossTimeframeFeatureGenerator:
    """Test CrossTimeframeFeatureGenerator class."""
    
    @pytest.fixture
    def feature_config(self):
        """Create CrossTimeframeFeatureConfig instance for testing."""
        return CrossTimeframeFeatureConfig()
    
    @pytest.fixture
    def generator(self, feature_config):
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
    
    def test_init(self, feature_config):
        """Test CrossTimeframeFeatureGenerator initialization."""
        generator = CrossTimeframeFeatureGenerator(config=feature_config)
        
        assert generator.config == feature_config
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
        assert generator.ratio_features == []
        assert generator.difference_features == []
        assert generator.momentum_features == []
        assert generator.volatility_features == []
    
    def test_get_required_columns(self, generator):
        """Test get_required_columns."""
        required_columns = generator.get_required_columns()
        
        assert required_columns == ['Open', 'High', 'Low', 'Close']
    
    def test_validate_data_none(self, generator):
        """Test validate_data with None data."""
        result = generator.validate_data(None)
        assert result is False
    
    def test_validate_data_empty(self, generator):
        """Test validate_data with empty DataFrame."""
        result = generator.validate_data(pd.DataFrame())
        assert result is False
    
    def test_validate_data_missing_columns(self, generator):
        """Test validate_data with missing required columns."""
        data = pd.DataFrame({'Open': [1, 2, 3]})  # Missing High, Low, Close
        result = generator.validate_data(data)
        assert result is False
    
    def test_validate_data_insufficient_rows(self, generator):
        """Test validate_data with insufficient data rows."""
        data = pd.DataFrame({
            'Open': [1, 2, 3],
            'High': [2, 3, 4],
            'Low': [0, 1, 2],
            'Close': [1.5, 2.5, 3.5]
        })
        result = generator.validate_data(data)
        assert result is False  # Less than max(lookback_periods) = 50
    
    def test_validate_data_valid(self, generator, sample_data):
        """Test validate_data with valid data."""
        result = generator.validate_data(sample_data)
        assert result is True
    
    def test_generate_features_invalid_data(self, generator):
        """Test generate_features with invalid data."""
        result = generator.generate_features(None)
        assert result is None
    
    def test_generate_features_valid_data(self, generator, sample_data):
        """Test generate_features with valid data."""
        result = generator.generate_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert result.shape[1] >= sample_data.shape[1]  # Should have at least original columns
    
    def test_generate_features_only_ratio(self, generator, sample_data):
        """Test generate_features with only ratio features."""
        generator.config.feature_types = ['ratio']
        
        result = generator.generate_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.ratio_features) > 0
        assert len(generator.difference_features) == 0
        assert len(generator.momentum_features) == 0
        assert len(generator.volatility_features) == 0
    
    def test_generate_features_only_difference(self, generator, sample_data):
        """Test generate_features with only difference features."""
        generator.config.feature_types = ['difference']
        
        result = generator.generate_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.ratio_features) == 0
        assert len(generator.difference_features) > 0
        assert len(generator.momentum_features) == 0
        assert len(generator.volatility_features) == 0
    
    def test_generate_features_only_momentum(self, generator, sample_data):
        """Test generate_features with only momentum features."""
        generator.config.feature_types = ['momentum']
        
        result = generator.generate_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.ratio_features) == 0
        assert len(generator.difference_features) == 0
        assert len(generator.momentum_features) > 0
        assert len(generator.volatility_features) == 0
    
    def test_generate_features_only_volatility(self, generator, sample_data):
        """Test generate_features with only volatility features."""
        generator.config.feature_types = ['volatility']
        
        result = generator.generate_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.ratio_features) == 0
        assert len(generator.difference_features) == 0
        assert len(generator.momentum_features) == 0
        assert len(generator.volatility_features) > 0
    
    def test_generate_ratio_features(self, generator, sample_data):
        """Test _generate_ratio_features."""
        result = generator._generate_ratio_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.ratio_features) > 0
        
        # Check that ratio features were added
        ratio_columns = [col for col in result.columns if 'ratio_' in col]
        assert len(ratio_columns) > 0
    
    def test_generate_difference_features(self, generator, sample_data):
        """Test _generate_difference_features."""
        result = generator._generate_difference_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.difference_features) > 0
        
        # Check that difference features were added
        diff_columns = [col for col in result.columns if 'diff_' in col or 'norm_diff_' in col]
        assert len(diff_columns) > 0
    
    def test_generate_momentum_features(self, generator, sample_data):
        """Test _generate_momentum_features."""
        result = generator._generate_momentum_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.momentum_features) > 0
        
        # Check that momentum features were added
        momentum_columns = [col for col in result.columns if 'momentum_' in col]
        assert len(momentum_columns) > 0
    
    def test_generate_volatility_features(self, generator, sample_data):
        """Test _generate_volatility_features."""
        result = generator._generate_volatility_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.volatility_features) > 0
        
        # Check that volatility features were added
        volatility_columns = [col for col in result.columns if 'volatility_' in col]
        assert len(volatility_columns) > 0
    
    def test_calculate_cross_timeframe_ratio(self, generator, sample_data):
        """Test _calculate_cross_timeframe_ratio."""
        result = generator._calculate_cross_timeframe_ratio(sample_data, 'Close', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert not result.isna().all()  # Should not be all NaN
    
    def test_calculate_cross_timeframe_ratio_invalid_column(self, generator, sample_data):
        """Test _calculate_cross_timeframe_ratio with invalid column."""
        result = generator._calculate_cross_timeframe_ratio(sample_data, 'InvalidColumn', 10)
        
        assert isinstance(result, pd.Series)
        assert result.empty or result.dtype == float
    
    def test_calculate_cross_timeframe_difference(self, generator, sample_data):
        """Test _calculate_cross_timeframe_difference."""
        result = generator._calculate_cross_timeframe_difference(sample_data, 'Close', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert not result.isna().all()  # Should not be all NaN
    
    def test_calculate_cross_timeframe_difference_invalid_column(self, generator, sample_data):
        """Test _calculate_cross_timeframe_difference with invalid column."""
        result = generator._calculate_cross_timeframe_difference(sample_data, 'InvalidColumn', 10)
        
        assert isinstance(result, pd.Series)
        assert result.empty or result.dtype == float
    
    def test_calculate_cross_timeframe_momentum(self, generator, sample_data):
        """Test _calculate_cross_timeframe_momentum."""
        result = generator._calculate_cross_timeframe_momentum(sample_data, 'Close', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert not result.isna().all()  # Should not be all NaN
    
    def test_calculate_cross_timeframe_momentum_invalid_column(self, generator, sample_data):
        """Test _calculate_cross_timeframe_momentum with invalid column."""
        result = generator._calculate_cross_timeframe_momentum(sample_data, 'InvalidColumn', 10)
        
        assert isinstance(result, pd.Series)
        assert result.empty or result.dtype == float
    
    def test_calculate_cross_timeframe_volatility(self, generator, sample_data):
        """Test _calculate_cross_timeframe_volatility."""
        result = generator._calculate_cross_timeframe_volatility(sample_data, 'Close', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert not result.isna().all()  # Should not be all NaN
    
    def test_calculate_cross_timeframe_volatility_invalid_column(self, generator, sample_data):
        """Test _calculate_cross_timeframe_volatility with invalid column."""
        result = generator._calculate_cross_timeframe_volatility(sample_data, 'InvalidColumn', 10)
        
        assert isinstance(result, pd.Series)
        assert result.empty or result.dtype == float
    
    def test_resample_data_empty(self, generator):
        """Test _resample_data with empty DataFrame."""
        result = generator._resample_data(pd.DataFrame(), '1D')
        assert result.empty
    
    def test_resample_data_no_datetime_index(self, generator, sample_data):
        """Test _resample_data with no datetime index."""
        # Remove datetime index
        data_no_index = sample_data.reset_index(drop=True)
        result = generator._resample_data(data_no_index, '1D')
        assert result.equals(data_no_index)
    
    def test_resample_data_with_datetime_index(self, generator, sample_data):
        """Test _resample_data with datetime index."""
        result = generator._resample_data(sample_data, '1D')
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= len(sample_data)  # Resampling might reduce data points
        assert not result.empty
    
    def test_aggregate_data_empty(self, generator):
        """Test _aggregate_data with empty DataFrame."""
        result = generator._aggregate_data(pd.DataFrame(), 'mean', 5)
        assert result.empty
    
    def test_aggregate_data_mean(self, generator, sample_data):
        """Test _aggregate_data with mean method."""
        result = generator._aggregate_data(sample_data, 'mean', 5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == sample_data.shape
    
    def test_aggregate_data_std(self, generator, sample_data):
        """Test _aggregate_data with std method."""
        result = generator._aggregate_data(sample_data, 'std', 5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == sample_data.shape
    
    def test_aggregate_data_min(self, generator, sample_data):
        """Test _aggregate_data with min method."""
        result = generator._aggregate_data(sample_data, 'min', 5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == sample_data.shape
    
    def test_aggregate_data_max(self, generator, sample_data):
        """Test _aggregate_data with max method."""
        result = generator._aggregate_data(sample_data, 'max', 5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == sample_data.shape
    
    def test_aggregate_data_last(self, generator, sample_data):
        """Test _aggregate_data with last method."""
        result = generator._aggregate_data(sample_data, 'last', 5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == sample_data.shape
    
    def test_aggregate_data_unknown_method(self, generator, sample_data):
        """Test _aggregate_data with unknown method."""
        result = generator._aggregate_data(sample_data, 'unknown', 5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.equals(sample_data)  # Should return original data
    
    @patch('psutil.Process')
    def test_get_memory_usage(self, mock_process, generator):
        """Test get_memory_usage."""
        # Mock process memory info
        mock_memory_info = Mock()
        mock_memory_info.rss = 1024 * 1024 * 100  # 100 MB
        mock_process.return_value.memory_info.return_value = mock_memory_info
        
        result = generator.get_memory_usage()
        
        assert isinstance(result, dict)
        assert 'config_size' in result
        assert 'features_generated' in result
        assert 'feature_names_count' in result
        assert 'ratio_features_count' in result
        assert 'difference_features_count' in result
        assert 'momentum_features_count' in result
        assert 'volatility_features_count' in result
        assert 'rss' in result
        assert result['rss'] == 100.0  # Should be 100 MB
    
    def test_get_feature_names(self, generator):
        """Test get_feature_names."""
        # Add some features
        generator.ratio_features = ['ratio_1', 'ratio_2']
        generator.difference_features = ['diff_1']
        generator.momentum_features = ['momentum_1', 'momentum_2', 'momentum_3']
        generator.volatility_features = ['vol_1']
        
        result = generator.get_feature_names()
        
        expected_features = ['ratio_1', 'ratio_2', 'diff_1', 'momentum_1', 'momentum_2', 'momentum_3', 'vol_1']
        assert result == expected_features
    
    def test_get_feature_categories(self, generator):
        """Test get_feature_categories."""
        # Add some features
        generator.ratio_features = ['ratio_1', 'ratio_2']
        generator.difference_features = ['diff_1']
        generator.momentum_features = ['momentum_1', 'momentum_2']
        generator.volatility_features = ['vol_1']
        
        result = generator.get_feature_categories()
        
        assert isinstance(result, dict)
        assert 'ratio' in result
        assert 'difference' in result
        assert 'momentum' in result
        assert 'volatility' in result
        assert 'all' in result
        
        assert result['ratio'] == ['ratio_1', 'ratio_2']
        assert result['difference'] == ['diff_1']
        assert result['momentum'] == ['momentum_1', 'momentum_2']
        assert result['volatility'] == ['vol_1']
        assert result['all'] == ['ratio_1', 'ratio_2', 'diff_1', 'momentum_1', 'momentum_2', 'vol_1']
