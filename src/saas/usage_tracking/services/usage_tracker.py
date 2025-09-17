"""
Usage Tracker Service

This service handles the core functionality of tracking usage events,
aggregating metrics, and enforcing limits.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import asdict

from ..models import (
    UsageEvent, EventType, EventStatus,
    UsageMetric, MetricType, MetricValue,
    UsageLimit, LimitType, LimitStatus
)

logger = logging.getLogger(__name__)


class UsageTracker:
    """
    Core service for tracking and managing usage events.
    
    This service provides functionality to:
    - Record usage events
    - Aggregate metrics
    - Check and enforce limits
    - Generate real-time analytics
    """
    
    def __init__(self, storage_backend=None, limits_service=None):
        """
        Initialize the usage tracker.
        
        Args:
            storage_backend: Storage backend for persisting data
            limits_service: Service for managing usage limits
        """
        self.storage_backend = storage_backend
        self.limits_service = limits_service
        self._event_queue = asyncio.Queue()
        self._processing = False
        self._metrics_cache = {}
        
    async def start(self):
        """Start the usage tracker background processing."""
        if self._processing:
            return
            
        self._processing = True
        asyncio.create_task(self._process_events())
        logger.info("Usage tracker started")
    
    async def stop(self):
        """Stop the usage tracker background processing."""
        self._processing = False
        logger.info("Usage tracker stopped")
    
    async def record_event(self, event: UsageEvent) -> str:
        """
        Record a usage event.
        
        Args:
            event: Usage event to record
            
        Returns:
            Event ID
        """
        try:
            # Validate event
            self._validate_event(event)
            
            # Check limits before recording
            if self.limits_service:
                await self._check_limits(event)
            
            # Add to processing queue
            await self._event_queue.put(event)
            
            # Store event immediately for real-time access
            if self.storage_backend:
                await self.storage_backend.store_event(event)
            
            logger.debug(f"Recorded usage event: {event.id}")
            return event.id
            
        except Exception as e:
            logger.error(f"Failed to record usage event: {e}")
            raise
    
    async def record_api_call(self, tenant_id: str, user_id: Optional[str] = None,
                            endpoint: str = "", method: str = "GET",
                            response_time_ms: Optional[int] = None,
                            status_code: int = 200, **kwargs) -> str:
        """
        Record an API call event.
        
        Args:
            tenant_id: Tenant ID
            user_id: User ID (optional)
            endpoint: API endpoint
            method: HTTP method
            response_time_ms: Response time in milliseconds
            status_code: HTTP status code
            **kwargs: Additional event data
            
        Returns:
            Event ID
        """
        event = UsageEvent(
            tenant_id=tenant_id,
            user_id=user_id,
            event_type=EventType.API_CALL,
            event_name=f"{method} {endpoint}",
            description=f"API call to {endpoint}",
            resource_consumed="api_calls",
            quantity=1.0,
            unit="calls",
            duration_ms=response_time_ms,
            metadata={
                "endpoint": endpoint,
                "method": method,
                "status_code": status_code,
                **kwargs
            }
        )
        
        return await self.record_event(event)
    
    async def record_storage_usage(self, tenant_id: str, user_id: Optional[str] = None,
                                 operation: str = "write", size_bytes: int = 0,
                                 file_type: str = "", **kwargs) -> str:
        """
        Record storage usage event.
        
        Args:
            tenant_id: Tenant ID
            user_id: User ID (optional)
            operation: Storage operation (read/write)
            size_bytes: Size in bytes
            file_type: Type of file
            **kwargs: Additional event data
            
        Returns:
            Event ID
        """
        event_type = EventType.STORAGE_WRITE if operation == "write" else EventType.STORAGE_READ
        
        event = UsageEvent(
            tenant_id=tenant_id,
            user_id=user_id,
            event_type=event_type,
            event_name=f"Storage {operation}",
            description=f"Storage {operation} operation",
            resource_consumed="storage_bytes",
            quantity=float(size_bytes),
            unit="bytes",
            metadata={
                "operation": operation,
                "file_type": file_type,
                "size_bytes": size_bytes,
                **kwargs
            }
        )
        
        return await self.record_event(event)
    
    async def record_database_query(self, tenant_id: str, user_id: Optional[str] = None,
                                  query_type: str = "select", table: str = "",
                                  execution_time_ms: Optional[int] = None,
                                  rows_affected: int = 0, **kwargs) -> str:
        """
        Record database query event.
        
        Args:
            tenant_id: Tenant ID
            user_id: User ID (optional)
            query_type: Type of query
            table: Database table
            execution_time_ms: Execution time in milliseconds
            rows_affected: Number of rows affected
            **kwargs: Additional event data
            
        Returns:
            Event ID
        """
        event = UsageEvent(
            tenant_id=tenant_id,
            user_id=user_id,
            event_type=EventType.DATABASE_QUERY,
            event_name=f"DB {query_type}",
            description=f"Database {query_type} on {table}",
            resource_consumed="database_queries",
            quantity=1.0,
            unit="queries",
            duration_ms=execution_time_ms,
            metadata={
                "query_type": query_type,
                "table": table,
                "rows_affected": rows_affected,
                **kwargs
            }
        )
        
        return await self.record_event(event)
    
    async def get_usage_metrics(self, tenant_id: str, resource_type: str,
                              period_start: datetime, period_end: datetime,
                              granularity: str = "hour") -> List[UsageMetric]:
        """
        Get usage metrics for a tenant and resource type.
        
        Args:
            tenant_id: Tenant ID
            resource_type: Resource type
            period_start: Start of period
            period_end: End of period
            granularity: Time granularity
            
        Returns:
            List of usage metrics
        """
        if self.storage_backend:
            return await self.storage_backend.get_metrics(
                tenant_id=tenant_id,
                resource_type=resource_type,
                period_start=period_start,
                period_end=period_end,
                granularity=granularity
            )
        return []
    
    async def get_current_usage(self, tenant_id: str, resource_type: str) -> float:
        """
        Get current usage for a tenant and resource type.
        
        Args:
            tenant_id: Tenant ID
            resource_type: Resource type
            
        Returns:
            Current usage value
        """
        if self.storage_backend:
            return await self.storage_backend.get_current_usage(
                tenant_id=tenant_id,
                resource_type=resource_type
            )
        return 0.0
    
    async def check_limit(self, tenant_id: str, resource_type: str) -> Tuple[bool, Optional[UsageLimit]]:
        """
        Check if usage is within limits.
        
        Args:
            tenant_id: Tenant ID
            resource_type: Resource type
            
        Returns:
            Tuple of (is_within_limit, limit_object)
        """
        if not self.limits_service:
            return True, None
        
        limits = await self.limits_service.get_active_limits(tenant_id, resource_type)
        current_usage = await self.get_current_usage(tenant_id, resource_type)
        
        for limit in limits:
            if limit.is_exceeded():
                return False, limit
        
        return True, None
    
    async def _process_events(self):
        """Process events from the queue."""
        while self._processing:
            try:
                # Get event from queue with timeout
                event = await asyncio.wait_for(self._event_queue.get(), timeout=1.0)
                
                # Process event
                await self._process_single_event(event)
                
                # Mark task as done
                self._event_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing event: {e}")
    
    async def _process_single_event(self, event: UsageEvent):
        """Process a single usage event."""
        try:
            # Update metrics
            await self._update_metrics(event)
            
            # Check for alerts
            await self._check_alerts(event)
            
            # Update limits
            if self.limits_service:
                await self.limits_service.update_usage(event)
            
            logger.debug(f"Processed usage event: {event.id}")
            
        except Exception as e:
            logger.error(f"Failed to process event {event.id}: {e}")
    
    async def _update_metrics(self, event: UsageEvent):
        """Update usage metrics based on event."""
        if not self.storage_backend:
            return
        
        # Get or create metric for current period
        metric = await self._get_or_create_metric(event)
        
        # Update metric with event data
        metric.add_event_data(
            event_count=1,
            user_id=event.user_id,
            session_id=event.session_id,
            cost=event.total_cost
        )
        
        # Update specific values based on event type
        if event.event_type == EventType.API_CALL:
            metric.increment_value(MetricValue.COUNT)
        elif event.event_type in [EventType.STORAGE_READ, EventType.STORAGE_WRITE]:
            metric.increment_value(MetricValue.SUM, event.quantity)
        elif event.event_type == EventType.DATABASE_QUERY:
            metric.increment_value(MetricValue.COUNT)
            if event.duration_ms:
                metric.increment_value(MetricValue.SUM, event.duration_ms)
        
        # Store updated metric
        await self.storage_backend.store_metric(metric)
    
    async def _get_or_create_metric(self, event: UsageEvent) -> UsageMetric:
        """Get or create metric for current period."""
        if not self.storage_backend:
            return UsageMetric()
        
        # Determine granularity based on event type
        granularity = "hour"  # Default granularity
        
        # Get current period
        now = datetime.now(datetime.UTC)
        period_start = self._get_period_start(now, granularity)
        period_end = self._get_period_end(period_start, granularity)
        
        # Try to get existing metric
        metrics = await self.storage_backend.get_metrics(
            tenant_id=event.tenant_id,
            resource_type=event.resource_consumed,
            period_start=period_start,
            period_end=period_end,
            granularity=granularity
        )
        
        if metrics:
            return metrics[0]
        
        # Create new metric
        metric = UsageMetric(
            tenant_id=event.tenant_id,
            metric_name=f"{event.resource_consumed}_usage",
            metric_type=MetricType.COUNTER,
            period_start=period_start,
            period_end=period_end,
            granularity=granularity,
            resource_type=event.resource_consumed,
            value_type=MetricValue.COUNT
        )
        
        return metric
    
    def _get_period_start(self, timestamp: datetime, granularity: str) -> datetime:
        """Get start of period for given granularity."""
        if granularity == "minute":
            return timestamp.replace(second=0, microsecond=0)
        elif granularity == "hour":
            return timestamp.replace(minute=0, second=0, microsecond=0)
        elif granularity == "day":
            return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            return timestamp
    
    def _get_period_end(self, period_start: datetime, granularity: str) -> datetime:
        """Get end of period for given granularity."""
        if granularity == "minute":
            return period_start + timedelta(minutes=1)
        elif granularity == "hour":
            return period_start + timedelta(hours=1)
        elif granularity == "day":
            return period_start + timedelta(days=1)
        else:
            return period_start + timedelta(hours=1)
    
    async def _check_limits(self, event: UsageEvent):
        """Check limits before recording event."""
        if not self.limits_service:
            return
        
        limits = await self.limits_service.get_active_limits(
            event.tenant_id, event.resource_consumed
        )
        
        for limit in limits:
            if limit.should_enforce():
                raise Exception(f"Usage limit exceeded: {limit.limit_name}")
    
    async def _check_alerts(self, event: UsageEvent):
        """Check for alerts based on event."""
        # This would integrate with the alert service
        pass
    
    def _validate_event(self, event: UsageEvent):
        """Validate usage event."""
        if not event.tenant_id:
            raise ValueError("Tenant ID is required")
        
        if not event.event_type:
            raise ValueError("Event type is required")
        
        if event.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        if event.cost_per_unit < 0:
            raise ValueError("Cost per unit cannot be negative")
