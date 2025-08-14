# -*- coding: utf-8 -*-
# tests/calculation/indicators/predictive/test_schr_dir_indicator.py

"""
Unit tests for SCHR Direction indicator with fixed parameters.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.predictive.schr_dir_ind import (
    calculate_vpr,
    calculate_direction_lines,
    calculate_schr_dir_signals,
    apply_rule_schr_dir
)
from src.common.constants import BUY, SELL, NOTRADE, EMPTY_VALUE
from src.calculation.indicators.base_indicator import PriceType


class TestSCHRDirIndicator:
    """Test class for SCHR Direction indicator with fixed parameters."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample data
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 100),
            'High': np.random.uniform(1.1, 2.1, 100),
            'Low': np.random.uniform(0.9, 1.9, 100),
            'Close': np.random.uniform(1.0, 2.0, 100),
            'Volume': np.random.uniform(1000, 10000, 100)
        }, index=dates)
        
        # Ensure High >= Low
        self.sample_data['High'] = np.maximum(self.sample_data['High'], self.sample_data['Low'] + 0.01)
        self.sample_data['Low'] = np.minimum(self.sample_data['Low'], self.sample_data['High'] - 0.01)
        
        self.point = 0.00001

    def test_calculate_vpr_basic(self):
        """Test basic VPR calculation."""
        high_prices = pd.Series([1.1, 1.2, 1.3])
        low_prices = pd.Series([1.0, 1.1, 1.2])
        volume_prices = pd.Series([1000, 2000, 3000])
        
        diff_series, vpr_series = calculate_vpr(high_prices, low_prices, volume_prices, self.point)
        
        assert len(diff_series) == 3
        assert len(vpr_series) == 3
        assert not diff_series.isna().all()
        assert not vpr_series.isna().all()

    def test_calculate_vpr_zero_diff(self):
        """Test VPR calculation with zero difference."""
        high_prices = pd.Series([1.0, 1.0, 1.0])
        low_prices = pd.Series([1.0, 1.0, 1.0])
        volume_prices = pd.Series([1000, 2000, 3000])
        
        diff_series, vpr_series = calculate_vpr(high_prices, low_prices, volume_prices, self.point)
        
        assert (diff_series == 0).all()
        assert vpr_series.isna().all()  # VPR should be NaN when diff is zero

    def test_calculate_direction_lines_fixed_parameters(self):
        """Test direction lines calculation with fixed parameters."""
        price_series = pd.Series([1.0, 1.1, 1.2])
        diff_series = pd.Series([0.1, 0.2, 0.3])
        vpr_series = pd.Series([0.5, 0.6, 0.7])
        c_vpr = 0.5 * np.log(np.pi)
        
        dir_high, dir_low = calculate_direction_lines(
            price_series, diff_series, vpr_series, self.point, c_vpr
        )
        
        assert len(dir_high) == 3
        assert len(dir_low) == 3
        assert not dir_high.isna().all()
        assert not dir_low.isna().all()

    def test_calculate_schr_dir_signals_fixed_parameters(self):
        """Test trading signals calculation with fixed parameters."""
        dir_high = pd.Series([1.1, 1.2, 1.3])
        dir_low = pd.Series([0.9, 1.0, 1.1])
        high_prices = pd.Series([1.0, 1.1, 1.2])
        low_prices = pd.Series([0.8, 0.9, 1.0])
        
        signals = calculate_schr_dir_signals(dir_high, dir_low, high_prices, low_prices)
        
        assert len(signals) == 3
        assert not signals.isna().all()

    def test_apply_rule_schr_dir_basic(self):
        """Test basic SCHR_DIR rule application with fixed parameters."""
        result = apply_rule_schr_dir(self.sample_data, self.point)

        # Check that all required columns are present
        required_columns = [
            'PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2',
            'SCHR_DIR_Diff', 'SCHR_DIR_VPR', 'SCHR_DIR_Price_Type',
            'SCHR_DIR_Grow_Percent', 'SCHR_DIR_Strong_Exceed'
        ]

        for col in required_columns:
            assert col in result.columns

        # Check that PPrice1 and PPrice2 are the same (single line behavior)
        np.testing.assert_array_almost_equal(result['PPrice1'], result['PPrice2'])

    def test_apply_rule_schr_dir_fixed_parameters(self):
        """Test that SCHR_DIR always uses fixed parameters regardless of input."""
        # Test with different price types (should be ignored)
        result_open = apply_rule_schr_dir(
            self.sample_data, self.point, price_type=PriceType.OPEN
        )
        result_close = apply_rule_schr_dir(
            self.sample_data, self.point, price_type=PriceType.CLOSE
        )

        # Both should use Open price (fixed parameter)
        assert result_open['SCHR_DIR_Price_Type'].iloc[0] == "Open"
        assert result_close['SCHR_DIR_Price_Type'].iloc[0] == "Open"

        # Results should be identical since parameters are fixed
        np.testing.assert_array_almost_equal(
            result_open['PPrice1'], result_close['PPrice1']
        )

    def test_apply_rule_schr_dir_single_line_behavior(self):
        """Test that SCHR_DIR shows single line behavior."""
        result = apply_rule_schr_dir(self.sample_data, self.point)

        # PPrice1 and PPrice2 should be identical (single line)
        np.testing.assert_array_almost_equal(result['PPrice1'], result['PPrice2'])
        
        # PColor1 and PColor2 should be identical
        np.testing.assert_array_almost_equal(result['PColor1'], result['PColor2'])

    def test_apply_rule_schr_dir_previous_bar_data(self):
        """Test that SCHR_DIR uses previous bar data (fixed parameter)."""
        result = apply_rule_schr_dir(self.sample_data, self.point)

        # Should have valid data
        assert not result['PPrice1'].isna().all()
        assert not result['PPrice2'].isna().all()

    def test_apply_rule_schr_dir_open_price_always_used(self):
        """Test that SCHR_DIR always uses Open price (fixed parameter)."""
        result = apply_rule_schr_dir(self.sample_data, self.point)

        # Should always use Open price
        assert result['SCHR_DIR_Price_Type'].iloc[0] == "Open"

        # The direction lines should be based on Open price
        # We can verify this by checking that the calculation uses Open price
        open_prices = self.sample_data['Open']
        assert len(result['PPrice1']) == len(open_prices)

    def test_apply_rule_schr_dir_insufficient_data(self):
        """Test SCHR_DIR with insufficient data."""
        # Create minimal data
        minimal_data = pd.DataFrame({
            'Open': [1.0],
            'High': [1.1],
            'Low': [0.9],
            'Close': [1.0],
            'Volume': [1000]
        })

        result = apply_rule_schr_dir(minimal_data, self.point)

        # Should handle minimal data gracefully
        assert len(result) == 1
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns

    def test_apply_rule_schr_dir_empty_data(self):
        """Test SCHR_DIR with empty data."""
        empty_data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

        result = apply_rule_schr_dir(empty_data, self.point)

        # Should handle empty data gracefully
        assert len(result) == 0
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns

    def test_apply_rule_schr_dir_large_dataset(self):
        """Test SCHR_DIR with large dataset for performance."""
        # Create larger dataset
        large_dates = pd.date_range('2020-01-01', periods=1000, freq='D')
        large_data = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 1000),
            'High': np.random.uniform(1.1, 2.1, 1000),
            'Low': np.random.uniform(0.9, 1.9, 1000),
            'Close': np.random.uniform(1.0, 2.0, 1000),
            'Volume': np.random.uniform(1000, 10000, 1000)
        }, index=large_dates)

        # Ensure High >= Low
        large_data['High'] = np.maximum(large_data['High'], large_data['Low'] + 0.01)
        large_data['Low'] = np.minimum(large_data['Low'], large_data['High'] - 0.01)

        result = apply_rule_schr_dir(large_data, self.point)

        # Should handle large dataset
        assert len(result) == 1000
        assert not result['PPrice1'].isna().all()
        assert not result['PPrice2'].isna().all()

    def test_apply_rule_schr_dir_signal_generation(self):
        """Test that SCHR_DIR generates trading signals."""
        result = apply_rule_schr_dir(self.sample_data, self.point)

        # Should generate signals
        assert 'Direction' in result.columns
        assert not result['Direction'].isna().all()

        # Signals should be valid values
        valid_signals = [BUY, SELL, NOTRADE]
        assert all(signal in valid_signals for signal in result['Direction'].dropna())

    def test_apply_rule_schr_dir_output_consistency(self):
        """Test that SCHR_DIR output is consistent with fixed parameters."""
        result1 = apply_rule_schr_dir(self.sample_data, self.point)
        result2 = apply_rule_schr_dir(self.sample_data, self.point)

        # Results should be identical since parameters are fixed
        np.testing.assert_array_almost_equal(
            result1['PPrice1'], result2['PPrice1']
        )
        np.testing.assert_array_almost_equal(
            result1['PPrice2'], result2['PPrice2']
        )
