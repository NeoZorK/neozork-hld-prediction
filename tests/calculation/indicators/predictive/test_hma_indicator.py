# tests/calculation/indicators/predictive/test_hma_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.predictive.hma_ind import HMAIndicator

class TestHMAIndicator:
    def setup_method(self):
        self.hma = HMAIndicator()
        self.sample_data = pd.DataFrame({
            'close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_hma_initialization(self):
        assert self.hma.name == "HMA"
        assert self.hma.category == "predictive"
        assert "Hull Moving Average" in self.hma.description

    def test_hma_calculation_basic(self):
        result = self.hma.calculate(self.sample_data)
        assert isinstance(result, pd.DataFrame)
        assert 'HMA' in result.columns
        assert len(result) == len(self.sample_data)

    def test_hma_custom_period(self):
        hma_custom = HMAIndicator(period=5)
        result = hma_custom.calculate(self.sample_data)
        assert 'HMA' in result.columns

    def test_hma_invalid_period(self):
        with pytest.raises(ValueError):
            HMAIndicator(period=0)
        with pytest.raises(ValueError):
            HMAIndicator(period=-1)

    def test_hma_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = self.hma.calculate(empty_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_hma_missing_columns(self):
        incomplete = self.sample_data.drop(columns=['close'])
        with pytest.raises(ValueError):
            self.hma.calculate(incomplete)

    def test_hma_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        result = self.hma.calculate(data_with_nan)
        assert 'HMA' in result.columns

    def test_hma_consistency(self):
        result1 = self.hma.calculate(self.sample_data)
        result2 = self.hma.calculate(self.sample_data)
        pd.testing.assert_frame_equal(result1, result2) 