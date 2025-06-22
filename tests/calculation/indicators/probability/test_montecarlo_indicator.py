# tests/calculation/indicators/probability/test_montecarlo_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.probability.montecarlo_ind import calculate_montecarlo, apply_rule_montecarlo

class TestMonteCarloIndicator:
    def setup_method(self):
        self.montecarlo = calculate_montecarlo
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_montecarlo_calculation_basic(self):
        result = self.montecarlo(self.sample_data['Close'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data)
        assert not result.isna().all()

    def test_montecarlo_with_custom_parameters(self):
        result = self.montecarlo(self.sample_data['Close'], simulations=500, period=10)
        assert isinstance(result, pd.Series)
        assert result.iloc[:9].isna().all()
        assert not result.iloc[9:].isna().all()

    def test_montecarlo_with_invalid_parameters(self):
        """Test Monte Carlo calculation with invalid parameters."""
        with pytest.raises(ValueError, match="Simulations and period must be positive"):
            self.montecarlo(self.sample_data['Close'], period=0)
        
        with pytest.raises(ValueError, match="Simulations and period must be positive"):
            self.montecarlo(self.sample_data['Close'], period=-1)
        
        with pytest.raises(ValueError, match="Simulations and period must be positive"):
            self.montecarlo(self.sample_data['Close'], simulations=0)

    def test_montecarlo_empty_dataframe(self):
        empty_series = pd.Series(dtype=float)
        result = self.montecarlo(empty_series)
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_montecarlo_insufficient_data(self):
        small_series = self.sample_data['Close'].head(5)
        result = self.montecarlo(small_series, period=20)
        assert result.isna().all()

    def test_montecarlo_parameter_validation(self):
        result = self.montecarlo(self.sample_data['Close'], period=20, simulations=1000)
        assert isinstance(result, pd.Series)
        result = self.montecarlo(self.sample_data['Close'], period=int(20.5), simulations=int(1000.5))
        assert isinstance(result, pd.Series)

    def test_montecarlo_with_nan_values(self):
        data_with_nan = self.sample_data['Close'].copy()
        data_with_nan.loc[5] = np.nan
        result = self.montecarlo(data_with_nan)
        assert isinstance(result, pd.Series)
        assert len(result) == len(data_with_nan)

    def test_montecarlo_performance(self):
        large_series = pd.Series(np.random.uniform(100, 200, 10000))
        import time
        start_time = time.time()
        result = self.montecarlo(large_series, simulations=100)
        end_time = time.time()
        assert end_time - start_time < 5.0  # Monte Carlo can be slower
        assert isinstance(result, pd.Series)

    def test_montecarlo_apply_rule(self):
        result = apply_rule_montecarlo(self.sample_data, point=0.01)
        assert 'MonteCarlo' in result
        assert 'MonteCarlo_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['MonteCarlo_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 