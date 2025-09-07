"""
Tenant Middleware for SaaS Platform

This middleware handles tenant identification, routing, and data isolation
for the multi-tenant SaaS platform.
"""

import logging
from typing import Dict, Optional, Any
from aiohttp import web
from aiohttp.web import Request, Response
import re

logger = logging.getLogger(__name__)


class TenantMiddleware:
    """
    Middleware for tenant identification and routing.
    
    This middleware:
    - Identifies tenant from subdomain, path, or header
    - Validates tenant existence and status
    - Adds tenant context to request
    - Handles tenant-specific routing
    """
    
    def __init__(self, tenant_service):
        self.tenant_service = tenant_service
        self.tenant_patterns = [
            r'^([a-zA-Z0-9-]+)\.',  # subdomain pattern
            r'^/tenant/([a-zA-Z0-9-]+)/',  # path pattern
        ]
    
    async def __call__(self, request: Request, handler) -> Response:
        """Process request and identify tenant."""
        try:
            # Extract tenant identifier
            tenant_id = await self._extract_tenant_id(request)
            
            if tenant_id:
                # Validate tenant
                tenant = await self.tenant_service.get_tenant(tenant_id)
                
                if not tenant:
                    return web.json_response(
                        {'error': 'Tenant not found'}, 
                        status=404
                    )
                
                if not tenant.is_active():
                    return web.json_response(
                        {'error': 'Tenant is not active'}, 
                        status=403
                    )
                
                # Add tenant context to request
                request['tenant'] = tenant
                request['tenant_id'] = tenant_id
                
                logger.debug(f"Request routed to tenant: {tenant.tenant_slug}")
            
            # Continue to next handler
            return await handler(request)
            
        except Exception as e:
            logger.error(f"Error in tenant middleware: {e}")
            return web.json_response(
                {'error': 'Internal server error'}, 
                status=500
            )
    
    async def _extract_tenant_id(self, request: Request) -> Optional[str]:
        """Extract tenant ID from request."""
        # Method 1: Check X-Tenant-ID header
        tenant_id = request.headers.get('X-Tenant-ID')
        if tenant_id:
            return tenant_id
        
        # Method 2: Check subdomain
        host = request.headers.get('Host', '')
        for pattern in self.tenant_patterns:
            match = re.search(pattern, host)
            if match:
                tenant_slug = match.group(1)
                # Convert slug to tenant ID
                tenant = await self.tenant_service.get_tenant_by_slug(tenant_slug)
                if tenant:
                    return tenant.tenant_id
        
        # Method 3: Check path parameter
        path = request.path
        for pattern in self.tenant_patterns:
            match = re.search(pattern, path)
            if match:
                tenant_slug = match.group(1)
                # Convert slug to tenant ID
                tenant = await self.tenant_service.get_tenant_by_slug(tenant_slug)
                if tenant:
                    return tenant.tenant_id
        
        # Method 4: Check query parameter
        tenant_slug = request.query.get('tenant')
        if tenant_slug:
            tenant = await self.tenant_service.get_tenant_by_slug(tenant_slug)
            if tenant:
                return tenant.tenant_id
        
        return None
    
    def get_tenant_from_request(self, request: Request) -> Optional[Any]:
        """Get tenant from request context."""
        return request.get('tenant')
    
    def get_tenant_id_from_request(self, request: Request) -> Optional[str]:
        """Get tenant ID from request context."""
        return request.get('tenant_id')


class TenantContextMiddleware:
    """
    Middleware for adding tenant context to all requests.
    """
    
    def __init__(self, tenant_service):
        self.tenant_service = tenant_service
    
    async def __call__(self, request: Request, handler) -> Response:
        """Add tenant context to request."""
        try:
            # Get tenant from request
            tenant = request.get('tenant')
            tenant_id = request.get('tenant_id')
            
            if tenant and tenant_id:
                # Add tenant context
                request['tenant_context'] = {
                    'tenant_id': tenant_id,
                    'tenant_slug': tenant.tenant_slug,
                    'tenant_name': tenant.name,
                    'tenant_type': tenant.tenant_type.value,
                    'tenant_status': tenant.status.value,
                    'features': tenant.features,
                    'limits': tenant.limits,
                    'settings': tenant.settings
                }
                
                logger.debug(f"Added tenant context for: {tenant.tenant_slug}")
            
            return await handler(request)
            
        except Exception as e:
            logger.error(f"Error in tenant context middleware: {e}")
            return await handler(request)


class TenantIsolationMiddleware:
    """
    Middleware for ensuring tenant data isolation.
    """
    
    def __init__(self):
        self.isolation_checks = []
    
    async def __call__(self, request: Request, handler) -> Response:
        """Ensure tenant data isolation."""
        try:
            tenant_id = request.get('tenant_id')
            
            if tenant_id:
                # Add tenant isolation context
                request['isolation_context'] = {
                    'tenant_id': tenant_id,
                    'data_scope': f'tenant:{tenant_id}',
                    'access_pattern': 'tenant_isolated'
                }
                
                # Perform isolation checks
                await self._perform_isolation_checks(request)
            
            return await handler(request)
            
        except Exception as e:
            logger.error(f"Error in tenant isolation middleware: {e}")
            return web.json_response(
                {'error': 'Data isolation error'}, 
                status=500
            )
    
    async def _perform_isolation_checks(self, request: Request):
        """Perform tenant data isolation checks."""
        tenant_id = request.get('tenant_id')
        
        # Check 1: Ensure all data queries are tenant-scoped
        if hasattr(request, 'data_queries'):
            for query in request.data_queries:
                if not query.get('tenant_id') == tenant_id:
                    raise ValueError("Query not properly tenant-scoped")
        
        # Check 2: Validate file access is tenant-scoped
        if hasattr(request, 'file_access'):
            for file_path in request.file_access:
                if not file_path.startswith(f'/tenant/{tenant_id}/'):
                    raise ValueError("File access not properly tenant-scoped")
        
        # Check 3: Ensure API calls are tenant-aware
        if hasattr(request, 'api_calls'):
            for api_call in request.api_calls:
                if not api_call.get('tenant_id') == tenant_id:
                    raise ValueError("API call not properly tenant-scoped")


class TenantRoutingMiddleware:
    """
    Middleware for tenant-specific routing and URL rewriting.
    """
    
    def __init__(self, tenant_service):
        self.tenant_service = tenant_service
        self.routing_rules = {}
    
    async def __call__(self, request: Request, handler) -> Response:
        """Handle tenant-specific routing."""
        try:
            tenant = request.get('tenant')
            if not tenant:
                return await handler(request)
            
            # Apply tenant-specific routing rules
            original_path = request.path
            new_path = await self._apply_routing_rules(tenant, original_path)
            
            if new_path != original_path:
                # Update request path
                request._path = new_path
                logger.debug(f"Routed {original_path} -> {new_path} for tenant: {tenant.tenant_slug}")
            
            return await handler(request)
            
        except Exception as e:
            logger.error(f"Error in tenant routing middleware: {e}")
            return await handler(request)
    
    async def _apply_routing_rules(self, tenant, path: str) -> str:
        """Apply tenant-specific routing rules."""
        # Example routing rules
        routing_rules = tenant.settings.get('routing_rules', {})
        
        for pattern, replacement in routing_rules.items():
            if re.match(pattern, path):
                return re.sub(pattern, replacement, path)
        
        return path
    
    def add_routing_rule(self, tenant_id: str, pattern: str, replacement: str):
        """Add a routing rule for a specific tenant."""
        if tenant_id not in self.routing_rules:
            self.routing_rules[tenant_id] = []
        
        self.routing_rules[tenant_id].append({
            'pattern': pattern,
            'replacement': replacement
        })
