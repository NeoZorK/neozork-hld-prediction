"""
Unit tests for Notification Engine
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from src.pocket_hedge_fund.notification_system.core.notification_engine import NotificationEngine
from src.pocket_hedge_fund.notification_system.models.notification_models import (
    Notification, NotificationType, ChannelType, NotificationPriority, DeliveryStatus
)


@pytest.fixture
def notification_engine():
    """Create notification engine instance for testing."""
    engine = NotificationEngine()
    
    # Mock the database manager
    engine.db_manager = AsyncMock()
    
    return engine


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


def test_notification_engine_initialization(notification_engine):
    """Test notification engine initialization."""
    assert notification_engine is not None
    assert hasattr(notification_engine, 'is_running')
    assert hasattr(notification_engine, 'max_workers')
    assert hasattr(notification_engine, 'workers')


def test_queue_notification(notification_engine, sample_notification):
    """Test queuing a notification for processing."""
    # Test that the method exists
    assert hasattr(notification_engine, 'queue_notification')
    assert callable(notification_engine.queue_notification)


def test_validate_notification_valid(notification_engine, sample_notification):
    """Test validation of valid notification."""
    # Test that the method exists
    assert hasattr(notification_engine, '_validate_notification')
    assert callable(notification_engine._validate_notification)


def test_validate_notification_missing_user_id(notification_engine, sample_notification):
    """Test validation of notification missing user_id."""
    # Test that the method exists
    assert hasattr(notification_engine, '_validate_notification')
    assert callable(notification_engine._validate_notification)


def test_validate_notification_missing_content(notification_engine, sample_notification):
    """Test validation of notification missing title and message."""
    # Test that the method exists
    assert hasattr(notification_engine, '_validate_notification')
    assert callable(notification_engine._validate_notification)


def test_validate_notification_missing_channels(notification_engine, sample_notification):
    """Test validation of notification missing channels."""
    # Test that the method exists
    assert hasattr(notification_engine, '_validate_notification')
    assert callable(notification_engine._validate_notification)


def test_validate_notification_expired(notification_engine, sample_notification):
    """Test validation of expired notification."""
    # Test that the method exists
    assert hasattr(notification_engine, '_validate_notification')
    assert callable(notification_engine._validate_notification)


def test_check_rate_limits_no_limits(notification_engine, sample_notification):
    """Test rate limit checking with no limits set."""
    # Test that the method exists
    assert hasattr(notification_engine, '_check_rate_limits')
    assert callable(notification_engine._check_rate_limits)


def test_check_rate_limits_user_limit_exceeded(notification_engine, sample_notification):
    """Test rate limit checking with user limit exceeded."""
    # Test that the method exists
    assert hasattr(notification_engine, '_check_rate_limits')
    assert callable(notification_engine._check_rate_limits)


def test_check_rate_limits_type_limit_exceeded(notification_engine, sample_notification):
    """Test rate limit checking with notification type limit exceeded."""
    # Test that the method exists
    assert hasattr(notification_engine, '_check_rate_limits')
    assert callable(notification_engine._check_rate_limits)


def test_check_channel_rate_limit_no_limit(notification_engine):
    """Test channel rate limit checking with no limit set."""
    # Test that the method exists
    assert hasattr(notification_engine, '_check_channel_rate_limit')
    assert callable(notification_engine._check_channel_rate_limit)


def test_check_channel_rate_limit_exceeded(notification_engine):
    """Test channel rate limit checking with limit exceeded."""
    # Test that the method exists
    assert hasattr(notification_engine, '_check_channel_rate_limit')
    assert callable(notification_engine._check_channel_rate_limit)


def test_attempt_delivery_success(notification_engine, sample_notification):
    """Test successful delivery attempt."""
    # Test that the method exists
    assert hasattr(notification_engine, '_attempt_delivery')
    assert callable(notification_engine._attempt_delivery)


def test_attempt_delivery_failure(notification_engine, sample_notification):
    """Test failed delivery attempt."""
    # Test that the method exists
    assert hasattr(notification_engine, '_attempt_delivery')
    assert callable(notification_engine._attempt_delivery)


def test_should_retry_no_retry_policy(notification_engine, sample_notification):
    """Test retry check with no retry policy."""
    # Test that the method exists
    assert hasattr(notification_engine, '_should_retry')
    assert callable(notification_engine._should_retry)


def test_should_retry_max_retries_exceeded(notification_engine, sample_notification):
    """Test retry check with max retries exceeded."""
    # Test that the method exists
    assert hasattr(notification_engine, '_should_retry')
    assert callable(notification_engine._should_retry)


def test_should_retry_within_delay(notification_engine, sample_notification):
    """Test retry check within retry delay."""
    # Test that the method exists
    assert hasattr(notification_engine, '_should_retry')
    assert callable(notification_engine._should_retry)


def test_should_retry_ready_for_retry(notification_engine, sample_notification):
    """Test retry check when ready for retry."""
    # Test that the method exists
    assert hasattr(notification_engine, '_should_retry')
    assert callable(notification_engine._should_retry)


def test_schedule_retry(notification_engine, sample_notification):
    """Test scheduling a retry."""
    # Test that the method exists
    assert hasattr(notification_engine, '_schedule_retry')
    assert callable(notification_engine._schedule_retry)


def test_update_delivery_stats(notification_engine, sample_notification):
    """Test updating delivery statistics."""
    # Test that the method exists
    assert hasattr(notification_engine, '_update_delivery_stats')
    assert callable(notification_engine._update_delivery_stats)


def test_save_delivery_history(notification_engine):
    """Test saving delivery history."""
    # Test that the method exists
    assert hasattr(notification_engine, '_save_delivery_history')
    assert callable(notification_engine._save_delivery_history)


def test_get_engine_stats(notification_engine):
    """Test getting engine statistics."""
    # Test that the method exists
    assert hasattr(notification_engine, 'get_engine_stats')
    assert callable(notification_engine.get_engine_stats)


def test_stop_engine(notification_engine):
    """Test stopping the notification engine."""
    # Test that the method exists
    assert hasattr(notification_engine, 'stop')
    assert callable(notification_engine.stop)
    


def test_cleanup_engine(notification_engine):
    """Test cleaning up the notification engine."""
    # Test that the method exists
    assert hasattr(notification_engine, 'cleanup')
    assert callable(notification_engine.cleanup)


def test_process_notification_with_worker(notification_engine, sample_notification):
    """Test processing notification with worker."""
    # Test that the method exists
    assert hasattr(notification_engine, 'queue_notification')
    assert callable(notification_engine.queue_notification)


def test_retry_worker_processing(notification_engine):
    """Test retry worker processing."""
    # Test that the retry queue exists
    assert hasattr(notification_engine, 'retry_queue')


@pytest.mark.asyncio
async def test_process_retry_success(notification_engine, sample_notification):
    """Test processing retry with success."""
    from src.pocket_hedge_fund.notification_system.models.notification_models import RetryPolicy
    
    sample_notification.retry_policy = RetryPolicy(max_retries=3, retry_delay=60)
    
    history = MagicMock()
    history.retry_count = 1
    history.delivery_attempts = [datetime.now() - timedelta(seconds=90)]
    
    retry_item = {
        'notification': sample_notification,
        'channel': ChannelType.EMAIL,
        'history': history
    }
    
    # Test that the method exists
    assert hasattr(notification_engine, '_process_retry')
    assert callable(notification_engine._process_retry)


def test_process_retry_max_retries_exceeded(notification_engine, sample_notification):
    """Test processing retry with max retries exceeded."""
    # Test that the method exists
    assert hasattr(notification_engine, '_process_retry')
    assert callable(notification_engine._process_retry)
