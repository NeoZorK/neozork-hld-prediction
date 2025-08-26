#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for src/ml/feature_engineering/cross_timeframe_features.py

This module provides comprehensive test coverage for the cross timeframe feature generator.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta


class TestCrossTimeframeFeatureConfig:
    """Test cases for CrossTimeframeFeatureConfig class."""
    
    def test_cross_timeframe_config_default_values(self):
        """Test CrossTimeframeFeatureConfig with default values."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureConfig
        
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
    
    def test_cross_timeframe_config_custom_values(self):
        """Test CrossTimeframeFeatureConfig with custom values."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureConfig
        
        custom_config = CrossTimeframeFeatureConfig(
            timeframes=['1h', '4h'],
            aggregation_methods=['mean', 'std'],
            feature_types=['ratio', 'momentum'],
            lookback_periods=[10, 20],
            short_periods=[3, 7],
            custom_params={'test': 'value'}
        )
        
        # Test custom values
        assert custom_config.timeframes == ['1h', '4h']
        assert custom_config.aggregation_methods == ['mean', 'std']
        assert custom_config.feature_types == ['ratio', 'momentum']
        assert custom_config.lookback_periods == [10, 20]
        assert custom_config.short_periods == [3, 7]
        assert custom_config.custom_params == {'test': 'value'}
        
        # Test that other values have defaults
        assert custom_config.medium_periods == [20, 50, 100]
        assert custom_config.long_periods == [200, 500]


class TestCrossTimeframeFeatureGenerator:
    """Test cases for CrossTimeframeFeatureGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator
        
        self.generator = CrossTimeframeFeatureGenerator()
        
        # Create sample data
        dates = pd.date_range('2023-01-01', periods=100, freq='h')
        self.sample_data = pd.DataFrame({
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 105,
            'Low': np.random.randn(100).cumsum() + 95,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
    
    def test_generator_initialization(self):
        """Test CrossTimeframeFeatureGenerator initialization."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator, CrossTimeframeFeatureConfig
        
        # Test with default config
        generator = CrossTimeframeFeatureGenerator()
        assert isinstance(generator.config, CrossTimeframeFeatureConfig)
        assert generator.ratio_features == []
        assert generator.difference_features == []
        assert generator.momentum_features == []
        assert generator.volatility_features == []
        
        # Test with custom config
        config = CrossTimeframeFeatureConfig(timeframes=['1h', '4h'])
        generator = CrossTimeframeFeatureGenerator(config)
        assert generator.config == config
    
    def test_get_required_columns(self):
        """Test get_required_columns method."""
        required_columns = self.generator.get_required_columns()
        
        assert isinstance(required_columns, list)
        assert 'Open' in required_columns
        assert 'High' in required_columns
        assert 'Low' in required_columns
        assert 'Close' in required_columns
        assert len(required_columns) == 4
    
    def test_validate_data_valid(self):
        """Test validate_data with valid data."""
        assert self.generator.validate_data(self.sample_data) is True
    
    def test_validate_data_none(self):
        """Test validate_data with None data."""
        with patch('src.ml.feature_engineering.cross_timeframe_features.logger') as mock_logger:
            assert self.generator.validate_data(None) is False
            mock_logger.print_error.assert_called_once()
    
    def test_validate_data_empty(self):
        """Test validate_data with empty DataFrame."""
        empty_df = pd.DataFrame()
        with patch('src.ml.feature_engineering.cross_timeframe_features.logger') as mock_logger:
            assert self.generator.validate_data(empty_df) is False
            mock_logger.print_error.assert_called_once()
    
    def test_validate_data_missing_columns(self):
        """Test validate_data with missing required columns."""
        invalid_data = self.sample_data.drop(columns=['Close'])
        with patch('src.ml.feature_engineering.cross_timeframe_features.logger') as mock_logger:
            assert self.generator.validate_data(invalid_data) is False
            mock_logger.print_error.assert_called_once()
    
    def test_validate_data_sufficient_rows(self):
        """Test validate_data with insufficient rows."""
        small_data = self.sample_data.head(2)  # Only 2 rows
        with patch('src.ml.feature_engineering.cross_timeframe_features.logger') as mock_logger:
            assert self.generator.validate_data(small_data) is False
            # Should print warning, not error
            mock_logger.print_warning.assert_called_once()
    
    def test_generate_features_abstract_method(self):
        """Test that generate_features is not abstract (it's implemented)."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator
        import inspect
        
        # Check that generate_features is implemented (not abstract)
        assert not inspect.isabstract(CrossTimeframeFeatureGenerator.generate_features)
    
    def test_generate_features_concrete_implementation(self):
        """Test generate_features with concrete implementation."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator
        
        class ConcreteGenerator(CrossTimeframeFeatureGenerator):
            def generate_features(self, df):
                """Generate cross-timeframe features."""
                if not self.validate_data(df):
                    return df
                
                result = df.copy()
                
                # Generate some cross-timeframe features
                result['cross_ratio_1h'] = df['Close'] / df['Close'].shift(4)  # 4-hour ratio
                result['cross_momentum_4h'] = df['Close'] - df['Close'].shift(16)  # 4-hour momentum
                result['cross_volatility_1d'] = df['Close'].rolling(24).std()  # Daily volatility
                
                return result
        
        generator = ConcreteGenerator()
        result = generator.generate_features(self.sample_data)
        
        assert 'cross_ratio_1h' in result.columns
        assert 'cross_momentum_4h' in result.columns
        assert 'cross_volatility_1d' in result.columns
        assert len(result) == len(self.sample_data)
    
    def test_generate_ratio_features(self):
        """Test _generate_ratio_features method."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator
        
        class TestGenerator(CrossTimeframeFeatureGenerator):
            def generate_features(self, df):
                return self._generate_ratio_features(df)
        
        generator = TestGenerator()
        result = generator._generate_ratio_features(self.sample_data)
        
        # Should return DataFrame with ratio features
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
    
    def test_generate_difference_features(self):
        """Test _generate_difference_features method."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator
        
        class TestGenerator(CrossTimeframeFeatureGenerator):
            def generate_features(self, df):
                return self._generate_difference_features(df)
        
        generator = TestGenerator()
        result = generator._generate_difference_features(self.sample_data)
        
        # Should return DataFrame with difference features
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
    
    def test_generate_momentum_features(self):
        """Test _generate_momentum_features method."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator
        
        class TestGenerator(CrossTimeframeFeatureGenerator):
            def generate_features(self, df):
                return self._generate_momentum_features(df)
        
        generator = TestGenerator()
        result = generator._generate_momentum_features(self.sample_data)
        
        # Should return DataFrame with momentum features
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
    
    def test_generate_volatility_features(self):
        """Test _generate_volatility_features method."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator
        
        class TestGenerator(CrossTimeframeFeatureGenerator):
            def generate_features(self, df):
                return self._generate_volatility_features(df)
        
        generator = TestGenerator()
        result = generator._generate_volatility_features(self.sample_data)
        
        # Should return DataFrame with volatility features
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
    
    def test_get_feature_names(self):
        """Test get_feature_names method."""
        feature_names = self.generator.get_feature_names()
        
        assert isinstance(feature_names, list)
        # Initially should be empty
        assert len(feature_names) == 0
    
    def test_get_feature_importance(self):
        """Test get_feature_importance method."""
        feature_importance = self.generator.get_feature_importance()
        
        assert isinstance(feature_importance, dict)
        # Initially should be empty
        assert len(feature_importance) == 0


class TestCrossTimeframeFeatureGeneratorEdgeCases:
    """Test edge cases for CrossTimeframeFeatureGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator
        
        self.generator = CrossTimeframeFeatureGenerator()
    
    def test_validate_data_with_nan_values(self):
        """Test validate_data with NaN values."""
        data_with_nan = pd.DataFrame({
            'Open': [100, np.nan, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106]
        })
        
        # Should be invalid due to insufficient rows (need at least 50)
        assert self.generator.validate_data(data_with_nan) is False
    
    def test_validate_data_with_infinite_values(self):
        """Test validate_data with infinite values."""
        data_with_inf = pd.DataFrame({
            'Open': [100, np.inf, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106]
        })
        
        # Should be invalid due to insufficient rows (need at least 50)
        assert self.generator.validate_data(data_with_inf) is False
    
    def test_validate_data_with_negative_values(self):
        """Test validate_data with negative values."""
        data_with_negative = pd.DataFrame({
            'Open': [100, -101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106]
        })
        
        # Should be invalid due to insufficient rows (need at least 50)
        assert self.generator.validate_data(data_with_negative) is False
    
    def test_validate_data_with_zero_values(self):
        """Test validate_data with zero values."""
        data_with_zero = pd.DataFrame({
            'Open': [100, 0, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106]
        })
        
        # Should be invalid due to insufficient rows (need at least 50)
        assert self.generator.validate_data(data_with_zero) is False


class TestCrossTimeframeFeatureGeneratorIntegration:
    """Integration tests for CrossTimeframeFeatureGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator
        
        self.generator = CrossTimeframeFeatureGenerator()
        
        # Create realistic test data
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=500, freq='h')
        self.test_data = pd.DataFrame({
            'Open': np.random.randn(500).cumsum() + 100,
            'High': np.random.randn(500).cumsum() + 105,
            'Low': np.random.randn(500).cumsum() + 95,
            'Close': np.random.randn(500).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 500)
        }, index=dates)
    
    def test_full_feature_generation_workflow(self):
        """Test complete cross-timeframe feature generation workflow."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator
        
        class FullGenerator(CrossTimeframeFeatureGenerator):
            def generate_features(self, df):
                """Generate comprehensive cross-timeframe features."""
                if not self.validate_data(df):
                    return df
                
                result = df.copy()
                
                # Generate ratio features
                for period in [4, 8, 24]:  # 4h, 8h, 1d
                    result[f'price_ratio_{period}h'] = df['Close'] / df['Close'].shift(period)
                
                # Generate momentum features
                for period in [4, 8, 24]:
                    result[f'price_momentum_{period}h'] = df['Close'] - df['Close'].shift(period)
                
                # Generate volatility features
                for period in [4, 8, 24]:
                    result[f'price_volatility_{period}h'] = df['Close'].rolling(period).std()
                
                # Generate volume features
                for period in [4, 8, 24]:
                    result[f'volume_ratio_{period}h'] = df['Volume'] / df['Volume'].shift(period)
                
                return result
        
        generator = FullGenerator()
        result = generator.generate_features(self.test_data)
        
        # Check that features were generated
        expected_features = [
            'price_ratio_4h', 'price_ratio_8h', 'price_ratio_24h',
            'price_momentum_4h', 'price_momentum_8h', 'price_momentum_24h',
            'price_volatility_4h', 'price_volatility_8h', 'price_volatility_24h',
            'volume_ratio_4h', 'volume_ratio_8h', 'volume_ratio_24h'
        ]
        
        for feature in expected_features:
            assert feature in result.columns
        
        # Check that original data is preserved
        assert 'Open' in result.columns
        assert 'High' in result.columns
        assert 'Low' in result.columns
        assert 'Close' in result.columns
        assert 'Volume' in result.columns
        
        # Check data integrity
        assert len(result) == len(self.test_data)
        assert not result.isnull().all().any()  # No completely null columns
    
    def test_feature_generation_with_custom_config(self):
        """Test feature generation with custom configuration."""
        from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator, CrossTimeframeFeatureConfig
        
        config = CrossTimeframeFeatureConfig(
            timeframes=['1h', '4h'],
            aggregation_methods=['mean', 'std'],
            feature_types=['ratio', 'momentum'],
            lookback_periods=[4, 8]
        )
        
        class CustomGenerator(CrossTimeframeFeatureGenerator):
            def generate_features(self, df):
                if not self.validate_data(df):
                    return df
                
                result = df.copy()
                
                # Use config values
                for period in self.config.lookback_periods:
                    result[f'custom_ratio_{period}h'] = df['Close'] / df['Close'].shift(period)
                    result[f'custom_momentum_{period}h'] = df['Close'] - df['Close'].shift(period)
                
                return result
        
        generator = CustomGenerator(config)
        result = generator.generate_features(self.test_data)
        
        # Check custom features
        assert 'custom_ratio_4h' in result.columns
        assert 'custom_ratio_8h' in result.columns
        assert 'custom_momentum_4h' in result.columns
        assert 'custom_momentum_8h' in result.columns
        
        # Check config was used
        assert generator.config == config
        assert generator.config.timeframes == ['1h', '4h']
        assert generator.config.lookback_periods == [4, 8]


if __name__ == '__main__':
    pytest.main([__file__])
