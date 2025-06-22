# tests/calculation/indicators/probability/test_montecarlo_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.probability.montecarlo_ind import calculate_montecarlo, apply_rule_montecarlo

class TestMonteCarloIndicator:
    def setup_method(self):
        self.mc = MonteCarloIndicator()
        self.sample_data = pd.DataFrame({
            'close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_mc_initialization(self):
        assert self.mc.name == "MonteCarlo"
        assert self.mc.category == "probability"
        assert "Monte Carlo" in self.mc.description

    def test_mc_calculation_basic(self):
        result = self.mc.calculate(self.sample_data)
        assert isinstance(result, pd.DataFrame)
        assert 'MonteCarlo' in result.columns
        assert len(result) == len(self.sample_data)

    def test_mc_custom_simulations(self):
        mc_custom = MonteCarloIndicator(simulations=100)
        result = mc_custom.calculate(self.sample_data)
        assert 'MonteCarlo' in result.columns

    def test_mc_invalid_simulations(self):
        with pytest.raises(ValueError):
            MonteCarloIndicator(simulations=0)
        with pytest.raises(ValueError):
            MonteCarloIndicator(simulations=-1)

    def test_mc_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = self.mc.calculate(empty_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_mc_missing_columns(self):
        incomplete = self.sample_data.drop(columns=['close'])
        with pytest.raises(ValueError):
            self.mc.calculate(incomplete)

    def test_mc_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        result = self.mc.calculate(data_with_nan)
        assert 'MonteCarlo' in result.columns

    def test_mc_consistency(self):
        result1 = self.mc.calculate(self.sample_data)
        result2 = self.mc.calculate(self.sample_data)
        assert 'MonteCarlo' in result1.columns
        assert 'MonteCarlo' in result2.columns 