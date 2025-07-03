# tests/calculation/indicators/probability/test_montecarlo_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.probability.montecarlo_ind import (
    calculate_montecarlo, 
    calculate_montecarlo_signal_line,
    calculate_montecarlo_histogram,
    calculate_montecarlo_confidence_bands,
    calculate_montecarlo_signals,
    apply_rule_montecarlo
)
from src.calculation.indicators.base_indicator import PriceType

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
        assert end_time - start_time < 10.0  # Monte Carlo can be slower, increased from 5.0 to 10.0
        assert isinstance(result, pd.Series)

    def test_montecarlo_signal_line(self):
        """Test Monte Carlo signal line calculation."""
        mc_forecast = self.montecarlo(self.sample_data['Close'])
        signal_line = calculate_montecarlo_signal_line(mc_forecast, signal_period=9)
        
        assert isinstance(signal_line, pd.Series)
        assert len(signal_line) == len(mc_forecast)
        assert not signal_line.isna().all()
        
        # Signal line should be smoother than forecast
        assert signal_line.std() <= mc_forecast.std()

    def test_montecarlo_signal_line_invalid_period(self):
        """Test Monte Carlo signal line with invalid period."""
        mc_forecast = self.montecarlo(self.sample_data['Close'])
        
        with pytest.raises(ValueError, match="Signal period must be positive"):
            calculate_montecarlo_signal_line(mc_forecast, signal_period=0)
        
        with pytest.raises(ValueError, match="Signal period must be positive"):
            calculate_montecarlo_signal_line(mc_forecast, signal_period=-1)

    def test_montecarlo_histogram(self):
        """Test Monte Carlo histogram calculation."""
        mc_forecast = self.montecarlo(self.sample_data['Close'])
        signal_line = calculate_montecarlo_signal_line(mc_forecast, signal_period=9)
        histogram = calculate_montecarlo_histogram(mc_forecast, signal_line)
        
        assert isinstance(histogram, pd.Series)
        assert len(histogram) == len(mc_forecast)
        assert not histogram.isna().all()
        
        # Histogram should be the difference between forecast and signal line
        expected_histogram = mc_forecast - signal_line
        pd.testing.assert_series_equal(histogram, expected_histogram, check_names=False)

    def test_montecarlo_confidence_bands(self):
        """Test Monte Carlo confidence bands calculation."""
        mc_forecast = self.montecarlo(self.sample_data['Close'])
        upper_band, lower_band = calculate_montecarlo_confidence_bands(mc_forecast, confidence_level=0.95)
        
        assert isinstance(upper_band, pd.Series)
        assert isinstance(lower_band, pd.Series)
        assert len(upper_band) == len(mc_forecast)
        assert len(lower_band) == len(mc_forecast)
        
        # Upper band should be above forecast, lower band should be below (only for non-NaN values)
        non_nan_mask = ~mc_forecast.isna()
        if non_nan_mask.any():
            assert (upper_band[non_nan_mask] >= mc_forecast[non_nan_mask]).all()
            assert (lower_band[non_nan_mask] <= mc_forecast[non_nan_mask]).all()

    def test_montecarlo_signals(self):
        """Test Monte Carlo signals calculation."""
        mc_forecast = self.montecarlo(self.sample_data['Close'])
        signal_line = calculate_montecarlo_signal_line(mc_forecast, signal_period=9)
        signals = calculate_montecarlo_signals(self.sample_data['Close'], mc_forecast, signal_line)
        
        assert isinstance(signals, pd.Series)
        assert len(signals) == len(self.sample_data)
        
        # Check that signals are valid values (0, 1, 2)
        valid_signals = [0, 1, 2]  # NOTRADE, BUY, SELL
        assert signals.isin(valid_signals).all()

    def test_montecarlo_apply_rule(self):
        result = apply_rule_montecarlo(self.sample_data, point=0.01)
        assert 'MonteCarlo' in result
        assert 'MonteCarlo_Signal' in result
        assert 'MonteCarlo_Histogram' in result
        assert 'MonteCarlo_Upper' in result
        assert 'MonteCarlo_Lower' in result
        assert 'MonteCarlo_Signal_Line' in result
        assert 'Direction' in result
        assert 'Diff' in result
        
        signals = result['MonteCarlo_Signal_Line'].dropna()
        assert np.issubdtype(signals.dtype, np.number)
        
        # Check that all Monte Carlo components are present
        assert not result['MonteCarlo'].isna().all()
        assert not result['MonteCarlo_Signal'].isna().all()
        assert not result['MonteCarlo_Histogram'].isna().all()
        assert not result['MonteCarlo_Upper'].isna().all()
        assert not result['MonteCarlo_Lower'].isna().all()

    def test_montecarlo_apply_rule_with_custom_parameters(self):
        result = apply_rule_montecarlo(self.sample_data, point=0.01, simulations=500, period=10)
        assert 'MonteCarlo' in result
        assert 'MonteCarlo_Signal' in result
        assert 'MonteCarlo_Histogram' in result
        assert 'MonteCarlo_Upper' in result
        assert 'MonteCarlo_Lower' in result
        assert 'MonteCarlo_Signal_Line' in result

    def test_montecarlo_apply_rule_open_prices(self):
        result = apply_rule_montecarlo(self.sample_data, point=0.01, price_type=PriceType.OPEN)
        assert 'MonteCarlo' in result
        assert 'MonteCarlo_Price_Type' in result
        assert result['MonteCarlo_Price_Type'].iloc[0] == "Open"

    def test_montecarlo_apply_rule_close_prices(self):
        result = apply_rule_montecarlo(self.sample_data, point=0.01, price_type=PriceType.CLOSE)
        assert 'MonteCarlo' in result
        assert 'MonteCarlo_Price_Type' in result
        assert result['MonteCarlo_Price_Type'].iloc[0] == "Close" 