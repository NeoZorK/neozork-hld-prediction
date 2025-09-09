"""
Unit tests for Pocket Hedge Fund API endpoints.

This module tests the API endpoints including authentication,
fund management, portfolio operations, and performance tracking.
"""

import pytest
import asyncio
from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI

try:
    from src.pocket_hedge_fund.main import app
    from src.pocket_hedge_fund.database import DatabaseManager
    from src.pocket_hedge_fund.auth import AuthManager
except ImportError as e:
    pytest.skip(f"Skipping tests due to import error: {e}", allow_module_level=True)


class TestAuthAPI:
    """Test authentication API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_auth_manager(self):
        """Create mock auth manager."""
        mock_auth = AsyncMock(spec=AuthManager)
        return mock_auth
    
    def test_register_user_success(self, client, mock_auth_manager):
        """Test successful user registration."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager):
            mock_auth_manager.register_user.return_value = {
                'status': 'success',
                'user_id': 'test-user-123',
                'email': 'test@example.com'
            }
            
            user_data = {
                'email': 'test@example.com',
                'username': 'testuser',
                'password': 'TestPassword123!',
                'first_name': 'Test',
                'last_name': 'User',
                'role': 'investor'
            }
            
            response = client.post("/api/v1/auth/register", json=user_data)
            
            assert response.status_code == 201
            assert response.json()['status'] == 'success'
            assert response.json()['user_id'] == 'test-user-123'
    
    def test_register_user_validation_error(self, client):
        """Test user registration with validation error."""
        user_data = {
            'email': 'invalid-email',
            'username': 'ab',  # Too short
            'password': '123',  # Too short
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_login_success(self, client, mock_auth_manager):
        """Test successful user login."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager):
            mock_auth_manager.authenticate_user.return_value = {
                'status': 'success',
                'token': 'test-jwt-token',
                'refresh_token': 'test-refresh-token',
                'user': {
                    'id': 'test-user-123',
                    'email': 'test@example.com',
                    'username': 'testuser',
                    'role': 'investor'
                }
            }
            
            login_data = {
                'email': 'test@example.com',
                'password': 'TestPassword123!'
            }
            
            response = client.post("/api/v1/auth/login", json=login_data)
            
            assert response.status_code == 200
            assert response.json()['access_token'] == 'test-jwt-token'
            assert response.json()['token_type'] == 'bearer'
            assert response.json()['user']['email'] == 'test@example.com'
    
    def test_login_invalid_credentials(self, client, mock_auth_manager):
        """Test login with invalid credentials."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager):
            mock_auth_manager.authenticate_user.return_value = {
                'status': 'error',
                'message': 'Invalid credentials'
            }
            
            login_data = {
                'email': 'test@example.com',
                'password': 'wrong_password'
            }
            
            response = client.post("/api/v1/auth/login", json=login_data)
            
            assert response.status_code == 401
            assert response.json()['detail'] == 'Invalid credentials'
    
    def test_refresh_token_success(self, client, mock_auth_manager):
        """Test successful token refresh."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager):
            mock_auth_manager.refresh_token.return_value = {
                'status': 'success',
                'token': 'new-jwt-token'
            }
            
            refresh_data = {
                'refresh_token': 'test-refresh-token'
            }
            
            response = client.post("/api/v1/auth/refresh", json=refresh_data)
            
            assert response.status_code == 200
            assert response.json()['access_token'] == 'new-jwt-token'
            assert response.json()['token_type'] == 'bearer'
    
    def test_get_current_user_info(self, client, mock_auth_manager):
        """Test getting current user information."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager):
            mock_auth_manager.verify_token.return_value = {
                'status': 'success',
                'user': {
                    'id': 'test-user-123',
                    'email': 'test@example.com',
                    'username': 'testuser',
                    'role': 'investor'
                }
            }
            
            headers = {"Authorization": "Bearer test-jwt-token"}
            response = client.get("/api/v1/auth/me", headers=headers)
            
            assert response.status_code == 200
            assert response.json()['email'] == 'test@example.com'
            assert response.json()['role'] == 'investor'


class TestFundAPI:
    """Test fund management API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_auth_manager(self):
        """Create mock auth manager."""
        mock_auth = AsyncMock(spec=AuthManager)
        return mock_auth
    
    @pytest.fixture
    def mock_db_manager(self):
        """Create mock database manager."""
        mock_db = AsyncMock(spec=DatabaseManager)
        return mock_db
    
    def test_create_fund_success(self, client, mock_auth_manager, mock_db_manager):
        """Test successful fund creation."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager), \
             patch('src.pocket_hedge_fund.main.app.state.db_manager', mock_db_manager):
            
            # Mock authentication
            mock_auth_manager.verify_token.return_value = {
                'status': 'success',
                'user': {
                    'id': 'test-manager-123',
                    'role': 'fund_manager'
                }
            }
            
            # Mock database operations
            mock_session = AsyncMock()
            mock_db_manager.get_async_session.return_value.__aenter__.return_value = mock_session
            mock_session.execute.return_value.fetchone.return_value = None  # Fund doesn't exist
            mock_session.commit = AsyncMock()
            
            fund_data = {
                'name': 'Test Fund',
                'description': 'A test fund',
                'initial_capital': 100000.00,
                'management_fee_rate': 0.02,
                'performance_fee_rate': 0.20,
                'max_drawdown_limit': 0.10,
                'max_position_size': 0.10,
                'max_leverage': 1.0
            }
            
            headers = {"Authorization": "Bearer test-jwt-token"}
            response = client.post("/api/v1/funds/", json=fund_data, headers=headers)
            
            assert response.status_code == 201
            assert response.json()['name'] == 'Test Fund'
            assert response.json()['manager_id'] == 'test-manager-123'
    
    def test_create_fund_duplicate_name(self, client, mock_auth_manager, mock_db_manager):
        """Test fund creation with duplicate name."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager), \
             patch('src.pocket_hedge_fund.main.app.state.db_manager', mock_db_manager):
            
            # Mock authentication
            mock_auth_manager.verify_token.return_value = {
                'status': 'success',
                'user': {
                    'id': 'test-manager-123',
                    'role': 'fund_manager'
                }
            }
            
            # Mock database operations - fund already exists
            mock_session = AsyncMock()
            mock_db_manager.get_async_session.return_value.__aenter__.return_value = mock_session
            mock_session.execute.return_value.fetchone.return_value = Mock()  # Fund exists
            
            fund_data = {
                'name': 'Existing Fund',
                'description': 'A test fund',
                'initial_capital': 100000.00
            }
            
            headers = {"Authorization": "Bearer test-jwt-token"}
            response = client.post("/api/v1/funds/", json=fund_data, headers=headers)
            
            assert response.status_code == 400
            assert "already exists" in response.json()['detail']
    
    def test_list_funds(self, client, mock_auth_manager, mock_db_manager):
        """Test listing funds."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager), \
             patch('src.pocket_hedge_fund.main.app.state.db_manager', mock_db_manager):
            
            # Mock authentication
            mock_auth_manager.verify_token.return_value = {
                'status': 'success',
                'user': {
                    'id': 'test-user-123',
                    'role': 'investor'
                }
            }
            
            # Mock database operations
            mock_session = AsyncMock()
            mock_db_manager.get_async_session.return_value.__aenter__.return_value = mock_session
            mock_session.execute.return_value.fetchall.return_value = []
            
            headers = {"Authorization": "Bearer test-jwt-token"}
            response = client.get("/api/v1/funds/", headers=headers)
            
            assert response.status_code == 200
            assert isinstance(response.json(), list)
    
    def test_get_fund_by_id(self, client, mock_auth_manager, mock_db_manager):
        """Test getting fund by ID."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager), \
             patch('src.pocket_hedge_fund.main.app.state.db_manager', mock_db_manager):
            
            # Mock authentication
            mock_auth_manager.verify_token.return_value = {
                'status': 'success',
                'user': {
                    'id': 'test-user-123',
                    'role': 'investor'
                }
            }
            
            # Mock database operations
            mock_session = AsyncMock()
            mock_db_manager.get_async_session.return_value.__aenter__.return_value = mock_session
            
            mock_fund = Mock()
            mock_fund.id = 'test-fund-123'
            mock_fund.name = 'Test Fund'
            mock_fund.manager_id = 'test-manager-123'
            mock_fund.status = 'active'
            mock_fund.initial_capital = Decimal('100000.00')
            mock_fund.current_capital = Decimal('100000.00')
            mock_fund.management_fee_rate = Decimal('0.02')
            mock_fund.performance_fee_rate = Decimal('0.20')
            mock_fund.max_drawdown_limit = Decimal('0.10')
            mock_fund.max_position_size = Decimal('0.10')
            mock_fund.max_leverage = Decimal('1.0')
            mock_fund.created_at = datetime.utcnow()
            mock_fund.updated_at = datetime.utcnow()
            mock_fund.launched_at = None
            mock_fund.closed_at = None
            mock_fund.description = 'Test fund description'
            
            mock_session.execute.return_value.fetchone.return_value = mock_fund
            
            headers = {"Authorization": "Bearer test-jwt-token"}
            response = client.get("/api/v1/funds/test-fund-123", headers=headers)
            
            assert response.status_code == 200
            assert response.json()['id'] == 'test-fund-123'
            assert response.json()['name'] == 'Test Fund'
    
    def test_get_fund_not_found(self, client, mock_auth_manager, mock_db_manager):
        """Test getting non-existent fund."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager), \
             patch('src.pocket_hedge_fund.main.app.state.db_manager', mock_db_manager):
            
            # Mock authentication
            mock_auth_manager.verify_token.return_value = {
                'status': 'success',
                'user': {
                    'id': 'test-user-123',
                    'role': 'investor'
                }
            }
            
            # Mock database operations - fund not found
            mock_session = AsyncMock()
            mock_db_manager.get_async_session.return_value.__aenter__.return_value = mock_session
            mock_session.execute.return_value.fetchone.return_value = None
            
            headers = {"Authorization": "Bearer test-jwt-token"}
            response = client.get("/api/v1/funds/non-existent-fund", headers=headers)
            
            assert response.status_code == 404
            assert "not found" in response.json()['detail']


class TestPortfolioAPI:
    """Test portfolio management API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_auth_manager(self):
        """Create mock auth manager."""
        mock_auth = AsyncMock(spec=AuthManager)
        return mock_auth
    
    @pytest.fixture
    def mock_db_manager(self):
        """Create mock database manager."""
        mock_db = AsyncMock(spec=DatabaseManager)
        return mock_db
    
    def test_create_position_success(self, client, mock_auth_manager, mock_db_manager):
        """Test successful position creation."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager), \
             patch('src.pocket_hedge_fund.main.app.state.db_manager', mock_db_manager):
            
            # Mock authentication
            mock_auth_manager.verify_token.return_value = {
                'status': 'success',
                'user': {
                    'id': 'test-manager-123',
                    'role': 'fund_manager'
                }
            }
            
            # Mock database operations
            mock_session = AsyncMock()
            mock_db_manager.get_async_session.return_value.__aenter__.return_value = mock_session
            
            # Mock fund exists
            mock_fund = Mock()
            mock_fund.manager_id = 'test-manager-123'
            mock_session.execute.return_value.fetchone.return_value = mock_fund
            mock_session.commit = AsyncMock()
            
            position_data = {
                'fund_id': 'test-fund-123',
                'symbol': 'AAPL',
                'position_type': 'long',
                'quantity': 100.0,
                'entry_price': 150.0,
                'stop_loss': 140.0,
                'take_profit': 160.0,
                'notes': 'Test position'
            }
            
            headers = {"Authorization": "Bearer test-jwt-token"}
            response = client.post("/api/v1/portfolios/test-fund-123/positions", 
                                 json=position_data, headers=headers)
            
            assert response.status_code == 201
            assert response.json()['symbol'] == 'AAPL'
            assert response.json()['position_type'] == 'long'
    
    def test_list_positions(self, client, mock_auth_manager, mock_db_manager):
        """Test listing positions."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager), \
             patch('src.pocket_hedge_fund.main.app.state.db_manager', mock_db_manager):
            
            # Mock authentication
            mock_auth_manager.verify_token.return_value = {
                'status': 'success',
                'user': {
                    'id': 'test-user-123',
                    'role': 'investor'
                }
            }
            
            # Mock database operations
            mock_session = AsyncMock()
            mock_db_manager.get_async_session.return_value.__aenter__.return_value = mock_session
            
            # Mock fund exists
            mock_fund = Mock()
            mock_fund.manager_id = 'test-manager-123'
            mock_session.execute.return_value.fetchone.return_value = mock_fund
            
            # Mock positions
            mock_session.execute.return_value.fetchall.return_value = []
            
            headers = {"Authorization": "Bearer test-jwt-token"}
            response = client.get("/api/v1/portfolios/test-fund-123/positions", headers=headers)
            
            assert response.status_code == 200
            assert isinstance(response.json(), list)
    
    def test_get_position_by_id(self, client, mock_auth_manager, mock_db_manager):
        """Test getting position by ID."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager), \
             patch('src.pocket_hedge_fund.main.app.state.db_manager', mock_db_manager):
            
            # Mock authentication
            mock_auth_manager.verify_token.return_value = {
                'status': 'success',
                'user': {
                    'id': 'test-user-123',
                    'role': 'investor'
                }
            }
            
            # Mock database operations
            mock_session = AsyncMock()
            mock_db_manager.get_async_session.return_value.__aenter__.return_value = mock_session
            
            mock_position = Mock()
            mock_position.id = 'test-position-123'
            mock_position.fund_id = 'test-fund-123'
            mock_position.symbol = 'AAPL'
            mock_position.position_type = 'long'
            mock_position.quantity = Decimal('100.0')
            mock_position.entry_price = Decimal('150.0')
            mock_position.current_price = Decimal('155.0')
            mock_position.stop_loss = Decimal('140.0')
            mock_position.take_profit = Decimal('160.0')
            mock_position.unrealized_pnl = Decimal('500.0')
            mock_position.realized_pnl = Decimal('0.0')
            mock_position.notes = 'Test position'
            mock_position.created_at = datetime.utcnow()
            mock_position.updated_at = datetime.utcnow()
            mock_position.closed_at = None
            mock_position.manager_id = 'test-manager-123'
            
            mock_session.execute.return_value.fetchone.return_value = mock_position
            
            headers = {"Authorization": "Bearer test-jwt-token"}
            response = client.get("/api/v1/portfolios/test-fund-123/positions/test-position-123", 
                                headers=headers)
            
            assert response.status_code == 200
            assert response.json()['id'] == 'test-position-123'
            assert response.json()['symbol'] == 'AAPL'


class TestPerformanceAPI:
    """Test performance tracking API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_auth_manager(self):
        """Create mock auth manager."""
        mock_auth = AsyncMock(spec=AuthManager)
        return mock_auth
    
    @pytest.fixture
    def mock_db_manager(self):
        """Create mock database manager."""
        mock_db = AsyncMock(spec=DatabaseManager)
        return mock_db
    
    def test_get_performance_metrics(self, client, mock_auth_manager, mock_db_manager):
        """Test getting performance metrics."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager), \
             patch('src.pocket_hedge_fund.main.app.state.db_manager', mock_db_manager):
            
            # Mock authentication
            mock_auth_manager.verify_token.return_value = {
                'status': 'success',
                'user': {
                    'id': 'test-user-123',
                    'role': 'investor'
                }
            }
            
            # Mock database operations
            mock_session = AsyncMock()
            mock_db_manager.get_async_session.return_value.__aenter__.return_value = mock_session
            
            # Mock fund exists
            mock_fund = Mock()
            mock_fund.manager_id = 'test-manager-123'
            mock_session.execute.return_value.fetchone.return_value = mock_fund
            
            # Mock performance data
            mock_db_utils = AsyncMock()
            mock_db_utils.get_performance_metrics.return_value = {
                'total_return': Decimal('0.15'),
                'annualized_return': Decimal('0.12'),
                'volatility': Decimal('0.20'),
                'sharpe_ratio': Decimal('0.60'),
                'max_drawdown': Decimal('0.08'),
                'calmar_ratio': Decimal('1.50'),
                'win_rate': Decimal('0.65'),
                'profit_factor': Decimal('1.80'),
                'sortino_ratio': Decimal('0.75'),
                'var_95': Decimal('0.05'),
                'cvar_95': Decimal('0.07')
            }
            
            with patch('src.pocket_hedge_fund.api.performance_api.DatabaseUtils', return_value=mock_db_utils):
                headers = {"Authorization": "Bearer test-jwt-token"}
                response = client.get("/api/v1/performance/test-fund-123/metrics", headers=headers)
                
                assert response.status_code == 200
                assert response.json()['total_return'] == 0.15
                assert response.json()['sharpe_ratio'] == 0.60
    
    def test_get_performance_snapshots(self, client, mock_auth_manager, mock_db_manager):
        """Test getting performance snapshots."""
        with patch('src.pocket_hedge_fund.main.app.state.auth_manager', mock_auth_manager), \
             patch('src.pocket_hedge_fund.main.app.state.db_manager', mock_db_manager):
            
            # Mock authentication
            mock_auth_manager.verify_token.return_value = {
                'status': 'success',
                'user': {
                    'id': 'test-user-123',
                    'role': 'investor'
                }
            }
            
            # Mock database operations
            mock_session = AsyncMock()
            mock_db_manager.get_async_session.return_value.__aenter__.return_value = mock_session
            
            # Mock fund exists
            mock_fund = Mock()
            mock_fund.manager_id = 'test-manager-123'
            mock_session.execute.return_value.fetchone.return_value = mock_fund
            
            # Mock performance snapshots
            mock_db_utils = AsyncMock()
            mock_db_utils.get_performance_snapshots.return_value = []
            
            with patch('src.pocket_hedge_fund.api.performance_api.DatabaseUtils', return_value=mock_db_utils):
                headers = {"Authorization": "Bearer test-jwt-token"}
                response = client.get("/api/v1/performance/test-fund-123/snapshots", headers=headers)
                
                assert response.status_code == 200
                assert isinstance(response.json(), list)


class TestAPIIntegration:
    """Integration tests for API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()['status'] in ['healthy', 'unhealthy']
        assert 'timestamp' in response.json()
        assert 'version' in response.json()
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        assert response.json()['message'] == "Pocket Hedge Fund API"
        assert response.json()['version'] == "1.0.0"
    
    def test_openapi_docs(self, client):
        """Test OpenAPI documentation endpoint."""
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        assert 'openapi' in response.json()
        assert 'info' in response.json()
        assert response.json()['info']['title'] == "Pocket Hedge Fund API"


if __name__ == "__main__":
    pytest.main([__file__])
