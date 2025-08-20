# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_wave_ind_comprehensive.py

"""
Comprehensive tests for Wave indicator with -d fastest parameter covering all possible input parameter variations.

This test suite covers:
1. All ENUM_MOM_TR trading rules (10 variations)
2. All ENUM_GLOBAL_TR global trading rules (7 variations)
3. Various period combinations
4. Different price types (OPEN, CLOSE)
5. Edge cases and boundary conditions
6. Error handling scenarios
7. Performance with different data sizes
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import plotly.graph_objects as go

from src.calculation.indicators.trend.wave_ind import (
    apply_rule_wave, WaveParameters, ENUM_MOM_TR, ENUM_GLOBAL_TR,
    calculate_ecore, calc_draw_lines, tr_switch, global_tr_switch,
    sma_calculation, init_wave
)
from src.calculation.indicators.base_indicator import PriceType
from src.common.constants import BUY, SELL, NOTRADE


class TestWaveIndicatorComprehensive:
    """Comprehensive test cases for Wave indicator with -d fastest parameter."""
    
    @pytest.fixture
    def sample_data(self):
        """Create comprehensive sample data for testing."""
        # Create larger dataset for comprehensive testing
        dates = pd.date_range('2024-01-01', periods=500, freq='D')
        
        # Create realistic price data with trends and volatility
        np.random.seed(42)  # For reproducible tests
        
        # Base trend
        trend = np.linspace(100, 150, 500)
        
        # Add volatility
        volatility = np.random.normal(0, 5, 500)
        
        # Add some cycles
        cycles = 10 * np.sin(np.linspace(0, 4*np.pi, 500))
        
        # Combine all components
        base_price = trend + volatility + cycles
        
        # Create OHLCV data
        df = pd.DataFrame({
            'Open': base_price + np.random.normal(0, 1, 500),
            'High': base_price + np.abs(np.random.normal(0, 3, 500)),
            'Low': base_price - np.abs(np.random.normal(0, 3, 500)),
            'Close': base_price + np.random.normal(0, 1, 500),
            'Volume': np.random.uniform(1000, 10000, 500)
        }, index=dates)
        
        # Ensure High >= Low
        df['High'] = df[['Open', 'Close', 'High']].max(axis=1) + np.abs(np.random.normal(0, 1, 500))
        df['Low'] = df[['Open', 'Close', 'Low']].min(axis=1) - np.abs(np.random.normal(0, 1, 500))
        
        return df
    
    @pytest.fixture
    def edge_case_data(self):
        """Create edge case data for testing boundary conditions."""
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        
        # Test cases with extreme values
        test_cases = [
            # All same values
            pd.DataFrame({
                'Open': [100.0] * 100,
                'High': [100.0] * 100,
                'Low': [100.0] * 100,
                'Close': [100.0] * 100,
                'Volume': [1000] * 100
            }, index=dates),
            
            # Very small values
            pd.DataFrame({
                'Open': [0.001] * 100,
                'High': [0.002] * 100,
                'Low': [0.0005] * 100,
                'Close': [0.001] * 100,
                'Volume': [1] * 100
            }, index=dates),
            
            # Very large values
            pd.DataFrame({
                'Open': [1000000.0] * 100,
                'High': [1000001.0] * 100,
                'Low': [999999.0] * 100,
                'Close': [1000000.0] * 100,
                'Volume': [1000000] * 100
            }, index=dates),
            
            # Data with NaN values
            pd.DataFrame({
                'Open': [100.0 if i % 10 != 0 else np.nan for i in range(100)],
                'High': [101.0 if i % 10 != 0 else np.nan for i in range(100)],
                'Low': [99.0 if i % 10 != 0 else np.nan for i in range(100)],
                'Close': [100.5 if i % 10 != 0 else np.nan for i in range(100)],
                'Volume': [1000 if i % 10 != 0 else np.nan for i in range(100)]
            }, index=dates)
        ]
        
        return test_cases
    
    def test_all_enum_mom_tr_variations(self, sample_data):
        """Test all ENUM_MOM_TR trading rule variations."""
        all_tr_rules = [
            ENUM_MOM_TR.TR_Fast,
            ENUM_MOM_TR.TR_Zone,
            ENUM_MOM_TR.TR_StrongTrend,
            ENUM_MOM_TR.TR_WeakTrend,
            ENUM_MOM_TR.TR_FastZoneReverse,
            ENUM_MOM_TR.TR_BetterTrend,
            ENUM_MOM_TR.TR_BetterFast,
            ENUM_MOM_TR.TR_Rost,
            ENUM_MOM_TR.TR_TrendRost,
            ENUM_MOM_TR.TR_BetterTrendRost
        ]
        
        for tr1 in all_tr_rules:
            for tr2 in all_tr_rules:
                # Create Wave parameters with current trading rules
                wave_params = WaveParameters(
                    long1=50, fast1=10, trend1=5, tr1=tr1,
                    long2=30, fast2=8, trend2=3, tr2=tr2,
                    global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
                )
                
                # Test with both price types
                for price_type in [PriceType.OPEN, PriceType.CLOSE]:
                    result_df = apply_rule_wave(sample_data.copy(), wave_params, price_type)
                    
                    # Verify required columns exist
                    required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
                    for col in required_cols:
                        assert col in result_df.columns, f"Missing column {col} for {tr1.name} + {tr2.name}"
                    
                    # Verify signal values are valid
                    valid_signals = [NOTRADE, BUY, SELL]
                    assert result_df['_Signal'].isin(valid_signals).all(), f"Invalid signals for {tr1.name} + {tr2.name}"
                    assert result_df['_Plot_Color'].isin(valid_signals).all(), f"Invalid plot colors for {tr1.name} + {tr2.name}"
                    
                    # Verify we have some data
                    assert len(result_df) > 0, f"No data generated for {tr1.name} + {tr2.name}"
                    
                    # Verify direction matches plot color
                    assert all(result_df['_Direction'] == result_df['_Plot_Color']), f"Direction mismatch for {tr1.name} + {tr2.name}"
    
    def test_all_enum_global_tr_variations(self, sample_data):
        """Test all ENUM_GLOBAL_TR global trading rule variations."""
        all_global_rules = [
            ENUM_GLOBAL_TR.G_TR_PRIME,
            ENUM_GLOBAL_TR.G_TR_REVERSE,
            ENUM_GLOBAL_TR.G_TR_PRIME_ZONE,
            ENUM_GLOBAL_TR.G_TR_REVERSE_ZONE,
            ENUM_GLOBAL_TR.G_TR_NEW_ZONE,
            ENUM_GLOBAL_TR.G_TR_LONG_ZONE,
            ENUM_GLOBAL_TR.G_TR_LONG_ZONE_REVERSE
        ]
        
        for global_tr in all_global_rules:
            # Create Wave parameters with current global rule
            wave_params = WaveParameters(
                long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
                long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
                global_tr=global_tr, sma_period=20
            )
            
            # Test with both price types
            for price_type in [PriceType.OPEN, PriceType.CLOSE]:
                result_df = apply_rule_wave(sample_data.copy(), wave_params, price_type)
                
                # Verify required columns exist
                required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
                for col in required_cols:
                    assert col in result_df.columns, f"Missing column {col} for {global_tr.name}"
                
                # Verify signal values are valid
                valid_signals = [NOTRADE, BUY, SELL]
                assert result_df['_Signal'].isin(valid_signals).all(), f"Invalid signals for {global_tr.name}"
                assert result_df['_Plot_Color'].isin(valid_signals).all(), f"Invalid plot colors for {global_tr.name}"
                
                # Verify we have some data
                assert len(result_df) > 0, f"No data generated for {global_tr.name}"
                
                # Verify direction matches plot color
                assert all(result_df['_Direction'] == result_df['_Plot_Color']), f"Direction mismatch for {global_tr.name}"
    
    def test_period_combinations(self, sample_data):
        """Test various period combinations."""
        period_combinations = [
            # Small periods
            (5, 2, 1, 3, 1, 1),
            # Medium periods
            (20, 10, 5, 15, 8, 3),
            # Large periods
            (100, 50, 25, 80, 40, 20),
            # Mixed periods
            (50, 5, 20, 30, 15, 2),
            # Very large periods
            (200, 100, 50, 150, 75, 30),
            # Edge case periods
            (1, 1, 1, 1, 1, 1),
            # Asymmetric periods
            (100, 10, 50, 20, 5, 10)
        ]
        
        for long1, fast1, trend1, long2, fast2, trend2 in period_combinations:
            wave_params = WaveParameters(
                long1=long1, fast1=fast1, trend1=trend1, tr1=ENUM_MOM_TR.TR_Fast,
                long2=long2, fast2=fast2, trend2=trend2, tr2=ENUM_MOM_TR.TR_Fast,
                global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
            )
            
            # Test with both price types
            for price_type in [PriceType.OPEN, PriceType.CLOSE]:
                result_df = apply_rule_wave(sample_data.copy(), wave_params, price_type)
                
                # Verify required columns exist
                required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
                for col in required_cols:
                    assert col in result_df.columns, f"Missing column {col} for periods {long1},{fast1},{trend1},{long2},{fast2},{trend2}"
                
                # Verify signal values are valid
                valid_signals = [NOTRADE, BUY, SELL]
                assert result_df['_Signal'].isin(valid_signals).all(), f"Invalid signals for periods {long1},{fast1},{trend1},{long2},{fast2},{trend2}"
                assert result_df['_Plot_Color'].isin(valid_signals).all(), f"Invalid plot colors for periods {long1},{fast1},{trend1},{long2},{fast2},{trend2}"
                
                # Verify we have some data
                assert len(result_df) > 0, f"No data generated for periods {long1},{fast1},{trend1},{long2},{fast2},{trend2}"
    
    def test_sma_period_variations(self, sample_data):
        """Test various SMA period values."""
        sma_periods = [1, 5, 10, 20, 50, 100, 200]
        
        for sma_period in sma_periods:
            wave_params = WaveParameters(
                long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
                long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
                global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=sma_period
            )
            
            # Test with both price types
            for price_type in [PriceType.OPEN, PriceType.CLOSE]:
                result_df = apply_rule_wave(sample_data.copy(), wave_params, price_type)
                
                # Verify MA_Line column exists and has valid values
                assert 'MA_Line' in result_df.columns, f"Missing MA_Line column for SMA period {sma_period}"
                assert result_df['MA_Line'].notna().any(), f"No valid MA_Line values for SMA period {sma_period}"
                
                # Verify signal values are valid
                valid_signals = [NOTRADE, BUY, SELL]
                assert result_df['_Signal'].isin(valid_signals).all(), f"Invalid signals for SMA period {sma_period}"
                assert result_df['_Plot_Color'].isin(valid_signals).all(), f"Invalid plot colors for SMA period {sma_period}"
    
    def test_edge_cases(self, edge_case_data):
        """Test edge cases and boundary conditions."""
        for i, test_df in enumerate(edge_case_data):
            wave_params = WaveParameters(
                long1=10, fast1=5, trend1=2, tr1=ENUM_MOM_TR.TR_Fast,
                long2=8, fast2=4, trend2=2, tr2=ENUM_MOM_TR.TR_Fast,
                global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=5
            )
            
            # Test with both price types
            for price_type in [PriceType.OPEN, PriceType.CLOSE]:
                try:
                    result_df = apply_rule_wave(test_df.copy(), wave_params, price_type)
                    
                    # Verify required columns exist
                    required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
                    for col in required_cols:
                        assert col in result_df.columns, f"Missing column {col} for edge case {i}"
                    
                    # Verify signal values are valid
                    valid_signals = [NOTRADE, BUY, SELL]
                    assert result_df['_Signal'].isin(valid_signals).all(), f"Invalid signals for edge case {i}"
                    assert result_df['_Plot_Color'].isin(valid_signals).all(), f"Invalid plot colors for edge case {i}"
                    
                    # Verify we have some data
                    assert len(result_df) > 0, f"No data generated for edge case {i}"
                    
                except Exception as e:
                    # Some edge cases might fail, which is expected
                    assert "Not enough data" in str(e) or "period must be positive" in str(e), f"Unexpected error for edge case {i}: {e}"
    
    def test_error_handling(self):
        """Test error handling for invalid parameters."""
        # Test with invalid periods - validation happens in init_wave function
        invalid_periods = [0, -1, -10]
        
        for period in invalid_periods:
            wave_params = WaveParameters(
                long1=period, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
                long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
                global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
            )
            
            # Create test data
            test_df = pd.DataFrame({
                'Open': [100.0] * 50,
                'High': [101.0] * 50,
                'Low': [99.0] * 50,
                'Close': [100.5] * 50,
                'Volume': [1000] * 50
            })
            
            # This should raise ValueError when init_wave is called
            with pytest.raises(ValueError, match="must be positive"):
                apply_rule_wave(test_df, wave_params, PriceType.OPEN)
        
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        wave_params = WaveParameters()
        
        with pytest.raises(KeyError):
            apply_rule_wave(empty_df, wave_params, PriceType.OPEN)
        
        # Test with insufficient data
        small_df = pd.DataFrame({
            'Open': [100.0] * 5,
            'High': [101.0] * 5,
            'Low': [99.0] * 5,
            'Close': [100.5] * 5,
            'Volume': [1000] * 5
        })
        
        # This should raise ValueError due to insufficient data for SMA
        with pytest.raises(ValueError, match="Not enough data points"):
            apply_rule_wave(small_df, wave_params, PriceType.OPEN)
    
    def test_performance_with_different_data_sizes(self):
        """Test performance with different data sizes."""
        data_sizes = [100, 500, 1000, 2000]
        
        for size in data_sizes:
            # Create data of specified size
            dates = pd.date_range('2024-01-01', periods=size, freq='D')
            test_df = pd.DataFrame({
                'Open': np.random.uniform(100, 200, size),
                'High': np.random.uniform(200, 300, size),
                'Low': np.random.uniform(50, 100, size),
                'Close': np.random.uniform(100, 200, size),
                'Volume': np.random.uniform(1000, 10000, size)
            }, index=dates)
            
            wave_params = WaveParameters(
                long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
                long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
                global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
            )
            
            # Test with both price types
            for price_type in [PriceType.OPEN, PriceType.CLOSE]:
                result_df = apply_rule_wave(test_df.copy(), wave_params, price_type)
                
                # Verify required columns exist
                required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
                for col in required_cols:
                    assert col in result_df.columns, f"Missing column {col} for data size {size}"
                
                # Verify signal values are valid
                valid_signals = [NOTRADE, BUY, SELL]
                assert result_df['_Signal'].isin(valid_signals).all(), f"Invalid signals for data size {size}"
                assert result_df['_Plot_Color'].isin(valid_signals).all(), f"Invalid plot colors for data size {size}"
                
                # Verify we have the expected amount of data
                assert len(result_df) == size, f"Data size mismatch for size {size}"
    
    def test_complex_parameter_combinations(self, sample_data):
        """Test complex parameter combinations that might be used in practice."""
        complex_combinations = [
            # Default recommended settings
            (339, 10, 2, ENUM_MOM_TR.TR_Fast, 22, 11, 4, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME, 22),
            # Short-term trading
            (50, 5, 2, ENUM_MOM_TR.TR_BetterFast, 20, 8, 3, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_REVERSE, 15),
            # Long-term trend following
            (200, 20, 10, ENUM_MOM_TR.TR_StrongTrend, 100, 15, 8, ENUM_MOM_TR.TR_BetterTrend, ENUM_GLOBAL_TR.G_TR_PRIME_ZONE, 50),
            # Aggressive trading
            (30, 3, 1, ENUM_MOM_TR.TR_Fast, 15, 5, 2, ENUM_MOM_TR.TR_BetterFast, ENUM_GLOBAL_TR.G_TR_NEW_ZONE, 10),
            # Conservative approach
            (500, 50, 25, ENUM_MOM_TR.TR_WeakTrend, 200, 25, 15, ENUM_MOM_TR.TR_StrongTrend, ENUM_GLOBAL_TR.G_TR_LONG_ZONE, 100),
            # Zone-based strategy
            (100, 10, 5, ENUM_MOM_TR.TR_Zone, 50, 8, 4, ENUM_MOM_TR.TR_FastZoneReverse, ENUM_GLOBAL_TR.G_TR_PRIME_ZONE, 25),
            # Reverse strategy
            (80, 8, 4, ENUM_MOM_TR.TR_Rost, 40, 6, 3, ENUM_MOM_TR.TR_TrendRost, ENUM_GLOBAL_TR.G_TR_REVERSE, 20),
            # Enhanced trend strategy
            (150, 15, 8, ENUM_MOM_TR.TR_BetterTrend, 75, 12, 6, ENUM_MOM_TR.TR_BetterTrendRost, ENUM_GLOBAL_TR.G_TR_LONG_ZONE_REVERSE, 30)
        ]
        
        for long1, fast1, trend1, tr1, long2, fast2, trend2, tr2, global_tr, sma_period in complex_combinations:
            wave_params = WaveParameters(
                long1=long1, fast1=fast1, trend1=trend1, tr1=tr1,
                long2=long2, fast2=fast2, trend2=trend2, tr2=tr2,
                global_tr=global_tr, sma_period=sma_period
            )
            
            # Test with both price types
            for price_type in [PriceType.OPEN, PriceType.CLOSE]:
                result_df = apply_rule_wave(sample_data.copy(), wave_params, price_type)
                
                # Verify required columns exist
                required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
                for col in required_cols:
                    assert col in result_df.columns, f"Missing column {col} for complex combination"
                
                # Verify signal values are valid
                valid_signals = [NOTRADE, BUY, SELL]
                assert result_df['_Signal'].isin(valid_signals).all(), f"Invalid signals for complex combination"
                assert result_df['_Plot_Color'].isin(valid_signals).all(), f"Invalid plot colors for complex combination"
                
                # Verify we have some data
                assert len(result_df) > 0, f"No data generated for complex combination"
                
                # Verify direction matches plot color
                assert all(result_df['_Direction'] == result_df['_Plot_Color']), f"Direction mismatch for complex combination"
                
                # Verify signal generation logic (signals only when direction changes)
                for i in range(1, len(result_df)):
                    if result_df['_Signal'].iloc[i] != NOTRADE:
                        assert result_df['_Direction'].iloc[i] != result_df['_Direction'].iloc[i-1], "Signal should only be generated when direction changes"
    
    def test_fastest_mode_compatibility(self, sample_data):
        """Test compatibility with -d fastest mode plotting."""
        from src.plotting.dual_chart_fastest import add_wave_indicator
        
        # Test with various parameter combinations
        test_combinations = [
            # Default settings
            (339, 10, 2, ENUM_MOM_TR.TR_Fast, 22, 11, 4, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME, 22),
            # Short periods
            (50, 5, 2, ENUM_MOM_TR.TR_Fast, 20, 8, 3, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME, 15),
            # Different trading rules
            (100, 10, 5, ENUM_MOM_TR.TR_StrongTrend, 50, 8, 4, ENUM_MOM_TR.TR_BetterTrend, ENUM_GLOBAL_TR.G_TR_REVERSE, 25)
        ]
        
        for long1, fast1, trend1, tr1, long2, fast2, trend2, tr2, global_tr, sma_period in test_combinations:
            wave_params = WaveParameters(
                long1=long1, fast1=fast1, trend1=trend1, tr1=tr1,
                long2=long2, fast2=fast2, trend2=trend2, tr2=tr2,
                global_tr=global_tr, sma_period=sma_period
            )
            
            # Test with both price types
            for price_type in [PriceType.OPEN, PriceType.CLOSE]:
                result_df = apply_rule_wave(sample_data.copy(), wave_params, price_type)
                
                # Create mock figure for fastest mode plotting
                mock_fig = Mock()
                
                # Test fastest mode plotting
                add_wave_indicator(mock_fig, result_df)
                
                # Verify that add_trace was called (indicating lines were added)
                assert mock_fig.add_trace.called, f"add_trace should be called for fastest mode with parameters {long1},{fast1},{trend1},{tr1.name},{long2},{fast2},{trend2},{tr2.name},{global_tr.name},{sma_period}"
                
                # Get all calls to add_trace
                calls = mock_fig.add_trace.call_args_list
                
                # Should have at least some traces added
                assert len(calls) > 0, f"No traces added for fastest mode with parameters {long1},{fast1},{trend1},{tr1.name},{long2},{fast2},{trend2},{tr2.name},{global_tr.name},{sma_period}"
                
                # Check that traces have valid data
                for call in calls:
                    args, kwargs = call
                    trace = args[0]  # First argument is the trace
                    
                    # Check that trace has valid data
                    if hasattr(trace, 'x') and hasattr(trace, 'y'):
                        # x and y should not be empty
                        assert len(trace.x) > 0, f"Trace x data should not be empty for fastest mode"
                        assert len(trace.y) > 0, f"Trace y data should not be empty for fastest mode"
    
    def test_signal_consistency(self, sample_data):
        """Test signal consistency across different parameter combinations."""
        # Test that signals are consistent with the trading rules
        test_cases = [
            # Fast rule should generate signals based on wave vs fastline comparison
            (ENUM_MOM_TR.TR_Fast, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME),
            # Zone rule should generate signals based on wave > 0 or < 0
            (ENUM_MOM_TR.TR_Zone, ENUM_MOM_TR.TR_Zone, ENUM_GLOBAL_TR.G_TR_PRIME),
            # Strong trend should be more selective
            (ENUM_MOM_TR.TR_StrongTrend, ENUM_MOM_TR.TR_StrongTrend, ENUM_GLOBAL_TR.G_TR_PRIME),
            # Better trend should avoid false signals
            (ENUM_MOM_TR.TR_BetterTrend, ENUM_MOM_TR.TR_BetterTrend, ENUM_GLOBAL_TR.G_TR_PRIME)
        ]
        
        for tr1, tr2, global_tr in test_cases:
            wave_params = WaveParameters(
                long1=50, fast1=10, trend1=5, tr1=tr1,
                long2=30, fast2=8, trend2=3, tr2=tr2,
                global_tr=global_tr, sma_period=20
            )
            
            result_df = apply_rule_wave(sample_data.copy(), wave_params, PriceType.OPEN)
            
            # Verify signal consistency
            valid_signals = [NOTRADE, BUY, SELL]
            assert result_df['_Signal'].isin(valid_signals).all(), f"Invalid signals for {tr1.name} + {tr2.name} + {global_tr.name}"
            assert result_df['_Plot_Color'].isin(valid_signals).all(), f"Invalid plot colors for {tr1.name} + {tr2.name} + {global_tr.name}"
            
            # Verify that signals are only generated when direction changes
            for i in range(1, len(result_df)):
                if result_df['_Signal'].iloc[i] != NOTRADE:
                    assert result_df['_Direction'].iloc[i] != result_df['_Direction'].iloc[i-1], f"Signal should only be generated when direction changes for {tr1.name} + {tr2.name} + {global_tr.name}"
            
            # Verify direction matches plot color
            assert all(result_df['_Direction'] == result_df['_Plot_Color']), f"Direction should match plot color for {tr1.name} + {tr2.name} + {global_tr.name}"


if __name__ == "__main__":
    # Run comprehensive tests
    test_instance = TestWaveIndicatorComprehensive()
    
    print("🧪 Running comprehensive Wave indicator tests for -d fastest mode...")
    
    # Create sample data
    sample_data = test_instance.sample_data()
    
    print("✅ Sample data created")
    
    # Run all test methods
    test_methods = [
        test_instance.test_all_enum_mom_tr_variations,
        test_instance.test_all_enum_global_tr_variations,
        test_instance.test_period_combinations,
        test_instance.test_sma_period_variations,
        test_instance.test_edge_cases,
        test_instance.test_error_handling,
        test_instance.test_performance_with_different_data_sizes,
        test_instance.test_complex_parameter_combinations,
        test_instance.test_fastest_mode_compatibility,
        test_instance.test_signal_consistency
    ]
    
    for test_method in test_methods:
        try:
            test_method()
            print(f"✅ {test_method.__name__} passed")
        except Exception as e:
            print(f"❌ {test_method.__name__} failed: {e}")
    
    print("\n🎯 Comprehensive Wave indicator tests completed!")
    print("📊 Test coverage includes:")
    print("   - All 10 ENUM_MOM_TR trading rules")
    print("   - All 7 ENUM_GLOBAL_TR global trading rules")
    print("   - Various period combinations")
    print("   - Different price types (OPEN, CLOSE)")
    print("   - Edge cases and boundary conditions")
    print("   - Error handling scenarios")
    print("   - Performance with different data sizes")
    print("   - Complex parameter combinations")
    print("   - Fastest mode compatibility")
    print("   - Signal consistency validation")
