"""
Database Models for Pocket Hedge Fund

This module defines SQLAlchemy models for all database entities
in the Pocket Hedge Fund system.
"""

import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Dict, Any
from enum import Enum

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, Date, 
    Numeric, Text, ForeignKey, UniqueConstraint, Index,
    JSON, create_engine, func
)
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func as sql_func

Base = declarative_base()


class UserRole(Enum):
    """User role enumeration."""
    ADMIN = "admin"
    FUND_MANAGER = "fund_manager"
    INVESTOR = "investor"
    VIEWER = "viewer"


class FundStatus(Enum):
    """Fund status enumeration."""
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    LIQUIDATING = "liquidating"


class FundType(Enum):
    """Fund type enumeration."""
    MINI = "mini"
    STANDARD = "standard"
    PREMIUM = "premium"


class RiskLevel(Enum):
    """Risk level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class TransactionType(Enum):
    """Transaction type enumeration."""
    BUY = "buy"
    SELL = "sell"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    DIVIDEND = "dividend"
    FEE = "fee"


class AssetType(Enum):
    """Asset type enumeration."""
    CRYPTO = "crypto"
    STOCK = "stock"
    FOREX = "forex"
    COMMODITY = "commodity"
    BOND = "bond"
    ETF = "etf"


class StrategyType(Enum):
    """Strategy type enumeration."""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    ARBITRAGE = "arbitrage"
    ML = "ml"
    QUANTITATIVE = "quantitative"
    FUNDAMENTAL = "fundamental"


class User(Base):
    """User model for authentication and user management."""
    
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    date_of_birth = Column(Date)
    country = Column(String(100))
    kyc_status = Column(String(50), default='pending')
    kyc_verified_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    role = Column(String(50), default='investor')
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(32))
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    funds_created = relationship("Fund", back_populates="creator")
    user_investments = relationship("Investment", back_populates="investor")
    api_keys = relationship("APIKey", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    @hybrid_property
    def full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            'id': str(self.id),
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'country': self.country,
            'kyc_status': self.kyc_status,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'role': self.role,
            'mfa_enabled': self.mfa_enabled,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None if self.updated_at else None
        }


class Fund(Base):
    """Fund model for hedge fund management."""
    
    __tablename__ = 'funds'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    fund_type = Column(String(50), nullable=False, index=True)
    initial_capital = Column(Numeric(20, 8), nullable=False)
    current_value = Column(Numeric(20, 8), nullable=False)
    management_fee = Column(Numeric(5, 4), nullable=False)  # 0.02 = 2%
    performance_fee = Column(Numeric(5, 4), nullable=False)  # 0.20 = 20%
    min_investment = Column(Numeric(20, 8), nullable=False)
    max_investment = Column(Numeric(20, 8))
    max_investors = Column(Integer)
    current_investors = Column(Integer, default=0)
    status = Column(String(50), default='active', index=True)
    risk_level = Column(String(20), default='medium')
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", back_populates="funds_created")
    fund_investments = relationship("Investment", back_populates="fund")
    positions = relationship("PortfolioPosition", back_populates="fund")
    transactions = relationship("Transaction", back_populates="fund")
    performance_snapshots = relationship("PerformanceSnapshot", back_populates="fund")
    risk_metrics = relationship("RiskMetric", back_populates="fund")
    fund_strategies = relationship("FundStrategy", back_populates="fund")
    
    @hybrid_property
    def total_return(self):
        """Calculate total return."""
        return self.current_value - self.initial_capital
    
    @hybrid_property
    def total_return_percentage(self):
        """Calculate total return percentage."""
        if self.initial_capital > 0:
            return ((self.current_value - self.initial_capital) / self.initial_capital) * 100
        return Decimal('0')
    
    @hybrid_property
    def is_open_for_investment(self):
        """Check if fund is open for new investments."""
        return (
            self.status == FundStatus.ACTIVE.value and
            (self.max_investors is None or self.current_investors < self.max_investors)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert fund to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'fund_type': self.fund_type,
            'initial_capital': float(self.initial_capital),
            'current_value': float(self.current_value),
            'total_return': float(self.total_return),
            'total_return_percentage': float(self.total_return_percentage),
            'management_fee': float(self.management_fee),
            'performance_fee': float(self.performance_fee),
            'min_investment': float(self.min_investment),
            'max_investment': float(self.max_investment) if self.max_investment else None,
            'max_investors': self.max_investors,
            'current_investors': self.current_investors,
            'status': self.status,
            'risk_level': self.risk_level,
            'is_open_for_investment': self.is_open_for_investment,
            'created_by': str(self.created_by),
            'created_at': self.created_at.isoformat() if self.created_at else None if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Investment(Base):
    """Investment model for individual investments."""
    
    __tablename__ = 'investments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investor_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    fund_id = Column(UUID(as_uuid=True), ForeignKey('funds.id'), nullable=False)
    amount = Column(Numeric(20, 8), nullable=False)
    investment_type = Column(String(50), default='lump_sum')
    status = Column(String(50), default='active')
    shares_acquired = Column(Numeric(20, 8), nullable=False)
    share_price = Column(Numeric(20, 8), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    investor = relationship("User", back_populates="user_investments")
    fund = relationship("Fund", back_populates="fund_investments")
    
    @hybrid_property
    def current_value(self):
        """Calculate current value based on current fund value."""
        if self.fund and self.shares_acquired:
            return float(self.shares_acquired * self.fund.current_value / self.fund.initial_capital)
        return 0.0
    
    @hybrid_property
    def total_return(self):
        """Calculate total return."""
        return float(self.current_value) - float(self.amount)
    
    @hybrid_property
    def total_return_percentage(self):
        """Calculate total return percentage."""
        if float(self.amount) > 0:
            return float((self.total_return / float(self.amount)) * 100)
        return 0.0
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': str(self.id),
            'investor_id': str(self.investor_id),
            'fund_id': str(self.fund_id),
            'amount': float(self.amount),
            'investment_type': self.investment_type,
            'status': self.status,
            'shares_acquired': float(self.shares_acquired),
            'share_price': float(self.share_price),
            'current_value': self.current_value,
            'total_return': self.total_return,
            'total_return_percentage': self.total_return_percentage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PortfolioPosition(Base):
    """Portfolio position model for fund holdings."""
    
    __tablename__ = 'portfolio_positions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey('funds.id'), nullable=False)
    asset_symbol = Column(String(20), nullable=False)
    asset_name = Column(String(255))
    asset_type = Column(String(50), nullable=False)
    quantity = Column(Numeric(20, 8), nullable=False)
    average_price = Column(Numeric(20, 8), nullable=False)
    current_price = Column(Numeric(20, 8))
    current_value = Column(Numeric(20, 8))
    unrealized_pnl = Column(Numeric(20, 8))
    unrealized_pnl_percentage = Column(Numeric(10, 4))
    weight_percentage = Column(Numeric(5, 2))  # Percentage of total portfolio
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    fund = relationship("Fund", back_populates="positions")
    
    # Indexes
    __table_args__ = (
        Index('idx_portfolio_positions_fund_id', 'fund_id'),
        Index('idx_portfolio_positions_asset_symbol', 'asset_symbol'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert position to dictionary."""
        return {
            'id': str(self.id),
            'fund_id': str(self.fund_id),
            'asset_symbol': self.asset_symbol,
            'asset_name': self.asset_name,
            'asset_type': self.asset_type,
            'quantity': float(self.quantity),
            'average_price': float(self.average_price),
            'current_price': float(self.current_price) if self.current_price else None,
            'current_value': float(self.current_value) if self.current_value else None,
            'unrealized_pnl': float(self.unrealized_pnl) if self.unrealized_pnl else None,
            'unrealized_pnl_percentage': float(self.unrealized_pnl_percentage) if self.unrealized_pnl_percentage else None,
            'weight_percentage': float(self.weight_percentage) if self.weight_percentage else None,
            'created_at': self.created_at.isoformat() if self.created_at else None if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class TradingStrategy(Base):
    """Trading strategy model."""
    
    __tablename__ = 'trading_strategies'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    strategy_type = Column(String(100), nullable=False)
    parameters = Column(JSON)
    performance_metrics = Column(JSON)
    risk_metrics = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = relationship("User")
    fund_strategies = relationship("FundStrategy", back_populates="strategy")
    transactions = relationship("Transaction", back_populates="strategy")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert strategy to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'strategy_type': self.strategy_type,
            'parameters': self.parameters,
            'performance_metrics': self.performance_metrics,
            'risk_metrics': self.risk_metrics,
            'is_active': self.is_active,
            'created_by': str(self.created_by),
            'created_at': self.created_at.isoformat() if self.created_at else None if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FundStrategy(Base):
    """Fund strategy mapping model."""
    
    __tablename__ = 'fund_strategies'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey('funds.id'), nullable=False)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('trading_strategies.id'), nullable=False)
    allocation_percentage = Column(Numeric(5, 2), nullable=False)  # Percentage of fund allocated to this strategy
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    fund = relationship("Fund", back_populates="fund_strategies")
    strategy = relationship("TradingStrategy", back_populates="fund_strategies")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('fund_id', 'strategy_id', name='unique_fund_strategy'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert fund strategy to dictionary."""
        return {
            'id': str(self.id),
            'fund_id': str(self.fund_id),
            'strategy_id': str(self.strategy_id),
            'allocation_percentage': float(self.allocation_percentage),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Transaction(Base):
    """Transaction model for fund operations."""
    
    __tablename__ = 'transactions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey('funds.id'), nullable=False)
    transaction_type = Column(String(50), nullable=False)
    asset_symbol = Column(String(20), nullable=False)
    quantity = Column(Numeric(20, 8), nullable=False)
    price = Column(Numeric(20, 8), nullable=False)
    total_amount = Column(Numeric(20, 8), nullable=False)
    fees = Column(Numeric(20, 8), default=0)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('trading_strategies.id'))
    executed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    fund = relationship("Fund", back_populates="transactions")
    strategy = relationship("TradingStrategy", back_populates="transactions")
    
    # Indexes
    __table_args__ = (
        Index('idx_transactions_fund_id', 'fund_id'),
        Index('idx_transactions_executed_at', 'executed_at'),
        Index('idx_transactions_asset_symbol', 'asset_symbol'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary."""
        return {
            'id': str(self.id),
            'fund_id': str(self.fund_id),
            'transaction_type': self.transaction_type,
            'asset_symbol': self.asset_symbol,
            'quantity': float(self.quantity),
            'price': float(self.price),
            'total_amount': float(self.total_amount),
            'fees': float(self.fees),
            'strategy_id': str(self.strategy_id) if self.strategy_id else None,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PerformanceSnapshot(Base):
    """Performance snapshot model for historical performance tracking."""
    
    __tablename__ = 'performance_snapshots'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey('funds.id'), nullable=False)
    snapshot_date = Column(Date, nullable=False)
    total_value = Column(Numeric(20, 8), nullable=False)
    total_return = Column(Numeric(20, 8), nullable=False)
    total_return_percentage = Column(Numeric(10, 4), nullable=False)
    daily_return = Column(Numeric(10, 4))
    daily_return_percentage = Column(Numeric(10, 4))
    sharpe_ratio = Column(Numeric(10, 4))
    max_drawdown = Column(Numeric(10, 4))
    volatility = Column(Numeric(10, 4))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    fund = relationship("Fund", back_populates="performance_snapshots")
    
    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint('fund_id', 'snapshot_date', name='unique_fund_snapshot_date'),
        Index('idx_performance_snapshots_fund_id', 'fund_id'),
        Index('idx_performance_snapshots_date', 'snapshot_date'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert performance snapshot to dictionary."""
        return {
            'id': str(self.id),
            'fund_id': str(self.fund_id),
            'snapshot_date': self.snapshot_date.isoformat() if self.snapshot_date else None,
            'total_value': float(self.total_value),
            'total_return': float(self.total_return),
            'total_return_percentage': float(self.total_return_percentage),
            'daily_return': float(self.daily_return) if self.daily_return else None,
            'daily_return_percentage': float(self.daily_return_percentage) if self.daily_return_percentage else None,
            'sharpe_ratio': float(self.sharpe_ratio) if self.sharpe_ratio else None,
            'max_drawdown': float(self.max_drawdown) if self.max_drawdown else None,
            'volatility': float(self.volatility) if self.volatility else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class RiskMetric(Base):
    """Risk metrics model for risk analysis."""
    
    __tablename__ = 'risk_metrics'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey('funds.id'), nullable=False)
    calculation_date = Column(Date, nullable=False)
    var_95 = Column(Numeric(20, 8))  # Value at Risk 95%
    var_99 = Column(Numeric(20, 8))  # Value at Risk 99%
    cvar_95 = Column(Numeric(20, 8))  # Conditional Value at Risk 95%
    cvar_99 = Column(Numeric(20, 8))  # Conditional Value at Risk 99%
    beta = Column(Numeric(10, 4))
    correlation_spy = Column(Numeric(10, 4))
    tracking_error = Column(Numeric(10, 4))
    information_ratio = Column(Numeric(10, 4))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    fund = relationship("Fund", back_populates="risk_metrics")
    
    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint('fund_id', 'calculation_date', name='unique_fund_risk_date'),
        Index('idx_risk_metrics_fund_id', 'fund_id'),
        Index('idx_risk_metrics_date', 'calculation_date'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert risk metric to dictionary."""
        return {
            'id': str(self.id),
            'fund_id': str(self.fund_id),
            'calculation_date': self.calculation_date.isoformat() if self.calculation_date else None,
            'var_95': float(self.var_95) if self.var_95 else None,
            'var_99': float(self.var_99) if self.var_99 else None,
            'cvar_95': float(self.cvar_95) if self.cvar_95 else None,
            'cvar_99': float(self.cvar_99) if self.cvar_99 else None,
            'beta': float(self.beta) if self.beta else None,
            'correlation_spy': float(self.correlation_spy) if self.correlation_spy else None,
            'tracking_error': float(self.tracking_error) if self.tracking_error else None,
            'information_ratio': float(self.information_ratio) if self.information_ratio else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class APIKey(Base):
    """API key model for API access management."""
    
    __tablename__ = 'api_keys'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    key_name = Column(String(255), nullable=False)
    api_key = Column(String(255), unique=True, nullable=False)
    permissions = Column(JSON)
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert API key to dictionary."""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'key_name': self.key_name,
            'api_key': self.api_key,
            'permissions': self.permissions,
            'is_active': self.is_active,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AuditLog(Base):
    """Audit log model for tracking system changes."""
    
    __tablename__ = 'audit_log'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(UUID(as_uuid=True))
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(INET)
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_log_user_id', 'user_id'),
        Index('idx_audit_log_created_at', 'created_at'),
        Index('idx_audit_log_resource', 'resource_type', 'resource_id'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert audit log to dictionary."""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id) if self.user_id else None,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': str(self.resource_id) if self.resource_id else None,
            'old_values': self.old_values,
            'new_values': self.new_values,
            'ip_address': str(self.ip_address) if self.ip_address else None,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }