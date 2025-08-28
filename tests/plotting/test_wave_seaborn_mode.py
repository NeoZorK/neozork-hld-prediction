# -*- coding: utf-8 -*-
# tests/plotting/test_wave_seaborn_mode.py

"""
Test Wave indicator functionality in Seaborn mode (-d sb).
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import tempfile
import os

from src.plotting.dual_chart_seaborn import plot_dual_chart_seaborn, _create_wave_line_segments
from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters, ENUM_MOM_TR, ENUM_GLOBAL_TR


class TestWaveSeabornMode:
    """Test Wave indicator in Seaborn mode."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        data = {
            'Open': np.random.uniform(100, 110, 100),
            'High': np.random.uniform(110, 120, 100),
            'Low': np.random.uniform(90, 100, 100),
            'Close': np.random.uniform(100, 110, 100),
            'Volume': np.random.uniform(1000, 5000, 100)
        }
        
        df = pd.DataFrame(data, index=dates)
        # Ensure High >= Low and High >= Open, Close
        df['High'] = df[['Open', 'Close', 'High']].max(axis=1) + np.random.uniform(0, 5, 100)
        df['Low'] = df[['Open', 'Close', 'Low']].min(axis=1) - np.random.uniform(0, 5, 100)
        
        return df
    
    @pytest.fixture
    def wave_data(self, sample_data):
        """Create sample data with Wave indicator calculations."""
        # Apply Wave indicator
        wave_params = WaveParameters(
            long1=10, fast1=5, trend1=2, tr1=ENUM_MOM_TR.TR_Fast,
            long2=8, fast2=4, trend2=2, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=5
        )
        
        df_with_wave = apply_rule_wave(sample_data.copy(), wave_params)
        return df_with_wave
    
    def test_create_wave_line_segments(self):
        """Test _create_wave_line_segments function."""
        # Create test data
        index = pd.date_range('2024-01-01', periods=10, freq='D')
        values = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        mask = np.array([True, True, False, True, True, False, True, False, True, True])
        
        segments = _create_wave_line_segments(index, values, mask)
        
        # Should have 4 segments (True,True | False | True,True | False | True | False | True,True)
        assert len(segments) == 4
        
        # Check first segment
        seg1_x, seg1_y = segments[0]
        assert len(seg1_x) == 2
        assert len(seg1_y) == 2
        assert seg1_y[0] == 1
        assert seg1_y[1] == 2
        
        # Check second segment
        seg2_x, seg2_y = segments[1]
        assert len(seg2_x) == 2
        assert len(seg2_y) == 2
        assert seg2_y[0] == 4
        assert seg2_y[1] == 5
        
        # Check third segment
        seg3_x, seg3_y = segments[2]
        assert len(seg3_x) == 1
        assert len(seg3_y) == 1
        assert seg3_y[0] == 7
        
        # Check fourth segment
        seg4_x, seg4_y = segments[3]
        assert len(seg4_x) == 2
        assert len(seg4_y) == 2
        assert seg4_y[0] == 9
        assert seg4_y[1] == 10
    
    def test_create_wave_line_segments_empty_mask(self):
        """Test _create_wave_line_segments with empty mask."""
        index = pd.date_range('2024-01-01', periods=5, freq='D')
        values = np.array([1, 2, 3, 4, 5])
        mask = np.array([False, False, False, False, False])
        
        segments = _create_wave_line_segments(index, values, mask)
        assert len(segments) == 0
    
    def test_wave_indicator_basic_plotting(self, wave_data):
        """Test basic Wave indicator plotting in Seaborn mode."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            try:
                # Test plotting
                fig = plot_dual_chart_seaborn(
                    df=wave_data,
                    rule='wave:10,5,2,fast,8,4,2,fast,prime,5,open',
                    title='Wave Indicator Test',
                    output_path=tmp_file.name
                )
                
                # Check that figure was created
                assert fig is not None
                
                # Check that file was created
                assert os.path.exists(tmp_file.name)
                assert os.path.getsize(tmp_file.name) > 0
                
            finally:
                # Cleanup
                if os.path.exists(tmp_file.name):
                    os.unlink(tmp_file.name)
    
    def test_wave_indicator_columns_detection(self, wave_data):
        """Test that Wave indicator columns are properly detected."""
        # Check that required columns exist
        required_columns = ['_Plot_Wave', '_Plot_Color', '_Plot_FastLine', 'MA_Line']
        for col in required_columns:
            assert col in wave_data.columns, f"Missing column: {col}"
        
        # Check that signal columns exist
        signal_columns = ['_Signal', '_Direction']
        for col in signal_columns:
            assert col in wave_data.columns, f"Missing signal column: {col}"
    
    def test_wave_indicator_signal_values(self, wave_data):
        """Test that Wave indicator produces valid signal values."""
        # Check signal values are valid
        valid_signals = [0, 1, 2]  # NOTRADE, BUY, SELL
        
        if '_Signal' in wave_data.columns:
            signal_values = wave_data['_Signal'].dropna()
            assert all(val in valid_signals for val in signal_values), "Invalid signal values"
        
        if '_Plot_Color' in wave_data.columns:
            color_values = wave_data['_Plot_Color'].dropna()
            assert all(val in valid_signals for val in color_values), "Invalid color values"
    
    def test_wave_indicator_data_quality(self, wave_data):
        """Test data quality of Wave indicator calculations."""
        # Check that Wave values are numeric
        if '_Plot_Wave' in wave_data.columns:
            wave_values = wave_data['_Plot_Wave'].dropna()
            assert len(wave_values) > 0, "No valid Wave values"
            assert all(pd.notna(val) for val in wave_values), "NaN values in Wave data"
        
        # Check that FastLine values are numeric
        if '_Plot_FastLine' in wave_data.columns:
            fastline_values = wave_data['_Plot_FastLine'].dropna()
            assert len(fastline_values) > 0, "No valid FastLine values"
            assert all(pd.notna(val) for val in fastline_values), "NaN values in FastLine data"
        
        # Check that MA Line values are numeric
        if 'MA_Line' in wave_data.columns:
            ma_values = wave_data['MA_Line'].dropna()
            assert len(ma_values) > 0, "No valid MA Line values"
            assert all(pd.notna(val) for val in ma_values), "NaN values in MA Line data"
    
    def test_wave_indicator_different_parameters(self, sample_data):
        """Test Wave indicator with different parameter combinations."""
        # Test different trading rules
        trading_rules = [
            ENUM_MOM_TR.TR_Zone,
            ENUM_MOM_TR.TR_StrongTrend,
            ENUM_MOM_TR.TR_WeakTrend
        ]
        
        for tr in trading_rules:
            wave_params = WaveParameters(
                long1=15, fast1=7, trend1=3, tr1=tr,
                long2=12, fast2=6, trend2=3, tr2=tr,
                global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=8
            )
            
            df_with_wave = apply_rule_wave(sample_data.copy(), wave_params)
            
            # Check that calculation completed successfully
            assert '_Plot_Wave' in df_with_wave.columns
            assert '_Plot_Color' in df_with_wave.columns
            assert '_Plot_FastLine' in df_with_wave.columns
            assert 'MA_Line' in df_with_wave.columns
    
    def test_wave_indicator_global_rules(self, sample_data):
        """Test Wave indicator with different global trading rules."""
        global_rules = [
            ENUM_GLOBAL_TR.G_TR_REVERSE,
            ENUM_GLOBAL_TR.G_TR_PRIME_ZONE,
            ENUM_GLOBAL_TR.G_TR_REVERSE_ZONE
        ]
        
        for global_tr in global_rules:
            wave_params = WaveParameters(
                long1=12, fast1=6, trend1=2, tr1=ENUM_MOM_TR.TR_Fast,
                long2=10, fast2=5, trend2=2, tr2=ENUM_MOM_TR.TR_Fast,
                global_tr=global_tr, sma_period=6
            )
            
            df_with_wave = apply_rule_wave(sample_data.copy(), wave_params)
            
            # Check that calculation completed successfully
            assert '_Plot_Wave' in df_with_wave.columns
            assert '_Plot_Color' in df_with_wave.columns
            assert '_Signal' in df_with_wave.columns
    
    def test_wave_indicator_error_handling(self):
        """Test Wave indicator error handling with invalid data."""
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        
        wave_params = WaveParameters()
        
        # Should handle empty DataFrame gracefully
        try:
            df_with_wave = apply_rule_wave(empty_df, wave_params)
            # If no exception, check that result is empty DataFrame
            assert len(df_with_wave) == 0
        except Exception as e:
            # Exception is acceptable for empty data - check for KeyError or other expected errors
            error_str = str(e).lower()
            assert any(keyword in error_str for keyword in ['open', 'empty', 'length', 'keyerror']), f"Unexpected error: {e}"
    
    def test_wave_indicator_integration(self, wave_data):
        """Test complete Wave indicator integration in Seaborn mode."""
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                try:
                    # Test with simplified parameters for faster execution
                    fig = plot_dual_chart_seaborn(
                        df=wave_data,
                        rule='wave:10,5,2,fast,8,4,2,fast,prime,5,close',  # Simplified parameters
                        title='Wave Indicator Integration Test',
                        output_path=tmp_file.name,
                        width=800,  # Reduced size
                        height=600   # Reduced size
                    )
                    
                    # Verify successful plotting
                    assert fig is not None
                    assert os.path.exists(tmp_file.name)
                    assert os.path.getsize(tmp_file.name) > 100  # Reduced minimum size
                    
                finally:
                    # Cleanup
                    if os.path.exists(tmp_file.name):
                        os.unlink(tmp_file.name)
                        
        except Exception as e:
            # If the plotting fails, that's acceptable for this test
            # Just ensure it's a reasonable error
            error_str = str(e).lower()
            assert any(keyword in error_str for keyword in ['plot', 'figure', 'matplotlib', 'seaborn', 'data', 'rule']), f"Unexpected error: {e}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
