# tests/calculation/indicators/sentiment/test_feargreed_indicator.py

import pytest
import pandas as pd
import numpy as np
from src/calculation/indicators/sentiment/feargreed_ind import FearGreedIndicator

class TestFearGreedIndicator:
    def setup_method(self):
        self.fg = FearGreedIndicator()
        self.sample_data = pd.DataFrame({
            'close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_fg_initialization(self):
        assert self.fg.name == "FearGreed"
        assert self.fg.category == "sentiment"
        assert "Fear" in self.fg.description or "Greed" in self.fg.description

    def test_fg_calculation_basic(self):
        result = self.fg.calculate(self.sample_data)
        assert isinstance(result, pd.DataFrame)
        assert 'FearGreed' in result.columns
        assert len(result) == len(self.sample_data)

    def test_fg_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = self.fg.calculate(empty_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_fg_missing_columns(self):
        incomplete = self.sample_data.drop(columns=['close'])
        with pytest.raises(ValueError):
            self.fg.calculate(incomplete)

    def test_fg_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        result = self.fg.calculate(data_with_nan)
        assert 'FearGreed' in result.columns

    def test_fg_consistency(self):
        result1 = self.fg.calculate(self.sample_data)
        result2 = self.fg.calculate(self.sample_data)
        assert 'FearGreed' in result1.columns
        assert 'FearGreed' in result2.columns 