"""
Dashboard Builder for advanced analytics visualization.

This module provides dashboard building functionality for analytics visualizations.
"""

from typing import Dict, List, Any, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DashboardBuilder:
    """Builder for analytics dashboards."""
    
    def __init__(self, title: str = "Analytics Dashboard"):
        """Initialize dashboard builder."""
        self.title = title
        self.widgets: List[Dict[str, Any]] = []
        self.layout: Dict[str, Any] = {}
        self.logger = logger
    
    def add_widget(self, widget_type: str, data: Dict[str, Any], position: Dict[str, int]) -> 'DashboardBuilder':
        """Add a widget to the dashboard."""
        try:
            widget = {
                'id': f"widget_{len(self.widgets) + 1}",
                'type': widget_type,
                'data': data,
                'position': position,
                'created_at': datetime.now().isoformat()
            }
            self.widgets.append(widget)
            self.logger.info(f"Added {widget_type} widget to dashboard")
            return self
        except Exception as e:
            self.logger.error(f"Error adding widget: {e}")
            return self
    
    def add_chart(self, chart_data: Dict[str, Any], position: Dict[str, int]) -> 'DashboardBuilder':
        """Add a chart widget to the dashboard."""
        return self.add_widget('chart', chart_data, position)
    
    def add_metric(self, metric_data: Dict[str, Any], position: Dict[str, int]) -> 'DashboardBuilder':
        """Add a metric widget to the dashboard."""
        return self.add_widget('metric', metric_data, position)
    
    def add_table(self, table_data: Dict[str, Any], position: Dict[str, int]) -> 'DashboardBuilder':
        """Add a table widget to the dashboard."""
        return self.add_widget('table', table_data, position)
    
    def set_layout(self, layout_config: Dict[str, Any]) -> 'DashboardBuilder':
        """Set dashboard layout configuration."""
        try:
            self.layout = layout_config
            self.logger.info("Dashboard layout configured")
            return self
        except Exception as e:
            self.logger.error(f"Error setting layout: {e}")
            return self
    
    def build(self) -> Dict[str, Any]:
        """Build the dashboard configuration."""
        try:
            dashboard = {
                'title': self.title,
                'widgets': self.widgets,
                'layout': self.layout,
                'created_at': datetime.now().isoformat(),
                'version': '1.0'
            }
            self.logger.info(f"Dashboard built with {len(self.widgets)} widgets")
            return dashboard
        except Exception as e:
            self.logger.error(f"Error building dashboard: {e}")
            return {}
    
    def export_json(self, filepath: str) -> bool:
        """Export dashboard to JSON file."""
        try:
            dashboard = self.build()
            with open(filepath, 'w') as f:
                json.dump(dashboard, f, indent=2)
            self.logger.info(f"Dashboard exported to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting dashboard: {e}")
            return False
    
    def get_widget_count(self) -> int:
        """Get the number of widgets in the dashboard."""
        return len(self.widgets)
    
    def get_widget_by_id(self, widget_id: str) -> Optional[Dict[str, Any]]:
        """Get a widget by its ID."""
        for widget in self.widgets:
            if widget['id'] == widget_id:
                return widget
        return None
    
    def remove_widget(self, widget_id: str) -> bool:
        """Remove a widget from the dashboard."""
        try:
            self.widgets = [w for w in self.widgets if w['id'] != widget_id]
            self.logger.info(f"Widget {widget_id} removed from dashboard")
            return True
        except Exception as e:
            self.logger.error(f"Error removing widget: {e}")
            return False
    
    def clear_widgets(self) -> 'DashboardBuilder':
        """Clear all widgets from the dashboard."""
        self.widgets = []
        self.logger.info("All widgets cleared from dashboard")
        return self
