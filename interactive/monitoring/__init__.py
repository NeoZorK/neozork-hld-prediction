# -*- coding: utf-8 -*-
"""
Monitoring module for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive monitoring and alerting capabilities.
"""

from .system_monitor import SystemMonitor
from .performance_monitor import PerformanceMonitor
from .alert_manager import AlertManager
from .dashboard_generator import DashboardGenerator
from .prometheus_integration import PrometheusIntegration
from .grafana_dashboards import GrafanaDashboards
from .alerting_system import AlertingSystem
from .performance_monitoring import PerformanceMonitoring

class MonitoringSystem:
    """Main monitoring system class."""
    def __init__(self):
        self.system_monitor = SystemMonitor()
        self.performance_monitor = PerformanceMonitor()
        self.alert_manager = AlertManager()
        self.dashboard_generator = DashboardGenerator()
        self.prometheus_integration = PrometheusIntegration()
        self.grafana_dashboards = GrafanaDashboards()
        self.alerting_system = AlertingSystem()
        self.performance_monitoring = PerformanceMonitoring()

__all__ = [
    'MonitoringSystem',
    'SystemMonitor',
    'PerformanceMonitor',
    'AlertManager',
    'DashboardGenerator',
    'PrometheusIntegration',
    'GrafanaDashboards',
    'AlertingSystem',
    'PerformanceMonitoring'
]
