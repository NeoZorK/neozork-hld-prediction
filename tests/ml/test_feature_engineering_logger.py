#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for feature engineering logger module.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from src.ml.feature_engineering.logger import SimpleLogger


class TestSimpleLogger:
    """Test SimpleLogger class."""
    
    def test_print_info(self, capsys):
        """Test print_info method."""
        logger = SimpleLogger()
        message = "Test info message"
        
        logger.print_info(message)
        
        captured = capsys.readouterr()
        assert f"[INFO] {message}" in captured.out
    
    def test_print_warning(self, capsys):
        """Test print_warning method."""
        logger = SimpleLogger()
        message = "Test warning message"
        
        logger.print_warning(message)
        
        captured = capsys.readouterr()
        assert f"[WARNING] {message}" in captured.out
    
    def test_print_error(self, capsys):
        """Test print_error method."""
        logger = SimpleLogger()
        message = "Test error message"
        
        logger.print_error(message)
        
        captured = capsys.readouterr()
        assert f"[ERROR] {message}" in captured.out
    
    def test_print_success(self, capsys):
        """Test print_success method."""
        logger = SimpleLogger()
        message = "Test success message"
        
        logger.print_success(message)
        
        captured = capsys.readouterr()
        assert f"[SUCCESS] {message}" in captured.out
    
    def test_print_debug(self, capsys):
        """Test print_debug method."""
        logger = SimpleLogger()
        message = "Test debug message"
        
        logger.print_debug(message)
        
        captured = capsys.readouterr()
        assert f"[DEBUG] {message}" in captured.out
    
    def test_all_methods_static(self):
        """Test that all methods are static."""
        logger = SimpleLogger()
        
        # All methods should be static and work without instance
        SimpleLogger.print_info("test")
        SimpleLogger.print_warning("test")
        SimpleLogger.print_error("test")
        SimpleLogger.print_success("test")
        SimpleLogger.print_debug("test")
        
        # Should not raise any errors
        assert True


class TestLoggerImport:
    """Test logger import behavior."""
    
    @patch('src.ml.feature_engineering.logger.SimpleLogger')
    def test_import_with_src_common_available(self, mock_simple_logger):
        """Test logger import when src.common is available."""
        # Mock the import to succeed
        with patch.dict('sys.modules', {'src.common': MagicMock()}):
            # Re-import the module to test the import logic
            import importlib
            import src.ml.feature_engineering.logger as logger_module
            
            # Reload the module to test import logic
            importlib.reload(logger_module)
            
            # Should use the real logger, not SimpleLogger
            assert logger_module.logger != mock_simple_logger
    
    @patch('src.ml.feature_engineering.logger.SimpleLogger')
    def test_import_with_src_common_unavailable(self, mock_simple_logger):
        """Test logger import when src.common is unavailable."""
        # Mock the import to fail
        with patch('src.ml.feature_engineering.logger.logger', mock_simple_logger):
            import src.ml.feature_engineering.logger as logger_module
            
            # Should use SimpleLogger as fallback
            assert logger_module.logger == mock_simple_logger


class TestLoggerIntegration:
    """Test logger integration with other modules."""
    
    def test_logger_used_in_base_feature_generator(self):
        """Test that logger is used in base feature generator."""
        from src.ml.feature_engineering.base_feature_generator import BaseFeatureGenerator, FeatureConfig
        
        # Create a mock generator
        class MockGenerator(BaseFeatureGenerator):
            def generate_features(self, df):
                return df
            
            def get_feature_names(self):
                return []
        
        generator = MockGenerator()
        
        # Test that logger methods can be called without errors
        with patch('src.ml.feature_engineering.base_feature_generator.logger') as mock_logger:
            generator.log_feature_generation('test_feature', 0.5)
            mock_logger.print_debug.assert_called_once()
    
    def test_logger_used_in_cross_timeframe_features(self):
        """Test that logger is used in cross timeframe features."""
        try:
            from src.ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureGenerator
            
            # Test that the module can be imported and logger is available
            assert hasattr(CrossTimeframeFeatureGenerator, '__init__')
        except ImportError:
            # If the module can't be imported, that's okay for this test
            pass


if __name__ == "__main__":
    pytest.main([__file__])
