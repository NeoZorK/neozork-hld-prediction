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
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
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
    
    def add_metrics_to_plotly(self, fig: go.Figure, df: pd.DataFrame, 
                            metrics: Optional[Dict[str, float]] = None,
                            position: str = 'right') -> go.Figure:
        """
        Add trading metrics to Plotly figure.
        
        Args:
            fig (go.Figure): Plotly figure
            df (pd.DataFrame): DataFrame with trading data
            metrics (Dict[str, float], optional): Pre-calculated metrics
            position (str): Position of metrics box ('right', 'left', 'top', 'bottom')
        
        Returns:
            go.Figure: Updated figure with metrics
        """
        try:
            # Calculate metrics if not provided
            if metrics is None:
                metrics = calculate_trading_metrics(df)
            
            # Create metrics text
            metrics_text = self._format_metrics_for_plotly(metrics)
            
            # Add annotation based on position
            if position == 'right':
                x_pos, y_pos, xanchor, yanchor = 1.02, 0.98, 'left', 'top'
            elif position == 'left':
                x_pos, y_pos, xanchor, yanchor = -0.02, 0.98, 'right', 'top'
            elif position == 'top':
                x_pos, y_pos, xanchor, yanchor = 0.5, 1.02, 'center', 'bottom'
            else:  # bottom
                x_pos, y_pos, xanchor, yanchor = 0.5, -0.02, 'center', 'top'
            
            # Add metrics annotation
            fig.add_annotation(
                x=x_pos,
                y=y_pos,
                text=metrics_text,
                showarrow=False,
                xanchor=xanchor,
                yanchor=yanchor,
                font=dict(
                    family="Courier New, monospace",
                    size=10,
                    color=self.colors['text']
                ),
                bgcolor=self.colors['background'],
                bordercolor=self.colors['border'],
                borderwidth=1,
                align="left"
            )
            
            return fig
            
        except Exception as e:
            logger.print_error(f"Error adding metrics to Plotly chart: {e}")
            return fig
    
    def add_metrics_to_matplotlib(self, ax: plt.Axes, df: pd.DataFrame,
                                metrics: Optional[Dict[str, float]] = None,
                                position: str = 'right') -> plt.Axes:
        """
        Add trading metrics to Matplotlib axes.
        
        Args:
            ax (plt.Axes): Matplotlib axes
            df (pd.DataFrame): DataFrame with trading data
            metrics (Dict[str, float], optional): Pre-calculated metrics
            position (str): Position of metrics box ('right', 'left', 'top', 'bottom')
        
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
            
            # Create metrics box
            metrics_box = self._create_matplotlib_metrics_box(metrics, position, xlim, ylim)
            
            # Add box to axes
            ax.add_patch(metrics_box)
            
            # Add metrics text
            self._add_matplotlib_metrics_text(ax, metrics, position, xlim, ylim)
            
            return ax
            
        except Exception as e:
            logger.print_error(f"Error adding metrics to Matplotlib chart: {e}")
            return ax
    
    def _format_metrics_for_plotly(self, metrics: Dict[str, float]) -> str:
        """Format metrics for Plotly display."""
        try:
            lines = [
                "<b>📊 TRADING METRICS</b>",
                "─" * 25,
                f"🎯 Win Ratio: {metrics['win_ratio']:.1f}%",
                f"⚖️  Risk/Reward: {metrics['risk_reward_ratio']:.2f}",
                f"💰 Profit Factor: {metrics['profit_factor']:.2f}",
                f"📈 Total Return: {metrics['total_return']:.1f}%",
                f"📉 Max Drawdown: {metrics['max_drawdown']:.1f}%",
                f"📊 Sharpe Ratio: {metrics['sharpe_ratio']:.2f}",
                f"🛡️  Sortino Ratio: {metrics['sortino_ratio']:.2f}",
                f"🎲 Prob Risk Ratio: {metrics['probability_risk_ratio']:.2f}",
                f"📈 Volatility: {metrics['volatility']:.1f}%",
                f"⚡ Calmar Ratio: {metrics['calmar_ratio']:.2f}"
            ]
            
            # Add volume metrics if available
            if 'volume_weighted_return' in metrics and metrics['volume_weighted_return'] != 0:
                lines.extend([
                    f"📊 Vol Weighted Return: {metrics['volume_weighted_return']:.2f}%",
                    f"📊 Vol Win Ratio: {metrics['volume_win_ratio']:.1f}%"
                ])
            
            return "<br>".join(lines)
            
        except Exception as e:
            logger.print_debug(f"Error formatting metrics for Plotly: {e}")
            return "📊 Trading Metrics<br>Error displaying metrics"
    
    def _create_matplotlib_metrics_box(self, metrics: Dict[str, float], 
                                     position: str, xlim: Tuple[float, float], 
                                     ylim: Tuple[float, float]) -> FancyBboxPatch:
        """Create metrics box for Matplotlib."""
        try:
            # Calculate box position and size
            if position == 'right':
                x = xlim[1] + (xlim[1] - xlim[0]) * 0.02
                y = ylim[1] - (ylim[1] - ylim[0]) * 0.3
                width = (xlim[1] - xlim[0]) * 0.25
                height = (ylim[1] - ylim[0]) * 0.3
            elif position == 'left':
                x = xlim[0] - (xlim[1] - xlim[0]) * 0.27
                y = ylim[1] - (ylim[1] - ylim[0]) * 0.3
                width = (xlim[1] - xlim[0]) * 0.25
                height = (ylim[1] - ylim[0]) * 0.3
            elif position == 'top':
                x = xlim[0] + (xlim[1] - xlim[0]) * 0.1
                y = ylim[1] + (ylim[1] - ylim[0]) * 0.02
                width = (xlim[1] - xlim[0]) * 0.8
                height = (ylim[1] - ylim[0]) * 0.15
            else:  # bottom
                x = xlim[0] + (xlim[1] - xlim[0]) * 0.1
                y = ylim[0] - (ylim[1] - ylim[0]) * 0.17
                width = (xlim[1] - xlim[0]) * 0.8
                height = (ylim[1] - ylim[0]) * 0.15
            
            # Create fancy box
            box = FancyBboxPatch(
                (x, y), width, height,
                boxstyle="round,pad=0.02",
                facecolor=self.colors['background'],
                edgecolor=self.colors['border'],
                linewidth=1.5,
                alpha=0.95
            )
            
            return box
            
        except Exception as e:
            logger.print_debug(f"Error creating Matplotlib metrics box: {e}")
            # Return a simple rectangle as fallback
            return patches.Rectangle((0, 0), 1, 1, facecolor='white', alpha=0.8)
    
    def _add_matplotlib_metrics_text(self, ax: plt.Axes, metrics: Dict[str, float],
                                   position: str, xlim: Tuple[float, float], 
                                   ylim: Tuple[float, float]) -> None:
        """Add metrics text to Matplotlib axes."""
        try:
            # Calculate text position
            if position == 'right':
                x = xlim[1] + (xlim[1] - xlim[0]) * 0.025
                y = ylim[1] - (ylim[1] - ylim[0]) * 0.05
                ha, va = 'left', 'top'
            elif position == 'left':
                x = xlim[0] - (xlim[1] - xlim[0]) * 0.255
                y = ylim[1] - (ylim[1] - ylim[0]) * 0.05
                ha, va = 'left', 'top'
            elif position == 'top':
                x = xlim[0] + (xlim[1] - xlim[0]) * 0.125
                y = ylim[1] + (ylim[1] - ylim[0]) * 0.025
                ha, va = 'left', 'bottom'
            else:  # bottom
                x = xlim[0] + (xlim[1] - xlim[0]) * 0.125
                y = ylim[0] - (ylim[1] - ylim[0]) * 0.155
                ha, va = 'left', 'top'
            
            # Create metrics text
            lines = [
                "📊 TRADING METRICS",
                "─" * 25,
                f"🎯 Win Ratio: {metrics['win_ratio']:.1f}%",
                f"⚖️  Risk/Reward: {metrics['risk_reward_ratio']:.2f}",
                f"💰 Profit Factor: {metrics['profit_factor']:.2f}",
                f"📈 Total Return: {metrics['total_return']:.1f}%",
                f"📉 Max Drawdown: {metrics['max_drawdown']:.1f}%",
                f"📊 Sharpe Ratio: {metrics['sharpe_ratio']:.2f}",
                f"🛡️  Sortino Ratio: {metrics['sortino_ratio']:.2f}",
                f"🎲 Prob Risk Ratio: {metrics['probability_risk_ratio']:.2f}",
                f"📈 Volatility: {metrics['volatility']:.1f}%",
                f"⚡ Calmar Ratio: {metrics['calmar_ratio']:.2f}"
            ]
            
            # Add volume metrics if available
            if 'volume_weighted_return' in metrics and metrics['volume_weighted_return'] != 0:
                lines.extend([
                    f"📊 Vol Weighted Return: {metrics['volume_weighted_return']:.2f}%",
                    f"📊 Vol Win Ratio: {metrics['volume_win_ratio']:.1f}%"
                ])
            
            # Add text with styling
            text = ax.text(x, y, '\n'.join(lines), 
                          fontsize=8, fontfamily='monospace',
                          color=self.colors['text'],
                          ha=ha, va=va,
                          bbox=dict(boxstyle="round,pad=0.5", 
                                   facecolor=self.colors['background'],
                                   edgecolor=self.colors['border'],
                                   alpha=0.95))
            
            # Add text effects for better visibility
            text.set_path_effects([path_effects.withStroke(linewidth=2, foreground=self.colors['background'])])
            
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