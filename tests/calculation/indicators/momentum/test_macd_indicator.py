# -*- coding: utf-8 -*-
# tests/calculation/indicators/momentum/test_macd_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.momentum.macd_ind import calculate_macd, apply_rule_macd


class TestMACDIndicator:
    """Test cases for MACD (Moving Average Convergence Divergence) indicator."""

    def setup_method(self):
        """Set up test data."""
        self.macd = calculate_macd
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_macd_calculation_basic(self):
        """Test basic MACD calculation."""
        macd_line, signal_line, histogram = self.macd(self.sample_data['Close'])
        assert isinstance(macd_line, pd.Series)
        assert isinstance(signal_line, pd.Series)
        assert isinstance(histogram, pd.Series)
        assert len(macd_line) == len(self.sample_data)
        assert len(signal_line) == len(self.sample_data)
        assert len(histogram) == len(self.sample_data)
        assert not macd_line.isna().all()
        assert not signal_line.isna().all()
        assert not histogram.isna().all()

    def test_macd_with_custom_periods(self):
        """Test MACD calculation with custom periods."""
        macd_line, signal_line, histogram = self.macd(self.sample_data['Close'], fast_period=10, slow_period=20, signal_period=5)
        assert isinstance(macd_line, pd.Series)
        assert isinstance(signal_line, pd.Series)
        assert isinstance(histogram, pd.Series)
        assert len(macd_line) == len(self.sample_data)
        assert len(signal_line) == len(self.sample_data)
        assert len(histogram) == len(self.sample_data)
        assert not macd_line.isna().all()

    def test_macd_with_invalid_periods(self):
        """Test MACD calculation with invalid periods."""
        with pytest.raises(ValueError, match="All periods must be positive"):
            self.macd(self.sample_data['Close'], fast_period=0)
        with pytest.raises(ValueError, match="All periods must be positive"):
            self.macd(self.sample_data['Close'], slow_period=0)
        with pytest.raises(ValueError, match="All periods must be positive"):
            self.macd(self.sample_data['Close'], signal_period=0)

    def test_macd_empty_dataframe(self):
        """Test MACD calculation with empty dataframe."""
        empty_series = pd.Series(dtype=float)
        macd_line, signal_line, histogram = self.macd(empty_series)
        assert isinstance(macd_line, pd.Series)
        assert isinstance(signal_line, pd.Series)
        assert isinstance(histogram, pd.Series)
        assert len(macd_line) == 0
        assert len(signal_line) == 0
        assert len(histogram) == 0

    def test_macd_insufficient_data(self):
        """Test MACD calculation with insufficient data."""
        small_series = self.sample_data['Close'].head(10)
        macd_line, signal_line, histogram = self.macd(small_series, slow_period=20)
        assert macd_line.isna().all()
        assert signal_line.isna().all()
        assert histogram.isna().all()

    def test_macd_parameter_validation(self):
        """Test MACD parameter validation."""
        macd_line, signal_line, histogram = self.macd(self.sample_data['Close'], fast_period=12, slow_period=26, signal_period=9)
        assert isinstance(macd_line, pd.Series)
        assert isinstance(signal_line, pd.Series)
        assert isinstance(histogram, pd.Series)
        macd_line, signal_line, histogram = self.macd(self.sample_data['Close'], fast_period=int(12.5), slow_period=int(26.5), signal_period=int(9.5))
        assert isinstance(macd_line, pd.Series)
        assert isinstance(signal_line, pd.Series)
        assert isinstance(histogram, pd.Series)

    def test_macd_with_nan_values(self):
        """Test MACD calculation with NaN values in data."""
        data_with_nan = self.sample_data['Close'].copy()
        data_with_nan.loc[5] = np.nan
        macd_line, signal_line, histogram = self.macd(data_with_nan)
        assert isinstance(macd_line, pd.Series)
        assert isinstance(signal_line, pd.Series)
        assert isinstance(histogram, pd.Series)
        assert len(macd_line) == len(data_with_nan)
        assert len(signal_line) == len(data_with_nan)
        assert len(histogram) == len(data_with_nan)

    def test_macd_performance(self):
        """Test MACD calculation performance with larger dataset."""
        large_series = pd.Series(np.random.uniform(100, 200, 10000))
        import time
        start_time = time.time()
        macd_line, signal_line, histogram = self.macd(large_series)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(macd_line, pd.Series)
        assert isinstance(signal_line, pd.Series)
        assert isinstance(histogram, pd.Series)

    def test_macd_apply_rule(self):
        """Test MACD rule application."""
        result = apply_rule_macd(self.sample_data, point=0.01)
        assert 'MACD_Line' in result
        assert 'MACD_Signal' in result
        assert 'MACD_Histogram' in result
        assert 'MACD_Trading_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['MACD_Trading_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 