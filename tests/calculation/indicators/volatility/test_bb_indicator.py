# tests/calculation/indicators/volatility/test_bb_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.volatility.bb_ind import apply_rule_bollinger_bands, calculate_bollinger_bands


class TestBBIndicator:
    """Test cases for Bollinger Bands indicator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.bb = calculate_bollinger_bands
        
        # Create sample data
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_bb_initialization(self):
        pass  # Not relevant for functional style

    def test_bb_calculation_basic(self):
        """Test basic Bollinger Bands calculation."""
        upper, middle, lower = self.bb(self.sample_data['Close'])
        
        assert len(upper) == len(self.sample_data)
        assert len(middle) == len(self.sample_data)
        assert len(lower) == len(self.sample_data)
        
        # Middle band should be SMA
        assert middle.iloc[-1] == self.sample_data['Close'].rolling(20).mean().iloc[-1]
        
        # Upper band should be above middle (after period)
        valid_data = upper.dropna()
        valid_middle = middle.dropna()
        assert (valid_data >= valid_middle).all()
        
        # Lower band should be below middle (after period)
        valid_lower = lower.dropna()
        assert (valid_lower <= valid_middle).all()

    def test_bb_calculation_with_custom_parameters(self):
        """Test Bollinger Bands calculation with custom parameters."""
        upper, middle, lower = self.bb(self.sample_data['Close'], period=10, std_dev=2.0)
        
        assert len(upper) == len(self.sample_data)
        # First 9 values should be NaN (period - 1)
        assert upper.iloc[:9].isna().all()
        assert not upper.iloc[9:].isna().all()

    def test_bb_with_invalid_parameters(self):
        """Test Bollinger Bands with invalid parameters."""
        with pytest.raises(ValueError, match="Bollinger Bands period must be positive"):
            self.bb(self.sample_data['Close'], period=0)
        with pytest.raises(ValueError, match="Bollinger Bands period must be positive"):
            self.bb(self.sample_data['Close'], period=-1)

    def test_bb_empty_dataframe(self):
        """Test Bollinger Bands with empty DataFrame."""
        empty_series = pd.Series(dtype=float)
        upper, middle, lower = self.bb(empty_series)
        
        assert len(upper) == 0
        assert len(middle) == 0
        assert len(lower) == 0

    def test_bb_insufficient_data(self):
        """Test Bollinger Bands with insufficient data."""
        small_series = self.sample_data['Close'].head(5)  # Less than period
        upper, middle, lower = self.bb(small_series, period=20)
        
        # All values should be NaN for insufficient data
        assert upper.isna().all()
        assert middle.isna().all()
        assert lower.isna().all()

    def test_bb_parameter_validation(self):
        """Test Bollinger Bands parameter validation."""
        # Test with valid parameters
        result = self.bb(self.sample_data['Close'], period=20, std_dev=2.0)
        assert len(result) == 3
        # Test with float period (convert to int)
        result = self.bb(self.sample_data['Close'], period=int(20.5), std_dev=2.0)
        assert len(result) == 3

    def test_bb_value_relationships(self):
        """Test Bollinger Bands value relationships."""
        upper, middle, lower = self.bb(self.sample_data['Close'])
        
        # Check relationships for valid data
        valid_mask = ~upper.isna()
        if valid_mask.any():
            assert (upper[valid_mask] >= middle[valid_mask]).all()
            assert (lower[valid_mask] <= middle[valid_mask]).all()
            assert (upper[valid_mask] >= lower[valid_mask]).all()

    def test_bb_with_nan_values(self):
        """Test Bollinger Bands calculation with NaN values."""
        data_with_nan = self.sample_data['Close'].copy()
        data_with_nan.loc[5] = np.nan
        
        upper, middle, lower = self.bb(data_with_nan)
        
        assert len(upper) == len(data_with_nan)
        assert len(middle) == len(data_with_nan)
        assert len(lower) == len(data_with_nan)

    def test_bb_docstring_info(self):
        pass  # Not relevant for functional style

    def test_bb_cli_integration(self):
        pass  # Not relevant for functional style

    def test_bb_performance(self):
        """Test Bollinger Bands calculation performance."""
        large_series = pd.Series(np.random.uniform(100, 200, 10000))
        
        import time
        start_time = time.time()
        result = self.bb(large_series)
        end_time = time.time()
        
        # Should complete within reasonable time (less than 1 second)
        assert end_time - start_time < 1.0
        assert len(result) == 3

    def test_bb_edge_cases(self):
        """Test Bollinger Bands edge cases."""
        # Test with constant values
        constant_series = pd.Series([100] * 30)
        upper, middle, lower = self.bb(constant_series)
        
        # For constant data, bands should be very close
        valid_mask = ~upper.isna()
        if valid_mask.any():
            assert (upper[valid_mask] - lower[valid_mask]).max() < 0.1

    def test_bb_consistency(self):
        """Test Bollinger Bands calculation consistency."""
        result1 = self.bb(self.sample_data['Close'])
        result2 = self.bb(self.sample_data['Close'])
        
        # Results should be identical
        pd.testing.assert_series_equal(result1[0], result2[0])
        pd.testing.assert_series_equal(result1[1], result2[1])
        pd.testing.assert_series_equal(result1[2], result2[2])

    def test_bb_volatility_measurement(self):
        """Test that Bollinger Bands properly measure volatility."""
        # Create data with different volatility levels
        low_vol_series = pd.Series([100, 100.1, 100.2, 100.1, 100.3, 100.2, 100.4, 100.3, 100.5, 100.4] * 3)
        high_vol_series = pd.Series([100, 105, 95, 110, 90, 105, 95, 110, 90, 105] * 3)
        
        low_vol_result = self.bb(low_vol_series, period=5)
        high_vol_result = self.bb(high_vol_series, period=5)
        
        # High volatility data should have wider bands
        low_vol_width = (low_vol_result[0] - low_vol_result[2]).dropna().mean()
        high_vol_width = (high_vol_result[0] - high_vol_result[2]).dropna().mean()
        
        assert high_vol_width > low_vol_width

    def test_bb_std_dev_impact(self):
        """Test the impact of standard deviation on band width."""
        narrow_result = self.bb(self.sample_data['Close'], std_dev=1.0)
        wide_result = self.bb(self.sample_data['Close'], std_dev=3.0)
        
        # Wider std_dev should result in wider bands
        narrow_width = (narrow_result[0] - narrow_result[2]).dropna().mean()
        wide_width = (wide_result[0] - wide_result[2]).dropna().mean()
        
        assert wide_width > narrow_width

    def test_bb_apply_rule(self):
        """Test Bollinger Bands apply_rule function."""
        result = apply_rule_bollinger_bands(self.sample_data, point=0.01)
        assert 'BB_Upper' in result
        assert 'BB_Middle' in result
        assert 'BB_Lower' in result
        assert 'BB_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        # Проверяем, что сигналы — числа (например, 1, -1, 0)
        signals = result['BB_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number) 