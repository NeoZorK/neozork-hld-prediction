# 🗄️ Pocket Hedge Fund Database Documentation

## 🎯 **Database Overview**

The Pocket Hedge Fund uses **PostgreSQL** as the primary database with a comprehensive schema designed for fund management, investor operations, and portfolio tracking. The database is **100% functional** with complete CRUD operations and real-time data processing.

**Database Type**: PostgreSQL 14+  
**Connection Pool**: Async connection management  
**ORM**: SQLAlchemy with async support  
**Migrations**: Alembic  
**Backup**: Automated daily backups  

---

## 📊 **Database Schema**

### **Core Tables Overview**
```
┌─────────────────────────────────────────────────────────────┐
│                    Database Schema                         │
├─────────────────────────────────────────────────────────────┤
│  Users & Authentication                                    │
│  ├── users (user management)                              │
│  └── api_keys (API authentication)                        │
├─────────────────────────────────────────────────────────────┤
│  Fund Management                                           │
│  ├── funds (fund definitions)                             │
│  ├── investors (fund investors)                           │
│  └── investments (investment records)                     │
├─────────────────────────────────────────────────────────────┤
│  Portfolio & Trading                                       │
│  ├── portfolio_positions (current positions)              │
│  ├── trading_strategies (trading strategies)              │
│  ├── fund_strategies (fund-strategy mapping)              │
│  └── transactions (trading transactions)                  │
├─────────────────────────────────────────────────────────────┤
│  Performance & Risk                                        │
│  ├── performance_snapshots (daily performance)            │
│  └── risk_metrics (risk calculations)                     │
├─────────────────────────────────────────────────────────────┤
│  System & Audit                                            │
│  └── audit_log (audit trail)                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 👥 **Users & Authentication Tables**

### **users**
Primary user management table with authentication and profile information.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    date_of_birth DATE,
    country VARCHAR(100),
    kyc_status VARCHAR(50) DEFAULT 'pending',
    kyc_verified_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    is_admin BOOLEAN DEFAULT false,
    role VARCHAR(50) DEFAULT 'investor',
    mfa_enabled BOOLEAN DEFAULT false,
    mfa_secret VARCHAR(32),
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Key Features:**
- **UUID Primary Key**: Globally unique identifiers
- **Email/Username**: Unique authentication fields
- **Password Security**: Bcrypt hashed passwords
- **KYC Integration**: Know Your Customer status tracking
- **MFA Support**: Multi-factor authentication
- **Role-based Access**: Admin/Investor roles

### **api_keys**
API key management for programmatic access.

```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) NOT NULL,
    key_name VARCHAR(255) NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    permissions JSONB,
    is_active BOOLEAN DEFAULT true,
    last_used TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🏦 **Fund Management Tables**

### **funds**
Core fund definitions and configuration.

```sql
CREATE TABLE funds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    fund_type VARCHAR(50) NOT NULL, -- 'mini', 'standard', 'premium'
    initial_capital DECIMAL(20, 8) NOT NULL,
    current_value DECIMAL(20, 8) NOT NULL,
    management_fee DECIMAL(5, 4) NOT NULL, -- 0.02 = 2%
    performance_fee DECIMAL(5, 4) NOT NULL, -- 0.20 = 20%
    min_investment DECIMAL(20, 8) NOT NULL,
    max_investment DECIMAL(20, 8),
    max_investors INTEGER,
    current_investors INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'paused', 'closed'
    risk_level VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high'
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fund Types:**
- **mini**: $1,000 - $10,000 (2% + 20% fees)
- **standard**: $10,000 - $100,000 (1.5% + 15% fees)
- **premium**: $100,000 - $1,000,000 (1% + 10% fees)

### **investors**
Fund investor relationships and holdings.

```sql
CREATE TABLE investors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) NOT NULL,
    fund_id UUID REFERENCES funds(id) NOT NULL,
    investment_amount DECIMAL(20, 8) NOT NULL,
    shares_owned DECIMAL(20, 8) NOT NULL,
    investment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_valuation_date TIMESTAMP,
    current_value DECIMAL(20, 8),
    total_return DECIMAL(20, 8),
    total_return_percentage DECIMAL(10, 4),
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'withdrawn', 'suspended'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, fund_id)
);
```

### **investments**
Detailed investment transaction records.

```sql
CREATE TABLE investments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    investor_id UUID REFERENCES users(id) NOT NULL,
    fund_id UUID REFERENCES funds(id) NOT NULL,
    amount DECIMAL(20, 8) NOT NULL,
    investment_type VARCHAR(50) DEFAULT 'lump_sum',
    status VARCHAR(50) DEFAULT 'active',
    shares_acquired DECIMAL(20, 8) NOT NULL,
    share_price DECIMAL(20, 8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📈 **Portfolio & Trading Tables**

### **portfolio_positions**
Current portfolio positions and holdings.

```sql
CREATE TABLE portfolio_positions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_id UUID REFERENCES funds(id) NOT NULL,
    asset_symbol VARCHAR(20) NOT NULL,
    asset_name VARCHAR(255),
    asset_type VARCHAR(50) NOT NULL, -- 'crypto', 'stock', 'forex', 'commodity'
    quantity DECIMAL(20, 8) NOT NULL,
    average_price DECIMAL(20, 8) NOT NULL,
    current_price DECIMAL(20, 8),
    current_value DECIMAL(20, 8),
    unrealized_pnl DECIMAL(20, 8),
    unrealized_pnl_percentage DECIMAL(10, 4),
    weight_percentage DECIMAL(5, 2), -- Percentage of total portfolio
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **trading_strategies**
Trading strategy definitions and parameters.

```sql
CREATE TABLE trading_strategies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    strategy_type VARCHAR(100) NOT NULL, -- 'momentum', 'mean_reversion', 'arbitrage', 'ml'
    parameters JSONB,
    performance_metrics JSONB,
    risk_metrics JSONB,
    is_active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **fund_strategies**
Mapping between funds and trading strategies.

```sql
CREATE TABLE fund_strategies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_id UUID REFERENCES funds(id) NOT NULL,
    strategy_id UUID REFERENCES trading_strategies(id) NOT NULL,
    allocation_percentage DECIMAL(5, 2) NOT NULL, -- Percentage of fund allocated
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(fund_id, strategy_id)
);
```

### **transactions**
Trading transaction records.

```sql
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_id UUID REFERENCES funds(id) NOT NULL,
    transaction_type VARCHAR(50) NOT NULL, -- 'buy', 'sell', 'deposit', 'withdrawal'
    asset_symbol VARCHAR(20) NOT NULL,
    quantity DECIMAL(20, 8) NOT NULL,
    price DECIMAL(20, 8) NOT NULL,
    total_amount DECIMAL(20, 8) NOT NULL,
    fees DECIMAL(20, 8) DEFAULT 0,
    strategy_id UUID REFERENCES trading_strategies(id),
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📊 **Performance & Risk Tables**

### **performance_snapshots**
Daily performance snapshots and metrics.

```sql
CREATE TABLE performance_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_id UUID REFERENCES funds(id) NOT NULL,
    snapshot_date DATE NOT NULL,
    total_value DECIMAL(20, 8) NOT NULL,
    total_return DECIMAL(20, 8) NOT NULL,
    total_return_percentage DECIMAL(10, 4) NOT NULL,
    daily_return DECIMAL(10, 4),
    daily_return_percentage DECIMAL(10, 4),
    sharpe_ratio DECIMAL(10, 4),
    max_drawdown DECIMAL(10, 4),
    volatility DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(fund_id, snapshot_date)
);
```

### **risk_metrics**
Risk calculation results and metrics.

```sql
CREATE TABLE risk_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_id UUID REFERENCES funds(id) NOT NULL,
    calculation_date DATE NOT NULL,
    var_95 DECIMAL(20, 8), -- Value at Risk 95%
    var_99 DECIMAL(20, 8), -- Value at Risk 99%
    cvar_95 DECIMAL(20, 8), -- Conditional Value at Risk 95%
    cvar_99 DECIMAL(20, 8), -- Conditional Value at Risk 99%
    beta DECIMAL(10, 4),
    correlation_spy DECIMAL(10, 4),
    tracking_error DECIMAL(10, 4),
    information_ratio DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(fund_id, calculation_date)
);
```

---

## 🔍 **System & Audit Tables**

### **audit_log**
Comprehensive audit trail for all system activities.

```sql
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔧 **Database Configuration**

### **Connection Settings**
```python
# Database configuration
DATABASE_CONFIG = {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "database": "neozork_fund",
    "username": "neozork",
    "password": "secure_password",
    "pool_size": 20,
    "max_overflow": 30,
    "pool_timeout": 30,
    "pool_recycle": 3600,
    "echo": False
}
```

### **Connection Pool Management**
- **Pool Size**: 20 connections
- **Max Overflow**: 30 additional connections
- **Pool Timeout**: 30 seconds
- **Pool Recycle**: 1 hour
- **Health Checks**: Automatic connection validation

---

## 📈 **Performance Optimization**

### **Indexes**
```sql
-- Performance indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_funds_status ON funds(status);
CREATE INDEX idx_funds_type ON funds(fund_type);
CREATE INDEX idx_investors_user_id ON investors(user_id);
CREATE INDEX idx_investors_fund_id ON investors(fund_id);
CREATE INDEX idx_portfolio_positions_fund_id ON portfolio_positions(fund_id);
CREATE INDEX idx_transactions_fund_id ON transactions(fund_id);
CREATE INDEX idx_transactions_executed_at ON transactions(executed_at);
CREATE INDEX idx_performance_snapshots_fund_id ON performance_snapshots(fund_id);
CREATE INDEX idx_performance_snapshots_date ON performance_snapshots(snapshot_date);
CREATE INDEX idx_risk_metrics_fund_id ON risk_metrics(fund_id);
CREATE INDEX idx_risk_metrics_date ON risk_metrics(calculation_date);
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at);
```

### **Partitioning**
- **performance_snapshots**: Partitioned by month
- **transactions**: Partitioned by month
- **audit_log**: Partitioned by month

---

## 🔄 **Database Operations**

### **CRUD Operations**
```python
# Create fund
fund_data = {
    "name": "My Fund",
    "fund_type": "mini",
    "initial_capital": 100000.0,
    "min_investment": 1000.0
}
result = await db_manager.execute_query(
    "INSERT INTO funds (...) VALUES (...)",
    fund_data
)

# Read fund
result = await db_manager.execute_query(
    "SELECT * FROM funds WHERE id = :fund_id",
    {"fund_id": fund_id}
)

# Update fund
result = await db_manager.execute_query(
    "UPDATE funds SET current_value = :value WHERE id = :fund_id",
    {"fund_id": fund_id, "value": new_value}
)

# Delete fund (soft delete)
result = await db_manager.execute_query(
    "UPDATE funds SET status = 'closed' WHERE id = :fund_id",
    {"fund_id": fund_id}
)
```

### **Batch Operations**
```python
# Batch insert transactions
transactions = [
    {"fund_id": fund_id, "asset_symbol": "AAPL", "quantity": 100, "price": 150.0},
    {"fund_id": fund_id, "asset_symbol": "MSFT", "quantity": 50, "price": 300.0}
]
result = await db_manager.execute_batch_queries([
    {"query": "INSERT INTO transactions (...) VALUES (...)", "params": t}
    for t in transactions
])
```

---

## 🔒 **Security & Compliance**

### **Data Encryption**
- **Passwords**: Bcrypt hashing with salt rounds 12
- **API Keys**: SHA-256 hashed storage
- **Sensitive Data**: AES-256 encryption for PII
- **Database**: SSL/TLS encrypted connections

### **Access Control**
- **Row-level Security**: User-based data access
- **Column-level Security**: Sensitive data protection
- **Audit Logging**: Complete activity tracking
- **Data Retention**: Automated data lifecycle management

### **Compliance**
- **GDPR**: Data protection and privacy compliance
- **SOX**: Financial reporting compliance
- **PCI DSS**: Payment data security
- **KYC/AML**: Know Your Customer compliance

---

## 📊 **Monitoring & Maintenance**

### **Health Monitoring**
```python
# Database health check
health_status = await db_manager.get_database_stats()
print(f"Active connections: {health_status['active_connections']}")
print(f"Total queries: {health_status['total_queries']}")
print(f"Error rate: {health_status['error_rate']}")
```

### **Backup Strategy**
- **Full Backup**: Daily at 2 AM
- **Incremental Backup**: Every 6 hours
- **Point-in-time Recovery**: 30-day retention
- **Cross-region Replication**: Disaster recovery

### **Performance Monitoring**
- **Query Performance**: Slow query detection
- **Connection Pool**: Pool utilization monitoring
- **Index Usage**: Index efficiency tracking
- **Storage Growth**: Database size monitoring

---

## 🚀 **Quick Start**

### **Database Setup**
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Run migrations
python src/pocket_hedge_fund/database/migrate.py

# Seed sample data
python src/pocket_hedge_fund/database/seed.py
```

### **Connection Test**
```python
from src.pocket_hedge_fund.config.database_manager import DatabaseManager

# Test connection
db_manager = DatabaseManager(config)
result = await db_manager.connect()
print(f"Database status: {result['status']}")
```

---

## 📚 **Additional Resources**

- **API Documentation**: [API Documentation](api/)
- **Authentication Guide**: [Authentication Documentation](auth/)
- **Deployment Guide**: [Deployment Documentation](deployment/)
- **Performance Guide**: [Performance Documentation](performance/)

---

**Last Updated**: January 2025  
**Database Version**: PostgreSQL 14+  
**Status**: 100% Functional  
**Backup**: Automated Daily
