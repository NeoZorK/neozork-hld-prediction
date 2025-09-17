"""
Authentication middleware for Pocket Hedge Fund.

This module provides middleware for request authentication, authorization,
and security features.
"""

import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import asyncio

from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .auth_manager import AuthManager
from .jwt_handler import JWTHandler
from .permissions import PermissionManager

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware for Pocket Hedge Fund.
    
    Provides request authentication, authorization, and security features.
    """
    
    def __init__(self, app, auth_manager: AuthManager):
        """
        Initialize authentication middleware.
        
        Args:
            app: FastAPI application
            auth_manager: Authentication manager instance
        """
        super().__init__(app)
        self.auth_manager = auth_manager
        self.jwt_handler = JWTHandler()
        self.permission_manager = PermissionManager()
        
        # Public endpoints that don't require authentication
        self.public_endpoints = {
            '/',
            '/health',
            '/docs',
            '/openapi.json',
            '/auth/login',
            '/auth/register',
            '/auth/refresh',
            '/auth/forgot-password',
            '/auth/reset-password'
        }
        
        # Rate limiting (simple in-memory implementation)
        self.rate_limits: Dict[str, Dict[str, Any]] = {}
        self.rate_limit_window = 60  # seconds
        self.rate_limit_max_requests = 100
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request through authentication middleware.
        
        Args:
            request: HTTP request
            call_next: Next middleware/handler
            
        Returns:
            HTTP response
        """
        try:
            # Check if endpoint is public
            if self._is_public_endpoint(request.url.path):
                return await call_next(request)
            
            # Rate limiting
            if not await self._check_rate_limit(request):
                return Response(
                    content="Rate limit exceeded",
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS
                )
            
            # Extract and verify token
            token = await self._extract_token(request)
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication token required",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Verify token
            user_info = await self._verify_token(token)
            if not user_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Add user info to request state
            request.state.user = user_info
            
            # Check authorization for protected endpoints
            if not self._is_public_endpoint(request.url.path):
                if not await self._check_authorization(request, user_info):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient permissions"
                    )
            
            # Process request
            response = await call_next(request)
            
            # Add security headers
            self._add_security_headers(response)
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication middleware error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication error"
            )
    
    def _is_public_endpoint(self, path: str) -> bool:
        """
        Check if endpoint is public.
        
        Args:
            path: Request path
            
        Returns:
            True if endpoint is public, False otherwise
        """
        # Exact match
        if path in self.public_endpoints:
            return True
        
        # Pattern matching for API versions
        for public_endpoint in self.public_endpoints:
            if path.startswith(public_endpoint):
                return True
        
        return False
    
    async def _extract_token(self, request: Request) -> Optional[str]:
        """
        Extract JWT token from request.
        
        Args:
            request: HTTP request
            
        Returns:
            JWT token string or None
        """
        try:
            # Try Authorization header
            authorization = request.headers.get("Authorization")
            if authorization and authorization.startswith("Bearer "):
                return authorization.split(" ")[1]
            
            # Try query parameter
            token = request.query_params.get("token")
            if token:
                return token
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting token: {e}")
            return None
    
    async def _verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            User information or None
        """
        try:
            # Verify token with auth manager
            result = await self.auth_manager.verify_token(token)
            if result['status'] == 'success':
                return result['user']
            
            return None
            
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return None
    
    async def _check_authorization(self, request: Request, user_info: Dict[str, Any]) -> bool:
        """
        Check if user is authorized for the request.
        
        Args:
            request: HTTP request
            user_info: User information
            
        Returns:
            True if authorized, False otherwise
        """
        try:
            # Extract resource and action from path and method
            resource, action = self._extract_resource_action(request)
            if not resource or not action:
                return True  # Allow if we can't determine resource/action
            
            # Check permission
            return await self.auth_manager.check_permission(
                user_info['id'],
                resource,
                action
            )
            
        except Exception as e:
            logger.error(f"Error checking authorization: {e}")
            return False
    
    def _extract_resource_action(self, request: Request) -> tuple[Optional[str], Optional[str]]:
        """
        Extract resource and action from request.
        
        Args:
            request: HTTP request
            
        Returns:
            Tuple of (resource, action) or (None, None)
        """
        try:
            path = request.url.path
            method = request.method.upper()
            
            # Map HTTP methods to actions
            method_actions = {
                'GET': 'read',
                'POST': 'create',
                'PUT': 'update',
                'PATCH': 'update',
                'DELETE': 'delete'
            }
            
            action = method_actions.get(method)
            if not action:
                return None, None
            
            # Extract resource from path
            # Example: /api/v1/funds -> funds
            path_parts = path.strip('/').split('/')
            if len(path_parts) >= 2 and path_parts[0] == 'api':
                # Skip version part
                resource = path_parts[2] if len(path_parts) > 2 else path_parts[1]
                return resource, action
            
            return None, None
            
        except Exception as e:
            logger.error(f"Error extracting resource/action: {e}")
            return None, None
    
    async def _check_rate_limit(self, request: Request) -> bool:
        """
        Check rate limit for request.
        
        Args:
            request: HTTP request
            
        Returns:
            True if within rate limit, False otherwise
        """
        try:
            # Get client IP
            client_ip = request.client.host if request.client else "unknown"
            
            current_time = datetime.now(datetime.UTC)
            
            # Clean old entries
            self._cleanup_rate_limits(current_time)
            
            # Check rate limit
            if client_ip in self.rate_limits:
                client_data = self.rate_limits[client_ip]
                
                # Check if within window
                if (current_time - client_data['window_start']).seconds < self.rate_limit_window:
                    if client_data['request_count'] >= self.rate_limit_max_requests:
                        return False
                    client_data['request_count'] += 1
                else:
                    # Reset window
                    client_data['window_start'] = current_time
                    client_data['request_count'] = 1
            else:
                # New client
                self.rate_limits[client_ip] = {
                    'window_start': current_time,
                    'request_count': 1
                }
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True  # Allow on error
    
    def _cleanup_rate_limits(self, current_time: datetime):
        """Cleanup old rate limit entries."""
        try:
            expired_ips = []
            for ip, data in self.rate_limits.items():
                if (current_time - data['window_start']).seconds > self.rate_limit_window * 2:
                    expired_ips.append(ip)
            
            for ip in expired_ips:
                del self.rate_limits[ip]
                
        except Exception as e:
            logger.error(f"Error cleaning up rate limits: {e}")
    
    def _add_security_headers(self, response: Response):
        """
        Add security headers to response.
        
        Args:
            response: HTTP response
        """
        try:
            # Security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response.headers["Content-Security-Policy"] = "default-src 'self'"
            
        except Exception as e:
            logger.error(f"Error adding security headers: {e}")


# Dependency functions for FastAPI

async def get_current_user(request: Request) -> Dict[str, Any]:
    """
    Get current authenticated user.
    
    Args:
        request: HTTP request
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user is not authenticated
    """
    if not hasattr(request.state, 'user'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    return request.state.user


async def get_current_user_id(request: Request) -> str:
    """
    Get current user ID.
    
    Args:
        request: HTTP request
        
    Returns:
        User ID
        
    Raises:
        HTTPException: If user is not authenticated
    """
    user = await get_current_user(request)
    return user['id']


async def require_permission(resource: str, action: str):
    """
    Create dependency that requires specific permission.
    
    Args:
        resource: Resource name
        action: Action name
        
    Returns:
        Dependency function
    """
    async def permission_dependency(request: Request):
        user = await get_current_user(request)
        
        # Check permission
        auth_manager = request.app.state.auth_manager
        has_permission = await auth_manager.check_permission(
            user['id'],
            resource,
            action
        )
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions for {resource}:{action}"
            )
        
        return user
    
    return permission_dependency


async def require_role(required_role: str):
    """
    Create dependency that requires specific role.
    
    Args:
        required_role: Required role
        
    Returns:
        Dependency function
    """
    async def role_dependency(request: Request):
        user = await get_current_user(request)
        
        if user['role'] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {required_role} required"
            )
        
        return user
    
    return role_dependency


async def require_admin(request: Request):
    """
    Require admin role.
    
    Args:
        request: HTTP request
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user is not admin
    """
    return await require_role("admin")(request)


async def require_fund_manager(request: Request):
    """
    Require fund manager role.
    
    Args:
        request: HTTP request
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user is not fund manager
    """
    user = await get_current_user(request)
    
    if user['role'] not in ['admin', 'fund_manager']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Fund manager role required"
        )
    
    return user


# Token extraction utility

async def extract_token_from_request(request: Request) -> Optional[str]:
    """
    Extract JWT token from request.
    
    Args:
        request: HTTP request
        
    Returns:
        JWT token or None
    """
    try:
        # Try Authorization header
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            return authorization.split(" ")[1]
        
        # Try query parameter
        return request.query_params.get("token")
        
    except Exception:
        return None
