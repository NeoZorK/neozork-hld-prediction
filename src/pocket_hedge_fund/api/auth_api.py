"""Authentication API - RESTful API endpoints for user authentication and authorization"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, EmailStr
import uuid
import re

# Import our JWT manager
from ..auth.jwt_manager import JWTManager, UserRole, TokenType, AuthResult

logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
security = HTTPBearer()


class UserRegistrationRequest(BaseModel):
    """Request model for user registration."""
    username: str = Field(..., description="Username", min_length=3, max_length=50)
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password", min_length=8, max_length=100)
    first_name: str = Field(..., description="First name", min_length=1, max_length=100)
    last_name: str = Field(..., description="Last name", min_length=1, max_length=100)
    phone: Optional[str] = Field(None, description="Phone number", max_length=20)
    country: Optional[str] = Field(None, description="Country", max_length=100)


class UserLoginRequest(BaseModel):
    """Request model for user login."""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")


class PasswordResetRequest(BaseModel):
    """Request model for password reset."""
    email: EmailStr = Field(..., description="Email address")


class PasswordResetConfirmRequest(BaseModel):
    """Request model for password reset confirmation."""
    token: str = Field(..., description="Reset token")
    new_password: str = Field(..., description="New password", min_length=8, max_length=100)


class ChangePasswordRequest(BaseModel):
    """Request model for changing password."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., description="New password", min_length=8, max_length=100)


class UserResponse(BaseModel):
    """Response model for user data."""
    user_id: str
    username: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    country: Optional[str]
    role: str
    is_active: bool
    kyc_status: str
    created_at: datetime
    updated_at: datetime


class AuthResponse(BaseModel):
    """Response model for authentication."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class TokenRefreshRequest(BaseModel):
    """Request model for token refresh."""
    refresh_token: str = Field(..., description="Refresh token")


class AuthAPI:
    """Authentication API endpoints."""
    
    def __init__(self, database_manager, jwt_manager: JWTManager):
        self.database_manager = database_manager
        self.jwt_manager = jwt_manager
        
    def _validate_password(self, password: str) -> List[str]:
        """Validate password strength."""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r"\d", password):
            errors.append("Password must contain at least one digit")
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            errors.append("Password must contain at least one special character")
        
        return errors
    
    def _validate_username(self, username: str) -> List[str]:
        """Validate username format."""
        errors = []
        
        if len(username) < 3:
            errors.append("Username must be at least 3 characters long")
        
        if len(username) > 50:
            errors.append("Username must be less than 50 characters")
        
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            errors.append("Username can only contain letters, numbers, underscores, and hyphens")
        
        return errors
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
        """Get current authenticated user from token."""
        try:
            token = credentials.credentials
            payload = self.jwt_manager.verify_token(token, TokenType.ACCESS)
            
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Get user details from database
            user_query = """
            SELECT * FROM users WHERE id = :user_id
            """
            
            user_result = await self.database_manager.execute_query(
                user_query, 
                {"user_id": payload.user_id}
            )
            
            if 'error' in user_result or not user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_data = user_result['query_result']['data'][0]
            
            return {
                "user_id": user_data['id'],
                "username": user_data['username'],
                "email": user_data['email'],
                "role": payload.role,
                "permissions": payload.permissions,
                "is_active": user_data['is_active']
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get current user: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @router.post("/register", response_model=AuthResponse, status_code=201)
    async def register_user(self, request: UserRegistrationRequest) -> AuthResponse:
        """Register a new user."""
        try:
            # Validate username
            username_errors = self._validate_username(request.username)
            if username_errors:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Username validation failed: {', '.join(username_errors)}"
                )
            
            # Validate password
            password_errors = self._validate_password(request.password)
            if password_errors:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Password validation failed: {', '.join(password_errors)}"
                )
            
            # Check if username already exists
            username_check_query = "SELECT id FROM users WHERE username = :username"
            username_result = await self.database_manager.execute_query(
                username_check_query, 
                {"username": request.username}
            )
            
            if 'error' in username_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database error during username check"
                )
            
            if username_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            
            # Check if email already exists
            email_check_query = "SELECT id FROM users WHERE email = :email"
            email_result = await self.database_manager.execute_query(
                email_check_query, 
                {"email": request.email}
            )
            
            if 'error' in email_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database error during email check"
                )
            
            if email_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
            
            # Hash password
            hashed_password = self.jwt_manager.hash_password(request.password)
            
            # Create user
            user_id = str(uuid.uuid4())
            insert_query = """
            INSERT INTO users (
                id, username, email, password_hash, first_name, last_name,
                phone, country, kyc_status, is_active, is_admin
            ) VALUES (
                :user_id, :username, :email, :password_hash, :first_name, :last_name,
                :phone, :country, :kyc_status, :is_active, :is_admin
            )
            """
            
            insert_params = {
                "user_id": user_id,
                "username": request.username,
                "email": request.email,
                "password_hash": hashed_password,
                "first_name": request.first_name,
                "last_name": request.last_name,
                "phone": request.phone,
                "country": request.country,
                "kyc_status": "pending",
                "is_active": True,
                "is_admin": False
            }
            
            insert_result = await self.database_manager.execute_query(insert_query, insert_params)
            
            if 'error' in insert_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to create user: {insert_result['error']}"
                )
            
            # Get created user
            user_query = "SELECT * FROM users WHERE id = :user_id"
            user_result = await self.database_manager.execute_query(
                user_query, 
                {"user_id": user_id}
            )
            
            if 'error' in user_result or not user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve created user"
                )
            
            user_data = user_result['query_result']['data'][0]
            
            # Create tokens
            user_role = UserRole.INVESTOR  # Default role for new users
            permissions = self.jwt_manager.get_user_permissions(user_role)
            
            access_token = self.jwt_manager.create_access_token(
                user_id=user_id,
                username=request.username,
                email=request.email,
                role=user_role,
                permissions=permissions
            )
            
            refresh_token = self.jwt_manager.create_refresh_token(
                user_id=user_id,
                username=request.username,
                email=request.email,
                role=user_role,
                permissions=permissions
            )
            
            logger.info(f"User registered successfully: {request.username}")
            
            return AuthResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=self.jwt_manager.access_token_expire_minutes * 60,
                user=UserResponse(
                    user_id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    phone=user_data['phone'],
                    country=user_data['country'],
                    role=user_role.value,
                    is_active=user_data['is_active'],
                    kyc_status=user_data['kyc_status'],
                    created_at=user_data['created_at'],
                    updated_at=user_data['updated_at']
                )
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to register user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.post("/login", response_model=AuthResponse)
    async def login_user(self, request: UserLoginRequest) -> AuthResponse:
        """Login user with username/email and password."""
        try:
            # Find user by username or email
            user_query = """
            SELECT * FROM users 
            WHERE (username = :identifier OR email = :identifier) 
            AND is_active = true
            """
            
            user_result = await self.database_manager.execute_query(
                user_query, 
                {"identifier": request.username}
            )
            
            if 'error' in user_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database error during login"
                )
            
            if not user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            user_data = user_result['query_result']['data'][0]
            
            # Verify password
            if not self.jwt_manager.verify_password(request.password, user_data['password_hash']):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            # Determine user role
            user_role = UserRole.ADMIN if user_data['is_admin'] else UserRole.INVESTOR
            permissions = self.jwt_manager.get_user_permissions(user_role)
            
            # Create tokens
            access_token = self.jwt_manager.create_access_token(
                user_id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                role=user_role,
                permissions=permissions
            )
            
            refresh_token = self.jwt_manager.create_refresh_token(
                user_id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                role=user_role,
                permissions=permissions
            )
            
            logger.info(f"User logged in successfully: {user_data['username']}")
            
            return AuthResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=self.jwt_manager.access_token_expire_minutes * 60,
                user=UserResponse(
                    user_id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    phone=user_data['phone'],
                    country=user_data['country'],
                    role=user_role.value,
                    is_active=user_data['is_active'],
                    kyc_status=user_data['kyc_status'],
                    created_at=user_data['created_at'],
                    updated_at=user_data['updated_at']
                )
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to login user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.post("/refresh", response_model=Dict[str, Any])
    async def refresh_token(self, request: TokenRefreshRequest) -> Dict[str, Any]:
        """Refresh access token using refresh token."""
        try:
            new_access_token = self.jwt_manager.refresh_access_token(request.refresh_token)
            
            if not new_access_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired refresh token"
                )
            
            return {
                "access_token": new_access_token,
                "token_type": "bearer",
                "expires_in": self.jwt_manager.access_token_expire_minutes * 60
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to refresh token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.post("/logout")
    async def logout_user(
        self, 
        current_user: Dict[str, Any] = Depends(get_current_user),
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> Dict[str, Any]:
        """Logout user by blacklisting the token."""
        try:
            token = credentials.credentials
            success = self.jwt_manager.blacklist_token(token)
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to logout"
                )
            
            logger.info(f"User logged out successfully: {current_user['username']}")
            
            return {
                "message": "Successfully logged out"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to logout user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.get("/me", response_model=UserResponse)
    async def get_current_user_info(
        self, 
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> UserResponse:
        """Get current user information."""
        try:
            # Get full user details from database
            user_query = "SELECT * FROM users WHERE id = :user_id"
            user_result = await self.database_manager.execute_query(
                user_query, 
                {"user_id": current_user['user_id']}
            )
            
            if 'error' in user_result or not user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            user_data = user_result['query_result']['data'][0]
            
            return UserResponse(
                user_id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
                country=user_data['country'],
                role=current_user['role'].value,
                is_active=user_data['is_active'],
                kyc_status=user_data['kyc_status'],
                created_at=user_data['created_at'],
                updated_at=user_data['updated_at']
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get user info: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.post("/change-password")
    async def change_password(
        self,
        request: ChangePasswordRequest,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Change user password."""
        try:
            # Validate new password
            password_errors = self._validate_password(request.new_password)
            if password_errors:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Password validation failed: {', '.join(password_errors)}"
                )
            
            # Get current user data
            user_query = "SELECT password_hash FROM users WHERE id = :user_id"
            user_result = await self.database_manager.execute_query(
                user_query, 
                {"user_id": current_user['user_id']}
            )
            
            if 'error' in user_result or not user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            current_password_hash = user_result['query_result']['data'][0]['password_hash']
            
            # Verify current password
            if not self.jwt_manager.verify_password(request.current_password, current_password_hash):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Current password is incorrect"
                )
            
            # Hash new password
            new_password_hash = self.jwt_manager.hash_password(request.new_password)
            
            # Update password
            update_query = """
            UPDATE users 
            SET password_hash = :new_password_hash, updated_at = CURRENT_TIMESTAMP
            WHERE id = :user_id
            """
            
            update_result = await self.database_manager.execute_query(
                update_query, 
                {
                    "new_password_hash": new_password_hash,
                    "user_id": current_user['user_id']
                }
            )
            
            if 'error' in update_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to update password: {update_result['error']}"
                )
            
            logger.info(f"Password changed successfully for user: {current_user['username']}")
            
            return {
                "message": "Password changed successfully"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to change password: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


# Create router instance
def create_auth_api_router(database_manager, jwt_manager: JWTManager) -> APIRouter:
    """Create and configure the authentication API router."""
    api = AuthAPI(database_manager, jwt_manager)
    
    # Add the router methods to the router
    router.add_api_route("/register", api.register_user, methods=["POST"])
    router.add_api_route("/login", api.login_user, methods=["POST"])
    router.add_api_route("/refresh", api.refresh_token, methods=["POST"])
    router.add_api_route("/logout", api.logout_user, methods=["POST"])
    router.add_api_route("/me", api.get_current_user_info, methods=["GET"])
    router.add_api_route("/change-password", api.change_password, methods=["POST"])
    
    return router
