# tests/calculation/indicators/oscillators/test_rsi_ind_calc.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.oscillators.rsi_ind_calc import apply_rule_rsi, apply_rule_rsi_momentum, apply_rule_rsi_divergence, PriceType

class TestRSIIndCalc:
    def setup_method(self):
        self.df = pd.DataFrame({
            'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'open': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'high': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'low': [98, 99, 100, 101, 102, 103, 104, 105, 106, 107],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_apply_rule_rsi(self):
        result = apply_rule_rsi(self.df, point=0.01, rsi_period=5, price_type=PriceType.CLOSE)
        assert isinstance(result, pd.DataFrame)
        assert 'RSI' in result.columns
        assert len(result) == len(self.df)

    def test_apply_rule_rsi_open(self):
        result = apply_rule_rsi(self.df, point=0.01, rsi_period=5, price_type=PriceType.OPEN)
        assert 'RSI' in result.columns

    def test_apply_rule_rsi_invalid_period(self):
        with pytest.raises(ValueError):
            apply_rule_rsi(self.df, point=0.01, rsi_period=0, price_type=PriceType.CLOSE)
        with pytest.raises(ValueError):
            apply_rule_rsi(self.df, point=0.01, rsi_period=-1, price_type=PriceType.CLOSE)

    def test_apply_rule_rsi_momentum(self):
        result = apply_rule_rsi_momentum(self.df, point=0.01, rsi_period=5, price_type=PriceType.CLOSE)
        assert 'RSI_Momentum' in result.columns

    def test_apply_rule_rsi_divergence(self):
        result = apply_rule_rsi_divergence(self.df, point=0.01, rsi_period=5, price_type=PriceType.CLOSE)
        assert 'RSI_Divergence' in result.columns

    def test_apply_rule_rsi_nan(self):
        df_nan = self.df.copy()
        df_nan.iloc[2, self.df.columns.get_loc('close')] = np.nan
        result = apply_rule_rsi(df_nan, point=0.01, rsi_period=5, price_type=PriceType.CLOSE)
        assert 'RSI' in result.columns

    def test_apply_rule_rsi_empty(self):
        empty_df = pd.DataFrame()
        result = apply_rule_rsi(empty_df, point=0.01, rsi_period=5, price_type=PriceType.CLOSE)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0 