# tests/calculation/indicators/suportresist/test_pivot_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.suportresist.pivot_ind import calculate_pivot_points, apply_rule_pivot

class TestPivotIndicator:
    def setup_method(self):
        self.pivot = PivotIndicator()
        self.sample_data = pd.DataFrame({
            'close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_pivot_initialization(self):
        assert self.pivot.name == "Pivot"
        assert self.pivot.category == "suportresist"
        assert "Pivot" in self.pivot.description

    def test_pivot_calculation_basic(self):
        result = self.pivot.calculate(self.sample_data)
        assert isinstance(result, pd.DataFrame)
        assert 'Pivot' in result.columns
        assert len(result) == len(self.sample_data)

    def test_pivot_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = self.pivot.calculate(empty_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_pivot_missing_columns(self):
        incomplete = self.sample_data.drop(columns=['high'])
        with pytest.raises(ValueError):
            self.pivot.calculate(incomplete)

    def test_pivot_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'high'] = np.nan
        result = self.pivot.calculate(data_with_nan)
        assert 'Pivot' in result.columns

    def test_pivot_consistency(self):
        result1 = self.pivot.calculate(self.sample_data)
        result2 = self.pivot.calculate(self.sample_data)
        pd.testing.assert_frame_equal(result1, result2) 