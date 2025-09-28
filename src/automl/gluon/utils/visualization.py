"""
Visualization Utilities for SCHR Levels AutoML

Provides plotting and visualization utilities.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, List, Optional


class PlotUtils:
    """Utility functions for creating plots"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.colors = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#00ff88',
            'warning': '#ffa500',
            'danger': '#ff4444',
            'info': '#0066cc'
        }
    
    def create_line_plot(self, x: List, y: List, title: str, 
                         x_label: str = "X", y_label: str = "Y") -> go.Figure:
        """Create a simple line plot"""
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                mode='lines',
                name=title,
                line=dict(color=self.colors['primary'], width=2)
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title=x_label,
                yaxis_title=y_label,
                template='plotly_dark',
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Failed to create line plot: {e}")
            return go.Figure()
    
    def create_bar_plot(self, x: List, y: List, title: str,
                       x_label: str = "X", y_label: str = "Y") -> go.Figure:
        """Create a bar plot"""
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=x,
                y=y,
                name=title,
                marker_color=self.colors['primary']
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title=x_label,
                yaxis_title=y_label,
                template='plotly_dark'
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Failed to create bar plot: {e}")
            return go.Figure()
    
    def create_histogram(self, data: List, title: str, 
                        x_label: str = "Value", y_label: str = "Frequency") -> go.Figure:
        """Create a histogram"""
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Histogram(
                x=data,
                name=title,
                marker_color=self.colors['secondary']
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title=x_label,
                yaxis_title=y_label,
                template='plotly_dark'
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Failed to create histogram: {e}")
            return go.Figure()
    
    def create_heatmap(self, data: np.ndarray, x_labels: List, y_labels: List,
                      title: str) -> go.Figure:
        """Create a heatmap"""
        try:
            fig = go.Figure(data=go.Heatmap(
                z=data,
                x=x_labels,
                y=y_labels,
                colorscale='RdYlBu_r',
                hoverongaps=False
            ))
            
            fig.update_layout(
                title=title,
                template='plotly_dark'
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Failed to create heatmap: {e}")
            return go.Figure()
    
    def create_subplot(self, rows: int, cols: int, titles: List[str]) -> go.Figure:
        """Create a subplot figure"""
        try:
            fig = make_subplots(
                rows=rows, cols=cols,
                subplot_titles=titles,
                specs=[[{"secondary_y": False}] * cols] * rows
            )
            
            fig.update_layout(
                template='plotly_dark',
                height=400 * rows
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Failed to create subplot: {e}")
            return go.Figure()
