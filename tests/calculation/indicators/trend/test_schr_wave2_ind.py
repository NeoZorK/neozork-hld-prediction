# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_schr_wave2_ind.py

"""
Test SCHR_Wave2 indicator calculation module.
Tests all functions and edge cases for 100% coverage.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.trend.schr_wave2_ind import (
    SCHRWave2Indicator, calculate_schr_wave2, calculate_ecore,
    calculate_draw_lines, apply_trading_rule, apply_global_trading_rule,
    calculate_sma, get_trading_rule_enum, get_global_trading_rule_enum,
    TradingRuleEnum, GlobalTradingRuleEnum, apply_rule_schr_wave2
)
from src.common.constants import NOTRADE, BUY, SELL


class TestTradingRuleEnum:
    """Test TradingRuleEnum class."""
    
    def test_trading_rule_enum_values(self):
        """Test that all trading rule enum values are defined."""
        assert TradingRuleEnum.TR_FAST == 0
        assert TradingRuleEnum.TR_ZONE == 1
        assert TradingRuleEnum.TR_STRONG_TREND == 2
        assert TradingRuleEnum.TR_WEAK_TREND == 3
        assert TradingRuleEnum.TR_FAST_ZONE_REVERSE == 4
        assert TradingRuleEnum.TR_BETTER_TREND == 5
        assert TradingRuleEnum.TR_BETTER_FAST == 6
        assert TradingRuleEnum.TR_ROST == 7
        assert TradingRuleEnum.TR_TREND_ROST == 8
        assert TradingRuleEnum.TR_BETTER_TREND_ROST == 9


class TestGlobalTradingRuleEnum:
    """Test GlobalTradingRuleEnum class."""
    
    def test_global_trading_rule_enum_values(self):
        """Test that all global trading rule enum values are defined."""
        assert GlobalTradingRuleEnum.G_TR_PRIME == 0
        assert GlobalTradingRuleEnum.G_TR_REVERSE == 1
        assert GlobalTradingRuleEnum.G_TR_PRIME_ZONE == 2
        assert GlobalTradingRuleEnum.G_TR_REVERSE_ZONE == 3
        assert GlobalTradingRuleEnum.G_TR_NEW_ZONE == 4
        assert GlobalTradingRuleEnum.G_TR_LONG_ZONE == 5
        assert GlobalTradingRuleEnum.G_TR_LONG_ZONE_REVERSE == 6


class TestGetTradingRuleEnum:
    """Test get_trading_rule_enum function."""
    
    def test_get_trading_rule_enum_with_int(self):
        """Test get_trading_rule_enum with integer input."""
        assert get_trading_rule_enum(0) == TradingRuleEnum.TR_FAST
        assert get_trading_rule_enum(1) == TradingRuleEnum.TR_ZONE
        assert get_trading_rule_enum(2) == TradingRuleEnum.TR_STRONG_TREND
    
    def test_get_trading_rule_enum_with_string(self):
        """Test get_trading_rule_enum with string input."""
        assert get_trading_rule_enum('fast') == TradingRuleEnum.TR_FAST
        assert get_trading_rule_enum('zone') == TradingRuleEnum.TR_ZONE
        assert get_trading_rule_enum('strongtrend') == TradingRuleEnum.TR_STRONG_TREND
        assert get_trading_rule_enum('weaktrend') == TradingRuleEnum.TR_WEAK_TREND
        assert get_trading_rule_enum('fastzonereverse') == TradingRuleEnum.TR_FAST_ZONE_REVERSE
        assert get_trading_rule_enum('bettertrend') == TradingRuleEnum.TR_BETTER_TREND
        assert get_trading_rule_enum('betterfast') == TradingRuleEnum.TR_BETTER_FAST
        assert get_trading_rule_enum('rost') == TradingRuleEnum.TR_ROST
        assert get_trading_rule_enum('trendrost') == TradingRuleEnum.TR_TREND_ROST
        assert get_trading_rule_enum('bettertrendrost') == TradingRuleEnum.TR_BETTER_TREND_ROST
    
    def test_get_trading_rule_enum_with_unknown_string(self):
        """Test get_trading_rule_enum with unknown string input."""
        assert get_trading_rule_enum('unknown') == TradingRuleEnum.TR_FAST
    
    def test_get_trading_rule_enum_case_insensitive(self):
        """Test get_trading_rule_enum is case insensitive."""
        assert get_trading_rule_enum('FAST') == TradingRuleEnum.TR_FAST
        assert get_trading_rule_enum('Zone') == TradingRuleEnum.TR_ZONE
        assert get_trading_rule_enum('StrongTrend') == TradingRuleEnum.TR_STRONG_TREND


class TestGetGlobalTradingRuleEnum:
    """Test get_global_trading_rule_enum function."""
    
    def test_get_global_trading_rule_enum_with_int(self):
        """Test get_global_trading_rule_enum with integer input."""
        assert get_global_trading_rule_enum(0) == GlobalTradingRuleEnum.G_TR_PRIME
        assert get_global_trading_rule_enum(1) == GlobalTradingRuleEnum.G_TR_REVERSE
        assert get_global_trading_rule_enum(2) == GlobalTradingRuleEnum.G_TR_PRIME_ZONE
    
    def test_get_global_trading_rule_enum_with_string(self):
        """Test get_global_trading_rule_enum with string input."""
        assert get_global_trading_rule_enum('prime') == GlobalTradingRuleEnum.G_TR_PRIME
        assert get_global_trading_rule_enum('reverse') == GlobalTradingRuleEnum.G_TR_REVERSE
        assert get_global_trading_rule_enum('primezone') == GlobalTradingRuleEnum.G_TR_PRIME_ZONE
        assert get_global_trading_rule_enum('reversezone') == GlobalTradingRuleEnum.G_TR_REVERSE_ZONE
        assert get_global_trading_rule_enum('newzone') == GlobalTradingRuleEnum.G_TR_NEW_ZONE
        assert get_global_trading_rule_enum('longzone') == GlobalTradingRuleEnum.G_TR_LONG_ZONE
        assert get_global_trading_rule_enum('longzonereverse') == GlobalTradingRuleEnum.G_TR_LONG_ZONE_REVERSE
    
    def test_get_global_trading_rule_enum_with_unknown_string(self):
        """Test get_global_trading_rule_enum with unknown string input."""
        assert get_global_trading_rule_enum('unknown') == GlobalTradingRuleEnum.G_TR_PRIME
    
    def test_get_global_trading_rule_enum_case_insensitive(self):
        """Test get_global_trading_rule_enum is case insensitive."""
        assert get_global_trading_rule_enum('PRIME') == GlobalTradingRuleEnum.G_TR_PRIME
        assert get_global_trading_rule_enum('Reverse') == GlobalTradingRuleEnum.G_TR_REVERSE
        assert get_global_trading_rule_enum('PrimeZone') == GlobalTradingRuleEnum.G_TR_PRIME_ZONE


class TestCalculateEcore:
    """Test calculate_ecore function."""
    
    def test_calculate_ecore_empty_data(self):
        """Test calculate_ecore with empty data."""
        open_prices = pd.Series([], dtype=float)
        div = 0.1
        result = calculate_ecore(open_prices, div)
        assert len(result) == 0
    
    def test_calculate_ecore_single_value(self):
        """Test calculate_ecore with single value."""
        open_prices = pd.Series([100.0])
        div = 0.1
        result = calculate_ecore(open_prices, div)
        assert len(result) == 1
        assert result.iloc[0] == 0.0
    
    def test_calculate_ecore_two_values(self):
        """Test calculate_ecore with two values."""
        open_prices = pd.Series([100.0, 101.0])
        div = 0.1
        result = calculate_ecore(open_prices, div)
        assert len(result) == 2
        assert result.iloc[0] == 0.0
        # Use approximate comparison for float precision
        assert abs(result.iloc[1] - 0.1) < 1e-10
    
    def test_calculate_ecore_multiple_values(self):
        """Test calculate_ecore with multiple values."""
        open_prices = pd.Series([100.0, 101.0, 99.0, 102.0])
        div = 0.2
        result = calculate_ecore(open_prices, div)
        assert len(result) == 4
        assert result.iloc[0] == 0.0
        # Use approximate comparison for float precision
        assert abs(result.iloc[1] - 0.2) < 1e-10
        # Calculate expected values with approximate comparison
        # For the third value: previous (0.2) + div * (diff - previous)
        # diff = (99.0/101.0 - 1) * 100 = -1.9801980198019802
        # expected = 0.2 + 0.2 * (-1.9801980198019802 - 0.2) = 0.2 + 0.2 * (-2.1801980198019802) = 0.2 - 0.43603960396039604 = -0.23603960396039604
        expected_ecore2 = 0.2 + 0.2 * (-1.9801980198019802 - 0.2)
        assert abs(result.iloc[2] - expected_ecore2) < 1e-10
        # For the fourth value: previous + div * (diff - previous)
        # diff = (102.0/99.0 - 1) * 100 = 3.0303030303030303
        expected_ecore3 = result.iloc[2] + 0.2 * (3.0303030303030303 - result.iloc[2])
        assert abs(result.iloc[3] - expected_ecore3) < 1e-10
    
    def test_calculate_ecore_zero_division(self):
        """Test calculate_ecore with zero division factor."""
        open_prices = pd.Series([100.0, 101.0])
        div = 0.0
        result = calculate_ecore(open_prices, div)
        assert len(result) == 2
        assert result.iloc[0] == 0.0
        assert result.iloc[1] == 0.0  # No change due to zero div


class TestCalculateDrawLines:
    """Test calculate_draw_lines function."""
    
    def test_calculate_draw_lines_empty_data(self):
        """Test calculate_draw_lines with empty data."""
        ecore = pd.Series([], dtype=float)
        div_fast = 0.1
        div_dir = 0.05
        wave, fast_line = calculate_draw_lines(ecore, div_fast, div_dir)
        assert len(wave) == 0
        assert len(fast_line) == 0
    
    def test_calculate_draw_lines_single_value(self):
        """Test calculate_draw_lines with single value."""
        ecore = pd.Series([0.5])
        div_fast = 0.1
        div_dir = 0.05
        wave, fast_line = calculate_draw_lines(ecore, div_fast, div_dir)
        assert len(wave) == 1
        assert len(fast_line) == 1
        assert wave.iloc[0] == 0.0
        assert fast_line.iloc[0] == 0.0
    
    def test_calculate_draw_lines_multiple_values(self):
        """Test calculate_draw_lines with multiple values."""
        ecore = pd.Series([0.5, 1.0, -0.5, 0.8])
        div_fast = 0.2
        div_dir = 0.1
        wave, fast_line = calculate_draw_lines(ecore, div_fast, div_dir)
        assert len(wave) == 4
        assert len(fast_line) == 4
        
        # First values
        assert wave.iloc[0] == 0.0
        assert fast_line.iloc[0] == 0.0
        
        # Second values - use approximate comparison
        expected_wave1 = 0.0 + 0.2 * (1.0 - 0.0)  # 0.2
        expected_fast1 = 0.0 + 0.1 * (0.2 - 0.0)  # 0.02
        assert abs(wave.iloc[1] - expected_wave1) < 1e-10
        assert abs(fast_line.iloc[1] - expected_fast1) < 1e-10


class TestApplyTradingRule:
    """Test apply_trading_rule function."""
    
    def test_apply_trading_rule_empty_data(self):
        """Test apply_trading_rule with empty data."""
        wave = pd.Series([], dtype=float)
        fast_line = pd.Series([], dtype=float)
        tr_enum = TradingRuleEnum.TR_FAST
        result = apply_trading_rule(wave, fast_line, tr_enum)
        assert len(result) == 0
    
    def test_apply_trading_rule_single_value(self):
        """Test apply_trading_rule with single value."""
        wave = pd.Series([0.5])
        fast_line = pd.Series([0.2])
        tr_enum = TradingRuleEnum.TR_FAST
        result = apply_trading_rule(wave, fast_line, tr_enum)
        assert len(result) == 1
        assert result.iloc[0] == NOTRADE  # First value is always NOTRADE
    
    def test_apply_trading_rule_fast_rule(self):
        """Test apply_trading_rule with Fast rule."""
        wave = pd.Series([0.0, 0.5, -0.3, 0.8])
        fast_line = pd.Series([0.0, 0.2, 0.1, 0.6])
        tr_enum = TradingRuleEnum.TR_FAST
        result = apply_trading_rule(wave, fast_line, tr_enum)
        assert len(result) == 4
        assert result.iloc[0] == NOTRADE  # First value
        assert result.iloc[1] == BUY      # 0.5 > 0.2
        assert result.iloc[2] == SELL     # -0.3 < 0.1
        assert result.iloc[3] == BUY      # 0.8 > 0.6
    
    def test_apply_trading_rule_zone_rule(self):
        """Test apply_trading_rule with Zone rule."""
        wave = pd.Series([0.0, 0.5, -0.3, 0.8])
        fast_line = pd.Series([0.0, 0.2, 0.1, 0.6])
        tr_enum = TradingRuleEnum.TR_ZONE
        result = apply_trading_rule(wave, fast_line, tr_enum)
        assert len(result) == 4
        assert result.iloc[0] == NOTRADE  # First value
        assert result.iloc[1] == BUY      # 0.5 > 0
        assert result.iloc[2] == SELL     # -0.3 < 0
        assert result.iloc[3] == BUY      # 0.8 > 0
    
    def test_apply_trading_rule_strong_trend_rule(self):
        """Test apply_trading_rule with StrongTrend rule."""
        wave = pd.Series([0.0, 0.5, -0.3, 0.8])
        fast_line = pd.Series([0.0, 0.2, 0.1, 0.6])
        tr_enum = TradingRuleEnum.TR_STRONG_TREND
        result = apply_trading_rule(wave, fast_line, tr_enum)
        assert len(result) == 4
        assert result.iloc[0] == NOTRADE  # First value
        assert result.iloc[1] == BUY      # Plus zone, Wave > FastLine
        assert result.iloc[2] == SELL     # Minus zone, Wave < FastLine
        assert result.iloc[3] == BUY      # Plus zone, Wave > FastLine
    
    def test_apply_trading_rule_weak_trend_rule(self):
        """Test apply_trading_rule with WeakTrend rule."""
        wave = pd.Series([0.0, 0.5, -0.3, 0.8])
        fast_line = pd.Series([0.0, 0.2, 0.1, 0.6])
        tr_enum = TradingRuleEnum.TR_WEAK_TREND
        result = apply_trading_rule(wave, fast_line, tr_enum)
        assert len(result) == 4
        assert result.iloc[0] == NOTRADE  # First value
        assert result.iloc[1] == NOTRADE  # Plus zone, Wave > FastLine (not <)
        assert result.iloc[2] == NOTRADE  # Minus zone, Wave < FastLine (not >)
        assert result.iloc[3] == NOTRADE  # Plus zone, Wave > FastLine (not <)
    
    def test_apply_trading_rule_fast_zone_reverse_rule(self):
        """Test apply_trading_rule with FastZoneReverse rule."""
        wave = pd.Series([0.0, 0.5, -0.3, 0.8])
        fast_line = pd.Series([0.0, 0.2, 0.1, 0.6])
        tr_enum = TradingRuleEnum.TR_FAST_ZONE_REVERSE
        result = apply_trading_rule(wave, fast_line, tr_enum)
        assert len(result) == 4
        assert result.iloc[0] == NOTRADE  # First value
        assert result.iloc[1] == NOTRADE  # Plus zone, Wave > FastLine (not <)
        assert result.iloc[2] == BUY      # Minus zone, Wave > FastLine
        assert result.iloc[3] == NOTRADE  # Plus zone, Wave > FastLine (not <)
    
    def test_apply_trading_rule_unknown_rule(self):
        """Test apply_trading_rule with unknown rule."""
        wave = pd.Series([0.0, 0.5, -0.3])
        fast_line = pd.Series([0.0, 0.2, 0.1])
        tr_enum = 999  # Unknown rule
        result = apply_trading_rule(wave, fast_line, tr_enum)
        assert len(result) == 3
        assert result.iloc[0] == NOTRADE  # First value
        assert result.iloc[1] == BUY      # Default to Fast rule: 0.5 > 0.2
        assert result.iloc[2] == SELL     # Default to Fast rule: -0.3 < 0.1


class TestApplyGlobalTradingRule:
    """Test apply_global_trading_rule function."""
    
    def test_apply_global_trading_rule_empty_data(self):
        """Test apply_global_trading_rule with empty data."""
        color1 = pd.Series([], dtype=float)
        color2 = pd.Series([], dtype=float)
        wave1 = pd.Series([], dtype=float)
        global_tr_enum = GlobalTradingRuleEnum.G_TR_PRIME
        final_color, final_wave, final_fast_line = apply_global_trading_rule(
            color1, color2, wave1, global_tr_enum
        )
        assert len(final_color) == 0
        assert len(final_wave) == 0
        assert len(final_fast_line) == 0
    
    def test_apply_global_trading_rule_prime_rule(self):
        """Test apply_global_trading_rule with Prime rule."""
        color1 = pd.Series([NOTRADE, BUY, SELL, BUY])
        color2 = pd.Series([NOTRADE, BUY, SELL, BUY])
        wave1 = pd.Series([0.0, 0.5, -0.3, 0.8])
        global_tr_enum = GlobalTradingRuleEnum.G_TR_PRIME
        final_color, final_wave, final_fast_line = apply_global_trading_rule(
            color1, color2, wave1, global_tr_enum
        )
        assert len(final_color) == 4
        assert final_color.iloc[0] == NOTRADE  # First value
        assert final_color.iloc[1] == BUY      # Both agree on BUY
        assert final_color.iloc[2] == SELL     # Both agree on SELL
        assert final_color.iloc[3] == BUY      # Both agree on BUY
    
    def test_apply_global_trading_rule_reverse_rule(self):
        """Test apply_global_trading_rule with Reverse rule."""
        color1 = pd.Series([NOTRADE, BUY, SELL, BUY])
        color2 = pd.Series([NOTRADE, BUY, SELL, BUY])
        wave1 = pd.Series([0.0, 0.5, -0.3, 0.8])
        global_tr_enum = GlobalTradingRuleEnum.G_TR_REVERSE
        final_color, final_wave, final_fast_line = apply_global_trading_rule(
            color1, color2, wave1, global_tr_enum
        )
        assert len(final_color) == 4
        assert final_color.iloc[0] == NOTRADE  # First value
        assert final_color.iloc[1] == SELL     # Both agree on BUY, so reverse to SELL
        assert final_color.iloc[2] == BUY      # Both agree on SELL, so reverse to BUY
        assert final_color.iloc[3] == SELL     # Both agree on BUY, so reverse to SELL
    
    def test_apply_global_trading_rule_prime_zone_rule(self):
        """Test apply_global_trading_rule with PrimeZone rule."""
        color1 = pd.Series([NOTRADE, BUY, SELL, BUY])
        color2 = pd.Series([NOTRADE, BUY, SELL, BUY])
        wave1 = pd.Series([0.0, 0.5, -0.3, 0.8])
        global_tr_enum = GlobalTradingRuleEnum.G_TR_PRIME_ZONE
        final_color, final_wave, final_fast_line = apply_global_trading_rule(
            color1, color2, wave1, global_tr_enum
        )
        assert len(final_color) == 4
        assert final_color.iloc[0] == NOTRADE  # First value
        assert final_color.iloc[1] == BUY      # Both agree on BUY, wave1 > 0
        assert final_color.iloc[2] == NOTRADE  # Both agree on SELL, but wave1 < 0
        assert final_color.iloc[3] == BUY      # Both agree on BUY, wave1 > 0
    
    def test_apply_global_trading_rule_disagreeing_signals(self):
        """Test apply_global_trading_rule with disagreeing signals."""
        color1 = pd.Series([NOTRADE, BUY, SELL, BUY])
        color2 = pd.Series([NOTRADE, SELL, BUY, SELL])
        wave1 = pd.Series([0.0, 0.5, -0.3, 0.8])
        global_tr_enum = GlobalTradingRuleEnum.G_TR_PRIME
        final_color, final_wave, final_fast_line = apply_global_trading_rule(
            color1, color2, wave1, global_tr_enum
        )
        assert len(final_color) == 4
        assert final_color.iloc[0] == NOTRADE  # First value
        assert final_color.iloc[1] == NOTRADE  # Disagree: BUY vs SELL
        assert final_color.iloc[2] == NOTRADE  # Disagree: SELL vs BUY
        assert final_color.iloc[3] == NOTRADE  # Disagree: BUY vs SELL
    
    def test_apply_global_trading_rule_one_no_trade(self):
        """Test apply_global_trading_rule with one signal being NOTRADE."""
        color1 = pd.Series([NOTRADE, BUY, SELL, BUY])
        color2 = pd.Series([NOTRADE, NOTRADE, SELL, NOTRADE])
        wave1 = pd.Series([0.0, 0.5, -0.3, 0.8])
        global_tr_enum = GlobalTradingRuleEnum.G_TR_PRIME
        final_color, final_wave, final_fast_line = apply_global_trading_rule(
            color1, color2, wave1, global_tr_enum
        )
        assert len(final_color) == 4
        assert final_color.iloc[0] == NOTRADE  # First value
        assert final_color.iloc[1] == NOTRADE  # One is NOTRADE
        assert final_color.iloc[2] == SELL     # Both agree on SELL
        assert final_color.iloc[3] == NOTRADE  # One is NOTRADE


class TestCalculateSma:
    """Test calculate_sma function."""
    
    def test_calculate_sma_empty_data(self):
        """Test calculate_sma with empty data."""
        source = pd.Series([], dtype=float)
        period = 5
        result = calculate_sma(source, period)
        assert len(result) == 0
    
    def test_calculate_sma_insufficient_data(self):
        """Test calculate_sma with insufficient data."""
        source = pd.Series([1.0, 2.0, 3.0])
        period = 5
        result = calculate_sma(source, period)
        assert len(result) == 3
        # Should return original data when insufficient for SMA
    
    def test_calculate_sma_sufficient_data(self):
        """Test calculate_sma with sufficient data."""
        source = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        period = 3
        result = calculate_sma(source, period)
        assert len(result) == 6
        assert abs(result.iloc[2] - 2.0) < 1e-10  # (1+2+3)/3
        assert abs(result.iloc[3] - 3.0) < 1e-10  # (2+3+4)/3
        assert abs(result.iloc[4] - 4.0) < 1e-10  # (3+4+5)/3
        assert abs(result.iloc[5] - 5.0) < 1e-10  # (4+5+6)/3


class TestCalculateSchrWave2:
    """Test calculate_schr_wave2 function."""
    
    def test_calculate_schr_wave2_insufficient_data(self):
        """Test calculate_schr_wave2 with insufficient data."""
        df = pd.DataFrame({
            'Open': [100.0, 101.0, 102.0],  # Only 3 bars, need more
            'High': [101.0, 102.0, 103.0],
            'Low': [99.0, 100.0, 101.0],
            'Close': [100.5, 101.5, 102.5]
        })
        result = calculate_schr_wave2(df, long1=5, fast1=3, trend1=2, long2=4, fast2=2, trend2=3, sma_period=2)
        assert result is df  # Should return original DataFrame
    
    def test_calculate_schr_wave2_sufficient_data(self):
        """Test calculate_schr_wave2 with sufficient data."""
        # Create test data with enough bars
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 50),
            'High': np.random.uniform(110, 120, 50),
            'Low': np.random.uniform(90, 100, 50),
            'Close': np.random.uniform(100, 110, 50)
        }, index=dates)
        
        result = calculate_schr_wave2(df, long1=10, fast1=5, trend1=3, long2=8, fast2=4, trend2=2, sma_period=5)
        
        # Check that all required columns are present
        required_cols = [
            'schr_wave2_wave', 'schr_wave2_fast_line', 'schr_wave2_ma_line',
            'schr_wave2_direction', 'schr_wave2_signal'
        ]
        for col in required_cols:
            assert col in result.columns
        
        # Check that wave components are present
        wave_cols = [
            'schr_wave2_wave1', 'schr_wave2_wave2', 'schr_wave2_fast_line1',
            'schr_wave2_fast_line2', 'schr_wave2_color1', 'schr_wave2_color2'
        ]
        for col in wave_cols:
            assert col in result.columns
        
        # Check that parameters are stored
        param_cols = [
            'schr_wave2_long1', 'schr_wave2_fast1', 'schr_wave2_trend1',
            'schr_wave2_tr1', 'schr_wave2_long2', 'schr_wave2_fast2',
            'schr_wave2_trend2', 'schr_wave2_tr2', 'schr_wave2_global_tr',
            'schr_wave2_sma_period'
        ]
        for col in param_cols:
            assert col in result.columns
        
        # Check that signal values are valid
        assert result['schr_wave2_signal'].isin([NOTRADE, BUY, SELL]).all()
        assert result['schr_wave2_direction'].isin([NOTRADE, BUY, SELL]).all()


class TestSCHRWave2Indicator:
    """Test SCHRWave2Indicator class."""
    
    def test_schr_wave2_indicator_init(self):
        """Test SCHRWave2Indicator initialization."""
        indicator = SCHRWave2Indicator(
            long1=100, fast1=20, trend1=5, tr1='Fast',
            long2=50, fast2=15, trend2=3, tr2='Zone',
            global_tr='Prime', sma_period=30
        )
        
        assert indicator.long1 == 100
        assert indicator.fast1 == 20
        assert indicator.trend1 == 5
        assert indicator.tr1 == 'Fast'
        assert indicator.long2 == 50
        assert indicator.fast2 == 15
        assert indicator.trend2 == 3
        assert indicator.tr2 == 'Zone'
        assert indicator.global_tr == 'Prime'
        assert indicator.sma_period == 30
    
    def test_schr_wave2_indicator_default_init(self):
        """Test SCHRWave2Indicator with default parameters."""
        indicator = SCHRWave2Indicator()
        
        assert indicator.long1 == 339
        assert indicator.fast1 == 10
        assert indicator.trend1 == 2
        assert indicator.tr1 == 'Fast'
        assert indicator.long2 == 22
        assert indicator.fast2 == 11
        assert indicator.trend2 == 4
        assert indicator.tr2 == 'Fast'
        assert indicator.global_tr == 'Prime'
        assert indicator.sma_period == 22
    
    def test_schr_wave2_indicator_validate_data(self):
        """Test SCHRWave2Indicator data validation."""
        indicator = SCHRWave2Indicator(long1=10, fast1=5, trend1=3, long2=8, fast2=4, trend2=2, sma_period=5)
        
        # Test with insufficient data
        df_insufficient = pd.DataFrame({
            'Open': [100.0, 101.0, 102.0],  # Only 3 bars
            'High': [101.0, 102.0, 103.0],
            'Low': [99.0, 100.0, 101.0],
            'Close': [100.5, 101.5, 102.5]
        })
        assert not indicator.validate_data(df_insufficient, min_periods=10)
        
        # Test with sufficient data
        df_sufficient = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 20),
            'High': np.random.uniform(110, 120, 20),
            'Low': np.random.uniform(90, 100, 20),
            'Close': np.random.uniform(100, 110, 20)
        })
        assert indicator.validate_data(df_sufficient, min_periods=10)
    
    def test_schr_wave2_indicator_calculate(self):
        """Test SCHRWave2Indicator calculate method."""
        indicator = SCHRWave2Indicator(long1=10, fast1=5, trend1=3, long2=8, fast2=4, trend2=2, sma_period=5)
        
        # Create test data
        dates = pd.date_range('2023-01-01', periods=20, freq='D')
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 20),
            'High': np.random.uniform(110, 120, 20),
            'Low': np.random.uniform(90, 100, 20),
            'Close': np.random.uniform(100, 110, 20)
        }, index=dates)
        
        result = indicator.calculate(df)
        
        # Check that calculation was successful
        assert 'schr_wave2_wave' in result.columns
        assert 'schr_wave2_signal' in result.columns
        assert len(result) == 20
    
    def test_schr_wave2_indicator_apply_rule(self):
        """Test SCHRWave2Indicator apply_rule method."""
        indicator = SCHRWave2Indicator(long1=10, fast1=5, trend1=3, long2=8, fast2=4, trend2=2, sma_period=5)
        
        # Create test data
        dates = pd.date_range('2023-01-01', periods=20, freq='D')
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 20),
            'High': np.random.uniform(110, 120, 20),
            'Low': np.random.uniform(90, 100, 20),
            'Close': np.random.uniform(100, 110, 20)
        }, index=dates)
        
        result = indicator.apply_rule(df, point=0.00001)
        
        # Check that rule columns are present
        rule_cols = ['PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff']
        for col in rule_cols:
            assert col in result.columns
        
        # Check that indicator columns are present
        indicator_cols = ['schr_wave2_wave', 'schr_wave2_signal', 'schr_wave2_direction']
        for col in indicator_cols:
            assert col in result.columns


class TestApplyRuleSchrWave2:
    """Test apply_rule_schr_wave2 function."""
    
    def test_apply_rule_schr_wave2_default_params(self):
        """Test apply_rule_schr_wave2 with default parameters."""
        # Create test data with enough bars for default parameters (339)
        dates = pd.date_range('2023-01-01', periods=400, freq='D')
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 400),
            'High': np.random.uniform(110, 120, 400),
            'Low': np.random.uniform(90, 100, 400),
            'Close': np.random.uniform(100, 110, 400)
        }, index=dates)
        
        result = apply_rule_schr_wave2(df, point=0.00001)
        
        # Check that result contains expected columns
        assert 'schr_wave2_wave' in result.columns
        assert 'schr_wave2_signal' in result.columns
        assert 'PPrice1' in result.columns
        assert 'PColor1' in result.columns
    
    def test_apply_rule_schr_wave2_custom_params(self):
        """Test apply_rule_schr_wave2 with custom parameters."""
        # Create test data with enough bars for custom parameters (50)
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 100),
            'High': np.random.uniform(110, 120, 100),
            'Low': np.random.uniform(90, 100, 100),
            'Close': np.random.uniform(100, 110, 100)
        }, index=dates)
        
        result = apply_rule_schr_wave2(
            df, point=0.00001,
            long1=50, fast1=15, trend1=5, tr1='Zone',
            long2=25, fast2=10, trend2=3, tr2='StrongTrend',
            global_tr='Reverse', sma_period=15
        )
        
        # Check that result contains expected columns
        assert 'schr_wave2_wave' in result.columns
        assert 'schr_wave2_signal' in result.columns
        assert 'PPrice1' in result.columns
        assert 'PColor1' in result.columns
        
        # Check that custom parameters are stored
        assert result['schr_wave2_long1'].iloc[0] == 50
        assert result['schr_wave2_fast1'].iloc[0] == 15
        assert result['schr_wave2_tr1'].iloc[0] == 'Zone'
        assert result['schr_wave2_long2'].iloc[0] == 25
        assert result['schr_wave2_fast2'].iloc[0] == 10
        assert result['schr_wave2_tr2'].iloc[0] == 'StrongTrend'
        assert result['schr_wave2_global_tr'].iloc[0] == 'Reverse'
        assert result['schr_wave2_sma_period'].iloc[0] == 15
    
    def test_apply_rule_schr_wave2_price_type_open(self):
        """Test apply_rule_schr_wave2 with open price type."""
        # Create test data with enough bars for default parameters (339)
        dates = pd.date_range('2023-01-01', periods=400, freq='D')
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 400),
            'High': np.random.uniform(110, 120, 400),
            'Low': np.random.uniform(90, 100, 400),
            'Close': np.random.uniform(100, 110, 400)
        }, index=dates)
        
        result = apply_rule_schr_wave2(df, point=0.00001, price_type='open')
        
        # Check that result contains expected columns
        assert 'schr_wave2_wave' in result.columns
        assert 'schr_wave2_signal' in result.columns
    
    def test_apply_rule_schr_wave2_price_type_close(self):
        """Test apply_rule_schr_wave2 with close price type."""
        # Create test data with enough bars for default parameters (339)
        dates = pd.date_range('2023-01-01', periods=400, freq='D')
        df = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 400),
            'High': np.random.uniform(110, 120, 400),
            'Low': np.random.uniform(90, 100, 400),
            'Close': np.random.uniform(100, 110, 400)
        }, index=dates)
        
        result = apply_rule_schr_wave2(df, point=0.00001, price_type='close')
        
        # Check that result contains expected columns
        assert 'schr_wave2_wave' in result.columns
        assert 'schr_wave2_signal' in result.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
