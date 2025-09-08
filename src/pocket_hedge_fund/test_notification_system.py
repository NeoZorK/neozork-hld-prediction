"""
NeoZork Pocket Hedge Fund - Notification System Test Suite

This module provides comprehensive testing for the notification system including:
- Notification creation and sending
- User preferences management
- Template management
- Batch operations
- Statistics and analytics
- Real-time notifications
- Error handling and edge cases
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, List, Any

from .notifications.notification_manager import (
    NotificationManager, NotificationType, NotificationChannel,
    NotificationPriority, NotificationStatus, NotificationPreferences,
    NotificationTemplate, Notification
)
from .config.database_manager import DatabaseManager
from .config.config_manager import ConfigManager

class TestNotificationManager:
    """Test suite for NotificationManager"""
    
    @pytest.fixture
    async def notification_manager(self):
        """Create notification manager instance for testing"""
        db_manager = Mock(spec=DatabaseManager)
        config_manager = Mock(spec=ConfigManager)
        
        # Mock configuration
        config_manager.get_config.side_effect = lambda key: {
            "redis": {"host": "localhost", "port": 6379, "db": 0},
            "email": {
                "from_email": "test@example.com",
                "smtp_host": "smtp.example.com",
                "smtp_port": 587,
                "username": "test",
                "password": "password"
            },
            "sms": {
                "api_url": "https://sms.example.com/api",
                "api_key": "test_key"
            },
            "push": {
                "api_url": "https://push.example.com/api",
                "api_key": "test_key"
            },
            "webhook": {
                "api_url": "https://webhook.example.com/api"
            }
        }.get(key, {})
        
        manager = NotificationManager(db_manager, config_manager)
        
        # Mock Redis client
        manager.redis_client = AsyncMock()
        manager.redis_client.setex = AsyncMock()
        manager.redis_client.get = AsyncMock()
        manager.redis_client.lpush = AsyncMock()
        manager.redis_client.expire = AsyncMock()
        
        # Mock database session
        manager.db_manager.get_session.return_value.__aenter__ = AsyncMock()
        manager.db_manager.get_session.return_value.__aexit__ = AsyncMock()
        
        await manager.initialize()
        return manager
    
    @pytest.mark.asyncio
    async def test_create_notification(self, notification_manager):
        """Test notification creation"""
        notification_id = await notification_manager.create_notification(
            user_id="test_user_123",
            title="Test Notification",
            message="This is a test notification",
            notification_type=NotificationType.INFO,
            channel=NotificationChannel.IN_APP,
            priority=NotificationPriority.MEDIUM,
            data={"key": "value"}
        )
        
        assert notification_id is not None
        assert len(notification_id) == 36  # UUID length
        
        # Verify Redis storage was called
        notification_manager.redis_client.setex.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_email_notification(self, notification_manager):
        """Test email notification sending"""
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = Mock()
            mock_smtp.return_value = mock_server
            
            # Mock user email retrieval
            notification_manager._get_user_email = AsyncMock(return_value="user@example.com")
            
            success = await notification_manager.send_notification(
                notification_id="test_id",
                user_id="test_user_123",
                title="Test Email",
                message="Test email content",
                notification_type=NotificationType.INFO,
                channel=NotificationChannel.EMAIL
            )
            
            assert success is True
            mock_smtp.assert_called_once()
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once()
            mock_server.send_message.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_sms_notification(self, notification_manager):
        """Test SMS notification sending"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_response = Mock()
            mock_response.status = 200
            mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
            
            # Mock user phone retrieval
            notification_manager._get_user_phone = AsyncMock(return_value="+1234567890")
            
            success = await notification_manager.send_notification(
                notification_id="test_id",
                user_id="test_user_123",
                title="Test SMS",
                message="Test SMS content",
                notification_type=NotificationType.INFO,
                channel=NotificationChannel.SMS
            )
            
            assert success is True
    
    @pytest.mark.asyncio
    async def test_send_push_notification(self, notification_manager):
        """Test push notification sending"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_response = Mock()
            mock_response.status = 200
            mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
            
            # Mock user push tokens retrieval
            notification_manager._get_user_push_tokens = AsyncMock(return_value=["token1", "token2"])
            
            success = await notification_manager.send_notification(
                notification_id="test_id",
                user_id="test_user_123",
                title="Test Push",
                message="Test push content",
                notification_type=NotificationType.INFO,
                channel=NotificationChannel.PUSH
            )
            
            assert success is True
    
    @pytest.mark.asyncio
    async def test_send_webhook_notification(self, notification_manager):
        """Test webhook notification sending"""
        with patch('aiohttp.ClientSession') as mock_session:
            mock_response = Mock()
            mock_response.status = 200
            mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
            
            # Mock user webhook URL retrieval
            notification_manager._get_user_webhook_url = AsyncMock(return_value="https://webhook.example.com")
            
            success = await notification_manager.send_notification(
                notification_id="test_id",
                user_id="test_user_123",
                title="Test Webhook",
                message="Test webhook content",
                notification_type=NotificationType.INFO,
                channel=NotificationChannel.WEBHOOK
            )
            
            assert success is True
    
    @pytest.mark.asyncio
    async def test_send_in_app_notification(self, notification_manager):
        """Test in-app notification sending"""
        success = await notification_manager.send_notification(
            notification_id="test_id",
            user_id="test_user_123",
            title="Test In-App",
            message="Test in-app content",
            notification_type=NotificationType.INFO,
            channel=NotificationChannel.IN_APP
        )
        
        assert success is True
        notification_manager.redis_client.lpush.assert_called_once()
        notification_manager.redis_client.expire.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_user_notifications(self, notification_manager):
        """Test getting user notifications"""
        # Mock database query result
        mock_notification = Mock()
        mock_notification.notification_id = "test_id"
        mock_notification.user_id = "test_user_123"
        mock_notification.title = "Test Notification"
        mock_notification.message = "Test message"
        mock_notification.notification_type = NotificationType.INFO
        mock_notification.channel = NotificationChannel.IN_APP
        mock_notification.priority = NotificationPriority.MEDIUM
        mock_notification.status = NotificationStatus.SENT
        mock_notification.data = {}
        mock_notification.template_id = None
        mock_notification.scheduled_at = None
        mock_notification.sent_at = datetime.utcnow()
        mock_notification.read_at = None
        mock_notification.created_at = datetime.utcnow()
        mock_notification.updated_at = datetime.utcnow()
        
        # Mock database session
        mock_session = AsyncMock()
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [mock_notification]
        mock_session.execute.return_value = mock_result
        notification_manager.db_manager.get_session.return_value.__aenter__.return_value = mock_session
        
        notifications = await notification_manager.get_user_notifications(
            user_id="test_user_123",
            limit=10,
            offset=0
        )
        
        assert len(notifications) == 1
        assert notifications[0].notification_id == "test_id"
        assert notifications[0].user_id == "test_user_123"
    
    @pytest.mark.asyncio
    async def test_mark_notification_read(self, notification_manager):
        """Test marking notification as read"""
        # Mock database update
        mock_session = AsyncMock()
        mock_result = Mock()
        mock_result.rowcount = 1
        mock_session.execute.return_value = mock_result
        notification_manager.db_manager.get_session.return_value.__aenter__.return_value = mock_session
        
        # Mock Redis update
        notification_manager.redis_client.get = AsyncMock(return_value=json.dumps({
            "notification_id": "test_id",
            "user_id": "test_user_123",
            "status": "sent"
        }))
        
        success = await notification_manager.mark_notification_read("test_id", "test_user_123")
        
        assert success is True
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_user_preferences(self, notification_manager):
        """Test getting user preferences"""
        # Mock database query result
        mock_preferences = Mock()
        mock_preferences.user_id = "test_user_123"
        mock_preferences.email_enabled = True
        mock_preferences.sms_enabled = False
        mock_preferences.push_enabled = True
        mock_preferences.in_app_enabled = True
        mock_preferences.webhook_enabled = False
        mock_preferences.webhook_url = None
        mock_preferences.email_frequency = "immediate"
        mock_preferences.sms_frequency = "immediate"
        mock_preferences.push_frequency = "immediate"
        mock_preferences.notification_types = {
            NotificationType.INFO: True,
            NotificationType.WARNING: True,
            NotificationType.ERROR: True
        }
        mock_preferences.quiet_hours_start = None
        mock_preferences.quiet_hours_end = None
        mock_preferences.timezone = "UTC"
        mock_preferences.created_at = datetime.utcnow()
        mock_preferences.updated_at = datetime.utcnow()
        
        # Mock database session
        mock_session = AsyncMock()
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_preferences
        mock_session.execute.return_value = mock_result
        notification_manager.db_manager.get_session.return_value.__aenter__.return_value = mock_session
        
        preferences = await notification_manager.get_user_preferences("test_user_123")
        
        assert preferences is not None
        assert preferences.user_id == "test_user_123"
        assert preferences.email_enabled is True
        assert preferences.sms_enabled is False
    
    @pytest.mark.asyncio
    async def test_update_user_preferences(self, notification_manager):
        """Test updating user preferences"""
        # Mock database update
        mock_session = AsyncMock()
        mock_result = Mock()
        mock_result.rowcount = 1
        mock_session.execute.return_value = mock_result
        notification_manager.db_manager.get_session.return_value.__aenter__.return_value = mock_session
        
        preferences = NotificationPreferences(
            user_id="test_user_123",
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
                NotificationType.WARNING: True
            },
            quiet_hours_start=None,
            quiet_hours_end=None,
            timezone="UTC",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        success = await notification_manager.update_user_preferences("test_user_123", preferences)
        
        assert success is True
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_notification_template(self, notification_manager):
        """Test creating notification template"""
        template_id = await notification_manager.create_notification_template(
            name="Test Template",
            subject="Test Subject",
            body="Test body with {{variable}}",
            channel=NotificationChannel.EMAIL,
            notification_type=NotificationType.INFO,
            variables=["variable"]
        )
        
        assert template_id is not None
        assert len(template_id) == 36  # UUID length
    
    @pytest.mark.asyncio
    async def test_send_batch_notifications(self, notification_manager):
        """Test sending batch notifications"""
        notifications = [
            {
                "user_id": "user1",
                "title": "Batch Notification 1",
                "message": "Message 1",
                "notification_type": NotificationType.INFO,
                "channel": NotificationChannel.IN_APP,
                "priority": NotificationPriority.MEDIUM,
                "data": {}
            },
            {
                "user_id": "user2",
                "title": "Batch Notification 2",
                "message": "Message 2",
                "notification_type": NotificationType.WARNING,
                "channel": NotificationChannel.EMAIL,
                "priority": NotificationPriority.HIGH,
                "data": {}
            }
        ]
        
        # Mock create_notification to return success
        notification_manager.create_notification = AsyncMock(return_value="test_id")
        
        results = await notification_manager.send_batch_notifications(notifications)
        
        assert results["total"] == 2
        assert results["sent"] == 2
        assert results["failed"] == 0
        assert len(results["errors"]) == 0
    
    @pytest.mark.asyncio
    async def test_get_notification_statistics(self, notification_manager):
        """Test getting notification statistics"""
        # Mock database query result
        mock_notifications = []
        for i in range(5):
            mock_notification = Mock()
            mock_notification.status = NotificationStatus.SENT
            mock_notification.notification_type = NotificationType.INFO
            mock_notification.channel = NotificationChannel.EMAIL
            mock_notification.priority = NotificationPriority.MEDIUM
            mock_notification.read_at = datetime.utcnow() if i < 3 else None
            mock_notifications.append(mock_notification)
        
        # Mock database session
        mock_session = AsyncMock()
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_notifications
        mock_session.execute.return_value = mock_result
        notification_manager.db_manager.get_session.return_value.__aenter__.return_value = mock_session
        
        stats = await notification_manager.get_notification_statistics()
        
        assert stats["total_notifications"] == 5
        assert stats["by_status"]["sent"] == 5
        assert stats["by_type"]["info"] == 5
        assert stats["by_channel"]["email"] == 5
        assert stats["by_priority"]["medium"] == 5
        assert stats["sent_rate"] == 100.0
        assert stats["read_rate"] == 60.0  # 3 out of 5 read
    
    @pytest.mark.asyncio
    async def test_cleanup_expired_notifications(self, notification_manager):
        """Test cleaning up expired notifications"""
        # Mock database delete
        mock_session = AsyncMock()
        mock_result = Mock()
        mock_result.rowcount = 10
        mock_session.execute.return_value = mock_result
        notification_manager.db_manager.get_session.return_value.__aenter__.return_value = mock_session
        
        await notification_manager.cleanup_expired_notifications(30)
        
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_channel_enabled_check(self, notification_manager):
        """Test channel enabled check"""
        preferences = NotificationPreferences(
            user_id="test_user_123",
            email_enabled=True,
            sms_enabled=False,
            push_enabled=True,
            in_app_enabled=True,
            webhook_enabled=False,
            webhook_url=None,
            email_frequency="immediate",
            sms_frequency="immediate",
            push_frequency="immediate",
            notification_types={},
            quiet_hours_start=None,
            quiet_hours_end=None,
            timezone="UTC",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        assert notification_manager._is_channel_enabled(preferences, NotificationChannel.EMAIL) is True
        assert notification_manager._is_channel_enabled(preferences, NotificationChannel.SMS) is False
        assert notification_manager._is_channel_enabled(preferences, NotificationChannel.PUSH) is True
        assert notification_manager._is_channel_enabled(preferences, NotificationChannel.IN_APP) is True
        assert notification_manager._is_channel_enabled(preferences, NotificationChannel.WEBHOOK) is False
    
    @pytest.mark.asyncio
    async def test_quiet_hours_check(self, notification_manager):
        """Test quiet hours check"""
        # Test with quiet hours
        preferences = NotificationPreferences(
            user_id="test_user_123",
            email_enabled=True,
            sms_enabled=True,
            push_enabled=True,
            in_app_enabled=True,
            webhook_enabled=True,
            webhook_url=None,
            email_frequency="immediate",
            sms_frequency="immediate",
            push_frequency="immediate",
            notification_types={},
            quiet_hours_start="22:00",
            quiet_hours_end="08:00",
            timezone="UTC",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Mock current time to be within quiet hours
        with patch('src.pocket_hedge_fund.notifications.notification_manager.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 1, 1, 23, 0)  # 11 PM
            mock_datetime.strftime = datetime.strftime
            
            assert notification_manager._is_quiet_hours(preferences) is True
        
        # Test without quiet hours
        preferences.quiet_hours_start = None
        preferences.quiet_hours_end = None
        
        assert notification_manager._is_quiet_hours(preferences) is False
    
    @pytest.mark.asyncio
    async def test_error_handling(self, notification_manager):
        """Test error handling in notification operations"""
        # Test notification creation with invalid data
        with pytest.raises(Exception):
            await notification_manager.create_notification(
                user_id="",  # Invalid user ID
                title="Test",
                message="Test",
                notification_type=NotificationType.INFO,
                channel=NotificationChannel.IN_APP
            )
        
        # Test sending notification with disabled channel
        preferences = NotificationPreferences(
            user_id="test_user_123",
            email_enabled=False,  # Email disabled
            sms_enabled=False,
            push_enabled=False,
            in_app_enabled=False,
            webhook_enabled=False,
            webhook_url=None,
            email_frequency="immediate",
            sms_frequency="immediate",
            push_frequency="immediate",
            notification_types={},
            quiet_hours_start=None,
            quiet_hours_end=None,
            timezone="UTC",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        notification_manager.get_user_preferences = AsyncMock(return_value=preferences)
        
        success = await notification_manager.send_notification(
            notification_id="test_id",
            user_id="test_user_123",
            title="Test",
            message="Test",
            notification_type=NotificationType.INFO,
            channel=NotificationChannel.EMAIL
        )
        
        assert success is False  # Should fail because email is disabled

class TestNotificationAPI:
    """Test suite for Notification API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        from fastapi.testclient import TestClient
        from .api.notification_api import router
        
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)
    
    def test_create_notification_endpoint(self, client):
        """Test notification creation endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.notification_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "ADMIN"}
            
            # Mock notification manager
            with patch('src.pocket_hedge_fund.api.notification_api.get_notification_manager') as mock_mgr:
                mock_manager = AsyncMock()
                mock_manager.create_notification.return_value = "test_notification_id"
                mock_mgr.return_value = mock_manager
                
                response = client.post(
                    "/api/v1/notifications/",
                    json={
                        "user_id": "test_user_123",
                        "title": "Test Notification",
                        "message": "Test message",
                        "notification_type": "info",
                        "channel": "in_app",
                        "priority": "medium"
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
                assert "notification_id" in data
    
    def test_get_notifications_endpoint(self, client):
        """Test get notifications endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.notification_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock notification manager
            with patch('src.pocket_hedge_fund.api.notification_api.get_notification_manager') as mock_mgr:
                mock_manager = AsyncMock()
                mock_notification = Mock()
                mock_notification.notification_id = "test_id"
                mock_notification.user_id = "test_user"
                mock_notification.title = "Test"
                mock_notification.message = "Test message"
                mock_notification.notification_type = NotificationType.INFO
                mock_notification.channel = NotificationChannel.IN_APP
                mock_notification.priority = NotificationPriority.MEDIUM
                mock_notification.status = NotificationStatus.SENT
                mock_notification.data = {}
                mock_notification.template_id = None
                mock_notification.scheduled_at = None
                mock_notification.sent_at = datetime.utcnow()
                mock_notification.read_at = None
                mock_notification.created_at = datetime.utcnow()
                mock_notification.updated_at = datetime.utcnow()
                
                mock_manager.get_user_notifications.return_value = [mock_notification]
                mock_mgr.return_value = mock_manager
                
                response = client.get(
                    "/api/v1/notifications/",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert "notifications" in data
                assert len(data["notifications"]) == 1
    
    def test_mark_notification_read_endpoint(self, client):
        """Test mark notification as read endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.notification_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock notification manager
            with patch('src.pocket_hedge_fund.api.notification_api.get_notification_manager') as mock_mgr:
                mock_manager = AsyncMock()
                mock_manager.mark_notification_read.return_value = True
                mock_mgr.return_value = mock_manager
                
                response = client.put(
                    "/api/v1/notifications/test_id/read",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
    
    def test_get_preferences_endpoint(self, client):
        """Test get notification preferences endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.notification_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock notification manager
            with patch('src.pocket_hedge_fund.api.notification_api.get_notification_manager') as mock_mgr:
                mock_manager = AsyncMock()
                mock_preferences = Mock()
                mock_preferences.user_id = "test_user"
                mock_preferences.email_enabled = True
                mock_preferences.sms_enabled = False
                mock_preferences.push_enabled = True
                mock_preferences.in_app_enabled = True
                mock_preferences.webhook_enabled = False
                mock_preferences.webhook_url = None
                mock_preferences.email_frequency = "immediate"
                mock_preferences.sms_frequency = "immediate"
                mock_preferences.push_frequency = "immediate"
                mock_preferences.notification_types = {NotificationType.INFO: True}
                mock_preferences.quiet_hours_start = None
                mock_preferences.quiet_hours_end = None
                mock_preferences.timezone = "UTC"
                mock_preferences.created_at = datetime.utcnow()
                mock_preferences.updated_at = datetime.utcnow()
                
                mock_manager.get_user_preferences.return_value = mock_preferences
                mock_mgr.return_value = mock_manager
                
                response = client.get(
                    "/api/v1/notifications/preferences",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["user_id"] == "test_user"
                assert data["email_enabled"] is True
                assert data["sms_enabled"] is False
    
    def test_update_preferences_endpoint(self, client):
        """Test update notification preferences endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.notification_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock notification manager
            with patch('src.pocket_hedge_fund.api.notification_api.get_notification_manager') as mock_mgr:
                mock_manager = AsyncMock()
                mock_manager.update_user_preferences.return_value = True
                mock_mgr.return_value = mock_manager
                
                response = client.put(
                    "/api/v1/notifications/preferences",
                    json={
                        "email_enabled": True,
                        "sms_enabled": False,
                        "push_enabled": True,
                        "in_app_enabled": True,
                        "webhook_enabled": False,
                        "email_frequency": "immediate",
                        "sms_frequency": "immediate",
                        "push_frequency": "immediate",
                        "notification_types": {"info": True, "warning": True},
                        "timezone": "UTC"
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
    
    def test_create_template_endpoint(self, client):
        """Test create notification template endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.notification_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "ADMIN"}
            
            # Mock notification manager
            with patch('src.pocket_hedge_fund.api.notification_api.get_notification_manager') as mock_mgr:
                mock_manager = AsyncMock()
                mock_manager.create_notification_template.return_value = "test_template_id"
                mock_mgr.return_value = mock_manager
                
                response = client.post(
                    "/api/v1/notifications/templates",
                    json={
                        "name": "Test Template",
                        "subject": "Test Subject",
                        "body": "Test body with {{variable}}",
                        "channel": "email",
                        "notification_type": "info",
                        "variables": ["variable"]
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
                assert "template_id" in data
    
    def test_batch_notifications_endpoint(self, client):
        """Test batch notifications endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.notification_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "ADMIN"}
            
            # Mock notification manager
            with patch('src.pocket_hedge_fund.api.notification_api.get_notification_manager') as mock_mgr:
                mock_manager = AsyncMock()
                mock_manager.send_batch_notifications.return_value = {
                    "total": 2,
                    "sent": 2,
                    "failed": 0,
                    "errors": []
                }
                mock_mgr.return_value = mock_manager
                
                response = client.post(
                    "/api/v1/notifications/batch",
                    json={
                        "notifications": [
                            {
                                "user_id": "user1",
                                "title": "Batch 1",
                                "message": "Message 1",
                                "notification_type": "info",
                                "channel": "in_app"
                            },
                            {
                                "user_id": "user2",
                                "title": "Batch 2",
                                "message": "Message 2",
                                "notification_type": "warning",
                                "channel": "email"
                            }
                        ]
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["total"] == 2
                assert data["sent"] == 2
                assert data["failed"] == 0
    
    def test_statistics_endpoint(self, client):
        """Test notification statistics endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.notification_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "ADMIN"}
            
            # Mock notification manager
            with patch('src.pocket_hedge_fund.api.notification_api.get_notification_manager') as mock_mgr:
                mock_manager = AsyncMock()
                mock_manager.get_notification_statistics.return_value = {
                    "total_notifications": 100,
                    "by_status": {"sent": 95, "failed": 5},
                    "by_type": {"info": 50, "warning": 30, "error": 20},
                    "by_channel": {"email": 60, "in_app": 40},
                    "by_priority": {"medium": 70, "high": 30},
                    "sent_rate": 95.0,
                    "read_rate": 80.0
                }
                mock_mgr.return_value = mock_manager
                
                response = client.get(
                    "/api/v1/notifications/statistics",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["total_notifications"] == 100
                assert data["sent_rate"] == 95.0
                assert data["read_rate"] == 80.0
    
    def test_cleanup_endpoint(self, client):
        """Test cleanup expired notifications endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.notification_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "ADMIN"}
            
            # Mock notification manager
            with patch('src.pocket_hedge_fund.api.notification_api.get_notification_manager') as mock_mgr:
                mock_manager = AsyncMock()
                mock_mgr.return_value = mock_manager
                
                response = client.delete(
                    "/api/v1/notifications/cleanup?days=30",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
    
    def test_unauthorized_access(self, client):
        """Test unauthorized access to endpoints"""
        # Test without authentication
        response = client.get("/api/v1/notifications/")
        assert response.status_code == 401
        
        # Test with invalid token
        response = client.get(
            "/api/v1/notifications/",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def test_insufficient_permissions(self, client):
        """Test insufficient permissions for admin-only endpoints"""
        # Mock authentication with non-admin user
        with patch('src.pocket_hedge_fund.api.notification_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            response = client.post(
                "/api/v1/notifications/",
                json={
                    "user_id": "test_user_123",
                    "title": "Test",
                    "message": "Test",
                    "notification_type": "info",
                    "channel": "in_app"
                },
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 403
    
    def test_invalid_input_validation(self, client):
        """Test input validation for API endpoints"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.notification_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "ADMIN"}
            
            # Test with invalid notification type
            response = client.post(
                "/api/v1/notifications/",
                json={
                    "user_id": "test_user_123",
                    "title": "Test",
                    "message": "Test",
                    "notification_type": "invalid_type",
                    "channel": "in_app"
                },
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 400
            
            # Test with invalid channel
            response = client.post(
                "/api/v1/notifications/",
                json={
                    "user_id": "test_user_123",
                    "title": "Test",
                    "message": "Test",
                    "notification_type": "info",
                    "channel": "invalid_channel"
                },
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 400

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
