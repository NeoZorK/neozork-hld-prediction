"""
NeoZork Pocket Hedge Fund - Notification Manager

This module provides comprehensive notification management functionality including:
- Real-time notifications
- Email notifications
- SMS notifications
- Push notifications
- Notification templates
- Notification preferences
- Notification history
- Batch notifications
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from uuid import UUID, uuid4
import smtplib
import aiohttp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import aioredis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.orm import selectinload

from ..config.database_manager import DatabaseManager
from ..config.config_manager import ConfigManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationType(Enum):
    """Notification types"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    TRADE_ALERT = "trade_alert"
    PORTFOLIO_UPDATE = "portfolio_update"
    PERFORMANCE_ALERT = "performance_alert"
    RISK_ALERT = "risk_alert"
    FUND_UPDATE = "fund_update"
    INVESTMENT_ALERT = "investment_alert"
    WITHDRAWAL_ALERT = "withdrawal_alert"
    SYSTEM_MAINTENANCE = "system_maintenance"
    SECURITY_ALERT = "security_alert"
    MARKET_ALERT = "market_alert"

class NotificationChannel(Enum):
    """Notification channels"""
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WEBHOOK = "webhook"

class NotificationPriority(Enum):
    """Notification priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class NotificationStatus(Enum):
    """Notification status"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"
    ARCHIVED = "archived"

@dataclass
class NotificationTemplate:
    """Notification template"""
    template_id: str
    name: str
    subject: str
    body: str
    channel: NotificationChannel
    notification_type: NotificationType
    variables: List[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class Notification:
    """Notification data structure"""
    notification_id: str
    user_id: str
    title: str
    message: str
    notification_type: NotificationType
    channel: NotificationChannel
    priority: NotificationPriority
    status: NotificationStatus
    data: Dict[str, Any]
    template_id: Optional[str]
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    read_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

@dataclass
class NotificationPreferences:
    """User notification preferences"""
    user_id: str
    email_enabled: bool
    sms_enabled: bool
    push_enabled: bool
    in_app_enabled: bool
    webhook_enabled: bool
    webhook_url: Optional[str]
    email_frequency: str  # immediate, daily, weekly
    sms_frequency: str
    push_frequency: str
    notification_types: Dict[NotificationType, bool]
    quiet_hours_start: Optional[str]
    quiet_hours_end: Optional[str]
    timezone: str
    created_at: datetime
    updated_at: datetime

class NotificationManager:
    """Comprehensive notification management system"""
    
    def __init__(self, db_manager: DatabaseManager, config_manager: ConfigManager):
        self.db_manager = db_manager
        self.config_manager = config_manager
        self.redis_client = None
        self.email_config = None
        self.sms_config = None
        self.push_config = None
        self.webhook_config = None
        
    async def initialize(self):
        """Initialize notification manager"""
        try:
            # Initialize Redis for real-time notifications
            redis_config = self.config_manager.get_config("redis")
            self.redis_client = aioredis.from_url(
                f"redis://{redis_config['host']}:{redis_config['port']}/{redis_config['db']}"
            )
            
            # Load notification configurations
            self.email_config = self.config_manager.get_config("email")
            self.sms_config = self.config_manager.get_config("sms")
            self.push_config = self.config_manager.get_config("push")
            self.webhook_config = self.config_manager.get_config("webhook")
            
            logger.info("Notification Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Notification Manager: {e}")
            raise
    
    async def create_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: NotificationType,
        channel: NotificationChannel,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        data: Optional[Dict[str, Any]] = None,
        template_id: Optional[str] = None,
        scheduled_at: Optional[datetime] = None
    ) -> str:
        """Create a new notification"""
        try:
            notification_id = str(uuid4())
            
            notification = Notification(
                notification_id=notification_id,
                user_id=user_id,
                title=title,
                message=message,
                notification_type=notification_type,
                channel=channel,
                priority=priority,
                status=NotificationStatus.PENDING,
                data=data or {},
                template_id=template_id,
                scheduled_at=scheduled_at,
                sent_at=None,
                read_at=None,
                created_at=datetime.now(datetime.UTC),
                updated_at=datetime.now(datetime.UTC)
            )
            
            # Store in database
            async with self.db_manager.get_session() as session:
                await self._store_notification(session, notification)
            
            # Store in Redis for real-time access
            await self._store_notification_redis(notification)
            
            # Process notification if not scheduled
            if not scheduled_at or scheduled_at <= datetime.now(datetime.UTC):
                await self._process_notification(notification)
            
            logger.info(f"Notification created: {notification_id}")
            return notification_id
            
        except Exception as e:
            logger.error(f"Failed to create notification: {e}")
            raise
    
    async def send_notification(
        self,
        notification_id: str,
        user_id: str,
        title: str,
        message: str,
        notification_type: NotificationType,
        channel: NotificationChannel,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send notification immediately"""
        try:
            # Check user preferences
            preferences = await self.get_user_preferences(user_id)
            if not self._is_channel_enabled(preferences, channel):
                logger.info(f"Channel {channel.value} disabled for user {user_id}")
                return False
            
            # Check quiet hours
            if self._is_quiet_hours(preferences):
                logger.info(f"Quiet hours active for user {user_id}")
                return False
            
            # Send notification based on channel
            success = False
            if channel == NotificationChannel.EMAIL:
                success = await self._send_email_notification(user_id, title, message, data)
            elif channel == NotificationChannel.SMS:
                success = await self._send_sms_notification(user_id, message, data)
            elif channel == NotificationChannel.PUSH:
                success = await self._send_push_notification(user_id, title, message, data)
            elif channel == NotificationChannel.WEBHOOK:
                success = await self._send_webhook_notification(user_id, title, message, data)
            elif channel == NotificationChannel.IN_APP:
                success = await self._send_in_app_notification(user_id, title, message, data)
            
            # Update notification status
            if success:
                await self._update_notification_status(notification_id, NotificationStatus.SENT)
                logger.info(f"Notification sent successfully: {notification_id}")
            else:
                await self._update_notification_status(notification_id, NotificationStatus.FAILED)
                logger.error(f"Failed to send notification: {notification_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False
    
    async def get_user_notifications(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0,
        status: Optional[NotificationStatus] = None,
        notification_type: Optional[NotificationType] = None,
        unread_only: bool = False
    ) -> List[Notification]:
        """Get user notifications with filtering"""
        try:
            async with self.db_manager.get_session() as session:
                query = select(Notification).where(Notification.user_id == user_id)
                
                if status:
                    query = query.where(Notification.status == status)
                
                if notification_type:
                    query = query.where(Notification.notification_type == notification_type)
                
                if unread_only:
                    query = query.where(Notification.read_at.is_(None))
                
                query = query.order_by(Notification.created_at.desc())
                query = query.offset(offset).limit(limit)
                
                result = await session.execute(query)
                notifications = result.scalars().all()
                
                return notifications
                
        except Exception as e:
            logger.error(f"Failed to get user notifications: {e}")
            return []
    
    async def mark_notification_read(self, notification_id: str, user_id: str) -> bool:
        """Mark notification as read"""
        try:
            async with self.db_manager.get_session() as session:
                query = update(Notification).where(
                    and_(
                        Notification.notification_id == notification_id,
                        Notification.user_id == user_id
                    )
                ).values(
                    read_at=datetime.now(datetime.UTC),
                    status=NotificationStatus.READ,
                    updated_at=datetime.now(datetime.UTC)
                )
                
                result = await session.execute(query)
                await session.commit()
                
                if result.rowcount > 0:
                    # Update Redis cache
                    await self._update_notification_redis(notification_id, {
                        "read_at": datetime.now(datetime.UTC).isoformat(),
                        "status": NotificationStatus.READ.value
                    })
                    
                    logger.info(f"Notification marked as read: {notification_id}")
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"Failed to mark notification as read: {e}")
            return False
    
    async def get_user_preferences(self, user_id: str) -> Optional[NotificationPreferences]:
        """Get user notification preferences"""
        try:
            async with self.db_manager.get_session() as session:
                query = select(NotificationPreferences).where(
                    NotificationPreferences.user_id == user_id
                )
                
                result = await session.execute(query)
                preferences = result.scalar_one_or_none()
                
                if not preferences:
                    # Create default preferences
                    preferences = await self._create_default_preferences(user_id)
                
                return preferences
                
        except Exception as e:
            logger.error(f"Failed to get user preferences: {e}")
            return None
    
    async def update_user_preferences(
        self,
        user_id: str,
        preferences: NotificationPreferences
    ) -> bool:
        """Update user notification preferences"""
        try:
            async with self.db_manager.get_session() as session:
                query = update(NotificationPreferences).where(
                    NotificationPreferences.user_id == user_id
                ).values(
                    email_enabled=preferences.email_enabled,
                    sms_enabled=preferences.sms_enabled,
                    push_enabled=preferences.push_enabled,
                    in_app_enabled=preferences.in_app_enabled,
                    webhook_enabled=preferences.webhook_enabled,
                    webhook_url=preferences.webhook_url,
                    email_frequency=preferences.email_frequency,
                    sms_frequency=preferences.sms_frequency,
                    push_frequency=preferences.push_frequency,
                    notification_types=preferences.notification_types,
                    quiet_hours_start=preferences.quiet_hours_start,
                    quiet_hours_end=preferences.quiet_hours_end,
                    timezone=preferences.timezone,
                    updated_at=datetime.now(datetime.UTC)
                )
                
                result = await session.execute(query)
                await session.commit()
                
                if result.rowcount > 0:
                    logger.info(f"User preferences updated: {user_id}")
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"Failed to update user preferences: {e}")
            return False
    
    async def create_notification_template(
        self,
        name: str,
        subject: str,
        body: str,
        channel: NotificationChannel,
        notification_type: NotificationType,
        variables: List[str]
    ) -> str:
        """Create notification template"""
        try:
            template_id = str(uuid4())
            
            template = NotificationTemplate(
                template_id=template_id,
                name=name,
                subject=subject,
                body=body,
                channel=channel,
                notification_type=notification_type,
                variables=variables,
                created_at=datetime.now(datetime.UTC),
                updated_at=datetime.now(datetime.UTC)
            )
            
            async with self.db_manager.get_session() as session:
                await self._store_template(session, template)
            
            logger.info(f"Notification template created: {template_id}")
            return template_id
            
        except Exception as e:
            logger.error(f"Failed to create notification template: {e}")
            raise
    
    async def send_batch_notifications(
        self,
        notifications: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Send batch notifications"""
        try:
            results = {
                "total": len(notifications),
                "sent": 0,
                "failed": 0,
                "errors": []
            }
            
            for notification_data in notifications:
                try:
                    notification_id = await self.create_notification(**notification_data)
                    results["sent"] += 1
                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append({
                        "notification": notification_data,
                        "error": str(e)
                    })
            
            logger.info(f"Batch notifications processed: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to send batch notifications: {e}")
            raise
    
    async def get_notification_statistics(
        self,
        user_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get notification statistics"""
        try:
            async with self.db_manager.get_session() as session:
                query = select(Notification)
                
                if user_id:
                    query = query.where(Notification.user_id == user_id)
                
                if start_date:
                    query = query.where(Notification.created_at >= start_date)
                
                if end_date:
                    query = query.where(Notification.created_at <= end_date)
                
                result = await session.execute(query)
                notifications = result.scalars().all()
                
                stats = {
                    "total_notifications": len(notifications),
                    "by_status": {},
                    "by_type": {},
                    "by_channel": {},
                    "by_priority": {},
                    "sent_rate": 0,
                    "read_rate": 0
                }
                
                sent_count = 0
                read_count = 0
                
                for notification in notifications:
                    # Count by status
                    status = notification.status.value
                    stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
                    
                    # Count by type
                    ntype = notification.notification_type.value
                    stats["by_type"][ntype] = stats["by_type"].get(ntype, 0) + 1
                    
                    # Count by channel
                    channel = notification.channel.value
                    stats["by_channel"][channel] = stats["by_channel"].get(channel, 0) + 1
                    
                    # Count by priority
                    priority = notification.priority.value
                    stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
                    
                    # Count sent and read
                    if notification.status in [NotificationStatus.SENT, NotificationStatus.DELIVERED]:
                        sent_count += 1
                    
                    if notification.read_at:
                        read_count += 1
                
                # Calculate rates
                if len(notifications) > 0:
                    stats["sent_rate"] = (sent_count / len(notifications)) * 100
                    stats["read_rate"] = (read_count / len(notifications)) * 100
                
                return stats
                
        except Exception as e:
            logger.error(f"Failed to get notification statistics: {e}")
            return {}
    
    # Private helper methods
    
    async def _store_notification(self, session: AsyncSession, notification: Notification):
        """Store notification in database"""
        # Implementation would store notification in database
        pass
    
    async def _store_notification_redis(self, notification: Notification):
        """Store notification in Redis for real-time access"""
        if self.redis_client:
            key = f"notification:{notification.notification_id}"
            data = asdict(notification)
            # Convert datetime objects to strings
            for field in ["created_at", "updated_at", "scheduled_at", "sent_at", "read_at"]:
                if data.get(field):
                    data[field] = data[field].isoformat()
            # Convert enums to values
            data["notification_type"] = data["notification_type"].value
            data["channel"] = data["channel"].value
            data["priority"] = data["priority"].value
            data["status"] = data["status"].value
            
            await self.redis_client.setex(key, 86400, json.dumps(data))  # 24 hours TTL
    
    async def _process_notification(self, notification: Notification):
        """Process notification for sending"""
        # Check if notification should be sent immediately
        if notification.scheduled_at and notification.scheduled_at > datetime.now(datetime.UTC):
            return
        
        # Send notification
        await self.send_notification(
            notification.notification_id,
            notification.user_id,
            notification.title,
            notification.message,
            notification.notification_type,
            notification.channel,
            notification.priority,
            notification.data
        )
    
    async def _update_notification_status(
        self,
        notification_id: str,
        status: NotificationStatus
    ):
        """Update notification status"""
        async with self.db_manager.get_session() as session:
            query = update(Notification).where(
                Notification.notification_id == notification_id
            ).values(
                status=status,
                sent_at=datetime.now(datetime.UTC) if status == NotificationStatus.SENT else None,
                updated_at=datetime.now(datetime.UTC)
            )
            
            await session.execute(query)
            await session.commit()
    
    async def _update_notification_redis(self, notification_id: str, updates: Dict[str, Any]):
        """Update notification in Redis"""
        if self.redis_client:
            key = f"notification:{notification_id}"
            existing_data = await self.redis_client.get(key)
            if existing_data:
                data = json.loads(existing_data)
                data.update(updates)
                await self.redis_client.setex(key, 86400, json.dumps(data))
    
    def _is_channel_enabled(
        self,
        preferences: NotificationPreferences,
        channel: NotificationChannel
    ) -> bool:
        """Check if channel is enabled for user"""
        if channel == NotificationChannel.EMAIL:
            return preferences.email_enabled
        elif channel == NotificationChannel.SMS:
            return preferences.sms_enabled
        elif channel == NotificationChannel.PUSH:
            return preferences.push_enabled
        elif channel == NotificationChannel.IN_APP:
            return preferences.in_app_enabled
        elif channel == NotificationChannel.WEBHOOK:
            return preferences.webhook_enabled
        
        return False
    
    def _is_quiet_hours(self, preferences: NotificationPreferences) -> bool:
        """Check if current time is within quiet hours"""
        if not preferences.quiet_hours_start or not preferences.quiet_hours_end:
            return False
        
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        return preferences.quiet_hours_start <= current_time <= preferences.quiet_hours_end
    
    async def _send_email_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send email notification"""
        try:
            # Get user email
            user_email = await self._get_user_email(user_id)
            if not user_email:
                return False
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = user_email
            msg['Subject'] = title
            
            # Add body
            msg.attach(MIMEText(message, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.email_config['smtp_host'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
    
    async def _send_sms_notification(
        self,
        user_id: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send SMS notification"""
        try:
            # Get user phone number
            user_phone = await self._get_user_phone(user_id)
            if not user_phone:
                return False
            
            # Send SMS using configured SMS provider
            async with aiohttp.ClientSession() as session:
                payload = {
                    "to": user_phone,
                    "message": message,
                    "api_key": self.sms_config['api_key']
                }
                
                async with session.post(self.sms_config['api_url'], json=payload) as response:
                    return response.status == 200
            
        except Exception as e:
            logger.error(f"Failed to send SMS notification: {e}")
            return False
    
    async def _send_push_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send push notification"""
        try:
            # Get user push tokens
            push_tokens = await self._get_user_push_tokens(user_id)
            if not push_tokens:
                return False
            
            # Send push notification using configured provider
            async with aiohttp.ClientSession() as session:
                payload = {
                    "tokens": push_tokens,
                    "title": title,
                    "body": message,
                    "data": data or {}
                }
                
                headers = {
                    "Authorization": f"Bearer {self.push_config['api_key']}",
                    "Content-Type": "application/json"
                }
                
                async with session.post(self.push_config['api_url'], json=payload, headers=headers) as response:
                    return response.status == 200
            
        except Exception as e:
            logger.error(f"Failed to send push notification: {e}")
            return False
    
    async def _send_webhook_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send webhook notification"""
        try:
            # Get user webhook URL
            webhook_url = await self._get_user_webhook_url(user_id)
            if not webhook_url:
                return False
            
            # Send webhook notification
            async with aiohttp.ClientSession() as session:
                payload = {
                    "user_id": user_id,
                    "title": title,
                    "message": message,
                    "data": data or {},
                    "timestamp": datetime.now(datetime.UTC).isoformat()
                }
                
                async with session.post(webhook_url, json=payload) as response:
                    return response.status == 200
            
        except Exception as e:
            logger.error(f"Failed to send webhook notification: {e}")
            return False
    
    async def _send_in_app_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send in-app notification"""
        try:
            # Store in Redis for real-time delivery
            if self.redis_client:
                notification_data = {
                    "user_id": user_id,
                    "title": title,
                    "message": message,
                    "data": data or {},
                    "timestamp": datetime.now(datetime.UTC).isoformat()
                }
                
                key = f"in_app_notifications:{user_id}"
                await self.redis_client.lpush(key, json.dumps(notification_data))
                await self.redis_client.expire(key, 86400)  # 24 hours TTL
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send in-app notification: {e}")
            return False
    
    async def _create_default_preferences(self, user_id: str) -> NotificationPreferences:
        """Create default notification preferences"""
        preferences = NotificationPreferences(
            user_id=user_id,
            email_enabled=True,
            sms_enabled=False,
            push_enabled=True,
            in_app_enabled=True,
            webhook_enabled=False,
            webhook_url=None,
            email_frequency="immediate",
            sms_frequency="immediate",
            push_frequency="immediate",
            notification_types={
                NotificationType.INFO: True,
                NotificationType.WARNING: True,
                NotificationType.ERROR: True,
                NotificationType.SUCCESS: True,
                NotificationType.TRADE_ALERT: True,
                NotificationType.PORTFOLIO_UPDATE: True,
                NotificationType.PERFORMANCE_ALERT: True,
                NotificationType.RISK_ALERT: True,
                NotificationType.FUND_UPDATE: True,
                NotificationType.INVESTMENT_ALERT: True,
                NotificationType.WITHDRAWAL_ALERT: True,
                NotificationType.SYSTEM_MAINTENANCE: True,
                NotificationType.SECURITY_ALERT: True,
                NotificationType.MARKET_ALERT: True
            },
            quiet_hours_start=None,
            quiet_hours_end=None,
            timezone="UTC",
            created_at=datetime.now(datetime.UTC),
            updated_at=datetime.now(datetime.UTC)
        )
        
        # Store in database
        async with self.db_manager.get_session() as session:
            await self._store_preferences(session, preferences)
        
        return preferences
    
    async def _store_preferences(self, session: AsyncSession, preferences: NotificationPreferences):
        """Store notification preferences in database"""
        # Implementation would store preferences in database
        pass
    
    async def _store_template(self, session: AsyncSession, template: NotificationTemplate):
        """Store notification template in database"""
        # Implementation would store template in database
        pass
    
    async def _get_user_email(self, user_id: str) -> Optional[str]:
        """Get user email address"""
        # Implementation would get user email from database
        return "user@example.com"
    
    async def _get_user_phone(self, user_id: str) -> Optional[str]:
        """Get user phone number"""
        # Implementation would get user phone from database
        return "+1234567890"
    
    async def _get_user_push_tokens(self, user_id: str) -> List[str]:
        """Get user push notification tokens"""
        # Implementation would get user push tokens from database
        return ["push_token_1", "push_token_2"]
    
    async def _get_user_webhook_url(self, user_id: str) -> Optional[str]:
        """Get user webhook URL"""
        # Implementation would get user webhook URL from database
        return "https://user-webhook.example.com"
    
    async def cleanup_expired_notifications(self, days: int = 30):
        """Clean up expired notifications"""
        try:
            cutoff_date = datetime.now(datetime.UTC) - timedelta(days=days)
            
            async with self.db_manager.get_session() as session:
                query = delete(Notification).where(
                    and_(
                        Notification.created_at < cutoff_date,
                        Notification.status.in_([
                            NotificationStatus.READ,
                            NotificationStatus.ARCHIVED
                        ])
                    )
                )
                
                result = await session.execute(query)
                await session.commit()
                
                logger.info(f"Cleaned up {result.rowcount} expired notifications")
                
        except Exception as e:
            logger.error(f"Failed to cleanup expired notifications: {e}")
    
    async def close(self):
        """Close notification manager"""
        if self.redis_client:
            await self.redis_client.close()
        logger.info("Notification Manager closed")
