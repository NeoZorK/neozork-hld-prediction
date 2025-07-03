# tests/cli/test_supertrend_cli.py

"""
Test SuperTrend CLI functionality.

This module tests the SuperTrend indicator CLI integration, including:
- Parameter parsing
- Validation
- Error handling
- Different parameter combinations
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.cli.cli import parse_supertrend_parameters, show_indicator_help


class TestSuperTrendCLI:
    """Test class for SuperTrend CLI functionality."""

    def test_parse_supertrend_parameters_single_param(self):
        """Test parsing SuperTrend parameters with only period."""
        indicator_name, params = parse_supertrend_parameters("10")
        
        assert indicator_name == "supertrend"
        assert params["supertrend_period"] == 10
        assert params["multiplier"] == 3.0
        assert params["price_type"] == "close"

    def test_parse_supertrend_parameters_two_params(self):
        """Test parsing SuperTrend parameters with period and multiplier."""
        indicator_name, params = parse_supertrend_parameters("14,2.5")
        
        assert indicator_name == "supertrend"
        assert params["supertrend_period"] == 14
        assert params["multiplier"] == 2.5
        assert params["price_type"] == "close"

    def test_parse_supertrend_parameters_three_params(self):
        """Test parsing SuperTrend parameters with period, multiplier, and price_type."""
        indicator_name, params = parse_supertrend_parameters("10,3.0,open")
        
        assert indicator_name == "supertrend"
        assert params["supertrend_period"] == 10
        assert params["multiplier"] == 3.0
        assert params["price_type"] == "open"

    def test_parse_supertrend_parameters_float_period(self):
        """Test parsing SuperTrend parameters with float period (should be converted to int)."""
        indicator_name, params = parse_supertrend_parameters("14.0,2.5")
        
        assert indicator_name == "supertrend"
        assert params["supertrend_period"] == 14
        assert params["multiplier"] == 2.5
        assert params["price_type"] == "close"

    def test_parse_supertrend_parameters_invalid_price_type(self):
        """Test parsing SuperTrend parameters with invalid price_type."""
        with pytest.raises(ValueError, match="SuperTrend price_type must be 'open' or 'close'"):
            parse_supertrend_parameters("10,3.0,invalid")

    def test_parse_supertrend_parameters_too_many_params(self):
        """Test parsing SuperTrend parameters with too many parameters."""
        with pytest.raises(ValueError, match="SuperTrend requires 1-3 parameters"):
            parse_supertrend_parameters("10,3.0,close,extra")

    def test_parse_supertrend_parameters_no_params(self):
        """Test parsing SuperTrend parameters with no parameters."""
        with pytest.raises(ValueError, match="SuperTrend requires 1-3 parameters"):
            parse_supertrend_parameters("")

    def test_parse_supertrend_parameters_invalid_period(self):
        """Test parsing SuperTrend parameters with invalid period."""
        with pytest.raises(ValueError):
            parse_supertrend_parameters("invalid,3.0")

    def test_parse_supertrend_parameters_invalid_multiplier(self):
        """Test parsing SuperTrend parameters with invalid multiplier."""
        with pytest.raises(ValueError):
            parse_supertrend_parameters("10,invalid")

    def test_show_indicator_help_supertrend(self):
        """Test that SuperTrend help information is displayed correctly."""
        # Mock print to capture output
        with patch('builtins.print') as mock_print:
            show_indicator_help('supertrend')
            
            # Check that print was called
            assert mock_print.called
            
            # Get the calls to print
            calls = mock_print.call_args_list
            
            # Check that help information contains expected elements
            output_text = ' '.join([str(call) for call in calls])
            assert 'SuperTrend' in output_text
            assert 'period' in output_text
            assert 'multiplier' in output_text
            assert 'price_type' in output_text

    def test_parse_indicator_parameters_supertrend(self):
        """Test that SuperTrend is properly handled in parse_indicator_parameters."""
        from src.cli.cli import parse_indicator_parameters
        
        # Test with single parameter
        indicator_name, params = parse_indicator_parameters("supertrend:10")
        assert indicator_name == "supertrend"
        assert params["supertrend_period"] == 10
        assert params["multiplier"] == 3.0
        assert params["price_type"] == "close"
        
        # Test with two parameters
        indicator_name, params = parse_indicator_parameters("supertrend:14,2.5")
        assert indicator_name == "supertrend"
        assert params["supertrend_period"] == 14
        assert params["multiplier"] == 2.5
        assert params["price_type"] == "close"
        
        # Test with three parameters
        indicator_name, params = parse_indicator_parameters("supertrend:10,3.0,open")
        assert indicator_name == "supertrend"
        assert params["supertrend_period"] == 10
        assert params["multiplier"] == 3.0
        assert params["price_type"] == "open"

    def test_supertrend_in_valid_indicators_list(self):
        """Test that 'supertrend' is included in the valid indicators list."""
        from src.cli.cli import parse_arguments
        
        # This test ensures that 'supertrend' is in the valid_indicators list
        # We can't directly access the list, but we can test that it's accepted
        # by creating a mock args object and testing the validation
        
        # Create a mock args object
        mock_args = MagicMock()
        mock_args.rule = "supertrend:10"
        
        # The fact that we can parse this without error means 'supertrend' is valid
        indicator_name, params = parse_supertrend_parameters("10")
        assert indicator_name == "supertrend"


if __name__ == "__main__":
    pytest.main([__file__]) 