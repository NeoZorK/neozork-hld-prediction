# tests/calculation/indicators/suportresist/test_fiboretr_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.suportresist.fiboretr_ind import calculate_fiboretr, apply_rule_fiboretr

class TestFiboretrIndicator:
    def setup_method(self):
        self.fiboretr = calculate_fiboretr
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_fiboretr_calculation_basic(self):
        result = self.fiboretr(self.sample_data)
        assert isinstance(result, tuple)
        assert len(result) == 3
        for level in result:
            assert isinstance(level, pd.Series)
            assert len(level) == len(self.sample_data)

    def test_fiboretr_with_custom_period(self):
        result = self.fiboretr(self.sample_data, period=10)
        assert isinstance(result, tuple)
        assert len(result) == 3
        for level in result:
            assert level.iloc[:9].isna().all()
            assert not level.iloc[9:].isna().all()

    def test_fiboretr_with_invalid_period(self):
        with pytest.raises(ValueError, match="Fibonacci Retracement period must be positive"):
            self.fiboretr(self.sample_data, period=0)
        with pytest.raises(ValueError, match="Fibonacci Retracement period must be positive"):
            self.fiboretr(self.sample_data, period=-1)

    def test_fiboretr_empty_dataframe(self):
        empty_df = pd.DataFrame({'High': [], 'Low': [], 'Close': []})
        result = self.fiboretr(empty_df)
        assert isinstance(result, tuple)
        assert len(result) == 3
        for level in result:
            assert isinstance(level, pd.Series)
            assert len(level) == 0

    def test_fiboretr_insufficient_data(self):
        small_df = self.sample_data.head(5)
        result = self.fiboretr(small_df, period=20)
        for level in result:
            assert level.isna().all()

    def test_fiboretr_parameter_validation(self):
        result = self.fiboretr(self.sample_data, period=20)
        assert isinstance(result, tuple)
        result = self.fiboretr(self.sample_data, period=int(20.5))
        assert isinstance(result, tuple)

    def test_fiboretr_with_nan_values(self):
        df_with_nan = self.sample_data.copy()
        df_with_nan.loc[5, 'High'] = np.nan
        result = self.fiboretr(df_with_nan)
        for level in result:
            assert isinstance(level, pd.Series)
            assert len(level) == len(df_with_nan)

    def test_fiboretr_performance(self):
        large_df = pd.DataFrame({
            'High': np.random.uniform(100, 200, 10000),
            'Low': np.random.uniform(50, 100, 10000),
            'Close': np.random.uniform(75, 150, 10000)
        })
        import time
        start_time = time.time()
        result = self.fiboretr(large_df)
        end_time = time.time()
        assert end_time - start_time < 5.0
        for level in result:
            assert isinstance(level, pd.Series)

    def test_fiboretr_apply_rule(self):
        result = apply_rule_fiboretr(self.sample_data, point=0.01)
        assert 'FibRetr_236' in result
        assert 'FibRetr_382' in result
        assert 'FibRetr_618' in result
        assert 'FibRetr_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['FibRetr_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 