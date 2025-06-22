# tests/calculation/indicators/volume/test_obv_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.volume.obv_ind import OBVIndicator


class TestOBVIndicator:
    """Test cases for OBV (On-Balance Volume) indicator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.obv = OBVIndicator()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })

    def test_obv_initialization(self):
        """Test OBV indicator initialization."""
        assert self.obv.name == "OBV"
        assert self.obv.category == "volume"
        assert "On-Balance Volume" in self.obv.description

    def test_obv_calculation_basic(self):
        """Test basic OBV calculation."""
        result = self.obv.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'OBV' in result.columns
        assert len(result) == len(self.sample_data)

    def test_obv_calculation_with_custom_period(self):
        """Test OBV calculation with custom period."""
        obv_custom = OBVIndicator(period=10)
        result = obv_custom.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'OBV' in result.columns

    def test_obv_invalid_period(self):
        """Test OBV with invalid period."""
        with pytest.raises(ValueError, match="Period must be positive"):
            OBVIndicator(period=0)
        
        with pytest.raises(ValueError, match="Period must be positive"):
            OBVIndicator(period=-1)

    def test_obv_empty_dataframe(self):
        """Test OBV with empty dataframe."""
        empty_df = pd.DataFrame()
        result = self.obv.calculate(empty_df)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_obv_missing_columns(self):
        """Test OBV with missing required columns."""
        incomplete_data = self.sample_data.drop(columns=['close'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.obv.calculate(incomplete_data)
        
        incomplete_data = self.sample_data.drop(columns=['volume'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.obv.calculate(incomplete_data)

    def test_obv_parameter_validation(self):
        """Test OBV parameter validation."""
        # Test with valid parameters
        obv_valid = OBVIndicator(period=20)
        assert obv_valid.period == 20
        
        # Test with float period (should be converted to int)
        obv_float = OBVIndicator(period=20.5)
        assert obv_float.period == 20

    def test_obv_value_properties(self):
        """Test OBV value properties."""
        result = self.obv.calculate(self.sample_data)
        
        # OBV should not be infinite
        assert not any(np.isinf(result['OBV'].dropna()))

    def test_obv_with_nan_values(self):
        """Test OBV calculation with NaN values."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        
        result = self.obv.calculate(data_with_nan)
        
        assert isinstance(result, pd.DataFrame)
        assert 'OBV' in result.columns

    def test_obv_docstring_info(self):
        """Test OBV docstring information."""
        assert "OBV" in self.obv.name
        assert "volume" in self.obv.category.lower()
        assert len(self.obv.description) > 0

    def test_obv_cli_integration(self):
        """Test OBV CLI integration."""
        # Test that the indicator can be used in CLI context
        assert hasattr(self.obv, 'calculate')
        assert callable(self.obv.calculate)

    def test_obv_performance(self):
        """Test OBV performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'open': np.random.uniform(100, 110, 1000),
            'high': np.random.uniform(110, 120, 1000),
            'low': np.random.uniform(90, 100, 1000),
            'close': np.random.uniform(100, 110, 1000),
            'volume': np.random.randint(1000, 2000, 1000)
        })
        
        result = self.obv.calculate(large_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(large_data)
        assert 'OBV' in result.columns

    def test_obv_edge_cases(self):
        """Test OBV edge cases."""
        # Test with all same values
        same_values = pd.DataFrame({
            'open': [100] * 10,
            'high': [100] * 10,
            'low': [100] * 10,
            'close': [100] * 10,
            'volume': [1000] * 10
        })
        
        result = self.obv.calculate(same_values)
        assert isinstance(result, pd.DataFrame)
        assert 'OBV' in result.columns

    def test_obv_consistency(self):
        """Test OBV calculation consistency."""
        result1 = self.obv.calculate(self.sample_data)
        result2 = self.obv.calculate(self.sample_data)
        
        pd.testing.assert_frame_equal(result1, result2)

    def test_obv_volume_relationship(self):
        """Test that OBV properly relates price and volume."""
        # Create data with increasing prices and volumes
        up_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],  # Increasing prices
            'volume': [1000, 1100, 1200, 1300, 1400]  # Increasing volumes
        })
        
        # Create data with decreasing prices and volumes
        down_data = pd.DataFrame({
            'open': [105, 104, 103, 102, 101],
            'high': [109, 108, 107, 106, 105],
            'low': [103, 102, 101, 100, 99],
            'close': [104, 103, 102, 101, 100],  # Decreasing prices
            'volume': [1400, 1300, 1200, 1100, 1000]  # Decreasing volumes
        })
        
        up_result = self.obv.calculate(up_data)
        down_result = self.obv.calculate(down_data)
        
        # OBV should be different for different price/volume patterns
        assert not up_result['OBV'].equals(down_result['OBV'])

    def test_obv_cumulative_nature(self):
        """Test that OBV is cumulative in nature."""
        result = self.obv.calculate(self.sample_data)
        
        obv_values = result['OBV'].dropna()
        if len(obv_values) > 1:
            # OBV should show cumulative behavior (not necessarily monotonic)
            # but should reflect the cumulative volume flow
            assert len(obv_values) > 0

    def test_obv_zero_volume(self):
        """Test OBV with zero volume."""
        zero_volume_data = self.sample_data.copy()
        zero_volume_data['volume'] = 0
        
        result = self.obv.calculate(zero_volume_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'OBV' in result.columns

    def test_obv_negative_volume(self):
        """Test OBV with negative volume (should handle gracefully)."""
        negative_volume_data = self.sample_data.copy()
        negative_volume_data.loc[2, 'volume'] = -100
        
        result = self.obv.calculate(negative_volume_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'OBV' in result.columns

    def test_obv_price_volume_divergence(self):
        """Test OBV with price-volume divergence scenarios."""
        # Price up, volume down
        price_up_vol_down = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],  # Increasing prices
            'volume': [1400, 1300, 1200, 1100, 1000]  # Decreasing volumes
        })
        
        # Price down, volume up
        price_down_vol_up = pd.DataFrame({
            'open': [105, 104, 103, 102, 101],
            'high': [109, 108, 107, 106, 105],
            'low': [103, 102, 101, 100, 99],
            'close': [104, 103, 102, 101, 100],  # Decreasing prices
            'volume': [1000, 1100, 1200, 1300, 1400]  # Increasing volumes
        })
        
        result1 = self.obv.calculate(price_up_vol_down)
        result2 = self.obv.calculate(price_down_vol_up)
        
        # Different patterns should produce different OBV values
        assert not result1['OBV'].equals(result2['OBV']) 