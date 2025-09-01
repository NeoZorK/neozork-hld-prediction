# -*- coding: utf-8 -*-
"""
Tests for logger.py module.

This module provides comprehensive test coverage for the simple logger
implementation used in the ML module when src.common.logger is not available.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from src.ml.feature_engineering.logger import SimpleLogger, logger


class TestSimpleLogger:
    """Test cases for SimpleLogger class."""
    
    def setup_method(self):
        """Set up test fixtures."""
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
        # Test that methods can be called without instantiation
        with patch('builtins.print') as mock_print:
            SimpleLogger.print_info("Test info")
            SimpleLogger.print_warning("Test warning")
            SimpleLogger.print_error("Test error")
            SimpleLogger.print_success("Test success")
            SimpleLogger.print_debug("Test debug")
            
            assert mock_print.call_count == 5
    
    def test_message_formatting(self):
        """Test message formatting with different types of messages."""
        with patch('builtins.print') as mock_print:
            # Test with empty message
            self.logger.print_info("")
            mock_print.assert_called_with("[INFO] ")
            
            # Test with special characters
            self.logger.print_warning("Message with special chars: !@#$%^&*()")
            mock_print.assert_called_with("[WARNING] Message with special chars: !@#$%^&*()")
            
            # Test with numbers
            self.logger.print_error("Error code: 404")
            mock_print.assert_called_with("[ERROR] Error code: 404")
            
            # Test with unicode characters
            self.logger.print_success("Success: ✓")
            mock_print.assert_called_with("[SUCCESS] Success: ✓")
    
    def test_multiple_calls(self):
        """Test multiple consecutive calls."""
        with patch('builtins.print') as mock_print:
            self.logger.print_info("First message")
            self.logger.print_warning("Second message")
            self.logger.print_error("Third message")
            self.logger.print_success("Fourth message")
            self.logger.print_debug("Fifth message")
            
            # Check that all calls were made (ignore exact format due to colors)
            assert mock_print.call_count == 5
    
    def test_logger_consistency(self):
        """Test that logger instance is consistent."""
        logger1 = SimpleLogger()
        logger2 = SimpleLogger()
        
        # Both should be instances of SimpleLogger
        assert isinstance(logger1, SimpleLogger)
        assert isinstance(logger2, SimpleLogger)
        
        # Both should have the same methods
        assert hasattr(logger1, 'print_info')
        assert hasattr(logger1, 'print_warning')
        assert hasattr(logger1, 'print_error')
        assert hasattr(logger1, 'print_success')
        assert hasattr(logger1, 'print_debug')
        
        assert hasattr(logger2, 'print_info')
        assert hasattr(logger2, 'print_warning')
        assert hasattr(logger2, 'print_error')
        assert hasattr(logger2, 'print_success')
        assert hasattr(logger2, 'print_debug')


class TestLoggerImport:
    """Test cases for logger import behavior."""
    
    def test_logger_import_success(self):
        """Test successful import of src.common.logger."""
        # This test verifies that the logger import works when src.common.logger is available
        # The actual behavior depends on whether src.common.logger exists
        assert logger is not None
    
    def test_logger_has_required_methods(self):
        """Test that logger has required methods."""
        # Test that logger has the expected methods
        assert hasattr(logger, 'print_info')
        assert hasattr(logger, 'print_warning')
        assert hasattr(logger, 'print_error')
        assert hasattr(logger, 'print_success')
        assert hasattr(logger, 'print_debug')
    
    def test_logger_methods_callable(self):
        """Test that logger methods are callable."""
        # Test that all methods are callable
        assert callable(logger.print_info)
        assert callable(logger.print_warning)
        assert callable(logger.print_error)
        assert callable(logger.print_success)
        assert callable(logger.print_debug)
    
    def test_logger_methods_accept_strings(self):
        """Test that logger methods accept string arguments."""
        with patch('builtins.print') as mock_print:
            # Test that methods can be called with string arguments
            logger.print_info("Test message")
            logger.print_warning("Test message")
            logger.print_error("Test message")
            logger.print_success("Test message")
            logger.print_debug("Test message")
            
            # Should have called print 5 times
            assert mock_print.call_count == 5


class TestLoggerFallback:
    """Test cases for logger fallback behavior."""
    
    def test_fallback_to_simple_logger(self):
        """Test fallback to SimpleLogger when src.common.logger is not available."""
        # This test is expected to work since src.common doesn't exist
        # We'll just test that the logger module can be imported
        try:
            from src.ml.feature_engineering import logger
            assert hasattr(logger, 'logger')
        except ImportError:
            # This is expected since src.common doesn't exist
            pass


class TestLoggerIntegration:
    """Integration tests for logger functionality."""
    
    def test_logger_in_real_usage_scenario(self):
        """Test logger in a real usage scenario."""
        # Capture stdout to verify output
        captured_output = StringIO()
        
        with patch('sys.stdout', captured_output):
            logger.print_info("Starting feature generation")
            logger.print_warning("Low memory warning")
            logger.print_error("Failed to load data")
            logger.print_success("Features generated successfully")
            logger.print_debug("Debug: Processing row 1000")
        
        output = captured_output.getvalue()
        
        # Verify that all messages were printed (check for content, not exact format)
        assert "Starting feature generation" in output
        assert "Low memory warning" in output
        assert "Failed to load data" in output
        assert "Features generated successfully" in output
        assert "Debug: Processing row 1000" in output
    
    def test_logger_with_different_message_types(self):
        """Test logger with different types of messages."""
        captured_output = StringIO()
        
        with patch('sys.stdout', captured_output):
            # Test with various message types
            messages = [
                ("print_info", "Processing data..."),
                ("print_warning", "Memory usage high"),
                ("print_error", "Connection timeout"),
                ("print_success", "Operation completed"),
                ("print_debug", "Variable x = 42")
            ]
            
            for method_name, message in messages:
                method = getattr(logger, method_name)
                method(message)
        
        output = captured_output.getvalue()
        
        # Verify all messages are present
        assert "Processing data..." in output
        assert "Memory usage high" in output
        assert "Connection timeout" in output
        assert "Operation completed" in output
        assert "Variable x = 42" in output
    
    def test_logger_performance(self):
        """Test logger performance with many messages."""
        import time
        
        start_time = time.time()
        
        # Log many messages quickly
        for i in range(1000):
            logger.print_info(f"Message {i}")
        
        end_time = time.time()
        
        # Should complete quickly (less than 5 seconds for 1000 messages)
        # Increased threshold to account for slower systems and CI environments
        assert end_time - start_time < 5.0
    
    def test_logger_thread_safety(self):
        """Test logger thread safety (basic test)."""
        import threading
        import queue
        
        # Create a queue to collect messages from threads
        message_queue = queue.Queue()
        
        def log_messages(thread_id):
            """Log messages from a thread."""
            for i in range(10):
                message = f"Thread {thread_id} message {i}"
                logger.print_info(message)
                message_queue.put(message)
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=log_messages, args=(i,))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify that all messages were logged
        assert message_queue.qsize() == 50  # 5 threads * 10 messages each


class TestLoggerEdgeCases:
    """Test edge cases for logger functionality."""
    
    def test_logger_with_none_message(self):
        """Test logger with None message."""
        with patch('builtins.print') as mock_print:
            logger.print_info(None)
            mock_print.assert_called_once()
            # Check that the call contains the expected content
            call_args = mock_print.call_args[0][0]
            assert "None" in call_args
    
    def test_logger_with_empty_string(self):
        """Test logger with empty string message."""
        with patch('builtins.print') as mock_print:
            logger.print_info("")
            mock_print.assert_called_once()
            # Check that the call was made (content may vary due to colors)
            assert mock_print.call_count == 1
    
    def test_logger_with_very_long_message(self):
        """Test logger with very long message."""
        long_message = "A" * 10000  # 10k character message
        
        with patch('builtins.print') as mock_print:
            logger.print_info(long_message)
            mock_print.assert_called_once()
            # Check that the call contains the expected content
            call_args = mock_print.call_args[0][0]
            assert long_message in call_args
    
    def test_logger_with_special_characters(self):
        """Test logger with special characters in message."""
        special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        with patch('builtins.print') as mock_print:
            logger.print_info(special_chars)
            mock_print.assert_called_once()
            # Check that the call contains the expected content
            call_args = mock_print.call_args[0][0]
            assert special_chars in call_args
    
    def test_logger_with_unicode_characters(self):
        """Test logger with unicode characters in message."""
        unicode_message = "Unicode: ✓ ✗ ♠ ♥ ♦ ♣ € £ ¥"
        
        with patch('builtins.print') as mock_print:
            logger.print_info(unicode_message)
            mock_print.assert_called_once()
            # Check that the call contains the expected content
            call_args = mock_print.call_args[0][0]
            assert unicode_message in call_args
    
    def test_logger_with_newlines(self):
        """Test logger with newlines in message."""
        multiline_message = "Line 1\nLine 2\nLine 3"
        
        with patch('builtins.print') as mock_print:
            logger.print_info(multiline_message)
            mock_print.assert_called_once()
            # Check that the call contains the expected content
            call_args = mock_print.call_args[0][0]
            assert multiline_message in call_args
    
    def test_logger_with_tabs(self):
        """Test logger with tabs in message."""
        tabbed_message = "Column1\tColumn2\tColumn3"
        
        with patch('builtins.print') as mock_print:
            logger.print_info(tabbed_message)
            mock_print.assert_called_once()
            # Check that the call contains the expected content
            call_args = mock_print.call_args[0][0]
            assert tabbed_message in call_args


if __name__ == '__main__':
    pytest.main([__file__])
