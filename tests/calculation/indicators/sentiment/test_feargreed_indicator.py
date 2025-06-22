# tests/calculation/indicators/sentiment/test_feargreed_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.sentiment.feargreed_ind import calculate_feargreed, apply_rule_feargreed

class TestFearGreedIndicator:
    def setup_method(self):
        self.feargreed = calculate_feargreed
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_feargreed_calculation_basic(self):
        result = self.feargreed(self.sample_data['Close'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data)
        assert not result.isna().all()

    def test_feargreed_with_custom_period(self):
        result = self.feargreed(self.sample_data['Close'], period=10)
        assert isinstance(result, pd.Series)
        assert result.iloc[:9].isna().all()
        assert not result.iloc[9:].isna().all()

    def test_feargreed_with_invalid_period(self):
        with pytest.raises(ValueError, match="Fear & Greed period must be positive"):
            self.feargreed(self.sample_data['Close'], period=0)
        with pytest.raises(ValueError, match="Fear & Greed period must be positive"):
            self.feargreed(self.sample_data['Close'], period=-1)

    def test_feargreed_empty_dataframe(self):
        empty_series = pd.Series(dtype=float)
        result = self.feargreed(empty_series)
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_feargreed_insufficient_data(self):
        small_series = self.sample_data['Close'].head(5)
        result = self.feargreed(small_series, period=20)
        assert result.isna().all()

    def test_feargreed_parameter_validation(self):
        result = self.feargreed(self.sample_data['Close'], period=20)
        assert isinstance(result, pd.Series)
        result = self.feargreed(self.sample_data['Close'], period=int(20.5))
        assert isinstance(result, pd.Series)

    def test_feargreed_with_nan_values(self):
        data_with_nan = self.sample_data['Close'].copy()
        data_with_nan.loc[5] = np.nan
        result = self.feargreed(data_with_nan)
        assert isinstance(result, pd.Series)
        assert len(result) == len(data_with_nan)

    def test_feargreed_performance(self):
        large_series = pd.Series(np.random.uniform(100, 200, 10000))
        import time
        start_time = time.time()
        result = self.feargreed(large_series)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, pd.Series)

    def test_feargreed_apply_rule(self):
        result = apply_rule_feargreed(self.sample_data, point=0.01)
        assert 'FearGreed' in result
        assert 'FearGreed_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['FearGreed_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 