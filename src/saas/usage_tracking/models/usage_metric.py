"""
Usage Metric Model

This model represents aggregated usage metrics and statistics
for tracking resource consumption over time.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from uuid import uuid4


class MetricType(Enum):
    """Types of usage metrics."""
    COUNTER = "counter"  # Incremental counter
    GAUGE = "gauge"      # Current value
    HISTOGRAM = "histogram"  # Distribution of values
    RATE = "rate"        # Rate of change
    PERCENTILE = "percentile"  # Percentile values


class MetricValue(Enum):
    """Types of metric values."""
    COUNT = "count"
    SUM = "sum"
    AVERAGE = "average"
    MIN = "min"
    MAX = "max"
    MEDIAN = "median"
    P95 = "p95"
    P99 = "p99"
    RATE = "rate"
    PERCENTAGE = "percentage"


@dataclass
class UsageMetric:
    """
    Represents an aggregated usage metric.
    
    This model stores pre-calculated metrics for efficient
    querying and reporting of usage data.
    """
    
    # Primary identifiers
    id: str = field(default_factory=lambda: str(uuid4()))
    tenant_id: str = ""
    metric_name: str = ""
    metric_type: MetricType = MetricType.COUNTER
    
    # Time period
    period_start: datetime = field(default_factory=datetime.utcnow)
    period_end: datetime = field(default_factory=lambda: datetime.now(datetime.UTC) + timedelta(hours=1))
    granularity: str = "hour"  # minute, hour, day, week, month
    
    # Metric values
    values: Dict[str, float] = field(default_factory=dict)
    value_type: MetricValue = MetricValue.COUNT
    
    # Resource information
    resource_type: str = ""  # e.g., "api_calls", "storage_gb"
    resource_id: Optional[str] = None
    
    # Aggregation details
    event_count: int = 0
    unique_users: int = 0
    unique_sessions: int = 0
    
    # Cost information
    total_cost: float = 0.0
    currency: str = "USD"
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate and set default values."""
        if not self.values:
            self.values = {self.value_type.value: 0.0}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "metric_name": self.metric_name,
            "metric_type": self.metric_type.value,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "granularity": self.granularity,
            "values": self.values,
            "value_type": self.value_type.value,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "event_count": self.event_count,
            "unique_users": self.unique_users,
            "unique_sessions": self.unique_sessions,
            "total_cost": self.total_cost,
            "currency": self.currency,
            "metadata": self.metadata,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UsageMetric":
        """Create from dictionary representation."""
        # Convert timestamp strings back to datetime objects
        for field_name in ["period_start", "period_end", "created_at", "updated_at"]:
            if isinstance(data.get(field_name), str):
                data[field_name] = datetime.fromisoformat(data[field_name])
        
        # Convert enum values
        if isinstance(data.get("metric_type"), str):
            data["metric_type"] = MetricType(data["metric_type"])
        if isinstance(data.get("value_type"), str):
            data["value_type"] = MetricValue(data["value_type"])
        
        return cls(**data)
    
    def get_value(self, value_type: Optional[MetricValue] = None) -> float:
        """Get metric value for specific type."""
        if value_type is None:
            value_type = self.value_type
        
        return self.values.get(value_type.value, 0.0)
    
    def set_value(self, value_type: MetricValue, value: float) -> None:
        """Set metric value for specific type."""
        self.values[value_type.value] = value
        self.updated_at = datetime.now(datetime.UTC)
    
    def increment_value(self, value_type: MetricValue, increment: float = 1.0) -> None:
        """Increment metric value."""
        current_value = self.get_value(value_type)
        self.set_value(value_type, current_value + increment)
    
    def add_event_data(self, event_count: int = 1, user_id: Optional[str] = None, 
                      session_id: Optional[str] = None, cost: float = 0.0) -> None:
        """Add data from a usage event."""
        self.event_count += event_count
        self.total_cost += cost
        
        if user_id and user_id not in self.metadata.get("user_ids", []):
            if "user_ids" not in self.metadata:
                self.metadata["user_ids"] = []
            self.metadata["user_ids"].append(user_id)
            self.unique_users = len(self.metadata["user_ids"])
        
        if session_id and session_id not in self.metadata.get("session_ids", []):
            if "session_ids" not in self.metadata:
                self.metadata["session_ids"] = []
            self.metadata["session_ids"].append(session_id)
            self.unique_sessions = len(self.metadata["session_ids"])
        
        self.updated_at = datetime.now(datetime.UTC)
    
    def calculate_rate(self, time_window: timedelta) -> float:
        """Calculate rate of events per time window."""
        if self.event_count == 0:
            return 0.0
        
        period_duration = (self.period_end - self.period_start).total_seconds()
        if period_duration == 0:
            return 0.0
        
        return self.event_count / (period_duration / time_window.total_seconds())
    
    def calculate_percentile(self, percentile: float) -> float:
        """Calculate percentile value from histogram data."""
        if self.metric_type != MetricType.HISTOGRAM:
            return 0.0
        
        histogram_data = self.metadata.get("histogram", {})
        if not histogram_data:
            return 0.0
        
        # Sort values and calculate percentile
        sorted_values = sorted(histogram_data.keys())
        total_count = sum(histogram_data.values())
        target_count = total_count * (percentile / 100.0)
        
        current_count = 0
        for value in sorted_values:
            current_count += histogram_data[value]
            if current_count >= target_count:
                return float(value)
        
        return float(sorted_values[-1]) if sorted_values else 0.0
    
    def merge_with(self, other: "UsageMetric") -> None:
        """Merge another metric into this one."""
        if (self.tenant_id != other.tenant_id or 
            self.metric_name != other.metric_name or
            self.resource_type != other.resource_type):
            raise ValueError("Cannot merge metrics with different identifiers")
        
        # Merge values
        for value_type, value in other.values.items():
            current_value = self.values.get(value_type, 0.0)
            self.values[value_type] = current_value + value
        
        # Merge counts
        self.event_count += other.event_count
        self.total_cost += other.total_cost
        
        # Merge unique users and sessions
        if "user_ids" not in self.metadata:
            self.metadata["user_ids"] = []
        if "session_ids" not in self.metadata:
            self.metadata["session_ids"] = []
        
        self.metadata["user_ids"].extend(other.metadata.get("user_ids", []))
        self.metadata["session_ids"].extend(other.metadata.get("session_ids", []))
        
        # Remove duplicates
        self.metadata["user_ids"] = list(set(self.metadata["user_ids"]))
        self.metadata["session_ids"] = list(set(self.metadata["session_ids"]))
        
        self.unique_users = len(self.metadata["user_ids"])
        self.unique_sessions = len(self.metadata["session_ids"])
        
        self.updated_at = datetime.now(datetime.UTC)
    
    def is_within_period(self, timestamp: datetime) -> bool:
        """Check if timestamp is within metric period."""
        return self.period_start <= timestamp <= self.period_end
    
    def get_duration(self) -> timedelta:
        """Get duration of the metric period."""
        return self.period_end - self.period_start
