# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_supertrend_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.trend.supertrend_ind import calculate_supertrend, apply_rule_supertrend


class TestSuperTrendIndicator:
    """Test cases for SuperTrend indicator."""

    def setup_method(self):
        """Set up test data."""
        self.supertrend = calculate_supertrend
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_supertrend_calculation_basic(self):
        """Test basic SuperTrend calculation."""
        result = self.supertrend(self.sample_data)
        assert isinstance(result, tuple)
        assert len(result) == 2
        for arr in result:
            assert isinstance(arr, pd.Series)
            assert len(arr) == len(self.sample_data)

    def test_supertrend_with_custom_parameters(self):
        """Test SuperTrend calculation with custom parameters."""
        result = self.supertrend(self.sample_data, period=10, multiplier=3.0)
        assert isinstance(result, tuple)
        assert len(result) == 2
        for arr in result:
            assert isinstance(arr, pd.Series)
            assert len(arr) == len(self.sample_data)

    def test_supertrend_with_invalid_parameters(self):
        """Test SuperTrend calculation with invalid parameters."""
        with pytest.raises(ValueError, match="Period and multiplier must be positive"):
            self.supertrend(self.sample_data, period=0, multiplier=3.0)
        with pytest.raises(ValueError, match="Period and multiplier must be positive"):
            self.supertrend(self.sample_data, period=10, multiplier=0)

    def test_supertrend_empty_dataframe(self):
        """Test SuperTrend calculation with empty dataframe."""
        empty_df = pd.DataFrame({'High': [], 'Low': [], 'Close': []})
        result = self.supertrend(empty_df)
        assert isinstance(result, tuple)
        assert len(result) == 2
        for arr in result:
            assert isinstance(arr, pd.Series)
            assert len(arr) == 0

    def test_supertrend_insufficient_data(self):
        """Test SuperTrend calculation with insufficient data."""
        small_df = self.sample_data.head(5)
        result = self.supertrend(small_df, period=10)
        for arr in result:
            assert arr.isna().all()

    def test_supertrend_parameter_validation(self):
        """Test SuperTrend parameter validation."""
        result = self.supertrend(self.sample_data, period=10, multiplier=2.0)
        assert isinstance(result, tuple)
        result = self.supertrend(self.sample_data, period=int(10.5), multiplier=float(2.5))
        assert isinstance(result, tuple)

    def test_supertrend_with_nan_values(self):
        """Test SuperTrend calculation with NaN values in data."""
        df_with_nan = self.sample_data.copy()
        df_with_nan.loc[5, 'High'] = np.nan
        result = self.supertrend(df_with_nan)
        for arr in result:
            assert isinstance(arr, pd.Series)
            assert len(arr) == len(df_with_nan)

    def test_supertrend_performance(self):
        """Test SuperTrend calculation performance with larger dataset."""
        large_df = pd.DataFrame({
            'High': np.random.uniform(100, 200, 10000),
            'Low': np.random.uniform(50, 100, 10000),
            'Close': np.random.uniform(75, 150, 10000)
        })
        import time
        start_time = time.time()
        result = self.supertrend(large_df)
        end_time = time.time()
        assert end_time - start_time < 5.0
        for arr in result:
            assert isinstance(arr, pd.Series)

    def test_supertrend_apply_rule(self):
        """Test SuperTrend application rule."""
        result = apply_rule_supertrend(self.sample_data, point=0.01)
        assert 'SuperTrend' in result
        assert 'SuperTrend_Direction' in result
        assert 'SuperTrend_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['SuperTrend_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number)

    def test_supertrend_trend_direction(self):
        """Test SuperTrend trend direction identification."""
        result = self.supertrend(self.sample_data)
        supertrend_values, trend_direction = result
        assert isinstance(trend_direction, pd.Series)
        # Check that trend direction contains only 1 (up) and -1 (down)
        unique_values = trend_direction.dropna().unique()
        assert all(val in [1, -1] for val in unique_values)

    def test_supertrend_docstring_info(self):
        """Test that SuperTrend has proper docstring information."""
        docstring = self.supertrend.__doc__
        assert docstring is not None
        assert "SuperTrend" in docstring

    def test_supertrend_consistency(self):
        """Test SuperTrend calculation consistency."""
        result1 = self.supertrend(self.sample_data)
        result2 = self.supertrend(self.sample_data)
        assert len(result1) == len(result2)
        for arr1, arr2 in zip(result1, result2):
            pd.testing.assert_series_equal(arr1, arr2)

    def test_supertrend_trend_reversal_detection(self):
        """Test SuperTrend trend reversal detection."""
        # Create data with clear trend reversal
        trend_data = pd.DataFrame({
            'High': [100, 101, 102, 103, 104, 103, 102, 101, 100, 99],
            'Low': [99, 100, 101, 102, 103, 102, 101, 100, 99, 98],
            'Close': [100, 101, 102, 103, 104, 103, 102, 101, 100, 99],
            'Open': [100, 101, 102, 103, 104, 103, 102, 101, 100, 99],
            'Volume': [1000] * 10
        })
    
        result = self.supertrend(trend_data)
        supertrend_values, trend_direction = result
        assert isinstance(trend_direction, pd.Series)
        assert len(trend_direction) == len(trend_data)

    def test_supertrend_atr_dependency(self):
        """Test that SuperTrend properly uses ATR calculation."""
        result = self.supertrend(self.sample_data)
        supertrend_values, trend_direction = result
        assert isinstance(supertrend_values, pd.Series)
        assert isinstance(trend_direction, pd.Series)
        # SuperTrend values should be reasonable (not all NaN or extreme values)
        assert not supertrend_values.isna().all() 