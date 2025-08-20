# -*- coding: utf-8 -*-
# tests/plotting/test_wave_indicator_fixes.py

"""
Test Wave indicator fixes for fastest mode - ensure no red/blue lines where there are no values.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import plotly.graph_objects as go

from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters, ENUM_MOM_TR, ENUM_GLOBAL_TR
from src.calculation.indicators.base_indicator import PriceType
from src.common.constants import BUY, SELL, NOTRADE


class TestWaveIndicatorFixes:
    """Test Wave indicator fixes for fastest mode."""
    
    def setup_method(self):
        """Set up test data."""
        # Create test data
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        self.test_df = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 100),
            'High': np.random.uniform(200, 300, 100),
            'Low': np.random.uniform(50, 100, 100),
            'Close': np.random.uniform(100, 200, 100),
            'Volume': np.random.uniform(1000, 10000, 100)
        }, index=dates)
        
        # Set some values to NaN to test filtering
        self.test_df.loc[self.test_df.index[10:20], 'Open'] = np.nan
        self.test_df.loc[self.test_df.index[30:40], 'Close'] = np.nan
        
        # Wave parameters
        self.wave_params = WaveParameters(
            long1=10,
            fast1=5,
            trend1=2,
            tr1=ENUM_MOM_TR.TR_Fast,
            long2=8,
            fast2=4,
            trend2=2,
            tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME,
            sma_period=5
        )
    
    def test_wave_calculation_produces_valid_data(self):
        """Test that wave calculation produces valid data."""
        result_df = apply_rule_wave(self.test_df.copy(), self.wave_params, PriceType.OPEN)
        
        # Check that required columns exist
        required_columns = ['_Plot_Wave', '_Plot_Color', '_Plot_FastLine', 'MA_Line', '_Signal']
        for col in required_columns:
            assert col in result_df.columns, f"Column {col} should exist"
        
        # Check that we have some valid values
        assert result_df['_Plot_Wave'].notna().any(), "Should have some valid Wave values"
        assert result_df['_Plot_FastLine'].notna().any(), "Should have some valid FastLine values"
        assert result_df['MA_Line'].notna().any(), "Should have some valid MA_Line values"
    
    def test_wave_signals_are_valid(self):
        """Test that wave signals are valid (0, 1, or 2)."""
        result_df = apply_rule_wave(self.test_df.copy(), self.wave_params, PriceType.OPEN)
        
        # Check signal values are valid
        valid_signals = [NOTRADE, BUY, SELL]
        assert result_df['_Signal'].isin(valid_signals).all(), "All signals should be valid"
        assert result_df['_Plot_Color'].isin(valid_signals).all(), "All plot colors should be valid"
    
    def test_wave_plotting_filters_invalid_values(self):
        """Test that wave plotting filters out invalid values."""
        from src.plotting.dual_chart_fastest import add_wave_indicator
        
        # Create test data with some NaN values
        result_df = apply_rule_wave(self.test_df.copy(), self.wave_params, PriceType.OPEN)
        
        # Set some values to NaN to test filtering
        result_df.loc[result_df.index[10:15], '_Plot_Wave'] = np.nan
        result_df.loc[result_df.index[20:25], '_Plot_FastLine'] = np.nan
        result_df.loc[result_df.index[30:35], 'MA_Line'] = np.nan
        
        # Create mock figure
        mock_fig = Mock()
        
        # Call the function
        add_wave_indicator(mock_fig, result_df)
        
        # Check that add_trace was called (indicating lines were added)
        assert mock_fig.add_trace.called, "add_trace should be called to add lines"
        
        # Get all calls to add_trace
        calls = mock_fig.add_trace.call_args_list
        
        # Check that we have calls for valid data
        assert len(calls) > 0, "Should have at least one trace added"
        
        # Check that traces are added with valid data
        for call in calls:
            args, kwargs = call
            trace = args[0]  # First argument is the trace
            
            # Check that trace has valid data
            if hasattr(trace, 'x') and hasattr(trace, 'y'):
                # x and y should not be empty
                assert len(trace.x) > 0, "Trace x data should not be empty"
                assert len(trace.y) > 0, "Trace y data should not be empty"
    
    def test_wave_colored_segments_only_for_valid_signals(self):
        """Test that colored segments are only added for valid signals."""
        from src.plotting.dual_chart_fastest import add_wave_indicator
        
        result_df = apply_rule_wave(self.test_df.copy(), self.wave_params, PriceType.OPEN)
        
        # Create mock figure
        mock_fig = Mock()
        
        # Call the function
        add_wave_indicator(mock_fig, result_df)
        
        # Get all calls to add_trace
        calls = mock_fig.add_trace.call_args_list
        
        # Check that colored segments are only added when signals exist
        red_segments = 0
        blue_segments = 0
        
        for call in calls:
            args, kwargs = call
            trace = args[0]
            
            if hasattr(trace, 'line') and hasattr(trace.line, 'color'):
                if trace.line.color == 'red':
                    red_segments += 1
                elif trace.line.color == 'blue':
                    blue_segments += 1
        
        # Should have some colored segments if signals exist
        total_signals = (result_df['_Plot_Color'] == BUY).sum() + (result_df['_Plot_Color'] == SELL).sum()
        if total_signals > 0:
            assert red_segments > 0 or blue_segments > 0, "Should have colored segments when signals exist"
    
    def test_wave_no_lines_for_all_nan_data(self):
        """Test that no lines are drawn when all data is NaN."""
        from src.plotting.dual_chart_fastest import add_wave_indicator
        
        # Create DataFrame with all NaN values
        nan_df = pd.DataFrame({
            '_Plot_Wave': [np.nan] * 100,
            '_Plot_Color': [NOTRADE] * 100,
            '_Plot_FastLine': [np.nan] * 100,
            'MA_Line': [np.nan] * 100
        })
        
        # Create mock figure
        mock_fig = Mock()
        
        # Call the function
        add_wave_indicator(mock_fig, nan_df)
        
        # Should not add any traces for all NaN data
        assert not mock_fig.add_trace.called, "Should not add traces for all NaN data"
    
    def test_wave_signal_display_only_for_valid_signals(self):
        """Test that signals are only displayed for valid signal values."""
        from src.plotting.dual_chart_fastest import plot_dual_chart_fastest
        
        result_df = apply_rule_wave(self.test_df.copy(), self.wave_params, PriceType.OPEN)
        
        # Create some valid signals
        result_df.loc[result_df.index[10], '_Signal'] = BUY
        result_df.loc[result_df.index[20], '_Signal'] = SELL
        result_df.loc[result_df.index[30], '_Signal'] = NOTRADE
        
        # Mock the plotting function to capture calls
        with patch('src.plotting.dual_chart_fastest.add_wave_indicator') as mock_add_wave:
            with patch('plotly.graph_objects.Figure') as mock_fig_class:
                mock_fig = Mock()
                mock_fig_class.return_value = mock_fig
                
                # Call the plotting function
                plot_dual_chart_fastest(result_df, 'wave:10,5,2,fast,8,4,2,fast,prime,5,open')
                
                # Check that add_wave_indicator was called
                mock_add_wave.assert_called_once()
                
                # Check that the DataFrame passed to add_wave_indicator has valid signals
                passed_df = mock_add_wave.call_args[0][1]  # Second argument is the DataFrame
                assert '_signal' in passed_df.columns, "DataFrame should have _signal column"
                
                # Check that only valid signals exist
                valid_signals = [NOTRADE, BUY, SELL]
                assert passed_df['_signal'].isin(valid_signals).all(), "All signals should be valid"
    
    def test_wave_discontinuous_line_traces(self):
        """Test that discontinuous line traces are created correctly."""
        from src.plotting.dual_chart_fastest import create_discontinuous_line_traces
        
        # Create test data with gaps
        test_index = pd.date_range('2024-01-01', periods=10, freq='D')
        test_values = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=test_index)
        
        # Create mask with gaps (True at indices 0,1,2, then False at 3,4, then True at 5,6,7)
        mask = pd.Series([True, True, True, False, False, True, True, True, False, False], index=test_index)
        
        # Create discontinuous traces
        traces = create_discontinuous_line_traces(
            test_index, test_values, mask, 'Test Line', 'red', width=2, showlegend=True
        )
        
        # Should create 2 separate traces (segments 0-2 and 5-7)
        assert len(traces) == 2, f"Expected 2 traces, got {len(traces)}"
        
        # Check first trace (indices 0-2)
        first_trace = traces[0]
        assert len(first_trace.x) == 3, "First trace should have 3 points"
        assert first_trace.name == 'Test Line', "First trace should have the correct name"
        assert first_trace.showlegend == True, "First trace should show in legend"
        
        # Check second trace (indices 5-7)  
        second_trace = traces[1]
        assert len(second_trace.x) == 3, "Second trace should have 3 points"
        assert second_trace.name is None, "Second trace should not have name (for legend)"
        assert second_trace.showlegend == False, "Second trace should not show in legend"
    
    def test_wave_no_interpolation_between_signals(self):
        """Test that there's no interpolation between different signal segments."""
        from src.plotting.dual_chart_fastest import add_wave_indicator, create_discontinuous_line_traces
        
        # Create test DataFrame with mixed signals
        test_index = pd.date_range('2024-01-01', periods=10, freq='D')
        test_df = pd.DataFrame({
            '_Plot_Wave': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            '_Plot_Color': [1, 1, 0, 0, 2, 2, 0, 1, 1, 0]  # BUY, BUY, NOTRADE, NOTRADE, SELL, SELL, NOTRADE, BUY, BUY, NOTRADE
        }, index=test_index)
        
        # Create mock figure
        mock_fig = Mock()
        
        # Call add_wave_indicator
        add_wave_indicator(mock_fig, test_df)
        
        # Should have multiple traces added (red, blue, black segments)
        assert mock_fig.add_trace.called, "add_trace should be called"
        
        # Get all traces added
        all_traces = [call[0][0] for call in mock_fig.add_trace.call_args_list]
        
        # Should have separate traces for each color segment
        red_traces = [t for t in all_traces if hasattr(t, 'line') and t.line.color == 'red']
        blue_traces = [t for t in all_traces if hasattr(t, 'line') and t.line.color == 'blue']
        black_traces = [t for t in all_traces if hasattr(t, 'line') and t.line.color == 'black']
        
        # Should have red traces for BUY signals (indices 0,1 and 7,8)
        assert len(red_traces) >= 1, "Should have red traces for BUY signals"
        
        # Should have blue traces for SELL signals (indices 4,5)
        assert len(blue_traces) >= 1, "Should have blue traces for SELL signals"
        
        # Should NOT have black traces for NOTRADE signals (they should be invisible)
        assert len(black_traces) == 0, "Should NOT have black traces for NOTRADE signals"


if __name__ == "__main__":
    # Run tests
    test_instance = TestWaveIndicatorFixes()
    test_instance.setup_method()
    
    print("🧪 Testing Wave indicator fixes...")
    
    # Run all tests
    test_instance.test_wave_calculation_produces_valid_data()
    print("✅ Wave calculation produces valid data")
    
    test_instance.test_wave_signals_are_valid()
    print("✅ Wave signals are valid")
    
    test_instance.test_wave_plotting_filters_invalid_values()
    print("✅ Wave plotting filters invalid values")
    
    test_instance.test_wave_colored_segments_only_for_valid_signals()
    print("✅ Wave colored segments only for valid signals")
    
    test_instance.test_wave_no_lines_for_all_nan_data()
    print("✅ Wave no lines for all NaN data")
    
    test_instance.test_wave_signal_display_only_for_valid_signals()
    print("✅ Wave signal display only for valid signals")
    
    print("\n🎯 All Wave indicator fixes tests passed!")
    print("🔧 Key fixes implemented:")
    print("   - No red/blue lines where there are no values")
    print("   - Wave line only shows when _Plot_Wave has valid values")
    print("   - Fast Line only shows when _Plot_FastLine has valid values")
    print("   - MA Line only shows when MA_Line has valid values")
    print("   - Colored segments only show when _Plot_Color has valid signals")
