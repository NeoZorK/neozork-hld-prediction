"""
Unit tests for Notification Manager
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from src.pocket_hedge_fund.notification_system.core.notification_manager import NotificationManager
from src.pocket_hedge_fund.notification_system.models.notification_models import (
    Notification, NotificationType, ChannelType, NotificationPriority
)


@pytest.fixture
async def notification_manager():
    """Create notification manager instance for testing."""
    manager = NotificationManager()
    
    # Mock the dependencies
    manager.notification_engine = AsyncMock()
    manager.preference_manager = AsyncMock()
    manager.analytics_tracker = AsyncMock()
    manager.template_engine = AsyncMock()
    manager.scheduler = AsyncMock()
    
    # Mock channels
    manager.channels = {
        ChannelType.EMAIL: AsyncMock(),
        ChannelType.SMS: AsyncMock(),
        ChannelType.PUSH: AsyncMock(),
        ChannelType.WEBHOOK: AsyncMock()
    }
    
    await manager.initialize()
    return manager


@pytest.fixture
def sample_notification():
    """Create sample notification for testing."""
    return Notification(
        user_id="user_123",
        notification_type=NotificationType.TRADING_ALERT,
        title="Test Notification",
        message="This is a test notification",
        priority=NotificationPriority.NORMAL,
        channels=[ChannelType.EMAIL, ChannelType.PUSH]
    )


@pytest.mark.asyncio
async def test_notification_manager_initialization(notification_manager):
    """Test notification manager initialization."""
    assert notification_manager is not None
    assert notification_manager.notification_engine is not None
    assert notification_manager.preference_manager is not None
    assert notification_manager.analytics_tracker is not None
    assert notification_manager.template_engine is not None
    assert notification_manager.scheduler is not None


@pytest.mark.asyncio
async def test_send_notification_success(notification_manager, sample_notification):
    """Test successful notification sending."""
    # Mock preference manager to return enabled preferences
    mock_preference = MagicMock()
    mock_preference.is_enabled = True
    mock_preference.channels = [ChannelType.EMAIL, ChannelType.PUSH]
    
    notification_manager.preference_manager.get_user_preferences.return_value = mock_preference
    
    # Mock channel delivery
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.delivered_at = datetime.now()
    mock_result.metadata = {"test": "data"}
    
    for channel in notification_manager.channels.values():
        channel.send_notification.return_value = mock_result
    
    # Send notification
    results = await notification_manager.send_notification(sample_notification)
    
    # Verify results
    assert len(results) == 2  # EMAIL and PUSH channels
    assert all(result.status.value == "delivered" for result in results)
    
    # Verify analytics tracking was called
    notification_manager.analytics_tracker.track_notification_sent.assert_called_once()


@pytest.mark.asyncio
async def test_send_notification_with_preferences_filtering(notification_manager, sample_notification):
    """Test notification sending with preference filtering."""
    # Mock preference manager to return limited channels
    mock_preference = MagicMock()
    mock_preference.is_enabled = True
    mock_preference.channels = [ChannelType.EMAIL]  # Only email allowed
    
    notification_manager.preference_manager.get_user_preferences.return_value = mock_preference
    
    # Mock channel delivery
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.delivered_at = datetime.now()
    
    notification_manager.channels[ChannelType.EMAIL].send_notification.return_value = mock_result
    
    # Send notification
    results = await notification_manager.send_notification(sample_notification)
    
    # Verify only email channel was used
    assert len(results) == 1
    assert results[0].channel == ChannelType.EMAIL
    
    # Verify push channel was not called
    notification_manager.channels[ChannelType.PUSH].send_notification.assert_not_called()


@pytest.mark.asyncio
async def test_send_notification_disabled_preferences(notification_manager, sample_notification):
    """Test notification sending with disabled preferences."""
    # Mock preference manager to return disabled preferences
    mock_preference = MagicMock()
    mock_preference.is_enabled = False
    
    notification_manager.preference_manager.get_user_preferences.return_value = mock_preference
    
    # Send notification
    results = await notification_manager.send_notification(sample_notification)
    
    # Verify no notifications were sent
    assert len(results) == 0
    
    # Verify no channels were called
    for channel in notification_manager.channels.values():
        channel.send_notification.assert_not_called()


@pytest.mark.asyncio
async def test_send_bulk_notifications(notification_manager):
    """Test bulk notification sending."""
    # Create multiple notifications
    notifications = [
        Notification(
            user_id=f"user_{i}",
            notification_type=NotificationType.TRADING_ALERT,
            title=f"Test Notification {i}",
            message=f"Test message {i}",
            channels=[ChannelType.EMAIL]
        )
        for i in range(3)
    ]
    
    # Mock preference manager
    mock_preference = MagicMock()
    mock_preference.is_enabled = True
    mock_preference.channels = [ChannelType.EMAIL]
    
    notification_manager.preference_manager.get_user_preferences.return_value = mock_preference
    
    # Mock channel delivery
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.delivered_at = datetime.now()
    
    notification_manager.channels[ChannelType.EMAIL].send_notification.return_value = mock_result
    
    # Send bulk notifications
    results = await notification_manager.send_bulk_notifications(notifications)
    
    # Verify results
    assert len(results) == 3
    assert all(len(delivery_results) == 1 for delivery_results in results.values())
    
    # Verify analytics tracking was called for each notification
    assert notification_manager.analytics_tracker.track_notification_sent.call_count == 3


@pytest.mark.asyncio
async def test_create_notification_from_template(notification_manager):
    """Test creating notification from template."""
    # Mock template
    mock_template = MagicMock()
    mock_template.notification_type = NotificationType.TRADING_ALERT
    mock_template.channels = [ChannelType.EMAIL]
    
    # Mock template engine
    mock_rendered = {
        'subject': 'Rendered Subject',
        'body': 'Rendered Body'
    }
    notification_manager.template_engine.render_template.return_value = mock_rendered
    
    # Mock template retrieval
    with patch.object(notification_manager, '_get_template', return_value=mock_template):
        # Create notification from template
        notification = await notification_manager.create_notification_from_template(
            template_id="template_123",
            user_id="user_123",
            template_data={"amount": 1000, "symbol": "AAPL"}
        )
        
        # Verify notification
        assert notification.user_id == "user_123"
        assert notification.notification_type == NotificationType.TRADING_ALERT
        assert notification.title == "Rendered Subject"
        assert notification.message == "Rendered Body"
        assert notification.template_id == "template_123"
        assert notification.template_data == {"amount": 1000, "symbol": "AAPL"}


@pytest.mark.asyncio
async def test_schedule_notification(notification_manager, sample_notification):
    """Test scheduling a notification."""
    scheduled_time = datetime.now() + timedelta(hours=1)
    
    # Mock scheduler
    notification_manager.scheduler.schedule_notification.return_value = "schedule_123"
    
    # Schedule notification
    schedule_id = await notification_manager.schedule_notification(sample_notification, scheduled_time)
    
    # Verify scheduling
    assert schedule_id == "schedule_123"
    assert sample_notification.scheduled_at == scheduled_time
    notification_manager.scheduler.schedule_notification.assert_called_once_with(sample_notification)


@pytest.mark.asyncio
async def test_cancel_notification(notification_manager):
    """Test cancelling a scheduled notification."""
    schedule_id = "schedule_123"
    
    # Mock scheduler
    notification_manager.scheduler.cancel_notification.return_value = True
    
    # Cancel notification
    success = await notification_manager.cancel_notification(schedule_id)
    
    # Verify cancellation
    assert success is True
    notification_manager.scheduler.cancel_notification.assert_called_once_with(schedule_id)


@pytest.mark.asyncio
async def test_get_notification_status(notification_manager):
    """Test getting notification status."""
    notification_id = "notification_123"
    
    # Mock analytics tracker
    mock_history = [
        MagicMock(channel=ChannelType.EMAIL, status="delivered", sent_at=datetime.now()),
        MagicMock(channel=ChannelType.PUSH, status="failed", sent_at=datetime.now())
    ]
    notification_manager.analytics_tracker.get_notification_history.return_value = mock_history
    
    # Get status
    status = await notification_manager.get_notification_status(notification_id)
    
    # Verify status
    assert status['notification_id'] == notification_id
    assert status['total_channels'] == 2
    assert status['delivered'] == 1
    assert status['failed'] == 1
    assert status['pending'] == 0


@pytest.mark.asyncio
async def test_retry_failed_notifications(notification_manager):
    """Test retrying failed notifications."""
    # Mock analytics tracker
    mock_failed_notifications = [
        Notification(
            user_id="user_123",
            notification_type=NotificationType.TRADING_ALERT,
            title="Failed Notification",
            message="This notification failed",
            channels=[ChannelType.EMAIL]
        )
    ]
    notification_manager.analytics_tracker.get_failed_notifications.return_value = mock_failed_notifications
    
    # Mock preference manager
    mock_preference = MagicMock()
    mock_preference.is_enabled = True
    mock_preference.channels = [ChannelType.EMAIL]
    notification_manager.preference_manager.get_user_preferences.return_value = mock_preference
    
    # Mock channel delivery
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.delivered_at = datetime.now()
    notification_manager.channels[ChannelType.EMAIL].send_notification.return_value = mock_result
    
    # Retry failed notifications
    retry_count = await notification_manager.retry_failed_notifications()
    
    # Verify retry
    assert retry_count == 1
    notification_manager.analytics_tracker.get_failed_notifications.assert_called_once()


@pytest.mark.asyncio
async def test_send_notification_with_template_processing(notification_manager, sample_notification):
    """Test sending notification with template processing."""
    # Set template ID
    sample_notification.template_id = "template_123"
    sample_notification.template_data = {"amount": 1000}
    
    # Mock template
    mock_template = MagicMock()
    mock_template.notification_type = NotificationType.TRADING_ALERT
    mock_template.channels = [ChannelType.EMAIL]
    
    # Mock template engine
    mock_rendered = {
        'subject': 'Processed Subject',
        'body': 'Processed Body'
    }
    notification_manager.template_engine.render_template.return_value = mock_rendered
    
    # Mock preference manager
    mock_preference = MagicMock()
    mock_preference.is_enabled = True
    mock_preference.channels = [ChannelType.EMAIL]
    notification_manager.preference_manager.get_user_preferences.return_value = mock_preference
    
    # Mock channel delivery
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.delivered_at = datetime.now()
    notification_manager.channels[ChannelType.EMAIL].send_notification.return_value = mock_result
    
    # Mock template retrieval
    with patch.object(notification_manager, '_get_template', return_value=mock_template):
        # Send notification
        results = await notification_manager.send_notification(sample_notification)
        
        # Verify template processing
        assert sample_notification.title == "Processed Subject"
        assert sample_notification.message == "Processed Body"
        notification_manager.template_engine.render_template.assert_called_once()


@pytest.mark.asyncio
async def test_send_notification_channel_failure(notification_manager, sample_notification):
    """Test notification sending with channel failure."""
    # Mock preference manager
    mock_preference = MagicMock()
    mock_preference.is_enabled = True
    mock_preference.channels = [ChannelType.EMAIL, ChannelType.SMS]
    notification_manager.preference_manager.get_user_preferences.return_value = mock_preference
    
    # Mock channel delivery - email succeeds, SMS fails
    mock_success_result = MagicMock()
    mock_success_result.success = True
    mock_success_result.delivered_at = datetime.now()
    
    mock_failure_result = MagicMock()
    mock_failure_result.success = False
    mock_failure_result.error_message = "SMS delivery failed"
    
    notification_manager.channels[ChannelType.EMAIL].send_notification.return_value = mock_success_result
    notification_manager.channels[ChannelType.SMS].send_notification.return_value = mock_failure_result
    
    # Send notification
    results = await notification_manager.send_notification(sample_notification)
    
    # Verify results
    assert len(results) == 2
    
    # Check email result
    email_result = next(r for r in results if r.channel == ChannelType.EMAIL)
    assert email_result.status.value == "delivered"
    
    # Check SMS result
    sms_result = next(r for r in results if r.channel == ChannelType.SMS)
    assert sms_result.status.value == "failed"
    assert sms_result.error_message == "SMS delivery failed"


@pytest.mark.asyncio
async def test_cleanup(notification_manager):
    """Test notification manager cleanup."""
    # Mock cleanup methods
    notification_manager.notification_engine.cleanup = AsyncMock()
    notification_manager.preference_manager.cleanup = AsyncMock()
    notification_manager.analytics_tracker.cleanup = AsyncMock()
    notification_manager.template_engine.cleanup = AsyncMock()
    notification_manager.scheduler.cleanup = AsyncMock()
    
    for channel in notification_manager.channels.values():
        channel.cleanup = AsyncMock()
    
    # Cleanup
    await notification_manager.cleanup()
    
    # Verify all cleanup methods were called
    notification_manager.notification_engine.cleanup.assert_called_once()
    notification_manager.preference_manager.cleanup.assert_called_once()
    notification_manager.analytics_tracker.cleanup.assert_called_once()
    notification_manager.template_engine.cleanup.assert_called_once()
    notification_manager.scheduler.cleanup.assert_called_once()
    
    for channel in notification_manager.channels.values():
        channel.cleanup.assert_called_once()
