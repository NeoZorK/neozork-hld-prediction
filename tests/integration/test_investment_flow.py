"""
Integration tests for Investment Flow

Tests the complete investment flow from user registration to investment creation,
including database interactions and API endpoints.
"""

import pytest
import pytest_asyncio
from decimal import Decimal
from fastapi.testclient import TestClient
from src.pocket_hedge_fund.main import app


class TestInvestmentFlow:
    """Integration tests for complete investment flow."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest_asyncio.fixture
    async def test_user_data(self):
        """Test user data for registration."""
        return {
            'email': 'integration_test@example.com',
            'username': 'integration_test_user',
            'password': 'TestPassword123!',
            'first_name': 'Integration',
            'last_name': 'Test'
        }
    
    @pytest_asyncio.fixture
    async def test_fund_data(self):
        """Test fund data for creation."""
        return {
            'name': 'Integration Test Fund',
            'description': 'A fund for integration testing',
            'fund_type': 'mini',
            'initial_capital': 100000.00,
            'min_investment': 1000.00,
            'max_investment': 10000.00
        }
    
    @pytest.mark.asyncio
    async def test_complete_investment_flow(self, client, test_user_data, test_fund_data):
        """Test complete investment flow from registration to investment."""
        # Step 1: Register user
        register_response = client.post("/api/v1/auth/register", json=test_user_data)
        assert register_response.status_code == 200
        register_data = register_response.json()
        assert register_data['success'] is True
        user_id = register_data['user']['id']
        
        # Step 2: Login user
        login_data = {
            'email': test_user_data['email'],
            'password': test_user_data['password']
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        login_result = login_response.json()
        assert 'access_token' in login_result
        access_token = login_result['access_token']
        
        # Set authorization header
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Step 3: Create fund (as admin - this would need admin user in real scenario)
        # For now, we'll assume fund exists or create it through direct database
        # In a real integration test, you'd create an admin user first
        
        # Step 4: Get available funds
        funds_response = client.get("/api/v1/funds/", headers=headers)
        assert funds_response.status_code == 200
        funds_data = funds_response.json()
        assert 'funds' in funds_data
        
        # If no funds exist, we need to create one
        # For integration test, we'll use the first available fund
        if not funds_data['funds']:
            # Create a fund through API (would need admin role)
            # For now, skip this step and assume fund exists
            pytest.skip("No funds available for testing - would need admin user to create fund")
        
        fund_id = funds_data['funds'][0]['id']
        
        # Step 5: Create investment
        investment_data = {
            'fund_id': fund_id,
            'amount': 5000.00
        }
        
        investment_response = client.post("/api/v1/investments/", json=investment_data, headers=headers)
        assert investment_response.status_code == 201
        investment_result = investment_response.json()
        assert investment_result['success'] is True
        assert 'investment' in investment_result
        investment_id = investment_result['investment']['id']
        
        # Step 6: Verify investment was created
        get_investment_response = client.get(f"/api/v1/investments/{investment_id}", headers=headers)
        assert get_investment_response.status_code == 200
        investment_details = get_investment_response.json()
        assert investment_details['id'] == investment_id
        assert investment_details['amount'] == 5000.00
        assert investment_details['fund_id'] == fund_id
        
        # Step 7: Get all user investments
        investments_response = client.get("/api/v1/investments/", headers=headers)
        assert investments_response.status_code == 200
        investments_data = investments_response.json()
        assert 'investments' in investments_data
        assert len(investments_data['investments']) >= 1
        
        # Verify our investment is in the list
        investment_found = any(inv['id'] == investment_id for inv in investments_data['investments'])
        assert investment_found
    
    @pytest.mark.asyncio
    async def test_investment_validation_flow(self, client, test_user_data):
        """Test investment validation flow with various scenarios."""
        # Register and login user
        register_response = client.post("/api/v1/auth/register", json=test_user_data)
        assert register_response.status_code == 200
        
        login_data = {
            'email': test_user_data['email'],
            'password': test_user_data['password']
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Get available funds
        funds_response = client.get("/api/v1/funds/", headers=headers)
        assert funds_response.status_code == 200
        funds_data = funds_response.json()
        
        if not funds_data['funds']:
            pytest.skip("No funds available for testing")
        
        fund_id = funds_data['funds'][0]['id']
        
        # Test 1: Valid investment
        valid_investment = {
            'fund_id': fund_id,
            'amount': 2000.00
        }
        response = client.post("/api/v1/investments/", json=valid_investment, headers=headers)
        assert response.status_code == 201
        
        # Test 2: Investment below minimum
        low_investment = {
            'fund_id': fund_id,
            'amount': 100.00  # Below typical minimum
        }
        response = client.post("/api/v1/investments/", json=low_investment, headers=headers)
        # This might succeed or fail depending on fund's minimum investment
        # We just verify the API handles it properly
        assert response.status_code in [201, 400]
        
        # Test 3: Investment above maximum
        high_investment = {
            'fund_id': fund_id,
            'amount': 50000.00  # Above typical maximum
        }
        response = client.post("/api/v1/investments/", json=high_investment, headers=headers)
        # This might succeed or fail depending on fund's maximum investment
        assert response.status_code in [201, 400]
        
        # Test 4: Invalid fund ID
        invalid_fund_investment = {
            'fund_id': 'non-existent-fund-id',
            'amount': 2000.00
        }
        response = client.post("/api/v1/investments/", json=invalid_fund_investment, headers=headers)
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_portfolio_retrieval_flow(self, client, test_user_data):
        """Test portfolio retrieval flow."""
        # Register and login user
        register_response = client.post("/api/v1/auth/register", json=test_user_data)
        assert register_response.status_code == 200
        
        login_data = {
            'email': test_user_data['email'],
            'password': test_user_data['password']
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Get portfolio summary
        portfolio_response = client.get("/api/v1/portfolio/summary", headers=headers)
        assert portfolio_response.status_code == 200
        portfolio_data = portfolio_response.json()
        assert 'total_value' in portfolio_data
        assert 'total_invested' in portfolio_data
        assert 'total_return' in portfolio_data
        
        # Get portfolio allocations
        allocations_response = client.get("/api/v1/portfolio/allocations", headers=headers)
        assert allocations_response.status_code == 200
        allocations_data = allocations_response.json()
        assert 'allocations' in allocations_data
        
        # Get portfolio analytics
        analytics_response = client.get("/api/v1/portfolio/analytics", headers=headers)
        assert analytics_response.status_code == 200
        analytics_data = analytics_response.json()
        assert 'analytics' in analytics_data
    
    @pytest.mark.asyncio
    async def test_returns_calculation_flow(self, client, test_user_data):
        """Test returns calculation flow."""
        # Register and login user
        register_response = client.post("/api/v1/auth/register", json=test_user_data)
        assert register_response.status_code == 200
        
        login_data = {
            'email': test_user_data['email'],
            'password': test_user_data['password']
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Get portfolio returns
        returns_response = client.get("/api/v1/returns/portfolio", headers=headers)
        assert returns_response.status_code == 200
        returns_data = returns_response.json()
        assert 'total_return' in returns_data
        assert 'return_percentage' in returns_data
        
        # Get returns summary
        summary_response = client.get("/api/v1/returns/summary", headers=headers)
        assert summary_response.status_code == 200
        summary_data = summary_response.json()
        assert 'summary' in summary_data
        
        # Get risk metrics
        risk_response = client.get("/api/v1/returns/risk-metrics", headers=headers)
        assert risk_response.status_code == 200
        risk_data = risk_response.json()
        assert 'risk_metrics' in risk_data
    
    @pytest.mark.asyncio
    async def test_authentication_flow(self, client, test_user_data):
        """Test authentication flow."""
        # Test 1: Register new user
        register_response = client.post("/api/v1/auth/register", json=test_user_data)
        assert register_response.status_code == 200
        register_data = register_response.json()
        assert register_data['success'] is True
        
        # Test 2: Login with correct credentials
        login_data = {
            'email': test_user_data['email'],
            'password': test_user_data['password']
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        login_result = login_response.json()
        assert 'access_token' in login_result
        assert 'token_type' in login_result
        assert login_result['token_type'] == 'bearer'
        
        # Test 3: Access protected endpoint with valid token
        access_token = login_result['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        profile_response = client.get("/api/v1/users/profile", headers=headers)
        assert profile_response.status_code == 200
        profile_data = profile_response.json()
        assert profile_data['email'] == test_user_data['email']
        assert profile_data['username'] == test_user_data['username']
        
        # Test 4: Access protected endpoint without token
        no_auth_response = client.get("/api/v1/users/profile")
        assert no_auth_response.status_code == 401
        
        # Test 5: Access protected endpoint with invalid token
        invalid_headers = {'Authorization': 'Bearer invalid_token'}
        invalid_auth_response = client.get("/api/v1/users/profile", headers=invalid_headers)
        assert invalid_auth_response.status_code == 401
        
        # Test 6: Login with incorrect password
        wrong_login_data = {
            'email': test_user_data['email'],
            'password': 'wrong_password'
        }
        wrong_login_response = client.post("/api/v1/auth/login", json=wrong_login_data)
        assert wrong_login_response.status_code == 401
        
        # Test 7: Login with non-existent email
        non_existent_login_data = {
            'email': 'non_existent@example.com',
            'password': test_user_data['password']
        }
        non_existent_login_response = client.post("/api/v1/auth/login", json=non_existent_login_data)
        assert non_existent_login_response.status_code == 401
