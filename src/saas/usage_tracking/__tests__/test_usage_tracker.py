"""
Usage Tracker Tests

Unit tests for the usage tracker service.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock

from ..models import UsageEvent, EventType, EventStatus, UsageMetric, MetricType, MetricValue
from ..services import UsageTracker


class TestUsageTracker:
    """Test cases for UsageTracker service."""
    
    @pytest.fixture
    def mock_storage_backend(self):
        """Mock storage backend."""
        backend = Mock()
        backend.store_event = AsyncMock()
        backend.store_metric = AsyncMock()
        backend.get_metrics = AsyncMock(return_value=[])
        backend.get_current_usage = AsyncMock(return_value=0.0)
        return backend
    
    @pytest.fixture
    def mock_limits_service(self):
        """Mock limits service."""
        service = Mock()
        service.get_active_limits = AsyncMock(return_value=[])
        service.update_usage = AsyncMock()
        return service
    
    @pytest.fixture
    def usage_tracker(self, mock_storage_backend, mock_limits_service):
        """Usage tracker instance with mocked dependencies."""
        return UsageTracker(
            storage_backend=mock_storage_backend,
            limits_service=mock_limits_service
        )
    
    @pytest.fixture
    def sample_event(self):
        """Sample usage event for testing."""
        return UsageEvent(
            tenant_id="tenant-1",
            user_id="user-1",
            event_type=EventType.API_CALL,
            event_name="GET /api/users",
            description="API call to get users",
            resource_consumed="api_calls",
            quantity=1.0,
            unit="calls"
        )
    
    @pytest.mark.asyncio
    async def test_record_event_success(self, usage_tracker, sample_event):
        """Test successful event recording."""
        event_id = await usage_tracker.record_event(sample_event)
        
        assert event_id == sample_event.id
        usage_tracker.storage_backend.store_event.assert_called_once_with(sample_event)
    
    @pytest.mark.asyncio
    async def test_record_event_validation_error(self, usage_tracker):
        """Test event recording with validation error."""
        # Create invalid event (missing tenant_id)
        invalid_event = UsageEvent(
            tenant_id="",  # Invalid: empty tenant_id
            event_type=EventType.API_CALL,
            resource_consumed="api_calls",
            quantity=1.0
        )
        
        with pytest.raises(ValueError, match="Tenant ID is required"):
            await usage_tracker.record_event(invalid_event)
    
    @pytest.mark.asyncio
    async def test_record_api_call(self, usage_tracker):
        """Test API call recording."""
        event_id = await usage_tracker.record_api_call(
            tenant_id="tenant-1",
            user_id="user-1",
            endpoint="/api/users",
            method="GET",
            response_time_ms=150,
            status_code=200
        )
        
        assert event_id is not None
        usage_tracker.storage_backend.store_event.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_record_storage_usage(self, usage_tracker):
        """Test storage usage recording."""
        event_id = await usage_tracker.record_storage_usage(
            tenant_id="tenant-1",
            user_id="user-1",
            operation="write",
            size_bytes=1024,
            file_type="image/jpeg"
        )
        
        assert event_id is not None
        usage_tracker.storage_backend.store_event.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_record_database_query(self, usage_tracker):
        """Test database query recording."""
        event_id = await usage_tracker.record_database_query(
            tenant_id="tenant-1",
            user_id="user-1",
            query_type="select",
            table="users",
            execution_time_ms=50,
            rows_affected=10
        )
        
        assert event_id is not None
        usage_tracker.storage_backend.store_event.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_usage_metrics(self, usage_tracker, mock_storage_backend):
        """Test getting usage metrics."""
        # Mock metrics data
        mock_metrics = [
            UsageMetric(
                tenant_id="tenant-1",
                resource_type="api_calls",
                metric_name="api_calls_usage",
                values={MetricValue.COUNT.value: 100}
            )
        ]
        mock_storage_backend.get_metrics.return_value = mock_metrics
        
        start_date = datetime.now(datetime.UTC) - timedelta(days=7)
        end_date = datetime.now(datetime.UTC)
        
        metrics = await usage_tracker.get_usage_metrics(
            tenant_id="tenant-1",
            resource_type="api_calls",
            period_start=start_date,
            period_end=end_date,
            granularity="hour"
        )
        
        assert len(metrics) == 1
        assert metrics[0].tenant_id == "tenant-1"
        assert metrics[0].resource_type == "api_calls"
        mock_storage_backend.get_metrics.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_current_usage(self, usage_tracker, mock_storage_backend):
        """Test getting current usage."""
        mock_storage_backend.get_current_usage.return_value = 150.0
        
        current_usage = await usage_tracker.get_current_usage(
            tenant_id="tenant-1",
            resource_type="api_calls"
        )
        
        assert current_usage == 150.0
        mock_storage_backend.get_current_usage.assert_called_once_with(
            tenant_id="tenant-1",
            resource_type="api_calls"
        )
    
    @pytest.mark.asyncio
    async def test_check_limit_within_limit(self, usage_tracker, mock_limits_service):
        """Test limit check when within limit."""
        mock_limits_service.get_active_limits.return_value = []
        
        is_within_limit, limit = await usage_tracker.check_limit(
            tenant_id="tenant-1",
            resource_type="api_calls"
        )
        
        assert is_within_limit is True
        assert limit is None
    
    @pytest.mark.asyncio
    async def test_check_limit_exceeded(self, usage_tracker, mock_limits_service):
        """Test limit check when limit is exceeded."""
        from ..models import UsageLimit, LimitType, LimitStatus
        
        exceeded_limit = UsageLimit(
            tenant_id="tenant-1",
            resource_type="api_calls",
            limit_value=100.0,
            current_usage=150.0,  # Exceeded
            status=LimitStatus.ACTIVE
        )
        mock_limits_service.get_active_limits.return_value = [exceeded_limit]
        
        is_within_limit, limit = await usage_tracker.check_limit(
            tenant_id="tenant-1",
            resource_type="api_calls"
        )
        
        assert is_within_limit is False
        assert limit == exceeded_limit
    
    @pytest.mark.asyncio
    async def test_start_and_stop(self, usage_tracker):
        """Test starting and stopping the usage tracker."""
        await usage_tracker.start()
        assert usage_tracker._processing is True
        
        await usage_tracker.stop()
        assert usage_tracker._processing is False
    
    @pytest.mark.asyncio
    async def test_process_single_event(self, usage_tracker, sample_event):
        """Test processing a single event."""
        await usage_tracker._process_single_event(sample_event)
        
        # Verify that storage backend was called
        usage_tracker.storage_backend.store_metric.assert_called_once()
        
        # Verify that limits service was called
        usage_tracker.limits_service.update_usage.assert_called_once_with(sample_event)
    
    @pytest.mark.asyncio
    async def test_get_or_create_metric_existing(self, usage_tracker, mock_storage_backend):
        """Test getting existing metric."""
        existing_metric = UsageMetric(
            tenant_id="tenant-1",
            resource_type="api_calls",
            metric_name="api_calls_usage"
        )
        mock_storage_backend.get_metrics.return_value = [existing_metric]
        
        event = UsageEvent(
            tenant_id="tenant-1",
            resource_consumed="api_calls"
        )
        
        metric = await usage_tracker._get_or_create_metric(event)
        
        assert metric == existing_metric
        mock_storage_backend.get_metrics.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_or_create_metric_new(self, usage_tracker, mock_storage_backend):
        """Test creating new metric when none exists."""
        mock_storage_backend.get_metrics.return_value = []
        
        event = UsageEvent(
            tenant_id="tenant-1",
            resource_consumed="api_calls"
        )
        
        metric = await usage_tracker._get_or_create_metric(event)
        
        assert metric.tenant_id == "tenant-1"
        assert metric.resource_type == "api_calls"
        assert metric.metric_name == "api_calls_usage"
    
    @pytest.mark.asyncio
    async def test_validate_event_success(self, usage_tracker, sample_event):
        """Test successful event validation."""
        # Should not raise any exception
        usage_tracker._validate_event(sample_event)
    
    @pytest.mark.asyncio
    async def test_validate_event_missing_tenant_id(self, usage_tracker):
        """Test event validation with missing tenant ID."""
        invalid_event = UsageEvent(
            tenant_id="",  # Invalid
            event_type=EventType.API_CALL,
            resource_consumed="api_calls",
            quantity=1.0
        )
        
        with pytest.raises(ValueError, match="Tenant ID is required"):
            usage_tracker._validate_event(invalid_event)
    
    @pytest.mark.asyncio
    async def test_validate_event_negative_quantity(self, usage_tracker):
        """Test event validation with negative quantity."""
        invalid_event = UsageEvent(
            tenant_id="tenant-1",
            event_type=EventType.API_CALL,
            resource_consumed="api_calls",
            quantity=-1.0  # Invalid
        )
        
        with pytest.raises(ValueError, match="Quantity cannot be negative"):
            usage_tracker._validate_event(invalid_event)
    
    @pytest.mark.asyncio
    async def test_validate_event_negative_cost(self, usage_tracker):
        """Test event validation with negative cost."""
        invalid_event = UsageEvent(
            tenant_id="tenant-1",
            event_type=EventType.API_CALL,
            resource_consumed="api_calls",
            quantity=1.0,
            cost_per_unit=-1.0  # Invalid
        )
        
        with pytest.raises(ValueError, match="Cost per unit cannot be negative"):
            usage_tracker._validate_event(invalid_event)
