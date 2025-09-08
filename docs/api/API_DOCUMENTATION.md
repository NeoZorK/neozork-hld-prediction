# 📚 NeoZork Pocket Hedge Fund - Complete API Documentation

## 📊 **OVERVIEW**

This document provides comprehensive documentation for all APIs implemented in the NeoZork Pocket Hedge Fund system. The system includes 5 major API modules with 25+ endpoints covering authentication, fund management, portfolio operations, user management, strategy marketplace, and investor portal functionality.

---

## 🔐 **AUTHENTICATION**

All API endpoints require JWT-based authentication. Include the JWT token in the Authorization header:

```http
Authorization: Bearer <your-jwt-token>
```

### **Token Types**
- **Access Token**: Short-lived token for API access (15 minutes)
- **Refresh Token**: Long-lived token for refreshing access tokens (7 days)

---

## 📋 **API MODULES**

### **1. Authentication API** (`/api/v1/auth/`)
### **2. Fund Management API** (`/api/v1/funds/`)
### **3. Portfolio API** (`/api/v1/portfolio/`)
### **4. User Management API** (`/api/v1/users/`)
### **5. Strategy Marketplace API** (`/api/v1/strategies/`)
### **6. Investor Portal API** (`/api/v1/investor/`)

---

## 🔐 **1. AUTHENTICATION API**

Base URL: `/api/v1/auth/`

### **POST /register**
Register a new user account.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "role": "INVESTOR"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "username": "john_doe",
    "email": "john@example.com",
    "role": "INVESTOR",
    "created_at": "2025-09-08T10:00:00Z"
  }
}
```

### **POST /login**
Authenticate user and get access tokens.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123!"
}
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
      "username": "john_doe",
      "email": "john@example.com",
      "role": "INVESTOR"
    }
  }
}
```

### **POST /refresh**
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 900
  }
}
```

### **POST /logout**
Logout user and blacklist tokens.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "status": "success",
  "message": "Logged out successfully"
}
```

### **GET /me**
Get current user information.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "INVESTOR",
    "is_active": true,
    "created_at": "2025-09-08T10:00:00Z"
  }
}
```

### **POST /change-password**
Change user password.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "current_password": "OldPass123!",
  "new_password": "NewPass123!"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Password changed successfully"
}
```

---

## 💰 **2. FUND MANAGEMENT API**

Base URL: `/api/v1/funds/`

### **POST /**
Create a new fund.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "name": "Growth Fund",
  "description": "A diversified growth fund focusing on technology stocks",
  "strategy": "growth",
  "risk_level": 7,
  "target_return": 15.0,
  "min_investment": 1000.0,
  "management_fee": 2.0,
  "performance_fee": 20.0
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "fund_id": "456e7890-e89b-12d3-a456-426614174001",
    "name": "Growth Fund",
    "description": "A diversified growth fund focusing on technology stocks",
    "strategy": "growth",
    "risk_level": 7,
    "target_return": 15.0,
    "min_investment": 1000.0,
    "management_fee": 2.0,
    "performance_fee": 20.0,
    "status": "active",
    "created_at": "2025-09-08T10:00:00Z"
  }
}
```

### **GET /**
Get list of funds with pagination and filtering.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Page size (default: 20, max: 100)
- `strategy` (string): Filter by strategy
- `risk_level` (int): Filter by risk level (1-10)
- `status` (string): Filter by status
- `search` (string): Search by name or description

**Response:**
```json
{
  "funds": [
    {
      "fund_id": "456e7890-e89b-12d3-a456-426614174001",
      "name": "Growth Fund",
      "description": "A diversified growth fund focusing on technology stocks",
      "strategy": "growth",
      "risk_level": 7,
      "target_return": 15.0,
      "min_investment": 1000.0,
      "management_fee": 2.0,
      "performance_fee": 20.0,
      "status": "active",
      "created_at": "2025-09-08T10:00:00Z"
    }
  ],
  "total_count": 1,
  "page": 1,
  "page_size": 20,
  "total_pages": 1
}
```

### **GET /{fund_id}**
Get fund details by ID.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "fund_id": "456e7890-e89b-12d3-a456-426614174001",
  "name": "Growth Fund",
  "description": "A diversified growth fund focusing on technology stocks",
  "strategy": "growth",
  "risk_level": 7,
  "target_return": 15.0,
  "min_investment": 1000.0,
  "management_fee": 2.0,
  "performance_fee": 20.0,
  "status": "active",
  "current_value": 1500000.0,
  "initial_capital": 1000000.0,
  "total_investors": 25,
  "created_at": "2025-09-08T10:00:00Z"
}
```

### **GET /{fund_id}/performance**
Get fund performance history.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `days` (int): Number of days (default: 30, max: 365)

**Response:**
```json
{
  "fund_id": "456e7890-e89b-12d3-a456-426614174001",
  "performance_history": [
    {
      "date": "2025-09-08",
      "total_value": 1500000.0,
      "total_return": 500000.0,
      "total_return_percentage": 50.0,
      "daily_return": 15000.0,
      "daily_return_percentage": 1.0
    }
  ],
  "total_records": 30,
  "period_days": 30
}
```

### **GET /{fund_id}/investors**
Get fund investors.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "fund_id": "456e7890-e89b-12d3-a456-426614174001",
  "investors": [
    {
      "investor_id": "123e4567-e89b-12d3-a456-426614174000",
      "username": "john_doe",
      "email": "john@example.com",
      "investment_amount": 10000.0,
      "investment_date": "2025-09-08T10:00:00Z",
      "current_value": 15000.0
    }
  ],
  "total_investors": 25,
  "total_invested": 500000.0
}
```

---

## 📊 **3. PORTFOLIO API**

Base URL: `/api/v1/portfolio/`

### **GET /{fund_id}/positions**
Get portfolio positions for a fund.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "positions": [
    {
      "position_id": "789e0123-e89b-12d3-a456-426614174002",
      "asset_symbol": "BTC",
      "asset_name": "Bitcoin",
      "asset_type": "crypto",
      "quantity": 0.5,
      "average_price": 45000.0,
      "current_price": 46000.0,
      "current_value": 23000.0,
      "unrealized_pnl": 500.0,
      "unrealized_pnl_percentage": 2.22,
      "weight_percentage": 15.33,
      "created_at": "2025-09-08T10:00:00Z",
      "updated_at": "2025-09-08T10:00:00Z"
    }
  ],
  "total_positions": 1,
  "total_value": 150000.0
}
```

### **POST /{fund_id}/positions**
Add a new position to the portfolio.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "asset_symbol": "ETH",
  "asset_name": "Ethereum",
  "asset_type": "crypto",
  "quantity": 2.0,
  "price": 3000.0
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "position_id": "789e0123-e89b-12d3-a456-426614174002",
    "asset_symbol": "ETH",
    "asset_name": "Ethereum",
    "asset_type": "crypto",
    "quantity": 2.0,
    "average_price": 3000.0,
    "current_price": 3000.0,
    "current_value": 6000.0,
    "unrealized_pnl": 0.0,
    "unrealized_pnl_percentage": 0.0,
    "weight_percentage": 4.0
  },
  "message": "Position added successfully"
}
```

### **DELETE /{fund_id}/positions/{asset_symbol}**
Remove or reduce a position from the portfolio.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `quantity` (float, optional): Quantity to remove (if None, removes entire position)

**Response:**
```json
{
  "status": "success",
  "data": {
    "position_id": "789e0123-e89b-12d3-a456-426614174002",
    "asset_symbol": "ETH",
    "quantity_removed": 1.0,
    "remaining_quantity": 1.0,
    "realized_pnl": 100.0
  },
  "message": "Position removed successfully"
}
```

### **PUT /{fund_id}/prices**
Update current prices for portfolio positions.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "price_updates": {
    "BTC": 47000.0,
    "ETH": 3100.0,
    "SOL": 105.0
  }
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_updated": 3,
    "updated_positions": [
      {
        "asset_symbol": "BTC",
        "old_price": 46000.0,
        "new_price": 47000.0,
        "unrealized_pnl": 500.0,
        "unrealized_pnl_percentage": 2.17
      }
    ]
  },
  "message": "Position prices updated successfully"
}
```

### **GET /{fund_id}/metrics**
Get portfolio performance metrics.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "fund_id": "456e7890-e89b-12d3-a456-426614174001",
  "total_value": 150000.0,
  "initial_capital": 100000.0,
  "total_pnl": 50000.0,
  "total_return_percentage": 50.0,
  "daily_return": 1500.0,
  "daily_return_percentage": 1.0,
  "risk_metrics": {
    "sharpe_ratio": 1.2,
    "max_drawdown": 0.08,
    "volatility": 0.15,
    "beta": 0.85,
    "alpha": 0.02
  },
  "calculated_at": "2025-09-08T10:00:00Z"
}
```

### **POST /{fund_id}/rebalance**
Rebalance portfolio to target weights.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "target_weights": {
    "BTC": 40.0,
    "ETH": 30.0,
    "SOL": 15.0,
    "ADA": 10.0,
    "DOT": 5.0
  }
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_trades": 3,
    "rebalancing_trades": [
      {
        "asset_symbol": "BTC",
        "current_weight": 35.0,
        "target_weight": 40.0,
        "trade_type": "buy",
        "quantity": 0.1,
        "price": 47000.0
      }
    ],
    "total_cost": 4700.0,
    "rebalancing_completed": true
  },
  "message": "Portfolio rebalancing completed successfully"
}
```

### **GET /{fund_id}/transactions**
Get portfolio transaction history.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Page size (default: 20, max: 100)
- `transaction_type` (string): Filter by transaction type

**Response:**
```json
{
  "fund_id": "456e7890-e89b-12d3-a456-426614174001",
  "transactions": [
    {
      "transaction_id": "abc12345-e89b-12d3-a456-426614174003",
      "transaction_type": "buy",
      "asset_symbol": "BTC",
      "quantity": 0.5,
      "price": 45000.0,
      "total_amount": 22500.0,
      "fees": 22.5,
      "executed_at": "2025-09-08T10:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total_transactions": 1
}
```

---

## 👥 **4. USER MANAGEMENT API**

Base URL: `/api/v1/users/`

### **POST /**
Create a new user.

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Request Body:**
```json
{
  "username": "jane_smith",
  "email": "jane@example.com",
  "password": "SecurePass123!",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "TRADER",
  "phone": "+1234567890",
  "country": "United States",
  "timezone": "America/New_York"
}
```

**Response:**
```json
{
  "user_id": "987e6543-e89b-12d3-a456-426614174004",
  "username": "jane_smith",
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "TRADER",
  "phone": "+1234567890",
  "country": "United States",
  "timezone": "America/New_York",
  "is_active": true,
  "email_verified": false,
  "created_at": "2025-09-08T10:00:00Z",
  "updated_at": "2025-09-08T10:00:00Z",
  "last_login": null
}
```

### **GET /**
Get list of users with pagination and filtering.

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Page size (default: 20, max: 100)
- `role` (string): Filter by role
- `is_active` (boolean): Filter by active status
- `search` (string): Search by username, email, or name

**Response:**
```json
{
  "users": [
    {
      "user_id": "987e6543-e89b-12d3-a456-426614174004",
      "username": "jane_smith",
      "email": "jane@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "role": "TRADER",
      "phone": "+1234567890",
      "country": "United States",
      "timezone": "America/New_York",
      "is_active": true,
      "email_verified": false,
      "created_at": "2025-09-08T10:00:00Z",
      "updated_at": "2025-09-08T10:00:00Z",
      "last_login": null
    }
  ],
  "total_count": 1,
  "page": 1,
  "page_size": 20,
  "total_pages": 1
}
```

### **GET /{user_id}**
Get user by ID.

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Response:**
```json
{
  "user_id": "987e6543-e89b-12d3-a456-426614174004",
  "username": "jane_smith",
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "TRADER",
  "phone": "+1234567890",
  "country": "United States",
  "timezone": "America/New_York",
  "is_active": true,
  "email_verified": false,
  "created_at": "2025-09-08T10:00:00Z",
  "updated_at": "2025-09-08T10:00:00Z",
  "last_login": null
}
```

### **PUT /{user_id}**
Update user information.

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith-Wilson",
  "email": "jane.wilson@example.com",
  "phone": "+1234567891",
  "country": "Canada",
  "timezone": "America/Toronto",
  "is_active": true
}
```

**Response:**
```json
{
  "user_id": "987e6543-e89b-12d3-a456-426614174004",
  "username": "jane_smith",
  "email": "jane.wilson@example.com",
  "first_name": "Jane",
  "last_name": "Smith-Wilson",
  "role": "TRADER",
  "phone": "+1234567891",
  "country": "Canada",
  "timezone": "America/Toronto",
  "is_active": true,
  "email_verified": false,
  "created_at": "2025-09-08T10:00:00Z",
  "updated_at": "2025-09-08T10:00:00Z",
  "last_login": null
}
```

### **DELETE /{user_id}**
Delete user (soft delete by setting is_active to False).

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Response:**
```json
{
  "status": "success",
  "message": "User deleted successfully",
  "user_id": "987e6543-e89b-12d3-a456-426614174004"
}
```

### **POST /{user_id}/change-password**
Change user password.

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Request Body:**
```json
{
  "current_password": "OldPass123!",
  "new_password": "NewPass123!"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Password changed successfully",
  "user_id": "987e6543-e89b-12d3-a456-426614174004"
}
```

### **POST /{user_id}/assign-role**
Assign role to user.

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Request Body:**
```json
{
  "user_id": "987e6543-e89b-12d3-a456-426614174004",
  "role": "MANAGER"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Role assigned successfully",
  "user_id": "987e6543-e89b-12d3-a456-426614174004",
  "role": "MANAGER"
}
```

### **GET /stats/overview**
Get user statistics overview.

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Response:**
```json
{
  "total_users": 150,
  "active_users": 142,
  "inactive_users": 8,
  "users_by_role": {
    "ADMIN": 2,
    "MANAGER": 5,
    "TRADER": 15,
    "ANALYST": 25,
    "INVESTOR": 103
  },
  "new_users_today": 3,
  "new_users_this_week": 12,
  "new_users_this_month": 45
}
```

---

## 🎯 **5. STRATEGY MARKETPLACE API**

Base URL: `/api/v1/strategies/`

### **POST /**
Create a new trading strategy.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "name": "Momentum Trading Strategy",
  "description": "A momentum-based trading strategy that follows market trends",
  "strategy_type": "momentum",
  "parameters": {
    "lookback_period": 20,
    "threshold": 0.02,
    "stop_loss": 0.05,
    "take_profit": 0.10
  },
  "risk_level": 7,
  "expected_return": 25.0,
  "max_drawdown": 15.0,
  "min_capital": 10000.0,
  "tags": ["momentum", "trend", "high-risk"],
  "is_public": true,
  "price": 99.99
}
```

**Response:**
```json
{
  "strategy_id": "def45678-e89b-12d3-a456-426614174005",
  "name": "Momentum Trading Strategy",
  "description": "A momentum-based trading strategy that follows market trends",
  "strategy_type": "momentum",
  "parameters": {
    "lookback_period": 20,
    "threshold": 0.02,
    "stop_loss": 0.05,
    "take_profit": 0.10
  },
  "risk_level": 7,
  "expected_return": 25.0,
  "max_drawdown": 15.0,
  "min_capital": 10000.0,
  "tags": ["momentum", "trend", "high-risk"],
  "is_public": true,
  "price": 99.99,
  "status": "draft",
  "author_id": "123e4567-e89b-12d3-a456-426614174000",
  "author_name": "john_doe",
  "created_at": "2025-09-08T10:00:00Z",
  "updated_at": "2025-09-08T10:00:00Z",
  "total_views": 0,
  "total_downloads": 0,
  "rating": 0.0,
  "total_ratings": 0
}
```

### **GET /**
Get list of strategies with pagination and filtering.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Page size (default: 20, max: 100)
- `strategy_type` (string): Filter by strategy type
- `risk_level` (int): Filter by risk level (1-10)
- `min_return` (float): Minimum expected return
- `max_drawdown` (float): Maximum drawdown
- `tags` (string): Filter by tags (comma-separated)
- `search` (string): Search by name or description
- `sort_by` (string): Sort by field (created_at, name, expected_return, risk_level, rating)
- `sort_order` (string): Sort order (asc/desc)

**Response:**
```json
{
  "strategies": [
    {
      "strategy_id": "def45678-e89b-12d3-a456-426614174005",
      "name": "Momentum Trading Strategy",
      "description": "A momentum-based trading strategy that follows market trends",
      "strategy_type": "momentum",
      "parameters": {
        "lookback_period": 20,
        "threshold": 0.02,
        "stop_loss": 0.05,
        "take_profit": 0.10
      },
      "risk_level": 7,
      "expected_return": 25.0,
      "max_drawdown": 15.0,
      "min_capital": 10000.0,
      "tags": ["momentum", "trend", "high-risk"],
      "is_public": true,
      "price": 99.99,
      "status": "published",
      "author_id": "123e4567-e89b-12d3-a456-426614174000",
      "author_name": "john_doe",
      "created_at": "2025-09-08T10:00:00Z",
      "updated_at": "2025-09-08T10:00:00Z",
      "total_views": 125,
      "total_downloads": 15,
      "rating": 4.2,
      "total_ratings": 8
    }
  ],
  "total_count": 1,
  "page": 1,
  "page_size": 20,
  "total_pages": 1
}
```

### **GET /{strategy_id}**
Get strategy by ID.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "strategy_id": "def45678-e89b-12d3-a456-426614174005",
  "name": "Momentum Trading Strategy",
  "description": "A momentum-based trading strategy that follows market trends",
  "strategy_type": "momentum",
  "parameters": {
    "lookback_period": 20,
    "threshold": 0.02,
    "stop_loss": 0.05,
    "take_profit": 0.10
  },
  "risk_level": 7,
  "expected_return": 25.0,
  "max_drawdown": 15.0,
  "min_capital": 10000.0,
  "tags": ["momentum", "trend", "high-risk"],
  "is_public": true,
  "price": 99.99,
  "status": "published",
  "author_id": "123e4567-e89b-12d3-a456-426614174000",
  "author_name": "john_doe",
  "created_at": "2025-09-08T10:00:00Z",
  "updated_at": "2025-09-08T10:00:00Z",
  "total_views": 126,
  "total_downloads": 15,
  "rating": 4.2,
  "total_ratings": 8
}
```

### **GET /stats/overview**
Get strategy marketplace statistics.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "total_strategies": 50,
  "public_strategies": 35,
  "private_strategies": 15,
  "strategies_by_type": {
    "momentum": 15,
    "mean_reversion": 10,
    "arbitrage": 5,
    "scalping": 8,
    "swing": 7,
    "trend_following": 5
  },
  "strategies_by_status": {
    "published": 35,
    "draft": 10,
    "archived": 5
  },
  "total_downloads": 1250,
  "total_views": 15000,
  "average_rating": 4.1
}
```

---

## 💼 **6. INVESTOR PORTAL API**

Base URL: `/api/v1/investor/`

### **GET /dashboard**
Get investor dashboard data.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "investor_id": "123e4567-e89b-12d3-a456-426614174000",
  "total_investments": 50000.0,
  "total_withdrawals": 5000.0,
  "net_investment": 45000.0,
  "current_portfolio_value": 52000.0,
  "total_pnl": 7000.0,
  "total_return_percentage": 15.56,
  "active_investments": 3,
  "funds_invested": [
    {
      "fund_id": "456e7890-e89b-12d3-a456-426614174001",
      "fund_name": "Growth Fund",
      "invested_amount": 20000.0,
      "current_value": 23000.0,
      "pnl": 3000.0,
      "return_percentage": 15.0
    }
  ],
  "recent_transactions": [
    {
      "transaction_id": "ghi78901-e89b-12d3-a456-426614174006",
      "transaction_type": "investment",
      "fund_id": "456e7890-e89b-12d3-a456-426614174001",
      "fund_name": "Growth Fund",
      "amount": 10000.0,
      "status": "completed",
      "created_at": "2025-09-08T10:00:00Z",
      "notes": "Additional investment"
    }
  ],
  "performance_summary": {
    "total_return": 7000.0,
    "total_return_percentage": 15.56,
    "best_performing_fund": "Growth Fund",
    "worst_performing_fund": "Value Fund",
    "average_return": 12.5
  },
  "risk_metrics": {
    "portfolio_volatility": 0.15,
    "max_drawdown": 0.08,
    "sharpe_ratio": 1.2,
    "beta": 0.85
  }
}
```

### **POST /invest**
Make an investment in a fund.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "fund_id": "456e7890-e89b-12d3-a456-426614174001",
  "amount": 10000.0,
  "investment_type": "lump_sum",
  "notes": "Initial investment in growth fund"
}
```

**Response:**
```json
{
  "investment_id": "jkl01234-e89b-12d3-a456-426614174007",
  "fund_id": "456e7890-e89b-12d3-a456-426614174001",
  "fund_name": "Growth Fund",
  "amount": 10000.0,
  "investment_type": "lump_sum",
  "status": "pending",
  "created_at": "2025-09-08T10:00:00Z",
  "notes": "Initial investment in growth fund"
}
```

### **POST /withdraw**
Make a withdrawal from a fund.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "fund_id": "456e7890-e89b-12d3-a456-426614174001",
  "amount": 2000.0,
  "withdrawal_type": "partial",
  "notes": "Emergency withdrawal"
}
```

**Response:**
```json
{
  "transaction_id": "mno34567-e89b-12d3-a456-426614174008",
  "transaction_type": "withdrawal",
  "fund_id": "456e7890-e89b-12d3-a456-426614174001",
  "fund_name": "Growth Fund",
  "amount": 2000.0,
  "status": "pending",
  "created_at": "2025-09-08T10:00:00Z",
  "notes": "Emergency withdrawal"
}
```

### **GET /portfolio/summary**
Get portfolio summary for the investor.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "total_value": 52000.0,
  "total_invested": 45000.0,
  "total_pnl": 7000.0,
  "total_return_percentage": 15.56,
  "daily_change": 520.0,
  "daily_change_percentage": 1.01,
  "asset_allocation": {
    "Growth Fund": 60.0,
    "Value Fund": 25.0,
    "Tech Fund": 15.0
  },
  "performance_metrics": {
    "sharpe_ratio": 1.2,
    "max_drawdown": 0.08,
    "volatility": 0.15,
    "beta": 0.85,
    "alpha": 0.02
  }
}
```

### **GET /transactions**
Get transaction history for the investor.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Page size (default: 20, max: 100)
- `transaction_type` (string): Filter by transaction type
- `fund_id` (string): Filter by fund ID

**Response:**
```json
{
  "transactions": [
    {
      "transaction_id": "jkl01234-e89b-12d3-a456-426614174007",
      "transaction_type": "investment",
      "fund_id": "456e7890-e89b-12d3-a456-426614174001",
      "fund_name": "Growth Fund",
      "amount": 10000.0,
      "status": "completed",
      "created_at": "2025-09-08T10:00:00Z",
      "notes": "Initial investment in growth fund"
    }
  ],
  "total_count": 1,
  "page": 1,
  "page_size": 20,
  "total_pages": 1
}
```

---

## 🔒 **AUTHENTICATION & AUTHORIZATION**

### **User Roles and Permissions**

#### **ADMIN**
- Full system access
- All CRUD operations
- User management
- System configuration

#### **MANAGER**
- Fund and portfolio management
- User read/update operations
- Analytics and reporting

#### **TRADER**
- Trading operations
- Portfolio management
- Strategy execution

#### **ANALYST**
- Read-only access to most data
- Analytics and reporting
- Strategy analysis

#### **INVESTOR**
- Basic portfolio access
- Investment operations
- Transaction history

### **Permission System**
All endpoints check for specific permissions:
- `users:create`, `users:read`, `users:update`, `users:delete`
- `funds:create`, `funds:read`, `funds:update`, `funds:delete`
- `portfolio:create`, `portfolio:read`, `portfolio:update`, `portfolio:delete`
- `strategies:create`, `strategies:read`, `strategies:update`, `strategies:delete`

---

## 📊 **ERROR HANDLING**

### **Standard Error Response Format**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "reason": "Invalid email format"
    }
  }
}
```

### **HTTP Status Codes**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

### **Common Error Codes**
- `INVALID_TOKEN` - Invalid or expired JWT token
- `INSUFFICIENT_PERMISSIONS` - User lacks required permissions
- `VALIDATION_ERROR` - Input validation failed
- `RESOURCE_NOT_FOUND` - Requested resource not found
- `DUPLICATE_RESOURCE` - Resource already exists
- `INSUFFICIENT_BALANCE` - Insufficient funds for operation

---

## 🚀 **GETTING STARTED**

### **1. Register a User**
```bash
curl -X POST "https://api.neozork.com/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "role": "INVESTOR"
  }'
```

### **2. Login and Get Token**
```bash
curl -X POST "https://api.neozork.com/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'
```

### **3. Use Token for API Calls**
```bash
curl -X GET "https://api.neozork.com/api/v1/funds/" \
  -H "Authorization: Bearer <your-access-token>"
```

---

## 📈 **RATE LIMITING**

- **Rate Limit**: 1000 requests per hour per user
- **Burst Limit**: 100 requests per minute
- **Headers**: Rate limit information included in response headers
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

---

## 🔧 **SDK AND CLIENT LIBRARIES**

### **Python SDK**
```python
from neozork import NeoZorkClient

client = NeoZorkClient(api_key="your-api-key")

# Get funds
funds = client.funds.list()

# Create investment
investment = client.investor.invest(
    fund_id="fund-uuid",
    amount=10000.0
)
```

### **JavaScript SDK**
```javascript
import { NeoZorkClient } from '@neozork/sdk';

const client = new NeoZorkClient('your-api-key');

// Get portfolio
const portfolio = await client.portfolio.getSummary();

// Make investment
const investment = await client.investor.invest({
  fund_id: 'fund-uuid',
  amount: 10000.0
});
```

---

## 📞 **SUPPORT**

- **Documentation**: https://docs.neozork.com
- **API Status**: https://status.neozork.com
- **Support Email**: support@neozork.com
- **Community Forum**: https://community.neozork.com

---

**Last Updated**: September 8, 2025  
**API Version**: v1.0  
**Status**: 🚀 **Production Ready**
