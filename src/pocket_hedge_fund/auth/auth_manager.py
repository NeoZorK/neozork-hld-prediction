"""
Authentication manager for Pocket Hedge Fund.

This module provides comprehensive authentication and authorization
functionality including user management, session handling, and security.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import uuid

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
import jwt
from passlib.context import CryptContext

from ..database.connection import DatabaseManager
from ..database.models import UserModel, UserRole
from .jwt_handler import JWTHandler
from .password_manager import PasswordManager
from .permissions import PermissionManager

logger = logging.getLogger(__name__)


class AuthManager:
    """
    Authentication manager for Pocket Hedge Fund.
    
    Provides user authentication, authorization, session management,
    and security features.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize authentication manager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager
        self.jwt_handler = JWTHandler()
        self.password_manager = PasswordManager()
        self.permission_manager = PermissionManager()
        
        # Session management
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.session_timeout = timedelta(hours=24)
    
    async def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new user.
        
        Args:
            user_data: User registration data
            
        Returns:
            Dict containing registration results
        """
        try:
            # Validate required fields
            required_fields = ['email', 'username', 'password', 'first_name', 'last_name']
            for field in required_fields:
                if field not in user_data or not user_data[field]:
                    return {
                        'status': 'error',
                        'message': f'Missing required field: {field}'
                    }
            
            # Validate email format
            if not self._validate_email(user_data['email']):
                return {
                    'status': 'error',
                    'message': 'Invalid email format'
                }
            
            # Check if user already exists
            if await self._user_exists(user_data['email'], user_data['username']):
                return {
                    'status': 'error',
                    'message': 'User with this email or username already exists'
                }
            
            # Hash password
            password_hash = self.password_manager.hash_password(user_data['password'])
            
            # Create user
            user_id = str(uuid.uuid4())
            role = user_data.get('role', UserRole.INVESTOR.value)
            
            async with self.db_manager.get_async_session() as session:
                await session.execute(
                    text("""
                        INSERT INTO users (id, email, username, password_hash, first_name, last_name, role, is_active, is_verified, created_at, updated_at)
                        VALUES (:id, :email, :username, :password_hash, :first_name, :last_name, :role, :is_active, :is_verified, :created_at, :updated_at)
                    """),
                    {
                        'id': user_id,
                        'email': user_data['email'].lower(),
                        'username': user_data['username'],
                        'password_hash': password_hash,
                        'first_name': user_data['first_name'],
                        'last_name': user_data['last_name'],
                        'role': role,
                        'is_active': True,
                        'is_verified': False,
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }
                )
                await session.commit()
            
            logger.info(f"User registered successfully: {user_data['email']}")
            
            return {
                'status': 'success',
                'message': 'User registered successfully',
                'user_id': user_id,
                'email': user_data['email']
            }
            
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return {
                'status': 'error',
                'message': f'Registration failed: {str(e)}'
            }
    
    async def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dict containing authentication results
        """
        try:
            # Get user from database
            user = await self._get_user_by_email(email)
            if not user:
                return {
                    'status': 'error',
                    'message': 'Invalid email or password'
                }
            
            # Check if user is active
            if not user['is_active']:
                return {
                    'status': 'error',
                    'message': 'Account is deactivated'
                }
            
            # Verify password
            if not self.password_manager.verify_password(password, user['password_hash']):
                return {
                    'status': 'error',
                    'message': 'Invalid email or password'
                }
            
            # Update last login
            await self._update_last_login(user['id'])
            
            # Generate JWT token
            token_data = {
                'user_id': user['id'],
                'email': user['email'],
                'role': user['role'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            token = self.jwt_handler.create_token(token_data)
            
            # Create session
            session_id = str(uuid.uuid4())
            self.active_sessions[session_id] = {
                'user_id': user['id'],
                'email': user['email'],
                'role': user['role'],
                'created_at': datetime.utcnow(),
                'last_activity': datetime.utcnow()
            }
            
            logger.info(f"User authenticated successfully: {email}")
            
            return {
                'status': 'success',
                'message': 'Authentication successful',
                'token': token,
                'session_id': session_id,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'username': user['username'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'role': user['role']
                }
            }
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return {
                'status': 'error',
                'message': f'Authentication failed: {str(e)}'
            }
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Dict containing verification results
        """
        try:
            # Verify token
            payload = self.jwt_handler.verify_token(token)
            if not payload:
                return {
                    'status': 'error',
                    'message': 'Invalid token'
                }
            
            # Check if user still exists and is active
            user = await self._get_user_by_id(payload['user_id'])
            if not user or not user['is_active']:
                return {
                    'status': 'error',
                    'message': 'User not found or inactive'
                }
            
            return {
                'status': 'success',
                'message': 'Token verified',
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'username': user['username'],
                    'role': user['role']
                }
            }
            
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return {
                'status': 'error',
                'message': f'Token verification failed: {str(e)}'
            }
    
    async def refresh_token(self, token: str) -> Dict[str, Any]:
        """
        Refresh JWT token.
        
        Args:
            token: Current JWT token
            
        Returns:
            Dict containing new token
        """
        try:
            # Verify current token
            payload = self.jwt_handler.verify_token(token)
            if not payload:
                return {
                    'status': 'error',
                    'message': 'Invalid token'
                }
            
            # Check if user still exists and is active
            user = await self._get_user_by_id(payload['user_id'])
            if not user or not user['is_active']:
                return {
                    'status': 'error',
                    'message': 'User not found or inactive'
                }
            
            # Generate new token
            new_token_data = {
                'user_id': user['id'],
                'email': user['email'],
                'role': user['role'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            new_token = self.jwt_handler.create_token(new_token_data)
            
            return {
                'status': 'success',
                'message': 'Token refreshed',
                'token': new_token
            }
            
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return {
                'status': 'error',
                'message': f'Token refresh failed: {str(e)}'
            }
    
    async def logout_user(self, session_id: str) -> Dict[str, Any]:
        """
        Logout user and invalidate session.
        
        Args:
            session_id: Session ID to invalidate
            
        Returns:
            Dict containing logout results
        """
        try:
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
            
            return {
                'status': 'success',
                'message': 'Logout successful'
            }
            
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return {
                'status': 'error',
                'message': f'Logout failed: {str(e)}'
            }
    
    async def change_password(self, user_id: str, old_password: str, new_password: str) -> Dict[str, Any]:
        """
        Change user password.
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            Dict containing password change results
        """
        try:
            # Get user
            user = await self._get_user_by_id(user_id)
            if not user:
                return {
                    'status': 'error',
                    'message': 'User not found'
                }
            
            # Verify old password
            if not self.password_manager.verify_password(old_password, user['password_hash']):
                return {
                    'status': 'error',
                    'message': 'Current password is incorrect'
                }
            
            # Validate new password
            if not self.password_manager.validate_password(new_password):
                return {
                    'status': 'error',
                    'message': 'New password does not meet requirements'
                }
            
            # Hash new password
            new_password_hash = self.password_manager.hash_password(new_password)
            
            # Update password
            async with self.db_manager.get_async_session() as session:
                await session.execute(
                    text("""
                        UPDATE users 
                        SET password_hash = :password_hash, updated_at = :updated_at
                        WHERE id = :user_id
                    """),
                    {
                        'password_hash': new_password_hash,
                        'updated_at': datetime.utcnow(),
                        'user_id': user_id
                    }
                )
                await session.commit()
            
            logger.info(f"Password changed for user: {user['email']}")
            
            return {
                'status': 'success',
                'message': 'Password changed successfully'
            }
            
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            return {
                'status': 'error',
                'message': f'Password change failed: {str(e)}'
            }
    
    async def check_permission(self, user_id: str, resource: str, action: str) -> bool:
        """
        Check if user has permission for resource and action.
        
        Args:
            user_id: User ID
            resource: Resource name
            action: Action name
            
        Returns:
            True if user has permission, False otherwise
        """
        try:
            # Get user role
            user = await self._get_user_by_id(user_id)
            if not user:
                return False
            
            # Check permission
            return self.permission_manager.has_permission(user['role'], resource, action)
            
        except Exception as e:
            logger.error(f"Error checking permission: {e}")
            return False
    
    async def get_user_permissions(self, user_id: str) -> List[str]:
        """
        Get all permissions for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of permission strings
        """
        try:
            # Get user role
            user = await self._get_user_by_id(user_id)
            if not user:
                return []
            
            # Get permissions for role
            return self.permission_manager.get_role_permissions(user['role'])
            
        except Exception as e:
            logger.error(f"Error getting user permissions: {e}")
            return []
    
    async def cleanup_expired_sessions(self):
        """Cleanup expired sessions."""
        try:
            current_time = datetime.utcnow()
            expired_sessions = []
            
            for session_id, session_data in self.active_sessions.items():
                if current_time - session_data['last_activity'] > self.session_timeout:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del self.active_sessions[session_id]
            
            if expired_sessions:
                logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
                
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {e}")
    
    # Private helper methods
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    async def _user_exists(self, email: str, username: str) -> bool:
        """Check if user exists by email or username."""
        try:
            async with self.db_manager.get_async_session() as session:
                result = await session.execute(
                    text("""
                        SELECT 1 FROM users 
                        WHERE email = :email OR username = :username
                    """),
                    {'email': email.lower(), 'username': username}
                )
                return result.fetchone() is not None
        except Exception:
            return False
    
    async def _get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        try:
            async with self.db_manager.get_async_session() as session:
                result = await session.execute(
                    text("SELECT * FROM users WHERE email = :email"),
                    {'email': email.lower()}
                )
                row = result.fetchone()
                return dict(row._mapping) if row else None
        except Exception:
            return None
    
    async def _get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        try:
            async with self.db_manager.get_async_session() as session:
                result = await session.execute(
                    text("SELECT * FROM users WHERE id = :user_id"),
                    {'user_id': user_id}
                )
                row = result.fetchone()
                return dict(row._mapping) if row else None
        except Exception:
            return None
    
    async def _update_last_login(self, user_id: str):
        """Update user's last login time."""
        try:
            async with self.db_manager.get_async_session() as session:
                await session.execute(
                    text("""
                        UPDATE users 
                        SET last_login = :last_login, updated_at = :updated_at
                        WHERE id = :user_id
                    """),
                    {
                        'last_login': datetime.utcnow(),
                        'updated_at': datetime.utcnow(),
                        'user_id': user_id
                    }
                )
                await session.commit()
        except Exception as e:
            logger.error(f"Error updating last login: {e}")
