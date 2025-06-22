# -*- coding: utf-8 -*-
# tests/calculation/indicators/oscillators/test_cci_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.oscillators.cci_ind import calculate_cci, apply_rule_cci


class TestCCIIndicator:
    """Test cases for CCI (Commodity Channel Index) indicator."""

    def setup_method(self):
        """Set up test data."""
        self.cci = calculate_cci
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_cci_calculation_basic(self):
        """Test basic CCI calculation."""
        result = self.cci(self.sample_data['Close'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data)
        assert not result.isna().all()

    def test_cci_with_custom_period(self):
        """Test CCI calculation with custom period."""
        result = self.cci(self.sample_data['Close'], period=10)
        assert isinstance(result, pd.Series)
        assert result.iloc[:9].isna().all()
        assert not result.iloc[9:].isna().all()

    def test_cci_with_invalid_period(self):
        """Test CCI calculation with invalid period."""
        with pytest.raises(ValueError, match="CCI period must be positive"):
            self.cci(self.sample_data['Close'], period=0)
        with pytest.raises(ValueError, match="CCI period must be positive"):
            self.cci(self.sample_data['Close'], period=-1)

    def test_cci_empty_dataframe(self):
        """Test CCI calculation with empty dataframe."""
        empty_series = pd.Series(dtype=float)
        result = self.cci(empty_series)
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_cci_insufficient_data(self):
        """Test CCI calculation with insufficient data."""
        small_series = self.sample_data['Close'].head(5)
        result = self.cci(small_series, period=20)
        assert result.isna().all()

    def test_cci_parameter_validation(self):
        """Test CCI parameter validation."""
        result = self.cci(self.sample_data['Close'], period=20)
        assert isinstance(result, pd.Series)
        result = self.cci(self.sample_data['Close'], period=int(20.5))
        assert isinstance(result, pd.Series)

    def test_cci_with_nan_values(self):
        """Test CCI calculation with NaN values in data."""
        data_with_nan = self.sample_data['Close'].copy()
        data_with_nan.loc[5] = np.nan
        result = self.cci(data_with_nan)
        assert isinstance(result, pd.Series)
        assert len(result) == len(data_with_nan)

    def test_cci_performance(self):
        """Test CCI calculation performance with larger dataset."""
        large_series = pd.Series(np.random.uniform(100, 200, 10000))
        import time
        start_time = time.time()
        result = self.cci(large_series)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, pd.Series)

    def test_cci_apply_rule(self):
        """Test CCI rule application."""
        result = apply_rule_cci(self.sample_data, point=0.01)
        assert 'CCI' in result
        assert 'CCI_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['CCI_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 