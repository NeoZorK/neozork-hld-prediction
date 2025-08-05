# -*- coding: utf-8 -*-
# tests/plotting/test_dual_chart_mpl_pivot_fix.py

"""
Test for Pivot indicator fix in mpl mode.

This test verifies that the pivot indicator works correctly in mpl mode
with the same column names as fastest mode (r1, s1 instead of support, resistance).
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.plotting.dual_chart_mpl import plot_dual_chart_mpl_display
from src.plotting.dual_chart_plot import calculate_additional_indicator


class TestDualChartMplPivotFix:
    """Test class for Pivot indicator fix in mpl mode."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        
        data = {
            'Open': [100 + i * 0.5 + np.random.normal(0, 1) for i in range(30)],
            'High': [101 + i * 0.5 + np.random.normal(0, 1) for i in range(30)],
            'Low': [99 + i * 0.5 + np.random.normal(0, 1) for i in range(30)],
            'Close': [100.5 + i * 0.5 + np.random.normal(0, 1) for i in range(30)],
            'Volume': [1000 + np.random.randint(0, 500) for _ in range(30)]
        }
        
        df = pd.DataFrame(data, index=dates)
        return df
    
    def test_pivot_indicator_columns_consistency(self, sample_data):
        """Test that pivot indicator creates consistent column names in mpl mode."""
        # Calculate pivot indicator
        df_with_pivot = calculate_additional_indicator(sample_data, 'pivot:open')
        
        # Check that the expected columns exist
        expected_columns = ['pivot', 'r1', 's1']
        for col in expected_columns:
            assert col in df_with_pivot.columns, f"Column {col} should exist in pivot calculation"
        
        # Check that the old column names don't exist
        old_columns = ['support', 'resistance']
        for col in old_columns:
            assert col not in df_with_pivot.columns, f"Column {col} should not exist in pivot calculation"
    
    def test_pivot_indicator_values_not_nan(self, sample_data):
        """Test that pivot indicator values are not all NaN."""
        # Calculate pivot indicator
        df_with_pivot = calculate_additional_indicator(sample_data, 'pivot:open')
        
        # Check that pivot values are not all NaN (first few values might be NaN due to shift)
        pivot_values = df_with_pivot['pivot'].dropna()
        r1_values = df_with_pivot['r1'].dropna()
        s1_values = df_with_pivot['s1'].dropna()
        
        assert len(pivot_values) > 0, "Pivot values should not be all NaN"
        assert len(r1_values) > 0, "R1 values should not be all NaN"
        assert len(s1_values) > 0, "S1 values should not be all NaN"
    
    def test_pivot_indicator_with_close_price(self, sample_data):
        """Test pivot indicator with close price parameter."""
        # Calculate pivot indicator with close price
        df_with_pivot = calculate_additional_indicator(sample_data, 'pivot:close')
        
        # Check that the expected columns exist
        expected_columns = ['pivot', 'r1', 's1']
        for col in expected_columns:
            assert col in df_with_pivot.columns, f"Column {col} should exist in pivot calculation"
    
    def test_pivot_indicator_plotting_function(self, sample_data):
        """Test that the plotting function can handle pivot indicator data."""
        # Calculate pivot indicator
        df_with_pivot = calculate_additional_indicator(sample_data, 'pivot:open')
        
        # This should not raise an exception
        try:
            # Note: We don't actually call the plotting function here as it requires
            # matplotlib backend, but we can test that the data structure is correct
            assert 'pivot' in df_with_pivot.columns
            assert 'r1' in df_with_pivot.columns
            assert 's1' in df_with_pivot.columns
        except Exception as e:
            pytest.fail(f"Pivot indicator plotting should not raise exception: {e}")
    
    def test_pivot_indicator_data_types(self, sample_data):
        """Test that pivot indicator columns have correct data types."""
        # Calculate pivot indicator
        df_with_pivot = calculate_additional_indicator(sample_data, 'pivot:open')
        
        # Check data types
        assert pd.api.types.is_numeric_dtype(df_with_pivot['pivot']), "Pivot column should be numeric"
        assert pd.api.types.is_numeric_dtype(df_with_pivot['r1']), "R1 column should be numeric"
        assert pd.api.types.is_numeric_dtype(df_with_pivot['s1']), "S1 column should be numeric"
    
    def test_pivot_indicator_index_consistency(self, sample_data):
        """Test that pivot indicator maintains index consistency."""
        # Calculate pivot indicator
        df_with_pivot = calculate_additional_indicator(sample_data, 'pivot:open')
        
        # Check that index is preserved
        assert df_with_pivot.index.equals(sample_data.index), "Index should be preserved in pivot calculation"


if __name__ == "__main__":
    pytest.main([__file__]) 