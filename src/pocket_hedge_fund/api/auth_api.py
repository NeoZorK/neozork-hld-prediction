"""
Authentication API for Pocket Hedge Fund.

This module provides authentication endpoints for user registration,
login, logout, and token management.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, validator

from ..auth import AuthManager
from ..database import DatabaseManager

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Create router
router = APIRouter(prefix="/auth", tags=["Authentication"])


# Pydantic models for request/response

class UserRegistration(BaseModel):
    """User registration request model."""
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str
    role: Optional[str] = "investor"
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v


class UserLogin(BaseModel):
    """User login request model."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response model."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]


class UserResponse(BaseModel):
    """User response model."""
    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]


class PasswordChange(BaseModel):
    """Password change request model."""
    old_password: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('New password must be at least 8 characters long')
        return v


class RefreshTokenRequest(BaseModel):
    """Refresh token request model."""
    refresh_token: str


# API endpoints

@router.post("/register", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegistration,
    request: Request
) -> Dict[str, Any]:
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        request: HTTP request
        
    Returns:
        Registration result
        
    Raises:
        HTTPException: If registration fails
    """
    try:
        # Get auth manager from app state
        auth_manager: AuthManager = request.app.state.auth_manager
        
        # Register user
        result = await auth_manager.register_user(user_data.dict())
        
        if result['status'] == 'error':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result['message']
            )
        
        logger.info(f"User registered successfully: {user_data.email}")
        
        return {
            'status': 'success',
            'message': 'User registered successfully',
            'user_id': result['user_id'],
            'email': result['email']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    login_data: UserLogin,
    request: Request
) -> TokenResponse:
    """
    Authenticate user and return tokens.
    
    Args:
        login_data: User login data
        request: HTTP request
        
    Returns:
        Authentication tokens and user info
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Get auth manager from app state
        auth_manager: AuthManager = request.app.state.auth_manager
        
        # Authenticate user
        result = await auth_manager.authenticate_user(
            login_data.email,
            login_data.password
        )
        
        if result['status'] == 'error':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result['message']
            )
        
        logger.info(f"User logged in successfully: {login_data.email}")
        
        return TokenResponse(
            access_token=result['token'],
            refresh_token=result.get('refresh_token', ''),
            token_type="bearer",
            expires_in=86400,  # 24 hours
            user=result['user']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in user login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=Dict[str, str])
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    request: Request
) -> Dict[str, str]:
    """
    Refresh access token.
    
    Args:
        refresh_data: Refresh token data
        request: HTTP request
        
    Returns:
        New access token
        
    Raises:
        HTTPException: If token refresh fails
    """
    try:
        # Get auth manager from app state
        auth_manager: AuthManager = request.app.state.auth_manager
        
        # Refresh token
        result = await auth_manager.refresh_token(refresh_data.refresh_token)
        
        if result['status'] == 'error':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result['message']
            )
        
        return {
            'access_token': result['token'],
            'token_type': 'bearer',
            'expires_in': '86400'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refreshing token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout", response_model=Dict[str, str])
async def logout_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, str]:
    """
    Logout user and invalidate session.
    
    Args:
        request: HTTP request
        credentials: HTTP authorization credentials
        
    Returns:
        Logout confirmation
        
    Raises:
        HTTPException: If logout fails
    """
    try:
        # Get auth manager from app state
        auth_manager: AuthManager = request.app.state.auth_manager
        
        # Extract session ID from token (simplified)
        session_id = credentials.credentials  # In real implementation, extract from token
        
        # Logout user
        result = await auth_manager.logout_user(session_id)
        
        if result['status'] == 'error':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result['message']
            )
        
        return {
            'message': 'Logout successful'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in user logout: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserResponse:
    """
    Get current user information.
    
    Args:
        request: HTTP request
        credentials: HTTP authorization credentials
        
    Returns:
        Current user information
        
    Raises:
        HTTPException: If user not found
    """
    try:
        # Get auth manager from app state
        auth_manager: AuthManager = request.app.state.auth_manager
        
        # Verify token
        result = await auth_manager.verify_token(credentials.credentials)
        
        if result['status'] == 'error':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result['message']
            )
        
        user_info = result['user']
        
        return UserResponse(
            id=user_info['id'],
            email=user_info['email'],
            username=user_info['username'],
            first_name=user_info.get('first_name', ''),
            last_name=user_info.get('last_name', ''),
            role=user_info['role'],
            is_active=True,  # If token is valid, user is active
            is_verified=True,  # Simplified
            created_at=datetime.utcnow(),  # Simplified
            last_login=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )


@router.post("/change-password", response_model=Dict[str, str])
async def change_password(
    password_data: PasswordChange,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, str]:
    """
    Change user password.
    
    Args:
        password_data: Password change data
        request: HTTP request
        credentials: HTTP authorization credentials
        
    Returns:
        Password change confirmation
        
    Raises:
        HTTPException: If password change fails
    """
    try:
        # Get auth manager from app state
        auth_manager: AuthManager = request.app.state.auth_manager
        
        # Verify token and get user ID
        result = await auth_manager.verify_token(credentials.credentials)
        
        if result['status'] == 'error':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result['message']
            )
        
        user_id = result['user']['id']
        
        # Change password
        change_result = await auth_manager.change_password(
            user_id,
            password_data.old_password,
            password_data.new_password
        )
        
        if change_result['status'] == 'error':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=change_result['message']
            )
        
        return {
            'message': 'Password changed successfully'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )


@router.get("/permissions", response_model=Dict[str, Any])
async def get_user_permissions(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Get user permissions.
    
    Args:
        request: HTTP request
        credentials: HTTP authorization credentials
        
    Returns:
        User permissions
        
    Raises:
        HTTPException: If permissions retrieval fails
    """
    try:
        # Get auth manager from app state
        auth_manager: AuthManager = request.app.state.auth_manager
        
        # Verify token and get user ID
        result = await auth_manager.verify_token(credentials.credentials)
        
        if result['status'] == 'error':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result['message']
            )
        
        user_id = result['user']['id']
        
        # Get user permissions
        permissions = await auth_manager.get_user_permissions(user_id)
        
        return {
            'permissions': permissions,
            'role': result['user']['role']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user permissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user permissions"
        )


@router.post("/verify-token", response_model=Dict[str, Any])
async def verify_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Verify token validity.
    
    Args:
        request: HTTP request
        credentials: HTTP authorization credentials
        
    Returns:
        Token verification result
        
    Raises:
        HTTPException: If token verification fails
    """
    try:
        # Get auth manager from app state
        auth_manager: AuthManager = request.app.state.auth_manager
        
        # Verify token
        result = await auth_manager.verify_token(credentials.credentials)
        
        if result['status'] == 'error':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result['message']
            )
        
        return {
            'valid': True,
            'user': result['user']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token verification failed"
        )