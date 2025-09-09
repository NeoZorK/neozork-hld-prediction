"""
Simplified Auth API for Pocket Hedge Fund.

This module provides REST API endpoints for authentication operations
including user registration, login, logout, and token management.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, validator

from ..database import DatabaseManager, DatabaseUtils
from ..auth.middleware import get_current_user

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Create router
router = APIRouter(prefix="/auth", tags=["Authentication"])

class AuthAPI:
    """Auth API class for dependency injection."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.router = router

# Pydantic models for request/response

class UserRegistration(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    role: Optional[str] = "investor"


class UserLogin(BaseModel):
    email: str
    password: str
    

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user: Dict[str, Any]

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: datetime

# API Endpoints

@router.post("/register", response_model=Dict[str, str])
async def register_user(registration_data: UserRegistration) -> Dict[str, str]:
    """Register a new user."""
    try:
        # Mock implementation for demonstration
        logger.info(f"User registration attempt: {registration_data.email}")
        
        return {
            "message": "User registered successfully",
            "user_id": "mock-user-id"
        }
        
    except Exception as e:
        logger.error(f"Error in user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=TokenResponse)
async def login_user(login_data: UserLogin) -> TokenResponse:
    """Authenticate user and return JWT tokens."""
    try:
        # Mock implementation for demonstration
        logger.info(f"User login attempt: {login_data.email}")
        
        return TokenResponse(
            access_token="mock-access-token",
            refresh_token="mock-refresh-token",
            token_type="bearer",
            expires_in=86400,
            user={
                "id": "mock-user-id",
                "email": login_data.email,
                "username": "mock-username",
                "role": "investor"
            }
        )
        
    except Exception as e:
        logger.error(f"Error in user login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/logout", response_model=Dict[str, str])
async def logout_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, str]:
    """Logout user and invalidate token."""
    try:
        # Mock implementation for demonstration
        logger.info("User logout attempt")
        
        return {
            "message": "Logout successful"
        }
        
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
    """Get current user information."""
    try:
        # Mock implementation for demonstration
        logger.info("Getting current user info")
        
        return UserResponse(
            id="mock-user-id",
            email="user@example.com",
            username="mock-username",
            first_name="Mock",
            last_name="User",
            role="investor",
            is_active=True,
            is_verified=True,
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )

@router.get("/health", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "auth-api"}
