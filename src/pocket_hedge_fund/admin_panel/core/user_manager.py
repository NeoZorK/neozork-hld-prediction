"""
User Manager

Manages admin users, roles, and permissions.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal
import bcrypt
import secrets

from ..models.admin_models import (
    AdminUser, AdminRole, AdminPermission, AdminSession,
    AdminRoleType, AdminPermissionType, AdminSessionStatus
)

logger = logging.getLogger(__name__)


class UserManager:
    """
    Manages admin users, roles, and permissions.
    """
    
    def __init__(self, db_manager=None):
        """Initialize user manager."""
        self.db_manager = db_manager
        self.users = {}
        self.roles = {}
        self.permissions = {}
        self.sessions = {}
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize user manager."""
        try:
            # Load users from database
            await self._load_users()
            
            # Load roles from database
            await self._load_roles()
            
            # Load permissions from database
            await self._load_permissions()
            
            # Create default admin user if none exists
            await self._create_default_admin()
            
            self.is_initialized = True
            logger.info("User manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize user manager: {e}")
            raise
    
    async def _load_users(self):
        """Load users from database."""
        try:
            # This would load from database
            # For now, use empty dict
            self.users = {}
            logger.info("Loaded users from database")
        except Exception as e:
            logger.error(f"Failed to load users: {e}")
            raise
    
    async def _load_roles(self):
        """Load roles from database."""
        try:
            # This would load from database
            # For now, use empty dict
            self.roles = {}
            logger.info("Loaded roles from database")
        except Exception as e:
            logger.error(f"Failed to load roles: {e}")
            raise
    
    async def _load_permissions(self):
        """Load permissions from database."""
        try:
            # This would load from database
            # For now, use empty dict
            self.permissions = {}
            logger.info("Loaded permissions from database")
        except Exception as e:
            logger.error(f"Failed to load permissions: {e}")
            raise
    
    async def _create_default_admin(self):
        """Create default admin user if none exists."""
        try:
            # Check if any super admin exists
            super_admins = [u for u in self.users.values() if u.role == AdminRoleType.SUPER_ADMIN]
            
            if not super_admins:
                # Create default super admin
                default_admin = AdminUser(
                    username="admin",
                    email="admin@pockethedgefund.com",
                    full_name="System Administrator",
                    role=AdminRoleType.SUPER_ADMIN,
                    permissions=list(AdminPermissionType),
                    is_active=True,
                    is_verified=True,
                    created_by="system"
                )
                
                # Set default password
                default_password = "admin123"
                default_admin.password_hash = self._hash_password(default_password)
                
                self.users[default_admin.id] = default_admin
                
                logger.info("Created default admin user (username: admin, password: admin123)")
        except Exception as e:
            logger.error(f"Failed to create default admin: {e}")
            raise
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to hash password: {e}")
            raise
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            logger.error(f"Failed to verify password: {e}")
            return False
    
    async def authenticate_user(self, username: str, password: str) -> Optional[AdminUser]:
        """Authenticate user with username and password."""
        try:
            # Find user by username
            user = None
            for u in self.users.values():
                if u.username == username:
                    user = u
                    break
            
            if not user:
                logger.warning(f"Authentication failed: user {username} not found")
                return None
            
            # Check if user is active
            if not user.is_active:
                logger.warning(f"Authentication failed: user {username} is inactive")
                return None
            
            # Check if user is locked
            if user.locked_until and user.locked_until > datetime.now():
                logger.warning(f"Authentication failed: user {username} is locked until {user.locked_until}")
                return None
            
            # Verify password
            if not user.password_hash or not self._verify_password(password, user.password_hash):
                # Increment login attempts
                user.login_attempts += 1
                
                # Lock user if max attempts reached
                max_attempts = 5  # This should come from config
                if user.login_attempts >= max_attempts:
                    user.locked_until = datetime.now() + timedelta(minutes=30)
                    logger.warning(f"User {username} locked due to too many failed attempts")
                
                logger.warning(f"Authentication failed: invalid password for user {username}")
                return None
            
            # Reset login attempts on successful login
            user.login_attempts = 0
            user.locked_until = None
            user.last_login = datetime.now()
            
            logger.info(f"User {username} authenticated successfully")
            return user
            
        except Exception as e:
            logger.error(f"Authentication error for user {username}: {e}")
            return None
    
    async def create_user(self, user_data: Dict[str, Any]) -> AdminUser:
        """Create new admin user."""
        try:
            # Validate required fields
            required_fields = ['username', 'email', 'full_name', 'role']
            for field in required_fields:
                if field not in user_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Check if username already exists
            for existing_user in self.users.values():
                if existing_user.username == user_data['username']:
                    raise ValueError("Username already exists")
            
            # Check if email already exists
            for existing_user in self.users.values():
                if existing_user.email == user_data['email']:
                    raise ValueError("Email already exists")
            
            # Create user
            user = AdminUser(
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                role=AdminRoleType(user_data['role']),
                permissions=user_data.get('permissions', []),
                is_active=user_data.get('is_active', True),
                is_verified=user_data.get('is_verified', False),
                timezone=user_data.get('timezone', 'UTC'),
                language=user_data.get('language', 'en'),
                preferences=user_data.get('preferences'),
                created_by=user_data.get('created_by', 'system')
            )
            
            # Set password if provided
            if 'password' in user_data:
                user.password_hash = self._hash_password(user_data['password'])
            
            # Add user
            self.users[user.id] = user
            
            logger.info(f"Created user {user.username} with role {user.role}")
            return user
            
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise
    
    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> AdminUser:
        """Update admin user."""
        try:
            if user_id not in self.users:
                raise ValueError("User not found")
            
            user = self.users[user_id]
            
            # Update fields
            for field, value in updates.items():
                if field == 'password':
                    user.password_hash = self._hash_password(value)
                elif field == 'role':
                    user.role = AdminRoleType(value)
                elif field == 'permissions':
                    user.permissions = [AdminPermissionType(p) for p in value]
                elif hasattr(user, field):
                    setattr(user, field, value)
            
            user.updated_at = datetime.now()
            
            logger.info(f"Updated user {user.username}")
            return user
            
        except Exception as e:
            logger.error(f"Failed to update user: {e}")
            raise
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete admin user."""
        try:
            if user_id not in self.users:
                raise ValueError("User not found")
            
            user = self.users[user_id]
            
            # Don't allow deleting the last super admin
            if user.role == AdminRoleType.SUPER_ADMIN:
                super_admins = [u for u in self.users.values() if u.role == AdminRoleType.SUPER_ADMIN]
                if len(super_admins) <= 1:
                    raise ValueError("Cannot delete the last super admin")
            
            # Terminate all user sessions
            await self._terminate_user_sessions(user_id)
            
            # Delete user
            del self.users[user_id]
            
            logger.info(f"Deleted user {user.username}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete user: {e}")
            raise
    
    async def get_user(self, user_id: str) -> Optional[AdminUser]:
        """Get user by ID."""
        try:
            return self.users.get(user_id)
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            return None
    
    async def get_user_by_username(self, username: str) -> Optional[AdminUser]:
        """Get user by username."""
        try:
            for user in self.users.values():
                if user.username == username:
                    return user
            return None
        except Exception as e:
            logger.error(f"Failed to get user by username: {e}")
            return None
    
    async def list_users(
        self,
        role: Optional[AdminRoleType] = None,
        is_active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AdminUser]:
        """List users with optional filtering."""
        try:
            users = list(self.users.values())
            
            # Apply filters
            if role:
                users = [u for u in users if u.role == role]
            
            if is_active is not None:
                users = [u for u in users if u.is_active == is_active]
            
            # Apply pagination
            users = users[offset:offset + limit]
            
            return users
        except Exception as e:
            logger.error(f"Failed to list users: {e}")
            return []
    
    async def has_permission(self, user: AdminUser, permission: str) -> bool:
        """Check if user has specific permission."""
        try:
            # Super admin has all permissions
            if user.role == AdminRoleType.SUPER_ADMIN:
                return True
            
            # Check user's direct permissions
            if permission in [p.value for p in user.permissions]:
                return True
            
            # Check role-based permissions
            if user.role in self.roles:
                role = self.roles[user.role]
                if permission in [p.value for p in role.permissions]:
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Failed to check permission: {e}")
            return False
    
    async def create_session(self, user: AdminUser, ip_address: str = None, user_agent: str = None) -> AdminSession:
        """Create user session."""
        try:
            # Generate session token
            session_token = secrets.token_urlsafe(32)
            
            # Create session
            session = AdminSession(
                user_id=user.id,
                username=user.username,
                session_token=session_token,
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=datetime.now() + timedelta(hours=8)
            )
            
            # Store session
            self.sessions[session.id] = session
            
            logger.info(f"Created session for user {user.username}")
            return session
            
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            raise
    
    async def validate_session(self, session_token: str) -> Optional[AdminSession]:
        """Validate session token."""
        try:
            # Find session by token
            session = None
            for s in self.sessions.values():
                if s.session_token == session_token:
                    session = s
                    break
            
            if not session:
                return None
            
            # Check if session is active
            if session.status != AdminSessionStatus.ACTIVE:
                return None
            
            # Check if session is expired
            if session.expires_at < datetime.now():
                session.status = AdminSessionStatus.EXPIRED
                return None
            
            # Update last activity
            session.last_activity = datetime.now()
            
            return session
            
        except Exception as e:
            logger.error(f"Failed to validate session: {e}")
            return None
    
    async def terminate_session(self, session_id: str, terminated_by: str = None, reason: str = None) -> bool:
        """Terminate user session."""
        try:
            if session_id not in self.sessions:
                return False
            
            session = self.sessions[session_id]
            session.status = AdminSessionStatus.TERMINATED
            session.terminated_at = datetime.now()
            session.terminated_by = terminated_by
            session.termination_reason = reason
            
            logger.info(f"Terminated session for user {session.username}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to terminate session: {e}")
            return False
    
    async def _terminate_user_sessions(self, user_id: str):
        """Terminate all sessions for user."""
        try:
            for session in self.sessions.values():
                if session.user_id == user_id and session.status == AdminSessionStatus.ACTIVE:
                    session.status = AdminSessionStatus.TERMINATED
                    session.terminated_at = datetime.now()
                    session.termination_reason = "user_deleted"
            
            logger.info(f"Terminated all sessions for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to terminate user sessions: {e}")
    
    async def create_role(self, role_data: Dict[str, Any]) -> AdminRole:
        """Create new admin role."""
        try:
            # Validate required fields
            required_fields = ['name', 'description']
            for field in required_fields:
                if field not in role_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Check if role name already exists
            for existing_role in self.roles.values():
                if existing_role.name == role_data['name']:
                    raise ValueError("Role name already exists")
            
            # Create role
            role = AdminRole(
                name=role_data['name'],
                description=role_data['description'],
                permissions=[AdminPermissionType(p) for p in role_data.get('permissions', [])],
                is_system_role=role_data.get('is_system_role', False),
                is_active=role_data.get('is_active', True),
                created_by=role_data.get('created_by', 'system')
            )
            
            # Add role
            self.roles[role.id] = role
            
            logger.info(f"Created role {role.name}")
            return role
            
        except Exception as e:
            logger.error(f"Failed to create role: {e}")
            raise
    
    async def update_role(self, role_id: str, updates: Dict[str, Any]) -> AdminRole:
        """Update admin role."""
        try:
            if role_id not in self.roles:
                raise ValueError("Role not found")
            
            role = self.roles[role_id]
            
            # Don't allow updating system roles
            if role.is_system_role:
                raise ValueError("Cannot update system roles")
            
            # Update fields
            for field, value in updates.items():
                if field == 'permissions':
                    role.permissions = [AdminPermissionType(p) for p in value]
                elif hasattr(role, field):
                    setattr(role, field, value)
            
            role.updated_at = datetime.now()
            
            logger.info(f"Updated role {role.name}")
            return role
            
        except Exception as e:
            logger.error(f"Failed to update role: {e}")
            raise
    
    async def delete_role(self, role_id: str) -> bool:
        """Delete admin role."""
        try:
            if role_id not in self.roles:
                raise ValueError("Role not found")
            
            role = self.roles[role_id]
            
            # Don't allow deleting system roles
            if role.is_system_role:
                raise ValueError("Cannot delete system roles")
            
            # Check if role is in use
            for user in self.users.values():
                if user.role.value == role.name:
                    raise ValueError("Cannot delete role that is in use")
            
            # Delete role
            del self.roles[role_id]
            
            logger.info(f"Deleted role {role.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete role: {e}")
            raise
    
    async def get_user_activity_report(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get user activity report."""
        try:
            # Mock user activity data
            activity_data = {
                "total_users": len(self.users),
                "active_users": len([u for u in self.users.values() if u.is_active]),
                "users_by_role": {},
                "recent_logins": [],
                "failed_logins": 0,
                "locked_users": 0
            }
            
            # Count users by role
            for user in self.users.values():
                role = user.role.value
                if role not in activity_data["users_by_role"]:
                    activity_data["users_by_role"][role] = 0
                activity_data["users_by_role"][role] += 1
            
            # Get recent logins
            recent_users = sorted(
                [u for u in self.users.values() if u.last_login],
                key=lambda x: x.last_login,
                reverse=True
            )[:10]
            
            activity_data["recent_logins"] = [
                {
                    "username": u.username,
                    "last_login": u.last_login.isoformat() if u.last_login else None,
                    "role": u.role.value
                }
                for u in recent_users
            ]
            
            # Count failed logins and locked users
            for user in self.users.values():
                if user.login_attempts > 0:
                    activity_data["failed_logins"] += user.login_attempts
                if user.locked_until and user.locked_until > datetime.now():
                    activity_data["locked_users"] += 1
            
            return activity_data
        except Exception as e:
            logger.error(f"Failed to get user activity report: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup user manager resources."""
        try:
            self.users.clear()
            self.roles.clear()
            self.permissions.clear()
            self.sessions.clear()
            self.is_initialized = False
            logger.info("User manager cleanup completed")
        except Exception as e:
            logger.error(f"Error during user manager cleanup: {e}")
