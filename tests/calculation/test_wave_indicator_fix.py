#!/usr/bin/env python3
"""
Test for Wave indicator fix - ensures that Wave indicator generates signals correctly.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.calculation.indicators.trend.wave_ind import (
    apply_rule_wave, WaveParameters, ENUM_MOM_TR, ENUM_GLOBAL_TR
)
from src.calculation.indicators.base_indicator import PriceType
from src.common.constants import BUY, SELL, NOTRADE


class TestWaveIndicatorFix:
    """Test cases for Wave indicator fix."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample trading data for testing."""
        dates = pd.date_range('2023-01-01', periods=400, freq='D')
        np.random.seed(42)
        
        # Generate realistic price data
        base_price = 1.5
        returns = np.random.normal(0.0001, 0.02, 400)  # Daily returns
        prices = [base_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        # Generate OHLCV data
        df = pd.DataFrame({
            'Open': prices,
            'High': [p * 1.01 for p in prices],
            'Low': [p * 0.99 for p in prices],
            'Close': prices,
            'Volume': np.random.randint(1000, 10000, 400)
        }, index=dates)
        
        return df
    
    @pytest.fixture
    def wave_params(self):
        """Create Wave parameters for testing."""
        return WaveParameters(
            long1=339,
            fast1=10,
            trend1=2,
            tr1=ENUM_MOM_TR.TR_Fast,
            long2=22,
            fast2=11,
            trend2=4,
            tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME,
            sma_period=55
        )
    
    def test_wave_indicator_generates_signals(self, sample_data, wave_params):
        """Test that Wave indicator generates signals correctly."""
        # Apply Wave indicator
        result_df = apply_rule_wave(sample_data, wave_params, PriceType.OPEN)
        
        # Check that required columns are created
        required_columns = [
            '_Signal', '_Direction', '_LastSignal',
            'ecore1', 'ecore2', 'wave1', 'fastline1', 'wave2', 'fastline2',
            'Wave1', 'Wave2', '_Plot_Color', '_Plot_Wave', '_Plot_FastLine', 'MA_Line'
        ]
        
        for col in required_columns:
            assert col in result_df.columns, f"Required column '{col}' not found"
        
        # Check that signals are generated
        signal_counts = result_df['_Signal'].value_counts()
        assert len(signal_counts) > 0, "No signals generated"
        
        # Check that we have some non-zero signals
        non_zero_signals = result_df[result_df['_Signal'] != NOTRADE]
        assert len(non_zero_signals) > 0, "No non-zero signals generated"
        
        # Check signal values are valid
        valid_signals = [NOTRADE, BUY, SELL]
        for signal in result_df['_Signal'].unique():
            assert signal in valid_signals, f"Invalid signal value: {signal}"
    
    def test_wave_indicator_signal_distribution(self, sample_data, wave_params):
        """Test that Wave indicator generates reasonable signal distribution."""
        # Apply Wave indicator
        result_df = apply_rule_wave(sample_data, wave_params, PriceType.OPEN)
        
        # Check signal distribution
        signal_counts = result_df['_Signal'].value_counts()
        
        # Should have some BUY and SELL signals
        assert BUY in signal_counts.index, "No BUY signals generated"
        assert SELL in signal_counts.index, "No SELL signals generated"
        
        # Check that signals are not all the same
        assert len(signal_counts) > 1, "All signals are the same"
        
        # Check that we have reasonable number of signals (not too many, not too few)
        total_signals = signal_counts[BUY] + signal_counts[SELL]
        assert 10 <= total_signals <= len(result_df) * 0.3, f"Unreasonable number of signals: {total_signals}"
    
    def test_wave_indicator_wave_values(self, sample_data, wave_params):
        """Test that Wave indicator generates valid wave values."""
        # Apply Wave indicator
        result_df = apply_rule_wave(sample_data, wave_params, PriceType.OPEN)
        
        # Check wave values are not all NaN
        wave_columns = ['wave1', 'wave2', 'fastline1', 'fastline2']
        for col in wave_columns:
            assert not result_df[col].isna().all(), f"All values in {col} are NaN"
            assert len(result_df[col].dropna()) > 0, f"No valid values in {col}"
    
    def test_wave_indicator_individual_signals(self, sample_data, wave_params):
        """Test that individual wave signals are generated correctly."""
        # Apply Wave indicator
        result_df = apply_rule_wave(sample_data, wave_params, PriceType.OPEN)
        
        # Check individual wave signals
        wave1_signals = result_df['Wave1'].value_counts()
        wave2_signals = result_df['Wave2'].value_counts()
        
        # Both waves should generate signals
        assert len(wave1_signals) > 0, "Wave1 generated no signals"
        assert len(wave2_signals) > 0, "Wave2 generated no signals"
        
        # Check that both waves have BUY and SELL signals
        for wave_signals in [wave1_signals, wave2_signals]:
            assert BUY in wave_signals.index, "No BUY signals in individual wave"
            assert SELL in wave_signals.index, "No SELL signals in individual wave"
    
    def test_wave_indicator_global_signals(self, sample_data, wave_params):
        """Test that global signal combination works correctly."""
        # Apply Wave indicator
        result_df = apply_rule_wave(sample_data, wave_params, PriceType.OPEN)
        
        # Check global signal combination
        plot_color_signals = result_df['_Plot_Color'].value_counts()
        
        # Should have some combined signals
        assert len(plot_color_signals) > 0, "No global signals generated"
        
        # Check that global signals are valid
        valid_signals = [NOTRADE, BUY, SELL]
        for signal in result_df['_Plot_Color'].unique():
            assert signal in valid_signals, f"Invalid global signal value: {signal}"
    
    def test_wave_indicator_signal_consistency(self, sample_data, wave_params):
        """Test that signal generation is consistent."""
        # Apply Wave indicator multiple times
        result1 = apply_rule_wave(sample_data, wave_params, PriceType.OPEN)
        result2 = apply_rule_wave(sample_data, wave_params, PriceType.OPEN)
        
        # Results should be identical
        pd.testing.assert_frame_equal(result1, result2, check_dtype=False)
    
    def test_wave_indicator_with_different_parameters(self, sample_data):
        """Test Wave indicator with different parameters."""
        # Test with different trading rules
        params = WaveParameters(
            long1=100,
            fast1=5,
            trend1=1,
            tr1=ENUM_MOM_TR.TR_Zone,
            long2=20,
            fast2=10,
            trend2=2,
            tr2=ENUM_MOM_TR.TR_StrongTrend,
            global_tr=ENUM_GLOBAL_TR.G_TR_REVERSE,
            sma_period=20
        )
        
        result_df = apply_rule_wave(sample_data, params, PriceType.CLOSE)
        
        # Should still generate signals
        signal_counts = result_df['_Signal'].value_counts()
        assert len(signal_counts) > 0, "No signals generated with different parameters"
        
        # Should have non-zero signals
        non_zero_signals = result_df[result_df['_Signal'] != NOTRADE]
        assert len(non_zero_signals) > 0, "No non-zero signals with different parameters"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
