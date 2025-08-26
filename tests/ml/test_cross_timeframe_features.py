#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for CrossTimeframeFeatureGenerator class.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch

from src.ml.feature_engineering.cross_timeframe_features import (
    CrossTimeframeFeatureGenerator,
    CrossTimeframeFeatureConfig
)


class TestCrossTimeframeFeatureConfig:
    """Test CrossTimeframeFeatureConfig dataclass."""
    
    def test_default_values(self):
        """Test default values are set correctly."""
        config = CrossTimeframeFeatureConfig()
        
        # Test inherited values
        assert config.short_periods == [5, 10, 14]
        assert config.medium_periods == [20, 50, 100]
        assert config.long_periods == [200, 500]
        
        # Test specific values
        assert config.timeframes == ['1m', '5m', '15m', '1h', '4h', '1d']
        assert config.aggregation_methods == ['mean', 'std', 'min', 'max', 'last']
        assert config.feature_types == ['ratio', 'difference', 'momentum', 'volatility']
        assert config.lookback_periods == [5, 10, 20, 50]
    
    def test_custom_values(self):
        """Test custom values are preserved."""
        custom_config = CrossTimeframeFeatureConfig(
            timeframes=['1h', '1d'],
            feature_types=['ratio', 'momentum'],
            lookback_periods=[10, 20]
        )
        
        assert custom_config.timeframes == ['1h', '1d']
        assert custom_config.feature_types == ['ratio', 'momentum']
        assert custom_config.lookback_periods == [10, 20]
        
        # Default values should still be set
        assert custom_config.aggregation_methods == ['mean', 'std', 'min', 'max', 'last']


class TestCrossTimeframeFeatureGenerator:
    """Test CrossTimeframeFeatureGenerator class."""
    
    def test_initialization(self):
        """Test initialization with default config."""
        generator = CrossTimeframeFeatureGenerator()
        
        assert generator.config is not None
        assert isinstance(generator.config, CrossTimeframeFeatureConfig)
        assert generator.features_generated == 0
        assert generator.ratio_features == []
        assert generator.difference_features == []
        assert generator.momentum_features == []
        assert generator.volatility_features == []
    
    def test_initialization_with_custom_config(self):
        """Test initialization with custom config."""
        custom_config = CrossTimeframeFeatureConfig(
            timeframes=['1h', '1d'],
            feature_types=['ratio']
        )
        generator = CrossTimeframeFeatureGenerator(config=custom_config)
        
        assert generator.config.timeframes == ['1h', '1d']
        assert generator.config.feature_types == ['ratio']
    
    def test_generate_features_invalid_data(self):
        """Test generate_features with invalid data."""
        generator = CrossTimeframeFeatureGenerator()
        df = pd.DataFrame()  # Empty DataFrame
        
        result = generator.generate_features(df)
        
        assert result.equals(df)  # Should return original DataFrame unchanged
    
    def test_generate_features_valid_data(self):
        """Test generate_features with valid data."""
        generator = CrossTimeframeFeatureGenerator()
        # Create enough data to pass validation (need at least 500 rows)
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 500),
            'High': np.random.uniform(200, 300, 500),
            'Low': np.random.uniform(50, 100, 500),
            'Close': np.random.uniform(100, 200, 500),
            'Volume': np.random.uniform(1000, 10000, 500)
        })
        
        result = generator.generate_features(df)
        
        # Should return DataFrame with additional features
        assert len(result.columns) > len(df.columns)
        assert all(col in result.columns for col in df.columns)
    
    def test_generate_features_only_ratio(self):
        """Test generate_features with only ratio features."""
        config = CrossTimeframeFeatureConfig(feature_types=['ratio'])
        generator = CrossTimeframeFeatureGenerator(config=config)
        
        # Create enough data to pass validation
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 500),
            'High': np.random.uniform(200, 300, 500),
            'Low': np.random.uniform(50, 100, 500),
            'Close': np.random.uniform(100, 200, 500),
            'Volume': np.random.uniform(1000, 10000, 500)
        })
        
        result = generator.generate_features(df)
        
        # Should have ratio features
        assert len(result.columns) > len(df.columns)
        assert len(generator.ratio_features) > 0
    
    def test_generate_features_only_difference(self):
        """Test generate_features with only difference features."""
        config = CrossTimeframeFeatureConfig(feature_types=['difference'])
        generator = CrossTimeframeFeatureGenerator(config=config)
        
        # Create enough data to pass validation
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 500),
            'High': np.random.uniform(200, 300, 500),
            'Low': np.random.uniform(50, 100, 500),
            'Close': np.random.uniform(100, 200, 500),
            'Volume': np.random.uniform(1000, 10000, 500)
        })
        
        result = generator.generate_features(df)
        
        # Should have difference features
        assert len(result.columns) > len(df.columns)
        assert len(generator.difference_features) > 0
    
    def test_generate_features_only_momentum(self):
        """Test generate_features with only momentum features."""
        config = CrossTimeframeFeatureConfig(feature_types=['momentum'])
        generator = CrossTimeframeFeatureGenerator(config=config)
        
        # Create enough data to pass validation
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 500),
            'High': np.random.uniform(200, 300, 500),
            'Low': np.random.uniform(50, 100, 500),
            'Close': np.random.uniform(100, 200, 500),
            'Volume': np.random.uniform(1000, 10000, 500)
        })
        
        result = generator.generate_features(df)
        
        # Should have momentum features
        assert len(result.columns) > len(df.columns)
        assert len(generator.momentum_features) > 0
    
    def test_generate_features_only_volatility(self):
        """Test generate_features with only volatility features."""
        config = CrossTimeframeFeatureConfig(feature_types=['volatility'])
        generator = CrossTimeframeFeatureGenerator(config=config)
        
        # Create enough data to pass validation
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 500),
            'High': np.random.uniform(200, 300, 500),
            'Low': np.random.uniform(50, 100, 500),
            'Close': np.random.uniform(100, 200, 500),
            'Volume': np.random.uniform(1000, 10000, 500)
        })
        
        result = generator.generate_features(df)
        
        # Should have volatility features
        assert len(result.columns) > len(df.columns)
        assert len(generator.volatility_features) > 0
    
    def test_generate_features_logging(self):
        """Test that feature generation is logged."""
        generator = CrossTimeframeFeatureGenerator()
        # Create enough data to pass validation
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 500),
            'High': np.random.uniform(200, 300, 500),
            'Low': np.random.uniform(50, 100, 500),
            'Close': np.random.uniform(100, 200, 500),
            'Volume': np.random.uniform(1000, 10000, 500)
        })
        
        # Capture stdout to check logging
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            generator.generate_features(df)
            output = sys.stdout.getvalue()
            
            # Should have logged feature generation
            assert "Debug: Generated feature:" in output
            assert generator.features_generated > 0
        finally:
            sys.stdout = old_stdout
    
    def test_get_feature_names(self):
        """Test get_feature_names method."""
        generator = CrossTimeframeFeatureGenerator()
        # Set feature names in the correct attributes
        generator.ratio_features = ['ratio_1h_close']
        generator.momentum_features = ['momentum_4h_volume']
        
        names = generator.get_feature_names()
        
        assert 'ratio_1h_close' in names
        assert 'momentum_4h_volume' in names
        assert len(names) == 2
        # Should return a copy
        names.append('new_feature')
        assert 'new_feature' not in generator.ratio_features
        assert 'new_feature' not in generator.momentum_features
    
    def test_get_feature_names_empty(self):
        """Test get_feature_names method with empty feature list."""
        generator = CrossTimeframeFeatureGenerator()
        
        names = generator.get_feature_names()
        
        assert names == []
    
    def test_str_representation(self):
        """Test string representation."""
        generator = CrossTimeframeFeatureGenerator()
        generator.features_generated = 10
        
        result = str(generator)
        
        assert "CrossTimeframeFeatureGenerator" in result
        assert "features_generated=10" in result
    
    def test_repr_representation(self):
        """Test detailed string representation."""
        generator = CrossTimeframeFeatureGenerator()
        generator.features_generated = 10
        
        result = repr(generator)
        
        assert "CrossTimeframeFeatureGenerator" in result
        assert "features_generated=10" in result
        assert "config=" in result


class TestCrossTimeframeFeatureGeneratorIntegration:
    """Integration tests for CrossTimeframeFeatureGenerator."""
    
    def test_full_feature_generation_workflow(self):
        """Test complete feature generation workflow."""
        generator = CrossTimeframeFeatureGenerator()
        
        # Create realistic test data with enough rows
        dates = pd.date_range('2024-01-01', periods=500, freq='h')
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 500),
            'High': np.random.uniform(200, 300, 500),
            'Low': np.random.uniform(50, 100, 500),
            'Close': np.random.uniform(100, 200, 500),
            'Volume': np.random.uniform(1000, 10000, 500)
        }, index=dates)
        
        # Generate features
        result = generator.generate_features(df)
        
        # Verify results
        assert len(result) == len(df)  # Same number of rows
        assert len(result.columns) > len(df.columns)  # More columns
        assert generator.features_generated > 0  # Features were generated
        
        # Check that original data is preserved
        for col in df.columns:
            pd.testing.assert_series_equal(result[col], df[col])
    
    def test_feature_generation_with_missing_values(self):
        """Test feature generation with missing values."""
        generator = CrossTimeframeFeatureGenerator()
        
        # Create data with missing values but enough rows
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 500),
            'High': np.random.uniform(200, 300, 500),
            'Low': np.random.uniform(50, 100, 500),
            'Close': np.random.uniform(100, 200, 500),
            'Volume': np.random.uniform(1000, 10000, 500)
        })
        
        # Add some missing values
        df.loc[10:20, 'Open'] = np.nan
        df.loc[30:40, 'High'] = np.nan
        
        result = generator.generate_features(df)
        
        # Should handle missing values gracefully
        assert len(result) > 0
        assert len(result.columns) > len(df.columns)


if __name__ == "__main__":
    pytest.main([__file__])
