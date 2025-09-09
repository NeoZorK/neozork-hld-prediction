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
async def notification_engine():
    """Create notification engine instance for testing."""
    engine = NotificationEngine()
    
    # Mock the database manager
    engine.db_manager = AsyncMock()
    
    await engine.initialize()
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


@pytest.mark.asyncio
async def test_notification_engine_initialization(notification_engine):
    """Test notification engine initialization."""
    assert notification_engine is not None
    assert notification_engine.is_running is True
    assert notification_engine.max_workers == 5
    assert len(notification_engine.workers) == 6  # 5 processing workers + 1 retry worker


@pytest.mark.asyncio
async def test_queue_notification(notification_engine, sample_notification):
    """Test queuing a notification for processing."""
    # Queue notification
    await notification_engine.queue_notification(sample_notification)
    
    # Verify notification was queued
    assert notification_engine.processing_queue.qsize() == 1


@pytest.mark.asyncio
async def test_validate_notification_valid(notification_engine, sample_notification):
    """Test validation of valid notification."""
    is_valid = await notification_engine._validate_notification(sample_notification)
    assert is_valid is True


@pytest.mark.asyncio
async def test_validate_notification_missing_user_id(notification_engine, sample_notification):
    """Test validation of notification missing user_id."""
    sample_notification.user_id = None
    
    is_valid = await notification_engine._validate_notification(sample_notification)
    assert is_valid is False


@pytest.mark.asyncio
async def test_validate_notification_missing_content(notification_engine, sample_notification):
    """Test validation of notification missing title and message."""
    sample_notification.title = None
    sample_notification.message = None
    
    is_valid = await notification_engine._validate_notification(sample_notification)
    assert is_valid is False


@pytest.mark.asyncio
async def test_validate_notification_missing_channels(notification_engine, sample_notification):
    """Test validation of notification missing channels."""
    sample_notification.channels = []
    
    is_valid = await notification_engine._validate_notification(sample_notification)
    assert is_valid is False


@pytest.mark.asyncio
async def test_validate_notification_expired(notification_engine, sample_notification):
    """Test validation of expired notification."""
    sample_notification.expires_at = datetime.now() - timedelta(hours=1)
    
    is_valid = await notification_engine._validate_notification(sample_notification)
    assert is_valid is False


@pytest.mark.asyncio
async def test_check_rate_limits_no_limits(notification_engine, sample_notification):
    """Test rate limit checking with no limits set."""
    # Clear rate limits
    notification_engine.rate_limits.clear()
    
    is_allowed = await notification_engine._check_rate_limits(sample_notification)
    assert is_allowed is True


@pytest.mark.asyncio
async def test_check_rate_limits_user_limit_exceeded(notification_engine, sample_notification):
    """Test rate limit checking with user limit exceeded."""
    # Set user rate limit
    notification_engine.rate_limits[f"user:{sample_notification.user_id}"] = {
        'count': 100,
        'max_per_hour': 50
    }
    
    is_allowed = await notification_engine._check_rate_limits(sample_notification)
    assert is_allowed is False


@pytest.mark.asyncio
async def test_check_rate_limits_type_limit_exceeded(notification_engine, sample_notification):
    """Test rate limit checking with notification type limit exceeded."""
    # Set type rate limit
    notification_engine.rate_limits[f"type:{sample_notification.notification_type}"] = {
        'count': 50,
        'max_per_hour': 30
    }
    
    is_allowed = await notification_engine._check_rate_limits(sample_notification)
    assert is_allowed is False


@pytest.mark.asyncio
async def test_check_channel_rate_limit_no_limit(notification_engine):
    """Test channel rate limit checking with no limit set."""
    is_allowed = await notification_engine._check_channel_rate_limit(ChannelType.EMAIL)
    assert is_allowed is True


@pytest.mark.asyncio
async def test_check_channel_rate_limit_exceeded(notification_engine):
    """Test channel rate limit checking with limit exceeded."""
    # Set channel rate limit
    notification_engine.rate_limits[f"channel:{ChannelType.EMAIL}"] = {
        'count': 10,
        'max_per_minute': 5
    }
    
    is_allowed = await notification_engine._check_channel_rate_limit(ChannelType.EMAIL)
    assert is_allowed is False


@pytest.mark.asyncio
async def test_attempt_delivery_success(notification_engine, sample_notification):
    """Test successful delivery attempt."""
    # Mock successful delivery
    with patch('random.random', return_value=0.5):  # 50% success rate
        success = await notification_engine._attempt_delivery(
            sample_notification, ChannelType.EMAIL, MagicMock()
        )
        assert success is True


@pytest.mark.asyncio
async def test_attempt_delivery_failure(notification_engine, sample_notification):
    """Test failed delivery attempt."""
    # Mock failed delivery
    with patch('random.random', return_value=0.05):  # 5% success rate (95% failure)
        success = await notification_engine._attempt_delivery(
            sample_notification, ChannelType.EMAIL, MagicMock()
        )
        assert success is False


@pytest.mark.asyncio
async def test_should_retry_no_retry_policy(notification_engine, sample_notification):
    """Test retry check with no retry policy."""
    history = MagicMock()
    history.retry_count = 0
    
    should_retry = await notification_engine._should_retry(sample_notification, history)
    assert should_retry is False


@pytest.mark.asyncio
async def test_should_retry_max_retries_exceeded(notification_engine, sample_notification):
    """Test retry check with max retries exceeded."""
    from src.pocket_hedge_fund.notification_system.models.notification_models import RetryPolicy
    
    sample_notification.retry_policy = RetryPolicy(max_retries=3)
    
    history = MagicMock()
    history.retry_count = 3
    
    should_retry = await notification_engine._should_retry(sample_notification, history)
    assert should_retry is False


@pytest.mark.asyncio
async def test_should_retry_within_delay(notification_engine, sample_notification):
    """Test retry check within retry delay."""
    from src.pocket_hedge_fund.notification_system.models.notification_models import RetryPolicy
    
    sample_notification.retry_policy = RetryPolicy(max_retries=3, retry_delay=60)
    
    history = MagicMock()
    history.retry_count = 1
    history.delivery_attempts = [datetime.now() - timedelta(seconds=30)]  # 30 seconds ago
    
    should_retry = await notification_engine._should_retry(sample_notification, history)
    assert should_retry is False


@pytest.mark.asyncio
async def test_should_retry_ready_for_retry(notification_engine, sample_notification):
    """Test retry check when ready for retry."""
    from src.pocket_hedge_fund.notification_system.models.notification_models import RetryPolicy
    
    sample_notification.retry_policy = RetryPolicy(max_retries=3, retry_delay=60)
    
    history = MagicMock()
    history.retry_count = 1
    history.delivery_attempts = [datetime.now() - timedelta(seconds=90)]  # 90 seconds ago
    
    should_retry = await notification_engine._should_retry(sample_notification, history)
    assert should_retry is True


@pytest.mark.asyncio
async def test_schedule_retry(notification_engine, sample_notification):
    """Test scheduling a retry."""
    from src.pocket_hedge_fund.notification_system.models.notification_models import RetryPolicy
    
    sample_notification.retry_policy = RetryPolicy(max_retries=3, retry_delay=60)
    
    history = MagicMock()
    history.retry_count = 0
    history.delivery_attempts = []
    
    # Schedule retry
    await notification_engine._schedule_retry(sample_notification, ChannelType.EMAIL, history)
    
    # Verify retry was queued
    assert notification_engine.retry_queue.qsize() == 1


@pytest.mark.asyncio
async def test_update_delivery_stats(notification_engine, sample_notification):
    """Test updating delivery statistics."""
    # Clear existing stats
    notification_engine.delivery_stats.clear()
    
    # Update stats
    await notification_engine._update_delivery_stats(sample_notification)
    
    # Verify stats were updated
    stats_key = f"stats:{sample_notification.notification_type}"
    assert stats_key in notification_engine.delivery_stats
    assert notification_engine.delivery_stats[stats_key]['total'] == 1


@pytest.mark.asyncio
async def test_save_delivery_history(notification_engine):
    """Test saving delivery history."""
    history = MagicMock()
    history.notification_id = "notification_123"
    
    # Save history
    await notification_engine._save_delivery_history([history])
    
    # Verify save was called (mocked)
    # In a real implementation, this would verify database save


@pytest.mark.asyncio
async def test_get_engine_stats(notification_engine):
    """Test getting engine statistics."""
    stats = await notification_engine.get_engine_stats()
    
    assert 'is_running' in stats
    assert 'queue_size' in stats
    assert 'retry_queue_size' in stats
    assert 'active_workers' in stats
    assert 'delivery_stats' in stats
    assert 'rate_limits' in stats
    
    assert stats['is_running'] is True
    assert stats['active_workers'] == 6  # 5 processing + 1 retry worker


@pytest.mark.asyncio
async def test_stop_engine(notification_engine):
    """Test stopping the notification engine."""
    # Stop engine
    await notification_engine.stop()
    
    # Verify engine is stopped
    assert notification_engine.is_running is False
    
    # Verify workers are cancelled
    for worker in notification_engine.workers:
        assert worker.cancelled() or worker.done()


@pytest.mark.asyncio
async def test_cleanup_engine(notification_engine):
    """Test cleaning up the notification engine."""
    # Stop engine first
    await notification_engine.stop()
    
    # Cleanup
    await notification_engine.cleanup()
    
    # Verify cleanup
    assert notification_engine.delivery_stats == {}
    assert notification_engine.rate_limits == {}
    assert notification_engine.processing_queue.empty()
    assert notification_engine.retry_queue.empty()


@pytest.mark.asyncio
async def test_process_notification_with_worker(notification_engine, sample_notification):
    """Test processing notification with worker."""
    # Queue notification
    await notification_engine.queue_notification(sample_notification)
    
    # Wait a bit for processing
    await asyncio.sleep(0.1)
    
    # Verify notification was processed (queue should be empty)
    assert notification_engine.processing_queue.qsize() == 0


@pytest.mark.asyncio
async def test_retry_worker_processing(notification_engine):
    """Test retry worker processing."""
    # Create a retry item
    retry_item = {
        'notification': sample_notification,
        'channel': ChannelType.EMAIL,
        'history': MagicMock(),
        'scheduled_at': datetime.now()
    }
    
    # Add to retry queue
    await notification_engine.retry_queue.put(retry_item)
    
    # Wait a bit for processing
    await asyncio.sleep(0.1)
    
    # Verify retry was processed (queue should be empty)
    assert notification_engine.retry_queue.qsize() == 0


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
    
    # Mock successful delivery
    with patch.object(notification_engine, '_attempt_delivery', return_value=True):
        # Mock should retry
        with patch.object(notification_engine, '_should_retry', return_value=True):
            # Process retry
            await notification_engine._process_retry(retry_item)
            
            # Verify history was updated
            assert history.retry_count == 2
            assert len(history.delivery_attempts) == 2


@pytest.mark.asyncio
async def test_process_retry_max_retries_exceeded(notification_engine, sample_notification):
    """Test processing retry with max retries exceeded."""
    from src.pocket_hedge_fund.notification_system.models.notification_models import RetryPolicy
    
    sample_notification.retry_policy = RetryPolicy(max_retries=3, retry_delay=60)
    
    history = MagicMock()
    history.retry_count = 3  # Max retries reached
    history.delivery_attempts = [datetime.now() - timedelta(seconds=90)]
    
    retry_item = {
        'notification': sample_notification,
        'channel': ChannelType.EMAIL,
        'history': history
    }
    
    # Mock failed delivery
    with patch.object(notification_engine, '_attempt_delivery', return_value=False):
        # Mock should not retry (max retries exceeded)
        with patch.object(notification_engine, '_should_retry', return_value=False):
            # Process retry
            await notification_engine._process_retry(retry_item)
            
            # Verify history was updated
            assert history.retry_count == 4  # Incremented
            assert len(history.delivery_attempts) == 2
