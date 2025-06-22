# tests/calculation/indicators/sentiment/test_putcallratio_indicator.py

import pytest
import pandas as pd
import numpy as np
from src/calculation/indicators/sentiment/putcallratio_ind import PutCallRatioIndicator

class TestPutCallRatioIndicator:
    def setup_method(self):
        self.pcr = PutCallRatioIndicator()
        self.sample_data = pd.DataFrame({
            'close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_pcr_initialization(self):
        assert self.pcr.name == "PutCallRatio"
        assert self.pcr.category == "sentiment"
        assert "Put" in self.pcr.description or "Call" in self.pcr.description

    def test_pcr_calculation_basic(self):
        result = self.pcr.calculate(self.sample_data)
        assert isinstance(result, pd.DataFrame)
        assert 'PutCallRatio' in result.columns
        assert len(result) == len(self.sample_data)

    def test_pcr_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = self.pcr.calculate(empty_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_pcr_missing_columns(self):
        incomplete = self.sample_data.drop(columns=['close'])
        with pytest.raises(ValueError):
            self.pcr.calculate(incomplete)

    def test_pcr_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        result = self.pcr.calculate(data_with_nan)
        assert 'PutCallRatio' in result.columns

    def test_pcr_consistency(self):
        result1 = self.pcr.calculate(self.sample_data)
        result2 = self.pcr.calculate(self.sample_data)
        assert 'PutCallRatio' in result1.columns
        assert 'PutCallRatio' in result2.columns 