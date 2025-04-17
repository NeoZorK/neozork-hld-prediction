# tests/common/test_logger.py

import unittest
from unittest.mock import patch, call
import io # For capturing print output
from colorama import Fore, Style

# Import functions from the module to be tested
# Adjust the import path based on your test runner's root directory
# Assuming tests run from the project root
from src.common import logger

# Set RESET_ALL explicitly for comparison if needed outside colorama's autoreset
RESET_ALL = Style.RESET_ALL


# Unit tests for the logger module
class TestLogger(unittest.TestCase):

    # Test print_info function
    # Use patch to redirect stdout to a StringIO object to capture print output
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_info(self, mock_stdout):
        message = "Test info message"
        expected_output = f"{logger.INFO_COLOR}{message}\n"
        logger.print_info(message)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    # Test print_warning function
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_warning(self, mock_stdout):
        message = "Test warning message"
        # Check that the "Warning: " prefix is added
        expected_output = f"{logger.WARNING_COLOR}Warning: {message}\n"
        logger.print_warning(message)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    # Test print_error function
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_error(self, mock_stdout):
        message = "Test error message"
        # Check that the "Error: " prefix is added
        expected_output = f"{logger.ERROR_COLOR}Error: {message}\n"
        logger.print_error(message)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    # Test print_debug function
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_debug(self, mock_stdout):
        message = "Test debug message"
         # Check that the "Debug: " prefix is added
        expected_output = f"{logger.DEBUG_COLOR}Debug: {message}\n"
        logger.print_debug(message)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    # Test print_success function
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_success(self, mock_stdout):
        message = "Test success message"
        expected_output = f"{logger.SUCCESS_COLOR}{message}\n"
        logger.print_success(message)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    # Test format_summary_line function
    def test_format_summary_line(self):
        key = "Test Key"
        value = "Test Value"
        key_width = 15
        # Manually construct expected string with colors and padding
        padded_key = f"{key+':':<{key_width}}"
        expected_output = f"{logger.HIGHLIGHT_COLOR}{padded_key}{RESET_ALL} {value}"
        # Call the function and assert equality
        formatted_line = logger.format_summary_line(key, value, key_width)
        self.assertEqual(formatted_line, expected_output)

    # Test format_summary_line with default width
    def test_format_summary_line_default_width(self):
        key = "Key"
        value = "Value"
        default_key_width = 25
        padded_key = f"{key+':':<{default_key_width}}"
        expected_output = f"{logger.HIGHLIGHT_COLOR}{padded_key}{RESET_ALL} {value}"
        formatted_line = logger.format_summary_line(key, value) # Use default width
        self.assertEqual(formatted_line, expected_output)

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()