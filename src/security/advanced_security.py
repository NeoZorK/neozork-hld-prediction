#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Security and Compliance Module

This module provides comprehensive security features including:
- Multi-factor authentication (MFA)
- Role-based access control (RBAC)
- API security and rate limiting
- Data encryption and key management
- Audit logging and compliance
- Security monitoring and threat detection
"""

import hashlib
import hmac
import secrets
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import jwt
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
import asyncio
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class UserRole(Enum):
    """User roles."""
    ADMIN = "admin"
    TRADER = "trader"
    ANALYST = "analyst"
    VIEWER = "viewer"
    AUDITOR = "auditor"

class Permission(Enum):
    """Permissions."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"
    TRADE = "trade"
    MANAGE_USERS = "manage_users"
    VIEW_AUDIT = "view_audit"

class ThreatLevel(Enum):
    """Threat levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class User:
    """User model."""
    user_id: str
    username: str
    email: str
    password_hash: str
    role: UserRole
    permissions: List[Permission] = field(default_factory=list)
    mfa_enabled: bool = False
    mfa_secret: Optional[str] = None
    last_login: Optional[datetime] = None
    failed_attempts: int = 0
    locked_until: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class SecurityEvent:
    """Security event model."""
    event_id: str
    user_id: Optional[str]
    event_type: str
    threat_level: ThreatLevel
    description: str
    ip_address: str
    user_agent: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class APIKey:
    """API key model."""
    key_id: str
    user_id: str
    key_hash: str
    permissions: List[Permission]
    rate_limit: int
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class AuditLog:
    """Audit log entry."""
    log_id: str
    user_id: Optional[str]
    action: str
    resource: str
    result: str
    ip_address: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

class EncryptionManager:
    """Manages encryption and decryption."""
    
    def __init__(self):
        self.fernet_key = Fernet.generate_key()
        self.fernet = Fernet(self.fernet_key)
        self.rsa_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.rsa_public_key = self.rsa_private_key.public_key()
    
    def encrypt_symmetric(self, data: str) -> str:
        """Encrypt data using symmetric encryption."""
        try:
            encrypted_data = self.fernet.encrypt(data.encode())
            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Symmetric encryption failed: {e}")
            raise
    
    def decrypt_symmetric(self, encrypted_data: str) -> str:
        """Decrypt data using symmetric encryption."""
        try:
            decoded_data = base64.b64decode(encrypted_data.encode())
            decrypted_data = self.fernet.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Symmetric decryption failed: {e}")
            raise
    
    def encrypt_asymmetric(self, data: str) -> str:
        """Encrypt data using asymmetric encryption."""
        try:
            encrypted_data = self.rsa_public_key.encrypt(
                data.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Asymmetric encryption failed: {e}")
            raise
    
    def decrypt_asymmetric(self, encrypted_data: str) -> str:
        """Decrypt data using asymmetric encryption."""
        try:
            decoded_data = base64.b64decode(encrypted_data.encode())
            decrypted_data = self.rsa_private_key.decrypt(
                decoded_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Asymmetric decryption failed: {e}")
            raise

class MFAManager:
    """Manages multi-factor authentication."""
    
    def __init__(self):
        self.totp_secret_length = 32
    
    def generate_secret(self) -> str:
        """Generate TOTP secret."""
        return base64.b32encode(secrets.token_bytes(self.totp_secret_length)).decode()
    
    def generate_totp(self, secret: str, time_step: int = 30) -> str:
        """Generate TOTP code."""
        try:
            import pyotp
            totp = pyotp.TOTP(secret, interval=time_step)
            return totp.now()
        except ImportError:
            # Fallback implementation
            current_time = int(time.time() // time_step)
            key = base64.b32decode(secret)
            time_bytes = current_time.to_bytes(8, byteorder='big')
            hmac_hash = hmac.new(key, time_bytes, hashlib.sha1).digest()
            offset = hmac_hash[-1] & 0x0f
            code = int.from_bytes(hmac_hash[offset:offset+4], byteorder='big') & 0x7fffffff
            return str(code % 1000000).zfill(6)
    
    def verify_totp(self, secret: str, code: str, time_step: int = 30, window: int = 1) -> bool:
        """Verify TOTP code."""
        try:
            import pyotp
            totp = pyotp.TOTP(secret, interval=time_step)
            return totp.verify(code, valid_window=window)
        except ImportError:
            # Fallback implementation
            current_time = int(time.time() // time_step)
            for i in range(-window, window + 1):
                test_time = current_time + i
                test_code = self.generate_totp(secret, time_step)
                if test_code == code:
                    return True
            return False

class RateLimiter:
    """Rate limiting implementation."""
    
    def __init__(self, max_requests: int = 100, time_window: int = 3600):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(deque)
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed."""
        now = time.time()
        request_times = self.requests[identifier]
        
        # Remove old requests
        while request_times and request_times[0] <= now - self.time_window:
            request_times.popleft()
        
        # Check if under limit
        if len(request_times) < self.max_requests:
            request_times.append(now)
            return True
        
        return False
    
    def get_remaining_requests(self, identifier: str) -> int:
        """Get remaining requests."""
        now = time.time()
        request_times = self.requests[identifier]
        
        # Remove old requests
        while request_times and request_times[0] <= now - self.time_window:
            request_times.popleft()
        
        return max(0, self.max_requests - len(request_times))

class SecurityMonitor:
    """Monitors security events and detects threats."""
    
    def __init__(self):
        self.events = deque(maxlen=10000)
        self.threat_patterns = {
            'brute_force': {'max_attempts': 5, 'time_window': 300},
            'suspicious_login': {'max_attempts': 3, 'time_window': 600},
            'api_abuse': {'max_requests': 1000, 'time_window': 3600}
        }
        self.blocked_ips = set()
        self.suspicious_users = set()
    
    def log_event(self, event: SecurityEvent):
        """Log security event."""
        self.events.append(event)
        logger.warning(f"Security event: {event.event_type} - {event.description}")
        
        # Check for threats
        self._check_threat_patterns(event)
    
    def _check_threat_patterns(self, event: SecurityEvent):
        """Check for threat patterns."""
        if event.event_type == 'failed_login':
            self._check_brute_force(event)
        elif event.event_type == 'api_request':
            self._check_api_abuse(event)
        elif event.event_type == 'suspicious_activity':
            self._check_suspicious_activity(event)
    
    def _check_brute_force(self, event: SecurityEvent):
        """Check for brute force attacks."""
        pattern = self.threat_patterns['brute_force']
        recent_events = [
            e for e in self.events
            if e.event_type == 'failed_login' and
            e.ip_address == event.ip_address and
            (event.timestamp - e.timestamp).total_seconds() <= pattern['time_window']
        ]
        
        if len(recent_events) >= pattern['max_attempts']:
            self.blocked_ips.add(event.ip_address)
            logger.critical(f"Brute force attack detected from {event.ip_address}")
    
    def _check_api_abuse(self, event: SecurityEvent):
        """Check for API abuse."""
        pattern = self.threat_patterns['api_abuse']
        recent_events = [
            e for e in self.events
            if e.event_type == 'api_request' and
            e.ip_address == event.ip_address and
            (event.timestamp - e.timestamp).total_seconds() <= pattern['time_window']
        ]
        
        if len(recent_events) >= pattern['max_requests']:
            self.blocked_ips.add(event.ip_address)
            logger.critical(f"API abuse detected from {event.ip_address}")
    
    def _check_suspicious_activity(self, event: SecurityEvent):
        """Check for suspicious activity."""
        if event.user_id:
            self.suspicious_users.add(event.user_id)
            logger.warning(f"Suspicious activity from user {event.user_id}")
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if IP is blocked."""
        return ip_address in self.blocked_ips
    
    def is_user_suspicious(self, user_id: str) -> bool:
        """Check if user is suspicious."""
        return user_id in self.suspicious_users

class AdvancedSecurityManager:
    """Main security manager."""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.api_keys: Dict[str, APIKey] = {}
        self.audit_logs: List[AuditLog] = []
        self.encryption_manager = EncryptionManager()
        self.mfa_manager = MFAManager()
        self.rate_limiter = RateLimiter()
        self.security_monitor = SecurityMonitor()
        self.session_tokens: Dict[str, Dict[str, Any]] = {}
        
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
            role=UserRole.ADMIN,
            permissions=[Permission.ADMIN, Permission.MANAGE_USERS, Permission.VIEW_AUDIT]
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
    
    def _generate_token(self, user_id: str, expires_in: int = 3600) -> str:
        """Generate JWT token."""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, 'secret_key', algorithm='HS256')
    
    def _verify_token(self, token: str) -> Optional[str]:
        """Verify JWT token."""
        try:
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def register_user(self, username: str, email: str, password: str, 
                     role: UserRole = UserRole.VIEWER) -> Dict[str, Any]:
        """Register new user."""
        try:
            # Check if user already exists
            if any(u.username == username or u.email == email for u in self.users.values()):
                return {'status': 'error', 'message': 'User already exists'}
            
            # Create user
            user_id = secrets.token_urlsafe(16)
            password_hash = self._hash_password(password)
            
            # Set default permissions based on role
            permissions = self._get_default_permissions(role)
            
            user = User(
                user_id=user_id,
                username=username,
                email=email,
                password_hash=password_hash,
                role=role,
                permissions=permissions
            )
            
            self.users[user_id] = user
            
            # Log audit event
            self._log_audit_event(user_id, 'user_registration', 'user', 'success')
            
            logger.info(f"User {username} registered successfully")
            return {'status': 'success', 'user_id': user_id, 'message': 'User registered successfully'}
            
        except Exception as e:
            logger.error(f"User registration failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def authenticate_user(self, username: str, password: str, 
                         mfa_code: Optional[str] = None, 
                         ip_address: str = "unknown") -> Dict[str, Any]:
        """Authenticate user."""
        try:
            # Find user
            user = None
            for u in self.users.values():
                if u.username == username:
                    user = u
                    break
            
            if not user:
                self._log_security_event(None, 'failed_login', ThreatLevel.MEDIUM, 
                                       f"Login attempt with non-existent username: {username}", 
                                       ip_address, "unknown")
                return {'status': 'error', 'message': 'Invalid credentials'}
            
            # Check if user is locked
            if user.locked_until and user.locked_until > datetime.now():
                self._log_security_event(user.user_id, 'failed_login', ThreatLevel.HIGH,
                                       f"Login attempt on locked account: {username}",
                                       ip_address, "unknown")
                return {'status': 'error', 'message': 'Account is locked'}
            
            # Check if IP is blocked
            if self.security_monitor.is_ip_blocked(ip_address):
                self._log_security_event(user.user_id, 'blocked_ip_access', ThreatLevel.CRITICAL,
                                       f"Login attempt from blocked IP: {ip_address}",
                                       ip_address, "unknown")
                return {'status': 'error', 'message': 'IP address is blocked'}
            
            # Verify password
            if not self._verify_password(password, user.password_hash):
                user.failed_attempts += 1
                if user.failed_attempts >= 5:
                    user.locked_until = datetime.now() + timedelta(minutes=30)
                
                self._log_security_event(user.user_id, 'failed_login', ThreatLevel.MEDIUM,
                                       f"Invalid password for user: {username}",
                                       ip_address, "unknown")
                return {'status': 'error', 'message': 'Invalid credentials'}
            
            # Check MFA if enabled
            if user.mfa_enabled:
                if not mfa_code:
                    return {'status': 'error', 'message': 'MFA code required'}
                
                if not self.mfa_manager.verify_totp(user.mfa_secret, mfa_code):
                    self._log_security_event(user.user_id, 'failed_mfa', ThreatLevel.HIGH,
                                           f"Invalid MFA code for user: {username}",
                                           ip_address, "unknown")
                    return {'status': 'error', 'message': 'Invalid MFA code'}
            
            # Reset failed attempts
            user.failed_attempts = 0
            user.locked_until = None
            user.last_login = datetime.now()
            
            # Generate token
            token = self._generate_token(user.user_id)
            self.session_tokens[token] = {
                'user_id': user.user_id,
                'created_at': datetime.now(),
                'last_activity': datetime.now()
            }
            
            # Log successful login
            self._log_audit_event(user.user_id, 'login', 'authentication', 'success')
            self._log_security_event(user.user_id, 'successful_login', ThreatLevel.LOW,
                                   f"Successful login for user: {username}",
                                   ip_address, "unknown")
            
            logger.info(f"User {username} authenticated successfully")
            return {
                'status': 'success',
                'token': token,
                'user_id': user.user_id,
                'role': user.role.value,
                'permissions': [p.value for p in user.permissions]
            }
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def enable_mfa(self, user_id: str, password: str) -> Dict[str, Any]:
        """Enable MFA for user."""
        try:
            user = self.users.get(user_id)
            if not user:
                return {'status': 'error', 'message': 'User not found'}
            
            if not self._verify_password(password, user.password_hash):
                return {'status': 'error', 'message': 'Invalid password'}
            
            secret = self.mfa_manager.generate_secret()
            user.mfa_enabled = True
            user.mfa_secret = secret
            
            self._log_audit_event(user_id, 'enable_mfa', 'security', 'success')
            
            logger.info(f"MFA enabled for user {user.username}")
            return {
                'status': 'success',
                'secret': secret,
                'qr_code_url': f"otpauth://totp/{user.username}?secret={secret}&issuer=TradingSystem"
            }
            
        except Exception as e:
            logger.error(f"MFA enablement failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def create_api_key(self, user_id: str, permissions: List[Permission], 
                      rate_limit: int = 1000, expires_in_days: Optional[int] = None) -> Dict[str, Any]:
        """Create API key for user."""
        try:
            user = self.users.get(user_id)
            if not user:
                return {'status': 'error', 'message': 'User not found'}
            
            # Check if user has permission to create API keys
            if Permission.ADMIN not in user.permissions:
                return {'status': 'error', 'message': 'Insufficient permissions'}
            
            # Generate API key
            key_id = secrets.token_urlsafe(16)
            key_value = secrets.token_urlsafe(32)
            key_hash = hashlib.sha256(key_value.encode()).hexdigest()
            
            expires_at = None
            if expires_in_days:
                expires_at = datetime.now() + timedelta(days=expires_in_days)
            
            api_key = APIKey(
                key_id=key_id,
                user_id=user_id,
                key_hash=key_hash,
                permissions=permissions,
                rate_limit=rate_limit,
                expires_at=expires_at
            )
            
            self.api_keys[key_id] = api_key
            
            self._log_audit_event(user_id, 'create_api_key', 'api_key', 'success')
            
            logger.info(f"API key created for user {user.username}")
            return {
                'status': 'success',
                'key_id': key_id,
                'key_value': key_value,
                'expires_at': expires_at.isoformat() if expires_at else None
            }
            
        except Exception as e:
            logger.error(f"API key creation failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def verify_api_key(self, key_value: str, required_permission: Permission) -> Dict[str, Any]:
        """Verify API key and check permissions."""
        try:
            key_hash = hashlib.sha256(key_value.encode()).hexdigest()
            
            # Find matching API key
            api_key = None
            for key in self.api_keys.values():
                if key.key_hash == key_hash:
                    api_key = key
                    break
            
            if not api_key:
                return {'status': 'error', 'message': 'Invalid API key'}
            
            # Check expiration
            if api_key.expires_at and api_key.expires_at < datetime.now():
                return {'status': 'error', 'message': 'API key expired'}
            
            # Check permissions
            if required_permission not in api_key.permissions:
                return {'status': 'error', 'message': 'Insufficient permissions'}
            
            # Update last used
            api_key.last_used = datetime.now()
            
            return {
                'status': 'success',
                'user_id': api_key.user_id,
                'permissions': [p.value for p in api_key.permissions]
            }
            
        except Exception as e:
            logger.error(f"API key verification failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if user has permission."""
        user = self.users.get(user_id)
        if not user:
            return False
        
        return permission in user.permissions
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data."""
        return self.encryption_manager.encrypt_symmetric(data)
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        return self.encryption_manager.decrypt_symmetric(encrypted_data)
    
    def _get_default_permissions(self, role: UserRole) -> List[Permission]:
        """Get default permissions for role."""
        permissions_map = {
            UserRole.ADMIN: [Permission.ADMIN, Permission.MANAGE_USERS, Permission.VIEW_AUDIT],
            UserRole.TRADER: [Permission.READ, Permission.WRITE, Permission.TRADE],
            UserRole.ANALYST: [Permission.READ, Permission.WRITE],
            UserRole.VIEWER: [Permission.READ],
            UserRole.AUDITOR: [Permission.READ, Permission.VIEW_AUDIT]
        }
        return permissions_map.get(role, [Permission.READ])
    
    def _log_audit_event(self, user_id: Optional[str], action: str, resource: str, result: str):
        """Log audit event."""
        audit_log = AuditLog(
            log_id=secrets.token_urlsafe(16),
            user_id=user_id,
            action=action,
            resource=resource,
            result=result,
            ip_address="system",
            timestamp=datetime.now()
        )
        self.audit_logs.append(audit_log)
    
    def _log_security_event(self, user_id: Optional[str], event_type: str, 
                           threat_level: ThreatLevel, description: str, 
                           ip_address: str, user_agent: str):
        """Log security event."""
        event = SecurityEvent(
            event_id=secrets.token_urlsafe(16),
            user_id=user_id,
            event_type=event_type,
            threat_level=threat_level,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.now()
        )
        self.security_monitor.log_event(event)
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get security summary."""
        return {
            'total_users': len(self.users),
            'total_api_keys': len(self.api_keys),
            'active_sessions': len(self.session_tokens),
            'blocked_ips': len(self.security_monitor.blocked_ips),
            'suspicious_users': len(self.security_monitor.suspicious_users),
            'recent_events': len([e for e in self.security_monitor.events 
                                if (datetime.now() - e.timestamp).total_seconds() <= 3600]),
            'audit_logs_count': len(self.audit_logs)
        }
    
    def get_audit_logs(self, user_id: Optional[str] = None, 
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get audit logs."""
        logs = self.audit_logs
        
        if user_id:
            logs = [log for log in logs if log.user_id == user_id]
        
        if start_date:
            logs = [log for log in logs if log.timestamp >= start_date]
        
        if end_date:
            logs = [log for log in logs if log.timestamp <= end_date]
        
        return [
            {
                'log_id': log.log_id,
                'user_id': log.user_id,
                'action': log.action,
                'resource': log.resource,
                'result': log.result,
                'ip_address': log.ip_address,
                'timestamp': log.timestamp.isoformat(),
                'metadata': log.metadata
            }
            for log in logs
        ]

# Example usage and testing
if __name__ == "__main__":
    # Create security manager
    security_manager = AdvancedSecurityManager()
    
    # Test user registration
    print("Testing user registration...")
    result = security_manager.register_user("testuser", "test@example.com", "password123", UserRole.TRADER)
    print(f"Registration result: {result}")
    
    # Test authentication
    print("\nTesting authentication...")
    auth_result = security_manager.authenticate_user("testuser", "password123", ip_address="192.168.1.1")
    print(f"Authentication result: {auth_result}")
    
    # Test MFA setup
    if auth_result['status'] == 'success':
        user_id = auth_result['user_id']
        print("\nTesting MFA setup...")
        mfa_result = security_manager.enable_mfa(user_id, "password123")
        print(f"MFA setup result: {mfa_result}")
    
    # Test API key creation
    print("\nTesting API key creation...")
    api_result = security_manager.create_api_key("admin", [Permission.READ, Permission.WRITE])
    print(f"API key creation result: {api_result}")
    
    # Test security summary
    print("\nSecurity summary:")
    summary = security_manager.get_security_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\nAdvanced Security Manager initialized successfully!")
