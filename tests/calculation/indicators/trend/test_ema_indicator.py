# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_ema_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.trend.ema_ind import EMAIndicator


class TestEMAIndicator:
    """Test cases for EMA (Exponential Moving Average) indicator."""

    def setup_method(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'High': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'Close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        self.ema_indicator = EMAIndicator()

    def test_ema_initialization(self):
        """Test EMA indicator initialization."""
        assert self.ema_indicator.name == "EMA"
        assert self.ema_indicator.category == "Trend"

    def test_ema_calculation_basic(self):
        """Test basic EMA calculation."""
        result = self.ema_indicator.calculate(
            self.sample_data, 
            period=5, 
            price_type='close'
        )
        
        assert 'EMA' in result.columns
        assert len(result) == len(self.sample_data)
        assert not result['EMA'].isna().all()

    def test_ema_calculation_with_open_price(self):
        """Test EMA calculation using open price."""
        result = self.ema_indicator.calculate(
            self.sample_data, 
            period=5, 
            price_type='open'
        )
        
        assert 'EMA' in result.columns
        assert len(result) == len(self.sample_data)

    def test_ema_different_periods(self):
        """Test EMA calculation with different periods."""
        periods = [3, 5, 10, 20]
        
        for period in periods:
            result = self.ema_indicator.calculate(
                self.sample_data, 
                period=period, 
                price_type='close'
            )
            
            assert 'EMA' in result.columns
            # First few values should be NaN due to insufficient data
            assert result['EMA'].iloc[:period-1].isna().all()

    def test_ema_invalid_period(self):
        """Test EMA calculation with invalid period."""
        with pytest.raises(ValueError):
            self.ema_indicator.calculate(
                self.sample_data, 
                period=0, 
                price_type='close'
            )

    def test_ema_empty_dataframe(self):
        """Test EMA calculation with empty dataframe."""
        empty_df = pd.DataFrame()
        
        with pytest.raises(ValueError):
            self.ema_indicator.calculate(
                empty_df, 
                period=5, 
                price_type='close'
            )

    def test_ema_missing_columns(self):
        """Test EMA calculation with missing required columns."""
        incomplete_df = self.sample_data.drop(columns=['Close'])
        
        with pytest.raises(ValueError):
            self.ema_indicator.calculate(
                incomplete_df, 
                period=5, 
                price_type='close'
            )

    def test_ema_parameter_validation(self):
        """Test EMA parameter validation."""
        # Test invalid price_type
        with pytest.raises(ValueError):
            self.ema_indicator.calculate(
                self.sample_data, 
                period=5, 
                price_type='invalid'
            )

    def test_ema_mathematical_correctness(self):
        """Test EMA mathematical correctness."""
        # Create simple test data
        simple_data = pd.DataFrame({
            'Close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        })
        
        result = self.ema_indicator.calculate(
            simple_data, 
            period=3, 
            price_type='close'
        )
        
        # Check that EMA values are reasonable
        assert result['EMA'].iloc[-1] > result['EMA'].iloc[-2]  # Should be increasing
        assert not result['EMA'].isna().all()

    def test_ema_with_nan_values(self):
        """Test EMA calculation with NaN values in data."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'Close'] = np.nan
        
        result = self.ema_indicator.calculate(
            data_with_nan, 
            period=5, 
            price_type='close'
        )
        
        assert 'EMA' in result.columns
        # Should handle NaN values gracefully

    def test_ema_docstring_info(self):
        """Test that EMA has proper docstring information."""
        docstring = self.ema_indicator.__doc__
        assert docstring is not None
        assert "EMA" in docstring
        assert "Exponential Moving Average" in docstring

    def test_ema_cli_integration(self):
        """Test EMA CLI integration."""
        # Test that the indicator can be called via CLI parameters
        result = self.ema_indicator.calculate(
            self.sample_data, 
            period=10, 
            price_type='close'
        )
        
        assert 'EMA' in result.columns
        assert 'EMA_Period' in result.columns
        assert 'EMA_Price_Type' in result.columns

    def test_ema_performance(self):
        """Test EMA calculation performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'Close': np.random.uniform(100, 200, 1000),
            'Open': np.random.uniform(100, 200, 1000),
            'High': np.random.uniform(100, 200, 1000),
            'Low': np.random.uniform(100, 200, 1000),
            'Volume': np.random.uniform(1000, 5000, 1000)
        })
        
        result = self.ema_indicator.calculate(
            large_data, 
            period=20, 
            price_type='close'
        )
        
        assert 'EMA' in result.columns
        assert len(result) == 1000 