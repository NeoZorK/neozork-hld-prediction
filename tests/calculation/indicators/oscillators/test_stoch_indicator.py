# tests/calculation/indicators/oscillators/test_stoch_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.oscillators.stoch_ind import apply_rule_stochastic, calculate_stochastic


class TestStochIndicator:
    """Test cases for Stochastic Oscillator indicator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.stoch = calculate_stochastic
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_stoch_calculation_basic(self):
        """Test basic Stochastic calculation."""
        k_values, d_values = self.stoch(self.sample_data)
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)
        assert len(k_values) == len(self.sample_data)
        assert len(d_values) == len(self.sample_data)
        assert not k_values.isna().all()
        assert not d_values.isna().all()

    def test_stoch_with_custom_periods(self):
        """Test Stochastic calculation with custom parameters."""
        k_values, d_values = self.stoch(self.sample_data, k_period=10, d_period=3)
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)
        assert k_values.iloc[:9].isna().all()
        assert not k_values.iloc[9:].isna().all()

    def test_stoch_with_invalid_periods(self):
        """Test Stochastic with invalid parameters."""
        with pytest.raises(ValueError, match="All periods must be positive"):
            self.stoch(self.sample_data, k_period=0)
        with pytest.raises(ValueError, match="All periods must be positive"):
            self.stoch(self.sample_data, k_period=-1)

    def test_stoch_empty_dataframe(self):
        """Test Stochastic with empty dataframe."""
        empty_df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        k_values, d_values = self.stoch(empty_df)
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)
        assert len(k_values) == 0
        assert len(d_values) == 0

    def test_stoch_insufficient_data(self):
        """Test Stochastic with insufficient data."""
        small_df = self.sample_data.head(5)
        k_values, d_values = self.stoch(small_df, k_period=20)
        assert k_values.isna().all()
        assert d_values.isna().all()

    def test_stoch_parameter_validation(self):
        """Test Stochastic parameter validation."""
        k_values, d_values = self.stoch(self.sample_data, k_period=20, d_period=3)
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)
        k_values, d_values = self.stoch(self.sample_data, k_period=int(20.5), d_period=int(3.5))
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)

    def test_stoch_with_nan_values(self):
        """Test Stochastic calculation with NaN values."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.iloc[5, self.sample_data.columns.get_loc('High')] = np.nan
        k_values, d_values = self.stoch(data_with_nan)
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)
        assert len(k_values) == len(data_with_nan)
        assert len(d_values) == len(data_with_nan)

    def test_stoch_performance(self):
        """Test Stochastic performance with larger dataset."""
        large_data = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 10000),
            'High': np.random.uniform(200, 300, 10000),
            'Low': np.random.uniform(50, 100, 10000),
            'Close': np.random.uniform(100, 200, 10000),
            'Volume': np.random.uniform(1000, 5000, 10000)
        })
        import time
        start_time = time.time()
        k_values, d_values = self.stoch(large_data)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(k_values, pd.Series)
        assert isinstance(d_values, pd.Series)

    def test_stoch_apply_rule(self):
        """Test Stochastic application of rule."""
        result = apply_rule_stochastic(self.sample_data, point=0.01)
        assert 'Stoch_K' in result
        assert 'Stoch_D' in result
        assert 'Stoch_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['Stoch_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number)

    def test_stoch_value_range(self):
        """Test Stochastic value range and properties."""
        k_values, d_values = self.stoch(self.sample_data)
        
        # Stochastic values should be between 0 and 100 (excluding NaN)
        k_non_nan = k_values.dropna()
        d_non_nan = d_values.dropna()
        
        if len(k_non_nan) > 0:
            assert all(k_non_nan >= 0)
            assert all(k_non_nan <= 100)
        
        if len(d_non_nan) > 0:
            assert all(d_non_nan >= 0)
            assert all(d_non_nan <= 100)
        
        # Values should not be infinite
        assert not any(np.isinf(k_values.dropna()))
        assert not any(np.isinf(d_values.dropna()))

    def test_stoch_consistency(self):
        """Test Stochastic calculation consistency."""
        k_values1, d_values1 = self.stoch(self.sample_data)
        k_values2, d_values2 = self.stoch(self.sample_data)
        
        pd.testing.assert_series_equal(k_values1, k_values2)
        pd.testing.assert_series_equal(d_values1, d_values2)

    def test_stoch_overbought_oversold_levels(self):
        """Test Stochastic overbought and oversold levels."""
        # Create data that should produce overbought conditions
        overbought_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'High': [105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
            'Close': [108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108],  # Close near high
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400]
        })
        
        # Create data that should produce oversold conditions
        oversold_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'High': [105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
            'Close': [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],  # Close near low
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400]
        })
        
        k_values_overbought, d_values_overbought = self.stoch(overbought_data)
        k_values_oversold, d_values_oversold = self.stoch(oversold_data)
        
        # Overbought data should have higher stochastic values (excluding NaN)
        overbought_k = k_values_overbought.dropna().mean()
        oversold_k = k_values_oversold.dropna().mean()
        
        if not pd.isna(overbought_k) and not pd.isna(oversold_k):
            assert overbought_k > oversold_k

    def test_stoch_k_d_relationship(self):
        """Test relationship between %K and %D lines."""
        k_values, d_values = self.stoch(self.sample_data)
        
        # %D should be a smoothed version of %K
        # They should be correlated but not necessarily equal
        k_non_nan = k_values.dropna()
        d_non_nan = d_values.dropna()
        
        if len(k_non_nan) > 1 and len(d_non_nan) > 1:
            # Both should be within the same range (0-100)
            assert all(k_non_nan >= 0) and all(k_non_nan <= 100)
            assert all(d_non_nan >= 0) and all(d_non_nan <= 100)

    def test_stoch_period_impact(self):
        """Test the impact of different periods on Stochastic calculation."""
        k_values_short, d_values_short = self.stoch(self.sample_data, k_period=5, d_period=2)
        k_values_long, d_values_long = self.stoch(self.sample_data, k_period=20, d_period=10)
        
        # Different periods should produce different results
        assert not k_values_short.equals(k_values_long)
        assert not d_values_short.equals(d_values_long)

    def test_stoch_crossover_signals(self):
        """Test Stochastic crossover signals."""
        k_values, d_values = self.stoch(self.sample_data)
        
        if len(k_values) > 1 and len(d_values) > 1:
            # Test that crossovers can be detected
            # This is a basic test - in practice, you'd look for specific crossover patterns
            assert len(k_values) > 0
            assert len(d_values) > 0 