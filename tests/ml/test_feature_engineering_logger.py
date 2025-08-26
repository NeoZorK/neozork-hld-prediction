#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for src/ml/feature_engineering/logger.py

This module provides comprehensive test coverage for the logger module.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock, call
from io import StringIO


class TestSimpleLogger:
    """Test cases for SimpleLogger class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        from src.ml.feature_engineering.logger import SimpleLogger
        self.logger = SimpleLogger()
    
    def test_print_info(self):
        """Test print_info method."""
        with patch('builtins.print') as mock_print:
            self.logger.print_info("Test info message")
            mock_print.assert_called_once_with("[INFO] Test info message")
    
    def test_print_warning(self):
        """Test print_warning method."""
        with patch('builtins.print') as mock_print:
            self.logger.print_warning("Test warning message")
            mock_print.assert_called_once_with("[WARNING] Test warning message")
    
    def test_print_error(self):
        """Test print_error method."""
        with patch('builtins.print') as mock_print:
            self.logger.print_error("Test error message")
            mock_print.assert_called_once_with("[ERROR] Test error message")
    
    def test_print_success(self):
        """Test print_success method."""
        with patch('builtins.print') as mock_print:
            self.logger.print_success("Test success message")
            mock_print.assert_called_once_with("[SUCCESS] Test success message")
    
    def test_print_debug(self):
        """Test print_debug method."""
        with patch('builtins.print') as mock_print:
            self.logger.print_debug("Test debug message")
            mock_print.assert_called_once_with("[DEBUG] Test debug message")
    
    def test_all_methods_static(self):
        """Test that all methods are static."""
        import inspect
        
        methods = [
            self.logger.print_info,
            self.logger.print_warning,
            self.logger.print_error,
            self.logger.print_success,
            self.logger.print_debug
        ]
        
        for method in methods:
            assert inspect.isfunction(method), f"Method {method.__name__} should be static"


class TestLoggerIntegration:
    """Integration tests for logger functionality."""
    
    def test_logger_output_capture(self):
        """Test that logger output can be captured."""
        from src.ml.feature_engineering.logger import SimpleLogger
        
        logger = SimpleLogger()
        
        # Capture stdout
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            logger.print_info("Integration test message")
        
        assert "[INFO] Integration test message" in captured_output.getvalue()
    
    def test_logger_multiple_messages(self):
        """Test multiple logger messages."""
        from src.ml.feature_engineering.logger import SimpleLogger
        
        logger = SimpleLogger()
        
        with patch('builtins.print') as mock_print:
            logger.print_info("Message 1")
            logger.print_warning("Message 2")
            logger.print_error("Message 3")
            logger.print_success("Message 4")
            logger.print_debug("Message 5")
        
        # Check that all calls were made
        assert mock_print.call_count == 5
        
        # Check specific calls
        calls = mock_print.call_args_list
        assert calls[0] == call("[INFO] Message 1")
        assert calls[1] == call("[WARNING] Message 2")
        assert calls[2] == call("[ERROR] Message 3")
        assert calls[3] == call("[SUCCESS] Message 4")
        assert calls[4] == call("[DEBUG] Message 5")
    
    def test_logger_empty_messages(self):
        """Test logger with empty messages."""
        from src.ml.feature_engineering.logger import SimpleLogger
        
        logger = SimpleLogger()
        
        with patch('builtins.print') as mock_print:
            logger.print_info("")
            logger.print_warning("")
            logger.print_error("")
            logger.print_success("")
            logger.print_debug("")
        
        # Check that all calls were made
        assert mock_print.call_count == 5
        
        # Check specific calls
        calls = mock_print.call_args_list
        assert calls[0] == call("[INFO] ")
        assert calls[1] == call("[WARNING] ")
        assert calls[2] == call("[ERROR] ")
        assert calls[3] == call("[SUCCESS] ")
        assert calls[4] == call("[DEBUG] ")


if __name__ == '__main__':
    pytest.main([__file__])
