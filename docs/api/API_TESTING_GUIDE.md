# 🧪 NeoZork Pocket Hedge Fund - API Testing Guide

## 📊 **OVERVIEW**

This guide provides comprehensive testing strategies, tools, and examples for the NeoZork Pocket Hedge Fund APIs. It covers unit testing, integration testing, performance testing, and security testing.

---

## 🛠️ **TESTING TOOLS**

### **Recommended Testing Tools**
- **Postman** - API testing and documentation
- **curl** - Command-line testing
- **pytest** - Python testing framework
- **Jest** - JavaScript testing framework
- **Newman** - Postman CLI runner
- **Artillery** - Performance testing
- **OWASP ZAP** - Security testing

---

## 🔧 **SETUP AND CONFIGURATION**

### **Environment Setup**
```bash
# Create virtual environment
python -m venv neozork-testing
source neozork-testing/bin/activate  # Linux/Mac
# neozork-testing\Scripts\activate  # Windows

# Install dependencies
pip install pytest requests python-dotenv
```

### **Test Configuration**
```python
# test_config.py
import os
from dotenv import load_dotenv

load_dotenv()

class TestConfig:
    BASE_URL = os.getenv('NEOZORK_BASE_URL', 'https://api.neozork.com')
    API_KEY = os.getenv('NEOZORK_API_KEY')
    TEST_USERNAME = os.getenv('TEST_USERNAME', 'test_user')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD', 'TestPass123!')
    
    # Test data
    TEST_FUND_ID = "456e7890-e89b-12d3-a456-426614174001"
    TEST_STRATEGY_ID = "def45678-e89b-12d3-a456-426614174005"
```

---

## 🔐 **AUTHENTICATION TESTING**

### **Test Authentication Flow**
```python
# test_auth.py
import pytest
import requests
from test_config import TestConfig

class TestAuthentication:
    def setup_method(self):
        self.base_url = TestConfig.BASE_URL
        self.auth_url = f"{self.base_url}/api/v1/auth"
        
    def test_user_registration(self):
        """Test user registration"""
        payload = {
            "username": "test_user_001",
            "email": "test001@example.com",
            "password": "TestPass123!",
            "first_name": "Test",
            "last_name": "User",
            "role": "INVESTOR"
        }
        
        response = requests.post(f"{self.auth_url}/register", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "user_id" in data["data"]
        
    def test_user_login(self):
        """Test user login"""
        payload = {
            "username": TestConfig.TEST_USERNAME,
            "password": TestConfig.TEST_PASSWORD
        }
        
        response = requests.post(f"{self.auth_url}/login", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        
        # Store token for other tests
        self.access_token = data["data"]["access_token"]
        
    def test_token_refresh(self):
        """Test token refresh"""
        # First login to get refresh token
        login_payload = {
            "username": TestConfig.TEST_USERNAME,
            "password": TestConfig.TEST_PASSWORD
        }
        
        login_response = requests.post(f"{self.auth_url}/login", json=login_payload)
        refresh_token = login_response.json()["data"]["refresh_token"]
        
        # Test refresh
        refresh_payload = {"refresh_token": refresh_token}
        response = requests.post(f"{self.auth_url}/refresh", json=refresh_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data["data"]
        
    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        payload = {
            "username": "invalid_user",
            "password": "invalid_password"
        }
        
        response = requests.post(f"{self.auth_url}/login", json=payload)
        
        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        
    def test_expired_token(self):
        """Test API call with expired token"""
        headers = {"Authorization": "Bearer expired_token"}
        response = requests.get(f"{self.base_url}/api/v1/funds/", headers=headers)
        
        assert response.status_code == 401
```

---

## 💰 **FUND MANAGEMENT TESTING**

### **Test Fund Operations**
```python
# test_funds.py
import pytest
import requests
from test_config import TestConfig

class TestFundManagement:
    def setup_method(self):
        self.base_url = TestConfig.BASE_URL
        self.funds_url = f"{self.base_url}/api/v1/funds"
        self.access_token = self._get_access_token()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        
    def _get_access_token(self):
        """Helper method to get access token"""
        login_payload = {
            "username": TestConfig.TEST_USERNAME,
            "password": TestConfig.TEST_PASSWORD
        }
        response = requests.post(f"{self.base_url}/api/v1/auth/login", json=login_payload)
        return response.json()["data"]["access_token"]
        
    def test_create_fund(self):
        """Test fund creation"""
        payload = {
            "name": "Test Growth Fund",
            "description": "A test fund for automated testing",
            "strategy": "growth",
            "risk_level": 7,
            "target_return": 15.0,
            "min_investment": 1000.0,
            "management_fee": 2.0,
            "performance_fee": 20.0
        }
        
        response = requests.post(self.funds_url, json=payload, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["name"] == payload["name"]
        
        # Store fund ID for other tests
        self.test_fund_id = data["data"]["fund_id"]
        
    def test_get_funds(self):
        """Test getting list of funds"""
        response = requests.get(self.funds_url, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "funds" in data
        assert "total_count" in data
        
    def test_get_fund_by_id(self):
        """Test getting fund by ID"""
        fund_id = TestConfig.TEST_FUND_ID
        response = requests.get(f"{self.funds_url}/{fund_id}", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["fund_id"] == fund_id
        
    def test_fund_filtering(self):
        """Test fund filtering"""
        params = {
            "strategy": "growth",
            "risk_level": 7,
            "page": 1,
            "page_size": 10
        }
        
        response = requests.get(self.funds_url, params=params, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all returned funds match filter criteria
        for fund in data["funds"]:
            assert fund["strategy"] == "growth"
            assert fund["risk_level"] == 7
            
    def test_fund_performance(self):
        """Test getting fund performance"""
        fund_id = TestConfig.TEST_FUND_ID
        response = requests.get(f"{self.funds_url}/{fund_id}/performance", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "performance_history" in data
        assert "total_records" in data
        
    def test_fund_investors(self):
        """Test getting fund investors"""
        fund_id = TestConfig.TEST_FUND_ID
        response = requests.get(f"{self.funds_url}/{fund_id}/investors", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "investors" in data
        assert "total_investors" in data
```

---

## 📊 **PORTFOLIO TESTING**

### **Test Portfolio Operations**
```python
# test_portfolio.py
import pytest
import requests
from test_config import TestConfig

class TestPortfolioManagement:
    def setup_method(self):
        self.base_url = TestConfig.BASE_URL
        self.portfolio_url = f"{self.base_url}/api/v1/portfolio"
        self.access_token = self._get_access_token()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.fund_id = TestConfig.TEST_FUND_ID
        
    def _get_access_token(self):
        """Helper method to get access token"""
        login_payload = {
            "username": TestConfig.TEST_USERNAME,
            "password": TestConfig.TEST_PASSWORD
        }
        response = requests.post(f"{self.base_url}/api/v1/auth/login", json=login_payload)
        return response.json()["data"]["access_token"]
        
    def test_get_portfolio_positions(self):
        """Test getting portfolio positions"""
        response = requests.get(f"{self.portfolio_url}/{self.fund_id}/positions", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "positions" in data
        assert "total_positions" in data
        
    def test_add_position(self):
        """Test adding new position"""
        payload = {
            "asset_symbol": "TEST",
            "asset_name": "Test Asset",
            "asset_type": "stock",
            "quantity": 100,
            "price": 50.0
        }
        
        response = requests.post(f"{self.portfolio_url}/{self.fund_id}/positions", 
                               json=payload, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["asset_symbol"] == payload["asset_symbol"]
        
    def test_update_position_prices(self):
        """Test updating position prices"""
        payload = {
            "price_updates": {
                "TEST": 55.0,
                "AAPL": 155.0
            }
        }
        
        response = requests.put(f"{self.portfolio_url}/{self.fund_id}/prices", 
                              json=payload, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_updated" in data["data"]
        
    def test_portfolio_metrics(self):
        """Test getting portfolio metrics"""
        response = requests.get(f"{self.portfolio_url}/{self.fund_id}/metrics", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_value" in data
        assert "total_pnl" in data
        assert "total_return_percentage" in data
        
    def test_portfolio_rebalancing(self):
        """Test portfolio rebalancing"""
        payload = {
            "target_weights": {
                "TEST": 50.0,
                "AAPL": 30.0,
                "GOOGL": 20.0
            }
        }
        
        response = requests.post(f"{self.portfolio_url}/{self.fund_id}/rebalance", 
                               json=payload, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_trades" in data["data"]
        
    def test_transaction_history(self):
        """Test getting transaction history"""
        response = requests.get(f"{self.portfolio_url}/{self.fund_id}/transactions", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "transactions" in data
        assert "total_transactions" in data
```

---

## 👥 **USER MANAGEMENT TESTING**

### **Test User Operations**
```python
# test_users.py
import pytest
import requests
from test_config import TestConfig

class TestUserManagement:
    def setup_method(self):
        self.base_url = TestConfig.BASE_URL
        self.users_url = f"{self.base_url}/api/v1/users"
        self.access_token = self._get_admin_token()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        
    def _get_admin_token(self):
        """Helper method to get admin token"""
        login_payload = {
            "username": "admin_user",
            "password": "AdminPass123!"
        }
        response = requests.post(f"{self.base_url}/api/v1/auth/login", json=login_payload)
        return response.json()["data"]["access_token"]
        
    def test_create_user(self):
        """Test user creation"""
        payload = {
            "username": "test_user_002",
            "email": "test002@example.com",
            "password": "TestPass123!",
            "first_name": "Test",
            "last_name": "User",
            "role": "INVESTOR"
        }
        
        response = requests.post(self.users_url, json=payload, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == payload["username"]
        assert data["role"] == payload["role"]
        
    def test_get_users(self):
        """Test getting list of users"""
        response = requests.get(self.users_url, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert "total_count" in data
        
    def test_user_filtering(self):
        """Test user filtering"""
        params = {
            "role": "INVESTOR",
            "is_active": True,
            "page": 1,
            "page_size": 10
        }
        
        response = requests.get(self.users_url, params=params, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all returned users match filter criteria
        for user in data["users"]:
            assert user["role"] == "INVESTOR"
            assert user["is_active"] == True
            
    def test_update_user(self):
        """Test user update"""
        user_id = "test-user-id"
        payload = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@example.com"
        }
        
        response = requests.put(f"{self.users_url}/{user_id}", json=payload, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == payload["first_name"]
        
    def test_user_statistics(self):
        """Test user statistics"""
        response = requests.get(f"{self.users_url}/stats/overview", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "active_users" in data
        assert "users_by_role" in data
```

---

## 🎯 **STRATEGY MARKETPLACE TESTING**

### **Test Strategy Operations**
```python
# test_strategies.py
import pytest
import requests
from test_config import TestConfig

class TestStrategyMarketplace:
    def setup_method(self):
        self.base_url = TestConfig.BASE_URL
        self.strategies_url = f"{self.base_url}/api/v1/strategies"
        self.access_token = self._get_access_token()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        
    def _get_access_token(self):
        """Helper method to get access token"""
        login_payload = {
            "username": TestConfig.TEST_USERNAME,
            "password": TestConfig.TEST_PASSWORD
        }
        response = requests.post(f"{self.base_url}/api/v1/auth/login", json=login_payload)
        return response.json()["data"]["access_token"]
        
    def test_create_strategy(self):
        """Test strategy creation"""
        payload = {
            "name": "Test Momentum Strategy",
            "description": "A test momentum strategy for automated testing",
            "strategy_type": "momentum",
            "parameters": {
                "lookback_period": 20,
                "threshold": 0.02,
                "stop_loss": 0.05
            },
            "risk_level": 7,
            "expected_return": 25.0,
            "max_drawdown": 15.0,
            "min_capital": 10000.0,
            "tags": ["test", "momentum"],
            "is_public": True,
            "price": 99.99
        }
        
        response = requests.post(self.strategies_url, json=payload, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["strategy_type"] == payload["strategy_type"]
        
    def test_get_strategies(self):
        """Test getting list of strategies"""
        response = requests.get(self.strategies_url, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "strategies" in data
        assert "total_count" in data
        
    def test_strategy_filtering(self):
        """Test strategy filtering"""
        params = {
            "strategy_type": "momentum",
            "risk_level": 7,
            "min_return": 20.0,
            "sort_by": "expected_return",
            "sort_order": "desc"
        }
        
        response = requests.get(self.strategies_url, params=params, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all returned strategies match filter criteria
        for strategy in data["strategies"]:
            assert strategy["strategy_type"] == "momentum"
            assert strategy["risk_level"] == 7
            assert strategy["expected_return"] >= 20.0
            
    def test_get_strategy_by_id(self):
        """Test getting strategy by ID"""
        strategy_id = TestConfig.TEST_STRATEGY_ID
        response = requests.get(f"{self.strategies_url}/{strategy_id}", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["strategy_id"] == strategy_id
        
    def test_strategy_statistics(self):
        """Test strategy statistics"""
        response = requests.get(f"{self.strategies_url}/stats/overview", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_strategies" in data
        assert "strategies_by_type" in data
        assert "average_rating" in data
```

---

## 💼 **INVESTOR PORTAL TESTING**

### **Test Investor Operations**
```python
# test_investor.py
import pytest
import requests
from test_config import TestConfig

class TestInvestorPortal:
    def setup_method(self):
        self.base_url = TestConfig.BASE_URL
        self.investor_url = f"{self.base_url}/api/v1/investor"
        self.access_token = self._get_access_token()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        
    def _get_access_token(self):
        """Helper method to get access token"""
        login_payload = {
            "username": TestConfig.TEST_USERNAME,
            "password": TestConfig.TEST_PASSWORD
        }
        response = requests.post(f"{self.base_url}/api/v1/auth/login", json=login_payload)
        return response.json()["data"]["access_token"]
        
    def test_get_dashboard(self):
        """Test getting investor dashboard"""
        response = requests.get(f"{self.investor_url}/dashboard", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "investor_id" in data
        assert "total_investments" in data
        assert "current_portfolio_value" in data
        
    def test_make_investment(self):
        """Test making investment"""
        payload = {
            "fund_id": TestConfig.TEST_FUND_ID,
            "amount": 10000.0,
            "investment_type": "lump_sum",
            "notes": "Test investment"
        }
        
        response = requests.post(f"{self.investor_url}/invest", json=payload, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == payload["amount"]
        assert data["fund_id"] == payload["fund_id"]
        
    def test_make_withdrawal(self):
        """Test making withdrawal"""
        payload = {
            "fund_id": TestConfig.TEST_FUND_ID,
            "amount": 2000.0,
            "withdrawal_type": "partial",
            "notes": "Test withdrawal"
        }
        
        response = requests.post(f"{self.investor_url}/withdraw", json=payload, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == payload["amount"]
        assert data["transaction_type"] == "withdrawal"
        
    def test_get_portfolio_summary(self):
        """Test getting portfolio summary"""
        response = requests.get(f"{self.investor_url}/portfolio/summary", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_value" in data
        assert "total_invested" in data
        assert "asset_allocation" in data
        
    def test_get_transaction_history(self):
        """Test getting transaction history"""
        response = requests.get(f"{self.investor_url}/transactions", headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "transactions" in data
        assert "total_count" in data
```

---

## 🚀 **PERFORMANCE TESTING**

### **Load Testing with Artillery**
```yaml
# artillery-config.yml
config:
  target: 'https://api.neozork.com'
  phases:
    - duration: 60
      arrivalRate: 10
    - duration: 120
      arrivalRate: 20
    - duration: 60
      arrivalRate: 10
  defaults:
    headers:
      Authorization: 'Bearer {{ $processEnvironment.NEOZORK_API_KEY }}'

scenarios:
  - name: "API Load Test"
    weight: 100
    flow:
      - get:
          url: "/api/v1/funds/"
      - think: 1
      - get:
          url: "/api/v1/portfolio/{{ $processEnvironment.TEST_FUND_ID }}/positions"
      - think: 2
      - get:
          url: "/api/v1/investor/dashboard"
```

### **Run Performance Test**
```bash
# Install Artillery
npm install -g artillery

# Run load test
artillery run artillery-config.yml

# Run with custom config
artillery run artillery-config.yml --config config.json
```

### **Performance Test Results**
```bash
# Expected output
All VUs finished
Summary report @ 10:30:45(+0000) 2025-09-08
  Scenarios launched:  3000
  Scenarios completed: 3000
  Requests completed:  9000
  Mean response/sec:   150
  Response time (msec):
    min: 45
    max: 1200
    median: 180
    p95: 350
    p99: 500
  Scenario counts:
    API Load Test: 3000 (100%)
  Codes:
    200: 9000
```

---

## 🔒 **SECURITY TESTING**

### **OWASP ZAP Security Testing**
```bash
# Install OWASP ZAP
docker pull owasp/zap2docker-stable

# Run security scan
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://api.neozork.com \
  -J zap-report.json \
  -x zap-report.xml
```

### **Security Test Cases**
```python
# test_security.py
import pytest
import requests
from test_config import TestConfig

class TestSecurity:
    def setup_method(self):
        self.base_url = TestConfig.BASE_URL
        
    def test_sql_injection_protection(self):
        """Test SQL injection protection"""
        malicious_payload = {
            "username": "admin'; DROP TABLE users; --",
            "password": "password"
        }
        
        response = requests.post(f"{self.base_url}/api/v1/auth/login", json=malicious_payload)
        
        # Should not return 500 error (SQL error)
        assert response.status_code != 500
        
    def test_xss_protection(self):
        """Test XSS protection"""
        malicious_payload = {
            "name": "<script>alert('XSS')</script>",
            "description": "Test fund"
        }
        
        # This should be sanitized
        response = requests.post(f"{self.base_url}/api/v1/funds/", json=malicious_payload)
        
        # Should not execute script
        assert "<script>" not in response.text
        
    def test_rate_limiting(self):
        """Test rate limiting"""
        headers = {"Authorization": f"Bearer {TestConfig.API_KEY}"}
        
        # Make many requests quickly
        for i in range(110):  # Exceed rate limit
            response = requests.get(f"{self.base_url}/api/v1/funds/", headers=headers)
            
            if i >= 100:  # After rate limit
                assert response.status_code == 429  # Too Many Requests
                
    def test_authentication_bypass(self):
        """Test authentication bypass attempts"""
        # Test without token
        response = requests.get(f"{self.base_url}/api/v1/funds/")
        assert response.status_code == 401
        
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = requests.get(f"{self.base_url}/api/v1/funds/", headers=headers)
        assert response.status_code == 401
        
        # Test with malformed token
        headers = {"Authorization": "InvalidFormat token"}
        response = requests.get(f"{self.base_url}/api/v1/funds/", headers=headers)
        assert response.status_code == 401
```

---

## 📊 **TEST REPORTING**

### **Generate Test Reports**
```bash
# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run tests with JUnit XML output
pytest --junitxml=test-results.xml

# Run tests with HTML report
pytest --html=test-report.html --self-contained-html
```

### **Test Report Example**
```html
<!-- test-report.html -->
<!DOCTYPE html>
<html>
<head>
    <title>NeoZork API Test Report</title>
</head>
<body>
    <h1>Test Results Summary</h1>
    <table>
        <tr>
            <th>Test Suite</th>
            <th>Tests</th>
            <th>Passed</th>
            <th>Failed</th>
            <th>Coverage</th>
        </tr>
        <tr>
            <td>Authentication</td>
            <td>5</td>
            <td>5</td>
            <td>0</td>
            <td>95%</td>
        </tr>
        <tr>
            <td>Fund Management</td>
            <td>6</td>
            <td>6</td>
            <td>0</td>
            <td>92%</td>
        </tr>
        <tr>
            <td>Portfolio</td>
            <td>6</td>
            <td>6</td>
            <td>0</td>
            <td>88%</td>
        </tr>
        <tr>
            <td>User Management</td>
            <td>5</td>
            <td>5</td>
            <td>0</td>
            <td>90%</td>
        </tr>
        <tr>
            <td>Strategy Marketplace</td>
            <td>5</td>
            <td>5</td>
            <td>0</td>
            <td>85%</td>
        </tr>
        <tr>
            <td>Investor Portal</td>
            <td>5</td>
            <td>5</td>
            <td>0</td>
            <td>87%</td>
        </tr>
        <tr>
            <td><strong>Total</strong></td>
            <td><strong>32</strong></td>
            <td><strong>32</strong></td>
            <td><strong>0</strong></td>
            <td><strong>89%</strong></td>
        </tr>
    </table>
</body>
</html>
```

---

## 🔄 **CI/CD INTEGRATION**

### **GitHub Actions Workflow**
```yaml
# .github/workflows/api-tests.yml
name: API Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run tests
      env:
        NEOZORK_API_KEY: ${{ secrets.NEOZORK_API_KEY }}
        NEOZORK_BASE_URL: ${{ secrets.NEOZORK_BASE_URL }}
      run: |
        pytest --cov=src --cov-report=xml --junitxml=test-results.xml
        
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
        
    - name: Upload test results
      uses: actions/upload-artifact@v2
      with:
        name: test-results
        path: test-results.xml
```

### **Jenkins Pipeline**
```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        NEOZORK_API_KEY = credentials('neozork-api-key')
        NEOZORK_BASE_URL = 'https://api.neozork.com'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'pytest --cov=src --cov-report=html --junitxml=test-results.xml'
            }
        }
        
        stage('Publish Results') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'htmlcov',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report'
                ])
                
                junit 'test-results.xml'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'test-results.xml', fingerprint: true
        }
    }
}
```

---

## 📋 **TEST CHECKLIST**

### **Pre-Release Testing Checklist**
- [ ] **Authentication Tests**
  - [ ] User registration
  - [ ] User login
  - [ ] Token refresh
  - [ ] Token expiration
  - [ ] Invalid credentials
  
- [ ] **Fund Management Tests**
  - [ ] Create fund
  - [ ] Get funds list
  - [ ] Get fund by ID
  - [ ] Fund filtering
  - [ ] Fund performance
  - [ ] Fund investors
  
- [ ] **Portfolio Tests**
  - [ ] Get positions
  - [ ] Add position
  - [ ] Update prices
  - [ ] Portfolio metrics
  - [ ] Rebalancing
  - [ ] Transaction history
  
- [ ] **User Management Tests**
  - [ ] Create user
  - [ ] Get users
  - [ ] Update user
  - [ ] User filtering
  - [ ] User statistics
  
- [ ] **Strategy Marketplace Tests**
  - [ ] Create strategy
  - [ ] Get strategies
  - [ ] Strategy filtering
  - [ ] Strategy statistics
  
- [ ] **Investor Portal Tests**
  - [ ] Dashboard
  - [ ] Make investment
  - [ ] Make withdrawal
  - [ ] Portfolio summary
  - [ ] Transaction history
  
- [ ] **Security Tests**
  - [ ] SQL injection protection
  - [ ] XSS protection
  - [ ] Rate limiting
  - [ ] Authentication bypass
  
- [ ] **Performance Tests**
  - [ ] Load testing
  - [ ] Response time
  - [ ] Throughput
  - [ ] Resource usage

---

**Last Updated**: September 8, 2025  
**Testing Guide Version**: v1.0  
**Status**: 🚀 **Production Ready**
