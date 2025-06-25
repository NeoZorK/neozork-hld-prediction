# -*- coding: utf-8 -*-
# src/plotting/metrics_display.py

"""
Trading Metrics Display Module
Provides beautiful and informative display of trading metrics on charts.
NOTE: All HTML chart metrics have been removed as requested.
Metrics are now displayed only in console output.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
from plotly import graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from src.common import logger
from src.calculation.trading_metrics import calculate_trading_metrics


class MetricsDisplay:
    """
    Trading metrics display for charts.
    NOTE: HTML chart metrics have been removed - metrics are displayed only in console.
    """
    
    def __init__(self, theme: str = 'dark'):
        """
        Initialize metrics display.
        
        Args:
            theme (str): Display theme ('dark' or 'light') - not used for HTML charts
        """
        self.theme = theme
        self.colors = self._get_theme_colors()
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """Get color scheme based on theme - not used for HTML charts."""
        if self.theme == 'dark':
            return {
                'background': '#1e1e1e',
                'text': '#ffffff',
                'border': '#404040',
                'win': '#00ff88',
                'loss': '#ff4444',
                'neutral': '#888888',
                'good': '#00cc66',
                'bad': '#ff4444',
                'warning': '#ffaa00',
                'danger': '#ff4444'
            }
        else:
            return {
                'background': '#ffffff',
                'text': '#000000',
                'border': '#cccccc',
                'win': '#008800',
                'loss': '#cc0000',
                'neutral': '#666666',
                'good': '#006600',
                'bad': '#cc0000',
                'warning': '#cc6600',
                'danger': '#cc0000'
            }
    
    def _get_metric_color(self, metric_name: str, value: float) -> str:
        """Get color for metric value - not used for HTML charts."""
        try:
            if metric_name in ['win_ratio', 'signal_accuracy', 'signal_stability', 
                             'pattern_consistency', 'signal_clustering', 'strategy_sustainability']:
                if value >= 70:
                    return self.colors['good']
                elif value >= 50:
                    return self.colors['warning']
                else:
                    return self.colors['bad']
            elif metric_name in ['risk_reward_ratio', 'profit_factor', 'sharpe_ratio', 
                               'sortino_ratio', 'calmar_ratio', 'kelly_fraction']:
                if value >= 2.0:
                    return self.colors['good']
                elif value >= 1.5:
                    return self.colors['warning']
                else:
                    return self.colors['bad']
            elif metric_name in ['max_drawdown', 'volatility', 'mc_var_95', 'mc_cvar_95', 
                               'mc_max_loss', 'risk_of_ruin']:
                if value <= 10:
                    return self.colors['good']
                elif value <= 20:
                    return self.colors['warning']
                else:
                    return self.colors['bad']
            elif metric_name in ['total_return', 'net_return', 'mc_expected_return', 
                               'mc_probability_profit', 'mc_max_gain']:
                if value >= 20:
                    return self.colors['good']
                elif value >= 10:
                    return self.colors['warning']
                else:
                    return self.colors['bad']
            else:
                return self.colors['neutral']
        except:
            return self.colors['neutral']
    
    def add_metrics_to_plotly(self, fig: go.Figure, df: pd.DataFrame, 
                            metrics: Optional[Dict[str, float]] = None,
                            position: str = 'right',
                            lot_size: float = 1.0,
                            risk_reward_ratio: float = 2.0,
                            fee_per_trade: float = 0.07) -> go.Figure:
        """
        Add trading metrics to Plotly figure.
        NOTE: This method has been disabled - metrics are not displayed on HTML charts.
        Metrics are now displayed only in console output.
        
        Args:
            fig (go.Figure): Plotly figure
            df (pd.DataFrame): DataFrame with trading data
            metrics (Dict[str, float], optional): Pre-calculated metrics
            position (str): Position of metrics - not used
            lot_size (float): Position size - not used
            risk_reward_ratio (float): Risk to reward ratio - not used
            fee_per_trade (float): Fee per trade - not used
        
        Returns:
            go.Figure: Original figure unchanged (no metrics added)
        """
        # Metrics have been removed from HTML charts as requested
        # Return the original figure without any modifications
        return fig
    
    def add_metrics_to_matplotlib(self, ax: plt.Axes, df: pd.DataFrame,
                                metrics: Optional[Dict[str, float]] = None,
                                position: str = 'right') -> plt.Axes:
        """
        Add trading metrics to Matplotlib axes.
        NOTE: This method has been disabled - metrics are not displayed on charts.
        Metrics are now displayed only in console output.
        
        Args:
            ax (plt.Axes): Matplotlib axes
            df (pd.DataFrame): DataFrame with trading data
            metrics (Dict[str, float], optional): Pre-calculated metrics
            position (str): Position of metrics - not used
        
        Returns:
            plt.Axes: Original axes unchanged (no metrics added)
        """
        # Metrics have been removed from charts as requested
        # Return the original axes without any modifications
        return ax
    
    def _format_metrics_for_plotly(self, metrics: Dict[str, float]) -> str:
        """Format metrics for Plotly display - not used."""
        # This method is no longer used since metrics are not displayed on HTML charts
        return ""
    
    def _format_additional_metrics_for_plotly(self, metrics: Dict[str, float]) -> str:
        """Format additional ML and Monte Carlo metrics for Plotly display - not used."""
        # This method is no longer used since metrics are not displayed on HTML charts
        return ""
    
    def _add_matplotlib_metrics_text(self, ax: plt.Axes, metrics: Dict[str, float],
                                   position: str, xlim: Tuple[float, float], 
                                   ylim: Tuple[float, float]) -> None:
        """Add metrics text to Matplotlib axes - not used."""
        # This method is no longer used since metrics are not displayed on charts
        pass
    
    def get_metrics_summary(self, metrics: Dict[str, float]) -> str:
        """Get a concise summary of the most important metrics - not used for charts."""
        try:
            summary_lines = [
                f"Win Rate: {metrics['win_ratio']:.1f}% | ",
                f"R/R: {metrics['risk_reward_ratio']:.2f} | ",
                f"PF: {metrics['profit_factor']:.2f} | ",
                f"Return: {metrics['total_return']:.1f}% | ",
                f"Sharpe: {metrics['sharpe_ratio']:.2f}"
            ]
            return "".join(summary_lines)
            
        except Exception as e:
            logger.print_debug(f"Error creating metrics summary: {e}")
            return "Metrics calculation error"


def add_metrics_to_plotly_chart(fig: go.Figure, df: pd.DataFrame, 
                               metrics: Optional[Dict[str, float]] = None,
                               position: str = 'right',
                               lot_size: float = 1.0,
                               risk_reward_ratio: float = 2.0,
                               fee_per_trade: float = 0.07) -> go.Figure:
    """
    Add trading metrics to Plotly chart.
    NOTE: This function has been disabled - metrics are not displayed on HTML charts.
    Metrics are now displayed only in console output.
    
    Args:
        fig (go.Figure): Plotly figure
        df (pd.DataFrame): DataFrame with trading data
        metrics (Dict[str, float], optional): Pre-calculated metrics
        position (str): Position of metrics - not used
        lot_size (float): Position size - not used
        risk_reward_ratio (float): Risk to reward ratio - not used
        fee_per_trade (float): Fee per trade - not used
    
    Returns:
        go.Figure: Original figure unchanged (no metrics added)
    """
    # Metrics have been removed from HTML charts as requested
    # Return the original figure without any modifications
    return fig


def add_metrics_to_matplotlib_chart(ax: plt.Axes, df: pd.DataFrame,
                                  position: str = 'right') -> plt.Axes:
    """
    Convenience function to add metrics to Matplotlib chart.
    NOTE: This function has been disabled - metrics are not displayed on charts.
    Metrics are now displayed only in console output.
    
    Args:
        ax (plt.Axes): Matplotlib axes
        df (pd.DataFrame): DataFrame with trading data
        position (str): Position of metrics - not used
    
    Returns:
        plt.Axes: Original axes unchanged (no metrics added)
    """
    # Metrics have been removed from charts as requested
    # Return the original axes without any modifications
    return ax 