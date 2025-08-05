# -*- coding: utf-8 -*-
# tests/plotting/test_dual_chart_rsi_variants.py

"""
Test cases for RSI variants (rsi_mom, rsi_div) in dual chart plotting.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.plotting.dual_chart_plot import (
    is_dual_chart_rule, 
    calculate_additional_indicator,
    create_dual_chart_layout
)


class TestRSIVariantsDualChart:
    """Test RSI variants in dual chart mode."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, 100),
            'High': np.random.uniform(1.1, 2.1, 100),
            'Low': np.random.uniform(0.9, 1.9, 100),
            'Close': np.random.uniform(1.0, 2.0, 100),
            'Volume': np.random.randint(1000, 10000, 100)
        }
        
        df = pd.DataFrame(data, index=dates)
        # Ensure High >= Open, Close and Low <= Open, Close
        df['High'] = df[['Open', 'Close', 'High']].max(axis=1)
        df['Low'] = df[['Open', 'Close', 'Low']].min(axis=1)
        
        return df
    
    def test_is_dual_chart_rule_rsi_mom(self):
        """Test that rsi_mom is recognized as dual chart rule."""
        rule = "rsi_mom:14,30,70,open"
        assert is_dual_chart_rule(rule) == True
    
    def test_is_dual_chart_rule_rsi_div(self):
        """Test that rsi_div is recognized as dual chart rule."""
        rule = "rsi_div:14,30,70,open"
        assert is_dual_chart_rule(rule) == True
    
    def test_is_dual_chart_rule_rsi_mom_invalid_params(self):
        """Test that rsi_mom with invalid parameters is rejected."""
        rule = "rsi_mom:14,30"  # Missing parameters
        assert is_dual_chart_rule(rule) == False
    
    def test_is_dual_chart_rule_rsi_div_invalid_params(self):
        """Test that rsi_div with invalid parameters is rejected."""
        rule = "rsi_div:14,30"  # Missing parameters
        assert is_dual_chart_rule(rule) == False
    
    def test_calculate_additional_indicator_rsi_mom(self, sample_data):
        """Test RSI momentum calculation."""
        rule = "rsi_mom:14,30,70,open"
        result = calculate_additional_indicator(sample_data, rule)
        
        # Check that required columns are added
        assert 'rsi' in result.columns
        assert 'rsi_momentum' in result.columns
        assert 'rsi_oversold' in result.columns
        assert 'rsi_overbought' in result.columns
        
        # Check that RSI momentum is calculated as difference
        assert result['rsi_momentum'].dtype in ['float64', 'float32']
        
        # Check that oversold/overbought levels are set correctly
        assert result['rsi_oversold'].iloc[0] == 30
        assert result['rsi_overbought'].iloc[0] == 70
    
    def test_calculate_additional_indicator_rsi_div(self, sample_data):
        """Test RSI divergence calculation."""
        rule = "rsi_div:14,30,70,open"
        result = calculate_additional_indicator(sample_data, rule)
        
        # Check that required columns are added
        assert 'rsi' in result.columns
        assert 'rsi_divergence' in result.columns
        assert 'rsi_oversold' in result.columns
        assert 'rsi_overbought' in result.columns
        
        # Check that RSI divergence is calculated
        assert result['rsi_divergence'].dtype in ['float64', 'float32']
        
        # Check that oversold/overbought levels are set correctly
        assert result['rsi_oversold'].iloc[0] == 30
        assert result['rsi_overbought'].iloc[0] == 70
    
    def test_create_dual_chart_layout_rsi_mom(self):
        """Test layout creation for RSI momentum."""
        rule = "rsi_mom:14,30,70,open"
        layout = create_dual_chart_layout('mpl', rule)
        
        assert layout['indicator_name'] == 'RSI Momentum with params: 14,30,70,open'
        assert layout['mode'] == 'mpl'
        assert layout['main_chart_height'] == 0.6
        assert layout['indicator_chart_height'] == 0.4
    
    def test_create_dual_chart_layout_rsi_div(self):
        """Test layout creation for RSI divergence."""
        rule = "rsi_div:14,30,70,open"
        layout = create_dual_chart_layout('mpl', rule)
        
        assert layout['indicator_name'] == 'RSI Divergence with params: 14,30,70,open'
        assert layout['mode'] == 'mpl'
        assert layout['main_chart_height'] == 0.6
        assert layout['indicator_chart_height'] == 0.4
    
    def test_rsi_mom_with_close_price(self, sample_data):
        """Test RSI momentum with close price."""
        rule = "rsi_mom:14,30,70,close"
        result = calculate_additional_indicator(sample_data, rule)
        
        assert 'rsi' in result.columns
        assert 'rsi_momentum' in result.columns
        assert result['rsi_oversold'].iloc[0] == 30
        assert result['rsi_overbought'].iloc[0] == 70
    
    def test_rsi_div_with_close_price(self, sample_data):
        """Test RSI divergence with close price."""
        rule = "rsi_div:14,30,70,close"
        result = calculate_additional_indicator(sample_data, rule)
        
        assert 'rsi' in result.columns
        assert 'rsi_divergence' in result.columns
        assert result['rsi_oversold'].iloc[0] == 30
        assert result['rsi_overbought'].iloc[0] == 70
    
    def test_rsi_mom_different_periods(self, sample_data):
        """Test RSI momentum with different periods."""
        rule = "rsi_mom:21,25,75,open"
        result = calculate_additional_indicator(sample_data, rule)
        
        assert 'rsi' in result.columns
        assert 'rsi_momentum' in result.columns
        assert result['rsi_oversold'].iloc[0] == 25
        assert result['rsi_overbought'].iloc[0] == 75
    
    def test_rsi_div_different_periods(self, sample_data):
        """Test RSI divergence with different periods."""
        rule = "rsi_div:21,25,75,open"
        result = calculate_additional_indicator(sample_data, rule)
        
        assert 'rsi' in result.columns
        assert 'rsi_divergence' in result.columns
        assert result['rsi_oversold'].iloc[0] == 25
        assert result['rsi_overbought'].iloc[0] == 75


if __name__ == "__main__":
    pytest.main([__file__]) 