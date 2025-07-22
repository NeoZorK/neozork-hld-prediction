# -*- coding: utf-8 -*-
# tests/calculation/test_indicator_parameter_parsing.py

"""
Tests for indicator parameter parsing functionality.
Tests the ability to parse parameterized indicator rules like 'rsi:14,30,70,open'.
All comments and texts in English.
"""

import pytest
from src.cli.cli import (
    parse_indicator_parameters, parse_rsi_parameters, parse_macd_parameters,
    parse_stoch_parameters, parse_ema_parameters, parse_bb_parameters,
    parse_atr_parameters, parse_cci_parameters, parse_vwap_parameters,
    parse_pivot_parameters, parse_hma_parameters, parse_tsf_parameters,
    parse_monte_parameters, parse_kelly_parameters, parse_donchain_parameters,
    parse_fibo_parameters, parse_obv_parameters, parse_stdev_parameters,
    parse_adx_parameters, parse_sar_parameters, show_indicator_help
)


class TestIndicatorParameterParsing:
    """Test cases for indicator parameter parsing functionality."""
    
    def test_parse_rsi_parameters_valid(self):
        """Test parsing valid RSI parameters."""
        indicator_name, params = parse_rsi_parameters("14,30,70,close")
        
        assert indicator_name == "rsi"
        assert params["rsi_period"] == 14
        assert params["oversold"] == 30.0
        assert params["overbought"] == 70.0
        assert params["price_type"] == "close"
    
    def test_parse_rsi_parameters_with_open(self):
        """Test parsing RSI parameters with open price type."""
        indicator_name, params = parse_rsi_parameters("21,25,75,open")
        
        assert indicator_name == "rsi"
        assert params["rsi_period"] == 21
        assert params["oversold"] == 25.0
        assert params["overbought"] == 75.0
        assert params["price_type"] == "open"
    
    def test_parse_rsi_parameters_invalid_count(self):
        """Test parsing RSI parameters with invalid count."""
        with pytest.raises(ValueError, match="RSI requires exactly 4 parameters"):
            parse_rsi_parameters("14,30,70")
    
    def test_parse_rsi_parameters_invalid_price_type(self):
        """Test parsing RSI parameters with invalid price type."""
        with pytest.raises(ValueError, match="RSI price_type must be 'open' or 'close'"):
            parse_rsi_parameters("14,30,70,invalid")
    
    def test_parse_rsi_parameters_invalid_period(self):
        """Test parsing RSI parameters with invalid period."""
        with pytest.raises(ValueError, match="RSI period must be a positive integer"):
            parse_rsi_parameters("0,30,70,close")
    
    def test_parse_rsi_parameters_invalid_thresholds(self):
        """Test parsing RSI parameters with invalid thresholds."""
        with pytest.raises(ValueError, match="RSI oversold must be between 0 and 100"):
            parse_rsi_parameters("14,-10,70,close")
    
    def test_parse_macd_parameters_valid(self):
        """Test parsing valid MACD parameters."""
        indicator_name, params = parse_macd_parameters("12,26,9,close")
        
        assert indicator_name == "macd"
        assert params["macd_fast"] == 12
        assert params["macd_slow"] == 26
        assert params["macd_signal"] == 9
        assert params["price_type"] == "close"
    
    def test_parse_stoch_parameters_valid(self):
        """Test valid Stochastic parameter parsing."""
        indicator_name, params = parse_stoch_parameters("14,3,close")
        assert indicator_name == "stoch"
        assert params == {
            'stoch_k_period': 14,
            'stoch_d_period': 3,
            'price_type': 'close'
        }
    
    def test_parse_stochastic_parameters_valid(self):
        """Test valid Stochastic (full name) parameter parsing."""
        from src.cli.cli import parse_indicator_parameters
        indicator_name, params = parse_indicator_parameters("stochastic:14,3,close")
        assert indicator_name == "stoch"
        assert params == {
            'stoch_k_period': 14,
            'stoch_d_period': 3,
            'price_type': 'close'
        }
    
    def test_stochastic_in_valid_indicators_list(self):
        """Test that 'stochastic' is in the valid_indicators list."""
        from src.cli.cli import parse_arguments
        import sys
        from io import StringIO
        
        # Temporarily redirect stderr to capture the error message
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        
        try:
            # This should not raise an error for stochastic
            sys.argv = ['run_analysis.py', 'show', 'csv', 'mn1', '--rule', 'stochastic:14,3,close']
            args = parse_arguments()
            # If we get here, stochastic is valid
            assert True
        except SystemExit:
            # Check if the error message mentions stochastic as invalid
            error_output = sys.stderr.getvalue()
            assert 'stochastic' not in error_output.lower(), f"stochastic should be valid, but got error: {error_output}"
        finally:
            sys.stderr = old_stderr
    
    def test_parse_ema_parameters_valid(self):
        """Test parsing valid EMA parameters."""
        indicator_name, params = parse_ema_parameters("20,close")
        
        assert indicator_name == "ema"
        assert params["ema_period"] == 20
        assert params["price_type"] == "close"
    
    def test_parse_bb_parameters_valid(self):
        """Test valid Bollinger Bands parameter parsing."""
        indicator_name, params = parse_bb_parameters("20,2,close")
        assert indicator_name == "bb"
        assert params == {
            'bb_period': 20,
            'bb_std_dev': 2.0,
            'price_type': 'close'
        }
    
    def test_parse_atr_parameters_valid(self):
        """Test parsing valid ATR parameters."""
        indicator_name, params = parse_atr_parameters("14")
        
        assert indicator_name == "atr"
        assert params["atr_period"] == 14
    
    def test_parse_cci_parameters_valid(self):
        """Test parsing valid CCI parameters."""
        indicator_name, params = parse_cci_parameters("20,close")
        
        assert indicator_name == "cci"
        assert params["cci_period"] == 20
        assert params["price_type"] == "close"
    
    def test_parse_vwap_parameters_valid(self):
        """Test parsing valid VWAP parameters."""
        indicator_name, params = parse_vwap_parameters("close")
        
        assert indicator_name == "vwap"
        assert params["price_type"] == "close"
    
    def test_parse_pivot_parameters_valid(self):
        """Test parsing valid Pivot Points parameters."""
        indicator_name, params = parse_pivot_parameters("close")
        
        assert indicator_name == "pivot"
        assert params["price_type"] == "close"
    
    def test_parse_hma_parameters_valid(self):
        """Test parsing valid HMA parameters."""
        indicator_name, params = parse_hma_parameters("20,close")
        
        assert indicator_name == "hma"
        assert params["hma_period"] == 20
        assert params["price_type"] == "close"
    
    def test_parse_tsf_parameters_valid(self):
        """Test valid TSF parameter parsing."""
        indicator_name, params = parse_tsf_parameters("20,close")
        assert indicator_name == "tsf"
        assert params == {
            'tsforecast_period': 20,
            'price_type': 'close'
        }
    
    def test_parse_monte_parameters_valid(self):
        """Test valid Monte Carlo parameter parsing."""
        indicator_name, params = parse_monte_parameters("1000,252")
        assert indicator_name == "monte"
        assert params == {
            'monte_simulations': 1000,
            'monte_period': 252
        }
    
    def test_parse_kelly_parameters_valid(self):
        """Test valid Kelly Criterion parameter parsing."""
        indicator_name, params = parse_kelly_parameters("20")
        assert indicator_name == "kelly"
        assert params == {
            'kelly_period': 20
        }
    
    def test_parse_donchain_parameters_valid(self):
        """Test parsing valid Donchian Channels parameters."""
        indicator_name, params = parse_donchain_parameters("20")
        
        assert indicator_name == "donchain"
        assert params["donchain_period"] == 20
    
    def test_parse_fibo_parameters_valid(self):
        """Test valid Fibonacci Retracements parameter parsing."""
        indicator_name, params = parse_fibo_parameters("0.236,0.382,0.5,0.618,0.786")
        assert indicator_name == "fibo"
        assert params == {
            'fib_levels': [0.236, 0.382, 0.5, 0.618, 0.786]
        }
    
    def test_parse_fibo_parameters_all(self):
        """Test Fibonacci Retracements parameter parsing with 'all'."""
        indicator_name, params = parse_fibo_parameters("all")
        assert indicator_name == "fibo"
        assert params == {
            'fib_levels': [0.236, 0.382, 0.5, 0.618, 0.786]
        }
    
    def test_parse_obv_parameters_valid(self):
        """Test valid OBV parameter parsing."""
        indicator_name, params = parse_obv_parameters("")
        assert indicator_name == "obv"
        assert params == {}
    
    def test_parse_stdev_parameters_valid(self):
        """Test parsing valid Standard Deviation parameters."""
        indicator_name, params = parse_stdev_parameters("20,close")
        
        assert indicator_name == "stdev"
        assert params["stdev_period"] == 20
        assert params["price_type"] == "close"
    
    def test_parse_adx_parameters_valid(self):
        """Test parsing valid ADX parameters."""
        indicator_name, params = parse_adx_parameters("14")
        
        assert indicator_name == "adx"
        assert params["adx_period"] == 14
    
    def test_parse_sar_parameters_valid(self):
        """Test parsing valid SAR parameters."""
        indicator_name, params = parse_sar_parameters("0.02,0.2")
        
        assert indicator_name == "sar"
        assert params["sar_acceleration"] == 0.02
        assert params["sar_maximum"] == 0.2
    
    def test_parse_indicator_parameters_no_params(self):
        """Test parsing indicator without parameters."""
        indicator_name, params = parse_indicator_parameters("rsi")
        
        assert indicator_name == "rsi"
        assert params == {}
    
    def test_parse_indicator_parameters_with_params(self):
        """Test parsing indicator with parameters."""
        indicator_name, params = parse_indicator_parameters("rsi:14,30,70,close")
        
        assert indicator_name == "rsi"
        assert params["rsi_period"] == 14
        assert params["oversold"] == 30.0
        assert params["overbought"] == 70.0
        assert params["price_type"] == "close"
    
    def test_parse_indicator_parameters_invalid_format(self):
        """Test parsing indicator with invalid format."""
        with pytest.raises(ValueError, match="RSI requires exactly 4 parameters"):
            parse_indicator_parameters("rsi:14:30,70,close")
    
    def test_parse_indicator_parameters_unknown_indicator(self):
        """Test parsing unknown indicator."""
        with pytest.raises(ValueError, match="Unknown indicator"):
            parse_indicator_parameters("unknown:14,30,70,close")
    
    def test_parse_indicator_parameters_error_handling(self):
        """Test error handling in parameter parsing."""
        # This should raise ValueError for invalid parameters
        with pytest.raises(ValueError, match="RSI requires exactly 4 parameters"):
            parse_indicator_parameters("rsi:invalid,params")
    
    def test_parse_indicator_parameters_edge_cases(self):
        """Test edge cases in parameter parsing."""
        # Test with whitespace
        indicator_name, params = parse_indicator_parameters(" rsi : 14 , 30 , 70 , close ")
        
        assert indicator_name == "rsi"
        assert params["rsi_period"] == 14
        assert params["oversold"] == 30.0
        assert params["overbought"] == 70.0
        assert params["price_type"] == "close"
        
        # Test with different number formats (float values for period)
        indicator_name, params = parse_indicator_parameters("rsi:14.0,30.0,70.0,close")
        
        assert indicator_name == "rsi"
        assert params["rsi_period"] == 14
        assert params["oversold"] == 30.0
        assert params["overbought"] == 70.0
        assert params["price_type"] == "close"

    def test_show_indicator_help_rsi(self):
        """Test showing help for RSI indicator."""
        # This should not raise an exception
        show_indicator_help("rsi")

    def test_show_indicator_help_unknown(self):
        """Test showing help for unknown indicator."""
        # This should not raise an exception and should show generic help
        show_indicator_help("unknown")


class TestErrorHandling:
    """Test cases for error handling and help display."""

    def test_rsi_missing_parameters_error(self):
        """Test RSI error handling with missing parameters."""
        with pytest.raises(ValueError, match="RSI requires exactly 4 parameters"):
            parse_rsi_parameters("14,30,70")

    def test_rsi_invalid_price_type_error(self):
        """Test RSI error handling with invalid price type."""
        with pytest.raises(ValueError, match="RSI price_type must be 'open' or 'close'"):
            parse_rsi_parameters("14,30,70,invalid")

    def test_macd_invalid_parameter_count(self):
        """Test MACD error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="MACD requires exactly 4 parameters"):
            parse_macd_parameters("12,26")

    def test_stoch_invalid_parameter_count(self):
        """Test Stochastic error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="Stochastic requires exactly 3 parameters"):
            parse_stoch_parameters("14,3")

    def test_ema_invalid_parameter_count(self):
        """Test EMA error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="EMA requires exactly 2 parameters"):
            parse_ema_parameters("20")

    def test_bb_invalid_parameter_count(self):
        """Test Bollinger Bands error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="Bollinger Bands requires exactly 3 parameters"):
            parse_bb_parameters("20,2")

    def test_atr_invalid_parameter_count(self):
        """Test ATR error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="ATR requires exactly 1 parameter"):
            parse_atr_parameters("14,20")

    def test_cci_invalid_parameter_count(self):
        """Test CCI error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="CCI requires exactly 2 parameters"):
            parse_cci_parameters("20")

    def test_vwap_invalid_parameter_count(self):
        """Test VWAP error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="VWAP requires exactly 1 parameter"):
            parse_vwap_parameters("close,open")

    def test_pivot_invalid_parameter_count(self):
        """Test Pivot Points error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="Pivot Points requires exactly 1 parameter"):
            parse_pivot_parameters("close,open")

    def test_hma_invalid_parameter_count(self):
        """Test HMA error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="HMA requires exactly 2 parameters"):
            parse_hma_parameters("20")

    def test_tsf_invalid_parameter_count(self):
        """Test TSF error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="TSF requires exactly 2 parameters"):
            parse_tsf_parameters("20")

    def test_monte_invalid_parameter_count(self):
        """Test Monte Carlo error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="Invalid Monte Carlo parameters"):
            parse_monte_parameters("0,close")

    def test_kelly_invalid_parameter_count(self):
        """Test Kelly Criterion error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="Kelly Criterion requires exactly 1 parameter"):
            parse_kelly_parameters("close,open")

    def test_donchain_invalid_parameter_count(self):
        """Test Donchian Channels error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="Donchian Channels requires exactly 1 parameter"):
            parse_donchain_parameters("20,30")

    def test_fibo_invalid_parameter_count(self):
        """Test Fibonacci Retracements error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="Invalid Fibonacci Retracements parameters"):
            parse_fibo_parameters("close,open")

    def test_obv_invalid_parameter_count(self):
        """Test OBV error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="OBV does not require parameters"):
            parse_obv_parameters("close,open")

    def test_stdev_invalid_parameter_count(self):
        """Test Standard Deviation error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="Standard Deviation requires exactly 2 parameters"):
            parse_stdev_parameters("20")

    def test_adx_invalid_parameter_count(self):
        """Test ADX error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="ADX requires exactly 1 parameter"):
            parse_adx_parameters("14,20")

    def test_sar_invalid_parameter_count(self):
        """Test SAR error handling with wrong parameter count."""
        with pytest.raises(ValueError, match="SAR requires exactly 2 parameters"):
            parse_sar_parameters("0.02")

    def test_tsf_invalid_price_type(self):
        """Test TSF price type validation."""
        with pytest.raises(ValueError, match="TSF price_type must be 'open' or 'close'"):
            parse_tsf_parameters("20,invalid")


class TestParameterValidation:
    """Test cases for parameter validation."""

    def test_rsi_invalid_price_type(self):
        """Test RSI price type validation."""
        with pytest.raises(ValueError, match="RSI price_type must be 'open' or 'close'"):
            parse_rsi_parameters("14,30,70,invalid")

    def test_macd_invalid_price_type(self):
        """Test MACD price type validation."""
        with pytest.raises(ValueError, match="MACD price_type must be 'open' or 'close'"):
            parse_macd_parameters("12,26,9,invalid")

    def test_stoch_invalid_price_type(self):
        """Test Stochastic price type validation."""
        with pytest.raises(ValueError, match="Stochastic price_type must be 'open' or 'close'"):
            parse_stoch_parameters("14,3,invalid")

    def test_ema_invalid_price_type(self):
        """Test EMA price type validation."""
        with pytest.raises(ValueError, match="EMA price_type must be 'open' or 'close'"):
            parse_ema_parameters("20,invalid")

    def test_bb_invalid_price_type(self):
        """Test Bollinger Bands price type validation."""
        with pytest.raises(ValueError, match="Bollinger Bands price_type must be 'open' or 'close'"):
            parse_bb_parameters("20,2,invalid")

    def test_cci_invalid_price_type(self):
        """Test CCI price type validation."""
        with pytest.raises(ValueError, match="CCI price_type must be 'open' or 'close'"):
            parse_cci_parameters("20,invalid")

    def test_vwap_invalid_price_type(self):
        """Test VWAP price type validation."""
        with pytest.raises(ValueError, match="VWAP price_type must be 'open' or 'close'"):
            parse_vwap_parameters("invalid")

    def test_pivot_invalid_price_type(self):
        """Test Pivot Points price type validation."""
        with pytest.raises(ValueError, match="Pivot Points price_type must be 'open' or 'close'"):
            parse_pivot_parameters("invalid")

    def test_hma_invalid_price_type(self):
        """Test HMA price type validation."""
        with pytest.raises(ValueError, match="HMA price_type must be 'open' or 'close'"):
            parse_hma_parameters("20,invalid")

    def test_tsf_invalid_price_type(self):
        """Test TSF price type validation."""
        with pytest.raises(ValueError, match="TSF price_type must be 'open' or 'close'"):
            parse_tsf_parameters("20,invalid")

    def test_stdev_invalid_price_type(self):
        """Test Standard Deviation price type validation."""
        with pytest.raises(ValueError, match="Standard Deviation price_type must be 'open' or 'close'"):
            parse_stdev_parameters("20,invalid") 