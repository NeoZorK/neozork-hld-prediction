# 🏦 Pocket Hedge Fund API Documentation

## 🎯 **API Overview**

The Pocket Hedge Fund API provides comprehensive RESTful endpoints for fund management, investor operations, and portfolio tracking. The API is **100% functional** with complete database integration and authentication.

**Base URL**: `http://localhost:8080/api/v1`
**Authentication**: JWT Bearer Token
**Content-Type**: `application/json`

---

## 🔐 **Authentication**

### **Register User**
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### **Login User**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "username"
  }
}
```

---

## 🏦 **Fund Management API**

### **Create Fund**
```http
POST /api/v1/funds/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My Investment Fund",
  "description": "AI-powered investment fund",
  "fund_type": "mini",
  "initial_capital": 100000.0,
  "management_fee": 0.02,
  "performance_fee": 0.20,
  "min_investment": 1000.0,
  "max_investment": 10000.0,
  "max_investors": 100,
  "risk_level": "medium"
}
```

**Response:**
```json
{
  "fund_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "My Investment Fund",
  "description": "AI-powered investment fund",
  "fund_type": "mini",
  "initial_capital": 100000.0,
  "current_value": 100000.0,
  "management_fee": 0.02,
  "performance_fee": 0.20,
  "min_investment": 1000.0,
  "max_investment": 10000.0,
  "max_investors": 100,
  "current_investors": 0,
  "status": "active",
  "risk_level": "medium",
  "created_by": "admin",
  "created_at": "2025-01-05T10:00:00Z",
  "updated_at": "2025-01-05T10:00:00Z"
}
```

### **List Funds**
```http
GET /api/v1/funds/?fund_type=mini&status=active&page=1&page_size=20
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "fund_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Investment Fund",
    "fund_type": "mini",
    "current_value": 105000.0,
    "current_investors": 5,
    "status": "active",
    "risk_level": "medium",
    "created_by": "admin",
    "created_at": "2025-01-05T10:00:00Z"
  }
]
```

### **Get Fund Details**
```http
GET /api/v1/funds/{fund_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "fund": {
    "fund_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Investment Fund",
    "description": "AI-powered investment fund",
    "fund_type": "mini",
    "initial_capital": 100000.0,
    "current_value": 105000.0,
    "management_fee": 0.02,
    "performance_fee": 0.20,
    "min_investment": 1000.0,
    "max_investment": 10000.0,
    "max_investors": 100,
    "current_investors": 5,
    "status": "active",
    "risk_level": "medium",
    "created_by": "admin",
    "created_at": "2025-01-05T10:00:00Z",
    "updated_at": "2025-01-05T10:00:00Z"
  },
  "performance": {
    "total_return": 5000.0,
    "total_return_percentage": 5.0,
    "daily_return": 100.0,
    "daily_return_percentage": 0.1,
    "sharpe_ratio": 1.2,
    "max_drawdown": -2.5,
    "volatility": 12.5,
    "snapshot_date": "2025-01-05T00:00:00Z"
  },
  "risk_metrics": {
    "var_95": -1500.0,
    "var_99": -2500.0,
    "cvar_95": -1800.0,
    "cvar_99": -3000.0,
    "beta": 0.85,
    "correlation_spy": 0.75,
    "tracking_error": 8.5,
    "information_ratio": 0.15,
    "calculation_date": "2025-01-05T00:00:00Z"
  },
  "portfolio": [
    {
      "asset_symbol": "AAPL",
      "asset_name": "Apple Inc.",
      "asset_type": "stock",
      "quantity": 100.0,
      "average_price": 150.0,
      "current_price": 155.0,
      "current_value": 15500.0,
      "unrealized_pnl": 500.0,
      "unrealized_pnl_percentage": 3.33,
      "weight_percentage": 14.76
    }
  ],
  "strategies": [
    {
      "strategy_id": "strategy-uuid",
      "name": "Momentum Strategy",
      "description": "AI-powered momentum trading",
      "strategy_type": "momentum",
      "allocation_percentage": 60.0,
      "parameters": {
        "lookback_period": 20,
        "threshold": 0.02
      },
      "is_active": true
    }
  ]
}
```

### **Get Fund Performance**
```http
GET /api/v1/funds/{fund_id}/performance?days=30
Authorization: Bearer <token>
```

**Response:**
```json
{
  "fund_id": "550e8400-e29b-41d4-a716-446655440000",
  "period_days": 30,
  "performance_history": [
    {
      "date": "2025-01-05T00:00:00Z",
      "total_value": 105000.0,
      "total_return": 5000.0,
      "total_return_percentage": 5.0,
      "daily_return": 100.0,
      "daily_return_percentage": 0.1,
      "sharpe_ratio": 1.2,
      "max_drawdown": -2.5,
      "volatility": 12.5
    }
  ],
  "total_records": 30
}
```

### **Get Fund Investors**
```http
GET /api/v1/funds/{fund_id}/investors?page=1&page_size=20
Authorization: Bearer <token>
```

**Response:**
```json
{
  "fund_id": "550e8400-e29b-41d4-a716-446655440000",
  "investors": [
    {
      "investor_id": "investor-uuid",
      "user_id": "user-uuid",
      "username": "investor1",
      "email": "investor1@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "investment_amount": 5000.0,
      "shares_owned": 50.0,
      "current_value": 5250.0,
      "total_return": 250.0,
      "total_return_percentage": 5.0,
      "investment_date": "2025-01-01T00:00:00Z",
      "status": "active"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total_investors": 5
}
```

---

## 📊 **Portfolio Management API**

### **Get Portfolio Positions**
```http
GET /api/v1/portfolio/{fund_id}/positions
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "asset_symbol": "AAPL",
    "asset_name": "Apple Inc.",
    "asset_type": "stock",
    "quantity": 100.0,
    "average_price": 150.0,
    "current_price": 155.0,
    "current_value": 15500.0,
    "unrealized_pnl": 500.0,
    "unrealized_pnl_percentage": 3.33,
    "weight_percentage": 14.76
  }
]
```

### **Add Portfolio Position**
```http
POST /api/v1/portfolio/{fund_id}/positions
Authorization: Bearer <token>
Content-Type: application/json

{
  "asset_symbol": "MSFT",
  "asset_name": "Microsoft Corporation",
  "asset_type": "stock",
  "quantity": 50.0,
  "average_price": 300.0
}
```

### **Update Portfolio Prices**
```http
PUT /api/v1/portfolio/{fund_id}/prices
Authorization: Bearer <token>
Content-Type: application/json

{
  "prices": {
    "AAPL": 160.0,
    "MSFT": 310.0
  }
}
```

---

## 📈 **Performance & Analytics API**

### **Get Performance Metrics**
```http
GET /api/v1/returns/{fund_id}/metrics
Authorization: Bearer <token>
```

**Response:**
```json
{
  "fund_id": "550e8400-e29b-41d4-a716-446655440000",
  "metrics": {
    "total_return": 5000.0,
    "total_return_percentage": 5.0,
    "annualized_return": 18.25,
    "sharpe_ratio": 1.2,
    "sortino_ratio": 1.8,
    "calmar_ratio": 2.0,
    "max_drawdown": -2.5,
    "volatility": 12.5,
    "var_95": -1500.0,
    "cvar_95": -1800.0,
    "beta": 0.85,
    "alpha": 0.05,
    "information_ratio": 0.15
  },
  "calculation_date": "2025-01-05T00:00:00Z"
}
```

### **Get Risk Metrics**
```http
GET /api/v1/risk/{fund_id}/metrics
Authorization: Bearer <token>
```

**Response:**
```json
{
  "fund_id": "550e8400-e29b-41d4-a716-446655440000",
  "risk_metrics": {
    "var_95": -1500.0,
    "var_99": -2500.0,
    "cvar_95": -1800.0,
    "cvar_99": -3000.0,
    "beta": 0.85,
    "correlation_spy": 0.75,
    "tracking_error": 8.5,
    "information_ratio": 0.15,
    "max_drawdown": -2.5,
    "volatility": 12.5
  },
  "calculation_date": "2025-01-05T00:00:00Z"
}
```

---

## 🔧 **System API**

### **Health Check**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-05T00:00:00Z",
  "version": "1.0.0",
  "database": "connected",
  "authentication": "ready"
}
```

### **API Status**
```http
GET /api/v1/status
Authorization: Bearer <token>
```

**Response:**
```json
{
  "api_version": "1.0.0",
  "status": "operational",
  "uptime": 86400,
  "database_status": "connected",
  "redis_status": "connected",
  "active_connections": 15,
  "total_requests": 1000,
  "error_rate": 0.01
}
```

---

## 📝 **Error Handling**

### **Error Response Format**
```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "details": {
    "field": "specific field error"
  },
  "timestamp": "2025-01-05T00:00:00Z",
  "request_id": "req-uuid"
}
```

### **Common Error Codes**
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Invalid or missing authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

---

## 🚀 **Quick Start Examples**

### **Python Example**
```python
import requests

# Login
response = requests.post('http://localhost:8080/api/v1/auth/login', json={
    'email': 'user@example.com',
    'password': 'password123'
})
token = response.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Create fund
fund_data = {
    'name': 'My Fund',
    'fund_type': 'mini',
    'initial_capital': 100000,
    'min_investment': 1000
}
response = requests.post('http://localhost:8080/api/v1/funds/', 
                        json=fund_data, headers=headers)
fund = response.json()

# Get fund details
response = requests.get(f'http://localhost:8080/api/v1/funds/{fund["fund_id"]}', 
                       headers=headers)
fund_details = response.json()
```

### **cURL Examples**
```bash
# Login
curl -X POST "http://localhost:8080/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Create fund
curl -X POST "http://localhost:8080/api/v1/funds/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Fund", "fund_type": "mini", "initial_capital": 100000}'

# List funds
curl -X GET "http://localhost:8080/api/v1/funds/" \
  -H "Authorization: Bearer <token>"
```

---

## 📚 **Additional Resources**

- **OpenAPI Documentation**: http://localhost:8080/docs
- **ReDoc Documentation**: http://localhost:8080/redoc
- **Database Schema**: [Database Documentation](database/)
- **Authentication Guide**: [Authentication Documentation](auth/)
- **Deployment Guide**: [Deployment Documentation](deployment/)

---

**Last Updated**: January 2025  
**API Version**: 1.0.0  
**Status**: 100% Functional  
**Authentication**: JWT Bearer Token
