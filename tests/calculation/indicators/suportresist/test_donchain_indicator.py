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
        result = self.donchain(self.sample_data)
        assert isinstance(result, tuple)
        assert len(result) == 3
        for band in result:
            assert isinstance(band, pd.Series)
            assert len(band) == len(self.sample_data)

    def test_donchain_with_custom_period(self):
        result = self.donchain(self.sample_data, period=10)
        assert isinstance(result, tuple)
        assert len(result) == 3
        for band in result:
            assert band.iloc[:9].isna().all()
            assert not band.iloc[9:].isna().all()

    def test_donchain_with_invalid_period(self):
        with pytest.raises(ValueError, match="Donchian Channel period must be positive"):
            self.donchain(self.sample_data, period=0)
        with pytest.raises(ValueError, match="Donchian Channel period must be positive"):
            self.donchain(self.sample_data, period=-1)

    def test_donchain_empty_dataframe(self):
        empty_df = pd.DataFrame({'High': [], 'Low': [], 'Close': []})
        result = self.donchain(empty_df)
        assert isinstance(result, tuple)
        assert len(result) == 3
        for band in result:
            assert isinstance(band, pd.Series)
            assert len(band) == 0

    def test_donchain_insufficient_data(self):
        small_df = self.sample_data.head(5)
        result = self.donchain(small_df, period=20)
        for band in result:
            assert band.isna().all()

    def test_donchain_parameter_validation(self):
        result = self.donchain(self.sample_data, period=20)
        assert isinstance(result, tuple)
        result = self.donchain(self.sample_data, period=int(20.5))
        assert isinstance(result, tuple)

    def test_donchain_with_nan_values(self):
        df_with_nan = self.sample_data.copy()
        df_with_nan.loc[5, 'High'] = np.nan
        result = self.donchain(df_with_nan)
        for band in result:
            assert isinstance(band, pd.Series)
            assert len(band) == len(df_with_nan)

    def test_donchain_performance(self):
        large_df = pd.DataFrame({
            'High': np.random.uniform(100, 200, 10000),
            'Low': np.random.uniform(50, 100, 10000),
            'Close': np.random.uniform(75, 150, 10000)
        })
        import time
        start_time = time.time()
        result = self.donchain(large_df)
        end_time = time.time()
        assert end_time - start_time < 5.0
        for band in result:
            assert isinstance(band, pd.Series)

    def test_donchain_apply_rule(self):
        result = apply_rule_donchain(self.sample_data, point=0.01)
        assert 'Donchain_Upper' in result
        assert 'Donchain_Middle' in result
        assert 'Donchain_Lower' in result
        assert 'Donchain_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['Donchain_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 