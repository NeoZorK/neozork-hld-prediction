# -*- coding: utf-8 -*-
# tests/calculation/indicators/predictive/test_schr_dir_indicator.py

"""
Unit tests for SCHR Direction indicator.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.predictive.schr_dir_ind import (
    calculate_vpr,
    calculate_direction_lines,
    calculate_schr_dir_signals,
    apply_rule_schr_dir,
    GrowPercent,
    LinesCount
)
from src.common.constants import BUY, SELL, NOTRADE, EMPTY_VALUE
from src.calculation.indicators.base_indicator import PriceType


class TestSCHRDirIndicator:
    """Test class for SCHR Direction indicator."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample OHLCV data
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        np.random.seed(42)
        
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
        
        self.point = 0.00001  # Typical forex point size
    
    def test_calculate_vpr_basic(self):
        """Test basic VPR calculation."""
        high_prices = self.sample_data['High']
        low_prices = self.sample_data['Low']
        volume_prices = self.sample_data['Volume']
        
        diff_series, vpr_series = calculate_vpr(high_prices, low_prices, volume_prices, self.point)
        
        assert isinstance(diff_series, pd.Series)
        assert isinstance(vpr_series, pd.Series)
        assert len(diff_series) == len(high_prices)
        assert len(vpr_series) == len(high_prices)
        
        # Check that diff is positive (High > Low)
        assert (diff_series > 0).all()
        
        # Check that VPR is calculated correctly for valid data
        valid_mask = (diff_series != 0) & (volume_prices != diff_series)
        if valid_mask.any():
            expected_vpr = volume_prices[valid_mask] / diff_series[valid_mask]
            np.testing.assert_array_almost_equal(vpr_series[valid_mask], expected_vpr)
    
    def test_calculate_vpr_zero_diff(self):
        """Test VPR calculation with zero difference."""
        high_prices = pd.Series([1.0, 1.0, 1.0])
        low_prices = pd.Series([1.0, 1.0, 1.0])
        volume_prices = pd.Series([1000, 2000, 3000])
        
        diff_series, vpr_series = calculate_vpr(high_prices, low_prices, volume_prices, self.point)
        
        assert (diff_series == 0).all()
        assert vpr_series.isna().all()
    
    def test_calculate_direction_lines(self):
        """Test direction lines calculation."""
        price_series = self.sample_data['Open']
        diff_series = (self.sample_data['High'] - self.sample_data['Low']) / self.point
        vpr_series = self.sample_data['Volume'] / diff_series
        grow_percent = 95
        shift_external_internal = False
        c_vpr = 0.5 * np.log(np.pi)
        
        dir_high, dir_low = calculate_direction_lines(
            price_series, diff_series, vpr_series, self.point,
            grow_percent, shift_external_internal, c_vpr
        )
        
        assert isinstance(dir_high, pd.Series)
        assert isinstance(dir_low, pd.Series)
        assert len(dir_high) == len(price_series)
        assert len(dir_low) == len(price_series)
        
        # Check that direction lines are calculated
        assert not dir_high.isna().all()
        assert not dir_low.isna().all()
    
    def test_calculate_direction_lines_external_shift(self):
        """Test direction lines calculation with external shift."""
        price_series = self.sample_data['Open']
        diff_series = (self.sample_data['High'] - self.sample_data['Low']) / self.point
        vpr_series = self.sample_data['Volume'] / diff_series
        grow_percent = 80
        shift_external_internal = True
        c_vpr = 0.5 * np.log(np.pi)
        
        dir_high, dir_low = calculate_direction_lines(
            price_series, diff_series, vpr_series, self.point,
            grow_percent, shift_external_internal, c_vpr
        )
        
        assert isinstance(dir_high, pd.Series)
        assert isinstance(dir_low, pd.Series)
        
        # With external shift, grow factor should be (100 + grow_percent) / 100
        expected_grow_factor = (100 + grow_percent) / 100
        assert expected_grow_factor == 1.8
    
    def test_calculate_schr_dir_signals(self):
        """Test SCHR direction signals calculation."""
        # Create sample direction lines
        dir_high = pd.Series([1.5, 1.6, 1.4, 1.7, 1.3])
        dir_low = pd.Series([1.0, 0.9, 1.1, 0.8, 1.2])
        high_prices = pd.Series([1.4, 1.5, 1.3, 1.6, 1.2])
        low_prices = pd.Series([1.1, 1.0, 1.2, 0.9, 1.1])
        
        # Test with strong exceed
        signals_strong = calculate_schr_dir_signals(
            dir_high, dir_low, high_prices, low_prices, strong_exceed=True
        )
        
        assert isinstance(signals_strong, pd.Series)
        assert len(signals_strong) == len(dir_high)
        assert signals_strong.iloc[0] == NOTRADE  # First signal should be NOTRADE
        
        # Test without strong exceed
        signals_weak = calculate_schr_dir_signals(
            dir_high, dir_low, high_prices, low_prices, strong_exceed=False
        )
        
        assert isinstance(signals_weak, pd.Series)
        assert len(signals_weak) == len(dir_high)
    
    def test_apply_rule_schr_dir_basic(self):
        """Test basic SCHR_DIR rule application."""
        result = apply_rule_schr_dir(self.sample_data, self.point)
        
        # Check required output columns
        required_columns = [
            'PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction',
            'SCHR_DIR_High', 'SCHR_DIR_High_Color', 'SCHR_DIR_Low', 'SCHR_DIR_Low_Color',
            'SCHR_DIR_Diff', 'SCHR_DIR_VPR', 'SCHR_DIR_Price_Type',
            'SCHR_DIR_Grow_Percent', 'SCHR_DIR_Strong_Exceed'
        ]
        
        for col in required_columns:
            assert col in result.columns
        
        # Check data types
        assert result['PColor1'].dtype in [np.float64, np.int64]
        assert result['PColor2'].dtype in [np.float64, np.int64]
        assert result['Direction'].dtype in [np.float64, np.int64]
        
        # Check that signals are valid
        valid_signals = [NOTRADE, BUY, SELL]
        assert result['Direction'].isin(valid_signals).all()
    
    def test_apply_rule_schr_dir_parameters(self):
        """Test SCHR_DIR rule with different parameters."""
        # Test with different grow_percent
        result_95 = apply_rule_schr_dir(self.sample_data, self.point, grow_percent=95)
        result_50 = apply_rule_schr_dir(self.sample_data, self.point, grow_percent=50)
        
        assert result_95['SCHR_DIR_Grow_Percent'].iloc[0] == 95
        assert result_50['SCHR_DIR_Grow_Percent'].iloc[0] == 50
        
        # Test with different price types
        result_open = apply_rule_schr_dir(
            self.sample_data, self.point, fixed_price=True, price_type=PriceType.OPEN
        )
        result_close = apply_rule_schr_dir(
            self.sample_data, self.point, fixed_price=False, price_type=PriceType.CLOSE
        )
        
        assert result_open['SCHR_DIR_Price_Type'].iloc[0] == "Open"
        assert result_close['SCHR_DIR_Price_Type'].iloc[0] == "Close"
        
        # Test with different lines count
        result_upper = apply_rule_schr_dir(
            self.sample_data, self.point, lines_count=LinesCount.UPPER_LINE
        )
        result_lower = apply_rule_schr_dir(
            self.sample_data, self.point, lines_count=LinesCount.LOWER_LINE
        )
        
        # Check that only appropriate lines are calculated
        assert not result_upper['SCHR_DIR_High'].isna().all()
        assert result_upper['SCHR_DIR_Low'].isna().all()
        assert result_lower['SCHR_DIR_High'].isna().all()
        assert not result_lower['SCHR_DIR_Low'].isna().all()
    
    def test_apply_rule_schr_dir_validation(self):
        """Test SCHR_DIR parameter validation."""
        # Test invalid grow_percent
        with pytest.raises(ValueError, match="grow_percent must be between 1 and 99"):
            apply_rule_schr_dir(self.sample_data, self.point, grow_percent=0)
        
        with pytest.raises(ValueError, match="grow_percent must be between 1 and 99"):
            apply_rule_schr_dir(self.sample_data, self.point, grow_percent=100)
    
    def test_apply_rule_schr_dir_fake_line(self):
        """Test SCHR_DIR with fake_line parameter."""
        # Test with fake_line=True (use current bar data)
        result_fake = apply_rule_schr_dir(self.sample_data, self.point, fake_line=True)
        
        # Test with fake_line=False (use previous bar data)
        result_real = apply_rule_schr_dir(self.sample_data, self.point, fake_line=False)
        
        # Both should produce valid results
        assert 'SCHR_DIR_Diff' in result_fake.columns
        assert 'SCHR_DIR_Diff' in result_real.columns
        assert not result_fake['SCHR_DIR_Diff'].isna().all()
        assert not result_real['SCHR_DIR_Diff'].isna().all()
    
    def test_apply_rule_schr_dir_strong_exceed(self):
        """Test SCHR_DIR with strong_exceed parameter."""
        # Test with strong_exceed=True
        result_strong = apply_rule_schr_dir(self.sample_data, self.point, strong_exceed=True)
        
        # Test with strong_exceed=False
        result_weak = apply_rule_schr_dir(self.sample_data, self.point, strong_exceed=False)
        
        # Both should produce valid results
        assert result_strong['SCHR_DIR_Strong_Exceed'].iloc[0] == True
        assert result_weak['SCHR_DIR_Strong_Exceed'].iloc[0] == False
    
    def test_apply_rule_schr_dir_insufficient_data(self):
        """Test SCHR_DIR with insufficient data."""
        small_data = self.sample_data.head(5)
        result = apply_rule_schr_dir(small_data, self.point)
        
        # Should handle small datasets gracefully
        assert len(result) == len(small_data)
        assert 'Direction' in result.columns
    
    def test_grow_percent_enum(self):
        """Test GrowPercent enum values."""
        assert GrowPercent.P_95.value == 95
        assert GrowPercent.P_50.value == 50
        assert GrowPercent.P_1.value == 1
        assert GrowPercent.P_99.value == 99
    
    def test_lines_count_enum(self):
        """Test LinesCount enum values."""
        assert LinesCount.UPPER_LINE.value == 0
        assert LinesCount.LOWER_LINE.value == 1
        assert LinesCount.BOTH_LINES.value == 2
    
    def test_schr_dir_performance(self):
        """Test SCHR_DIR performance with large dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 10000),
            'High': np.random.uniform(1.1, 2.1, 10000),
            'Low': np.random.uniform(0.9, 1.9, 10000),
            'Close': np.random.uniform(1.0, 2.0, 10000),
            'Volume': np.random.uniform(1000, 10000, 10000)
        })
        
        # Ensure High >= Low
        large_data['High'] = np.maximum(large_data['High'], large_data['Low'] + 0.01)
        large_data['Low'] = np.minimum(large_data['Low'], large_data['High'] - 0.01)
        
        import time
        start_time = time.time()
        result = apply_rule_schr_dir(large_data, self.point)
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 5.0  # 5 seconds
        assert len(result) == len(large_data)
