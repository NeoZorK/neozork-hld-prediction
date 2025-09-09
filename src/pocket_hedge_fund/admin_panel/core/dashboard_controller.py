"""
Dashboard Controller

Controls dashboard functionality and data aggregation.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal

from ..models.admin_models import (
    AdminUser, AdminDashboard, AdminWidget, AdminChart,
    AdminTable, AdminAlert, AdminRoleType, AdminPermissionType
)

logger = logging.getLogger(__name__)


class DashboardController:
    """
    Controls dashboard functionality and data aggregation.
    """
    
    def __init__(self, db_manager=None):
        """Initialize dashboard controller."""
        self.db_manager = db_manager
        self.dashboards = {}
        self.widgets = {}
        self.charts = {}
        self.tables = {}
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize dashboard controller."""
        try:
            # Load default dashboards
            await self._load_default_dashboards()
            
            # Load default widgets
            await self._load_default_widgets()
            
            # Load default charts
            await self._load_default_charts()
            
            # Load default tables
            await self._load_default_tables()
            
            self.is_initialized = True
            logger.info("Dashboard controller initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize dashboard controller: {e}")
            raise
    
    async def _load_default_dashboards(self):
        """Load default dashboards."""
        try:
            # Create default dashboard
            default_dashboard = AdminDashboard(
                name="default",
                description="Default admin dashboard",
                layout={
                    "columns": 12,
                    "rows": 8,
                    "widgets": [
                        {"id": "system_metrics", "x": 0, "y": 0, "width": 6, "height": 3},
                        {"id": "user_activity", "x": 6, "y": 0, "width": 6, "height": 3},
                        {"id": "recent_alerts", "x": 0, "y": 3, "width": 4, "height": 3},
                        {"id": "system_health", "x": 4, "y": 3, "width": 4, "height": 3},
                        {"id": "audit_log", "x": 8, "y": 3, "width": 4, "height": 3},
                        {"id": "performance_chart", "x": 0, "y": 6, "width": 8, "height": 2},
                        {"id": "quick_actions", "x": 8, "y": 6, "width": 4, "height": 2}
                    ]
                },
                widgets=[
                    "system_metrics", "user_activity", "recent_alerts",
                    "system_health", "audit_log", "performance_chart", "quick_actions"
                ],
                is_default=True,
                created_by="system"
            )
            
            self.dashboards["default"] = default_dashboard
            
            # Create role-specific dashboards
            role_dashboards = {
                "super_admin": AdminDashboard(
                    name="super_admin",
                    description="Super Administrator Dashboard",
                    layout=default_dashboard.layout,
                    widgets=default_dashboard.widgets + ["security_overview", "backup_status"],
                    created_by="system"
                ),
                "admin": AdminDashboard(
                    name="admin",
                    description="Administrator Dashboard",
                    layout=default_dashboard.layout,
                    widgets=default_dashboard.widgets,
                    created_by="system"
                ),
                "moderator": AdminDashboard(
                    name="moderator",
                    description="Moderator Dashboard",
                    layout={
                        "columns": 12,
                        "rows": 6,
                        "widgets": [
                            {"id": "user_activity", "x": 0, "y": 0, "width": 6, "height": 3},
                            {"id": "recent_alerts", "x": 6, "y": 0, "width": 6, "height": 3},
                            {"id": "audit_log", "x": 0, "y": 3, "width": 12, "height": 3}
                        ]
                    },
                    widgets=["user_activity", "recent_alerts", "audit_log"],
                    created_by="system"
                ),
                "viewer": AdminDashboard(
                    name="viewer",
                    description="Viewer Dashboard",
                    layout={
                        "columns": 12,
                        "rows": 4,
                        "widgets": [
                            {"id": "system_metrics", "x": 0, "y": 0, "width": 6, "height": 2},
                            {"id": "system_health", "x": 6, "y": 0, "width": 6, "height": 2},
                            {"id": "performance_chart", "x": 0, "y": 2, "width": 12, "height": 2}
                        ]
                    },
                    widgets=["system_metrics", "system_health", "performance_chart"],
                    created_by="system"
                )
            }
            
            for role, dashboard in role_dashboards.items():
                self.dashboards[role] = dashboard
            
            logger.info("Loaded default dashboards")
        except Exception as e:
            logger.error(f"Failed to load default dashboards: {e}")
            raise
    
    async def _load_default_widgets(self):
        """Load default widgets."""
        try:
            default_widgets = {
                "system_metrics": AdminWidget(
                    name="system_metrics",
                    type="metrics_card",
                    title="System Metrics",
                    description="Current system performance metrics",
                    configuration={
                        "metrics": ["cpu_usage", "memory_usage", "disk_usage", "network_io"],
                        "refresh_interval": 30,
                        "show_trends": True
                    },
                    data_source="system_monitor",
                    refresh_interval=30
                ),
                "user_activity": AdminWidget(
                    name="user_activity",
                    type="table",
                    title="Recent User Activity",
                    description="Latest user login and activity",
                    configuration={
                        "columns": ["username", "action", "timestamp", "ip_address"],
                        "max_rows": 10,
                        "sort_by": "timestamp",
                        "sort_order": "desc"
                    },
                    data_source="audit_log",
                    refresh_interval=60
                ),
                "recent_alerts": AdminWidget(
                    name="recent_alerts",
                    type="alert_list",
                    title="Recent Alerts",
                    description="Latest system alerts and notifications",
                    configuration={
                        "max_alerts": 5,
                        "alert_levels": ["error", "warning", "critical"],
                        "show_acknowledged": False
                    },
                    data_source="alert_system",
                    refresh_interval=15
                ),
                "system_health": AdminWidget(
                    name="system_health",
                    type="health_status",
                    title="System Health",
                    description="Overall system health status",
                    configuration={
                        "show_details": True,
                        "show_history": True,
                        "history_hours": 24
                    },
                    data_source="system_monitor",
                    refresh_interval=30
                ),
                "audit_log": AdminWidget(
                    name="audit_log",
                    type="table",
                    title="Audit Log",
                    description="Recent audit log entries",
                    configuration={
                        "columns": ["timestamp", "username", "action", "resource", "success"],
                        "max_rows": 20,
                        "filter_levels": ["info", "warning", "error"]
                    },
                    data_source="audit_log",
                    refresh_interval=60
                ),
                "performance_chart": AdminWidget(
                    name="performance_chart",
                    type="chart",
                    title="Performance Trends",
                    description="System performance over time",
                    configuration={
                        "chart_type": "line",
                        "metrics": ["cpu_usage", "memory_usage", "response_time"],
                        "time_range": "24h",
                        "show_legend": True
                    },
                    data_source="system_monitor",
                    refresh_interval=60
                ),
                "quick_actions": AdminWidget(
                    name="quick_actions",
                    type="action_buttons",
                    title="Quick Actions",
                    description="Common administrative actions",
                    configuration={
                        "actions": [
                            {"name": "Create User", "action": "create_user", "icon": "user-plus"},
                            {"name": "Generate Report", "action": "generate_report", "icon": "file-text"},
                            {"name": "System Backup", "action": "create_backup", "icon": "save"},
                            {"name": "View Logs", "action": "view_logs", "icon": "list"}
                        ]
                    },
                    data_source="static"
                ),
                "security_overview": AdminWidget(
                    name="security_overview",
                    type="security_status",
                    title="Security Overview",
                    description="Security status and recent events",
                    configuration={
                        "show_failed_logins": True,
                        "show_suspicious_activity": True,
                        "show_security_alerts": True
                    },
                    data_source="security_monitor",
                    refresh_interval=60
                ),
                "backup_status": AdminWidget(
                    name="backup_status",
                    type="backup_status",
                    title="Backup Status",
                    description="Recent backup operations and status",
                    configuration={
                        "show_recent_backups": True,
                        "show_backup_schedule": True,
                        "max_backups": 5
                    },
                    data_source="backup_system",
                    refresh_interval=300
                )
            }
            
            for widget_id, widget in default_widgets.items():
                self.widgets[widget_id] = widget
            
            logger.info("Loaded default widgets")
        except Exception as e:
            logger.error(f"Failed to load default widgets: {e}")
            raise
    
    async def _load_default_charts(self):
        """Load default charts."""
        try:
            default_charts = {
                "performance_chart": AdminChart(
                    name="performance_chart",
                    type="line",
                    title="System Performance",
                    data=[
                        {"timestamp": "2024-01-01T00:00:00Z", "cpu_usage": 45.2, "memory_usage": 67.8, "response_time": 120},
                        {"timestamp": "2024-01-01T01:00:00Z", "cpu_usage": 52.1, "memory_usage": 71.2, "response_time": 135},
                        {"timestamp": "2024-01-01T02:00:00Z", "cpu_usage": 38.7, "memory_usage": 65.4, "response_time": 110}
                    ],
                    options={
                        "responsive": True,
                        "scales": {
                            "y": {"beginAtZero": True, "max": 100},
                            "x": {"type": "time"}
                        }
                    },
                    x_axis="timestamp",
                    y_axis="value",
                    colors=["#3B82F6", "#EF4444", "#10B981"]
                ),
                "user_activity_chart": AdminChart(
                    name="user_activity_chart",
                    type="bar",
                    title="User Activity by Hour",
                    data=[
                        {"hour": "00:00", "logins": 5, "actions": 23},
                        {"hour": "01:00", "logins": 3, "actions": 18},
                        {"hour": "02:00", "logins": 2, "actions": 12}
                    ],
                    options={
                        "responsive": True,
                        "scales": {
                            "y": {"beginAtZero": True}
                        }
                    },
                    x_axis="hour",
                    y_axis="count",
                    colors=["#8B5CF6", "#F59E0B"]
                )
            }
            
            for chart_id, chart in default_charts.items():
                self.charts[chart_id] = chart
            
            logger.info("Loaded default charts")
        except Exception as e:
            logger.error(f"Failed to load default charts: {e}")
            raise
    
    async def _load_default_tables(self):
        """Load default tables."""
        try:
            default_tables = {
                "user_activity": AdminTable(
                    name="user_activity",
                    title="User Activity",
                    columns=[
                        {"key": "username", "title": "Username", "sortable": True},
                        {"key": "action", "title": "Action", "sortable": True},
                        {"key": "timestamp", "title": "Timestamp", "sortable": True},
                        {"key": "ip_address", "title": "IP Address", "sortable": False},
                        {"key": "success", "title": "Success", "sortable": True}
                    ],
                    data=[
                        {
                            "username": "admin",
                            "action": "login",
                            "timestamp": "2024-01-01T10:30:00Z",
                            "ip_address": "192.168.1.100",
                            "success": True
                        },
                        {
                            "username": "user1",
                            "action": "create_user",
                            "timestamp": "2024-01-01T10:25:00Z",
                            "ip_address": "192.168.1.101",
                            "success": True
                        }
                    ],
                    pagination=True,
                    page_size=25,
                    sorting={"timestamp": "desc"},
                    searchable=True,
                    exportable=True
                ),
                "audit_log": AdminTable(
                    name="audit_log",
                    title="Audit Log",
                    columns=[
                        {"key": "timestamp", "title": "Timestamp", "sortable": True},
                        {"key": "username", "title": "Username", "sortable": True},
                        {"key": "action", "title": "Action", "sortable": True},
                        {"key": "resource", "title": "Resource", "sortable": True},
                        {"key": "success", "title": "Success", "sortable": True},
                        {"key": "ip_address", "title": "IP Address", "sortable": False}
                    ],
                    data=[
                        {
                            "timestamp": "2024-01-01T10:30:00Z",
                            "username": "admin",
                            "action": "login",
                            "resource": "auth",
                            "success": True,
                            "ip_address": "192.168.1.100"
                        }
                    ],
                    pagination=True,
                    page_size=50,
                    sorting={"timestamp": "desc"},
                    searchable=True,
                    exportable=True
                )
            }
            
            for table_id, table in default_tables.items():
                self.tables[table_id] = table
            
            logger.info("Loaded default tables")
        except Exception as e:
            logger.error(f"Failed to load default tables: {e}")
            raise
    
    async def get_dashboard_data(self, user: AdminUser) -> Dict[str, Any]:
        """Get dashboard data for user."""
        try:
            # Get user's dashboard
            dashboard = await self.get_user_dashboard(user)
            
            # Get widget data
            widget_data = {}
            for widget_id in dashboard.widgets:
                if widget_id in self.widgets:
                    widget = self.widgets[widget_id]
                    data = await self._get_widget_data(widget, user)
                    widget_data[widget_id] = data
            
            return {
                "dashboard": dashboard.dict(),
                "widgets": widget_data,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role.value,
                    "permissions": [p.value for p in user.permissions]
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {e}")
            raise
    
    async def get_user_dashboard(self, user: AdminUser) -> AdminDashboard:
        """Get dashboard for user based on role."""
        try:
            # Check if user has custom dashboard
            if user.id in self.dashboards:
                return self.dashboards[user.id]
            
            # Get role-based dashboard
            role_dashboard = self.dashboards.get(user.role.value)
            if role_dashboard:
                return role_dashboard
            
            # Fall back to default dashboard
            return self.dashboards["default"]
        except Exception as e:
            logger.error(f"Failed to get user dashboard: {e}")
            raise
    
    async def _get_widget_data(self, widget: AdminWidget, user: AdminUser) -> Dict[str, Any]:
        """Get data for specific widget."""
        try:
            if widget.data_source == "static":
                return {"type": "static", "data": widget.configuration}
            
            elif widget.data_source == "system_monitor":
                return await self._get_system_metrics_data(widget)
            
            elif widget.data_source == "audit_log":
                return await self._get_audit_log_data(widget, user)
            
            elif widget.data_source == "alert_system":
                return await self._get_alert_data(widget)
            
            elif widget.data_source == "security_monitor":
                return await self._get_security_data(widget)
            
            elif widget.data_source == "backup_system":
                return await self._get_backup_data(widget)
            
            else:
                return {"type": "unknown", "data": {}}
                
        except Exception as e:
            logger.error(f"Failed to get widget data for {widget.name}: {e}")
            return {"type": "error", "data": {"error": str(e)}}
    
    async def _get_system_metrics_data(self, widget: AdminWidget) -> Dict[str, Any]:
        """Get system metrics data."""
        try:
            # Mock system metrics data
            metrics_data = {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 23.4,
                "network_io": {"in": 1024, "out": 2048},
                "active_connections": 156,
                "response_time": 120.5,
                "error_rate": 0.2,
                "throughput": 1250.7,
                "queue_size": 12,
                "cache_hit_rate": 89.3,
                "database_connections": 25
            }
            
            # Filter metrics based on widget configuration
            requested_metrics = widget.configuration.get("metrics", list(metrics_data.keys()))
            filtered_data = {k: v for k, v in metrics_data.items() if k in requested_metrics}
            
            return {
                "type": "metrics",
                "data": filtered_data,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get system metrics data: {e}")
            return {"type": "error", "data": {"error": str(e)}}
    
    async def _get_audit_log_data(self, widget: AdminWidget, user: AdminUser) -> Dict[str, Any]:
        """Get audit log data."""
        try:
            # Mock audit log data
            audit_data = [
                {
                    "timestamp": "2024-01-01T10:30:00Z",
                    "username": "admin",
                    "action": "login",
                    "resource": "auth",
                    "success": True,
                    "ip_address": "192.168.1.100"
                },
                {
                    "timestamp": "2024-01-01T10:25:00Z",
                    "username": "user1",
                    "action": "create_user",
                    "resource": "users",
                    "success": True,
                    "ip_address": "192.168.1.101"
                },
                {
                    "timestamp": "2024-01-01T10:20:00Z",
                    "username": "user2",
                    "action": "failed_login",
                    "resource": "auth",
                    "success": False,
                    "ip_address": "192.168.1.102"
                }
            ]
            
            # Filter data based on widget configuration
            max_rows = widget.configuration.get("max_rows", 10)
            filtered_data = audit_data[:max_rows]
            
            return {
                "type": "table",
                "data": filtered_data,
                "columns": widget.configuration.get("columns", []),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get audit log data: {e}")
            return {"type": "error", "data": {"error": str(e)}}
    
    async def _get_alert_data(self, widget: AdminWidget) -> Dict[str, Any]:
        """Get alert data."""
        try:
            # Mock alert data
            alert_data = [
                {
                    "id": "alert_1",
                    "title": "High CPU Usage",
                    "message": "CPU usage is above 80%",
                    "level": "warning",
                    "timestamp": "2024-01-01T10:30:00Z",
                    "acknowledged": False
                },
                {
                    "id": "alert_2",
                    "title": "Disk Space Low",
                    "message": "Disk usage is above 90%",
                    "level": "error",
                    "timestamp": "2024-01-01T10:25:00Z",
                    "acknowledged": True
                }
            ]
            
            # Filter alerts based on configuration
            max_alerts = widget.configuration.get("max_alerts", 5)
            alert_levels = widget.configuration.get("alert_levels", ["error", "warning", "critical"])
            show_acknowledged = widget.configuration.get("show_acknowledged", False)
            
            filtered_data = [
                alert for alert in alert_data
                if alert["level"] in alert_levels
                and (show_acknowledged or not alert["acknowledged"])
            ][:max_alerts]
            
            return {
                "type": "alerts",
                "data": filtered_data,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get alert data: {e}")
            return {"type": "error", "data": {"error": str(e)}}
    
    async def _get_security_data(self, widget: AdminWidget) -> Dict[str, Any]:
        """Get security data."""
        try:
            # Mock security data
            security_data = {
                "failed_logins": 3,
                "suspicious_activity": 1,
                "security_alerts": 2,
                "active_sessions": 15,
                "blocked_ips": 5,
                "last_security_scan": "2024-01-01T09:00:00Z"
            }
            
            return {
                "type": "security",
                "data": security_data,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get security data: {e}")
            return {"type": "error", "data": {"error": str(e)}}
    
    async def _get_backup_data(self, widget: AdminWidget) -> Dict[str, Any]:
        """Get backup data."""
        try:
            # Mock backup data
            backup_data = {
                "recent_backups": [
                    {
                        "id": "backup_1",
                        "type": "full",
                        "status": "completed",
                        "created_at": "2024-01-01T02:00:00Z",
                        "size": "2.5 GB"
                    },
                    {
                        "id": "backup_2",
                        "type": "incremental",
                        "status": "completed",
                        "created_at": "2024-01-01T08:00:00Z",
                        "size": "500 MB"
                    }
                ],
                "next_backup": "2024-01-01T14:00:00Z",
                "backup_schedule": "daily"
            }
            
            return {
                "type": "backup",
                "data": backup_data,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get backup data: {e}")
            return {"type": "error", "data": {"error": str(e)}}
    
    async def create_custom_dashboard(
        self,
        user: AdminUser,
        name: str,
        description: str,
        layout: Dict[str, Any],
        widgets: List[str]
    ) -> AdminDashboard:
        """Create custom dashboard for user."""
        try:
            dashboard = AdminDashboard(
                name=name,
                description=description,
                layout=layout,
                widgets=widgets,
                created_by=user.id
            )
            
            self.dashboards[user.id] = dashboard
            
            return dashboard
        except Exception as e:
            logger.error(f"Failed to create custom dashboard: {e}")
            raise
    
    async def update_dashboard(
        self,
        user: AdminUser,
        dashboard_id: str,
        updates: Dict[str, Any]
    ) -> AdminDashboard:
        """Update user dashboard."""
        try:
            if dashboard_id not in self.dashboards:
                raise ValueError("Dashboard not found")
            
            dashboard = self.dashboards[dashboard_id]
            
            # Update fields
            for field, value in updates.items():
                if hasattr(dashboard, field):
                    setattr(dashboard, field, value)
            
            dashboard.updated_at = datetime.now()
            
            return dashboard
        except Exception as e:
            logger.error(f"Failed to update dashboard: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup dashboard controller resources."""
        try:
            self.dashboards.clear()
            self.widgets.clear()
            self.charts.clear()
            self.tables.clear()
            self.is_initialized = False
            logger.info("Dashboard controller cleanup completed")
        except Exception as e:
            logger.error(f"Error during dashboard controller cleanup: {e}")
