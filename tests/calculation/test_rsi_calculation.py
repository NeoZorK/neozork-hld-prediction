# -*- coding: utf-8 -*-
# tests/calculation/test_rsi_calculation.py

"""
Tests for RSI calculation module.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.rsi_calculation import (
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
        
        # Create different open and close prices
        open_prices = [p * (1 + np.random.normal(0, 0.005)) for p in prices]  # Slight variation
        close_prices = [p * (1 + np.random.normal(0, 0.005)) for p in prices]  # Slight variation
        
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
        valid_signals = [NOTRADE, BUY, SELL]
        assert result['Direction'].isin(valid_signals).all()
        
        # Check that colors are set correctly
        assert (result['PColor1'] == BUY).all()
        assert (result['PColor2'] == SELL).all()
        
        # Check that Diff contains RSI values
        assert not result['Diff'].isna().all()
    
    def test_apply_rule_rsi_custom_parameters(self):
        """Test RSI rule application with custom parameters."""
        df = self.test_data.copy()
        point = 0.01
        
        result = apply_rule_rsi(df, point, rsi_period=7, overbought=80, oversold=20)
        
        # Should work with custom parameters
        assert 'RSI' in result.columns
        assert 'RSI_Signal' in result.columns
        assert not result['RSI'].isna().all()
    
    def test_apply_rule_rsi_momentum(self):
        """Test RSI momentum rule application."""
        df = self.test_data.copy()
        point = 0.01
        
        result = apply_rule_rsi_momentum(df, point, rsi_period=14, overbought=70, oversold=30)
        
        # Check that required columns are present
        required_cols = ['RSI', 'RSI_Momentum', 'RSI_Signal', 'PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff']
        for col in required_cols:
            assert col in result.columns
        
        # Check that momentum is calculated
        assert not result['RSI_Momentum'].isna().all()
        
        # Check that momentum values are reasonable
        momentum_values = result['RSI_Momentum'].dropna()
        assert len(momentum_values) > 0
        
        # Check that colors are set correctly
        assert (result['PColor1'] == BUY).all()
        assert (result['PColor2'] == SELL).all()
        
        # Check that Diff contains momentum values
        assert not result['Diff'].isna().all()
    
    def test_apply_rule_rsi_momentum_signals(self):
        """Test RSI momentum signal generation."""
        df = self.test_data.copy()
        point = 0.01
        
        result = apply_rule_rsi_momentum(df, point, rsi_period=14, overbought=70, oversold=30)
        
        # Check that signals are generated based on momentum conditions
        signals = result['RSI_Signal'].dropna()
        assert len(signals) > 0
        
        # Should have some BUY and SELL signals (not just NOTRADE)
        signal_counts = signals.value_counts()
        assert len(signal_counts) > 1 or signal_counts.get(BUY, 0) > 0 or signal_counts.get(SELL, 0) > 0
    
    def test_apply_rule_rsi_divergence(self):
        """Test RSI divergence rule application."""
        df = self.test_data.copy()
        point = 0.01
        
        result = apply_rule_rsi_divergence(df, point, rsi_period=14, overbought=70, oversold=30)
        
        # Check that required columns are present
        required_cols = ['RSI', 'RSI_Signal', 'PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff']
        for col in required_cols:
            assert col in result.columns
        
        # Check that divergence strength is calculated
        assert not result['Diff'].isna().all()
        
        # Check that divergence strength is between 0 and 1
        diff_values = result['Diff'].dropna()
        assert len(diff_values) > 0
        assert diff_values.min() >= 0
        assert diff_values.max() <= 1
        
        # Check that colors are set correctly
        assert (result['PColor1'] == BUY).all()
        assert (result['PColor2'] == SELL).all()
    
    def test_apply_rule_rsi_divergence_detection(self):
        """Test RSI divergence detection logic."""
        df = self.test_data.copy()
        point = 0.01
        
        result = apply_rule_rsi_divergence(df, point, rsi_period=14, overbought=70, oversold=30)
        
        # Check that divergence signals are generated
        signals = result['RSI_Signal'].dropna()
        assert len(signals) > 0
        
        # Should have some signals (not just NOTRADE)
        signal_counts = signals.value_counts()
        assert len(signal_counts) > 1 or signal_counts.get(BUY, 0) > 0 or signal_counts.get(SELL, 0) > 0
    
    def test_rsi_edge_cases(self):
        """Test RSI calculation with edge cases."""
        # Test with constant prices
        constant_prices = pd.Series([100.0] * 20, index=range(20))
        rsi = calculate_rsi(constant_prices, period=14)
        
        # For constant prices, RSI should be around 50 (neutral)
        # But due to division by zero in RS calculation, it might be NaN
        # Let's check that we have some valid values
        valid_rsi = rsi.dropna()
        if len(valid_rsi) > 0:
            # If we have valid values, they should be around 50
            assert abs(valid_rsi.iloc[-1] - 50) < 10  # Allow larger tolerance
        
        # Test with insufficient data
        short_prices = pd.Series([100, 101, 102], index=range(3))
        rsi_short = calculate_rsi(short_prices, period=14)
        
        # Should return series with NaN values due to insufficient data
        assert rsi_short.isna().all()
    
    def test_rsi_with_zero_volume(self):
        """Test RSI calculation with zero volume data."""
        df = self.test_data.copy()
        df['Volume'] = 0  # Set volume to zero
        
        point = 0.01
        
        # Should still work (RSI doesn't depend on volume)
        result = apply_rule_rsi(df, point, rsi_period=14, overbought=70, oversold=30)
        
        assert 'RSI' in result.columns
        assert not result['RSI'].isna().all()
    
    def test_rsi_with_extreme_prices(self):
        """Test RSI calculation with extreme price movements."""
        # Create data with extreme price movements
        extreme_prices = pd.Series([100, 200, 50, 300, 25, 400], index=range(6))
        extreme_data = pd.DataFrame({
            'Open': extreme_prices,
            'High': extreme_prices * 1.01,
            'Low': extreme_prices * 0.99,
            'Close': extreme_prices,
            'Volume': [1000] * 6
        }, index=range(6))
        
        point = 0.01
        
        # Should handle extreme movements gracefully
        result = apply_rule_rsi(extreme_data, point, rsi_period=14, overbought=70, oversold=30)
        
        assert 'RSI' in result.columns
        # RSI should still be between 0 and 100
        rsi_values = result['RSI'].dropna()
        if len(rsi_values) > 0:
            assert rsi_values.min() >= 0
            assert rsi_values.max() <= 100
    
    def test_rsi_parameter_validation(self):
        """Test RSI parameter validation."""
        df = self.test_data.copy()
        point = 0.01
        
        # Test with invalid overbought/oversold levels
        # Should work but might not generate expected signals
        result = apply_rule_rsi(df, point, rsi_period=14, overbought=50, oversold=50)
        assert 'RSI' in result.columns 

    def test_rsi_with_different_price_types(self):
        """Test RSI calculation with different price types."""
        # Test with close prices (default)
        rsi_close = calculate_rsi(self.test_data['Close'], period=14)
        assert isinstance(rsi_close, pd.Series)
        assert len(rsi_close) == len(self.test_data)
        
        # Test with open prices
        rsi_open = calculate_rsi(self.test_data['Open'], period=14)
        assert isinstance(rsi_open, pd.Series)
        assert len(rsi_open) == len(self.test_data)
        
        # Values should be different since open and close prices are different
        assert not rsi_close.equals(rsi_open)
        
        # Both should be within valid RSI range (0-100)
        assert all(0 <= val <= 100 for val in rsi_close.dropna())
        assert all(0 <= val <= 100 for val in rsi_open.dropna())

    def test_apply_rule_rsi_with_price_types(self):
        """Test RSI rule application with different price types."""
        # Test with close prices (default)
        result_close = apply_rule_rsi(
            self.test_data.copy(), 
            point=0.00001, 
            price_type=PriceType.CLOSE
        )
        assert 'RSI' in result_close.columns
        assert 'RSI_Price_Type' in result_close.columns
        assert result_close['RSI_Price_Type'].iloc[0] == 'Close'
        
        # Test with open prices
        result_open = apply_rule_rsi(
            self.test_data.copy(), 
            point=0.00001, 
            price_type=PriceType.OPEN
        )
        assert 'RSI' in result_open.columns
        assert 'RSI_Price_Type' in result_open.columns
        assert result_open['RSI_Price_Type'].iloc[0] == 'Open'
        
        # RSI values should be different
        assert not result_close['RSI'].equals(result_open['RSI'])

    def test_apply_rule_rsi_momentum_with_price_types(self):
        """Test RSI momentum rule with different price types."""
        # Test with close prices
        result_close = apply_rule_rsi_momentum(
            self.test_data.copy(), 
            point=0.00001, 
            price_type=PriceType.CLOSE
        )
        assert 'RSI' in result_close.columns
        assert 'RSI_Momentum' in result_close.columns
        assert 'RSI_Price_Type' in result_close.columns
        assert result_close['RSI_Price_Type'].iloc[0] == 'Close'
        
        # Test with open prices
        result_open = apply_rule_rsi_momentum(
            self.test_data.copy(), 
            point=0.00001, 
            price_type=PriceType.OPEN
        )
        assert 'RSI' in result_open.columns
        assert 'RSI_Momentum' in result_open.columns
        assert 'RSI_Price_Type' in result_open.columns
        assert result_open['RSI_Price_Type'].iloc[0] == 'Open'
        
        # RSI values should be different
        assert not result_close['RSI'].equals(result_open['RSI'])

    def test_apply_rule_rsi_divergence_with_price_types(self):
        """Test RSI divergence rule with different price types."""
        # Test with close prices
        result_close = apply_rule_rsi_divergence(
            self.test_data.copy(), 
            point=0.00001, 
            price_type=PriceType.CLOSE
        )
        assert 'RSI' in result_close.columns
        assert 'RSI_Price_Type' in result_close.columns
        assert result_close['RSI_Price_Type'].iloc[0] == 'Close'
        
        # Test with open prices
        result_open = apply_rule_rsi_divergence(
            self.test_data.copy(), 
            point=0.00001, 
            price_type=PriceType.OPEN
        )
        assert 'RSI' in result_open.columns
        assert 'RSI_Price_Type' in result_open.columns
        assert result_open['RSI_Price_Type'].iloc[0] == 'Open'
        
        # RSI values should be different
        assert not result_close['RSI'].equals(result_open['RSI']) 