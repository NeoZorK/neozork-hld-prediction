# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_sar_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.trend.sar_ind import calculate_sar, apply_rule_sar


class TestSARIndicator:
    """Test cases for SAR (Parabolic SAR) indicator."""

    def setup_method(self):
        """Set up test data."""
        self.sar = calculate_sar
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_sar_calculation_basic(self):
        """Test basic SAR calculation."""
        result = self.sar(self.sample_data['High'], self.sample_data['Low'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data)
        assert not result.isna().all()

    def test_sar_with_custom_parameters(self):
        """Test SAR calculation with custom parameters."""
        result = self.sar(self.sample_data['High'], self.sample_data['Low'], acceleration=0.02, maximum=0.2)
        assert isinstance(result, pd.Series)
        assert not result.isna().all()

    def test_sar_with_invalid_parameters(self):
        """Test SAR calculation with invalid parameters."""
        with pytest.raises(ValueError, match="SAR acceleration must be positive"):
            self.sar(self.sample_data['High'], self.sample_data['Low'], acceleration=0)
        with pytest.raises(ValueError, match="SAR acceleration must be positive"):
            self.sar(self.sample_data['High'], self.sample_data['Low'], acceleration=-0.01)
        with pytest.raises(ValueError, match="SAR maximum must be positive"):
            self.sar(self.sample_data['High'], self.sample_data['Low'], maximum=0)
        with pytest.raises(ValueError, match="SAR maximum must be positive"):
            self.sar(self.sample_data['High'], self.sample_data['Low'], maximum=-0.1)

    def test_sar_empty_dataframe(self):
        """Test SAR calculation with empty dataframe."""
        empty_series = pd.Series(dtype=float)
        result = self.sar(empty_series, empty_series)
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_sar_insufficient_data(self):
        """Test SAR calculation with insufficient data."""
        small_high = self.sample_data['High'].head(5)
        small_low = self.sample_data['Low'].head(5)
        result = self.sar(small_high, small_low)
        assert not result.isna().all()

    def test_sar_parameter_validation(self):
        """Test SAR parameter validation."""
        result = self.sar(self.sample_data['High'], self.sample_data['Low'], acceleration=0.02, maximum=0.2)
        assert isinstance(result, pd.Series)
        result = self.sar(self.sample_data['High'], self.sample_data['Low'], acceleration=float(0.02), maximum=float(0.2))
        assert isinstance(result, pd.Series)

    def test_sar_with_nan_values(self):
        """Test SAR calculation with NaN values in data."""
        high_with_nan = self.sample_data['High'].copy()
        high_with_nan.loc[5] = np.nan
        result = self.sar(high_with_nan, self.sample_data['Low'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(high_with_nan)

    def test_sar_performance(self):
        """Test SAR calculation performance with larger dataset."""
        large_high = pd.Series(np.random.uniform(100, 200, 10000))
        large_low = pd.Series(np.random.uniform(50, 100, 10000))
        import time
        start_time = time.time()
        result = self.sar(large_high, large_low)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, pd.Series)

    def test_sar_apply_rule(self):
        """Test SAR apply rule."""
        result = apply_rule_sar(self.sample_data, point=0.01)
        assert 'SAR' in result
        assert 'SAR_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['SAR_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 