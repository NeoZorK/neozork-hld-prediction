# -*- coding: utf-8 -*-
# tests/cli/test_cli_metric_flag.py

"""
Tests for CLI metric flag functionality and interactive mode.
"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock
from src.cli.quant_encyclopedia import QuantEncyclopedia


class TestQuantEncyclopedia:
    """Test QuantEncyclopedia class functionality."""
    
    def test_encyclopedia_initialization(self):
        """Test QuantEncyclopedia initialization."""
        encyclopedia = QuantEncyclopedia()
        assert encyclopedia is not None
        assert hasattr(encyclopedia, 'metrics')
        assert hasattr(encyclopedia, 'tips')
    
    def test_show_all_metrics(self):
        """Test show_all_metrics method."""
        with patch('builtins.print') as mock_print:
            encyclopedia = QuantEncyclopedia()
            encyclopedia.show_all_metrics()
            mock_print.assert_called()
    
    def test_show_all_tips(self):
        """Test show_all_tips method."""
        with patch('builtins.print') as mock_print:
            encyclopedia = QuantEncyclopedia()
            encyclopedia.show_all_tips()
            mock_print.assert_called()
    
    def test_show_filtered_content(self):
        """Test show_filtered_content method."""
        with patch('builtins.print') as mock_print:
            encyclopedia = QuantEncyclopedia()
            encyclopedia.show_filtered_content('winrate')
            mock_print.assert_called()
    
    def test_show_all_metrics_with_filter(self):
        """Test show_all_metrics method with filter."""
        with patch('builtins.print') as mock_print:
            encyclopedia = QuantEncyclopedia()
            encyclopedia.show_all_metrics('profit')
            mock_print.assert_called()
    
    def test_show_all_tips_with_filter(self):
        """Test show_all_tips method with filter."""
        with patch('builtins.print') as mock_print:
            encyclopedia = QuantEncyclopedia()
            encyclopedia.show_all_tips('monte carlo')
            mock_print.assert_called()


class TestCLIInteractiveFlag:
    """Test CLI interactive flag functionality."""
    
    def test_interactive_mode_positional(self):
        """Test interactive mode as positional argument."""
        with patch('sys.argv', ['run_analysis.py', 'interactive']):
            with patch('sys.exit') as mock_exit:
                with patch('src.cli.interactive_mode.start_interactive_mode') as mock_start:
                    from src.cli.cli import parse_arguments
                    parse_arguments()
                    mock_start.assert_called_once()
                    mock_exit.assert_called_with(0)


class TestCLIMetricFlagIntegration:
    """Integration tests for CLI metric flag functionality."""
    
    def test_metric_flag_examples_integration(self):
        """Test that --metric flag appears in examples."""
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--examples']
    
        # Capture examples output
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            with patch('sys.exit') as mock_exit:
                from src.cli.cli import parse_arguments
                parse_arguments()
    
        # Get examples output
        examples_output = mock_stdout.getvalue()
    
        # Verify --metric flag is mentioned in examples
        assert '--metric' in examples_output


if __name__ == "__main__":
    pytest.main([__file__]) 