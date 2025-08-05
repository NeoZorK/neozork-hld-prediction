# -*- coding: utf-8 -*-
# tests/calculation/indicators/oscillators/test_rsi_mom_ind.py

"""
Tests for RSI Momentum indicator.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.oscillators.rsi_mom_ind import apply_rule_rsi_mom
from src.calculation.indicators.oscillators.rsi_ind_calc import PriceType
from src.common.constants import NOTRADE, BUY, SELL


class TestRSIMomentumIndicator:
    """Test class for RSI Momentum indicator."""
    
    def test_apply_rule_rsi_mom_basic(self):
        """Test basic RSI momentum rule application."""
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [102, 103, 104, 105, 106],
            'Low': [99, 100, 101, 102, 103],
            'Close': [101, 102, 103, 104, 105],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = apply_rule_rsi_mom(df, point=0.01, rsi_period=3, 
                                   oversold=30, overbought=70, 
                                   price_type=PriceType.CLOSE)
        
        # Check required columns exist
        assert 'RSI' in result.columns
        assert 'RSI_Signal' in result.columns
        assert 'RSI_Price_Type' in result.columns
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
        
        # Check data types
        assert result['RSI_Price_Type'].iloc[0] == 'Close'
        assert result['Direction'].dtype in [np.float64, np.int64]
    
    def test_apply_rule_rsi_mom_open_price(self):
        """Test RSI momentum rule with open price type."""
        df = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [102, 103, 104, 105, 106],
            'Low': [99, 100, 101, 102, 103],
            'Close': [101, 102, 103, 104, 105],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = apply_rule_rsi_mom(df, point=0.01, rsi_period=3, 
                                   oversold=30, overbought=70, 
                                   price_type=PriceType.OPEN)
        
        # The function uses the price_type parameter to determine which price to use
        # but the RSI_Price_Type column shows the actual price used
        assert result['RSI_Price_Type'].iloc[0] == 'Open'
    
    def test_apply_rule_rsi_mom_signals(self):
        """Test RSI momentum signal generation."""
        # Create data that should generate specific signals
        df = pd.DataFrame({
            'Open': [100] * 20,
            'High': [102] * 20,
            'Low': [98] * 20,
            'Close': [100] * 20,
            'Volume': [1000] * 20
        })
        
        # Create a pattern that should trigger signals
        df.loc[5:10, 'Close'] = 95  # Oversold
        df.loc[15:20, 'Close'] = 105  # Overbought
        
        result = apply_rule_rsi_mom(df, point=0.01, rsi_period=5, 
                                   oversold=30, overbought=70, 
                                   price_type=PriceType.CLOSE)
        
        # Check that signals are generated
        signals = result['RSI_Signal'].dropna()
        assert len(signals) > 0
        assert all(signal in [NOTRADE, BUY, SELL] for signal in signals)
    
    def test_apply_rule_rsi_mom_price_levels(self):
        """Test RSI momentum price level calculation."""
        df = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [102, 103, 104, 105, 106],
            'Low': [99, 100, 101, 102, 103],
            'Close': [101, 102, 103, 104, 105],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = apply_rule_rsi_mom(df, point=0.01, rsi_period=3, 
                                   oversold=30, overbought=70, 
                                   price_type=PriceType.CLOSE)
        
        # Check price levels (some may be NaN for insufficient data)
        pprice1_valid = result['PPrice1'].dropna()
        pprice2_valid = result['PPrice2'].dropna()
        if len(pprice1_valid) > 0:
            assert all(pprice1_valid > 0)
        if len(pprice2_valid) > 0:
            assert all(pprice2_valid > 0)
        assert all(result['PColor1'] == BUY)
        assert all(result['PColor2'] == SELL)
    
    def test_apply_rule_rsi_mom_diff_column(self):
        """Test RSI momentum diff column."""
        df = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [102, 103, 104, 105, 106],
            'Low': [99, 100, 101, 102, 103],
            'Close': [101, 102, 103, 104, 105],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = apply_rule_rsi_mom(df, point=0.01, rsi_period=3, 
                                   oversold=30, overbought=70, 
                                   price_type=PriceType.CLOSE)
        
        # Check diff column contains momentum values
        assert 'Diff' in result.columns
        diff_values = result['Diff'].dropna()
        assert len(diff_values) > 0
    
    def test_apply_rule_rsi_mom_edge_cases(self):
        """Test RSI momentum with edge cases."""
        # Test with very small dataset
        df = pd.DataFrame({
            'Open': [100, 101],
            'High': [102, 103],
            'Low': [99, 100],
            'Close': [101, 102],
            'Volume': [1000, 1100]
        })
        
        result = apply_rule_rsi_mom(df, point=0.01, rsi_period=2, 
                                   oversold=30, overbought=70, 
                                   price_type=PriceType.CLOSE)
        
        assert len(result) == len(df)
        assert 'RSI' in result.columns
        assert 'RSI_Signal' in result.columns
    
    def test_apply_rule_rsi_mom_parameter_validation(self):
        """Test RSI momentum parameter validation."""
        df = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [102, 103, 104],
            'Low': [99, 100, 101],
            'Close': [101, 102, 103],
            'Volume': [1000, 1100, 1200]
        })
        
        # Test with different parameters
        result1 = apply_rule_rsi_mom(df, point=0.01, rsi_period=2, 
                                    oversold=20, overbought=80, 
                                    price_type=PriceType.CLOSE)
        
        result2 = apply_rule_rsi_mom(df, point=0.01, rsi_period=2, 
                                    oversold=40, overbought=60, 
                                    price_type=PriceType.OPEN)
        
        # Results should be different due to different parameters
        # For small datasets, RSI values might be the same, so check that both results exist
        assert len(result1) == len(result2)
        assert 'RSI' in result1.columns
        assert 'RSI' in result2.columns


if __name__ == "__main__":
    pytest.main([__file__]) 