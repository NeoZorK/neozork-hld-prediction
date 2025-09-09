"""
Base Channel

Base class for all notification delivery channels.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from ..models.notification_models import (
    Notification, NotificationPreference, ChannelType
)

logger = logging.getLogger(__name__)


@dataclass
class DeliveryResult:
    """Result of notification delivery attempt."""
    success: bool
    message_id: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    delivered_at: Optional[datetime] = None


class BaseChannel(ABC):
    """
    Base class for all notification delivery channels.
    """
    
    def __init__(self, channel_type: ChannelType):
        """Initialize base channel."""
        self.channel_type = channel_type
        self.is_initialized = False
        self.configuration = {}
        self.rate_limiter = None
        self.retry_policy = None
    
    @abstractmethod
    async def initialize(self):
        """Initialize the channel."""
        pass
    
    @abstractmethod
    async def send_notification(
        self,
        notification: Notification,
        preferences: Optional[NotificationPreference] = None
    ) -> DeliveryResult:
        """
        Send notification via this channel.
        
        Args:
            notification: Notification to send
            preferences: User preferences
            
        Returns:
            Delivery result
        """
        pass
    
    @abstractmethod
    async def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """
        Validate channel configuration.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if valid
        """
        pass
    
    async def test_connection(self) -> bool:
        """
        Test channel connection.
        
        Returns:
            True if connection is working
        """
        try:
            # Default implementation - can be overridden
            return self.is_initialized
        except Exception as e:
            logger.error(f"Failed to test connection for {self.channel_type}: {e}")
            return False
    
    async def get_delivery_status(self, message_id: str) -> Optional[DeliveryResult]:
        """
        Get delivery status for a message.
        
        Args:
            message_id: Message identifier
            
        Returns:
            Delivery result or None if not found
        """
        try:
            # Default implementation - can be overridden
            return None
        except Exception as e:
            logger.error(f"Failed to get delivery status for {message_id}: {e}")
            return None
    
    async def cleanup(self):
        """Cleanup channel resources."""
        try:
            self.is_initialized = False
            self.configuration.clear()
            logger.info(f"Cleaned up {self.channel_type} channel")
        except Exception as e:
            logger.error(f"Error cleaning up {self.channel_type} channel: {e}")
    
    def _format_message(
        self,
        notification: Notification,
        preferences: Optional[NotificationPreference] = None
    ) -> Dict[str, str]:
        """
        Format notification message for this channel.
        
        Args:
            notification: Notification to format
            preferences: User preferences
            
        Returns:
            Formatted message dictionary
        """
        try:
            # Default formatting - can be overridden
            return {
                'subject': notification.title,
                'body': notification.message,
                'priority': notification.priority.value
            }
        except Exception as e:
            logger.error(f"Failed to format message: {e}")
            return {
                'subject': 'Notification',
                'body': notification.message or 'No message',
                'priority': 'normal'
            }
    
    def _apply_rate_limiting(self) -> bool:
        """
        Apply rate limiting.
        
        Returns:
            True if rate limit allows sending
        """
        try:
            if not self.rate_limiter:
                return True
            
            # Default rate limiting logic - can be overridden
            return True
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            return True
    
    def _get_retry_delay(self, attempt: int) -> int:
        """
        Get retry delay for attempt.
        
        Args:
            attempt: Attempt number (0-based)
            
        Returns:
            Delay in seconds
        """
        try:
            if not self.retry_policy:
                return 60  # Default 1 minute
            
            # Calculate exponential backoff
            delay = self.retry_policy.retry_delay * (2 ** attempt)
            return min(delay, self.retry_policy.max_delay)
        except Exception as e:
            logger.error(f"Error calculating retry delay: {e}")
            return 60
    
    def _extract_recipient_info(
        self,
        notification: Notification,
        preferences: Optional[NotificationPreference] = None
    ) -> Dict[str, Any]:
        """
        Extract recipient information.
        
        Args:
            notification: Notification
            preferences: User preferences
            
        Returns:
            Recipient information dictionary
        """
        try:
            recipient_info = {
                'user_id': notification.user_id,
                'channels': notification.channels
            }
            
            # Add channel-specific recipient info
            if self.channel_type == ChannelType.EMAIL:
                recipient_info['email'] = self._get_user_email(notification.user_id)
            elif self.channel_type == ChannelType.SMS:
                recipient_info['phone'] = self._get_user_phone(notification.user_id)
            elif self.channel_type == ChannelType.PUSH:
                recipient_info['device_tokens'] = self._get_user_device_tokens(notification.user_id)
            elif self.channel_type == ChannelType.WEBHOOK:
                recipient_info['webhook_url'] = self._get_user_webhook_url(notification.user_id)
            
            return recipient_info
        except Exception as e:
            logger.error(f"Failed to extract recipient info: {e}")
            return {'user_id': notification.user_id}
    
    def _get_user_email(self, user_id: str) -> Optional[str]:
        """Get user email address."""
        # This would query the user database
        # For now, return mock email
        return f"{user_id}@example.com"
    
    def _get_user_phone(self, user_id: str) -> Optional[str]:
        """Get user phone number."""
        # This would query the user database
        # For now, return mock phone
        return "+1234567890"
    
    def _get_user_device_tokens(self, user_id: str) -> List[str]:
        """Get user device tokens for push notifications."""
        # This would query the user database
        # For now, return mock tokens
        return [f"device_token_{user_id}_1", f"device_token_{user_id}_2"]
    
    def _get_user_webhook_url(self, user_id: str) -> Optional[str]:
        """Get user webhook URL."""
        # This would query the user database
        # For now, return mock URL
        return f"https://webhook.example.com/user/{user_id}"
    
    def _validate_recipient(self, recipient_info: Dict[str, Any]) -> bool:
        """
        Validate recipient information.
        
        Args:
            recipient_info: Recipient information
            
        Returns:
            True if valid
        """
        try:
            if not recipient_info.get('user_id'):
                return False
            
            # Channel-specific validation
            if self.channel_type == ChannelType.EMAIL:
                email = recipient_info.get('email')
                return email and '@' in email
            elif self.channel_type == ChannelType.SMS:
                phone = recipient_info.get('phone')
                return phone and len(phone) >= 10
            elif self.channel_type == ChannelType.PUSH:
                tokens = recipient_info.get('device_tokens', [])
                return len(tokens) > 0
            elif self.channel_type == ChannelType.WEBHOOK:
                url = recipient_info.get('webhook_url')
                return url and url.startswith('http')
            
            return True
        except Exception as e:
            logger.error(f"Failed to validate recipient: {e}")
            return False
    
    def _log_delivery_attempt(
        self,
        notification: Notification,
        success: bool,
        error_message: Optional[str] = None
    ):
        """Log delivery attempt."""
        try:
            if success:
                logger.info(f"Successfully sent notification {notification.id} via {self.channel_type}")
            else:
                logger.warning(f"Failed to send notification {notification.id} via {self.channel_type}: {error_message}")
        except Exception as e:
            logger.error(f"Failed to log delivery attempt: {e}")
    
    def __str__(self) -> str:
        """String representation of channel."""
        return f"{self.__class__.__name__}({self.channel_type})"
    
    def __repr__(self) -> str:
        """Detailed string representation of channel."""
        return f"{self.__class__.__name__}(channel_type={self.channel_type}, initialized={self.is_initialized})"
