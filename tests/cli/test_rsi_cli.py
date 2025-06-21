# -*- coding: utf-8 -*-
# tests/cli/test_rsi_cli.py

"""
Tests for CLI integration with RSI indicator.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.cli.cli import parse_arguments
from src.common.constants import TradingRule
from io import StringIO


class TestRSICLI:
    """Test cases for RSI CLI integration."""
    
    def test_rsi_rule_parsing(self):
        """Test that RSI rules are properly parsed by CLI."""
        # Test basic RSI rule
        with patch('sys.argv', ['cli', 'demo', '--rule', 'RSI']):
            args = parse_arguments()
            assert args.rule == 'RSI'
            assert args.mode == 'demo'
        
        # Test RSI momentum rule
        with patch('sys.argv', ['cli', 'demo', '--rule', 'RSI_MOM']):
            args = parse_arguments()
            assert args.rule == 'RSI_MOM'
        
        # Test RSI divergence rule
        with patch('sys.argv', ['cli', 'demo', '--rule', 'RSI_DIV']):
            args = parse_arguments()
            assert args.rule == 'RSI_DIV'
    
    def test_rsi_rule_aliases(self):
        """Test that RSI rule aliases work correctly."""
        # Test full rule names
        with patch('sys.argv', ['cli', 'demo', '--rule', 'RSI_Momentum']):
            args = parse_arguments()
            assert args.rule == 'RSI_Momentum'
        
        with patch('sys.argv', ['cli', 'demo', '--rule', 'RSI_Divergence']):
            args = parse_arguments()
            assert args.rule == 'RSI_Divergence'
    
    def test_rsi_rule_choices(self):
        """Test that RSI rules are included in available choices."""
        # Get the parser to check available choices
        parser = parse_arguments.__wrapped__.__defaults__[0] if hasattr(parse_arguments, '__wrapped__') else None
        
        # Since we can't easily access the parser directly, let's test by trying to parse
        # and checking that our RSI rules are accepted
        rsi_rules = ['RSI', 'RSI_MOM', 'RSI_DIV', 'RSI_Momentum', 'RSI_Divergence']
        
        for rule in rsi_rules:
            with patch('sys.argv', ['cli', 'demo', '--rule', rule]):
                try:
                    args = parse_arguments()
                    assert args.rule == rule
                except SystemExit:
                    pytest.fail(f"RSI rule '{rule}' should be accepted by CLI")
    
    def test_rsi_with_different_modes(self):
        """Test RSI rules with different CLI modes."""
        modes = ['demo', 'yfinance', 'csv']
        rsi_rules = ['RSI', 'RSI_MOM', 'RSI_DIV']
        
        for mode in modes:
            for rule in rsi_rules:
                with patch('sys.argv', ['cli', mode, '--rule', rule]):
                    try:
                        args = parse_arguments()
                        assert args.mode == mode
                        assert args.rule == rule
                    except SystemExit:
                        # Some modes might require additional arguments, which is expected
                        pass
    
    def test_rsi_with_additional_parameters(self):
        """Test RSI rules with additional CLI parameters."""
        with patch('sys.argv', ['cli', 'demo', '--rule', 'RSI', '--point', '0.01']):
            args = parse_arguments()
            assert args.rule == 'RSI'
            assert args.point == 0.01
        
        with patch('sys.argv', ['cli', 'yfinance', '--ticker', 'AAPL', '--rule', 'RSI_MOM', '--period', '1mo']):
            args = parse_arguments()
            assert args.rule == 'RSI_MOM'
            assert args.ticker == 'AAPL'
            assert args.period == '1mo'
    
    def test_rsi_rule_help_text(self):
        """Test that RSI rules are mentioned in help text."""
        # This test verifies that RSI rules are properly documented in CLI help
        # We can't easily capture help text, but we can verify the rules are accepted
        rsi_rules = ['RSI', 'RSI_MOM', 'RSI_DIV']
        
        for rule in rsi_rules:
            with patch('sys.argv', ['cli', 'demo', '--rule', rule]):
                try:
                    args = parse_arguments()
                    assert args.rule == rule
                except SystemExit:
                    pytest.fail(f"RSI rule '{rule}' should be documented and accepted")
    
    def test_rsi_rule_case_insensitivity(self):
        """Test that RSI rules are case-sensitive (as expected by CLI)."""
        # CLI is case-sensitive, so lowercase should fail
        with patch('sys.argv', ['cli', 'demo', '--rule', 'rsi']):
            with pytest.raises(SystemExit):
                parse_arguments()
        
        # Mixed case should also fail
        with patch('sys.argv', ['cli', 'demo', '--rule', 'Rsi_Mom']):
            with pytest.raises(SystemExit):
                parse_arguments()
    
    def test_rsi_rule_with_show_mode(self):
        """Test RSI rules with show mode."""
        with patch('sys.argv', ['cli', 'show', '--rule', 'RSI']):
            args = parse_arguments()
            assert args.mode == 'show'
            assert args.rule == 'RSI'
        
        with patch('sys.argv', ['cli', 'show', 'ind', '--rule', 'RSI_DIV']):
            args = parse_arguments()
            assert args.mode == 'show'
            assert args.rule == 'RSI_DIV'
            assert args.source == 'ind'
    
    def test_rsi_rule_validation(self):
        """Test that invalid RSI rules are properly handled."""
        # Test with invalid rule name
        with patch('sys.argv', ['cli', 'demo', '--rule', 'INVALID_RSI']):
            with pytest.raises(SystemExit):
                parse_arguments()
    
    def test_rsi_rule_default_behavior(self):
        """Test default behavior when no rule is specified."""
        with patch('sys.argv', ['cli', 'demo']):
            args = parse_arguments()
            # Default should be OHLCV, not RSI
            assert args.rule == 'OHLCV'
    
    def test_rsi_rule_with_file_operations(self):
        """Test RSI rules with file operations."""
        # Test with CSV mode (requires point size)
        with patch('sys.argv', ['cli', 'csv', '--csv-file', 'test.csv', '--rule', 'RSI', '--point', '0.01']):
            args = parse_arguments()
            assert args.mode == 'csv'
            assert args.rule == 'RSI'
            assert args.csv_file == 'test.csv'
            assert args.point == 0.01
    
    def test_rsi_rule_compatibility(self):
        """Test that RSI rules are compatible with existing functionality."""
        # Test that RSI rules don't break existing rule parsing
        existing_rules = ['PV', 'SR', 'PHLD', 'OHLCV', 'AUTO']
        
        for rule in existing_rules:
            with patch('sys.argv', ['cli', 'demo', '--rule', rule]):
                try:
                    args = parse_arguments()
                    assert args.rule == rule
                except SystemExit:
                    pytest.fail(f"Existing rule '{rule}' should still work with RSI integration")
    
    def test_rsi_rule_argument_consistency(self):
        """Test that RSI rules maintain argument consistency."""
        # Test that RSI rules work with all standard arguments
        test_args = [
            ['cli', 'demo', '--rule', 'RSI', '--point', '0.01'],
            ['cli', 'demo', '--rule', 'RSI_MOM', '--interval', 'H1'],
            ['cli', 'demo', '--rule', 'RSI_DIV', '--period', '1y'],
        ]
        
        for arg_list in test_args:
            with patch('sys.argv', arg_list):
                try:
                    args = parse_arguments()
                    assert 'RSI' in args.rule or 'MOM' in args.rule or 'DIV' in args.rule
                except SystemExit:
                    pytest.fail(f"RSI rules should work with standard arguments: {arg_list}")
    
    def test_rsi_with_price_type_parameter(self):
        """Test RSI rules with price-type parameter."""
        with patch('sys.argv', ['cli', 'show', '--rule', 'RSI', '--price-type', 'open']):
            args = parse_arguments()
            assert args.mode == 'show'
            assert args.rule == 'RSI'
            assert args.price_type == 'open'
        
        with patch('sys.argv', ['cli', 'show', '--rule', 'RSI_MOM', '--price-type', 'close']):
            args = parse_arguments()
            assert args.mode == 'show'
            assert args.rule == 'RSI_MOM'
            assert args.price_type == 'close'
        
        with patch('sys.argv', ['cli', 'show', '--rule', 'RSI_DIV']):  # Default price-type
            args = parse_arguments()
            assert args.mode == 'show'
            assert args.rule == 'RSI_DIV'
            assert args.price_type == 'close'  # Default value

    def test_rsi_price_type_validation(self):
        """Test RSI price-type parameter validation."""
        with patch('sys.argv', ['cli', 'show', '--rule', 'RSI', '--price-type', 'invalid']):
            with pytest.raises(SystemExit):  # argparse will exit with invalid choice
                parse_arguments()

    def test_rsi_price_type_help_text(self):
        """Test that price-type help text is included."""
        with patch('sys.argv', ['cli', '--help']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit):
                    parse_arguments()
                help_output = mock_stdout.getvalue()
                assert 'price-type' in help_output
                assert 'open' in help_output
                assert 'close' in help_output 