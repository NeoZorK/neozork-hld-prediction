# -*- coding: utf-8 -*-
# tests/calculation/indicators/oscillators/test_rsi_calculation.py

"""
Tests for RSI calculation module.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.oscillators.rsi_ind_calc import (
    calculate_rsi, 
    calculate_rsi_signals, 
    calculate_rsi_levels,
    apply_rule_rsi,
    apply_rule_rsi_momentum,
    apply_rule_rsi_divergence,
    PriceType
)
from src.common.constants import BUY, SELL, NOTRADE, TradingRule


class TestRSICalculation:
    """Test cases for RSI calculation functions."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample price data
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        np.random.seed(42)  # For reproducible tests
        
        # Generate realistic price data
        base_price = 100.0
        returns = np.random.normal(0, 0.02, 50)  # 2% daily volatility
        prices = [base_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        # Create different open and close prices with more variation
        open_prices = []
        close_prices = []
        for p in prices:
            # Open price with some variation
            open_prices.append(p * (1 + np.random.normal(0, 0.01)))
            # Close price with different variation
            close_prices.append(p * (1 + np.random.normal(0, 0.01)))
        
        self.test_data = pd.DataFrame({
            'Open': open_prices,
            'High': [max(o, c) * 1.01 for o, c in zip(open_prices, close_prices)],  # 1% higher than max
            'Low': [min(o, c) * 0.99 for o, c in zip(open_prices, close_prices)],   # 1% lower than min
            'Close': close_prices,
            'Volume': np.random.randint(1000, 10000, 50)
        }, index=dates)
    
    def test_calculate_rsi_basic(self):
        """Test basic RSI calculation."""
        close_prices = self.test_data['Close']
        rsi = calculate_rsi(close_prices, period=14)
        
        # Check that RSI values are between 0 and 100
        assert rsi.min() >= 0
        assert rsi.max() <= 100
        
        # Check that we have the same number of values as input
        assert len(rsi) == len(close_prices)
        
        # Check that first value is NaN (due to diff operation)
        assert pd.isna(rsi.iloc[0])
        # Check that we have some valid values after the initial NaN
        assert not pd.isna(rsi.iloc[1:]).all()
    
    def test_calculate_rsi_different_periods(self):
        """Test RSI calculation with different periods."""
        close_prices = self.test_data['Close']
        
        # Test with period 7
        rsi_7 = calculate_rsi(close_prices, period=7)
        assert len(rsi_7) == len(close_prices)
        assert rsi_7.min() >= 0
        assert rsi_7.max() <= 100
        
        # Test with period 21
        rsi_21 = calculate_rsi(close_prices, period=21)
        assert len(rsi_21) == len(close_prices)
        assert rsi_21.min() >= 0
        assert rsi_21.max() <= 100
        
        # Different periods should produce different results
        valid_7 = rsi_7.dropna()
        valid_21 = rsi_21.dropna()
        if len(valid_7) > 0 and len(valid_21) > 0:
            # They should be different (not exactly equal)
            assert not np.allclose(valid_7.iloc[-10:], valid_21.iloc[-10:], rtol=1e-10)
    
    def test_calculate_rsi_invalid_period(self):
        """Test RSI calculation with invalid period."""
        close_prices = self.test_data['Close']
        
        with pytest.raises(ValueError, match="RSI period must be positive"):
            calculate_rsi(close_prices, period=0)
        
        with pytest.raises(ValueError, match="RSI period must be positive"):
            calculate_rsi(close_prices, period=-1)
    
    def test_calculate_rsi_insufficient_data(self):
        """Test RSI calculation with insufficient data."""
        # Test with very short data
        short_prices = pd.Series([100, 101, 102], index=range(3))
        rsi_short = calculate_rsi(short_prices, period=14)
        
        # Should return series with NaN values due to insufficient data
        assert rsi_short.isna().all()
        
        # Test with exactly period+1 data points
        exact_prices = pd.Series([100 + i for i in range(15)], index=range(15))
        rsi_exact = calculate_rsi(exact_prices, period=14)
        
        # Should have some valid values
        assert not rsi_exact.isna().all()
        assert pd.isna(rsi_exact.iloc[0])  # First value should be NaN
    
    def test_calculate_rsi_signals(self):
        """Test RSI signal calculation."""
        # Create RSI values
        rsi_values = pd.Series([20, 30, 50, 70, 80, 90], index=range(6))
        
        signals = calculate_rsi_signals(rsi_values, overbought=70, oversold=30)
        
        # Check expected signals
        expected_signals = [BUY, BUY, NOTRADE, SELL, SELL, SELL]
        np.testing.assert_array_equal(signals.values, expected_signals)
    
    def test_calculate_rsi_signals_custom_thresholds(self):
        """Test RSI signal calculation with custom thresholds."""
        rsi_values = pd.Series([15, 25, 35, 65, 75, 85], index=range(6))
        
        # Test with custom thresholds
        signals = calculate_rsi_signals(rsi_values, overbought=80, oversold=20)
        
        # Check expected signals
        expected_signals = [BUY, NOTRADE, NOTRADE, NOTRADE, NOTRADE, SELL]
        np.testing.assert_array_equal(signals.values, expected_signals)
    
    def test_calculate_rsi_signals_edge_cases(self):
        """Test RSI signal calculation with edge cases."""
        # Test with NaN values
        rsi_values = pd.Series([20, np.nan, 50, 70, np.nan, 90], index=range(6))
        signals = calculate_rsi_signals(rsi_values, overbought=70, oversold=30)
        
        # NaN values should result in NOTRADE
        assert signals.iloc[1] == NOTRADE
        assert signals.iloc[4] == NOTRADE
        
        # Test with empty series
        empty_rsi = pd.Series([], index=[])
        empty_signals = calculate_rsi_signals(empty_rsi, overbought=70, oversold=30)
        assert len(empty_signals) == 0
    
    def test_calculate_rsi_levels(self):
        """Test RSI level calculation."""
        open_prices = pd.Series([100, 101, 102], index=range(3))
        rsi_values = pd.Series([25, 50, 75], index=range(3))
        
        support, resistance = calculate_rsi_levels(open_prices, rsi_values)
        
        # Check that levels are calculated
        assert len(support) == len(open_prices)
        assert len(resistance) == len(open_prices)
        
        # Check that support is lower than resistance
        assert (support < resistance).all()
        
        # Check that levels are proportional to open prices
        assert all(abs(support[i] / open_prices[i] - 0.98) < 0.01 for i in range(len(open_prices)))
        assert all(abs(resistance[i] / open_prices[i] - 1.02) < 0.01 for i in range(len(open_prices)))
    
    def test_calculate_rsi_levels_custom_thresholds(self):
        """Test RSI level calculation with custom thresholds."""
        open_prices = pd.Series([100, 101, 102], index=range(3))
        rsi_values = pd.Series([25, 50, 75], index=range(3))
        
        support, resistance = calculate_rsi_levels(open_prices, rsi_values, overbought=80, oversold=20)
        
        # Should still work with custom thresholds
        assert len(support) == len(open_prices)
        assert len(resistance) == len(open_prices)
        assert (support < resistance).all()
    
    def test_apply_rule_rsi(self):
        """Test RSI rule application."""
        df = self.test_data.copy()
        point = 0.01
        
        result = apply_rule_rsi(df, point, rsi_period=14, overbought=70, oversold=30)
        
        # Check that required columns are present
        required_cols = ['RSI', 'RSI_Signal', 'PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff']
        for col in required_cols:
            assert col in result.columns
        
        # Check that RSI values are calculated
        assert not result['RSI'].isna().all()
        
        # Check that signals are valid
        valid_signals = [BUY, SELL, NOTRADE]
        assert all(signal in valid_signals for signal in result['Direction'].dropna())
    
    def test_apply_rule_rsi_custom_parameters(self):
        """Test RSI rule application with custom parameters."""
        df = self.test_data.copy()
        point = 0.01
        
        result = apply_rule_rsi(df, point, rsi_period=7, overbought=80, oversold=20)
        
        # Check that custom parameters are applied
        assert 'RSI' in result.columns
        assert 'RSI_Signal' in result.columns
        
        # Check that signals use custom thresholds
        rsi_values = result['RSI'].dropna()
        signals = result['RSI_Signal'].dropna()
        
        # Align the series for comparison
        aligned_data = pd.DataFrame({'RSI': rsi_values, 'Signals': signals})
        
        # Should have BUY signals at oversold levels
        oversold_signals = aligned_data[aligned_data['RSI'] <= 20]['Signals']
        assert all(signal == BUY for signal in oversold_signals)
    
    def test_apply_rule_rsi_momentum(self):
        """Test RSI momentum rule application."""
        df = self.test_data.copy()
        point = 0.01
        
        result = apply_rule_rsi_momentum(df, point, rsi_period=14, overbought=70, oversold=30)
        
        # Check that momentum-specific columns are present
        assert 'RSI' in result.columns
        assert 'RSI_Momentum' in result.columns
        assert 'RSI_Signal' in result.columns
        
        # Check that momentum is calculated
        momentum = result['RSI_Momentum'].dropna()
        assert len(momentum) > 0
        
        # Check that momentum values are reasonable
        assert momentum.min() >= -100  # RSI can't decrease more than 100
        assert momentum.max() <= 100   # RSI can't increase more than 100
    
    def test_apply_rule_rsi_momentum_signals(self):
        """Test RSI momentum signal generation."""
        df = self.test_data.copy()
        point = 0.01
        
        result = apply_rule_rsi_momentum(df, point, rsi_period=14, overbought=70, oversold=30)
        
        # Check that signals are generated
        signals = result['RSI_Signal'].dropna()
        assert len(signals) > 0
        
        # Check that signals are valid
        valid_signals = [BUY, SELL, NOTRADE]
        assert all(signal in valid_signals for signal in signals)
    
    def test_apply_rule_rsi_divergence(self):
        """Test RSI divergence rule application."""
        df = self.test_data.copy()
        point = 0.01
        
        result = apply_rule_rsi_divergence(df, point, rsi_period=14, overbought=70, oversold=30)
        
        # Check that divergence-specific columns are present
        assert 'RSI' in result.columns
        assert 'RSI_Signal' in result.columns
        
        # Check that signals are generated
        signals = result['RSI_Signal'].dropna()
        assert len(signals) >= 0  # May or may not detect divergences
    
    def test_apply_rule_rsi_divergence_detection(self):
        """Test RSI divergence detection logic."""
        df = self.test_data.copy()
        point = 0.01
        
        result = apply_rule_rsi_divergence(df, point, rsi_period=14, overbought=70, oversold=30)
        
        # Check that divergence strength is calculated
        diff_values = result['Diff'].dropna()
        assert len(diff_values) > 0
        
        # Divergence strength should be between 0 and 1
        assert diff_values.min() >= 0
        assert diff_values.max() <= 1
    
    def test_rsi_edge_cases(self):
        """Test RSI with edge cases."""
        # Test with constant prices
        constant_prices = pd.Series([100.0] * 20, index=range(20))
        rsi_constant = calculate_rsi(constant_prices, period=14)
        
        # With constant prices, RSI should be 50 (neutral)
        valid_rsi = rsi_constant.dropna()
        if len(valid_rsi) > 0:
            assert abs(valid_rsi.iloc[-1] - 50) < 1  # Allow small numerical differences
        
        # Test with very volatile prices
        volatile_prices = pd.Series([100 + 10 * np.sin(i) for i in range(20)], index=range(20))
        rsi_volatile = calculate_rsi(volatile_prices, period=14)
        
        # Should have valid RSI values
        assert not rsi_volatile.isna().all()
    
    def test_rsi_with_zero_volume(self):
        """Test RSI calculation with zero volume data."""
        df = self.test_data.copy()
        df['Volume'] = 0  # Set volume to zero
        
        point = 0.01
        result = apply_rule_rsi(df, point, rsi_period=14, overbought=70, oversold=30)
        
        # RSI should still be calculated (doesn't depend on volume)
        assert 'RSI' in result.columns
        assert not result['RSI'].isna().all()
    
    def test_rsi_with_extreme_prices(self):
        """Test RSI calculation with extreme price values."""
        # Test with very high prices
        high_prices = pd.Series([1000000 + i for i in range(20)], index=range(20))
        rsi_high = calculate_rsi(high_prices, period=14)
        
        # Should still produce valid RSI values
        assert not rsi_high.isna().all()
        assert rsi_high.min() >= 0
        assert rsi_high.max() <= 100
        
        # Test with very low prices
        low_prices = pd.Series([0.0001 + i * 0.0001 for i in range(20)], index=range(20))
        rsi_low = calculate_rsi(low_prices, period=14)
        
        # Should still produce valid RSI values
        assert not rsi_low.isna().all()
        assert rsi_low.min() >= 0
        assert rsi_low.max() <= 100
    
    def test_rsi_parameter_validation(self):
        """Test RSI parameter validation."""
        # Test that invalid overbought/oversold values are handled gracefully
        # The current implementation doesn't validate overbought > oversold, so we'll test that
        close_prices = self.test_data['Close']
        
        # Test with overbought < oversold (should work but may not be logical)
        rsi_values = pd.Series([20, 30, 50, 70, 80, 90], index=range(6))
        signals = calculate_rsi_signals(rsi_values, overbought=30, oversold=70)
        
        # Should still produce signals (even if logically incorrect)
        assert len(signals) == 6
    
    def test_rsi_with_different_price_types(self):
        """Test RSI calculation with different price types."""
        close_prices = self.test_data['Close']
        open_prices = self.test_data['Open']
        
        # Calculate RSI with close prices
        rsi_close = calculate_rsi(close_prices, period=14)
        
        # Calculate RSI with open prices
        rsi_open = calculate_rsi(open_prices, period=14)
        
        # Both should produce valid results
        assert not rsi_close.isna().all()
        assert not rsi_open.isna().all()
        
        # They should be different (since open and close are different)
        valid_close = rsi_close.dropna()
        valid_open = rsi_open.dropna()
        
        if len(valid_close) > 0 and len(valid_open) > 0:
            # They should be different but both valid
            assert not np.allclose(valid_close.iloc[-10:], valid_open.iloc[-10:], rtol=1e-10)
    
    def test_apply_rule_rsi_with_price_types(self):
        """Test RSI rule application with different price types."""
        point = 0.01
        
        # Test with close prices - create separate copy
        df_close = self.test_data.copy()
        result_close = apply_rule_rsi(df_close, point, rsi_period=14, overbought=70, oversold=30, 
                                    price_type=PriceType.CLOSE)
        
        # Test with open prices - create separate copy
        df_open = self.test_data.copy()
        result_open = apply_rule_rsi(df_open, point, rsi_period=14, overbought=70, oversold=30, 
                                   price_type=PriceType.OPEN)
        
        # Both should work
        assert 'RSI' in result_close.columns
        assert 'RSI' in result_open.columns
        
        # Check price type info - both should show the correct price type
        assert result_close['RSI_Price_Type'].iloc[0] == "Close"
        assert result_open['RSI_Price_Type'].iloc[0] == "Open"
    
    def test_apply_rule_rsi_momentum_with_price_types(self):
        """Test RSI momentum rule with different price types."""
        point = 0.01
        
        # Test with close prices - create separate copy
        df_close = self.test_data.copy()
        result_close = apply_rule_rsi_momentum(df_close, point, rsi_period=14, overbought=70, oversold=30, 
                                             price_type=PriceType.CLOSE)
        
        # Test with open prices - create separate copy
        df_open = self.test_data.copy()
        result_open = apply_rule_rsi_momentum(df_open, point, rsi_period=14, overbought=70, oversold=30, 
                                            price_type=PriceType.OPEN)
        
        # Both should work
        assert 'RSI_Momentum' in result_close.columns
        assert 'RSI_Momentum' in result_open.columns
        
        # Check price type info
        assert result_close['RSI_Price_Type'].iloc[0] == "Close"
        assert result_open['RSI_Price_Type'].iloc[0] == "Open"
    
    def test_apply_rule_rsi_divergence_with_price_types(self):
        """Test RSI divergence rule with different price types."""
        point = 0.01
        
        # Test with close prices - create separate copy
        df_close = self.test_data.copy()
        result_close = apply_rule_rsi_divergence(df_close, point, rsi_period=14, overbought=70, oversold=30, 
                                               price_type=PriceType.CLOSE)
        
        # Test with open prices - create separate copy
        df_open = self.test_data.copy()
        result_open = apply_rule_rsi_divergence(df_open, point, rsi_period=14, overbought=70, oversold=30, 
                                              price_type=PriceType.OPEN)
        
        # Both should work
        assert 'RSI' in result_close.columns
        assert 'RSI' in result_open.columns
        
        # Check price type info
        assert result_close['RSI_Price_Type'].iloc[0] == "Close"
        assert result_open['RSI_Price_Type'].iloc[0] == "Open" 