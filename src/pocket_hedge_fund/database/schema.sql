-- NeoZork Pocket Hedge Fund Database Schema
-- PostgreSQL Database Schema for Fund Management

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database if not exists (run this manually)
-- CREATE DATABASE neozork_fund;

-- Users table
CREATE TABLE IF NOT EXISTS users (
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

-- Funds table
CREATE TABLE IF NOT EXISTS funds (
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

-- Investors table
CREATE TABLE IF NOT EXISTS investors (
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

-- Portfolio positions table
CREATE TABLE IF NOT EXISTS portfolio_positions (
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

-- Trading strategies table
CREATE TABLE IF NOT EXISTS trading_strategies (
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

-- Fund strategies mapping
CREATE TABLE IF NOT EXISTS fund_strategies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_id UUID REFERENCES funds(id) NOT NULL,
    strategy_id UUID REFERENCES trading_strategies(id) NOT NULL,
    allocation_percentage DECIMAL(5, 2) NOT NULL, -- Percentage of fund allocated to this strategy
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(fund_id, strategy_id)
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
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

-- Performance snapshots table
CREATE TABLE IF NOT EXISTS performance_snapshots (
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

-- Risk metrics table
CREATE TABLE IF NOT EXISTS risk_metrics (
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

-- API keys table
CREATE TABLE IF NOT EXISTS api_keys (
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

-- Audit log table
CREATE TABLE IF NOT EXISTS audit_log (
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

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_funds_status ON funds(status);
CREATE INDEX IF NOT EXISTS idx_funds_type ON funds(fund_type);
CREATE INDEX IF NOT EXISTS idx_investors_user_id ON investors(user_id);
CREATE INDEX IF NOT EXISTS idx_investors_fund_id ON investors(fund_id);
CREATE INDEX IF NOT EXISTS idx_portfolio_positions_fund_id ON portfolio_positions(fund_id);
CREATE INDEX IF NOT EXISTS idx_transactions_fund_id ON transactions(fund_id);
CREATE INDEX IF NOT EXISTS idx_transactions_executed_at ON transactions(executed_at);
CREATE INDEX IF NOT EXISTS idx_performance_snapshots_fund_id ON performance_snapshots(fund_id);
CREATE INDEX IF NOT EXISTS idx_performance_snapshots_date ON performance_snapshots(snapshot_date);
CREATE INDEX IF NOT EXISTS idx_risk_metrics_fund_id ON risk_metrics(fund_id);
CREATE INDEX IF NOT EXISTS idx_risk_metrics_date ON risk_metrics(calculation_date);
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_log(created_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
DROP TRIGGER IF EXISTS update_funds_updated_at ON funds;
DROP TRIGGER IF EXISTS update_investors_updated_at ON investors;
DROP TRIGGER IF EXISTS update_portfolio_positions_updated_at ON portfolio_positions;
DROP TRIGGER IF EXISTS update_trading_strategies_updated_at ON trading_strategies;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_funds_updated_at BEFORE UPDATE ON funds FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_investors_updated_at BEFORE UPDATE ON investors FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_portfolio_positions_updated_at BEFORE UPDATE ON portfolio_positions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_trading_strategies_updated_at BEFORE UPDATE ON trading_strategies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO users (email, username, password_hash, first_name, last_name, is_admin) VALUES
('admin@neozork.com', 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2O', 'Admin', 'User', true),
('demo@neozork.com', 'demo', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2O', 'Demo', 'User', false)
ON CONFLICT (email) DO NOTHING;

INSERT INTO funds (name, description, fund_type, initial_capital, current_value, management_fee, performance_fee, min_investment, max_investment, max_investors, created_by) VALUES
('NeoZork Mini Fund', 'AI-powered mini hedge fund for small investors', 'mini', 100000.00, 105000.00, 0.015, 0.15, 1000.00, 10000.00, 100, (SELECT id FROM users WHERE username = 'admin')),
('NeoZork Standard Fund', 'AI-powered standard hedge fund for medium investors', 'standard', 1000000.00, 1100000.00, 0.02, 0.20, 10000.00, 100000.00, 50, (SELECT id FROM users WHERE username = 'admin')),
('NeoZork Premium Fund', 'AI-powered premium hedge fund for large investors', 'premium', 10000000.00, 12000000.00, 0.025, 0.25, 100000.00, 1000000.00, 20, (SELECT id FROM users WHERE username = 'admin'))
ON CONFLICT DO NOTHING;

INSERT INTO trading_strategies (name, description, strategy_type, parameters, created_by) VALUES
('Momentum Strategy', 'AI-powered momentum trading strategy', 'momentum', '{"lookback_period": 20, "threshold": 0.02}', (SELECT id FROM users WHERE username = 'admin')),
('Mean Reversion Strategy', 'AI-powered mean reversion strategy', 'mean_reversion', '{"lookback_period": 14, "threshold": 0.015}', (SELECT id FROM users WHERE username = 'admin')),
('Arbitrage Strategy', 'Cross-exchange arbitrage strategy', 'arbitrage', '{"min_profit": 0.005, "max_slippage": 0.001}', (SELECT id FROM users WHERE username = 'admin'))
ON CONFLICT DO NOTHING;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO neozork_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO neozork_user;
