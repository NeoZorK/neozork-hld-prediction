"""
Usage API

This module provides API endpoints for usage tracking functionality.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from aiohttp import web
from aiohttp.web import Request, Response

from ..models import UsageEvent, EventType, EventStatus
from ..services import UsageTracker

logger = logging.getLogger(__name__)


class UsageAPI:
    """
    API endpoints for usage tracking.
    
    This class provides REST API endpoints for:
    - Recording usage events
    - Retrieving usage data
    - Managing usage metrics
    - Real-time usage monitoring
    """
    
    def __init__(self, usage_tracker: UsageTracker):
        """
        Initialize the usage API.
        
        Args:
            usage_tracker: Usage tracker service instance
        """
        self.usage_tracker = usage_tracker
        self.app = web.Application()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes."""
        # Event recording endpoints
        self.app.router.add_post('/api/v1/usage/events', self.record_event)
        self.app.router.add_post('/api/v1/usage/events/batch', self.record_events_batch)
        
        # API call tracking
        self.app.router.add_post('/api/v1/usage/api-calls', self.record_api_call)
        self.app.router.add_post('/api/v1/usage/storage', self.record_storage_usage)
        self.app.router.add_post('/api/v1/usage/database', self.record_database_query)
        
        # Usage retrieval endpoints
        self.app.router.add_get('/api/v1/usage/events', self.get_events)
        self.app.router.add_get('/api/v1/usage/events/{event_id}', self.get_event)
        self.app.router.add_get('/api/v1/usage/metrics', self.get_metrics)
        self.app.router.add_get('/api/v1/usage/current', self.get_current_usage)
        
        # Real-time endpoints
        self.app.router.add_get('/api/v1/usage/stream', self.stream_usage)
        self.app.router.add_get('/api/v1/usage/health', self.health_check)
    
    async def record_event(self, request: Request) -> Response:
        """Record a single usage event."""
        try:
            data = await request.json()
            
            # Create usage event from request data
            event = UsageEvent.from_dict(data)
            
            # Record the event
            event_id = await self.usage_tracker.record_event(event)
            
            return web.json_response({
                "success": True,
                "event_id": event_id,
                "message": "Event recorded successfully"
            })
            
        except Exception as e:
            logger.error(f"Failed to record event: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=400)
    
    async def record_events_batch(self, request: Request) -> Response:
        """Record multiple usage events in batch."""
        try:
            data = await request.json()
            events_data = data.get("events", [])
            
            if not events_data:
                return web.json_response({
                    "success": False,
                    "error": "No events provided"
                }, status=400)
            
            # Create events
            events = []
            for event_data in events_data:
                event = UsageEvent.from_dict(event_data)
                events.append(event)
            
            # Record events
            event_ids = []
            for event in events:
                event_id = await self.usage_tracker.record_event(event)
                event_ids.append(event_id)
            
            return web.json_response({
                "success": True,
                "event_ids": event_ids,
                "count": len(event_ids),
                "message": "Events recorded successfully"
            })
            
        except Exception as e:
            logger.error(f"Failed to record events batch: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=400)
    
    async def record_api_call(self, request: Request) -> Response:
        """Record an API call event."""
        try:
            data = await request.json()
            
            # Extract parameters
            tenant_id = data.get("tenant_id")
            user_id = data.get("user_id")
            endpoint = data.get("endpoint", "")
            method = data.get("method", "GET")
            response_time_ms = data.get("response_time_ms")
            status_code = data.get("status_code", 200)
            
            if not tenant_id:
                return web.json_response({
                    "success": False,
                    "error": "tenant_id is required"
                }, status=400)
            
            # Record API call
            event_id = await self.usage_tracker.record_api_call(
                tenant_id=tenant_id,
                user_id=user_id,
                endpoint=endpoint,
                method=method,
                response_time_ms=response_time_ms,
                status_code=status_code,
                **data.get("metadata", {})
            )
            
            return web.json_response({
                "success": True,
                "event_id": event_id,
                "message": "API call recorded successfully"
            })
            
        except Exception as e:
            logger.error(f"Failed to record API call: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=400)
    
    async def record_storage_usage(self, request: Request) -> Response:
        """Record storage usage event."""
        try:
            data = await request.json()
            
            # Extract parameters
            tenant_id = data.get("tenant_id")
            user_id = data.get("user_id")
            operation = data.get("operation", "write")
            size_bytes = data.get("size_bytes", 0)
            file_type = data.get("file_type", "")
            
            if not tenant_id:
                return web.json_response({
                    "success": False,
                    "error": "tenant_id is required"
                }, status=400)
            
            # Record storage usage
            event_id = await self.usage_tracker.record_storage_usage(
                tenant_id=tenant_id,
                user_id=user_id,
                operation=operation,
                size_bytes=size_bytes,
                file_type=file_type,
                **data.get("metadata", {})
            )
            
            return web.json_response({
                "success": True,
                "event_id": event_id,
                "message": "Storage usage recorded successfully"
            })
            
        except Exception as e:
            logger.error(f"Failed to record storage usage: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=400)
    
    async def record_database_query(self, request: Request) -> Response:
        """Record database query event."""
        try:
            data = await request.json()
            
            # Extract parameters
            tenant_id = data.get("tenant_id")
            user_id = data.get("user_id")
            query_type = data.get("query_type", "select")
            table = data.get("table", "")
            execution_time_ms = data.get("execution_time_ms")
            rows_affected = data.get("rows_affected", 0)
            
            if not tenant_id:
                return web.json_response({
                    "success": False,
                    "error": "tenant_id is required"
                }, status=400)
            
            # Record database query
            event_id = await self.usage_tracker.record_database_query(
                tenant_id=tenant_id,
                user_id=user_id,
                query_type=query_type,
                table=table,
                execution_time_ms=execution_time_ms,
                rows_affected=rows_affected,
                **data.get("metadata", {})
            )
            
            return web.json_response({
                "success": True,
                "event_id": event_id,
                "message": "Database query recorded successfully"
            })
            
        except Exception as e:
            logger.error(f"Failed to record database query: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=400)
    
    async def get_events(self, request: Request) -> Response:
        """Get usage events with filtering."""
        try:
            # Extract query parameters
            tenant_id = request.query.get("tenant_id")
            user_id = request.query.get("user_id")
            resource_type = request.query.get("resource_type")
            event_type = request.query.get("event_type")
            start_date = request.query.get("start_date")
            end_date = request.query.get("end_date")
            limit = int(request.query.get("limit", 100))
            offset = int(request.query.get("offset", 0))
            
            if not tenant_id:
                return web.json_response({
                    "success": False,
                    "error": "tenant_id is required"
                }, status=400)
            
            # Parse dates
            if start_date:
                start_date = datetime.fromisoformat(start_date)
            if end_date:
                end_date = datetime.fromisoformat(end_date)
            
            # Get events from storage backend
            if self.usage_tracker.storage_backend:
                events = await self.usage_tracker.storage_backend.get_events(
                    tenant_id=tenant_id,
                    user_id=user_id,
                    resource_type=resource_type,
                    event_type=event_type,
                    start_date=start_date,
                    end_date=end_date,
                    limit=limit,
                    offset=offset
                )
                
                # Convert to dict format
                events_data = [event.to_dict() for event in events]
                
                return web.json_response({
                    "success": True,
                    "events": events_data,
                    "count": len(events_data)
                })
            else:
                return web.json_response({
                    "success": False,
                    "error": "Storage backend not configured"
                }, status=500)
            
        except Exception as e:
            logger.error(f"Failed to get events: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def get_event(self, request: Request) -> Response:
        """Get a specific usage event by ID."""
        try:
            event_id = request.match_info["event_id"]
            
            if self.usage_tracker.storage_backend:
                event = await self.usage_tracker.storage_backend.get_event(event_id)
                
                if event:
                    return web.json_response({
                        "success": True,
                        "event": event.to_dict()
                    })
                else:
                    return web.json_response({
                        "success": False,
                        "error": "Event not found"
                    }, status=404)
            else:
                return web.json_response({
                    "success": False,
                    "error": "Storage backend not configured"
                }, status=500)
            
        except Exception as e:
            logger.error(f"Failed to get event: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def get_metrics(self, request: Request) -> Response:
        """Get usage metrics."""
        try:
            # Extract query parameters
            tenant_id = request.query.get("tenant_id")
            resource_type = request.query.get("resource_type")
            start_date = request.query.get("start_date")
            end_date = request.query.get("end_date")
            granularity = request.query.get("granularity", "hour")
            
            if not tenant_id:
                return web.json_response({
                    "success": False,
                    "error": "tenant_id is required"
                }, status=400)
            
            # Parse dates
            if start_date:
                start_date = datetime.fromisoformat(start_date)
            else:
                start_date = datetime.now(timezone.utc) - timedelta(days=7)
            
            if end_date:
                end_date = datetime.fromisoformat(end_date)
            else:
                end_date = datetime.now(timezone.utc)
            
            # Get metrics
            metrics = await self.usage_tracker.get_usage_metrics(
                tenant_id=tenant_id,
                resource_type=resource_type,
                period_start=start_date,
                period_end=end_date,
                granularity=granularity
            )
            
            # Convert to dict format
            metrics_data = [metric.to_dict() for metric in metrics]
            
            return web.json_response({
                "success": True,
                "metrics": metrics_data,
                "count": len(metrics_data)
            })
            
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def get_current_usage(self, request: Request) -> Response:
        """Get current usage for a tenant and resource type."""
        try:
            # Extract query parameters
            tenant_id = request.query.get("tenant_id")
            resource_type = request.query.get("resource_type")
            
            if not tenant_id:
                return web.json_response({
                    "success": False,
                    "error": "tenant_id is required"
                }, status=400)
            
            # Get current usage
            current_usage = await self.usage_tracker.get_current_usage(
                tenant_id=tenant_id,
                resource_type=resource_type
            )
            
            return web.json_response({
                "success": True,
                "current_usage": current_usage,
                "resource_type": resource_type,
                "tenant_id": tenant_id
            })
            
        except Exception as e:
            logger.error(f"Failed to get current usage: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def stream_usage(self, request: Request) -> Response:
        """Stream real-time usage data via Server-Sent Events."""
        try:
            tenant_id = request.query.get("tenant_id")
            resource_type = request.query.get("resource_type")
            
            if not tenant_id:
                return web.json_response({
                    "success": False,
                    "error": "tenant_id is required"
                }, status=400)
            
            # Create SSE response
            response = web.StreamResponse()
            response.headers['Content-Type'] = 'text/event-stream'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'keep-alive'
            
            await response.prepare(request)
            
            # Send initial data
            current_usage = await self.usage_tracker.get_current_usage(
                tenant_id=tenant_id,
                resource_type=resource_type
            )
            
            await response.write(f"data: {current_usage}\n\n".encode())
            
            # Keep connection alive (in real implementation, you'd use WebSocket)
            while True:
                await asyncio.sleep(1)
                # In real implementation, you'd check for new data
                # and send updates via SSE
                
        except Exception as e:
            logger.error(f"Failed to stream usage: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
    
    async def health_check(self, request: Request) -> Response:
        """Health check endpoint."""
        return web.json_response({
            "status": "healthy",
            "service": "Usage Tracking API",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
