# -*- coding: utf-8 -*-
# tests/cli/test_wave_mpl_cli.py

"""
Tests for Wave indicator CLI commands with -d mpl parameter.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import tempfile
import os

from src.calculation.indicators.trend.wave_ind import (
    apply_rule_wave, WaveParameters, ENUM_MOM_TR, ENUM_GLOBAL_TR
)


class TestWaveMplCLI:
    """Test cases for Wave indicator CLI commands with -d mpl parameter."""

    @pytest.fixture
    def sample_csv_data(self):
        """Create sample CSV data for testing."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = {
            'DateTime': dates,
            'Open': np.random.uniform(100, 200, 100),
            'High': np.random.uniform(200, 300, 100),
            'Low': np.random.uniform(50, 100, 100),
            'Close': np.random.uniform(100, 200, 100),
            'Volume': np.random.uniform(1000, 10000, 100)
        }
        df = pd.DataFrame(data)
        
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            temp_file = f.name
        
        yield temp_file
        
        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)

    def test_wave_cli_mpl_basic_command(self, sample_csv_data):
        """Test basic wave CLI command with -d mpl."""
        from src.cli.cli import parse_wave_parameters
        
        # Test parameter parsing
        param_str = "339,10,2,fast,22,11,4,fast,prime,22,open"
        indicator_name, params = parse_wave_parameters(param_str)
        
        assert indicator_name == 'wave'
        assert params['long1'] == 339
        assert params['fast1'] == 10
        assert params['trend1'] == 2
        assert params['tr1'] == ENUM_MOM_TR.TR_Fast
        assert params['long2'] == 22
        assert params['fast2'] == 11
        assert params['trend2'] == 4
        assert params['tr2'] == ENUM_MOM_TR.TR_Fast
        assert params['global_tr'] == ENUM_GLOBAL_TR.G_TR_PRIME
        assert params['sma_period'] == 22
        assert params['price_type'] == 'open'

    def test_wave_cli_mpl_parameter_parsing(self):
        """Test wave CLI parameter parsing for mpl mode."""
        from src.cli.cli import parse_wave_parameters
        
        # Test different parameter combinations
        test_cases = [
            ("339,10,2,fast,22,11,4,fast,prime,22,open", "Fast", "Fast", "Prime", "open"),
            ("100,5,1,zone,50,25,2,strongtrend,reverse,50,close", "Zone Plus/Minus", "Strong Trend", "Reverse", "close"),
            ("200,20,3,weaktrend,100,50,5,betterfast,primezone,30,open", "Weak Trend", "Better Fast", "Prime Zone", "open"),
        ]
        
        for param_str, expected_tr1, expected_tr2, expected_global_tr, expected_price_type in test_cases:
            indicator_name, params = parse_wave_parameters(param_str)
            
            assert indicator_name == 'wave'
            assert params['tr1'].value == expected_tr1
            assert params['tr2'].value == expected_tr2
            assert params['global_tr'].value == expected_global_tr
            assert params['price_type'] == expected_price_type

    def test_wave_cli_mpl_invalid_parameters(self):
        """Test error handling in wave CLI commands for mpl mode."""
        from src.cli.cli import parse_wave_parameters
        
        # Test invalid parameter count
        with pytest.raises(ValueError, match="Wave requires exactly 11 parameters"):
            parse_wave_parameters("339,10,2,fast,22,11,4,fast,prime,22")
        
        # Test invalid trading rule
        with pytest.raises(ValueError, match="Invalid tr1 value"):
            parse_wave_parameters("339,10,2,invalid,22,11,4,fast,prime,22,open")
        
        # Test invalid global rule
        with pytest.raises(ValueError, match="Invalid global_tr value"):
            parse_wave_parameters("339,10,2,fast,22,11,4,fast,invalid,22,open")
        
        # Test invalid price type
        with pytest.raises(ValueError, match="Wave price_type must be 'open' or 'close'"):
            parse_wave_parameters("339,10,2,fast,22,11,4,fast,prime,22,invalid")

    def test_wave_cli_mpl_all_trading_rules(self):
        """Test all trading rules work with mpl mode."""
        from src.cli.cli import parse_wave_parameters
        
        trading_rules = [
            'fast', 'zone', 'strongtrend', 'weaktrend', 'fastzonereverse',
            'bettertrend', 'betterfast', 'rost', 'trendrost', 'bettertrendrost'
        ]
        
        for tr in trading_rules:
            param_str = f"339,10,2,{tr},22,11,4,{tr},prime,22,open"
            indicator_name, params = parse_wave_parameters(param_str)
            assert indicator_name == 'wave'
            assert params['tr1'] == params['tr2']

    def test_wave_cli_mpl_all_global_rules(self):
        """Test all global rules work with mpl mode."""
        from src.cli.cli import parse_wave_parameters
        
        global_rules = [
            ('prime', 'Prime'),
            ('reverse', 'Reverse'),
            ('primezone', 'Prime Zone'),
            ('reversezone', 'Reverse Zone'),
            ('newzone', 'New Zone'),
            ('longzone', 'Long Zone'),
            ('longzonereverse', 'Long Zone Reverse')
        ]
        
        for global_tr, expected_value in global_rules:
            param_str = f"339,10,2,fast,22,11,4,fast,{global_tr},22,open"
            indicator_name, params = parse_wave_parameters(param_str)
            assert indicator_name == 'wave'
            assert params['global_tr'].value == expected_value

    def test_wave_cli_mpl_period_combinations(self):
        """Test different period combinations work with mpl mode."""
        from src.cli.cli import parse_wave_parameters
        
        period_combinations = [
            (100, 5, 1, 50, 25, 2, 30),
            (200, 20, 3, 100, 50, 5, 50),
            (500, 50, 10, 250, 125, 20, 100),
        ]
        
        for long1, fast1, trend1, long2, fast2, trend2, sma_period in period_combinations:
            param_str = f"{long1},{fast1},{trend1},fast,{long2},{fast2},{trend2},fast,prime,{sma_period},open"
            indicator_name, params = parse_wave_parameters(param_str)
            
            assert indicator_name == 'wave'
            assert params['long1'] == long1
            assert params['fast1'] == fast1
            assert params['trend1'] == trend1
            assert params['long2'] == long2
            assert params['fast2'] == fast2
            assert params['trend2'] == trend2
            assert params['sma_period'] == sma_period

    def test_wave_cli_mpl_price_types(self):
        """Test both price types work with mpl mode."""
        from src.cli.cli import parse_wave_parameters
        
        for price_type in ['open', 'close']:
            param_str = f"339,10,2,fast,22,11,4,fast,prime,22,{price_type}"
            indicator_name, params = parse_wave_parameters(param_str)
            assert indicator_name == 'wave'
            assert params['price_type'] == price_type

    def test_wave_cli_mpl_complex_combinations(self):
        """Test complex parameter combinations work with mpl mode."""
        from src.cli.cli import parse_wave_parameters
        
        complex_combinations = [
            "339,10,2,strongtrend,22,11,4,weaktrend,reverse,22,open",
            "200,20,3,bettertrend,100,50,5,betterfast,primezone,50,close",
            "500,50,10,rost,250,125,20,trendrost,newzone,100,open",
        ]
        
        for param_str in complex_combinations:
            indicator_name, params = parse_wave_parameters(param_str)
            assert indicator_name == 'wave'
            assert all(key in params for key in ['long1', 'fast1', 'trend1', 'tr1', 
                                               'long2', 'fast2', 'trend2', 'tr2', 
                                               'global_tr', 'sma_period', 'price_type'])

    @patch('src.plotting.dual_chart_mpl.plot_dual_chart_mpl')
    def test_wave_cli_mpl_integration(self, mock_plot, sample_csv_data):
        """Test wave CLI integration with mpl mode."""
        # This test would require running the actual CLI command
        # For now, we'll test that the plotting function can be called
        mock_plot.return_value = MagicMock()
        
        # Test that the plotting function exists and can be called
        from src.plotting.dual_chart_mpl import plot_dual_chart_mpl
        assert callable(plot_dual_chart_mpl)

    def test_wave_cli_mpl_error_handling(self):
        """Test error handling in wave CLI commands for mpl mode."""
        from src.cli.cli import parse_wave_parameters
        
        # Test various error conditions
        error_cases = [
            ("", "Wave requires exactly 11 parameters"),
            ("339,10,2", "Wave requires exactly 11 parameters"),
            ("339,10,2,fast,22,11,4,fast,prime,22,open,extra", "Wave requires exactly 11 parameters"),
            ("invalid,10,2,fast,22,11,4,fast,prime,22,open", "Invalid Wave parameters"),
            ("339,invalid,2,fast,22,11,4,fast,prime,22,open", "Invalid Wave parameters"),
            ("339,10,2,invalid_rule,22,11,4,fast,prime,22,open", "Invalid tr1 value"),
            ("339,10,2,fast,22,11,4,invalid_rule,prime,22,open", "Invalid tr2 value"),
            ("339,10,2,fast,22,11,4,fast,invalid_global,22,open", "Invalid global_tr value"),
            ("339,10,2,fast,22,11,4,fast,prime,22,invalid_type", "Wave price_type must be 'open' or 'close'"),
        ]
        
        for param_str, expected_error in error_cases:
            with pytest.raises(ValueError, match=expected_error):
                parse_wave_parameters(param_str)


if __name__ == "__main__":
    pytest.main([__file__])
