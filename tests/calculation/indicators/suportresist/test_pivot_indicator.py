# tests/calculation/indicators/suportresist/test_pivot_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.suportresist.pivot_ind import calculate_pivot, apply_rule_pivot

class TestPivotIndicator:
    def setup_method(self):
        self.pivot = calculate_pivot
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_pivot_calculation_basic(self):
        result = self.pivot(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
        assert 'Pivot' in result.columns
        assert 'R1' in result.columns
        assert 'R2' in result.columns
        assert 'R3' in result.columns
        assert 'S1' in result.columns
        assert 'S2' in result.columns
        assert 'S3' in result.columns

    def test_pivot_with_custom_period(self):
        result = self.pivot(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=10)
        assert isinstance(result, pd.DataFrame)
        assert result.iloc[:9]['Pivot'].isna().all()
        assert not result.iloc[9:]['Pivot'].isna().all()

    def test_pivot_with_invalid_period(self):
        with pytest.raises(ValueError, match="Pivot period must be positive"):
            self.pivot(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=0)
        with pytest.raises(ValueError, match="Pivot period must be positive"):
            self.pivot(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=-1)

    def test_pivot_empty_dataframe(self):
        empty_series = pd.Series(dtype=float)
        result = self.pivot(empty_series, empty_series, empty_series)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_pivot_insufficient_data(self):
        small_high = self.sample_data['High'].head(5)
        small_low = self.sample_data['Low'].head(5)
        small_close = self.sample_data['Close'].head(5)
        result = self.pivot(small_high, small_low, small_close, period=20)
        assert result['Pivot'].isna().all()

    def test_pivot_parameter_validation(self):
        result = self.pivot(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=20)
        assert isinstance(result, pd.DataFrame)
        result = self.pivot(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=int(20.5))
        assert isinstance(result, pd.DataFrame)

    def test_pivot_with_nan_values(self):
        high_with_nan = self.sample_data['High'].copy()
        high_with_nan.loc[5] = np.nan
        result = self.pivot(high_with_nan, self.sample_data['Low'], self.sample_data['Close'])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(high_with_nan)

    def test_pivot_performance(self):
        large_high = pd.Series(np.random.uniform(100, 200, 10000))
        large_low = pd.Series(np.random.uniform(50, 100, 10000))
        large_close = pd.Series(np.random.uniform(75, 150, 10000))
        import time
        start_time = time.time()
        result = self.pivot(large_high, large_low, large_close)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, pd.DataFrame)

    def test_pivot_apply_rule(self):
        result = apply_rule_pivot(self.sample_data, point=0.01)
        assert 'Pivot' in result
        assert 'R1' in result
        assert 'R2' in result
        assert 'R3' in result
        assert 'S1' in result
        assert 'S2' in result
        assert 'S3' in result
        assert 'Pivot_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['Pivot_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 