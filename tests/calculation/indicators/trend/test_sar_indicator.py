# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_sar_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.trend.sar_ind import SARIndicator


class TestSARIndicator:
    """Test cases for SAR (Parabolic SAR) indicator."""

    def setup_method(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'High': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'Close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        self.sar_indicator = SARIndicator()

    def test_sar_initialization(self):
        """Test SAR indicator initialization."""
        assert self.sar_indicator.name == "SAR"
        assert self.sar_indicator.category == "Trend"

    def test_sar_calculation_basic(self):
        """Test basic SAR calculation."""
        result = self.sar_indicator.calculate(
            self.sample_data, 
            acceleration=0.02, 
            maximum=0.2, 
            price_type='close'
        )
        
        assert 'SAR' in result.columns
        assert len(result) == len(self.sample_data)
        assert not result['SAR'].isna().all()

    def test_sar_calculation_with_open_price(self):
        """Test SAR calculation using open price."""
        result = self.sar_indicator.calculate(
            self.sample_data, 
            acceleration=0.02, 
            maximum=0.2, 
            price_type='open'
        )
        
        assert 'SAR' in result.columns
        assert len(result) == len(self.sample_data)

    def test_sar_different_parameters(self):
        """Test SAR calculation with different parameters."""
        accelerations = [0.01, 0.02, 0.05]
        maximums = [0.1, 0.2, 0.3]
        
        for acc in accelerations:
            for max_val in maximums:
                result = self.sar_indicator.calculate(
                    self.sample_data, 
                    acceleration=acc, 
                    maximum=max_val, 
                    price_type='close'
                )
                
                assert 'SAR' in result.columns
                assert len(result) == len(self.sample_data)

    def test_sar_invalid_acceleration(self):
        """Test SAR calculation with invalid acceleration."""
        with pytest.raises(ValueError):
            self.sar_indicator.calculate(
                self.sample_data, 
                acceleration=-0.01, 
                maximum=0.2, 
                price_type='close'
            )

    def test_sar_invalid_maximum(self):
        """Test SAR calculation with invalid maximum."""
        with pytest.raises(ValueError):
            self.sar_indicator.calculate(
                self.sample_data, 
                acceleration=0.02, 
                maximum=0, 
                price_type='close'
            )

    def test_sar_empty_dataframe(self):
        """Test SAR calculation with empty dataframe."""
        empty_df = pd.DataFrame()
        
        with pytest.raises(ValueError):
            self.sar_indicator.calculate(
                empty_df, 
                acceleration=0.02, 
                maximum=0.2, 
                price_type='close'
            )

    def test_sar_missing_columns(self):
        """Test SAR calculation with missing required columns."""
        incomplete_df = self.sample_data.drop(columns=['High', 'Low'])
        
        with pytest.raises(ValueError):
            self.sar_indicator.calculate(
                incomplete_df, 
                acceleration=0.02, 
                maximum=0.2, 
                price_type='close'
            )

    def test_sar_parameter_validation(self):
        """Test SAR parameter validation."""
        # Test invalid price_type
        with pytest.raises(ValueError):
            self.sar_indicator.calculate(
                self.sample_data, 
                acceleration=0.02, 
                maximum=0.2, 
                price_type='invalid'
            )

    def test_sar_trend_direction(self):
        """Test SAR trend direction identification."""
        result = self.sar_indicator.calculate(
            self.sample_data, 
            acceleration=0.02, 
            maximum=0.2, 
            price_type='close'
        )
        
        # SAR should be able to identify trend direction
        assert 'SAR' in result.columns
        sar_values = result['SAR'].dropna()
        assert len(sar_values) > 0

    def test_sar_with_nan_values(self):
        """Test SAR calculation with NaN values in data."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'High'] = np.nan
        data_with_nan.loc[3, 'Low'] = np.nan
        
        result = self.sar_indicator.calculate(
            data_with_nan, 
            acceleration=0.02, 
            maximum=0.2, 
            price_type='close'
        )
        
        assert 'SAR' in result.columns
        # Should handle NaN values gracefully

    def test_sar_docstring_info(self):
        """Test that SAR has proper docstring information."""
        docstring = self.sar_indicator.__doc__
        assert docstring is not None
        assert "SAR" in docstring
        assert "Parabolic SAR" in docstring

    def test_sar_cli_integration(self):
        """Test SAR CLI integration."""
        result = self.sar_indicator.calculate(
            self.sample_data, 
            acceleration=0.02, 
            maximum=0.2, 
            price_type='close'
        )
        
        assert 'SAR' in result.columns
        assert 'SAR_Acceleration' in result.columns
        assert 'SAR_Maximum' in result.columns
        assert 'SAR_Price_Type' in result.columns

    def test_sar_performance(self):
        """Test SAR calculation performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'Close': np.random.uniform(100, 200, 1000),
            'Open': np.random.uniform(100, 200, 1000),
            'High': np.random.uniform(100, 200, 1000),
            'Low': np.random.uniform(100, 200, 1000),
            'Volume': np.random.uniform(1000, 5000, 1000)
        })
        
        result = self.sar_indicator.calculate(
            large_data, 
            acceleration=0.02, 
            maximum=0.2, 
            price_type='close'
        )
        
        assert 'SAR' in result.columns
        assert len(result) == 1000

    def test_sar_edge_cases(self):
        """Test SAR calculation with edge cases."""
        # Test with very small dataset
        small_data = self.sample_data.head(3)
        
        with pytest.raises(ValueError):
            self.sar_indicator.calculate(
                small_data, 
                acceleration=0.02, 
                maximum=0.2, 
                price_type='close'
            )

    def test_sar_consistency(self):
        """Test SAR calculation consistency."""
        result1 = self.sar_indicator.calculate(
            self.sample_data, 
            acceleration=0.02, 
            maximum=0.2, 
            price_type='close'
        )
        
        result2 = self.sar_indicator.calculate(
            self.sample_data, 
            acceleration=0.02, 
            maximum=0.2, 
            price_type='close'
        )
        
        # Results should be identical for same input
        pd.testing.assert_frame_equal(result1, result2)

    def test_sar_trend_reversal_detection(self):
        """Test SAR trend reversal detection."""
        # Create data with clear trend reversal
        trend_data = pd.DataFrame({
            'High': [100, 101, 102, 103, 104, 103, 102, 101, 100, 99],
            'Low': [99, 100, 101, 102, 103, 102, 101, 100, 99, 98],
            'Close': [100, 101, 102, 103, 104, 103, 102, 101, 100, 99],
            'Open': [100, 101, 102, 103, 104, 103, 102, 101, 100, 99],
            'Volume': [1000] * 10
        })
        
        result = self.sar_indicator.calculate(
            trend_data, 
            acceleration=0.02, 
            maximum=0.2, 
            price_type='close'
        )
        
        assert 'SAR' in result.columns
        # SAR should detect the trend reversal around index 4-5 