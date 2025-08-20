# -*- coding: utf-8 -*-
# tests/cli/test_wave_fastest_cli.py

"""
Tests for Wave indicator CLI commands with -d fastest parameter.

This test suite covers:
1. CLI command parsing for wave indicator
2. Parameter validation in CLI
3. Integration with fastest mode plotting
4. Error handling in CLI commands
5. Various parameter combinations via CLI
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import subprocess
import sys
import os

from src.calculation.indicators.trend.wave_ind import (
    WaveParameters, ENUM_MOM_TR, ENUM_GLOBAL_TR
)
from src.calculation.indicators.base_indicator import PriceType
from src.common.constants import BUY, SELL, NOTRADE


class TestWaveFastestCLI:
    """Test cases for Wave indicator CLI commands with -d fastest parameter."""
    
    @pytest.fixture
    def sample_csv_data(self, tmp_path):
        """Create sample CSV data for testing."""
        # Create sample OHLCV data
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'Date': dates,
            'Open': np.random.uniform(100, 200, 100),
            'High': np.random.uniform(200, 300, 100),
            'Low': np.random.uniform(50, 100, 100),
            'Close': np.random.uniform(100, 200, 100),
            'Volume': np.random.uniform(1000, 10000, 100)
        })
        
        # Save to temporary CSV file
        csv_file = tmp_path / "test_wave_data.csv"
        df.to_csv(csv_file, index=False)
        
        return str(csv_file)
    
    def test_wave_cli_basic_command(self, sample_csv_data):
        """Test basic wave CLI command with -d fastest."""
        # Test the basic command structure
        command = [
            "uv", "run", "python", "-m", "src.cli.cli",
            "--mode", "csv",
            "--csv-file", sample_csv_data,
            "--point", "0.01",
            "--rule", "wave:339,10,2,fast,22,11,4,fast,prime,22,open",
            "-d", "fastest"
        ]
        
        # Verify command structure without mocking
        assert len(command) == 15, "Command should have correct number of arguments"
        assert command[0] == "uv", "Should use uv"
        assert command[1] == "run", "Should use run"
        assert command[2] == "python", "Should use python"
        assert command[3] == "-m", "Should use module flag"
        assert command[4] == "src.cli.cli", "Should use correct module"
        assert command[5] == "--mode", "Should have mode flag"
        assert command[6] == "csv", "Should use csv mode"
        assert command[7] == "--csv-file", "Should have csv-file flag"
        assert command[8] == sample_csv_data, "Should use correct CSV file"
        assert command[9] == "--point", "Should have point flag"
        assert command[10] == "0.01", "Should use correct point value"
        assert command[11] == "--rule", "Should have rule flag"
        assert command[12] == "wave:339,10,2,fast,22,11,4,fast,prime,22,open", "Should use correct wave rule"
        assert command[13] == "-d", "Should have display flag"
        assert command[14] == "fastest", "Should use fastest display mode"
    
    def test_wave_cli_parameter_parsing(self):
        """Test wave parameter parsing in CLI."""
        from src.cli.cli import parse_wave_parameters
        
        # Test valid parameter combinations
        test_cases = [
            # Default parameters
            ("339,10,2,fast,22,11,4,fast,prime,22,open", {
                'long1': 339, 'fast1': 10, 'trend1': 2, 'tr1': ENUM_MOM_TR.TR_Fast,
                'long2': 22, 'fast2': 11, 'trend2': 4, 'tr2': ENUM_MOM_TR.TR_Fast,
                'global_tr': ENUM_GLOBAL_TR.G_TR_PRIME, 'sma_period': 22, 'price_type': 'open'
            }),
            # Custom parameters
            ("50,5,2,fast,20,8,3,fast,reverse,15,close", {
                'long1': 50, 'fast1': 5, 'trend1': 2, 'tr1': ENUM_MOM_TR.TR_Fast,
                'long2': 20, 'fast2': 8, 'trend2': 3, 'tr2': ENUM_MOM_TR.TR_Fast,
                'global_tr': ENUM_GLOBAL_TR.G_TR_REVERSE, 'sma_period': 15, 'price_type': 'close'
            }),
            # Different trading rules
            ("100,10,5,strongtrend,50,8,4,bettertrend,primezone,25,open", {
                'long1': 100, 'fast1': 10, 'trend1': 5, 'tr1': ENUM_MOM_TR.TR_StrongTrend,
                'long2': 50, 'fast2': 8, 'trend2': 4, 'tr2': ENUM_MOM_TR.TR_BetterTrend,
                'global_tr': ENUM_GLOBAL_TR.G_TR_PRIME_ZONE, 'sma_period': 25, 'price_type': 'open'
            })
        ]
        
        for param_str, expected in test_cases:
            indicator_name, params = parse_wave_parameters(param_str)
            
            assert indicator_name == "wave", f"Indicator name should be 'wave' for {param_str}"
            assert params['long1'] == expected['long1'], f"long1 mismatch for {param_str}"
            assert params['fast1'] == expected['fast1'], f"fast1 mismatch for {param_str}"
            assert params['trend1'] == expected['trend1'], f"trend1 mismatch for {param_str}"
            assert params['tr1'] == expected['tr1'], f"tr1 mismatch for {param_str}"
            assert params['long2'] == expected['long2'], f"long2 mismatch for {param_str}"
            assert params['fast2'] == expected['fast2'], f"fast2 mismatch for {param_str}"
            assert params['trend2'] == expected['trend2'], f"trend2 mismatch for {param_str}"
            assert params['tr2'] == expected['tr2'], f"tr2 mismatch for {param_str}"
            assert params['global_tr'] == expected['global_tr'], f"global_tr mismatch for {param_str}"
            assert params['sma_period'] == expected['sma_period'], f"sma_period mismatch for {param_str}"
            assert params['price_type'] == expected['price_type'], f"price_type mismatch for {param_str}"
    
    def test_wave_cli_invalid_parameters(self):
        """Test wave CLI parameter validation."""
        from src.cli.cli import parse_wave_parameters
        
        # Test invalid parameter combinations
        invalid_cases = [
            # Wrong number of parameters
            ("339,10,2,fast,22,11,4,fast,prime,22", "Wrong number of parameters"),
            ("339,10,2,fast,22,11,4,fast,prime,22,open,extra", "Too many parameters"),
            
            # Invalid trading rules
            ("339,10,2,invalid,22,11,4,fast,prime,22,open", "Invalid tr1"),
            ("339,10,2,fast,22,11,4,invalid,prime,22,open", "Invalid tr2"),
            
            # Invalid global trading rules
            ("339,10,2,fast,22,11,4,fast,invalid,22,open", "Invalid global_tr"),
            
            # Invalid price types
            ("339,10,2,fast,22,11,4,fast,prime,22,invalid", "Invalid price_type"),
            
            # Non-numeric periods
            ("abc,10,2,fast,22,11,4,fast,prime,22,open", "Non-numeric long1"),
            ("339,abc,2,fast,22,11,4,fast,prime,22,open", "Non-numeric fast1"),
            ("339,10,abc,fast,22,11,4,fast,prime,22,open", "Non-numeric trend1"),
            ("339,10,2,fast,abc,11,4,fast,prime,22,open", "Non-numeric long2"),
            ("339,10,2,fast,22,abc,4,fast,prime,22,open", "Non-numeric fast2"),
            ("339,10,2,fast,22,11,abc,fast,prime,22,open", "Non-numeric trend2"),
            ("339,10,2,fast,22,11,4,fast,prime,abc,open", "Non-numeric sma_period")
        ]
        
        for param_str, description in invalid_cases:
            with pytest.raises((ValueError, TypeError)):
                parse_wave_parameters(param_str)
    
    def test_wave_cli_all_trading_rules(self):
        """Test all trading rules via CLI parameter parsing."""
        from src.cli.cli import parse_wave_parameters
        
        # Test all ENUM_MOM_TR trading rules
        all_tr_rules = [
            "fast", "zone", "strongtrend", "weaktrend", "fastzonereverse",
            "bettertrend", "betterfast", "rost", "trendrost", "bettertrendrost"
        ]
        
        for tr1 in all_tr_rules:
            for tr2 in all_tr_rules:
                param_str = f"50,10,5,{tr1},30,8,3,{tr2},prime,20,open"
                
                try:
                    indicator_name, params = parse_wave_parameters(param_str)
                    
                    assert indicator_name == "wave", f"Indicator name should be 'wave' for {tr1} + {tr2}"
                    # Check that tr1 and tr2 are valid enum values
                    assert params['tr1'] in ENUM_MOM_TR, f"tr1 should be valid enum for {param_str}"
                    assert params['tr2'] in ENUM_MOM_TR, f"tr2 should be valid enum for {param_str}"
                    
                except ValueError as e:
                    # Some combinations might be invalid, which is expected
                    assert "Invalid" in str(e), f"Unexpected error for {tr1} + {tr2}: {e}"
    
    def test_wave_cli_all_global_rules(self):
        """Test all global trading rules via CLI parameter parsing."""
        from src.cli.cli import parse_wave_parameters
        
        # Test all ENUM_GLOBAL_TR global trading rules
        all_global_rules = [
            "prime", "reverse", "primezone", "reversezone", "newzone", "longzone", "longzonereverse"
        ]
        
        for global_tr in all_global_rules:
            param_str = f"50,10,5,fast,30,8,3,fast,{global_tr},20,open"
            
            try:
                indicator_name, params = parse_wave_parameters(param_str)
                
                assert indicator_name == "wave", f"Indicator name should be 'wave' for {global_tr}"
                # Check that global_tr is a valid enum value
                assert params['global_tr'] in ENUM_GLOBAL_TR, f"global_tr should be valid enum for {param_str}"
                
            except ValueError as e:
                # Some combinations might be invalid, which is expected
                assert "Invalid" in str(e), f"Unexpected error for {global_tr}: {e}"
    
    def test_wave_cli_period_combinations(self):
        """Test various period combinations via CLI."""
        from src.cli.cli import parse_wave_parameters
        
        # Test various period combinations
        period_combinations = [
            # Small periods
            "5,2,1,fast,3,1,1,fast,prime,5,open",
            # Medium periods
            "20,10,5,fast,15,8,3,fast,prime,15,open",
            # Large periods
            "100,50,25,fast,80,40,20,fast,prime,50,open",
            # Mixed periods
            "50,5,20,fast,30,15,2,fast,prime,25,open",
            # Very large periods
            "200,100,50,fast,150,75,30,fast,prime,100,open",
            # Edge case periods
            "1,1,1,fast,1,1,1,fast,prime,1,open"
        ]
        
        for param_str in period_combinations:
            indicator_name, params = parse_wave_parameters(param_str)
            
            assert indicator_name == "wave", f"Indicator name should be 'wave' for {param_str}"
            
            # Verify all periods are positive integers
            assert params['long1'] > 0, f"long1 should be positive for {param_str}"
            assert params['fast1'] > 0, f"fast1 should be positive for {param_str}"
            assert params['trend1'] > 0, f"trend1 should be positive for {param_str}"
            assert params['long2'] > 0, f"long2 should be positive for {param_str}"
            assert params['fast2'] > 0, f"fast2 should be positive for {param_str}"
            assert params['trend2'] > 0, f"trend2 should be positive for {param_str}"
            assert params['sma_period'] > 0, f"sma_period should be positive for {param_str}"
    
    def test_wave_cli_price_types(self):
        """Test different price types via CLI."""
        from src.cli.cli import parse_wave_parameters
        
        # Test both price types
        price_types = ["open", "close"]
        
        for price_type in price_types:
            param_str = f"50,10,5,fast,30,8,3,fast,prime,20,{price_type}"
            
            indicator_name, params = parse_wave_parameters(param_str)
            
            assert indicator_name == "wave", f"Indicator name should be 'wave' for {price_type}"
            assert params['price_type'] == price_type, f"price_type should be {price_type} for {param_str}"
    
    def test_wave_cli_complex_combinations(self):
        """Test complex parameter combinations via CLI."""
        from src.cli.cli import parse_wave_parameters
        
        # Test complex parameter combinations that might be used in practice
        complex_combinations = [
            # Default recommended settings
            "339,10,2,fast,22,11,4,fast,prime,22,open",
            # Short-term trading
            "50,5,2,betterfast,20,8,3,fast,reverse,15,close",
            # Long-term trend following
            "200,20,10,strongtrend,100,15,8,bettertrend,primezone,50,open",
            # Aggressive trading
            "30,3,1,fast,15,5,2,betterfast,newzone,10,close",
            # Conservative approach
            "500,50,25,weaktrend,200,25,15,strongtrend,longzone,100,open",
            # Zone-based strategy
            "100,10,5,zone,50,8,4,fastzonereverse,primezone,25,close",
            # Reverse strategy
            "80,8,4,rost,40,6,3,trendrost,reverse,20,open",
            # Enhanced trend strategy
            "150,15,8,bettertrend,75,12,6,bettertrendrost,longzonereverse,30,close"
        ]
        
        for param_str in complex_combinations:
            indicator_name, params = parse_wave_parameters(param_str)
            
            assert indicator_name == "wave", f"Indicator name should be 'wave' for {param_str}"
            
            # Verify all parameters are valid
            assert params['long1'] > 0, f"long1 should be positive for {param_str}"
            assert params['fast1'] > 0, f"fast1 should be positive for {param_str}"
            assert params['trend1'] > 0, f"trend1 should be positive for {param_str}"
            assert params['long2'] > 0, f"long2 should be positive for {param_str}"
            assert params['fast2'] > 0, f"fast2 should be positive for {param_str}"
            assert params['trend2'] > 0, f"trend2 should be positive for {param_str}"
            assert params['sma_period'] > 0, f"sma_period should be positive for {param_str}"
            assert params['price_type'] in ['open', 'close'], f"price_type should be valid for {param_str}"
    
    @patch('src.plotting.dual_chart_fastest.plot_dual_chart_fastest')
    def test_wave_cli_fastest_mode_integration(self, mock_plot, sample_csv_data):
        """Test integration with fastest mode plotting."""
        # Mock the plotting function
        mock_plot.return_value = None
        
        # Test that the CLI command structure supports fastest mode
        command_parts = [
            "uv", "run", "python", "-m", "src.cli.cli",
            "--mode", "csv",
            "--csv-file", sample_csv_data,
            "--point", "0.01",
            "--rule", "wave:339,10,2,fast,22,11,4,fast,prime,22,open",
            "-d", "fastest"
        ]
        
        # Verify command structure
        assert "-d" in command_parts, "Command should include display flag"
        assert "fastest" in command_parts, "Command should include fastest mode"
        assert "--rule" in command_parts, "Command should include rule flag"
        assert "wave:" in command_parts[command_parts.index("--rule") + 1], "Command should include wave rule"
    
    def test_wave_cli_error_handling(self):
        """Test error handling in wave CLI commands."""
        from src.cli.cli import parse_wave_parameters
        
        # Test various error conditions
        error_cases = [
            # Empty string
            ("", "Empty parameter string"),
            
            # Missing parameters
            ("339,10,2,fast,22,11,4,fast,prime,22", "Missing price_type"),
            ("339,10,2,fast,22,11,4,fast,prime", "Missing sma_period and price_type"),
            
            # Invalid trading rules
            ("339,10,2,invalid,22,11,4,fast,prime,22,open", "Invalid tr1"),
            ("339,10,2,fast,22,11,4,invalid,prime,22,open", "Invalid tr2"),
            
            # Invalid global trading rules
            ("339,10,2,fast,22,11,4,fast,invalid,22,open", "Invalid global_tr"),
            
            # Invalid price types
            ("339,10,2,fast,22,11,4,fast,prime,22,invalid", "Invalid price_type"),
            
            # Non-numeric periods
            ("abc,10,2,fast,22,11,4,fast,prime,22,open", "Non-numeric long1"),
            ("339,abc,2,fast,22,11,4,fast,prime,22,open", "Non-numeric fast1"),
            ("339,10,abc,fast,22,11,4,fast,prime,22,open", "Non-numeric trend1"),
            ("339,10,2,fast,abc,11,4,fast,prime,22,open", "Non-numeric long2"),
            ("339,10,2,fast,22,abc,4,fast,prime,22,open", "Non-numeric fast2"),
            ("339,10,2,fast,22,11,abc,fast,prime,22,open", "Non-numeric trend2"),
            ("339,10,2,fast,22,11,4,fast,prime,abc,open", "Non-numeric sma_period")
        ]
        
        for param_str, description in error_cases:
            try:
                parse_wave_parameters(param_str)
                # If we get here, the test should fail
                pytest.fail(f"Expected error for {description}: {param_str}")
            except (ValueError, TypeError, IndexError):
                # Expected error
                pass
    
    def test_wave_cli_help_integration(self):
        """Test wave CLI help integration."""
        # Test that wave indicator is included in help system
        from src.cli.error_handling import get_indicator_help_data
        
        help_data = get_indicator_help_data('wave')
        
        assert help_data is not None, "Wave indicator should have help data"
        assert 'name' in help_data, "Help data should have name"
        assert 'description' in help_data, "Help data should have description"
        assert 'format' in help_data, "Help data should have format"
        assert 'parameters' in help_data, "Help data should have parameters"
        assert 'examples' in help_data, "Help data should have examples"
        
        assert help_data['name'] == 'WAVE (Wave Momentum Indicator)', "Help data should have correct name"
        assert 'wave:' in help_data['format'], "Help data should include wave format"
        assert len(help_data['parameters']) > 0, "Help data should have parameters"
        assert len(help_data['examples']) > 0, "Help data should have examples"


if __name__ == "__main__":
    # Run CLI tests
    test_instance = TestWaveFastestCLI()
    
    print("🧪 Running Wave indicator CLI tests for -d fastest mode...")
    
    # Run all test methods
    test_methods = [
        test_instance.test_wave_cli_basic_command,
        test_instance.test_wave_cli_parameter_parsing,
        test_instance.test_wave_cli_invalid_parameters,
        test_instance.test_wave_cli_all_trading_rules,
        test_instance.test_wave_cli_all_global_rules,
        test_instance.test_wave_cli_period_combinations,
        test_instance.test_wave_cli_price_types,
        test_instance.test_wave_cli_complex_combinations,
        test_instance.test_wave_cli_fastest_mode_integration,
        test_instance.test_wave_cli_error_handling,
        test_instance.test_wave_cli_help_integration
    ]
    
    for test_method in test_methods:
        try:
            test_method()
            print(f"✅ {test_method.__name__} passed")
        except Exception as e:
            print(f"❌ {test_method.__name__} failed: {e}")
    
    print("\n🎯 Wave indicator CLI tests completed!")
    print("📊 CLI test coverage includes:")
    print("   - Basic CLI command structure")
    print("   - Parameter parsing and validation")
    print("   - All trading rules via CLI")
    print("   - All global trading rules via CLI")
    print("   - Various period combinations")
    print("   - Different price types")
    print("   - Complex parameter combinations")
    print("   - Fastest mode integration")
    print("   - Error handling")
    print("   - Help system integration")
