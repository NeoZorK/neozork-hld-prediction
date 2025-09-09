"""
Authentication module for Pocket Hedge Fund.

This module provides authentication, authorization, and security
functionality for the Pocket Hedge Fund system.
"""

__version__ = "1.0.0"
__author__ = "NeoZork Team"

# Import authentication components
from .auth_manager import AuthManager
from .jwt_handler import JWTHandler
from .password_manager import PasswordManager
from .permissions import PermissionManager
from .middleware import AuthMiddleware

__all__ = [
    "AuthManager",
    "JWTHandler", 
    "PasswordManager",
    "PermissionManager",
    "AuthMiddleware"
]
