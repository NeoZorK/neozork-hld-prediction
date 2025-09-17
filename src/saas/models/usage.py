"""
Usage Model for SaaS Platform

This module defines the usage model which tracks customer usage of platform
features, API calls, and resource consumption for billing and analytics.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid


class UsageType(Enum):
    """Usage type enumeration"""
    API_CALL = "api_call"
    STORAGE = "storage"
    COMPUTE = "compute"
    BANDWIDTH = "bandwidth"
    FEATURE_ACCESS = "feature_access"
    USER_SESSION = "user_session"
    DATA_EXPORT = "data_export"
    CUSTOM_QUERY = "custom_query"


class UsageMetric(Enum):
    """Usage metric enumeration"""
    COUNT = "count"
    BYTES = "bytes"
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    GIGABYTES = "gigabytes"
    MEGABYTES = "megabytes"
    KILOBYTES = "kilobytes"


@dataclass
class Usage:
    """
    Usage model representing customer usage of platform resources and features.
    
    Each usage record includes:
    - Resource type and consumption amount
    - Timestamp and billing period
    - Associated tenant and customer
    - Cost calculation and billing information
    - Metadata and context
    """
    
    # Core identification
    usage_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    customer_id: Optional[str] = None
    subscription_id: Optional[str] = None
    
    # Usage details
    usage_type: UsageType = UsageType.API_CALL
    metric: UsageMetric = UsageMetric.COUNT
    amount: float = 0.0
    unit: str = ""
    
    # Resource information
    resource_id: Optional[str] = None
    resource_name: Optional[str] = None
    feature_name: Optional[str] = None
    
    # Cost and billing
    cost_per_unit: float = 0.0
    total_cost: float = 0.0
    currency: str = "USD"
    billable: bool = True
    
    # Timestamp information
    timestamp: datetime = field(default_factory=datetime.utcnow)
    billing_period_start: datetime = field(default_factory=datetime.utcnow)
    billing_period_end: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30))
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    # Context information
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    api_endpoint: Optional[str] = None
    request_id: Optional[str] = None
    
    # Processing status
    processed: bool = False
    processed_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Post-initialization setup"""
        # Calculate total cost if not set
        if self.total_cost == 0.0 and self.cost_per_unit > 0:
            self.total_cost = self.amount * self.cost_per_unit
        
        # Set unit based on metric if not specified
        if not self.unit:
            self.unit = self._get_default_unit()
    
    def _get_default_unit(self) -> str:
        """Get default unit based on metric"""
        unit_mapping = {
            UsageMetric.COUNT: "calls",
            UsageMetric.BYTES: "bytes",
            UsageMetric.SECONDS: "seconds",
            UsageMetric.MINUTES: "minutes",
            UsageMetric.HOURS: "hours",
            UsageMetric.GIGABYTES: "GB",
            UsageMetric.MEGABYTES: "MB",
            UsageMetric.KILOBYTES: "KB"
        }
        return unit_mapping.get(self.metric, "units")
    
    def is_billable(self) -> bool:
        """Check if usage is billable"""
        return self.billable and self.total_cost > 0
    
    def is_processed(self) -> bool:
        """Check if usage has been processed"""
        return self.processed
    
    def is_in_billing_period(self, date: Optional[datetime] = None) -> bool:
        """Check if usage is within billing period"""
        if date is None:
            date = datetime.now(timezone.utc)
        return self.billing_period_start <= date <= self.billing_period_end
    
    def get_cost_breakdown(self) -> Dict[str, float]:
        """Get cost breakdown"""
        return {
            "amount": self.amount,
            "cost_per_unit": self.cost_per_unit,
            "total_cost": self.total_cost,
            "currency": self.currency
        }
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to usage record"""
        self.metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value"""
        return self.metadata.get(key, default)
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to usage record"""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from usage record"""
        if tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if usage record has a specific tag"""
        return tag in self.tags
    
    def mark_as_processed(self) -> None:
        """Mark usage as processed"""
        self.processed = True
        self.processed_at = datetime.now(timezone.utc)
    
    def update_cost(self, cost_per_unit: float) -> None:
        """Update cost information"""
        self.cost_per_unit = cost_per_unit
        self.total_cost = self.amount * cost_per_unit
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert usage to dictionary"""
        return {
            "usage_id": self.usage_id,
            "tenant_id": self.tenant_id,
            "customer_id": self.customer_id,
            "subscription_id": self.subscription_id,
            "usage_type": self.usage_type.value,
            "metric": self.metric.value,
            "amount": self.amount,
            "unit": self.unit,
            "resource_id": self.resource_id,
            "resource_name": self.resource_name,
            "feature_name": self.feature_name,
            "cost_per_unit": self.cost_per_unit,
            "total_cost": self.total_cost,
            "currency": self.currency,
            "billable": self.billable,
            "timestamp": self.timestamp.isoformat(),
            "billing_period_start": self.billing_period_start.isoformat(),
            "billing_period_end": self.billing_period_end.isoformat(),
            "metadata": self.metadata,
            "tags": self.tags,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "api_endpoint": self.api_endpoint,
            "request_id": self.request_id,
            "processed": self.processed,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Usage":
        """Create usage from dictionary"""
        # Convert string dates back to datetime objects
        date_fields = [
            "timestamp", "billing_period_start", "billing_period_end", "processed_at"
        ]
        
        for field in date_fields:
            if data.get(field):
                data[field] = datetime.fromisoformat(data[field])
        
        # Convert enum values
        if data.get("usage_type"):
            data["usage_type"] = UsageType(data["usage_type"])
        if data.get("metric"):
            data["metric"] = UsageMetric(data["metric"])
        
        return cls(**data)
    
    def __str__(self) -> str:
        return f"Usage({self.usage_type.value}: {self.amount} {self.unit})"
    
    def __repr__(self) -> str:
        return f"Usage(id='{self.usage_id}', type='{self.usage_type.value}', amount={self.amount})"


@dataclass
class UsageAggregate:
    """
    Usage aggregate model for summarizing usage data over time periods.
    """
    
    # Core identification
    aggregate_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    
    # Aggregation details
    usage_type: UsageType = UsageType.API_CALL
    metric: UsageMetric = UsageMetric.COUNT
    period_start: datetime = field(default_factory=datetime.utcnow)
    period_end: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=1))
    
    # Aggregated values
    total_amount: float = 0.0
    total_cost: float = 0.0
    count: int = 0
    average_amount: float = 0.0
    min_amount: float = 0.0
    max_amount: float = 0.0
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_usage(self, usage: Usage) -> None:
        """Add usage to aggregate"""
        self.total_amount += usage.amount
        self.total_cost += usage.total_cost
        self.count += 1
        
        if self.count == 1:
            self.min_amount = usage.amount
            self.max_amount = usage.amount
        else:
            self.min_amount = min(self.min_amount, usage.amount)
            self.max_amount = max(self.max_amount, usage.amount)
        
        self.average_amount = self.total_amount / self.count
        self.updated_at = datetime.now(timezone.utc)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get usage aggregate summary"""
        return {
            "aggregate_id": self.aggregate_id,
            "tenant_id": self.tenant_id,
            "usage_type": self.usage_type.value,
            "metric": self.metric.value,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "total_amount": self.total_amount,
            "total_cost": self.total_cost,
            "count": self.count,
            "average_amount": self.average_amount,
            "min_amount": self.min_amount,
            "max_amount": self.max_amount
        }
