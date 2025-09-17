"""JWT Manager - JSON Web Token authentication and authorization system"""

import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import jwt
import bcrypt
import secrets
import uuid
from passlib.context import CryptContext

logger = logging.getLogger(__name__)


class TokenType(Enum):
    """Token type enumeration."""
    ACCESS = "access"
    REFRESH = "refresh"
    RESET_PASSWORD = "reset_password"
    EMAIL_VERIFICATION = "email_verification"


class UserRole(Enum):
    """User role enumeration."""
    ADMIN = "admin"
    FUND_MANAGER = "fund_manager"
    INVESTOR = "investor"
    ANALYST = "analyst"
    VIEWER = "viewer"


@dataclass
class TokenPayload:
    """Token payload data class."""
    user_id: str
    username: str
    email: str
    role: UserRole
    permissions: List[str]
    token_type: TokenType
    issued_at: datetime
    expires_at: datetime
    jti: str  # JWT ID for token tracking


@dataclass
class AuthResult:
    """Authentication result data class."""
    success: bool
    user_id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
    permissions: Optional[List[str]] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    error_message: Optional[str] = None


class JWTManager:
    """JWT authentication and authorization manager."""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Token expiration times
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7
        self.reset_token_expire_hours = 1
        self.verification_token_expire_hours = 24
        
        # Token blacklist for logout
        self.token_blacklist: set = set()
        
        logger.info("JWT Manager initialized")
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        try:
            return self.password_context.hash(password)
        except Exception as e:
            logger.error(f"Failed to hash password: {e}")
            raise
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            return self.password_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Failed to verify password: {e}")
            return False
    
    def create_token_payload(self, user_id: str, username: str, email: str, 
                           role: UserRole, permissions: List[str], 
                           token_type: TokenType, expires_in_minutes: int) -> TokenPayload:
        """Create token payload."""
        now = datetime.now(datetime.UTC)
        expires_at = now + timedelta(minutes=expires_in_minutes)
        
        return TokenPayload(
            user_id=user_id,
            username=username,
            email=email,
            role=role,
            permissions=permissions,
            token_type=token_type,
            issued_at=now,
            expires_at=expires_at,
            jti=str(uuid.uuid4())
        )
    
    def create_access_token(self, user_id: str, username: str, email: str, 
                          role: UserRole, permissions: List[str]) -> str:
        """Create access token."""
        try:
            payload = self.create_token_payload(
                user_id=user_id,
                username=username,
                email=email,
                role=role,
                permissions=permissions,
                token_type=TokenType.ACCESS,
                expires_in_minutes=self.access_token_expire_minutes
            )
            
            # Convert to dict for JWT encoding
            token_data = {
                "user_id": payload.user_id,
                "username": payload.username,
                "email": payload.email,
                "role": payload.role.value,
                "permissions": payload.permissions,
                "token_type": payload.token_type.value,
                "iat": int(payload.issued_at.timestamp()),
                "exp": int(payload.expires_at.timestamp()),
                "jti": payload.jti
            }
            
            token = jwt.encode(token_data, self.secret_key, algorithm=self.algorithm)
            
            logger.info(f"Created access token for user {username}")
            return token
            
        except Exception as e:
            logger.error(f"Failed to create access token: {e}")
            raise
    
    def create_refresh_token(self, user_id: str, username: str, email: str, 
                           role: UserRole, permissions: List[str]) -> str:
        """Create refresh token."""
        try:
            payload = self.create_token_payload(
                user_id=user_id,
                username=username,
                email=email,
                role=role,
                permissions=permissions,
                token_type=TokenType.REFRESH,
                expires_in_minutes=self.refresh_token_expire_days * 24 * 60
            )
            
            # Convert to dict for JWT encoding
            token_data = {
                "user_id": payload.user_id,
                "username": payload.username,
                "email": payload.email,
                "role": payload.role.value,
                "permissions": payload.permissions,
                "token_type": payload.token_type.value,
                "iat": int(payload.issued_at.timestamp()),
                "exp": int(payload.expires_at.timestamp()),
                "jti": payload.jti
            }
            
            token = jwt.encode(token_data, self.secret_key, algorithm=self.algorithm)
            
            logger.info(f"Created refresh token for user {username}")
            return token
            
        except Exception as e:
            logger.error(f"Failed to create refresh token: {e}")
            raise
    
    def verify_token(self, token: str, token_type: TokenType = TokenType.ACCESS) -> Optional[TokenPayload]:
        """Verify and decode a JWT token."""
        try:
            # Check if token is blacklisted
            if token in self.token_blacklist:
                logger.warning("Token is blacklisted")
                return None
            
            # Decode token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Validate token type
            if payload.get("token_type") != token_type.value:
                logger.warning(f"Invalid token type: expected {token_type.value}, got {payload.get('token_type')}")
                return None
            
            # Check expiration
            exp_timestamp = payload.get("exp")
            if exp_timestamp and datetime.now(datetime.UTC).timestamp() > exp_timestamp:
                logger.warning("Token has expired")
                return None
            
            # Create TokenPayload object
            token_payload = TokenPayload(
                user_id=payload["user_id"],
                username=payload["username"],
                email=payload["email"],
                role=UserRole(payload["role"]),
                permissions=payload["permissions"],
                token_type=TokenType(payload["token_type"]),
                issued_at=datetime.fromtimestamp(payload["iat"]),
                expires_at=datetime.fromtimestamp(payload["exp"]),
                jti=payload["jti"]
            )
            
            logger.debug(f"Token verified for user {token_payload.username}")
            return token_payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to verify token: {e}")
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Create new access token from refresh token."""
        try:
            # Verify refresh token
            payload = self.verify_token(refresh_token, TokenType.REFRESH)
            if not payload:
                return None
            
            # Create new access token
            new_access_token = self.create_access_token(
                user_id=payload.user_id,
                username=payload.username,
                email=payload.email,
                role=payload.role,
                permissions=payload.permissions
            )
            
            logger.info(f"Refreshed access token for user {payload.username}")
            return new_access_token
            
        except Exception as e:
            logger.error(f"Failed to refresh access token: {e}")
            return None
    
    def blacklist_token(self, token: str) -> bool:
        """Add token to blacklist."""
        try:
            self.token_blacklist.add(token)
            logger.info("Token added to blacklist")
            return True
        except Exception as e:
            logger.error(f"Failed to blacklist token: {e}")
            return False
    
    def create_password_reset_token(self, user_id: str, email: str) -> str:
        """Create password reset token."""
        try:
            payload = self.create_token_payload(
                user_id=user_id,
                username="",  # Not needed for reset token
                email=email,
                role=UserRole.VIEWER,  # Default role
                permissions=[],  # No permissions needed
                token_type=TokenType.RESET_PASSWORD,
                expires_in_minutes=self.reset_token_expire_hours * 60
            )
            
            token_data = {
                "user_id": payload.user_id,
                "email": payload.email,
                "token_type": payload.token_type.value,
                "iat": int(payload.issued_at.timestamp()),
                "exp": int(payload.expires_at.timestamp()),
                "jti": payload.jti
            }
            
            token = jwt.encode(token_data, self.secret_key, algorithm=self.algorithm)
            
            logger.info(f"Created password reset token for user {user_id}")
            return token
            
        except Exception as e:
            logger.error(f"Failed to create password reset token: {e}")
            raise
    
    def create_email_verification_token(self, user_id: str, email: str) -> str:
        """Create email verification token."""
        try:
            payload = self.create_token_payload(
                user_id=user_id,
                username="",  # Not needed for verification token
                email=email,
                role=UserRole.VIEWER,  # Default role
                permissions=[],  # No permissions needed
                token_type=TokenType.EMAIL_VERIFICATION,
                expires_in_minutes=self.verification_token_expire_hours * 60
            )
            
            token_data = {
                "user_id": payload.user_id,
                "email": payload.email,
                "token_type": payload.token_type.value,
                "iat": int(payload.issued_at.timestamp()),
                "exp": int(payload.expires_at.timestamp()),
                "jti": payload.jti
            }
            
            token = jwt.encode(token_data, self.secret_key, algorithm=self.algorithm)
            
            logger.info(f"Created email verification token for user {user_id}")
            return token
            
        except Exception as e:
            logger.error(f"Failed to create email verification token: {e}")
            raise
    
    def get_user_permissions(self, role: UserRole) -> List[str]:
        """Get permissions for a user role."""
        permissions_map = {
            UserRole.ADMIN: [
                "fund:create", "fund:read", "fund:update", "fund:delete",
                "investor:create", "investor:read", "investor:update", "investor:delete",
                "portfolio:read", "portfolio:update", "portfolio:delete",
                "strategy:create", "strategy:read", "strategy:update", "strategy:delete",
                "user:create", "user:read", "user:update", "user:delete",
                "system:admin"
            ],
            UserRole.FUND_MANAGER: [
                "fund:create", "fund:read", "fund:update",
                "investor:read", "investor:update",
                "portfolio:read", "portfolio:update",
                "strategy:create", "strategy:read", "strategy:update",
                "user:read"
            ],
            UserRole.INVESTOR: [
                "fund:read",
                "investor:read",
                "portfolio:read",
                "strategy:read"
            ],
            UserRole.ANALYST: [
                "fund:read",
                "portfolio:read",
                "strategy:read",
                "analytics:read"
            ],
            UserRole.VIEWER: [
                "fund:read",
                "portfolio:read"
            ]
        }
        
        return permissions_map.get(role, [])
    
    def has_permission(self, user_permissions: List[str], required_permission: str) -> bool:
        """Check if user has required permission."""
        return required_permission in user_permissions or "system:admin" in user_permissions
    
    def get_token_info(self, token: str) -> Optional[Dict[str, Any]]:
        """Get token information without verification."""
        try:
            # Decode without verification to get payload
            payload = jwt.decode(token, options={"verify_signature": False})
            
            return {
                "user_id": payload.get("user_id"),
                "username": payload.get("username"),
                "email": payload.get("email"),
                "role": payload.get("role"),
                "token_type": payload.get("token_type"),
                "issued_at": datetime.fromtimestamp(payload.get("iat", 0)).isoformat(),
                "expires_at": datetime.fromtimestamp(payload.get("exp", 0)).isoformat(),
                "jti": payload.get("jti")
            }
            
        except Exception as e:
            logger.error(f"Failed to get token info: {e}")
            return None
    
    def cleanup_expired_tokens(self) -> int:
        """Clean up expired tokens from blacklist."""
        try:
            initial_count = len(self.token_blacklist)
            
            # This is a simplified cleanup - in production, you'd want to
            # store tokens with expiration times and clean them up properly
            # For now, we'll just clear the blacklist periodically
            
            if initial_count > 1000:  # Arbitrary threshold
                self.token_blacklist.clear()
                logger.info(f"Cleaned up token blacklist: {initial_count} tokens removed")
                return initial_count
            
            return 0
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired tokens: {e}")
            return 0
    
    def get_blacklist_size(self) -> int:
        """Get current blacklist size."""
        return len(self.token_blacklist)
    
    def is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted."""
        return token in self.token_blacklist
