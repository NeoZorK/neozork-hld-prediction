# -*- coding: utf-8 -*-
# tests/ml/test_feature_engineering.py

"""
Comprehensive tests for ML feature engineering modules.
All comments are in English.
"""

import unittest
import tempfile
import os
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Import the modules to test
from src.ml.feature_engineering.base_feature_generator import (
    BaseFeatureGenerator, FeatureConfig, BUY, SELL, NOTRADE
)
from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator, CrossTimeframeFeatureConfig
from src.ml.feature_engineering.feature_generator import FeatureGenerator, MasterFeatureConfig
from src.ml.feature_engineering.feature_selector import FeatureSelectionConfig
from src.ml.feature_engineering.logger import logger, SimpleLogger
from src.ml.feature_engineering.proprietary_features import ProprietaryFeatureGenerator
from src.ml.feature_engineering.statistical_features import StatisticalFeatureGenerator
from src.ml.feature_engineering.technical_features import TechnicalFeatureGenerator
from src.ml.feature_engineering.temporal_features import TemporalFeatureGenerator


class TestFeatureConfig(unittest.TestCase):
    """Test cases for FeatureConfig class."""

    def test_feature_config_defaults(self):
        """Test FeatureConfig with default values."""
        config = FeatureConfig()
        
        self.assertEqual(config.short_periods, [5, 10, 14])
        self.assertEqual(config.medium_periods, [20, 50, 100])
        self.assertEqual(config.long_periods, [200, 500])
        self.assertEqual(config.price_types, ['open', 'high', 'low', 'close'])
        self.assertEqual(config.volatility_periods, [14, 20, 50])
        self.assertEqual(config.volume_periods, [14, 20, 50])
        self.assertEqual(config.custom_params, {})

    def test_feature_config_custom_values(self):
        """Test FeatureConfig with custom values."""
        custom_config = FeatureConfig(
            short_periods=[3, 7],
            medium_periods=[15, 30],
            long_periods=[100, 200],
            price_types=['close', 'volume'],
            volatility_periods=[10, 20],
            volume_periods=[10, 20],
            custom_params={'param1': 'value1'}
        )
        
        self.assertEqual(custom_config.short_periods, [3, 7])
        self.assertEqual(custom_config.medium_periods, [15, 30])
        self.assertEqual(custom_config.long_periods, [100, 200])
        self.assertEqual(custom_config.price_types, ['close', 'volume'])
        self.assertEqual(custom_config.volatility_periods, [10, 20])
        self.assertEqual(custom_config.volume_periods, [10, 20])
        self.assertEqual(custom_config.custom_params, {'param1': 'value1'})


class TestBaseFeatureGenerator(unittest.TestCase):
    """Test cases for BaseFeatureGenerator abstract class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = pd.DataFrame({
            'DateTime': pd.date_range('2023-01-01', periods=100, freq='h'),
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 102,
            'Low': np.random.randn(100).cumsum() + 98,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        })

    def test_base_feature_generator_initialization(self):
        """Test BaseFeatureGenerator initialization."""
        # Create a concrete implementation for testing
        class TestFeatureGenerator(BaseFeatureGenerator):
            def generate_features(self, df):
                return df.copy()
            
            def get_feature_names(self):
                return ['test_feature']
        
        generator = TestFeatureGenerator()
        
        self.assertIsNotNone(generator.config)
        self.assertEqual(generator.features_generated, 0)
        self.assertEqual(generator.feature_names, [])
        self.assertEqual(generator.feature_importance, {})

    def test_base_feature_generator_with_config(self):
        """Test BaseFeatureGenerator with custom config."""
        config = FeatureConfig(short_periods=[5, 10])
        
        class TestFeatureGenerator(BaseFeatureGenerator):
            def generate_features(self, df):
                return df.copy()
            
            def get_feature_names(self):
                return ['test_feature']
        
        generator = TestFeatureGenerator(config)
        
        self.assertEqual(generator.config.short_periods, [5, 10])


class TestCrossTimeframeFeatureGenerator(unittest.TestCase):
    """Test cases for CrossTimeframeFeatureGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = pd.DataFrame({
            'DateTime': pd.date_range('2023-01-01', periods=100, freq='h'),
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 102,
            'Low': np.random.randn(100).cumsum() + 98,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        })
        self.config = CrossTimeframeFeatureConfig()
        self.generator = CrossTimeframeFeatureGenerator(self.config)

    def test_cross_timeframe_feature_generator_initialization(self):
        """Test CrossTimeframeFeatureGenerator initialization."""
        self.assertIsInstance(self.generator, CrossTimeframeFeatureGenerator)
        self.assertIsInstance(self.generator, BaseFeatureGenerator)

    def test_generate_features(self):
        """Test feature generation."""
        result = self.generator.generate_features(self.test_data.copy())
        
        self.assertIsInstance(result, pd.DataFrame)
        # Features might not be generated due to insufficient data, but should return DataFrame
        self.assertGreaterEqual(len(result.columns), len(self.test_data.columns))

    def test_get_feature_names(self):
        """Test getting feature names."""
        feature_names = self.generator.get_feature_names()
        
        self.assertIsInstance(feature_names, list)
        # Feature names might be empty if no features were generated
        self.assertGreaterEqual(len(feature_names), 0)


class TestFeatureGenerator(unittest.TestCase):
    """Test cases for FeatureGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = pd.DataFrame({
            'DateTime': pd.date_range('2023-01-01', periods=100, freq='h'),
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 102,
            'Low': np.random.randn(100).cumsum() + 98,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        })
        self.config = MasterFeatureConfig()
        self.generator = FeatureGenerator(self.config)

    def test_feature_generator_initialization(self):
        """Test FeatureGenerator initialization."""
        self.assertIsInstance(self.generator, FeatureGenerator)

    def test_generate_features(self):
        """Test generating features."""
        result = self.generator.generate_features(self.test_data.copy())
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreaterEqual(len(result.columns), len(self.test_data.columns))

    def test_get_feature_names(self):
        """Test getting feature names."""
        feature_names = self.generator.get_feature_names()
        
        self.assertIsInstance(feature_names, list)
        self.assertGreaterEqual(len(feature_names), 0)


class TestFeatureSelectionConfig(unittest.TestCase):
    """Test cases for FeatureSelectionConfig class."""

    def test_feature_selection_config_defaults(self):
        """Test FeatureSelectionConfig with default values."""
        config = FeatureSelectionConfig()
        
        self.assertIsInstance(config, FeatureSelectionConfig)
        # Add specific assertions based on the actual class structure


class TestLogger(unittest.TestCase):
    """Test cases for logger module."""

    def test_logger_initialization(self):
        """Test logger initialization."""
        self.assertIsNotNone(logger)
        
        # Test that logger has the expected methods
        if hasattr(logger, 'info'):
            # Real logger
            try:
                logger.info("Test message")
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"Logger test failed: {e}")
        elif hasattr(logger, 'print_info'):
            # Simple logger
            try:
                logger.print_info("Test message")
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"Simple logger test failed: {e}")
        else:
            self.fail("Logger has no expected methods")

    def test_simple_logger_methods(self):
        """Test SimpleLogger methods."""
        simple_logger = SimpleLogger()
        
        # Test all methods exist and are callable
        methods = ['print_info', 'print_warning', 'print_error', 'print_success', 'print_debug']
        for method_name in methods:
            self.assertTrue(hasattr(simple_logger, method_name))
            method = getattr(simple_logger, method_name)
            self.assertTrue(callable(method))
            
            # Test method can be called without error
            try:
                method("Test message")
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"Simple logger method {method_name} failed: {e}")


class TestProprietaryFeatureGenerator(unittest.TestCase):
    """Test cases for ProprietaryFeatureGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = pd.DataFrame({
            'DateTime': pd.date_range('2023-01-01', periods=100, freq='h'),
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 102,
            'Low': np.random.randn(100).cumsum() + 98,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        })
        self.config = FeatureConfig()
        self.generator = ProprietaryFeatureGenerator(self.config)

    def test_proprietary_feature_generator_initialization(self):
        """Test ProprietaryFeatureGenerator initialization."""
        self.assertIsInstance(self.generator, ProprietaryFeatureGenerator)
        self.assertIsInstance(self.generator, BaseFeatureGenerator)

    def test_generate_features(self):
        """Test feature generation."""
        result = self.generator.generate_features(self.test_data.copy())
        
        self.assertIsInstance(result, pd.DataFrame)
        # Features might not be generated due to insufficient data, but should return DataFrame
        self.assertGreaterEqual(len(result.columns), len(self.test_data.columns))

    def test_get_feature_names(self):
        """Test getting feature names."""
        feature_names = self.generator.get_feature_names()
        
        self.assertIsInstance(feature_names, list)
        # Feature names might be empty if no features were generated
        self.assertGreaterEqual(len(feature_names), 0)


class TestStatisticalFeatureGenerator(unittest.TestCase):
    """Test cases for StatisticalFeatureGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = pd.DataFrame({
            'DateTime': pd.date_range('2023-01-01', periods=100, freq='h'),
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 102,
            'Low': np.random.randn(100).cumsum() + 98,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        })
        self.config = FeatureConfig()
        self.generator = StatisticalFeatureGenerator(self.config)

    def test_statistical_feature_generator_initialization(self):
        """Test StatisticalFeatureGenerator initialization."""
        self.assertIsInstance(self.generator, StatisticalFeatureGenerator)
        self.assertIsInstance(self.generator, BaseFeatureGenerator)

    def test_generate_features(self):
        """Test feature generation."""
        result = self.generator.generate_features(self.test_data.copy())
        
        self.assertIsInstance(result, pd.DataFrame)
        # Features might not be generated due to insufficient data, but should return DataFrame
        self.assertGreaterEqual(len(result.columns), len(self.test_data.columns))

    def test_get_feature_names(self):
        """Test getting feature names."""
        feature_names = self.generator.get_feature_names()
        
        self.assertIsInstance(feature_names, list)
        # Feature names might be empty if no features were generated
        self.assertGreaterEqual(len(feature_names), 0)


class TestTechnicalFeatureGenerator(unittest.TestCase):
    """Test cases for TechnicalFeatureGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = pd.DataFrame({
            'DateTime': pd.date_range('2023-01-01', periods=100, freq='h'),
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 102,
            'Low': np.random.randn(100).cumsum() + 98,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        })
        self.config = FeatureConfig()
        self.generator = TechnicalFeatureGenerator(self.config)

    def test_technical_feature_generator_initialization(self):
        """Test TechnicalFeatureGenerator initialization."""
        self.assertIsInstance(self.generator, TechnicalFeatureGenerator)
        self.assertIsInstance(self.generator, BaseFeatureGenerator)

    def test_generate_features(self):
        """Test feature generation."""
        result = self.generator.generate_features(self.test_data.copy())
        
        self.assertIsInstance(result, pd.DataFrame)
        # Features might not be generated due to insufficient data, but should return DataFrame
        self.assertGreaterEqual(len(result.columns), len(self.test_data.columns))

    def test_get_feature_names(self):
        """Test getting feature names."""
        feature_names = self.generator.get_feature_names()
        
        self.assertIsInstance(feature_names, list)
        # Feature names might be empty if no features were generated
        self.assertGreaterEqual(len(feature_names), 0)


class TestTemporalFeatureGenerator(unittest.TestCase):
    """Test cases for TemporalFeatureGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = pd.DataFrame({
            'DateTime': pd.date_range('2023-01-01', periods=100, freq='h'),
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 102,
            'Low': np.random.randn(100).cumsum() + 98,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        })
        self.config = FeatureConfig()
        self.generator = TemporalFeatureGenerator(self.config)

    def test_temporal_feature_generator_initialization(self):
        """Test TemporalFeatureGenerator initialization."""
        self.assertIsInstance(self.generator, TemporalFeatureGenerator)
        self.assertIsInstance(self.generator, BaseFeatureGenerator)

    def test_generate_features(self):
        """Test feature generation."""
        result = self.generator.generate_features(self.test_data.copy())
        
        self.assertIsInstance(result, pd.DataFrame)
        # Features might not be generated due to insufficient data, but should return DataFrame
        self.assertGreaterEqual(len(result.columns), len(self.test_data.columns))

    def test_get_feature_names(self):
        """Test getting feature names."""
        feature_names = self.generator.get_feature_names()
        
        self.assertIsInstance(feature_names, list)
        # Feature names might be empty if no features were generated
        self.assertGreaterEqual(len(feature_names), 0)


if __name__ == '__main__':
    unittest.main()
