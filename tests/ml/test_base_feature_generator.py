#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for src/ml/feature_engineering/base_feature_generator.py

This module provides comprehensive test coverage for the base feature generator.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from abc import ABC


class TestFeatureConfig:
    """Test cases for FeatureConfig class."""
    
    def test_feature_config_default_values(self):
        """Test FeatureConfig with default values."""
        from src.ml.feature_engineering.base_feature_generator import FeatureConfig
        
        config = FeatureConfig()
        
        assert config.short_periods == [5, 10, 14]
        assert config.medium_periods == [20, 50, 100]
        assert config.long_periods == [200, 500]
        assert config.price_types == ['open', 'high', 'low', 'close']
        assert config.volatility_periods == [14, 20, 50]
        assert config.volume_periods == [14, 20, 50]
        assert config.feature_types == ['ratio', 'difference', 'momentum', 'volatility']
        assert config.custom_params == {}
    
    def test_feature_config_custom_values(self):
        """Test FeatureConfig with custom values."""
        from src.ml.feature_engineering.base_feature_generator import FeatureConfig
        
        custom_config = FeatureConfig(
            short_periods=[3, 7],
            medium_periods=[15, 30],
            long_periods=[100, 200],
            price_types=['close', 'volume'],
            volatility_periods=[10, 20],
            volume_periods=[10, 20],
            feature_types=['ratio', 'momentum'],
            custom_params={'param1': 'value1'}
        )
        
        assert custom_config.short_periods == [3, 7]
        assert custom_config.medium_periods == [15, 30]
        assert custom_config.long_periods == [100, 200]
        assert custom_config.price_types == ['close', 'volume']
        assert custom_config.volatility_periods == [10, 20]
        assert custom_config.volume_periods == [10, 20]
        assert custom_config.feature_types == ['ratio', 'momentum']
        assert custom_config.custom_params == {'param1': 'value1'}
    
    def test_feature_config_partial_custom_values(self):
        """Test FeatureConfig with partial custom values."""
        from src.ml.feature_engineering.base_feature_generator import FeatureConfig
        
        config = FeatureConfig(
            short_periods=[3, 7],
            custom_params={'test': 'value'}
        )
        
        # Custom values should be set
        assert config.short_periods == [3, 7]
        assert config.custom_params == {'test': 'value'}
        
        # Other values should have defaults
        assert config.medium_periods == [20, 50, 100]
        assert config.long_periods == [200, 500]
        assert config.price_types == ['open', 'high', 'low', 'close']
        assert config.volatility_periods == [14, 20, 50]
        assert config.volume_periods == [14, 20, 50]
        assert config.feature_types == ['ratio', 'difference', 'momentum', 'volatility']


class TestBaseFeatureGenerator:
    """Test cases for BaseFeatureGenerator class."""
    
    def test_base_feature_generator_is_abstract(self):
        """Test that BaseFeatureGenerator is an abstract class."""
        from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator
        
        assert issubclass(BaseFeatureGenerator, ABC)
    
    def test_base_feature_generator_init_with_config(self):
        """Test BaseFeatureGenerator initialization with config."""
        from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator, FeatureConfig
        
        config = FeatureConfig(short_periods=[3, 7])
        
        # Create a concrete implementation for testing
        class TestGenerator(BaseFeatureGenerator):
            def generate_features(self, df):
                return df
            
            def get_feature_names(self):
                return []
        
        generator = TestGenerator(config)
        
        assert generator.config == config
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
    
    def test_base_feature_generator_init_without_config(self):
        """Test BaseFeatureGenerator initialization without config."""
        from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator, FeatureConfig
        
        # Create a concrete implementation for testing
        class TestGenerator(BaseFeatureGenerator):
            def generate_features(self, df):
                return df
            
            def get_feature_names(self):
                return []
        
        generator = TestGenerator()
        
        assert generator.config is not None
        assert isinstance(generator.config, FeatureConfig)
        assert generator.features_generated == 0
        assert generator.feature_names == []
        assert generator.feature_importance == {}
    
    def test_base_feature_generator_abstract_methods(self):
        """Test that BaseFeatureGenerator has abstract methods."""
        from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator
        import inspect
        
        # Check that the class is abstract
        assert inspect.isabstract(BaseFeatureGenerator)
        
        # Check that generate_features is abstract
        assert hasattr(BaseFeatureGenerator, 'generate_features')
        
        # Check that get_feature_names is abstract
        assert hasattr(BaseFeatureGenerator, 'get_feature_names')
    
    def test_base_feature_generator_cannot_be_instantiated(self):
        """Test that BaseFeatureGenerator cannot be instantiated directly."""
        from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator
        
        with pytest.raises(TypeError):
            BaseFeatureGenerator()


class TestConcreteFeatureGenerator:
    """Test cases for concrete feature generator implementation."""
    
    def test_concrete_generator_implementation(self):
        """Test a concrete implementation of BaseFeatureGenerator."""
        from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator, FeatureConfig
        
        class ConcreteGenerator(BaseFeatureGenerator):
            def generate_features(self, df):
                """Generate features from DataFrame."""
                result = df.copy()
                result['feature_1'] = df['close'] * 2
                result['feature_2'] = df['volume'] / 1000
                return result
            
            def get_feature_names(self):
                return ['feature_1', 'feature_2']
        
        # Test instantiation
        generator = ConcreteGenerator()
        assert isinstance(generator, BaseFeatureGenerator)
        
        # Test feature generation
        test_data = pd.DataFrame({
            'open': [100, 101, 102],
            'high': [105, 106, 107],
            'low': [95, 96, 97],
            'close': [102, 103, 104],
            'volume': [1000, 2000, 3000]
        })
        
        result = generator.generate_features(test_data)
        
        assert 'feature_1' in result.columns
        assert 'feature_2' in result.columns
        assert result['feature_1'].iloc[0] == 204  # 102 * 2
        assert result['feature_2'].iloc[0] == 1.0  # 1000 / 1000
    
    def test_concrete_generator_with_custom_config(self):
        """Test concrete generator with custom configuration."""
        from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator, FeatureConfig
        
        class CustomGenerator(BaseFeatureGenerator):
            def generate_features(self, df):
                result = df.copy()
                for period in self.config.short_periods:
                    result[f'sma_{period}'] = df['close'].rolling(period).mean()
                return result
            
            def get_feature_names(self):
                return [f'sma_{period}' for period in self.config.short_periods]
        
        config = FeatureConfig(short_periods=[3, 5])
        generator = CustomGenerator(config)
        
        test_data = pd.DataFrame({
            'close': [100, 101, 102, 103, 104, 105]
        })
        
        result = generator.generate_features(test_data)
        
        assert 'sma_3' in result.columns
        assert 'sma_5' in result.columns
        assert result['sma_3'].iloc[2] == 101.0  # (100 + 101 + 102) / 3
        assert result['sma_5'].iloc[4] == 102.0  # (100 + 101 + 102 + 103 + 104) / 5


class TestConstants:
    """Test cases for module constants."""
    
    def test_trading_signal_constants(self):
        """Test trading signal constants."""
        from src.ml.feature_engineering.base_feature_generator import BUY, SELL, NOTRADE
        
        assert BUY == 1
        assert SELL == -1
        assert NOTRADE == 0
        
        # Test that constants are different
        assert BUY != SELL
        assert BUY != NOTRADE
        assert SELL != NOTRADE


class TestIntegration:
    """Integration tests for base feature generator."""
    
    def test_feature_generator_with_real_data(self):
        """Test feature generator with realistic data."""
        from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator, FeatureConfig
        
        class RealisticGenerator(BaseFeatureGenerator):
            def generate_features(self, df):
                result = df.copy()
                
                # Generate some realistic features
                result['price_change'] = df['close'].pct_change()
                result['volume_ma'] = df['volume'].rolling(20).mean()
                result['volatility'] = df['close'].rolling(14).std()
                
                return result
            
            def get_feature_names(self):
                return ['price_change', 'volume_ma', 'volatility']
        
        # Create realistic test data
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        test_data = pd.DataFrame({
            'open': np.random.randn(100).cumsum() + 100,
            'high': np.random.randn(100).cumsum() + 105,
            'low': np.random.randn(100).cumsum() + 95,
            'close': np.random.randn(100).cumsum() + 100,
            'volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
        
        generator = RealisticGenerator()
        result = generator.generate_features(test_data)
        
        # Check that features were generated
        assert 'price_change' in result.columns
        assert 'volume_ma' in result.columns
        assert 'volatility' in result.columns
        
        # Check that original data is preserved
        assert 'open' in result.columns
        assert 'high' in result.columns
        assert 'low' in result.columns
        assert 'close' in result.columns
        assert 'volume' in result.columns
        
        # Check data types
        assert result['price_change'].dtype in [np.float64, np.float32]
        assert result['volume_ma'].dtype in [np.float64, np.float32]
        assert result['volatility'].dtype in [np.float64, np.float32]
    
    def test_feature_generator_error_handling(self):
        """Test feature generator error handling."""
        from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator
        
        class ErrorGenerator(BaseFeatureGenerator):
            def generate_features(self, df):
                if df is None or df.empty:
                    raise ValueError("Invalid data provided")
                return df
            
            def get_feature_names(self):
                return []
        
        generator = ErrorGenerator()
        
        # Test with None data
        with pytest.raises(ValueError, match="Invalid data provided"):
            generator.generate_features(None)
        
        # Test with empty DataFrame
        with pytest.raises(ValueError, match="Invalid data provided"):
            generator.generate_features(pd.DataFrame())


if __name__ == '__main__':
    pytest.main([__file__])
