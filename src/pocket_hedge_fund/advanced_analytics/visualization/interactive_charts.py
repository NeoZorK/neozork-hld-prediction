"""
Interactive Charts for advanced analytics visualization.

This module provides interactive chart functionality for analytics visualizations.
"""

from typing import Dict, List, Any, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class InteractiveCharts:
    """Interactive charts for analytics visualization."""
    
    def __init__(self, chart_library: str = "plotly"):
        """Initialize interactive charts."""
        self.chart_library = chart_library
        self.charts: List[Dict[str, Any]] = []
        self.interactions: List[Dict[str, Any]] = []
        self.logger = logger
    
    def create_line_chart(self, data: Dict[str, Any], title: str = "") -> Dict[str, Any]:
        """Create an interactive line chart."""
        try:
            chart = {
                'type': 'line',
                'title': title or "Line Chart",
                'data': data,
                'library': self.chart_library,
                'interactive': True,
                'created_at': datetime.now().isoformat()
            }
            self.charts.append(chart)
            self.logger.info(f"Created interactive line chart: {title}")
            return chart
        except Exception as e:
            self.logger.error(f"Error creating line chart: {e}")
            return {}
    
    def create_bar_chart(self, data: Dict[str, Any], title: str = "") -> Dict[str, Any]:
        """Create an interactive bar chart."""
        try:
            chart = {
                'type': 'bar',
                'title': title or "Bar Chart",
                'data': data,
                'library': self.chart_library,
                'interactive': True,
                'created_at': datetime.now().isoformat()
            }
            self.charts.append(chart)
            self.logger.info(f"Created interactive bar chart: {title}")
            return chart
        except Exception as e:
            self.logger.error(f"Error creating bar chart: {e}")
            return {}
    
    def create_scatter_plot(self, data: Dict[str, Any], title: str = "") -> Dict[str, Any]:
        """Create an interactive scatter plot."""
        try:
            chart = {
                'type': 'scatter',
                'title': title or "Scatter Plot",
                'data': data,
                'library': self.chart_library,
                'interactive': True,
                'created_at': datetime.now().isoformat()
            }
            self.charts.append(chart)
            self.logger.info(f"Created interactive scatter plot: {title}")
            return chart
        except Exception as e:
            self.logger.error(f"Error creating scatter plot: {e}")
            return {}
    
    def create_heatmap(self, data: Dict[str, Any], title: str = "") -> Dict[str, Any]:
        """Create an interactive heatmap."""
        try:
            chart = {
                'type': 'heatmap',
                'title': title or "Heatmap",
                'data': data,
                'library': self.chart_library,
                'interactive': True,
                'created_at': datetime.now().isoformat()
            }
            self.charts.append(chart)
            self.logger.info(f"Created interactive heatmap: {title}")
            return chart
        except Exception as e:
            self.logger.error(f"Error creating heatmap: {e}")
            return {}
    
    def add_interaction(self, chart_id: str, interaction_type: str, config: Dict[str, Any]) -> bool:
        """Add an interaction to a chart."""
        try:
            interaction = {
                'chart_id': chart_id,
                'type': interaction_type,
                'config': config,
                'created_at': datetime.now().isoformat()
            }
            self.interactions.append(interaction)
            self.logger.info(f"Added {interaction_type} interaction to chart {chart_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding interaction: {e}")
            return False
    
    def get_chart(self, chart_id: str) -> Optional[Dict[str, Any]]:
        """Get a chart by ID."""
        for chart in self.charts:
            if chart.get('id') == chart_id:
                return chart
        return None
    
    def get_charts_by_type(self, chart_type: str) -> List[Dict[str, Any]]:
        """Get all charts of a specific type."""
        return [chart for chart in self.charts if chart.get('type') == chart_type]
    
    def export_chart(self, chart_id: str, format: str = "json") -> Optional[str]:
        """Export a chart in the specified format."""
        try:
            chart = self.get_chart(chart_id)
            if not chart:
                self.logger.warning(f"Chart {chart_id} not found")
                return None
            
            if format == "json":
                return json.dumps(chart, indent=2)
            else:
                self.logger.warning(f"Unsupported export format: {format}")
                return None
        except Exception as e:
            self.logger.error(f"Error exporting chart: {e}")
            return None
    
    def get_chart_count(self) -> int:
        """Get the number of charts."""
        return len(self.charts)
    
    def get_interaction_count(self) -> int:
        """Get the number of interactions."""
        return len(self.interactions)
    
    def clear_charts(self) -> 'InteractiveCharts':
        """Clear all charts."""
        self.charts = []
        self.logger.info("All charts cleared")
        return self
    
    def clear_interactions(self) -> 'InteractiveCharts':
        """Clear all interactions."""
        self.interactions = []
        self.logger.info("All interactions cleared")
        return self
    
    def clear_all(self) -> 'InteractiveCharts':
        """Clear all charts and interactions."""
        self.clear_charts()
        self.clear_interactions()
        return self
