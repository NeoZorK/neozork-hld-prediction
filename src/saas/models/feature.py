"""
Feature Model for SaaS Platform

This module defines the feature model which represents individual features
and capabilities available in the SaaS platform.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid


class FeatureType(Enum):
    """Feature type enumeration"""
    CORE = "core"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    ADDON = "addon"
    EXPERIMENTAL = "experimental"


class FeatureAccess(Enum):
    """Feature access enumeration"""
    FREE = "free"
    PAID = "paid"
    TRIAL = "trial"
    RESTRICTED = "restricted"


@dataclass
class Feature:
    """
    Feature model representing individual features and capabilities.
    
    Each feature includes:
    - Feature identification and description
    - Access level and pricing
    - Dependencies and requirements
    - Usage tracking and analytics
    - Configuration and settings
    """
    
    # Core identification
    feature_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    display_name: str = ""
    description: str = ""
    
    # Feature classification
    feature_type: FeatureType = FeatureType.CORE
    access_level: FeatureAccess = FeatureAccess.FREE
    
    # Pricing information
    price: float = 0.0
    currency: str = "USD"
    billing_frequency: str = "monthly"  # monthly, annual, one_time, usage_based
    
    # Feature details
    category: str = ""
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    
    # Dependencies and requirements
    dependencies: List[str] = field(default_factory=list)
    requirements: Dict[str, Any] = field(default_factory=dict)
    
    # Configuration
    settings: Dict[str, Any] = field(default_factory=dict)
    default_settings: Dict[str, Any] = field(default_factory=dict)
    
    # Usage tracking
    usage_metrics: List[str] = field(default_factory=list)
    usage_limits: Dict[str, int] = field(default_factory=dict)
    
    # Availability
    is_active: bool = True
    is_public: bool = True
    is_beta: bool = False
    is_deprecated: bool = False
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Documentation and support
    documentation_url: Optional[str] = None
    support_level: str = "standard"  # standard, priority, dedicated
    
    # Analytics and tracking
    usage_count: int = 0
    last_used: Optional[datetime] = None
    
    def __post_init__(self):
        """Post-initialization setup"""
        if not self.display_name:
            self.display_name = self.name
    
    def is_available(self) -> bool:
        """Check if feature is available"""
        return self.is_active and not self.is_deprecated
    
    def is_publicly_available(self) -> bool:
        """Check if feature is publicly available"""
        return self.is_available() and self.is_public
    
    def is_beta_feature(self) -> bool:
        """Check if feature is in beta"""
        return self.is_beta and self.is_available()
    
    def is_deprecated_feature(self) -> bool:
        """Check if feature is deprecated"""
        return self.is_deprecated
    
    def is_free(self) -> bool:
        """Check if feature is free"""
        return self.access_level == FeatureAccess.FREE
    
    def is_paid(self) -> bool:
        """Check if feature is paid"""
        return self.access_level == FeatureAccess.PAID
    
    def is_trial_available(self) -> bool:
        """Check if feature has trial access"""
        return self.access_level == FeatureAccess.TRIAL
    
    def is_restricted(self) -> bool:
        """Check if feature is restricted"""
        return self.access_level == FeatureAccess.RESTRICTED
    
    def has_dependency(self, dependency_name: str) -> bool:
        """Check if feature has a specific dependency"""
        return dependency_name in self.dependencies
    
    def add_dependency(self, dependency_name: str) -> None:
        """Add a dependency to the feature"""
        if dependency_name not in self.dependencies:
            self.dependencies.append(dependency_name)
            self.updated_at = datetime.now(datetime.UTC)
    
    def remove_dependency(self, dependency_name: str) -> None:
        """Remove a dependency from the feature"""
        if dependency_name in self.dependencies:
            self.dependencies.remove(dependency_name)
            self.updated_at = datetime.now(datetime.UTC)
    
    def has_tag(self, tag: str) -> bool:
        """Check if feature has a specific tag"""
        return tag in self.tags
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the feature"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now(datetime.UTC)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the feature"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now(datetime.UTC)
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set a feature setting"""
        self.settings[key] = value
        self.updated_at = datetime.now(datetime.UTC)
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a feature setting"""
        return self.settings.get(key, self.default_settings.get(key, default))
    
    def set_usage_limit(self, metric: str, limit: int) -> None:
        """Set usage limit for a metric"""
        self.usage_limits[metric] = limit
        self.updated_at = datetime.now(datetime.UTC)
    
    def get_usage_limit(self, metric: str, default: int = 0) -> int:
        """Get usage limit for a metric"""
        return self.usage_limits.get(metric, default)
    
    def is_within_usage_limit(self, metric: str, current_usage: int) -> bool:
        """Check if current usage is within limit"""
        limit = self.get_usage_limit(metric)
        if limit == -1:  # unlimited
            return True
        return current_usage <= limit
    
    def get_usage_percentage(self, metric: str, current_usage: int) -> float:
        """Get usage percentage for a metric"""
        limit = self.get_usage_limit(metric)
        if limit == -1:  # unlimited
            return 0.0
        if limit == 0:
            return 0.0
        return min(100.0, (current_usage / limit) * 100.0)
    
    def record_usage(self) -> None:
        """Record feature usage"""
        self.usage_count += 1
        self.last_used = datetime.now(datetime.UTC)
        self.updated_at = datetime.now(datetime.UTC)
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get feature usage statistics"""
        return {
            "usage_count": self.usage_count,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "usage_metrics": self.usage_metrics,
            "usage_limits": self.usage_limits
        }
    
    def get_pricing_info(self) -> Dict[str, Any]:
        """Get feature pricing information"""
        return {
            "price": self.price,
            "currency": self.currency,
            "billing_frequency": self.billing_frequency,
            "access_level": self.access_level.value,
            "is_free": self.is_free(),
            "is_paid": self.is_paid(),
            "trial_available": self.is_trial_available()
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get feature summary"""
        return {
            "feature_id": self.feature_id,
            "name": self.name,
            "display_name": self.display_name,
            "feature_type": self.feature_type.value,
            "access_level": self.access_level.value,
            "category": self.category,
            "version": self.version,
            "is_active": self.is_active,
            "is_public": self.is_public,
            "is_beta": self.is_beta,
            "is_deprecated": self.is_deprecated,
            "price": self.price,
            "currency": self.currency,
            "usage_count": self.usage_count,
            "tags": self.tags,
            "dependencies_count": len(self.dependencies)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert feature to dictionary"""
        return {
            "feature_id": self.feature_id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "feature_type": self.feature_type.value,
            "access_level": self.access_level.value,
            "price": self.price,
            "currency": self.currency,
            "billing_frequency": self.billing_frequency,
            "category": self.category,
            "tags": self.tags,
            "version": self.version,
            "dependencies": self.dependencies,
            "requirements": self.requirements,
            "settings": self.settings,
            "default_settings": self.default_settings,
            "usage_metrics": self.usage_metrics,
            "usage_limits": self.usage_limits,
            "is_active": self.is_active,
            "is_public": self.is_public,
            "is_beta": self.is_beta,
            "is_deprecated": self.is_deprecated,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "documentation_url": self.documentation_url,
            "support_level": self.support_level,
            "usage_count": self.usage_count,
            "last_used": self.last_used.isoformat() if self.last_used else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Feature":
        """Create feature from dictionary"""
        # Convert string dates back to datetime objects
        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        if data.get("last_used"):
            data["last_used"] = datetime.fromisoformat(data["last_used"])
        
        # Convert enum values
        if data.get("feature_type"):
            data["feature_type"] = FeatureType(data["feature_type"])
        if data.get("access_level"):
            data["access_level"] = FeatureAccess(data["access_level"])
        
        return cls(**data)
    
    def __str__(self) -> str:
        return f"Feature({self.name}: {self.feature_type.value})"
    
    def __repr__(self) -> str:
        return f"Feature(id='{self.feature_id}', name='{self.name}', type='{self.feature_type.value}')"
