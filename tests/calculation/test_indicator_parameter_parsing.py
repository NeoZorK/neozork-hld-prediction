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
    parse_adx_parameters, parse_sar_parameters
)


class TestIndicatorParameterParsing:
    """Test cases for indicator parameter parsing functionality."""
    
    def test_parse_rsi_parameters_valid(self):
        """Test parsing valid RSI parameters."""
        indicator_name, params = parse_rsi_parameters("14,30,70,open")
        
        assert indicator_name == "rsi"
        assert params["rsi_period"] == 14
        assert params["oversold"] == 30.0
        assert params["overbought"] == 70.0
        assert params["price_type"] == "open"
    
    def test_parse_rsi_parameters_close(self):
        """Test parsing RSI parameters with close price type."""
        indicator_name, params = parse_rsi_parameters("21,25,75,close")
        
        assert indicator_name == "rsi"
        assert params["rsi_period"] == 21
        assert params["oversold"] == 25.0
        assert params["overbought"] == 75.0
        assert params["price_type"] == "close"
    
    def test_parse_rsi_parameters_invalid_count(self):
        """Test parsing RSI parameters with wrong number of parameters."""
        with pytest.raises(ValueError, match="RSI requires exactly 4 parameters"):
            parse_rsi_parameters("14,30,70")
    
    def test_parse_rsi_parameters_invalid_price_type(self):
        """Test parsing RSI parameters with invalid price type."""
        with pytest.raises(ValueError, match="RSI price_type must be 'open' or 'close'"):
            parse_rsi_parameters("14,30,70,high")
    
    def test_parse_macd_parameters_valid(self):
        """Test parsing valid MACD parameters."""
        indicator_name, params = parse_macd_parameters("8,21,5,open")
        
        assert indicator_name == "macd"
        assert params["macd_fast"] == 8
        assert params["macd_slow"] == 21
        assert params["macd_signal"] == 5
        assert params["price_type"] == "open"
    
    def test_parse_stoch_parameters_valid(self):
        """Test parsing valid Stochastic parameters."""
        indicator_name, params = parse_stoch_parameters("14,3,close")
        
        assert indicator_name == "stoch"
        assert params["stoch_k_period"] == 14
        assert params["stoch_d_period"] == 3
        assert params["price_type"] == "close"
    
    def test_parse_ema_parameters_valid(self):
        """Test parsing valid EMA parameters."""
        indicator_name, params = parse_ema_parameters("20,open")
        
        assert indicator_name == "ema"
        assert params["ema_period"] == 20
        assert params["price_type"] == "open"
    
    def test_parse_bb_parameters_valid(self):
        """Test parsing valid Bollinger Bands parameters."""
        indicator_name, params = parse_bb_parameters("20,2.5,close")
        
        assert indicator_name == "bb"
        assert params["bb_period"] == 20
        assert params["bb_std_dev"] == 2.5
        assert params["price_type"] == "close"
    
    def test_parse_atr_parameters_valid(self):
        """Test parsing valid ATR parameters."""
        indicator_name, params = parse_atr_parameters("14")
        
        assert indicator_name == "atr"
        assert params["atr_period"] == 14
    
    def test_parse_cci_parameters_valid(self):
        """Test parsing valid CCI parameters."""
        indicator_name, params = parse_cci_parameters("20,open")
        
        assert indicator_name == "cci"
        assert params["cci_period"] == 20
        assert params["price_type"] == "open"
    
    def test_parse_vwap_parameters_valid(self):
        """Test parsing valid VWAP parameters."""
        indicator_name, params = parse_vwap_parameters("close")
        
        assert indicator_name == "vwap"
        assert params["price_type"] == "close"
    
    def test_parse_pivot_parameters_valid(self):
        """Test parsing valid Pivot Points parameters."""
        indicator_name, params = parse_pivot_parameters("open")
        
        assert indicator_name == "pivot"
        assert params["price_type"] == "open"
    
    def test_parse_hma_parameters_valid(self):
        """Test parsing valid HMA parameters."""
        indicator_name, params = parse_hma_parameters("20,close")
        
        assert indicator_name == "hma"
        assert params["hma_period"] == 20
        assert params["price_type"] == "close"
    
    def test_parse_tsf_parameters_valid(self):
        """Test parsing valid TSF parameters."""
        indicator_name, params = parse_tsf_parameters("20,5,open")
        
        assert indicator_name == "tsf"
        assert params["tsf_period"] == 20
        assert params["tsf_forecast"] == 5
        assert params["price_type"] == "open"
    
    def test_parse_monte_parameters_valid(self):
        """Test parsing valid Monte Carlo parameters."""
        indicator_name, params = parse_monte_parameters("1000,252")
        
        assert indicator_name == "monte"
        assert params["monte_simulations"] == 1000
        assert params["monte_period"] == 252
    
    def test_parse_kelly_parameters_valid(self):
        """Test parsing valid Kelly Criterion parameters."""
        indicator_name, params = parse_kelly_parameters("20")
        
        assert indicator_name == "kelly"
        assert params["kelly_period"] == 20
    
    def test_parse_donchain_parameters_valid(self):
        """Test parsing valid Donchian Channels parameters."""
        indicator_name, params = parse_donchain_parameters("20")
        
        assert indicator_name == "donchain"
        assert params["donchain_period"] == 20
    
    def test_parse_fibo_parameters_valid(self):
        """Test parsing valid Fibonacci Retracements parameters."""
        indicator_name, params = parse_fibo_parameters("0.236,0.382,0.5,0.618,0.786")
        
        assert indicator_name == "fibo"
        assert params["fib_levels"] == [0.236, 0.382, 0.5, 0.618, 0.786]
    
    def test_parse_obv_parameters_valid(self):
        """Test parsing valid OBV parameters."""
        indicator_name, params = parse_obv_parameters("")
        
        assert indicator_name == "obv"
        assert params == {}
    
    def test_parse_obv_parameters_invalid(self):
        """Test parsing OBV parameters with invalid input."""
        with pytest.raises(ValueError, match="OBV does not require parameters"):
            parse_obv_parameters("20")
    
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
        indicator_name, params = parse_indicator_parameters("rsi:14,30,70,open")
        
        assert indicator_name == "rsi"
        assert params["rsi_period"] == 14
        assert params["oversold"] == 30.0
        assert params["overbought"] == 70.0
        assert params["price_type"] == "open"
    
    def test_parse_indicator_parameters_invalid_format(self):
        """Test parsing indicator with invalid format."""
        # This should raise ValueError for invalid format (wrong parameter count)
        with pytest.raises(ValueError, match="RSI requires exactly 4 parameters"):
            parse_indicator_parameters("rsi:14,30,70:open")
    
    def test_parse_indicator_parameters_unknown_indicator(self):
        """Test parsing unknown indicator."""
        indicator_name, params = parse_indicator_parameters("unknown:param1,param2")
        
        assert indicator_name == "unknown"
        assert params == {}
    
    def test_parse_indicator_parameters_error_handling(self):
        """Test error handling in parameter parsing."""
        # This should raise ValueError for invalid parameters
        with pytest.raises(ValueError, match="RSI requires exactly 4 parameters"):
            parse_indicator_parameters("rsi:invalid,params")
    
    def test_parse_indicator_parameters_edge_cases(self):
        """Test edge cases in parameter parsing."""
        # Test with whitespace
        indicator_name, params = parse_indicator_parameters(" rsi : 14 , 30 , 70 , open ")
        
        assert indicator_name == "rsi"
        assert params["rsi_period"] == 14
        assert params["oversold"] == 30.0
        assert params["overbought"] == 70.0
        assert params["price_type"] == "open"
        
        # Test with different number formats (float values for period)
        indicator_name, params = parse_indicator_parameters("rsi:14.0,30.0,70.0,open")
        
        assert indicator_name == "rsi"
        assert params["rsi_period"] == 14
        assert params["oversold"] == 30.0
        assert params["overbought"] == 70.0
        assert params["price_type"] == "open" 