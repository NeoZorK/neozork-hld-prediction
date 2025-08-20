# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_wave_prime_rule.py

"""
Test for Wave indicator Prime rule with specific user command.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.trend.wave_ind import (
    g_prime_tr, g_reverse_tr, ENUM_GLOBAL_TR, ENUM_MOM_TR, WaveParameters,
    apply_rule_wave, BUY, SELL, NOTRADE
)
from src.cli.cli import parse_wave_parameters


class TestWavePrimeRule:
    """Test cases for Wave indicator Prime rule with user command."""

    @pytest.fixture
    def sample_price_data(self):
        """Create sample price data for testing."""
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        data = {
            'DateTime': dates,
            'Open': np.random.uniform(100, 200, 50),
            'High': np.random.uniform(200, 300, 50),
            'Low': np.random.uniform(50, 100, 50),
            'Close': np.random.uniform(100, 200, 50),
            'Volume': np.random.uniform(1000, 10000, 50)
        }
        df = pd.DataFrame(data)
        df.set_index('DateTime', inplace=True)
        return df

    def test_user_command_parsing(self):
        """Test parsing of user command: wave:339,10,2,fast,22,11,4,fast,prime,10,close"""
        command = "339,10,2,fast,22,11,4,fast,prime,10,close"
        
        rule_name, params = parse_wave_parameters(command)
        
        assert rule_name == 'wave'
        assert params['long1'] == 339
        assert params['fast1'] == 10
        assert params['trend1'] == 2
        assert params['tr1'] == ENUM_MOM_TR.TR_Fast
        assert params['long2'] == 22
        assert params['fast2'] == 11
        assert params['trend2'] == 4
        assert params['tr2'] == ENUM_MOM_TR.TR_Fast
        assert params['global_tr'] == ENUM_GLOBAL_TR.G_TR_PRIME
        assert params['sma_period'] == 10
        assert params['price_type'] == 'close'

    def test_prime_vs_reverse_behavior(self):
        """Test that Prime and Reverse rules behave differently."""
        # Create test data where both indicators agree
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        wave1 = pd.Series([0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1, -0.2, 0.3, -0.1], index=dates)
        wave2 = pd.Series([0.15, -0.25, 0.35, -0.15, 0.25, -0.35, 0.15, -0.25, 0.35, -0.15], index=dates)
        fastline1 = pd.Series([0.05, -0.15, 0.25, -0.05, 0.15, -0.25, 0.05, -0.15, 0.25, -0.05], index=dates)
        fastline2 = pd.Series([0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1, -0.2, 0.3, -0.1], index=dates)
        color1 = pd.Series([BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL], index=dates)
        color2 = pd.Series([BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL], index=dates)
        
        # Test Prime rule
        prime_result = g_prime_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Test Reverse rule
        reverse_result = g_reverse_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Prime should preserve signals, Reverse should invert them
        for i in range(len(prime_result)):
            if prime_result.iloc[i] != NOTRADE:
                if prime_result.iloc[i] == BUY:
                    assert reverse_result.iloc[i] == SELL, f"Position {i}: Prime=BUY, Reverse should be SELL"
                elif prime_result.iloc[i] == SELL:
                    assert reverse_result.iloc[i] == BUY, f"Position {i}: Prime=SELL, Reverse should be BUY"

    def test_prime_rule_preserves_signals(self):
        """Test that Prime rule preserves signals when both indicators agree."""
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        wave1 = pd.Series([0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1, -0.2, 0.3, -0.1], index=dates)
        wave2 = pd.Series([0.15, -0.25, 0.35, -0.15, 0.25, -0.35, 0.15, -0.25, 0.35, -0.15], index=dates)
        fastline1 = pd.Series([0.05, -0.15, 0.25, -0.05, 0.15, -0.25, 0.05, -0.15, 0.25, -0.05], index=dates)
        fastline2 = pd.Series([0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1, -0.2, 0.3, -0.1], index=dates)
        color1 = pd.Series([BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL], index=dates)
        color2 = pd.Series([BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL], index=dates)
        
        result = g_prime_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Prime should preserve the original signals
        expected = pd.Series([BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL], index=dates)
        pd.testing.assert_series_equal(result, expected, check_names=False)

    def test_reverse_rule_reverses_signals(self):
        """Test that Reverse rule reverses signals when both indicators agree."""
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        wave1 = pd.Series([0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1, -0.2, 0.3, -0.1], index=dates)
        wave2 = pd.Series([0.15, -0.25, 0.35, -0.15, 0.25, -0.35, 0.15, -0.25, 0.35, -0.15], index=dates)
        fastline1 = pd.Series([0.05, -0.15, 0.25, -0.05, 0.15, -0.25, 0.05, -0.15, 0.25, -0.05], index=dates)
        fastline2 = pd.Series([0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1, -0.2, 0.3, -0.1], index=dates)
        color1 = pd.Series([BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL], index=dates)
        color2 = pd.Series([BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL], index=dates)
        
        result = g_reverse_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Reverse should reverse the signals
        expected = pd.Series([SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY], index=dates)
        pd.testing.assert_series_equal(result, expected, check_names=False)

    def test_wave_parameters_creation(self):
        """Test creating WaveParameters from user command."""
        command = "339,10,2,fast,22,11,4,fast,prime,10,close"
        rule_name, params = parse_wave_parameters(command)
        
        wave_params = WaveParameters(
            long1=params['long1'],
            fast1=params['fast1'],
            trend1=params['trend1'],
            tr1=params['tr1'],
            long2=params['long2'],
            fast2=params['fast2'],
            trend2=params['trend2'],
            tr2=params['tr2'],
            global_tr=params['global_tr'],
            sma_period=params['sma_period']
        )
        
        assert wave_params.global_tr == ENUM_GLOBAL_TR.G_TR_PRIME
        assert wave_params.global_tr.value == "Prime"

    def test_prime_rule_documentation_accuracy(self):
        """Test that Prime rule behavior matches documentation."""
        # Documentation says: "generates signals when both wave indicators agree (same signal)"
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        wave1 = pd.Series([0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1, -0.2, 0.3, -0.1], index=dates)
        wave2 = pd.Series([0.15, -0.25, 0.35, -0.15, 0.25, -0.35, 0.15, -0.25, 0.35, -0.15], index=dates)
        fastline1 = pd.Series([0.05, -0.15, 0.25, -0.05, 0.15, -0.25, 0.05, -0.15, 0.25, -0.05], index=dates)
        fastline2 = pd.Series([0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1, -0.2, 0.3, -0.1], index=dates)
        
        # Test case 1: Both indicators agree (same signal)
        color1 = pd.Series([BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL], index=dates)
        color2 = pd.Series([BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL], index=dates)
        
        result = g_prime_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # Should preserve signals when both agree
        expected = pd.Series([BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL], index=dates)
        pd.testing.assert_series_equal(result, expected, check_names=False)
        
        # Test case 2: Indicators disagree
        color2_different = pd.Series([SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY, SELL, BUY], index=dates)
        
        result_different = g_prime_tr(wave1, wave2, fastline1, fastline2, color1, color2_different)
        
        # Should not generate signals when they disagree
        expected_no_signals = pd.Series([NOTRADE] * 10, index=dates)
        pd.testing.assert_series_equal(result_different, expected_no_signals, check_names=False)

    def test_user_expectation_analysis(self):
        """Analyze what the user might expect vs what Prime actually does."""
        # User says "prime" is reversed - let's check if they expect Reverse behavior
        
        dates = pd.date_range('2023-01-01', periods=5, freq='D')
        wave1 = pd.Series([0.1, -0.2, 0.3, -0.1, 0.2], index=dates)
        wave2 = pd.Series([0.15, -0.25, 0.35, -0.15, 0.25], index=dates)
        fastline1 = pd.Series([0.05, -0.15, 0.25, -0.05, 0.15], index=dates)
        fastline2 = pd.Series([0.1, -0.2, 0.3, -0.1, 0.2], index=dates)
        color1 = pd.Series([BUY, SELL, BUY, SELL, BUY], index=dates)
        color2 = pd.Series([BUY, SELL, BUY, SELL, BUY], index=dates)
        
        # What Prime actually does (preserves signals)
        prime_result = g_prime_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # What Reverse does (inverts signals)
        reverse_result = g_reverse_tr(wave1, wave2, fastline1, fastline2, color1, color2)
        
        # If user expects Prime to be "reversed", they might want Reverse behavior
        print(f"Prime result: {prime_result.values}")
        print(f"Reverse result: {reverse_result.values}")
        print(f"Original signals: {color1.values}")
        
        # Prime preserves: [BUY, SELL, BUY, SELL, BUY]
        # Reverse inverts: [SELL, BUY, SELL, BUY, SELL]
        # If user expects "reversed", they want Reverse behavior


if __name__ == "__main__":
    pytest.main([__file__])
