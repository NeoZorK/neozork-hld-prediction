# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_schr_wave2_ind.py

"""
Test module for SCHR_Wave2 indicator.
Tests all major functionality including calculation, trading rules, and signal generation.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.calculation.indicators.trend.schr_wave2_ind import (
    SCHRWave2Indicator,
    calculate_schr_wave2,
    apply_rule_schr_wave2,
    get_trading_rule_enum,
    get_global_trading_rule_enum,
    calculate_ecore,
    calculate_draw_lines,
    apply_trading_rule,
    apply_global_trading_rule,
    calculate_sma
)


class TestSCHRWave2Indicator:
    """Test class for SCHR_Wave2 indicator functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        np.random.seed(42)  # For reproducible results
        
        # Generate realistic price data
        base_price = 100.0
        returns = np.random.normal(0, 0.02, 100)  # 2% daily volatility
        prices = [base_price]
        
        for ret in returns[1:]:
            new_price = prices[-1] * (1 + ret)
            prices.append(new_price)
        
        data = {
            'Open': prices,
            'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            'Close': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
            'Volume': np.random.randint(1000, 10000, 100)
        }
        
        df = pd.DataFrame(data, index=dates)
        # Ensure High >= Low and High >= Open, Close
        df['High'] = df[['Open', 'Close', 'High']].max(axis=1)
        df['Low'] = df[['Open', 'Close', 'Low']].min(axis=1)
        
        return df
    
    def test_trading_rule_enum_conversion(self):
        """Test trading rule enum conversion functions."""
        # Test string to enum conversion
        assert get_trading_rule_enum('fast') == 0
        assert get_trading_rule_enum('zone') == 1
        assert get_trading_rule_enum('strongtrend') == 2
        assert get_trading_rule_enum('weaktrend') == 3
        
        # Test integer enum values
        assert get_trading_rule_enum(0) == 0
        assert get_trading_rule_enum(1) == 1
        
        # Test default fallback
        assert get_trading_rule_enum('unknown') == 0
    
    def test_global_trading_rule_enum_conversion(self):
        """Test global trading rule enum conversion functions."""
        # Test string to enum conversion
        assert get_global_trading_rule_enum('prime') == 0
        assert get_global_trading_rule_enum('reverse') == 1
        assert get_global_trading_rule_enum('primezone') == 2
        
        # Test integer enum values
        assert get_global_trading_rule_enum(0) == 0
        assert get_global_trading_rule_enum(1) == 1
        
        # Test default fallback
        assert get_global_trading_rule_enum('unknown') == 0
    
    def test_calculate_ecore(self, sample_data):
        """Test ECORE calculation function."""
        open_prices = sample_data['Open']
        div = 2.0 / 10  # For period 10
        
        ecore = calculate_ecore(open_prices, div)
        
        assert len(ecore) == len(open_prices)
        assert ecore.iloc[0] == 0.0  # First value should be 0
        assert not ecore.isna().any()  # No NaN values
        assert isinstance(ecore.iloc[1], float)  # Should be numeric
    
    def test_calculate_draw_lines(self, sample_data):
        """Test Wave and FastLine calculation."""
        open_prices = sample_data['Open']
        div_fast = 2.0 / 10
        div_dir = 2.0 / 3
        
        ecore = calculate_ecore(open_prices, div_fast)
        wave, fast_line = calculate_draw_lines(ecore, div_fast, div_dir)
        
        assert len(wave) == len(open_prices)
        assert len(fast_line) == len(open_prices)
        assert wave.iloc[0] == 0.0  # First values should be 0
        assert fast_line.iloc[0] == 0.0
        assert not wave.isna().any()
        assert not fast_line.isna().any()
    
    def test_apply_trading_rule(self, sample_data):
        """Test trading rule application."""
        open_prices = sample_data['Open']
        div_fast = 2.0 / 10
        div_dir = 2.0 / 3
        
        ecore = calculate_ecore(open_prices, div_fast)
        wave, fast_line = calculate_draw_lines(ecore, div_fast, div_dir)
        
        # Test Fast rule
        color = apply_trading_rule(wave, fast_line, 0)  # TR_FAST
        assert len(color) == len(open_prices)
        assert color.iloc[0] == 0  # First value should be NOTRADE
        assert all(val in [0, 1, 2] for val in color.dropna())  # Valid signal values
        
        # Test Zone rule
        color_zone = apply_trading_rule(wave, fast_line, 1)  # TR_ZONE
        assert len(color_zone) == len(open_prices)
        assert all(val in [0, 1, 2] for val in color_zone.dropna())
    
    def test_apply_global_trading_rule(self, sample_data):
        """Test global trading rule application."""
        open_prices = sample_data['Open']
        div_fast = 2.0 / 10
        div_dir = 2.0 / 3
        
        ecore = calculate_ecore(open_prices, div_fast)
        wave, fast_line = calculate_draw_lines(ecore, div_fast, div_dir)
        
        color1 = apply_trading_rule(wave, fast_line, 0)  # TR_FAST
        color2 = apply_trading_rule(wave, fast_line, 1)  # TR_ZONE
        
        # Test Prime rule
        final_color, final_wave, final_fast_line = apply_global_trading_rule(
            color1, color2, wave, 0  # G_TR_PRIME
        )
        
        assert len(final_color) == len(open_prices)
        assert len(final_wave) == len(open_prices)
        assert len(final_fast_line) == len(open_prices)
        assert all(val in [0, 1, 2] for val in final_color.dropna())
    
    def test_calculate_sma(self, sample_data):
        """Test SMA calculation function."""
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        period = 3
        
        sma = calculate_sma(data, period)
        
        assert len(sma) == len(data)
        assert sma.iloc[0] == 1.0  # First value should be the same
        assert sma.iloc[2] == 2.0  # Third value should be average of first 3
        assert not sma.isna().any()
    
    def test_calculate_schr_wave2(self, sample_data):
        """Test main SCHR Wave2 calculation function."""
        result = calculate_schr_wave2(
            sample_data,
            long1=20, fast1=5, trend1=2, tr1='Fast',
            long2=10, fast2=3, trend2=2, tr2='Fast',
            global_tr='Prime', sma_period=5
        )
        
        # Check that all expected columns are present
        expected_columns = [
            'schr_wave2_wave', 'schr_wave2_fast_line', 'schr_wave2_ma_line',
            'schr_wave2_direction', 'schr_wave2_signal',
            'schr_wave2_wave1', 'schr_wave2_wave2',
            'schr_wave2_fast_line1', 'schr_wave2_fast_line2',
            'schr_wave2_color1', 'schr_wave2_color2'
        ]
        
        for col in expected_columns:
            assert col in result.columns, f"Column {col} not found in result"
        
        # Check data integrity
        assert len(result) == len(sample_data)
        assert not result['schr_wave2_wave'].isna().all()  # Should have some valid values
        assert not result['schr_wave2_signal'].isna().all()
    
    def test_schr_wave2_indicator_class(self, sample_data):
        """Test SCHRWave2Indicator class functionality."""
        indicator = SCHRWave2Indicator(
            long1=20, fast1=5, trend1=2, tr1='Fast',
            long2=10, fast2=3, trend2=2, tr2='Fast',
            global_tr='Prime', sma_period=5
        )
        
        # Test calculation
        result = indicator.calculate(sample_data)
        assert 'schr_wave2_wave' in result.columns
        assert 'schr_wave2_signal' in result.columns
        
        # Test apply_rule
        result_rule = indicator.apply_rule(sample_data, point=0.00001)
        assert 'PPrice1' in result_rule.columns
        assert 'PColor1' in result_rule.columns
        assert 'PPrice2' in result_rule.columns
        assert 'PColor2' in result_rule.columns
        assert 'Direction' in result_rule.columns
        assert 'Diff' in result_rule.columns
    
    def test_apply_rule_schr_wave2(self, sample_data):
        """Test apply_rule_schr_wave2 function."""
        result = apply_rule_schr_wave2(
            sample_data,
            point=0.00001,
            long1=20, fast1=5, trend1=2, tr1='Fast',
            long2=10, fast2=3, trend2=2, tr2='Fast',
            global_tr='Prime', sma_period=5
        )
        
        # Check output columns
        expected_outputs = ['PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff']
        for col in expected_outputs:
            assert col in result.columns, f"Output column {col} not found"
        
        # Check data integrity
        assert len(result) == len(sample_data)
        assert not result['PPrice1'].isna().all()
        assert not result['Direction'].isna().all()
    
    def test_edge_cases(self, sample_data):
        """Test edge cases and error handling."""
        # Test with insufficient data
        small_data = sample_data.head(5)  # Less than minimum required periods
        
        result = calculate_schr_wave2(
            small_data,
            long1=20, fast1=5, trend1=2, tr1='Fast',
            long2=10, fast2=3, trend2=2, tr2='Fast',
            global_tr='Prime', sma_period=5
        )
        
        # Should return original data when insufficient
        assert len(result) == len(small_data)
        assert 'schr_wave2_wave' not in result.columns  # No calculation performed
    
    def test_parameter_validation(self):
        """Test parameter validation and edge cases."""
        # Test with zero periods (should handle gracefully)
        indicator = SCHRWave2Indicator(
            long1=0, fast1=0, trend1=0, tr1='Fast',
            long2=0, fast2=0, trend2=0, tr2='Fast',
            global_tr='Prime', sma_period=0
        )
        
        # Should not raise errors during initialization
        assert indicator.long1 == 0
        assert indicator.fast1 == 0
        assert indicator.trend1 == 0
    
    def test_trading_rule_combinations(self, sample_data):
        """Test different trading rule combinations."""
        # Test different trading rule combinations
        rules_to_test = [
            ('Fast', 'Zone', 'Prime'),
            ('Zone', 'StrongTrend', 'Reverse'),
            ('WeakTrend', 'Fast', 'PrimeZone')
        ]
        
        for tr1, tr2, global_tr in rules_to_test:
            result = calculate_schr_wave2(
                sample_data,
                long1=20, fast1=5, trend1=2, tr1=tr1,
                long2=10, fast2=3, trend2=2, tr2=tr2,
                global_tr=global_tr, sma_period=5
            )
            
            # Should complete without errors
            assert len(result) == len(sample_data)
            assert 'schr_wave2_signal' in result.columns
    
    def test_signal_generation(self, sample_data):
        """Test signal generation logic."""
        result = calculate_schr_wave2(
            sample_data,
            long1=20, fast1=5, trend1=2, tr1='Fast',
            long2=10, fast2=3, trend2=2, tr2='Fast',
            global_tr='Prime', sma_period=5
        )
        
        # Check signal values
        signals = result['schr_wave2_signal']
        assert all(val in [0, 1, 2] for val in signals.dropna())  # Valid signal values
        
        # Check direction values
        directions = result['schr_wave2_direction']
        assert all(val in [0, 1, 2] for val in directions.dropna())  # Valid direction values
        
        # Check that signals are generated when direction changes
        direction_changes = directions.diff() != 0
        signal_points = signals != 0
        
        # Most direction changes should have corresponding signals
        # (allowing for some edge cases at boundaries)
        assert signal_points.sum() > 0  # Should have some signals
