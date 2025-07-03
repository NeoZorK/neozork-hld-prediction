# tests/calculation/indicators/sentiment/test_cot_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.sentiment.cot_ind import calculate_cot, apply_rule_cot

class TestCOTIndicator:
    def setup_method(self):
        self.cot = calculate_cot
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_cot_calculation_basic(self):
        result = self.cot(self.sample_data['Close'], self.sample_data['Volume'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data)
        assert not result.isna().all()

    def test_cot_with_custom_period(self):
        result = self.cot(self.sample_data['Close'], self.sample_data['Volume'], period=10)
        assert isinstance(result, pd.Series)
        assert result.iloc[:9].isna().all()
        assert not result.iloc[9:].isna().all()

    def test_cot_with_invalid_period(self):
        with pytest.raises(ValueError, match="COT period must be positive"):
            self.cot(self.sample_data['Close'], self.sample_data['Volume'], period=0)
        with pytest.raises(ValueError, match="COT period must be positive"):
            self.cot(self.sample_data['Close'], self.sample_data['Volume'], period=-1)

    def test_cot_empty_dataframe(self):
        empty_series = pd.Series(dtype=float)
        result = self.cot(empty_series, empty_series)
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_cot_insufficient_data(self):
        small_series = self.sample_data['Close'].head(5)
        small_volume = self.sample_data['Volume'].head(5)
        result = self.cot(small_series, small_volume, period=20)
        assert result.isna().all()

    def test_cot_parameter_validation(self):
        result = self.cot(self.sample_data['Close'], self.sample_data['Volume'], period=20)
        assert isinstance(result, pd.Series)
        result = self.cot(self.sample_data['Close'], self.sample_data['Volume'], period=int(20.5))
        assert isinstance(result, pd.Series)

    def test_cot_with_nan_values(self):
        close_with_nan = self.sample_data['Close'].copy()
        close_with_nan.loc[5] = np.nan
        result = self.cot(close_with_nan, self.sample_data['Volume'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(close_with_nan)

    def test_cot_performance(self):
        large_series = pd.Series(np.random.uniform(100, 200, 10000))
        large_volume = pd.Series(np.random.uniform(1000, 5000, 10000), index=large_series.index)
        import time
        start_time = time.time()
        result = self.cot(large_series, large_volume)
        end_time = time.time()
        assert end_time - start_time < 10.0
        assert isinstance(result, pd.Series)

    def test_cot_apply_rule(self):
        result = apply_rule_cot(self.sample_data, point=0.01)
        assert 'COT' in result
        assert 'COT_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['COT_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number)

    def test_cot_with_only_volume_column(self):
        """Test that apply_rule_cot works with only 'Volume' column (no 'TickVolume')."""
        df = self.sample_data.copy()
        # Удаляем TickVolume, если вдруг есть
        if 'TickVolume' in df.columns:
            df = df.drop(columns=['TickVolume'])
        # Проверяем, что нет TickVolume
        assert 'TickVolume' not in df.columns
        # Должен работать без ошибок
        result = apply_rule_cot(df, point=0.01, cot_period=10, price_type='close')
        assert 'COT' in result
        assert 'COT_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        # Проверяем, что нет ошибок и есть значения
        assert not result['COT'].isna().all() 