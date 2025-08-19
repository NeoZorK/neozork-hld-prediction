# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_wave_ind.py

"""
Test module for Wave indicator calculations.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.trend.wave_ind import (
    calculate_wave, 
    apply_rule_wave, 
    WaveParameters, 
    TrendType, 
    GlobalTrendType
)
from src.common.constants import BUY, SELL, NOTRADE, PriceType


class TestWaveParameters:
    """Test WaveParameters dataclass."""
    
    def test_default_parameters(self):
        """Test default parameter values."""
        params = WaveParameters()
        
        assert params.long1 == 339
        assert params.fast1 == 10
        assert params.trend1 == 2
        assert params.tr1 == TrendType.FAST
        assert params.long2 == 22
        assert params.fast2 == 11
        assert params.trend2 == 4
        assert params.tr2 == TrendType.FAST
        assert params.global_tr == GlobalTrendType.PRIME
        assert params.sma_period == 22
        assert params.price_type == PriceType.CLOSE
    
    def test_custom_parameters(self):
        """Test custom parameter values."""
        params = WaveParameters(
            long1=200,
            fast1=5,
            trend1=1,
            tr1=TrendType.SLOW,
            long2=15,
            fast2=8,
            trend2=3,
            tr2=TrendType.MEDIUM,
            global_tr=GlobalTrendType.SECONDARY,
            sma_period=20,
            price_type=PriceType.OPEN
        )
        
        assert params.long1 == 200
        assert params.fast1 == 5
        assert params.trend1 == 1
        assert params.tr1 == TrendType.SLOW
        assert params.long2 == 15
        assert params.fast2 == 8
        assert params.trend2 == 3
        assert params.tr2 == TrendType.MEDIUM
        assert params.global_tr == GlobalTrendType.SECONDARY
        assert params.sma_period == 20
        assert params.price_type == PriceType.OPEN


class TestTrendType:
    """Test TrendType enum."""
    
    def test_trend_type_values(self):
        """Test TrendType enum values."""
        assert TrendType.FAST.value == "fast"
        assert TrendType.SLOW.value == "slow"
        assert TrendType.MEDIUM.value == "medium"
    
    def test_trend_type_from_string(self):
        """Test creating TrendType from string."""
        assert TrendType("fast") == TrendType.FAST
        assert TrendType("slow") == TrendType.SLOW
        assert TrendType("medium") == TrendType.MEDIUM
    
    def test_invalid_trend_type(self):
        """Test invalid trend type raises ValueError."""
        with pytest.raises(ValueError):
            TrendType("invalid")


class TestGlobalTrendType:
    """Test GlobalTrendType enum."""
    
    def test_global_trend_type_values(self):
        """Test GlobalTrendType enum values."""
        assert GlobalTrendType.PRIME.value == "prime"
        assert GlobalTrendType.SECONDARY.value == "secondary"
        assert GlobalTrendType.TERTIARY.value == "tertiary"
    
    def test_global_trend_type_from_string(self):
        """Test creating GlobalTrendType from string."""
        assert GlobalTrendType("prime") == GlobalTrendType.PRIME
        assert GlobalTrendType("secondary") == GlobalTrendType.SECONDARY
        assert GlobalTrendType("tertiary") == GlobalTrendType.TERTIARY
    
    def test_invalid_global_trend_type(self):
        """Test invalid global trend type raises ValueError."""
        with pytest.raises(ValueError):
            GlobalTrendType("invalid")


class TestCalculateWave:
    """Test calculate_wave function."""
    
    def setup_method(self):
        """Set up test data."""
        # Create test price series
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=500, freq='D')
        self.price_series = pd.Series(
            np.random.randn(500).cumsum() + 100,  # Random walk starting at 100
            index=dates
        )
        
        # Default parameters
        self.default_params = WaveParameters()
    
    def test_calculate_wave_default_parameters(self):
        """Test wave calculation with default parameters."""
        wave_values, wave_signals = calculate_wave(self.price_series, self.default_params)
        
        # Check that we get the expected output types
        assert isinstance(wave_values, pd.Series)
        assert isinstance(wave_signals, pd.Series)
        
        # Check that the series have the same index as input
        assert wave_values.index.equals(self.price_series.index)
        assert wave_signals.index.equals(self.price_series.index)
        
        # Check that wave values are numeric
        assert not wave_values.isna().all()
        assert wave_values.dtype in ['float64', 'float32']
        
        # Check that signals contain valid values
        valid_signals = [NOTRADE, BUY, SELL]
        assert all(signal in valid_signals for signal in wave_signals.dropna())
    
    def test_calculate_wave_custom_parameters(self):
        """Test wave calculation with custom parameters."""
        custom_params = WaveParameters(
            long1=50,
            fast1=5,
            trend1=10,
            tr1=TrendType.SLOW,
            long2=20,
            fast2=3,
            trend2=7,
            tr2=TrendType.FAST,
            global_tr=GlobalTrendType.SECONDARY,
            sma_period=15
        )
        
        wave_values, wave_signals = calculate_wave(self.price_series, custom_params)
        
        # Check that we get the expected output types
        assert isinstance(wave_values, pd.Series)
        assert isinstance(wave_signals, pd.Series)
        
        # Check that the series have the same index as input
        assert wave_values.index.equals(self.price_series.index)
        assert wave_signals.index.equals(self.price_series.index)
    
    def test_calculate_wave_insufficient_data(self):
        """Test wave calculation with insufficient data."""
        short_series = self.price_series.head(10)  # Only 10 data points
        
        wave_values, wave_signals = calculate_wave(short_series, self.default_params)
        
        # Should return empty series with NOTRADE signals
        assert wave_values.isna().all()
        assert all(signal == NOTRADE for signal in wave_signals)
    
    def test_calculate_wave_different_trend_types(self):
        """Test wave calculation with different trend type combinations."""
        # Test FAST trend type
        fast_params = WaveParameters(tr1=TrendType.FAST, tr2=TrendType.FAST)
        wave_values_fast, _ = calculate_wave(self.price_series, fast_params)
        
        # Test SLOW trend type
        slow_params = WaveParameters(tr1=TrendType.SLOW, tr2=TrendType.SLOW)
        wave_values_slow, _ = calculate_wave(self.price_series, slow_params)
        
        # Test MEDIUM trend type
        medium_params = WaveParameters(tr1=TrendType.MEDIUM, tr2=TrendType.MEDIUM)
        wave_values_medium, _ = calculate_wave(self.price_series, medium_params)
        
        # Values should be different for different trend types
        assert not wave_values_fast.equals(wave_values_slow)
        assert not wave_values_slow.equals(wave_values_medium)
        assert not wave_values_fast.equals(wave_values_medium)
    
    def test_calculate_wave_different_global_trends(self):
        """Test wave calculation with different global trend types."""
        # Test PRIME global trend
        prime_params = WaveParameters(global_tr=GlobalTrendType.PRIME, sma_period=20)
        wave_values_prime, _ = calculate_wave(self.price_series, prime_params)
        
        # Test SECONDARY global trend
        secondary_params = WaveParameters(global_tr=GlobalTrendType.SECONDARY, sma_period=20)
        wave_values_secondary, _ = calculate_wave(self.price_series, secondary_params)
        
        # Test TERTIARY global trend
        tertiary_params = WaveParameters(global_tr=GlobalTrendType.TERTIARY, sma_period=20)
        wave_values_tertiary, _ = calculate_wave(self.price_series, tertiary_params)
        
        # Values should be different for different global trend types
        assert not wave_values_prime.equals(wave_values_secondary)
        assert not wave_values_secondary.equals(wave_values_tertiary)
        assert not wave_values_prime.equals(wave_values_tertiary)
    
    def test_calculate_wave_signal_generation(self):
        """Test that wave signals are generated correctly."""
        # Create a simple price series with clear trends
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        # Create a series that goes up then down
        prices = pd.Series([100 + i for i in range(50)] + [150 - i for i in range(50)], index=dates)
        
        simple_params = WaveParameters(long1=10, fast1=5, trend1=3, long2=8, fast2=4, trend2=2, sma_period=5)
        wave_values, wave_signals = calculate_wave(prices, simple_params)
        
        # Should have some BUY and SELL signals
        assert BUY in wave_signals.values
        assert SELL in wave_signals.values
        assert NOTRADE in wave_signals.values


class TestApplyRuleWave:
    """Test apply_rule_wave function."""
    
    def setup_method(self):
        """Set up test data."""
        # Create test DataFrame
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        
        self.test_df = pd.DataFrame({
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 102,
            'Low': np.random.randn(100).cumsum() + 98,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
    
    def test_apply_rule_wave_default_parameters(self):
        """Test wave rule application with default parameters."""
        result_df = apply_rule_wave(self.test_df, point=0.01)
        
        # Check that required columns are added
        assert 'wave' in result_df.columns
        assert 'wave_signal' in result_df.columns
        assert 'wave_price_type' in result_df.columns
        assert 'wave_upper' in result_df.columns
        assert 'wave_lower' in result_df.columns
        
        # Check that original data is preserved
        assert all(col in result_df.columns for col in self.test_df.columns)
        
        # Check data types
        assert result_df['wave'].dtype in ['float64', 'float32']
        assert result_df['wave_signal'].dtype in ['float64', 'float32']
        assert result_df['wave_price_type'].dtype == 'object'
        
        # Check that price type is set correctly
        assert result_df['wave_price_type'].iloc[0] == "Close"
    
    def test_apply_rule_wave_open_price(self):
        """Test wave rule application with Open price."""
        result_df = apply_rule_wave(self.test_df, point=0.01, price_type=PriceType.OPEN)
        
        # Check that price type is set correctly
        assert result_df['wave_price_type'].iloc[0] == "Open"
    
    def test_apply_rule_wave_custom_parameters(self):
        """Test wave rule application with custom parameters."""
        result_df = apply_rule_wave(
            self.test_df, 
            point=0.01,
            wave_long1=50,
            wave_fast1=5,
            wave_trend1=10,
            wave_tr1='slow',
            wave_long2=20,
            wave_fast2=3,
            wave_trend2=7,
            wave_tr2='fast',
            wave_global_tr='secondary',
            wave_sma_period=15
        )
        
        # Check that required columns are added
        assert 'wave' in result_df.columns
        assert 'wave_signal' in result_df.columns
        assert 'wave_price_type' in result_df.columns
        assert 'wave_upper' in result_df.columns
        assert 'wave_lower' in result_df.columns
    
    def test_apply_rule_wave_invalid_trend_type(self):
        """Test wave rule application with invalid trend type."""
        with pytest.raises(ValueError):
            apply_rule_wave(
                self.test_df, 
                point=0.01,
                wave_tr1='invalid_trend_type'
            )
    
    def test_apply_rule_wave_invalid_global_trend(self):
        """Test wave rule application with invalid global trend type."""
        with pytest.raises(ValueError):
            apply_rule_wave(
                self.test_df, 
                point=0.01,
                wave_global_tr='invalid_global_trend'
            )
    
    def test_apply_rule_wave_price_levels(self):
        """Test that price levels are calculated correctly."""
        result_df = apply_rule_wave(self.test_df, point=0.01)
        
        # Check that upper and lower bands are calculated
        assert 'wave_upper' in result_df.columns
        assert 'wave_lower' in result_df.columns
        
        # Check that upper band is above wave values
        assert all(result_df['wave_upper'] >= result_df['wave'])
        
        # Check that lower band is below wave values
        assert all(result_df['wave_lower'] <= result_df['wave'])
        
        # Check that bands are separated by the expected distance
        expected_distance = 0.01 * 10 * 2  # point * 10 * 2 (upper and lower)
        actual_distance = result_df['wave_upper'] - result_df['wave_lower']
        assert all(actual_distance >= expected_distance)
    
    def test_apply_rule_wave_signal_values(self):
        """Test that signal values are valid."""
        result_df = apply_rule_wave(self.test_df, point=0.01)
        
        # Check that signals contain valid values
        valid_signals = [NOTRADE, BUY, SELL]
        assert all(signal in valid_signals for signal in result_df['wave_signal'].dropna())
    
    def test_apply_rule_wave_empty_dataframe(self):
        """Test wave rule application with empty DataFrame."""
        empty_df = pd.DataFrame()
        result_df = apply_rule_wave(empty_df, point=0.01)
        
        # Should return empty DataFrame with wave columns
        assert result_df.empty
        assert 'wave' in result_df.columns
        assert 'wave_signal' in result_df.columns
        assert 'wave_price_type' in result_df.columns
        assert 'wave_upper' in result_df.columns
        assert 'wave_lower' in result_df.columns


class TestWaveIndicatorIntegration:
    """Test Wave indicator integration with the system."""
    
    def test_wave_indicator_import(self):
        """Test that Wave indicator can be imported correctly."""
        from src.calculation.indicators.trend.wave_ind import apply_rule_wave
        assert callable(apply_rule_wave)
    
    def test_wave_indicator_docstring(self):
        """Test that Wave indicator has proper documentation."""
        from src.calculation.indicators.trend.wave_ind import apply_rule_wave
        
        doc = apply_rule_wave.__doc__
        assert doc is not None
        assert "Wave" in doc
        assert "DataFrame" in doc
        assert "point" in doc
    
    def test_wave_indicator_info(self):
        """Test that Wave indicator has proper INDICATOR INFO."""
        import src.calculation.indicators.trend.wave_ind as wave_module
        
        module_doc = wave_module.__doc__
        assert module_doc is not None
        assert "INDICATOR INFO:" in module_doc
        assert "Name: Wave" in module_doc
        assert "Category: Trend" in module_doc
        assert "Usage:" in module_doc
        assert "Parameters:" in module_doc
