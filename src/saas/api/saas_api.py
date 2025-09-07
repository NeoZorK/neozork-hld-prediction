"""
Main SaaS API for NeoZork Trading Platform

This module provides the main API endpoints for the SaaS platform,
integrating all SaaS services and providing a unified interface.
"""

import logging
from aiohttp import web
from aiohttp.web import Request, Response
from typing import Dict, Any
import json

from ..services import (
    TenantService,
    SubscriptionService,
    BillingService,
    CustomerService,
    UsageService,
    PlanService
)
from ..auth import SaaSUserManager
from ..middleware import TenantMiddleware, RateLimitMiddleware, UsageTrackingMiddleware

logger = logging.getLogger(__name__)


class SaaSAPI:
    """
    Main SaaS API that provides unified access to all SaaS services.
    
    This API provides:
    - Tenant management endpoints
    - Subscription and billing endpoints
    - Customer management endpoints
    - Usage tracking endpoints
    - Authentication and authorization endpoints
    - System administration endpoints
    """
    
    def __init__(self):
        # Initialize services
        self.tenant_service = TenantService()
        self.subscription_service = SubscriptionService()
        self.billing_service = BillingService()
        self.customer_service = CustomerService()
        self.usage_service = UsageService()
        self.plan_service = PlanService()
        
        # Initialize authentication
        self.user_manager = SaaSUserManager()
        
        # Initialize middleware
        self.tenant_middleware = TenantMiddleware(self.tenant_service)
        self.rate_limit_middleware = RateLimitMiddleware()
        self.usage_tracking_middleware = UsageTrackingMiddleware()
        
        # Create web application
        self.app = web.Application()
        self._setup_middleware()
        self._setup_routes()
    
    def _setup_middleware(self):
        """Setup middleware stack."""
        self.app.middlewares.append(self.tenant_middleware)
        self.app.middlewares.append(self.rate_limit_middleware)
        self.app.middlewares.append(self.usage_tracking_middleware)
        self.app.middlewares.append(self._error_handler_middleware)
        self.app.middlewares.append(self._cors_middleware)
    
    def _setup_routes(self):
        """Setup API routes."""
        # Health check
        self.app.router.add_get('/health', self.health_check)
        
        # Tenant routes
        self.app.router.add_post('/api/v1/tenants', self.create_tenant)
        self.app.router.add_get('/api/v1/tenants/{tenant_id}', self.get_tenant)
        self.app.router.add_put('/api/v1/tenants/{tenant_id}', self.update_tenant)
        self.app.router.add_delete('/api/v1/tenants/{tenant_id}', self.delete_tenant)
        self.app.router.add_get('/api/v1/tenants', self.list_tenants)
        
        # Subscription routes
        self.app.router.add_post('/api/v1/tenants/{tenant_id}/subscriptions', self.create_subscription)
        self.app.router.add_get('/api/v1/tenants/{tenant_id}/subscriptions', self.get_tenant_subscription)
        self.app.router.add_put('/api/v1/subscriptions/{subscription_id}', self.update_subscription)
        self.app.router.add_post('/api/v1/subscriptions/{subscription_id}/cancel', self.cancel_subscription)
        
        # Customer routes
        self.app.router.add_post('/api/v1/tenants/{tenant_id}/customers', self.create_customer)
        self.app.router.add_get('/api/v1/tenants/{tenant_id}/customers', self.list_tenant_customers)
        self.app.router.add_get('/api/v1/customers/{customer_id}', self.get_customer)
        self.app.router.add_put('/api/v1/customers/{customer_id}', self.update_customer)
        
        # Usage routes
        self.app.router.add_post('/api/v1/usage', self.record_usage)
        self.app.router.add_get('/api/v1/tenants/{tenant_id}/usage', self.get_tenant_usage)
        self.app.router.add_get('/api/v1/usage/analytics', self.get_usage_analytics)
        
        # Plan routes
        self.app.router.add_get('/api/v1/plans', self.list_plans)
        self.app.router.add_get('/api/v1/plans/{plan_id}', self.get_plan)
        
        # Authentication routes
        self.app.router.add_post('/api/v1/auth/login', self.authenticate_user)
        self.app.router.add_post('/api/v1/auth/logout', self.logout_user)
        self.app.router.add_get('/api/v1/auth/me', self.get_current_user)
        
        # System administration routes
        self.app.router.add_get('/api/v1/admin/stats', self.get_system_stats)
        self.app.router.add_get('/api/v1/admin/tenants', self.admin_list_tenants)
        self.app.router.add_get('/api/v1/admin/subscriptions', self.admin_list_subscriptions)
    
    # Health check endpoint
    async def health_check(self, request: Request) -> Response:
        """Health check endpoint."""
        return web.json_response({
            "status": "healthy",
            "service": "NeoZork SaaS API",
            "version": "1.0.0"
        })
    
    # Tenant endpoints
    async def create_tenant(self, request: Request) -> Response:
        """Create a new tenant."""
        try:
            data = await request.json()
            
            result = await self.tenant_service.create_tenant(
                name=data.get('name'),
                email=data.get('email'),
                tenant_type=data.get('tenant_type', 'individual'),
                trial_days=data.get('trial_days', 14)
            )
            
            if result['status'] == 'success':
                return web.json_response(result, status=201)
            else:
                return web.json_response(result, status=400)
                
        except Exception as e:
            logger.error(f"Error creating tenant: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def get_tenant(self, request: Request) -> Response:
        """Get tenant by ID."""
        try:
            tenant_id = request.match_info['tenant_id']
            tenant = await self.tenant_service.get_tenant(tenant_id)
            
            if tenant:
                return web.json_response({
                    'status': 'success',
                    'tenant': tenant.to_dict()
                })
            else:
                return web.json_response(
                    {'error': 'Tenant not found'}, 
                    status=404
                )
                
        except Exception as e:
            logger.error(f"Error getting tenant: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def update_tenant(self, request: Request) -> Response:
        """Update tenant."""
        try:
            tenant_id = request.match_info['tenant_id']
            data = await request.json()
            
            result = await self.tenant_service.update_tenant(tenant_id, data)
            
            if result['status'] == 'success':
                return web.json_response(result)
            else:
                return web.json_response(result, status=400)
                
        except Exception as e:
            logger.error(f"Error updating tenant: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def delete_tenant(self, request: Request) -> Response:
        """Delete tenant."""
        try:
            tenant_id = request.match_info['tenant_id']
            
            result = await self.tenant_service.delete_tenant(tenant_id)
            
            if result['status'] == 'success':
                return web.json_response(result)
            else:
                return web.json_response(result, status=400)
                
        except Exception as e:
            logger.error(f"Error deleting tenant: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def list_tenants(self, request: Request) -> Response:
        """List tenants with optional filtering."""
        try:
            # Get query parameters
            status = request.query.get('status')
            tenant_type = request.query.get('tenant_type')
            limit = int(request.query.get('limit', 100))
            offset = int(request.query.get('offset', 0))
            
            result = await self.tenant_service.list_tenants(
                status=status,
                tenant_type=tenant_type,
                limit=limit,
                offset=offset
            )
            
            return web.json_response(result)
            
        except Exception as e:
            logger.error(f"Error listing tenants: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    # Subscription endpoints
    async def create_subscription(self, request: Request) -> Response:
        """Create subscription for tenant."""
        try:
            tenant_id = request.match_info['tenant_id']
            data = await request.json()
            
            # Get plan
            plan_id = data.get('plan_id')
            plan = await self.plan_service.get_plan(plan_id)
            
            if not plan:
                return web.json_response(
                    {'error': 'Plan not found'}, 
                    status=404
                )
            
            result = await self.subscription_service.create_subscription(
                tenant_id=tenant_id,
                plan=plan,
                billing_cycle=data.get('billing_cycle', 'monthly'),
                trial_days=data.get('trial_days', 0)
            )
            
            if result['status'] == 'success':
                return web.json_response(result, status=201)
            else:
                return web.json_response(result, status=400)
                
        except Exception as e:
            logger.error(f"Error creating subscription: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def get_tenant_subscription(self, request: Request) -> Response:
        """Get subscription for tenant."""
        try:
            tenant_id = request.match_info['tenant_id']
            subscription = await self.subscription_service.get_tenant_subscription(tenant_id)
            
            if subscription:
                return web.json_response({
                    'status': 'success',
                    'subscription': subscription.to_dict()
                })
            else:
                return web.json_response(
                    {'error': 'Subscription not found'}, 
                    status=404
                )
                
        except Exception as e:
            logger.error(f"Error getting tenant subscription: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def update_subscription(self, request: Request) -> Response:
        """Update subscription."""
        try:
            subscription_id = request.match_info['subscription_id']
            data = await request.json()
            
            result = await self.subscription_service.update_subscription(subscription_id, data)
            
            if result['status'] == 'success':
                return web.json_response(result)
            else:
                return web.json_response(result, status=400)
                
        except Exception as e:
            logger.error(f"Error updating subscription: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def cancel_subscription(self, request: Request) -> Response:
        """Cancel subscription."""
        try:
            subscription_id = request.match_info['subscription_id']
            data = await request.json()
            
            result = await self.subscription_service.cancel_subscription(
                subscription_id, 
                data.get('effective_date')
            )
            
            if result['status'] == 'success':
                return web.json_response(result)
            else:
                return web.json_response(result, status=400)
                
        except Exception as e:
            logger.error(f"Error cancelling subscription: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    # Customer endpoints
    async def create_customer(self, request: Request) -> Response:
        """Create customer for tenant."""
        try:
            tenant_id = request.match_info['tenant_id']
            data = await request.json()
            
            result = await self.customer_service.create_customer(
                tenant_id=tenant_id,
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                customer_type=data.get('customer_type', 'viewer')
            )
            
            if result['status'] == 'success':
                return web.json_response(result, status=201)
            else:
                return web.json_response(result, status=400)
                
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def list_tenant_customers(self, request: Request) -> Response:
        """List customers for tenant."""
        try:
            tenant_id = request.match_info['tenant_id']
            
            result = await self.customer_service.list_tenant_customers(tenant_id)
            
            return web.json_response(result)
            
        except Exception as e:
            logger.error(f"Error listing tenant customers: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def get_customer(self, request: Request) -> Response:
        """Get customer by ID."""
        try:
            customer_id = request.match_info['customer_id']
            customer = await self.customer_service.get_customer(customer_id)
            
            if customer:
                return web.json_response({
                    'status': 'success',
                    'customer': customer.to_dict()
                })
            else:
                return web.json_response(
                    {'error': 'Customer not found'}, 
                    status=404
                )
                
        except Exception as e:
            logger.error(f"Error getting customer: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def update_customer(self, request: Request) -> Response:
        """Update customer."""
        try:
            customer_id = request.match_info['customer_id']
            data = await request.json()
            
            result = await self.customer_service.update_customer(customer_id, data)
            
            if result['status'] == 'success':
                return web.json_response(result)
            else:
                return web.json_response(result, status=400)
                
        except Exception as e:
            logger.error(f"Error updating customer: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    # Usage endpoints
    async def record_usage(self, request: Request) -> Response:
        """Record usage."""
        try:
            data = await request.json()
            
            result = await self.usage_service.record_usage(
                tenant_id=data.get('tenant_id'),
                customer_id=data.get('customer_id'),
                usage_type=data.get('usage_type'),
                amount=data.get('amount'),
                metadata=data.get('metadata', {})
            )
            
            if result['status'] == 'success':
                return web.json_response(result, status=201)
            else:
                return web.json_response(result, status=400)
                
        except Exception as e:
            logger.error(f"Error recording usage: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def get_tenant_usage(self, request: Request) -> Response:
        """Get usage for tenant."""
        try:
            tenant_id = request.match_info['tenant_id']
            
            result = await self.usage_service.get_tenant_usage(tenant_id)
            
            return web.json_response(result)
            
        except Exception as e:
            logger.error(f"Error getting tenant usage: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def get_usage_analytics(self, request: Request) -> Response:
        """Get usage analytics."""
        try:
            # Get query parameters
            tenant_id = request.query.get('tenant_id')
            start_date = request.query.get('start_date')
            end_date = request.query.get('end_date')
            
            result = await self.usage_service.get_usage_analytics(
                tenant_id=tenant_id,
                start_date=start_date,
                end_date=end_date
            )
            
            return web.json_response(result)
            
        except Exception as e:
            logger.error(f"Error getting usage analytics: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    # Plan endpoints
    async def list_plans(self, request: Request) -> Response:
        """List available plans."""
        try:
            result = await self.plan_service.list_plans()
            
            return web.json_response(result)
            
        except Exception as e:
            logger.error(f"Error listing plans: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def get_plan(self, request: Request) -> Response:
        """Get plan by ID."""
        try:
            plan_id = request.match_info['plan_id']
            plan = await self.plan_service.get_plan(plan_id)
            
            if plan:
                return web.json_response({
                    'status': 'success',
                    'plan': plan.to_dict()
                })
            else:
                return web.json_response(
                    {'error': 'Plan not found'}, 
                    status=404
                )
                
        except Exception as e:
            logger.error(f"Error getting plan: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    # Authentication endpoints
    async def authenticate_user(self, request: Request) -> Response:
        """Authenticate user."""
        try:
            data = await request.json()
            
            result = await self.user_manager.authenticate_tenant_user(
                username=data.get('username'),
                password=data.get('password'),
                tenant_id=data.get('tenant_id'),
                mfa_code=data.get('mfa_code')
            )
            
            if result['status'] == 'success':
                return web.json_response(result)
            else:
                return web.json_response(result, status=401)
                
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def logout_user(self, request: Request) -> Response:
        """Logout user."""
        try:
            # Implementation would depend on session management
            return web.json_response({
                'status': 'success',
                'message': 'User logged out successfully'
            })
            
        except Exception as e:
            logger.error(f"Error logging out user: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def get_current_user(self, request: Request) -> Response:
        """Get current user information."""
        try:
            # Implementation would depend on session management
            return web.json_response({
                'status': 'success',
                'user': {
                    'user_id': 'current_user_id',
                    'username': 'current_user',
                    'tenant_id': 'current_tenant_id'
                }
            })
            
        except Exception as e:
            logger.error(f"Error getting current user: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    # System administration endpoints
    async def get_system_stats(self, request: Request) -> Response:
        """Get system statistics."""
        try:
            tenant_stats = await self.tenant_service.get_system_stats()
            subscription_stats = await self.subscription_service.get_system_stats()
            user_stats = await self.user_manager.get_system_user_stats()
            
            return web.json_response({
                'status': 'success',
                'stats': {
                    'tenants': tenant_stats.get('stats', {}),
                    'subscriptions': subscription_stats.get('stats', {}),
                    'users': user_stats.get('stats', {})
                }
            })
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def admin_list_tenants(self, request: Request) -> Response:
        """Admin endpoint to list all tenants."""
        try:
            result = await self.tenant_service.list_tenants()
            
            return web.json_response(result)
            
        except Exception as e:
            logger.error(f"Error listing tenants (admin): {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def admin_list_subscriptions(self, request: Request) -> Response:
        """Admin endpoint to list all subscriptions."""
        try:
            result = await self.subscription_service.list_subscriptions()
            
            return web.json_response(result)
            
        except Exception as e:
            logger.error(f"Error listing subscriptions (admin): {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    # Middleware methods
    async def _error_handler_middleware(self, request: Request, handler):
        """Error handling middleware."""
        try:
            return await handler(request)
        except Exception as e:
            logger.error(f"Unhandled error: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def _cors_middleware(self, request: Request, handler):
        """CORS middleware."""
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Tenant-ID'
        return response
    
    def run(self, host: str = '0.0.0.0', port: int = 8080):
        """Run the SaaS API server."""
        logger.info(f"Starting NeoZork SaaS API on {host}:{port}")
        web.run_app(self.app, host=host, port=port)
