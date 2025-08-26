#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for cross_timeframe_features.py module.

This module provides comprehensive test coverage for the cross-timeframe feature
generator that creates ML features by combining data from different timeframes.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from src.ml.feature_engineering.cross_timeframe_features import (
    CrossTimeframeFeatureGenerator, CrossTimeframeFeatureConfig
)


class TestCrossTimeframeFeatureConfig:
    """Test cases for CrossTimeframeFeatureConfig class."""
    
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
        assert config.custom_params == {}
        
        # Test cross-timeframe specific values
        assert config.timeframes == ['1m', '5m', '15m', '1h', '4h', '1d']
        assert config.aggregation_methods == ['mean', 'std', 'min', 'max', 'last']
        assert config.feature_types == ['ratio', 'difference', 'momentum', 'volatility']
        assert config.lookback_periods == [5, 10, 20, 50]
    
    def test_init_custom_values(self):
        """Test CrossTimeframeFeatureConfig initialization with custom values."""
        config = CrossTimeframeFeatureConfig(
            timeframes=['1h', '4h'],
            aggregation_methods=['mean', 'std'],
            feature_types=['ratio', 'difference'],
            lookback_periods=[10, 20]
        )
        
        assert config.timeframes == ['1h', '4h']
        assert config.aggregation_methods == ['mean', 'std']
        assert config.feature_types == ['ratio', 'difference']
        assert config.lookback_periods == [10, 20]
    
    def test_post_init_partial_custom_values(self):
        """Test CrossTimeframeFeatureConfig post_init with partial custom values."""
        config = CrossTimeframeFeatureConfig(
            timeframes=['1h', '4h']
        )
        
        assert config.timeframes == ['1h', '4h']
        assert config.aggregation_methods == ['mean', 'std', 'min', 'max', 'last']  # Default
        assert config.feature_types == ['ratio', 'difference', 'momentum', 'volatility']  # Default
        assert config.lookback_periods == [5, 10, 20, 50]  # Default


class TestCrossTimeframeFeatureGenerator:
    """Test cases for CrossTimeframeFeatureGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = CrossTimeframeFeatureConfig()
        self.generator = CrossTimeframeFeatureGenerator(self.config)
        
        # Create sample data with datetime index
        dates = pd.date_range('2023-01-01', periods=100, freq='1h')
        self.sample_data = pd.DataFrame({
            'Open': np.random.rand(100) * 100,
            'High': np.random.rand(100) * 100,
            'Low': np.random.rand(100) * 100,
            'Close': np.random.rand(100) * 100,
            'Volume': np.random.rand(100) * 1000
        }, index=dates)
    
    def test_init(self):
        """Test CrossTimeframeFeatureGenerator initialization."""
        assert self.generator.config == self.config
        assert self.generator.features_generated == 0
        assert self.generator.feature_names == []
        assert self.generator.feature_importance == {}
        assert self.generator.ratio_features == []
        assert self.generator.difference_features == []
        assert self.generator.momentum_features == []
        assert self.generator.volatility_features == []
    
    def test_init_without_config(self):
        """Test CrossTimeframeFeatureGenerator initialization without config."""
        generator = CrossTimeframeFeatureGenerator()
        assert generator.config is not None
        assert isinstance(generator.config, CrossTimeframeFeatureConfig)
    
    def test_validate_data_valid(self):
        """Test validate_data with valid data."""
        assert self.generator.validate_data(self.sample_data)
    
    def test_validate_data_empty(self):
        """Test validate_data with empty DataFrame."""
        empty_df = pd.DataFrame()
        assert not self.generator.validate_data(empty_df)
    
    def test_validate_data_none(self):
        """Test validate_data with None DataFrame."""
        assert not self.generator.validate_data(None)
    
    def test_validate_data_missing_columns(self):
        """Test validate_data with missing required columns."""
        invalid_data = self.sample_data.drop(columns=['Close'])
        assert not self.generator.validate_data(invalid_data)
    
    def test_get_required_columns(self):
        """Test get_required_columns method."""
        required_columns = self.generator.get_required_columns()
        assert isinstance(required_columns, list)
        assert 'Close' in required_columns
    
    def test_generate_features_no_validation(self):
        """Test generate_features when validation fails."""
        empty_df = pd.DataFrame()
        result = self.generator.generate_features(empty_df)
        assert result.equals(empty_df)
    
    def test_generate_features_ratio_only(self):
        """Test generate_features with ratio features only."""
        self.config.feature_types = ['ratio']
    
        with patch.object(self.generator, '_generate_ratio_features') as mock_ratio:
            mock_ratio.return_value = self.sample_data
            with patch.object(self.generator, 'validate_data', return_value=True):
                result = self.generator.generate_features(self.sample_data)
    
                # Check that the method was called
                assert mock_ratio.called
            assert result.equals(self.sample_data)
    
    def test_generate_features_difference_only(self):
        """Test generate_features with difference features only."""
        self.config.feature_types = ['difference']
    
        with patch.object(self.generator, '_generate_difference_features') as mock_diff:
            mock_diff.return_value = self.sample_data
            with patch.object(self.generator, 'validate_data', return_value=True):
                result = self.generator.generate_features(self.sample_data)
    
                # Check that the method was called
                assert mock_diff.called
            assert result.equals(self.sample_data)
    
    def test_generate_features_momentum_only(self):
        """Test generate_features with momentum features only."""
        self.config.feature_types = ['momentum']
    
        with patch.object(self.generator, '_generate_momentum_features') as mock_momentum:
            mock_momentum.return_value = self.sample_data
            with patch.object(self.generator, 'validate_data', return_value=True):
                result = self.generator.generate_features(self.sample_data)
    
                # Check that the method was called
                assert mock_momentum.called
            assert result.equals(self.sample_data)
    
    def test_generate_features_volatility_only(self):
        """Test generate_features with volatility features only."""
        self.config.feature_types = ['volatility']
    
        with patch.object(self.generator, '_generate_volatility_features') as mock_vol:
            mock_vol.return_value = self.sample_data
            with patch.object(self.generator, 'validate_data', return_value=True):
                result = self.generator.generate_features(self.sample_data)
    
                # Check that the method was called
                assert mock_vol.called
            assert result.equals(self.sample_data)
    
    def test_generate_features_all_types(self):
        """Test generate_features with all feature types."""
        with patch.object(self.generator, '_generate_ratio_features') as mock_ratio:
            with patch.object(self.generator, '_generate_difference_features') as mock_diff:
                with patch.object(self.generator, '_generate_momentum_features') as mock_momentum:
                    with patch.object(self.generator, '_generate_volatility_features') as mock_vol:
                        mock_ratio.return_value = self.sample_data
                        mock_diff.return_value = self.sample_data
                        mock_momentum.return_value = self.sample_data
                        mock_vol.return_value = self.sample_data
                        
                        result = self.generator.generate_features(self.sample_data)
                        
                        mock_ratio.assert_called_once()
                        mock_diff.assert_called_once()
                        mock_momentum.assert_called_once()
                        mock_vol.assert_called_once()
                        assert result.equals(self.sample_data)
    
    def test_generate_ratio_features(self):
        """Test _generate_ratio_features method."""
        result = self.generator._generate_ratio_features(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
        
        # Check that ratio features were added
        ratio_columns = [col for col in result.columns if 'ratio' in col.lower()]
        assert len(ratio_columns) > 0
    
    def test_generate_difference_features(self):
        """Test _generate_difference_features method."""
        result = self.generator._generate_difference_features(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
        
        # Check that difference features were added
        diff_columns = [col for col in result.columns if 'diff' in col.lower()]
        assert len(diff_columns) > 0
    
    def test_generate_momentum_features(self):
        """Test _generate_momentum_features method."""
        result = self.generator._generate_momentum_features(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
        
        # Check that momentum features were added
        momentum_columns = [col for col in result.columns if 'momentum' in col.lower()]
        assert len(momentum_columns) > 0
    
    def test_generate_volatility_features(self):
        """Test _generate_volatility_features method."""
        result = self.generator._generate_volatility_features(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
        
        # Check that volatility features were added
        vol_columns = [col for col in result.columns if 'volatility' in col.lower()]
        assert len(vol_columns) > 0
    
    def test_calculate_cross_timeframe_ratio(self):
        """Test _calculate_cross_timeframe_ratio method."""
        # Create sample data with different timeframes
        data_1h = self.sample_data.copy()
        data_4h = self.sample_data.resample('4h').mean().dropna()
    
        ratio = self.generator._calculate_cross_timeframe_ratio(
            data_1h, 'Close', 20
        )
        
        assert isinstance(ratio, pd.Series)
        assert len(ratio) == len(data_1h)
    
    def test_calculate_cross_timeframe_difference(self):
        """Test _calculate_cross_timeframe_difference method."""
        # Create sample data with different timeframes
        data_1h = self.sample_data.copy()
        data_4h = self.sample_data.resample('4h').mean().dropna()
    
        diff = self.generator._calculate_cross_timeframe_difference(
            data_1h, 'Close', 20
        )
        
        assert isinstance(diff, pd.Series)
        assert len(diff) == len(data_1h)
    
    def test_calculate_cross_timeframe_momentum(self):
        """Test _calculate_cross_timeframe_momentum method."""
        # Create sample data with different timeframes
        data_1h = self.sample_data.copy()
        data_4h = self.sample_data.resample('4h').mean().dropna()
    
        momentum = self.generator._calculate_cross_timeframe_momentum(
            data_1h, 'Close', 20
        )
        
        assert isinstance(momentum, pd.Series)
        assert len(momentum) == len(data_1h)
    
    def test_calculate_cross_timeframe_volatility(self):
        """Test _calculate_cross_timeframe_volatility method."""
        # Create sample data with different timeframes
        data_1h = self.sample_data.copy()
        data_4h = self.sample_data.resample('4h').mean().dropna()
    
        volatility = self.generator._calculate_cross_timeframe_volatility(
            data_1h, 'Close', 20
        )
        
        assert isinstance(volatility, pd.Series)
        assert len(volatility) == len(data_1h)
    
    def test_resample_data(self):
        """Test _resample_data method."""
        # Test resampling to different timeframes
        for timeframe in ['1H', '4H', '1D']:
            resampled = self.generator._resample_data(self.sample_data, timeframe)
            assert isinstance(resampled, pd.DataFrame)
            assert len(resampled) <= len(self.sample_data)
    
    def test_aggregate_data(self):
        """Test _aggregate_data method."""
        # Test different aggregation methods
        for method in ['mean', 'std', 'min', 'max', 'last']:
            aggregated = self.generator._aggregate_data(self.sample_data, method, 10)
            assert isinstance(aggregated, pd.DataFrame)
            assert len(aggregated) == len(self.sample_data)
    
    def test_get_feature_names(self):
        """Test get_feature_names method."""
        # Generate some features first
        self.generator.ratio_features = ['ratio_1', 'ratio_2']
        self.generator.difference_features = ['diff_1']
        self.generator.momentum_features = ['momentum_1']
        self.generator.volatility_features = ['vol_1']
        
        feature_names = self.generator.get_feature_names()
        expected = ['ratio_1', 'ratio_2', 'diff_1', 'momentum_1', 'vol_1']
        assert feature_names == expected
    
    def test_get_feature_importance(self):
        """Test get_feature_importance method."""
        # Set some feature importance
        self.generator.feature_importance = {
            'ratio_1': 0.8,
            'diff_1': 0.6,
            'momentum_1': 0.7
        }
        
        importance = self.generator.get_feature_importance()
        assert importance == self.generator.feature_importance
    
    def test_log_feature_generation(self):
        """Test log_feature_generation method."""
        # Test that the method doesn't raise an exception
        try:
            self.generator.log_feature_generation('test_feature', 0.8)
            # If we get here, the method worked
            assert True
        except Exception as e:
            assert False, f"log_feature_generation raised an exception: {e}"


class TestCrossTimeframeFeatureGeneratorEdgeCases:
    """Test edge cases for CrossTimeframeFeatureGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = CrossTimeframeFeatureGenerator()
    
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
        assert len(result) == 1
    
    def test_generate_features_with_large_data(self):
        """Test generate_features with large dataset."""
        dates = pd.date_range('2023-01-01', periods=10000, freq='1H')
        large_data = pd.DataFrame({
            'open': np.random.rand(10000) * 100,
            'high': np.random.rand(10000) * 100,
            'low': np.random.rand(10000) * 100,
            'close': np.random.rand(10000) * 100,
            'volume': np.random.rand(10000) * 1000
        }, index=dates)
        
        result = self.generator.generate_features(large_data)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10000
    
    def test_resample_data_empty_dataframe(self):
        """Test _resample_data with empty DataFrame."""
        empty_df = pd.DataFrame()
        resampled = self.generator._resample_data(empty_df, '1H')
        assert isinstance(resampled, pd.DataFrame)
        assert len(resampled) == 0
    
    def test_aggregate_data_unknown_method(self):
        """Test _aggregate_data with unknown aggregation method."""
        data = pd.DataFrame({'Close': [100, 101, 102]})
    
        # Should fall back to mean for unknown method
        aggregated = self.generator._aggregate_data(data, 'unknown_method', 10)
        assert isinstance(aggregated, pd.DataFrame)
        assert len(aggregated) == len(data)


class TestCrossTimeframeFeatureGeneratorIntegration:
    """Integration tests for CrossTimeframeFeatureGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = CrossTimeframeFeatureGenerator()
        
        # Create comprehensive test data
        dates = pd.date_range('2023-01-01', periods=1000, freq='1h')
        self.test_data = pd.DataFrame({
            'Open': np.random.rand(1000) * 100,
            'High': np.random.rand(1000) * 100,
            'Low': np.random.rand(1000) * 100,
            'Close': np.random.rand(1000) * 100,
            'Volume': np.random.rand(1000) * 1000
        }, index=dates)
    
    def test_full_feature_generation_workflow(self):
        """Test complete cross-timeframe feature generation workflow."""
        # Generate features
        result = self.generator.generate_features(self.test_data)
        
        # Verify results
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.test_data)
        
        # Check that features were generated
        feature_names = self.generator.get_feature_names()
        assert len(feature_names) > 0
        
        # Check feature importance
        feature_importance = self.generator.get_feature_importance()
        assert isinstance(feature_importance, dict)
        
        # Check feature categories
        categories = self.generator.get_feature_categories()
        assert isinstance(categories, dict)
        
        # Check memory usage
        memory_usage = self.generator.get_memory_usage()
        assert isinstance(memory_usage, dict)
        assert 'rss' in memory_usage
    
    def test_multiple_timeframe_combinations(self):
        """Test multiple timeframe combinations."""
        # Test different timeframe combinations
        timeframe_combinations = [
            (['1H', '4H'], ['ratio', 'difference']),
            (['1H', '1D'], ['momentum', 'volatility']),
            (['4H', '1D'], ['ratio', 'momentum'])
        ]
        
        for timeframes, feature_types in timeframe_combinations:
            config = CrossTimeframeFeatureConfig(
                timeframes=timeframes,
                feature_types=feature_types
            )
            generator = CrossTimeframeFeatureGenerator(config)
            
            result = generator.generate_features(self.test_data)
            assert isinstance(result, pd.DataFrame)
            assert len(result) == len(self.test_data)
    
    def test_feature_generation_performance(self):
        """Test feature generation performance with large dataset."""
        # Create large dataset
        dates = pd.date_range('2023-01-01', periods=50000, freq='1h')
        large_data = pd.DataFrame({
            'Open': np.random.rand(50000) * 100,
            'High': np.random.rand(50000) * 100,
            'Low': np.random.rand(50000) * 100,
            'Close': np.random.rand(50000) * 100,
            'Volume': np.random.rand(50000) * 1000
        }, index=dates)
        
        # Generate features
        result = self.generator.generate_features(large_data)
        
        # Verify results
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(large_data)
        
        # Check memory usage
        memory_usage = self.generator.get_memory_usage()
        assert isinstance(memory_usage, dict)
        assert 'rss' in memory_usage


if __name__ == '__main__':
    pytest.main([__file__])
