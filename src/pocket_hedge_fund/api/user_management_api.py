"""User Management API - RESTful API endpoints for user management"""

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

# Import our components
from ..auth.jwt_manager import JWTManager, UserRole, TokenType

logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter(prefix="/api/v1/users", tags=["user-management"])
security = HTTPBearer()


class CreateUserRequest(BaseModel):
    """Request model for creating a new user."""
    username: str = Field(..., description="Username", min_length=3, max_length=50)
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password", min_length=8, max_length=128)
    first_name: str = Field(..., description="First name", min_length=1, max_length=100)
    last_name: str = Field(..., description="Last name", min_length=1, max_length=100)
    role: Optional[str] = Field("INVESTOR", description="User role")
    phone: Optional[str] = Field(None, description="Phone number", max_length=20)
    country: Optional[str] = Field(None, description="Country", max_length=100)
    timezone: Optional[str] = Field("UTC", description="Timezone", max_length=50)


class UpdateUserRequest(BaseModel):
    """Request model for updating user information."""
    first_name: Optional[str] = Field(None, description="First name", min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, description="Last name", min_length=1, max_length=100)
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number", max_length=20)
    country: Optional[str] = Field(None, description="Country", max_length=100)
    timezone: Optional[str] = Field(None, description="Timezone", max_length=50)
    is_active: Optional[bool] = Field(None, description="User active status")


class ChangePasswordRequest(BaseModel):
    """Request model for changing user password."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., description="New password", min_length=8, max_length=128)


class AssignRoleRequest(BaseModel):
    """Request model for assigning roles to users."""
    user_id: str = Field(..., description="User ID")
    role: str = Field(..., description="Role to assign")


class UserResponse(BaseModel):
    """Response model for user data."""
    user_id: str
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    phone: Optional[str]
    country: Optional[str]
    timezone: str
    is_active: bool
    email_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]


class UserListResponse(BaseModel):
    """Response model for user list."""
    users: List[UserResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int


class UserStatsResponse(BaseModel):
    """Response model for user statistics."""
    total_users: int
    active_users: int
    inactive_users: int
    users_by_role: Dict[str, int]
    new_users_today: int
    new_users_this_week: int
    new_users_this_month: int


class UserManagementAPI:
    """User management API endpoints."""
    
    def __init__(self, database_manager, jwt_manager: JWTManager):
        self.database_manager = database_manager
        self.jwt_manager = jwt_manager
        
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
    
    def _check_permission(self, user_permissions: List[str], required_permission: str) -> bool:
        """Check if user has required permission."""
        return self.jwt_manager.has_permission(user_permissions, required_permission)
    
    def _validate_password(self, password: str) -> Dict[str, Any]:
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
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    def _validate_username(self, username: str) -> Dict[str, Any]:
        """Validate username format."""
        errors = []
        
        if len(username) < 3:
            errors.append("Username must be at least 3 characters long")
        
        if len(username) > 50:
            errors.append("Username must be at most 50 characters long")
        
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            errors.append("Username can only contain letters, numbers, underscores, and hyphens")
        
        if username.startswith('-') or username.endswith('-'):
            errors.append("Username cannot start or end with a hyphen")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    def _is_valid_uuid(self, uuid_string: str) -> bool:
        """Validate UUID format."""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False
    
    @router.post("/", response_model=UserResponse)
    async def create_user(
        self,
        request: CreateUserRequest = ...,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> UserResponse:
        """Create a new user."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "users:create"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to create users"
                )
            
            # Validate username
            username_validation = self._validate_username(request.username)
            if not username_validation['is_valid']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid username: {', '.join(username_validation['errors'])}"
                )
            
            # Validate password
            password_validation = self._validate_password(request.password)
            if not password_validation['is_valid']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid password: {', '.join(password_validation['errors'])}"
                )
            
            # Validate role
            try:
                user_role = UserRole(request.role.upper())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid role: {request.role}. Valid roles are: {', '.join([r.value for r in UserRole])}"
                )
            
            # Check if username already exists
            username_check_query = "SELECT id FROM users WHERE username = :username"
            username_check_result = await self.database_manager.execute_query(
                username_check_query,
                {"username": request.username}
            )
            
            if 'error' not in username_check_result and username_check_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            
            # Check if email already exists
            email_check_query = "SELECT id FROM users WHERE email = :email"
            email_check_result = await self.database_manager.execute_query(
                email_check_query,
                {"email": request.email}
            )
            
            if 'error' not in email_check_result and email_check_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
            
            # Hash password
            hashed_password = self.jwt_manager.hash_password(request.password)
            
            # Create user
            user_id = str(uuid.uuid4())
            create_user_query = """
            INSERT INTO users (
                id, username, email, password_hash, first_name, last_name,
                role, phone, country, timezone, is_active, email_verified,
                created_at, updated_at
            ) VALUES (
                :id, :username, :email, :password_hash, :first_name, :last_name,
                :role, :phone, :country, :timezone, :is_active, :email_verified,
                :created_at, :updated_at
            )
            """
            
            now = datetime.now()
            create_params = {
                "id": user_id,
                "username": request.username,
                "email": request.email,
                "password_hash": hashed_password,
                "first_name": request.first_name,
                "last_name": request.last_name,
                "role": user_role.value,
                "phone": request.phone,
                "country": request.country,
                "timezone": request.timezone,
                "is_active": True,
                "email_verified": False,
                "created_at": now,
                "updated_at": now
            }
            
            create_result = await self.database_manager.execute_query(create_user_query, create_params)
            
            if 'error' in create_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to create user: {create_result['error']}"
                )
            
            # Get created user
            get_user_query = "SELECT * FROM users WHERE id = :user_id"
            get_user_result = await self.database_manager.execute_query(
                get_user_query,
                {"user_id": user_id}
            )
            
            if 'error' in get_user_result or not get_user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve created user"
                )
            
            user_data = get_user_result['query_result']['data'][0]
            
            logger.info(f"User created successfully: {request.username} ({user_id})")
            
            return UserResponse(
                user_id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role'],
                phone=user_data['phone'],
                country=user_data['country'],
                timezone=user_data['timezone'],
                is_active=user_data['is_active'],
                email_verified=user_data['email_verified'],
                created_at=user_data['created_at'],
                updated_at=user_data['updated_at'],
                last_login=user_data['last_login']
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.get("/", response_model=UserListResponse)
    async def get_users(
        self,
        page: int = Query(1, description="Page number", ge=1),
        page_size: int = Query(20, description="Page size", ge=1, le=100),
        role: Optional[str] = Query(None, description="Filter by role"),
        is_active: Optional[bool] = Query(None, description="Filter by active status"),
        search: Optional[str] = Query(None, description="Search by username, email, or name"),
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> UserListResponse:
        """Get list of users with pagination and filtering."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "users:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to read users"
                )
            
            # Build query with filters
            where_conditions = []
            params = {}
            
            if role:
                where_conditions.append("role = :role")
                params["role"] = role.upper()
            
            if is_active is not None:
                where_conditions.append("is_active = :is_active")
                params["is_active"] = is_active
            
            if search:
                where_conditions.append("(username ILIKE :search OR email ILIKE :search OR first_name ILIKE :search OR last_name ILIKE :search)")
                params["search"] = f"%{search}%"
            
            where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
            
            # Get total count
            count_query = f"SELECT COUNT(*) as total FROM users {where_clause}"
            count_result = await self.database_manager.execute_query(count_query, params)
            
            if 'error' in count_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {count_result['error']}"
                )
            
            total_count = count_result['query_result']['data'][0]['total']
            total_pages = (total_count + page_size - 1) // page_size
            
            # Get users with pagination
            offset = (page - 1) * page_size
            params["limit"] = page_size
            params["offset"] = offset
            
            users_query = f"""
            SELECT * FROM users 
            {where_clause}
            ORDER BY created_at DESC
            LIMIT :limit OFFSET :offset
            """
            
            users_result = await self.database_manager.execute_query(users_query, params)
            
            if 'error' in users_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {users_result['error']}"
                )
            
            users = []
            for user_data in users_result['query_result']['data']:
                users.append(UserResponse(
                    user_id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    role=user_data['role'],
                    phone=user_data['phone'],
                    country=user_data['country'],
                    timezone=user_data['timezone'],
                    is_active=user_data['is_active'],
                    email_verified=user_data['email_verified'],
                    created_at=user_data['created_at'],
                    updated_at=user_data['updated_at'],
                    last_login=user_data['last_login']
                ))
            
            return UserListResponse(
                users=users,
                total_count=total_count,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get users: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.get("/{user_id}", response_model=UserResponse)
    async def get_user(
        self,
        user_id: str = Path(..., description="User ID"),
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> UserResponse:
        """Get user by ID."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "users:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to read users"
                )
            
            # Validate user_id format
            if not self._is_valid_uuid(user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid user ID format"
                )
            
            # Get user
            user_query = "SELECT * FROM users WHERE id = :user_id"
            user_result = await self.database_manager.execute_query(
                user_query,
                {"user_id": user_id}
            )
            
            if 'error' in user_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {user_result['error']}"
                )
            
            if not user_result['query_result']['data']:
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
                role=user_data['role'],
                phone=user_data['phone'],
                country=user_data['country'],
                timezone=user_data['timezone'],
                is_active=user_data['is_active'],
                email_verified=user_data['email_verified'],
                created_at=user_data['created_at'],
                updated_at=user_data['updated_at'],
                last_login=user_data['last_login']
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.put("/{user_id}", response_model=UserResponse)
    async def update_user(
        self,
        user_id: str = Path(..., description="User ID"),
        request: UpdateUserRequest = ...,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> UserResponse:
        """Update user information."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "users:update"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to update users"
                )
            
            # Validate user_id format
            if not self._is_valid_uuid(user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid user ID format"
                )
            
            # Check if user exists
            user_query = "SELECT * FROM users WHERE id = :user_id"
            user_result = await self.database_manager.execute_query(
                user_query,
                {"user_id": user_id}
            )
            
            if 'error' in user_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {user_result['error']}"
                )
            
            if not user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Check if email is being updated and if it already exists
            if request.email:
                email_check_query = "SELECT id FROM users WHERE email = :email AND id != :user_id"
                email_check_result = await self.database_manager.execute_query(
                    email_check_query,
                    {"email": request.email, "user_id": user_id}
                )
                
                if 'error' not in email_check_result and email_check_result['query_result']['data']:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already exists"
                    )
            
            # Build update query
            update_fields = []
            params = {"user_id": user_id, "updated_at": datetime.now()}
            
            if request.first_name is not None:
                update_fields.append("first_name = :first_name")
                params["first_name"] = request.first_name
            
            if request.last_name is not None:
                update_fields.append("last_name = :last_name")
                params["last_name"] = request.last_name
            
            if request.email is not None:
                update_fields.append("email = :email")
                params["email"] = request.email
            
            if request.phone is not None:
                update_fields.append("phone = :phone")
                params["phone"] = request.phone
            
            if request.country is not None:
                update_fields.append("country = :country")
                params["country"] = request.country
            
            if request.timezone is not None:
                update_fields.append("timezone = :timezone")
                params["timezone"] = request.timezone
            
            if request.is_active is not None:
                update_fields.append("is_active = :is_active")
                params["is_active"] = request.is_active
            
            if not update_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No fields to update"
                )
            
            update_fields.append("updated_at = :updated_at")
            
            update_query = f"""
            UPDATE users 
            SET {', '.join(update_fields)}
            WHERE id = :user_id
            """
            
            update_result = await self.database_manager.execute_query(update_query, params)
            
            if 'error' in update_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to update user: {update_result['error']}"
                )
            
            # Get updated user
            get_user_query = "SELECT * FROM users WHERE id = :user_id"
            get_user_result = await self.database_manager.execute_query(
                get_user_query,
                {"user_id": user_id}
            )
            
            if 'error' in get_user_result or not get_user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve updated user"
                )
            
            user_data = get_user_result['query_result']['data'][0]
            
            logger.info(f"User updated successfully: {user_id}")
            
            return UserResponse(
                user_id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role'],
                phone=user_data['phone'],
                country=user_data['country'],
                timezone=user_data['timezone'],
                is_active=user_data['is_active'],
                email_verified=user_data['email_verified'],
                created_at=user_data['created_at'],
                updated_at=user_data['updated_at'],
                last_login=user_data['last_login']
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to update user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.delete("/{user_id}", response_model=Dict[str, Any])
    async def delete_user(
        self,
        user_id: str = Path(..., description="User ID"),
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Delete user (soft delete by setting is_active to False)."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "users:delete"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to delete users"
                )
            
            # Validate user_id format
            if not self._is_valid_uuid(user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid user ID format"
                )
            
            # Check if user exists
            user_query = "SELECT * FROM users WHERE id = :user_id"
            user_result = await self.database_manager.execute_query(
                user_query,
                {"user_id": user_id}
            )
            
            if 'error' in user_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {user_result['error']}"
                )
            
            if not user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Soft delete user
            delete_query = """
            UPDATE users 
            SET is_active = :is_active, updated_at = :updated_at
            WHERE id = :user_id
            """
            
            delete_params = {
                "user_id": user_id,
                "is_active": False,
                "updated_at": datetime.now()
            }
            
            delete_result = await self.database_manager.execute_query(delete_query, delete_params)
            
            if 'error' in delete_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to delete user: {delete_result['error']}"
                )
            
            logger.info(f"User deleted successfully: {user_id}")
            
            return {
                "status": "success",
                "message": "User deleted successfully",
                "user_id": user_id
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to delete user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.post("/{user_id}/change-password", response_model=Dict[str, Any])
    async def change_user_password(
        self,
        user_id: str = Path(..., description="User ID"),
        request: ChangePasswordRequest = ...,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Change user password."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "users:update"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to update users"
                )
            
            # Validate user_id format
            if not self._is_valid_uuid(user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid user ID format"
                )
            
            # Validate new password
            password_validation = self._validate_password(request.new_password)
            if not password_validation['is_valid']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid new password: {', '.join(password_validation['errors'])}"
                )
            
            # Get user
            user_query = "SELECT * FROM users WHERE id = :user_id"
            user_result = await self.database_manager.execute_query(
                user_query,
                {"user_id": user_id}
            )
            
            if 'error' in user_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {user_result['error']}"
                )
            
            if not user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            user_data = user_result['query_result']['data'][0]
            
            # Verify current password
            if not self.jwt_manager.verify_password(request.current_password, user_data['password_hash']):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Current password is incorrect"
                )
            
            # Hash new password
            new_password_hash = self.jwt_manager.hash_password(request.new_password)
            
            # Update password
            update_query = """
            UPDATE users 
            SET password_hash = :password_hash, updated_at = :updated_at
            WHERE id = :user_id
            """
            
            update_params = {
                "user_id": user_id,
                "password_hash": new_password_hash,
                "updated_at": datetime.now()
            }
            
            update_result = await self.database_manager.execute_query(update_query, update_params)
            
            if 'error' in update_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to update password: {update_result['error']}"
                )
            
            logger.info(f"Password changed successfully for user: {user_id}")
            
            return {
                "status": "success",
                "message": "Password changed successfully",
                "user_id": user_id
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to change password: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.post("/{user_id}/assign-role", response_model=Dict[str, Any])
    async def assign_user_role(
        self,
        user_id: str = Path(..., description="User ID"),
        request: AssignRoleRequest = ...,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Assign role to user."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "users:update"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to update users"
                )
            
            # Validate user_id format
            if not self._is_valid_uuid(user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid user ID format"
                )
            
            # Validate role
            try:
                user_role = UserRole(request.role.upper())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid role: {request.role}. Valid roles are: {', '.join([r.value for r in UserRole])}"
                )
            
            # Check if user exists
            user_query = "SELECT * FROM users WHERE id = :user_id"
            user_result = await self.database_manager.execute_query(
                user_query,
                {"user_id": user_id}
            )
            
            if 'error' in user_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {user_result['error']}"
                )
            
            if not user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Update user role
            update_query = """
            UPDATE users 
            SET role = :role, updated_at = :updated_at
            WHERE id = :user_id
            """
            
            update_params = {
                "user_id": user_id,
                "role": user_role.value,
                "updated_at": datetime.now()
            }
            
            update_result = await self.database_manager.execute_query(update_query, update_params)
            
            if 'error' in update_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to assign role: {update_result['error']}"
                )
            
            logger.info(f"Role assigned successfully to user {user_id}: {user_role.value}")
            
            return {
                "status": "success",
                "message": "Role assigned successfully",
                "user_id": user_id,
                "role": user_role.value
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to assign role: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.get("/stats/overview", response_model=UserStatsResponse)
    async def get_user_stats(
        self,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> UserStatsResponse:
        """Get user statistics overview."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "users:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to read user statistics"
                )
            
            # Get total users
            total_query = "SELECT COUNT(*) as total FROM users"
            total_result = await self.database_manager.execute_query(total_query)
            
            if 'error' in total_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {total_result['error']}"
                )
            
            total_users = total_result['query_result']['data'][0]['total']
            
            # Get active users
            active_query = "SELECT COUNT(*) as total FROM users WHERE is_active = true"
            active_result = await self.database_manager.execute_query(active_query)
            
            if 'error' in active_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {active_result['error']}"
                )
            
            active_users = active_result['query_result']['data'][0]['total']
            inactive_users = total_users - active_users
            
            # Get users by role
            role_query = "SELECT role, COUNT(*) as count FROM users GROUP BY role"
            role_result = await self.database_manager.execute_query(role_query)
            
            if 'error' in role_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {role_result['error']}"
                )
            
            users_by_role = {}
            for row in role_result['query_result']['data']:
                users_by_role[row['role']] = row['count']
            
            # Get new users today
            today = datetime.now().date()
            today_query = "SELECT COUNT(*) as total FROM users WHERE DATE(created_at) = :today"
            today_result = await self.database_manager.execute_query(today_query, {"today": today})
            
            if 'error' in today_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {today_result['error']}"
                )
            
            new_users_today = today_result['query_result']['data'][0]['total']
            
            # Get new users this week
            week_start = today - timedelta(days=today.weekday())
            week_query = "SELECT COUNT(*) as total FROM users WHERE DATE(created_at) >= :week_start"
            week_result = await self.database_manager.execute_query(week_query, {"week_start": week_start})
            
            if 'error' in week_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {week_result['error']}"
                )
            
            new_users_this_week = week_result['query_result']['data'][0]['total']
            
            # Get new users this month
            month_start = today.replace(day=1)
            month_query = "SELECT COUNT(*) as total FROM users WHERE DATE(created_at) >= :month_start"
            month_result = await self.database_manager.execute_query(month_query, {"month_start": month_start})
            
            if 'error' in month_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {month_result['error']}"
                )
            
            new_users_this_month = month_result['query_result']['data'][0]['total']
            
            return UserStatsResponse(
                total_users=total_users,
                active_users=active_users,
                inactive_users=inactive_users,
                users_by_role=users_by_role,
                new_users_today=new_users_today,
                new_users_this_week=new_users_this_week,
                new_users_this_month=new_users_this_month
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get user stats: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


# Create router instance
def create_user_management_api_router(database_manager, jwt_manager: JWTManager) -> APIRouter:
    """Create and configure the user management API router."""
    api = UserManagementAPI(database_manager, jwt_manager)
    
    # Add the router methods to the router
    router.add_api_route("/", api.create_user, methods=["POST"])
    router.add_api_route("/", api.get_users, methods=["GET"])
    router.add_api_route("/{user_id}", api.get_user, methods=["GET"])
    router.add_api_route("/{user_id}", api.update_user, methods=["PUT"])
    router.add_api_route("/{user_id}", api.delete_user, methods=["DELETE"])
    router.add_api_route("/{user_id}/change-password", api.change_user_password, methods=["POST"])
    router.add_api_route("/{user_id}/assign-role", api.assign_user_role, methods=["POST"])
    router.add_api_route("/stats/overview", api.get_user_stats, methods=["GET"])
    
    return router
