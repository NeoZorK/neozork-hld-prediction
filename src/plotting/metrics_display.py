# -*- coding: utf-8 -*-
# src/plotting/metrics_display.py

"""
Trading Metrics Display Module
Provides beautiful and informative display of trading metrics on charts.
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
    Beautiful trading metrics display for charts.
    """
    
    def __init__(self, theme: str = 'dark'):
        """
        Initialize metrics display.
        
        Args:
            theme (str): Display theme ('dark' or 'light')
        """
        self.theme = theme
        self.colors = self._get_theme_colors()
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """Get color scheme based on theme."""
        if self.theme == 'dark':
            return {
                'background': '#1e1e1e',
                'text': '#ffffff',
                'border': '#404040',
                'win': '#00ff88',
                'loss': '#ff4444',
                'neutral': '#888888',
                'good': '#00cc66',
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
                'warning': '#cc6600',
                'danger': '#cc0000'
            }
    
    def _get_metric_color(self, metric: str, value: float) -> str:
        """Return color hex for a metric value based on standard trading thresholds."""
        # Standard thresholds for each metric
        thresholds = {
            'win_ratio':      [(60, 'green'), (40, 'yellow'), (0, 'red')],
            'risk_reward_ratio': [(2.0, 'green'), (1.2, 'yellow'), (0, 'red')],
            'profit_factor': [(1.5, 'green'), (1.1, 'yellow'), (0, 'red')],
            'sharpe_ratio':  [(1.0, 'green'), (0.5, 'yellow'), (0, 'red')],
            'sortino_ratio': [(1.5, 'green'), (0.8, 'yellow'), (0, 'red')],
            'max_drawdown':  [(10, 'green', True), (25, 'yellow', True), (float('inf'), 'red', True)],
            'total_return':  [(20, 'green'), (5, 'yellow'), (float('-inf'), 'red')],
            'volatility':    [(15, 'green', True), (30, 'yellow', True), (float('inf'), 'red', True)],
            'calmar_ratio':  [(1.0, 'green'), (0.5, 'yellow'), (0, 'red')],
        }
        # Color hex mapping
        color_map = {'green': '#00ff88', 'yellow': '#ffaa00', 'red': '#ff4444'}
        # For metrics where lower is better (drawdown, volatility), use reverse logic
        if metric in thresholds:
            for t in thresholds[metric]:
                if len(t) == 3 and t[2]:  # Lower is better
                    if value <= t[0]:
                        return color_map[t[1]]
                else:  # Higher is better
                    if value >= t[0]:
                        return color_map[t[1]]
        return self.colors['neutral']
    
    def add_metrics_to_plotly(self, fig: go.Figure, df: pd.DataFrame, 
                            metrics: Optional[Dict[str, float]] = None,
                            position: str = 'right') -> go.Figure:
        """
        Add trading metrics to Plotly figure near the legend area.
        """
        try:
            if metrics is None:
                metrics = calculate_trading_metrics(df)
            metrics_text = self._format_metrics_for_plotly(metrics)
            # Place metrics near the legend area (top-right of plot)
            fig.add_annotation(
                x=0.98,  # near right edge of plot
                y=0.95,  # near top of plot
                text=metrics_text,
                showarrow=False,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                font=dict(
                    family="Courier New, monospace",
                    size=10,
                    color=self.colors['text']
                ),
                bgcolor=self.colors['background'],
                bordercolor=self.colors['border'],
                borderwidth=1,
                align="right"
            )
            return fig
        except Exception as e:
            logger.print_error(f"Error adding metrics to Plotly chart: {e}")
            return fig
    
    def add_metrics_to_matplotlib(self, ax: plt.Axes, df: pd.DataFrame,
                                metrics: Optional[Dict[str, float]] = None,
                                position: str = 'right') -> plt.Axes:
        """
        Add trading metrics to Matplotlib axes near the legend area.
        
        Args:
            ax (plt.Axes): Matplotlib axes
            df (pd.DataFrame): DataFrame with trading data
            metrics (Dict[str, float], optional): Pre-calculated metrics
            position (str): Position of metrics ('right', 'left', 'top', 'bottom')
        
        Returns:
            plt.Axes: Updated axes with metrics
        """
        try:
            # Calculate metrics if not provided
            if metrics is None:
                metrics = calculate_trading_metrics(df)
            
            # Get axes limits for positioning
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            
            # Add metrics text near legend area (top-right)
            self._add_matplotlib_metrics_text(ax, metrics, position, xlim, ylim)
            
            return ax
            
        except Exception as e:
            logger.print_error(f"Error adding metrics to Matplotlib chart: {e}")
            return ax
    
    def _format_metrics_for_plotly(self, metrics: Dict[str, float]) -> str:
        """Format metrics for Plotly display with colorized values near legend."""
        try:
            def color_span(val, color):
                return f'<span style="color:{color};font-weight:bold">{val}</span>'
            lines = [
                "<b>📊 TRADING METRICS</b>",
                "─" * 20,
                f"🎯 Win Ratio: {color_span(f'{metrics['win_ratio']:.1f}%', self._get_metric_color('win_ratio', metrics['win_ratio']))}",
                f"⚖️  Risk/Reward: {color_span(f'{metrics['risk_reward_ratio']:.2f}', self._get_metric_color('risk_reward_ratio', metrics['risk_reward_ratio']))}",
                f"💰 Profit Factor: {color_span(f'{metrics['profit_factor']:.2f}', self._get_metric_color('profit_factor', metrics['profit_factor']))}",
                f"📈 Total Return: {color_span(f'{metrics['total_return']:.1f}%', self._get_metric_color('total_return', metrics['total_return']))}",
                f"📉 Max Drawdown: {color_span(f'{metrics['max_drawdown']:.1f}%', self._get_metric_color('max_drawdown', metrics['max_drawdown']))}",
                f"📊 Sharpe Ratio: {color_span(f'{metrics['sharpe_ratio']:.2f}', self._get_metric_color('sharpe_ratio', metrics['sharpe_ratio']))}",
                f"🛡️  Sortino Ratio: {color_span(f'{metrics['sortino_ratio']:.2f}', self._get_metric_color('sortino_ratio', metrics['sortino_ratio']))}",
                f"🎲 Prob Risk Ratio: {color_span(f'{metrics['probability_risk_ratio']:.2f}', self.colors['neutral'])}",
                f"📈 Volatility: {color_span(f'{metrics['volatility']:.1f}%', self._get_metric_color('volatility', metrics['volatility']))}",
                f"⚡ Calmar Ratio: {color_span(f'{metrics['calmar_ratio']:.2f}', self._get_metric_color('calmar_ratio', metrics['calmar_ratio']))}"
            ]
            if 'volume_weighted_return' in metrics and metrics['volume_weighted_return'] != 0:
                lines.extend([
                    f"📊 Vol Weighted Return: {color_span(f'{metrics['volume_weighted_return']:.2f}%', self.colors['neutral'])}",
                    f"📊 Vol Win Ratio: {color_span(f'{metrics['volume_win_ratio']:.1f}%', self.colors['neutral'])}"
                ])
            return "<br>".join(lines)
        except Exception as e:
            logger.print_debug(f"Error formatting metrics for Plotly: {e}")
            return "📊 Trading Metrics<br>Error displaying metrics"
    
    def _add_matplotlib_metrics_text(self, ax: plt.Axes, metrics: Dict[str, float],
                                   position: str, xlim: Tuple[float, float], 
                                   ylim: Tuple[float, float]) -> None:
        """Add metrics text to Matplotlib axes near legend area."""
        try:
            def colorize(val, color):
                return f"\\color{{{color}}}{{{val}}}"
            
            # Position near legend area (top-right of plot)
            if position == 'right':
                x = xlim[1] - (xlim[1] - xlim[0]) * 0.02
                y = ylim[1] - (ylim[1] - ylim[0]) * 0.05
                ha = 'right'
            elif position == 'left':
                x = xlim[0] + (xlim[1] - xlim[0]) * 0.02
                y = ylim[1] - (ylim[1] - ylim[0]) * 0.05
                ha = 'left'
            elif position == 'top':
                x = xlim[1] - (xlim[1] - xlim[0]) * 0.02
                y = ylim[1] - (ylim[1] - ylim[0]) * 0.02
                ha = 'right'
            else:  # bottom
                x = xlim[1] - (xlim[1] - xlim[0]) * 0.02
                y = ylim[0] + (ylim[1] - ylim[0]) * 0.05
                ha = 'right'
            
            # Format metrics text
            lines = [
                "📊 TRADING METRICS",
                "─" * 20,
                f"🎯 Win Ratio: {colorize(f'{metrics['win_ratio']:.1f}%', self._get_metric_color('win_ratio', metrics['win_ratio']))}",
                f"⚖️  Risk/Reward: {colorize(f'{metrics['risk_reward_ratio']:.2f}', self._get_metric_color('risk_reward_ratio', metrics['risk_reward_ratio']))}",
                f"💰 Profit Factor: {colorize(f'{metrics['profit_factor']:.2f}', self._get_metric_color('profit_factor', metrics['profit_factor']))}",
                f"📈 Total Return: {colorize(f'{metrics['total_return']:.1f}%', self._get_metric_color('total_return', metrics['total_return']))}",
                f"📉 Max Drawdown: {colorize(f'{metrics['max_drawdown']:.1f}%', self._get_metric_color('max_drawdown', metrics['max_drawdown']))}",
                f"📊 Sharpe Ratio: {colorize(f'{metrics['sharpe_ratio']:.2f}', self._get_metric_color('sharpe_ratio', metrics['sharpe_ratio']))}",
                f"🛡️  Sortino Ratio: {colorize(f'{metrics['sortino_ratio']:.2f}', self._get_metric_color('sortino_ratio', metrics['sortino_ratio']))}",
                f"🎲 Prob Risk Ratio: {colorize(f'{metrics['probability_risk_ratio']:.2f}', self.colors['neutral'])}",
                f"📈 Volatility: {colorize(f'{metrics['volatility']:.1f}%', self._get_metric_color('volatility', metrics['volatility']))}",
                f"⚡ Calmar Ratio: {colorize(f'{metrics['calmar_ratio']:.2f}', self._get_metric_color('calmar_ratio', metrics['calmar_ratio']))}"
            ]
            
            if 'volume_weighted_return' in metrics and metrics['volume_weighted_return'] != 0:
                lines.extend([
                    f"📊 Vol Weighted Return: {colorize(f'{metrics['volume_weighted_return']:.2f}%', self.colors['neutral'])}",
                    f"📊 Vol Win Ratio: {colorize(f'{metrics['volume_win_ratio']:.1f}%', self.colors['neutral'])}"
                ])
            
            # Add text with background box
            text = '\n'.join(lines)
            bbox_props = dict(
                boxstyle="round,pad=0.5",
                facecolor=self.colors['background'],
                edgecolor=self.colors['border'],
                alpha=0.9
            )
            
            ax.text(x, y, text, fontsize=8, ha=ha, va='top',
                   bbox=bbox_props, color=self.colors['text'],
                   fontfamily='monospace')
            
        except Exception as e:
            logger.print_debug(f"Error adding Matplotlib metrics text: {e}")
    
    def get_metrics_summary(self, metrics: Dict[str, float]) -> str:
        """Get a concise summary of the most important metrics."""
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
                               position: str = 'right') -> go.Figure:
    """
    Convenience function to add metrics to Plotly chart.
    
    Args:
        fig (go.Figure): Plotly figure
        df (pd.DataFrame): DataFrame with trading data
        position (str): Position of metrics box
    
    Returns:
        go.Figure: Updated figure with metrics
    """
    display = MetricsDisplay()
    return display.add_metrics_to_plotly(fig, df, position=position)


def add_metrics_to_matplotlib_chart(ax: plt.Axes, df: pd.DataFrame,
                                  position: str = 'right') -> plt.Axes:
    """
    Convenience function to add metrics to Matplotlib chart.
    
    Args:
        ax (plt.Axes): Matplotlib axes
        df (pd.DataFrame): DataFrame with trading data
        position (str): Position of metrics box
    
    Returns:
        plt.Axes: Updated axes with metrics
    """
    display = MetricsDisplay()
    return display.add_metrics_to_matplotlib(ax, df, position=position) 