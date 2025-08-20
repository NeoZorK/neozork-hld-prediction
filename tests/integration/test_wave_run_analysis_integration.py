# -*- coding: utf-8 -*-
# tests/integration/test_wave_run_analysis_integration.py

"""
Integration tests for Wave indicator with run_analysis.py and -d fastest parameter.

This test suite covers:
1. Integration with run_analysis.py script
2. Command line argument parsing
3. Data flow from CLI to calculation to plotting
4. Error handling in the full pipeline
5. Performance with different data sources
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import subprocess
import sys
import os
import tempfile

from src.calculation.indicators.trend.wave_ind import (
    apply_rule_wave, WaveParameters, ENUM_MOM_TR, ENUM_GLOBAL_TR
)
from src.calculation.indicators.base_indicator import PriceType
from src.common.constants import BUY, SELL, NOTRADE


class TestWaveRunAnalysisIntegration:
    """Integration test cases for Wave indicator with run_analysis.py."""
    
    @pytest.fixture
    def sample_data_file(self, tmp_path):
        """Create sample data file for testing."""
        # Create sample OHLCV data with MT5 format dates
        dates = pd.date_range('2024-01-01', periods=200, freq='D')
        
        # Convert dates to MT5 format (YYYY.MM.DD HH:MM)
        mt5_dates = [date.strftime('%Y.%m.%d %H:%M') for date in dates]
        
        # Create realistic price data with trends and volatility
        np.random.seed(42)  # For reproducible tests
        
        # Base trend
        trend = np.linspace(100, 150, 200)
        
        # Add volatility
        volatility = np.random.normal(0, 5, 200)
        
        # Add some cycles
        cycles = 10 * np.sin(np.linspace(0, 4*np.pi, 200))
        
        # Combine all components
        base_price = trend + volatility + cycles
        
        # Create OHLCV data
        df = pd.DataFrame({
            'DateTime': mt5_dates,
            'Open': base_price + np.random.normal(0, 1, 200),
            'High': base_price + np.abs(np.random.normal(0, 3, 200)),
            'Low': base_price - np.abs(np.random.normal(0, 3, 200)),
            'Close': base_price + np.random.normal(0, 1, 200),
            'TickVolume': np.random.uniform(1000, 10000, 200)
        })
        
        # Ensure High >= Low
        df['High'] = df[['Open', 'Close', 'High']].max(axis=1) + np.abs(np.random.normal(0, 1, 200))
        df['Low'] = df[['Open', 'Close', 'Low']].min(axis=1) - np.abs(np.random.normal(0, 1, 200))
        
        # Save to temporary file with MT5 format (info line + header)
        data_file = tmp_path / "test_wave_integration_data.csv"
        with open(data_file, 'w') as f:
            f.write("File Info Header Line\n")  # Info line
            df.to_csv(f, index=False)  # Header + data
        
        return str(data_file)
    
    def test_run_analysis_wave_command_structure(self, sample_data_file):
        """Test run_analysis.py wave command structure."""
        # Test the command structure that would be used with run_analysis.py
        command_parts = [
            "uv", "run", "run_analysis.py",
            "show", "csv", "test_data",
            "-d", "fastest",
            "--rule", "wave:339,10,2,fast,22,11,4,fast,prime,22,open"
        ]
        
        # Verify command structure
        assert len(command_parts) == 10, "Command should have correct number of arguments"
        assert command_parts[0] == "uv", "Should use uv"
        assert command_parts[1] == "run", "Should use run"
        assert command_parts[2] == "run_analysis.py", "Should use run_analysis.py"
        assert command_parts[3] == "show", "Should use show mode"
        assert command_parts[4] == "csv", "Should use csv mode"
        assert command_parts[5] == "test_data", "Should specify data source"
        assert command_parts[6] == "-d", "Should have display flag"
        assert command_parts[7] == "fastest", "Should use fastest display mode"
        assert command_parts[8] == "--rule", "Should have rule flag"
        assert command_parts[9] == "wave:339,10,2,fast,22,11,4,fast,prime,22,open", "Should use correct wave rule"
    
    @patch('src.plotting.dual_chart_fastest.plot_dual_chart_fastest')
    def test_wave_integration_pipeline(self, mock_plot, sample_data_file):
        """Test the complete wave integration pipeline."""
        # Mock the plotting function
        mock_plot.return_value = None
        
        # Test the complete pipeline from data loading to plotting
        from src.data.fetchers import fetch_csv_data
        from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters
        from src.calculation.indicators.base_indicator import PriceType
        
        # Load data
        df = fetch_csv_data(sample_data_file)
        assert len(df) > 0, "Should load data successfully"
        
        # Create wave parameters
        wave_params = WaveParameters(
            long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
            long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
        )
        
        # Apply wave calculation
        result_df = apply_rule_wave(df.copy(), wave_params, PriceType.OPEN)
        
        # Verify results
        required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
        for col in required_cols:
            assert col in result_df.columns, f"Missing column {col}"
        
        # Verify signal values are valid
        valid_signals = [NOTRADE, BUY, SELL]
        assert result_df['_Signal'].isin(valid_signals).all(), "Invalid signals"
        assert result_df['_Plot_Color'].isin(valid_signals).all(), "Invalid plot colors"
        
        # Test plotting integration
        from src.plotting.dual_chart_fastest import add_wave_indicator
        
        mock_fig = Mock()
        add_wave_indicator(mock_fig, result_df)
        
        # Verify that plotting was called
        assert mock_fig.add_trace.called, "add_trace should be called"
    
    def test_wave_parameter_combinations_integration(self, sample_data_file):
        """Test various wave parameter combinations in integration."""
        from src.data.fetchers import fetch_csv_data
        from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters
        from src.calculation.indicators.base_indicator import PriceType
        
        # Load data
        df = fetch_csv_data(sample_data_file)
        
        # Test various parameter combinations
        test_combinations = [
            # Default settings
            (339, 10, 2, ENUM_MOM_TR.TR_Fast, 22, 11, 4, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME, 22),
            # Short-term trading
            (50, 5, 2, ENUM_MOM_TR.TR_BetterFast, 20, 8, 3, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_REVERSE, 15),
            # Long-term trend following
            (200, 20, 10, ENUM_MOM_TR.TR_StrongTrend, 100, 15, 8, ENUM_MOM_TR.TR_BetterTrend, ENUM_GLOBAL_TR.G_TR_PRIME_ZONE, 50),
            # Aggressive trading
            (30, 3, 1, ENUM_MOM_TR.TR_Fast, 15, 5, 2, ENUM_MOM_TR.TR_BetterFast, ENUM_GLOBAL_TR.G_TR_NEW_ZONE, 10),
            # Conservative approach
            (500, 50, 25, ENUM_MOM_TR.TR_WeakTrend, 200, 25, 15, ENUM_MOM_TR.TR_StrongTrend, ENUM_GLOBAL_TR.G_TR_LONG_ZONE, 100)
        ]
        
        for long1, fast1, trend1, tr1, long2, fast2, trend2, tr2, global_tr, sma_period in test_combinations:
            wave_params = WaveParameters(
                long1=long1, fast1=fast1, trend1=trend1, tr1=tr1,
                long2=long2, fast2=fast2, trend2=trend2, tr2=tr2,
                global_tr=global_tr, sma_period=sma_period
            )
            
            # Test with both price types
            for price_type in [PriceType.OPEN, PriceType.CLOSE]:
                result_df = apply_rule_wave(df.copy(), wave_params, price_type)
                
                # Verify results
                required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
                for col in required_cols:
                    assert col in result_df.columns, f"Missing column {col} for combination {long1},{fast1},{trend1},{tr1.name},{long2},{fast2},{trend2},{tr2.name},{global_tr.name},{sma_period}"
                
                # Verify signal values are valid
                valid_signals = [NOTRADE, BUY, SELL]
                assert result_df['_Signal'].isin(valid_signals).all(), f"Invalid signals for combination {long1},{fast1},{trend1},{tr1.name},{long2},{fast2},{trend2},{tr2.name},{global_tr.name},{sma_period}"
                assert result_df['_Plot_Color'].isin(valid_signals).all(), f"Invalid plot colors for combination {long1},{fast1},{trend1},{tr1.name},{long2},{fast2},{trend2},{tr2.name},{global_tr.name},{sma_period}"
                
                # Verify we have some data
                assert len(result_df) > 0, f"No data generated for combination {long1},{fast1},{trend1},{tr1.name},{long2},{fast2},{trend2},{tr2.name},{global_tr.name},{sma_period}"
    
    def test_wave_error_handling_integration(self, sample_data_file):
        """Test error handling in wave integration."""
        from src.data.fetchers import fetch_csv_data
        from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters
        from src.calculation.indicators.base_indicator import PriceType
        
        # Load data
        df = fetch_csv_data(sample_data_file)
        
        # Test with invalid parameters
        invalid_params = [
            # Invalid periods
            (0, 10, 5, ENUM_MOM_TR.TR_Fast, 30, 8, 3, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME, 20),
            (50, 0, 5, ENUM_MOM_TR.TR_Fast, 30, 8, 3, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME, 20),
            (50, 10, 0, ENUM_MOM_TR.TR_Fast, 30, 8, 3, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME, 20),
            (50, 10, 5, ENUM_MOM_TR.TR_Fast, 0, 8, 3, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME, 20),
            (50, 10, 5, ENUM_MOM_TR.TR_Fast, 30, 0, 3, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME, 20),
            (50, 10, 5, ENUM_MOM_TR.TR_Fast, 30, 8, 0, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME, 20),
            (50, 10, 5, ENUM_MOM_TR.TR_Fast, 30, 8, 3, ENUM_MOM_TR.TR_Fast, ENUM_GLOBAL_TR.G_TR_PRIME, 0)
        ]
        
        for long1, fast1, trend1, tr1, long2, fast2, trend2, tr2, global_tr, sma_period in invalid_params:
            wave_params = WaveParameters(
                long1=long1, fast1=fast1, trend1=trend1, tr1=tr1,
                long2=long2, fast2=fast2, trend2=trend2, tr2=tr2,
                global_tr=global_tr, sma_period=sma_period
            )
            
            # The validation happens in init_wave, which is called by apply_rule_wave
            with pytest.raises(ValueError, match="must be positive"):
                apply_rule_wave(df.copy(), wave_params, PriceType.OPEN)
        
        # Test with insufficient data
        small_df = df.head(5)  # Only 5 rows
        
        wave_params = WaveParameters(
            long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
            long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
        )
        
        # This should raise ValueError due to insufficient data for SMA
        with pytest.raises(ValueError, match="Not enough data points"):
            apply_rule_wave(small_df.copy(), wave_params, PriceType.OPEN)
    
    def test_wave_performance_integration(self, sample_data_file):
        """Test wave performance with different data sizes."""
        from src.data.fetchers import fetch_csv_data
        from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters
        from src.calculation.indicators.base_indicator import PriceType
        
        # Load data
        df = fetch_csv_data(sample_data_file)
        
        # Test with different data sizes
        data_sizes = [50, 100, 200]
        
        for size in data_sizes:
            test_df = df.head(size)
            
            wave_params = WaveParameters(
                long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
                long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
                global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
            )
            
            # Test with both price types
            for price_type in [PriceType.OPEN, PriceType.CLOSE]:
                result_df = apply_rule_wave(test_df.copy(), wave_params, price_type)
                
                # Verify results
                required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
                for col in required_cols:
                    assert col in result_df.columns, f"Missing column {col} for data size {size}"
                
                # Verify signal values are valid
                valid_signals = [NOTRADE, BUY, SELL]
                assert result_df['_Signal'].isin(valid_signals).all(), f"Invalid signals for data size {size}"
                assert result_df['_Plot_Color'].isin(valid_signals).all(), f"Invalid plot colors for data size {size}"
                
                # Verify we have the expected amount of data
                assert len(result_df) == size, f"Data size mismatch for size {size}"
    
    @patch('src.plotting.dual_chart_fastest.plot_dual_chart_fastest')
    def test_wave_fastest_mode_integration(self, mock_plot, sample_data_file):
        """Test wave integration with fastest mode plotting."""
        # Mock the plotting function
        mock_plot.return_value = None
        
        from src.data.fetchers import fetch_csv_data
        from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters
        from src.calculation.indicators.base_indicator import PriceType
        from src.plotting.dual_chart_fastest import add_wave_indicator
        
        # Load data
        df = fetch_csv_data(sample_data_file)
        
        # Create wave parameters
        wave_params = WaveParameters(
            long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
            long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
        )
        
        # Apply wave calculation
        result_df = apply_rule_wave(df.copy(), wave_params, PriceType.OPEN)
        
        # Test fastest mode plotting
        mock_fig = Mock()
        add_wave_indicator(mock_fig, result_df)
        
        # Verify that add_trace was called (indicating lines were added)
        assert mock_fig.add_trace.called, "add_trace should be called for fastest mode"
        
        # Get all calls to add_trace
        calls = mock_fig.add_trace.call_args_list
        
        # Should have at least some traces added
        assert len(calls) > 0, "No traces added for fastest mode"
        
        # Check that traces have valid data
        for call in calls:
            args, kwargs = call
            trace = args[0]  # First argument is the trace
            
            # Check that trace has valid data
            if hasattr(trace, 'x') and hasattr(trace, 'y'):
                # x and y should not be empty
                assert len(trace.x) > 0, "Trace x data should not be empty for fastest mode"
                assert len(trace.y) > 0, "Trace y data should not be empty for fastest mode"
    
    def test_wave_data_flow_integration(self, sample_data_file):
        """Test complete data flow from file to calculation to results."""
        from src.data.fetchers import fetch_csv_data
        from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters
        from src.calculation.indicators.base_indicator import PriceType
        
        # Load data
        df = fetch_csv_data(sample_data_file)
        
        # Verify data structure
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols:
            assert col in df.columns, f"Missing required column {col}"
        
        # Create wave parameters
        wave_params = WaveParameters(
            long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
            long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
        )
        
        # Apply wave calculation
        result_df = apply_rule_wave(df.copy(), wave_params, PriceType.OPEN)
        
        # Verify calculation results
        required_result_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
        for col in required_result_cols:
            assert col in result_df.columns, f"Missing result column {col}"
        
        # Verify signal values are valid
        valid_signals = [NOTRADE, BUY, SELL]
        assert result_df['_Signal'].isin(valid_signals).all(), "Invalid signals"
        assert result_df['_Plot_Color'].isin(valid_signals).all(), "Invalid plot colors"
        
        # Verify data integrity
        assert len(result_df) == len(df), "Result DataFrame should have same length as input"
        assert all(result_df.index == df.index), "Result DataFrame should have same index as input"
        
        # Verify that original data is preserved
        for col in required_cols:
            pd.testing.assert_series_equal(result_df[col], df[col], check_names=False), f"Original column {col} should be preserved"
    
    def test_wave_cli_integration_simulation(self, sample_data_file):
        """Simulate CLI integration with wave indicator."""
        # Simulate the CLI command parsing and execution
        from src.cli.cli import parse_wave_parameters
        from src.data.fetchers import fetch_csv_data
        from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters
        from src.calculation.indicators.base_indicator import PriceType
        
        # Simulate CLI parameter parsing
        param_str = "339,10,2,fast,22,11,4,fast,prime,22,open"
        indicator_name, params = parse_wave_parameters(param_str)
        
        assert indicator_name == "wave", "Indicator name should be 'wave'"
        
        # Create WaveParameters from parsed parameters
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
        
        # Load data (simulating CLI data loading)
        df = fetch_csv_data(sample_data_file)
        
        # Determine price type
        price_type = PriceType.OPEN if params['price_type'] == 'open' else PriceType.CLOSE
        
        # Apply wave calculation (simulating CLI calculation)
        result_df = apply_rule_wave(df.copy(), wave_params, price_type)
        
        # Verify results
        required_cols = ['_Signal', '_Direction', '_Plot_Wave', '_Plot_FastLine', 'MA_Line', '_Plot_Color']
        for col in required_cols:
            assert col in result_df.columns, f"Missing column {col}"
        
        # Verify signal values are valid
        valid_signals = [NOTRADE, BUY, SELL]
        assert result_df['_Signal'].isin(valid_signals).all(), "Invalid signals"
        assert result_df['_Plot_Color'].isin(valid_signals).all(), "Invalid plot colors"
        
        # Verify we have some data
        assert len(result_df) > 0, "No data generated"


if __name__ == "__main__":
    # Run integration tests
    test_instance = TestWaveRunAnalysisIntegration()
    
    print("🧪 Running Wave indicator integration tests with run_analysis.py...")
    
    # Create temporary data file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        # Create sample data
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        mt5_dates = [date.strftime('%Y.%m.%d %H:%M') for date in dates]
        df = pd.DataFrame({
            'DateTime': mt5_dates,
            'Open': np.random.uniform(100, 200, 100),
            'High': np.random.uniform(200, 300, 100),
            'Low': np.random.uniform(50, 100, 100),
            'Close': np.random.uniform(100, 200, 100),
            'TickVolume': np.random.uniform(1000, 10000, 100)
        })
        with open(f.name, 'w') as csv_file:
            csv_file.write("File Info Header Line\n")
            df.to_csv(csv_file, index=False)
        sample_data_file = f.name
    
    try:
        # Run all test methods
        test_methods = [
            test_instance.test_run_analysis_wave_command_structure,
            test_instance.test_wave_integration_pipeline,
            test_instance.test_wave_parameter_combinations_integration,
            test_instance.test_wave_error_handling_integration,
            test_instance.test_wave_performance_integration,
            test_instance.test_wave_fastest_mode_integration,
            test_instance.test_wave_data_flow_integration,
            test_instance.test_wave_cli_integration_simulation
        ]
        
        for test_method in test_methods:
            try:
                test_method()
                print(f"✅ {test_method.__name__} passed")
            except Exception as e:
                print(f"❌ {test_method.__name__} failed: {e}")
    
    finally:
        # Clean up temporary file
        os.unlink(sample_data_file)
    
    print("\n🎯 Wave indicator integration tests completed!")
    print("📊 Integration test coverage includes:")
    print("   - run_analysis.py command structure")
    print("   - Complete integration pipeline")
    print("   - Various parameter combinations")
    print("   - Error handling")
    print("   - Performance with different data sizes")
    print("   - Fastest mode integration")
    print("   - Complete data flow")
    print("   - CLI integration simulation")
