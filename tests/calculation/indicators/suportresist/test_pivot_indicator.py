# tests/calculation/indicators/suportresist/test_pivot_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.suportresist.pivot_ind import calculate_pivot_points, apply_rule_pivot

class TestPivotIndicator:
    def setup_method(self):
        self.pivot = calculate_pivot_points
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_pivot_calculation_basic(self):
        result = self.pivot(self.sample_data)
        assert isinstance(result, tuple)
        assert len(result) == 3
        pivot_point, resistance_1, support_1 = result
        assert isinstance(pivot_point, pd.Series)
        assert isinstance(resistance_1, pd.Series)
        assert isinstance(support_1, pd.Series)
        assert len(pivot_point) == len(self.sample_data)

    def test_pivot_with_custom_price_type(self):
        from src.calculation.indicators.base_indicator import PriceType
        result = self.pivot(self.sample_data, price_type=PriceType.OPEN)
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_pivot_empty_dataframe(self):
        empty_df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        result = self.pivot(empty_df)
        assert isinstance(result, tuple)
        assert len(result) == 3
        pivot_point, resistance_1, support_1 = result
        assert len(pivot_point) == 0

    def test_pivot_insufficient_data(self):
        small_df = self.sample_data.head(1)
        result = self.pivot(small_df)
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_pivot_with_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[5, 'High'] = np.nan
        result = self.pivot(data_with_nan)
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_pivot_performance(self):
        large_df = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 10000),
            'High': np.random.uniform(150, 250, 10000),
            'Low': np.random.uniform(50, 150, 10000),
            'Close': np.random.uniform(75, 175, 10000),
            'Volume': np.random.uniform(1000, 5000, 10000)
        })
        import time
        start_time = time.time()
        result = self.pivot(large_df)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, tuple)

    def test_pivot_apply_rule(self):
        result = apply_rule_pivot(self.sample_data, point=0.01)
        assert 'Pivot_PP' in result
        assert 'Pivot_R1' in result
        assert 'Pivot_S1' in result
        assert 'Pivot_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['Pivot_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 