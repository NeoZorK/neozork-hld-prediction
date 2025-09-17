# -*- coding: utf-8 -*-
"""
Access Control for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive access control and authentication capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
import hashlib
import secrets
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import warnings

class UserRole(Enum):
    """User role enumeration."""
    ADMIN = "admin"
    TRADER = "trader"
    ANALYST = "analyst"
    VIEWER = "viewer"
    AUDITOR = "auditor"

class Permission(Enum):
    """Permission enumeration."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"

class AccessControl:
    """
    Access control system for user authentication and authorization.
    
    Features:
    - User Management
    - Role-based Access Control (RBAC)
    - Permission Management
    - Session Management
    - Multi-factor Authentication
    - Audit Logging
    """
    
    def __init__(self):
        """Initialize the Access Control system."""
        self.users = {}
        self.roles = {}
        self.permissions = {}
        self.sessions = {}
        self.audit_log = []
        self.mfa_tokens = {}
        self.failed_attempts = {}
    
    def create_user(self, username: str, email: str, password: str, 
                   role: str = UserRole.VIEWER.value) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            username: Username
            email: Email address
            password: Password (will be hashed)
            role: User role
            
        Returns:
            User creation result
        """
        try:
            # Validate role
            valid_roles = [r.value for r in UserRole]
            if role not in valid_roles:
                return {"status": "error", "message": f"Invalid role: {role}"}
            
            # Check if user already exists
            if username in self.users:
                return {"status": "error", "message": f"User {username} already exists"}
            
            # Hash password
            password_hash = self._hash_password(password)
            
            # Generate user ID
            user_id = f"user_{int(time.time())}"
            
            # Create user
            user = {
                "user_id": user_id,
                "username": username,
                "email": email,
                "password_hash": password_hash,
                "role": role,
                "is_active": True,
                "created_time": time.time(),
                "last_login": None,
                "failed_attempts": 0,
                "locked_until": None,
                "mfa_enabled": False,
                "mfa_secret": None
            }
            
            # Store user
            self.users[username] = user
            
            # Log audit event
            self._log_audit_event("user_created", username, {"role": role})
            
            result = {
                "status": "success",
                "user_id": user_id,
                "username": username,
                "email": email,
                "role": role,
                "message": "User created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create user: {str(e)}"}
    
    def authenticate_user(self, username: str, password: str, 
                         mfa_token: str = None) -> Dict[str, Any]:
        """
        Authenticate a user.
        
        Args:
            username: Username
            password: Password
            mfa_token: Multi-factor authentication token
            
        Returns:
            Authentication result
        """
        try:
            # Check if user exists
            if username not in self.users:
                self._log_failed_attempt(username, "user_not_found")
                return {"status": "error", "message": "Invalid credentials"}
            
            user = self.users[username]
            
            # Check if user is active
            if not user["is_active"]:
                return {"status": "error", "message": "User account is disabled"}
            
            # Check if account is locked
            if user["locked_until"] and time.time() < user["locked_until"]:
                return {"status": "error", "message": "Account is temporarily locked"}
            
            # Verify password
            if not self._verify_password(password, user["password_hash"]):
                self._log_failed_attempt(username, "invalid_password")
                user["failed_attempts"] += 1
                
                # Lock account after 5 failed attempts
                if user["failed_attempts"] >= 5:
                    user["locked_until"] = time.time() + 3600  # Lock for 1 hour
                    self._log_audit_event("account_locked", username, {"reason": "too_many_failed_attempts"})
                
                return {"status": "error", "message": "Invalid credentials"}
            
            # Check MFA if enabled
            if user["mfa_enabled"]:
                if not mfa_token:
                    return {"status": "error", "message": "MFA token required"}
                
                if not self._verify_mfa_token(username, mfa_token):
                    self._log_failed_attempt(username, "invalid_mfa_token")
                    return {"status": "error", "message": "Invalid MFA token"}
            
            # Reset failed attempts
            user["failed_attempts"] = 0
            user["locked_until"] = None
            user["last_login"] = time.time()
            
            # Create session
            session_id = self._create_session(username)
            
            # Log successful authentication
            self._log_audit_event("user_authenticated", username, {"session_id": session_id})
            
            result = {
                "status": "success",
                "user_id": user["user_id"],
                "username": username,
                "role": user["role"],
                "session_id": session_id,
                "mfa_required": user["mfa_enabled"],
                "message": "Authentication successful"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Authentication failed: {str(e)}"}
    
    def create_role(self, role_name: str, permissions: List[str], 
                   description: str = "") -> Dict[str, Any]:
        """
        Create a new role.
        
        Args:
            role_name: Name of the role
            permissions: List of permissions
            description: Role description
            
        Returns:
            Role creation result
        """
        try:
            # Validate permissions
            valid_permissions = [p.value for p in Permission]
            invalid_permissions = [p for p in permissions if p not in valid_permissions]
            if invalid_permissions:
                return {"status": "error", "message": f"Invalid permissions: {invalid_permissions}"}
            
            # Check if role already exists
            if role_name in self.roles:
                return {"status": "error", "message": f"Role {role_name} already exists"}
            
            # Generate role ID
            role_id = f"role_{int(time.time())}"
            
            # Create role
            role = {
                "role_id": role_id,
                "role_name": role_name,
                "permissions": permissions,
                "description": description,
                "created_time": time.time(),
                "created_by": "system"
            }
            
            # Store role
            self.roles[role_name] = role
            
            # Log audit event
            self._log_audit_event("role_created", "system", {"role_name": role_name, "permissions": permissions})
            
            result = {
                "status": "success",
                "role_id": role_id,
                "role_name": role_name,
                "permissions": permissions,
                "description": description,
                "message": "Role created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create role: {str(e)}"}
    
    def assign_role(self, username: str, role_name: str, 
                   assigned_by: str = "admin") -> Dict[str, Any]:
        """
        Assign a role to a user.
        
        Args:
            username: Username
            role_name: Role name
            assigned_by: User who assigned the role
            
        Returns:
            Role assignment result
        """
        try:
            # Check if user exists
            if username not in self.users:
                return {"status": "error", "message": f"User {username} not found"}
            
            # Check if role exists
            if role_name not in self.roles:
                return {"status": "error", "message": f"Role {role_name} not found"}
            
            # Update user role
            old_role = self.users[username]["role"]
            self.users[username]["role"] = role_name
            
            # Log audit event
            self._log_audit_event("role_assigned", assigned_by, {
                "username": username,
                "old_role": old_role,
                "new_role": role_name
            })
            
            result = {
                "status": "success",
                "username": username,
                "old_role": old_role,
                "new_role": role_name,
                "assigned_by": assigned_by,
                "message": "Role assigned successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to assign role: {str(e)}"}
    
    def check_permission(self, username: str, resource: str, 
                        permission: str) -> Dict[str, Any]:
        """
        Check if a user has permission to access a resource.
        
        Args:
            username: Username
            resource: Resource name
            permission: Permission type
            
        Returns:
            Permission check result
        """
        try:
            # Check if user exists
            if username not in self.users:
                return {"status": "error", "message": f"User {username} not found"}
            
            user = self.users[username]
            
            # Check if user is active
            if not user["is_active"]:
                return {"status": "error", "message": "User account is disabled"}
            
            # Get user role
            role_name = user["role"]
            
            # Check if role exists
            if role_name not in self.roles:
                return {"status": "error", "message": f"Role {role_name} not found"}
            
            role = self.roles[role_name]
            
            # Check if role has permission
            has_permission = permission in role["permissions"]
            
            # Log permission check
            self._log_audit_event("permission_checked", username, {
                "resource": resource,
                "permission": permission,
                "granted": has_permission
            })
            
            result = {
                "status": "success",
                "username": username,
                "role": role_name,
                "resource": resource,
                "permission": permission,
                "granted": has_permission,
                "message": "Permission granted" if has_permission else "Permission denied"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to check permission: {str(e)}"}
    
    def enable_mfa(self, username: str, mfa_secret: str = None) -> Dict[str, Any]:
        """
        Enable multi-factor authentication for a user.
        
        Args:
            username: Username
            mfa_secret: MFA secret (if None, will be generated)
            
        Returns:
            MFA enablement result
        """
        try:
            # Check if user exists
            if username not in self.users:
                return {"status": "error", "message": f"User {username} not found"}
            
            user = self.users[username]
            
            # Generate MFA secret if not provided
            if mfa_secret is None:
                mfa_secret = self._generate_mfa_secret()
            
            # Enable MFA
            user["mfa_enabled"] = True
            user["mfa_secret"] = mfa_secret
            
            # Store MFA token
            self.mfa_tokens[username] = {
                "secret": mfa_secret,
                "created_time": time.time()
            }
            
            # Log audit event
            self._log_audit_event("mfa_enabled", username, {"mfa_secret": mfa_secret[:8] + "..."})
            
            result = {
                "status": "success",
                "username": username,
                "mfa_secret": mfa_secret,
                "qr_code": f"otpauth://totp/{username}?secret={mfa_secret}&issuer=NeoZork",
                "message": "MFA enabled successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to enable MFA: {str(e)}"}
    
    def disable_mfa(self, username: str) -> Dict[str, Any]:
        """
        Disable multi-factor authentication for a user.
        
        Args:
            username: Username
            
        Returns:
            MFA disablement result
        """
        try:
            # Check if user exists
            if username not in self.users:
                return {"status": "error", "message": f"User {username} not found"}
            
            user = self.users[username]
            
            # Disable MFA
            user["mfa_enabled"] = False
            user["mfa_secret"] = None
            
            # Remove MFA token
            if username in self.mfa_tokens:
                del self.mfa_tokens[username]
            
            # Log audit event
            self._log_audit_event("mfa_disabled", username, {})
            
            result = {
                "status": "success",
                "username": username,
                "message": "MFA disabled successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to disable MFA: {str(e)}"}
    
    def logout_user(self, session_id: str) -> Dict[str, Any]:
        """
        Logout a user session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Logout result
        """
        try:
            # Check if session exists
            if session_id not in self.sessions:
                return {"status": "error", "message": "Invalid session"}
            
            session = self.sessions[session_id]
            username = session["username"]
            
            # Remove session
            del self.sessions[session_id]
            
            # Log audit event
            self._log_audit_event("user_logout", username, {"session_id": session_id})
            
            result = {
                "status": "success",
                "session_id": session_id,
                "username": username,
                "message": "Logout successful"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to logout: {str(e)}"}
    
    def get_user_info(self, username: str) -> Dict[str, Any]:
        """
        Get user information.
        
        Args:
            username: Username
            
        Returns:
            User information result
        """
        try:
            # Check if user exists
            if username not in self.users:
                return {"status": "error", "message": f"User {username} not found"}
            
            user = self.users[username]
            
            # Remove sensitive information
            user_info = {
                "user_id": user["user_id"],
                "username": user["username"],
                "email": user["email"],
                "role": user["role"],
                "is_active": user["is_active"],
                "created_time": user["created_time"],
                "last_login": user["last_login"],
                "mfa_enabled": user["mfa_enabled"]
            }
            
            result = {
                "status": "success",
                "user_info": user_info
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get user info: {str(e)}"}
    
    def get_audit_log(self, limit: int = 100, username: str = None) -> Dict[str, Any]:
        """
        Get audit log entries.
        
        Args:
            limit: Maximum number of entries to return
            username: Filter by username (optional)
            
        Returns:
            Audit log result
        """
        try:
            # Filter audit log
            filtered_log = self.audit_log
            
            if username:
                filtered_log = [entry for entry in filtered_log if entry.get("username") == username]
            
            # Sort by timestamp (newest first)
            filtered_log.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
            
            # Limit results
            limited_log = filtered_log[:limit]
            
            result = {
                "status": "success",
                "audit_log": limited_log,
                "n_entries": len(limited_log),
                "total_entries": len(self.audit_log)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get audit log: {str(e)}"}
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        try:
            salt, hash_part = password_hash.split(":")
            computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return computed_hash == hash_part
        except:
            return False
    
    def _generate_mfa_secret(self) -> str:
        """Generate a random MFA secret."""
        return secrets.token_hex(16)
    
    def _verify_mfa_token(self, username: str, token: str) -> bool:
        """Verify MFA token (simplified implementation)."""
        # In real implementation, this would use TOTP
        # For now, just check if token is 6 digits
        return token.isdigit() and len(token) == 6
    
    def _create_session(self, username: str) -> str:
        """Create a new session for a user."""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            "username": username,
            "created_time": time.time(),
            "last_activity": time.time()
        }
        return session_id
    
    def _log_audit_event(self, event_type: str, username: str, details: Dict[str, Any]) -> None:
        """Log an audit event."""
        audit_entry = {
            "timestamp": time.time(),
            "event_type": event_type,
            "username": username,
            "details": details
        }
        self.audit_log.append(audit_entry)
    
    def _log_failed_attempt(self, username: str, reason: str) -> None:
        """Log a failed authentication attempt."""
        self._log_audit_event("failed_authentication", username, {"reason": reason})
        
        if username not in self.failed_attempts:
            self.failed_attempts[username] = 0
        self.failed_attempts[username] += 1
