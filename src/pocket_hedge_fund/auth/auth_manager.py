"""
Authentication Manager for Pocket Hedge Fund

This module provides comprehensive authentication and authorization
functionality including JWT tokens, MFA, password management, and
role-based access control.
"""

import asyncio
import logging
import secrets
import hashlib
import hmac
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
import uuid

import bcrypt
import pyotp
import qrcode
from io import BytesIO
import base64
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from ..database.connection import get_db_manager
from ..database.models import User, UserRole, APIKey, AuditLog
from ..validation import get_user_validator

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer

logger = logging.getLogger(__name__)


@dataclass
class AuthConfig:
    """Authentication configuration."""
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    refresh_token_expiration_days: int = 30
    password_min_length: int = 8
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 30
    mfa_issuer: str = "NeoZork Pocket Hedge Fund"


@dataclass
class LoginAttempt:
    """Login attempt tracking."""
    user_id: str
    attempts: int
    last_attempt: datetime
    locked_until: Optional[datetime] = None


class PasswordManager:
    """Password management utilities."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
        """Validate password strength."""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            errors.append("Password must contain at least one special character")
        
        return len(errors) == 0, errors


class MFAManager:
    """Multi-Factor Authentication manager."""
    
    def __init__(self, config: AuthConfig):
        self.config = config
    
    def generate_secret(self) -> str:
        """Generate MFA secret."""
        return pyotp.random_base32()
    
    def generate_qr_code(self, user_email: str, secret: str) -> str:
        """Generate QR code for MFA setup."""
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name=self.config.mfa_issuer
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_base64}"
    
    def verify_totp(self, secret: str, token: str) -> bool:
        """Verify TOTP token."""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)
    
    def generate_backup_codes(self, count: int = 10) -> List[str]:
        """Generate backup codes for MFA."""
        return [secrets.token_hex(4).upper() for _ in range(count)]


class JWTManager:
    """JWT token management."""
    
    def __init__(self, config: AuthConfig):
        self.config = config
    
    def generate_access_token(self, user_id: str, email: str, role: str, mfa_verified: bool = False) -> str:
        """Generate JWT access token."""
        payload = {
            'user_id': user_id,
            'email': email,
            'role': role,
            'mfa_verified': mfa_verified,
            'type': 'access',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=self.config.jwt_expiration_hours)
        }
        
        return jwt.encode(payload, self.config.jwt_secret, algorithm=self.config.jwt_algorithm)
    
    def generate_refresh_token(self, user_id: str) -> str:
        """Generate JWT refresh token."""
        payload = {
            'user_id': user_id,
            'type': 'refresh',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=self.config.refresh_token_expiration_days)
        }
        
        return jwt.encode(payload, self.config.jwt_secret, algorithm=self.config.jwt_algorithm)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, self.config.jwt_secret, algorithms=[self.config.jwt_algorithm])
            return payload
        except ExpiredSignatureError:
            raise ValueError("Token has expired")
        except InvalidTokenError:
            raise ValueError("Invalid token")
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """Generate new access token from refresh token."""
        payload = self.verify_token(refresh_token)
        
        if payload.get('type') != 'refresh':
            raise ValueError("Invalid refresh token")
        
        # Get user details from database
        # This would need to be implemented with database access
        user_id = payload['user_id']
        
        # For now, return a new token with basic info
        # In real implementation, fetch user details from database
        return self.generate_access_token(user_id, "", "", False)


class AuthenticationManager:
    """
    Main authentication manager for Pocket Hedge Fund.
    
    This class provides:
    - User registration and login
    - Password management
    - JWT token generation and validation
    - Multi-factor authentication
    - Role-based access control
    - Login attempt tracking and lockout
    - API key management
    """
    
    def __init__(self, config: Optional[AuthConfig] = None):
        self.config = config or AuthConfig(
            jwt_secret=secrets.token_urlsafe(32)
        )
        self.password_manager = PasswordManager()
        self.mfa_manager = MFAManager(self.config)
        self.jwt_manager = JWTManager(self.config)
        self.login_attempts: Dict[str, LoginAttempt] = {}
    
    async def register_user(
        self,
        email: str,
        username: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        phone: str = "",
        country: str = ""
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Register a new user.
            
        Returns:
            Tuple of (success, message, user_data)
        """
        try:
            db_manager = await get_db_manager()
            
            # Validate password strength
            is_valid, errors = self.password_manager.validate_password_strength(password)
            if not is_valid:
                return False, f"Password validation failed: {', '.join(errors)}", None
            
            # Check if user already exists
            existing_user_query = """
                SELECT id FROM users WHERE email = $1 OR username = $2
            """
            existing_users = await db_manager.execute_query(
                existing_user_query, 
                [email, username]
            )
            
            if existing_users:
                return False, "User with this email or username already exists", None
            
            # Hash password
            password_hash = self.password_manager.hash_password(password)
            
            # Create user
            user_id = str(uuid.uuid4())
            create_user_query = """
                INSERT INTO users (
                    id, email, username, password_hash, first_name, last_name,
                    phone, country, kyc_status, is_active, role, created_at, updated_at
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
                )
            """
            
            now = datetime.utcnow()
            await db_manager.execute_command(
                create_user_query,
                [
                    user_id, email, username, password_hash, first_name, last_name,
                    phone, country, 'pending', True, 'investor', now, now
                ]
            )
            
            # Log registration
            await self._log_audit_event(
                user_id=user_id,
                action="user_registered",
                resource_type="user",
                resource_id=user_id,
                new_values={'email': email, 'username': username}
            )
            
            user_data = {
                'id': user_id,
                'email': email,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'role': 'investor'
            }
            
            return True, "User registered successfully", user_data
            
        except Exception as e:
            logger.error(f"User registration failed: {e}")
            return False, f"Registration failed: {str(e)}", None
    
    async def login_user(
        self,
        email: str,
        password: str,
        mfa_token: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Authenticate user login.
            
        Returns:
            Tuple of (success, message, auth_data)
        """
        try:
            db_manager = await get_db_manager()
            
            # Get user by email
            user_query = """
                SELECT id, email, username, password_hash, first_name, last_name,
                       role, is_active, mfa_enabled, mfa_secret, last_login
                FROM users WHERE email = $1
            """
            users = await db_manager.execute_query(user_query, [email])
            
            if not users:
                return False, "Invalid email or password", None
            
            user = users[0]
            user_id = str(user['id'])
            
            # Check if user is active
            if not user['is_active']:
                return False, "Account is deactivated", None
            
            # Check login attempts and lockout
            if self._is_user_locked(user_id):
                return False, "Account is temporarily locked due to too many failed attempts", None
            
            # Verify password
            if not self.password_manager.verify_password(password, user['password_hash']):
                await self._record_failed_login(user_id)
                return False, "Invalid email or password", None
            
            # Check MFA if enabled
            mfa_verified = False
            if user['mfa_enabled']:
                if not mfa_token:
                    return False, "MFA token required", {'mfa_required': True}
                
                if not self.mfa_manager.verify_totp(user['mfa_secret'], mfa_token):
                    await self._record_failed_login(user_id)
                    return False, "Invalid MFA token", None
                
                mfa_verified = True
            
            # Clear failed login attempts
            self._clear_failed_logins(user_id)
            
            # Update last login
            await self._update_last_login(user_id)
            
            # Generate tokens
            access_token = self.jwt_manager.generate_access_token(
                user_id, user['email'], user['role'], mfa_verified
            )
            refresh_token = self.jwt_manager.generate_refresh_token(user_id)
            
            # Log successful login
            await self._log_audit_event(
                user_id=user_id,
                action="user_login",
                resource_type="user",
                resource_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            auth_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': str(user_id),
                    'email': user['email'],
                    'username': user['username'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'role': user['role'],
                    'mfa_enabled': user['mfa_enabled']
                },
                'expires_in': self.config.jwt_expiration_hours * 3600
            }
            
            return True, "Login successful", auth_data
            
        except Exception as e:
            logger.error(f"User login failed: {e}")
            return False, f"Login failed: {str(e)}", None
    
    async def setup_mfa(self, user_id: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Setup MFA for user."""
        try:
            db_manager = await get_db_manager()
            
            # Generate MFA secret
            secret = self.mfa_manager.generate_secret()
            
            # Get user email for QR code
            user_query = "SELECT email FROM users WHERE id = $1"
            users = await db_manager.execute_query(user_query, [user_id])
            
            if not users:
                return False, "User not found", None
            
            user_email = users[0]['email']
            
            # Generate QR code
            qr_code = self.mfa_manager.generate_qr_code(user_email, secret)
            
            # Generate backup codes
            backup_codes = self.mfa_manager.generate_backup_codes()
            
            # Update user with MFA secret (but don't enable yet)
            update_query = """
                UPDATE users SET mfa_secret = $1, updated_at = $2
                WHERE id = $3
            """
            await db_manager.execute_command(
                update_query,
                [secret, datetime.utcnow(), user_id]
            )
            
            mfa_data = {
                'secret': secret,
                'qr_code': qr_code,
                'backup_codes': backup_codes
            }
            
            return True, "MFA setup data generated", mfa_data
            
        except Exception as e:
            logger.error(f"MFA setup failed: {e}")
            return False, f"MFA setup failed: {str(e)}", None
    
    async def enable_mfa(self, user_id: str, verification_token: str) -> Tuple[bool, str]:
        """Enable MFA for user after verification."""
        try:
            db_manager = await get_db_manager()
            
            # Get user's MFA secret
            user_query = "SELECT mfa_secret FROM users WHERE id = $1"
            users = await db_manager.execute_query(user_query, [user_id])
            
            if not users:
                return False, "User not found"
            
            secret = users[0]['mfa_secret']
            if not secret:
                return False, "MFA not set up"
            
            # Verify token
            if not self.mfa_manager.verify_totp(secret, verification_token):
                return False, "Invalid verification token"
            
            # Enable MFA
            update_query = """
                UPDATE users SET mfa_enabled = true, updated_at = $1
                WHERE id = $2
            """
            await db_manager.execute_command(
                update_query,
                [datetime.utcnow(), user_id]
            )
            
            # Log MFA enablement
            await self._log_audit_event(
                user_id=user_id,
                action="mfa_enabled",
                resource_type="user",
                resource_id=user_id
            )
            
            return True, "MFA enabled successfully"
            
        except Exception as e:
            logger.error(f"MFA enablement failed: {e}")
            return False, f"MFA enablement failed: {str(e)}"
    
    async def verify_token(self, token: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Verify JWT token and return user info."""
        try:
            payload = self.jwt_manager.verify_token(token)
            
            if payload.get('type') != 'access':
                return False, "Invalid token type", None
            
            # Get user details from database
            db_manager = await get_db_manager()
            user_query = """
                SELECT id, email, username, first_name, last_name, role, is_active, mfa_enabled
                FROM users WHERE id = $1
            """
            users = await db_manager.execute_query(user_query, [payload['user_id']])
            
            if not users:
                return False, "User not found", None
            
            user = users[0]
            if not user['is_active']:
                return False, "User account is deactivated", None
            
            user_data = {
                'id': user['id'],
                'email': user['email'],
                'username': user['username'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'role': user['role'],
                'mfa_enabled': user['mfa_enabled'],
                'mfa_verified': payload.get('mfa_verified', False)
            }
            
            return True, "Token valid", user_data
            
        except ValueError as e:
            return False, str(e), None
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return False, f"Token verification failed: {str(e)}", None
    
    async def create_api_key(
        self,
        user_id: str,
        key_name: str,
        permissions: List[str],
        expires_days: Optional[int] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Create API key for user."""
        try:
            db_manager = await get_db_manager()
            
            # Generate API key
            api_key = f"nz_{secrets.token_urlsafe(32)}"
            
            # Calculate expiration
            expires_at = None
            if expires_days:
                expires_at = datetime.utcnow() + timedelta(days=expires_days)
            
            # Create API key record
            key_id = str(uuid.uuid4())
            create_key_query = """
                INSERT INTO api_keys (
                    id, user_id, key_name, api_key, permissions, is_active,
                    expires_at, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """
            
            await db_manager.execute_command(
                create_key_query,
                [
                    key_id, user_id, key_name, api_key, permissions, True, expires_at, datetime.utcnow()
                ]
            )
            
            # Log API key creation
            await self._log_audit_event(
                user_id=user_id,
                action="api_key_created",
                resource_type="api_key",
                resource_id=key_id,
                new_values={'key_name': key_name, 'permissions': permissions}
            )
            
            api_key_data = {
                'id': key_id,
                'key_name': key_name,
                'api_key': api_key,
                'permissions': permissions,
                'expires_at': expires_at.isoformat() if expires_at else None,
                'created_at': datetime.utcnow().isoformat()
            }
            
            return True, "API key created successfully", api_key_data
                
        except Exception as e:
            logger.error(f"API key creation failed: {e}")
            return False, f"API key creation failed: {str(e)}", None
    
    def _is_user_locked(self, user_id: str) -> bool:
        """Check if user is locked due to failed login attempts."""
        if user_id not in self.login_attempts:
            return False
        
        attempt = self.login_attempts[user_id]
        if attempt.locked_until and datetime.utcnow() < attempt.locked_until:
            return True
        
        return False
    
    async def _record_failed_login(self, user_id: str):
        """Record failed login attempt."""
        if user_id not in self.login_attempts:
            self.login_attempts[user_id] = LoginAttempt(
                user_id=user_id,
                attempts=0,
                last_attempt=datetime.utcnow()
            )
        
        attempt = self.login_attempts[user_id]
        attempt.attempts += 1
        attempt.last_attempt = datetime.utcnow()
        
        if attempt.attempts >= self.config.max_login_attempts:
            attempt.locked_until = datetime.utcnow() + timedelta(
                minutes=self.config.lockout_duration_minutes
            )
    
    def _clear_failed_logins(self, user_id: str):
        """Clear failed login attempts for user."""
        if user_id in self.login_attempts:
            del self.login_attempts[user_id]
    
    async def _update_last_login(self, user_id: str):
        """Update user's last login timestamp."""
        db_manager = await get_db_manager()
        update_query = """
            UPDATE users SET last_login = $1, updated_at = $2
            WHERE id = $3
        """
        await db_manager.execute_command(
            update_query,
            [datetime.utcnow(), datetime.utcnow(), user_id]
        )
    
    async def _log_audit_event(
        self,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """Log audit event."""
        try:
            db_manager = await get_db_manager()
            log_query = """
                INSERT INTO audit_log (
                    id, user_id, action, resource_type, resource_id,
                    old_values, new_values, ip_address, user_agent, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            """
            
            import json
            
            await db_manager.execute_command(
                log_query,
                [
                    str(uuid.uuid4()), user_id, action, resource_type, resource_id,
                    json.dumps(old_values) if old_values else None,
                    json.dumps(new_values) if new_values else None,
                    ip_address, user_agent, datetime.utcnow()
                ]
            )
        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")


# Global authentication manager instance
auth_manager = AuthenticationManager()


async def get_auth_manager() -> AuthenticationManager:
    """Get global authentication manager instance."""
    return auth_manager

async def get_current_user(token: str = Depends(HTTPBearer())) -> Dict[str, Any]:
    """Get current user from JWT token."""
    try:
        auth_manager = await get_auth_manager()
        is_valid, message, user_data = await auth_manager.verify_token(token.credentials)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=message
            )
        
        return user_data
    except Exception as e:
        logger.error(f"Failed to get current user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )