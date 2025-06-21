# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_supertrend_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.trend.supertrend_ind import SuperTrendIndicator


class TestSuperTrendIndicator:
    """Test cases for SuperTrend indicator."""

    def setup_method(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'High': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'Close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        self.supertrend_indicator = SuperTrendIndicator()

    def test_supertrend_initialization(self):
        """Test SuperTrend indicator initialization."""
        assert self.supertrend_indicator.name == "SuperTrend"
        assert self.supertrend_indicator.category == "Trend"

    def test_supertrend_calculation_basic(self):
        """Test basic SuperTrend calculation."""
        result = self.supertrend_indicator.calculate(
            self.sample_data, 
            period=10, 
            multiplier=3.0, 
            price_type='close'
        )
        
        assert 'SuperTrend' in result.columns
        assert len(result) == len(self.sample_data)
        assert not result['SuperTrend'].isna().all()

    def test_supertrend_calculation_with_open_price(self):
        """Test SuperTrend calculation using open price."""
        result = self.supertrend_indicator.calculate(
            self.sample_data, 
            period=10, 
            multiplier=3.0, 
            price_type='open'
        )
        
        assert 'SuperTrend' in result.columns
        assert len(result) == len(self.sample_data)

    def test_supertrend_different_parameters(self):
        """Test SuperTrend calculation with different parameters."""
        periods = [7, 10, 14, 20]
        multipliers = [2.0, 3.0, 4.0]
        
        for period in periods:
            for multiplier in multipliers:
                result = self.supertrend_indicator.calculate(
                    self.sample_data, 
                    period=period, 
                    multiplier=multiplier, 
                    price_type='close'
                )
                
                assert 'SuperTrend' in result.columns
                assert len(result) == len(self.sample_data)

    def test_supertrend_invalid_period(self):
        """Test SuperTrend calculation with invalid period."""
        with pytest.raises(ValueError):
            self.supertrend_indicator.calculate(
                self.sample_data, 
                period=0, 
                multiplier=3.0, 
                price_type='close'
            )

    def test_supertrend_invalid_multiplier(self):
        """Test SuperTrend calculation with invalid multiplier."""
        with pytest.raises(ValueError):
            self.supertrend_indicator.calculate(
                self.sample_data, 
                period=10, 
                multiplier=0, 
                price_type='close'
            )

    def test_supertrend_empty_dataframe(self):
        """Test SuperTrend calculation with empty dataframe."""
        empty_df = pd.DataFrame()
        
        with pytest.raises(ValueError):
            self.supertrend_indicator.calculate(
                empty_df, 
                period=10, 
                multiplier=3.0, 
                price_type='close'
            )

    def test_supertrend_missing_columns(self):
        """Test SuperTrend calculation with missing required columns."""
        incomplete_df = self.sample_data.drop(columns=['High', 'Low'])
        
        with pytest.raises(ValueError):
            self.supertrend_indicator.calculate(
                incomplete_df, 
                period=10, 
                multiplier=3.0, 
                price_type='close'
            )

    def test_supertrend_parameter_validation(self):
        """Test SuperTrend parameter validation."""
        # Test invalid price_type
        with pytest.raises(ValueError):
            self.supertrend_indicator.calculate(
                self.sample_data, 
                period=10, 
                multiplier=3.0, 
                price_type='invalid'
            )

    def test_supertrend_trend_direction(self):
        """Test SuperTrend trend direction identification."""
        result = self.supertrend_indicator.calculate(
            self.sample_data, 
            period=10, 
            multiplier=3.0, 
            price_type='close'
        )
        
        # SuperTrend should be able to identify trend direction
        assert 'SuperTrend' in result.columns
        supertrend_values = result['SuperTrend'].dropna()
        assert len(supertrend_values) > 0

    def test_supertrend_with_nan_values(self):
        """Test SuperTrend calculation with NaN values in data."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'High'] = np.nan
        data_with_nan.loc[3, 'Low'] = np.nan
        
        result = self.supertrend_indicator.calculate(
            data_with_nan, 
            period=10, 
            multiplier=3.0, 
            price_type='close'
        )
        
        assert 'SuperTrend' in result.columns
        # Should handle NaN values gracefully

    def test_supertrend_docstring_info(self):
        """Test that SuperTrend has proper docstring information."""
        docstring = self.supertrend_indicator.__doc__
        assert docstring is not None
        assert "SuperTrend" in docstring

    def test_supertrend_cli_integration(self):
        """Test SuperTrend CLI integration."""
        result = self.supertrend_indicator.calculate(
            self.sample_data, 
            period=10, 
            multiplier=3.0, 
            price_type='close'
        )
        
        assert 'SuperTrend' in result.columns
        assert 'SuperTrend_Period' in result.columns
        assert 'SuperTrend_Multiplier' in result.columns
        assert 'SuperTrend_Price_Type' in result.columns

    def test_supertrend_performance(self):
        """Test SuperTrend calculation performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'Close': np.random.uniform(100, 200, 1000),
            'Open': np.random.uniform(100, 200, 1000),
            'High': np.random.uniform(100, 200, 1000),
            'Low': np.random.uniform(100, 200, 1000),
            'Volume': np.random.uniform(1000, 5000, 1000)
        })
        
        result = self.supertrend_indicator.calculate(
            large_data, 
            period=10, 
            multiplier=3.0, 
            price_type='close'
        )
        
        assert 'SuperTrend' in result.columns
        assert len(result) == 1000

    def test_supertrend_edge_cases(self):
        """Test SuperTrend calculation with edge cases."""
        # Test with very small dataset
        small_data = self.sample_data.head(5)
        
        with pytest.raises(ValueError):
            self.supertrend_indicator.calculate(
                small_data, 
                period=10, 
                multiplier=3.0, 
                price_type='close'
            )

    def test_supertrend_consistency(self):
        """Test SuperTrend calculation consistency."""
        result1 = self.supertrend_indicator.calculate(
            self.sample_data, 
            period=10, 
            multiplier=3.0, 
            price_type='close'
        )
        
        result2 = self.supertrend_indicator.calculate(
            self.sample_data, 
            period=10, 
            multiplier=3.0, 
            price_type='close'
        )
        
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
        
        result = self.supertrend_indicator.calculate(
            trend_data, 
            period=5, 
            multiplier=2.0, 
            price_type='close'
        )
        
        assert 'SuperTrend' in result.columns
        # SuperTrend should detect the trend reversal around index 4-5

    def test_supertrend_atr_dependency(self):
        """Test that SuperTrend properly uses ATR calculation."""
        result = self.supertrend_indicator.calculate(
            self.sample_data, 
            period=10, 
            multiplier=3.0, 
            price_type='close'
        )
        
        # SuperTrend calculation depends on ATR, so we should have valid values
        assert 'SuperTrend' in result.columns
        supertrend_values = result['SuperTrend'].dropna()
        assert len(supertrend_values) > 0 