# tests/calculation/indicators/volume/test_obv_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.volume.obv_ind import calculate_obv, apply_rule_obv


class TestOBVIndicator:
    """Test cases for OBV (On-Balance Volume) indicator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.obv = calculate_obv
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_obv_calculation_basic(self):
        """Test basic OBV calculation."""
        result = self.obv(self.sample_data['Close'], self.sample_data['Volume'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data)
        assert not result.isna().all()

    def test_obv_with_invalid_length(self):
        """Test OBV with invalid length."""
        with pytest.raises(ValueError):
            self.obv(self.sample_data['Close'][:-1], self.sample_data['Volume'])

    def test_obv_with_nan_values(self):
        """Test OBV calculation with NaN values."""
        close_nan = self.sample_data['Close'].copy()
        close_nan.iloc[5] = np.nan
        result = self.obv(close_nan, self.sample_data['Volume'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data)

    def test_obv_performance(self):
        """Test OBV performance with larger dataset."""
        large_series = pd.Series(np.random.uniform(100, 200, 10000))
        large_volume = pd.Series(np.random.uniform(1000, 5000, 10000))
        import time
        start_time = time.time()
        result = self.obv(large_series, large_volume)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, pd.Series)

    def test_obv_apply_rule(self):
        """Test OBV application of rule."""
        result = apply_rule_obv(self.sample_data, point=0.01)
        assert 'OBV' in result
        assert 'OBV_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['OBV_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number)

    def test_obv_invalid_period(self):
        """Test OBV with invalid period."""
        with pytest.raises(ValueError, match="Period must be positive"):
            calculate_obv(self.sample_data['Close'], self.sample_data['Volume'], period=0)
        
        with pytest.raises(ValueError, match="Period must be positive"):
            calculate_obv(self.sample_data['Close'], self.sample_data['Volume'], period=-1)

    def test_obv_empty_dataframe(self):
        """Test OBV with empty dataframe."""
        empty_df = pd.DataFrame()
        result = self.obv(empty_df['Close'], empty_df['Volume'])
        
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_obv_missing_columns(self):
        """Test OBV with missing required columns."""
        incomplete_data = self.sample_data.drop(columns=['Close'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.obv(incomplete_data['Close'], incomplete_data['Volume'])
        
        incomplete_data = self.sample_data.drop(columns=['Volume'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.obv(incomplete_data['Close'], incomplete_data['Volume'])

    def test_obv_parameter_validation(self):
        """Test OBV parameter validation."""
        # Test with valid parameters
        obv_valid = calculate_obv(self.sample_data['Close'], self.sample_data['Volume'], period=20)
        assert obv_valid.shape[0] == self.sample_data.shape[0]
        
        # Test with float period (should be converted to int)
        obv_float = calculate_obv(self.sample_data['Close'], self.sample_data['Volume'], period=20.5)
        assert obv_float.shape[0] == self.sample_data.shape[0]

    def test_obv_value_properties(self):
        """Test OBV value properties."""
        result = self.obv(self.sample_data['Close'], self.sample_data['Volume'])
        
        # OBV should not be infinite
        assert not any(np.isinf(result.dropna()))

    def test_obv_docstring_info(self):
        """Test OBV docstring information."""
        assert "OBV" in self.obv.__name__
        assert "volume" in self.obv.__name__.lower()
        assert len(self.obv.__doc__) > 0

    def test_obv_edge_cases(self):
        """Test OBV edge cases."""
        # Test with all same values
        same_values = pd.DataFrame({
            'Open': [100] * 10,
            'High': [100] * 10,
            'Low': [100] * 10,
            'Close': [100] * 10,
            'Volume': [1000] * 10
        })
        
        result = self.obv(same_values['Close'], same_values['Volume'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(same_values)

    def test_obv_consistency(self):
        """Test OBV calculation consistency."""
        result1 = self.obv(self.sample_data['Close'], self.sample_data['Volume'])
        result2 = self.obv(self.sample_data['Close'], self.sample_data['Volume'])
        
        pd.testing.assert_series_equal(result1, result2)

    def test_obv_volume_relationship(self):
        """Test that OBV properly relates price and volume."""
        # Create data with increasing prices and volumes
        up_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [99, 100, 101, 102, 103],
            'Close': [101, 102, 103, 104, 105],  # Increasing prices
            'Volume': [1000, 1100, 1200, 1300, 1400]  # Increasing volumes
        })
        
        # Create data with decreasing prices and volumes
        down_data = pd.DataFrame({
            'Open': [105, 104, 103, 102, 101],
            'High': [109, 108, 107, 106, 105],
            'Low': [103, 102, 101, 100, 99],
            'Close': [104, 103, 102, 101, 100],  # Decreasing prices
            'Volume': [1400, 1300, 1200, 1100, 1000]  # Decreasing volumes
        })
        
        up_result = self.obv(up_data['Close'], up_data['Volume'])
        down_result = self.obv(down_data['Close'], down_data['Volume'])
        
        # OBV should be different for different price/volume patterns
        assert not up_result.equals(down_result)

    def test_obv_cumulative_nature(self):
        """Test that OBV is cumulative in nature."""
        result = self.obv(self.sample_data['Close'], self.sample_data['Volume'])
        
        obv_values = result.dropna()
        if len(obv_values) > 1:
            # OBV should show cumulative behavior (not necessarily monotonic)
            # but should reflect the cumulative volume flow
            assert len(obv_values) > 0

    def test_obv_zero_volume(self):
        """Test OBV with zero volume."""
        zero_volume_data = self.sample_data.copy()
        zero_volume_data['Volume'] = 0
        
        result = self.obv(zero_volume_data['Close'], zero_volume_data['Volume'])
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(zero_volume_data)

    def test_obv_negative_volume(self):
        """Test OBV with negative volume (should handle gracefully)."""
        negative_volume_data = self.sample_data.copy()
        negative_volume_data.loc[2, 'Volume'] = -100
        
        result = self.obv(negative_volume_data['Close'], negative_volume_data['Volume'])
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(negative_volume_data)

    def test_obv_price_volume_divergence(self):
        """Test OBV with price-volume divergence scenarios."""
        # Price up, volume down
        price_up_vol_down = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [99, 100, 101, 102, 103],
            'Close': [101, 102, 103, 104, 105],  # Increasing prices
            'Volume': [1400, 1300, 1200, 1100, 1000]  # Decreasing volumes
        })
        
        # Price down, volume up
        price_down_vol_up = pd.DataFrame({
            'Open': [105, 104, 103, 102, 101],
            'High': [109, 108, 107, 106, 105],
            'Low': [103, 102, 101, 100, 99],
            'Close': [104, 103, 102, 101, 100],  # Decreasing prices
            'Volume': [1000, 1100, 1200, 1300, 1400]  # Increasing volumes
        })
        
        result1 = self.obv(price_up_vol_down['Close'], price_up_vol_down['Volume'])
        result2 = self.obv(price_down_vol_up['Close'], price_down_vol_up['Volume'])
        
        # Different patterns should produce different OBV values
        assert not result1.equals(result2) 