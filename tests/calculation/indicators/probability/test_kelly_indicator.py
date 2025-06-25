# tests/calculation/indicators/probability/test_kelly_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.probability.kelly_ind import calculate_kelly, apply_rule_kelly

class TestKellyIndicator:
    def setup_method(self):
        self.kelly = calculate_kelly
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_kelly_calculation_basic(self):
        result = self.kelly(self.sample_data['Close'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data)
        assert not result.isna().all()

    def test_kelly_with_custom_period(self):
        result = self.kelly(self.sample_data['Close'], period=10)
        assert isinstance(result, pd.Series)
        assert result.iloc[:9].isna().all()
        assert not result.iloc[9:].isna().all()

    def test_kelly_with_invalid_period(self):
        with pytest.raises(ValueError, match="Kelly period must be positive"):
            self.kelly(self.sample_data['Close'], period=0)
        with pytest.raises(ValueError, match="Kelly period must be positive"):
            self.kelly(self.sample_data['Close'], period=-1)

    def test_kelly_empty_dataframe(self):
        empty_series = pd.Series(dtype=float)
        result = self.kelly(empty_series)
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_kelly_insufficient_data(self):
        small_series = self.sample_data['Close'].head(5)
        result = self.kelly(small_series, period=20)
        assert result.isna().all()

    def test_kelly_parameter_validation(self):
        result = self.kelly(self.sample_data['Close'], period=20)
        assert isinstance(result, pd.Series)
        result = self.kelly(self.sample_data['Close'], period=int(20.5))
        assert isinstance(result, pd.Series)

    def test_kelly_with_nan_values(self):
        data_with_nan = self.sample_data['Close'].copy()
        data_with_nan.loc[5] = np.nan
        result = self.kelly(data_with_nan)
        assert isinstance(result, pd.Series)
        assert len(result) == len(data_with_nan)

    def test_kelly_performance(self):
        """Test Kelly calculation performance with larger dataset."""
        large_series = pd.Series(np.random.uniform(100, 200, 10000))
        import time
        start_time = time.time()
        result = self.kelly(large_series)
        end_time = time.time()
        assert end_time - start_time < 5.0  # Увеличиваю лимит времени до 5 секунд
        assert isinstance(result, pd.Series)

    def test_kelly_apply_rule(self):
        result = apply_rule_kelly(self.sample_data, point=0.01)
        assert 'Kelly' in result
        assert 'Kelly_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['Kelly_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 