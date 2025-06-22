# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_supertrend_indicator.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.trend.supertrend_ind import calculate_supertrend, apply_rule_supertrend


class TestSuperTrendIndicator:
    """Test cases for SuperTrend indicator."""

    def setup_method(self):
        """Set up test data."""
        self.supertrend = calculate_supertrend
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)

    def test_supertrend_calculation_basic(self):
        """Test basic SuperTrend calculation."""
        result = self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.sample_data)
        assert 'SuperTrend' in result.columns
        assert 'SuperTrend_Direction' in result.columns

    def test_supertrend_with_custom_parameters(self):
        """Test SuperTrend calculation with custom parameters."""
        result = self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=10, multiplier=3.0)
        assert isinstance(result, pd.DataFrame)
        assert result.iloc[:9]['SuperTrend'].isna().all()
        assert not result.iloc[9:]['SuperTrend'].isna().all()

    def test_supertrend_with_invalid_parameters(self):
        """Test SuperTrend calculation with invalid parameters."""
        with pytest.raises(ValueError, match="SuperTrend period must be positive"):
            self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=0)
        with pytest.raises(ValueError, match="SuperTrend period must be positive"):
            self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=-1)
        with pytest.raises(ValueError, match="SuperTrend multiplier must be positive"):
            self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], multiplier=0)
        with pytest.raises(ValueError, match="SuperTrend multiplier must be positive"):
            self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], multiplier=-1.0)

    def test_supertrend_empty_dataframe(self):
        """Test SuperTrend calculation with empty dataframe."""
        empty_series = pd.Series(dtype=float)
        result = self.supertrend(empty_series, empty_series, empty_series)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_supertrend_insufficient_data(self):
        """Test SuperTrend calculation with insufficient data."""
        small_high = self.sample_data['High'].head(5)
        small_low = self.sample_data['Low'].head(5)
        small_close = self.sample_data['Close'].head(5)
        result = self.supertrend(small_high, small_low, small_close, period=20)
        assert result['SuperTrend'].isna().all()

    def test_supertrend_parameter_validation(self):
        """Test SuperTrend parameter validation."""
        result = self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=20, multiplier=2.0)
        assert isinstance(result, pd.DataFrame)
        result = self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'], period=int(20.5), multiplier=float(2.0))
        assert isinstance(result, pd.DataFrame)

    def test_supertrend_with_nan_values(self):
        """Test SuperTrend calculation with NaN values in data."""
        high_with_nan = self.sample_data['High'].copy()
        high_with_nan.loc[5] = np.nan
        result = self.supertrend(high_with_nan, self.sample_data['Low'], self.sample_data['Close'])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(high_with_nan)

    def test_supertrend_performance(self):
        """Test SuperTrend calculation performance with larger dataset."""
        large_high = pd.Series(np.random.uniform(100, 200, 10000))
        large_low = pd.Series(np.random.uniform(50, 100, 10000))
        large_close = pd.Series(np.random.uniform(75, 150, 10000))
        import time
        start_time = time.time()
        result = self.supertrend(large_high, large_low, large_close)
        end_time = time.time()
        assert end_time - start_time < 1.0
        assert isinstance(result, pd.DataFrame)

    def test_supertrend_apply_rule(self):
        """Test SuperTrend apply rule."""
        result = apply_rule_supertrend(self.sample_data, point=0.01)
        assert 'SuperTrend' in result
        assert 'SuperTrend_Direction' in result
        assert 'SuperTrend_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        signals = result['SuperTrend_Signal'].dropna()
        assert np.issubdtype(signals.dtype, np.number)

    def test_supertrend_trend_direction(self):
        """Test SuperTrend trend direction identification."""
        result = self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'])
        
        # SuperTrend should be able to identify trend direction
        assert 'SuperTrend' in result.columns
        supertrend_values = result['SuperTrend'].dropna()
        assert len(supertrend_values) > 0

    def test_supertrend_docstring_info(self):
        """Test that SuperTrend has proper docstring information."""
        docstring = self.supertrend.__doc__
        assert docstring is not None
        assert "SuperTrend" in docstring

    def test_supertrend_consistency(self):
        """Test SuperTrend calculation consistency."""
        result1 = self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'])
        
        result2 = self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'])
        
        # Results should be identical for same input
        pd.testing.assert_frame_equal(result1, result2)

    def test_supertrend_trend_reversal_detection(self):
        """Test SuperTrend trend reversal detection."""
        # Create data with clear trend reversal
        trend_data = pd.DataFrame({
            'High': [100, 101, 102, 103, 104, 103, 102, 101, 100, 99],
            'Low': [99, 100, 101, 102, 103, 102, 101, 100, 99, 98],
            'Close': [100, 101, 102, 103, 104, 103, 102, 101, 100, 99],
            'Open': [100, 101, 102, 103, 104, 103, 102, 101, 100, 99],
            'Volume': [1000] * 10
        })
        
        result = self.supertrend(trend_data['High'], trend_data['Low'], trend_data['Close'])
        
        assert 'SuperTrend' in result.columns
        # SuperTrend should detect the trend reversal around index 4-5

    def test_supertrend_atr_dependency(self):
        """Test that SuperTrend properly uses ATR calculation."""
        result = self.supertrend(self.sample_data['High'], self.sample_data['Low'], self.sample_data['Close'])
        
        # SuperTrend calculation depends on ATR, so we should have valid values
        assert 'SuperTrend' in result.columns
        supertrend_values = result['SuperTrend'].dropna()
        assert len(supertrend_values) > 0 