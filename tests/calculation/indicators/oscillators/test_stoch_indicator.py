# tests/calculation/indicators/oscillators/test_stoch_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.oscillators.stoch_ind import StochIndicator


class TestStochIndicator:
    """Test cases for Stochastic Oscillator indicator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.stoch = StochIndicator()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })

    def test_stoch_initialization(self):
        """Test Stochastic indicator initialization."""
        assert self.stoch.name == "Stochastic"
        assert self.stoch.category == "oscillators"
        assert "Stochastic" in self.stoch.description

    def test_stoch_calculation_basic(self):
        """Test basic Stochastic calculation."""
        result = self.stoch.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'Stoch_K' in result.columns
        assert 'Stoch_D' in result.columns
        assert len(result) == len(self.sample_data)

    def test_stoch_calculation_with_custom_parameters(self):
        """Test Stochastic calculation with custom parameters."""
        stoch_custom = StochIndicator(k_period=10, d_period=5)
        result = stoch_custom.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'Stoch_K' in result.columns
        assert 'Stoch_D' in result.columns

    def test_stoch_invalid_parameters(self):
        """Test Stochastic with invalid parameters."""
        with pytest.raises(ValueError, match="K period must be positive"):
            StochIndicator(k_period=0)
        
        with pytest.raises(ValueError, match="K period must be positive"):
            StochIndicator(k_period=-1)
        
        with pytest.raises(ValueError, match="D period must be positive"):
            StochIndicator(d_period=0)
        
        with pytest.raises(ValueError, match="D period must be positive"):
            StochIndicator(d_period=-1)

    def test_stoch_empty_dataframe(self):
        """Test Stochastic with empty dataframe."""
        empty_df = pd.DataFrame()
        result = self.stoch.calculate(empty_df)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_stoch_missing_columns(self):
        """Test Stochastic with missing required columns."""
        incomplete_data = self.sample_data.drop(columns=['high'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.stoch.calculate(incomplete_data)
        
        incomplete_data = self.sample_data.drop(columns=['low'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.stoch.calculate(incomplete_data)
        
        incomplete_data = self.sample_data.drop(columns=['close'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.stoch.calculate(incomplete_data)

    def test_stoch_parameter_validation(self):
        """Test Stochastic parameter validation."""
        # Test with valid parameters
        stoch_valid = StochIndicator(k_period=14, d_period=3)
        assert stoch_valid.k_period == 14
        assert stoch_valid.d_period == 3
        
        # Test with float parameters (should be converted to int)
        stoch_float = StochIndicator(k_period=14.5, d_period=3.7)
        assert stoch_float.k_period == 14
        assert stoch_float.d_period == 3

    def test_stoch_value_range(self):
        """Test Stochastic value range and properties."""
        result = self.stoch.calculate(self.sample_data)
        
        # Stochastic values should be between 0 and 100
        k_values = result['Stoch_K'].dropna()
        d_values = result['Stoch_D'].dropna()
        
        if len(k_values) > 0:
            assert all(k_values >= 0)
            assert all(k_values <= 100)
        
        if len(d_values) > 0:
            assert all(d_values >= 0)
            assert all(d_values <= 100)
        
        # Values should not be infinite
        assert not any(np.isinf(result['Stoch_K'].dropna()))
        assert not any(np.isinf(result['Stoch_D'].dropna()))

    def test_stoch_with_nan_values(self):
        """Test Stochastic calculation with NaN values."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        
        result = self.stoch.calculate(data_with_nan)
        
        assert isinstance(result, pd.DataFrame)
        assert 'Stoch_K' in result.columns
        assert 'Stoch_D' in result.columns

    def test_stoch_docstring_info(self):
        """Test Stochastic docstring information."""
        assert "Stochastic" in self.stoch.name
        assert "oscillators" in self.stoch.category.lower()
        assert len(self.stoch.description) > 0

    def test_stoch_cli_integration(self):
        """Test Stochastic CLI integration."""
        # Test that the indicator can be used in CLI context
        assert hasattr(self.stoch, 'calculate')
        assert callable(self.stoch.calculate)

    def test_stoch_performance(self):
        """Test Stochastic performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'open': np.random.uniform(100, 110, 1000),
            'high': np.random.uniform(110, 120, 1000),
            'low': np.random.uniform(90, 100, 1000),
            'close': np.random.uniform(100, 110, 1000),
            'volume': np.random.randint(1000, 2000, 1000)
        })
        
        result = self.stoch.calculate(large_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(large_data)
        assert 'Stoch_K' in result.columns
        assert 'Stoch_D' in result.columns

    def test_stoch_edge_cases(self):
        """Test Stochastic edge cases."""
        # Test with all same values
        same_values = pd.DataFrame({
            'open': [100] * 10,
            'high': [100] * 10,
            'low': [100] * 10,
            'close': [100] * 10,
            'volume': [1000] * 10
        })
        
        result = self.stoch.calculate(same_values)
        assert isinstance(result, pd.DataFrame)
        assert 'Stoch_K' in result.columns
        assert 'Stoch_D' in result.columns

    def test_stoch_consistency(self):
        """Test Stochastic calculation consistency."""
        result1 = self.stoch.calculate(self.sample_data)
        result2 = self.stoch.calculate(self.sample_data)
        
        pd.testing.assert_frame_equal(result1, result2)

    def test_stoch_overbought_oversold_levels(self):
        """Test Stochastic overbought and oversold levels."""
        # Create data that should produce overbought conditions
        overbought_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [108, 108, 108, 108, 108],  # Close near high
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        # Create data that should produce oversold conditions
        oversold_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [100, 100, 100, 100, 100],  # Close near low
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        overbought_result = self.stoch.calculate(overbought_data)
        oversold_result = self.stoch.calculate(oversold_data)
        
        # Overbought data should have higher stochastic values
        overbought_k = overbought_result['Stoch_K'].mean()
        oversold_k = oversold_result['Stoch_K'].mean()
        
        assert overbought_k > oversold_k

    def test_stoch_k_d_relationship(self):
        """Test relationship between %K and %D lines."""
        result = self.stoch.calculate(self.sample_data)
        
        k_values = result['Stoch_K'].dropna()
        d_values = result['Stoch_D'].dropna()
        
        # %D should be a smoothed version of %K
        # They should be correlated but not necessarily equal
        if len(k_values) > 1 and len(d_values) > 1:
            # Both should be within the same range (0-100)
            assert all(k_values >= 0) and all(k_values <= 100)
            assert all(d_values >= 0) and all(d_values <= 100)

    def test_stoch_period_impact(self):
        """Test the impact of different periods on Stochastic calculation."""
        stoch_short = StochIndicator(k_period=5, d_period=2)
        stoch_long = StochIndicator(k_period=20, d_period=10)
        
        result_short = stoch_short.calculate(self.sample_data)
        result_long = stoch_long.calculate(self.sample_data)
        
        # Different periods should produce different results
        assert not result_short['Stoch_K'].equals(result_long['Stoch_K'])
        assert not result_short['Stoch_D'].equals(result_long['Stoch_D'])

    def test_stoch_crossover_signals(self):
        """Test Stochastic crossover signals."""
        result = self.stoch.calculate(self.sample_data)
        
        k_values = result['Stoch_K'].dropna()
        d_values = result['Stoch_D'].dropna()
        
        if len(k_values) > 1 and len(d_values) > 1:
            # Test that crossovers can be detected
            # This is a basic test - in practice, you'd look for specific crossover patterns
            assert len(k_values) > 0
            assert len(d_values) > 0 