"""
User Validation Module

This module provides comprehensive validation for user operations
including registration, authentication, and profile management.
"""

import logging
import re
from typing import Dict, List, Tuple, Any
from datetime import datetime, timedelta

from src.pocket_hedge_fund.database.connection import get_db_manager

logger = logging.getLogger(__name__)

class UserValidator:
    """Comprehensive user validation with business rules."""
    
    def __init__(self):
        self.min_password_length = 8
        self.max_password_length = 128
        self.min_username_length = 3
        self.max_username_length = 50
        self.min_name_length = 2
        self.max_name_length = 50
        self.max_login_attempts = 5
        self.lockout_duration = timedelta(minutes=30)
        
        # Password requirements
        self.password_patterns = {
            'uppercase': r'[A-Z]',
            'lowercase': r'[a-z]',
            'digit': r'\d',
            'special': r'[!@#$%^&*(),.?":{}|<>]'
        }
        
        # Email validation
        self.email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Username validation
        self.username_pattern = r'^[a-zA-Z0-9_-]+$'
        
    async def validate_user_registration(self, user_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate user registration request.
        
        Args:
            user_data: User registration data
            
        Returns:
            Tuple of (is_valid, error_message, validation_data)
        """
        try:
            validation_data = {}
            
            # Validate email
            is_valid, error_msg = self._validate_email(user_data.get('email', ''))
            if not is_valid:
                return False, error_msg, validation_data
            
            # Check email uniqueness
            is_valid, error_msg = await self._validate_email_uniqueness(user_data.get('email', ''))
            if not is_valid:
                return False, error_msg, validation_data
            
            # Validate username
            is_valid, error_msg = self._validate_username(user_data.get('username', ''))
            if not is_valid:
                return False, error_msg, validation_data
            
            # Check username uniqueness
            is_valid, error_msg = await self._validate_username_uniqueness(user_data.get('username', ''))
            if not is_valid:
                return False, error_msg, validation_data
            
            # Validate password
            is_valid, error_msg = self._validate_password(user_data.get('password', ''))
            if not is_valid:
                return False, error_msg, validation_data
            
            # Validate names
            is_valid, error_msg = self._validate_names(
                user_data.get('first_name', ''),
                user_data.get('last_name', '')
            )
            if not is_valid:
                return False, error_msg, validation_data
            
            # Validate role if provided
            if 'role' in user_data:
                is_valid, error_msg = self._validate_role(user_data['role'])
                if not is_valid:
                    return False, error_msg, validation_data
            
            # Check for suspicious patterns
            is_valid, error_msg = self._validate_suspicious_patterns(user_data)
            if not is_valid:
                return False, error_msg, validation_data
            
            return True, "User registration validation passed", validation_data
            
        except Exception as e:
            logger.error(f"User registration validation failed: {e}")
            return False, f"User registration validation error: {str(e)}", {}
    
    async def validate_user_login(self, email: str, password: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate user login request.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Tuple of (is_valid, error_message, validation_data)
        """
        try:
            validation_data = {}
            
            # Validate email format
            is_valid, error_msg = self._validate_email(email)
            if not is_valid:
                return False, error_msg, validation_data
            
            # Check if user exists
            is_valid, error_msg, user_data = await self._validate_user_exists(email)
            if not is_valid:
                return False, error_msg, validation_data
            validation_data['user'] = user_data
            
            # Check account status
            is_valid, error_msg = self._validate_account_status(user_data)
            if not is_valid:
                return False, error_msg, validation_data
            
            # Check login attempts
            is_valid, error_msg = await self._validate_login_attempts(user_data['id'])
            if not is_valid:
                return False, error_msg, validation_data
            
            return True, "User login validation passed", validation_data
            
        except Exception as e:
            logger.error(f"User login validation failed: {e}")
            return False, f"User login validation error: {str(e)}", {}
    
    async def validate_password_change(self, user_id: str, old_password: str, new_password: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate password change request.
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            Tuple of (is_valid, error_message, validation_data)
        """
        try:
            validation_data = {}
            
            # Validate new password
            is_valid, error_msg = self._validate_password(new_password)
            if not is_valid:
                return False, error_msg, validation_data
            
            # Check if new password is different from old
            if old_password == new_password:
                return False, "New password must be different from current password", validation_data
            
            # Get user data
            is_valid, error_msg, user_data = await self._validate_user_exists_by_id(user_id)
            if not is_valid:
                return False, error_msg, validation_data
            validation_data['user'] = user_data
            
            return True, "Password change validation passed", validation_data
            
        except Exception as e:
            logger.error(f"Password change validation failed: {e}")
            return False, f"Password change validation error: {str(e)}", {}
    
    def _validate_email(self, email: str) -> Tuple[bool, str]:
        """Validate email format."""
        if not email or not isinstance(email, str):
            return False, "Email is required"
        
        if not re.match(self.email_pattern, email):
            return False, "Invalid email format"
        
        if len(email) > 254:  # RFC 5321 limit
            return False, "Email address too long"
        
        return True, "Email validation passed"
    
    async def _validate_email_uniqueness(self, email: str) -> Tuple[bool, str]:
        """Validate email uniqueness."""
        try:
            db_manager = await get_db_manager()
            
            email_query = "SELECT id FROM users WHERE email = $1"
            result = await db_manager.execute_query(email_query, email.lower())
            
            if result:
                return False, "Email address already registered"
            
            return True, "Email uniqueness validation passed"
            
        except Exception as e:
            logger.error(f"Email uniqueness validation failed: {e}")
            return False, f"Email uniqueness validation error: {str(e)}"
    
    def _validate_username(self, username: str) -> Tuple[bool, str]:
        """Validate username format."""
        if not username or not isinstance(username, str):
            return False, "Username is required"
        
        if len(username) < self.min_username_length:
            return False, f"Username must be at least {self.min_username_length} characters"
        
        if len(username) > self.max_username_length:
            return False, f"Username must be no more than {self.max_username_length} characters"
        
        if not re.match(self.username_pattern, username):
            return False, "Username can only contain letters, numbers, underscores, and hyphens"
        
        # Check for reserved usernames
        reserved_usernames = ['admin', 'administrator', 'root', 'system', 'api', 'www', 'mail', 'support']
        if username.lower() in reserved_usernames:
            return False, "Username is reserved"
        
        return True, "Username validation passed"
    
    async def _validate_username_uniqueness(self, username: str) -> Tuple[bool, str]:
        """Validate username uniqueness."""
        try:
            db_manager = await get_db_manager()
            
            username_query = "SELECT id FROM users WHERE username = $1"
            result = await db_manager.execute_query(username_query, username.lower())
            
            if result:
                return False, "Username already taken"
            
            return True, "Username uniqueness validation passed"
            
        except Exception as e:
            logger.error(f"Username uniqueness validation failed: {e}")
            return False, f"Username uniqueness validation error: {str(e)}"
    
    def _validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate password strength."""
        if not password or not isinstance(password, str):
            return False, "Password is required"
        
        if len(password) < self.min_password_length:
            return False, f"Password must be at least {self.min_password_length} characters"
        
        if len(password) > self.max_password_length:
            return False, f"Password must be no more than {self.max_password_length} characters"
        
        # Check password requirements
        missing_requirements = []
        for requirement, pattern in self.password_patterns.items():
            if not re.search(pattern, password):
                missing_requirements.append(requirement)
        
        if missing_requirements:
            return False, f"Password must contain: {', '.join(missing_requirements)}"
        
        # Check for common passwords
        common_passwords = ['password', '123456', 'qwerty', 'abc123', 'password123']
        if password.lower() in common_passwords:
            return False, "Password is too common"
        
        # Check for repeated characters
        if len(set(password)) < len(password) * 0.5:
            return False, "Password contains too many repeated characters"
        
        return True, "Password validation passed"
    
    def _validate_names(self, first_name: str, last_name: str) -> Tuple[bool, str]:
        """Validate first and last names."""
        if not first_name or not isinstance(first_name, str):
            return False, "First name is required"
        
        if not last_name or not isinstance(last_name, str):
            return False, "Last name is required"
        
        if len(first_name) < self.min_name_length:
            return False, f"First name must be at least {self.min_name_length} characters"
        
        if len(last_name) < self.min_name_length:
            return False, f"Last name must be at least {self.min_name_length} characters"
        
        if len(first_name) > self.max_name_length:
            return False, f"First name must be no more than {self.max_name_length} characters"
        
        if len(last_name) > self.max_name_length:
            return False, f"Last name must be no more than {self.max_name_length} characters"
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        name_pattern = r"^[a-zA-Z\s\-']+$"
        if not re.match(name_pattern, first_name):
            return False, "First name contains invalid characters"
        
        if not re.match(name_pattern, last_name):
            return False, "Last name contains invalid characters"
        
        return True, "Names validation passed"
    
    def _validate_role(self, role: str) -> Tuple[bool, str]:
        """Validate user role."""
        valid_roles = ['investor', 'fund_manager', 'admin', 'premium_investor', 'institutional']
        
        if role not in valid_roles:
            return False, f"Invalid role. Valid roles: {', '.join(valid_roles)}"
        
        return True, "Role validation passed"
    
    def _validate_suspicious_patterns(self, user_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Check for suspicious registration patterns."""
        # Check for test patterns
        email = user_data.get('email', '').lower()
        username = user_data.get('username', '').lower()
        
        test_patterns = ['test', 'demo', 'example', 'sample']
        for pattern in test_patterns:
            if pattern in email or pattern in username:
                return False, "Registration contains test patterns"
        
        # Check for sequential patterns
        if username.isdigit() and len(username) > 3:
            return False, "Username appears to be sequential numbers"
        
        return True, "Suspicious patterns validation passed"
    
    async def _validate_user_exists(self, email: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate user exists by email."""
        try:
            db_manager = await get_db_manager()
            
            user_query = """
                SELECT id, username, email, role, is_active, created_at, last_login
                FROM users 
                WHERE email = $1
            """
            
            result = await db_manager.execute_query(user_query, email.lower())
            
            if not result:
                return False, "User not found", {}
            
            return True, "User exists", dict(result[0])
            
        except Exception as e:
            logger.error(f"User existence validation failed: {e}")
            return False, f"User existence validation error: {str(e)}", {}
    
    async def _validate_user_exists_by_id(self, user_id: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate user exists by ID."""
        try:
            db_manager = await get_db_manager()
            
            user_query = """
                SELECT id, username, email, role, is_active, created_at, last_login
                FROM users 
                WHERE id = $1
            """
            
            result = await db_manager.execute_query(user_query, user_id)
            
            if not result:
                return False, "User not found", {}
            
            return True, "User exists", dict(result[0])
            
        except Exception as e:
            logger.error(f"User existence validation failed: {e}")
            return False, f"User existence validation error: {str(e)}", {}
    
    def _validate_account_status(self, user_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate account status."""
        if not user_data.get('is_active', False):
            return False, "Account is deactivated"
        
        return True, "Account status validation passed"
    
    async def _validate_login_attempts(self, user_id: str) -> Tuple[bool, str]:
        """Validate login attempts and lockout status."""
        try:
            db_manager = await get_db_manager()
            
            # Get recent failed login attempts
            attempts_query = """
                SELECT COUNT(*) as attempt_count, MAX(created_at) as last_attempt
                FROM audit_logs 
                WHERE user_id = $1 
                AND action = 'login_failed' 
                AND created_at > NOW() - INTERVAL '30 minutes'
            """
            
            result = await db_manager.execute_query(attempts_query, user_id)
            attempt_count = result[0]['attempt_count'] if result else 0
            
            if attempt_count >= self.max_login_attempts:
                return False, f"Account temporarily locked due to {attempt_count} failed login attempts"
            
            return True, "Login attempts validation passed"
            
        except Exception as e:
            logger.error(f"Login attempts validation failed: {e}")
            return False, f"Login attempts validation error: {str(e)}"

# Global validator instance
_user_validator = None

async def get_user_validator() -> UserValidator:
    """Get global user validator instance."""
    global _user_validator
    if _user_validator is None:
        _user_validator = UserValidator()
    return _user_validator
