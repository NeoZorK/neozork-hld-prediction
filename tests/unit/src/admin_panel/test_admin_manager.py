"""
Unit tests for Admin Manager
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from src.admin_panel.core.admin_manager import AdminManager
from src.admin_panel.models.admin_models import (
    AdminUser, AdminRoleType, AdminPermissionType, AdminAlertLevel
)


@pytest.fixture
def admin_manager():
    """Create admin manager instance for testing."""
    manager = AdminManager()
    
    # Mock the dependencies
    manager.dashboard_controller = AsyncMock()
    manager.user_manager = AsyncMock()
    manager.system_monitor = AsyncMock()
    manager.audit_logger = AsyncMock()
    
    # Initialize synchronously for testing
    manager.is_initialized = True
    manager.startup_time = datetime.now()
    manager.system_health = "healthy"
    manager._user_cache = {}
    manager._role_cache = {}
    manager._permission_cache = {}
    manager._config_cache = {}
    
    return manager


@pytest.fixture
def sample_admin_user():
    """Create sample admin user for testing."""
    return AdminUser(
        username="test_admin",
        email="admin@test.com",
        full_name="Test Administrator",
        role=AdminRoleType.ADMIN,
        permissions=[AdminPermissionType.USER_MANAGEMENT, AdminPermissionType.SYSTEM_MONITORING]
    )


@pytest.mark.asyncio
async def test_admin_manager_initialization(admin_manager):
    """Test admin manager initialization."""
    assert admin_manager is not None
    assert admin_manager.is_initialized is True
    assert admin_manager.startup_time is not None
    assert admin_manager.system_health == "healthy"
    assert admin_manager.dashboard_controller is not None
    assert admin_manager.user_manager is not None
    assert admin_manager.system_monitor is not None
    assert admin_manager.audit_logger is not None


@pytest.mark.asyncio
async def test_get_system_status(admin_manager):
    """Test getting system status."""
    # Mock system monitor responses
    admin_manager.system_monitor.get_current_metrics.return_value = MagicMock()
    admin_manager.system_monitor.get_system_health.return_value = {
        'status': 'healthy',
        'metrics': {'cpu_usage': 45.2, 'memory_usage': 67.8}
    }
    
    status = await admin_manager.get_system_status()
    
    assert 'status' in status
    assert 'uptime' in status
    assert 'initialized' in status
    assert 'startup_time' in status
    assert 'metrics' in status
    assert 'health' in status
    assert 'cache_stats' in status
    assert status['status'] == 'healthy'
    assert status['initialized'] is True


@pytest.mark.asyncio
async def test_get_dashboard_data(admin_manager, sample_admin_user):
    """Test getting dashboard data for user."""
    # Mock user manager
    admin_manager.user_manager.get_user.return_value = sample_admin_user
    
    # Mock dashboard controller
    mock_dashboard_data = {
        'dashboard': {'name': 'default'},
        'widgets': {'system_metrics': {'type': 'metrics'}},
        'user': {'username': 'test_admin'}
    }
    admin_manager.dashboard_controller.get_dashboard_data.return_value = mock_dashboard_data
    
    dashboard_data = await admin_manager.get_dashboard_data(sample_admin_user.id)
    
    assert 'dashboard' in dashboard_data
    assert 'widgets' in dashboard_data
    assert 'user' in dashboard_data
    assert dashboard_data['user']['username'] == 'test_admin'
    
    # Verify user manager was called
    admin_manager.user_manager.get_user.assert_called_once_with(sample_admin_user.id)
    admin_manager.dashboard_controller.get_dashboard_data.assert_called_once()


@pytest.mark.asyncio
async def test_execute_admin_action_success(admin_manager, sample_admin_user):
    """Test successful admin action execution."""
    # Mock user manager
    admin_manager.user_manager.get_user.return_value = sample_admin_user
    admin_manager.user_manager.has_permission.return_value = True
    
    # Mock action execution
    admin_manager.user_manager.create_user.return_value = MagicMock()
    
    result = await admin_manager.execute_admin_action(
        user_id=sample_admin_user.id,
        action="create_user",
        parameters={'username': 'new_user', 'email': 'new@test.com'}
    )
    
    assert result is not None
    
    # Verify audit logging was called
    assert admin_manager.audit_logger.log_event.call_count >= 2  # Start and complete


@pytest.mark.asyncio
async def test_execute_admin_action_insufficient_permissions(admin_manager, sample_admin_user):
    """Test admin action with insufficient permissions."""
    # Mock user manager
    admin_manager.user_manager.get_user.return_value = sample_admin_user
    admin_manager.user_manager.has_permission.return_value = False
    
    with pytest.raises(PermissionError):
        await admin_manager.execute_admin_action(
            user_id=sample_admin_user.id,
            action="create_user",
            parameters={'username': 'new_user'}
        )


@pytest.mark.asyncio
async def test_execute_admin_action_user_not_found(admin_manager):
    """Test admin action with non-existent user."""
    # Mock user manager to return None
    admin_manager.user_manager.get_user.return_value = None
    
    with pytest.raises(ValueError, match="User not found"):
        await admin_manager.execute_admin_action(
            user_id="non_existent_user",
            action="create_user",
            parameters={}
        )


@pytest.mark.asyncio
async def test_execute_admin_action_unknown_action(admin_manager, sample_admin_user):
    """Test admin action with unknown action type."""
    # Mock user manager
    admin_manager.user_manager.get_user.return_value = sample_admin_user
    admin_manager.user_manager.has_permission.return_value = True
    
    with pytest.raises(ValueError, match="Unknown action"):
        await admin_manager.execute_admin_action(
            user_id=sample_admin_user.id,
            action="unknown_action",
            parameters={}
        )


@pytest.mark.asyncio
async def test_create_user_action(admin_manager, sample_admin_user):
    """Test create user action."""
    # Mock user manager
    admin_manager.user_manager.get_user.return_value = sample_admin_user
    admin_manager.user_manager.has_permission.return_value = True
    
    # Mock user creation
    new_user = MagicMock()
    new_user.id = "new_user_id"
    admin_manager.user_manager.create_user.return_value = new_user
    
    result = await admin_manager.execute_admin_action(
        user_id=sample_admin_user.id,
        action="create_user",
        parameters={'username': 'new_user', 'email': 'new@test.com'}
    )
    
    assert result is not None
    admin_manager.user_manager.create_user.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_action(admin_manager, sample_admin_user):
    """Test update user action."""
    # Mock user manager
    admin_manager.user_manager.get_user.return_value = sample_admin_user
    admin_manager.user_manager.has_permission.return_value = True
    
    # Mock user update
    updated_user = MagicMock()
    admin_manager.user_manager.update_user.return_value = updated_user
    
    result = await admin_manager.execute_admin_action(
        user_id=sample_admin_user.id,
        action="update_user",
        parameters={'user_id': 'target_user', 'username': 'updated_user'}
    )
    
    assert result is not None
    admin_manager.user_manager.update_user.assert_called_once()


@pytest.mark.asyncio
async def test_delete_user_action(admin_manager, sample_admin_user):
    """Test delete user action."""
    # Mock user manager
    admin_manager.user_manager.get_user.return_value = sample_admin_user
    admin_manager.user_manager.has_permission.return_value = True
    
    # Mock user deletion
    admin_manager.user_manager.delete_user.return_value = True
    
    result = await admin_manager.execute_admin_action(
        user_id=sample_admin_user.id,
        action="delete_user",
        parameters={'user_id': 'target_user'}
    )
    
    assert result is not None
    admin_manager.user_manager.delete_user.assert_called_once()


@pytest.mark.asyncio
async def test_update_configuration_action(admin_manager, sample_admin_user):
    """Test update configuration action."""
    # Mock user manager
    admin_manager.user_manager.get_user.return_value = sample_admin_user
    admin_manager.user_manager.has_permission.return_value = True
    
    result = await admin_manager.execute_admin_action(
        user_id=sample_admin_user.id,
        action="update_configuration",
        parameters={'key': 'test_config', 'value': 'test_value'}
    )
    
    assert result is not None
    assert result['success'] is True
    assert 'test_config' in admin_manager._config_cache


@pytest.mark.asyncio
async def test_generate_report_action(admin_manager, sample_admin_user):
    """Test generate report action."""
    # Mock user manager
    admin_manager.user_manager.get_user.return_value = sample_admin_user
    admin_manager.user_manager.has_permission.return_value = True
    
    # Mock system monitor
    admin_manager.system_monitor.get_system_health_report.return_value = {
        'status': 'healthy',
        'metrics': {'cpu_usage': 45.2}
    }
    
    result = await admin_manager.execute_admin_action(
        user_id=sample_admin_user.id,
        action="generate_report",
        parameters={'type': 'system_health'}
    )
    
    assert result is not None
    assert result['success'] is True
    assert result['report_type'] == 'system_health'
    assert 'data' in result


@pytest.mark.asyncio
async def test_create_backup_action(admin_manager, sample_admin_user):
    """Test create backup action."""
    # Mock user manager
    admin_manager.user_manager.get_user.return_value = sample_admin_user
    admin_manager.user_manager.has_permission.return_value = True
    
    result = await admin_manager.execute_admin_action(
        user_id=sample_admin_user.id,
        action="create_backup",
        parameters={'type': 'full'}
    )
    
    assert result is not None
    assert result['success'] is True
    assert result['backup_type'] == 'full'
    assert 'backup_id' in result


@pytest.mark.asyncio
async def test_execute_maintenance_action(admin_manager, sample_admin_user):
    """Test execute maintenance action."""
    # Mock user manager
    admin_manager.user_manager.get_user.return_value = sample_admin_user
    admin_manager.user_manager.has_permission.return_value = True
    
    result = await admin_manager.execute_admin_action(
        user_id=sample_admin_user.id,
        action="execute_maintenance",
        parameters={'type': 'database_optimization'}
    )
    
    assert result is not None
    assert result['success'] is True
    assert result['maintenance_type'] == 'database_optimization'
    assert result['status'] == 'completed'


@pytest.mark.asyncio
async def test_system_health_monitoring(admin_manager):
    """Test system health monitoring."""
    # Mock system monitor
    admin_manager.system_monitor.get_system_health.return_value = {
        'status': 'warning',
        'previous_status': 'healthy'
    }
    
    # Start monitoring (this would normally be done in background)
    await admin_manager._monitor_system_health()
    
    # Verify system health was checked
    admin_manager.system_monitor.get_system_health.assert_called()


@pytest.mark.asyncio
async def test_cache_cleanup(admin_manager):
    """Test cache cleanup."""
    # Add some cache entries
    admin_manager._user_cache['user1'] = {
        'data': 'test',
        'expires_at': datetime.now() - timedelta(hours=1)  # Expired
    }
    admin_manager._user_cache['user2'] = {
        'data': 'test',
        'expires_at': datetime.now() + timedelta(hours=1)  # Not expired
    }
    
    # Run cleanup
    await admin_manager._cleanup_cache()
    
    # Verify expired entry was removed
    assert 'user1' not in admin_manager._user_cache
    assert 'user2' in admin_manager._user_cache


@pytest.mark.asyncio
async def test_audit_log_cleanup(admin_manager):
    """Test audit log cleanup."""
    # Mock audit logger
    admin_manager.audit_logger.cleanup_old_logs = AsyncMock()
    
    # Run cleanup
    await admin_manager._cleanup_audit_logs()
    
    # Verify cleanup was called
    admin_manager.audit_logger.cleanup_old_logs.assert_called()


@pytest.mark.asyncio
async def test_cleanup(admin_manager):
    """Test admin manager cleanup."""
    # Mock cleanup methods
    admin_manager.dashboard_controller.cleanup = AsyncMock()
    admin_manager.user_manager.cleanup = AsyncMock()
    admin_manager.system_monitor.cleanup = AsyncMock()
    admin_manager.audit_logger.cleanup = AsyncMock()
    
    # Cleanup
    await admin_manager.cleanup()
    
    # Verify all cleanup methods were called
    admin_manager.dashboard_controller.cleanup.assert_called_once()
    admin_manager.user_manager.cleanup.assert_called_once()
    admin_manager.system_monitor.cleanup.assert_called_once()
    admin_manager.audit_logger.cleanup.assert_called_once()
    
    # Verify caches were cleared
    assert len(admin_manager._user_cache) == 0
    assert len(admin_manager._role_cache) == 0
    assert len(admin_manager._permission_cache) == 0
    assert len(admin_manager._config_cache) == 0


@pytest.mark.asyncio
async def test_load_system_configuration(admin_manager):
    """Test loading system configuration."""
    # Verify default configurations were loaded
    assert 'system_name' in admin_manager._config_cache
    assert 'system_version' in admin_manager._config_cache
    assert 'session_timeout' in admin_manager._config_cache
    assert 'max_login_attempts' in admin_manager._config_cache
    
    # Verify configuration values
    assert admin_manager._config_cache['system_name'].value == 'Pocket Hedge Fund Admin'
    assert admin_manager._config_cache['system_version'].value == '1.0.0'
    assert admin_manager._config_cache['session_timeout'].value == 28800


@pytest.mark.asyncio
async def test_load_default_roles_permissions(admin_manager):
    """Test loading default roles and permissions."""
    # Verify default permissions were loaded
    assert len(admin_manager._permission_cache) > 0
    assert AdminPermissionType.USER_MANAGEMENT in admin_manager._permission_cache
    assert AdminPermissionType.SYSTEM_MONITORING in admin_manager._permission_cache
    assert AdminPermissionType.ANALYTICS_VIEW in admin_manager._permission_cache
    
    # Verify default roles were loaded
    assert len(admin_manager._role_cache) > 0
    assert 'super_admin' in admin_manager._role_cache
    assert 'admin' in admin_manager._role_cache
    assert 'moderator' in admin_manager._role_cache
    assert 'viewer' in admin_manager._role_cache
    assert 'auditor' in admin_manager._role_cache
    
    # Verify super admin has all permissions
    super_admin_role = admin_manager._role_cache['super_admin']
    assert len(super_admin_role.permissions) == len(AdminPermissionType)
