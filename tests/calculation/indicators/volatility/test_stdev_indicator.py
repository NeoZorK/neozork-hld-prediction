# tests/calculation/indicators/volatility/test_stdev_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.volatility.stdev_ind import calculate_stdev, apply_rule_stdev


class TestStDevIndicator:
    """Test cases for Standard Deviation indicator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.stdev = calculate_stdev
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_stdev_calculation_basic(self):
        """Test basic Standard Deviation calculation."""
        result = self.stdev(self.sample_data['Close'])
        assert isinstance(result, pd.Series)
        assert len(result) == len(self.sample_data) - 1
        assert not result.isna().all()

    def test_stdev_with_custom_period(self):
        """Test Standard Deviation calculation with custom period."""
        result = self.stdev(self.sample_data['Close'], period=10)
        assert isinstance(result, pd.Series)
        assert result.iloc[:9].isna().all()
        assert not result.iloc[9:].isna().all()

    def test_stdev_with_invalid_period(self):
        """Test Standard Deviation with invalid period."""
        with pytest.raises(ValueError, match="Standard Deviation period must be positive"):
            self.stdev(self.sample_data['Close'], period=0)
        with pytest.raises(ValueError, match="Standard Deviation period must be positive"):
            self.stdev(self.sample_data['Close'], period=-1)

    def test_stdev_empty_dataframe(self):
        """Test Standard Deviation with empty dataframe."""
        empty_series = pd.Series(dtype=float)
        result = self.stdev(empty_series)
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_stdev_insufficient_data(self):
        """Test Standard Deviation with insufficient data."""
        small_series = self.sample_data['Close'].head(5)
        result = self.stdev(small_series, period=20)
        assert result.isna().all()

    def test_stdev_parameter_validation(self):
        """Test Standard Deviation parameter validation."""
        result = self.stdev(self.sample_data['Close'], period=20)
        assert isinstance(result, pd.Series)
        result = self.stdev(self.sample_data['Close'], period=int(20.5))
        assert isinstance(result, pd.Series)

    def test_stdev_with_nan_values(self):
        """Test Standard Deviation calculation with NaN values."""
        data_with_nan = self.sample_data['Close'].copy()
        data_with_nan.loc[5] = np.nan
        result = self.stdev(data_with_nan)
        assert isinstance(result, pd.Series)
        assert len(result) == len(data_with_nan) - 1

    def test_stdev_performance(self):
        """Test Standard Deviation performance with larger dataset."""
        large_series = pd.Series(np.random.uniform(100, 200, 10000))
        import time
        start_time = time.time()
        result = self.stdev(large_series)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, pd.Series)

    def test_stdev_edge_cases(self):
        """Test Standard Deviation edge cases."""
        constant_series = pd.Series([100] * 30)
        result = self.stdev(constant_series)
        valid = result.dropna()
        if not valid.empty:
            assert (valid < 0.01).all()

    def test_stdev_apply_rule(self):
        """Test Standard Deviation rule application."""
        result = apply_rule_stdev(self.sample_data, point=0.01)
        assert 'StDev' in result
        assert 'StDev_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['StDev_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number)

    def test_stdev_value_range(self):
        """Test Standard Deviation value range and properties."""
        result = self.stdev(self.sample_data['Close'])
        valid = result.dropna()
        assert (valid >= 0).all()
        assert not any(np.isinf(valid))

    def test_stdev_mathematical_properties(self):
        """Test mathematical properties of Standard Deviation."""
        result = self.stdev(self.sample_data['Close'])
        valid = result.dropna()
        if len(valid) > 0:
            assert (valid >= 0).all()
            assert (valid <= 2.0).all()

    def test_stdev_period_impact(self):
        """Test the impact of period on Standard Deviation calculation."""
        result_short = self.stdev(self.sample_data['Close'], period=5)
        result_long = self.stdev(self.sample_data['Close'], period=20)
        
        # Different periods should produce different results
        assert not result_short.equals(result_long)

    def test_stdev_consistency(self):
        """Test Standard Deviation calculation consistency."""
        result1 = self.stdev(self.sample_data['Close'])
        result2 = self.stdev(self.sample_data['Close'])
        
        pd.testing.assert_series_equal(result1, result2)

    def test_stdev_volatility_measurement(self):
        """Test that Standard Deviation properly measures volatility."""
        # Create data with different volatility levels
        low_vol_data = pd.DataFrame({
            'Open': [100 + i * 0.01 for i in range(30)],
            'High': [100.1 + i * 0.01 for i in range(30)],
            'Low': [99.9 + i * 0.01 for i in range(30)],
            'Close': [100.05 + i * 0.01 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        })
        
        high_vol_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [105 + i * 0.1 for i in range(30)],
            'Low': [95 + i * 0.1 for i in range(30)],
            'Close': [105 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        })
        
        low_vol_result = self.stdev(low_vol_data['Close'])
        high_vol_result = self.stdev(high_vol_data['Close'])
        
        # High volatility data should have higher standard deviation
        low_vol_stdev = low_vol_result.mean()
        high_vol_stdev = high_vol_result.mean()
        
        assert high_vol_stdev > low_vol_stdev 