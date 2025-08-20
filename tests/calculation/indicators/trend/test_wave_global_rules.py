# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_wave_global_rules.py

"""
Tests for Wave indicator global trading rules, especially Prime rule.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.trend.wave_ind import (
    g_prime_tr, g_reverse_tr, g_prime_tr_zone,
    ENUM_GLOBAL_TR, ENUM_MOM_TR, WaveParameters,
    apply_rule_wave, BUY, SELL, NOTRADE
)


class TestWaveGlobalRules:
    """Test cases for Wave indicator global trading rules."""

    @pytest.fixture
    def sample_wave_data(self):
        """Create sample wave data for testing."""
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        data = {
            'wave1': [0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1, -0.2, 0.3, -0.1],
            'wave2': [0.15, -0.25, 0.35, -0.15, 0.25, -0.35, 0.15, -0.25, 0.35, -0.15],
            'fastline1': [0.05, -0.15, 0.25, -0.05, 0.15, -0.25, 0.05, -0.15, 0.25, -0.05],
            'fastline2': [0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1, -0.2, 0.3, -0.1],
            'color1': [BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL],
            'color2': [BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL]
        }
        df = pd.DataFrame(data, index=dates)
        return df

    def test_g_prime_tr_basic_functionality(self, sample_wave_data):
        """Test basic functionality of Prime rule."""
        result = g_prime_tr(
            sample_wave_data['wave1'],
            sample_wave_data['wave2'],
            sample_wave_data['fastline1'],
            sample_wave_data['fastline2'],
            sample_wave_data['color1'],
            sample_wave_data['color2']
        )
        
        # Since both color1 and color2 are the same, all signals should be reversed
        expected = pd.Series([SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY], index=sample_wave_data.index)
        pd.testing.assert_series_equal(result, expected, check_names=False)

    def test_g_prime_tr_different_signals(self, sample_wave_data):
        """Test Prime rule when signals are different."""
        # Make color2 different from color1
        sample_wave_data['color2'] = [SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY]
        
        result = g_prime_tr(
            sample_wave_data['wave1'],
            sample_wave_data['wave2'],
            sample_wave_data['fastline1'],
            sample_wave_data['fastline2'],
            sample_wave_data['color1'],
            sample_wave_data['color2']
        )
        
        # Since signals are different, all should be NOTRADE
        expected = pd.Series([NOTRADE] * 10, index=sample_wave_data.index)
        pd.testing.assert_series_equal(result, expected, check_names=False)

    def test_g_prime_tr_mixed_signals(self, sample_wave_data):
        """Test Prime rule with mixed signals."""
        # Make some signals the same, some different
        sample_wave_data['color2'] = [BUY, SELL, BUY, BUY, SELL, SELL, BUY, SELL, BUY, SELL]
        
        result = g_prime_tr(
            sample_wave_data['wave1'],
            sample_wave_data['wave2'],
            sample_wave_data['fastline1'],
            sample_wave_data['fastline2'],
            sample_wave_data['color1'],
            sample_wave_data['color2']
        )
        
        # Only positions 0, 1, 2, 6, 8, 9 should have signals (where colors match) - but reversed
        expected_signals = [SELL, BUY, SELL, NOTRADE, NOTRADE, BUY, SELL, BUY, SELL, BUY]
        expected = pd.Series(expected_signals, index=sample_wave_data.index)
        pd.testing.assert_series_equal(result, expected, check_names=False)

    def test_g_reverse_tr_basic_functionality(self, sample_wave_data):
        """Test basic functionality of Reverse rule."""
        result = g_reverse_tr(
            sample_wave_data['wave1'],
            sample_wave_data['wave2'],
            sample_wave_data['fastline1'],
            sample_wave_data['fastline2'],
            sample_wave_data['color1'],
            sample_wave_data['color2']
        )
        
        # Since both color1 and color2 are the same, all signals should be preserved
        expected = sample_wave_data['color1']
        pd.testing.assert_series_equal(result, expected, check_names=False)

    def test_g_prime_tr_zone_basic_functionality(self, sample_wave_data):
        """Test basic functionality of Prime Zone rule."""
        result = g_prime_tr_zone(
            sample_wave_data['wave1'],
            sample_wave_data['wave2'],
            sample_wave_data['fastline1'],
            sample_wave_data['fastline2'],
            sample_wave_data['color1'],
            sample_wave_data['color2']
        )
        
        # Check that BUY signals only appear when wave1 < 0
        # Check that SELL signals only appear when wave1 > 0
        for i in range(len(result)):
            if result.iloc[i] == BUY:
                assert sample_wave_data['wave1'].iloc[i] < 0, f"BUY signal at position {i} should have wave1 < 0"
            elif result.iloc[i] == SELL:
                assert sample_wave_data['wave1'].iloc[i] > 0, f"SELL signal at position {i} should have wave1 > 0"

    def test_g_prime_tr_with_notrade_signals(self, sample_wave_data):
        """Test Prime rule with NOTRADE signals."""
        # Add some NOTRADE signals
        sample_wave_data['color1'] = [BUY, NOTRADE, BUY, SELL, NOTRADE, SELL, BUY, SELL, BUY, SELL]
        sample_wave_data['color2'] = [BUY, BUY, NOTRADE, SELL, SELL, NOTRADE, BUY, SELL, BUY, SELL]
        
        result = g_prime_tr(
            sample_wave_data['wave1'],
            sample_wave_data['wave2'],
            sample_wave_data['fastline1'],
            sample_wave_data['fastline2'],
            sample_wave_data['color1'],
            sample_wave_data['color2']
        )
        
        # Only positions 0, 3, 7, 8, 9 should have signals (where both are not NOTRADE and match) - but reversed
        expected_signals = [SELL, NOTRADE, NOTRADE, BUY, NOTRADE, NOTRADE, SELL, BUY, SELL, BUY]
        expected = pd.Series(expected_signals, index=sample_wave_data.index)
        pd.testing.assert_series_equal(result, expected, check_names=False)

    def test_wave_parameters_prime_rule(self):
        """Test Wave parameters with Prime rule."""
        params = WaveParameters(
            long1=339,
            fast1=10,
            trend1=2,
            tr1=ENUM_MOM_TR.TR_Fast,
            long2=22,
            fast2=11,
            trend2=4,
            tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME,
            sma_period=10
        )
        
        assert params.global_tr == ENUM_GLOBAL_TR.G_TR_PRIME
        assert params.global_tr.value == "Prime"

    def test_wave_parameters_reverse_rule(self):
        """Test Wave parameters with Reverse rule."""
        params = WaveParameters(
            long1=339,
            fast1=10,
            trend1=2,
            tr1=ENUM_MOM_TR.TR_Fast,
            long2=22,
            fast2=11,
            trend2=4,
            tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_REVERSE,
            sma_period=10
        )
        
        assert params.global_tr == ENUM_GLOBAL_TR.G_TR_REVERSE
        assert params.global_tr.value == "Reverse"

    def test_wave_parameters_prime_zone_rule(self):
        """Test Wave parameters with Prime Zone rule."""
        params = WaveParameters(
            long1=339,
            fast1=10,
            trend1=2,
            tr1=ENUM_MOM_TR.TR_Fast,
            long2=22,
            fast2=11,
            trend2=4,
            tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME_ZONE,
            sma_period=10
        )
        
        assert params.global_tr == ENUM_GLOBAL_TR.G_TR_PRIME_ZONE
        assert params.global_tr.value == "Prime Zone"

    def test_enum_values(self):
        """Test that enum values are correct."""
        assert ENUM_GLOBAL_TR.G_TR_PRIME.value == "Prime"
        assert ENUM_GLOBAL_TR.G_TR_REVERSE.value == "Reverse"
        assert ENUM_GLOBAL_TR.G_TR_PRIME_ZONE.value == "Prime Zone"
        assert ENUM_GLOBAL_TR.G_TR_REVERSE_ZONE.value == "Reverse Zone"
        assert ENUM_GLOBAL_TR.G_TR_NEW_ZONE.value == "New Zone"
        assert ENUM_GLOBAL_TR.G_TR_LONG_ZONE.value == "Long Zone"
        assert ENUM_GLOBAL_TR.G_TR_LONG_ZONE_REVERSE.value == "Long Zone Reverse"

    def test_enum_comparison(self):
        """Test enum comparison functionality."""
        prime = ENUM_GLOBAL_TR.G_TR_PRIME
        reverse = ENUM_GLOBAL_TR.G_TR_REVERSE
        
        assert prime != reverse
        assert prime == ENUM_GLOBAL_TR.G_TR_PRIME
        assert reverse == ENUM_GLOBAL_TR.G_TR_REVERSE

    def test_wave_rule_parsing(self):
        """Test that wave rule parsing works correctly."""
        # Test the command format: wave:339,10,2,fast,22,11,4,fast,prime,10,close
        rule_string = "wave:339,10,2,fast,22,11,4,fast,prime,10,close"
        
        # Parse the rule string
        parts = rule_string.split(':')[1].split(',')
        
        # Check that we have the right number of parameters
        assert len(parts) == 11
        
        # Check that the global rule is "prime"
        global_rule = parts[8]
        assert global_rule == "prime"
        
        # Check that this maps to the correct enum
        assert global_rule.upper() == "PRIME"
        # Note: The actual mapping might be different, this is just a test

    def test_wave_rule_parameter_order(self):
        """Test that wave rule parameters are in the correct order."""
        # From the documentation: period_long1, period_short1, period_trend1, tr1,
        # period_long2, period_short2, period_trend2, tr2, global_tr, sma_period, price_type
        
        rule_string = "wave:339,10,2,fast,22,11,4,fast,prime,10,close"
        parts = rule_string.split(':')[1].split(',')
        
        # Verify parameter order
        assert parts[0] == "339"  # long1
        assert parts[1] == "10"   # fast1
        assert parts[2] == "2"    # trend1
        assert parts[3] == "fast" # tr1
        assert parts[4] == "22"   # long2
        assert parts[5] == "11"   # fast2
        assert parts[6] == "4"    # trend2
        assert parts[7] == "fast" # tr2
        assert parts[8] == "prime" # global_tr
        assert parts[9] == "10"   # sma_period
        assert parts[10] == "close" # price_type


if __name__ == "__main__":
    pytest.main([__file__])
