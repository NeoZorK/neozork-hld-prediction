"""
Webhook Channel

Webhook notification delivery channel for external integrations.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import aiohttp
import json
import hmac
import hashlib
import base64

from .base_channel import BaseChannel, DeliveryResult
from ..models.notification_models import (
    Notification, NotificationPreference, ChannelType
)

logger = logging.getLogger(__name__)


class WebhookChannel(BaseChannel):
    """
    Webhook notification delivery channel for external integrations.
    """
    
    def __init__(self):
        """Initialize webhook channel."""
        super().__init__(ChannelType.WEBHOOK)
        self.default_timeout = 30  # seconds
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        self.signature_header = 'X-Webhook-Signature'
        self.signature_algorithm = 'sha256'
        self.secret_key = None
        self.allowed_methods = ['POST', 'PUT', 'PATCH']
        self.default_method = 'POST'
        self.default_headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Pocket-Hedge-Fund-Webhook/1.0'
        }
    
    async def initialize(self):
        """Initialize webhook channel."""
        try:
            # Load configuration
            self.configuration = {
                'secret_key': 'your_webhook_secret_key',
                'timeout': 30,
                'max_retries': 3,
                'retry_delay': 5,
                'signature_algorithm': 'sha256',
                'default_method': 'POST',
                'allowed_methods': ['POST', 'PUT', 'PATCH']
            }
            
            # Extract configuration
            self.secret_key = self.configuration.get('secret_key')
            self.default_timeout = self.configuration.get('timeout', 30)
            self.max_retries = self.configuration.get('max_retries', 3)
            self.retry_delay = self.configuration.get('retry_delay', 5)
            self.signature_algorithm = self.configuration.get('signature_algorithm', 'sha256')
            self.default_method = self.configuration.get('default_method', 'POST')
            self.allowed_methods = self.configuration.get('allowed_methods', ['POST', 'PUT', 'PATCH'])
            
            # Validate configuration
            if not await self.validate_configuration(self.configuration):
                raise ValueError("Invalid webhook channel configuration")
            
            self.is_initialized = True
            logger.info("Webhook channel initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize webhook channel: {e}")
            raise
    
    async def send_notification(
        self,
        notification: Notification,
        preferences: Optional[NotificationPreference] = None
    ) -> DeliveryResult:
        """
        Send webhook notification.
        
        Args:
            notification: Notification to send
            preferences: User preferences
            
        Returns:
            Delivery result
        """
        try:
            if not self.is_initialized:
                return DeliveryResult(
                    success=False,
                    error_message="Webhook channel not initialized"
                )
            
            # Apply rate limiting
            if not self._apply_rate_limiting():
                return DeliveryResult(
                    success=False,
                    error_message="Rate limit exceeded"
                )
            
            # Extract recipient information
            recipient_info = self._extract_recipient_info(notification, preferences)
            
            # Validate recipient
            if not self._validate_recipient(recipient_info):
                return DeliveryResult(
                    success=False,
                    error_message="Invalid webhook URL"
                )
            
            # Format message
            formatted_message = self._format_message(notification, preferences)
            
            # Send webhook
            success = await self._send_webhook(
                formatted_message, recipient_info['webhook_url']
            )
            
            if success:
                result = DeliveryResult(
                    success=True,
                    message_id=f"webhook_{notification.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    delivered_at=datetime.now(),
                    metadata={
                        'webhook_url': recipient_info['webhook_url'],
                        'method': self.default_method,
                        'channel': 'webhook'
                    }
                )
                self._log_delivery_attempt(notification, True)
                return result
            else:
                result = DeliveryResult(
                    success=False,
                    error_message="Failed to send webhook"
                )
                self._log_delivery_attempt(notification, False, result.error_message)
                return result
                
        except Exception as e:
            error_msg = f"Webhook delivery failed: {str(e)}"
            logger.error(error_msg)
            return DeliveryResult(
                success=False,
                error_message=error_msg
            )
    
    async def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """
        Validate webhook channel configuration.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if valid
        """
        try:
            # Validate timeout
            timeout = config.get('timeout', 30)
            if not isinstance(timeout, int) or timeout <= 0 or timeout > 300:
                logger.error("Invalid timeout value")
                return False
            
            # Validate max retries
            max_retries = config.get('max_retries', 3)
            if not isinstance(max_retries, int) or max_retries < 0 or max_retries > 10:
                logger.error("Invalid max_retries value")
                return False
            
            # Validate retry delay
            retry_delay = config.get('retry_delay', 5)
            if not isinstance(retry_delay, int) or retry_delay <= 0 or retry_delay > 60:
                logger.error("Invalid retry_delay value")
                return False
            
            # Validate signature algorithm
            algorithm = config.get('signature_algorithm', 'sha256')
            if algorithm not in ['sha1', 'sha256', 'sha512']:
                logger.error("Invalid signature algorithm")
                return False
            
            # Validate default method
            method = config.get('default_method', 'POST')
            if method not in ['POST', 'PUT', 'PATCH']:
                logger.error("Invalid default method")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """
        Test webhook connection.
        
        Returns:
            True if connection is working
        """
        try:
            # Webhook channel doesn't have a persistent connection
            # Test is done per webhook URL
            return True
        except Exception as e:
            logger.error(f"Webhook connection test failed: {e}")
            return False
    
    async def _send_webhook(
        self,
        formatted_message: Dict[str, Any],
        webhook_url: str
    ) -> bool:
        """
        Send webhook notification.
        
        Args:
            formatted_message: Formatted message content
            webhook_url: Webhook URL
            
        Returns:
            True if successful
        """
        try:
            # Prepare headers
            headers = self.default_headers.copy()
            
            # Add signature if secret key is available
            if self.secret_key:
                signature = self._generate_signature(formatted_message)
                headers[self.signature_header] = f"{self.signature_algorithm}={signature}"
            
            # Add timestamp
            headers['X-Webhook-Timestamp'] = str(int(datetime.now().timestamp()))
            
            # Add notification metadata
            headers['X-Notification-ID'] = formatted_message.get('notification_id', '')
            headers['X-Notification-Type'] = formatted_message.get('type', '')
            headers['X-Notification-Priority'] = formatted_message.get('priority', 'normal')
            
            # Send webhook with retries
            for attempt in range(self.max_retries + 1):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            webhook_url,
                            json=formatted_message,
                            headers=headers,
                            timeout=aiohttp.ClientTimeout(total=self.default_timeout)
                        ) as response:
                            if response.status in [200, 201, 202, 204]:
                                logger.info(f"Webhook sent successfully to {webhook_url}")
                                return True
                            else:
                                error_text = await response.text()
                                logger.warning(f"Webhook returned status {response.status}: {error_text}")
                                
                                # Don't retry on client errors (4xx)
                                if 400 <= response.status < 500:
                                    return False
                                
                                # Retry on server errors (5xx)
                                if attempt < self.max_retries:
                                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                                    continue
                                else:
                                    return False
                                    
                except asyncio.TimeoutError:
                    logger.warning(f"Webhook timeout for {webhook_url}")
                    if attempt < self.max_retries:
                        await asyncio.sleep(self.retry_delay * (2 ** attempt))
                        continue
                    else:
                        return False
                        
                except Exception as e:
                    logger.error(f"Webhook send error: {e}")
                    if attempt < self.max_retries:
                        await asyncio.sleep(self.retry_delay * (2 ** attempt))
                        continue
                    else:
                        return False
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to send webhook: {e}")
            return False
    
    def _generate_signature(self, payload: Dict[str, Any]) -> str:
        """
        Generate webhook signature.
        
        Args:
            payload: Payload to sign
            
        Returns:
            Base64 encoded signature
        """
        try:
            # Convert payload to JSON string
            payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
            
            # Create HMAC signature
            if self.signature_algorithm == 'sha1':
                signature = hmac.new(
                    self.secret_key.encode('utf-8'),
                    payload_str.encode('utf-8'),
                    hashlib.sha1
                ).digest()
            elif self.signature_algorithm == 'sha256':
                signature = hmac.new(
                    self.secret_key.encode('utf-8'),
                    payload_str.encode('utf-8'),
                    hashlib.sha256
                ).digest()
            elif self.signature_algorithm == 'sha512':
                signature = hmac.new(
                    self.secret_key.encode('utf-8'),
                    payload_str.encode('utf-8'),
                    hashlib.sha512
                ).digest()
            else:
                raise ValueError(f"Unsupported signature algorithm: {self.signature_algorithm}")
            
            # Encode signature as base64
            return base64.b64encode(signature).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Failed to generate signature: {e}")
            return ""
    
    def _format_message(
        self,
        notification: Notification,
        preferences: Optional[NotificationPreference] = None
    ) -> Dict[str, Any]:
        """
        Format notification message for webhook.
        
        Args:
            notification: Notification to format
            preferences: User preferences
            
        Returns:
            Formatted message dictionary
        """
        try:
            # Create webhook payload
            payload = {
                'notification_id': notification.id,
                'user_id': notification.user_id,
                'type': notification.notification_type.value,
                'priority': notification.priority.value,
                'title': notification.title,
                'message': notification.message,
                'timestamp': datetime.now().isoformat(),
                'channels': [ch.value for ch in notification.channels],
                'metadata': notification.metadata or {}
            }
            
            # Add template information if available
            if notification.template_id:
                payload['template_id'] = notification.template_id
                payload['template_data'] = notification.template_data or {}
            
            # Add scheduling information if available
            if notification.scheduled_at:
                payload['scheduled_at'] = notification.scheduled_at.isoformat()
            
            if notification.expires_at:
                payload['expires_at'] = notification.expires_at.isoformat()
            
            # Add retry policy if available
            if notification.retry_policy:
                payload['retry_policy'] = {
                    'max_retries': notification.retry_policy.max_retries,
                    'retry_delay': notification.retry_policy.retry_delay,
                    'backoff_multiplier': notification.retry_policy.backoff_multiplier,
                    'max_delay': notification.retry_policy.max_delay
                }
            
            # Add webhook-specific fields
            payload['webhook'] = {
                'version': '1.0',
                'source': 'pocket_hedge_fund',
                'event': 'notification.sent'
            }
            
            return payload
            
        except Exception as e:
            logger.error(f"Failed to format webhook message: {e}")
            return {
                'notification_id': notification.id,
                'user_id': notification.user_id,
                'type': notification.notification_type.value,
                'title': notification.title or 'Notification',
                'message': notification.message or 'No message',
                'timestamp': datetime.now().isoformat(),
                'webhook': {
                    'version': '1.0',
                    'source': 'pocket_hedge_fund',
                    'event': 'notification.sent'
                }
            }
    
    def _validate_webhook_url(self, url: str) -> bool:
        """
        Validate webhook URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid
        """
        try:
            # Basic URL validation
            if not url.startswith(('http://', 'https://')):
                return False
            
            # Check for valid domain
            if len(url) < 10:  # Minimum reasonable URL length
                return False
            
            # Additional validation could be added here
            return True
            
        except Exception as e:
            logger.error(f"Webhook URL validation failed: {e}")
            return False
    
    async def cleanup(self):
        """Cleanup webhook channel resources."""
        try:
            await super().cleanup()
            self.secret_key = None
            logger.info("Webhook channel cleanup completed")
        except Exception as e:
            logger.error(f"Error during webhook channel cleanup: {e}")
