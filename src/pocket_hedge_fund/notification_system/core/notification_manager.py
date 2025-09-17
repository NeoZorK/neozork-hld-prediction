"""
Notification Manager

Main orchestrator for notification system operations.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal

from ..models.notification_models import (
    Notification, NotificationTemplate, NotificationChannel,
    NotificationPreference, NotificationHistory, NotificationEvent,
    DeliveryStatus, NotificationPriority, NotificationType, ChannelType
)
from .notification_engine import NotificationEngine
from .preference_manager import PreferenceManager
from .analytics_tracker import AnalyticsTracker
from ..channels.base_channel import BaseChannel
from ..templates.template_engine import TemplateEngine
from ..scheduler.notification_scheduler import NotificationScheduler

logger = logging.getLogger(__name__)


class NotificationManager:
    """
    Main notification manager that orchestrates all notification operations.
    """
    
    def __init__(self, db_manager=None):
        """Initialize notification manager."""
        self.db_manager = db_manager
        self.notification_engine = NotificationEngine(db_manager)
        self.preference_manager = PreferenceManager(db_manager)
        self.analytics_tracker = AnalyticsTracker(db_manager)
        self.template_engine = TemplateEngine()
        self.scheduler = NotificationScheduler()
        
        # Channel registry
        self.channels: Dict[ChannelType, BaseChannel] = {}
        
        # Cache for frequently accessed data
        self._template_cache = {}
        self._preference_cache = {}
        self._channel_cache = {}
    
    async def initialize(self):
        """Initialize notification manager."""
        try:
            await self.notification_engine.initialize()
            await self.preference_manager.initialize()
            await self.analytics_tracker.initialize()
            await self.template_engine.initialize()
            await self.scheduler.initialize()
            
            # Load channels
            await self._load_channels()
            
            logger.info("Notification manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize notification manager: {e}")
            raise
    
    async def _load_channels(self):
        """Load and initialize notification channels."""
        try:
            # This would load channel configurations from database
            # For now, we'll create default channels
            from ..channels.email_channel import EmailChannel
            from ..channels.sms_channel import SMSChannel
            from ..channels.push_channel import PushChannel
            from ..channels.webhook_channel import WebhookChannel
            
            self.channels[ChannelType.EMAIL] = EmailChannel()
            self.channels[ChannelType.SMS] = SMSChannel()
            self.channels[ChannelType.PUSH] = PushChannel()
            self.channels[ChannelType.WEBHOOK] = WebhookChannel()
            
            # Initialize all channels
            for channel in self.channels.values():
                await channel.initialize()
            
            logger.info(f"Loaded {len(self.channels)} notification channels")
        except Exception as e:
            logger.error(f"Failed to load channels: {e}")
            raise
    
    async def send_notification(
        self,
        notification: Notification,
        user_id: str = None
    ) -> List[NotificationHistory]:
        """
        Send a notification to specified channels.
        
        Args:
            notification: Notification to send
            user_id: Target user ID (overrides notification.user_id)
            
        Returns:
            List of delivery history records
        """
        try:
            if user_id:
                notification.user_id = user_id
            
            # Get user preferences
            preferences = await self.preference_manager.get_user_preferences(
                notification.user_id, notification.notification_type
            )
            
            # Filter channels based on preferences
            allowed_channels = self._filter_channels_by_preferences(
                notification.channels, preferences
            )
            
            if not allowed_channels:
                logger.warning(f"No allowed channels for user {notification.user_id}")
                return []
            
            # Check if notification should be sent now or scheduled
            if notification.scheduled_at and notification.scheduled_at > datetime.now():
                return await self._schedule_notification(notification, allowed_channels)
            
            # Process template if needed
            if notification.template_id:
                notification = await self._process_template(notification)
            
            # Send notification through each channel
            delivery_results = []
            for channel_type in allowed_channels:
                try:
                    result = await self._send_via_channel(
                        notification, channel_type, preferences
                    )
                    delivery_results.append(result)
                except Exception as e:
                    logger.error(f"Failed to send via {channel_type}: {e}")
                    # Create failed delivery record
                    failed_result = NotificationHistory(
                        notification_id=notification.id,
                        user_id=notification.user_id,
                        channel=channel_type,
                        status=DeliveryStatus.FAILED,
                        failed_at=datetime.now(),
                        error_message=str(e)
                    )
                    delivery_results.append(failed_result)
            
            # Track analytics
            await self.analytics_tracker.track_notification_sent(notification, delivery_results)
            
            return delivery_results
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            raise
    
    async def send_bulk_notifications(
        self,
        notifications: List[Notification]
    ) -> Dict[str, List[NotificationHistory]]:
        """
        Send multiple notifications in bulk.
        
        Args:
            notifications: List of notifications to send
            
        Returns:
            Dictionary mapping notification IDs to delivery results
        """
        try:
            results = {}
            
            # Process notifications in batches to avoid overwhelming the system
            batch_size = 50
            for i in range(0, len(notifications), batch_size):
                batch = notifications[i:i + batch_size]
                
                # Process batch concurrently
                tasks = [self.send_notification(notification) for notification in batch]
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Collect results
                for notification, result in zip(batch, batch_results):
                    if isinstance(result, Exception):
                        logger.error(f"Failed to send notification {notification.id}: {result}")
                        results[notification.id] = []
                    else:
                        results[notification.id] = result
                
                # Small delay between batches
                if i + batch_size < len(notifications):
                    await asyncio.sleep(0.1)
            
            logger.info(f"Sent {len(notifications)} notifications in bulk")
            return results
            
        except Exception as e:
            logger.error(f"Failed to send bulk notifications: {e}")
            raise
    
    async def create_notification_from_template(
        self,
        template_id: str,
        user_id: str,
        template_data: Dict[str, Any],
        channels: List[ChannelType] = None,
        priority: NotificationPriority = NotificationPriority.NORMAL
    ) -> Notification:
        """
        Create notification from template.
        
        Args:
            template_id: Template identifier
            user_id: Target user ID
            template_data: Data for template rendering
            channels: Delivery channels
            priority: Notification priority
            
        Returns:
            Created notification
        """
        try:
            # Get template
            template = await self._get_template(template_id)
            
            # Render template
            rendered_content = await self.template_engine.render_template(
                template, template_data
            )
            
            # Create notification
            notification = Notification(
                user_id=user_id,
                notification_type=template.notification_type,
                title=rendered_content.get('subject', ''),
                message=rendered_content.get('body', ''),
                priority=priority,
                channels=channels or template.channels,
                template_id=template_id,
                template_data=template_data
            )
            
            return notification
            
        except Exception as e:
            logger.error(f"Failed to create notification from template: {e}")
            raise
    
    async def schedule_notification(
        self,
        notification: Notification,
        scheduled_at: datetime
    ) -> str:
        """
        Schedule a notification for future delivery.
        
        Args:
            notification: Notification to schedule
            scheduled_at: When to deliver the notification
            
        Returns:
            Schedule ID
        """
        try:
            notification.scheduled_at = scheduled_at
            schedule_id = await self.scheduler.schedule_notification(notification)
            
            logger.info(f"Scheduled notification {notification.id} for {scheduled_at}")
            return schedule_id
            
        except Exception as e:
            logger.error(f"Failed to schedule notification: {e}")
            raise
    
    async def cancel_notification(self, notification_id: str) -> bool:
        """
        Cancel a scheduled notification.
        
        Args:
            notification_id: Notification ID to cancel
            
        Returns:
            True if cancelled successfully
        """
        try:
            success = await self.scheduler.cancel_notification(notification_id)
            
            if success:
                logger.info(f"Cancelled notification {notification_id}")
            else:
                logger.warning(f"Failed to cancel notification {notification_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to cancel notification: {e}")
            raise
    
    async def get_notification_status(self, notification_id: str) -> Dict[str, Any]:
        """
        Get delivery status for a notification.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Status information
        """
        try:
            history = await self.analytics_tracker.get_notification_history(notification_id)
            
            status = {
                'notification_id': notification_id,
                'total_channels': len(history),
                'delivered': sum(1 for h in history if h.status == DeliveryStatus.DELIVERED),
                'failed': sum(1 for h in history if h.status == DeliveryStatus.FAILED),
                'pending': sum(1 for h in history if h.status == DeliveryStatus.PENDING),
                'channels': [{'channel': h.channel, 'status': h.status, 'sent_at': h.sent_at} for h in history]
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get notification status: {e}")
            raise
    
    async def retry_failed_notifications(
        self,
        notification_id: str = None,
        hours_back: int = 24
    ) -> int:
        """
        Retry failed notifications.
        
        Args:
            notification_id: Specific notification ID (optional)
            hours_back: How many hours back to look for failed notifications
            
        Returns:
            Number of notifications retried
        """
        try:
            failed_notifications = await self.analytics_tracker.get_failed_notifications(
                notification_id, hours_back
            )
            
            retry_count = 0
            for notification in failed_notifications:
                try:
                    await self.send_notification(notification)
                    retry_count += 1
                except Exception as e:
                    logger.error(f"Failed to retry notification {notification.id}: {e}")
            
            logger.info(f"Retried {retry_count} failed notifications")
            return retry_count
            
        except Exception as e:
            logger.error(f"Failed to retry failed notifications: {e}")
            raise
    
    def _filter_channels_by_preferences(
        self,
        requested_channels: List[ChannelType],
        preferences: Optional[NotificationPreference]
    ) -> List[ChannelType]:
        """Filter channels based on user preferences."""
        if not preferences or not preferences.is_enabled:
            return []
        
        # Filter by allowed channels
        allowed_channels = [ch for ch in requested_channels if ch in preferences.channels]
        
        # Check quiet hours
        if preferences.quiet_hours_start and preferences.quiet_hours_end:
            current_time = datetime.now().strftime('%H:%M')
            if preferences.quiet_hours_start <= current_time <= preferences.quiet_hours_end:
                # Only allow high priority notifications during quiet hours
                return []
        
        return allowed_channels
    
    async def _schedule_notification(
        self,
        notification: Notification,
        channels: List[ChannelType]
    ) -> List[NotificationHistory]:
        """Schedule notification for future delivery."""
        try:
            schedule_id = await self.scheduler.schedule_notification(notification)
            
            # Create pending delivery records
            delivery_results = []
            for channel in channels:
                history = NotificationHistory(
                    notification_id=notification.id,
                    user_id=notification.user_id,
                    channel=channel,
                    status=DeliveryStatus.PENDING
                )
                delivery_results.append(history)
            
            return delivery_results
            
        except Exception as e:
            logger.error(f"Failed to schedule notification: {e}")
            raise
    
    async def _process_template(self, notification: Notification) -> Notification:
        """Process notification template."""
        try:
            if not notification.template_id:
                return notification
            
            template = await self._get_template(notification.template_id)
            rendered_content = await self.template_engine.render_template(
                template, notification.template_data or {}
            )
            
            notification.title = rendered_content.get('subject', notification.title)
            notification.message = rendered_content.get('body', notification.message)
            
            return notification
            
        except Exception as e:
            logger.error(f"Failed to process template: {e}")
            return notification
    
    async def _send_via_channel(
        self,
        notification: Notification,
        channel_type: ChannelType,
        preferences: Optional[NotificationPreference]
    ) -> NotificationHistory:
        """Send notification via specific channel."""
        try:
            if channel_type not in self.channels:
                raise ValueError(f"Channel {channel_type} not available")
            
            channel = self.channels[channel_type]
            
            # Send notification
            result = await channel.send_notification(notification, preferences)
            
            # Create delivery history
            history = NotificationHistory(
                notification_id=notification.id,
                user_id=notification.user_id,
                channel=channel_type,
                status=DeliveryStatus.DELIVERED if result.success else DeliveryStatus.FAILED,
                sent_at=datetime.now(),
                delivered_at=datetime.now() if result.success else None,
                failed_at=datetime.now() if not result.success else None,
                error_message=result.error_message,
                metadata=result.metadata
            )
            
            return history
            
        except Exception as e:
            logger.error(f"Failed to send via {channel_type}: {e}")
            raise
    
    async def _get_template(self, template_id: str) -> NotificationTemplate:
        """Get template from cache or database."""
        try:
            if template_id in self._template_cache:
                return self._template_cache[template_id]
            
            # This would query the database
            # For now, return a mock template
            template = NotificationTemplate(
                name=f"Template {template_id}",
                notification_type=NotificationType.CUSTOM,
                template_type="text",
                body_template="Default template: {{message}}",
                created_by="system"
            )
            
            self._template_cache[template_id] = template
            return template
            
        except Exception as e:
            logger.error(f"Failed to get template: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            await self.notification_engine.cleanup()
            await self.preference_manager.cleanup()
            await self.analytics_tracker.cleanup()
            await self.template_engine.cleanup()
            await self.scheduler.cleanup()
            
            # Cleanup channels
            for channel in self.channels.values():
                await channel.cleanup()
            
            # Clear caches
            self._template_cache.clear()
            self._preference_cache.clear()
            self._channel_cache.clear()
            
            logger.info("Notification manager cleanup completed")
        except Exception as e:
            logger.error(f"Error during notification manager cleanup: {e}")
