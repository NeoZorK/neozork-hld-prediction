"""
Usage Limit Model

This model represents usage limits and quotas for tenants,
including enforcement rules and violation handling.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from uuid import uuid4


class LimitType(Enum):
    """Types of usage limits."""
    HARD_LIMIT = "hard_limit"      # Hard stop when exceeded
    SOFT_LIMIT = "soft_limit"      # Warning when exceeded
    RATE_LIMIT = "rate_limit"      # Rate-based limiting
    BURST_LIMIT = "burst_limit"    # Burst capacity limit
    DAILY_LIMIT = "daily_limit"    # Daily usage limit
    MONTHLY_LIMIT = "monthly_limit"  # Monthly usage limit
    ANNUAL_LIMIT = "annual_limit"  # Annual usage limit


class LimitStatus(Enum):
    """Status of usage limits."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    VIOLATED = "violated"


@dataclass
class UsageLimit:
    """
    Represents a usage limit or quota for a tenant.
    
    This model defines limits on resource consumption and
    provides enforcement mechanisms.
    """
    
    # Primary identifiers
    id: str = field(default_factory=lambda: str(uuid4()))
    tenant_id: str = ""
    limit_name: str = ""
    limit_type: LimitType = LimitType.HARD_LIMIT
    
    # Resource information
    resource_type: str = ""  # e.g., "api_calls", "storage_gb"
    resource_id: Optional[str] = None
    
    # Limit values
    limit_value: float = 0.0
    unit: str = ""  # e.g., "calls", "gb", "seconds"
    
    # Time period
    period_type: str = "month"  # minute, hour, day, week, month, year
    period_value: int = 1  # Number of periods
    
    # Enforcement
    status: LimitStatus = LimitStatus.ACTIVE
    enforce_immediately: bool = True
    grace_period_minutes: int = 0
    
    # Violation handling
    violation_action: str = "block"  # block, throttle, warn, notify
    violation_message: str = "Usage limit exceeded"
    violation_webhook_url: Optional[str] = None
    
    # Notifications
    warning_threshold: float = 0.8  # 80% of limit
    warning_message: str = "Approaching usage limit"
    notification_emails: List[str] = field(default_factory=list)
    notification_webhook_url: Optional[str] = None
    
    # Metadata
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    
    # Current usage (calculated)
    current_usage: float = 0.0
    usage_percentage: float = 0.0
    last_updated: Optional[datetime] = None
    
    def __post_init__(self):
        """Calculate derived values after initialization."""
        self._calculate_usage_percentage()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "limit_name": self.limit_name,
            "limit_type": self.limit_type.value,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "limit_value": self.limit_value,
            "unit": self.unit,
            "period_type": self.period_type,
            "period_value": self.period_value,
            "status": self.status.value,
            "enforce_immediately": self.enforce_immediately,
            "grace_period_minutes": self.grace_period_minutes,
            "violation_action": self.violation_action,
            "violation_message": self.violation_message,
            "violation_webhook_url": self.violation_webhook_url,
            "warning_threshold": self.warning_threshold,
            "warning_message": self.warning_message,
            "notification_emails": self.notification_emails,
            "notification_webhook_url": self.notification_webhook_url,
            "description": self.description,
            "metadata": self.metadata,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "current_usage": self.current_usage,
            "usage_percentage": self.usage_percentage,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UsageLimit":
        """Create from dictionary representation."""
        # Convert timestamp strings back to datetime objects
        for field_name in ["created_at", "updated_at", "expires_at", "last_updated"]:
            if isinstance(data.get(field_name), str):
                data[field_name] = datetime.fromisoformat(data[field_name])
        
        # Convert enum values
        if isinstance(data.get("limit_type"), str):
            data["limit_type"] = LimitType(data["limit_type"])
        if isinstance(data.get("status"), str):
            data["status"] = LimitStatus(data["status"])
        
        return cls(**data)
    
    def _calculate_usage_percentage(self) -> None:
        """Calculate usage percentage."""
        if self.limit_value > 0:
            self.usage_percentage = (self.current_usage / self.limit_value) * 100
        else:
            self.usage_percentage = 0.0
    
    def update_usage(self, usage: float) -> None:
        """Update current usage and recalculate percentage."""
        self.current_usage = usage
        self.last_updated = datetime.utcnow()
        self._calculate_usage_percentage()
        self.updated_at = datetime.utcnow()
    
    def is_exceeded(self) -> bool:
        """Check if limit is exceeded."""
        return self.current_usage > self.limit_value
    
    def is_warning_threshold_reached(self) -> bool:
        """Check if warning threshold is reached."""
        return self.usage_percentage >= (self.warning_threshold * 100)
    
    def is_violated(self) -> bool:
        """Check if limit is violated (exceeded and enforcement is active)."""
        return self.is_exceeded() and self.status == LimitStatus.ACTIVE
    
    def get_remaining_usage(self) -> float:
        """Get remaining usage before limit is reached."""
        return max(0, self.limit_value - self.current_usage)
    
    def get_usage_until_warning(self) -> float:
        """Get usage until warning threshold is reached."""
        warning_usage = self.limit_value * self.warning_threshold
        return max(0, warning_usage - self.current_usage)
    
    def get_period_start(self) -> datetime:
        """Get start of current period."""
        now = datetime.utcnow()
        
        if self.period_type == "minute":
            return now.replace(second=0, microsecond=0)
        elif self.period_type == "hour":
            return now.replace(minute=0, second=0, microsecond=0)
        elif self.period_type == "day":
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.period_type == "week":
            days_since_monday = now.weekday()
            return (now - timedelta(days=days_since_monday)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif self.period_type == "month":
            return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif self.period_type == "year":
            return now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            return now
    
    def get_period_end(self) -> datetime:
        """Get end of current period."""
        period_start = self.get_period_start()
        
        if self.period_type == "minute":
            return period_start + timedelta(minutes=self.period_value)
        elif self.period_type == "hour":
            return period_start + timedelta(hours=self.period_value)
        elif self.period_type == "day":
            return period_start + timedelta(days=self.period_value)
        elif self.period_type == "week":
            return period_start + timedelta(weeks=self.period_value)
        elif self.period_type == "month":
            # Approximate month as 30 days
            return period_start + timedelta(days=30 * self.period_value)
        elif self.period_type == "year":
            # Approximate year as 365 days
            return period_start + timedelta(days=365 * self.period_value)
        else:
            return period_start + timedelta(hours=1)
    
    def is_expired(self) -> bool:
        """Check if limit has expired."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    def is_active(self) -> bool:
        """Check if limit is active."""
        return (self.status == LimitStatus.ACTIVE and 
                not self.is_expired())
    
    def should_enforce(self) -> bool:
        """Check if limit should be enforced."""
        return (self.is_violated() and 
                self.enforce_immediately and
                self.is_active())
    
    def get_violation_severity(self) -> str:
        """Get violation severity level."""
        if not self.is_exceeded():
            return "none"
        
        excess_percentage = ((self.current_usage - self.limit_value) / self.limit_value) * 100
        
        if excess_percentage <= 10:
            return "low"
        elif excess_percentage <= 50:
            return "medium"
        else:
            return "high"
    
    def add_notification_email(self, email: str) -> None:
        """Add notification email."""
        if email not in self.notification_emails:
            self.notification_emails.append(email)
            self.updated_at = datetime.utcnow()
    
    def remove_notification_email(self, email: str) -> None:
        """Remove notification email."""
        if email in self.notification_emails:
            self.notification_emails.remove(email)
            self.updated_at = datetime.utcnow()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the limit."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the limit."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()
    
    def suspend(self) -> None:
        """Suspend the limit."""
        self.status = LimitStatus.SUSPENDED
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate the limit."""
        self.status = LimitStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate the limit."""
        self.status = LimitStatus.INACTIVE
        self.updated_at = datetime.utcnow()
