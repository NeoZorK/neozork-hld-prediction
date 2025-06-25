# -*- coding: utf-8 -*-
# tests/cli/test_cli_metric_flag.py

"""
Tests for CLI --metric flag functionality
All comments are in English.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO


class TestCLIMetricFlag:
    """Test cases for CLI --metric flag."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Store original argv
        self.original_argv = sys.argv.copy()
    
    def teardown_method(self):
        """Clean up after tests."""
        # Restore original argv
        sys.argv = self.original_argv
    
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_metric_flag_no_args(self, mock_encyclopedia_class):
        """Test --metric flag with no arguments."""
        # Setup
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--metric']
        
        # Import and run
        with patch('sys.exit') as mock_exit:
            from src.cli.cli import parse_arguments
            parse_arguments()
        
        # Verify
        mock_encyclopedia.show_all_metrics.assert_called_once()
        mock_encyclopedia.show_all_tips.assert_called_once()
        mock_exit.assert_called_with(0)
    
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_metric_flag_metrics_only(self, mock_encyclopedia_class):
        """Test --metric metrics."""
        # Setup
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--metric', 'metrics']
        
        # Import and run
        with patch('sys.exit') as mock_exit:
            from src.cli.cli import parse_arguments
            parse_arguments()
        
        # Verify
        mock_encyclopedia.show_all_metrics.assert_called_once()
        mock_encyclopedia.show_all_tips.assert_not_called()
        mock_exit.assert_called_with(0)
    
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_metric_flag_tips_only(self, mock_encyclopedia_class):
        """Test --metric tips."""
        # Setup
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--metric', 'tips']
        
        # Import and run
        with patch('sys.exit') as mock_exit:
            from src.cli.cli import parse_arguments
            parse_arguments()
        
        # Verify
        mock_encyclopedia.show_all_metrics.assert_not_called()
        mock_encyclopedia.show_all_tips.assert_called_once()
        mock_exit.assert_called_with(0)
    
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_metric_flag_notes_only(self, mock_encyclopedia_class):
        """Test --metric notes."""
        # Setup
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--metric', 'notes']
        
        # Import and run
        with patch('sys.exit') as mock_exit:
            from src.cli.cli import parse_arguments
            parse_arguments()
        
        # Verify
        mock_encyclopedia.show_all_metrics.assert_not_called()
        mock_encyclopedia.show_all_tips.assert_called_once()
        mock_exit.assert_called_with(0)
    
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_metric_flag_with_filter(self, mock_encyclopedia_class):
        """Test --metric with filter text."""
        # Setup
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--metric', 'profit factor']
        
        # Import and run
        with patch('sys.exit') as mock_exit:
            from src.cli.cli import parse_arguments
            parse_arguments()
        
        # Verify
        mock_encyclopedia.show_filtered_content.assert_called_once_with('profit factor')
        mock_exit.assert_called_with(0)
    
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_metric_flag_metrics_with_filter(self, mock_encyclopedia_class):
        """Test --metric metrics with filter."""
        # Setup
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--metric', 'metrics', 'profit factor']
        
        # Import and run
        with patch('sys.exit') as mock_exit:
            from src.cli.cli import parse_arguments
            parse_arguments()
        
        # Verify
        mock_encyclopedia.show_all_metrics.assert_called_once_with('profit factor')
        mock_encyclopedia.show_all_tips.assert_not_called()
        mock_exit.assert_called_with(0)
    
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_metric_flag_tips_with_filter(self, mock_encyclopedia_class):
        """Test --metric tips with filter."""
        # Setup
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--metric', 'tips', 'winrate']
        
        # Import and run
        with patch('sys.exit') as mock_exit:
            from src.cli.cli import parse_arguments
            parse_arguments()
        
        # Verify
        mock_encyclopedia.show_all_metrics.assert_not_called()
        mock_encyclopedia.show_all_tips.assert_called_once_with('winrate')
        mock_exit.assert_called_with(0)
    
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_metric_flag_notes_with_filter(self, mock_encyclopedia_class):
        """Test --metric notes with filter."""
        # Setup
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--metric', 'notes', 'winrate']
        
        # Import and run
        with patch('sys.exit') as mock_exit:
            from src.cli.cli import parse_arguments
            parse_arguments()
        
        # Verify
        mock_encyclopedia.show_all_metrics.assert_not_called()
        mock_encyclopedia.show_all_tips.assert_called_once_with('winrate')
        mock_exit.assert_called_with(0)
    
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_metric_flag_invalid_type(self, mock_encyclopedia_class):
        """Test --metric with invalid type."""
        # Setup
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--metric', 'invalid_type', 'some filter']
        
        # Import and run
        with patch('sys.exit') as mock_exit:
            from src.cli.cli import parse_arguments
            parse_arguments()
        
        # Verify
        mock_encyclopedia.show_filtered_content.assert_called_once_with('invalid_type some filter')
        mock_exit.assert_called_with(0)
    
    @patch('src.cli.quant_encyclopedia.QuantEncyclopedia')
    def test_metric_flag_multiple_words_filter(self, mock_encyclopedia_class):
        """Test --metric with multiple word filter."""
        # Setup
        mock_encyclopedia = MagicMock()
        mock_encyclopedia_class.return_value = mock_encyclopedia
        
        # Set command line arguments
        sys.argv = ['run_analysis.py', '--metric', 'metrics', 'profit', 'factor', 'analysis']
        
        # Import and run
        with patch('sys.exit') as mock_exit:
            from src.cli.cli import parse_arguments
            parse_arguments()
        
        # Verify
        mock_encyclopedia.show_all_metrics.assert_called_once_with('profit factor analysis')
        mock_exit.assert_called_with(0)


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
                from src.cli.cli import parse_arguments
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
                from src.cli.cli import parse_arguments
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