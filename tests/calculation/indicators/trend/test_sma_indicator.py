# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_sma_indicator.py

"""
Tests for SMA (Simple Moving Average) indicator.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.trend.sma_ind import calculate_sma, apply_rule_sma
from src.calculation.indicators.base_indicator import PriceType


class TestSMAIndicator:
    """Test class for SMA indicator calculations."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample OHLCV data
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        np.random.seed(42)  # For reproducible tests
        
        # Generate realistic price data
        base_price = 100.0
        price_changes = np.random.normal(0, 1, 50)  # Random price changes
        prices = [base_price]
        
        for change in price_changes[1:]:
            new_price = prices[-1] + change
            prices.append(max(new_price, 1.0))  # Ensure positive prices
        
        self.sample_data = pd.DataFrame({
            'Open': prices,
            'High': [p * 1.02 for p in prices],  # High is 2% above open
            'Low': [p * 0.98 for p in prices],   # Low is 2% below open
            'Close': [p * 1.01 for p in prices], # Close is 1% above open
            'Volume': np.random.randint(1000, 10000, 50)
        }, index=dates)
        
        self.point = 0.01  # Point size for testing
    
    def test_calculate_sma_basic(self):
        """Test basic SMA calculation."""
        period = 10
        close_prices = self.sample_data['Close']
        sma_values = calculate_sma(close_prices, period)
        
        # Check that SMA is calculated
        assert len(sma_values) == len(close_prices)
        assert not sma_values.isna().all()
        
        # Check that first (period-1) values are NaN
        assert sma_values.iloc[:period-1].isna().all()
        
        # Check that period-th value is not NaN
        assert not pd.isna(sma_values.iloc[period-1])
        
        # Check that SMA is reasonable (within price range)
        assert sma_values.iloc[period-1] > 0
        assert sma_values.iloc[period-1] < close_prices.max() * 1.1
    
    def test_calculate_sma_different_periods(self):
        """Test SMA calculation with different periods."""
        close_prices = self.sample_data['Close']
        
        for period in [5, 10, 20]:
            sma_values = calculate_sma(close_prices, period)
            
            # Check that first (period-1) values are NaN
            assert sma_values.iloc[:period-1].isna().all()
            
            # Check that period-th value is not NaN
            assert not pd.isna(sma_values.iloc[period-1])
            
            # Check that SMA values are reasonable
            assert sma_values.iloc[period-1] > 0
    
    def test_calculate_sma_invalid_period(self):
        """Test SMA calculation with invalid period."""
        close_prices = self.sample_data['Close']
        
        # Test with zero period
        with pytest.raises(ValueError, match="SMA period must be positive"):
            calculate_sma(close_prices, 0)
        
        # Test with negative period
        with pytest.raises(ValueError, match="SMA period must be positive"):
            calculate_sma(close_prices, -5)
    
    def test_calculate_sma_insufficient_data(self):
        """Test SMA calculation with insufficient data."""
        short_data = self.sample_data.head(5)
        close_prices = short_data['Close']
        
        # Should not raise error, but return NaN values
        sma_values = calculate_sma(close_prices, 10)
        assert sma_values.isna().all()
    
    def test_apply_rule_sma_close_prices(self):
        """Test SMA rule application with close prices."""
        result = apply_rule_sma(self.sample_data, point=self.point, 
                               sma_period=10, price_type=PriceType.CLOSE)
        
        # Check that required columns are added
        assert 'SMA' in result.columns
        assert 'SMA_Price_Type' in result.columns
        assert 'SMA_Signal' in result.columns
        
        # Check that output columns are present
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'PColor1' in result.columns
        assert 'PColor2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
        
        # Check price type
        assert result['SMA_Price_Type'].iloc[0] == 'Close'
        
        # Check that SMA values are calculated
        assert not result['SMA'].isna().all()
        
        # Check that signals are calculated
        assert 'SMA_Signal' in result.columns
    
    def test_apply_rule_sma_open_prices(self):
        """Test SMA rule application with open prices."""
        result = apply_rule_sma(self.sample_data, point=self.point, 
                               sma_period=10, price_type=PriceType.OPEN)
        
        # Check price type
        assert result['SMA_Price_Type'].iloc[0] == 'Open'
        
        # Check that SMA values are calculated
        assert not result['SMA'].isna().all()
    
    def test_apply_rule_sma_default_parameters(self):
        """Test SMA rule application with default parameters."""
        result = apply_rule_sma(self.sample_data, point=self.point)
        
        # Should use default period (20) and close prices
        assert result['SMA_Price_Type'].iloc[0] == 'Close'
        
        # Check that SMA values are calculated
        assert not result['SMA'].isna().all()
    
    def test_apply_rule_sma_support_resistance_levels(self):
        """Test that SMA rule calculates support and resistance levels."""
        result = apply_rule_sma(self.sample_data, point=self.point, 
                               sma_period=10, price_type=PriceType.CLOSE)
        
        # Check that support and resistance levels are calculated
        assert not result['PPrice1'].isna().all()  # Support levels
        assert not result['PPrice2'].isna().all()  # Resistance levels
        
        # Check that support is below resistance
        valid_mask = ~(result['PPrice1'].isna() | result['PPrice2'].isna())
        if valid_mask.any():
            assert (result.loc[valid_mask, 'PPrice1'] <= result.loc[valid_mask, 'PPrice2']).all()
    
    def test_apply_rule_sma_signals(self):
        """Test that SMA rule generates trading signals."""
        result = apply_rule_sma(self.sample_data, point=self.point, 
                               sma_period=10, price_type=PriceType.CLOSE)
        
        # Check that signals are generated
        assert 'SMA_Signal' in result.columns
        assert not result['SMA_Signal'].isna().all()
        
        # Check that signals are valid values (0, 1, 2)
        valid_signals = result['SMA_Signal'].dropna()
        assert all(signal in [0, 1, 2] for signal in valid_signals)
    
    def test_apply_rule_sma_difference_calculation(self):
        """Test that SMA rule calculates price difference."""
        result = apply_rule_sma(self.sample_data, point=self.point, 
                               sma_period=10, price_type=PriceType.CLOSE)
        
        # Check that difference is calculated
        assert 'Diff' in result.columns
        assert not result['Diff'].isna().all()
        
        # Check that difference is price - SMA
        valid_mask = ~(result['SMA'].isna() | result['Close'].isna())
        if valid_mask.any():
            expected_diff = result.loc[valid_mask, 'Close'] - result.loc[valid_mask, 'SMA']
            actual_diff = result.loc[valid_mask, 'Diff']
            pd.testing.assert_series_equal(expected_diff, actual_diff, check_names=False)
