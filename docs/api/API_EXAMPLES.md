# 🚀 NeoZork Pocket Hedge Fund - API Examples

## 📊 **OVERVIEW**

This document provides practical examples for using the NeoZork Pocket Hedge Fund APIs. All examples include request/response samples, error handling, and best practices.

---

## 🔐 **AUTHENTICATION EXAMPLES**

### **User Registration**
```bash
curl -X POST "https://api.neozork.com/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_trader",
    "email": "alice@example.com",
    "password": "SecurePass123!",
    "first_name": "Alice",
    "last_name": "Johnson",
    "role": "TRADER",
    "phone": "+1234567890",
    "country": "United States",
    "timezone": "America/New_York"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "username": "alice_trader",
    "email": "alice@example.com",
    "role": "TRADER",
    "created_at": "2025-09-08T10:00:00Z"
  }
}
```

### **User Login**
```bash
curl -X POST "https://api.neozork.com/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_trader",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 900,
    "user": {
      "user_id": "123e4567-e89b-12d3-a456-426614174000",
      "username": "alice_trader",
      "email": "alice@example.com",
      "role": "TRADER"
    }
  }
}
```

### **Token Refresh**
```bash
curl -X POST "https://api.neozork.com/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

---

## 💰 **FUND MANAGEMENT EXAMPLES**

### **Create a New Fund**
```bash
curl -X POST "https://api.neozork.com/api/v1/funds/" \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Growth Fund",
    "description": "A technology-focused growth fund targeting innovative companies",
    "strategy": "growth",
    "risk_level": 8,
    "target_return": 20.0,
    "min_investment": 5000.0,
    "management_fee": 1.5,
    "performance_fee": 15.0
  }'
```

### **Get All Funds with Filtering**
```bash
curl -X GET "https://api.neozork.com/api/v1/funds/?strategy=growth&risk_level=8&page=1&page_size=10" \
  -H "Authorization: Bearer <access-token>"
```

### **Get Fund Performance History**
```bash
curl -X GET "https://api.neozork.com/api/v1/funds/456e7890-e89b-12d3-a456-426614174001/performance?days=90" \
  -H "Authorization: Bearer <access-token>"
```

---

## 📊 **PORTFOLIO MANAGEMENT EXAMPLES**

### **Get Portfolio Positions**
```bash
curl -X GET "https://api.neozork.com/api/v1/portfolio/456e7890-e89b-12d3-a456-426614174001/positions" \
  -H "Authorization: Bearer <access-token>"
```

### **Add New Position**
```bash
curl -X POST "https://api.neozork.com/api/v1/portfolio/456e7890-e89b-12d3-a456-426614174001/positions" \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_symbol": "AAPL",
    "asset_name": "Apple Inc.",
    "asset_type": "stock",
    "quantity": 100,
    "price": 150.0
  }'
```

### **Update Position Prices**
```bash
curl -X PUT "https://api.neozork.com/api/v1/portfolio/456e7890-e89b-12d3-a456-426614174001/prices" \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "price_updates": {
      "AAPL": 155.0,
      "GOOGL": 2800.0,
      "TSLA": 800.0
    }
  }'
```

### **Rebalance Portfolio**
```bash
curl -X POST "https://api.neozork.com/api/v1/portfolio/456e7890-e89b-12d3-a456-426614174001/rebalance" \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "target_weights": {
      "AAPL": 30.0,
      "GOOGL": 25.0,
      "TSLA": 20.0,
      "MSFT": 15.0,
      "NVDA": 10.0
    }
  }'
```

### **Get Portfolio Metrics**
```bash
curl -X GET "https://api.neozork.com/api/v1/portfolio/456e7890-e89b-12d3-a456-426614174001/metrics" \
  -H "Authorization: Bearer <access-token>"
```

---

## 👥 **USER MANAGEMENT EXAMPLES**

### **Create New User (Admin Only)**
```bash
curl -X POST "https://api.neozork.com/api/v1/users/" \
  -H "Authorization: Bearer <admin-access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "bob_analyst",
    "email": "bob@example.com",
    "password": "SecurePass123!",
    "first_name": "Bob",
    "last_name": "Smith",
    "role": "ANALYST",
    "phone": "+1234567891",
    "country": "Canada",
    "timezone": "America/Toronto"
  }'
```

### **Get Users with Search and Filtering**
```bash
curl -X GET "https://api.neozork.com/api/v1/users/?role=TRADER&is_active=true&search=bob&page=1&page_size=20" \
  -H "Authorization: Bearer <admin-access-token>"
```

### **Update User Information**
```bash
curl -X PUT "https://api.neozork.com/api/v1/users/987e6543-e89b-12d3-a456-426614174004" \
  -H "Authorization: Bearer <admin-access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Robert",
    "last_name": "Smith-Wilson",
    "email": "robert.wilson@example.com",
    "country": "United States",
    "timezone": "America/Los_Angeles"
  }'
```

### **Assign Role to User**
```bash
curl -X POST "https://api.neozork.com/api/v1/users/987e6543-e89b-12d3-a456-426614174004/assign-role" \
  -H "Authorization: Bearer <admin-access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "987e6543-e89b-12d3-a456-426614174004",
    "role": "MANAGER"
  }'
```

### **Get User Statistics**
```bash
curl -X GET "https://api.neozork.com/api/v1/users/stats/overview" \
  -H "Authorization: Bearer <admin-access-token>"
```

---

## 🎯 **STRATEGY MARKETPLACE EXAMPLES**

### **Create Trading Strategy**
```bash
curl -X POST "https://api.neozork.com/api/v1/strategies/" \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mean Reversion Strategy",
    "description": "A mean reversion strategy that profits from price corrections",
    "strategy_type": "mean_reversion",
    "parameters": {
      "lookback_period": 14,
      "deviation_threshold": 2.0,
      "reversion_factor": 0.5,
      "stop_loss": 0.03,
      "take_profit": 0.06
    },
    "risk_level": 5,
    "expected_return": 18.0,
    "max_drawdown": 12.0,
    "min_capital": 5000.0,
    "tags": ["mean-reversion", "low-risk", "stable"],
    "is_public": true,
    "price": 49.99
  }'
```

### **Search Strategies with Advanced Filtering**
```bash
curl -X GET "https://api.neozork.com/api/v1/strategies/?strategy_type=momentum&risk_level=7&min_return=20&tags=trend,high-risk&sort_by=expected_return&sort_order=desc&page=1&page_size=10" \
  -H "Authorization: Bearer <access-token>"
```

### **Get Strategy Details**
```bash
curl -X GET "https://api.neozork.com/api/v1/strategies/def45678-e89b-12d3-a456-426614174005" \
  -H "Authorization: Bearer <access-token>"
```

### **Get Marketplace Statistics**
```bash
curl -X GET "https://api.neozork.com/api/v1/strategies/stats/overview" \
  -H "Authorization: Bearer <access-token>"
```

---

## 💼 **INVESTOR PORTAL EXAMPLES**

### **Get Investor Dashboard**
```bash
curl -X GET "https://api.neozork.com/api/v1/investor/dashboard" \
  -H "Authorization: Bearer <access-token>"
```

### **Make Investment**
```bash
curl -X POST "https://api.neozork.com/api/v1/investor/invest" \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "fund_id": "456e7890-e89b-12d3-a456-426614174001",
    "amount": 25000.0,
    "investment_type": "lump_sum",
    "notes": "Initial investment in tech growth fund"
  }'
```

### **Make Withdrawal**
```bash
curl -X POST "https://api.neozork.com/api/v1/investor/withdraw" \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "fund_id": "456e7890-e89b-12d3-a456-426614174001",
    "amount": 5000.0,
    "withdrawal_type": "partial",
    "notes": "Partial withdrawal for personal expenses"
  }'
```

### **Get Portfolio Summary**
```bash
curl -X GET "https://api.neozork.com/api/v1/investor/portfolio/summary" \
  -H "Authorization: Bearer <access-token>"
```

### **Get Transaction History with Filtering**
```bash
curl -X GET "https://api.neozork.com/api/v1/investor/transactions?transaction_type=investment&page=1&page_size=20" \
  -H "Authorization: Bearer <access-token>"
```

---

## 🐍 **PYTHON SDK EXAMPLES**

### **Installation**
```bash
pip install neozork-sdk
```

### **Basic Usage**
```python
from neozork import NeoZorkClient

# Initialize client
client = NeoZorkClient(
    api_key="your-api-key",
    base_url="https://api.neozork.com"
)

# Authenticate
auth_response = client.auth.login(
    username="alice_trader",
    password="SecurePass123!"
)

# Store token for future requests
client.set_token(auth_response['access_token'])

# Get funds
funds = client.funds.list(
    strategy="growth",
    risk_level=8,
    page=1,
    page_size=10
)

print(f"Found {len(funds['funds'])} funds")

# Create investment
investment = client.investor.invest(
    fund_id="456e7890-e89b-12d3-a456-426614174001",
    amount=10000.0,
    investment_type="lump_sum",
    notes="Python SDK investment"
)

print(f"Investment created: {investment['investment_id']}")

# Get portfolio summary
portfolio = client.investor.get_portfolio_summary()
print(f"Portfolio value: ${portfolio['total_value']:,.2f}")
print(f"Total return: {portfolio['total_return_percentage']:.2f}%")
```

### **Advanced Portfolio Management**
```python
# Get portfolio positions
positions = client.portfolio.get_positions("456e7890-e89b-12d3-a456-426614174001")

# Add new position
new_position = client.portfolio.add_position(
    fund_id="456e7890-e89b-12d3-a456-426614174001",
    asset_symbol="NVDA",
    asset_name="NVIDIA Corporation",
    asset_type="stock",
    quantity=50,
    price=400.0
)

# Update prices
price_updates = {
    "AAPL": 155.0,
    "GOOGL": 2800.0,
    "NVDA": 410.0
}

updated_positions = client.portfolio.update_prices(
    fund_id="456e7890-e89b-12d3-a456-426614174001",
    price_updates=price_updates
)

# Rebalance portfolio
rebalance_result = client.portfolio.rebalance(
    fund_id="456e7890-e89b-12d3-a456-426614174001",
    target_weights={
        "AAPL": 30.0,
        "GOOGL": 25.0,
        "NVDA": 20.0,
        "MSFT": 15.0,
        "TSLA": 10.0
    }
)

print(f"Rebalancing completed: {rebalance_result['total_trades']} trades executed")
```

### **Strategy Marketplace Integration**
```python
# Create strategy
strategy = client.strategies.create(
    name="AI Trading Strategy",
    description="Machine learning-based trading strategy",
    strategy_type="momentum",
    parameters={
        "model_type": "neural_network",
        "lookback_period": 30,
        "confidence_threshold": 0.8
    },
    risk_level=6,
    expected_return=22.0,
    max_drawdown=10.0,
    min_capital=15000.0,
    tags=["ai", "ml", "momentum"],
    is_public=True,
    price=199.99
)

# Search strategies
strategies = client.strategies.search(
    strategy_type="momentum",
    risk_level=6,
    min_return=20.0,
    tags=["ai", "ml"],
    sort_by="expected_return",
    sort_order="desc"
)

print(f"Found {len(strategies['strategies'])} AI strategies")
```

---

## 🟨 **JAVASCRIPT SDK EXAMPLES**

### **Installation**
```bash
npm install @neozork/sdk
```

### **Basic Usage**
```javascript
import { NeoZorkClient } from '@neozork/sdk';

// Initialize client
const client = new NeoZorkClient({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.neozork.com'
});

// Authenticate
const authResponse = await client.auth.login({
  username: 'alice_trader',
  password: 'SecurePass123!'
});

// Set token for future requests
client.setToken(authResponse.access_token);

// Get funds
const funds = await client.funds.list({
  strategy: 'growth',
  risk_level: 8,
  page: 1,
  page_size: 10
});

console.log(`Found ${funds.funds.length} funds`);

// Create investment
const investment = await client.investor.invest({
  fund_id: '456e7890-e89b-12d3-a456-426614174001',
  amount: 10000.0,
  investment_type: 'lump_sum',
  notes: 'JavaScript SDK investment'
});

console.log(`Investment created: ${investment.investment_id}`);

// Get portfolio summary
const portfolio = await client.investor.getPortfolioSummary();
console.log(`Portfolio value: $${portfolio.total_value.toLocaleString()}`);
console.log(`Total return: ${portfolio.total_return_percentage.toFixed(2)}%`);
```

### **React Integration Example**
```jsx
import React, { useState, useEffect } from 'react';
import { NeoZorkClient } from '@neozork/sdk';

const PortfolioDashboard = () => {
  const [client] = useState(new NeoZorkClient({
    apiKey: process.env.REACT_APP_NEOZORK_API_KEY,
    baseUrl: process.env.REACT_APP_NEOZORK_BASE_URL
  }));
  
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPortfolio = async () => {
      try {
        const portfolioData = await client.investor.getPortfolioSummary();
        setPortfolio(portfolioData);
      } catch (error) {
        console.error('Failed to fetch portfolio:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPortfolio();
  }, [client]);

  const handleInvestment = async (fundId, amount) => {
    try {
      const investment = await client.investor.invest({
        fund_id: fundId,
        amount: amount,
        investment_type: 'lump_sum'
      });
      
      console.log('Investment successful:', investment);
      // Refresh portfolio data
      const updatedPortfolio = await client.investor.getPortfolioSummary();
      setPortfolio(updatedPortfolio);
    } catch (error) {
      console.error('Investment failed:', error);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="portfolio-dashboard">
      <h2>Portfolio Summary</h2>
      <div className="metrics">
        <div className="metric">
          <label>Total Value</label>
          <span>${portfolio?.total_value?.toLocaleString()}</span>
        </div>
        <div className="metric">
          <label>Total Return</label>
          <span>{portfolio?.total_return_percentage?.toFixed(2)}%</span>
        </div>
        <div className="metric">
          <label>Total PnL</label>
          <span>${portfolio?.total_pnl?.toLocaleString()}</span>
        </div>
      </div>
      
      <div className="asset-allocation">
        <h3>Asset Allocation</h3>
        {Object.entries(portfolio?.asset_allocation || {}).map(([fund, percentage]) => (
          <div key={fund} className="allocation-item">
            <span>{fund}</span>
            <span>{percentage.toFixed(1)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PortfolioDashboard;
```

---

## 🔧 **ERROR HANDLING EXAMPLES**

### **Python Error Handling**
```python
from neozork import NeoZorkClient, NeoZorkError

client = NeoZorkClient(api_key="your-api-key")

try:
    # Attempt to make investment
    investment = client.investor.invest(
        fund_id="invalid-fund-id",
        amount=10000.0
    )
except NeoZorkError as e:
    if e.status_code == 404:
        print("Fund not found")
    elif e.status_code == 400:
        print(f"Validation error: {e.message}")
    elif e.status_code == 403:
        print("Insufficient permissions")
    else:
        print(f"Unexpected error: {e.message}")
except Exception as e:
    print(f"Network or other error: {e}")
```

### **JavaScript Error Handling**
```javascript
try {
  const investment = await client.investor.invest({
    fund_id: 'invalid-fund-id',
    amount: 10000.0
  });
} catch (error) {
  if (error.status === 404) {
    console.log('Fund not found');
  } else if (error.status === 400) {
    console.log(`Validation error: ${error.message}`);
  } else if (error.status === 403) {
    console.log('Insufficient permissions');
  } else {
    console.log(`Unexpected error: ${error.message}`);
  }
}
```

### **Common Error Scenarios**
```bash
# Invalid token
curl -X GET "https://api.neozork.com/api/v1/funds/" \
  -H "Authorization: Bearer invalid-token"

# Response:
{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Invalid or expired token"
  }
}

# Insufficient permissions
curl -X POST "https://api.neozork.com/api/v1/users/" \
  -H "Authorization: Bearer <investor-token>"

# Response:
{
  "error": {
    "code": "INSUFFICIENT_PERMISSIONS",
    "message": "Insufficient permissions to create users"
  }
}

# Validation error
curl -X POST "https://api.neozork.com/api/v1/investor/invest" \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "fund_id": "invalid-uuid",
    "amount": -1000.0
  }'

# Response:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "fund_id": "Invalid UUID format",
      "amount": "Amount must be positive"
    }
  }
}
```

---

## 📊 **BEST PRACTICES**

### **1. Token Management**
```python
# Store tokens securely
import os
from neozork import NeoZorkClient

client = NeoZorkClient(api_key=os.getenv('NEOZORK_API_KEY'))

# Refresh token before expiration
def ensure_valid_token():
    if client.is_token_expired():
        client.refresh_token()
```

### **2. Rate Limiting**
```python
import time
from neozork import NeoZorkClient, RateLimitError

client = NeoZorkClient(api_key="your-api-key")

def make_request_with_retry(func, *args, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            if attempt < max_retries - 1:
                time.sleep(e.retry_after)
            else:
                raise
```

### **3. Pagination**
```python
# Handle pagination properly
def get_all_funds():
    all_funds = []
    page = 1
    
    while True:
        response = client.funds.list(page=page, page_size=100)
        all_funds.extend(response['funds'])
        
        if page >= response['total_pages']:
            break
            
        page += 1
    
    return all_funds
```

### **4. Data Validation**
```python
# Validate data before sending
def validate_investment_data(fund_id, amount):
    if not fund_id or not isinstance(fund_id, str):
        raise ValueError("Fund ID must be a valid string")
    
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Amount must be a positive number")
    
    return True

# Use validation
if validate_investment_data(fund_id, amount):
    investment = client.investor.invest(fund_id=fund_id, amount=amount)
```

---

## 🚀 **DEPLOYMENT EXAMPLES**

### **Docker Configuration**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### **Environment Variables**
```bash
# .env file
NEOZORK_API_KEY=your-api-key
NEOZORK_BASE_URL=https://api.neozork.com
NEOZORK_ENVIRONMENT=production
```

### **Kubernetes Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neozork-client
spec:
  replicas: 3
  selector:
    matchLabels:
      app: neozork-client
  template:
    metadata:
      labels:
        app: neozork-client
    spec:
      containers:
      - name: neozork-client
        image: neozork-client:latest
        env:
        - name: NEOZORK_API_KEY
          valueFrom:
            secretKeyRef:
              name: neozork-secrets
              key: api-key
        - name: NEOZORK_BASE_URL
          value: "https://api.neozork.com"
```

---

**Last Updated**: September 8, 2025  
**Examples Version**: v1.0  
**Status**: 🚀 **Production Ready**
