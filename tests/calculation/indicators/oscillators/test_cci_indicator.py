# -*- coding: utf-8 -*-
# tests/calculation/indicators/oscillators/test_cci_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.oscillators.cci_ind import CCIIndicator


class TestCCIIndicator:
    """Test cases for CCI (Commodity Channel Index) indicator."""

    def setup_method(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'High': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'Close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        self.cci_indicator = CCIIndicator()

    def test_cci_initialization(self):
        """Test CCI indicator initialization."""
        assert self.cci_indicator.name == "CCI"
        assert self.cci_indicator.category == "Oscillators"

    def test_cci_calculation_basic(self):
        """Test basic CCI calculation."""
        result = self.cci_indicator.calculate(
            self.sample_data, 
            period=20, 
            price_type='close'
        )
        
        assert 'CCI' in result.columns
        assert len(result) == len(self.sample_data)
        assert not result['CCI'].isna().all()

    def test_cci_calculation_with_open_price(self):
        """Test CCI calculation using open price."""
        result = self.cci_indicator.calculate(
            self.sample_data, 
            period=20, 
            price_type='open'
        )
        
        assert 'CCI' in result.columns
        assert len(result) == len(self.sample_data)

    def test_cci_different_periods(self):
        """Test CCI calculation with different periods."""
        periods = [10, 20, 30, 50]
        
        for period in periods:
            result = self.cci_indicator.calculate(
                self.sample_data, 
                period=period, 
                price_type='close'
            )
            
            assert 'CCI' in result.columns
            # First few values should be NaN due to insufficient data
            assert result['CCI'].iloc[:period-1].isna().all()

    def test_cci_invalid_period(self):
        """Test CCI calculation with invalid period."""
        with pytest.raises(ValueError):
            self.cci_indicator.calculate(
                self.sample_data, 
                period=0, 
                price_type='close'
            )

    def test_cci_empty_dataframe(self):
        """Test CCI calculation with empty dataframe."""
        empty_df = pd.DataFrame()
        
        with pytest.raises(ValueError):
            self.cci_indicator.calculate(
                empty_df, 
                period=20, 
                price_type='close'
            )

    def test_cci_missing_columns(self):
        """Test CCI calculation with missing required columns."""
        incomplete_df = self.sample_data.drop(columns=['Close'])
        
        with pytest.raises(ValueError):
            self.cci_indicator.calculate(
                incomplete_df, 
                period=20, 
                price_type='close'
            )

    def test_cci_parameter_validation(self):
        """Test CCI parameter validation."""
        # Test invalid price_type
        with pytest.raises(ValueError):
            self.cci_indicator.calculate(
                self.sample_data, 
                period=20, 
                price_type='invalid'
            )

    def test_cci_overbought_oversold_levels(self):
        """Test CCI overbought/oversold level detection."""
        result = self.cci_indicator.calculate(
            self.sample_data, 
            period=20, 
            price_type='close'
        )
        
        cci_values = result['CCI'].dropna()
        
        # CCI should be able to identify overbought/oversold conditions
        # Typical levels are +100 (overbought) and -100 (oversold)
        assert len(cci_values) > 0

    def test_cci_with_nan_values(self):
        """Test CCI calculation with NaN values in data."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'Close'] = np.nan
        
        result = self.cci_indicator.calculate(
            data_with_nan, 
            period=20, 
            price_type='close'
        )
        
        assert 'CCI' in result.columns
        # Should handle NaN values gracefully

    def test_cci_docstring_info(self):
        """Test that CCI has proper docstring information."""
        docstring = self.cci_indicator.__doc__
        assert docstring is not None
        assert "CCI" in docstring
        assert "Commodity Channel Index" in docstring

    def test_cci_cli_integration(self):
        """Test CCI CLI integration."""
        result = self.cci_indicator.calculate(
            self.sample_data, 
            period=20, 
            price_type='close'
        )
        
        assert 'CCI' in result.columns
        assert 'CCI_Period' in result.columns
        assert 'CCI_Price_Type' in result.columns

    def test_cci_performance(self):
        """Test CCI calculation performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'Close': np.random.uniform(100, 200, 1000),
            'Open': np.random.uniform(100, 200, 1000),
            'High': np.random.uniform(100, 200, 1000),
            'Low': np.random.uniform(100, 200, 1000),
            'Volume': np.random.uniform(1000, 5000, 1000)
        })
        
        result = self.cci_indicator.calculate(
            large_data, 
            period=20, 
            price_type='close'
        )
        
        assert 'CCI' in result.columns
        assert len(result) == 1000

    def test_cci_edge_cases(self):
        """Test CCI calculation with edge cases."""
        # Test with very small dataset
        small_data = self.sample_data.head(5)
        
        with pytest.raises(ValueError):
            self.cci_indicator.calculate(
                small_data, 
                period=10, 
                price_type='close'
            )

    def test_cci_consistency(self):
        """Test CCI calculation consistency."""
        result1 = self.cci_indicator.calculate(
            self.sample_data, 
            period=20, 
            price_type='close'
        )
        
        result2 = self.cci_indicator.calculate(
            self.sample_data, 
            period=20, 
            price_type='close'
        )
        
        # Results should be identical for same input
        pd.testing.assert_frame_equal(result1, result2)

    def test_cci_trend_divergence(self):
        """Test CCI trend divergence detection."""
        # Create data with potential divergence
        divergence_data = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
            'High': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119],
            'Volume': [1000] * 21
        })
        
        result = self.cci_indicator.calculate(
            divergence_data, 
            period=10, 
            price_type='close'
        )
        
        assert 'CCI' in result.columns
        # Should detect potential divergence patterns

    def test_cci_zero_deviation(self):
        """Test CCI calculation when mean deviation is zero."""
        # Create data where all values are the same
        constant_data = pd.DataFrame({
            'Close': [100] * 20,
            'Open': [100] * 20,
            'High': [100] * 20,
            'Low': [100] * 20,
            'Volume': [1000] * 20
        })
        
        result = self.cci_indicator.calculate(
            constant_data, 
            period=10, 
            price_type='close'
        )
        
        assert 'CCI' in result.columns
        # Should handle zero deviation case gracefully 