"""
Admin Panel Module for Pocket Hedge Fund

This module provides comprehensive administrative capabilities including:
- User management and role-based access control
- System monitoring and health checks
- Analytics dashboard and reporting
- Configuration management
- Audit logging and compliance
- Performance monitoring
- Security management
- Data management and backup
"""

from .core.admin_manager import AdminManager
from .core.dashboard_controller import DashboardController
from .core.user_manager import UserManager
from .core.system_monitor import SystemMonitor
from .core.audit_logger import AuditLogger

from .models.admin_models import (
    AdminUser,
    AdminRole,
    AdminPermission,
    SystemMetrics,
    AuditLog,
    AdminSession,
    AdminConfiguration,
    AdminReport,
    AdminAlert
)

from .views.admin_views import (
    AdminDashboardView,
    UserManagementView,
    SystemMonitoringView,
    AnalyticsView,
    ConfigurationView,
    AuditLogView,
    ReportsView,
    SecurityView
)

from .components.dashboard_components import (
    DashboardWidget,
    MetricsCard,
    ChartComponent,
    TableComponent,
    AlertComponent
)

from .services.admin_services import (
    AdminAuthService,
    AdminDataService,
    AdminReportService,
    AdminConfigService,
    AdminAuditService
)

from .utils.admin_utils import (
    AdminHelpers,
    AdminValidators,
    AdminFormatters,
    AdminExporters,
    AdminImporters
)

__version__ = "1.0.0"
__author__ = "Pocket Hedge Fund Team"

__all__ = [
    # Core components
    "AdminManager",
    "DashboardController",
    "UserManager",
    "SystemMonitor",
    "AuditLogger",
    
    # Models
    "AdminUser",
    "AdminRole",
    "AdminPermission",
    "SystemMetrics",
    "AuditLog",
    "AdminSession",
    "AdminConfiguration",
    "AdminReport",
    "AdminAlert",
    
    # Views
    "AdminDashboardView",
    "UserManagementView",
    "SystemMonitoringView",
    "AnalyticsView",
    "ConfigurationView",
    "AuditLogView",
    "ReportsView",
    "SecurityView",
    
    # Components
    "DashboardWidget",
    "MetricsCard",
    "ChartComponent",
    "TableComponent",
    "AlertComponent",
    
    # Services
    "AdminAuthService",
    "AdminDataService",
    "AdminReportService",
    "AdminConfigService",
    "AdminAuditService",
    
    # Utils
    "AdminHelpers",
    "AdminValidators",
    "AdminFormatters",
    "AdminExporters",
    "AdminImporters"
]
