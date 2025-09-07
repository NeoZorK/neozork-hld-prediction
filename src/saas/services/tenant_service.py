"""
Tenant Service for SaaS Platform

This service handles all tenant-related operations including creation, management,
and multi-tenant data isolation.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import secrets
import uuid

from ..models.tenant import Tenant, TenantStatus, TenantType

logger = logging.getLogger(__name__)


class TenantService:
    """
    Service for managing tenants in the SaaS platform.
    
    This service provides:
    - Tenant creation and onboarding
    - Tenant configuration and settings
    - Multi-tenant data isolation
    - Tenant analytics and monitoring
    - Tenant lifecycle management
    """
    
    def __init__(self):
        self.tenants: Dict[str, Tenant] = {}
        self.tenant_slugs: Dict[str, str] = {}  # slug -> tenant_id mapping
        self.tenant_emails: Dict[str, str] = {}  # email -> tenant_id mapping
    
    async def create_tenant(self, name: str, email: str, tenant_type: TenantType = TenantType.INDIVIDUAL,
                           admin_user_id: Optional[str] = None, trial_days: int = 14) -> Dict[str, Any]:
        """
        Create a new tenant.
        
        Args:
            name: Tenant organization name
            email: Primary contact email
            tenant_type: Type of tenant (individual, small_business, enterprise, institutional)
            admin_user_id: ID of the admin user
            trial_days: Number of trial days
            
        Returns:
            Dict containing tenant information and status
        """
        try:
            # Validate input
            if not name or not email:
                return {
                    "status": "error",
                    "message": "Name and email are required"
                }
            
            # Check if tenant already exists
            if email in self.tenant_emails:
                return {
                    "status": "error",
                    "message": "Tenant with this email already exists"
                }
            
            # Create tenant
            tenant = Tenant(
                name=name,
                email=email,
                tenant_type=tenant_type,
                admin_user_id=admin_user_id,
                status=TenantStatus.TRIAL if trial_days > 0 else TenantStatus.PENDING
            )
            
            # Set trial period
            if trial_days > 0:
                tenant.trial_ends_at = datetime.utcnow() + timedelta(days=trial_days)
            
            # Set default limits based on tenant type
            self._set_default_limits(tenant)
            
            # Store tenant
            self.tenants[tenant.tenant_id] = tenant
            self.tenant_slugs[tenant.tenant_slug] = tenant.tenant_id
            self.tenant_emails[email] = tenant.tenant_id
            
            logger.info(f"Created tenant: {tenant.tenant_slug} ({tenant.name})")
            
            return {
                "status": "success",
                "tenant": tenant.to_dict(),
                "message": "Tenant created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating tenant: {e}")
            return {
                "status": "error",
                "message": f"Failed to create tenant: {str(e)}"
            }
    
    async def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """Get tenant by ID."""
        return self.tenants.get(tenant_id)
    
    async def get_tenant_by_slug(self, tenant_slug: str) -> Optional[Tenant]:
        """Get tenant by slug."""
        tenant_id = self.tenant_slugs.get(tenant_slug)
        if tenant_id:
            return self.tenants.get(tenant_id)
        return None
    
    async def get_tenant_by_email(self, email: str) -> Optional[Tenant]:
        """Get tenant by email."""
        tenant_id = self.tenant_emails.get(email)
        if tenant_id:
            return self.tenants.get(tenant_id)
        return None
    
    async def update_tenant(self, tenant_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update tenant information.
        
        Args:
            tenant_id: Tenant ID
            updates: Dictionary of fields to update
            
        Returns:
            Dict containing update status
        """
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                return {
                    "status": "error",
                    "message": "Tenant not found"
                }
            
            # Update allowed fields
            allowed_fields = [
                "name", "display_name", "email", "phone", "website", "address",
                "tenant_type", "settings", "features", "limits", "billing_email",
                "compliance_level", "data_retention_days", "security_settings", "branding"
            ]
            
            for field, value in updates.items():
                if field in allowed_fields and hasattr(tenant, field):
                    setattr(tenant, field, value)
            
            tenant.updated_at = datetime.utcnow()
            
            # Update email mapping if email changed
            if "email" in updates and updates["email"] != tenant.email:
                old_email = tenant.email
                new_email = updates["email"]
                
                if old_email in self.tenant_emails:
                    del self.tenant_emails[old_email]
                self.tenant_emails[new_email] = tenant_id
            
            logger.info(f"Updated tenant: {tenant.tenant_slug}")
            
            return {
                "status": "success",
                "tenant": tenant.to_dict(),
                "message": "Tenant updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating tenant: {e}")
            return {
                "status": "error",
                "message": f"Failed to update tenant: {str(e)}"
            }
    
    async def activate_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """Activate a tenant."""
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                return {
                    "status": "error",
                    "message": "Tenant not found"
                }
            
            tenant.status = TenantStatus.ACTIVE
            tenant.updated_at = datetime.utcnow()
            
            logger.info(f"Activated tenant: {tenant.tenant_slug}")
            
            return {
                "status": "success",
                "message": "Tenant activated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error activating tenant: {e}")
            return {
                "status": "error",
                "message": f"Failed to activate tenant: {str(e)}"
            }
    
    async def suspend_tenant(self, tenant_id: str, reason: str = "") -> Dict[str, Any]:
        """Suspend a tenant."""
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                return {
                    "status": "error",
                    "message": "Tenant not found"
                }
            
            tenant.status = TenantStatus.SUSPENDED
            tenant.updated_at = datetime.utcnow()
            
            if reason:
                tenant.settings["suspension_reason"] = reason
            
            logger.info(f"Suspended tenant: {tenant.tenant_slug} - {reason}")
            
            return {
                "status": "success",
                "message": "Tenant suspended successfully"
            }
            
        except Exception as e:
            logger.error(f"Error suspending tenant: {e}")
            return {
                "status": "error",
                "message": f"Failed to suspend tenant: {str(e)}"
            }
    
    async def delete_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """Delete a tenant (soft delete)."""
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                return {
                    "status": "error",
                    "message": "Tenant not found"
                }
            
            # Soft delete - mark as inactive
            tenant.status = TenantStatus.INACTIVE
            tenant.updated_at = datetime.utcnow()
            
            # Remove from mappings
            if tenant.email in self.tenant_emails:
                del self.tenant_emails[tenant.email]
            if tenant.tenant_slug in self.tenant_slugs:
                del self.tenant_slugs[tenant.tenant_slug]
            
            logger.info(f"Deleted tenant: {tenant.tenant_slug}")
            
            return {
                "status": "success",
                "message": "Tenant deleted successfully"
            }
            
        except Exception as e:
            logger.error(f"Error deleting tenant: {e}")
            return {
                "status": "error",
                "message": f"Failed to delete tenant: {str(e)}"
            }
    
    async def get_tenant_usage(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant usage statistics."""
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                return {
                    "status": "error",
                    "message": "Tenant not found"
                }
            
            usage_stats = {
                "api_calls_this_month": tenant.api_calls_this_month,
                "storage_used_mb": tenant.storage_used_mb,
                "user_count": tenant.user_count,
                "max_users": tenant.max_users,
                "usage_percentages": {}
            }
            
            # Calculate usage percentages
            for limit_type, limit_value in tenant.limits.items():
                if limit_type == "api_calls":
                    current_usage = tenant.api_calls_this_month
                elif limit_type == "storage":
                    current_usage = tenant.storage_used_mb
                elif limit_type == "users":
                    current_usage = tenant.user_count
                else:
                    current_usage = 0
                
                usage_percentage = tenant.get_usage_percentage(limit_type, current_usage)
                usage_stats["usage_percentages"][limit_type] = usage_percentage
            
            return {
                "status": "success",
                "usage": usage_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting tenant usage: {e}")
            return {
                "status": "error",
                "message": f"Failed to get tenant usage: {str(e)}"
            }
    
    async def update_tenant_usage(self, tenant_id: str, usage_type: str, amount: int) -> Dict[str, Any]:
        """Update tenant usage statistics."""
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                return {
                    "status": "error",
                    "message": "Tenant not found"
                }
            
            tenant.update_usage(usage_type, amount)
            
            return {
                "status": "success",
                "message": "Usage updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating tenant usage: {e}")
            return {
                "status": "error",
                "message": f"Failed to update tenant usage: {str(e)}"
            }
    
    async def get_tenant_analytics(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant analytics and insights."""
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                return {
                    "status": "error",
                    "message": "Tenant not found"
                }
            
            analytics = {
                "tenant_info": {
                    "name": tenant.name,
                    "tenant_type": tenant.tenant_type.value,
                    "status": tenant.status.value,
                    "created_at": tenant.created_at.isoformat(),
                    "last_activity": tenant.last_activity.isoformat() if tenant.last_activity else None
                },
                "usage_stats": {
                    "api_calls_this_month": tenant.api_calls_this_month,
                    "storage_used_mb": tenant.storage_used_mb,
                    "user_count": tenant.user_count,
                    "max_users": tenant.max_users
                },
                "subscription_info": {
                    "subscription_id": tenant.subscription_id,
                    "trial_ends_at": tenant.trial_ends_at.isoformat() if tenant.trial_ends_at else None,
                    "trial_days_remaining": tenant.get_trial_days_remaining()
                },
                "features": tenant.features,
                "limits": tenant.limits
            }
            
            return {
                "status": "success",
                "analytics": analytics
            }
            
        except Exception as e:
            logger.error(f"Error getting tenant analytics: {e}")
            return {
                "status": "error",
                "message": f"Failed to get tenant analytics: {str(e)}"
            }
    
    async def list_tenants(self, status: Optional[TenantStatus] = None, 
                          tenant_type: Optional[TenantType] = None,
                          limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """List tenants with optional filtering."""
        try:
            tenants = list(self.tenants.values())
            
            # Apply filters
            if status:
                tenants = [t for t in tenants if t.status == status]
            if tenant_type:
                tenants = [t for t in tenants if t.tenant_type == tenant_type]
            
            # Sort by created_at (newest first)
            tenants.sort(key=lambda t: t.created_at, reverse=True)
            
            # Apply pagination
            total_count = len(tenants)
            tenants = tenants[offset:offset + limit]
            
            return {
                "status": "success",
                "tenants": [tenant.to_dict() for tenant in tenants],
                "total_count": total_count,
                "limit": limit,
                "offset": offset
            }
            
        except Exception as e:
            logger.error(f"Error listing tenants: {e}")
            return {
                "status": "error",
                "message": f"Failed to list tenants: {str(e)}"
            }
    
    def _set_default_limits(self, tenant: Tenant) -> None:
        """Set default limits based on tenant type."""
        default_limits = {
            TenantType.INDIVIDUAL: {
                "api_calls": 10000,
                "storage": 1000,  # MB
                "users": 1,
                "strategies": 5,
                "backtests": 10
            },
            TenantType.SMALL_BUSINESS: {
                "api_calls": 50000,
                "storage": 5000,  # MB
                "users": 5,
                "strategies": 25,
                "backtests": 100
            },
            TenantType.ENTERPRISE: {
                "api_calls": 500000,
                "storage": 50000,  # MB
                "users": 50,
                "strategies": -1,  # unlimited
                "backtests": -1  # unlimited
            },
            TenantType.INSTITUTIONAL: {
                "api_calls": -1,  # unlimited
                "storage": -1,  # unlimited
                "users": -1,  # unlimited
                "strategies": -1,  # unlimited
                "backtests": -1  # unlimited
            }
        }
        
        if tenant.tenant_type in default_limits:
            tenant.limits = default_limits[tenant.tenant_type]
            tenant.max_users = tenant.limits.get("users", 1)
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get system-wide tenant statistics."""
        try:
            total_tenants = len(self.tenants)
            active_tenants = len([t for t in self.tenants.values() if t.status == TenantStatus.ACTIVE])
            trial_tenants = len([t for t in self.tenants.values() if t.status == TenantStatus.TRIAL])
            suspended_tenants = len([t for t in self.tenants.values() if t.status == TenantStatus.SUSPENDED])
            
            # Tenant type distribution
            type_distribution = {}
            for tenant in self.tenants.values():
                tenant_type = tenant.tenant_type.value
                type_distribution[tenant_type] = type_distribution.get(tenant_type, 0) + 1
            
            return {
                "status": "success",
                "stats": {
                    "total_tenants": total_tenants,
                    "active_tenants": active_tenants,
                    "trial_tenants": trial_tenants,
                    "suspended_tenants": suspended_tenants,
                    "type_distribution": type_distribution
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {
                "status": "error",
                "message": f"Failed to get system stats: {str(e)}"
            }
