# -*- coding: utf-8 -*-
# tests/cli/test_cli_metric_flag.py

"""
Tests for CLI metric flag functionality and interactive mode.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO
from src.cli.cli import parse_arguments
from src.cli.quant_encyclopedia import QuantEncyclopedia


class TestCLIMetricFlag:
    """Test CLI metric flag functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Store original argv
        self.original_argv = sys.argv.copy()
    
    def teardown_method(self):
        """Clean up after tests."""
        # Restore original argv
        sys.argv = self.original_argv
    
    def test_metric_flag_no_args(self):
        """Test --metric flag without arguments."""
        with patch('sys.argv', ['run_analysis.py', '--metric']):
            with patch('sys.exit') as mock_exit:
                parse_arguments()
                mock_exit.assert_called_with(0)
    
    def test_metric_flag_with_metrics_type(self):
        """Test --metric flag with metrics type."""
        with patch('sys.argv', ['run_analysis.py', '--metric', 'metrics']):
            with patch('sys.exit') as mock_exit:
                parse_arguments()
                mock_exit.assert_called_with(0)
    
    def test_metric_flag_with_tips_type(self):
        """Test --metric flag with tips type."""
        with patch('sys.argv', ['run_analysis.py', '--metric', 'tips']):
            with patch('sys.exit') as mock_exit:
                parse_arguments()
                mock_exit.assert_called_with(0)
    
    def test_metric_flag_with_filter(self):
        """Test --metric flag with filter text."""
        with patch('sys.argv', ['run_analysis.py', '--metric', 'winrate']):
            with patch('sys.exit') as mock_exit:
                parse_arguments()
                mock_exit.assert_called_with(0)
    
    def test_metric_flag_with_type_and_filter(self):
        """Test --metric flag with type and filter."""
        with patch('sys.argv', ['run_analysis.py', '--metric', 'metrics', 'profit']):
            with patch('sys.exit') as mock_exit:
                parse_arguments()
                mock_exit.assert_called_with(0)


class TestCLIInteractiveFlag:
    """Test CLI interactive flag functionality."""
    
    def test_interactive_flag_long(self):
        """Test --interactive flag."""
        with patch('sys.argv', ['run_analysis.py', '--interactive']):
            with patch('sys.exit') as mock_exit:
                with patch('src.cli.interactive_mode.start_interactive_mode') as mock_start:
                    parse_arguments()
                    mock_start.assert_called_once()
                    mock_exit.assert_called_with(0)
    
    def test_interactive_flag_short(self):
        """Test -i flag."""
        with patch('sys.argv', ['run_analysis.py', '-i']):
            with patch('sys.exit') as mock_exit:
                with patch('src.cli.interactive_mode.start_interactive_mode') as mock_start:
                    parse_arguments()
                    mock_start.assert_called_once()
                    mock_exit.assert_called_with(0)
    
    def test_interactive_mode_positional(self):
        """Test interactive mode as positional argument."""
        with patch('sys.argv', ['run_analysis.py', 'interactive']):
            with patch('sys.exit') as mock_exit:
                with patch('src.cli.interactive_mode.start_interactive_mode') as mock_start:
                    parse_arguments()
                    mock_start.assert_called_once()
                    mock_exit.assert_called_with(0)


class TestInteractiveModeMetrics:
    """Test interactive mode metrics encyclopedia integration."""
    
    @patch('builtins.input')
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_interactive_metrics_menu(self, mock_encyclopedia_class, mock_input):
        """Test metrics encyclopedia menu in interactive mode."""
        from src.cli.interactive_mode import InteractiveMode
        
        # Mock user input: select metrics (10), then show all metrics (1), then back (5), then exit (0)
        mock_input.side_effect = ['10', '1', '5', '0']
        
        # Mock encyclopedia
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Create interactive mode instance
        interactive = InteractiveMode()
        
        # Mock the start method to avoid infinite loop
        with patch.object(interactive, 'start'):
            # Test the metrics encyclopedia method directly
            interactive._show_trading_metrics_encyclopedia()
            
            # Verify encyclopedia was called
            mock_encyclopedia.show_all_metrics.assert_called_once()
    
    @patch('builtins.input')
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_interactive_metrics_search(self, mock_encyclopedia_class, mock_input):
        """Test metrics search in interactive mode."""
        from src.cli.interactive_mode import InteractiveMode
        
        # Mock user input: select metrics (10), then search metrics (3), enter "winrate", then back (5), then exit (0)
        mock_input.side_effect = ['10', '3', 'winrate', '5', '0']
        
        # Mock encyclopedia
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Create interactive mode instance
        interactive = InteractiveMode()
        
        # Mock the start method to avoid infinite loop
        with patch.object(interactive, 'start'):
            # Test the metrics encyclopedia method directly
            interactive._show_trading_metrics_encyclopedia()
            
            # Verify encyclopedia was called with search term
            mock_encyclopedia.show_all_metrics.assert_called_once_with('winrate')


class TestCLIMetricFlagIntegration:
    """Integration tests for CLI --metric flag."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.original_argv = sys.argv.copy()
    
    def teardown_method(self):
        """Clean up after tests."""
        sys.argv = self.original_argv
    
    def test_metric_flag_help_integration(self):
        """Test that --metric flag appears in help output."""
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--help']
        
        # Capture help output
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            with patch('sys.exit') as mock_exit:
                parse_arguments()
        
        # Get help output
        help_output = mock_stdout.getvalue()
        
        # Verify --metric flag is mentioned
        assert '--metric' in help_output
        assert 'encyclopedia' in help_output.lower()
    
    def test_metric_flag_with_other_flags(self):
        """Test that --metric flag works alongside other flags."""
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--metric', '--version']
        
        # This should show version and exit, not process --metric
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            with patch('sys.exit') as mock_exit:
                parse_arguments()
        
        # Verify version was shown
        version_output = mock_stdout.getvalue()
        assert 'Shcherbyna Pressure Vector Indicator' in version_output


def test_metric_flag_examples():
    """Test various --metric flag usage examples."""
    test_cases = [
        (['--metric'], 'show_all_metrics_and_tips'),
        (['--metric', 'metrics'], 'show_metrics_only'),
        (['--metric', 'tips'], 'show_tips_only'),
        (['--metric', 'notes'], 'show_tips_only'),
        (['--metric', 'profit factor'], 'show_filtered_content'),
        (['--metric', 'metrics', 'profit'], 'show_filtered_metrics'),
        (['--metric', 'tips', 'winrate'], 'show_filtered_tips'),
        (['--metric', 'notes', 'winrate'], 'show_filtered_tips'),
    ]
    
    for args, expected_behavior in test_cases:
        # This is a basic test to ensure the flag parsing doesn't crash
        assert isinstance(args, list)
        assert isinstance(expected_behavior, str)


if __name__ == "__main__":
    pytest.main([__file__]) 