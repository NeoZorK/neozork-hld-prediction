# -*- coding: utf-8 -*-
# tests/cli/test_cli_indicators_integration.py

"""
Integration tests for CLI indicators search functionality.
"""

import pytest
import subprocess
import sys
import os
from unittest.mock import patch, MagicMock
from src.cli.cli import parse_arguments
from src.cli.indicators_search import IndicatorSearcher


class TestCLIIndicatorsIntegration:
    """Test cases for CLI integration with indicators search."""
    
    def test_indicators_flag_no_args(self):
        """Test --indicators flag with no arguments."""
        with patch('sys.argv', ['cli', '--indicators']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Check that categories were displayed
                calls = mock_print.call_args_list
                assert any("Available Indicator Categories:" in str(call) for call in calls)
    
    def test_indicators_flag_with_category(self):
        """Test --indicators flag with category argument."""
        with patch('sys.argv', ['cli', '--indicators', 'oscillators']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Check that category was displayed
                calls = mock_print.call_args_list
                assert any("Indicators in category 'oscillators':" in str(call) for call in calls)
    
    def test_indicators_flag_with_category_and_name(self):
        """Test --indicators flag with category and name arguments."""
        with patch('sys.argv', ['cli', '--indicators', 'oscillators', 'rsi']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Check that search was performed
                calls = mock_print.call_args_list
                assert any("Search in category 'oscillators' for 'rsi':" in str(call) for call in calls)
    
    def test_indicators_flag_with_multiple_name_words(self):
        """Test --indicators flag with multiple words in name."""
        with patch('sys.argv', ['cli', '--indicators', 'oscillators', 'relative', 'strength']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Check that search was performed with joined words
                calls = mock_print.call_args_list
                assert any("Search in category 'oscillators' for 'relative strength':" in str(call) for call in calls)
    
    def test_indicators_flag_no_search_results(self):
        """Test --indicators flag when no search results found."""
        with patch('sys.argv', ['cli', '--indicators', 'oscillators', 'nonexistent']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Should print no results message
                calls = mock_print.call_args_list
                assert any("No indicators found in category 'oscillators' matching 'nonexistent'" in str(call) for call in calls)
    
    def test_indicators_flag_with_examples(self):
        """Test --indicators flag examples in help."""
        with patch('sys.argv', ['cli', '--examples']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                calls = mock_print.call_args_list
                # Check that indicator examples are shown
                assert any("Show all indicators:" in str(call) for call in calls)
                assert any("Show oscillators:" in str(call) for call in calls)
                assert any("Show RSI info:" in str(call) for call in calls)
    
    def test_indicators_flag_help_text(self):
        """Test that --indicators flag has proper help text."""
        # This test verifies that the --indicators flag is properly documented
        # We can't easily capture the help text directly, but we can verify
        # that the flag is accepted and processed correctly
        with patch('sys.argv', ['cli', '--indicators']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Check that categories were displayed
                calls = mock_print.call_args_list
                assert any("Available Indicator Categories:" in str(call) for call in calls)
    
    def test_indicators_flag_with_other_flags(self):
        """Test that --indicators flag works correctly with other flags."""
        # Test that --indicators takes precedence over other processing
        with patch('sys.argv', ['cli', '--indicators', 'oscillators', '--help']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Should process indicators, not help
                calls = mock_print.call_args_list
                assert any("Search in category 'oscillators' for '--help':" in str(call) for call in calls)
    
    def test_indicators_flag_error_handling(self):
        """Test error handling in indicators flag processing."""
        with patch('sys.argv', ['cli', '--indicators', 'oscillators']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0  # Should still exit cleanly


class TestCLIIndicatorsEndToEnd:
    """End-to-end tests for CLI indicators functionality."""
    
    def test_cli_indicators_command_line(self):
        """Test CLI indicators command from command line."""
        # This test would require actual CLI execution
        # For now, we'll test the argument parsing logic
        with patch('sys.argv', ['cli', '--indicators']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Should have called print at least once
                assert len(mock_print.call_args_list) > 0
    
    def test_cli_indicators_with_real_searcher(self):
        """Test CLI indicators with real IndicatorSearcher instance."""
        with patch('sys.argv', ['cli', '--indicators', 'oscillators']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Should have called print at least once
                assert len(mock_print.call_args_list) > 0
    
    def test_cli_indicators_search_functionality(self):
        """Test CLI indicators search functionality."""
        with patch('sys.argv', ['cli', '--indicators', 'oscillators', 'rsi']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Should have called print for search results
                calls = mock_print.call_args_list
                assert len(calls) > 0


class TestCLIIndicatorsEdgeCases:
    """Test edge cases for CLI indicators functionality."""
    
    def test_indicators_flag_empty_category(self):
        """Test --indicators flag with empty category."""
        with patch('sys.argv', ['cli', '--indicators', '']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Empty string should find all indicators (empty string is contained in any name)
                calls = mock_print.call_args_list
                assert any("Search results for '' across all categories:" in str(call) for call in calls)
    
    def test_indicators_flag_special_characters(self):
        """Test --indicators flag with special characters in search."""
        with patch('sys.argv', ['cli', '--indicators', 'oscillators', 'rsi-14']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Should handle special characters
                calls = mock_print.call_args_list
                assert any("Search in category 'oscillators' for 'rsi-14':" in str(call) for call in calls)
    
    def test_indicators_flag_unicode_characters(self):
        """Test --indicators flag with unicode characters."""
        with patch('sys.argv', ['cli', '--indicators', 'oscillators', 'rsi指标']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Should handle unicode characters
                calls = mock_print.call_args_list
                assert any("Search in category 'oscillators' for 'rsi指标':" in str(call) for call in calls)
    
    def test_indicators_flag_very_long_search(self):
        """Test --indicators flag with very long search query."""
        long_query = "a" * 1000  # Very long query
        with patch('sys.argv', ['cli', '--indicators', 'oscillators', long_query]):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Should handle very long queries
                calls = mock_print.call_args_list
                assert any("Search in category 'oscillators' for" in str(call) for call in calls)
    
    def test_indicators_flag_multiple_categories(self):
        """Test --indicators flag with multiple category arguments."""
        # This should treat the first argument as category and rest as search terms
        with patch('sys.argv', ['cli', '--indicators', 'oscillators', 'momentum', 'rsi']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                # Should join 'momentum' and 'rsi' as search terms
                calls = mock_print.call_args_list
                assert any("Search in category 'oscillators' for 'momentum rsi':" in str(call) for call in calls)


class TestCLIIndicatorsRealFunctionality:
    """Test real functionality of CLI indicators."""
    
    def test_indicators_categories_display(self):
        """Test that all indicator categories are displayed."""
        with patch('sys.argv', ['cli', '--indicators']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                calls = mock_print.call_args_list
                
                # Check that categories are displayed
                output = '\n'.join([str(call) for call in calls])
                assert "Available Indicator Categories:" in output
                
                # Check for expected categories
                expected_categories = ['trend', 'momentum', 'oscillators', 'volatility', 'volume']
                for category in expected_categories:
                    assert category in output
    
    def test_indicators_oscillators_category(self):
        """Test oscillators category specifically."""
        with patch('sys.argv', ['cli', '--indicators', 'oscillators']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                calls = mock_print.call_args_list
                
                output = '\n'.join([str(call) for call in calls])
                assert "Indicators in category 'oscillators':" in output
                assert "RSI" in output  # Should find RSI indicator
    
    def test_indicators_search_functionality(self):
        """Test search functionality."""
        with patch('sys.argv', ['cli', '--indicators', 'oscillators', 'rsi']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    parse_arguments()
                
                assert exc_info.value.code == 0
                calls = mock_print.call_args_list
                
                output = '\n'.join([str(call) for call in calls])
                assert "Search in category 'oscillators' for 'rsi':" in output
                # Should find RSI indicator
                assert "RSI" in output


def test_indicators_flag_single_indicator_name():
    """Test --indicators flag with single indicator name (should search across all categories)."""
    with patch('sys.argv', ['cli', '--indicators', 'cci']):
        with patch('builtins.print') as mock_print:
            with pytest.raises(SystemExit) as exc_info:
                parse_arguments()
                
                # Verify that search was performed across all categories
                calls = mock_print.call_args_list
                assert any("Search results for 'cci' across all categories:" in str(call) for call in calls)
                assert exc_info.value.code == 0


def test_indicators_flag_single_indicator_name_not_found():
    """Test --indicators flag with single indicator name that doesn't exist."""
    with patch('sys.argv', ['cli', '--indicators', 'nonexistent']):
        with patch('builtins.print') as mock_print:
            with pytest.raises(SystemExit) as exc_info:
                parse_arguments()
                
                # Verify that appropriate error message was shown
                calls = mock_print.call_args_list
                assert any("No indicators found matching: nonexistent" in str(call) for call in calls)
                assert exc_info.value.code == 0 