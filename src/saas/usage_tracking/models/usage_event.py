"""
Usage Event Model

This model represents individual usage events in the system,
tracking when and how resources are consumed.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from uuid import uuid4


class EventType(Enum):
    """Types of usage events."""
    API_CALL = "api_call"
    STORAGE_READ = "storage_read"
    STORAGE_WRITE = "storage_write"
    DATABASE_QUERY = "database_query"
    FILE_UPLOAD = "file_upload"
    FILE_DOWNLOAD = "file_download"
    EMAIL_SENT = "email_sent"
    SMS_SENT = "sms_sent"
    PUSH_NOTIFICATION = "push_notification"
    WEBHOOK_CALL = "webhook_call"
    CUSTOM_EVENT = "custom_event"


class EventStatus(Enum):
    """Status of usage events."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class UsageEvent:
    """
    Represents a single usage event in the system.
    
    This model tracks individual resource consumption events,
    including metadata, timing, and associated costs.
    """
    
    # Primary identifiers
    id: str = field(default_factory=lambda: str(uuid4()))
    tenant_id: str = ""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    
    # Event details
    event_type: EventType = EventType.API_CALL
    event_name: str = ""
    description: str = ""
    
    # Resource consumption
    resource_consumed: str = ""  # e.g., "api_calls", "storage_gb", "compute_seconds"
    quantity: float = 0.0
    unit: str = ""  # e.g., "calls", "gb", "seconds"
    
    # Cost information
    cost_per_unit: float = 0.0
    total_cost: float = 0.0
    currency: str = "USD"
    
    # Timing
    timestamp: datetime = field(default_factory=datetime.utcnow)
    duration_ms: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Status and metadata
    status: EventStatus = EventStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    
    # Error information
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    
    # Source information
    source_ip: Optional[str] = None
    user_agent: Optional[str] = None
    api_version: Optional[str] = None
    
    # Related entities
    related_event_id: Optional[str] = None
    parent_event_id: Optional[str] = None
    
    def __post_init__(self):
        """Calculate total cost after initialization."""
        if self.quantity > 0 and self.cost_per_unit > 0:
            self.total_cost = self.quantity * self.cost_per_unit
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "event_type": self.event_type.value,
            "event_name": self.event_name,
            "description": self.description,
            "resource_consumed": self.resource_consumed,
            "quantity": self.quantity,
            "unit": self.unit,
            "cost_per_unit": self.cost_per_unit,
            "total_cost": self.total_cost,
            "currency": self.currency,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status.value,
            "metadata": self.metadata,
            "tags": self.tags,
            "error_code": self.error_code,
            "error_message": self.error_message,
            "source_ip": self.source_ip,
            "user_agent": self.user_agent,
            "api_version": self.api_version,
            "related_event_id": self.related_event_id,
            "parent_event_id": self.parent_event_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UsageEvent":
        """Create from dictionary representation."""
        # Convert timestamp strings back to datetime objects
        if isinstance(data.get("timestamp"), str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        if isinstance(data.get("start_time"), str):
            data["start_time"] = datetime.fromisoformat(data["start_time"])
        if isinstance(data.get("end_time"), str):
            data["end_time"] = datetime.fromisoformat(data["end_time"])
        
        # Convert enum values
        if isinstance(data.get("event_type"), str):
            data["event_type"] = EventType(data["event_type"])
        if isinstance(data.get("status"), str):
            data["status"] = EventStatus(data["status"])
        
        return cls(**data)
    
    def is_completed(self) -> bool:
        """Check if event is completed."""
        return self.status == EventStatus.COMPLETED
    
    def is_failed(self) -> bool:
        """Check if event failed."""
        return self.status == EventStatus.FAILED
    
    def is_pending(self) -> bool:
        """Check if event is pending."""
        return self.status == EventStatus.PENDING
    
    def mark_completed(self) -> None:
        """Mark event as completed."""
        self.status = EventStatus.COMPLETED
        if self.start_time and not self.end_time:
            self.end_time = datetime.now(datetime.UTC)
            if self.duration_ms is None:
                self.duration_ms = int((self.end_time - self.start_time).total_seconds() * 1000)
    
    def mark_failed(self, error_code: str, error_message: str) -> None:
        """Mark event as failed with error details."""
        self.status = EventStatus.FAILED
        self.error_code = error_code
        self.error_message = error_message
        if self.start_time and not self.end_time:
            self.end_time = datetime.now(datetime.UTC)
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the event."""
        self.metadata[key] = value
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the event."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def get_cost_in_currency(self, target_currency: str, exchange_rate: float) -> float:
        """Get cost in target currency using exchange rate."""
        if self.currency == target_currency:
            return self.total_cost
        return self.total_cost * exchange_rate
