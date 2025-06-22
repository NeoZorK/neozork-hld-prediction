# tests/calculation/indicators/volume/test_vwap_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.volume.vwap_ind import calculate_vwap, apply_rule_vwap


class TestVWAPIndicator:
    """Test cases for VWAP (Volume Weighted Average Price) indicator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.vwap = calculate_vwap
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_vwap_calculation_basic(self):
        result = self.vwap(self.sample_data)
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data)
        assert not result.isna().all()

    def test_vwap_with_custom_period(self):
        result = self.vwap(self.sample_data, period=10)
        assert isinstance(result, pd.Series)
        assert result.iloc[:9].isna().all()
        assert not result.iloc[9:].isna().all()

    def test_vwap_with_invalid_period(self):
        with pytest.raises(ValueError, match="VWAP period must be positive"):
            self.vwap(self.sample_data, period=0)
        with pytest.raises(ValueError, match="VWAP period must be positive"):
            self.vwap(self.sample_data, period=-1)

    def test_vwap_empty_dataframe(self):
        empty_df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        result = self.vwap(empty_df)
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_vwap_insufficient_data(self):
        small_df = self.sample_data.head(5)
        result = self.vwap(small_df, period=14)
        assert result.isna().all()

    def test_vwap_parameter_validation(self):
        result = self.vwap(self.sample_data, period=20)
        assert isinstance(result, pd.Series)
        result = self.vwap(self.sample_data, period=int(20.5))
        assert isinstance(result, pd.Series)

    def test_vwap_with_nan_values(self):
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[5, 'High'] = np.nan
        result = self.vwap(data_with_nan)
        assert isinstance(result, pd.Series)
        assert len(result) == len(data_with_nan)

    def test_vwap_performance(self):
        large_data = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 10000),
            'High': np.random.uniform(200, 300, 10000),
            'Low': np.random.uniform(50, 100, 10000),
            'Close': np.random.uniform(100, 200, 10000),
            'Volume': np.random.uniform(1000, 5000, 10000)
        })
        import time
        start_time = time.time()
        result = self.vwap(large_data)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, pd.Series)

    def test_vwap_apply_rule(self):
        result = apply_rule_vwap(self.sample_data, point=0.01)
        assert 'VWAP' in result
        assert 'VWAP_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['VWAP_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number)

    def test_vwap_value_range(self):
        """Test VWAP value range and properties."""
        result = self.vwap(self.sample_data)
        
        # VWAP should be within the price range
        vwap_values = result.dropna()
        if len(vwap_values) > 0:
            assert all(vwap_values >= self.sample_data['Low'].min())
            assert all(vwap_values <= self.sample_data['High'].max())
        
        # VWAP should not be infinite
        assert not any(np.isinf(result.dropna()))

    def test_vwap_docstring_info(self):
        """Test VWAP docstring information."""
        assert "VWAP" in self.vwap.__name__
        assert "volume" in self.vwap.__name__.lower()
        assert len(self.vwap.__doc__) > 0

    def test_vwap_edge_cases(self):
        """Test VWAP edge cases."""
        # Test with all same values
        same_values = pd.DataFrame({
            'Open': [100] * 10,
            'High': [100] * 10,
            'Low': [100] * 10,
            'Close': [100] * 10,
            'Volume': [1000] * 10
        })
        
        result = self.vwap(same_values)
        assert isinstance(result, pd.Series)
        assert not result.isna().all()

    def test_vwap_consistency(self):
        """Test VWAP calculation consistency."""
        result1 = self.vwap(self.sample_data)
        result2 = self.vwap(self.sample_data)
        
        pd.testing.assert_series_equal(result1, result2)

    def test_vwap_volume_weighting(self):
        """Test that VWAP properly weights by volume."""
        # Create data with different volume patterns
        high_volume_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [99, 100, 101, 102, 103],
            'Close': [101, 102, 103, 104, 105],
            'Volume': [1000, 2000, 3000, 4000, 5000]  # Increasing volumes
        })
        
        low_volume_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [99, 100, 101, 102, 103],
            'Close': [101, 102, 103, 104, 105],
            'Volume': [5000, 4000, 3000, 2000, 1000]  # Decreasing volumes
        })
        
        high_vol_result = self.vwap(high_volume_data)
        low_vol_result = self.vwap(low_volume_data)
        
        # VWAP should be different for different volume patterns
        assert not high_vol_result.equals(low_vol_result)

    def test_vwap_price_volume_relationship(self):
        """Test VWAP relationship between price and volume."""
        # Create data where higher prices have higher volumes
        price_vol_corr = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [99, 100, 101, 102, 103],
            'Close': [101, 102, 103, 104, 105],  # Increasing prices
            'Volume': [1000, 1100, 1200, 1300, 1400]  # Increasing volumes
        })
        
        # Create data where higher prices have lower volumes
        price_vol_anti = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [99, 100, 101, 102, 103],
            'Close': [101, 102, 103, 104, 105],  # Increasing prices
            'Volume': [1400, 1300, 1200, 1100, 1000]  # Decreasing volumes
        })
        
        result1 = self.vwap(price_vol_corr)
        result2 = self.vwap(price_vol_anti)
        
        # Different price-volume relationships should produce different VWAP
        assert not result1.equals(result2)

    def test_vwap_zero_volume(self):
        """Test VWAP with zero volume."""
        zero_volume_data = self.sample_data.copy()
        zero_volume_data['Volume'] = 0
        
        result = self.vwap(zero_volume_data)
        
        assert isinstance(result, pd.Series)
        assert not result.isna().all()

    def test_vwap_negative_volume(self):
        """Test VWAP with negative volume (should handle gracefully)."""
        negative_volume_data = self.sample_data.copy()
        negative_volume_data.loc[5, 'Volume'] = -100
        
        result = self.vwap(negative_volume_data)
        
        assert isinstance(result, pd.Series)
        assert not result.isna().all()

    def test_vwap_period_impact(self):
        """Test the impact of period on VWAP calculation."""
        vwap_short = self.vwap(self.sample_data, period=5)
        vwap_long = self.vwap(self.sample_data, period=20)
        
        result_short = vwap_short
        result_long = vwap_long
        
        # Different periods should produce different results
        assert not result_short.equals(result_long)

    def test_vwap_mathematical_properties(self):
        """Test mathematical properties of VWAP."""
        # VWAP should be a weighted average of typical prices
        # where typical price = (high + low + close) / 3
        result = self.vwap(self.sample_data)
        
        vwap_values = result.dropna()
        if len(vwap_values) > 0:
            # VWAP should be within reasonable bounds
            assert all(vwap_values >= 0)
            assert all(vwap_values <= 1000)  # Reasonable upper bound for this data 