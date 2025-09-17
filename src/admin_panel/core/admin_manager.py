"""
Admin Manager

Main orchestrator for admin panel operations.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal

from ..models.admin_models import (
    AdminUser, AdminRole, AdminPermission, SystemMetrics,
    AuditLog, AdminSession, AdminConfiguration, AdminReport,
    AdminAlert, AdminRoleType, AdminPermissionType, AdminAlertLevel
)
from .dashboard_controller import DashboardController
from .user_manager import UserManager
from .system_monitor import SystemMonitor
from .audit_logger import AuditLogger

logger = logging.getLogger(__name__)


class AdminManager:
    """
    Main admin manager that orchestrates all admin panel operations.
    """
    
    def __init__(self, db_manager=None):
        """Initialize admin manager."""
        self.db_manager = db_manager
        self.dashboard_controller = DashboardController(db_manager)
        self.user_manager = UserManager(db_manager)
        self.system_monitor = SystemMonitor(db_manager)
        self.audit_logger = AuditLogger(db_manager)
        
        # Cache for frequently accessed data
        self._user_cache = {}
        self._role_cache = {}
        self._permission_cache = {}
        self._config_cache = {}
        
        # System state
        self.is_initialized = False
        self.startup_time = None
        self.system_health = "unknown"
    
    async def initialize(self):
        """Initialize admin manager."""
        try:
            # Initialize components
            await self.dashboard_controller.initialize()
            await self.user_manager.initialize()
            await self.system_monitor.initialize()
            await self.audit_logger.initialize()
            
            # Load system configuration
            await self._load_system_configuration()
            
            # Load default roles and permissions
            await self._load_default_roles_permissions()
            
            # Start background tasks
            await self._start_background_tasks()
            
            self.is_initialized = True
            self.startup_time = datetime.now()
            self.system_health = "healthy"
            
            # Log initialization
            await self.audit_logger.log_event(
                action="system_initialized",
                resource="admin_manager",
                details={"startup_time": self.startup_time.isoformat()}
            )
            
            logger.info("Admin manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize admin manager: {e}")
            self.system_health = "error"
            raise
    
    async def _load_system_configuration(self):
        """Load system configuration."""
        try:
            # Load configuration from database or defaults
            default_configs = {
                'system_name': 'Pocket Hedge Fund Admin',
                'system_version': '1.0.0',
                'session_timeout': 28800,  # 8 hours
                'max_login_attempts': 5,
                'lockout_duration': 1800,  # 30 minutes
                'password_min_length': 8,
                'require_two_factor': False,
                'audit_retention_days': 365,
                'backup_retention_days': 30,
                'maintenance_mode': False,
                'debug_mode': False
            }
            
            for key, value in default_configs.items():
                config = AdminConfiguration(
                    key=key,
                    value=value,
                    category="system",
                    description=f"System configuration for {key}"
                )
                self._config_cache[key] = config
            
            logger.info("Loaded system configuration")
        except Exception as e:
            logger.error(f"Failed to load system configuration: {e}")
            raise
    
    async def _load_default_roles_permissions(self):
        """Load default roles and permissions."""
        try:
            # Create default permissions
            default_permissions = [
                AdminPermission(
                    name=AdminPermissionType.USER_MANAGEMENT,
                    description="Manage users and roles",
                    resource="users",
                    action="manage"
                ),
                AdminPermission(
                    name=AdminPermissionType.SYSTEM_MONITORING,
                    description="Monitor system health and performance",
                    resource="system",
                    action="monitor"
                ),
                AdminPermission(
                    name=AdminPermissionType.ANALYTICS_VIEW,
                    description="View analytics and reports",
                    resource="analytics",
                    action="read"
                ),
                AdminPermission(
                    name=AdminPermissionType.CONFIGURATION_MANAGE,
                    description="Manage system configuration",
                    resource="configuration",
                    action="manage"
                ),
                AdminPermission(
                    name=AdminPermissionType.AUDIT_LOG_VIEW,
                    description="View audit logs",
                    resource="audit",
                    action="read"
                ),
                AdminPermission(
                    name=AdminPermissionType.REPORTS_GENERATE,
                    description="Generate reports",
                    resource="reports",
                    action="create"
                ),
                AdminPermission(
                    name=AdminPermissionType.SECURITY_MANAGE,
                    description="Manage security settings",
                    resource="security",
                    action="manage"
                ),
                AdminPermission(
                    name=AdminPermissionType.BACKUP_MANAGE,
                    description="Manage backups",
                    resource="backup",
                    action="manage"
                ),
                AdminPermission(
                    name=AdminPermissionType.MAINTENANCE_EXECUTE,
                    description="Execute maintenance tasks",
                    resource="maintenance",
                    action="execute"
                )
            ]
            
            for permission in default_permissions:
                self._permission_cache[permission.name] = permission
            
            # Create default roles
            default_roles = [
                AdminRole(
                    name="super_admin",
                    description="Super Administrator with full access",
                    permissions=list(AdminPermissionType),
                    is_system_role=True
                ),
                AdminRole(
                    name="admin",
                    description="Administrator with most permissions",
                    permissions=[
                        AdminPermissionType.USER_MANAGEMENT,
                        AdminPermissionType.SYSTEM_MONITORING,
                        AdminPermissionType.ANALYTICS_VIEW,
                        AdminPermissionType.CONFIGURATION_MANAGE,
                        AdminPermissionType.AUDIT_LOG_VIEW,
                        AdminPermissionType.REPORTS_GENERATE
                    ],
                    is_system_role=True
                ),
                AdminRole(
                    name="moderator",
                    description="Moderator with limited permissions",
                    permissions=[
                        AdminPermissionType.ANALYTICS_VIEW,
                        AdminPermissionType.AUDIT_LOG_VIEW,
                        AdminPermissionType.REPORTS_GENERATE
                    ],
                    is_system_role=True
                ),
                AdminRole(
                    name="viewer",
                    description="Viewer with read-only access",
                    permissions=[
                        AdminPermissionType.ANALYTICS_VIEW,
                        AdminPermissionType.AUDIT_LOG_VIEW
                    ],
                    is_system_role=True
                ),
                AdminRole(
                    name="auditor",
                    description="Auditor with audit and compliance access",
                    permissions=[
                        AdminPermissionType.AUDIT_LOG_VIEW,
                        AdminPermissionType.REPORTS_GENERATE,
                        AdminPermissionType.SECURITY_MANAGE
                    ],
                    is_system_role=True
                )
            ]
            
            for role in default_roles:
                self._role_cache[role.name] = role
            
            logger.info("Loaded default roles and permissions")
        except Exception as e:
            logger.error(f"Failed to load default roles and permissions: {e}")
            raise
    
    async def _start_background_tasks(self):
        """Start background monitoring tasks."""
        try:
            # Start system monitoring
            asyncio.create_task(self._monitor_system_health())
            
            # Start cache cleanup
            asyncio.create_task(self._cleanup_cache())
            
            # Start audit log cleanup
            asyncio.create_task(self._cleanup_audit_logs())
            
            logger.info("Started background tasks")
        except Exception as e:
            logger.error(f"Failed to start background tasks: {e}")
            raise
    
    async def _monitor_system_health(self):
        """Monitor system health."""
        try:
            while self.is_initialized:
                try:
                    # Check system health
                    health_status = await self.system_monitor.get_system_health()
                    
                    if health_status['status'] != self.system_health:
                        self.system_health = health_status['status']
                        
                        # Log health change
                        await self.audit_logger.log_event(
                            action="system_health_changed",
                            resource="system",
                            details={
                                "old_status": health_status.get('previous_status'),
                                "new_status": self.system_health,
                                "timestamp": datetime.now().isoformat()
                            }
                        )
                    
                    # Wait before next check
                    await asyncio.sleep(60)  # Check every minute
                    
                except Exception as e:
                    logger.error(f"System health monitoring error: {e}")
                    await asyncio.sleep(60)
                    
        except Exception as e:
            logger.error(f"System health monitoring failed: {e}")
    
    async def _cleanup_cache(self):
        """Cleanup expired cache entries."""
        try:
            while self.is_initialized:
                try:
                    # Cleanup user cache
                    current_time = datetime.now()
                    expired_users = []
                    
                    for user_id, user_data in self._user_cache.items():
                        if 'expires_at' in user_data and user_data['expires_at'] < current_time:
                            expired_users.append(user_id)
                    
                    for user_id in expired_users:
                        del self._user_cache[user_id]
                    
                    # Wait before next cleanup
                    await asyncio.sleep(300)  # Cleanup every 5 minutes
                    
                except Exception as e:
                    logger.error(f"Cache cleanup error: {e}")
                    await asyncio.sleep(300)
                    
        except Exception as e:
            logger.error(f"Cache cleanup failed: {e}")
    
    async def _cleanup_audit_logs(self):
        """Cleanup old audit logs."""
        try:
            while self.is_initialized:
                try:
                    # Get retention period from config
                    retention_days = self._config_cache.get('audit_retention_days', {}).get('value', 365)
                    cutoff_date = datetime.now() - timedelta(days=retention_days)
                    
                    # Cleanup old audit logs
                    await self.audit_logger.cleanup_old_logs(cutoff_date)
                    
                    # Wait before next cleanup
                    await asyncio.sleep(86400)  # Cleanup daily
                    
                except Exception as e:
                    logger.error(f"Audit log cleanup error: {e}")
                    await asyncio.sleep(86400)
                    
        except Exception as e:
            logger.error(f"Audit log cleanup failed: {e}")
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        try:
            system_metrics = await self.system_monitor.get_current_metrics()
            health_status = await self.system_monitor.get_system_health()
            
            return {
                'status': self.system_health,
                'uptime': (datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0,
                'initialized': self.is_initialized,
                'startup_time': self.startup_time.isoformat() if self.startup_time else None,
                'metrics': system_metrics,
                'health': health_status,
                'cache_stats': {
                    'users': len(self._user_cache),
                    'roles': len(self._role_cache),
                    'permissions': len(self._permission_cache),
                    'configs': len(self._config_cache)
                }
            }
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def get_dashboard_data(self, user_id: str) -> Dict[str, Any]:
        """Get dashboard data for user."""
        try:
            # Get user permissions
            user = await self.user_manager.get_user(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Get dashboard data based on permissions
            dashboard_data = await self.dashboard_controller.get_dashboard_data(user)
            
            return dashboard_data
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {e}")
            raise
    
    async def execute_admin_action(
        self,
        user_id: str,
        action: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute admin action with proper authorization."""
        try:
            # Get user and check permissions
            user = await self.user_manager.get_user(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Check if user has permission for this action
            if not await self.user_manager.has_permission(user, action):
                raise PermissionError(f"User {user.username} does not have permission for action {action}")
            
            # Log action start
            await self.audit_logger.log_event(
                user_id=user_id,
                username=user.username,
                action=f"execute_{action}",
                resource="admin_action",
                details=parameters or {}
            )
            
            # Execute action based on type
            result = await self._execute_action(action, parameters, user)
            
            # Log action completion
            await self.audit_logger.log_event(
                user_id=user_id,
                username=user.username,
                action=f"complete_{action}",
                resource="admin_action",
                details={"result": "success", "parameters": parameters}
            )
            
            return result
            
        except Exception as e:
            # Log action failure
            await self.audit_logger.log_event(
                user_id=user_id,
                action=f"failed_{action}",
                resource="admin_action",
                details={"error": str(e), "parameters": parameters},
                success=False,
                error_message=str(e)
            )
            raise
    
    async def _execute_action(
        self,
        action: str,
        parameters: Optional[Dict[str, Any]],
        user: AdminUser
    ) -> Dict[str, Any]:
        """Execute specific admin action."""
        try:
            if action == "create_user":
                return await self.user_manager.create_user(parameters)
            elif action == "update_user":
                return await self.user_manager.update_user(parameters.get('user_id'), parameters)
            elif action == "delete_user":
                return await self.user_manager.delete_user(parameters.get('user_id'))
            elif action == "create_role":
                return await self.user_manager.create_role(parameters)
            elif action == "update_role":
                return await self.user_manager.update_role(parameters.get('role_id'), parameters)
            elif action == "delete_role":
                return await self.user_manager.delete_role(parameters.get('role_id'))
            elif action == "update_configuration":
                return await self._update_configuration(parameters)
            elif action == "generate_report":
                return await self._generate_report(parameters, user)
            elif action == "create_backup":
                return await self._create_backup(parameters, user)
            elif action == "execute_maintenance":
                return await self._execute_maintenance(parameters, user)
            else:
                raise ValueError(f"Unknown action: {action}")
                
        except Exception as e:
            logger.error(f"Failed to execute action {action}: {e}")
            raise
    
    async def _update_configuration(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Update system configuration."""
        try:
            key = parameters.get('key')
            value = parameters.get('value')
            
            if not key:
                raise ValueError("Configuration key is required")
            
            # Update configuration
            if key in self._config_cache:
                config = self._config_cache[key]
                config.value = value
                config.updated_at = datetime.now()
            else:
                config = AdminConfiguration(
                    key=key,
                    value=value,
                    category=parameters.get('category', 'general')
                )
                self._config_cache[key] = config
            
            return {"success": True, "message": f"Configuration {key} updated successfully"}
            
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            raise
    
    async def _generate_report(self, parameters: Dict[str, Any], user: AdminUser) -> Dict[str, Any]:
        """Generate admin report."""
        try:
            report_type = parameters.get('type', 'system_health')
            report_params = parameters.get('parameters', {})
            
            # Generate report based on type
            if report_type == 'system_health':
                data = await self.system_monitor.get_system_health_report()
            elif report_type == 'user_activity':
                data = await self.user_manager.get_user_activity_report(report_params)
            elif report_type == 'audit_log':
                data = await self.audit_logger.get_audit_report(report_params)
            else:
                raise ValueError(f"Unknown report type: {report_type}")
            
            return {
                "success": True,
                "report_type": report_type,
                "data": data,
                "generated_by": user.username,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            raise
    
    async def _create_backup(self, parameters: Dict[str, Any], user: AdminUser) -> Dict[str, Any]:
        """Create system backup."""
        try:
            backup_type = parameters.get('type', 'full')
            
            # This would implement actual backup creation
            # For now, return mock result
            return {
                "success": True,
                "backup_type": backup_type,
                "backup_id": f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "created_by": user.username,
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise
    
    async def _execute_maintenance(self, parameters: Dict[str, Any], user: AdminUser) -> Dict[str, Any]:
        """Execute maintenance task."""
        try:
            maintenance_type = parameters.get('type')
            
            if not maintenance_type:
                raise ValueError("Maintenance type is required")
            
            # This would implement actual maintenance execution
            # For now, return mock result
            return {
                "success": True,
                "maintenance_type": maintenance_type,
                "executed_by": user.username,
                "executed_at": datetime.now().isoformat(),
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Failed to execute maintenance: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup admin manager resources."""
        try:
            self.is_initialized = False
            
            # Cleanup components
            await self.dashboard_controller.cleanup()
            await self.user_manager.cleanup()
            await self.system_monitor.cleanup()
            await self.audit_logger.cleanup()
            
            # Clear caches
            self._user_cache.clear()
            self._role_cache.clear()
            self._permission_cache.clear()
            self._config_cache.clear()
            
            logger.info("Admin manager cleanup completed")
        except Exception as e:
            logger.error(f"Error during admin manager cleanup: {e}")
