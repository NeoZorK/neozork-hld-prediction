"""
Admin Panel Views and Controllers

This module provides view controllers for admin panel functionality.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from fastapi import APIRouter, HTTPException, Depends, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from ..models.admin_models import (
    AdminUser, AdminRole, AdminPermission, SystemMetrics,
    AuditLog, AdminConfiguration, AdminReport, AdminAlert,
    AdminRoleType, AdminPermissionType, AdminAlertLevel
)
from ..core.admin_manager import AdminManager
from ...auth.auth_manager import get_current_user

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/admin", tags=["admin"])

# Global admin manager instance
admin_manager = None

# Templates
templates = Jinja2Templates(directory="src/admin_panel/templates")


async def get_admin_manager() -> AdminManager:
    """Get admin manager instance."""
    global admin_manager
    if admin_manager is None:
        admin_manager = AdminManager()
        await admin_manager.initialize()
    return admin_manager


class AdminBaseView:
    """Base view class for admin panel."""
    
    def __init__(self, admin_manager: AdminManager):
        self.admin_manager = admin_manager
    
    async def check_permission(self, user: AdminUser, permission: AdminPermissionType) -> bool:
        """Check if user has permission."""
        return await self.admin_manager.user_manager.has_permission(user, permission.value)
    
    async def require_permission(self, user: AdminUser, permission: AdminPermissionType):
        """Require permission or raise exception."""
        if not await self.check_permission(user, permission):
            raise HTTPException(status_code=403, detail="Insufficient permissions")


class AdminDashboardView(AdminBaseView):
    """Dashboard view controller."""
    
    async def get_dashboard(self, request: Request, user: AdminUser = Depends(get_current_user)):
        """Get admin dashboard."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.ANALYTICS_VIEW)
            
            # Get dashboard data
            dashboard_data = await self.admin_manager.get_dashboard_data(user.id)
            
            # Render dashboard template
            return templates.TemplateResponse(
                "dashboard.html",
                {
                    "request": request,
                    "user": user,
                    "dashboard_data": dashboard_data
                }
            )
        except Exception as e:
            logger.error(f"Failed to get dashboard: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_dashboard_data(self, user: AdminUser = Depends(get_current_user)):
        """Get dashboard data as JSON."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.ANALYTICS_VIEW)
            
            # Get dashboard data
            dashboard_data = await self.admin_manager.get_dashboard_data(user.id)
            
            return JSONResponse(content=dashboard_data)
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {e}")
            raise HTTPException(status_code=500, detail=str(e))


class UserManagementView(AdminBaseView):
    """User management view controller."""
    
    async def get_users(self, request: Request, user: AdminUser = Depends(get_current_user)):
        """Get users management page."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.USER_MANAGEMENT)
            
            # Get users list
            users = await self.admin_manager.user_manager.list_users()
            
            # Render users template
            return templates.TemplateResponse(
                "users.html",
                {
                    "request": request,
                    "user": user,
                    "users": users
                }
            )
        except Exception as e:
            logger.error(f"Failed to get users: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def create_user(
        self,
        request: Request,
        username: str = Form(...),
        email: str = Form(...),
        full_name: str = Form(...),
        role: str = Form(...),
        password: str = Form(...),
        current_user: AdminUser = Depends(get_current_user)
    ):
        """Create new user."""
        try:
            # Check permission
            await self.require_permission(current_user, AdminPermissionType.USER_MANAGEMENT)
            
            # Create user
            user_data = {
                'username': username,
                'email': email,
                'full_name': full_name,
                'role': role,
                'password': password,
                'created_by': current_user.id
            }
            
            new_user = await self.admin_manager.user_manager.create_user(user_data)
            
            # Log user creation
            await self.admin_manager.audit_logger.log_user_creation(
                created_by=current_user.username,
                new_username=new_user.username,
                new_user_id=new_user.id
            )
            
            return JSONResponse(content={"success": True, "user_id": new_user.id})
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def update_user(
        self,
        user_id: str,
        request: Request,
        current_user: AdminUser = Depends(get_current_user)
    ):
        """Update user."""
        try:
            # Check permission
            await self.require_permission(current_user, AdminPermissionType.USER_MANAGEMENT)
            
            # Get form data
            form_data = await request.form()
            updates = dict(form_data)
            
            # Update user
            updated_user = await self.admin_manager.user_manager.update_user(user_id, updates)
            
            # Log user update
            await self.admin_manager.audit_logger.log_user_update(
                updated_by=current_user.username,
                target_username=updated_user.username,
                target_user_id=updated_user.id,
                changes=updates
            )
            
            return JSONResponse(content={"success": True})
        except Exception as e:
            logger.error(f"Failed to update user: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def delete_user(
        self,
        user_id: str,
        current_user: AdminUser = Depends(get_current_user)
    ):
        """Delete user."""
        try:
            # Check permission
            await self.require_permission(current_user, AdminPermissionType.USER_MANAGEMENT)
            
            # Get user before deletion
            user_to_delete = await self.admin_manager.user_manager.get_user(user_id)
            if not user_to_delete:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Delete user
            await self.admin_manager.user_manager.delete_user(user_id)
            
            # Log user deletion
            await self.admin_manager.audit_logger.log_user_deletion(
                deleted_by=current_user.username,
                target_username=user_to_delete.username,
                target_user_id=user_to_delete.id
            )
            
            return JSONResponse(content={"success": True})
        except Exception as e:
            logger.error(f"Failed to delete user: {e}")
            raise HTTPException(status_code=500, detail=str(e))


class SystemMonitoringView(AdminBaseView):
    """System monitoring view controller."""
    
    async def get_monitoring(self, request: Request, user: AdminUser = Depends(get_current_user)):
        """Get system monitoring page."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.SYSTEM_MONITORING)
            
            # Get system status
            system_status = await self.admin_manager.get_system_status()
            
            # Render monitoring template
            return templates.TemplateResponse(
                "monitoring.html",
                {
                    "request": request,
                    "user": user,
                    "system_status": system_status
                }
            )
        except Exception as e:
            logger.error(f"Failed to get monitoring: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_system_health(self, user: AdminUser = Depends(get_current_user)):
        """Get system health data."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.SYSTEM_MONITORING)
            
            # Get system health
            health_data = await self.admin_manager.system_monitor.get_system_health()
            
            return JSONResponse(content=health_data)
        except Exception as e:
            logger.error(f"Failed to get system health: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_metrics_history(
        self,
        hours: int = 24,
        user: AdminUser = Depends(get_current_user)
    ):
        """Get metrics history."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.SYSTEM_MONITORING)
            
            # Get metrics history
            metrics = await self.admin_manager.system_monitor.get_metrics_history(hours=hours)
            
            return JSONResponse(content=[m.dict() for m in metrics])
        except Exception as e:
            logger.error(f"Failed to get metrics history: {e}")
            raise HTTPException(status_code=500, detail=str(e))


class AnalyticsView(AdminBaseView):
    """Analytics view controller."""
    
    async def get_analytics(self, request: Request, user: AdminUser = Depends(get_current_user)):
        """Get analytics page."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.ANALYTICS_VIEW)
            
            # Get analytics data
            analytics_data = await self._get_analytics_data()
            
            # Render analytics template
            return templates.TemplateResponse(
                "analytics.html",
                {
                    "request": request,
                    "user": user,
                    "analytics_data": analytics_data
                }
            )
        except Exception as e:
            logger.error(f"Failed to get analytics: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _get_analytics_data(self) -> Dict[str, Any]:
        """Get analytics data."""
        try:
            # Get system metrics
            system_health = await self.admin_manager.system_monitor.get_system_health()
            
            # Get user statistics
            user_stats = await self.admin_manager.user_manager.get_user_activity_report({})
            
            # Get audit statistics
            audit_stats = await self.admin_manager.audit_logger.get_audit_statistics()
            
            return {
                'system_health': system_health,
                'user_stats': user_stats,
                'audit_stats': audit_stats,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get analytics data: {e}")
            return {}


class ConfigurationView(AdminBaseView):
    """Configuration view controller."""
    
    async def get_configuration(self, request: Request, user: AdminUser = Depends(get_current_user)):
        """Get configuration page."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.CONFIGURATION_MANAGE)
            
            # Get configuration data
            config_data = await self._get_configuration_data()
            
            # Render configuration template
            return templates.TemplateResponse(
                "configuration.html",
                {
                    "request": request,
                    "user": user,
                    "config_data": config_data
                }
            )
        except Exception as e:
            logger.error(f"Failed to get configuration: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def update_configuration(
        self,
        config_key: str,
        config_value: str = Form(...),
        current_user: AdminUser = Depends(get_current_user)
    ):
        """Update configuration."""
        try:
            # Check permission
            await self.require_permission(current_user, AdminPermissionType.CONFIGURATION_MANAGE)
            
            # Get old value
            old_value = None
            if config_key in self.admin_manager._config_cache:
                old_value = self.admin_manager._config_cache[config_key].value
            
            # Update configuration
            result = await self.admin_manager.execute_admin_action(
                user_id=current_user.id,
                action="update_configuration",
                parameters={'key': config_key, 'value': config_value}
            )
            
            # Log configuration change
            await self.admin_manager.audit_logger.log_configuration_change(
                changed_by=current_user.username,
                config_key=config_key,
                old_value=old_value,
                new_value=config_value
            )
            
            return JSONResponse(content=result)
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _get_configuration_data(self) -> Dict[str, Any]:
        """Get configuration data."""
        try:
            config_data = {}
            for key, config in self.admin_manager._config_cache.items():
                config_data[key] = {
                    'value': config.value,
                    'description': config.description,
                    'category': config.category,
                    'is_sensitive': config.is_sensitive,
                    'is_readonly': config.is_readonly
                }
            return config_data
        except Exception as e:
            logger.error(f"Failed to get configuration data: {e}")
            return {}


class AuditLogView(AdminBaseView):
    """Audit log view controller."""
    
    async def get_audit_logs(self, request: Request, user: AdminUser = Depends(get_current_user)):
        """Get audit logs page."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.AUDIT_LOG_VIEW)
            
            # Get audit logs
            audit_logs = await self.admin_manager.audit_logger.get_audit_logs(limit=100)
            
            # Render audit logs template
            return templates.TemplateResponse(
                "audit_logs.html",
                {
                    "request": request,
                    "user": user,
                    "audit_logs": audit_logs
                }
            )
        except Exception as e:
            logger.error(f"Failed to get audit logs: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def export_audit_logs(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        format: str = "json",
        user: AdminUser = Depends(get_current_user)
    ):
        """Export audit logs."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.AUDIT_LOG_VIEW)
            
            # Parse dates
            start_dt = datetime.fromisoformat(start_date) if start_date else None
            end_dt = datetime.fromisoformat(end_date) if end_date else None
            
            # Export logs
            export_data = await self.admin_manager.audit_logger.export_audit_logs(
                start_date=start_dt,
                end_date=end_dt,
                format=format
            )
            
            # Return file response
            filename = f"audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            
            if format == "json":
                return JSONResponse(content=export_data)
            else:
                # For CSV, you would need to convert to CSV format
                return JSONResponse(content=export_data)
        except Exception as e:
            logger.error(f"Failed to export audit logs: {e}")
            raise HTTPException(status_code=500, detail=str(e))


class ReportsView(AdminBaseView):
    """Reports view controller."""
    
    async def get_reports(self, request: Request, user: AdminUser = Depends(get_current_user)):
        """Get reports page."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.REPORTS_GENERATE)
            
            # Get available reports
            available_reports = await self._get_available_reports()
            
            # Render reports template
            return templates.TemplateResponse(
                "reports.html",
                {
                    "request": request,
                    "user": user,
                    "available_reports": available_reports
                }
            )
        except Exception as e:
            logger.error(f"Failed to get reports: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def generate_report(
        self,
        report_type: str = Form(...),
        parameters: str = Form("{}"),
        current_user: AdminUser = Depends(get_current_user)
    ):
        """Generate report."""
        try:
            # Check permission
            await self.require_permission(current_user, AdminPermissionType.REPORTS_GENERATE)
            
            # Parse parameters
            import json
            report_params = json.loads(parameters)
            
            # Generate report
            result = await self.admin_manager.execute_admin_action(
                user_id=current_user.id,
                action="generate_report",
                parameters={'type': report_type, 'parameters': report_params}
            )
            
            return JSONResponse(content=result)
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _get_available_reports(self) -> List[Dict[str, Any]]:
        """Get available reports."""
        try:
            return [
                {
                    'type': 'system_health',
                    'name': 'System Health Report',
                    'description': 'Comprehensive system health and performance report'
                },
                {
                    'type': 'user_activity',
                    'name': 'User Activity Report',
                    'description': 'User login and activity statistics'
                },
                {
                    'type': 'audit_log',
                    'name': 'Audit Log Report',
                    'description': 'Security and compliance audit report'
                }
            ]
        except Exception as e:
            logger.error(f"Failed to get available reports: {e}")
            return []


class SecurityView(AdminBaseView):
    """Security view controller."""
    
    async def get_security(self, request: Request, user: AdminUser = Depends(get_current_user)):
        """Get security page."""
        try:
            # Check permission
            await self.require_permission(user, AdminPermissionType.SECURITY_MANAGE)
            
            # Get security data
            security_data = await self._get_security_data()
            
            # Render security template
            return templates.TemplateResponse(
                "security.html",
                {
                    "request": request,
                    "user": user,
                    "security_data": security_data
                }
            )
        except Exception as e:
            logger.error(f"Failed to get security: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _get_security_data(self) -> Dict[str, Any]:
        """Get security data."""
        try:
            # Get security events
            security_events = await self.admin_manager.audit_logger.get_audit_logs(
                resource="security",
                limit=50
            )
            
            # Get failed login attempts
            failed_logins = await self.admin_manager.audit_logger.get_audit_logs(
                action="login",
                success=False,
                limit=20
            )
            
            # Get active sessions
            active_sessions = [
                session for session in self.admin_manager.user_manager.sessions.values()
                if session.status.value == "active"
            ]
            
            return {
                'security_events': security_events,
                'failed_logins': failed_logins,
                'active_sessions': active_sessions,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get security data: {e}")
            return {}


class AdminAPIView:
    """Admin API view controller."""
    
    def __init__(self, admin_manager: AdminManager):
        self.admin_manager = admin_manager
    
    async def get_system_status(self, user: AdminUser = Depends(get_current_user)):
        """Get system status API."""
        try:
            system_status = await self.admin_manager.get_system_status()
            return JSONResponse(content=system_status)
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def execute_action(
        self,
        action: str,
        parameters: Dict[str, Any],
        user: AdminUser = Depends(get_current_user)
    ):
        """Execute admin action API."""
        try:
            result = await self.admin_manager.execute_admin_action(
                user_id=user.id,
                action=action,
                parameters=parameters
            )
            return JSONResponse(content=result)
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            raise HTTPException(status_code=500, detail=str(e))
