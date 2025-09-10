"""
Plan Model for SaaS Platform

This module defines the plan model which represents subscription plans
and pricing tiers available in the SaaS platform.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid


class PlanType(Enum):
    """Plan type enumeration"""
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    INSTITUTIONAL = "institutional"
    CUSTOM = "custom"


class PlanStatus(Enum):
    """Plan status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    DRAFT = "draft"


@dataclass
class Plan:
    """
    Plan model representing subscription plans and pricing tiers.
    
    Each plan includes:
    - Pricing and billing information
    - Feature access and limits
    - Usage quotas and restrictions
    - Terms and conditions
    - Availability and targeting
    """
    
    # Core identification
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    display_name: str = ""
    description: str = ""
    
    # Plan classification
    plan_type: PlanType = PlanType.STARTER
    status: PlanStatus = PlanStatus.DRAFT
    
    # Pricing information
    monthly_price: float = 0.0
    annual_price: float = 0.0
    currency: str = "USD"
    billing_cycle: str = "monthly"  # monthly, annual, quarterly
    
    # Features and limits
    features: List[str] = field(default_factory=list)
    limits: Dict[str, int] = field(default_factory=dict)
    
    # Usage quotas
    api_calls_per_month: int = 0
    storage_gb: int = 0
    max_users: int = 1
    max_strategies: int = 0
    max_backtests: int = 0
    
    # Trial information
    trial_days: int = 0
    trial_features: List[str] = field(default_factory=list)
    
    # Terms and conditions
    terms: Optional[str] = None
    cancellation_policy: Optional[str] = None
    refund_policy: Optional[str] = None
    
    # Availability
    is_public: bool = True
    is_featured: bool = False
    target_audience: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Custom pricing (for enterprise plans)
    custom_pricing_available: bool = False
    minimum_commitment: Optional[str] = None
    
    # Add-ons and extras
    available_addons: List[Dict[str, Any]] = field(default_factory=list)
    
    # Support and service level
    support_level: str = "standard"  # standard, priority, dedicated
    sla_uptime: float = 99.9  # percentage
    
    def __post_init__(self):
        """Post-initialization setup"""
        if not self.display_name:
            self.display_name = self.name
        
        # Set default limits based on plan type
        self._set_default_limits()
    
    def _set_default_limits(self) -> None:
        """Set default limits based on plan type"""
        default_limits = {
            PlanType.STARTER: {
                "api_calls_per_month": 10000,
                "storage_gb": 1,
                "max_users": 1,
                "max_strategies": 5,
                "max_backtests": 10
            },
            PlanType.PROFESSIONAL: {
                "api_calls_per_month": 100000,
                "storage_gb": 10,
                "max_users": 5,
                "max_strategies": 25,
                "max_backtests": 100
            },
            PlanType.ENTERPRISE: {
                "api_calls_per_month": 1000000,
                "storage_gb": 100,
                "max_users": 50,
                "max_strategies": -1,  # unlimited
                "max_backtests": -1  # unlimited
            },
            PlanType.INSTITUTIONAL: {
                "api_calls_per_month": -1,  # unlimited
                "storage_gb": -1,  # unlimited
                "max_users": -1,  # unlimited
                "max_strategies": -1,  # unlimited
                "max_backtests": -1  # unlimited
            }
        }
        
        if self.plan_type in default_limits:
            limits = default_limits[self.plan_type]
            self.api_calls_per_month = limits["api_calls_per_month"]
            self.storage_gb = limits["storage_gb"]
            self.max_users = limits["max_users"]
            self.max_strategies = limits["max_strategies"]
            self.max_backtests = limits["max_backtests"]
    
    def is_active(self) -> bool:
        """Check if plan is active"""
        return self.status == PlanStatus.ACTIVE
    
    def is_publicly_available(self) -> bool:
        """Check if plan is publicly available"""
        return self.is_public and self.is_active()
    
    def is_featured(self) -> bool:
        """Check if plan is featured"""
        return self.is_featured and self.is_active()
    
    def has_trial(self) -> bool:
        """Check if plan includes trial period"""
        return self.trial_days > 0
    
    def get_effective_price(self, billing_cycle: str = None) -> float:
        """Get effective price for billing cycle"""
        if billing_cycle is None:
            billing_cycle = self.billing_cycle
        
        if billing_cycle == "annual":
            return self.annual_price
        else:
            return self.monthly_price
    
    def get_annual_savings(self) -> float:
        """Get annual savings compared to monthly billing"""
        if self.annual_price == 0 or self.monthly_price == 0:
            return 0.0
        
        monthly_annual_cost = self.monthly_price * 12
        return monthly_annual_cost - self.annual_price
    
    def get_annual_savings_percentage(self) -> float:
        """Get annual savings percentage"""
        if self.annual_price == 0 or self.monthly_price == 0:
            return 0.0
        
        monthly_annual_cost = self.monthly_price * 12
        if monthly_annual_cost == 0:
            return 0.0
        
        return (self.get_annual_savings() / monthly_annual_cost) * 100
    
    def has_feature(self, feature_name: str) -> bool:
        """Check if plan includes a feature"""
        return feature_name in self.features
    
    def add_feature(self, feature_name: str) -> None:
        """Add a feature to the plan"""
        if feature_name not in self.features:
            self.features.append(feature_name)
            self.updated_at = datetime.utcnow()
    
    def remove_feature(self, feature_name: str) -> None:
        """Remove a feature from the plan"""
        if feature_name in self.features:
            self.features.remove(feature_name)
            self.updated_at = datetime.utcnow()
    
    def set_limit(self, limit_type: str, value: int) -> None:
        """Set a limit for the plan"""
        self.limits[limit_type] = value
        self.updated_at = datetime.utcnow()
    
    def get_limit(self, limit_type: str, default: int = 0) -> int:
        """Get a limit for the plan"""
        return self.limits.get(limit_type, default)
    
    def is_within_limit(self, limit_type: str, current_usage: int) -> bool:
        """Check if current usage is within plan limits"""
        limit = self.get_limit(limit_type)
        if limit == -1:  # unlimited
            return True
        return current_usage <= limit
    
    def get_usage_percentage(self, limit_type: str, current_usage: int) -> float:
        """Get usage percentage for a limit type"""
        limit = self.get_limit(limit_type)
        if limit == -1:  # unlimited
            return 0.0
        if limit == 0:
            return 0.0
        return min(100.0, (current_usage / limit) * 100.0)
    
    def add_addon(self, addon_name: str, price: float, description: str = "") -> None:
        """Add an add-on to the plan"""
        addon = {
            "id": str(uuid.uuid4()),
            "name": addon_name,
            "price": price,
            "description": description,
            "created_at": datetime.utcnow().isoformat()
        }
        self.available_addons.append(addon)
        self.updated_at = datetime.utcnow()
    
    def remove_addon(self, addon_id: str) -> None:
        """Remove an add-on from the plan"""
        self.available_addons = [addon for addon in self.available_addons if addon["id"] != addon_id]
        self.updated_at = datetime.utcnow()
    
    def get_addon(self, addon_id: str) -> Optional[Dict[str, Any]]:
        """Get an add-on by ID"""
        for addon in self.available_addons:
            if addon["id"] == addon_id:
                return addon
        return None
    
    def is_suitable_for_audience(self, audience: str) -> bool:
        """Check if plan is suitable for target audience"""
        return not self.target_audience or audience in self.target_audience
    
    def get_summary(self) -> Dict[str, Any]:
        """Get plan summary"""
        return {
            "plan_id": self.plan_id,
            "name": self.name,
            "display_name": self.display_name,
            "plan_type": self.plan_type.value,
            "status": self.status.value,
            "monthly_price": self.monthly_price,
            "annual_price": self.annual_price,
            "currency": self.currency,
            "trial_days": self.trial_days,
            "max_users": self.max_users,
            "api_calls_per_month": self.api_calls_per_month,
            "storage_gb": self.storage_gb,
            "features_count": len(self.features),
            "is_public": self.is_public,
            "is_featured": self.is_featured,
            "support_level": self.support_level,
            "sla_uptime": self.sla_uptime
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert plan to dictionary"""
        return {
            "plan_id": self.plan_id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "plan_type": self.plan_type.value,
            "status": self.status.value,
            "monthly_price": self.monthly_price,
            "annual_price": self.annual_price,
            "currency": self.currency,
            "billing_cycle": self.billing_cycle,
            "features": self.features,
            "limits": self.limits,
            "api_calls_per_month": self.api_calls_per_month,
            "storage_gb": self.storage_gb,
            "max_users": self.max_users,
            "max_strategies": self.max_strategies,
            "max_backtests": self.max_backtests,
            "trial_days": self.trial_days,
            "trial_features": self.trial_features,
            "terms": self.terms,
            "cancellation_policy": self.cancellation_policy,
            "refund_policy": self.refund_policy,
            "is_public": self.is_public,
            "is_featured": self.is_featured,
            "target_audience": self.target_audience,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "custom_pricing_available": self.custom_pricing_available,
            "minimum_commitment": self.minimum_commitment,
            "available_addons": self.available_addons,
            "support_level": self.support_level,
            "sla_uptime": self.sla_uptime
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Plan":
        """Create plan from dictionary"""
        # Convert string dates back to datetime objects
        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        # Convert enum values
        if data.get("plan_type"):
            data["plan_type"] = PlanType(data["plan_type"])
        if data.get("status"):
            data["status"] = PlanStatus(data["status"])
        
        return cls(**data)
    
    def __str__(self) -> str:
        return f"Plan({self.name}: {self.plan_type.value})"
    
    def __repr__(self) -> str:
        return f"Plan(id='{self.plan_id}', name='{self.name}', type='{self.plan_type.value}')"
