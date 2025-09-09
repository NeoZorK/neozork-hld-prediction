"""
Notification System Data Models

This module defines Pydantic models for notification system data structures.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal
from enum import Enum
import uuid

from pydantic import BaseModel, Field, validator, EmailStr


class DeliveryStatus(str, Enum):
    """Notification delivery status enumeration."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


class NotificationPriority(str, Enum):
    """Notification priority enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class NotificationType(str, Enum):
    """Notification type enumeration."""
    TRADING_ALERT = "trading_alert"
    PRICE_ALERT = "price_alert"
    RISK_WARNING = "risk_warning"
    SYSTEM_MAINTENANCE = "system_maintenance"
    ACCOUNT_UPDATE = "account_update"
    SECURITY_ALERT = "security_alert"
    MARKET_ANALYSIS = "market_analysis"
    PORTFOLIO_REPORT = "portfolio_report"
    CUSTOM = "custom"


class ChannelType(str, Enum):
    """Notification channel type enumeration."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WEBHOOK = "webhook"
    IN_APP = "in_app"
    SLACK = "slack"
    TELEGRAM = "telegram"


class TemplateType(str, Enum):
    """Template type enumeration."""
    HTML = "html"
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"
    XML = "xml"


class RetryPolicy(BaseModel):
    """Retry policy configuration."""
    max_retries: int = Field(default=3, ge=0, le=10)
    retry_delay: int = Field(default=60, ge=1, le=3600)  # seconds
    backoff_multiplier: float = Field(default=2.0, ge=1.0, le=10.0)
    max_delay: int = Field(default=3600, ge=60, le=86400)  # seconds


class Notification(BaseModel):
    """Core notification model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    notification_type: NotificationType
    title: str
    message: str
    priority: NotificationPriority = NotificationPriority.NORMAL
    channels: List[ChannelType] = Field(default_factory=list)
    template_id: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None
    scheduled_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    retry_policy: Optional[RetryPolicy] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @validator('expires_at')
    def validate_expires_at(cls, v, values):
        if v and 'scheduled_at' in values and values['scheduled_at'] and v <= values['scheduled_at']:
            raise ValueError('Expires at must be after scheduled at')
        return v

    @validator('channels')
    def validate_channels(cls, v):
        if not v:
            raise ValueError('At least one channel must be specified')
        return v


class NotificationTemplate(BaseModel):
    """Notification template model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    notification_type: NotificationType
    template_type: TemplateType
    subject_template: Optional[str] = None
    body_template: str
    channels: List[ChannelType] = Field(default_factory=list)
    variables: List[str] = Field(default_factory=list)
    is_active: bool = True
    version: int = Field(default=1, ge=1)
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @validator('body_template')
    def validate_body_template(cls, v):
        if not v or not v.strip():
            raise ValueError('Body template cannot be empty')
        return v


class NotificationChannel(BaseModel):
    """Notification channel configuration."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    channel_type: ChannelType
    name: str
    description: Optional[str] = None
    configuration: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True
    rate_limit: Optional[int] = None  # notifications per minute
    priority: int = Field(default=1, ge=1, le=10)
    retry_policy: Optional[RetryPolicy] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @validator('configuration')
    def validate_configuration(cls, v, values):
        if 'channel_type' in values:
            channel_type = values['channel_type']
            if channel_type == ChannelType.EMAIL:
                required_fields = ['smtp_host', 'smtp_port', 'username', 'password']
                for field in required_fields:
                    if field not in v:
                        raise ValueError(f'Email channel requires {field} in configuration')
            elif channel_type == ChannelType.SMS:
                required_fields = ['api_key', 'api_secret']
                for field in required_fields:
                    if field not in v:
                        raise ValueError(f'SMS channel requires {field} in configuration')
        return v


class NotificationPreference(BaseModel):
    """User notification preferences."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    notification_type: NotificationType
    channels: List[ChannelType] = Field(default_factory=list)
    is_enabled: bool = True
    quiet_hours_start: Optional[str] = None  # HH:MM format
    quiet_hours_end: Optional[str] = None    # HH:MM format
    timezone: str = Field(default="UTC")
    frequency_limit: Optional[int] = None    # max notifications per hour
    priority_threshold: NotificationPriority = NotificationPriority.LOW
    custom_settings: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @validator('quiet_hours_start', 'quiet_hours_end')
    def validate_quiet_hours(cls, v):
        if v:
            try:
                datetime.strptime(v, '%H:%M')
            except ValueError:
                raise ValueError('Quiet hours must be in HH:MM format')
        return v


class NotificationHistory(BaseModel):
    """Notification delivery history."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    notification_id: str
    user_id: str
    channel: ChannelType
    status: DeliveryStatus
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = Field(default=0, ge=0)
    delivery_attempts: List[datetime] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)

    @validator('delivered_at')
    def validate_delivered_at(cls, v, values):
        if v and 'sent_at' in values and values['sent_at'] and v < values['sent_at']:
            raise ValueError('Delivered at cannot be before sent at')
        return v


class NotificationEvent(BaseModel):
    """Event-triggered notification."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    event_data: Dict[str, Any]
    user_id: Optional[str] = None
    user_group: Optional[str] = None
    template_id: str
    priority: NotificationPriority = NotificationPriority.NORMAL
    delay: Optional[int] = None  # seconds
    conditions: Optional[Dict[str, Any]] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class NotificationMetrics(BaseModel):
    """Notification system metrics."""
    total_sent: int = Field(default=0, ge=0)
    total_delivered: int = Field(default=0, ge=0)
    total_failed: int = Field(default=0, ge=0)
    delivery_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    average_delivery_time: float = Field(default=0.0, ge=0.0)  # seconds
    channel_metrics: Dict[ChannelType, Dict[str, int]] = Field(default_factory=dict)
    type_metrics: Dict[NotificationType, Dict[str, int]] = Field(default_factory=dict)
    period_start: datetime
    period_end: datetime
    generated_at: datetime = Field(default_factory=datetime.now)

    @validator('delivery_rate')
    def validate_delivery_rate(cls, v, values):
        if 'total_sent' in values and values['total_sent'] > 0:
            expected_rate = values.get('total_delivered', 0) / values['total_sent']
            if abs(v - expected_rate) > 0.01:  # Allow small floating point differences
                raise ValueError('Delivery rate must match delivered/sent ratio')
        return v
