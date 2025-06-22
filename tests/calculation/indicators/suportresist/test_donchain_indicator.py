# tests/calculation/indicators/suportresist/test_donchain_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.suportresist.donchain_ind import calculate_donchain, apply_rule_donchain

class TestDonchianIndicator:
    def setup_method(self):
        self.donchain = calculate_donchain
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_donchain_calculation_basic(self):
        result = self.donchain(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
        assert 'Donchian_Upper' in result.columns
        assert 'Donchian_Lower' in result.columns
        assert 'Donchian_Middle' in result.columns

    def test_donchain_with_custom_period(self):
        result = self.donchain(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=10)
        assert isinstance(result, pd.DataFrame)
        assert result.iloc[:9]['Donchian_Upper'].isna().all()
        assert not result.iloc[9:]['Donchian_Upper'].isna().all()

    def test_donchain_with_invalid_period(self):
        with pytest.raises(ValueError, match="Donchian period must be positive"):
            self.donchain(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=0)
        with pytest.raises(ValueError, match="Donchian period must be positive"):
            self.donchain(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=-1)

    def test_donchain_empty_dataframe(self):
        empty_series = pd.Series(dtype=float)
        result = self.donchain(empty_series, empty_series, empty_series)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_donchain_insufficient_data(self):
        small_high = self.sample_data['High'].head(5)
        small_low = self.sample_data['Low'].head(5)
        small_close = self.sample_data['Close'].head(5)
        result = self.donchain(small_high, small_low, small_close, period=20)
        assert result['Donchian_Upper'].isna().all()

    def test_donchain_parameter_validation(self):
        result = self.donchain(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=20)
        assert isinstance(result, pd.DataFrame)
        result = self.donchain(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=int(20.5))
        assert isinstance(result, pd.DataFrame)

    def test_donchain_with_nan_values(self):
        high_with_nan = self.sample_data['High'].copy()
        high_with_nan.loc[5] = np.nan
        result = self.donchain(high_with_nan, self.sample_data['Low'], self.sample_data['Close'])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(high_with_nan)

    def test_donchain_performance(self):
        large_high = pd.Series(np.random.uniform(100, 200, 10000))
        large_low = pd.Series(np.random.uniform(50, 100, 10000))
        large_close = pd.Series(np.random.uniform(75, 150, 10000))
        import time
        start_time = time.time()
        result = self.donchain(large_high, large_low, large_close)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, pd.DataFrame)

    def test_donchain_apply_rule(self):
        result = apply_rule_donchain(self.sample_data, point=0.01)
        assert 'Donchian_Upper' in result
        assert 'Donchian_Lower' in result
        assert 'Donchian_Middle' in result
        assert 'Donchian_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['Donchian_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 