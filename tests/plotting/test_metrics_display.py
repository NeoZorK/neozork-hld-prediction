#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for Metrics Display Module
Comprehensive unit test suite for trading metrics display functionality
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.plotting.metrics_display import (
    MetricsDisplay,
    add_metrics_to_plotly_chart,
    add_metrics_to_matplotlib_chart
)

class TestMetricsDisplay:
    """Test MetricsDisplay class"""
    
    @pytest.fixture
    def metrics_display_dark(self):
        """Create MetricsDisplay instance with dark theme"""
        return MetricsDisplay(theme='dark')
    
    @pytest.fixture
    def metrics_display_light(self):
        """Create MetricsDisplay instance with light theme"""
        return MetricsDisplay(theme='light')
    
    @pytest.fixture
    def sample_metrics(self):
        """Create sample trading metrics"""
        return {
            'win_ratio': 65.5,
            'risk_reward_ratio': 2.1,
            'profit_factor': 1.8,
            'total_return': 25.3,
            'sharpe_ratio': 1.2,
            'max_drawdown': 15.2,
            'volatility': 12.8,
            'mc_var_95': 8.5,
            'mc_cvar_95': 12.3,
            'mc_max_loss': 18.7,
            'risk_of_ruin': 5.2,
            'net_return': 22.1,
            'mc_expected_return': 28.5,
            'mc_probability_profit': 75.8,
            'mc_max_gain': 45.2,
            'signal_accuracy': 72.3,
            'signal_stability': 68.9,
            'pattern_consistency': 71.4,
            'signal_clustering': 69.7,
            'strategy_sustainability': 73.1,
            'sortino_ratio': 1.5,
            'calmar_ratio': 1.8,
            'kelly_fraction': 0.25
        }
    
    @pytest.fixture
    def sample_dataframe(self):
        """Create sample DataFrame for testing"""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = {
            'time': dates,
            'open': np.random.uniform(100, 110, 100),
            'high': np.random.uniform(105, 115, 100),
            'low': np.random.uniform(95, 105, 100),
            'close': np.random.uniform(100, 110, 100),
            'volume': np.random.randint(1000, 10000, 100)
        }
        return pd.DataFrame(data)
    
    def test_initialization_dark_theme(self, metrics_display_dark):
        """Test initialization with dark theme"""
        assert metrics_display_dark.theme == 'dark'
        assert metrics_display_dark.colors is not None
        assert 'background' in metrics_display_dark.colors
        assert 'text' in metrics_display_dark.colors
        assert 'win' in metrics_display_dark.colors
        assert 'loss' in metrics_display_dark.colors
    
    def test_initialization_light_theme(self, metrics_display_light):
        """Test initialization with light theme"""
        assert metrics_display_light.theme == 'light'
        assert metrics_display_light.colors is not None
        assert 'background' in metrics_display_light.colors
        assert 'text' in metrics_display_light.colors
        assert 'win' in metrics_display_light.colors
        assert 'loss' in metrics_display_light.colors
    
    def test_get_theme_colors_dark(self, metrics_display_dark):
        """Test dark theme colors"""
        colors = metrics_display_dark._get_theme_colors()
        
        assert colors['background'] == '#1e1e1e'
        assert colors['text'] == '#ffffff'
        assert colors['border'] == '#404040'
        assert colors['win'] == '#00ff88'
        assert colors['loss'] == '#ff4444'
        assert colors['neutral'] == '#888888'
        assert colors['good'] == '#00cc66'
        assert colors['bad'] == '#ff4444'
        assert colors['warning'] == '#ffaa00'
        assert colors['danger'] == '#ff4444'
    
    def test_get_theme_colors_light(self, metrics_display_light):
        """Test light theme colors"""
        colors = metrics_display_light._get_theme_colors()
        
        assert colors['background'] == '#ffffff'
        assert colors['text'] == '#000000'
        assert colors['border'] == '#cccccc'
        assert colors['win'] == '#008800'
        assert colors['loss'] == '#cc0000'
        assert colors['neutral'] == '#666666'
        assert colors['good'] == '#006600'
        assert colors['bad'] == '#cc0000'
        assert colors['warning'] == '#cc6600'
        assert colors['danger'] == '#cc0000'
    
    def test_get_metric_color_win_ratio_good(self, metrics_display_dark):
        """Test metric color for good win ratio"""
        color = metrics_display_dark._get_metric_color('win_ratio', 75.0)
        assert color == metrics_display_dark.colors['good']
    
    def test_get_metric_color_win_ratio_warning(self, metrics_display_dark):
        """Test metric color for warning win ratio"""
        color = metrics_display_dark._get_metric_color('win_ratio', 60.0)
        assert color == metrics_display_dark.colors['warning']
    
    def test_get_metric_color_win_ratio_bad(self, metrics_display_dark):
        """Test metric color for bad win ratio"""
        color = metrics_display_dark._get_metric_color('win_ratio', 40.0)
        assert color == metrics_display_dark.colors['bad']
    
    def test_get_metric_color_risk_reward_good(self, metrics_display_dark):
        """Test metric color for good risk/reward ratio"""
        color = metrics_display_dark._get_metric_color('risk_reward_ratio', 2.5)
        assert color == metrics_display_dark.colors['good']
    
    def test_get_metric_color_risk_reward_warning(self, metrics_display_dark):
        """Test metric color for warning risk/reward ratio"""
        color = metrics_display_dark._get_metric_color('risk_reward_ratio', 1.7)
        assert color == metrics_display_dark.colors['warning']
    
    def test_get_metric_color_risk_reward_bad(self, metrics_display_dark):
        """Test metric color for bad risk/reward ratio"""
        color = metrics_display_dark._get_metric_color('risk_reward_ratio', 1.2)
        assert color == metrics_display_dark.colors['bad']
    
    def test_get_metric_color_max_drawdown_good(self, metrics_display_dark):
        """Test metric color for good max drawdown"""
        color = metrics_display_dark._get_metric_color('max_drawdown', 8.0)
        assert color == metrics_display_dark.colors['good']
    
    def test_get_metric_color_max_drawdown_warning(self, metrics_display_dark):
        """Test metric color for warning max drawdown"""
        color = metrics_display_dark._get_metric_color('max_drawdown', 15.0)
        assert color == metrics_display_dark.colors['warning']
    
    def test_get_metric_color_max_drawdown_bad(self, metrics_display_dark):
        """Test metric color for bad max drawdown"""
        color = metrics_display_dark._get_metric_color('max_drawdown', 25.0)
        assert color == metrics_display_dark.colors['bad']
    
    def test_get_metric_color_total_return_good(self, metrics_display_dark):
        """Test metric color for good total return"""
        color = metrics_display_dark._get_metric_color('total_return', 25.0)
        assert color == metrics_display_dark.colors['good']
    
    def test_get_metric_color_total_return_warning(self, metrics_display_dark):
        """Test metric color for warning total return"""
        color = metrics_display_dark._get_metric_color('total_return', 15.0)
        assert color == metrics_display_dark.colors['warning']
    
    def test_get_metric_color_total_return_bad(self, metrics_display_dark):
        """Test metric color for bad total return"""
        color = metrics_display_dark._get_metric_color('total_return', 5.0)
        assert color == metrics_display_dark.colors['bad']
    
    def test_get_metric_color_unknown_metric(self, metrics_display_dark):
        """Test metric color for unknown metric"""
        color = metrics_display_dark._get_metric_color('unknown_metric', 50.0)
        assert color == metrics_display_dark.colors['neutral']
    
    def test_get_metric_color_exception_handling(self, metrics_display_dark):
        """Test metric color exception handling"""
        color = metrics_display_dark._get_metric_color('win_ratio', 'invalid_value')
        assert color == metrics_display_dark.colors['neutral']
    
    def test_add_metrics_to_plotly_disabled(self, metrics_display_dark, sample_dataframe):
        """Test that add_metrics_to_plotly is disabled"""
        from plotly import graph_objects as go
        
        fig = go.Figure()
        original_fig = fig
        
        result = metrics_display_dark.add_metrics_to_plotly(
            fig=fig,
            df=sample_dataframe,
            metrics={'win_ratio': 65.5},
            position='right',
            lot_size=1.0,
            risk_reward_ratio=2.0,
            fee_per_trade=0.07
        )
        
        # Should return original figure unchanged
        assert result is original_fig
    
    def test_add_metrics_to_matplotlib_disabled(self, metrics_display_dark, sample_dataframe):
        """Test that add_metrics_to_matplotlib is disabled"""
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots()
        original_ax = ax
        
        result = metrics_display_dark.add_metrics_to_matplotlib(
            ax=ax,
            df=sample_dataframe,
            metrics={'win_ratio': 65.5},
            position='right'
        )
        
        # Should return original axes unchanged
        assert result is original_ax
    
    def test_format_metrics_for_plotly_disabled(self, metrics_display_dark, sample_metrics):
        """Test that format_metrics_for_plotly is disabled"""
        result = metrics_display_dark._format_metrics_for_plotly(sample_metrics)
        assert result == ""
    
    def test_format_additional_metrics_for_plotly_disabled(self, metrics_display_dark, sample_metrics):
        """Test that format_additional_metrics_for_plotly is disabled"""
        result = metrics_display_dark._format_additional_metrics_for_plotly(sample_metrics)
        assert result == ""
    
    def test_add_matplotlib_metrics_text_disabled(self, metrics_display_dark, sample_metrics):
        """Test that add_matplotlib_metrics_text is disabled"""
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots()
        
        # Should not raise any exception
        metrics_display_dark._add_matplotlib_metrics_text(
            ax=ax,
            metrics=sample_metrics,
            position='right',
            xlim=(0, 100),
            ylim=(0, 100)
        )
    
    def test_get_metrics_summary_success(self, metrics_display_dark, sample_metrics):
        """Test successful metrics summary generation"""
        summary = metrics_display_dark.get_metrics_summary(sample_metrics)
        
        assert isinstance(summary, str)
        assert "Win Rate:" in summary
        assert "R/R:" in summary
        assert "PF:" in summary
        assert "Return:" in summary
        assert "Sharpe:" in summary
        assert "65.5" in summary  # win_ratio
        assert "2.10" in summary  # risk_reward_ratio
        assert "1.80" in summary  # profit_factor
        assert "25.3" in summary  # total_return
        assert "1.20" in summary  # sharpe_ratio
    
    def test_get_metrics_summary_missing_metrics(self, metrics_display_dark):
        """Test metrics summary with missing metrics"""
        incomplete_metrics = {'win_ratio': 65.5}
        
        with patch('src.plotting.metrics_display.logger') as mock_logger:
            summary = metrics_display_dark.get_metrics_summary(incomplete_metrics)
            assert summary == "Metrics calculation error"
            mock_logger.print_debug.assert_called_once()
    
    def test_get_metrics_summary_exception(self, metrics_display_dark):
        """Test metrics summary with exception"""
        invalid_metrics = None
        
        with patch('src.plotting.metrics_display.logger') as mock_logger:
            summary = metrics_display_dark.get_metrics_summary(invalid_metrics)
            assert summary == "Metrics calculation error"
            mock_logger.print_debug.assert_called_once()

class TestStandaloneFunctions:
    """Test standalone functions"""
    
    @pytest.fixture
    def sample_dataframe(self):
        """Create sample DataFrame for testing"""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = {
            'time': dates,
            'open': np.random.uniform(100, 110, 100),
            'high': np.random.uniform(105, 115, 100),
            'low': np.random.uniform(95, 105, 100),
            'close': np.random.uniform(100, 110, 100),
            'volume': np.random.randint(1000, 10000, 100)
        }
        return pd.DataFrame(data)
    
    def test_add_metrics_to_plotly_chart_disabled(self, sample_dataframe):
        """Test that add_metrics_to_plotly_chart is disabled"""
        from plotly import graph_objects as go
        
        fig = go.Figure()
        original_fig = fig
        
        result = add_metrics_to_plotly_chart(
            fig=fig,
            df=sample_dataframe,
            metrics={'win_ratio': 65.5},
            position='right',
            lot_size=1.0,
            risk_reward_ratio=2.0,
            fee_per_trade=0.07
        )
        
        # Should return original figure unchanged
        assert result is original_fig
    
    def test_add_metrics_to_matplotlib_chart_disabled(self, sample_dataframe):
        """Test that add_metrics_to_matplotlib_chart is disabled"""
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots()
        original_ax = ax
        
        result = add_metrics_to_matplotlib_chart(
            ax=ax,
            df=sample_dataframe,
            position='right'
        )
        
        # Should return original axes unchanged
        assert result is original_ax

class TestIntegration:
    """Integration tests"""
    
    @pytest.fixture
    def metrics_display(self):
        """Create MetricsDisplay instance"""
        return MetricsDisplay(theme='dark')
    
    @pytest.fixture
    def sample_metrics(self):
        """Create sample trading metrics"""
        return {
            'win_ratio': 65.5,
            'risk_reward_ratio': 2.1,
            'profit_factor': 1.8,
            'total_return': 25.3,
            'sharpe_ratio': 1.2
        }
    
    def test_full_workflow(self, metrics_display, sample_metrics):
        """Test full workflow with all methods"""
        # Test color generation
        colors = metrics_display._get_theme_colors()
        assert len(colors) > 0
        
        # Test metric color assignment
        win_color = metrics_display._get_metric_color('win_ratio', 65.5)
        assert win_color in colors.values()
        
        # Test metrics summary
        summary = metrics_display.get_metrics_summary(sample_metrics)
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_theme_consistency(self):
        """Test theme consistency across different instances"""
        dark_display = MetricsDisplay(theme='dark')
        light_display = MetricsDisplay(theme='light')
        
        dark_colors = dark_display._get_theme_colors()
        light_colors = light_display._get_theme_colors()
        
        # Colors should be different between themes
        assert dark_colors['background'] != light_colors['background']
        assert dark_colors['text'] != light_colors['text']
        
        # But structure should be the same
        assert set(dark_colors.keys()) == set(light_colors.keys())

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 