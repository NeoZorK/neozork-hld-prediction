"""
Tenant Model for Multi-Tenant SaaS Architecture

This module defines the tenant model which represents a customer organization
in the multi-tenant SaaS platform.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
import secrets
import uuid


class TenantStatus(Enum):
    """Tenant status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TRIAL = "trial"
    EXPIRED = "expired"
    PENDING = "pending"


class TenantType(Enum):
    """Tenant type enumeration"""
    INDIVIDUAL = "individual"
    SMALL_BUSINESS = "small_business"
    ENTERPRISE = "enterprise"
    INSTITUTIONAL = "institutional"


@dataclass
class Tenant:
    """
    Tenant model representing a customer organization in the SaaS platform.
    
    Each tenant represents a separate customer organization with their own:
    - Data isolation
    - User management
    - Subscription and billing
    - Usage tracking
    - Custom configurations
    """
    
    # Core identification
    tenant_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_slug: str = field(default_factory=lambda: secrets.token_urlsafe(8))
    name: str = ""
    display_name: str = ""
    
    # Contact information
    email: str = ""
    phone: Optional[str] = None
    website: Optional[str] = None
    
    # Address information
    address: Optional[Dict[str, str]] = field(default_factory=dict)
    
    # Tenant classification
    tenant_type: TenantType = TenantType.INDIVIDUAL
    status: TenantStatus = TenantStatus.PENDING
    
    # Subscription and billing
    subscription_id: Optional[str] = None
    billing_email: Optional[str] = None
    payment_method_id: Optional[str] = None
    
    # Configuration and settings
    settings: Dict[str, Any] = field(default_factory=dict)
    features: List[str] = field(default_factory=list)
    limits: Dict[str, int] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    trial_ends_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    
    # User management
    admin_user_id: Optional[str] = None
    user_count: int = 0
    max_users: int = 1
    
    # Usage tracking
    api_calls_this_month: int = 0
    storage_used_mb: int = 0
    last_billing_date: Optional[datetime] = None
    
    # Compliance and security
    compliance_level: str = "standard"
    data_retention_days: int = 365
    security_settings: Dict[str, Any] = field(default_factory=dict)
    
    # Custom branding
    branding: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization setup"""
        if not self.display_name:
            self.display_name = self.name
        if not self.tenant_slug:
            self.tenant_slug = self._generate_slug()
    
    def _generate_slug(self) -> str:
        """Generate a unique tenant slug"""
        base_slug = self.name.lower().replace(" ", "-").replace("_", "-")
        # Remove special characters
        import re
        base_slug = re.sub(r'[^a-z0-9-]', '', base_slug)
        # Add random suffix for uniqueness
        return f"{base_slug}-{secrets.token_urlsafe(4)}"
    
    def is_active(self) -> bool:
        """Check if tenant is active"""
        return self.status == TenantStatus.ACTIVE
    
    def is_trial(self) -> bool:
        """Check if tenant is in trial period"""
        return self.status == TenantStatus.TRIAL
    
    def is_trial_expired(self) -> bool:
        """Check if trial period has expired"""
        if not self.is_trial() or not self.trial_ends_at:
            return False
        return datetime.now(datetime.UTC) > self.trial_ends_at
    
    def get_trial_days_remaining(self) -> int:
        """Get number of trial days remaining"""
        if not self.is_trial() or not self.trial_ends_at:
            return 0
        delta = self.trial_ends_at - datetime.now(datetime.UTC)
        return max(0, delta.days)
    
    def can_add_user(self) -> bool:
        """Check if tenant can add more users"""
        return self.user_count < self.max_users
    
    def is_within_limits(self, limit_type: str, current_usage: int) -> bool:
        """Check if current usage is within limits"""
        limit = self.limits.get(limit_type, 0)
        return current_usage <= limit
    
    def get_usage_percentage(self, limit_type: str, current_usage: int) -> float:
        """Get usage percentage for a limit type"""
        limit = self.limits.get(limit_type, 1)
        if limit == 0:
            return 0.0
        return min(100.0, (current_usage / limit) * 100.0)
    
    def has_feature(self, feature_name: str) -> bool:
        """Check if tenant has access to a feature"""
        return feature_name in self.features
    
    def add_feature(self, feature_name: str) -> None:
        """Add a feature to tenant"""
        if feature_name not in self.features:
            self.features.append(feature_name)
            self.updated_at = datetime.now(datetime.UTC)
    
    def remove_feature(self, feature_name: str) -> None:
        """Remove a feature from tenant"""
        if feature_name in self.features:
            self.features.remove(feature_name)
            self.updated_at = datetime.now(datetime.UTC)
    
    def update_setting(self, key: str, value: Any) -> None:
        """Update a tenant setting"""
        self.settings[key] = value
        self.updated_at = datetime.now(datetime.UTC)
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a tenant setting"""
        return self.settings.get(key, default)
    
    def update_usage(self, usage_type: str, amount: int) -> None:
        """Update usage statistics"""
        if usage_type == "api_calls":
            self.api_calls_this_month += amount
        elif usage_type == "storage":
            self.storage_used_mb += amount
        
        self.last_activity = datetime.now(datetime.UTC)
        self.updated_at = datetime.now(datetime.UTC)
    
    def reset_monthly_usage(self) -> None:
        """Reset monthly usage counters"""
        self.api_calls_this_month = 0
        self.last_billing_date = datetime.now(datetime.UTC)
        self.updated_at = datetime.now(datetime.UTC)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tenant to dictionary"""
        return {
            "tenant_id": self.tenant_id,
            "tenant_slug": self.tenant_slug,
            "name": self.name,
            "display_name": self.display_name,
            "email": self.email,
            "phone": self.phone,
            "website": self.website,
            "address": self.address,
            "tenant_type": self.tenant_type.value,
            "status": self.status.value,
            "subscription_id": self.subscription_id,
            "billing_email": self.billing_email,
            "settings": self.settings,
            "features": self.features,
            "limits": self.limits,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "trial_ends_at": self.trial_ends_at.isoformat() if self.trial_ends_at else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "admin_user_id": self.admin_user_id,
            "user_count": self.user_count,
            "max_users": self.max_users,
            "api_calls_this_month": self.api_calls_this_month,
            "storage_used_mb": self.storage_used_mb,
            "last_billing_date": self.last_billing_date.isoformat() if self.last_billing_date else None,
            "compliance_level": self.compliance_level,
            "data_retention_days": self.data_retention_days,
            "security_settings": self.security_settings,
            "branding": self.branding
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tenant":
        """Create tenant from dictionary"""
        # Convert string dates back to datetime objects
        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        if data.get("trial_ends_at"):
            data["trial_ends_at"] = datetime.fromisoformat(data["trial_ends_at"])
        if data.get("last_activity"):
            data["last_activity"] = datetime.fromisoformat(data["last_activity"])
        if data.get("last_billing_date"):
            data["last_billing_date"] = datetime.fromisoformat(data["last_billing_date"])
        
        # Convert enum values
        if data.get("tenant_type"):
            data["tenant_type"] = TenantType(data["tenant_type"])
        if data.get("status"):
            data["status"] = TenantStatus(data["status"])
        
        return cls(**data)
    
    def __str__(self) -> str:
        return f"Tenant({self.tenant_slug}: {self.display_name})"
    
    def __repr__(self) -> str:
        return f"Tenant(tenant_id='{self.tenant_id}', slug='{self.tenant_slug}', name='{self.name}')"
