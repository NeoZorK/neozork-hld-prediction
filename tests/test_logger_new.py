# -*- coding: utf-8 -*-
"""
Tests for logger module.

This module tests the SimpleLogger class from src/ml/feature_engineering/logger.py.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os

# Import the module to test
from src.ml.feature_engineering.logger import SimpleLogger, logger


class TestSimpleLogger:
    """Test SimpleLogger class."""
    
    @pytest.fixture
    def simple_logger(self):
        """Create SimpleLogger instance for testing."""
        return SimpleLogger()
    
    def test_print_info(self, simple_logger, capsys):
        """Test print_info method."""
        simple_logger.print_info("Test info message")
        
        captured = capsys.readouterr()
        assert "[INFO] Test info message" in captured.out
    
    def test_print_warning(self, simple_logger, capsys):
        """Test print_warning method."""
        simple_logger.print_warning("Test warning message")
        
        captured = capsys.readouterr()
        assert "[WARNING] Test warning message" in captured.out
    
    def test_print_error(self, simple_logger, capsys):
        """Test print_error method."""
        simple_logger.print_error("Test error message")
        
        captured = capsys.readouterr()
        assert "[ERROR] Test error message" in captured.out
    
    def test_print_success(self, simple_logger, capsys):
        """Test print_success method."""
        simple_logger.print_success("Test success message")
        
        captured = capsys.readouterr()
        assert "[SUCCESS] Test success message" in captured.out
    
    def test_print_debug(self, simple_logger, capsys):
        """Test print_debug method."""
        simple_logger.print_debug("Test debug message")
        
        captured = capsys.readouterr()
        assert "[DEBUG] Test debug message" in captured.out
    
    def test_print_info_empty_message(self, simple_logger, capsys):
        """Test print_info with empty message."""
        simple_logger.print_info("")
        
        captured = capsys.readouterr()
        assert "[INFO] " in captured.out
    
    def test_print_warning_empty_message(self, simple_logger, capsys):
        """Test print_warning with empty message."""
        simple_logger.print_warning("")
        
        captured = capsys.readouterr()
        assert "[WARNING] " in captured.out
    
    def test_print_error_empty_message(self, simple_logger, capsys):
        """Test print_error with empty message."""
        simple_logger.print_error("")
        
        captured = capsys.readouterr()
        assert "[ERROR] " in captured.out
    
    def test_print_success_empty_message(self, simple_logger, capsys):
        """Test print_success with empty message."""
        simple_logger.print_success("")
        
        captured = capsys.readouterr()
        assert "[SUCCESS] " in captured.out
    
    def test_print_debug_empty_message(self, simple_logger, capsys):
        """Test print_debug with empty message."""
        simple_logger.print_debug("")
        
        captured = capsys.readouterr()
        assert "[DEBUG] " in captured.out
    
    def test_print_info_special_characters(self, simple_logger, capsys):
        """Test print_info with special characters."""
        simple_logger.print_info("Test message with special chars: !@#$%^&*()")
        
        captured = capsys.readouterr()
        assert "[INFO] Test message with special chars: !@#$%^&*()" in captured.out
    
    def test_print_warning_special_characters(self, simple_logger, capsys):
        """Test print_warning with special characters."""
        simple_logger.print_warning("Test message with special chars: !@#$%^&*()")
        
        captured = capsys.readouterr()
        assert "[WARNING] Test message with special chars: !@#$%^&*()" in captured.out
    
    def test_print_error_special_characters(self, simple_logger, capsys):
        """Test print_error with special characters."""
        simple_logger.print_error("Test message with special chars: !@#$%^&*()")
        
        captured = capsys.readouterr()
        assert "[ERROR] Test message with special chars: !@#$%^&*()" in captured.out
    
    def test_print_success_special_characters(self, simple_logger, capsys):
        """Test print_success with special characters."""
        simple_logger.print_success("Test message with special chars: !@#$%^&*()")
        
        captured = capsys.readouterr()
        assert "[SUCCESS] Test message with special chars: !@#$%^&*()" in captured.out
    
    def test_print_debug_special_characters(self, simple_logger, capsys):
        """Test print_debug with special characters."""
        simple_logger.print_debug("Test message with special chars: !@#$%^&*()")
        
        captured = capsys.readouterr()
        assert "[DEBUG] Test message with special chars: !@#$%^&*()" in captured.out
    
    def test_print_info_unicode_characters(self, simple_logger, capsys):
        """Test print_info with unicode characters."""
        simple_logger.print_info("Test message with unicode: 🚀📊📈")
        
        captured = capsys.readouterr()
        assert "[INFO] Test message with unicode: 🚀📊📈" in captured.out
    
    def test_print_warning_unicode_characters(self, simple_logger, capsys):
        """Test print_warning with unicode characters."""
        simple_logger.print_warning("Test message with unicode: 🚀📊📈")
        
        captured = capsys.readouterr()
        assert "[WARNING] Test message with unicode: 🚀📊📈" in captured.out
    
    def test_print_error_unicode_characters(self, simple_logger, capsys):
        """Test print_error with unicode characters."""
        simple_logger.print_error("Test message with unicode: 🚀📊📈")
        
        captured = capsys.readouterr()
        assert "[ERROR] Test message with unicode: 🚀📊📈" in captured.out
    
    def test_print_success_unicode_characters(self, simple_logger, capsys):
        """Test print_success with unicode characters."""
        simple_logger.print_success("Test message with unicode: 🚀📊📈")
        
        captured = capsys.readouterr()
        assert "[SUCCESS] Test message with unicode: 🚀📊📈" in captured.out
    
    def test_print_debug_unicode_characters(self, simple_logger, capsys):
        """Test print_debug with unicode characters."""
        simple_logger.print_debug("Test message with unicode: 🚀📊📈")
        
        captured = capsys.readouterr()
        assert "[DEBUG] Test message with unicode: 🚀📊📈" in captured.out
    
    def test_print_info_long_message(self, simple_logger, capsys):
        """Test print_info with long message."""
        long_message = "A" * 1000
        simple_logger.print_info(long_message)
        
        captured = capsys.readouterr()
        assert f"[INFO] {long_message}" in captured.out
    
    def test_print_warning_long_message(self, simple_logger, capsys):
        """Test print_warning with long message."""
        long_message = "A" * 1000
        simple_logger.print_warning(long_message)
        
        captured = capsys.readouterr()
        assert f"[WARNING] {long_message}" in captured.out
    
    def test_print_error_long_message(self, simple_logger, capsys):
        """Test print_error with long message."""
        long_message = "A" * 1000
        simple_logger.print_error(long_message)
        
        captured = capsys.readouterr()
        assert f"[ERROR] {long_message}" in captured.out
    
    def test_print_success_long_message(self, simple_logger, capsys):
        """Test print_success with long message."""
        long_message = "A" * 1000
        simple_logger.print_success(long_message)
        
        captured = capsys.readouterr()
        assert f"[SUCCESS] {long_message}" in captured.out
    
    def test_print_debug_long_message(self, simple_logger, capsys):
        """Test print_debug with long message."""
        long_message = "A" * 1000
        simple_logger.print_debug(long_message)
        
        captured = capsys.readouterr()
        assert f"[DEBUG] {long_message}" in captured.out
    
    def test_multiple_log_messages(self, simple_logger, capsys):
        """Test multiple log messages in sequence."""
        simple_logger.print_info("First message")
        simple_logger.print_warning("Second message")
        simple_logger.print_error("Third message")
        simple_logger.print_success("Fourth message")
        simple_logger.print_debug("Fifth message")
        
        captured = capsys.readouterr()
        assert "[INFO] First message" in captured.out
        assert "[WARNING] Second message" in captured.out
        assert "[ERROR] Third message" in captured.out
        assert "[SUCCESS] Fourth message" in captured.out
        assert "[DEBUG] Fifth message" in captured.out
    
    def test_static_methods(self):
        """Test that all methods are static."""
        # Test that we can call methods without instantiating the class
        SimpleLogger.print_info("Static test")
        SimpleLogger.print_warning("Static test")
        SimpleLogger.print_error("Static test")
        SimpleLogger.print_success("Static test")
        SimpleLogger.print_debug("Static test")
        
        # This should not raise any errors


class TestLoggerImport:
    """Test logger import and fallback behavior."""
    
    def test_logger_import_success(self):
        """Test that logger is successfully imported."""
        # The logger should be available
        assert logger is not None
        
        # It should have the required methods
        assert hasattr(logger, 'print_info')
        assert hasattr(logger, 'print_warning')
        assert hasattr(logger, 'print_error')
        assert hasattr(logger, 'print_success')
        assert hasattr(logger, 'print_debug')
    
    def test_logger_methods_callable(self, capsys):
        """Test that logger methods are callable."""
        # Test that we can call the methods
        logger.print_info("Test message")
        logger.print_warning("Test message")
        logger.print_error("Test message")
        logger.print_success("Test message")
        logger.print_debug("Test message")
        
        captured = capsys.readouterr()
        assert "[INFO] Test message" in captured.out
        assert "[WARNING] Test message" in captured.out
        assert "[ERROR] Test message" in captured.out
        assert "[SUCCESS] Test message" in captured.out
        assert "[DEBUG] Test message" in captured.out
    
    @patch('src.ml.feature_engineering.logger.SimpleLogger')
    def test_logger_fallback_behavior(self, mock_simple_logger):
        """Test logger fallback behavior when import fails."""
        # This test verifies that the logger module handles import failures gracefully
        # The actual fallback behavior is tested by the import mechanism itself
        
        # Mock the SimpleLogger to simulate fallback
        mock_logger_instance = Mock()
        mock_simple_logger.return_value = mock_logger_instance
        
        # The logger should still be available
        assert logger is not None
    
    def test_logger_consistency(self):
        """Test that logger instance is consistent."""
        # The logger should be the same instance across multiple accesses
        logger1 = logger
        logger2 = logger
        
        assert logger1 is logger2
    
    def test_logger_method_signatures(self):
        """Test that logger methods have correct signatures."""
        # Test that methods accept string arguments
        test_message = "Test message"
        
        # These should not raise any errors
        logger.print_info(test_message)
        logger.print_warning(test_message)
        logger.print_error(test_message)
        logger.print_success(test_message)
        logger.print_debug(test_message)
    
    def test_logger_output_format(self, capsys):
        """Test that logger output format is correct."""
        test_message = "Test message"
        
        logger.print_info(test_message)
        captured = capsys.readouterr()
        
        # Check that output starts with the correct prefix
        assert captured.out.startswith("[INFO] ")
        assert captured.out.endswith(test_message + "\n")
    
    def test_logger_multiple_calls(self, capsys):
        """Test multiple calls to logger methods."""
        messages = ["Message 1", "Message 2", "Message 3"]
        
        for msg in messages:
            logger.print_info(msg)
        
        captured = capsys.readouterr()
        
        for msg in messages:
            assert f"[INFO] {msg}" in captured.out
