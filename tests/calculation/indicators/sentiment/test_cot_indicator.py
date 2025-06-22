# tests/calculation/indicators/sentiment/test_cot_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.sentiment.cot_ind import COTIndicator

class TestCOTIndicator:
    def setup_method(self):
        self.cot = COTIndicator()
        self.sample_data = pd.DataFrame({
            'close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_cot_initialization(self):
        assert self.cot.name == "COT"
        assert self.cot.category == "sentiment"
        assert "COT" in self.cot.description

    def test_cot_calculation_basic(self):
        result = self.cot.calculate(self.sample_data)
        assert isinstance(result, pd.DataFrame)
        assert 'COT' in result.columns
        assert len(result) == len(self.sample_data)

    def test_cot_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = self.cot.calculate(empty_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_cot_missing_columns(self):
        incomplete = self.sample_data.drop(columns=['close'])
        with pytest.raises(ValueError):
            self.cot.calculate(incomplete)

    def test_cot_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        result = self.cot.calculate(data_with_nan)
        assert 'COT' in result.columns

    def test_cot_consistency(self):
        result1 = self.cot.calculate(self.sample_data)
        result2 = self.cot.calculate(self.sample_data)
        assert 'COT' in result1.columns
        assert 'COT' in result2.columns 