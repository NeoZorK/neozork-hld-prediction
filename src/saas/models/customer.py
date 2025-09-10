"""
Customer Model for SaaS Platform

This module defines the customer model which represents individual users
within tenant organizations in the SaaS platform.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid


class CustomerStatus(Enum):
    """Customer status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"
    LOCKED = "locked"


class CustomerType(Enum):
    """Customer type enumeration"""
    ADMIN = "admin"
    MANAGER = "manager"
    TRADER = "trader"
    ANALYST = "analyst"
    VIEWER = "viewer"
    AUDITOR = "auditor"


@dataclass
class Customer:
    """
    Customer model representing individual users within tenant organizations.
    
    Each customer includes:
    - Personal information and contact details
    - Role and permissions within the tenant
    - Usage tracking and activity monitoring
    - Preferences and settings
    - Security and authentication data
    """
    
    # Core identification
    customer_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    user_id: str = ""  # Reference to main user management system
    
    # Personal information
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: Optional[str] = None
    
    # Customer classification
    customer_type: CustomerType = CustomerType.VIEWER
    status: CustomerStatus = CustomerStatus.PENDING
    
    # Role and permissions
    role: str = "viewer"
    permissions: List[str] = field(default_factory=list)
    is_tenant_admin: bool = False
    
    # Usage and activity
    last_login: Optional[datetime] = None
    login_count: int = 0
    api_calls_this_month: int = 0
    storage_used_mb: int = 0
    
    # Preferences and settings
    preferences: Dict[str, Any] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: Optional[datetime] = None
    
    # Security
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    password_changed_at: Optional[datetime] = None
    
    # Profile information
    profile_data: Dict[str, Any] = field(default_factory=dict)
    avatar_url: Optional[str] = None
    
    # Notification preferences
    notification_preferences: Dict[str, bool] = field(default_factory=dict)
    
    # Timezone and locale
    timezone: str = "UTC"
    locale: str = "en_US"
    
    def __post_init__(self):
        """Post-initialization setup"""
        # Set default notification preferences
        if not self.notification_preferences:
            self.notification_preferences = {
                "email_notifications": True,
                "push_notifications": True,
                "sms_notifications": False,
                "trading_alerts": True,
                "system_updates": True,
                "marketing_emails": False
            }
    
    def get_full_name(self) -> str:
        """Get customer's full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def is_active(self) -> bool:
        """Check if customer is active"""
        return self.status == CustomerStatus.ACTIVE
    
    def is_locked(self) -> bool:
        """Check if customer account is locked"""
        return (self.status == CustomerStatus.LOCKED or 
                (self.locked_until is not None and datetime.utcnow() < self.locked_until))
    
    def is_tenant_admin(self) -> bool:
        """Check if customer is tenant administrator"""
        return self.is_tenant_admin
    
    def has_permission(self, permission: str) -> bool:
        """Check if customer has a specific permission"""
        return permission in self.permissions
    
    def add_permission(self, permission: str) -> None:
        """Add a permission to customer"""
        if permission not in self.permissions:
            self.permissions.append(permission)
            self.updated_at = datetime.utcnow()
    
    def remove_permission(self, permission: str) -> None:
        """Remove a permission from customer"""
        if permission in self.permissions:
            self.permissions.remove(permission)
            self.updated_at = datetime.utcnow()
    
    def update_preference(self, key: str, value: Any) -> None:
        """Update a customer preference"""
        self.preferences[key] = value
        self.updated_at = datetime.utcnow()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a customer preference"""
        return self.preferences.get(key, default)
    
    def update_setting(self, key: str, value: Any) -> None:
        """Update a customer setting"""
        self.settings[key] = value
        self.updated_at = datetime.utcnow()
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a customer setting"""
        return self.settings.get(key, default)
    
    def update_notification_preference(self, notification_type: str, enabled: bool) -> None:
        """Update notification preference"""
        self.notification_preferences[notification_type] = enabled
        self.updated_at = datetime.utcnow()
    
    def is_notification_enabled(self, notification_type: str) -> bool:
        """Check if notification type is enabled"""
        return self.notification_preferences.get(notification_type, False)
    
    def record_login(self, ip_address: str = None) -> None:
        """Record customer login"""
        self.last_login = datetime.utcnow()
        self.login_count += 1
        self.last_activity = datetime.utcnow()
        self.failed_login_attempts = 0
        self.locked_until = None
        self.updated_at = datetime.utcnow()
    
    def record_failed_login(self) -> None:
        """Record failed login attempt"""
        self.failed_login_attempts += 1
        self.updated_at = datetime.utcnow()
        
        # Lock account after 5 failed attempts
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)
            self.status = CustomerStatus.LOCKED
    
    def unlock_account(self) -> None:
        """Unlock customer account"""
        self.failed_login_attempts = 0
        self.locked_until = None
        if self.status == CustomerStatus.LOCKED:
            self.status = CustomerStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def update_usage(self, usage_type: str, amount: int) -> None:
        """Update usage statistics"""
        if usage_type == "api_calls":
            self.api_calls_this_month += amount
        elif usage_type == "storage":
            self.storage_used_mb += amount
        
        self.last_activity = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def reset_monthly_usage(self) -> None:
        """Reset monthly usage counters"""
        self.api_calls_this_month = 0
        self.updated_at = datetime.utcnow()
    
    def update_profile(self, profile_data: Dict[str, Any]) -> None:
        """Update customer profile data"""
        self.profile_data.update(profile_data)
        self.updated_at = datetime.utcnow()
    
    def get_profile_summary(self) -> Dict[str, Any]:
        """Get customer profile summary"""
        return {
            "customer_id": self.customer_id,
            "name": self.get_full_name(),
            "email": self.email,
            "customer_type": self.customer_type.value,
            "status": self.status.value,
            "is_tenant_admin": self.is_tenant_admin,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "login_count": self.login_count,
            "created_at": self.created_at.isoformat(),
            "avatar_url": self.avatar_url
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert customer to dictionary"""
        return {
            "customer_id": self.customer_id,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "customer_type": self.customer_type.value,
            "status": self.status.value,
            "role": self.role,
            "permissions": self.permissions,
            "is_tenant_admin": self.is_tenant_admin,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "login_count": self.login_count,
            "api_calls_this_month": self.api_calls_this_month,
            "storage_used_mb": self.storage_used_mb,
            "preferences": self.preferences,
            "settings": self.settings,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "failed_login_attempts": self.failed_login_attempts,
            "locked_until": self.locked_until.isoformat() if self.locked_until else None,
            "password_changed_at": self.password_changed_at.isoformat() if self.password_changed_at else None,
            "profile_data": self.profile_data,
            "avatar_url": self.avatar_url,
            "notification_preferences": self.notification_preferences,
            "timezone": self.timezone,
            "locale": self.locale
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Customer":
        """Create customer from dictionary"""
        # Convert string dates back to datetime objects
        date_fields = [
            "created_at", "updated_at", "last_login", "last_activity", 
            "locked_until", "password_changed_at"
        ]
        
        for field in date_fields:
            if data.get(field):
                data[field] = datetime.fromisoformat(data[field])
        
        # Convert enum values
        if data.get("customer_type"):
            data["customer_type"] = CustomerType(data["customer_type"])
        if data.get("status"):
            data["status"] = CustomerStatus(data["status"])
        
        return cls(**data)
    
    def __str__(self) -> str:
        return f"Customer({self.get_full_name()}: {self.status.value})"
    
    def __repr__(self) -> str:
        return f"Customer(id='{self.customer_id}', name='{self.get_full_name()}', status='{self.status.value}')"
