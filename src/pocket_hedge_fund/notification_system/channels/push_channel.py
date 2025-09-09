"""
Push Channel

Push notification delivery channel for mobile and web applications.
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


class PushChannel(BaseChannel):
    """
    Push notification delivery channel for mobile and web applications.
    """
    
    def __init__(self):
        """Initialize push channel."""
        super().__init__(ChannelType.PUSH)
        self.provider = 'fcm'  # Default provider (Firebase Cloud Messaging)
        self.api_key = None
        self.project_id = None
        self.server_key = None
        self.provider_configs = {
            'fcm': {
                'base_url': 'https://fcm.googleapis.com/fcm/send',
                'auth_type': 'key'
            },
            'apns': {
                'base_url': 'https://api.push.apple.com/3/device',
                'auth_type': 'certificate'
            },
            'web_push': {
                'base_url': 'https://web-push-codelab.glitch.me/api/send-push-msg',
                'auth_type': 'vapid'
            }
        }
        self.platform_configs = {
            'android': {
                'priority': 'high',
                'ttl': 3600
            },
            'ios': {
                'priority': 10,
                'expiration': 3600
            },
            'web': {
                'ttl': 3600,
                'urgency': 'high'
            }
        }
    
    async def initialize(self):
        """Initialize push channel."""
        try:
            # Load configuration
            self.configuration = {
                'provider': 'fcm',
                'api_key': 'your_api_key_here',
                'project_id': 'your_project_id',
                'server_key': 'your_server_key_here',
                'android_config': {
                    'priority': 'high',
                    'ttl': 3600
                },
                'ios_config': {
                    'priority': 10,
                    'expiration': 3600
                },
                'web_config': {
                    'ttl': 3600,
                    'urgency': 'high'
                }
            }
            
            # Extract configuration
            self.provider = self.configuration.get('provider', 'fcm')
            self.api_key = self.configuration.get('api_key')
            self.project_id = self.configuration.get('project_id')
            self.server_key = self.configuration.get('server_key')
            
            # Validate configuration
            if not await self.validate_configuration(self.configuration):
                raise ValueError("Invalid push channel configuration")
            
            # Test connection
            if await self.test_connection():
                self.is_initialized = True
                logger.info(f"Push channel initialized successfully with {self.provider}")
            else:
                logger.warning("Push channel initialized but connection test failed")
                
        except Exception as e:
            logger.error(f"Failed to initialize push channel: {e}")
            raise
    
    async def send_notification(
        self,
        notification: Notification,
        preferences: Optional[NotificationPreference] = None
    ) -> DeliveryResult:
        """
        Send push notification.
        
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
                    error_message="Push channel not initialized"
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
                    error_message="Invalid recipient device tokens"
                )
            
            # Format message
            formatted_message = self._format_message(notification, preferences)
            
            # Send push notification
            results = await self._send_push_notification(
                formatted_message, recipient_info['device_tokens']
            )
            
            # Process results
            successful_sends = [r for r in results if r['success']]
            failed_sends = [r for r in results if not r['success']]
            
            if successful_sends:
                result = DeliveryResult(
                    success=True,
                    message_id=f"push_{notification.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    delivered_at=datetime.now(),
                    metadata={
                        'recipients': len(recipient_info['device_tokens']),
                        'successful': len(successful_sends),
                        'failed': len(failed_sends),
                        'provider': self.provider,
                        'channel': 'push'
                    }
                )
                self._log_delivery_attempt(notification, True)
                return result
            else:
                error_msg = f"All push notifications failed: {[r['error'] for r in failed_sends]}"
                result = DeliveryResult(
                    success=False,
                    error_message=error_msg
                )
                self._log_delivery_attempt(notification, False, result.error_message)
                return result
                
        except Exception as e:
            error_msg = f"Push delivery failed: {str(e)}"
            logger.error(error_msg)
            return DeliveryResult(
                success=False,
                error_message=error_msg
            )
    
    async def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """
        Validate push channel configuration.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if valid
        """
        try:
            required_fields = ['provider']
            
            for field in required_fields:
                if field not in config:
                    logger.error(f"Missing required configuration field: {field}")
                    return False
            
            # Validate provider
            provider = config['provider']
            if provider not in self.provider_configs:
                logger.error(f"Unsupported push provider: {provider}")
                return False
            
            # Provider-specific validation
            if provider == 'fcm':
                if not config.get('server_key'):
                    logger.error("FCM requires server_key")
                    return False
            elif provider == 'apns':
                if not config.get('certificate_path'):
                    logger.error("APNS requires certificate_path")
                    return False
            elif provider == 'web_push':
                if not config.get('vapid_public_key'):
                    logger.error("Web Push requires vapid_public_key")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """
        Test push provider connection.
        
        Returns:
            True if connection is working
        """
        try:
            if self.provider == 'fcm':
                return await self._test_fcm_connection()
            elif self.provider == 'apns':
                return await self._test_apns_connection()
            elif self.provider == 'web_push':
                return await self._test_web_push_connection()
            else:
                logger.error(f"Unknown provider for connection test: {self.provider}")
                return False
                
        except Exception as e:
            logger.error(f"Push connection test failed: {e}")
            return False
    
    async def _send_push_notification(
        self,
        formatted_message: Dict[str, Any],
        device_tokens: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Send push notification to multiple devices.
        
        Args:
            formatted_message: Formatted message content
            device_tokens: List of device tokens
            
        Returns:
            List of send results
        """
        try:
            results = []
            
            # Send to each device token
            for token in device_tokens:
                try:
                    if self.provider == 'fcm':
                        result = await self._send_via_fcm(formatted_message, token)
                    elif self.provider == 'apns':
                        result = await self._send_via_apns(formatted_message, token)
                    elif self.provider == 'web_push':
                        result = await self._send_via_web_push(formatted_message, token)
                    else:
                        result = {'success': False, 'error': f'Unknown provider: {self.provider}'}
                    
                    results.append(result)
                    
                except Exception as e:
                    results.append({
                        'success': False,
                        'error': str(e),
                        'token': token
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to send push notifications: {e}")
            return [{'success': False, 'error': str(e)}]
    
    async def _send_via_fcm(
        self,
        formatted_message: Dict[str, Any],
        device_token: str
    ) -> Dict[str, Any]:
        """Send push notification via Firebase Cloud Messaging."""
        try:
            # Prepare FCM payload
            payload = {
                'to': device_token,
                'notification': {
                    'title': formatted_message['title'],
                    'body': formatted_message['body'],
                    'icon': 'ic_notification',
                    'sound': 'default'
                },
                'data': formatted_message.get('data', {}),
                'priority': 'high',
                'time_to_live': 3600
            }
            
            # Add Android-specific config
            if 'android' in formatted_message.get('platforms', []):
                payload['android'] = {
                    'priority': 'high',
                    'ttl': '3600s',
                    'notification': {
                        'click_action': 'FLUTTER_NOTIFICATION_CLICK'
                    }
                }
            
            # Add iOS-specific config
            if 'ios' in formatted_message.get('platforms', []):
                payload['apns'] = {
                    'headers': {
                        'apns-priority': '10'
                    },
                    'payload': {
                        'aps': {
                            'alert': {
                                'title': formatted_message['title'],
                                'body': formatted_message['body']
                            },
                            'sound': 'default',
                            'badge': 1
                        }
                    }
                }
            
            # Send request
            headers = {
                'Authorization': f'key={self.server_key}',
                'Content-Type': 'application/json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.provider_configs['fcm']['base_url'],
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Push notification sent via FCM to {device_token}")
                        return {
                            'success': True,
                            'message_id': result.get('message_id'),
                            'token': device_token
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"FCM API error: {response.status} - {error_text}")
                        return {
                            'success': False,
                            'error': f"FCM API error: {response.status}",
                            'token': device_token
                        }
                        
        except Exception as e:
            logger.error(f"FCM push send failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'token': device_token
            }
    
    async def _send_via_apns(
        self,
        formatted_message: Dict[str, Any],
        device_token: str
    ) -> Dict[str, Any]:
        """Send push notification via Apple Push Notification Service."""
        try:
            # This would implement APNS sending
            # For now, return mock result
            logger.info(f"Mock push notification sent via APNS to {device_token}")
            return {
                'success': True,
                'message_id': f"apns_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'token': device_token
            }
            
        except Exception as e:
            logger.error(f"APNS push send failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'token': device_token
            }
    
    async def _send_via_web_push(
        self,
        formatted_message: Dict[str, Any],
        device_token: str
    ) -> Dict[str, Any]:
        """Send push notification via Web Push."""
        try:
            # This would implement Web Push sending
            # For now, return mock result
            logger.info(f"Mock push notification sent via Web Push to {device_token}")
            return {
                'success': True,
                'message_id': f"web_push_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'token': device_token
            }
            
        except Exception as e:
            logger.error(f"Web Push send failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'token': device_token
            }
    
    async def _test_fcm_connection(self) -> bool:
        """Test FCM connection."""
        try:
            # Test FCM connection by sending a test message
            test_payload = {
                'to': 'test_token',
                'notification': {
                    'title': 'Test',
                    'body': 'Connection test'
                }
            }
            
            headers = {
                'Authorization': f'key={self.server_key}',
                'Content-Type': 'application/json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.provider_configs['fcm']['base_url'],
                    json=test_payload,
                    headers=headers
                ) as response:
                    # FCM returns 400 for invalid token, but that means connection works
                    return response.status in [200, 400]
                    
        except Exception as e:
            logger.error(f"FCM connection test failed: {e}")
            return False
    
    async def _test_apns_connection(self) -> bool:
        """Test APNS connection."""
        try:
            # This would implement APNS connection test
            # For now, return True
            return True
        except Exception as e:
            logger.error(f"APNS connection test failed: {e}")
            return False
    
    async def _test_web_push_connection(self) -> bool:
        """Test Web Push connection."""
        try:
            # This would implement Web Push connection test
            # For now, return True
            return True
        except Exception as e:
            logger.error(f"Web Push connection test failed: {e}")
            return False
    
    def _format_message(
        self,
        notification: Notification,
        preferences: Optional[NotificationPreference] = None
    ) -> Dict[str, Any]:
        """
        Format notification message for push notification.
        
        Args:
            notification: Notification to format
            preferences: User preferences
            
        Returns:
            Formatted message dictionary
        """
        try:
            # Create push notification payload
            title = notification.title or f"Pocket Hedge Fund - {notification.notification_type.value.replace('_', ' ').title()}"
            body = notification.message or "You have a new notification"
            
            # Add priority indicator to title for high priority notifications
            if notification.priority in ['high', 'urgent', 'critical']:
                priority_emoji = {
                    'high': '⚠️',
                    'urgent': '🚨',
                    'critical': '🔴'
                }.get(notification.priority.value, '')
                title = f"{priority_emoji} {title}"
            
            # Create data payload
            data = {
                'notification_id': notification.id,
                'type': notification.notification_type.value,
                'priority': notification.priority.value,
                'timestamp': datetime.now().isoformat()
            }
            
            # Add metadata if available
            if notification.metadata:
                data.update(notification.metadata)
            
            # Determine platforms based on notification type
            platforms = ['android', 'ios', 'web']
            
            return {
                'title': title,
                'body': body,
                'data': data,
                'platforms': platforms,
                'priority': notification.priority.value
            }
            
        except Exception as e:
            logger.error(f"Failed to format push message: {e}")
            return {
                'title': 'Pocket Hedge Fund Notification',
                'body': notification.message or 'You have a new notification',
                'data': {'notification_id': notification.id},
                'platforms': ['android', 'ios', 'web'],
                'priority': 'normal'
            }
    
    async def cleanup(self):
        """Cleanup push channel resources."""
        try:
            await super().cleanup()
            self.api_key = None
            self.project_id = None
            self.server_key = None
            logger.info("Push channel cleanup completed")
        except Exception as e:
            logger.error(f"Error during push channel cleanup: {e}")
