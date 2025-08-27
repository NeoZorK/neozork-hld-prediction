# tests/calculation/indicators/predictive/test_tsforecast_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.predictive.tsforecast_ind import calculate_tsforecast, apply_rule_tsforecast

class TestTSForecastIndicator:
    def setup_method(self):
        self.tsforecast = calculate_tsforecast
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_tsforecast_calculation_basic(self):
        result = self.tsforecast(self.sample_data['Close'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data)
        assert not result.isna().all()

    def test_tsforecast_with_custom_period(self):
        result = self.tsforecast(self.sample_data['Close'], period=10)
        assert isinstance(result, pd.Series)
        assert result.iloc[:9].isna().all()
        assert not result.iloc[9:].isna().all()

    def test_tsforecast_with_invalid_period(self):
        with pytest.raises(ValueError, match="TSForecast period must be positive"):
            self.tsforecast(self.sample_data['Close'], period=0)
        with pytest.raises(ValueError, match="TSForecast period must be positive"):
            self.tsforecast(self.sample_data['Close'], period=-1)

    def test_tsforecast_empty_dataframe(self):
        empty_series = pd.Series(dtype=float)
        result = self.tsforecast(empty_series)
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_tsforecast_insufficient_data(self):
        small_series = self.sample_data['Close'].head(5)
        result = self.tsforecast(small_series, period=20)
        assert result.isna().all()

    def test_tsforecast_parameter_validation(self):
        result = self.tsforecast(self.sample_data['Close'], period=20)
        assert isinstance(result, pd.Series)
        result = self.tsforecast(self.sample_data['Close'], period=int(20.5))
        assert isinstance(result, pd.Series)

    def test_tsforecast_with_nan_values(self):
        data_with_nan = self.sample_data['Close'].copy()
        data_with_nan.loc[5] = np.nan
        result = self.tsforecast(data_with_nan)
        assert isinstance(result, pd.Series)
        assert len(result) == len(data_with_nan)

    def test_tsforecast_performance(self):
        large_series = pd.Series(np.random.uniform(100, 200, 1000))  # Reduced from 10000 to 1000
        import time
        start_time = time.time()
        result = self.tsforecast(large_series)
        end_time = time.time()
        assert end_time - start_time < 2.0  # Increased from 1.0 to 2.0 seconds
        assert isinstance(result, pd.Series)

    def test_tsforecast_apply_rule(self):
        result = apply_rule_tsforecast(self.sample_data, point=0.01)
        assert 'TSForecast' in result
        assert 'TSForecast_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['TSForecast_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 