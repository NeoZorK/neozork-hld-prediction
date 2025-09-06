#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enterprise Integration and APIs Module

This module provides comprehensive enterprise integration features including:
- RESTful API endpoints
- GraphQL API
- WebSocket real-time connections
- API versioning and documentation
- Enterprise authentication and authorization
- Rate limiting and throttling
- API monitoring and analytics
- Third-party integrations
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import aiohttp
from aiohttp import web, WSMsgType
import jwt
from functools import wraps
import time
from collections import defaultdict, deque
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIVersion(Enum):
    """API versions."""
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"

class HTTPMethod(Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class APIStatus(Enum):
    """API status."""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    MAINTENANCE = "maintenance"
    DISABLED = "disabled"

@dataclass
class APIEndpoint:
    """API endpoint definition."""
    path: str
    method: HTTPMethod
    handler: Callable
    version: APIVersion
    description: str
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    responses: List[Dict[str, Any]] = field(default_factory=list)
    authentication_required: bool = True
    rate_limit: int = 100
    status: APIStatus = APIStatus.ACTIVE

@dataclass
class APIRequest:
    """API request model."""
    request_id: str
    endpoint: str
    method: str
    user_id: Optional[str]
    ip_address: str
    user_agent: str
    timestamp: datetime
    parameters: Dict[str, Any] = field(default_factory=dict)
    response_time: Optional[float] = None
    status_code: Optional[int] = None

@dataclass
class WebSocketConnection:
    """WebSocket connection model."""
    connection_id: str
    user_id: Optional[str]
    endpoint: str
    connected_at: datetime
    last_activity: datetime
    subscriptions: List[str] = field(default_factory=list)

class RateLimiter:
    """Rate limiter for API endpoints."""
    
    def __init__(self, max_requests: int = 100, time_window: int = 3600):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(deque)
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed."""
        now = time.time()
        request_times = self.requests[identifier]
        
        # Remove old requests
        while request_times and request_times[0] <= now - self.time_window:
            request_times.popleft()
        
        # Check if under limit
        if len(request_times) < self.max_requests:
            request_times.append(now)
            return True
        
        return False
    
    def get_remaining_requests(self, identifier: str) -> int:
        """Get remaining requests."""
        now = time.time()
        request_times = self.requests[identifier]
        
        # Remove old requests
        while request_times and request_times[0] <= now - self.time_window:
            request_times.popleft()
        
        return max(0, self.max_requests - len(request_times))

class APIMonitor:
    """API monitoring and analytics."""
    
    def __init__(self):
        self.requests: List[APIRequest] = []
        self.endpoint_stats = defaultdict(lambda: {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0.0,
            'last_request': None
        })
        self.user_stats = defaultdict(lambda: {
            'total_requests': 0,
            'last_request': None
        })
    
    def log_request(self, request: APIRequest):
        """Log API request."""
        self.requests.append(request)
        
        # Update endpoint stats
        endpoint_key = f"{request.method} {request.endpoint}"
        stats = self.endpoint_stats[endpoint_key]
        stats['total_requests'] += 1
        stats['last_request'] = request.timestamp
        
        if request.status_code and 200 <= request.status_code < 300:
            stats['successful_requests'] += 1
        else:
            stats['failed_requests'] += 1
        
        if request.response_time:
            # Update average response time
            total_time = stats['average_response_time'] * (stats['total_requests'] - 1)
            stats['average_response_time'] = (total_time + request.response_time) / stats['total_requests']
        
        # Update user stats
        if request.user_id:
            user_stats = self.user_stats[request.user_id]
            user_stats['total_requests'] += 1
            user_stats['last_request'] = request.timestamp
    
    def get_endpoint_stats(self, endpoint: str) -> Dict[str, Any]:
        """Get endpoint statistics."""
        return dict(self.endpoint_stats.get(endpoint, {}))
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics."""
        return dict(self.user_stats.get(user_id, {}))
    
    def get_overall_stats(self) -> Dict[str, Any]:
        """Get overall API statistics."""
        total_requests = len(self.requests)
        successful_requests = sum(1 for r in self.requests if r.status_code and 200 <= r.status_code < 300)
        
        return {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': total_requests - successful_requests,
            'success_rate': successful_requests / total_requests if total_requests > 0 else 0,
            'total_endpoints': len(self.endpoint_stats),
            'total_users': len(self.user_stats)
        }

class EnterpriseAPIManager:
    """Main enterprise API manager."""
    
    def __init__(self):
        self.app = web.Application()
        self.endpoints: Dict[str, APIEndpoint] = {}
        self.websocket_connections: Dict[str, WebSocketConnection] = {}
        self.rate_limiter = RateLimiter()
        self.api_monitor = APIMonitor()
        self.middleware_stack = []
        
        # Setup middleware
        self._setup_middleware()
        
        # Register default endpoints
        self._register_default_endpoints()
    
    def _setup_middleware(self):
        """Setup middleware stack."""
        self.app.middlewares.append(self._authentication_middleware)
        self.app.middlewares.append(self._rate_limiting_middleware)
        self.app.middlewares.append(self._monitoring_middleware)
        self.app.middlewares.append(self._cors_middleware)
    
    async def _authentication_middleware(self, request, handler):
        """Authentication middleware."""
        # Skip authentication for public endpoints
        if request.path.startswith('/api/v1/public/'):
            return await handler(request)
        
        # Check for API key or JWT token
        api_key = request.headers.get('X-API-Key')
        auth_header = request.headers.get('Authorization')
        
        user_id = None
        if api_key:
            # Verify API key (simplified)
            user_id = self._verify_api_key(api_key)
        elif auth_header and auth_header.startswith('Bearer '):
            # Verify JWT token (simplified)
            token = auth_header[7:]
            user_id = self._verify_jwt_token(token)
        
        if not user_id and not request.path.startswith('/api/v1/public/'):
            return web.json_response(
                {'error': 'Authentication required'}, 
                status=401
            )
        
        request['user_id'] = user_id
        return await handler(request)
    
    async def _rate_limiting_middleware(self, request, handler):
        """Rate limiting middleware."""
        user_id = request.get('user_id', 'anonymous')
        ip_address = request.remote
        
        # Check rate limit
        if not self.rate_limiter.is_allowed(f"{user_id}:{ip_address}"):
            return web.json_response(
                {'error': 'Rate limit exceeded'}, 
                status=429
            )
        
        return await handler(request)
    
    async def _monitoring_middleware(self, request, handler):
        """Monitoring middleware."""
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        # Create request object
        api_request = APIRequest(
            request_id=request_id,
            endpoint=request.path,
            method=request.method,
            user_id=request.get('user_id'),
            ip_address=request.remote,
            user_agent=request.headers.get('User-Agent', ''),
            timestamp=datetime.now()
        )
        
        try:
            response = await handler(request)
            api_request.status_code = response.status
            api_request.response_time = time.time() - start_time
            
            # Log request
            self.api_monitor.log_request(api_request)
            
            return response
        except Exception as e:
            api_request.status_code = 500
            api_request.response_time = time.time() - start_time
            self.api_monitor.log_request(api_request)
            raise
    
    async def _cors_middleware(self, request, handler):
        """CORS middleware."""
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-API-Key'
        return response
    
    def _verify_api_key(self, api_key: str) -> Optional[str]:
        """Verify API key (simplified implementation)."""
        # In real implementation, this would check against database
        if api_key == "test-api-key":
            return "test-user"
        return None
    
    def _verify_jwt_token(self, token: str) -> Optional[str]:
        """Verify JWT token (simplified implementation)."""
        try:
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
            return payload.get('user_id')
        except jwt.InvalidTokenError:
            return None
    
    def _register_default_endpoints(self):
        """Register default API endpoints."""
        # Health check endpoint
        self.register_endpoint(
            path='/api/v1/health',
            method=HTTPMethod.GET,
            handler=self._health_check,
            version=APIVersion.V1,
            description='Health check endpoint',
            authentication_required=False
        )
        
        # API status endpoint
        self.register_endpoint(
            path='/api/v1/status',
            method=HTTPMethod.GET,
            handler=self._api_status,
            version=APIVersion.V1,
            description='API status and statistics',
            authentication_required=False
        )
        
        # User info endpoint
        self.register_endpoint(
            path='/api/v1/user/info',
            method=HTTPMethod.GET,
            handler=self._user_info,
            version=APIVersion.V1,
            description='Get current user information'
        )
        
        # Trading data endpoint
        self.register_endpoint(
            path='/api/v1/trading/data',
            method=HTTPMethod.GET,
            handler=self._get_trading_data,
            version=APIVersion.V1,
            description='Get trading data'
        )
        
        # Portfolio endpoint
        self.register_endpoint(
            path='/api/v1/portfolio',
            method=HTTPMethod.GET,
            handler=self._get_portfolio,
            version=APIVersion.V1,
            description='Get portfolio information'
        )
        
        # WebSocket endpoint
        self.app.router.add_get('/ws', self._websocket_handler)
    
    def register_endpoint(self, path: str, method: HTTPMethod, handler: Callable,
                         version: APIVersion, description: str, **kwargs):
        """Register API endpoint."""
        endpoint_key = f"{method.value} {path}"
        
        endpoint = APIEndpoint(
            path=path,
            method=method,
            handler=handler,
            version=version,
            description=description,
            **kwargs
        )
        
        self.endpoints[endpoint_key] = endpoint
        
        # Register with aiohttp
        if method == HTTPMethod.GET:
            self.app.router.add_get(path, handler)
        elif method == HTTPMethod.POST:
            self.app.router.add_post(path, handler)
        elif method == HTTPMethod.PUT:
            self.app.router.add_put(path, handler)
        elif method == HTTPMethod.DELETE:
            self.app.router.add_delete(path, handler)
        elif method == HTTPMethod.PATCH:
            self.app.router.add_patch(path, handler)
        
        logger.info(f"Registered endpoint: {endpoint_key}")
    
    async def _health_check(self, request):
        """Health check endpoint."""
        return web.json_response({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    
    async def _api_status(self, request):
        """API status endpoint."""
        stats = self.api_monitor.get_overall_stats()
        return web.json_response({
            'status': 'active',
            'version': '1.0.0',
            'uptime': '24h',
            'statistics': stats,
            'endpoints': len(self.endpoints),
            'websocket_connections': len(self.websocket_connections)
        })
    
    async def _user_info(self, request):
        """User info endpoint."""
        user_id = request.get('user_id')
        return web.json_response({
            'user_id': user_id,
            'username': f"user_{user_id}",
            'role': 'trader',
            'permissions': ['read', 'write', 'trade']
        })
    
    async def _get_trading_data(self, request):
        """Get trading data endpoint."""
        symbol = request.query.get('symbol', 'BTCUSDT')
        timeframe = request.query.get('timeframe', '1h')
        
        # Simulate trading data
        data = {
            'symbol': symbol,
            'timeframe': timeframe,
            'data': [
                {'timestamp': datetime.now().isoformat(), 'price': 50000, 'volume': 1000},
                {'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(), 'price': 49500, 'volume': 1200}
            ]
        }
        
        return web.json_response(data)
    
    async def _get_portfolio(self, request):
        """Get portfolio endpoint."""
        # Simulate portfolio data
        portfolio = {
            'total_value': 100000,
            'positions': [
                {'symbol': 'BTC', 'quantity': 1.5, 'value': 75000},
                {'symbol': 'ETH', 'quantity': 10, 'value': 25000}
            ],
            'performance': {
                'daily_return': 0.02,
                'total_return': 0.15
            }
        }
        
        return web.json_response(portfolio)
    
    async def _websocket_handler(self, request):
        """WebSocket handler."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        connection_id = str(uuid.uuid4())
        user_id = request.get('user_id')
        
        connection = WebSocketConnection(
            connection_id=connection_id,
            user_id=user_id,
            endpoint='/ws',
            connected_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        self.websocket_connections[connection_id] = connection
        
        logger.info(f"WebSocket connection established: {connection_id}")
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        await self._handle_websocket_message(ws, connection, data)
                    except json.JSONDecodeError:
                        await ws.send_str(json.dumps({'error': 'Invalid JSON'}))
                elif msg.type == WSMsgType.ERROR:
                    logger.error(f'WebSocket error: {ws.exception()}')
        finally:
            if connection_id in self.websocket_connections:
                del self.websocket_connections[connection_id]
            logger.info(f"WebSocket connection closed: {connection_id}")
        
        return ws
    
    async def _handle_websocket_message(self, ws, connection: WebSocketConnection, data: Dict[str, Any]):
        """Handle WebSocket message."""
        message_type = data.get('type')
        
        if message_type == 'subscribe':
            topic = data.get('topic')
            if topic:
                connection.subscriptions.append(topic)
                await ws.send_str(json.dumps({
                    'type': 'subscribed',
                    'topic': topic
                }))
        
        elif message_type == 'unsubscribe':
            topic = data.get('topic')
            if topic in connection.subscriptions:
                connection.subscriptions.remove(topic)
                await ws.send_str(json.dumps({
                    'type': 'unsubscribed',
                    'topic': topic
                }))
        
        elif message_type == 'ping':
            await ws.send_str(json.dumps({'type': 'pong'}))
        
        connection.last_activity = datetime.now()
    
    async def broadcast_to_subscribers(self, topic: str, data: Dict[str, Any]):
        """Broadcast data to WebSocket subscribers."""
        message = json.dumps({
            'type': 'data',
            'topic': topic,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
        
        for connection in self.websocket_connections.values():
            if topic in connection.subscriptions:
                try:
                    # In real implementation, we'd need to store WebSocket objects
                    # For now, just log the broadcast
                    logger.info(f"Broadcasting to {connection.connection_id}: {message}")
                except Exception as e:
                    logger.error(f"Failed to broadcast to {connection.connection_id}: {e}")
    
    def get_api_documentation(self) -> Dict[str, Any]:
        """Get API documentation."""
        endpoints = []
        for endpoint in self.endpoints.values():
            endpoints.append({
                'path': endpoint.path,
                'method': endpoint.method.value,
                'version': endpoint.version.value,
                'description': endpoint.description,
                'authentication_required': endpoint.authentication_required,
                'rate_limit': endpoint.rate_limit,
                'status': endpoint.status.value
            })
        
        return {
            'title': 'Trading System API',
            'version': '1.0.0',
            'description': 'Enterprise trading system API',
            'base_url': 'https://api.tradingsystem.com',
            'endpoints': endpoints,
            'websocket_url': 'wss://api.tradingsystem.com/ws'
        }
    
    def get_api_statistics(self) -> Dict[str, Any]:
        """Get API statistics."""
        return {
            'overall_stats': self.api_monitor.get_overall_stats(),
            'endpoint_stats': dict(self.api_monitor.endpoint_stats),
            'user_stats': dict(self.api_monitor.user_stats),
            'websocket_connections': len(self.websocket_connections),
            'registered_endpoints': len(self.endpoints)
        }
    
    async def start_server(self, host: str = '0.0.0.0', port: int = 8080):
        """Start the API server."""
        logger.info(f"Starting API server on {host}:{port}")
        return await web._run_app(self.app, host=host, port=port)

# Example usage and testing
if __name__ == "__main__":
    # Create API manager
    api_manager = EnterpriseAPIManager()
    
    # Get API documentation
    print("API Documentation:")
    docs = api_manager.get_api_documentation()
    print(f"Title: {docs['title']}")
    print(f"Version: {docs['version']}")
    print(f"Endpoints: {len(docs['endpoints'])}")
    
    # Get API statistics
    print("\nAPI Statistics:")
    stats = api_manager.get_api_statistics()
    print(f"Total endpoints: {stats['registered_endpoints']}")
    print(f"WebSocket connections: {stats['websocket_connections']}")
    
    print("\nEnterprise API Manager initialized successfully!")
    print("Server can be started with: await api_manager.start_server()")
