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
        result = self.fiboretr(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
        assert 'Fiboretr_0' in result.columns
        assert 'Fiboretr_236' in result.columns
        assert 'Fiboretr_382' in result.columns
        assert 'Fiboretr_500' in result.columns
        assert 'Fiboretr_618' in result.columns
        assert 'Fiboretr_786' in result.columns
        assert 'Fiboretr_100' in result.columns

    def test_fiboretr_with_custom_period(self):
        result = self.fiboretr(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=10)
        assert isinstance(result, pd.DataFrame)
        assert result.iloc[:9]['Fiboretr_236'].isna().all()
        assert not result.iloc[9:]['Fiboretr_236'].isna().all()

    def test_fiboretr_with_invalid_period(self):
        with pytest.raises(ValueError, match="Fibonacci period must be positive"):
            self.fiboretr(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=0)
        with pytest.raises(ValueError, match="Fibonacci period must be positive"):
            self.fiboretr(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=-1)

    def test_fiboretr_empty_dataframe(self):
        empty_series = pd.Series(dtype=float)
        result = self.fiboretr(empty_series, empty_series, empty_series)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_fiboretr_insufficient_data(self):
        small_high = self.sample_data['High'].head(5)
        small_low = self.sample_data['Low'].head(5)
        small_close = self.sample_data['Close'].head(5)
        result = self.fiboretr(small_high, small_low, small_close, period=20)
        assert result['Fiboretr_236'].isna().all()

    def test_fiboretr_parameter_validation(self):
        result = self.fiboretr(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=20)
        assert isinstance(result, pd.DataFrame)
        result = self.fiboretr(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=int(20.5))
        assert isinstance(result, pd.DataFrame)

    def test_fiboretr_with_nan_values(self):
        high_with_nan = self.sample_data['High'].copy()
        high_with_nan.loc[5] = np.nan
        result = self.fiboretr(high_with_nan, self.sample_data['Low'], self.sample_data['Close'])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(high_with_nan)

    def test_fiboretr_performance(self):
        large_high = pd.Series(np.random.uniform(100, 200, 10000))
        large_low = pd.Series(np.random.uniform(50, 100, 10000))
        large_close = pd.Series(np.random.uniform(75, 150, 10000))
        import time
        start_time = time.time()
        result = self.fiboretr(large_high, large_low, large_close)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, pd.DataFrame)

    def test_fiboretr_apply_rule(self):
        result = apply_rule_fiboretr(self.sample_data, point=0.01)
        assert 'Fiboretr_0' in result
        assert 'Fiboretr_236' in result
        assert 'Fiboretr_382' in result
        assert 'Fiboretr_500' in result
        assert 'Fiboretr_618' in result
        assert 'Fiboretr_786' in result
        assert 'Fiboretr_100' in result
        assert 'Fiboretr_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['Fiboretr_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 