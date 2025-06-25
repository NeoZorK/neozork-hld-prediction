# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_adx_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.trend.adx_ind import calculate_adx, apply_rule_adx


class TestADXIndicator:
    """Test cases for ADX (Average Directional Index) indicator."""

    def setup_method(self):
        """Set up test data."""
        self.adx = calculate_adx
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_adx_calculation_basic(self):
        """Test basic ADX calculation."""
        result = self.adx(self.sample_data)
        assert isinstance(result, tuple)
        assert len(result) == 3
        for arr in result:
            assert isinstance(arr, pd.Series)
            assert len(arr) == len(self.sample_data)

    def test_adx_with_custom_period(self):
        """Test ADX calculation with custom period."""
        result = self.adx(self.sample_data, period=10)
        assert isinstance(result, tuple)
        assert len(result) == 3
        for arr in result:
            assert isinstance(arr, pd.Series)
            assert len(arr) == len(self.sample_data)
            # ADX may have values from the beginning, so we just check it's not all NaN
            assert not arr.isna().all()

    def test_adx_with_invalid_period(self):
        """Test ADX calculation with invalid period."""
        with pytest.raises(ValueError, match="ADX period must be positive"):
            self.adx(self.sample_data, period=0)
        with pytest.raises(ValueError, match="ADX period must be positive"):
            self.adx(self.sample_data, period=-1)

    def test_adx_empty_dataframe(self):
        """Test ADX calculation with empty dataframe."""
        empty_df = pd.DataFrame({'High': [], 'Low': [], 'Close': []})
        result = self.adx(empty_df)
        assert isinstance(result, tuple)
        assert len(result) == 3
        for arr in result:
            assert isinstance(arr, pd.Series)
            assert len(arr) == 0

    def test_adx_insufficient_data(self):
        """Test ADX calculation with insufficient data."""
        small_df = self.sample_data.head(5)
        result = self.adx(small_df, period=14)
        for arr in result:
            assert arr.isna().all()

    def test_adx_parameter_validation(self):
        """Test ADX parameter validation."""
        result = self.adx(self.sample_data, period=14)
        assert isinstance(result, tuple)
        result = self.adx(self.sample_data, period=int(14.5))
        assert isinstance(result, tuple)

    def test_adx_with_nan_values(self):
        """Test ADX calculation with NaN values in data."""
        df_with_nan = self.sample_data.copy()
        df_with_nan.loc[5, 'High'] = np.nan
        result = self.adx(df_with_nan)
        for arr in result:
            assert isinstance(arr, pd.Series)
            assert len(arr) == len(df_with_nan)

    def test_adx_performance(self):
        """Test ADX calculation performance with larger dataset."""
        large_df = pd.DataFrame({
            'High': np.random.uniform(100, 200, 10000),
            'Low': np.random.uniform(50, 100, 10000),
            'Close': np.random.uniform(75, 150, 10000)
        })
        import time
        start_time = time.time()
        result = self.adx(large_df)
        end_time = time.time()
        assert end_time - start_time < 5.0
        for arr in result:
            assert isinstance(arr, pd.Series)

    def test_adx_apply_rule(self):
        """Test ADX application rule."""
        result = apply_rule_adx(self.sample_data, point=0.01)
        assert 'ADX' in result
        assert 'ADX_PlusDI' in result
        assert 'ADX_MinusDI' in result
        assert 'ADX_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['ADX_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 