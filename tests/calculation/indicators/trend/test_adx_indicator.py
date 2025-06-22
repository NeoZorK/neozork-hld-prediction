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
        result = self.adx(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
        assert 'ADX' in result.columns
        assert 'DI_Plus' in result.columns
        assert 'DI_Minus' in result.columns

    def test_adx_with_custom_period(self):
        """Test ADX calculation with custom period."""
        result = self.adx(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=10)
        assert isinstance(result, pd.DataFrame)
        assert result.iloc[:9]['ADX'].isna().all()
        assert not result.iloc[9:]['ADX'].isna().all()

    def test_adx_with_invalid_period(self):
        """Test ADX calculation with invalid period."""
        with pytest.raises(ValueError, match="ADX period must be positive"):
            self.adx(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=0)
        with pytest.raises(ValueError, match="ADX period must be positive"):
            self.adx(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=-1)

    def test_adx_empty_dataframe(self):
        """Test ADX calculation with empty dataframe."""
        empty_series = pd.Series(dtype=float)
        result = self.adx(empty_series, empty_series, empty_series)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_adx_insufficient_data(self):
        """Test ADX calculation with insufficient data."""
        small_high = self.sample_data['High'].head(5)
        small_low = self.sample_data['Low'].head(5)
        small_close = self.sample_data['Close'].head(5)
        result = self.adx(small_high, small_low, small_close, period=20)
        assert result['ADX'].isna().all()

    def test_adx_parameter_validation(self):
        """Test ADX parameter validation."""
        result = self.adx(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=20)
        assert isinstance(result, pd.DataFrame)
        result = self.adx(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=int(20.5))
        assert isinstance(result, pd.DataFrame)

    def test_adx_with_nan_values(self):
        """Test ADX calculation with NaN values in data."""
        high_with_nan = self.sample_data['High'].copy()
        high_with_nan.loc[5] = np.nan
        result = self.adx(high_with_nan, self.sample_data['Low'], self.sample_data['Close'])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(high_with_nan)

    def test_adx_performance(self):
        """Test ADX calculation performance with larger dataset."""
        large_high = pd.Series(np.random.uniform(100, 200, 10000))
        large_low = pd.Series(np.random.uniform(50, 100, 10000))
        large_close = pd.Series(np.random.uniform(75, 150, 10000))
        import time
        start_time = time.time()
        result = self.adx(large_high, large_low, large_close)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, pd.DataFrame)

    def test_adx_apply_rule(self):
        """Test ADX application rule."""
        result = apply_rule_adx(self.sample_data, point=0.01)
        assert 'ADX' in result
        assert 'DI_Plus' in result
        assert 'DI_Minus' in result
        assert 'ADX_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['ADX_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 