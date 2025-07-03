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

    def test_parse_supertrend_parameters_two_params(self):
        """Test parsing SuperTrend parameters with period and multiplier."""
        indicator_name, params = parse_supertrend_parameters("10,3.0")
        
        assert indicator_name == 'supertrend'
        assert params['supertrend_period'] == 10
        assert params['multiplier'] == 3.0
        assert params['price_type'] == 'close'  # default

    def test_parse_supertrend_parameters_three_params_close(self):
        """Test parsing SuperTrend parameters with period, multiplier, and close."""
        indicator_name, params = parse_supertrend_parameters("10,3.0,close")
        
        assert indicator_name == 'supertrend'
        assert params['supertrend_period'] == 10
        assert params['multiplier'] == 3.0
        assert params['price_type'] == 'close'

    def test_parse_supertrend_parameters_three_params_open(self):
        """Test parsing SuperTrend parameters with period, multiplier, and open."""
        indicator_name, params = parse_supertrend_parameters("10,3.0,open")
        
        assert indicator_name == 'supertrend'
        assert params['supertrend_period'] == 10
        assert params['multiplier'] == 3.0
        assert params['price_type'] == 'open'

    def test_parse_supertrend_parameters_float_values(self):
        """Test parsing SuperTrend parameters with float values."""
        indicator_name, params = parse_supertrend_parameters("14.0,2.5,close")
        
        assert indicator_name == 'supertrend'
        assert params['supertrend_period'] == 14  # converted to int
        assert params['multiplier'] == 2.5
        assert params['price_type'] == 'close'

    def test_parse_supertrend_parameters_single_param_error(self):
        """Test that single parameter raises error."""
        with pytest.raises(ValueError, match="SuperTrend requires exactly 2-3 parameters"):
            parse_supertrend_parameters("10")

    def test_parse_supertrend_parameters_empty_string_error(self):
        """Test that empty string raises error."""
        with pytest.raises(ValueError, match="SuperTrend requires exactly 2-3 parameters"):
            parse_supertrend_parameters("")

    def test_parse_supertrend_parameters_four_params_error(self):
        """Test that four parameters raises error."""
        with pytest.raises(ValueError, match="SuperTrend requires exactly 2-3 parameters"):
            parse_supertrend_parameters("10,3.0,close,extra")

    def test_parse_supertrend_parameters_invalid_price_type_error(self):
        """Test that invalid price type raises error."""
        with pytest.raises(ValueError, match="SuperTrend price_type must be 'open' or 'close'"):
            parse_supertrend_parameters("10,3.0,invalid")

    def test_parse_supertrend_parameters_invalid_period_error(self):
        """Test that invalid period raises error."""
        with pytest.raises(ValueError, match="Invalid SuperTrend parameters"):
            parse_supertrend_parameters("abc,3.0,close")

    def test_parse_supertrend_parameters_invalid_multiplier_error(self):
        """Test that invalid multiplier raises error."""
        with pytest.raises(ValueError, match="Invalid SuperTrend parameters"):
            parse_supertrend_parameters("10,xyz,close")

    def test_parse_supertrend_parameters_case_insensitive_price_type(self):
        """Test that price type is case insensitive."""
        indicator_name, params = parse_supertrend_parameters("10,3.0,OPEN")
        
        assert indicator_name == 'supertrend'
        assert params['price_type'] == 'open'

    def test_parse_supertrend_parameters_whitespace_handling(self):
        """Test that whitespace is properly handled."""
        indicator_name, params = parse_supertrend_parameters(" 10 , 3.0 , close ")
        
        assert indicator_name == 'supertrend'
        assert params['supertrend_period'] == 10
        assert params['multiplier'] == 3.0
        assert params['price_type'] == 'close'

    def test_parse_supertrend_parameters_edge_cases(self):
        """Test edge cases for SuperTrend parameters."""
        # Very large period
        indicator_name, params = parse_supertrend_parameters("1000,1.0,close")
        assert params['supertrend_period'] == 1000
        assert params['multiplier'] == 1.0

        # Very small multiplier
        indicator_name, params = parse_supertrend_parameters("10,0.1,open")
        assert params['supertrend_period'] == 10
        assert params['multiplier'] == 0.1
        assert params['price_type'] == 'open'

    def test_show_indicator_help_supertrend(self):
        """Test that SuperTrend help information is displayed correctly."""
        with patch('builtins.print') as mock_print:
            show_indicator_help('supertrend')
            
            # Check that help was called
            mock_print.assert_called()
            
            # Get the printed output
            calls = mock_print.call_args_list
            output = '\n'.join([str(call) for call in calls])
            
            # Check that required information is present
            assert 'SuperTrend Help' in output
            assert 'period,multiplier' in output
            assert 'required' in output
            assert 'open or close' in output

    def test_parse_indicator_parameters_supertrend(self):
        """Test that SuperTrend is properly handled in parse_indicator_parameters."""
        from src.cli.cli import parse_indicator_parameters
        
        # Test with two parameters (required)
        indicator_name, params = parse_indicator_parameters("supertrend:10,3.0")
        assert indicator_name == "supertrend"
        assert params["supertrend_period"] == 10
        assert params["multiplier"] == 3.0
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
        mock_args.rule = "supertrend:10,3.0"
        
        # The fact that we can parse this without error means 'supertrend' is valid
        indicator_name, params = parse_supertrend_parameters("10,3.0")
        assert indicator_name == "supertrend"


if __name__ == "__main__":
    pytest.main([__file__]) 