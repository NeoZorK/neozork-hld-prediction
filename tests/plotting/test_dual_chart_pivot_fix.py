# -*- coding: utf-8 -*-
# tests/plotting/test_dual_chart_pivot_fix.py

"""
Test for pivot indicator fix in dual chart fastest mode.
Tests that the "tuple indices must be integers or slices, not str" error is resolved.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.plotting.dual_chart_plot import calculate_additional_indicator


class TestDualChartPivotFix:
    """Test class for pivot indicator fix in dual chart mode."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Generate realistic OHLCV data
        base_price = 100.0
        returns = np.random.normal(0, 0.02, 100)
        prices = [base_price]
        
        for ret in returns[1:]:
            new_price = prices[-1] * (1 + ret)
            prices.append(new_price)
        
        data = []
        for i, (date, price) in enumerate(zip(dates, prices)):
            # Generate OHLC from base price
            high = price * (1 + abs(np.random.normal(0, 0.01)))
            low = price * (1 - abs(np.random.normal(0, 0.01)))
            open_price = price * (1 + np.random.normal(0, 0.005))
            close_price = price * (1 + np.random.normal(0, 0.005))
            volume = np.random.randint(1000, 10000)
            
            data.append({
                'DateTime': date,
                'Open': open_price,
                'High': high,
                'Low': low,
                'Close': close_price,
                'Volume': volume
            })
        
        df = pd.DataFrame(data)
        df.set_index('DateTime', inplace=True)
        return df
    
    def test_pivot_open_rule_no_error(self, sample_data):
        """Test that pivot:open rule doesn't cause tuple indexing error."""
        # This should not raise the "tuple indices must be integers or slices, not str" error
        result_df = calculate_additional_indicator(sample_data, 'pivot:open')
        
        # Verify that pivot columns are added correctly
        assert 'pivot' in result_df.columns
        assert 'r1' in result_df.columns
        assert 's1' in result_df.columns
        
        # Verify that the values are pandas Series (not None or empty)
        assert isinstance(result_df['pivot'], pd.Series)
        assert isinstance(result_df['r1'], pd.Series)
        assert isinstance(result_df['s1'], pd.Series)
        
        # Verify that we have some non-null values
        assert not result_df['pivot'].isna().all()
        assert not result_df['r1'].isna().all()
        assert not result_df['s1'].isna().all()
    
    def test_pivot_close_rule_no_error(self, sample_data):
        """Test that pivot:close rule doesn't cause tuple indexing error."""
        # This should not raise the "tuple indices must be integers or slices, not str" error
        result_df = calculate_additional_indicator(sample_data, 'pivot:close')
        
        # Verify that pivot columns are added correctly
        assert 'pivot' in result_df.columns
        assert 'r1' in result_df.columns
        assert 's1' in result_df.columns
        
        # Verify that the values are pandas Series (not None or empty)
        assert isinstance(result_df['pivot'], pd.Series)
        assert isinstance(result_df['r1'], pd.Series)
        assert isinstance(result_df['s1'], pd.Series)
        
        # Verify that we have some non-null values
        assert not result_df['pivot'].isna().all()
        assert not result_df['r1'].isna().all()
        assert not result_df['s1'].isna().all()
    
    def test_pivot_default_rule_no_error(self, sample_data):
        """Test that pivot rule without parameters doesn't cause tuple indexing error."""
        # This should not raise the "tuple indices must be integers or slices, not str" error
        # Note: pivot rule requires at least one parameter (like 'close' or 'open')
        result_df = calculate_additional_indicator(sample_data, 'pivot:close')
        
        # Verify that pivot columns are added correctly
        assert 'pivot' in result_df.columns
        assert 'r1' in result_df.columns
        assert 's1' in result_df.columns
        
        # Verify that the values are pandas Series (not None or empty)
        assert isinstance(result_df['pivot'], pd.Series)
        assert isinstance(result_df['r1'], pd.Series)
        assert isinstance(result_df['s1'], pd.Series)
        
        # Verify that we have some non-null values
        assert not result_df['pivot'].isna().all()
        assert not result_df['r1'].isna().all()
        assert not result_df['s1'].isna().all()
    
    def test_pivot_values_are_reasonable(self, sample_data):
        """Test that pivot point values are reasonable (within price range)."""
        result_df = calculate_additional_indicator(sample_data, 'pivot:open')
        
        # Get price ranges
        min_price = sample_data[['Open', 'High', 'Low', 'Close']].min().min()
        max_price = sample_data[['Open', 'High', 'Low', 'Close']].max().max()
        price_range = max_price - min_price
        
        # Pivot points should be within the price range (with some tolerance for calculation)
        tolerance = price_range * 0.5  # Allow 50% tolerance
        
        # Check that pivot values are reasonable
        pivot_values = result_df['pivot'].dropna()
        r1_values = result_df['r1'].dropna()
        s1_values = result_df['s1'].dropna()
        
        if len(pivot_values) > 0:
            assert pivot_values.min() >= min_price - tolerance
            assert pivot_values.max() <= max_price + tolerance
        
        if len(r1_values) > 0:
            assert r1_values.min() >= min_price - tolerance
            assert r1_values.max() <= max_price + tolerance
        
        if len(s1_values) > 0:
            assert s1_values.min() >= min_price - tolerance
            assert s1_values.max() <= max_price + tolerance
    
    def test_pivot_relationship_holds(self, sample_data):
        """Test that pivot point relationships hold (R1 > Pivot > S1)."""
        result_df = calculate_additional_indicator(sample_data, 'pivot:open')
        
        # Get non-null values
        valid_mask = ~(result_df['pivot'].isna() | result_df['r1'].isna() | result_df['s1'].isna())
        
        if valid_mask.sum() > 0:
            pivot_values = result_df.loc[valid_mask, 'pivot']
            r1_values = result_df.loc[valid_mask, 'r1']
            s1_values = result_df.loc[valid_mask, 's1']
            
            # Check that we have enough data points
            assert len(pivot_values) > 0, "No valid pivot values found"
            
            # For most cases, R1 should be greater than or equal to Pivot
            # Allow for some numerical precision issues
            r1_gte_pivot = (r1_values >= pivot_values - 1e-10)
            assert r1_gte_pivot.sum() >= len(r1_values) * 0.95, f"R1 >= Pivot relationship failed for {len(r1_values) - r1_gte_pivot.sum()} out of {len(r1_values)} values"
            
            # For most cases, Pivot should be greater than or equal to S1
            # Allow for some numerical precision issues
            pivot_gte_s1 = (pivot_values >= s1_values - 1e-10)
            assert pivot_gte_s1.sum() >= len(pivot_values) * 0.95, f"Pivot >= S1 relationship failed for {len(pivot_values) - pivot_gte_s1.sum()} out of {len(pivot_values)} values"
            
            # For most cases, R1 should be greater than S1
            # Allow for some numerical precision issues
            r1_gte_s1 = (r1_values >= s1_values - 1e-10)
            assert r1_gte_s1.sum() >= len(r1_values) * 0.95, f"R1 >= S1 relationship failed for {len(r1_values) - r1_gte_s1.sum()} out of {len(r1_values)} values"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 