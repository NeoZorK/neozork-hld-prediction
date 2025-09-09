"""
JWT token handler for Pocket Hedge Fund.

This module provides JWT token creation, verification, and management
for the authentication system.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from jose import jwt
import os
from jose.exceptions import JWTError, ExpiredSignatureError

logger = logging.getLogger(__name__)


class JWTHandler:
    """
    JWT token handler for Pocket Hedge Fund.
    
    Provides token creation, verification, and management functionality.
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize JWT handler.
        
        Args:
            secret_key: JWT secret key. If None, uses environment variable.
        """
        self.secret_key = secret_key or os.getenv('JWT_SECRET_KEY', 'default-secret-key-change-in-production')
        self.algorithm = 'HS256'
        self.default_expiry = timedelta(hours=24)
        self.refresh_expiry = timedelta(days=7)
    
    def create_token(self, payload: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT token.
        
        Args:
            payload: Token payload data
            expires_delta: Token expiration time
            
        Returns:
            JWT token string
        """
        try:
            # Set expiration time
            if expires_delta:
                expire = datetime.now(timezone.utc) + expires_delta
            else:
                expire = datetime.now(timezone.utc) + self.default_expiry
            
            # Add standard claims
            payload.update({
                'exp': expire,
                'iat': datetime.now(timezone.utc),
                'iss': 'pocket-hedge-fund',
                'aud': 'pocket-hedge-fund-users'
            })
            
            # Create token
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            
            logger.debug(f"JWT token created for user: {payload.get('user_id', 'unknown')}")
            return token
            
        except Exception as e:
            logger.error(f"Error creating JWT token: {e}")
            raise
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Token payload if valid, None otherwise
        """
        try:
            # Decode token
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm],
                audience='pocket-hedge-fund-users',
                issuer='pocket-hedge-fund'
            )
            
            # Check if token is expired
            if 'exp' in payload:
                exp_timestamp = payload['exp']
                if datetime.now(timezone.utc).timestamp() > exp_timestamp:
                    logger.warning("JWT token has expired")
                    return None
            
            logger.debug(f"JWT token verified for user: {payload.get('user_id', 'unknown')}")
            return payload
            
        except ExpiredSignatureError:
            logger.warning("JWT token has expired")
            return None
        except JWTError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error verifying JWT token: {e}")
            return None
    
    def create_refresh_token(self, user_id: str) -> str:
        """
        Create refresh token.
        
        Args:
            user_id: User ID
            
        Returns:
            Refresh token string
        """
        try:
            payload = {
                'user_id': user_id,
                'type': 'refresh',
                'exp': datetime.now(timezone.utc) + self.refresh_expiry
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            
            logger.debug(f"Refresh token created for user: {user_id}")
            return token
            
        except Exception as e:
            logger.error(f"Error creating refresh token: {e}")
            raise
    
    def verify_refresh_token(self, token: str) -> Optional[str]:
        """
        Verify refresh token and return user ID.
        
        Args:
            token: Refresh token to verify
            
        Returns:
            User ID if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check token type
            if payload.get('type') != 'refresh':
                logger.warning("Invalid refresh token type")
                return None
            
            user_id = payload.get('user_id')
            if not user_id:
                logger.warning("No user_id in refresh token")
                return None
            
            logger.debug(f"Refresh token verified for user: {user_id}")
            return user_id
            
        except ExpiredSignatureError:
            logger.warning("Refresh token has expired")
            return None
        except JWTError as e:
            logger.warning(f"Invalid refresh token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error verifying refresh token: {e}")
            return None
    
    def decode_token_without_verification(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Decode token without verification (for debugging).
        
        Args:
            token: JWT token to decode
            
        Returns:
            Token payload or None
        """
        try:
            payload = jwt.decode(token, key="", options={"verify_signature": False, "verify_aud": False, "verify_iss": False})
            return payload
        except Exception as e:
            logger.error(f"Error decoding token: {e}")
            return None
    
    def get_token_expiry(self, token: str) -> Optional[datetime]:
        """
        Get token expiration time.
        
        Args:
            token: JWT token
            
        Returns:
            Expiration datetime or None
        """
        try:
            payload = self.decode_token_without_verification(token)
            if payload and 'exp' in payload:
                return datetime.fromtimestamp(payload['exp'])
            return None
        except Exception as e:
            logger.error(f"Error getting token expiry: {e}")
            return None
    
    def is_token_expired(self, token: str) -> bool:
        """
        Check if token is expired.
        
        Args:
            token: JWT token
            
        Returns:
            True if expired, False otherwise
        """
        try:
            expiry = self.get_token_expiry(token)
            if expiry:
                # Ensure both datetimes are timezone-aware
                if expiry.tzinfo is None:
                    expiry = expiry.replace(tzinfo=timezone.utc)
                return datetime.now(timezone.utc) > expiry
            return True
        except Exception as e:
            logger.error(f"Error checking token expiry: {e}")
            return True
    
    def create_access_token(self, user_id: str, email: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create access token for user.
        
        Args:
            user_id: User ID
            email: User email
            role: User role
            expires_delta: Token expiration time
            
        Returns:
            Access token string
        """
        try:
            payload = {
                'user_id': user_id,
                'email': email,
                'role': role,
                'type': 'access'
            }
            
            return self.create_token(payload, expires_delta)
            
        except Exception as e:
            logger.error(f"Error creating access token: {e}")
            raise
    
    def create_tokens_pair(self, user_id: str, email: str, role: str) -> Dict[str, str]:
        """
        Create access and refresh token pair.
        
        Args:
            user_id: User ID
            email: User email
            role: User role
            
        Returns:
            Dict containing access and refresh tokens
        """
        try:
            access_token = self.create_access_token(user_id, email, role)
            refresh_token = self.create_refresh_token(user_id)
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'bearer',
                'expires_in': int(self.default_expiry.total_seconds())
            }
            
        except Exception as e:
            logger.error(f"Error creating token pair: {e}")
            raise
    
    def extract_user_info(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Extract user information from token.
        
        Args:
            token: JWT token
            
        Returns:
            User information dict or None
        """
        try:
            payload = self.verify_token(token)
            if not payload:
                return None
            
            return {
                'user_id': payload.get('user_id'),
                'email': payload.get('email'),
                'role': payload.get('role'),
                'exp': payload.get('exp'),
                'iat': payload.get('iat')
            }
            
        except Exception as e:
            logger.error(f"Error extracting user info: {e}")
            return None
    
    def validate_token_structure(self, token: str) -> bool:
        """
        Validate token structure without verification.
        
        Args:
            token: JWT token
            
        Returns:
            True if structure is valid, False otherwise
        """
        try:
            payload = self.decode_token_without_verification(token)
            if not payload:
                return False
            
            # Check required fields
            required_fields = ['user_id', 'exp', 'iat']
            for field in required_fields:
                if field not in payload:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating token structure: {e}")
            return False
    
    def get_token_info(self, token: str) -> Dict[str, Any]:
        """
        Get comprehensive token information.
        
        Args:
            token: JWT token
            
        Returns:
            Dict containing token information
        """
        try:
            payload = self.decode_token_without_verification(token)
            if not payload:
                return {'valid': False, 'error': 'Invalid token'}
            
            expiry = self.get_token_expiry(token)
            is_expired = self.is_token_expired(token)
            
            return {
                'valid': not is_expired,
                'expired': is_expired,
                'user_id': payload.get('user_id'),
                'email': payload.get('email'),
                'role': payload.get('role'),
                'type': payload.get('type'),
                'issued_at': datetime.fromtimestamp(payload.get('iat', 0)) if payload.get('iat') else None,
                'expires_at': expiry,
                'time_until_expiry': (expiry - datetime.now(timezone.utc)).total_seconds() if expiry and not is_expired else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting token info: {e}")
            return {'valid': False, 'error': str(e)}
