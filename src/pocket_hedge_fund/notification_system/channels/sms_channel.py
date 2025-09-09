"""
SMS Channel

SMS notification delivery channel using various SMS providers.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import aiohttp
import json

from .base_channel import BaseChannel, DeliveryResult
from ..models.notification_models import (
    Notification, NotificationPreference, ChannelType
)

logger = logging.getLogger(__name__)


class SMSChannel(BaseChannel):
    """
    SMS notification delivery channel using various SMS providers.
    """
    
    def __init__(self):
        """Initialize SMS channel."""
        super().__init__(ChannelType.SMS)
        self.provider = 'twilio'  # Default provider
        self.api_key = None
        self.api_secret = None
        self.from_number = None
        self.webhook_url = None
        self.max_message_length = 160  # Standard SMS length
        self.provider_configs = {
            'twilio': {
                'base_url': 'https://api.twilio.com/2010-04-01',
                'auth_type': 'basic'
            },
            'aws_sns': {
                'base_url': 'https://sns.us-east-1.amazonaws.com',
                'auth_type': 'aws'
            },
            'sendgrid': {
                'base_url': 'https://api.sendgrid.com/v3',
                'auth_type': 'bearer'
            }
        }
    
    async def initialize(self):
        """Initialize SMS channel."""
        try:
            # Load configuration
            self.configuration = {
                'provider': 'twilio',
                'api_key': 'your_api_key_here',
                'api_secret': 'your_api_secret_here',
                'from_number': '+1234567890',
                'webhook_url': 'https://webhook.example.com/sms',
                'max_message_length': 160
            }
            
            # Extract configuration
            self.provider = self.configuration.get('provider', 'twilio')
            self.api_key = self.configuration.get('api_key')
            self.api_secret = self.configuration.get('api_secret')
            self.from_number = self.configuration.get('from_number')
            self.webhook_url = self.configuration.get('webhook_url')
            self.max_message_length = self.configuration.get('max_message_length', 160)
            
            # Validate configuration
            if not await self.validate_configuration(self.configuration):
                raise ValueError("Invalid SMS channel configuration")
            
            # Test connection
            if await self.test_connection():
                self.is_initialized = True
                logger.info(f"SMS channel initialized successfully with {self.provider}")
            else:
                logger.warning("SMS channel initialized but connection test failed")
                
        except Exception as e:
            logger.error(f"Failed to initialize SMS channel: {e}")
            raise
    
    async def send_notification(
        self,
        notification: Notification,
        preferences: Optional[NotificationPreference] = None
    ) -> DeliveryResult:
        """
        Send SMS notification.
        
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
                    error_message="SMS channel not initialized"
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
                    error_message="Invalid recipient phone number"
                )
            
            # Format message
            formatted_message = self._format_message(notification, preferences)
            
            # Check message length
            if len(formatted_message['body']) > self.max_message_length:
                formatted_message['body'] = self._truncate_message(
                    formatted_message['body'], self.max_message_length
                )
            
            # Send SMS based on provider
            message_id = await self._send_sms(
                formatted_message, recipient_info['phone']
            )
            
            if message_id:
                result = DeliveryResult(
                    success=True,
                    message_id=message_id,
                    delivered_at=datetime.now(),
                    metadata={
                        'recipient': recipient_info['phone'],
                        'provider': self.provider,
                        'message_length': len(formatted_message['body']),
                        'channel': 'sms'
                    }
                )
                self._log_delivery_attempt(notification, True)
                return result
            else:
                result = DeliveryResult(
                    success=False,
                    error_message="Failed to send SMS"
                )
                self._log_delivery_attempt(notification, False, result.error_message)
                return result
                
        except Exception as e:
            error_msg = f"SMS delivery failed: {str(e)}"
            logger.error(error_msg)
            return DeliveryResult(
                success=False,
                error_message=error_msg
            )
    
    async def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """
        Validate SMS channel configuration.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if valid
        """
        try:
            required_fields = ['provider', 'api_key', 'api_secret', 'from_number']
            
            for field in required_fields:
                if field not in config:
                    logger.error(f"Missing required configuration field: {field}")
                    return False
            
            # Validate provider
            provider = config['provider']
            if provider not in self.provider_configs:
                logger.error(f"Unsupported SMS provider: {provider}")
                return False
            
            # Validate phone number format
            from_number = config['from_number']
            if not self._is_valid_phone_number(from_number):
                logger.error("Invalid from_number format")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """
        Test SMS provider connection.
        
        Returns:
            True if connection is working
        """
        try:
            if not all([self.api_key, self.api_secret, self.from_number]):
                return False
            
            # Test connection based on provider
            if self.provider == 'twilio':
                return await self._test_twilio_connection()
            elif self.provider == 'aws_sns':
                return await self._test_aws_sns_connection()
            elif self.provider == 'sendgrid':
                return await self._test_sendgrid_connection()
            else:
                logger.error(f"Unknown provider for connection test: {self.provider}")
                return False
                
        except Exception as e:
            logger.error(f"SMS connection test failed: {e}")
            return False
    
    async def _send_sms(
        self,
        formatted_message: Dict[str, str],
        phone_number: str
    ) -> Optional[str]:
        """
        Send SMS via configured provider.
        
        Args:
            formatted_message: Formatted message content
            phone_number: Recipient phone number
            
        Returns:
            Message ID if successful, None otherwise
        """
        try:
            if self.provider == 'twilio':
                return await self._send_via_twilio(formatted_message, phone_number)
            elif self.provider == 'aws_sns':
                return await self._send_via_aws_sns(formatted_message, phone_number)
            elif self.provider == 'sendgrid':
                return await self._send_via_sendgrid(formatted_message, phone_number)
            else:
                logger.error(f"Unknown SMS provider: {self.provider}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to send SMS via {self.provider}: {e}")
            return None
    
    async def _send_via_twilio(
        self,
        formatted_message: Dict[str, str],
        phone_number: str
    ) -> Optional[str]:
        """Send SMS via Twilio."""
        try:
            import base64
            
            # Prepare authentication
            auth_string = f"{self.api_key}:{self.api_secret}"
            auth_bytes = auth_string.encode('ascii')
            auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
            
            # Prepare request data
            data = {
                'From': self.from_number,
                'To': phone_number,
                'Body': formatted_message['body']
            }
            
            if self.webhook_url:
                data['StatusCallback'] = self.webhook_url
            
            # Send request
            url = f"{self.provider_configs['twilio']['base_url']}/Accounts/{self.api_key}/Messages.json"
            headers = {
                'Authorization': f'Basic {auth_b64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data, headers=headers) as response:
                    if response.status == 201:
                        result = await response.json()
                        message_id = result.get('sid')
                        logger.info(f"SMS sent via Twilio to {phone_number}")
                        return message_id
                    else:
                        error_text = await response.text()
                        logger.error(f"Twilio API error: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            logger.error(f"Twilio SMS send failed: {e}")
            return None
    
    async def _send_via_aws_sns(
        self,
        formatted_message: Dict[str, str],
        phone_number: str
    ) -> Optional[str]:
        """Send SMS via AWS SNS."""
        try:
            # This would implement AWS SNS SMS sending
            # For now, return mock message ID
            logger.info(f"Mock SMS sent via AWS SNS to {phone_number}")
            return f"aws_sns_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
        except Exception as e:
            logger.error(f"AWS SNS SMS send failed: {e}")
            return None
    
    async def _send_via_sendgrid(
        self,
        formatted_message: Dict[str, str],
        phone_number: str
    ) -> Optional[str]:
        """Send SMS via SendGrid."""
        try:
            # This would implement SendGrid SMS sending
            # For now, return mock message ID
            logger.info(f"Mock SMS sent via SendGrid to {phone_number}")
            return f"sendgrid_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
        except Exception as e:
            logger.error(f"SendGrid SMS send failed: {e}")
            return None
    
    async def _test_twilio_connection(self) -> bool:
        """Test Twilio connection."""
        try:
            import base64
            
            auth_string = f"{self.api_key}:{self.api_secret}"
            auth_bytes = auth_string.encode('ascii')
            auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
            
            url = f"{self.provider_configs['twilio']['base_url']}/Accounts/{self.api_key}.json"
            headers = {'Authorization': f'Basic {auth_b64}'}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"Twilio connection test failed: {e}")
            return False
    
    async def _test_aws_sns_connection(self) -> bool:
        """Test AWS SNS connection."""
        try:
            # This would implement AWS SNS connection test
            # For now, return True
            return True
        except Exception as e:
            logger.error(f"AWS SNS connection test failed: {e}")
            return False
    
    async def _test_sendgrid_connection(self) -> bool:
        """Test SendGrid connection."""
        try:
            # This would implement SendGrid connection test
            # For now, return True
            return True
        except Exception as e:
            logger.error(f"SendGrid connection test failed: {e}")
            return False
    
    def _format_message(
        self,
        notification: Notification,
        preferences: Optional[NotificationPreference] = None
    ) -> Dict[str, str]:
        """
        Format notification message for SMS.
        
        Args:
            notification: Notification to format
            preferences: User preferences
            
        Returns:
            Formatted message dictionary
        """
        try:
            # Create concise SMS message
            if notification.title and notification.message:
                # Combine title and message
                body = f"{notification.title}: {notification.message}"
            else:
                body = notification.message or notification.title or "Pocket Hedge Fund notification"
            
            # Add priority indicator for high priority notifications
            if notification.priority in ['high', 'urgent', 'critical']:
                priority_prefix = {
                    'high': '⚠️ ',
                    'urgent': '🚨 ',
                    'critical': '🔴 '
                }.get(notification.priority.value, '')
                body = f"{priority_prefix}{body}"
            
            # Add notification type context
            type_context = {
                'trading_alert': 'TRADE',
                'price_alert': 'PRICE',
                'risk_warning': 'RISK',
                'security_alert': 'SECURITY',
                'system_maintenance': 'SYSTEM'
            }.get(notification.notification_type.value, 'ALERT')
            
            body = f"[{type_context}] {body}"
            
            return {
                'subject': '',  # SMS doesn't have subject
                'body': body,
                'priority': notification.priority.value
            }
            
        except Exception as e:
            logger.error(f"Failed to format SMS message: {e}")
            return {
                'subject': '',
                'body': notification.message or 'Pocket Hedge Fund notification',
                'priority': 'normal'
            }
    
    def _truncate_message(self, message: str, max_length: int) -> str:
        """
        Truncate message to fit SMS length limit.
        
        Args:
            message: Message to truncate
            max_length: Maximum message length
            
        Returns:
            Truncated message
        """
        try:
            if len(message) <= max_length:
                return message
            
            # Truncate and add ellipsis
            truncated = message[:max_length - 3] + "..."
            return truncated
            
        except Exception as e:
            logger.error(f"Failed to truncate message: {e}")
            return message[:max_length] if len(message) > max_length else message
    
    def _is_valid_phone_number(self, phone_number: str) -> bool:
        """
        Validate phone number format.
        
        Args:
            phone_number: Phone number to validate
            
        Returns:
            True if valid
        """
        try:
            # Remove all non-digit characters except +
            cleaned = ''.join(c for c in phone_number if c.isdigit() or c == '+')
            
            # Check if it starts with + and has 10-15 digits
            if cleaned.startswith('+'):
                digits = cleaned[1:]
                return len(digits) >= 10 and len(digits) <= 15
            else:
                # Check if it has 10-15 digits
                return len(cleaned) >= 10 and len(cleaned) <= 15
                
        except Exception as e:
            logger.error(f"Phone number validation failed: {e}")
            return False
    
    async def cleanup(self):
        """Cleanup SMS channel resources."""
        try:
            await super().cleanup()
            self.api_key = None
            self.api_secret = None
            self.from_number = None
            self.webhook_url = None
            logger.info("SMS channel cleanup completed")
        except Exception as e:
            logger.error(f"Error during SMS channel cleanup: {e}")
