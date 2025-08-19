# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_wave_ind.py

"""
Tests for Wave indicator Global TR Switch functions.
"""

import pytest
import pandas as pd
import numpy as np

from src.calculation.indicators.trend.wave_ind import (
    global_tr_switch, g_prime_tr, g_reverse_tr, g_prime_tr_zone,
    g_reverse_tr_zone, g_new_zone_tr, g_long_zone_tr, g_long_zone_reverse_tr,
    ENUM_GLOBAL_TR, BUY, SELL, NOTRADE
)


class TestGlobalTRSwitch:
    """Test cases for Global TR Switch functions."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        index = pd.date_range('2023-01-01', periods=10, freq='D')
        
        # Create sample wave and fastline data
        wave1 = pd.Series([1.0, 2.0, -1.0, -2.0, 1.5, -1.5, 0.5, -0.5, 2.5, -2.5], index=index)
        wave2 = pd.Series([0.5, 1.5, -0.5, -1.5, 1.0, -1.0, 0.3, -0.3, 2.0, -2.0], index=index)
        fastline1 = pd.Series([0.8, 1.8, -0.8, -1.8, 1.3, -1.3, 0.4, -0.4, 2.3, -2.3], index=index)
        fastline2 = pd.Series([0.3, 1.3, -0.3, -1.3, 0.8, -0.8, 0.2, -0.2, 1.8, -1.8], index=index)
        
        # Create sample color signals
        color1 = pd.Series([BUY, BUY, SELL, SELL, BUY, SELL, BUY, SELL, BUY, SELL], index=index)
        color2 = pd.Series([BUY, SELL, SELL, BUY, BUY, SELL, BUY, SELL, BUY, SELL], index=index)
        
        return wave1, wave2, fastline1, fastline2, color1, color2
    
    def test_g_prime_tr_basic(self, sample_data):
        """Test G Prime TR with basic signals."""
        wave1, wave2, fastline1, fastline2, color1, color2 = sample_data
        
        result = g_prime_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Check that signals are only generated when both colors agree
        assert result.iloc[0] == BUY  # Both BUY
        assert result.iloc[1] == NOTRADE  # BUY vs SELL
        assert result.iloc[2] == SELL  # Both SELL
        assert result.iloc[3] == NOTRADE  # SELL vs BUY
        assert result.iloc[4] == BUY  # Both BUY
        assert result.iloc[5] == SELL  # Both SELL
        assert result.iloc[6] == BUY  # Both BUY
        assert result.iloc[7] == SELL  # Both SELL
        assert result.iloc[8] == BUY  # Both BUY
        assert result.iloc[9] == SELL  # Both SELL
    
    def test_g_reverse_tr_basic(self, sample_data):
        """Test G Reverse TR with basic signals."""
        wave1, wave2, fastline1, fastline2, color1, color2 = sample_data
        
        result = g_reverse_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Check that signals are reversed when both colors agree
        assert result.iloc[0] == SELL  # Both BUY -> SELL
        assert result.iloc[1] == NOTRADE  # BUY vs SELL
        assert result.iloc[2] == BUY  # Both SELL -> BUY
        assert result.iloc[3] == NOTRADE  # SELL vs BUY
        assert result.iloc[4] == SELL  # Both BUY -> SELL
        assert result.iloc[5] == BUY  # Both SELL -> BUY
        assert result.iloc[6] == SELL  # Both BUY -> SELL
        assert result.iloc[7] == BUY  # Both SELL -> BUY
        assert result.iloc[8] == SELL  # Both BUY -> SELL
        assert result.iloc[9] == BUY  # Both SELL -> BUY
    
    def test_g_prime_tr_zone(self, sample_data):
        """Test G Prime TR Zone with zone filtering."""
        wave1, wave2, fastline1, fastline2, color1, color2 = sample_data
        
        result = g_prime_tr_zone(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Check zone filtering: BUY only in negative zone, SELL only in positive zone
        # Index 0: wave1=1.0 (positive), color1=BUY, color2=BUY -> BUY in positive zone = NOTRADE
        assert result.iloc[0] == NOTRADE  # BUY in positive zone (wave1 > 0)
        # Index 1: wave1=2.0 (positive), color1=BUY, color2=SELL -> different signals = NOTRADE
        assert result.iloc[1] == NOTRADE  # BUY vs SELL
        # Index 2: wave1=-1.0 (negative), color1=SELL, color2=SELL -> SELL in negative zone = NOTRADE
        assert result.iloc[2] == NOTRADE  # SELL in negative zone (wave1 < 0) - should be NOTRADE
        # Index 3: wave1=-2.0 (negative), color1=SELL, color2=BUY -> different signals = NOTRADE
        assert result.iloc[3] == NOTRADE  # SELL vs BUY
        # Index 4: wave1=1.5 (positive), color1=BUY, color2=BUY -> BUY in positive zone = NOTRADE
        assert result.iloc[4] == NOTRADE  # BUY in positive zone (wave1 > 0)
        # Index 5: wave1=-1.5 (negative), color1=SELL, color2=SELL -> SELL in negative zone = NOTRADE
        assert result.iloc[5] == NOTRADE  # SELL in negative zone (wave1 < 0) - should be NOTRADE
        # Index 6: wave1=0.5 (positive), color1=BUY, color2=BUY -> BUY in positive zone = NOTRADE
        assert result.iloc[6] == NOTRADE  # BUY in positive zone (wave1 > 0)
        # Index 7: wave1=-0.5 (negative), color1=SELL, color2=SELL -> SELL in negative zone = NOTRADE
        assert result.iloc[7] == NOTRADE  # SELL in negative zone (wave1 < 0) - should be NOTRADE
        # Index 8: wave1=2.5 (positive), color1=BUY, color2=BUY -> BUY in positive zone = NOTRADE
        assert result.iloc[8] == NOTRADE  # BUY in positive zone (wave1 > 0)
        # Index 9: wave1=-2.5 (negative), color1=SELL, color2=SELL -> SELL in negative zone = NOTRADE
        assert result.iloc[9] == NOTRADE  # SELL in negative zone (wave1 < 0) - should be NOTRADE
    
    def test_g_reverse_tr_zone(self, sample_data):
        """Test G Reverse TR Zone with reversed zone filtering."""
        wave1, wave2, fastline1, fastline2, color1, color2 = sample_data
        
        result = g_reverse_tr_zone(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Check reversed zone filtering: BUY in negative zone -> SELL, SELL in positive zone -> BUY
        # Index 0: wave1=1.0 (positive), color1=BUY, color2=BUY -> BUY in positive zone = NOTRADE
        assert result.iloc[0] == NOTRADE  # BUY in positive zone -> no signal
        # Index 1: wave1=2.0 (positive), color1=BUY, color2=SELL -> different signals = NOTRADE
        assert result.iloc[1] == NOTRADE  # BUY vs SELL
        # Index 2: wave1=-1.0 (negative), color1=SELL, color2=SELL -> SELL in negative zone = NOTRADE
        assert result.iloc[2] == NOTRADE  # SELL in negative zone -> no signal
        # Index 3: wave1=-2.0 (negative), color1=SELL, color2=BUY -> different signals = NOTRADE
        assert result.iloc[3] == NOTRADE  # SELL vs BUY
        # Index 4: wave1=1.5 (positive), color1=BUY, color2=BUY -> BUY in positive zone = NOTRADE
        assert result.iloc[4] == NOTRADE  # BUY in positive zone -> no signal
        # Index 5: wave1=-1.5 (negative), color1=SELL, color2=SELL -> SELL in negative zone = NOTRADE
        assert result.iloc[5] == NOTRADE  # SELL in negative zone -> no signal
        # Index 6: wave1=0.5 (positive), color1=BUY, color2=BUY -> BUY in positive zone = NOTRADE
        assert result.iloc[6] == NOTRADE  # BUY in positive zone -> no signal
        # Index 7: wave1=-0.5 (negative), color1=SELL, color2=SELL -> SELL in negative zone = NOTRADE
        assert result.iloc[7] == NOTRADE  # SELL in negative zone -> no signal
        # Index 8: wave1=2.5 (positive), color1=BUY, color2=BUY -> BUY in positive zone = NOTRADE
        assert result.iloc[8] == NOTRADE  # BUY in positive zone -> no signal
        # Index 9: wave1=-2.5 (negative), color1=SELL, color2=SELL -> SELL in negative zone = NOTRADE
        assert result.iloc[9] == NOTRADE  # SELL in negative zone -> no signal
    
    def test_g_new_zone_tr(self, sample_data):
        """Test G New Zone TR with signal disagreement logic."""
        wave1, wave2, fastline1, fastline2, color1, color2 = sample_data
        
        result = g_new_zone_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Check that signals are generated when colors disagree
        assert result.iloc[0] == NOTRADE  # Both BUY (agree)
        assert result.iloc[1] == SELL  # BUY vs SELL (disagree) -> opposite of last signal (BUY)
        assert result.iloc[2] == NOTRADE  # Both SELL (agree)
        assert result.iloc[3] == BUY  # SELL vs BUY (disagree) -> opposite of last signal (SELL)
        assert result.iloc[4] == NOTRADE  # Both BUY (agree)
        assert result.iloc[5] == NOTRADE  # Both SELL (agree)
        assert result.iloc[6] == NOTRADE  # Both BUY (agree)
        assert result.iloc[7] == NOTRADE  # Both SELL (agree)
        assert result.iloc[8] == NOTRADE  # Both BUY (agree)
        assert result.iloc[9] == NOTRADE  # Both SELL (agree)
    
    def test_g_long_zone_tr(self, sample_data):
        """Test G Long Zone TR with opposite signal generation."""
        wave1, wave2, fastline1, fastline2, color1, color2 = sample_data
        
        result = g_long_zone_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Check that opposite signals are always generated
        assert result.iloc[0] == SELL  # Last signal BUY -> SELL
        assert result.iloc[1] == SELL  # Last signal BUY -> SELL
        assert result.iloc[2] == BUY  # Last signal SELL -> BUY
        assert result.iloc[3] == BUY  # Last signal SELL -> BUY
        assert result.iloc[4] == SELL  # Last signal BUY -> SELL
        assert result.iloc[5] == BUY  # Last signal SELL -> BUY
        assert result.iloc[6] == SELL  # Last signal BUY -> SELL
        assert result.iloc[7] == BUY  # Last signal SELL -> BUY
        assert result.iloc[8] == SELL  # Last signal BUY -> SELL
        assert result.iloc[9] == BUY  # Last signal SELL -> BUY
    
    def test_g_long_zone_reverse_tr(self, sample_data):
        """Test G Long Zone Reverse TR with same signal generation."""
        wave1, wave2, fastline1, fastline2, color1, color2 = sample_data
        
        result = g_long_zone_reverse_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Check that same signals are always generated
        assert result.iloc[0] == BUY  # Last signal BUY -> BUY
        assert result.iloc[1] == BUY  # Last signal BUY -> BUY
        assert result.iloc[2] == SELL  # Last signal SELL -> SELL
        assert result.iloc[3] == SELL  # Last signal SELL -> SELL
        assert result.iloc[4] == BUY  # Last signal BUY -> BUY
        assert result.iloc[5] == SELL  # Last signal SELL -> SELL
        assert result.iloc[6] == BUY  # Last signal BUY -> BUY
        assert result.iloc[7] == SELL  # Last signal SELL -> SELL
        assert result.iloc[8] == BUY  # Last signal BUY -> BUY
        assert result.iloc[9] == SELL  # Last signal SELL -> SELL
    
    def test_global_tr_switch_all_rules(self, sample_data):
        """Test global_tr_switch with all trading rules."""
        wave1, wave2, fastline1, fastline2, color1, color2 = sample_data
        
        # Test all global trading rules
        rules = [
            ENUM_GLOBAL_TR.G_TR_PRIME,
            ENUM_GLOBAL_TR.G_TR_REVERSE,
            ENUM_GLOBAL_TR.G_TR_PRIME_ZONE,
            ENUM_GLOBAL_TR.G_TR_REVERSE_ZONE,
            ENUM_GLOBAL_TR.G_TR_NEW_ZONE,
            ENUM_GLOBAL_TR.G_TR_LONG_ZONE,
            ENUM_GLOBAL_TR.G_TR_LONG_ZONE_REVERSE
        ]
        
        for rule in rules:
            plot_color, plot_wave, plot_fastline = global_tr_switch(
                rule, wave1, wave2, fastline1, fastline2, color1, color2
            )
            
            # Check that output series have correct length
            assert len(plot_color) == len(wave1)
            assert len(plot_wave) == len(wave1)
            assert len(plot_fastline) == len(wave1)
            
            # Check that plot_wave and plot_fastline are copies of wave1 and fastline1
            pd.testing.assert_series_equal(plot_wave, wave1)
            pd.testing.assert_series_equal(plot_fastline, fastline1)
    
    def test_global_tr_switch_invalid_rule(self, sample_data):
        """Test global_tr_switch with invalid rule (should default to G_TR_PRIME)."""
        wave1, wave2, fastline1, fastline2, color1, color2 = sample_data
        
        # Create an invalid rule (not in enum)
        class InvalidRule:
            pass
        
        invalid_rule = InvalidRule()
        
        plot_color, plot_wave, plot_fastline = global_tr_switch(
            invalid_rule, wave1, wave2, fastline1, fastline2, color1, color2
        )
        
        # Should default to G_TR_PRIME behavior
        expected_result = g_prime_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        pd.testing.assert_series_equal(plot_color, expected_result)
    
    def test_empty_signals(self):
        """Test functions with empty signals (all NOTRADE)."""
        index = pd.date_range('2023-01-01', periods=5, freq='D')
        wave1 = pd.Series([1.0, -1.0, 0.5, -0.5, 1.5], index=index)
        wave2 = pd.Series([0.5, -0.5, 0.3, -0.3, 1.0], index=index)
        fastline1 = pd.Series([0.8, -0.8, 0.4, -0.4, 1.3], index=index)
        fastline2 = pd.Series([0.3, -0.3, 0.2, -0.2, 0.8], index=index)
        color1 = pd.Series([NOTRADE, NOTRADE, NOTRADE, NOTRADE, NOTRADE], index=index)
        color2 = pd.Series([NOTRADE, NOTRADE, NOTRADE, NOTRADE, NOTRADE], index=index)
        
        # Test all functions with empty signals
        functions = [
            g_prime_tr, g_reverse_tr, g_prime_tr_zone, g_reverse_tr_zone,
            g_new_zone_tr, g_long_zone_tr, g_long_zone_reverse_tr
        ]
        
        for func in functions:
            result = func(wave1, wave2, fastline1, fastline2, color1, color2)
            # All results should be NOTRADE
            assert all(result == NOTRADE)
    
    def test_mixed_signals(self):
        """Test functions with mixed signals (some NOTRADE, some BUY/SELL)."""
        index = pd.date_range('2023-01-01', periods=6, freq='D')
        wave1 = pd.Series([1.0, -1.0, 0.5, -0.5, 1.5, -1.5], index=index)
        wave2 = pd.Series([0.5, -0.5, 0.3, -0.3, 1.0, -1.0], index=index)
        fastline1 = pd.Series([0.8, -0.8, 0.4, -0.4, 1.3, -1.3], index=index)
        fastline2 = pd.Series([0.3, -0.3, 0.2, -0.2, 0.8, -0.8], index=index)
        color1 = pd.Series([BUY, NOTRADE, SELL, BUY, NOTRADE, SELL], index=index)
        color2 = pd.Series([BUY, SELL, NOTRADE, NOTRADE, BUY, SELL], index=index)
        
        # Test g_prime_tr with mixed signals
        result = g_prime_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Only index 0 and 5 should have signals (both colors agree)
        assert result.iloc[0] == BUY  # Both BUY
        assert result.iloc[1] == NOTRADE  # BUY vs SELL
        assert result.iloc[2] == NOTRADE  # SELL vs NOTRADE
        assert result.iloc[3] == NOTRADE  # BUY vs NOTRADE
        assert result.iloc[4] == NOTRADE  # NOTRADE vs BUY
        assert result.iloc[5] == SELL  # Both SELL
    
    def test_zone_filtering_with_valid_signals(self):
        """Test zone filtering with signals that should pass the zone filter."""
        index = pd.date_range('2023-01-01', periods=4, freq='D')
        
        # Test data where signals should pass zone filtering
        wave1 = pd.Series([-1.0, 1.0, -2.0, 2.0], index=index)  # negative, positive, negative, positive
        wave2 = pd.Series([-0.5, 0.5, -1.5, 1.5], index=index)
        fastline1 = pd.Series([-0.8, 0.8, -1.8, 1.8], index=index)
        fastline2 = pd.Series([-0.3, 0.3, -1.3, 1.3], index=index)
        
        # BUY in negative zone, SELL in positive zone (should pass zone filter)
        color1 = pd.Series([BUY, SELL, BUY, SELL], index=index)
        color2 = pd.Series([BUY, SELL, BUY, SELL], index=index)
        
        # Test g_prime_tr_zone
        result = g_prime_tr_zone(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Index 0: BUY in negative zone (-1.0) -> should pass
        assert result.iloc[0] == BUY
        # Index 1: SELL in positive zone (1.0) -> should pass
        assert result.iloc[1] == SELL
        # Index 2: BUY in negative zone (-2.0) -> should pass
        assert result.iloc[2] == BUY
        # Index 3: SELL in positive zone (2.0) -> should pass
        assert result.iloc[3] == SELL
        
        # Test g_reverse_tr_zone
        result_reverse = g_reverse_tr_zone(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Index 0: BUY in negative zone -> should reverse to SELL
        assert result_reverse.iloc[0] == SELL
        # Index 1: SELL in positive zone -> should reverse to BUY
        assert result_reverse.iloc[1] == BUY
        # Index 2: BUY in negative zone -> should reverse to SELL
        assert result_reverse.iloc[2] == SELL
        # Index 3: SELL in positive zone -> should reverse to BUY
        assert result_reverse.iloc[3] == BUY
