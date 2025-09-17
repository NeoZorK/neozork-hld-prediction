"""
Notification System Data Models

This module contains Pydantic models for notification system data structures:
- Notification: Core notification data model
- NotificationTemplate: Template for generating notifications
- NotificationChannel: Channel configuration and settings
- NotificationPreference: User notification preferences
- NotificationHistory: Historical notification records
- NotificationEvent: Event-triggered notifications
"""

from .notification_models import (
    Notification,
    NotificationTemplate,
    NotificationChannel,
    NotificationPreference,
    NotificationHistory,
    NotificationEvent,
    DeliveryStatus,
    NotificationPriority,
    NotificationType,
    ChannelType,
    TemplateType,
    RetryPolicy,
    NotificationMetrics
)

__all__ = [
    "Notification",
    "NotificationTemplate",
    "NotificationChannel",
    "NotificationPreference",
    "NotificationHistory",
    "NotificationEvent",
    "DeliveryStatus",
    "NotificationPriority",
    "NotificationType",
    "ChannelType",
    "TemplateType",
    "RetryPolicy",
    "NotificationMetrics"
]
