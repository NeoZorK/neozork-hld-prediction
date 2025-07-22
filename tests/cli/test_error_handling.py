# -*- coding: utf-8 -*-
# tests/cli/test_error_handling.py

"""
Tests for enhanced CLI error handling with colorful help and icons.
All comments and text are in English.
"""

import pytest
from unittest.mock import patch, call
from src.cli.error_handling import (
    CLIErrorHandler,
    extract_indicator_name_from_error,
    get_indicator_help_data,
    show_enhanced_indicator_help,
    handle_indicator_error
)


class TestCLIErrorHandler:
    """Test cases for CLIErrorHandler class."""

    def test_icons_defined(self):
        """Test that all required icons are defined."""
        required_icons = ['error', 'warning', 'info', 'success', 'help', 'indicator', 'parameter', 'example', 'tip', 'fix']
        for icon in required_icons:
            assert icon in CLIErrorHandler.ICONS
            assert CLIErrorHandler.ICONS[icon] is not None

    def test_colors_defined(self):
        """Test that all required colors are defined."""
        required_colors = ['error', 'warning', 'info', 'success', 'help', 'indicator', 'parameter', 'example', 'tip', 'fix']
        for color in required_colors:
            assert color in CLIErrorHandler.COLORS
            assert CLIErrorHandler.COLORS[color] is not None

    @patch('builtins.print')
    def test_print_error_header(self, mock_print):
        """Test error header printing."""
        CLIErrorHandler.print_error_header("Test error message")
        
        calls = mock_print.call_args_list
        assert len(calls) == 2
        assert "ERROR:" in str(calls[0])
        assert "Test error message" in str(calls[0])
        assert "=" * 60 in str(calls[1])

    @patch('builtins.print')
    def test_print_help_section(self, mock_print):
        """Test help section printing."""
        CLIErrorHandler.print_help_section("Test Title", "Test content", "help")
        
        calls = mock_print.call_args_list
        assert len(calls) == 2
        assert "Test Title:" in str(calls[0])
        assert "Test content" in str(calls[1])

    @patch('builtins.print')
    def test_print_parameter_info(self, mock_print):
        """Test parameter info printing."""
        CLIErrorHandler.print_parameter_info("test_param", "Test description", "int", "10")
        
        calls = mock_print.call_args_list
        assert len(calls) == 2
        assert "test_param" in str(calls[0])
        assert "(int)" in str(calls[0])
        assert "[default: 10]" in str(calls[0])
        assert "Test description" in str(calls[1])

    @patch('builtins.print')
    def test_print_example(self, mock_print):
        """Test example printing."""
        CLIErrorHandler.print_example("test:example", "Test description")
        
        calls = mock_print.call_args_list
        assert len(calls) == 1
        assert "test:example" in str(calls[0])
        assert "Test description" in str(calls[0])

    @patch('builtins.print')
    def test_print_tip(self, mock_print):
        """Test tip printing."""
        CLIErrorHandler.print_tip("Test tip")
        
        calls = mock_print.call_args_list
        assert len(calls) == 1
        assert "Test tip" in str(calls[0])

    @patch('builtins.print')
    def test_print_fix(self, mock_print):
        """Test fix printing."""
        CLIErrorHandler.print_fix("Test fix")
        
        calls = mock_print.call_args_list
        assert len(calls) == 1
        assert "Test fix" in str(calls[0])

    @patch('builtins.print')
    def test_print_command_usage(self, mock_print):
        """Test command usage printing."""
        CLIErrorHandler.print_command_usage("test command", "Test description")
        
        calls = mock_print.call_args_list
        assert len(calls) == 1
        assert "test command" in str(calls[0])
        assert "Test description" in str(calls[0])

    @patch('builtins.print')
    def test_print_separator(self, mock_print):
        """Test separator printing."""
        CLIErrorHandler.print_separator()
        
        calls = mock_print.call_args_list
        assert len(calls) == 1
        assert "─" * 60 in str(calls[0])

    @patch('builtins.print')
    def test_print_footer(self, mock_print):
        """Test footer printing."""
        CLIErrorHandler.print_footer()
        
        calls = mock_print.call_args_list
        assert len(calls) == 4
        assert "Need more help?" in str(calls[0])
        assert "--indicators" in str(calls[1])
        assert "--examples" in str(calls[2])
        assert "--help" in str(calls[3])


class TestErrorExtraction:
    """Test cases for error message parsing."""

    def test_extract_rsi_from_price_type_error(self):
        """Test extracting RSI from price type error."""
        error_msg = "RSI price_type must be 'open' or 'close', got: clo"
        result = extract_indicator_name_from_error(error_msg)
        assert result == "rsi"

    def test_extract_macd_from_parameter_error(self):
        """Test extracting MACD from parameter error."""
        error_msg = "MACD requires exactly 4 parameters: fast_period,slow_period,signal_period,price_type. Got: 12,26"
        result = extract_indicator_name_from_error(error_msg)
        assert result == "macd"

    def test_extract_cot_from_invalid_parameter_error(self):
        """Test extracting COT from invalid parameter error."""
        error_msg = "Invalid COT parameters: 20,clo. Error: COT price_type must be 'open' or 'close', got: clo"
        result = extract_indicator_name_from_error(error_msg)
        assert result == "cot"

    def test_extract_unknown_indicator(self):
        """Test extracting unknown indicator name."""
        error_msg = "Unknown indicator: testindicator"
        result = extract_indicator_name_from_error(error_msg)
        assert result == "testindicator"

    def test_extract_none_from_generic_error(self):
        """Test extracting None from generic error."""
        error_msg = "Some generic error message"
        result = extract_indicator_name_from_error(error_msg)
        assert result is None

    def test_extract_case_insensitive(self):
        """Test that extraction is case insensitive."""
        error_msg = "rsi price_type must be 'open' or 'close'"
        result = extract_indicator_name_from_error(error_msg)
        assert result == "rsi"


class TestIndicatorHelpData:
    """Test cases for indicator help data."""

    def test_get_rsi_help_data(self):
        """Test getting RSI help data."""
        data = get_indicator_help_data('rsi')
        assert data is not None
        assert data['name'] == 'RSI (Relative Strength Index)'
        assert 'format' in data
        assert 'parameters' in data
        assert 'examples' in data
        assert 'tips' in data
        assert 'common_errors' in data

    def test_get_cot_help_data(self):
        """Test getting COT help data."""
        data = get_indicator_help_data('cot')
        assert data is not None
        assert data['name'] == 'COT (Commitment of Traders)'
        assert len(data['parameters']) == 2
        assert data['parameters'][0][0] == 'period'
        assert data['parameters'][1][0] == 'price_type'

    def test_get_unknown_indicator_data(self):
        """Test getting data for unknown indicator."""
        data = get_indicator_help_data('unknown_indicator')
        assert data is None

    def test_get_case_insensitive_data(self):
        """Test that help data retrieval is case insensitive."""
        data_lower = get_indicator_help_data('rsi')
        data_upper = get_indicator_help_data('RSI')
        assert data_lower == data_upper

    def test_all_indicators_have_required_fields(self):
        """Test that all indicators have required fields."""
        indicators = ['rsi', 'macd', 'stoch', 'ema', 'bb', 'cot', 'cci', 'vwap', 'pivot', 'atr']
        required_fields = ['name', 'description', 'format', 'parameters', 'examples', 'tips', 'common_errors']
        
        for indicator in indicators:
            data = get_indicator_help_data(indicator)
            assert data is not None
            for field in required_fields:
                assert field in data, f"Missing field '{field}' for indicator '{indicator}'"


class TestEnhancedHelpDisplay:
    """Test cases for enhanced help display."""

    @patch('builtins.print')
    def test_show_enhanced_indicator_help_rsi(self, mock_print):
        """Test showing enhanced help for RSI."""
        show_enhanced_indicator_help("RSI price_type must be 'open' or 'close', got: clo", "rsi")
        
        calls = mock_print.call_args_list
        assert len(calls) > 0
        
        # Check that error header was printed
        error_calls = [call for call in calls if "ERROR:" in str(call)]
        assert len(error_calls) > 0
        
        # Check that help sections were printed
        help_calls = [call for call in calls if "RSI" in str(call)]
        assert len(help_calls) > 0

    @patch('builtins.print')
    def test_show_enhanced_indicator_help_cot(self, mock_print):
        """Test showing enhanced help for COT."""
        show_enhanced_indicator_help("COT price_type must be 'open' or 'close', got: clo", "cot")
        
        calls = mock_print.call_args_list
        assert len(calls) > 0
        
        # Check that COT help was displayed
        cot_calls = [call for call in calls if "COT" in str(call)]
        assert len(cot_calls) > 0

    @patch('builtins.print')
    def test_show_enhanced_indicator_help_unknown(self, mock_print):
        """Test showing enhanced help for unknown indicator."""
        show_enhanced_indicator_help("Unknown indicator: test", "test")
        
        calls = mock_print.call_args_list
        assert len(calls) > 0
        
        # Check that unknown indicator message was displayed
        unknown_calls = [call for call in calls if "Unknown Indicator" in str(call)]
        assert len(unknown_calls) > 0

    @patch('builtins.print')
    def test_show_enhanced_indicator_help_no_indicator(self, mock_print):
        """Test showing enhanced help without indicator name."""
        show_enhanced_indicator_help("Some generic error")
        
        calls = mock_print.call_args_list
        assert len(calls) > 0
        
        # Check that general help was displayed
        general_calls = [call for call in calls if "General Help" in str(call)]
        assert len(general_calls) > 0

    @patch('builtins.print')
    def test_handle_indicator_error_with_help(self, mock_print):
        """Test handling indicator error with help."""
        handle_indicator_error("COT price_type must be 'open' or 'close', got: clo")
        
        calls = mock_print.call_args_list
        assert len(calls) > 0
        
        # Check that error was handled
        error_calls = [call for call in calls if "ERROR:" in str(call)]
        assert len(error_calls) > 0

    @patch('builtins.print')
    def test_handle_indicator_error_without_help(self, mock_print):
        """Test handling indicator error without help."""
        handle_indicator_error("Some error", show_help=False)
        
        calls = mock_print.call_args_list
        assert len(calls) > 0
        
        # Check that only error header was printed
        error_calls = [call for call in calls if "ERROR:" in str(call)]
        assert len(error_calls) > 0


    def test_get_atr_help_data(self):
        """Test getting ATR help data."""
        data = get_indicator_help_data('atr')
        assert data is not None
        assert data['name'] == 'ATR (Average True Range)'
        assert len(data['parameters']) == 1
        assert data['parameters'][0][0] == 'period'
        assert data['format'] == 'atr:period'
        
        # Test that ATR has examples
        assert len(data['examples']) >= 3
        assert 'atr:14' in [example[0] for example in data['examples']]
        
        # Test that ATR has tips
        assert len(data['tips']) > 0
        
        # Test that ATR has common errors
        assert len(data['common_errors']) > 0

    @patch('builtins.print')
    def test_show_enhanced_indicator_help_atr(self, mock_print):
        """Test showing enhanced help for ATR."""
        show_enhanced_indicator_help("ATR requires exactly 1 parameter: period. Got: 14,20", "atr")
        
        calls = mock_print.call_args_list
        assert len(calls) > 0
        
        # Check that ATR help was displayed
        atr_calls = [call for call in calls if "ATR" in str(call)]
        assert len(atr_calls) > 0
        
        # Check that parameters section was displayed
        param_calls = [call for call in calls if "period" in str(call)]
        assert len(param_calls) > 0
        
        # Check that examples were displayed
        example_calls = [call for call in calls if "atr:14" in str(call)]
        assert len(example_calls) > 0


class TestIntegration:
    """Integration tests for error handling."""

    @patch('builtins.print')
    def test_full_error_flow_cot(self, mock_print):
        """Test full error flow for COT indicator."""
        error_msg = "COT price_type must be 'open' or 'close', got: clo"
        
        # Extract indicator name
        indicator_name = extract_indicator_name_from_error(error_msg)
        assert indicator_name == "cot"
        
        # Get help data
        help_data = get_indicator_help_data(indicator_name)
        assert help_data is not None
        assert help_data['name'] == 'COT (Commitment of Traders)'
        
        # Show enhanced help
        show_enhanced_indicator_help(error_msg, indicator_name)
        
        calls = mock_print.call_args_list
        assert len(calls) > 0
        
        # Verify that all expected sections were printed
        sections_found = {
            'error_header': False,
            'indicator_name': False,
            'parameters': False,
            'examples': False,
            'command_usage': False,
            'footer': False
        }
        
        for call in calls:
            call_str = str(call)
            if "ERROR:" in call_str:
                sections_found['error_header'] = True
            if "COT" in call_str and "Help" in call_str:
                sections_found['indicator_name'] = True
            if "Parameters:" in call_str:
                sections_found['parameters'] = True
            if "Examples:" in call_str:
                sections_found['examples'] = True
            if "Command Usage:" in call_str:
                sections_found['command_usage'] = True
            if "Need more help?" in call_str:
                sections_found['footer'] = True
        
        # All sections should be found
        for section, found in sections_found.items():
            assert found, f"Section '{section}' was not found in output" 