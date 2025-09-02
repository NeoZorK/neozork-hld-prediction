# -*- coding: utf-8 -*-
"""
Tests for cross_timeframe_features.py.

This module tests the cross-timeframe feature generator functionality.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock

from src.ml.feature_engineering.cross_timeframe_features import (
    CrossTimeframeFeatureGenerator, CrossTimeframeFeatureConfig
)


class TestCrossTimeframeFeatureConfig:
    """Test CrossTimeframeFeatureConfig dataclass."""
    
    def test_init_default_values(self):
        """Test CrossTimeframeFeatureConfig initialization with default values."""
        config = CrossTimeframeFeatureConfig()
        
        # Test inherited values
        assert config.short_periods == [5, 10, 14]
        assert config.medium_periods == [20, 50, 100]
        assert config.long_periods == [200, 500]
        assert config.price_types == ['open', 'high', 'low', 'close']
        assert config.volatility_periods == [14, 20, 50]
        assert config.volume_periods == [14, 20, 50]
        assert config.feature_types == ['ratio', 'difference', 'momentum', 'volatility']
        assert config.custom_params == {}
        
        # Test specific values
        assert config.timeframes == ['1m', '5m', '15m', '1h', '4h', '1d']
        assert config.aggregation_methods == ['mean', 'std', 'min', 'max', 'last']
        assert config.lookback_periods == [5, 10, 20, 50]
    
    def test_init_custom_values(self):
        """Test CrossTimeframeFeatureConfig initialization with custom values."""
        custom_config = CrossTimeframeFeatureConfig(
            timeframes=['1h', '4h'],
            aggregation_methods=['mean', 'std'],
            lookback_periods=[10, 20],
            feature_types=['ratio', 'momentum']
        )
        
        assert custom_config.timeframes == ['1h', '4h']
        assert custom_config.aggregation_methods == ['mean', 'std']
        assert custom_config.lookback_periods == [10, 20]
        assert custom_config.feature_types == ['ratio', 'momentum']
    
    def test_post_init_inheritance(self):
        """Test that post_init properly inherits from parent class."""
        config = CrossTimeframeFeatureConfig(
            short_periods=[3, 7],
            timeframes=['1h']
        )
        
        # Custom values should be preserved
        assert config.short_periods == [3, 7]
        assert config.timeframes == ['1h']
        
        # Other values should have defaults
        assert config.medium_periods == [20, 50, 100]
        assert config.aggregation_methods == ['mean', 'std', 'min', 'max', 'last']


class TestCrossTimeframeFeatureGenerator:
    """Test CrossTimeframeFeatureGenerator class."""
    
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
    
    def test_init_with_config(self):
        """Test CrossTimeframeFeatureGenerator initialization with config."""
        config = CrossTimeframeFeatureConfig(timeframes=['1h', '4h'])
        generator = CrossTimeframeFeatureGenerator(config)
        
        assert generator.config == config
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.ratio_features == []
        assert generator.difference_features == []
        assert generator.momentum_features == []
        assert generator.volatility_features == []
    
    def test_init_without_config(self):
        """Test CrossTimeframeFeatureGenerator initialization without config."""
        generator = CrossTimeframeFeatureGenerator()
        
        assert isinstance(generator.config, CrossTimeframeFeatureConfig)
        assert generator.features_generated == 0
        assert generator.feature_names == []
    
    def test_get_required_columns(self):
        """Test getting required columns."""
        generator = CrossTimeframeFeatureGenerator()
        required_cols = generator.get_required_columns()
        
        assert required_cols == ['Open', 'High', 'Low', 'Close']
    
    def test_validate_data_valid(self, sample_data):
        """Test data validation with valid data."""
        generator = CrossTimeframeFeatureGenerator()
        result = generator.validate_data(sample_data)
        assert result is True
    
    def test_validate_data_none(self):
        """Test data validation with None data."""
        generator = CrossTimeframeFeatureGenerator()
        result = generator.validate_data(None)
        assert result is False
    
    def test_validate_data_empty(self):
        """Test data validation with empty DataFrame."""
        generator = CrossTimeframeFeatureGenerator()
        empty_df = pd.DataFrame()
        result = generator.validate_data(empty_df)
        assert result is False
    
    def test_validate_data_missing_columns(self, sample_data):
        """Test data validation with missing required columns."""
        generator = CrossTimeframeFeatureGenerator()
        # Remove required column
        invalid_data = sample_data.drop(columns=['Open'])
        result = generator.validate_data(invalid_data)
        assert result is False
    
    def test_validate_data_insufficient_data(self):
        """Test data validation with insufficient data."""
        generator = CrossTimeframeFeatureGenerator()
        # Create data with insufficient rows
        insufficient_data = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [150, 151, 152],
            'Low': [50, 51, 52],
            'Close': [100, 101, 102]
        })
        result = generator.validate_data(insufficient_data)
        assert result is False
    
    def test_generate_features_ratio_only(self, sample_data):
        """Test feature generation with ratio features only."""
        config = CrossTimeframeFeatureConfig(feature_types=['ratio'])
        generator = CrossTimeframeFeatureGenerator(config)
        
        result = generator.generate_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.ratio_features) > 0
        assert len(generator.difference_features) == 0
        assert len(generator.momentum_features) == 0
        assert len(generator.volatility_features) == 0
    
    def test_generate_features_difference_only(self, sample_data):
        """Test feature generation with difference features only."""
        config = CrossTimeframeFeatureConfig(feature_types=['difference'])
        generator = CrossTimeframeFeatureGenerator(config)
        
        result = generator.generate_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.ratio_features) == 0
        assert len(generator.difference_features) > 0
        assert len(generator.momentum_features) == 0
        assert len(generator.volatility_features) == 0
    
    def test_generate_features_momentum_only(self, sample_data):
        """Test feature generation with momentum features only."""
        config = CrossTimeframeFeatureConfig(feature_types=['momentum'])
        generator = CrossTimeframeFeatureGenerator(config)
        
        result = generator.generate_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.ratio_features) == 0
        assert len(generator.difference_features) == 0
        assert len(generator.momentum_features) > 0
        assert len(generator.volatility_features) == 0
    
    def test_generate_features_volatility_only(self, sample_data):
        """Test feature generation with volatility features only."""
        config = CrossTimeframeFeatureConfig(feature_types=['volatility'])
        generator = CrossTimeframeFeatureGenerator(config)
        
        result = generator.generate_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.ratio_features) == 0
        assert len(generator.difference_features) == 0
        assert len(generator.momentum_features) == 0
        assert len(generator.volatility_features) > 0
    
    def test_generate_features_all_types(self, sample_data):
        """Test feature generation with all feature types."""
        config = CrossTimeframeFeatureConfig(
            feature_types=['ratio', 'difference', 'momentum', 'volatility']
        )
        generator = CrossTimeframeFeatureGenerator(config)
        
        result = generator.generate_features(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert len(generator.ratio_features) > 0
        assert len(generator.difference_features) > 0
        assert len(generator.momentum_features) > 0
        assert len(generator.volatility_features) > 0
    
    def test_generate_features_invalid_data(self):
        """Test feature generation with invalid data."""
        generator = CrossTimeframeFeatureGenerator()
        
        # Test with None
        result = generator.generate_features(None)
        assert result is None
        
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        result = generator.generate_features(empty_df)
        assert result is empty_df


class TestCrossTimeframeFeatureGeneration:
    """Test specific feature generation methods."""
    
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
    
    def test_generate_ratio_features(self, sample_data):
        """Test ratio feature generation."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._generate_ratio_features(sample_data.copy())
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        
        # Check that ratio features were added
        ratio_cols = [col for col in result.columns if col.startswith('ratio_')]
        assert len(ratio_cols) > 0
        
        # Check that features were logged
        assert len(generator.ratio_features) > 0
        assert generator.features_generated > 0
    
    def test_generate_difference_features(self, sample_data):
        """Test difference feature generation."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._generate_difference_features(sample_data.copy())
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        
        # Check that difference features were added
        diff_cols = [col for col in result.columns if col.startswith('diff_')]
        norm_diff_cols = [col for col in result.columns if col.startswith('norm_diff_')]
        assert len(diff_cols) > 0 or len(norm_diff_cols) > 0
        
        # Check that features were logged
        assert len(generator.difference_features) > 0
        assert generator.features_generated > 0
    
    def test_generate_momentum_features(self, sample_data):
        """Test momentum feature generation."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._generate_momentum_features(sample_data.copy())
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        
        # Check that momentum features were added
        momentum_cols = [col for col in result.columns if col.startswith('momentum_')]
        assert len(momentum_cols) > 0
        
        # Check that features were logged
        assert len(generator.momentum_features) > 0
        assert generator.features_generated > 0
    
    def test_generate_volatility_features(self, sample_data):
        """Test volatility feature generation."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._generate_volatility_features(sample_data.copy())
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        
        # Check that volatility features were added
        vol_cols = [col for col in result.columns if col.startswith('volatility_')]
        assert len(vol_cols) > 0
        
        # Check that features were logged
        assert len(generator.volatility_features) > 0
        assert generator.features_generated > 0


class TestCrossTimeframeCalculations:
    """Test cross-timeframe calculation methods."""
    
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
    
    def test_calculate_cross_timeframe_ratio(self, sample_data):
        """Test cross-timeframe ratio calculation."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._calculate_cross_timeframe_ratio(sample_data, 'Close', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert not result.iloc[:10].isna().all()  # First 10 values should be NaN
        assert not result.iloc[10:].isna().all()  # Later values should not be all NaN
    
    def test_calculate_cross_timeframe_ratio_invalid_column(self, sample_data):
        """Test cross-timeframe ratio calculation with invalid column."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._calculate_cross_timeframe_ratio(sample_data, 'InvalidColumn', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == 0
    
    def test_calculate_cross_timeframe_difference(self, sample_data):
        """Test cross-timeframe difference calculation."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._calculate_cross_timeframe_difference(sample_data, 'Close', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert not result.iloc[:10].isna().all()  # First 10 values should be NaN
        assert not result.iloc[10:].isna().all()  # Later values should not be all NaN
    
    def test_calculate_cross_timeframe_difference_invalid_column(self, sample_data):
        """Test cross-timeframe difference calculation with invalid column."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._calculate_cross_timeframe_difference(sample_data, 'InvalidColumn', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == 0
    
    def test_calculate_cross_timeframe_momentum(self, sample_data):
        """Test cross-timeframe momentum calculation."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._calculate_cross_timeframe_momentum(sample_data, 'Close', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert result.iloc[:10].isna().all()  # First 10 values should be NaN
        assert not result.iloc[10:].isna().all()  # Later values should not be all NaN
    
    def test_calculate_cross_timeframe_momentum_invalid_column(self, sample_data):
        """Test cross-timeframe momentum calculation with invalid column."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._calculate_cross_timeframe_momentum(sample_data, 'InvalidColumn', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == 0
    
    def test_calculate_cross_timeframe_volatility(self, sample_data):
        """Test cross-timeframe volatility calculation."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._calculate_cross_timeframe_volatility(sample_data, 'Close', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_data)
        assert result.iloc[:10].isna().all()  # First 10 values should be NaN
        assert not result.iloc[10:].isna().all()  # Later values should not be all NaN
    
    def test_calculate_cross_timeframe_volatility_invalid_column(self, sample_data):
        """Test cross-timeframe volatility calculation with invalid column."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._calculate_cross_timeframe_volatility(sample_data, 'InvalidColumn', 10)
        
        assert isinstance(result, pd.Series)
        assert len(result) == 0


class TestDataResamplingAndAggregation:
    """Test data resampling and aggregation methods."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data with datetime index for testing."""
        dates = pd.date_range('2023-01-01', periods=100, freq='H')
        data = {
            'Open': np.random.uniform(100, 200, 100),
            'High': np.random.uniform(150, 250, 100),
            'Low': np.random.uniform(50, 150, 100),
            'Close': np.random.uniform(100, 200, 100),
            'Volume': np.random.uniform(1000, 10000, 100)
        }
        return pd.DataFrame(data, index=dates)
    
    def test_resample_data_valid_timeframe(self, sample_data):
        """Test data resampling with valid timeframe."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._resample_data(sample_data, '4H')
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) < len(sample_data)  # Should have fewer rows
        assert 'Open' in result.columns
        assert 'High' in result.columns
        assert 'Low' in result.columns
        assert 'Close' in result.columns
        assert 'Volume' in result.columns
    
    def test_resample_data_empty_dataframe(self):
        """Test data resampling with empty DataFrame."""
        generator = CrossTimeframeFeatureGenerator()
        empty_df = pd.DataFrame()
        
        result = generator._resample_data(empty_df, '4H')
        assert result is empty_df
    
    def test_resample_data_no_datetime_index(self):
        """Test data resampling with non-datetime index."""
        generator = CrossTimeframeFeatureGenerator()
        df_no_datetime = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [150, 151, 152],
            'Low': [50, 51, 52],
            'Close': [100, 101, 102],
            'Volume': [1000, 1001, 1002]
        })
        
        result = generator._resample_data(df_no_datetime, '4H')
        assert result is df_no_datetime
    
    def test_aggregate_data_mean(self, sample_data):
        """Test data aggregation with mean method."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._aggregate_data(sample_data, 'mean', 5)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert 'Open' in result.columns
        assert 'High' in result.columns
        assert 'Low' in result.columns
        assert 'Close' in result.columns
        assert 'Volume' in result.columns
    
    def test_aggregate_data_std(self, sample_data):
        """Test data aggregation with std method."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._aggregate_data(sample_data, 'std', 5)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
    
    def test_aggregate_data_min(self, sample_data):
        """Test data aggregation with min method."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._aggregate_data(sample_data, 'min', 5)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
    
    def test_aggregate_data_max(self, sample_data):
        """Test data aggregation with max method."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._aggregate_data(sample_data, 'max', 5)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
    
    def test_aggregate_data_last(self, sample_data):
        """Test data aggregation with last method."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._aggregate_data(sample_data, 'last', 5)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
    
    def test_aggregate_data_unknown_method(self, sample_data):
        """Test data aggregation with unknown method."""
        generator = CrossTimeframeFeatureGenerator()
        
        result = generator._aggregate_data(sample_data, 'unknown_method', 5)
        
        assert result is sample_data  # Should return original data
    
    def test_aggregate_data_empty_dataframe(self):
        """Test data aggregation with empty DataFrame."""
        generator = CrossTimeframeFeatureGenerator()
        empty_df = pd.DataFrame()
        
        result = generator._aggregate_data(empty_df, 'mean', 5)
        assert result is empty_df


class TestFeatureManagement:
    """Test feature management methods."""
    
    def test_get_feature_names(self):
        """Test getting feature names."""
        generator = CrossTimeframeFeatureGenerator()
        
        # Add some features
        generator.ratio_features = ['ratio_1', 'ratio_2']
        generator.difference_features = ['diff_1']
        generator.momentum_features = ['momentum_1', 'momentum_2', 'momentum_3']
        generator.volatility_features = ['vol_1']
        
        feature_names = generator.get_feature_names()
        
        expected_names = ['ratio_1', 'ratio_2', 'diff_1', 'momentum_1', 'momentum_2', 'momentum_3', 'vol_1']
        assert feature_names == expected_names
    
    def test_get_feature_categories(self):
        """Test getting feature categories."""
        generator = CrossTimeframeFeatureGenerator()
        
        # Add some features
        generator.ratio_features = ['ratio_1', 'ratio_2']
        generator.difference_features = ['diff_1']
        generator.momentum_features = ['momentum_1']
        generator.volatility_features = ['vol_1']
        
        categories = generator.get_feature_categories()
        
        assert categories['ratio'] == ['ratio_1', 'ratio_2']
        assert categories['difference'] == ['diff_1']
        assert categories['momentum'] == ['momentum_1']
        assert categories['volatility'] == ['vol_1']
        assert categories['all'] == ['ratio_1', 'ratio_2', 'diff_1', 'momentum_1', 'vol_1']
    
    def test_get_memory_usage(self):
        """Test getting memory usage information."""
        generator = CrossTimeframeFeatureGenerator()
        
        # Add some features
        generator.ratio_features = ['ratio_1', 'ratio_2']
        generator.difference_features = ['diff_1']
        generator.momentum_features = ['momentum_1']
        generator.volatility_features = ['vol_1']
        generator.features_generated = 4
        generator.feature_names = ['ratio_1', 'ratio_2', 'diff_1', 'momentum_1']
        
        memory_info = generator.get_memory_usage()
        
        assert 'config_size' in memory_info
        assert 'features_generated' in memory_info
        assert 'feature_names_count' in memory_info
        assert 'ratio_features_count' in memory_info
        assert 'difference_features_count' in memory_info
        assert 'momentum_features_count' in memory_info
        assert 'volatility_features_count' in memory_info
        assert 'rss' in memory_info
        
        assert memory_info['features_generated'] == 4
        assert memory_info['feature_names_count'] == 4
        assert memory_info['ratio_features_count'] == 2
        assert memory_info['difference_features_count'] == 1
        assert memory_info['momentum_features_count'] == 1
        assert memory_info['volatility_features_count'] == 1


class TestCrossTimeframeFeatureGeneratorIntegration:
    """Integration tests for cross-timeframe feature generator."""
    
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
    
    def test_full_workflow(self, sample_data):
        """Test complete cross-timeframe feature generation workflow."""
        config = CrossTimeframeFeatureConfig(
            timeframes=['1h', '4h'],
            lookback_periods=[5, 10],
            feature_types=['ratio', 'momentum']
        )
        generator = CrossTimeframeFeatureGenerator(config)
        
        # Generate features
        result = generator.generate_features(sample_data)
        
        # Verify results
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert generator.get_feature_count() > 0
        assert len(generator.get_feature_names()) > 0
        
        # Check feature categories
        categories = generator.get_feature_categories()
        assert len(categories['ratio']) > 0
        assert len(categories['momentum']) > 0
        assert len(categories['difference']) == 0
        assert len(categories['volatility']) == 0
    
    def test_feature_generation_with_different_configs(self, sample_data):
        """Test feature generation with different configurations."""
        # Test with minimal config
        config1 = CrossTimeframeFeatureConfig(
            lookback_periods=[5],
            feature_types=['ratio']
        )
        generator1 = CrossTimeframeFeatureGenerator(config1)
        result1 = generator1.generate_features(sample_data)
        
        # Test with comprehensive config
        config2 = CrossTimeframeFeatureConfig(
            lookback_periods=[5, 10, 20],
            feature_types=['ratio', 'difference', 'momentum', 'volatility']
        )
        generator2 = CrossTimeframeFeatureGenerator(config2)
        result2 = generator2.generate_features(sample_data)
        
        # Second generator should produce more features
        assert generator2.get_feature_count() > generator1.get_feature_count()
        assert len(result2.columns) > len(result1.columns)
    
    def test_feature_generation_with_missing_values(self, sample_data):
        """Test feature generation with missing values."""
        # Add some missing values using iloc for positional indexing
        sample_data.iloc[10:15, sample_data.columns.get_loc('Open')] = np.nan
        sample_data.iloc[20:25, sample_data.columns.get_loc('Close')] = np.nan
        
        generator = CrossTimeframeFeatureGenerator()
        result = generator.generate_features(sample_data)
        
        # Should handle missing values gracefully
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
