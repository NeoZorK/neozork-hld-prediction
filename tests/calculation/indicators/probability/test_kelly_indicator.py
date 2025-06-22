# tests/calculation/indicators/probability/test_kelly_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.probability.kelly_ind import calculate_kelly, apply_rule_kelly

class TestKellyIndicator:
    def setup_method(self):
        self.kelly = KellyIndicator()
        self.sample_data = pd.DataFrame({
            'close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_kelly_initialization(self):
        assert self.kelly.name == "Kelly"
        assert self.kelly.category == "probability"
        assert "Kelly" in self.kelly.description

    def test_kelly_calculation_basic(self):
        result = self.kelly.calculate(self.sample_data)
        assert isinstance(result, pd.DataFrame)
        assert 'Kelly' in result.columns
        assert len(result) == len(self.sample_data)

    def test_kelly_custom_parameters(self):
        kelly_custom = KellyIndicator(window=5)
        result = kelly_custom.calculate(self.sample_data)
        assert 'Kelly' in result.columns

    def test_kelly_invalid_window(self):
        with pytest.raises(ValueError):
            KellyIndicator(window=0)
        with pytest.raises(ValueError):
            KellyIndicator(window=-1)

    def test_kelly_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = self.kelly.calculate(empty_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_kelly_missing_columns(self):
        incomplete = self.sample_data.drop(columns=['close'])
        with pytest.raises(ValueError):
            self.kelly.calculate(incomplete)

    def test_kelly_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        result = self.kelly.calculate(data_with_nan)
        assert 'Kelly' in result.columns

    def test_kelly_consistency(self):
        result1 = self.kelly.calculate(self.sample_data)
        result2 = self.kelly.calculate(self.sample_data)
        assert 'Kelly' in result1.columns
        assert 'Kelly' in result2.columns 