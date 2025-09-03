# -*- coding: utf-8 -*-
"""
Tests for CLI Examples Module

This module tests the CLI examples functionality organized by indicator groups.
"""

import pytest
from src.cli.examples import (
    OscillatorExamples,
    TrendExamples,
    MomentumExamples,
    show_all_cli_examples,
    show_indicator_group_examples
)


class TestOscillatorExamples:
    """Test oscillator examples functionality."""
    
    def test_show_rsi_examples(self, capsys):
        """Test RSI examples display."""
        OscillatorExamples.show_rsi_examples()
        captured = capsys.readouterr()
        
        assert 'RSI (Relative Strength Index) Examples' in captured.out
        assert 'Basic RSI Analysis' in captured.out
        assert 'RSI with default settings' in captured.out
        assert 'python run_analysis.py csv --csv-file data.csv --rule RSI' in captured.out
    
    def test_show_stochastic_examples(self, capsys):
        """Test Stochastic examples display."""
        OscillatorExamples.show_stochastic_examples()
        captured = capsys.readouterr()
        
        assert 'Stochastic Oscillator Examples' in captured.out
        assert 'Basic Stochastic Analysis' in captured.out
        assert 'Stochastic with default settings' in captured.out
    
    def test_show_cci_examples(self, capsys):
        """Test CCI examples display."""
        OscillatorExamples.show_cci_examples()
        captured = capsys.readouterr()
        
        assert 'CCI (Commodity Channel Index) Examples' in captured.out
        assert 'Basic CCI Analysis' in captured.out
        assert 'CCI with default settings' in captured.out
    
    def test_show_williams_r_examples(self, capsys):
        """Test Williams %R examples display."""
        OscillatorExamples.show_williams_r_examples()
        captured = capsys.readouterr()
        
        assert 'Williams %R Examples' in captured.out
        assert 'Basic Williams %R Analysis' in captured.out
        assert 'Williams %R with default settings' in captured.out
    
    def test_show_all_oscillator_examples(self, capsys):
        """Test all oscillator examples display."""
        OscillatorExamples.show_all_oscillator_examples()
        captured = capsys.readouterr()
        
        assert 'OSCILLATOR INDICATORS - CLI EXAMPLES' in captured.out
        assert 'RSI (Relative Strength Index) Examples' in captured.out
        assert 'Stochastic Oscillator Examples' in captured.out
        assert 'CCI (Commodity Channel Index) Examples' in captured.out
        assert 'Williams %R Examples' in captured.out
        assert 'General Oscillator Tips' in captured.out


class TestTrendExamples:
    """Test trend examples functionality."""
    
    def test_show_ema_examples(self, capsys):
        """Test EMA examples display."""
        TrendExamples.show_ema_examples()
        captured = capsys.readouterr()
        
        assert 'EMA (Exponential Moving Average) Examples' in captured.out
        assert 'Basic EMA Analysis' in captured.out
        assert 'EMA with default settings' in captured.out
        assert 'python run_analysis.py csv --csv-file data.csv --rule EMA' in captured.out
    
    def test_show_sma_examples(self, capsys):
        """Test SMA examples display."""
        TrendExamples.show_sma_examples()
        captured = capsys.readouterr()
        
        assert 'SMA (Simple Moving Average) Examples' in captured.out
        assert 'Basic SMA Analysis' in captured.out
        assert 'SMA with default settings' in captured.out
    
    def test_show_adx_examples(self, capsys):
        """Test ADX examples display."""
        TrendExamples.show_adx_examples()
        captured = capsys.readouterr()
        
        assert 'ADX (Average Directional Index) Examples' in captured.out
        assert 'Basic ADX Analysis' in captured.out
        assert 'ADX with default settings' in captured.out
    
    def test_show_sar_examples(self, capsys):
        """Test SAR examples display."""
        TrendExamples.show_sar_examples()
        captured = capsys.readouterr()
        
        assert 'SAR (Parabolic SAR) Examples' in captured.out
        assert 'Basic SAR Analysis' in captured.out
        assert 'SAR with default settings' in captured.out
    
    def test_show_supertrend_examples(self, capsys):
        """Test SuperTrend examples display."""
        TrendExamples.show_supertrend_examples()
        captured = capsys.readouterr()
        
        assert 'SuperTrend Examples' in captured.out
        assert 'Basic SuperTrend Analysis' in captured.out
        assert 'SuperTrend with default settings' in captured.out
    
    def test_show_all_trend_examples(self, capsys):
        """Test all trend examples display."""
        TrendExamples.show_all_trend_examples()
        captured = capsys.readouterr()
        
        assert 'TREND INDICATORS - CLI EXAMPLES' in captured.out
        assert 'EMA (Exponential Moving Average) Examples' in captured.out
        assert 'SMA (Simple Moving Average) Examples' in captured.out
        assert 'ADX (Average Directional Index) Examples' in captured.out
        assert 'SAR (Parabolic SAR) Examples' in captured.out
        assert 'SuperTrend Examples' in captured.out
        assert 'General Trend Tips' in captured.out


class TestMomentumExamples:
    """Test momentum examples functionality."""
    
    def test_show_macd_examples(self, capsys):
        """Test MACD examples display."""
        MomentumExamples.show_macd_examples()
        captured = capsys.readouterr()
        
        assert 'MACD (Moving Average Convergence Divergence) Examples' in captured.out
        assert 'Basic MACD Analysis' in captured.out
        assert 'MACD with default settings' in captured.out
        assert 'python run_analysis.py csv --csv-file data.csv --rule MACD' in captured.out
    
    def test_show_stoch_oscillator_examples(self, capsys):
        """Test Stochastic Oscillator examples display."""
        MomentumExamples.show_stoch_oscillator_examples()
        captured = capsys.readouterr()
        
        assert 'Stochastic Oscillator Examples' in captured.out
        assert 'Basic Stochastic Analysis' in captured.out
        assert 'Stochastic with default settings' in captured.out
    
    def test_show_roc_examples(self, capsys):
        """Test ROC examples display."""
        MomentumExamples.show_roc_examples()
        captured = capsys.readouterr()
        
        assert 'ROC (Rate of Change) Examples' in captured.out
        assert 'Basic ROC Analysis' in captured.out
        assert 'ROC with default settings' in captured.out
    
    def test_show_momentum_examples(self, capsys):
        """Test Momentum examples display."""
        MomentumExamples.show_momentum_examples()
        captured = capsys.readouterr()
        
        assert 'Momentum Examples' in captured.out
        assert 'Basic Momentum Analysis' in captured.out
        assert 'Momentum with default settings' in captured.out
    
    def test_show_all_momentum_examples(self, capsys):
        """Test all momentum examples display."""
        MomentumExamples.show_all_momentum_examples()
        captured = capsys.readouterr()
        
        assert 'MOMENTUM INDICATORS - CLI EXAMPLES' in captured.out
        assert 'MACD (Moving Average Convergence Divergence) Examples' in captured.out
        assert 'Stochastic Oscillator Examples' in captured.out
        assert 'ROC (Rate of Change) Examples' in captured.out
        assert 'Momentum Examples' in captured.out
        assert 'General Momentum Tips' in captured.out


class TestMainExamples:
    """Test main examples functionality."""
    
    def test_show_all_cli_examples(self, capsys):
        """Test all CLI examples display."""
        show_all_cli_examples()
        captured = capsys.readouterr()
        
        assert 'COMPREHENSIVE CLI EXAMPLES - NEOZORk HLD PREDICTION' in captured.out
        assert 'OSCILLATOR INDICATORS - CLI EXAMPLES' in captured.out
        assert 'TREND INDICATORS - CLI EXAMPLES' in captured.out
        assert 'MOMENTUM INDICATORS - CLI EXAMPLES' in captured.out
        assert 'GENERAL CLI USAGE TIPS' in captured.out
    
    def test_show_indicator_group_examples_oscillators(self, capsys):
        """Test oscillator group examples display."""
        show_indicator_group_examples('oscillators')
        captured = capsys.readouterr()
        
        assert 'OSCILLATOR INDICATORS - CLI EXAMPLES' in captured.out
        assert 'RSI (Relative Strength Index) Examples' in captured.out
        assert 'Stochastic Oscillator Examples' in captured.out
    
    def test_show_indicator_group_examples_trend(self, capsys):
        """Test trend group examples display."""
        show_indicator_group_examples('trend')
        captured = capsys.readouterr()
        
        assert 'TREND INDICATORS - CLI EXAMPLES' in captured.out
        assert 'EMA (Exponential Moving Average) Examples' in captured.out
        assert 'SMA (Simple Moving Average) Examples' in captured.out
    
    def test_show_indicator_group_examples_momentum(self, capsys):
        """Test momentum group examples display."""
        show_indicator_group_examples('momentum')
        captured = capsys.readouterr()
        
        assert 'MOMENTUM INDICATORS - CLI EXAMPLES' in captured.out
        assert 'MACD (Moving Average Convergence Divergence) Examples' in captured.out
        assert 'Stochastic Oscillator Examples' in captured.out
    
    def test_show_indicator_group_examples_unknown(self, capsys):
        """Test unknown group examples display."""
        show_indicator_group_examples('unknown')
        captured = capsys.readouterr()
        
        assert 'Unknown indicator group: unknown' in captured.out
        assert 'Available groups: oscillators, trend, momentum' in captured.out
        # Should fall back to showing all examples
        assert 'COMPREHENSIVE CLI EXAMPLES - NEOZORk HLD PREDICTION' in captured.out


class TestExamplesContent:
    """Test examples content quality."""
    
    def test_examples_contain_python_commands(self, capsys):
        """Test that examples contain proper Python commands."""
        OscillatorExamples.show_rsi_examples()
        captured = capsys.readouterr()
        
        # Check for proper command structure
        assert 'python run_analysis.py' in captured.out
        assert '--rule RSI' in captured.out
        assert '--csv-file' in captured.out
    
    def test_examples_contain_data_sources(self, capsys):
        """Test that examples cover different data sources."""
        OscillatorExamples.show_rsi_examples()
        captured = capsys.readouterr()
        
        assert 'YFinance data' in captured.out
        assert 'Binance data' in captured.out
        assert 'Polygon data' in captured.out
    
    def test_examples_contain_visualization_options(self, capsys):
        """Test that examples cover visualization backends."""
        OscillatorExamples.show_rsi_examples()
        captured = capsys.readouterr()
        
        assert 'Plotly backend' in captured.out
        assert 'Seaborn backend' in captured.out
        assert 'Terminal backend' in captured.out
    
    def test_examples_contain_parameter_examples(self, capsys):
        """Test that examples show parameter customization."""
        OscillatorExamples.show_rsi_examples()
        captured = capsys.readouterr()
        
        assert 'RSI with custom period' in captured.out
        assert 'RSI with custom overbought/oversold' in captured.out
    
    def test_trend_examples_contain_parameter_examples(self, capsys):
        """Test that trend examples show parameter customization."""
        TrendExamples.show_ema_examples()
        captured = capsys.readouterr()
        
        assert 'EMA with custom period' in captured.out
        assert 'EMA with custom alpha' in captured.out
    
    def test_momentum_examples_contain_parameter_examples(self, capsys):
        """Test that momentum examples show parameter customization."""
        MomentumExamples.show_macd_examples()
        captured = capsys.readouterr()
        
        assert 'MACD with custom periods' in captured.out


class TestExamplesStructure:
    """Test examples structure consistency."""
    
    def test_all_examples_have_consistent_format(self, capsys):
        """Test that all examples follow consistent format."""
        # Test oscillator examples
        OscillatorExamples.show_all_oscillator_examples()
        captured = capsys.readouterr()
        oscillator_output = captured.out
        
        # Test trend examples
        TrendExamples.show_all_trend_examples()
        captured = capsys.readouterr()
        trend_output = captured.out
        
        # Test momentum examples
        MomentumExamples.show_all_momentum_examples()
        captured = capsys.readouterr()
        momentum_output = captured.out
        
        # Check that all follow similar structure
        for output in [oscillator_output, trend_output, momentum_output]:
            assert 'Examples' in output
            assert 'Basic' in output
            assert 'Different Data Sources' in output
            assert 'Visualization' in output
            assert 'General' in output
    
    def test_examples_contain_helpful_tips(self, capsys):
        """Test that examples contain helpful trading tips."""
        OscillatorExamples.show_all_oscillator_examples()
        captured = capsys.readouterr()
        
        assert 'General Oscillator Tips' in captured.out
        assert 'Combine multiple oscillators' in captured.out
        assert 'Use with volume confirmation' in captured.out
        assert 'Multiple timeframe analysis' in captured.out


if __name__ == "__main__":
    pytest.main([__file__])
