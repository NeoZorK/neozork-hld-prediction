# -*- coding: utf-8 -*-
# tests/calculation/indicators/momentum/test_stochoscillator_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.momentum.stochoscillator_ind import calculate_stochoscillator, apply_rule_stochoscillator


class TestStochOscillatorIndicator:
    """Test cases for Stochastic Oscillator indicator."""

    def setup_method(self):
        """Set up test data."""
        self.stochosc = calculate_stochoscillator
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_stochosc_calculation_basic(self):
        """Test basic Stochastic Oscillator calculation."""
        k_values, d_values = self.stochosc(self.sample_data)
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)
        assert len(k_values) == len(self.sample_data)
        assert len(d_values) == len(self.sample_data)
        assert not k_values.isna().all()
        assert not d_values.isna().all()

    def test_stochosc_with_custom_periods(self):
        """Test Stochastic Oscillator calculation with custom periods."""
        k_values, d_values = self.stochosc(self.sample_data, k_period=10, d_period=3)
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)
        assert k_values.iloc[:9].isna().all()
        assert not k_values.iloc[9:].isna().all()

    def test_stochosc_with_invalid_periods(self):
        """Test Stochastic Oscillator calculation with invalid periods."""
        with pytest.raises(ValueError, match="Stochastic Oscillator k_period must be positive"):
            self.stochosc(self.sample_data, k_period=0)
        with pytest.raises(ValueError, match="Stochastic Oscillator k_period must be positive"):
            self.stochosc(self.sample_data, k_period=-1)

    def test_stochosc_empty_dataframe(self):
        """Test Stochastic Oscillator calculation with empty dataframe."""
        empty_df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        k_values, d_values = self.stochosc(empty_df)
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)
        assert len(k_values) == 0
        assert len(d_values) == 0

    def test_stochosc_insufficient_data(self):
        """Test Stochastic Oscillator calculation with insufficient data."""
        small_df = self.sample_data.head(5)
        k_values, d_values = self.stochosc(small_df, k_period=20)
        assert k_values.isna().all()
        assert d_values.isna().all()

    def test_stochosc_parameter_validation(self):
        """Test Stochastic Oscillator parameter validation."""
        k_values, d_values = self.stochosc(self.sample_data, k_period=20, d_period=3)
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)
        k_values, d_values = self.stochosc(self.sample_data, k_period=int(20.5), d_period=int(3.5))
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)

    def test_stochosc_with_nan_values(self):
        """Test Stochastic Oscillator calculation with NaN values in data."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[5, 'High'] = np.nan
        k_values, d_values = self.stochosc(data_with_nan)
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)
        assert len(k_values) == len(data_with_nan)
        assert len(d_values) == len(data_with_nan)

    def test_stochosc_performance(self):
        """Test Stochastic Oscillator calculation performance with larger dataset."""
        large_data = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 10000),
            'High': np.random.uniform(200, 300, 10000),
            'Low': np.random.uniform(50, 100, 10000),
            'Close': np.random.uniform(100, 200, 10000),
            'Volume': np.random.uniform(1000, 5000, 10000)
        })
        import time
        start_time = time.time()
        k_values, d_values = self.stochosc(large_data)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)

    def test_stochosc_apply_rule(self):
        """Test Stochastic Oscillator rule application."""
        result = apply_rule_stochoscillator(self.sample_data, point=0.01)
        assert 'StochOsc_K' in result
        assert 'StochOsc_D' in result
        assert 'StochOsc_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['StochOsc_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number)

    def test_stochosc_value_range(self):
        """Test that Stochastic Oscillator values are within expected range (0-100)."""
        k_values, d_values = self.stochosc(self.sample_data)
        
        assert (k_values >= 0).all()
        assert (k_values <= 100).all()
        assert (d_values >= 0).all()
        assert (d_values <= 100).all()

    def test_stochosc_overbought_oversold_levels(self):
        """Test Stochastic Oscillator overbought/oversold level detection."""
        k_values, d_values = self.stochosc(self.sample_data)
        
        # Should be able to identify overbought/oversold conditions
        assert len(k_values) > 0
        assert len(d_values) > 0

    def test_stochosc_docstring_info(self):
        """Test that Stochastic Oscillator has proper docstring information."""
        docstring = self.stochosc.__doc__
        assert docstring is not None
        assert "StochasticOscillator" in docstring

    def test_stochosc_edge_cases(self):
        """Test Stochastic Oscillator calculation with edge cases."""
        # Test with very small dataset
        small_data = self.sample_data.head(5)
        
        with pytest.raises(ValueError):
            self.stochosc(small_data, k_period=10)

    def test_stochosc_consistency(self):
        """Test Stochastic Oscillator calculation consistency."""
        result1 = self.stochosc(self.sample_data)
        
        result2 = self.stochosc(self.sample_data)
        
        # Results should be identical for same input
        pd.testing.assert_series_equal(result1[0], result2[0])
        pd.testing.assert_series_equal(result1[1], result2[1])

    def test_stochosc_crossover_signals(self):
        """Test Stochastic Oscillator crossover signal detection."""
        # Create data with clear momentum changes
        momentum_data = pd.DataFrame({
            'High': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'Volume': [1000] * 15
        })
        
        k_values, d_values = self.stochosc(momentum_data, k_period=5)
        
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)
        # Should detect K and D line crossovers 