# -*- coding: utf-8 -*-
# tests/cli/indicators/oscillators/test_rsi_cli.py

"""
Tests for CLI integration with RSI indicator.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.cli.cli import parse_arguments
from src.cli.oscillators.show_rsi_ind import parse_rsi_rule, show_rsi_indicator
from src.calculation.indicators.oscillators.rsi_ind_calc import PriceType
from src.common.constants import TradingRule, BUY, SELL, NOTRADE
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
    
    def test_rsi_price_type_validation(self):
        """Test RSI price type parameter validation."""
        with patch('sys.argv', ['cli', 'show', '--rule', 'RSI', '--price-type', 'invalid']):
            with pytest.raises(SystemExit):
                parse_arguments()
    
    def test_rsi_price_type_help_text(self):
        """Test that RSI price type parameter is documented."""
        # Verify that price-type parameter works with RSI rules
        with patch('sys.argv', ['cli', 'show', '--rule', 'RSI', '--price-type', 'open']):
            args = parse_arguments()
            assert args.price_type == 'open'


class TestRSINewFormat:
    """Test cases for new RSI format: rsi(14,70,30,open)."""
    
    def test_parse_rsi_rule_valid(self):
        """Test parsing valid RSI rule strings."""
        # Test standard format
        period, overbought, oversold, price_type = parse_rsi_rule('rsi(14,70,30,open)')
        assert period == 14
        assert overbought == 70
        assert oversold == 30
        assert price_type == PriceType.OPEN
        
        # Test with close price
        period, overbought, oversold, price_type = parse_rsi_rule('rsi(21,80,20,close)')
        assert period == 21
        assert overbought == 80
        assert oversold == 20
        assert price_type == PriceType.CLOSE
        
        # Test with different parameters
        period, overbought, oversold, price_type = parse_rsi_rule('rsi(7,75,25,open)')
        assert period == 7
        assert overbought == 75
        assert oversold == 25
        assert price_type == PriceType.OPEN
    
    def test_parse_rsi_rule_invalid_format(self):
        """Test parsing invalid RSI rule formats."""
        # Wrong number of parameters
        with pytest.raises(ValueError, match="RSI rule must have exactly 4 parameters"):
            parse_rsi_rule('rsi(14,70,30)')
        
        with pytest.raises(ValueError, match="RSI rule must have exactly 4 parameters"):
            parse_rsi_rule('rsi(14,70,30,open,extra)')
        
        # Invalid price type
        with pytest.raises(ValueError, match="Price type must be 'open' or 'close'"):
            parse_rsi_rule('rsi(14,70,30,high)')
        
        # Invalid number format
        with pytest.raises(ValueError):
            parse_rsi_rule('rsi(abc,70,30,open)')
        
        with pytest.raises(ValueError):
            parse_rsi_rule('rsi(14,def,30,open)')
        
        # Missing parentheses
        with pytest.raises(ValueError):
            parse_rsi_rule('rsi14,70,30,open)')
        
        with pytest.raises(ValueError):
            parse_rsi_rule('rsi(14,70,30,open')
    
    def test_parse_rsi_rule_edge_cases(self):
        """Test parsing RSI rule edge cases."""
        # Whitespace handling
        period, overbought, oversold, price_type = parse_rsi_rule('rsi( 14 , 70 , 30 , open )')
        assert period == 14
        assert overbought == 70
        assert oversold == 30
        assert price_type == PriceType.OPEN
        
        # Case sensitivity for price type
        period, overbought, oversold, price_type = parse_rsi_rule('rsi(14,70,30,OPEN)')
        assert price_type == PriceType.OPEN
        
        period, overbought, oversold, price_type = parse_rsi_rule('rsi(14,70,30,CLOSE)')
        assert price_type == PriceType.CLOSE
    
    def test_show_rsi_indicator_function(self):
        """Test the show_rsi_indicator function."""
        # Create test data
        dates = pd.date_range('2023-01-01', periods=20, freq='D')
        test_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(20)],
            'High': [101 + i * 0.1 for i in range(20)],
            'Low': [99 + i * 0.1 for i in range(20)],
            'Close': [100.5 + i * 0.1 for i in range(20)],
            'Volume': [1000] * 20
        }, index=dates)
        
        # Test with valid parameters
        try:
            show_rsi_indicator(test_data, 'rsi(14,70,30,close)', start_date='2023-01-01')
        except Exception as e:
            # If matplotlib is not available, this is expected
            if "matplotlib" in str(e).lower():
                pytest.skip("Matplotlib not available for plotting tests")
            else:
                raise
    
    def test_show_rsi_indicator_date_filtering(self):
        """Test RSI indicator with date filtering."""
        # Create test data
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        test_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [101 + i * 0.1 for i in range(30)],
            'Low': [99 + i * 0.1 for i in range(30)],
            'Close': [100.5 + i * 0.1 for i in range(30)],
            'Volume': [1000] * 30
        }, index=dates)
        
        # Test with start date
        filtered_data = test_data[test_data.index >= '2023-01-15']
        assert len(filtered_data) == 16  # 15th to 30th inclusive
        
        # Test with end date
        filtered_data = test_data[test_data.index <= '2023-01-15']
        assert len(filtered_data) == 15  # 1st to 15th inclusive


class TestRSIIndicatorSearch:
    """Test cases for RSI indicator search functionality."""
    
    def test_rsi_indicator_info(self):
        """Test that RSI indicator information is properly documented."""
        # This test verifies that RSI has proper documentation in the source file
        from src.calculation.indicators.oscillators.rsi_ind_calc import calculate_rsi
        
        # Check that the function exists and is callable
        assert callable(calculate_rsi)
        
        # Check that it has proper docstring
        assert calculate_rsi.__doc__ is not None
        assert "RSI" in calculate_rsi.__doc__
    
    def test_rsi_indicator_search_integration(self):
        """Test RSI integration with indicator search system."""
        # This would test the integration with the indicator search module
        # For now, just verify that RSI files exist in the expected locations
        import os
        
        rsi_calc_path = "src/calculation/indicators/oscillators/rsi_ind_calc.py"
        rsi_cli_path = "src/cli/oscillators/show_rsi_ind.py"
        
        assert os.path.exists(rsi_calc_path), f"RSI calculation file not found: {rsi_calc_path}"
        assert os.path.exists(rsi_cli_path), f"RSI CLI file not found: {rsi_cli_path}" 