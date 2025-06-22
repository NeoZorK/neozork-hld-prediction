# tests/calculation/indicators/predictive/test_tsforecast_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.predictive.tsforecast_ind import calculate_tsforecast, apply_rule_tsforecast

class TestTSForecastIndicator:
    def setup_method(self):
        self.tsf = TSForecastIndicator()
        self.sample_data = pd.DataFrame({
            'close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_tsf_initialization(self):
        assert self.tsf.name == "TSForecast"
        assert self.tsf.category == "predictive"
        assert "Time Series Forecast" in self.tsf.description

    def test_tsf_calculation_basic(self):
        result = self.tsf.calculate(self.sample_data)
        assert isinstance(result, pd.DataFrame)
        assert 'TSForecast' in result.columns
        assert len(result) == len(self.sample_data)

    def test_tsf_custom_period(self):
        tsf_custom = TSForecastIndicator(period=5)
        result = tsf_custom.calculate(self.sample_data)
        assert 'TSForecast' in result.columns

    def test_tsf_invalid_period(self):
        with pytest.raises(ValueError):
            TSForecastIndicator(period=0)
        with pytest.raises(ValueError):
            TSForecastIndicator(period=-1)

    def test_tsf_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = self.tsf.calculate(empty_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_tsf_missing_columns(self):
        incomplete = self.sample_data.drop(columns=['close'])
        with pytest.raises(ValueError):
            self.tsf.calculate(incomplete)

    def test_tsf_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        result = self.tsf.calculate(data_with_nan)
        assert 'TSForecast' in result.columns

    def test_tsf_consistency(self):
        result1 = self.tsf.calculate(self.sample_data)
        result2 = self.tsf.calculate(self.sample_data)
        pd.testing.assert_frame_equal(result1, result2) 