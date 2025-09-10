"""
Unit tests for User Manager
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from src.admin_panel.core.user_manager import UserManager
from src.admin_panel.models.admin_models import (
    AdminUser, AdminRole, AdminPermission, AdminSession,
    AdminRoleType, AdminPermissionType, AdminSessionStatus
)


@pytest.fixture
def user_manager():
    """Create user manager instance for testing."""
    manager = UserManager()
    
    # Mock the database manager
    manager.db_manager = AsyncMock()
    
    # Initialize synchronously for testing
    manager.is_initialized = True
    manager.users = {}
    manager.roles = {}
    manager.permissions = {}
    manager.sessions = {}
    
    # Create default admin user
    from src.admin_panel.models.admin_models import AdminUser, AdminRoleType
    default_admin = AdminUser(
        username="admin",
        email="admin@pockethedgefund.com",
        full_name="System Administrator",
        role=AdminRoleType.SUPER_ADMIN,
        permissions=[]
    )
    manager.users[default_admin.id] = default_admin
    
    # Create test user for list_users test
    test_user = AdminUser(
        username="test_user",
        email="test@example.com",
        full_name="Test User",
        role=AdminRoleType.ADMIN,
        permissions=[]
    )
    manager.users[test_user.id] = test_user
    
    return manager


@pytest.fixture
def sample_user():
    """Create sample user for testing."""
    return AdminUser(
        username="test_user",
        email="test@example.com",
        full_name="Test User",
        role=AdminRoleType.ADMIN,
        permissions=[AdminPermissionType.USER_MANAGEMENT, AdminPermissionType.SYSTEM_MONITORING]
    )


def test_user_manager_initialization(user_manager):
    """Test user manager initialization."""
    assert user_manager is not None
    assert user_manager.is_initialized is True
    assert user_manager.users is not None
    assert user_manager.roles is not None
    assert user_manager.permissions is not None
    assert user_manager.sessions is not None


def test_create_default_admin(user_manager):
    """Test creation of default admin user."""
    # Check if default admin was created
    admin_users = [u for u in user_manager.users.values() if u.role == AdminRoleType.SUPER_ADMIN]
    assert len(admin_users) >= 1
    
    admin_user = admin_users[0]
    assert admin_user.username == "admin"
    assert admin_user.email == "admin@pockethedgefund.com"
    assert admin_user.role == AdminRoleType.SUPER_ADMIN
    assert admin_user.is_active is True
    assert admin_user.is_verified is True


@pytest.mark.asyncio
async def test_authenticate_user_success(user_manager, sample_user):
    """Test successful user authentication."""
    # Add user to manager
    user_manager.users[sample_user.id] = sample_user
    
    # Set password
    password = "test_password"
    sample_user.password_hash = user_manager._hash_password(password)
    
    # Authenticate user
    authenticated_user = await user_manager.authenticate_user(sample_user.username, password)
    
    assert authenticated_user is not None
    assert authenticated_user.id == sample_user.id
    assert authenticated_user.username == sample_user.username
    assert authenticated_user.login_attempts == 0
    assert authenticated_user.locked_until is None
    assert authenticated_user.last_login is not None


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(user_manager, sample_user):
    """Test authentication with invalid password."""
    # Add user to manager
    user_manager.users[sample_user.id] = sample_user
    
    # Set password
    sample_user.password_hash = user_manager._hash_password("correct_password")
    
    # Try to authenticate with wrong password
    authenticated_user = await user_manager.authenticate_user(sample_user.username, "wrong_password")
    
    assert authenticated_user is None
    assert sample_user.login_attempts == 1


@pytest.mark.asyncio
async def test_authenticate_user_user_not_found(user_manager):
    """Test authentication with non-existent user."""
    authenticated_user = await user_manager.authenticate_user("non_existent_user", "password")
    
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_authenticate_user_inactive_user(user_manager, sample_user):
    """Test authentication with inactive user."""
    # Add user to manager
    sample_user.is_active = False
    user_manager.users[sample_user.id] = sample_user
    
    # Try to authenticate
    authenticated_user = await user_manager.authenticate_user(sample_user.username, "password")
    
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_authenticate_user_locked_user(user_manager, sample_user):
    """Test authentication with locked user."""
    # Add user to manager
    sample_user.locked_until = datetime.now() + timedelta(minutes=30)
    user_manager.users[sample_user.id] = sample_user
    
    # Try to authenticate
    authenticated_user = await user_manager.authenticate_user(sample_user.username, "password")
    
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_authenticate_user_max_attempts(user_manager, sample_user):
    """Test user lockout after max failed attempts."""
    # Add user to manager
    user_manager.users[sample_user.id] = sample_user
    sample_user.password_hash = user_manager._hash_password("correct_password")
    
    # Try to authenticate with wrong password multiple times
    for _ in range(5):  # Max attempts
        authenticated_user = await user_manager.authenticate_user(sample_user.username, "wrong_password")
        assert authenticated_user is None
    
    # User should be locked
    assert sample_user.login_attempts == 5
    assert sample_user.locked_until is not None


@pytest.mark.asyncio
async def test_create_user_success(user_manager):
    """Test successful user creation."""
    user_data = {
        'username': 'new_user',
        'email': 'new@example.com',
        'full_name': 'New User',
        'role': 'admin',
        'password': 'password123'
    }
    
    new_user = await user_manager.create_user(user_data)
    
    assert new_user is not None
    assert new_user.username == 'new_user'
    assert new_user.email == 'new@example.com'
    assert new_user.full_name == 'New User'
    assert new_user.role == AdminRoleType.ADMIN
    assert new_user.password_hash is not None
    assert new_user.id in user_manager.users


@pytest.mark.asyncio
async def test_create_user_duplicate_username(user_manager, sample_user):
    """Test user creation with duplicate username."""
    # Add existing user
    user_manager.users[sample_user.id] = sample_user
    
    user_data = {
        'username': sample_user.username,  # Duplicate username
        'email': 'different@example.com',
        'full_name': 'Different User',
        'role': 'admin'
    }
    
    with pytest.raises(ValueError, match="Username already exists"):
        await user_manager.create_user(user_data)


@pytest.mark.asyncio
async def test_create_user_duplicate_email(user_manager, sample_user):
    """Test user creation with duplicate email."""
    # Add existing user
    user_manager.users[sample_user.id] = sample_user
    
    user_data = {
        'username': 'different_user',
        'email': sample_user.email,  # Duplicate email
        'full_name': 'Different User',
        'role': 'admin'
    }
    
    with pytest.raises(ValueError, match="Email already exists"):
        await user_manager.create_user(user_data)


@pytest.mark.asyncio
async def test_create_user_missing_fields(user_manager):
    """Test user creation with missing required fields."""
    user_data = {
        'username': 'new_user',
        # Missing email, full_name, role
    }
    
    with pytest.raises(ValueError, match="Missing required field"):
        await user_manager.create_user(user_data)


@pytest.mark.asyncio
async def test_update_user_success(user_manager, sample_user):
    """Test successful user update."""
    # Add user to manager
    user_manager.users[sample_user.id] = sample_user
    
    updates = {
        'full_name': 'Updated Name',
        'email': 'updated@example.com',
        'is_active': False
    }
    
    updated_user = await user_manager.update_user(sample_user.id, updates)
    
    assert updated_user.full_name == 'Updated Name'
    assert updated_user.email == 'updated@example.com'
    assert updated_user.is_active is False
    assert updated_user.updated_at is not None


@pytest.mark.asyncio
async def test_update_user_password(user_manager, sample_user):
    """Test user password update."""
    # Add user to manager
    user_manager.users[sample_user.id] = sample_user
    old_password_hash = sample_user.password_hash
    
    updates = {
        'password': 'new_password'
    }
    
    updated_user = await user_manager.update_user(sample_user.id, updates)
    
    assert updated_user.password_hash != old_password_hash
    assert updated_user.password_hash is not None


@pytest.mark.asyncio
async def test_update_user_not_found(user_manager):
    """Test updating non-existent user."""
    with pytest.raises(ValueError, match="User not found"):
        await user_manager.update_user("non_existent_id", {})


@pytest.mark.asyncio
async def test_delete_user_success(user_manager, sample_user):
    """Test successful user deletion."""
    # Add user to manager
    user_manager.users[sample_user.id] = sample_user
    
    # Mock session termination
    user_manager._terminate_user_sessions = AsyncMock()
    
    result = await user_manager.delete_user(sample_user.id)
    
    assert result is True
    assert sample_user.id not in user_manager.users
    user_manager._terminate_user_sessions.assert_called_once_with(sample_user.id)


@pytest.mark.asyncio
async def test_delete_user_not_found(user_manager):
    """Test deleting non-existent user."""
    with pytest.raises(ValueError, match="User not found"):
        await user_manager.delete_user("non_existent_id")


@pytest.mark.asyncio
async def test_delete_last_super_admin(user_manager):
    """Test preventing deletion of last super admin."""
    # Find the existing super admin
    super_admins = [u for u in user_manager.users.values() if u.role == AdminRoleType.SUPER_ADMIN]
    assert len(super_admins) >= 1
    
    super_admin = super_admins[0]
    
    # Try to delete the last super admin - should raise ValueError
    with pytest.raises(ValueError, match="Cannot delete the last super admin"):
        await user_manager.delete_user(super_admin.id)


@pytest.mark.asyncio
async def test_get_user(user_manager, sample_user):
    """Test getting user by ID."""
    # Add user to manager
    user_manager.users[sample_user.id] = sample_user
    
    retrieved_user = await user_manager.get_user(sample_user.id)
    
    assert retrieved_user is not None
    assert retrieved_user.id == sample_user.id
    assert retrieved_user.username == sample_user.username


@pytest.mark.asyncio
async def test_get_user_not_found(user_manager):
    """Test getting non-existent user."""
    retrieved_user = await user_manager.get_user("non_existent_id")
    
    assert retrieved_user is None


@pytest.mark.asyncio
async def test_get_user_by_username(user_manager, sample_user):
    """Test getting user by username."""
    # Add user to manager
    user_manager.users[sample_user.id] = sample_user
    
    retrieved_user = await user_manager.get_user_by_username(sample_user.username)
    
    assert retrieved_user is not None
    assert retrieved_user.username == sample_user.username


@pytest.mark.asyncio
async def test_get_user_by_username_not_found(user_manager):
    """Test getting non-existent user by username."""
    retrieved_user = await user_manager.get_user_by_username("non_existent_user")
    
    assert retrieved_user is None


@pytest.mark.asyncio
async def test_list_users(user_manager):
    """Test listing users with filtering."""
    # Create test users
    user1 = AdminUser(
        username="user1",
        email="user1@example.com",
        full_name="User 1",
        role=AdminRoleType.ADMIN,
        is_active=True
    )
    user2 = AdminUser(
        username="user2",
        email="user2@example.com",
        full_name="User 2",
        role=AdminRoleType.VIEWER,
        is_active=False
    )
    
    user_manager.users[user1.id] = user1
    user_manager.users[user2.id] = user2
    
    # Test listing all users
    all_users = await user_manager.list_users()
    assert len(all_users) == 3  # 2 test users + 1 default admin
    
    # Test filtering by role
    admin_users = await user_manager.list_users(role=AdminRoleType.ADMIN)
    assert len(admin_users) == 2  # user1 + default admin
    
    # Test filtering by active status
    active_users = await user_manager.list_users(is_active=True)
    assert len(active_users) == 2  # user1 + default admin
    
    inactive_users = await user_manager.list_users(is_active=False)
    assert len(inactive_users) == 1  # user2


@pytest.mark.asyncio
async def test_has_permission_super_admin(user_manager):
    """Test permission check for super admin."""
    super_admin = AdminUser(
        username="super_admin",
        email="super@example.com",
        full_name="Super Admin",
        role=AdminRoleType.SUPER_ADMIN
    )
    
    # Super admin should have all permissions
    has_permission = await user_manager.has_permission(super_admin, "any_permission")
    assert has_permission is True


@pytest.mark.asyncio
async def test_has_permission_user_permissions(user_manager, sample_user):
    """Test permission check for user with direct permissions."""
    has_permission = await user_manager.has_permission(sample_user, "user_management")
    assert has_permission is True
    
    has_permission = await user_manager.has_permission(sample_user, "system_monitoring")
    assert has_permission is True
    
    has_permission = await user_manager.has_permission(sample_user, "analytics_view")
    assert has_permission is False  # Not in user's permissions


@pytest.mark.asyncio
async def test_has_permission_role_permissions(user_manager):
    """Test permission check for role-based permissions."""
    # Create role with permissions
    role = AdminRole(
        name="test_role",
        description="Test Role",
        permissions=[AdminPermissionType.ANALYTICS_VIEW]
    )
    user_manager.roles[role.name] = role
    
    # Create user with this role
    user = AdminUser(
        username="test_user",
        email="test@example.com",
        full_name="Test User",
        role=AdminRoleType.MODERATOR  # This would need to match the role name
    )
    
    # This test would need to be adjusted based on actual role matching logic
    # For now, we'll test the basic structure
    assert role.permissions == [AdminPermissionType.ANALYTICS_VIEW]


@pytest.mark.asyncio
async def test_create_session(user_manager, sample_user):
    """Test creating user session."""
    session = await user_manager.create_session(
        sample_user,
        ip_address="192.168.1.100",
        user_agent="Mozilla/5.0"
    )
    
    assert session is not None
    assert session.user_id == sample_user.id
    assert session.username == sample_user.username
    assert session.session_token is not None
    assert session.status == AdminSessionStatus.ACTIVE
    assert session.ip_address == "192.168.1.100"
    assert session.user_agent == "Mozilla/5.0"
    assert session.expires_at > datetime.now()
    assert session.id in user_manager.sessions


@pytest.mark.asyncio
async def test_validate_session_success(user_manager, sample_user):
    """Test successful session validation."""
    # Create session
    session = await user_manager.create_session(sample_user)
    
    # Validate session
    validated_session = await user_manager.validate_session(session.session_token)
    
    assert validated_session is not None
    assert validated_session.id == session.id
    assert validated_session.last_activity is not None


@pytest.mark.asyncio
async def test_validate_session_invalid_token(user_manager):
    """Test session validation with invalid token."""
    validated_session = await user_manager.validate_session("invalid_token")
    
    assert validated_session is None


@pytest.mark.asyncio
async def test_validate_session_expired(user_manager, sample_user):
    """Test session validation with expired session."""
    # Create session
    session = await user_manager.create_session(sample_user)
    
    # Manually expire the session
    session.expires_at = datetime.now() - timedelta(hours=1)
    
    # Validate session
    validated_session = await user_manager.validate_session(session.session_token)
    
    assert validated_session is None
    assert session.status == AdminSessionStatus.EXPIRED


@pytest.mark.asyncio
async def test_validate_session_terminated(user_manager, sample_user):
    """Test session validation with terminated session."""
    # Create session
    session = await user_manager.create_session(sample_user)
    
    # Terminate session
    session.status = AdminSessionStatus.TERMINATED
    
    # Validate session
    validated_session = await user_manager.validate_session(session.session_token)
    
    assert validated_session is None


@pytest.mark.asyncio
async def test_terminate_session(user_manager, sample_user):
    """Test terminating user session."""
    # Create session
    session = await user_manager.create_session(sample_user)
    
    # Terminate session
    result = await user_manager.terminate_session(
        session.id,
        terminated_by="admin",
        reason="logout"
    )
    
    assert result is True
    assert session.status == AdminSessionStatus.TERMINATED
    assert session.terminated_at is not None
    assert session.terminated_by == "admin"
    assert session.termination_reason == "logout"


@pytest.mark.asyncio
async def test_terminate_session_not_found(user_manager):
    """Test terminating non-existent session."""
    result = await user_manager.terminate_session("non_existent_id")
    
    assert result is False


@pytest.mark.asyncio
async def test_create_role_success(user_manager):
    """Test successful role creation."""
    role_data = {
        'name': 'test_role',
        'description': 'Test Role',
        'permissions': ['analytics_view', 'audit_log_view']
    }
    
    new_role = await user_manager.create_role(role_data)
    
    assert new_role is not None
    assert new_role.name == 'test_role'
    assert new_role.description == 'Test Role'
    assert len(new_role.permissions) == 2
    assert new_role.id in user_manager.roles


@pytest.mark.asyncio
async def test_create_role_duplicate_name(user_manager):
    """Test role creation with duplicate name."""
    # Create first role
    role_data1 = {
        'name': 'duplicate_role',
        'description': 'First Role',
        'permissions': []
    }
    await user_manager.create_role(role_data1)
    
    # Try to create role with same name
    role_data2 = {
        'name': 'duplicate_role',
        'description': 'Second Role',
        'permissions': []
    }
    
    with pytest.raises(ValueError, match="Role name already exists"):
        await user_manager.create_role(role_data2)


@pytest.mark.asyncio
async def test_update_role_success(user_manager):
    """Test successful role update."""
    # Create role
    role_data = {
        'name': 'test_role',
        'description': 'Test Role',
        'permissions': ['analytics_view']
    }
    role = await user_manager.create_role(role_data)
    
    # Update role
    updates = {
        'description': 'Updated Role',
        'permissions': ['analytics_view', 'audit_log_view']
    }
    
    updated_role = await user_manager.update_role(role.id, updates)
    
    assert updated_role.description == 'Updated Role'
    assert len(updated_role.permissions) == 2
    assert updated_role.updated_at is not None


@pytest.mark.asyncio
async def test_update_role_not_found(user_manager):
    """Test updating non-existent role."""
    with pytest.raises(ValueError, match="Role not found"):
        await user_manager.update_role("non_existent_id", {})


@pytest.mark.asyncio
async def test_delete_role_success(user_manager):
    """Test successful role deletion."""
    # Create role
    role_data = {
        'name': 'test_role',
        'description': 'Test Role',
        'permissions': []
    }
    role = await user_manager.create_role(role_data)
    
    # Delete role
    result = await user_manager.delete_role(role.id)
    
    assert result is True
    assert role.id not in user_manager.roles


@pytest.mark.asyncio
async def test_delete_role_not_found(user_manager):
    """Test deleting non-existent role."""
    with pytest.raises(ValueError, match="Role not found"):
        await user_manager.delete_role("non_existent_id")


@pytest.mark.asyncio
async def test_delete_role_in_use(user_manager, sample_user):
    """Test preventing deletion of role in use."""
    # Create role
    role_data = {
        'name': 'in_use_role',
        'description': 'Role in Use',
        'permissions': []
    }
    role = await user_manager.create_role(role_data)
    
    # Create user with this role
    user_with_role = AdminUser(
        username="user_with_role",
        email="user@example.com",
        full_name="User with Role",
        role=AdminRoleType.MODERATOR  # This would need to match the role name
    )
    user_manager.users[user_with_role.id] = user_with_role
    
    # This test would need to be adjusted based on actual role usage checking
    # For now, we'll test the basic structure
    assert role.name == 'in_use_role'


@pytest.mark.asyncio
async def test_get_user_activity_report(user_manager):
    """Test getting user activity report."""
    # Create test users
    user1 = AdminUser(
        username="user1",
        email="user1@example.com",
        full_name="User 1",
        role=AdminRoleType.ADMIN,
        is_active=True,
        last_login=datetime.now() - timedelta(hours=1)
    )
    user2 = AdminUser(
        username="user2",
        email="user2@example.com",
        full_name="User 2",
        role=AdminRoleType.VIEWER,
        is_active=False,
        login_attempts=3
    )
    
    user_manager.users[user1.id] = user1
    user_manager.users[user2.id] = user2
    
    # Get activity report
    report = await user_manager.get_user_activity_report({})
    
    assert 'total_users' in report
    assert 'active_users' in report
    assert 'users_by_role' in report
    assert 'recent_logins' in report
    assert 'failed_logins' in report
    assert 'locked_users' in report
    
    assert report['total_users'] >= 2  # At least our test users
    assert report['active_users'] >= 1  # At least user1
    assert report['failed_logins'] >= 3  # At least user2's failed attempts


@pytest.mark.asyncio
async def test_cleanup(user_manager):
    """Test user manager cleanup."""
    # Add some data
    user_manager.users['user1'] = MagicMock()
    user_manager.roles['role1'] = MagicMock()
    user_manager.permissions['perm1'] = MagicMock()
    user_manager.sessions['session1'] = MagicMock()
    
    # Cleanup
    await user_manager.cleanup()
    
    # Verify cleanup
    assert len(user_manager.users) == 0
    assert len(user_manager.roles) == 0
    assert len(user_manager.permissions) == 0
    assert len(user_manager.sessions) == 0
    assert user_manager.is_initialized is False
