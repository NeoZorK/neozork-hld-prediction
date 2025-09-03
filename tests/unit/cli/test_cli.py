"""
Unit tests for CLI class in CLI module.

This module tests the main command-line interface.
"""

import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

from src.cli.core.cli import CLI


class TestCLI:
    """Test cases for CLI class."""
    
    def test_init(self):
        """Test CLI initialization."""
        cli = CLI("test-cli")
        
        assert cli.name == "test-cli"
        assert cli.command_manager is not None
        assert cli.parser is not None
    
    def test_create_parser(self):
        """Test argument parser creation."""
        cli = CLI("test-cli")
        parser = cli.parser
        
        # Check that parser has expected attributes
        assert parser.prog == "neozork"
        assert "analyze" in [action.dest for action in parser._subparsers._group_actions[0]._group_actions]
        assert "train" in [action.dest for action in parser._subparsers._group_actions[0]._group_actions]
        assert "predict" in [action.dest for action in parser._subparsers._group_actions[0]._group_actions]
    
    def test_setup_commands(self):
        """Test command setup."""
        cli = CLI("test-cli")
        
        # Check that all commands are properly configured
        subparsers = cli.parser._subparsers._group_actions[0]
        command_names = [action.dest for action in subparsers._group_actions]
        
        expected_commands = ["analyze", "train", "predict", "data", "help"]
        for cmd in expected_commands:
            assert cmd in command_names
    
    def test_run_no_args(self):
        """Test CLI run with no arguments."""
        cli = CLI("test-cli")
        
        with patch('sys.argv', ['neozork']):
            result = cli.run([])
            assert result == 0
    
    def test_run_help(self):
        """Test CLI run with help flag."""
        cli = CLI("test-cli")
        
        result = cli.run(["--help"])
        assert result == 0
    
    def test_run_version(self):
        """Test CLI run with version flag."""
        cli = CLI("test-cli")
        
        result = cli.run(["--version"])
        assert result == 0
    
    def test_run_verbose(self):
        """Test CLI run with verbose flag."""
        cli = CLI("test-cli")
        
        result = cli.run(["--verbose", "--help"])
        assert result == 0
        assert cli.logger.level == 10  # DEBUG level
    
    def test_run_analyze_command(self):
        """Test CLI run with analyze command."""
        cli = CLI("test-cli")
        
        with patch.object(cli, '_execute_analyze', return_value=True):
            result = cli.run(["analyze", "--data", "test.csv"])
            assert result == 0
    
    def test_run_train_command(self):
        """Test CLI run with train command."""
        cli = CLI("test-cli")
        
        with patch.object(cli, '_execute_train', return_value=True):
            result = cli.run(["train", "--model", "rf", "--data", "train.csv"])
            assert result == 0
    
    def test_run_predict_command(self):
        """Test CLI run with predict command."""
        cli = CLI("test-cli")
        
        with patch.object(cli, '_execute_predict', return_value=True):
            result = cli.run(["predict", "--model", "model.joblib", "--data", "test.csv"])
            assert result == 0
    
    def test_run_data_command(self):
        """Test CLI run with data command."""
        cli = CLI("test-cli")
        
        with patch.object(cli, '_execute_data', return_value=True):
            result = cli.run(["data", "fetch", "--source", "api"])
            assert result == 0
    
    def test_run_help_command(self):
        """Test CLI run with help command."""
        cli = CLI("test-cli")
        
        with patch.object(cli, '_execute_help', return_value=True):
            result = cli.run(["help"])
            assert result == 0
    
    def test_run_unknown_command(self):
        """Test CLI run with unknown command."""
        cli = CLI("test-cli")
        
        result = cli.run(["unknown"])
        assert result == 1
    
    def test_execute_command_error(self):
        """Test command execution error handling."""
        cli = CLI("test-cli")
        
        with patch.object(cli, '_execute_analyze', side_effect=Exception("Test error")):
            result = cli.run(["analyze", "--data", "test.csv"])
            assert result == 1
    
    def test_keyboard_interrupt(self):
        """Test keyboard interrupt handling."""
        cli = CLI("test-cli")
        
        with patch.object(cli, '_execute_analyze', side_effect=KeyboardInterrupt()):
            result = cli.run(["analyze", "--data", "test.csv"])
            assert result == 130
    
    def test_execute_analyze(self):
        """Test analyze command execution."""
        cli = CLI("test-cli")
        args = Mock()
        args.data = "test.csv"
        
        result = cli._execute_analyze(args)
        assert result is True
    
    def test_execute_train(self):
        """Test train command execution."""
        cli = CLI("test-cli")
        args = Mock()
        args.model = "rf"
        
        result = cli._execute_train(args)
        assert result is True
    
    def test_execute_predict(self):
        """Test predict command execution."""
        cli = CLI("test-cli")
        args = Mock()
        args.model = "model.joblib"
        
        result = cli._execute_predict(args)
        assert result is True
    
    def test_execute_data(self):
        """Test data command execution."""
        cli = CLI("test-cli")
        args = Mock()
        args.operation = "fetch"
        
        result = cli._execute_data(args)
        assert result is True
    
    def test_execute_help(self):
        """Test help command execution."""
        cli = CLI("test-cli")
        args = Mock()
        args.topic = None
        
        result = cli._execute_help(args)
        assert result is True
    
    def test_execute_help_with_topic(self):
        """Test help command execution with specific topic."""
        cli = CLI("test-cli")
        args = Mock()
        args.topic = "analysis"
        
        with patch.object(cli, '_show_topic_help') as mock_show:
            result = cli._execute_help(args)
            mock_show.assert_called_once_with("analysis")
            assert result is True


class TestCLIIntegration:
    """Test cases for CLI integration."""
    
    def test_cli_with_config(self):
        """Test CLI with configuration."""
        config = {"verbose": True, "log_level": "DEBUG"}
        cli = CLI("test-cli", config)
        
        assert cli.config == config
    
    def test_cli_command_flow(self):
        """Test complete CLI command flow."""
        cli = CLI("test-cli")
        
        # Test analyze command flow
        with patch.object(cli, '_execute_analyze', return_value=True):
            result = cli.run(["analyze", "--data", "data.csv", "--indicators", "sma,rsi"])
            assert result == 0
    
    def test_cli_error_handling(self):
        """Test CLI error handling."""
        cli = CLI("test-cli")
        
        # Test with invalid arguments
        with patch('argparse.ArgumentParser.parse_args', side_effect=SystemExit(2)):
            result = cli.run(["invalid", "arguments"])
            assert result == 1
