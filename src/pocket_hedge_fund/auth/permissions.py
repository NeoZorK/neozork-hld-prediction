"""
Permission system for Pocket Hedge Fund.

This module provides role-based access control (RBAC) and permission
management for the authentication system.
"""

import logging
from typing import Dict, List, Set, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class Permission(Enum):
    """System permissions."""
    # User management
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_LIST = "user:list"
    
    # Fund management
    FUND_CREATE = "fund:create"
    FUND_READ = "fund:read"
    FUND_UPDATE = "fund:update"
    FUND_DELETE = "fund:delete"
    FUND_LIST = "fund:list"
    FUND_MANAGE = "fund:manage"
    
    # Portfolio management
    PORTFOLIO_READ = "portfolio:read"
    PORTFOLIO_UPDATE = "portfolio:update"
    PORTFOLIO_MANAGE = "portfolio:manage"
    
    # Performance tracking
    PERFORMANCE_READ = "performance:read"
    PERFORMANCE_ANALYZE = "performance:analyze"
    
    # Transaction management
    TRANSACTION_CREATE = "transaction:create"
    TRANSACTION_READ = "transaction:read"
    TRANSACTION_UPDATE = "transaction:update"
    TRANSACTION_DELETE = "transaction:delete"
    TRANSACTION_LIST = "transaction:list"
    
    # Strategy management
    STRATEGY_CREATE = "strategy:create"
    STRATEGY_READ = "strategy:read"
    STRATEGY_UPDATE = "strategy:update"
    STRATEGY_DELETE = "strategy:delete"
    STRATEGY_EXECUTE = "strategy:execute"
    
    # Risk management
    RISK_READ = "risk:read"
    RISK_ANALYZE = "risk:analyze"
    RISK_MANAGE = "risk:manage"
    
    # Investment management
    INVESTMENT_CREATE = "investment:create"
    INVESTMENT_READ = "investment:read"
    INVESTMENT_UPDATE = "investment:update"
    INVESTMENT_DELETE = "investment:delete"
    
    # System administration
    SYSTEM_ADMIN = "system:admin"
    SYSTEM_CONFIG = "system:config"
    SYSTEM_MONITOR = "system:monitor"
    
    # Reporting
    REPORT_GENERATE = "report:generate"
    REPORT_VIEW = "report:view"
    REPORT_EXPORT = "report:export"


class Role(Enum):
    """User roles."""
    ADMIN = "admin"
    FUND_MANAGER = "fund_manager"
    INVESTOR = "investor"
    ANALYST = "analyst"
    VIEWER = "viewer"


class PermissionManager:
    """
    Permission manager for Pocket Hedge Fund.
    
    Provides role-based access control and permission management.
    """
    
    def __init__(self):
        """Initialize permission manager."""
        self.role_permissions = self._initialize_role_permissions()
        self.permission_hierarchy = self._initialize_permission_hierarchy()
    
    def _initialize_role_permissions(self) -> Dict[Role, Set[Permission]]:
        """Initialize role-permission mappings."""
        return {
            Role.ADMIN: {
                # Admin has all permissions
                Permission.USER_CREATE,
                Permission.USER_READ,
                Permission.USER_UPDATE,
                Permission.USER_DELETE,
                Permission.USER_LIST,
                Permission.FUND_CREATE,
                Permission.FUND_READ,
                Permission.FUND_UPDATE,
                Permission.FUND_DELETE,
                Permission.FUND_LIST,
                Permission.FUND_MANAGE,
                Permission.PORTFOLIO_READ,
                Permission.PORTFOLIO_UPDATE,
                Permission.PORTFOLIO_MANAGE,
                Permission.PERFORMANCE_READ,
                Permission.PERFORMANCE_ANALYZE,
                Permission.TRANSACTION_CREATE,
                Permission.TRANSACTION_READ,
                Permission.TRANSACTION_UPDATE,
                Permission.TRANSACTION_DELETE,
                Permission.TRANSACTION_LIST,
                Permission.STRATEGY_CREATE,
                Permission.STRATEGY_READ,
                Permission.STRATEGY_UPDATE,
                Permission.STRATEGY_DELETE,
                Permission.STRATEGY_EXECUTE,
                Permission.RISK_READ,
                Permission.RISK_ANALYZE,
                Permission.RISK_MANAGE,
                Permission.INVESTMENT_CREATE,
                Permission.INVESTMENT_READ,
                Permission.INVESTMENT_UPDATE,
                Permission.INVESTMENT_DELETE,
                Permission.SYSTEM_ADMIN,
                Permission.SYSTEM_CONFIG,
                Permission.SYSTEM_MONITOR,
                Permission.REPORT_GENERATE,
                Permission.REPORT_VIEW,
                Permission.REPORT_EXPORT,
            },
            
            Role.FUND_MANAGER: {
                # Fund managers can manage their funds
                Permission.USER_READ,
                Permission.USER_LIST,
                Permission.FUND_CREATE,
                Permission.FUND_READ,
                Permission.FUND_UPDATE,
                Permission.FUND_LIST,
                Permission.FUND_MANAGE,
                Permission.PORTFOLIO_READ,
                Permission.PORTFOLIO_UPDATE,
                Permission.PORTFOLIO_MANAGE,
                Permission.PERFORMANCE_READ,
                Permission.PERFORMANCE_ANALYZE,
                Permission.TRANSACTION_CREATE,
                Permission.TRANSACTION_READ,
                Permission.TRANSACTION_UPDATE,
                Permission.TRANSACTION_LIST,
                Permission.STRATEGY_CREATE,
                Permission.STRATEGY_READ,
                Permission.STRATEGY_UPDATE,
                Permission.STRATEGY_EXECUTE,
                Permission.RISK_READ,
                Permission.RISK_ANALYZE,
                Permission.RISK_MANAGE,
                Permission.INVESTMENT_READ,
                Permission.REPORT_GENERATE,
                Permission.REPORT_VIEW,
                Permission.REPORT_EXPORT,
            },
            
            Role.ANALYST: {
                # Analysts can read and analyze data
                Permission.USER_READ,
                Permission.USER_LIST,
                Permission.FUND_READ,
                Permission.FUND_LIST,
                Permission.PORTFOLIO_READ,
                Permission.PERFORMANCE_READ,
                Permission.PERFORMANCE_ANALYZE,
                Permission.TRANSACTION_READ,
                Permission.TRANSACTION_LIST,
                Permission.STRATEGY_READ,
                Permission.RISK_READ,
                Permission.RISK_ANALYZE,
                Permission.INVESTMENT_READ,
                Permission.REPORT_VIEW,
                Permission.REPORT_EXPORT,
            },
            
            Role.INVESTOR: {
                # Investors can view their investments
                Permission.USER_READ,
                Permission.USER_UPDATE,  # Update their own profile
                Permission.FUND_READ,
                Permission.FUND_LIST,
                Permission.PORTFOLIO_READ,
                Permission.PERFORMANCE_READ,
                Permission.TRANSACTION_READ,
                Permission.INVESTMENT_CREATE,
                Permission.INVESTMENT_READ,
                Permission.INVESTMENT_UPDATE,
                Permission.REPORT_VIEW,
            },
            
            Role.VIEWER: {
                # Viewers have read-only access
                Permission.USER_READ,
                Permission.FUND_READ,
                Permission.FUND_LIST,
                Permission.PORTFOLIO_READ,
                Permission.PERFORMANCE_READ,
                Permission.TRANSACTION_READ,
                Permission.STRATEGY_READ,
                Permission.RISK_READ,
                Permission.INVESTMENT_READ,
                Permission.REPORT_VIEW,
            }
        }
    
    def _initialize_permission_hierarchy(self) -> Dict[Permission, Set[Permission]]:
        """Initialize permission hierarchy (permissions that include others)."""
        return {
            Permission.FUND_MANAGE: {
                Permission.FUND_READ,
                Permission.FUND_UPDATE,
                Permission.PORTFOLIO_MANAGE,
                Permission.STRATEGY_EXECUTE,
                Permission.RISK_MANAGE,
            },
            Permission.PORTFOLIO_MANAGE: {
                Permission.PORTFOLIO_READ,
                Permission.PORTFOLIO_UPDATE,
                Permission.TRANSACTION_CREATE,
                Permission.TRANSACTION_UPDATE,
            },
            Permission.RISK_MANAGE: {
                Permission.RISK_READ,
                Permission.RISK_ANALYZE,
            },
            Permission.SYSTEM_ADMIN: {
                Permission.SYSTEM_CONFIG,
                Permission.SYSTEM_MONITOR,
                Permission.USER_DELETE,
                Permission.FUND_DELETE,
            }
        }
    
    def has_permission(self, role: str, resource: str, action: str) -> bool:
        """
        Check if role has permission for resource and action.
        
        Args:
            role: User role
            resource: Resource name
            action: Action name
            
        Returns:
            True if role has permission, False otherwise
        """
        try:
            # Convert string role to enum
            try:
                role_enum = Role(role)
            except ValueError:
                logger.warning(f"Invalid role: {role}")
                return False
            
            # Create permission from resource and action
            permission_str = f"{resource}:{action}"
            try:
                permission = Permission(permission_str)
            except ValueError:
                logger.warning(f"Invalid permission: {permission_str}")
                return False
            
            # Check direct permission
            if permission in self.role_permissions.get(role_enum, set()):
                return True
            
            # Check hierarchical permissions
            for parent_permission, child_permissions in self.permission_hierarchy.items():
                if parent_permission in self.role_permissions.get(role_enum, set()):
                    if permission in child_permissions:
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking permission: {e}")
            return False
    
    def has_permission_direct(self, role: str, permission: str) -> bool:
        """
        Check if role has specific permission.
        
        Args:
            role: User role
            permission: Permission string
            
        Returns:
            True if role has permission, False otherwise
        """
        try:
            # Convert string role to enum
            try:
                role_enum = Role(role)
            except ValueError:
                logger.warning(f"Invalid role: {role}")
                return False
            
            # Convert string permission to enum
            try:
                permission_enum = Permission(permission)
            except ValueError:
                logger.warning(f"Invalid permission: {permission}")
                return False
            
            # Check direct permission
            return permission_enum in self.role_permissions.get(role_enum, set())
            
        except Exception as e:
            logger.error(f"Error checking direct permission: {e}")
            return False
    
    def get_role_permissions(self, role: str) -> List[str]:
        """
        Get all permissions for a role.
        
        Args:
            role: User role
            
        Returns:
            List of permission strings
        """
        try:
            # Convert string role to enum
            try:
                role_enum = Role(role)
            except ValueError:
                logger.warning(f"Invalid role: {role}")
                return []
            
            # Get direct permissions
            permissions = self.role_permissions.get(role_enum, set())
            
            # Add hierarchical permissions
            for parent_permission, child_permissions in self.permission_hierarchy.items():
                if parent_permission in permissions:
                    permissions.update(child_permissions)
            
            return [permission.value for permission in permissions]
            
        except Exception as e:
            logger.error(f"Error getting role permissions: {e}")
            return []
    
    def get_all_permissions(self) -> List[str]:
        """
        Get all available permissions.
        
        Returns:
            List of all permission strings
        """
        return [permission.value for permission in Permission]
    
    def get_all_roles(self) -> List[str]:
        """
        Get all available roles.
        
        Returns:
            List of all role strings
        """
        return [role.value for role in Role]
    
    def validate_role(self, role: str) -> bool:
        """
        Validate if role exists.
        
        Args:
            role: Role string to validate
            
        Returns:
            True if role is valid, False otherwise
        """
        try:
            Role(role)
            return True
        except ValueError:
            return False
    
    def validate_permission(self, permission: str) -> bool:
        """
        Validate if permission exists.
        
        Args:
            permission: Permission string to validate
            
        Returns:
            True if permission is valid, False otherwise
        """
        try:
            Permission(permission)
            return True
        except ValueError:
            return False
    
    def get_permission_info(self, permission: str) -> Optional[Dict[str, str]]:
        """
        Get permission information.
        
        Args:
            permission: Permission string
            
        Returns:
            Dict containing permission info or None
        """
        try:
            permission_enum = Permission(permission)
            return {
                'permission': permission_enum.value,
                'resource': permission_enum.value.split(':')[0],
                'action': permission_enum.value.split(':')[1]
            }
        except ValueError:
            return None
    
    def get_role_info(self, role: str) -> Optional[Dict[str, Any]]:
        """
        Get role information.
        
        Args:
            role: Role string
            
        Returns:
            Dict containing role info or None
        """
        try:
            role_enum = Role(role)
            permissions = self.get_role_permissions(role)
            
            return {
                'role': role_enum.value,
                'permissions': permissions,
                'permission_count': len(permissions)
            }
        except ValueError:
            return None
    
    def can_access_resource(self, role: str, resource: str) -> bool:
        """
        Check if role can access resource (any action).
        
        Args:
            role: User role
            resource: Resource name
            
        Returns:
            True if role can access resource, False otherwise
        """
        try:
            permissions = self.get_role_permissions(role)
            return any(perm.startswith(f"{resource}:") for perm in permissions)
        except Exception as e:
            logger.error(f"Error checking resource access: {e}")
            return False
    
    def get_resource_actions(self, role: str, resource: str) -> List[str]:
        """
        Get allowed actions for resource and role.
        
        Args:
            role: User role
            resource: Resource name
            
        Returns:
            List of allowed action strings
        """
        try:
            permissions = self.get_role_permissions(role)
            actions = []
            
            for permission in permissions:
                if permission.startswith(f"{resource}:"):
                    action = permission.split(":", 1)[1]
                    actions.append(action)
            
            return actions
        except Exception as e:
            logger.error(f"Error getting resource actions: {e}")
            return []
