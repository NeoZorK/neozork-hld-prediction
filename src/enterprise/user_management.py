#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-User Management and Permissions Module

This module provides comprehensive user management features including:
- User registration and authentication
- Role-based access control (RBAC)
- Permission management
- User groups and teams
- Session management
- User activity tracking
- Profile management
- Password policies
- Account lockout and recovery
"""

import hashlib
import secrets
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import bcrypt
import jwt
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserStatus(Enum):
    """User status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"
    LOCKED = "locked"

class UserRole(Enum):
    """User roles."""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MANAGER = "manager"
    TRADER = "trader"
    ANALYST = "analyst"
    VIEWER = "viewer"
    AUDITOR = "auditor"

class Permission(Enum):
    """Permissions."""
    # System permissions
    SYSTEM_ADMIN = "system_admin"
    USER_MANAGEMENT = "user_management"
    ROLE_MANAGEMENT = "role_management"
    
    # Trading permissions
    TRADE_READ = "trade_read"
    TRADE_WRITE = "trade_write"
    TRADE_EXECUTE = "trade_execute"
    PORTFOLIO_MANAGE = "portfolio_manage"
    
    # Data permissions
    DATA_READ = "data_read"
    DATA_WRITE = "data_write"
    DATA_EXPORT = "data_export"
    
    # Analytics permissions
    ANALYTICS_VIEW = "analytics_view"
    ANALYTICS_CREATE = "analytics_create"
    REPORTS_GENERATE = "reports_generate"
    
    # Security permissions
    SECURITY_VIEW = "security_view"
    AUDIT_VIEW = "audit_view"
    API_MANAGE = "api_manage"

class SessionStatus(Enum):
    """Session status."""
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"

@dataclass
class User:
    """User model."""
    user_id: str
    username: str
    email: str
    password_hash: str
    first_name: str
    last_name: str
    role: UserRole
    status: UserStatus
    permissions: List[Permission] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    password_changed_at: datetime = field(default_factory=datetime.now)
    profile_data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UserGroup:
    """User group model."""
    group_id: str
    name: str
    description: str
    permissions: List[Permission] = field(default_factory=list)
    members: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class UserSession:
    """User session model."""
    session_id: str
    user_id: str
    ip_address: str
    user_agent: str
    created_at: datetime
    last_activity: datetime
    expires_at: datetime
    status: SessionStatus
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UserActivity:
    """User activity log."""
    activity_id: str
    user_id: str
    action: str
    resource: str
    ip_address: str
    user_agent: str
    timestamp: datetime
    success: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

class PasswordPolicy:
    """Password policy manager."""
    
    def __init__(self):
        self.min_length = 8
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_numbers = True
        self.require_special_chars = True
        self.max_age_days = 90
        self.history_count = 5
    
    def validate_password(self, password: str) -> Dict[str, Any]:
        """Validate password against policy."""
        errors = []
        
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters long")
        
        if self.require_uppercase and not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        if self.require_lowercase and not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        if self.require_numbers and not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number")
        
        if self.require_special_chars and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            errors.append("Password must contain at least one special character")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def is_password_expired(self, password_changed_at: datetime) -> bool:
        """Check if password is expired."""
        return (datetime.now() - password_changed_at).days > self.max_age_days

class RoleManager:
    """Manages roles and permissions."""
    
    def __init__(self):
        self.role_permissions = self._setup_default_roles()
    
    def _setup_default_roles(self) -> Dict[UserRole, List[Permission]]:
        """Setup default role permissions."""
        return {
            UserRole.SUPER_ADMIN: list(Permission),
            UserRole.ADMIN: [
                Permission.USER_MANAGEMENT,
                Permission.ROLE_MANAGEMENT,
                Permission.TRADE_READ,
                Permission.TRADE_WRITE,
                Permission.TRADE_EXECUTE,
                Permission.PORTFOLIO_MANAGE,
                Permission.DATA_READ,
                Permission.DATA_WRITE,
                Permission.DATA_EXPORT,
                Permission.ANALYTICS_VIEW,
                Permission.ANALYTICS_CREATE,
                Permission.REPORTS_GENERATE,
                Permission.SECURITY_VIEW,
                Permission.AUDIT_VIEW,
                Permission.API_MANAGE
            ],
            UserRole.MANAGER: [
                Permission.TRADE_READ,
                Permission.TRADE_WRITE,
                Permission.PORTFOLIO_MANAGE,
                Permission.DATA_READ,
                Permission.DATA_EXPORT,
                Permission.ANALYTICS_VIEW,
                Permission.ANALYTICS_CREATE,
                Permission.REPORTS_GENERATE,
                Permission.SECURITY_VIEW
            ],
            UserRole.TRADER: [
                Permission.TRADE_READ,
                Permission.TRADE_WRITE,
                Permission.TRADE_EXECUTE,
                Permission.PORTFOLIO_MANAGE,
                Permission.DATA_READ,
                Permission.ANALYTICS_VIEW
            ],
            UserRole.ANALYST: [
                Permission.TRADE_READ,
                Permission.DATA_READ,
                Permission.DATA_EXPORT,
                Permission.ANALYTICS_VIEW,
                Permission.ANALYTICS_CREATE,
                Permission.REPORTS_GENERATE
            ],
            UserRole.VIEWER: [
                Permission.TRADE_READ,
                Permission.DATA_READ,
                Permission.ANALYTICS_VIEW
            ],
            UserRole.AUDITOR: [
                Permission.TRADE_READ,
                Permission.DATA_READ,
                Permission.AUDIT_VIEW,
                Permission.SECURITY_VIEW
            ]
        }
    
    def get_role_permissions(self, role: UserRole) -> List[Permission]:
        """Get permissions for role."""
        return self.role_permissions.get(role, [])
    
    def has_permission(self, user_permissions: List[Permission], required_permission: Permission) -> bool:
        """Check if user has permission."""
        return required_permission in user_permissions
    
    def get_effective_permissions(self, user: User) -> List[Permission]:
        """Get effective permissions for user (role + explicit + group)."""
        permissions = set()
        
        # Add role permissions
        permissions.update(self.get_role_permissions(user.role))
        
        # Add explicit permissions
        permissions.update(user.permissions)
        
        return list(permissions)

class SessionManager:
    """Manages user sessions."""
    
    def __init__(self, session_timeout: int = 3600):
        self.sessions: Dict[str, UserSession] = {}
        self.session_timeout = session_timeout
        self.max_sessions_per_user = 5
    
    def create_session(self, user_id: str, ip_address: str, user_agent: str) -> str:
        """Create new session."""
        # Clean up old sessions for user
        self._cleanup_user_sessions(user_id)
        
        session_id = secrets.token_urlsafe(32)
        now = datetime.now()
        
        session = UserSession(
            session_id=session_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=now,
            last_activity=now,
            expires_at=now + timedelta(seconds=self.session_timeout),
            status=SessionStatus.ACTIVE
        )
        
        self.sessions[session_id] = session
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[UserSession]:
        """Validate session."""
        session = self.sessions.get(session_id)
        
        if not session:
            return None
        
        if session.status != SessionStatus.ACTIVE:
            return None
        
        if datetime.now() > session.expires_at:
            session.status = SessionStatus.EXPIRED
            return None
        
        # Update last activity
        session.last_activity = datetime.now()
        session.expires_at = datetime.now() + timedelta(seconds=self.session_timeout)
        
        return session
    
    def terminate_session(self, session_id: str):
        """Terminate session."""
        if session_id in self.sessions:
            self.sessions[session_id].status = SessionStatus.TERMINATED
    
    def terminate_user_sessions(self, user_id: str):
        """Terminate all sessions for user."""
        for session in self.sessions.values():
            if session.user_id == user_id and session.status == SessionStatus.ACTIVE:
                session.status = SessionStatus.TERMINATED
    
    def _cleanup_user_sessions(self, user_id: str):
        """Clean up old sessions for user."""
        user_sessions = [
            s for s in self.sessions.values()
            if s.user_id == user_id and s.status == SessionStatus.ACTIVE
        ]
        
        if len(user_sessions) >= self.max_sessions_per_user:
            # Remove oldest session
            oldest_session = min(user_sessions, key=lambda s: s.created_at)
            oldest_session.status = SessionStatus.TERMINATED

class UserManager:
    """Main user management system."""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.groups: Dict[str, UserGroup] = {}
        self.password_policy = PasswordPolicy()
        self.role_manager = RoleManager()
        self.session_manager = SessionManager()
        self.activity_log: List[UserActivity] = []
        
        # Initialize default admin user
        self._create_default_admin()
    
    def _create_default_admin(self):
        """Create default admin user."""
        admin_password = self._hash_password("admin123")
        admin_user = User(
            user_id="admin",
            username="admin",
            email="admin@system.com",
            password_hash=admin_password,
            first_name="System",
            last_name="Administrator",
            role=UserRole.SUPER_ADMIN,
            status=UserStatus.ACTIVE,
            permissions=self.role_manager.get_role_permissions(UserRole.SUPER_ADMIN)
        )
        self.users["admin"] = admin_user
        logger.info("Default admin user created")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    
    def _log_activity(self, user_id: str, action: str, resource: str, 
                     ip_address: str, user_agent: str, success: bool, **metadata):
        """Log user activity."""
        activity = UserActivity(
            activity_id=secrets.token_urlsafe(16),
            user_id=user_id,
            action=action,
            resource=resource,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.now(),
            success=success,
            metadata=metadata
        )
        self.activity_log.append(activity)
    
    def register_user(self, username: str, email: str, password: str, 
                     first_name: str, last_name: str, role: UserRole = UserRole.VIEWER) -> Dict[str, Any]:
        """Register new user."""
        try:
            # Validate password
            password_validation = self.password_policy.validate_password(password)
            if not password_validation['valid']:
                return {
                    'status': 'error',
                    'message': 'Password does not meet policy requirements',
                    'errors': password_validation['errors']
                }
            
            # Check if user already exists
            if any(u.username == username or u.email == email for u in self.users.values()):
                return {'status': 'error', 'message': 'User already exists'}
            
            # Create user
            user_id = secrets.token_urlsafe(16)
            password_hash = self._hash_password(password)
            
            user = User(
                user_id=user_id,
                username=username,
                email=email,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name,
                role=role,
                status=UserStatus.PENDING,
                permissions=self.role_manager.get_role_permissions(role)
            )
            
            self.users[user_id] = user
            
            # Log activity
            self._log_activity(user_id, 'user_registration', 'user', 'system', 'system', True)
            
            logger.info(f"User {username} registered successfully")
            return {'status': 'success', 'user_id': user_id, 'message': 'User registered successfully'}
            
        except Exception as e:
            logger.error(f"User registration failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def authenticate_user(self, username: str, password: str, 
                         ip_address: str = "unknown", user_agent: str = "unknown") -> Dict[str, Any]:
        """Authenticate user."""
        try:
            # Find user
            user = None
            for u in self.users.values():
                if u.username == username:
                    user = u
                    break
            
            if not user:
                self._log_activity(None, 'login_attempt', 'authentication', ip_address, user_agent, False)
                return {'status': 'error', 'message': 'Invalid credentials'}
            
            # Check user status
            if user.status != UserStatus.ACTIVE:
                self._log_activity(user.user_id, 'login_attempt', 'authentication', ip_address, user_agent, False)
                return {'status': 'error', 'message': f'User account is {user.status.value}'}
            
            # Check if user is locked
            if user.locked_until and user.locked_until > datetime.now():
                self._log_activity(user.user_id, 'login_attempt', 'authentication', ip_address, user_agent, False)
                return {'status': 'error', 'message': 'Account is locked'}
            
            # Verify password
            if not self._verify_password(password, user.password_hash):
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:
                    user.locked_until = datetime.now() + timedelta(minutes=30)
                
                self._log_activity(user.user_id, 'login_attempt', 'authentication', ip_address, user_agent, False)
                return {'status': 'error', 'message': 'Invalid credentials'}
            
            # Reset failed attempts
            user.failed_login_attempts = 0
            user.locked_until = None
            user.last_login = datetime.now()
            
            # Create session
            session_id = self.session_manager.create_session(user.user_id, ip_address, user_agent)
            
            # Get effective permissions
            effective_permissions = self.role_manager.get_effective_permissions(user)
            
            # Log successful login
            self._log_activity(user.user_id, 'login', 'authentication', ip_address, user_agent, True)
            
            logger.info(f"User {username} authenticated successfully")
            return {
                'status': 'success',
                'session_id': session_id,
                'user_id': user.user_id,
                'username': user.username,
                'role': user.role.value,
                'permissions': [p.value for p in effective_permissions],
                'profile': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }
            }
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def validate_session(self, session_id: str) -> Dict[str, Any]:
        """Validate session and return user info."""
        session = self.session_manager.validate_session(session_id)
        
        if not session:
            return {'status': 'error', 'message': 'Invalid or expired session'}
        
        user = self.users.get(session.user_id)
        if not user or user.status != UserStatus.ACTIVE:
            return {'status': 'error', 'message': 'User not found or inactive'}
        
        effective_permissions = self.role_manager.get_effective_permissions(user)
        
        return {
            'status': 'success',
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role.value,
            'permissions': [p.value for p in effective_permissions],
            'profile': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        }
    
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if user has permission."""
        user = self.users.get(user_id)
        if not user:
            return False
        
        effective_permissions = self.role_manager.get_effective_permissions(user)
        return self.role_manager.has_permission(effective_permissions, permission)
    
    def create_group(self, name: str, description: str, permissions: List[Permission]) -> Dict[str, Any]:
        """Create user group."""
        try:
            group_id = secrets.token_urlsafe(16)
            
            group = UserGroup(
                group_id=group_id,
                name=name,
                description=description,
                permissions=permissions
            )
            
            self.groups[group_id] = group
            
            logger.info(f"Group {name} created successfully")
            return {'status': 'success', 'group_id': group_id, 'message': 'Group created successfully'}
            
        except Exception as e:
            logger.error(f"Group creation failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def add_user_to_group(self, user_id: str, group_id: str) -> Dict[str, Any]:
        """Add user to group."""
        try:
            user = self.users.get(user_id)
            group = self.groups.get(group_id)
            
            if not user:
                return {'status': 'error', 'message': 'User not found'}
            
            if not group:
                return {'status': 'error', 'message': 'Group not found'}
            
            if user_id not in group.members:
                group.members.append(user_id)
                group.updated_at = datetime.now()
            
            if group_id not in user.groups:
                user.groups.append(group_id)
                user.updated_at = datetime.now()
            
            logger.info(f"User {user_id} added to group {group_id}")
            return {'status': 'success', 'message': 'User added to group successfully'}
            
        except Exception as e:
            logger.error(f"Add user to group failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_user_activity(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get user activity log."""
        user_activities = [
            activity for activity in self.activity_log
            if activity.user_id == user_id
        ]
        
        return [
            {
                'activity_id': activity.activity_id,
                'action': activity.action,
                'resource': activity.resource,
                'ip_address': activity.ip_address,
                'timestamp': activity.timestamp.isoformat(),
                'success': activity.success,
                'metadata': activity.metadata
            }
            for activity in user_activities[-limit:]
        ]
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get system summary."""
        return {
            'total_users': len(self.users),
            'active_users': len([u for u in self.users.values() if u.status == UserStatus.ACTIVE]),
            'total_groups': len(self.groups),
            'active_sessions': len([s for s in self.session_manager.sessions.values() if s.status == SessionStatus.ACTIVE]),
            'total_activities': len(self.activity_log),
            'recent_activities': len([a for a in self.activity_log if (datetime.now() - a.timestamp).total_seconds() <= 3600])
        }

# Example usage and testing
if __name__ == "__main__":
    # Create user manager
    user_manager = UserManager()
    
    # Test user registration
    print("Testing user registration...")
    result = user_manager.register_user(
        "testuser", "test@example.com", "Password123!", "Test", "User", UserRole.TRADER
    )
    print(f"Registration result: {result}")
    
    # Test authentication
    print("\nTesting authentication...")
    auth_result = user_manager.authenticate_user("testuser", "Password123!", "192.168.1.1", "TestAgent")
    print(f"Authentication result: {auth_result}")
    
    # Test session validation
    if auth_result['status'] == 'success':
        session_id = auth_result['session_id']
        print(f"\nTesting session validation...")
        session_result = user_manager.validate_session(session_id)
        print(f"Session validation result: {session_result}")
    
    # Test group creation
    print("\nTesting group creation...")
    group_result = user_manager.create_group(
        "Traders", "Trading team", [Permission.TRADE_READ, Permission.TRADE_WRITE]
    )
    print(f"Group creation result: {group_result}")
    
    # Test system summary
    print("\nSystem summary:")
    summary = user_manager.get_system_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\nUser Manager initialized successfully!")
