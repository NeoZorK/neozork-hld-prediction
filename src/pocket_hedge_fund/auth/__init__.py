"""
Authentication module for Pocket Hedge Fund.

This module provides authentication, authorization, and security
functionality for the Pocket Hedge Fund system.
"""

__version__ = "1.0.0"
__author__ = "NeoZork Team"

# Import authentication components
from .auth_manager import AuthenticationManager, get_auth_manager

__all__ = [
    "AuthenticationManager",
    "get_auth_manager"
]
