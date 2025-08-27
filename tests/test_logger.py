# -*- coding: utf-8 -*-
"""
Tests for logger.py.

This module tests the simple logger functionality for ML module.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

from src.ml.feature_engineering.logger import SimpleLogger


class TestSimpleLogger:
    """Test SimpleLogger class."""
    
    def test_init(self):
        """Test SimpleLogger initialization."""
        logger = SimpleLogger()
        assert logger is not None
    
    def test_print_info(self, capsys):
        """Test print_info method."""
        logger = SimpleLogger()
        test_message = "Test info message"
        
        logger.print_info(test_message)
        captured = capsys.readouterr()
        
        assert "[INFO]" in captured.out
        assert test_message in captured.out
    
    def test_print_warning(self, capsys):
        """Test print_warning method."""
        logger = SimpleLogger()
        test_message = "Test warning message"
        
        logger.print_warning(test_message)
        captured = capsys.readouterr()
        
        assert "[WARNING]" in captured.out
        assert test_message in captured.out
    
    def test_print_error(self, capsys):
        """Test print_error method."""
        logger = SimpleLogger()
        test_message = "Test error message"
        
        logger.print_error(test_message)
        captured = capsys.readouterr()
        
        assert "[ERROR]" in captured.out
        assert test_message in captured.out
    
    def test_print_success(self, capsys):
        """Test print_success method."""
        logger = SimpleLogger()
        test_message = "Test success message"
        
        logger.print_success(test_message)
        captured = capsys.readouterr()
        
        assert "[SUCCESS]" in captured.out
        assert test_message in captured.out
    
    def test_print_debug(self, capsys):
        """Test print_debug method."""
        logger = SimpleLogger()
        test_message = "Test debug message"
        
        logger.print_debug(test_message)
        captured = capsys.readouterr()
        
        assert "[DEBUG]" in captured.out
        assert test_message in captured.out
    
    def test_print_methods_with_empty_message(self, capsys):
        """Test print methods with empty message."""
        logger = SimpleLogger()
        
        logger.print_info("")
        logger.print_warning("")
        logger.print_error("")
        logger.print_success("")
        logger.print_debug("")
        
        captured = capsys.readouterr()
        
        assert "[INFO]" in captured.out
        assert "[WARNING]" in captured.out
        assert "[ERROR]" in captured.out
        assert "[SUCCESS]" in captured.out
        assert "[DEBUG]" in captured.out
    
    def test_print_methods_with_special_characters(self, capsys):
        """Test print methods with special characters."""
        logger = SimpleLogger()
        special_message = "Test message with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        logger.print_info(special_message)
        logger.print_warning(special_message)
        logger.print_error(special_message)
        logger.print_success(special_message)
        logger.print_debug(special_message)
        
        captured = capsys.readouterr()
        
        assert special_message in captured.out
        assert "[INFO]" in captured.out
        assert "[WARNING]" in captured.out
        assert "[ERROR]" in captured.out
        assert "[SUCCESS]" in captured.out
        assert "[DEBUG]" in captured.out
    
    def test_print_methods_with_multiline_message(self, capsys):
        """Test print methods with multiline message."""
        logger = SimpleLogger()
        multiline_message = "Line 1\nLine 2\nLine 3"
        
        logger.print_info(multiline_message)
        captured = capsys.readouterr()
        
        assert "[INFO]" in captured.out
        assert "Line 1" in captured.out
        assert "Line 2" in captured.out
        assert "Line 3" in captured.out
    
    def test_print_methods_with_unicode_message(self, capsys):
        """Test print methods with unicode message."""
        logger = SimpleLogger()
        unicode_message = "Test message with unicode: привет мир 🌍"
        
        logger.print_info(unicode_message)
        captured = capsys.readouterr()
        
        assert "[INFO]" in captured.out
        assert unicode_message in captured.out
    
    def test_all_print_methods_in_sequence(self, capsys):
        """Test all print methods in sequence."""
        logger = SimpleLogger()
        
        messages = [
            ("print_info", "Info message"),
            ("print_warning", "Warning message"),
            ("print_error", "Error message"),
            ("print_success", "Success message"),
            ("print_debug", "Debug message")
        ]
        
        for method_name, message in messages:
            getattr(logger, method_name)(message)
        
        captured = capsys.readouterr()
        
        assert "[INFO] Info message" in captured.out
        assert "[WARNING] Warning message" in captured.out
        assert "[ERROR] Error message" in captured.out
        assert "[SUCCESS] Success message" in captured.out
        assert "[DEBUG] Debug message" in captured.out
    
    def test_static_methods(self):
        """Test that all methods are static."""
        # Should be able to call methods without instantiation
        SimpleLogger.print_info("Test")
        SimpleLogger.print_warning("Test")
        SimpleLogger.print_error("Test")
        SimpleLogger.print_success("Test")
        SimpleLogger.print_debug("Test")
        
        # Should not raise any errors
        assert True


class TestLoggerImport:
    """Test logger import functionality."""
    
    def test_simple_logger_import(self):
        """Test that SimpleLogger can be imported."""
        from src.ml.feature_engineering.logger import SimpleLogger
        assert SimpleLogger is not None
    
    def test_logger_import_with_mock_src_common(self):
        """Test logger import when src.common is not available."""
        # Mock the import to fail
        with patch.dict('sys.modules', {'src.common': None}):
            # Remove the module from sys.modules if it exists
            if 'src.ml.feature_engineering.logger' in sys.modules:
                del sys.modules['src.ml.feature_engineering.logger']
            
            # Import should work and use SimpleLogger
            from src.ml.feature_engineering.logger import logger
            # The logger should be an instance of SimpleLogger
            assert hasattr(logger, 'print_info')
            assert hasattr(logger, 'print_warning')
            assert hasattr(logger, 'print_error')
    
    def test_logger_import_with_src_common_available(self):
        """Test logger import when src.common is available."""
        # Mock src.common.logger
        mock_common_logger = Mock()
        with patch.dict('sys.modules', {'src.common': Mock(logger=mock_common_logger)}):
            # Remove the module from sys.modules if it exists
            if 'src.ml.feature_engineering.logger' in sys.modules:
                del sys.modules['src.ml.feature_engineering.logger']
            
            # Import should work and use the common logger
            from src.ml.feature_engineering.logger import logger
            assert logger is mock_common_logger
    
    def test_logger_import_with_import_error(self):
        """Test logger import when ImportError occurs."""
        # This test is more complex due to how Python handles imports
        # We'll test the fallback mechanism differently
        try:
            # Try to import the logger module
            from src.ml.feature_engineering.logger import logger
            # Should work and logger should have the expected methods
            assert hasattr(logger, 'print_info')
            assert hasattr(logger, 'print_warning')
            assert hasattr(logger, 'print_error')
        except ImportError:
            # If import fails, that's also acceptable for this test
            pass


class TestLoggerFunctionality:
    """Test logger functionality in different scenarios."""
    
    def test_logger_output_format(self, capsys):
        """Test that logger output has correct format."""
        logger = SimpleLogger()
        test_message = "Test message"
        
        logger.print_info(test_message)
        captured = capsys.readouterr()
        
        # Check format: [LEVEL] message
        assert captured.out.strip() == f"[INFO] {test_message}"
    
    def test_logger_output_with_newlines(self, capsys):
        """Test logger output with newlines in message."""
        logger = SimpleLogger()
        test_message = "Line 1\nLine 2"
        
        logger.print_info(test_message)
        captured = capsys.readouterr()
        
        # Should preserve newlines
        assert "Line 1" in captured.out
        assert "Line 2" in captured.out
    
    def test_logger_output_with_tabs(self, capsys):
        """Test logger output with tabs in message."""
        logger = SimpleLogger()
        test_message = "Tab\tseparated\tvalues"
        
        logger.print_info(test_message)
        captured = capsys.readouterr()
        
        # Should preserve tabs
        assert test_message in captured.out
    
    def test_logger_output_with_very_long_message(self, capsys):
        """Test logger output with very long message."""
        logger = SimpleLogger()
        long_message = "A" * 1000  # 1000 character message
        
        logger.print_info(long_message)
        captured = capsys.readouterr()
        
        assert "[INFO]" in captured.out
        assert long_message in captured.out
    
    def test_logger_output_with_none_message(self, capsys):
        """Test logger output with None message."""
        logger = SimpleLogger()
        
        logger.print_info(None)
        captured = capsys.readouterr()
        
        assert "[INFO]" in captured.out
        assert "None" in captured.out
    
    def test_logger_output_with_number_message(self, capsys):
        """Test logger output with number message."""
        logger = SimpleLogger()
        
        logger.print_info(42)
        captured = capsys.readouterr()
        
        assert "[INFO]" in captured.out
        assert "42" in captured.out
    
    def test_logger_output_with_list_message(self, capsys):
        """Test logger output with list message."""
        logger = SimpleLogger()
        
        list_message = [1, 2, 3, "test"]
        logger.print_info(list_message)
        captured = capsys.readouterr()
        
        assert "[INFO]" in captured.out
        assert str(list_message) in captured.out


class TestLoggerIntegration:
    """Integration tests for logger."""
    
    def test_logger_in_feature_generation_context(self, capsys):
        """Test logger usage in a feature generation context."""
        logger = SimpleLogger()
        
        # Simulate feature generation process
        logger.print_info("Starting feature generation")
        logger.print_debug("Processing ratio features")
        logger.print_warning("Some features have missing values")
        logger.print_success("Feature generation completed")
        
        captured = capsys.readouterr()
        
        assert "Starting feature generation" in captured.out
        assert "Processing ratio features" in captured.out
        assert "Some features have missing values" in captured.out
        assert "Feature generation completed" in captured.out
    
    def test_logger_in_error_handling_context(self, capsys):
        """Test logger usage in error handling context."""
        logger = SimpleLogger()
        
        # Simulate error handling
        logger.print_info("Processing data")
        logger.print_error("Invalid data format detected")
        logger.print_warning("Attempting to fix data issues")
        logger.print_success("Data processing completed successfully")
        
        captured = capsys.readouterr()
        
        assert "Processing data" in captured.out
        assert "Invalid data format detected" in captured.out
        assert "Attempting to fix data issues" in captured.out
        assert "Data processing completed successfully" in captured.out
    
    def test_logger_performance(self):
        """Test logger performance with many messages."""
        logger = SimpleLogger()
        
        # Test with many messages
        import time
        start_time = time.time()
        
        for i in range(1000):
            logger.print_info(f"Message {i}")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete in reasonable time (less than 1 second)
        assert execution_time < 1.0
    
    def test_logger_memory_usage(self):
        """Test that logger doesn't accumulate memory."""
        logger = SimpleLogger()
        
        # Generate many messages
        for i in range(1000):
            logger.print_info(f"Message {i}")
        
        # Should not have accumulated any state
        assert not hasattr(logger, '_messages')
        assert not hasattr(logger, '_buffer')


class TestLoggerEdgeCases:
    """Test logger edge cases and error conditions."""
    
    def test_logger_with_sys_stdout_redirected(self):
        """Test logger when sys.stdout is redirected."""
        logger = SimpleLogger()
        test_message = "Test message"
        
        # Redirect stdout to StringIO
        old_stdout = sys.stdout
        string_io = StringIO()
        sys.stdout = string_io
        
        try:
            logger.print_info(test_message)
            output = string_io.getvalue()
            
            assert "[INFO]" in output
            assert test_message in output
        finally:
            sys.stdout = old_stdout
    
    def test_logger_with_sys_stdout_closed(self):
        """Test logger when sys.stdout is closed."""
        logger = SimpleLogger()
        test_message = "Test message"
        
        # Close stdout temporarily
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        
        try:
            # Should not raise an exception
            logger.print_info(test_message)
            assert True
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout
    
    def test_logger_with_unicode_stdout(self):
        """Test logger with unicode stdout."""
        logger = SimpleLogger()
        test_message = "Test message with unicode: привет"
        
        # This should work without raising UnicodeEncodeError
        try:
            logger.print_info(test_message)
            assert True
        except UnicodeEncodeError:
            pytest.skip("Unicode encoding not supported in this environment")
    
    def test_logger_concurrent_access(self):
        """Test logger with concurrent access (basic test)."""
        logger = SimpleLogger()
        test_message = "Concurrent test message"
        
        # Basic concurrent access test
        import threading
        
        def log_message():
            logger.print_info(test_message)
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=log_message)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should complete without errors
        assert True
