"""
Notification System Module for Pocket Hedge Fund

This module provides comprehensive notification capabilities including:
- Multi-channel notification delivery (email, SMS, push, webhook)
- Template-based message generation
- Scheduled and real-time notifications
- User preference management
- Notification history and analytics
- Retry mechanisms and error handling
- Integration with trading alerts and system events
"""

from .core.notification_manager import NotificationManager
from .core.notification_engine import NotificationEngine
from .core.preference_manager import PreferenceManager
from .core.analytics_tracker import AnalyticsTracker

from .models.notification_models import (
    Notification,
    NotificationTemplate,
    NotificationChannel,
    NotificationPreference,
    NotificationHistory,
    NotificationEvent,
    DeliveryStatus,
    NotificationPriority
)

from .channels.email_channel import EmailChannel
from .channels.sms_channel import SMSChannel
from .channels.push_channel import PushChannel
from .channels.webhook_channel import WebhookChannel

from .templates.template_engine import TemplateEngine
from .templates.template_manager import TemplateManager

from .scheduler.notification_scheduler import NotificationScheduler
from .scheduler.cron_manager import CronManager

__version__ = "1.0.0"
__author__ = "Pocket Hedge Fund Team"

__all__ = [
    # Core components
    "NotificationManager",
    "NotificationEngine",
    "PreferenceManager",
    "AnalyticsTracker",
    
    # Models
    "Notification",
    "NotificationTemplate",
    "NotificationChannel",
    "NotificationPreference",
    "NotificationHistory",
    "NotificationEvent",
    "DeliveryStatus",
    "NotificationPriority",
    
    # Channels
    "EmailChannel",
    "SMSChannel",
    "PushChannel",
    "WebhookChannel",
    
    # Templates
    "TemplateEngine",
    "TemplateManager",
    
    # Scheduler
    "NotificationScheduler",
    "CronManager"
]
