"""
Email Channel

Email notification delivery channel using SMTP.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from .base_channel import BaseChannel, DeliveryResult
from ..models.notification_models import (
    Notification, NotificationPreference, ChannelType
)

logger = logging.getLogger(__name__)


class EmailChannel(BaseChannel):
    """
    Email notification delivery channel using SMTP.
    """
    
    def __init__(self):
        """Initialize email channel."""
        super().__init__(ChannelType.EMAIL)
        self.smtp_server = None
        self.smtp_port = 587
        self.username = None
        self.password = None
        self.use_tls = True
        self.from_email = None
        self.from_name = "Pocket Hedge Fund"
    
    async def initialize(self):
        """Initialize email channel."""
        try:
            # Load configuration
            self.configuration = {
                'smtp_host': 'smtp.gmail.com',
                'smtp_port': 587,
                'username': 'notifications@pockethedgefund.com',
                'password': 'your_password_here',
                'use_tls': True,
                'from_email': 'notifications@pockethedgefund.com',
                'from_name': 'Pocket Hedge Fund'
            }
            
            # Extract configuration
            self.smtp_server = self.configuration.get('smtp_host')
            self.smtp_port = self.configuration.get('smtp_port', 587)
            self.username = self.configuration.get('username')
            self.password = self.configuration.get('password')
            self.use_tls = self.configuration.get('use_tls', True)
            self.from_email = self.configuration.get('from_email')
            self.from_name = self.configuration.get('from_name', 'Pocket Hedge Fund')
            
            # Test connection
            if await self.test_connection():
                self.is_initialized = True
                logger.info("Email channel initialized successfully")
            else:
                logger.warning("Email channel initialized but connection test failed")
                
        except Exception as e:
            logger.error(f"Failed to initialize email channel: {e}")
            raise
    
    async def send_notification(
        self,
        notification: Notification,
        preferences: Optional[NotificationPreference] = None
    ) -> DeliveryResult:
        """
        Send email notification.
        
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
                    error_message="Email channel not initialized"
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
                    error_message="Invalid recipient email address"
                )
            
            # Format message
            formatted_message = self._format_message(notification, preferences)
            
            # Create email
            email_message = await self._create_email_message(
                notification, formatted_message, recipient_info
            )
            
            # Send email
            message_id = await self._send_email(email_message, recipient_info['email'])
            
            if message_id:
                result = DeliveryResult(
                    success=True,
                    message_id=message_id,
                    delivered_at=datetime.now(),
                    metadata={
                        'recipient': recipient_info['email'],
                        'subject': formatted_message['subject'],
                        'channel': 'email'
                    }
                )
                self._log_delivery_attempt(notification, True)
                return result
            else:
                result = DeliveryResult(
                    success=False,
                    error_message="Failed to send email"
                )
                self._log_delivery_attempt(notification, False, result.error_message)
                return result
                
        except Exception as e:
            error_msg = f"Email delivery failed: {str(e)}"
            logger.error(error_msg)
            return DeliveryResult(
                success=False,
                error_message=error_msg
            )
    
    async def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """
        Validate email channel configuration.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if valid
        """
        try:
            required_fields = ['smtp_host', 'smtp_port', 'username', 'password', 'from_email']
            
            for field in required_fields:
                if field not in config:
                    logger.error(f"Missing required configuration field: {field}")
                    return False
            
            # Validate email format
            from_email = config['from_email']
            if '@' not in from_email or '.' not in from_email.split('@')[1]:
                logger.error("Invalid from_email format")
                return False
            
            # Validate port
            port = config.get('smtp_port', 587)
            if not isinstance(port, int) or port <= 0 or port > 65535:
                logger.error("Invalid SMTP port")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """
        Test SMTP connection.
        
        Returns:
            True if connection is working
        """
        try:
            if not all([self.smtp_server, self.username, self.password]):
                return False
            
            # Test SMTP connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            
            if self.use_tls:
                server.starttls()
            
            server.login(self.username, self.password)
            server.quit()
            
            logger.info("SMTP connection test successful")
            return True
            
        except Exception as e:
            logger.error(f"SMTP connection test failed: {e}")
            return False
    
    async def _create_email_message(
        self,
        notification: Notification,
        formatted_message: Dict[str, str],
        recipient_info: Dict[str, Any]
    ) -> MIMEMultipart:
        """
        Create email message.
        
        Args:
            notification: Notification
            formatted_message: Formatted message content
            recipient_info: Recipient information
            
        Returns:
            Email message
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = recipient_info['email']
            msg['Subject'] = formatted_message['subject']
            msg['Message-ID'] = f"<{notification.id}@pockethedgefund.com>"
            
            # Add headers
            msg['X-Notification-Type'] = notification.notification_type.value
            msg['X-Notification-Priority'] = notification.priority.value
            msg['X-Notification-ID'] = notification.id
            
            # Create text and HTML versions
            text_content = self._create_text_content(notification, formatted_message)
            html_content = self._create_html_content(notification, formatted_message)
            
            # Attach parts
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            html_part = MIMEText(html_content, 'html', 'utf-8')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            return msg
            
        except Exception as e:
            logger.error(f"Failed to create email message: {e}")
            raise
    
    def _create_text_content(
        self,
        notification: Notification,
        formatted_message: Dict[str, str]
    ) -> str:
        """Create plain text email content."""
        try:
            content = f"""
{formatted_message['subject']}

{formatted_message['body']}

---
Pocket Hedge Fund
Notification ID: {notification.id}
Priority: {notification.priority.value}
Type: {notification.notification_type.value}
"""
            
            if notification.metadata:
                content += f"\nAdditional Information:\n"
                for key, value in notification.metadata.items():
                    content += f"{key}: {value}\n"
            
            return content.strip()
            
        except Exception as e:
            logger.error(f"Failed to create text content: {e}")
            return formatted_message['body']
    
    def _create_html_content(
        self,
        notification: Notification,
        formatted_message: Dict[str, str]
    ) -> str:
        """Create HTML email content."""
        try:
            priority_color = {
                'low': '#28a745',
                'normal': '#17a2b8',
                'high': '#ffc107',
                'urgent': '#fd7e14',
                'critical': '#dc3545'
            }.get(notification.priority.value, '#17a2b8')
            
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{formatted_message['subject']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: {priority_color}; color: white; padding: 15px; border-radius: 5px 5px 0 0; }}
        .content {{ background-color: #f8f9fa; padding: 20px; border-radius: 0 0 5px 5px; }}
        .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #dee2e6; font-size: 12px; color: #6c757d; }}
        .priority-badge {{ display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 11px; font-weight: bold; text-transform: uppercase; }}
        .priority-{notification.priority.value} {{ background-color: {priority_color}; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{formatted_message['subject']}</h1>
            <span class="priority-badge priority-{notification.priority.value}">
                {notification.priority.value}
            </span>
        </div>
        <div class="content">
            <p>{formatted_message['body'].replace(chr(10), '<br>')}</p>
        </div>
        <div class="footer">
            <p><strong>Pocket Hedge Fund</strong></p>
            <p>Notification ID: {notification.id}</p>
            <p>Type: {notification.notification_type.value}</p>
            <p>Sent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        </div>
    </div>
</body>
</html>
"""
            
            return html_content
            
        except Exception as e:
            logger.error(f"Failed to create HTML content: {e}")
            return f"<html><body><p>{formatted_message['body']}</p></body></html>"
    
    async def _send_email(
        self,
        email_message: MIMEMultipart,
        recipient_email: str
    ) -> Optional[str]:
        """
        Send email via SMTP.
        
        Args:
            email_message: Email message to send
            recipient_email: Recipient email address
            
        Returns:
            Message ID if successful, None otherwise
        """
        try:
            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            
            if self.use_tls:
                server.starttls()
            
            # Login
            server.login(self.username, self.password)
            
            # Send email
            server.send_message(email_message, to_addrs=[recipient_email])
            server.quit()
            
            # Return message ID
            message_id = email_message['Message-ID']
            logger.info(f"Email sent successfully to {recipient_email}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            return None
    
    def _format_message(
        self,
        notification: Notification,
        preferences: Optional[NotificationPreference] = None
    ) -> Dict[str, str]:
        """
        Format notification message for email.
        
        Args:
            notification: Notification to format
            preferences: User preferences
            
        Returns:
            Formatted message dictionary
        """
        try:
            # Use notification title as subject, or create default
            subject = notification.title or f"Pocket Hedge Fund - {notification.notification_type.value.replace('_', ' ').title()}"
            
            # Format message body
            body = notification.message or "No message content"
            
            # Add priority indicator to subject for high priority notifications
            if notification.priority in ['high', 'urgent', 'critical']:
                priority_emoji = {
                    'high': '⚠️',
                    'urgent': '🚨',
                    'critical': '🔴'
                }.get(notification.priority.value, '')
                subject = f"{priority_emoji} {subject}"
            
            return {
                'subject': subject,
                'body': body,
                'priority': notification.priority.value
            }
            
        except Exception as e:
            logger.error(f"Failed to format email message: {e}")
            return {
                'subject': 'Pocket Hedge Fund Notification',
                'body': notification.message or 'No message content',
                'priority': 'normal'
            }
    
    async def cleanup(self):
        """Cleanup email channel resources."""
        try:
            await super().cleanup()
            self.smtp_server = None
            self.username = None
            self.password = None
            self.from_email = None
            logger.info("Email channel cleanup completed")
        except Exception as e:
            logger.error(f"Error during email channel cleanup: {e}")
