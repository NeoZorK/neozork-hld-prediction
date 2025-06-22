# -*- coding: utf-8 -*-
# tests/calculation/indicators/momentum/test_macd_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.momentum.macd_ind import calculate_macd, apply_rule_macd


class TestMACDIndicator:
    """Test cases for MACD (Moving Average Convergence Divergence) indicator."""

    def setup_method(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'High': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'Close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        self.macd_indicator = MACDIndicator()

    def test_macd_initialization(self):
        """Test MACD indicator initialization."""
        assert self.macd_indicator.name == "MACD"
        assert self.macd_indicator.category == "Momentum"

    def test_macd_calculation_basic(self):
        """Test basic MACD calculation."""
        result = self.macd_indicator.calculate(
            self.sample_data, 
            fast_period=12, 
            slow_period=26, 
            signal_period=9, 
            price_type='close'
        )
        
        assert 'MACD' in result.columns
        assert 'MACD_Signal' in result.columns
        assert 'MACD_Histogram' in result.columns
        assert len(result) == len(self.sample_data)

    def test_macd_calculation_with_open_price(self):
        """Test MACD calculation using open price."""
        result = self.macd_indicator.calculate(
            self.sample_data, 
            fast_period=12, 
            slow_period=26, 
            signal_period=9, 
            price_type='open'
        )
        
        assert 'MACD' in result.columns
        assert 'MACD_Signal' in result.columns
        assert 'MACD_Histogram' in result.columns
        assert len(result) == len(self.sample_data)

    def test_macd_different_parameters(self):
        """Test MACD calculation with different parameters."""
        fast_periods = [8, 12, 16]
        slow_periods = [21, 26, 30]
        signal_periods = [7, 9, 12]
        
        for fast in fast_periods:
            for slow in slow_periods:
                for signal in signal_periods:
                    if fast < slow:  # Valid combination
                        result = self.macd_indicator.calculate(
                            self.sample_data, 
                            fast_period=fast, 
                            slow_period=slow, 
                            signal_period=signal, 
                            price_type='close'
                        )
                        
                        assert 'MACD' in result.columns
                        assert 'MACD_Signal' in result.columns
                        assert 'MACD_Histogram' in result.columns

    def test_macd_invalid_fast_period(self):
        """Test MACD calculation with invalid fast period."""
        with pytest.raises(ValueError):
            self.macd_indicator.calculate(
                self.sample_data, 
                fast_period=0, 
                slow_period=26, 
                signal_period=9, 
                price_type='close'
            )

    def test_macd_invalid_slow_period(self):
        """Test MACD calculation with invalid slow period."""
        with pytest.raises(ValueError):
            self.macd_indicator.calculate(
                self.sample_data, 
                fast_period=12, 
                slow_period=0, 
                signal_period=9, 
                price_type='close'
            )

    def test_macd_invalid_signal_period(self):
        """Test MACD calculation with invalid signal period."""
        with pytest.raises(ValueError):
            self.macd_indicator.calculate(
                self.sample_data, 
                fast_period=12, 
                slow_period=26, 
                signal_period=0, 
                price_type='close'
            )

    def test_macd_fast_greater_than_slow(self):
        """Test MACD calculation when fast period > slow period."""
        with pytest.raises(ValueError):
            self.macd_indicator.calculate(
                self.sample_data, 
                fast_period=30, 
                slow_period=12, 
                signal_period=9, 
                price_type='close'
            )

    def test_macd_empty_dataframe(self):
        """Test MACD calculation with empty dataframe."""
        empty_df = pd.DataFrame()
        
        with pytest.raises(ValueError):
            self.macd_indicator.calculate(
                empty_df, 
                fast_period=12, 
                slow_period=26, 
                signal_period=9, 
                price_type='close'
            )

    def test_macd_missing_columns(self):
        """Test MACD calculation with missing required columns."""
        incomplete_df = self.sample_data.drop(columns=['Close'])
        
        with pytest.raises(ValueError):
            self.macd_indicator.calculate(
                incomplete_df, 
                fast_period=12, 
                slow_period=26, 
                signal_period=9, 
                price_type='close'
            )

    def test_macd_parameter_validation(self):
        """Test MACD parameter validation."""
        # Test invalid price_type
        with pytest.raises(ValueError):
            self.macd_indicator.calculate(
                self.sample_data, 
                fast_period=12, 
                slow_period=26, 
                signal_period=9, 
                price_type='invalid'
            )

    def test_macd_signal_line_calculation(self):
        """Test MACD signal line calculation."""
        result = self.macd_indicator.calculate(
            self.sample_data, 
            fast_period=12, 
            slow_period=26, 
            signal_period=9, 
            price_type='close'
        )
        
        # Signal line should be calculated from MACD line
        assert 'MACD_Signal' in result.columns
        signal_values = result['MACD_Signal'].dropna()
        assert len(signal_values) > 0

    def test_macd_histogram_calculation(self):
        """Test MACD histogram calculation."""
        result = self.macd_indicator.calculate(
            self.sample_data, 
            fast_period=12, 
            slow_period=26, 
            signal_period=9, 
            price_type='close'
        )
        
        # Histogram should be MACD - Signal
        assert 'MACD_Histogram' in result.columns
        histogram_values = result['MACD_Histogram'].dropna()
        assert len(histogram_values) > 0

    def test_macd_with_nan_values(self):
        """Test MACD calculation with NaN values in data."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'Close'] = np.nan
        
        result = self.macd_indicator.calculate(
            data_with_nan, 
            fast_period=12, 
            slow_period=26, 
            signal_period=9, 
            price_type='close'
        )
        
        assert 'MACD' in result.columns
        assert 'MACD_Signal' in result.columns
        assert 'MACD_Histogram' in result.columns
        # Should handle NaN values gracefully

    def test_macd_docstring_info(self):
        """Test that MACD has proper docstring information."""
        docstring = self.macd_indicator.__doc__
        assert docstring is not None
        assert "MACD" in docstring
        assert "Moving Average Convergence Divergence" in docstring

    def test_macd_cli_integration(self):
        """Test MACD CLI integration."""
        result = self.macd_indicator.calculate(
            self.sample_data, 
            fast_period=12, 
            slow_period=26, 
            signal_period=9, 
            price_type='close'
        )
        
        assert 'MACD' in result.columns
        assert 'MACD_Fast_Period' in result.columns
        assert 'MACD_Slow_Period' in result.columns
        assert 'MACD_Signal_Period' in result.columns
        assert 'MACD_Price_Type' in result.columns

    def test_macd_performance(self):
        """Test MACD calculation performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'Close': np.random.uniform(100, 200, 1000),
            'Open': np.random.uniform(100, 200, 1000),
            'High': np.random.uniform(100, 200, 1000),
            'Low': np.random.uniform(100, 200, 1000),
            'Volume': np.random.uniform(1000, 5000, 1000)
        })
        
        result = self.macd_indicator.calculate(
            large_data, 
            fast_period=12, 
            slow_period=26, 
            signal_period=9, 
            price_type='close'
        )
        
        assert 'MACD' in result.columns
        assert len(result) == 1000

    def test_macd_edge_cases(self):
        """Test MACD calculation with edge cases."""
        # Test with very small dataset
        small_data = self.sample_data.head(5)
        
        with pytest.raises(ValueError):
            self.macd_indicator.calculate(
                small_data, 
                fast_period=12, 
                slow_period=26, 
                signal_period=9, 
                price_type='close'
            )

    def test_macd_consistency(self):
        """Test MACD calculation consistency."""
        result1 = self.macd_indicator.calculate(
            self.sample_data, 
            fast_period=12, 
            slow_period=26, 
            signal_period=9, 
            price_type='close'
        )
        
        result2 = self.macd_indicator.calculate(
            self.sample_data, 
            fast_period=12, 
            slow_period=26, 
            signal_period=9, 
            price_type='close'
        )
        
        # Results should be identical for same input
        pd.testing.assert_frame_equal(result1, result2)

    def test_macd_crossover_signals(self):
        """Test MACD crossover signal detection."""
        # Create data with clear trend
        trend_data = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'High': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
            'Volume': [1000] * 15
        })
        
        result = self.macd_indicator.calculate(
            trend_data, 
            fast_period=5, 
            slow_period=10, 
            signal_period=3, 
            price_type='close'
        )
        
        assert 'MACD' in result.columns
        assert 'MACD_Signal' in result.columns
        assert 'MACD_Histogram' in result.columns
        # Should detect MACD line crossing signal line 