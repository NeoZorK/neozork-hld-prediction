"""
Unit tests for Investment API

Tests the investment API endpoints including request validation,
authentication, and response formatting.
"""

import pytest
import pytest_asyncio
from decimal import Decimal
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.pocket_hedge_fund.api.investment_api import router
from src.pocket_hedge_fund.validation.investment_validator import InvestmentValidator
from src.pocket_hedge_fund.api.investment_api import get_current_user


class TestInvestmentAPI:
    """Test cases for Investment API endpoints."""
    
    @pytest.fixture
    def app(self):
        """Create FastAPI app for testing."""
        app = FastAPI()
        app.include_router(router)
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_current_user(self):
        """Mock current user for authentication."""
        return {
            'id': 'test-user-id',
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'investor'
        }
    
    @pytest.fixture
    def sample_investment_request(self):
        """Sample investment request data."""
        return {
            'fund_id': 'test-fund-id',
            'amount': 5000.00
        }
    
    @pytest.mark.asyncio
    async def test_create_investment_success(self, client, mock_current_user, sample_investment_request):
        """Test successful investment creation."""
        # Mock dependencies
        mock_validator = AsyncMock()
        mock_validator.validate_investment.return_value = (
            True, 
            "Investment validation passed", 
            {
                'fund': {
                    'id': 'test-fund-id',
                    'name': 'Test Fund',
                    'current_value': Decimal('100000.00'),
                    'initial_capital': Decimal('100000.00')
                },
                'investor': {
                    'id': 'test-user-id',
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'role': 'investor',
                    'is_active': True
                },
                'investor_id': 'test-user-id',
                'risk_score': 25.0
            }
        )
        
        mock_db_manager = AsyncMock()
        mock_db_manager.execute_command.return_value = None
        mock_db_manager.execute_query.return_value = [{
            'id': 'new-investment-id',
            'investor_id': 'test-user-id',
            'fund_id': 'test-fund-id',
            'amount': Decimal('5000.00'),
            'investment_type': 'buy',
            'shares_acquired': Decimal('50.00'),
            'share_price': Decimal('100.00'),
            'status': 'active',
            'created_at': datetime.now(datetime.UTC),
            'updated_at': datetime.now(datetime.UTC)
        }]
        
        # Override dependencies
        client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
        
        with patch('src.pocket_hedge_fund.api.investment_api.get_investment_validator', return_value=mock_validator), \
             patch('src.pocket_hedge_fund.api.investment_api.get_db_manager', return_value=mock_db_manager):
            
            response = client.post("/api/v1/investments/", json=sample_investment_request)
            
            assert response.status_code == 201
            data = response.json()
            # API returns InvestmentResponse directly, not wrapped in success object
            assert data['fund_id'] == 'test-fund-id'
            assert data['amount'] == 5000.00
            assert data['investor_id'] == 'test-user-id'
        
        # Clean up
        client.app.dependency_overrides.clear()
    
    @pytest.mark.asyncio
    async def test_create_investment_validation_failed(self, client, mock_current_user, sample_investment_request):
        """Test investment creation with validation failure."""
        # Mock validator to return validation failure
        mock_validator = AsyncMock()
        mock_validator.validate_investment.return_value = (
            False, 
            "Investment amount below minimum", 
            {}
        )
        
        # Override dependencies
        client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
        
        with patch('src.pocket_hedge_fund.api.investment_api.get_investment_validator', return_value=mock_validator):
            
            response = client.post("/api/v1/investments/", json=sample_investment_request)
            
            assert response.status_code == 400
            data = response.json()
            assert 'detail' in data
            assert "Investment validation failed" in data['detail']
        
        # Clean up
        client.app.dependency_overrides.clear()
    
    @pytest.mark.asyncio
    async def test_create_investment_unauthorized_role(self, client, sample_investment_request):
        """Test investment creation with unauthorized role."""
        mock_current_user = {
            'id': 'test-user-id',
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'guest'  # Unauthorized role
        }
        
        # Override dependencies
        client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
        
        response = client.post("/api/v1/investments/", json=sample_investment_request)
        
        assert response.status_code == 403
        data = response.json()
        assert 'detail' in data
        assert "Requires investor role" in data['detail']
        
        # Clean up
        client.app.dependency_overrides.clear()
    
    @pytest.mark.asyncio
    async def test_get_investments_success(self, client, mock_current_user):
        """Test successful retrieval of investments."""
        mock_investments = [
            {
                'id': 'investment-1',
                'investor_id': 'test-user-id',
                'fund_id': 'fund-1',
                'amount': Decimal('5000.00'),
                'investment_type': 'buy',
                'shares_acquired': Decimal('50.00'),
                'share_price': Decimal('100.00'),
                'status': 'active',
                'created_at': datetime(2025, 1, 1, 0, 0, 0),
                'updated_at': datetime(2025, 1, 1, 0, 0, 0)
            },
            {
                'id': 'investment-2',
                'investor_id': 'test-user-id',
                'fund_id': 'fund-2',
                'amount': Decimal('3000.00'),
                'investment_type': 'buy',
                'shares_acquired': Decimal('30.00'),
                'share_price': Decimal('100.00'),
                'status': 'active',
                'created_at': datetime(2025, 1, 2, 0, 0, 0),
                'updated_at': datetime(2025, 1, 2, 0, 0, 0)
            }
        ]
        
        mock_db_manager = AsyncMock()
        mock_db_manager.execute_query.return_value = mock_investments
        
        # Override dependencies
        client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
        
        with patch('src.pocket_hedge_fund.api.investment_api.get_db_manager', return_value=mock_db_manager):
            
            response = client.get("/api/v1/investments/")
            
            assert response.status_code == 200
            data = response.json()
            # API returns list directly, not wrapped in 'investments' key
            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]['id'] == 'investment-1'
            assert data[1]['id'] == 'investment-2'
        
        # Clean up
        client.app.dependency_overrides.clear()
    
    @pytest.mark.asyncio
    async def test_get_investment_by_id_success(self, client, mock_current_user):
        """Test successful retrieval of specific investment."""
        mock_investment = {
            'id': 'investment-1',
            'investor_id': 'test-user-id',
            'fund_id': 'fund-1',
            'amount': Decimal('5000.00'),
            'investment_type': 'buy',
            'shares_acquired': Decimal('50.00'),
            'share_price': Decimal('100.00'),
            'status': 'active',
                'created_at': datetime(2025, 1, 1, 0, 0, 0),
                'updated_at': datetime(2025, 1, 1, 0, 0, 0)
        }
        
        mock_db_manager = AsyncMock()
        mock_db_manager.execute_query.return_value = [mock_investment]
        
        # Override dependencies
        client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
        
        with patch('src.pocket_hedge_fund.api.investment_api.get_db_manager', return_value=mock_db_manager):
            
            response = client.get("/api/v1/investments/investment-1")
            
            assert response.status_code == 200
            data = response.json()
            assert data['id'] == 'investment-1'
            assert data['amount'] == 5000.00
            assert data['shares_acquired'] == 50.00
        
        # Clean up
        client.app.dependency_overrides.clear()
    
    @pytest.mark.asyncio
    async def test_get_investment_by_id_not_found(self, client, mock_current_user):
        """Test retrieval of non-existent investment."""
        mock_db_manager = AsyncMock()
        mock_db_manager.execute_query.return_value = []
        
        # Override dependencies
        client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
        
        with patch('src.pocket_hedge_fund.api.investment_api.get_db_manager', return_value=mock_db_manager):
            
            response = client.get("/api/v1/investments/non-existent-id")
            
            assert response.status_code == 404
            data = response.json()
            assert 'detail' in data
            assert "Investment not found" in data['detail']
        
        # Clean up
        client.app.dependency_overrides.clear()
    
    @pytest.mark.asyncio
    async def test_get_investment_by_id_unauthorized(self, client):
        """Test retrieval of investment with unauthorized access."""
        mock_current_user = {
            'id': 'other-user-id',
            'username': 'otheruser',
            'email': 'other@example.com',
            'role': 'investor'
        }
        
        mock_investment = {
            'id': 'investment-1',
            'investor_id': 'different-user-id',  # Different investor
            'fund_id': 'fund-1',
            'amount': Decimal('5000.00'),
            'investment_type': 'buy',
            'shares_acquired': Decimal('50.00'),
            'share_price': Decimal('100.00'),
            'status': 'active',
                'created_at': datetime(2025, 1, 1, 0, 0, 0),
                'updated_at': datetime(2025, 1, 1, 0, 0, 0)
        }
        
        mock_db_manager = AsyncMock()
        # Mock empty result since investor_id doesn't match current_user['id']
        mock_db_manager.execute_query.return_value = []
        
        # Override dependencies
        client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
        
        with patch('src.pocket_hedge_fund.api.investment_api.get_db_manager', return_value=mock_db_manager):
            
            response = client.get("/api/v1/investments/investment-1")
            
            assert response.status_code == 404
            data = response.json()
            assert 'detail' in data
            assert "Investment not found" in data['detail']
        
        # Clean up
        client.app.dependency_overrides.clear()
    
    @pytest.mark.asyncio
    async def test_create_investment_invalid_amount(self, client, mock_current_user):
        """Test investment creation with invalid amount."""
        invalid_request = {
            'fund_id': 'test-fund-id',
            'amount': -1000.00  # Negative amount
        }
        
        # Override dependencies
        client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
        
        response = client.post("/api/v1/investments/", json=invalid_request)
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert 'detail' in data
        
        # Clean up
        client.app.dependency_overrides.clear()
    
    @pytest.mark.asyncio
    async def test_create_investment_missing_fields(self, client, mock_current_user):
        """Test investment creation with missing required fields."""
        incomplete_request = {
            'fund_id': 'test-fund-id'
            # Missing amount field
        }
        
        # Override dependencies
        client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
        
        response = client.post("/api/v1/investments/", json=incomplete_request)
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert 'detail' in data
        
        # Clean up
        client.app.dependency_overrides.clear()
    
    @pytest.mark.asyncio
    async def test_create_investment_database_error(self, client, mock_current_user, sample_investment_request):
        """Test investment creation with database error."""
        # Mock validator to return success
        mock_validator = AsyncMock()
        mock_validator.validate_investment.return_value = (
            True, 
            "Investment validation passed", 
            {
                'fund': {
                    'id': 'test-fund-id',
                    'name': 'Test Fund',
                    'current_value': Decimal('100000.00'),
                    'initial_capital': Decimal('100000.00')
                },
                'risk_score': 25.0
            }
        )
        
        # Mock database to raise exception
        mock_db_manager = AsyncMock()
        mock_db_manager.execute_command.side_effect = Exception("Database connection failed")
        
        # Override dependencies
        client.app.dependency_overrides[get_current_user] = lambda: mock_current_user
        
        with patch('src.pocket_hedge_fund.api.investment_api.get_investment_validator', return_value=mock_validator), \
             patch('src.pocket_hedge_fund.api.investment_api.get_db_manager', return_value=mock_db_manager):
            
            response = client.post("/api/v1/investments/", json=sample_investment_request)
            
            assert response.status_code == 500
            data = response.json()
            assert 'detail' in data
            assert "Investment creation failed" in data['detail']
        
        # Clean up
        client.app.dependency_overrides.clear()
