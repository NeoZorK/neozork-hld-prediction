# tests/calculation/indicators/suportresist/test_donchain_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.suportresist.donchain_ind import calculate_donchain, apply_rule_donchain

class TestDonchainIndicator:
    def setup_method(self):
        self.donchain = DonchainIndicator()
        self.sample_data = pd.DataFrame({
            'close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_donchain_initialization(self):
        assert self.donchain.name == "Donchain"
        assert self.donchain.category == "suportresist"
        assert "Donchian" in self.donchain.description

    def test_donchain_calculation_basic(self):
        result = self.donchain.calculate(self.sample_data)
        assert isinstance(result, pd.DataFrame)
        assert 'Donchain_Upper' in result.columns
        assert 'Donchain_Lower' in result.columns
        assert len(result) == len(self.sample_data)

    def test_donchain_custom_period(self):
        donchain_custom = DonchainIndicator(period=5)
        result = donchain_custom.calculate(self.sample_data)
        assert 'Donchain_Upper' in result.columns
        assert 'Donchain_Lower' in result.columns

    def test_donchain_invalid_period(self):
        with pytest.raises(ValueError):
            DonchainIndicator(period=0)
        with pytest.raises(ValueError):
            DonchainIndicator(period=-1)

    def test_donchain_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = self.donchain.calculate(empty_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_donchain_missing_columns(self):
        incomplete = self.sample_data.drop(columns=['high'])
        with pytest.raises(ValueError):
            self.donchain.calculate(incomplete)

    def test_donchain_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'high'] = np.nan
        result = self.donchain.calculate(data_with_nan)
        assert 'Donchain_Upper' in result.columns
        assert 'Donchain_Lower' in result.columns

    def test_donchain_consistency(self):
        result1 = self.donchain.calculate(self.sample_data)
        result2 = self.donchain.calculate(self.sample_data)
        pd.testing.assert_frame_equal(result1, result2) 