"""
SaaS User Manager for Multi-Tenant Authentication

This module provides user management services specifically designed for the SaaS platform,
integrating with the existing security system while adding multi-tenant capabilities.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
import secrets
import uuid

# Import existing security components
from ...security.advanced_security import AdvancedSecurityManager, UserRole, Permission
from ...enterprise.user_management import UserManager, User, UserStatus
from ..models.tenant import Tenant
from ..models.customer import Customer, CustomerType

logger = logging.getLogger(__name__)


class SaaSUserManager:
    """
    SaaS User Manager that extends the existing security system with multi-tenant capabilities.
    
    This manager provides:
    - Multi-tenant user creation and management
    - Tenant-aware authentication
    - Cross-tenant user isolation
    - Tenant-specific permissions and roles
    - Integration with existing security system
    """
    
    def __init__(self):
        # Initialize existing security components
        self.security_manager = AdvancedSecurityManager()
        self.user_manager = UserManager()
        
        # SaaS-specific storage
        self.tenant_users: Dict[str, List[str]] = {}  # tenant_id -> [user_ids]
        self.user_tenants: Dict[str, str] = {}  # user_id -> tenant_id
        self.customer_mappings: Dict[str, str] = {}  # user_id -> customer_id
    
    async def create_tenant_user(self, tenant_id: str, username: str, email: str, 
                                password: str, first_name: str, last_name: str,
                                role: UserRole = UserRole.VIEWER, 
                                customer_type: CustomerType = CustomerType.VIEWER,
                                is_tenant_admin: bool = False) -> Dict[str, Any]:
        """
        Create a new user within a specific tenant.
        
        Args:
            tenant_id: Tenant ID
            username: Username
            email: Email address
            password: Password
            first_name: First name
            last_name: Last name
            role: User role
            customer_type: Customer type within tenant
            is_tenant_admin: Whether user is tenant administrator
            
        Returns:
            Dict containing user information and status
        """
        try:
            # Validate tenant exists
            if tenant_id not in self.tenant_users:
                return {
                    "status": "error",
                    "message": "Tenant not found"
                }
            
            # Create user in security system
            user_result = await self.security_manager.create_user(
                username=username,
                email=email,
                role=role,
                password=password,
                require_mfa=False  # Can be enabled later
            )
            
            if user_result["status"] != "success":
                return user_result
            
            user_id = user_result["user_id"]
            
            # Create customer record
            customer = Customer(
                customer_id=str(uuid.uuid4()),
                tenant_id=tenant_id,
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                customer_type=customer_type,
                is_tenant_admin=is_tenant_admin,
                role=role.value
            )
            
            # Store mappings
            self.user_tenants[user_id] = tenant_id
            self.customer_mappings[user_id] = customer.customer_id
            
            if tenant_id not in self.tenant_users:
                self.tenant_users[tenant_id] = []
            self.tenant_users[tenant_id].append(user_id)
            
            logger.info(f"Created tenant user: {username} for tenant: {tenant_id}")
            
            return {
                "status": "success",
                "user_id": user_id,
                "customer_id": customer.customer_id,
                "user": {
                    "user_id": user_id,
                    "username": username,
                    "email": email,
                    "role": role.value,
                    "tenant_id": tenant_id,
                    "customer_type": customer_type.value,
                    "is_tenant_admin": is_tenant_admin
                },
                "message": "User created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating tenant user: {e}")
            return {
                "status": "error",
                "message": f"Failed to create user: {str(e)}"
            }
    
    async def authenticate_tenant_user(self, username: str, password: str, 
                                     tenant_id: str, mfa_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Authenticate a user within a specific tenant context.
        
        Args:
            username: Username
            password: Password
            tenant_id: Tenant ID
            mfa_code: Optional MFA code
            
        Returns:
            Dict containing authentication result
        """
        try:
            # Authenticate with security system
            auth_result = await self.security_manager.authenticate_user(
                username=username,
                password=password,
                mfa_code=mfa_code
            )
            
            if auth_result["status"] != "success":
                return auth_result
            
            user_id = auth_result["user"]["user_id"]
            
            # Verify user belongs to tenant
            if user_id not in self.user_tenants or self.user_tenants[user_id] != tenant_id:
                return {
                    "status": "error",
                    "message": "User does not belong to this tenant"
                }
            
            # Get customer information
            customer_id = self.customer_mappings.get(user_id)
            
            # Add tenant context to response
            auth_result["tenant_id"] = tenant_id
            auth_result["customer_id"] = customer_id
            
            logger.info(f"Authenticated tenant user: {username} for tenant: {tenant_id}")
            
            return auth_result
            
        except Exception as e:
            logger.error(f"Error authenticating tenant user: {e}")
            return {
                "status": "error",
                "message": f"Authentication failed: {str(e)}"
            }
    
    async def get_tenant_users(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all users for a specific tenant."""
        try:
            if tenant_id not in self.tenant_users:
                return []
            
            user_ids = self.tenant_users[tenant_id]
            users = []
            
            for user_id in user_ids:
                # Get user from security system
                user_data = self.security_manager.users.get(user_id)
                if user_data:
                    customer_id = self.customer_mappings.get(user_id)
                    user_info = {
                        "user_id": user_id,
                        "username": user_data["username"],
                        "email": user_data["email"],
                        "role": user_data["role"].value,
                        "customer_id": customer_id,
                        "created_at": user_data["created_at"].isoformat(),
                        "last_login": user_data["last_login"].isoformat() if user_data["last_login"] else None
                    }
                    users.append(user_info)
            
            return users
            
        except Exception as e:
            logger.error(f"Error getting tenant users: {e}")
            return []
    
    async def update_tenant_user(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a tenant user."""
        try:
            # Verify user exists and get tenant
            if user_id not in self.user_tenants:
                return {
                    "status": "error",
                    "message": "User not found"
                }
            
            tenant_id = self.user_tenants[user_id]
            user_data = self.security_manager.users.get(user_id)
            
            if not user_data:
                return {
                    "status": "error",
                    "message": "User not found in security system"
                }
            
            # Update allowed fields
            allowed_fields = ["email", "role"]
            for field, value in updates.items():
                if field in allowed_fields and field in user_data:
                    if field == "role":
                        user_data[field] = UserRole(value)
                    else:
                        user_data[field] = value
            
            user_data["updated_at"] = datetime.now(timezone.utc)
            
            logger.info(f"Updated tenant user: {user_id}")
            
            return {
                "status": "success",
                "message": "User updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating tenant user: {e}")
            return {
                "status": "error",
                "message": f"Failed to update user: {str(e)}"
            }
    
    async def remove_tenant_user(self, user_id: str) -> Dict[str, Any]:
        """Remove a user from a tenant."""
        try:
            # Verify user exists and get tenant
            if user_id not in self.user_tenants:
                return {
                    "status": "error",
                    "message": "User not found"
                }
            
            tenant_id = self.user_tenants[user_id]
            
            # Remove from security system
            if user_id in self.security_manager.users:
                del self.security_manager.users[user_id]
            
            # Remove from tenant users list
            if tenant_id in self.tenant_users and user_id in self.tenant_users[tenant_id]:
                self.tenant_users[tenant_id].remove(user_id)
            
            # Remove mappings
            del self.user_tenants[user_id]
            if user_id in self.customer_mappings:
                del self.customer_mappings[user_id]
            
            logger.info(f"Removed tenant user: {user_id} from tenant: {tenant_id}")
            
            return {
                "status": "success",
                "message": "User removed successfully"
            }
            
        except Exception as e:
            logger.error(f"Error removing tenant user: {e}")
            return {
                "status": "error",
                "message": f"Failed to remove user: {str(e)}"
            }
    
    async def check_tenant_permission(self, user_id: str, tenant_id: str, permission: Permission) -> bool:
        """Check if user has permission within a specific tenant."""
        try:
            # Verify user belongs to tenant
            if user_id not in self.user_tenants or self.user_tenants[user_id] != tenant_id:
                return False
            
            # Check permission in security system
            return await self.security_manager.check_permission(
                session_token="",  # This would need to be passed from session
                permission=permission
            )
            
        except Exception as e:
            logger.error(f"Error checking tenant permission: {e}")
            return False
    
    async def get_user_tenants(self, user_id: str) -> List[str]:
        """Get all tenants a user belongs to."""
        try:
            if user_id in self.user_tenants:
                return [self.user_tenants[user_id]]
            return []
            
        except Exception as e:
            logger.error(f"Error getting user tenants: {e}")
            return []
    
    async def transfer_user_to_tenant(self, user_id: str, from_tenant_id: str, to_tenant_id: str) -> Dict[str, Any]:
        """Transfer a user from one tenant to another."""
        try:
            # Verify user exists and belongs to source tenant
            if user_id not in self.user_tenants or self.user_tenants[user_id] != from_tenant_id:
                return {
                    "status": "error",
                    "message": "User not found in source tenant"
                }
            
            # Verify target tenant exists
            if to_tenant_id not in self.tenant_users:
                return {
                    "status": "error",
                    "message": "Target tenant not found"
                }
            
            # Remove from source tenant
            if from_tenant_id in self.tenant_users and user_id in self.tenant_users[from_tenant_id]:
                self.tenant_users[from_tenant_id].remove(user_id)
            
            # Add to target tenant
            if to_tenant_id not in self.tenant_users:
                self.tenant_users[to_tenant_id] = []
            self.tenant_users[to_tenant_id].append(user_id)
            
            # Update user-tenant mapping
            self.user_tenants[user_id] = to_tenant_id
            
            logger.info(f"Transferred user: {user_id} from tenant: {from_tenant_id} to tenant: {to_tenant_id}")
            
            return {
                "status": "success",
                "message": "User transferred successfully"
            }
            
        except Exception as e:
            logger.error(f"Error transferring user: {e}")
            return {
                "status": "error",
                "message": f"Failed to transfer user: {str(e)}"
            }
    
    async def get_tenant_user_stats(self, tenant_id: str) -> Dict[str, Any]:
        """Get user statistics for a tenant."""
        try:
            if tenant_id not in self.tenant_users:
                return {
                    "status": "error",
                    "message": "Tenant not found"
                }
            
            user_ids = self.tenant_users[tenant_id]
            total_users = len(user_ids)
            
            # Count users by role
            role_counts = {}
            for user_id in user_ids:
                user_data = self.security_manager.users.get(user_id)
                if user_data:
                    role = user_data["role"].value
                    role_counts[role] = role_counts.get(role, 0) + 1
            
            return {
                "status": "success",
                "stats": {
                    "total_users": total_users,
                    "role_distribution": role_counts
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting tenant user stats: {e}")
            return {
                "status": "error",
                "message": f"Failed to get user stats: {str(e)}"
            }
    
    async def get_system_user_stats(self) -> Dict[str, Any]:
        """Get system-wide user statistics."""
        try:
            total_users = len(self.user_tenants)
            total_tenants = len(self.tenant_users)
            
            # Count users per tenant
            tenant_user_counts = {}
            for tenant_id, user_ids in self.tenant_users.items():
                tenant_user_counts[tenant_id] = len(user_ids)
            
            return {
                "status": "success",
                "stats": {
                    "total_users": total_users,
                    "total_tenants": total_tenants,
                    "users_per_tenant": tenant_user_counts
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting system user stats: {e}")
            return {
                "status": "error",
                "message": f"Failed to get system user stats: {str(e)}"
            }
