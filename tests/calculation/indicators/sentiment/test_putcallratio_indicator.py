# tests/calculation/indicators/sentiment/test_putcallratio_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.sentiment.putcallratio_ind import calculate_putcallratio, apply_rule_putcallratio

class TestPutCallRatioIndicator:
    def setup_method(self):
        # Задаём одинаковый индекс для всех Series
        idx = pd.RangeIndex(0, 30)
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=idx)
        self.putcallratio = calculate_putcallratio

    def test_putcallratio_calculation_basic(self):
        close = self.sample_data['Close'].reset_index(drop=True)
        volume = self.sample_data['Volume'].reset_index(drop=True)
        result = self.putcallratio(close, volume)
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data)

    def test_putcallratio_with_custom_period(self):
        close = self.sample_data['Close'].reset_index(drop=True)
        volume = self.sample_data['Volume'].reset_index(drop=True)
        result = self.putcallratio(close, volume, period=10)
        assert isinstance(result, pd.Series)
        assert result.iloc[:9].isna().all()
        assert not result.iloc[9:].isna().all()

    def test_putcallratio_with_invalid_period(self):
        close = self.sample_data['Close'].reset_index(drop=True)
        volume = self.sample_data['Volume'].reset_index(drop=True)
        with pytest.raises(ValueError, match="Put/Call Ratio period must be positive"):
            self.putcallratio(close, volume, period=0)
        with pytest.raises(ValueError, match="Put/Call Ratio period must be positive"):
            self.putcallratio(close, volume, period=-1)

    def test_putcallratio_empty_dataframe(self):
        empty_series = pd.Series(dtype=float)
        empty_volume = pd.Series(dtype=float)
        result = self.putcallratio(empty_series, empty_volume)
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_putcallratio_insufficient_data(self):
        close = self.sample_data['Close'].head(5).reset_index(drop=True)
        volume = self.sample_data['Volume'].head(5).reset_index(drop=True)
        result = self.putcallratio(close, volume, period=20)
        assert result.isna().all()

    def test_putcallratio_parameter_validation(self):
        close = self.sample_data['Close'].reset_index(drop=True)
        volume = self.sample_data['Volume'].reset_index(drop=True)
        result = self.putcallratio(close, volume, period=20)
        assert isinstance(result, pd.Series)
        result = self.putcallratio(close, volume, period=int(20.5))
        assert isinstance(result, pd.Series)

    def test_putcallratio_with_nan_values(self):
        close = self.sample_data['Close'].copy().reset_index(drop=True)
        volume = self.sample_data['Volume'].copy().reset_index(drop=True)
        close.iloc[5] = np.nan
        volume.iloc[5] = np.nan
        result = self.putcallratio(close, volume)
        assert isinstance(result, pd.Series)
        assert len(result) == len(close)

    def test_putcallratio_performance(self):
        close = pd.Series(np.random.uniform(100, 200, 10000))
        volume = pd.Series(np.random.uniform(1000, 5000, 10000))
        close = close.reset_index(drop=True)
        volume = volume.reset_index(drop=True)
        import time
        start_time = time.time()
        result = self.putcallratio(close, volume)
        end_time = time.time()
        assert end_time - start_time < 2.0
        assert isinstance(result, pd.Series)

    def test_putcallratio_apply_rule(self):
        result = apply_rule_putcallratio(self.sample_data, point=0.01)
        assert 'PutCallRatio' in result
        assert 'PutCallRatio_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['PutCallRatio_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 