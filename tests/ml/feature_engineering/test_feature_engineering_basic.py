"""
Basic tests for feature engineering modules.

This module provides basic tests that work with the actual interfaces
of the feature engineering modules.
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# Import the modules we want to test
from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator, FeatureConfig
from src.ml.feature_engineering.logger import SimpleLogger


class TestBaseFeatureGeneratorBasic(unittest.TestCase):
    """Basic tests for BaseFeatureGenerator."""
    
    def setUp(self):
        """Set up test data."""
        self.config = FeatureConfig()
        
        # Create sample OHLCV data
        self.sample_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
    
    def test_feature_config_initialization(self):
        """Test FeatureConfig initialization."""
        config = FeatureConfig()
        self.assertIsNotNone(config.short_periods)
        self.assertIsNotNone(config.medium_periods)
        self.assertIsNotNone(config.long_periods)
        self.assertIsNotNone(config.price_types)
    
    def test_feature_config_custom_values(self):
        """Test FeatureConfig with custom values."""
        config = FeatureConfig(
            short_periods=[5, 10],
            medium_periods=[20, 50],
            long_periods=[100],
            price_types=['close']
        )
        self.assertEqual(config.short_periods, [5, 10])
        self.assertEqual(config.medium_periods, [20, 50])
        self.assertEqual(config.long_periods, [100])
        self.assertEqual(config.price_types, ['close'])


class TestSimpleLoggerBasic(unittest.TestCase):
    """Basic tests for SimpleLogger."""
    
    def setUp(self):
        """Set up test environment."""
        self.logger = SimpleLogger()
    
    @patch('sys.stdout')
    def test_print_info(self, mock_stdout):
        """Test print_info method."""
        message = "Test info message"
        self.logger.print_info(message)
        mock_stdout.write.assert_called()
    
    @patch('sys.stdout')
    def test_print_warning(self, mock_stdout):
        """Test print_warning method."""
        message = "Test warning message"
        self.logger.print_warning(message)
        mock_stdout.write.assert_called()
    
    @patch('sys.stdout')
    def test_print_error(self, mock_stdout):
        """Test print_error method."""
        message = "Test error message"
        self.logger.print_error(message)
        mock_stdout.write.assert_called()
    
    @patch('sys.stdout')
    def test_print_success(self, mock_stdout):
        """Test print_success method."""
        message = "Test success message"
        self.logger.print_success(message)
        mock_stdout.write.assert_called()
    
    @patch('sys.stdout')
    def test_print_debug(self, mock_stdout):
        """Test print_debug method."""
        message = "Test debug message"
        self.logger.print_debug(message)
        mock_stdout.write.assert_called()


class TestFeatureEngineeringImports(unittest.TestCase):
    """Test that all feature engineering modules can be imported."""
    
    def test_import_base_feature_generator(self):
        """Test importing base_feature_generator."""
        try:
            from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator, FeatureConfig
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import base_feature_generator: {e}")
    
    def test_import_logger(self):
        """Test importing logger."""
        try:
            from src.ml.feature_engineering.logger import SimpleLogger
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import logger: {e}")
    
    def test_import_feature_generator(self):
        """Test importing feature_generator."""
        try:
            from src.ml.feature_engineering.feature_generator import FeatureGenerator, MasterFeatureConfig
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import feature_generator: {e}")
    
    def test_import_feature_selector(self):
        """Test importing feature_selector."""
        try:
            from src.ml.feature_engineering.feature_selector import FeatureSelector, FeatureSelectionConfig
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import feature_selector: {e}")
    
    def test_import_proprietary_features(self):
        """Test importing proprietary_features."""
        try:
            from src.ml.feature_engineering.proprietary_features import ProprietaryFeatureGenerator, ProprietaryFeatureConfig
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import proprietary_features: {e}")
    
    def test_import_statistical_features(self):
        """Test importing statistical_features."""
        try:
            from src.ml.feature_engineering.statistical_features import StatisticalFeatureGenerator, StatisticalFeatureConfig
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import statistical_features: {e}")
    
    def test_import_technical_features(self):
        """Test importing technical_features."""
        try:
            from src.ml.feature_engineering.technical_features import TechnicalFeatureGenerator, TechnicalFeatureConfig
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import technical_features: {e}")
    
    def test_import_temporal_features(self):
        """Test importing temporal_features."""
        try:
            from src.ml.feature_engineering.temporal_features import TemporalFeatureGenerator, TemporalFeatureConfig
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import temporal_features: {e}")
    
    def test_import_cross_timeframe_features(self):
        """Test importing cross_timeframe_features."""
        try:
            from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator, CrossTimeframeFeatureConfig
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import cross_timeframe_features: {e}")


class TestFeatureEngineeringClasses(unittest.TestCase):
    """Test that feature engineering classes can be instantiated."""
    
    def test_base_feature_generator_instantiation(self):
        """Test BaseFeatureGenerator instantiation."""
        try:
            # This should raise TypeError since it's abstract
            with self.assertRaises(TypeError):
                BaseFeatureGenerator()
        except Exception as e:
            self.fail(f"Unexpected error: {e}")
    
    def test_feature_config_instantiation(self):
        """Test FeatureConfig instantiation."""
        try:
            config = FeatureConfig()
            self.assertIsInstance(config, FeatureConfig)
        except Exception as e:
            self.fail(f"Failed to instantiate FeatureConfig: {e}")
    
    def test_simple_logger_instantiation(self):
        """Test SimpleLogger instantiation."""
        try:
            logger = SimpleLogger()
            self.assertIsInstance(logger, SimpleLogger)
        except Exception as e:
            self.fail(f"Failed to instantiate SimpleLogger: {e}")


if __name__ == '__main__':
    unittest.main()
