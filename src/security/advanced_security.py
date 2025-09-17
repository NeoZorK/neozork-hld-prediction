"""
Advanced Security Module for NeoZork Trading System

This module provides enterprise-level security features including:
- Multi-Factor Authentication (MFA)
- Role-Based Access Control (RBAC)
- Advanced Encryption
- Security Monitoring
- Audit Logging
"""

import asyncio
import hashlib
import hmac
import json
import logging
import secrets
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import base64
import pyotp
import qrcode
from io import BytesIO

logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AuthenticationMethod(Enum):
    """Authentication method enumeration"""
    PASSWORD = "password"
    TOTP = "totp"
    SMS = "sms"
    EMAIL = "email"
    BIOMETRIC = "biometric"

class UserRole(Enum):
    """User role enumeration"""
    ADMIN = "admin"
    TRADER = "trader"
    ANALYST = "analyst"
    VIEWER = "viewer"
    AUDITOR = "auditor"

class Permission(Enum):
    """Permission enumeration"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"

class SecurityEvent(Enum):
    """Security event enumeration"""
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    MFA_SUCCESS = "mfa_success"
    MFA_FAILED = "mfa_failed"
    PERMISSION_DENIED = "permission_denied"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    DATA_ACCESS = "data_access"
    SYSTEM_CHANGE = "system_change"

class AdvancedSecurityManager:
    """Advanced Security Manager for enterprise-level security"""
    
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.security_events = []
        self.failed_attempts = {}
        self.locked_accounts = set()
        self.encryption_keys = {}
        self.mfa_secrets = {}
        self.role_permissions = self._initialize_role_permissions()
        self.security_policies = self._initialize_security_policies()
        
    def _initialize_role_permissions(self) -> Dict[UserRole, List[Permission]]:
        """Initialize role-based permissions"""
        return {
            UserRole.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.EXECUTE, Permission.ADMIN],
            UserRole.TRADER: [Permission.READ, Permission.WRITE, Permission.EXECUTE],
            UserRole.ANALYST: [Permission.READ, Permission.WRITE],
            UserRole.VIEWER: [Permission.READ],
            UserRole.AUDITOR: [Permission.READ, Permission.EXECUTE]
        }
    
    def _initialize_security_policies(self) -> Dict[str, Any]:
        """Initialize security policies"""
        return {
            "password_policy": {
                "min_length": 12,
                "require_uppercase": True,
                "require_lowercase": True,
                "require_numbers": True,
                "require_special": True,
                "max_age_days": 90
            },
            "mfa_policy": {
                "required_for_admin": True,
                "required_for_trader": True,
                "backup_codes_count": 10
            },
            "session_policy": {
                "timeout_minutes": 30,
                "max_concurrent_sessions": 3
            },
            "lockout_policy": {
                "max_failed_attempts": 5,
                "lockout_duration_minutes": 30
            }
        }
    
    async def create_user(self, username: str, email: str, role: UserRole, 
                         password: str, require_mfa: bool = True) -> Dict[str, Any]:
        """Create a new user with security settings"""
        try:
            # Validate password strength
            if not self._validate_password_strength(password):
                return {
                    "status": "error",
                    "message": "Password does not meet security requirements"
                }
            
            # Generate user ID and salt
            user_id = secrets.token_hex(16)
            salt = secrets.token_hex(32)
            
            # Hash password
            password_hash = self._hash_password(password, salt)
            
            # Generate MFA secret if required
            mfa_secret = None
            if require_mfa:
                mfa_secret = pyotp.random_base32()
                self.mfa_secrets[user_id] = mfa_secret
            
            # Create user record
            user = {
                "user_id": user_id,
                "username": username,
                "email": email,
                "role": role,
                "password_hash": password_hash,
                "salt": salt,
                "mfa_enabled": require_mfa,
                "mfa_secret": mfa_secret,
                "created_at": datetime.now(datetime.UTC),
                "last_login": None,
                "failed_attempts": 0,
                "locked_until": None,
                "permissions": self.role_permissions.get(role, [])
            }
            
            self.users[user_id] = user
            
            # Log security event
            await self._log_security_event(
                SecurityEvent.SYSTEM_CHANGE,
                f"User created: {username}",
                user_id=user_id,
                security_level=SecurityLevel.MEDIUM
            )
            
            return {
                "status": "success",
                "user_id": user_id,
                "mfa_secret": mfa_secret,
                "message": "User created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return {
                "status": "error",
                "message": f"Failed to create user: {str(e)}"
            }
    
    async def authenticate_user(self, username: str, password: str, 
                               mfa_code: Optional[str] = None) -> Dict[str, Any]:
        """Authenticate user with optional MFA"""
        try:
            # Find user by username
            user = None
            for u in self.users.values():
                if u["username"] == username:
                    user = u
                    break
            
            if not user:
                await self._log_security_event(
                    SecurityEvent.LOGIN_FAILED,
                    f"Login attempt with unknown username: {username}",
                    security_level=SecurityLevel.MEDIUM
                )
                return {
                    "status": "error",
                    "message": "Invalid credentials"
                }
            
            # Check if account is locked
            if user["user_id"] in self.locked_accounts:
                if user["locked_until"] and datetime.now(datetime.UTC) < user["locked_until"]:
                    return {
                        "status": "error",
                        "message": "Account is temporarily locked"
                    }
                else:
                    # Unlock account
                    self.locked_accounts.discard(user["user_id"])
                    user["locked_until"] = None
            
            # Verify password
            if not self._verify_password(password, user["password_hash"], user["salt"]):
                user["failed_attempts"] += 1
                
                # Check lockout policy
                if user["failed_attempts"] >= self.security_policies["lockout_policy"]["max_failed_attempts"]:
                    lockout_duration = timedelta(minutes=self.security_policies["lockout_policy"]["lockout_duration_minutes"])
                    user["locked_until"] = datetime.now(datetime.UTC) + lockout_duration
                    self.locked_accounts.add(user["user_id"])
                    
                    await self._log_security_event(
                        SecurityEvent.SUSPICIOUS_ACTIVITY,
                        f"Account locked due to failed login attempts: {username}",
                        user_id=user["user_id"],
                        security_level=SecurityLevel.HIGH
                    )
                
                await self._log_security_event(
                    SecurityEvent.LOGIN_FAILED,
                    f"Failed login attempt: {username}",
                    user_id=user["user_id"],
                    security_level=SecurityLevel.MEDIUM
                )
                
                return {
                    "status": "error",
                    "message": "Invalid credentials"
                }
            
            # Reset failed attempts on successful password verification
            user["failed_attempts"] = 0
            
            # Check MFA if enabled
            if user["mfa_enabled"]:
                if not mfa_code:
                    return {
                        "status": "mfa_required",
                        "message": "MFA code required"
                    }
                
                if not self._verify_mfa_code(user["mfa_secret"], mfa_code):
                    await self._log_security_event(
                        SecurityEvent.MFA_FAILED,
                        f"Failed MFA attempt: {username}",
                        user_id=user["user_id"],
                        security_level=SecurityLevel.MEDIUM
                    )
                    return {
                        "status": "error",
                        "message": "Invalid MFA code"
                    }
                
                await self._log_security_event(
                    SecurityEvent.MFA_SUCCESS,
                    f"Successful MFA: {username}",
                    user_id=user["user_id"],
                    security_level=SecurityLevel.LOW
                )
            
            # Create session
            session_token = self._generate_session_token()
            session = {
                "session_id": session_token,
                "user_id": user["user_id"],
                "created_at": datetime.now(datetime.UTC),
                "last_activity": datetime.now(datetime.UTC),
                "expires_at": datetime.now(datetime.UTC) + timedelta(minutes=self.security_policies["session_policy"]["timeout_minutes"])
            }
            
            self.sessions[session_token] = session
            user["last_login"] = datetime.now(datetime.UTC)
            
            await self._log_security_event(
                SecurityEvent.LOGIN_SUCCESS,
                f"Successful login: {username}",
                user_id=user["user_id"],
                security_level=SecurityLevel.LOW
            )
            
            return {
                "status": "success",
                "session_token": session_token,
                "user": {
                    "user_id": user["user_id"],
                    "username": user["username"],
                    "role": user["role"].value,
                    "permissions": [p.value for p in user["permissions"]]
                },
                "message": "Authentication successful"
            }
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return {
                "status": "error",
                "message": f"Authentication failed: {str(e)}"
            }
    
    async def check_permission(self, session_token: str, permission: Permission) -> bool:
        """Check if user has specific permission"""
        try:
            session = self.sessions.get(session_token)
            if not session:
                return False
            
            # Check session expiry
            if datetime.now(datetime.UTC) > session["expires_at"]:
                del self.sessions[session_token]
                return False
            
            # Update last activity
            session["last_activity"] = datetime.now(datetime.UTC)
            
            # Get user
            user = self.users.get(session["user_id"])
            if not user:
                return False
            
            # Check permission
            return permission in user["permissions"]
            
        except Exception as e:
            logger.error(f"Error checking permission: {e}")
            return False
    
    async def generate_mfa_qr_code(self, user_id: str) -> Dict[str, Any]:
        """Generate QR code for MFA setup"""
        try:
            user = self.users.get(user_id)
            if not user or not user["mfa_enabled"]:
                return {
                    "status": "error",
                    "message": "User not found or MFA not enabled"
                }
            
            # Generate TOTP URI
            totp_uri = pyotp.totp.TOTP(user["mfa_secret"]).provisioning_uri(
                name=user["username"],
                issuer_name="NeoZork Trading System"
            )
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(totp_uri)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return {
                "status": "success",
                "qr_code": img_str,
                "secret": user["mfa_secret"],
                "message": "QR code generated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error generating MFA QR code: {e}")
            return {
                "status": "error",
                "message": f"Failed to generate QR code: {str(e)}"
            }
    
    async def encrypt_data(self, data: str, key_id: str) -> Dict[str, Any]:
        """Encrypt sensitive data"""
        try:
            # Generate encryption key if not exists
            if key_id not in self.encryption_keys:
                self.encryption_keys[key_id] = secrets.token_hex(32)
            
            # Simple encryption (in production, use proper encryption library)
            key = self.encryption_keys[key_id]
            encrypted_data = self._simple_encrypt(data, key)
            
            return {
                "status": "success",
                "encrypted_data": encrypted_data,
                "key_id": key_id,
                "message": "Data encrypted successfully"
            }
            
        except Exception as e:
            logger.error(f"Error encrypting data: {e}")
            return {
                "status": "error",
                "message": f"Encryption failed: {str(e)}"
            }
    
    async def decrypt_data(self, encrypted_data: str, key_id: str) -> Dict[str, Any]:
        """Decrypt sensitive data"""
        try:
            if key_id not in self.encryption_keys:
                return {
                    "status": "error",
                    "message": "Encryption key not found"
                }
            
            key = self.encryption_keys[key_id]
            decrypted_data = self._simple_decrypt(encrypted_data, key)
            
            return {
                "status": "success",
                "decrypted_data": decrypted_data,
                "message": "Data decrypted successfully"
            }
            
        except Exception as e:
            logger.error(f"Error decrypting data: {e}")
            return {
                "status": "error",
                "message": f"Decryption failed: {str(e)}"
            }
    
    async def get_security_events(self, user_id: Optional[str] = None, 
                                 event_type: Optional[SecurityEvent] = None,
                                 limit: int = 100) -> Dict[str, Any]:
        """Get security events with filtering"""
        try:
            events = self.security_events.copy()
            
            # Filter by user
            if user_id:
                events = [e for e in events if e.get("user_id") == user_id]
            
            # Filter by event type
            if event_type:
                events = [e for e in events if e.get("event_type") == event_type]
            
            # Sort by timestamp (newest first)
            events.sort(key=lambda x: x.get("timestamp", datetime.min), reverse=True)
            
            # Limit results
            events = events[:limit]
            
            return {
                "status": "success",
                "events": events,
                "total_count": len(events),
                "message": "Security events retrieved successfully"
            }
            
        except Exception as e:
            logger.error(f"Error getting security events: {e}")
            return {
                "status": "error",
                "message": f"Failed to get security events: {str(e)}"
            }
    
    async def get_security_dashboard(self) -> Dict[str, Any]:
        """Get security dashboard data"""
        try:
            # Calculate security metrics
            total_users = len(self.users)
            active_sessions = len([s for s in self.sessions.values() 
                                 if datetime.now(datetime.UTC) < s["expires_at"]])
            locked_accounts = len(self.locked_accounts)
            
            # Recent security events
            recent_events = self.security_events[-10:] if self.security_events else []
            
            # Failed login attempts in last 24 hours
            last_24h = datetime.now(datetime.UTC) - timedelta(hours=24)
            failed_logins = len([e for e in self.security_events 
                               if e.get("event_type") == SecurityEvent.LOGIN_FAILED 
                               and e.get("timestamp", datetime.min) > last_24h])
            
            return {
                "status": "success",
                "dashboard": {
                    "total_users": total_users,
                    "active_sessions": active_sessions,
                    "locked_accounts": locked_accounts,
                    "failed_logins_24h": failed_logins,
                    "recent_events": recent_events,
                    "security_level": "HIGH" if locked_accounts > 0 or failed_logins > 10 else "MEDIUM"
                },
                "message": "Security dashboard data retrieved successfully"
            }
            
        except Exception as e:
            logger.error(f"Error getting security dashboard: {e}")
            return {
                "status": "error",
                "message": f"Failed to get security dashboard: {str(e)}"
            }
    
    def _validate_password_strength(self, password: str) -> bool:
        """Validate password strength against policy"""
        policy = self.security_policies["password_policy"]
        
        if len(password) < policy["min_length"]:
            return False
        
        if policy["require_uppercase"] and not any(c.isupper() for c in password):
            return False
        
        if policy["require_lowercase"] and not any(c.islower() for c in password):
            return False
        
        if policy["require_numbers"] and not any(c.isdigit() for c in password):
            return False
        
        if policy["require_special"] and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False
        
        return True
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Hash password with salt"""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def _verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password, salt) == password_hash
    
    def _verify_mfa_code(self, secret: str, code: str) -> bool:
        """Verify MFA TOTP code"""
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(code, valid_window=1)
        except Exception:
            return False
    
    def _generate_session_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    def _simple_encrypt(self, data: str, key: str) -> str:
        """Simple encryption (for demonstration - use proper encryption in production)"""
        # This is a simplified encryption - use proper encryption libraries in production
        return base64.b64encode(data.encode()).decode()
    
    def _simple_decrypt(self, encrypted_data: str, key: str) -> str:
        """Simple decryption (for demonstration - use proper decryption in production)"""
        # This is a simplified decryption - use proper decryption libraries in production
        return base64.b64decode(encrypted_data.encode()).decode()
    
    async def _log_security_event(self, event_type: SecurityEvent, description: str,
                                 user_id: Optional[str] = None, 
                                 security_level: SecurityLevel = SecurityLevel.MEDIUM):
        """Log security event"""
        event = {
            "event_id": secrets.token_hex(8),
            "event_type": event_type.value,
            "description": description,
            "user_id": user_id,
            "security_level": security_level.value,
            "timestamp": datetime.now(datetime.UTC),
            "ip_address": "127.0.0.1",  # In production, get real IP
            "user_agent": "NeoZork-System"  # In production, get real user agent
        }
        
        self.security_events.append(event)
        
        # Keep only last 1000 events
        if len(self.security_events) > 1000:
            self.security_events = self.security_events[-1000:]

# Example usage and testing
async def main():
    """Example usage of Advanced Security Manager"""
    security_manager = AdvancedSecurityManager()
    
    # Create test user
    result = await security_manager.create_user(
        username="testuser",
        email="test@example.com",
        role=UserRole.TRADER,
        password="SecurePass123!",
        require_mfa=True
    )
    print(f"User creation: {result}")
    
    if result["status"] == "success":
        user_id = result["user_id"]
        
        # Generate MFA QR code
        qr_result = await security_manager.generate_mfa_qr_code(user_id)
        print(f"MFA QR code: {qr_result['status']}")
        
        # Authenticate user
        auth_result = await security_manager.authenticate_user(
            username="testuser",
            password="SecurePass123!",
            mfa_code="123456"  # This would be a real TOTP code
        )
        print(f"Authentication: {auth_result}")
        
        # Get security dashboard
        dashboard = await security_manager.get_security_dashboard()
        print(f"Security dashboard: {dashboard}")

if __name__ == "__main__":
    asyncio.run(main())