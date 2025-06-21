# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_adx_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.trend.adx_ind import ADXIndicator


class TestADXIndicator:
    """Test cases for ADX (Average Directional Index) indicator."""

    def setup_method(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'High': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'Close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        self.adx_indicator = ADXIndicator()

    def test_adx_initialization(self):
        """Test ADX indicator initialization."""
        assert self.adx_indicator.name == "ADX"
        assert self.adx_indicator.category == "Trend"

    def test_adx_calculation_basic(self):
        """Test basic ADX calculation."""
        result = self.adx_indicator.calculate(
            self.sample_data, 
            period=14, 
            price_type='close'
        )
        
        assert 'ADX' in result.columns
        assert len(result) == len(self.sample_data)
        assert not result['ADX'].isna().all()

    def test_adx_calculation_with_open_price(self):
        """Test ADX calculation using open price."""
        result = self.adx_indicator.calculate(
            self.sample_data, 
            period=14, 
            price_type='open'
        )
        
        assert 'ADX' in result.columns
        assert len(result) == len(self.sample_data)

    def test_adx_different_periods(self):
        """Test ADX calculation with different periods."""
        periods = [10, 14, 20, 25]
        
        for period in periods:
            result = self.adx_indicator.calculate(
                self.sample_data, 
                period=period, 
                price_type='close'
            )
            
            assert 'ADX' in result.columns
            # First few values should be NaN due to insufficient data
            assert result['ADX'].iloc[:period-1].isna().all()

    def test_adx_invalid_period(self):
        """Test ADX calculation with invalid period."""
        with pytest.raises(ValueError):
            self.adx_indicator.calculate(
                self.sample_data, 
                period=0, 
                price_type='close'
            )

    def test_adx_empty_dataframe(self):
        """Test ADX calculation with empty dataframe."""
        empty_df = pd.DataFrame()
        
        with pytest.raises(ValueError):
            self.adx_indicator.calculate(
                empty_df, 
                period=14, 
                price_type='close'
            )

    def test_adx_missing_columns(self):
        """Test ADX calculation with missing required columns."""
        incomplete_df = self.sample_data.drop(columns=['High', 'Low'])
        
        with pytest.raises(ValueError):
            self.adx_indicator.calculate(
                incomplete_df, 
                period=14, 
                price_type='close'
            )

    def test_adx_parameter_validation(self):
        """Test ADX parameter validation."""
        # Test invalid price_type
        with pytest.raises(ValueError):
            self.adx_indicator.calculate(
                self.sample_data, 
                period=14, 
                price_type='invalid'
            )

    def test_adx_value_range(self):
        """Test that ADX values are within expected range (0-100)."""
        result = self.adx_indicator.calculate(
            self.sample_data, 
            period=14, 
            price_type='close'
        )
        
        adx_values = result['ADX'].dropna()
        assert (adx_values >= 0).all()
        assert (adx_values <= 100).all()

    def test_adx_trend_strength_interpretation(self):
        """Test ADX trend strength interpretation."""
        result = self.adx_indicator.calculate(
            self.sample_data, 
            period=14, 
            price_type='close'
        )
        
        adx_values = result['ADX'].dropna()
        
        # ADX should be able to identify different trend strengths
        # This is more of a validation that the calculation produces reasonable values
        assert len(adx_values) > 0

    def test_adx_with_nan_values(self):
        """Test ADX calculation with NaN values in data."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'High'] = np.nan
        data_with_nan.loc[3, 'Low'] = np.nan
        
        result = self.adx_indicator.calculate(
            data_with_nan, 
            period=14, 
            price_type='close'
        )
        
        assert 'ADX' in result.columns
        # Should handle NaN values gracefully

    def test_adx_docstring_info(self):
        """Test that ADX has proper docstring information."""
        docstring = self.adx_indicator.__doc__
        assert docstring is not None
        assert "ADX" in docstring
        assert "Average Directional Index" in docstring

    def test_adx_cli_integration(self):
        """Test ADX CLI integration."""
        result = self.adx_indicator.calculate(
            self.sample_data, 
            period=14, 
            price_type='close'
        )
        
        assert 'ADX' in result.columns
        assert 'ADX_Period' in result.columns
        assert 'ADX_Price_Type' in result.columns

    def test_adx_performance(self):
        """Test ADX calculation performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'Close': np.random.uniform(100, 200, 1000),
            'Open': np.random.uniform(100, 200, 1000),
            'High': np.random.uniform(100, 200, 1000),
            'Low': np.random.uniform(100, 200, 1000),
            'Volume': np.random.uniform(1000, 5000, 1000)
        })
        
        result = self.adx_indicator.calculate(
            large_data, 
            period=14, 
            price_type='close'
        )
        
        assert 'ADX' in result.columns
        assert len(result) == 1000

    def test_adx_edge_cases(self):
        """Test ADX calculation with edge cases."""
        # Test with very small dataset
        small_data = self.sample_data.head(5)
        
        with pytest.raises(ValueError):
            self.adx_indicator.calculate(
                small_data, 
                period=10, 
                price_type='close'
            )

    def test_adx_consistency(self):
        """Test ADX calculation consistency."""
        result1 = self.adx_indicator.calculate(
            self.sample_data, 
            period=14, 
            price_type='close'
        )
        
        result2 = self.adx_indicator.calculate(
            self.sample_data, 
            period=14, 
            price_type='close'
        )
        
        # Results should be identical for same input
        pd.testing.assert_frame_equal(result1, result2) 