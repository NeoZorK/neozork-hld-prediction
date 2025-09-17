"""
Report Visualizer for advanced analytics.

This module provides report visualization functionality for analytics reports.
"""

from typing import Dict, List, Any, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ReportVisualizer:
    """Visualizer for analytics reports."""
    
    def __init__(self, report_title: str = "Analytics Report"):
        """Initialize report visualizer."""
        self.report_title = report_title
        self.sections: List[Dict[str, Any]] = []
        self.charts: List[Dict[str, Any]] = []
        self.metrics: List[Dict[str, Any]] = []
        self.logger = logger
    
    def add_section(self, title: str, content: Dict[str, Any]) -> 'ReportVisualizer':
        """Add a section to the report."""
        try:
            section = {
                'title': title,
                'content': content,
                'created_at': datetime.now().isoformat()
            }
            self.sections.append(section)
            self.logger.info(f"Added section '{title}' to report")
            return self
        except Exception as e:
            self.logger.error(f"Error adding section: {e}")
            return self
    
    def add_chart(self, chart_type: str, data: Dict[str, Any], title: str = "") -> 'ReportVisualizer':
        """Add a chart to the report."""
        try:
            chart = {
                'type': chart_type,
                'data': data,
                'title': title or f"{chart_type.title()} Chart",
                'created_at': datetime.now().isoformat()
            }
            self.charts.append(chart)
            self.logger.info(f"Added {chart_type} chart to report")
            return self
        except Exception as e:
            self.logger.error(f"Error adding chart: {e}")
            return self
    
    def add_metric(self, name: str, value: Any, unit: str = "", description: str = "") -> 'ReportVisualizer':
        """Add a metric to the report."""
        try:
            metric = {
                'name': name,
                'value': value,
                'unit': unit,
                'description': description,
                'created_at': datetime.now().isoformat()
            }
            self.metrics.append(metric)
            self.logger.info(f"Added metric '{name}' to report")
            return self
        except Exception as e:
            self.logger.error(f"Error adding metric: {e}")
            return self
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate the complete report."""
        try:
            report = {
                'title': self.report_title,
                'sections': self.sections,
                'charts': self.charts,
                'metrics': self.metrics,
                'generated_at': datetime.now().isoformat(),
                'version': '1.0'
            }
            self.logger.info(f"Report generated with {len(self.sections)} sections, {len(self.charts)} charts, {len(self.metrics)} metrics")
            return report
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            return {}
    
    def export_json(self, filepath: str) -> bool:
        """Export report to JSON file."""
        try:
            report = self.generate_report()
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            self.logger.info(f"Report exported to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting report: {e}")
            return False
    
    def get_section_count(self) -> int:
        """Get the number of sections in the report."""
        return len(self.sections)
    
    def get_chart_count(self) -> int:
        """Get the number of charts in the report."""
        return len(self.charts)
    
    def get_metric_count(self) -> int:
        """Get the number of metrics in the report."""
        return len(self.metrics)
    
    def clear_sections(self) -> 'ReportVisualizer':
        """Clear all sections from the report."""
        self.sections = []
        self.logger.info("All sections cleared from report")
        return self
    
    def clear_charts(self) -> 'ReportVisualizer':
        """Clear all charts from the report."""
        self.charts = []
        self.logger.info("All charts cleared from report")
        return self
    
    def clear_metrics(self) -> 'ReportVisualizer':
        """Clear all metrics from the report."""
        self.metrics = []
        self.logger.info("All metrics cleared from report")
        return self
    
    def clear_all(self) -> 'ReportVisualizer':
        """Clear all content from the report."""
        self.clear_sections()
        self.clear_charts()
        self.clear_metrics()
        return self
