"""
Audit Logger

Logs admin activities and system events for compliance and security.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal

from ..models.admin_models import AuditLog, AdminAlertLevel

logger = logging.getLogger(__name__)


class AuditLogger:
    """
    Logs admin activities and system events for compliance and security.
    """
    
    def __init__(self, db_manager=None):
        """Initialize audit logger."""
        self.db_manager = db_manager
        self.audit_logs = []
        self.is_logging = True
        self.retention_days = 365
        self.max_logs = 100000
        self.log_levels = {
            'info': AdminAlertLevel.INFO,
            'warning': AdminAlertLevel.WARNING,
            'error': AdminAlertLevel.ERROR,
            'critical': AdminAlertLevel.CRITICAL
        }
    
    async def initialize(self):
        """Initialize audit logger."""
        try:
            # Load existing audit logs from database
            await self._load_audit_logs()
            
            # Start cleanup task
            asyncio.create_task(self._cleanup_task())
            
            logger.info("Audit logger initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize audit logger: {e}")
            raise
    
    async def _load_audit_logs(self):
        """Load existing audit logs from database."""
        try:
            # This would load from database
            # For now, use empty list
            self.audit_logs = []
            logger.info("Loaded audit logs from database")
        except Exception as e:
            logger.error(f"Failed to load audit logs: {e}")
            raise
    
    async def _cleanup_task(self):
        """Background task to cleanup old audit logs."""
        try:
            while True:
                try:
                    # Wait 24 hours before cleanup
                    await asyncio.sleep(86400)
                    
                    # Cleanup old logs
                    cutoff_date = datetime.now() - timedelta(days=self.retention_days)
                    await self.cleanup_old_logs(cutoff_date)
                    
                except Exception as e:
                    logger.error(f"Audit log cleanup task error: {e}")
                    await asyncio.sleep(3600)  # Wait 1 hour on error
                    
        except Exception as e:
            logger.error(f"Audit log cleanup task failed: {e}")
    
    async def log_event(
        self,
        action: str,
        resource: str,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        severity: AdminAlertLevel = AdminAlertLevel.INFO
    ) -> str:
        """
        Log an audit event.
        
        Args:
            action: Action performed
            resource: Resource affected
            user_id: User ID (optional)
            username: Username (optional)
            resource_id: Resource ID (optional)
            details: Additional details (optional)
            ip_address: IP address (optional)
            user_agent: User agent (optional)
            session_id: Session ID (optional)
            success: Whether action was successful
            error_message: Error message if failed
            severity: Log severity level
            
        Returns:
            Log entry ID
        """
        try:
            # Create audit log entry
            log_entry = AuditLog(
                user_id=user_id,
                username=username,
                action=action,
                resource=resource,
                resource_id=resource_id,
                details=details,
                ip_address=ip_address,
                user_agent=user_agent,
                session_id=session_id,
                success=success,
                error_message=error_message,
                severity=severity
            )
            
            # Add to logs
            self.audit_logs.append(log_entry)
            
            # Keep only max_logs entries
            if len(self.audit_logs) > self.max_logs:
                self.audit_logs = self.audit_logs[-self.max_logs:]
            
            # Log to system logger
            log_message = f"Audit: {action} on {resource}"
            if username:
                log_message = f"User {username}: {log_message}"
            if not success:
                log_message = f"FAILED - {log_message}"
            
            if severity == AdminAlertLevel.CRITICAL:
                logger.critical(log_message)
            elif severity == AdminAlertLevel.ERROR:
                logger.error(log_message)
            elif severity == AdminAlertLevel.WARNING:
                logger.warning(log_message)
            else:
                logger.info(log_message)
            
            return log_entry.id
            
        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")
            raise
    
    async def log_user_login(
        self,
        username: str,
        success: bool,
        ip_address: str = None,
        user_agent: str = None,
        session_id: str = None,
        error_message: str = None
    ) -> str:
        """Log user login event."""
        try:
            severity = AdminAlertLevel.ERROR if not success else AdminAlertLevel.INFO
            
            return await self.log_event(
                action="login",
                resource="auth",
                username=username,
                ip_address=ip_address,
                user_agent=user_agent,
                session_id=session_id,
                success=success,
                error_message=error_message,
                severity=severity
            )
        except Exception as e:
            logger.error(f"Failed to log user login: {e}")
            raise
    
    async def log_user_logout(
        self,
        username: str,
        session_id: str = None,
        ip_address: str = None
    ) -> str:
        """Log user logout event."""
        try:
            return await self.log_event(
                action="logout",
                resource="auth",
                username=username,
                session_id=session_id,
                ip_address=ip_address,
                success=True,
                severity=AdminAlertLevel.INFO
            )
        except Exception as e:
            logger.error(f"Failed to log user logout: {e}")
            raise
    
    async def log_user_creation(
        self,
        created_by: str,
        new_username: str,
        new_user_id: str,
        ip_address: str = None
    ) -> str:
        """Log user creation event."""
        try:
            return await self.log_event(
                action="create_user",
                resource="users",
                user_id=created_by,
                username=created_by,
                resource_id=new_user_id,
                details={"new_username": new_username, "new_user_id": new_user_id},
                ip_address=ip_address,
                success=True,
                severity=AdminAlertLevel.INFO
            )
        except Exception as e:
            logger.error(f"Failed to log user creation: {e}")
            raise
    
    async def log_user_update(
        self,
        updated_by: str,
        target_username: str,
        target_user_id: str,
        changes: Dict[str, Any],
        ip_address: str = None
    ) -> str:
        """Log user update event."""
        try:
            return await self.log_event(
                action="update_user",
                resource="users",
                user_id=updated_by,
                username=updated_by,
                resource_id=target_user_id,
                details={
                    "target_username": target_username,
                    "target_user_id": target_user_id,
                    "changes": changes
                },
                ip_address=ip_address,
                success=True,
                severity=AdminAlertLevel.INFO
            )
        except Exception as e:
            logger.error(f"Failed to log user update: {e}")
            raise
    
    async def log_user_deletion(
        self,
        deleted_by: str,
        target_username: str,
        target_user_id: str,
        ip_address: str = None
    ) -> str:
        """Log user deletion event."""
        try:
            return await self.log_event(
                action="delete_user",
                resource="users",
                user_id=deleted_by,
                username=deleted_by,
                resource_id=target_user_id,
                details={"target_username": target_username, "target_user_id": target_user_id},
                ip_address=ip_address,
                success=True,
                severity=AdminAlertLevel.WARNING
            )
        except Exception as e:
            logger.error(f"Failed to log user deletion: {e}")
            raise
    
    async def log_permission_change(
        self,
        changed_by: str,
        target_username: str,
        target_user_id: str,
        old_permissions: List[str],
        new_permissions: List[str],
        ip_address: str = None
    ) -> str:
        """Log permission change event."""
        try:
            return await self.log_event(
                action="change_permissions",
                resource="users",
                user_id=changed_by,
                username=changed_by,
                resource_id=target_user_id,
                details={
                    "target_username": target_username,
                    "target_user_id": target_user_id,
                    "old_permissions": old_permissions,
                    "new_permissions": new_permissions
                },
                ip_address=ip_address,
                success=True,
                severity=AdminAlertLevel.WARNING
            )
        except Exception as e:
            logger.error(f"Failed to log permission change: {e}")
            raise
    
    async def log_configuration_change(
        self,
        changed_by: str,
        config_key: str,
        old_value: Any,
        new_value: Any,
        ip_address: str = None
    ) -> str:
        """Log configuration change event."""
        try:
            return await self.log_event(
                action="change_configuration",
                resource="configuration",
                user_id=changed_by,
                username=changed_by,
                resource_id=config_key,
                details={
                    "config_key": config_key,
                    "old_value": str(old_value),
                    "new_value": str(new_value)
                },
                ip_address=ip_address,
                success=True,
                severity=AdminAlertLevel.INFO
            )
        except Exception as e:
            logger.error(f"Failed to log configuration change: {e}")
            raise
    
    async def log_security_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        severity: AdminAlertLevel = AdminAlertLevel.WARNING,
        ip_address: str = None
    ) -> str:
        """Log security-related event."""
        try:
            return await self.log_event(
                action=event_type,
                resource="security",
                details=details,
                ip_address=ip_address,
                success=False,  # Security events are typically failures
                severity=severity
            )
        except Exception as e:
            logger.error(f"Failed to log security event: {e}")
            raise
    
    async def log_system_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        severity: AdminAlertLevel = AdminAlertLevel.INFO
    ) -> str:
        """Log system event."""
        try:
            return await self.log_event(
                action=event_type,
                resource="system",
                details=details,
                success=True,
                severity=severity
            )
        except Exception as e:
            logger.error(f"Failed to log system event: {e}")
            raise
    
    async def get_audit_logs(
        self,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        action: Optional[str] = None,
        resource: Optional[str] = None,
        success: Optional[bool] = None,
        severity: Optional[AdminAlertLevel] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AuditLog]:
        """Get audit logs with optional filtering."""
        try:
            logs = self.audit_logs.copy()
            
            # Apply filters
            if user_id:
                logs = [log for log in logs if log.user_id == user_id]
            
            if username:
                logs = [log for log in logs if log.username == username]
            
            if action:
                logs = [log for log in logs if action.lower() in log.action.lower()]
            
            if resource:
                logs = [log for log in logs if log.resource == resource]
            
            if success is not None:
                logs = [log for log in logs if log.success == success]
            
            if severity:
                logs = [log for log in logs if log.severity == severity]
            
            if start_date:
                logs = [log for log in logs if log.timestamp >= start_date]
            
            if end_date:
                logs = [log for log in logs if log.timestamp <= end_date]
            
            # Sort by timestamp (newest first)
            logs.sort(key=lambda x: x.timestamp, reverse=True)
            
            # Apply pagination
            logs = logs[offset:offset + limit]
            
            return logs
            
        except Exception as e:
            logger.error(f"Failed to get audit logs: {e}")
            return []
    
    async def get_audit_report(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get audit report."""
        try:
            start_date = parameters.get('start_date', datetime.now() - timedelta(days=30))
            end_date = parameters.get('end_date', datetime.now())
            
            # Get logs for the period
            logs = await self.get_audit_logs(
                start_date=start_date,
                end_date=end_date,
                limit=10000  # Large limit for report
            )
            
            # Generate statistics
            total_events = len(logs)
            successful_events = len([log for log in logs if log.success])
            failed_events = total_events - successful_events
            
            # Events by severity
            events_by_severity = {}
            for log in logs:
                severity = log.severity.value
                events_by_severity[severity] = events_by_severity.get(severity, 0) + 1
            
            # Events by action
            events_by_action = {}
            for log in logs:
                action = log.action
                events_by_action[action] = events_by_action.get(action, 0) + 1
            
            # Events by resource
            events_by_resource = {}
            for log in logs:
                resource = log.resource
                events_by_resource[resource] = events_by_resource.get(resource, 0) + 1
            
            # Events by user
            events_by_user = {}
            for log in logs:
                if log.username:
                    events_by_user[log.username] = events_by_user.get(log.username, 0) + 1
            
            # Recent failed events
            recent_failures = [
                log for log in logs
                if not log.success and log.timestamp >= datetime.now() - timedelta(hours=24)
            ][:10]
            
            # Security events
            security_events = [
                log for log in logs
                if log.resource == "security" or log.severity in [AdminAlertLevel.ERROR, AdminAlertLevel.CRITICAL]
            ][:20]
            
            return {
                'report_generated_at': datetime.now().isoformat(),
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                'summary': {
                    'total_events': total_events,
                    'successful_events': successful_events,
                    'failed_events': failed_events,
                    'success_rate': (successful_events / total_events * 100) if total_events > 0 else 0
                },
                'events_by_severity': events_by_severity,
                'events_by_action': events_by_action,
                'events_by_resource': events_by_resource,
                'events_by_user': events_by_user,
                'recent_failures': [
                    {
                        'timestamp': log.timestamp.isoformat(),
                        'username': log.username,
                        'action': log.action,
                        'resource': log.resource,
                        'error_message': log.error_message
                    }
                    for log in recent_failures
                ],
                'security_events': [
                    {
                        'timestamp': log.timestamp.isoformat(),
                        'username': log.username,
                        'action': log.action,
                        'resource': log.resource,
                        'severity': log.severity.value,
                        'details': log.details
                    }
                    for log in security_events
                ]
            }
        except Exception as e:
            logger.error(f"Failed to get audit report: {e}")
            raise
    
    async def cleanup_old_logs(self, cutoff_date: datetime):
        """Cleanup old audit logs."""
        try:
            initial_count = len(self.audit_logs)
            
            # Remove logs older than cutoff date
            self.audit_logs = [
                log for log in self.audit_logs
                if log.timestamp >= cutoff_date
            ]
            
            removed_count = initial_count - len(self.audit_logs)
            
            if removed_count > 0:
                logger.info(f"Cleaned up {removed_count} old audit logs")
                
                # Log the cleanup event
                await self.log_system_event(
                    event_type="cleanup_audit_logs",
                    details={
                        "removed_count": removed_count,
                        "cutoff_date": cutoff_date.isoformat(),
                        "remaining_count": len(self.audit_logs)
                    }
                )
            
        except Exception as e:
            logger.error(f"Failed to cleanup old logs: {e}")
    
    async def export_audit_logs(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        format: str = "json"
    ) -> Dict[str, Any]:
        """Export audit logs."""
        try:
            # Get logs for the period
            logs = await self.get_audit_logs(
                start_date=start_date,
                end_date=end_date,
                limit=50000  # Large limit for export
            )
            
            # Convert logs to export format
            if format == "json":
                export_data = [log.dict() for log in logs]
            elif format == "csv":
                # Convert to CSV format
                export_data = []
                for log in logs:
                    export_data.append({
                        'timestamp': log.timestamp.isoformat(),
                        'user_id': log.user_id,
                        'username': log.username,
                        'action': log.action,
                        'resource': log.resource,
                        'resource_id': log.resource_id,
                        'success': log.success,
                        'severity': log.severity.value,
                        'ip_address': log.ip_address,
                        'error_message': log.error_message
                    })
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            return {
                'export_generated_at': datetime.now().isoformat(),
                'format': format,
                'record_count': len(export_data),
                'period': {
                    'start_date': start_date.isoformat() if start_date else None,
                    'end_date': end_date.isoformat() if end_date else None
                },
                'data': export_data
            }
            
        except Exception as e:
            logger.error(f"Failed to export audit logs: {e}")
            raise
    
    async def get_audit_statistics(self) -> Dict[str, Any]:
        """Get audit log statistics."""
        try:
            total_logs = len(self.audit_logs)
            
            if total_logs == 0:
                return {
                    'total_logs': 0,
                    'logs_today': 0,
                    'logs_this_week': 0,
                    'logs_this_month': 0,
                    'success_rate': 0,
                    'top_actions': [],
                    'top_users': [],
                    'top_resources': []
                }
            
            # Calculate time-based statistics
            now = datetime.now()
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
            week_ago = now - timedelta(days=7)
            month_ago = now - timedelta(days=30)
            
            logs_today = len([log for log in self.audit_logs if log.timestamp >= today])
            logs_this_week = len([log for log in self.audit_logs if log.timestamp >= week_ago])
            logs_this_month = len([log for log in self.audit_logs if log.timestamp >= month_ago])
            
            # Calculate success rate
            successful_logs = len([log for log in self.audit_logs if log.success])
            success_rate = (successful_logs / total_logs * 100) if total_logs > 0 else 0
            
            # Top actions
            action_counts = {}
            for log in self.audit_logs:
                action_counts[log.action] = action_counts.get(log.action, 0) + 1
            top_actions = sorted(action_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Top users
            user_counts = {}
            for log in self.audit_logs:
                if log.username:
                    user_counts[log.username] = user_counts.get(log.username, 0) + 1
            top_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Top resources
            resource_counts = {}
            for log in self.audit_logs:
                resource_counts[log.resource] = resource_counts.get(log.resource, 0) + 1
            top_resources = sorted(resource_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                'total_logs': total_logs,
                'logs_today': logs_today,
                'logs_this_week': logs_this_week,
                'logs_this_month': logs_this_month,
                'success_rate': success_rate,
                'top_actions': [{'action': action, 'count': count} for action, count in top_actions],
                'top_users': [{'username': username, 'count': count} for username, count in top_users],
                'top_resources': [{'resource': resource, 'count': count} for resource, count in top_resources]
            }
            
        except Exception as e:
            logger.error(f"Failed to get audit statistics: {e}")
            return {}
    
    async def cleanup(self):
        """Cleanup audit logger resources."""
        try:
            self.audit_logs.clear()
            self.is_logging = False
            logger.info("Audit logger cleanup completed")
        except Exception as e:
            logger.error(f"Error during audit logger cleanup: {e}")
