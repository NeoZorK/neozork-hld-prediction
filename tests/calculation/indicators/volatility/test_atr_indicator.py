# tests/calculation/indicators/volatility/test_atr_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.volatility.atr_ind import ATRIndicator


class TestATRIndicator:
    """Test cases for ATR (Average True Range) indicator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.atr = ATRIndicator()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })

    def test_atr_initialization(self):
        """Test ATR indicator initialization."""
        assert self.atr.name == "ATR"
        assert self.atr.category == "volatility"
        assert self.atr.description == "Average True Range - measures market volatility"

    def test_atr_calculation_basic(self):
        """Test basic ATR calculation."""
        result = self.atr.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'ATR' in result.columns
        assert len(result) == len(self.sample_data)
        
        # ATR values should be positive
        assert all(result['ATR'].dropna() >= 0)

    def test_atr_calculation_with_custom_period(self):
        """Test ATR calculation with custom period."""
        atr_custom = ATRIndicator(period=10)
        result = atr_custom.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'ATR' in result.columns

    def test_atr_invalid_period(self):
        """Test ATR with invalid period."""
        with pytest.raises(ValueError, match="Period must be positive"):
            ATRIndicator(period=0)
        
        with pytest.raises(ValueError, match="Period must be positive"):
            ATRIndicator(period=-1)

    def test_atr_empty_dataframe(self):
        """Test ATR with empty dataframe."""
        empty_df = pd.DataFrame()
        result = self.atr.calculate(empty_df)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_atr_missing_columns(self):
        """Test ATR with missing required columns."""
        incomplete_data = self.sample_data.drop(columns=['high'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.atr.calculate(incomplete_data)

    def test_atr_parameter_validation(self):
        """Test ATR parameter validation."""
        # Test with valid parameters
        atr_valid = ATRIndicator(period=14)
        assert atr_valid.period == 14
        
        # Test with float period (should be converted to int)
        atr_float = ATRIndicator(period=14.5)
        assert atr_float.period == 14

    def test_atr_value_range(self):
        """Test ATR value range and properties."""
        result = self.atr.calculate(self.sample_data)
        
        # ATR should be non-negative
        assert all(result['ATR'].dropna() >= 0)
        
        # ATR should not be infinite
        assert not any(np.isinf(result['ATR'].dropna()))

    def test_atr_with_nan_values(self):
        """Test ATR calculation with NaN values."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'high'] = np.nan
        
        result = self.atr.calculate(data_with_nan)
        
        assert isinstance(result, pd.DataFrame)
        assert 'ATR' in result.columns

    def test_atr_docstring_info(self):
        """Test ATR docstring information."""
        assert "ATR" in self.atr.name
        assert "volatility" in self.atr.category.lower()
        assert len(self.atr.description) > 0

    def test_atr_cli_integration(self):
        """Test ATR CLI integration."""
        # Test that the indicator can be used in CLI context
        assert hasattr(self.atr, 'calculate')
        assert callable(self.atr.calculate)

    def test_atr_performance(self):
        """Test ATR performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'open': np.random.uniform(100, 110, 1000),
            'high': np.random.uniform(110, 120, 1000),
            'low': np.random.uniform(90, 100, 1000),
            'close': np.random.uniform(100, 110, 1000),
            'volume': np.random.randint(1000, 2000, 1000)
        })
        
        result = self.atr.calculate(large_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(large_data)
        assert 'ATR' in result.columns

    def test_atr_edge_cases(self):
        """Test ATR edge cases."""
        # Test with all same values
        same_values = pd.DataFrame({
            'open': [100] * 10,
            'high': [100] * 10,
            'low': [100] * 10,
            'close': [100] * 10,
            'volume': [1000] * 10
        })
        
        result = self.atr.calculate(same_values)
        assert isinstance(result, pd.DataFrame)
        assert 'ATR' in result.columns

    def test_atr_consistency(self):
        """Test ATR calculation consistency."""
        result1 = self.atr.calculate(self.sample_data)
        result2 = self.atr.calculate(self.sample_data)
        
        pd.testing.assert_frame_equal(result1, result2)

    def test_atr_volatility_measurement(self):
        """Test that ATR properly measures volatility."""
        # Create data with different volatility levels
        low_vol_data = pd.DataFrame({
            'open': [100, 100.1, 100.2, 100.1, 100.3],
            'high': [100.2, 100.3, 100.4, 100.3, 100.5],
            'low': [99.9, 100.0, 100.1, 100.0, 100.2],
            'close': [100.1, 100.2, 100.3, 100.2, 100.4],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        high_vol_data = pd.DataFrame({
            'open': [100, 105, 95, 110, 90],
            'high': [110, 115, 105, 120, 100],
            'low': [90, 95, 85, 100, 80],
            'close': [105, 95, 110, 90, 105],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        low_vol_result = self.atr.calculate(low_vol_data)
        high_vol_result = self.atr.calculate(high_vol_data)
        
        # High volatility data should have higher ATR values
        low_vol_atr = low_vol_result['ATR'].mean()
        high_vol_atr = high_vol_result['ATR'].mean()
        
        assert high_vol_atr > low_vol_atr 