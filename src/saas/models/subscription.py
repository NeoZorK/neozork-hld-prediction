"""
Subscription Model for SaaS Platform

This module defines the subscription model which represents a customer's
subscription to the SaaS platform with different tiers and features.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid


class SubscriptionStatus(Enum):
    """Subscription status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    PAST_DUE = "past_due"
    TRIALING = "trialing"
    UNPAID = "unpaid"
    PENDING = "pending"


class SubscriptionTier(Enum):
    """Subscription tier enumeration"""
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    INSTITUTIONAL = "institutional"


@dataclass
class Subscription:
    """
    Subscription model representing a customer's subscription to the SaaS platform.
    
    Each subscription includes:
    - Plan details and pricing
    - Billing cycle and payment terms
    - Feature access and limits
    - Usage tracking
    - Status and lifecycle management
    """
    
    # Core identification
    subscription_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    plan_id: str = ""
    
    # Subscription details
    tier: SubscriptionTier = SubscriptionTier.STARTER
    status: SubscriptionStatus = SubscriptionStatus.PENDING
    
    # Pricing and billing
    monthly_price: float = 0.0
    annual_price: float = 0.0
    currency: str = "USD"
    billing_cycle: str = "monthly"  # monthly, annual, quarterly
    
    # Billing dates
    current_period_start: datetime = field(default_factory=datetime.utcnow)
    current_period_end: datetime = field(default_factory=lambda: datetime.now(datetime.UTC) + timedelta(days=30))
    trial_start: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    
    # Features and limits
    features: List[str] = field(default_factory=list)
    limits: Dict[str, int] = field(default_factory=dict)
    
    # Usage tracking
    usage_this_period: Dict[str, int] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Payment and billing
    payment_method_id: Optional[str] = None
    billing_email: Optional[str] = None
    auto_renew: bool = True
    
    # Custom pricing (for enterprise)
    custom_pricing: Optional[Dict[str, Any]] = None
    discount_percentage: float = 0.0
    
    # Add-ons and extras
    add_ons: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization setup"""
        # Set trial period if not specified
        if self.status == SubscriptionStatus.TRIALING and not self.trial_start:
            self.trial_start = datetime.now(datetime.UTC)
            self.trial_end = datetime.now(datetime.UTC) + timedelta(days=14)
    
    def is_active(self) -> bool:
        """Check if subscription is active"""
        return self.status == SubscriptionStatus.ACTIVE
    
    def is_trial(self) -> bool:
        """Check if subscription is in trial period"""
        return self.status == SubscriptionStatus.TRIALING
    
    def is_trial_expired(self) -> bool:
        """Check if trial period has expired"""
        if not self.is_trial() or not self.trial_end:
            return False
        return datetime.now(datetime.UTC) > self.trial_end
    
    def get_trial_days_remaining(self) -> int:
        """Get number of trial days remaining"""
        if not self.is_trial() or not self.trial_end:
            return 0
        delta = self.trial_end - datetime.now(datetime.UTC)
        return max(0, delta.days)
    
    def is_cancelled(self) -> bool:
        """Check if subscription is cancelled"""
        return self.status == SubscriptionStatus.CANCELLED
    
    def is_past_due(self) -> bool:
        """Check if subscription is past due"""
        return self.status == SubscriptionStatus.PAST_DUE
    
    def get_effective_price(self) -> float:
        """Get effective price after discounts"""
        base_price = self.annual_price if self.billing_cycle == "annual" else self.monthly_price
        
        if self.discount_percentage > 0:
            discount_amount = base_price * (self.discount_percentage / 100)
            return base_price - discount_amount
        
        return base_price
    
    def get_next_billing_date(self) -> datetime:
        """Get next billing date"""
        if self.billing_cycle == "annual":
            return self.current_period_end + timedelta(days=365)
        elif self.billing_cycle == "quarterly":
            return self.current_period_end + timedelta(days=90)
        else:  # monthly
            return self.current_period_end + timedelta(days=30)
    
    def get_days_until_renewal(self) -> int:
        """Get days until next renewal"""
        delta = self.current_period_end - datetime.now(datetime.UTC)
        return max(0, delta.days)
    
    def has_feature(self, feature_name: str) -> bool:
        """Check if subscription includes a feature"""
        return feature_name in self.features
    
    def is_within_limit(self, limit_type: str, current_usage: int) -> bool:
        """Check if current usage is within subscription limits"""
        limit = self.limits.get(limit_type, 0)
        return current_usage <= limit
    
    def get_usage_percentage(self, limit_type: str, current_usage: int) -> float:
        """Get usage percentage for a limit type"""
        limit = self.limits.get(limit_type, 1)
        if limit == 0:
            return 0.0
        return min(100.0, (current_usage / limit) * 100.0)
    
    def update_usage(self, usage_type: str, amount: int) -> None:
        """Update usage for current period"""
        if usage_type not in self.usage_this_period:
            self.usage_this_period[usage_type] = 0
        self.usage_this_period[usage_type] += amount
        self.updated_at = datetime.now(datetime.UTC)
    
    def reset_period_usage(self) -> None:
        """Reset usage counters for new billing period"""
        self.usage_this_period.clear()
        self.current_period_start = datetime.now(datetime.UTC)
        
        # Set next period end based on billing cycle
        if self.billing_cycle == "annual":
            self.current_period_end = datetime.now(datetime.UTC) + timedelta(days=365)
        elif self.billing_cycle == "quarterly":
            self.current_period_end = datetime.now(datetime.UTC) + timedelta(days=90)
        else:  # monthly
            self.current_period_end = datetime.now(datetime.UTC) + timedelta(days=30)
        
        self.updated_at = datetime.now(datetime.UTC)
    
    def cancel(self, effective_date: Optional[datetime] = None) -> None:
        """Cancel the subscription"""
        self.status = SubscriptionStatus.CANCELLED
        self.cancelled_at = effective_date or datetime.now(datetime.UTC)
        self.auto_renew = False
        self.updated_at = datetime.now(datetime.UTC)
    
    def reactivate(self) -> None:
        """Reactivate a cancelled subscription"""
        if self.status == SubscriptionStatus.CANCELLED:
            self.status = SubscriptionStatus.ACTIVE
            self.cancelled_at = None
            self.auto_renew = True
            self.updated_at = datetime.now(datetime.UTC)
    
    def upgrade_tier(self, new_tier: SubscriptionTier, new_plan_id: str) -> None:
        """Upgrade subscription to a new tier"""
        self.tier = new_tier
        self.plan_id = new_plan_id
        self.updated_at = datetime.now(datetime.UTC)
    
    def add_feature(self, feature_name: str) -> None:
        """Add a feature to the subscription"""
        if feature_name not in self.features:
            self.features.append(feature_name)
            self.updated_at = datetime.now(datetime.UTC)
    
    def remove_feature(self, feature_name: str) -> None:
        """Remove a feature from the subscription"""
        if feature_name in self.features:
            self.features.remove(feature_name)
            self.updated_at = datetime.now(datetime.UTC)
    
    def add_addon(self, addon_name: str, price: float, description: str = "") -> None:
        """Add an add-on to the subscription"""
        addon = {
            "name": addon_name,
            "price": price,
            "description": description,
            "added_at": datetime.now(datetime.UTC).isoformat()
        }
        self.add_ons.append(addon)
        self.updated_at = datetime.now(datetime.UTC)
    
    def remove_addon(self, addon_name: str) -> None:
        """Remove an add-on from the subscription"""
        self.add_ons = [addon for addon in self.add_ons if addon["name"] != addon_name]
        self.updated_at = datetime.now(datetime.UTC)
    
    def get_total_addon_price(self) -> float:
        """Get total price of all add-ons"""
        return sum(addon["price"] for addon in self.add_ons)
    
    def get_total_price(self) -> float:
        """Get total price including add-ons"""
        return self.get_effective_price() + self.get_total_addon_price()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert subscription to dictionary"""
        return {
            "subscription_id": self.subscription_id,
            "tenant_id": self.tenant_id,
            "plan_id": self.plan_id,
            "tier": self.tier.value,
            "status": self.status.value,
            "monthly_price": self.monthly_price,
            "annual_price": self.annual_price,
            "currency": self.currency,
            "billing_cycle": self.billing_cycle,
            "current_period_start": self.current_period_start.isoformat(),
            "current_period_end": self.current_period_end.isoformat(),
            "trial_start": self.trial_start.isoformat() if self.trial_start else None,
            "trial_end": self.trial_end.isoformat() if self.trial_end else None,
            "cancelled_at": self.cancelled_at.isoformat() if self.cancelled_at else None,
            "features": self.features,
            "limits": self.limits,
            "usage_this_period": self.usage_this_period,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "payment_method_id": self.payment_method_id,
            "billing_email": self.billing_email,
            "auto_renew": self.auto_renew,
            "custom_pricing": self.custom_pricing,
            "discount_percentage": self.discount_percentage,
            "add_ons": self.add_ons
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Subscription":
        """Create subscription from dictionary"""
        # Convert string dates back to datetime objects
        date_fields = [
            "current_period_start", "current_period_end", "trial_start", 
            "trial_end", "cancelled_at", "created_at", "updated_at"
        ]
        
        for field in date_fields:
            if data.get(field):
                data[field] = datetime.fromisoformat(data[field])
        
        # Convert enum values
        if data.get("tier"):
            data["tier"] = SubscriptionTier(data["tier"])
        if data.get("status"):
            data["status"] = SubscriptionStatus(data["status"])
        
        return cls(**data)
    
    def __str__(self) -> str:
        return f"Subscription({self.tier.value}: {self.status.value})"
    
    def __repr__(self) -> str:
        return f"Subscription(id='{self.subscription_id}', tier='{self.tier.value}', status='{self.status.value}')"
