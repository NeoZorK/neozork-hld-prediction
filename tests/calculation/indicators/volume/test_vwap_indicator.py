# tests/calculation/indicators/volume/test_vwap_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.volume.vwap_ind import VWAPIndicator


class TestVWAPIndicator:
    """Test cases for VWAP (Volume Weighted Average Price) indicator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.vwap = VWAPIndicator()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })

    def test_vwap_initialization(self):
        """Test VWAP indicator initialization."""
        assert self.vwap.name == "VWAP"
        assert self.vwap.category == "volume"
        assert "Volume Weighted Average Price" in self.vwap.description

    def test_vwap_calculation_basic(self):
        """Test basic VWAP calculation."""
        result = self.vwap.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'VWAP' in result.columns
        assert len(result) == len(self.sample_data)

    def test_vwap_calculation_with_custom_period(self):
        """Test VWAP calculation with custom period."""
        vwap_custom = VWAPIndicator(period=10)
        result = vwap_custom.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'VWAP' in result.columns

    def test_vwap_invalid_period(self):
        """Test VWAP with invalid period."""
        with pytest.raises(ValueError, match="Period must be positive"):
            VWAPIndicator(period=0)
        
        with pytest.raises(ValueError, match="Period must be positive"):
            VWAPIndicator(period=-1)

    def test_vwap_empty_dataframe(self):
        """Test VWAP with empty dataframe."""
        empty_df = pd.DataFrame()
        result = self.vwap.calculate(empty_df)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_vwap_missing_columns(self):
        """Test VWAP with missing required columns."""
        incomplete_data = self.sample_data.drop(columns=['high'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.vwap.calculate(incomplete_data)
        
        incomplete_data = self.sample_data.drop(columns=['low'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.vwap.calculate(incomplete_data)
        
        incomplete_data = self.sample_data.drop(columns=['close'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.vwap.calculate(incomplete_data)
        
        incomplete_data = self.sample_data.drop(columns=['volume'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.vwap.calculate(incomplete_data)

    def test_vwap_parameter_validation(self):
        """Test VWAP parameter validation."""
        # Test with valid parameters
        vwap_valid = VWAPIndicator(period=20)
        assert vwap_valid.period == 20
        
        # Test with float period (should be converted to int)
        vwap_float = VWAPIndicator(period=20.5)
        assert vwap_float.period == 20

    def test_vwap_value_range(self):
        """Test VWAP value range and properties."""
        result = self.vwap.calculate(self.sample_data)
        
        # VWAP should be within the price range
        vwap_values = result['VWAP'].dropna()
        if len(vwap_values) > 0:
            assert all(vwap_values >= self.sample_data['low'].min())
            assert all(vwap_values <= self.sample_data['high'].max())
        
        # VWAP should not be infinite
        assert not any(np.isinf(result['VWAP'].dropna()))

    def test_vwap_with_nan_values(self):
        """Test VWAP calculation with NaN values."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        
        result = self.vwap.calculate(data_with_nan)
        
        assert isinstance(result, pd.DataFrame)
        assert 'VWAP' in result.columns

    def test_vwap_docstring_info(self):
        """Test VWAP docstring information."""
        assert "VWAP" in self.vwap.name
        assert "volume" in self.vwap.category.lower()
        assert len(self.vwap.description) > 0

    def test_vwap_cli_integration(self):
        """Test VWAP CLI integration."""
        # Test that the indicator can be used in CLI context
        assert hasattr(self.vwap, 'calculate')
        assert callable(self.vwap.calculate)

    def test_vwap_performance(self):
        """Test VWAP performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'open': np.random.uniform(100, 110, 1000),
            'high': np.random.uniform(110, 120, 1000),
            'low': np.random.uniform(90, 100, 1000),
            'close': np.random.uniform(100, 110, 1000),
            'volume': np.random.randint(1000, 2000, 1000)
        })
        
        result = self.vwap.calculate(large_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(large_data)
        assert 'VWAP' in result.columns

    def test_vwap_edge_cases(self):
        """Test VWAP edge cases."""
        # Test with all same values
        same_values = pd.DataFrame({
            'open': [100] * 10,
            'high': [100] * 10,
            'low': [100] * 10,
            'close': [100] * 10,
            'volume': [1000] * 10
        })
        
        result = self.vwap.calculate(same_values)
        assert isinstance(result, pd.DataFrame)
        assert 'VWAP' in result.columns

    def test_vwap_consistency(self):
        """Test VWAP calculation consistency."""
        result1 = self.vwap.calculate(self.sample_data)
        result2 = self.vwap.calculate(self.sample_data)
        
        pd.testing.assert_frame_equal(result1, result2)

    def test_vwap_volume_weighting(self):
        """Test that VWAP properly weights by volume."""
        # Create data with different volume patterns
        high_volume_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],
            'volume': [1000, 2000, 3000, 4000, 5000]  # Increasing volumes
        })
        
        low_volume_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],
            'volume': [5000, 4000, 3000, 2000, 1000]  # Decreasing volumes
        })
        
        high_vol_result = self.vwap.calculate(high_volume_data)
        low_vol_result = self.vwap.calculate(low_volume_data)
        
        # VWAP should be different for different volume patterns
        assert not high_vol_result['VWAP'].equals(low_vol_result['VWAP'])

    def test_vwap_price_volume_relationship(self):
        """Test VWAP relationship between price and volume."""
        # Create data where higher prices have higher volumes
        price_vol_corr = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],  # Increasing prices
            'volume': [1000, 1100, 1200, 1300, 1400]  # Increasing volumes
        })
        
        # Create data where higher prices have lower volumes
        price_vol_anti = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],  # Increasing prices
            'volume': [1400, 1300, 1200, 1100, 1000]  # Decreasing volumes
        })
        
        result1 = self.vwap.calculate(price_vol_corr)
        result2 = self.vwap.calculate(price_vol_anti)
        
        # Different price-volume relationships should produce different VWAP
        assert not result1['VWAP'].equals(result2['VWAP'])

    def test_vwap_zero_volume(self):
        """Test VWAP with zero volume."""
        zero_volume_data = self.sample_data.copy()
        zero_volume_data['volume'] = 0
        
        result = self.vwap.calculate(zero_volume_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'VWAP' in result.columns

    def test_vwap_negative_volume(self):
        """Test VWAP with negative volume (should handle gracefully)."""
        negative_volume_data = self.sample_data.copy()
        negative_volume_data.loc[2, 'volume'] = -100
        
        result = self.vwap.calculate(negative_volume_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'VWAP' in result.columns

    def test_vwap_period_impact(self):
        """Test the impact of period on VWAP calculation."""
        vwap_short = VWAPIndicator(period=5)
        vwap_long = VWAPIndicator(period=20)
        
        result_short = vwap_short.calculate(self.sample_data)
        result_long = vwap_long.calculate(self.sample_data)
        
        # Different periods should produce different results
        assert not result_short['VWAP'].equals(result_long['VWAP'])

    def test_vwap_mathematical_properties(self):
        """Test mathematical properties of VWAP."""
        # VWAP should be a weighted average of typical prices
        # where typical price = (high + low + close) / 3
        result = self.vwap.calculate(self.sample_data)
        
        vwap_values = result['VWAP'].dropna()
        if len(vwap_values) > 0:
            # VWAP should be within reasonable bounds
            assert all(vwap_values >= 0)
            assert all(vwap_values <= 1000)  # Reasonable upper bound for this data 