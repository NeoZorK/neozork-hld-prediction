# tests/calculation/indicators/suportresist/test_fiboretr_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.suportresist.fiboretr_ind import calculate_fiboretr, apply_rule_fiboretr

class TestFiboRetrIndicator:
    def setup_method(self):
        self.fibo = FiboRetrIndicator()
        self.sample_data = pd.DataFrame({
            'close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_fibo_initialization(self):
        assert self.fibo.name == "FiboRetr"
        assert self.fibo.category == "suportresist"
        assert "Fibonacci" in self.fibo.description or "Fibo" in self.fibo.description

    def test_fibo_calculation_basic(self):
        result = self.fibo.calculate(self.sample_data)
        assert isinstance(result, pd.DataFrame)
        assert 'FiboRetr_0.0' in result.columns
        assert 'FiboRetr_100.0' in result.columns
        assert len(result) == len(self.sample_data)

    def test_fibo_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = self.fibo.calculate(empty_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_fibo_missing_columns(self):
        incomplete = self.sample_data.drop(columns=['high'])
        with pytest.raises(ValueError):
            self.fibo.calculate(incomplete)

    def test_fibo_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'high'] = np.nan
        result = self.fibo.calculate(data_with_nan)
        assert 'FiboRetr_0.0' in result.columns
        assert 'FiboRetr_100.0' in result.columns

    def test_fibo_consistency(self):
        result1 = self.fibo.calculate(self.sample_data)
        result2 = self.fibo.calculate(self.sample_data)
        pd.testing.assert_frame_equal(result1, result2) 