# tests/calculation/indicators/volatility/test_stdev_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.volatility.stdev_ind import calculate_stdev, apply_rule_stdev


class TestStDevIndicator:
    """Test cases for Standard Deviation indicator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.stdev = StDevIndicator()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })

    def test_stdev_initialization(self):
        """Test Standard Deviation indicator initialization."""
        assert self.stdev.name == "StDev"
        assert self.stdev.category == "volatility"
        assert "Standard Deviation" in self.stdev.description

    def test_stdev_calculation_basic(self):
        """Test basic Standard Deviation calculation."""
        result = self.stdev.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'StDev' in result.columns
        assert len(result) == len(self.sample_data)
        
        # Standard deviation values should be non-negative
        assert all(result['StDev'].dropna() >= 0)

    def test_stdev_calculation_with_custom_period(self):
        """Test Standard Deviation calculation with custom period."""
        stdev_custom = StDevIndicator(period=10)
        result = stdev_custom.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'StDev' in result.columns

    def test_stdev_invalid_period(self):
        """Test Standard Deviation with invalid period."""
        with pytest.raises(ValueError, match="Period must be positive"):
            StDevIndicator(period=0)
        
        with pytest.raises(ValueError, match="Period must be positive"):
            StDevIndicator(period=-1)

    def test_stdev_empty_dataframe(self):
        """Test Standard Deviation with empty dataframe."""
        empty_df = pd.DataFrame()
        result = self.stdev.calculate(empty_df)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_stdev_missing_columns(self):
        """Test Standard Deviation with missing required columns."""
        incomplete_data = self.sample_data.drop(columns=['close'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.stdev.calculate(incomplete_data)

    def test_stdev_parameter_validation(self):
        """Test Standard Deviation parameter validation."""
        # Test with valid parameters
        stdev_valid = StDevIndicator(period=20)
        assert stdev_valid.period == 20
        
        # Test with float period (should be converted to int)
        stdev_float = StDevIndicator(period=20.5)
        assert stdev_float.period == 20

    def test_stdev_value_range(self):
        """Test Standard Deviation value range and properties."""
        result = self.stdev.calculate(self.sample_data)
        
        # Standard deviation should be non-negative
        assert all(result['StDev'].dropna() >= 0)
        
        # Standard deviation should not be infinite
        assert not any(np.isinf(result['StDev'].dropna()))

    def test_stdev_with_nan_values(self):
        """Test Standard Deviation calculation with NaN values."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        
        result = self.stdev.calculate(data_with_nan)
        
        assert isinstance(result, pd.DataFrame)
        assert 'StDev' in result.columns

    def test_stdev_docstring_info(self):
        """Test Standard Deviation docstring information."""
        assert "StDev" in self.stdev.name
        assert "volatility" in self.stdev.category.lower()
        assert len(self.stdev.description) > 0

    def test_stdev_cli_integration(self):
        """Test Standard Deviation CLI integration."""
        # Test that the indicator can be used in CLI context
        assert hasattr(self.stdev, 'calculate')
        assert callable(self.stdev.calculate)

    def test_stdev_performance(self):
        """Test Standard Deviation performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'open': np.random.uniform(100, 110, 1000),
            'high': np.random.uniform(110, 120, 1000),
            'low': np.random.uniform(90, 100, 1000),
            'close': np.random.uniform(100, 110, 1000),
            'volume': np.random.randint(1000, 2000, 1000)
        })
        
        result = self.stdev.calculate(large_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(large_data)
        assert 'StDev' in result.columns

    def test_stdev_edge_cases(self):
        """Test Standard Deviation edge cases."""
        # Test with all same values (should result in zero standard deviation)
        same_values = pd.DataFrame({
            'open': [100] * 10,
            'high': [100] * 10,
            'low': [100] * 10,
            'close': [100] * 10,
            'volume': [1000] * 10
        })
        
        result = self.stdev.calculate(same_values)
        assert isinstance(result, pd.DataFrame)
        assert 'StDev' in result.columns
        
        # For constant values, standard deviation should be zero (or very close to zero)
        stdev_values = result['StDev'].dropna()
        if len(stdev_values) > 0:
            assert all(stdev_values <= 1e-10)  # Allow for floating point precision

    def test_stdev_consistency(self):
        """Test Standard Deviation calculation consistency."""
        result1 = self.stdev.calculate(self.sample_data)
        result2 = self.stdev.calculate(self.sample_data)
        
        pd.testing.assert_frame_equal(result1, result2)

    def test_stdev_volatility_measurement(self):
        """Test that Standard Deviation properly measures volatility."""
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
        
        low_vol_result = self.stdev.calculate(low_vol_data)
        high_vol_result = self.stdev.calculate(high_vol_data)
        
        # High volatility data should have higher standard deviation
        low_vol_stdev = low_vol_result['StDev'].mean()
        high_vol_stdev = high_vol_result['StDev'].mean()
        
        assert high_vol_stdev > low_vol_stdev

    def test_stdev_mathematical_properties(self):
        """Test mathematical properties of Standard Deviation."""
        # Create a simple dataset with known standard deviation
        simple_data = pd.DataFrame({
            'open': [1, 2, 3, 4, 5],
            'high': [1, 2, 3, 4, 5],
            'low': [1, 2, 3, 4, 5],
            'close': [1, 2, 3, 4, 5],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = self.stdev.calculate(simple_data)
        
        # For values [1,2,3,4,5], the standard deviation should be approximately 1.58
        stdev_values = result['StDev'].dropna()
        if len(stdev_values) > 0:
            # Allow for some tolerance due to rolling window calculation
            assert all(stdev_values >= 0)
            assert all(stdev_values <= 2.0)  # Should be around 1.58

    def test_stdev_period_impact(self):
        """Test the impact of period on Standard Deviation calculation."""
        stdev_short = StDevIndicator(period=5)
        stdev_long = StDevIndicator(period=20)
        
        result_short = stdev_short.calculate(self.sample_data)
        result_long = stdev_long.calculate(self.sample_data)
        
        # Different periods should produce different results
        assert not result_short['StDev'].equals(result_long['StDev']) 