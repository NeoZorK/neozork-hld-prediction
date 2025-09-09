"""
Unit tests for Pocket Hedge Fund authentication system.

This module tests the authentication components including JWT handler,
password manager, permissions, and middleware.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock, AsyncMock, patch

try:
    from src.pocket_hedge_fund.auth.jwt_handler import JWTHandler
    from src.pocket_hedge_fund.auth.password_manager import PasswordManager
    from src.pocket_hedge_fund.auth.permissions import PermissionManager, Permission, Role
    from src.pocket_hedge_fund.auth.auth_manager import AuthManager
    from src.pocket_hedge_fund.database import DatabaseManager
except ImportError as e:
    pytest.skip(f"Skipping tests due to import error: {e}", allow_module_level=True)


class TestJWTHandler:
    """Test JWT handler functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.jwt_handler = JWTHandler(secret_key="test-secret-key")
    
    def test_create_token(self):
        """Test token creation."""
        payload = {
            'user_id': 'test-user-123',
            'email': 'test@example.com',
            'role': 'investor'
        }
        
        token = self.jwt_handler.create_token(payload)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_token(self):
        """Test token verification."""
        payload = {
            'user_id': 'test-user-123',
            'email': 'test@example.com',
            'role': 'investor'
        }
        
        token = self.jwt_handler.create_token(payload)
        verified_payload = self.jwt_handler.verify_token(token)
        
        assert verified_payload is not None
        assert verified_payload['user_id'] == 'test-user-123'
        assert verified_payload['email'] == 'test@example.com'
        assert verified_payload['role'] == 'investor'
    
    def test_verify_invalid_token(self):
        """Test verification of invalid token."""
        invalid_token = "invalid.token.here"
        verified_payload = self.jwt_handler.verify_token(invalid_token)
        
        assert verified_payload is None
    
    def test_create_refresh_token(self):
        """Test refresh token creation."""
        user_id = 'test-user-123'
        refresh_token = self.jwt_handler.create_refresh_token(user_id)
        
        assert refresh_token is not None
        assert isinstance(refresh_token, str)
    
    def test_verify_refresh_token(self):
        """Test refresh token verification."""
        user_id = 'test-user-123'
        refresh_token = self.jwt_handler.create_refresh_token(user_id)
        verified_user_id = self.jwt_handler.verify_refresh_token(refresh_token)
        
        assert verified_user_id == user_id
    
    def test_create_tokens_pair(self):
        """Test creating access and refresh token pair."""
        user_id = 'test-user-123'
        email = 'test@example.com'
        role = 'investor'
        
        tokens = self.jwt_handler.create_tokens_pair(user_id, email, role)
        
        assert 'access_token' in tokens
        assert 'refresh_token' in tokens
        assert 'token_type' in tokens
        assert 'expires_in' in tokens
        assert tokens['token_type'] == 'bearer'
    
    def test_token_expiry(self):
        """Test token expiry functionality."""
        payload = {'user_id': 'test-user-123'}
        token = self.jwt_handler.create_token(payload, expires_delta=timedelta(seconds=1))
        
        # Token should be valid initially
        assert not self.jwt_handler.is_token_expired(token)
        
        # Wait for token to expire
        import time
        time.sleep(2)
        
        # Token should be expired now
        assert self.jwt_handler.is_token_expired(token)
    
    def test_extract_user_info(self):
        """Test extracting user info from token."""
        payload = {
            'user_id': 'test-user-123',
            'email': 'test@example.com',
            'role': 'investor'
        }
        
        token = self.jwt_handler.create_token(payload)
        user_info = self.jwt_handler.extract_user_info(token)
        
        assert user_info is not None
        assert user_info['user_id'] == 'test-user-123'
        assert user_info['email'] == 'test@example.com'
        assert user_info['role'] == 'investor'


class TestPasswordManager:
    """Test password manager functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.password_manager = PasswordManager()
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "test_password_123"
        hashed = self.password_manager.hash_password(password)
        
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0
    
    def test_verify_password(self):
        """Test password verification."""
        password = "test_password_123"
        hashed = self.password_manager.hash_password(password)
        
        # Correct password should verify
        assert self.password_manager.verify_password(password, hashed)
        
        # Wrong password should not verify
        assert not self.password_manager.verify_password("wrong_password", hashed)
    
    def test_validate_password(self):
        """Test password validation."""
        # Valid password
        valid_password = "TestPassword123!"
        validation = self.password_manager.validate_password(valid_password)
        
        assert validation['valid'] is True
        assert len(validation['errors']) == 0
        assert validation['strength_score'] > 0
        
        # Invalid password (too short)
        invalid_password = "123"
        validation = self.password_manager.validate_password(invalid_password)
        
        assert validation['valid'] is False
        assert len(validation['errors']) > 0
    
    def test_generate_secure_password(self):
        """Test secure password generation."""
        password = self.password_manager.generate_secure_password(length=16)
        
        assert len(password) == 16
        assert self.password_manager.validate_password(password)['valid'] is True
    
    def test_password_requirements(self):
        """Test password requirements."""
        requirements = self.password_manager.get_password_requirements()
        
        assert 'min_length' in requirements
        assert 'max_length' in requirements
        assert 'require_uppercase' in requirements
        assert 'require_lowercase' in requirements
        assert 'require_digits' in requirements
        assert 'require_special_chars' in requirements
    
    def test_check_password_breach(self):
        """Test password breach checking."""
        # Common password should be detected
        assert self.password_manager.check_password_breach("password")
        assert self.password_manager.check_password_breach("123456")
        
        # Secure password should not be detected
        assert not self.password_manager.check_password_breach("SecurePass123!")


class TestPermissionManager:
    """Test permission manager functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.permission_manager = PermissionManager()
    
    def test_has_permission(self):
        """Test permission checking."""
        # Admin should have all permissions
        assert self.permission_manager.has_permission("admin", "fund", "create")
        assert self.permission_manager.has_permission("admin", "user", "delete")
        
        # Investor should have limited permissions
        assert self.permission_manager.has_permission("investor", "fund", "read")
        assert not self.permission_manager.has_permission("investor", "fund", "create")
        
        # Fund manager should have fund management permissions
        assert self.permission_manager.has_permission("fund_manager", "fund", "create")
        assert self.permission_manager.has_permission("fund_manager", "portfolio", "manage")
    
    def test_has_permission_direct(self):
        """Test direct permission checking."""
        assert self.permission_manager.has_permission_direct("admin", "fund:create")
        assert not self.permission_manager.has_permission_direct("investor", "fund:create")
    
    def test_get_role_permissions(self):
        """Test getting role permissions."""
        admin_permissions = self.permission_manager.get_role_permissions("admin")
        investor_permissions = self.permission_manager.get_role_permissions("investor")
        
        assert len(admin_permissions) > len(investor_permissions)
        assert "fund:create" in admin_permissions
        assert "fund:create" not in investor_permissions
    
    def test_validate_role(self):
        """Test role validation."""
        assert self.permission_manager.validate_role("admin")
        assert self.permission_manager.validate_role("investor")
        assert not self.permission_manager.validate_role("invalid_role")
    
    def test_validate_permission(self):
        """Test permission validation."""
        assert self.permission_manager.validate_permission("fund:create")
        assert self.permission_manager.validate_permission("user:read")
        assert not self.permission_manager.validate_permission("invalid:permission")
    
    def test_get_permission_info(self):
        """Test getting permission information."""
        info = self.permission_manager.get_permission_info("fund:create")
        
        assert info is not None
        assert info['permission'] == "fund:create"
        assert info['resource'] == "fund"
        assert info['action'] == "create"
    
    def test_get_role_info(self):
        """Test getting role information."""
        info = self.permission_manager.get_role_info("admin")
        
        assert info is not None
        assert info['role'] == "admin"
        assert 'permissions' in info
        assert 'permission_count' in info
    
    def test_can_access_resource(self):
        """Test resource access checking."""
        assert self.permission_manager.can_access_resource("admin", "fund")
        assert self.permission_manager.can_access_resource("investor", "fund")
        assert not self.permission_manager.can_access_resource("viewer", "system")
    
    def test_get_resource_actions(self):
        """Test getting resource actions."""
        admin_actions = self.permission_manager.get_resource_actions("admin", "fund")
        investor_actions = self.permission_manager.get_resource_actions("investor", "fund")
        
        assert "create" in admin_actions
        assert "read" in admin_actions
        assert "create" not in investor_actions
        assert "read" in investor_actions


class TestAuthManager:
    """Test authentication manager functionality."""
    
    @pytest.fixture
    async def mock_db_manager(self):
        """Create mock database manager."""
        mock_db = AsyncMock(spec=DatabaseManager)
        mock_db.get_async_session.return_value.__aenter__.return_value = AsyncMock()
        return mock_db
    
    @pytest.fixture
    async def auth_manager(self, mock_db_manager):
        """Create auth manager with mock database."""
        auth_manager = AuthManager(mock_db_manager)
        await auth_manager.initialize()
        return auth_manager
    
    @pytest.mark.asyncio
    async def test_register_user(self, auth_manager):
        """Test user registration."""
        user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'TestPassword123!',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'investor'
        }
        
        # Mock database operations
        with patch.object(auth_manager.db_manager, 'get_async_session') as mock_session:
            mock_session.return_value.__aenter__.return_value.execute.return_value.fetchone.return_value = None
            mock_session.return_value.__aenter__.return_value.commit = AsyncMock()
            
            result = await auth_manager.register_user(user_data)
            
            assert result['status'] == 'success'
            assert 'user_id' in result
            assert result['email'] == 'test@example.com'
    
    @pytest.mark.asyncio
    async def test_authenticate_user(self, auth_manager):
        """Test user authentication."""
        email = 'test@example.com'
        password = 'TestPassword123!'
        
        # Mock database operations
        with patch.object(auth_manager.db_manager, 'get_async_session') as mock_session:
            mock_user = Mock()
            mock_user.id = 'test-user-123'
            mock_user.email = email
            mock_user.username = 'testuser'
            mock_user.role = 'investor'
            mock_user.password_hash = auth_manager.password_manager.hash_password(password)
            
            mock_session.return_value.__aenter__.return_value.execute.return_value.fetchone.return_value = mock_user
            
            result = await auth_manager.authenticate_user(email, password)
            
            assert result['status'] == 'success'
            assert 'token' in result
            assert 'user' in result
            assert result['user']['email'] == email
    
    @pytest.mark.asyncio
    async def test_verify_token(self, auth_manager):
        """Test token verification."""
        # Create a valid token
        user_data = {
            'user_id': 'test-user-123',
            'email': 'test@example.com',
            'role': 'investor'
        }
        token = auth_manager.jwt_handler.create_token(user_data)
        
        # Mock database operations
        with patch.object(auth_manager.db_manager, 'get_async_session') as mock_session:
            mock_user = Mock()
            mock_user.id = 'test-user-123'
            mock_user.email = 'test@example.com'
            mock_user.username = 'testuser'
            mock_user.role = 'investor'
            
            mock_session.return_value.__aenter__.return_value.execute.return_value.fetchone.return_value = mock_user
            
            result = await auth_manager.verify_token(token)
            
            assert result['status'] == 'success'
            assert 'user' in result
            assert result['user']['id'] == 'test-user-123'
    
    @pytest.mark.asyncio
    async def test_check_permission(self, auth_manager):
        """Test permission checking."""
        user_id = 'test-user-123'
        resource = 'fund'
        action = 'read'
        
        # Mock database operations
        with patch.object(auth_manager.db_manager, 'get_async_session') as mock_session:
            mock_user = Mock()
            mock_user.role = 'investor'
            
            mock_session.return_value.__aenter__.return_value.execute.return_value.fetchone.return_value = mock_user
            
            result = await auth_manager.check_permission(user_id, resource, action)
            
            assert result is True  # Investor can read funds
    
    @pytest.mark.asyncio
    async def test_get_user_permissions(self, auth_manager):
        """Test getting user permissions."""
        user_id = 'test-user-123'
        
        # Mock database operations
        with patch.object(auth_manager.db_manager, 'get_async_session') as mock_session:
            mock_user = Mock()
            mock_user.role = 'investor'
            
            mock_session.return_value.__aenter__.return_value.execute.return_value.fetchone.return_value = mock_user
            
            permissions = await auth_manager.get_user_permissions(user_id)
            
            assert isinstance(permissions, list)
            assert 'fund:read' in permissions
            assert 'fund:create' not in permissions


class TestAuthIntegration:
    """Integration tests for authentication system."""
    
    @pytest.mark.asyncio
    async def test_full_auth_flow(self):
        """Test complete authentication flow."""
        # Setup
        mock_db_manager = AsyncMock(spec=DatabaseManager)
        auth_manager = AuthManager(mock_db_manager)
        await auth_manager.initialize()
        
        # Mock database operations
        with patch.object(auth_manager.db_manager, 'get_async_session') as mock_session:
            mock_session.return_value.__aenter__.return_value.execute.return_value.fetchone.return_value = None
            mock_session.return_value.__aenter__.return_value.commit = AsyncMock()
            
            # 1. Register user
            user_data = {
                'email': 'test@example.com',
                'username': 'testuser',
                'password': 'TestPassword123!',
                'first_name': 'Test',
                'last_name': 'User',
                'role': 'investor'
            }
            
            register_result = await auth_manager.register_user(user_data)
            assert register_result['status'] == 'success'
            
            # 2. Authenticate user
            mock_user = Mock()
            mock_user.id = register_result['user_id']
            mock_user.email = user_data['email']
            mock_user.username = user_data['username']
            mock_user.role = user_data['role']
            mock_user.password_hash = auth_manager.password_manager.hash_password(user_data['password'])
            
            mock_session.return_value.__aenter__.return_value.execute.return_value.fetchone.return_value = mock_user
            
            auth_result = await auth_manager.authenticate_user(user_data['email'], user_data['password'])
            assert auth_result['status'] == 'success'
            
            # 3. Verify token
            token = auth_result['token']
            verify_result = await auth_manager.verify_token(token)
            assert verify_result['status'] == 'success'
            
            # 4. Check permissions
            permissions = await auth_manager.get_user_permissions(register_result['user_id'])
            assert 'fund:read' in permissions
            assert 'fund:create' not in permissions


if __name__ == "__main__":
    pytest.main([__file__])
