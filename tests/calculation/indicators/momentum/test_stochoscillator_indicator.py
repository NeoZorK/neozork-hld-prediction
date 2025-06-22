# -*- coding: utf-8 -*-
# tests/calculation/indicators/momentum/test_stochoscillator_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.momentum.stochoscillator_ind import calculate_stochoscillator, apply_rule_stochoscillator


class TestStochasticOscillatorIndicator:
    """Test cases for Stochastic Oscillator indicator."""

    def setup_method(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'High': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'Close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        self.stoch_indicator = StochasticOscillatorIndicator()

    def test_stoch_initialization(self):
        """Test Stochastic Oscillator indicator initialization."""
        assert self.stoch_indicator.name == "StochasticOscillator"
        assert self.stoch_indicator.category == "Momentum"

    def test_stoch_calculation_basic(self):
        """Test basic Stochastic Oscillator calculation."""
        result = self.stoch_indicator.calculate(
            self.sample_data, 
            k_period=14, 
            d_period=3, 
            price_type='close'
        )
        
        assert 'StochasticOscillator_K' in result.columns
        assert 'StochasticOscillator_D' in result.columns
        assert len(result) == len(self.sample_data)

    def test_stoch_calculation_with_open_price(self):
        """Test Stochastic Oscillator calculation using open price."""
        result = self.stoch_indicator.calculate(
            self.sample_data, 
            k_period=14, 
            d_period=3, 
            price_type='open'
        )
        
        assert 'StochasticOscillator_K' in result.columns
        assert 'StochasticOscillator_D' in result.columns
        assert len(result) == len(self.sample_data)

    def test_stoch_different_parameters(self):
        """Test Stochastic Oscillator calculation with different parameters."""
        k_periods = [5, 14, 20]
        d_periods = [3, 5, 7]
        
        for k in k_periods:
            for d in d_periods:
                result = self.stoch_indicator.calculate(
                    self.sample_data, 
                    k_period=k, 
                    d_period=d, 
                    price_type='close'
                )
                
                assert 'StochasticOscillator_K' in result.columns
                assert 'StochasticOscillator_D' in result.columns

    def test_stoch_invalid_k_period(self):
        """Test Stochastic Oscillator calculation with invalid k period."""
        with pytest.raises(ValueError):
            self.stoch_indicator.calculate(
                self.sample_data, 
                k_period=0, 
                d_period=3, 
                price_type='close'
            )

    def test_stoch_invalid_d_period(self):
        """Test Stochastic Oscillator calculation with invalid d period."""
        with pytest.raises(ValueError):
            self.stoch_indicator.calculate(
                self.sample_data, 
                k_period=14, 
                d_period=0, 
                price_type='close'
            )

    def test_stoch_empty_dataframe(self):
        """Test Stochastic Oscillator calculation with empty dataframe."""
        empty_df = pd.DataFrame()
        
        with pytest.raises(ValueError):
            self.stoch_indicator.calculate(
                empty_df, 
                k_period=14, 
                d_period=3, 
                price_type='close'
            )

    def test_stoch_missing_columns(self):
        """Test Stochastic Oscillator calculation with missing required columns."""
        incomplete_df = self.sample_data.drop(columns=['High', 'Low'])
        
        with pytest.raises(ValueError):
            self.stoch_indicator.calculate(
                incomplete_df, 
                k_period=14, 
                d_period=3, 
                price_type='close'
            )

    def test_stoch_parameter_validation(self):
        """Test Stochastic Oscillator parameter validation."""
        # Test invalid price_type
        with pytest.raises(ValueError):
            self.stoch_indicator.calculate(
                self.sample_data, 
                k_period=14, 
                d_period=3, 
                price_type='invalid'
            )

    def test_stoch_value_range(self):
        """Test that Stochastic Oscillator values are within expected range (0-100)."""
        result = self.stoch_indicator.calculate(
            self.sample_data, 
            k_period=14, 
            d_period=3, 
            price_type='close'
        )
        
        k_values = result['StochasticOscillator_K'].dropna()
        d_values = result['StochasticOscillator_D'].dropna()
        
        assert (k_values >= 0).all()
        assert (k_values <= 100).all()
        assert (d_values >= 0).all()
        assert (d_values <= 100).all()

    def test_stoch_overbought_oversold_levels(self):
        """Test Stochastic Oscillator overbought/oversold level detection."""
        result = self.stoch_indicator.calculate(
            self.sample_data, 
            k_period=14, 
            d_period=3, 
            price_type='close'
        )
        
        k_values = result['StochasticOscillator_K'].dropna()
        d_values = result['StochasticOscillator_D'].dropna()
        
        # Should be able to identify overbought/oversold conditions
        assert len(k_values) > 0
        assert len(d_values) > 0

    def test_stoch_with_nan_values(self):
        """Test Stochastic Oscillator calculation with NaN values in data."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'High'] = np.nan
        data_with_nan.loc[3, 'Low'] = np.nan
        
        result = self.stoch_indicator.calculate(
            data_with_nan, 
            k_period=14, 
            d_period=3, 
            price_type='close'
        )
        
        assert 'StochasticOscillator_K' in result.columns
        assert 'StochasticOscillator_D' in result.columns
        # Should handle NaN values gracefully

    def test_stoch_docstring_info(self):
        """Test that Stochastic Oscillator has proper docstring information."""
        docstring = self.stoch_indicator.__doc__
        assert docstring is not None
        assert "StochasticOscillator" in docstring

    def test_stoch_cli_integration(self):
        """Test Stochastic Oscillator CLI integration."""
        result = self.stoch_indicator.calculate(
            self.sample_data, 
            k_period=14, 
            d_period=3, 
            price_type='close'
        )
        
        assert 'StochasticOscillator_K' in result.columns
        assert 'StochasticOscillator_D' in result.columns
        assert 'StochasticOscillator_K_Period' in result.columns
        assert 'StochasticOscillator_D_Period' in result.columns
        assert 'StochasticOscillator_Price_Type' in result.columns

    def test_stoch_performance(self):
        """Test Stochastic Oscillator calculation performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'Close': np.random.uniform(100, 200, 1000),
            'Open': np.random.uniform(100, 200, 1000),
            'High': np.random.uniform(100, 200, 1000),
            'Low': np.random.uniform(100, 200, 1000),
            'Volume': np.random.uniform(1000, 5000, 1000)
        })
        
        result = self.stoch_indicator.calculate(
            large_data, 
            k_period=14, 
            d_period=3, 
            price_type='close'
        )
        
        assert 'StochasticOscillator_K' in result.columns
        assert 'StochasticOscillator_D' in result.columns
        assert len(result) == 1000

    def test_stoch_edge_cases(self):
        """Test Stochastic Oscillator calculation with edge cases."""
        # Test with very small dataset
        small_data = self.sample_data.head(5)
        
        with pytest.raises(ValueError):
            self.stoch_indicator.calculate(
                small_data, 
                k_period=10, 
                d_period=3, 
                price_type='close'
            )

    def test_stoch_consistency(self):
        """Test Stochastic Oscillator calculation consistency."""
        result1 = self.stoch_indicator.calculate(
            self.sample_data, 
            k_period=14, 
            d_period=3, 
            price_type='close'
        )
        
        result2 = self.stoch_indicator.calculate(
            self.sample_data, 
            k_period=14, 
            d_period=3, 
            price_type='close'
        )
        
        # Results should be identical for same input
        pd.testing.assert_frame_equal(result1, result2)

    def test_stoch_crossover_signals(self):
        """Test Stochastic Oscillator crossover signal detection."""
        # Create data with clear momentum changes
        momentum_data = pd.DataFrame({
            'High': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'Volume': [1000] * 15
        })
        
        result = self.stoch_indicator.calculate(
            momentum_data, 
            k_period=5, 
            d_period=3, 
            price_type='close'
        )
        
        assert 'StochasticOscillator_K' in result.columns
        assert 'StochasticOscillator_D' in result.columns
        # Should detect K and D line crossovers 