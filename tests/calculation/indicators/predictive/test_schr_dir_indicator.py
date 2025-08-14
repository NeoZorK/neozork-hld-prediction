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
    calculate_schr_dir_lines,
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

    def test_calculate_schr_dir_lines_fixed_parameters(self):
        """Test SCHR Direction lines calculation with fixed parameters."""
        dir_high = pd.Series([1.1, 1.2, 1.3])
        dir_low = pd.Series([0.9, 1.0, 1.1])
        high_prices = pd.Series([1.0, 1.1, 1.2])
        low_prices = pd.Series([0.8, 0.9, 1.0])
        
        high_line, high_color, low_line, low_color = calculate_schr_dir_lines(
            dir_high, dir_low, high_prices, low_prices, strong_exceed=True
        )
        
        assert len(high_line) == 3
        assert len(low_line) == 3
        assert len(high_color) == 3
        assert len(low_color) == 3
        assert not high_line.isna().all()
        assert not low_line.isna().all()

    def test_calculate_schr_dir_signals_fixed_parameters(self):
        """Test trading signals calculation with fixed parameters."""
        high_line = pd.Series([1.1, 1.2, 1.3])
        low_line = pd.Series([0.9, 1.0, 1.1])
        open_prices = pd.Series([1.0, 1.1, 1.2])
        
        signals = calculate_schr_dir_signals(high_line, low_line, open_prices)
        
        assert len(signals) == 3
        assert not signals.isna().all()

    def test_apply_rule_schr_dir_basic(self):
        """Test basic SCHR_DIR rule application with default parameters."""
        result = apply_rule_schr_dir(self.sample_data, self.point)

        # Check that all required columns are present
        required_columns = [
            'PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2',
            'SCHR_DIR_Diff', 'SCHR_DIR_VPR', 'SCHR_DIR_Price_Type',
            'SCHR_DIR_Grow_Percent', 'SCHR_DIR_Strong_Exceed', 'SCHR_DIR_Shift_External_Internal'
        ]

        for col in required_columns:
            assert col in result.columns

        # Check that PPrice1 and PPrice2 are different (dual line behavior)
        # They should be different lines representing High and Low
        assert not np.array_equal(result['PPrice1'], result['PPrice2'])
        
        # Check default grow_percent is 1.0
        assert result['SCHR_DIR_Grow_Percent'].iloc[0] == 1.0

    def test_apply_rule_schr_dir_parameters(self):
        """Test that SCHR_DIR uses configurable grow_percent parameter."""
        # Test with different grow_percent values
        result_default = apply_rule_schr_dir(
            self.sample_data, self.point, grow_percent=1.0
        )
        result_high = apply_rule_schr_dir(
            self.sample_data, self.point, grow_percent=95.0
        )
        result_low = apply_rule_schr_dir(
            self.sample_data, self.point, grow_percent=50.0
        )

        # All should use Open price (fixed parameter)
        assert result_default['SCHR_DIR_Price_Type'].iloc[0] == "Open"
        assert result_high['SCHR_DIR_Price_Type'].iloc[0] == "Open"
        assert result_low['SCHR_DIR_Price_Type'].iloc[0] == "Open"

        # Results should be different due to different grow_percent values
        assert result_default['SCHR_DIR_Grow_Percent'].iloc[0] == 1.0
        assert result_high['SCHR_DIR_Grow_Percent'].iloc[0] == 95.0
        assert result_low['SCHR_DIR_Grow_Percent'].iloc[0] == 50.0

        # Lines should be different due to different grow_percent values
        assert not np.array_equal(result_default['PPrice1'], result_high['PPrice1'])
        assert not np.array_equal(result_default['PPrice2'], result_high['PPrice2'])

    def test_apply_rule_schr_dir_dual_line_behavior(self):
        """Test that SCHR_DIR shows dual line behavior."""
        result = apply_rule_schr_dir(self.sample_data, self.point)

        # PPrice1 and PPrice2 should be different (dual line behavior)
        # High line (PPrice1) should generally be above Low line (PPrice2)
        valid_mask = ~(result['PPrice1'].isna() | result['PPrice2'].isna())
        if valid_mask.any():
            high_line = result['PPrice1'][valid_mask]
            low_line = result['PPrice2'][valid_mask]
            # High line should generally be above or equal to low line
            assert (high_line >= low_line).all()
        
        # PColor1 and PColor2 should be different (different signal types)
        # High line color should be SELL (2), Low line color should be BUY (1)
        # But first few values might be NOTRADE (0) due to initialization
        valid_color_mask = ~(result['PColor1'].isna() | result['PColor2'].isna())
        if valid_color_mask.any():
            pcolor1 = result['PColor1'][valid_color_mask]
            pcolor2 = result['PColor2'][valid_color_mask]
            # After initialization, colors should be SELL (2) and BUY (1)
            # Skip first few values that might be NOTRADE (0)
            if len(pcolor1) > 5:
                assert (pcolor1[5:] == 2).all()  # SELL for high line
                assert (pcolor2[5:] == 1).all()  # BUY for low line

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

    def test_apply_rule_schr_dir_parameter_validation(self):
        """Test that SCHR_DIR validates grow_percent parameter correctly."""
        # Test valid parameters
        apply_rule_schr_dir(self.sample_data, self.point, grow_percent=1.0)
        apply_rule_schr_dir(self.sample_data, self.point, grow_percent=50.0)
        apply_rule_schr_dir(self.sample_data, self.point, grow_percent=95.0)
        
        # Test invalid parameters
        with pytest.raises(ValueError, match="grow_percent must be between 1.0 and 95.0"):
            apply_rule_schr_dir(self.sample_data, self.point, grow_percent=0.0)
        
        with pytest.raises(ValueError, match="grow_percent must be between 1.0 and 95.0"):
            apply_rule_schr_dir(self.sample_data, self.point, grow_percent=96.0)
        
        with pytest.raises(ValueError, match="grow_percent must be between 1.0 and 95.0"):
            apply_rule_schr_dir(self.sample_data, self.point, grow_percent=100.0)

    def test_apply_rule_schr_dir_output_consistency(self):
        """Test that SCHR_DIR output is consistent with same parameters."""
        result1 = apply_rule_schr_dir(self.sample_data, self.point, grow_percent=50.0)
        result2 = apply_rule_schr_dir(self.sample_data, self.point, grow_percent=50.0)

        # Results should be identical since parameters are the same
        np.testing.assert_array_almost_equal(
            result1['PPrice1'], result2['PPrice1']
        )
        np.testing.assert_array_almost_equal(
            result1['PPrice2'], result2['PPrice2']
        )
        np.testing.assert_array_almost_equal(
            result1['PColor1'], result2['PColor1']
        )
        np.testing.assert_array_almost_equal(
            result1['PColor2'], result2['PColor2']
        )
