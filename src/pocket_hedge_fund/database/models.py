"""
Database models for Pocket Hedge Fund.

This module defines SQLAlchemy models for all Pocket Hedge Fund entities.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from enum import Enum
import uuid

from sqlalchemy import (
    Column, Integer, String, Float, Numeric as SQLDecimal, 
    DateTime, Date, Boolean, Text, ForeignKey, Index,
    UniqueConstraint, CheckConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import UUID, JSONB

Base = declarative_base()


class UserRole(Enum):
    """User roles in the system."""
    ADMIN = "admin"
    FUND_MANAGER = "fund_manager"
    INVESTOR = "investor"
    ANALYST = "analyst"
    VIEWER = "viewer"


class FundStatus(Enum):
    """Fund status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    CLOSED = "closed"


class TransactionType(Enum):
    """Transaction type enumeration."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    FEE = "fee"
    REBALANCE = "rebalance"


class StrategyStatus(Enum):
    """Strategy status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    TESTING = "testing"
    PAUSED = "paused"


class UserModel(Base):
    """User model for authentication and authorization."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False, default=UserRole.INVESTOR.value)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    funds = relationship("FundModel", back_populates="manager")
    investments = relationship("InvestmentModel", back_populates="investor")
    
    @validates('email')
    def validate_email(self, key, email):
        """Validate email format."""
        if '@' not in email:
            raise ValueError("Invalid email format")
        return email.lower()
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class FundModel(Base):
    """Fund model for hedge fund management."""
    
    __tablename__ = "funds"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False, default=FundStatus.ACTIVE.value)
    
    # Fund details
    initial_capital = Column(SQLDecimal(20, 2), nullable=False, default=Decimal('0.00'))
    current_capital = Column(SQLDecimal(20, 2), nullable=False, default=Decimal('0.00'))
    management_fee_rate = Column(SQLDecimal(5, 4), nullable=False, default=Decimal('0.0200'))  # 2%
    performance_fee_rate = Column(SQLDecimal(5, 4), nullable=False, default=Decimal('0.2000'))  # 20%
    
    # Risk parameters
    max_drawdown_limit = Column(SQLDecimal(5, 4), nullable=False, default=Decimal('0.1000'))  # 10%
    max_position_size = Column(SQLDecimal(5, 4), nullable=False, default=Decimal('0.1000'))  # 10%
    max_leverage = Column(SQLDecimal(5, 4), nullable=False, default=Decimal('1.0000'))  # 1x
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    launched_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    
    # Relationships
    manager = relationship("UserModel", back_populates="funds")
    portfolios = relationship("PortfolioModel", back_populates="fund")
    performances = relationship("PerformanceModel", back_populates="fund")
    transactions = relationship("TransactionModel", back_populates="fund")
    strategies = relationship("StrategyModel", back_populates="fund")
    
    @validates('management_fee_rate', 'performance_fee_rate')
    def validate_fee_rates(self, key, value):
        """Validate fee rates are between 0 and 1."""
        if not (0 <= value <= 1):
            raise ValueError(f"{key} must be between 0 and 1")
        return value
    
    def __repr__(self):
        return f"<Fund(id={self.id}, name={self.name}, status={self.status})>"


class PortfolioModel(Base):
    """Portfolio model for position tracking."""
    
    __tablename__ = "portfolios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=False)
    
    # Asset information
    asset_symbol = Column(String(50), nullable=False)
    asset_name = Column(String(200), nullable=False)
    asset_type = Column(String(50), nullable=False)  # stock, crypto, forex, etc.
    
    # Position details
    quantity = Column(SQLDecimal(20, 8), nullable=False, default=Decimal('0.00000000'))
    average_price = Column(SQLDecimal(20, 8), nullable=False, default=Decimal('0.00000000'))
    current_price = Column(SQLDecimal(20, 8), nullable=False, default=Decimal('0.00000000'))
    market_value = Column(SQLDecimal(20, 2), nullable=False, default=Decimal('0.00'))
    unrealized_pnl = Column(SQLDecimal(20, 2), nullable=False, default=Decimal('0.00'))
    
    # Risk metrics
    position_size_pct = Column(SQLDecimal(5, 4), nullable=False, default=Decimal('0.0000'))
    beta = Column(SQLDecimal(5, 4), nullable=True)
    volatility = Column(SQLDecimal(5, 4), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_price_update = Column(DateTime, nullable=True)
    
    # Relationships
    fund = relationship("FundModel", back_populates="portfolios")
    
    # Indexes
    __table_args__ = (
        Index('idx_portfolio_fund_asset', 'fund_id', 'asset_symbol'),
        UniqueConstraint('fund_id', 'asset_symbol', name='uq_fund_asset'),
    )
    
    def __repr__(self):
        return f"<Portfolio(id={self.id}, asset={self.asset_symbol}, quantity={self.quantity})>"


class PerformanceModel(Base):
    """Performance model for tracking fund performance."""
    
    __tablename__ = "performances"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=False)
    date = Column(Date, nullable=False)
    
    # Performance metrics
    total_return = Column(SQLDecimal(10, 6), nullable=False, default=Decimal('0.000000'))
    daily_return = Column(SQLDecimal(10, 6), nullable=False, default=Decimal('0.000000'))
    cumulative_return = Column(SQLDecimal(10, 6), nullable=False, default=Decimal('0.000000'))
    
    # Risk metrics
    volatility = Column(SQLDecimal(10, 6), nullable=False, default=Decimal('0.000000'))
    sharpe_ratio = Column(SQLDecimal(10, 6), nullable=True)
    max_drawdown = Column(SQLDecimal(10, 6), nullable=False, default=Decimal('0.000000'))
    var_95 = Column(SQLDecimal(10, 6), nullable=True)  # Value at Risk 95%
    
    # Portfolio metrics
    total_value = Column(SQLDecimal(20, 2), nullable=False, default=Decimal('0.00'))
    cash_balance = Column(SQLDecimal(20, 2), nullable=False, default=Decimal('0.00'))
    leverage = Column(SQLDecimal(5, 4), nullable=False, default=Decimal('0.0000'))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    fund = relationship("FundModel", back_populates="performances")
    
    # Indexes
    __table_args__ = (
        Index('idx_performance_fund_date', 'fund_id', 'date'),
        UniqueConstraint('fund_id', 'date', name='uq_fund_date'),
    )
    
    def __repr__(self):
        return f"<Performance(id={self.id}, fund_id={self.fund_id}, date={self.date})>"


class TransactionModel(Base):
    """Transaction model for tracking all fund transactions."""
    
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=False)
    transaction_type = Column(String(50), nullable=False)
    
    # Transaction details
    asset_symbol = Column(String(50), nullable=True)
    quantity = Column(SQLDecimal(20, 8), nullable=False, default=Decimal('0.00000000'))
    price = Column(SQLDecimal(20, 8), nullable=False, default=Decimal('0.00000000'))
    amount = Column(SQLDecimal(20, 2), nullable=False, default=Decimal('0.00'))
    fees = Column(SQLDecimal(20, 2), nullable=False, default=Decimal('0.00'))
    
    # Reference information
    reference_id = Column(String(100), nullable=True)  # External transaction ID
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    executed_at = Column(DateTime, nullable=True)
    
    # Relationships
    fund = relationship("FundModel", back_populates="transactions")
    
    # Indexes
    __table_args__ = (
        Index('idx_transaction_fund_type', 'fund_id', 'transaction_type'),
        Index('idx_transaction_executed_at', 'executed_at'),
    )
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"


class StrategyModel(Base):
    """Strategy model for trading strategies."""
    
    __tablename__ = "strategies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default=StrategyStatus.ACTIVE.value)
    
    # Strategy configuration
    config = Column(JSONB, nullable=True)  # Strategy parameters
    risk_params = Column(JSONB, nullable=True)  # Risk management parameters
    
    # Performance metrics
    total_return = Column(SQLDecimal(10, 6), nullable=False, default=Decimal('0.000000'))
    sharpe_ratio = Column(SQLDecimal(10, 6), nullable=True)
    max_drawdown = Column(SQLDecimal(10, 6), nullable=False, default=Decimal('0.000000'))
    win_rate = Column(SQLDecimal(5, 4), nullable=True)
    
    # Allocation
    allocation_pct = Column(SQLDecimal(5, 4), nullable=False, default=Decimal('0.0000'))
    max_allocation_pct = Column(SQLDecimal(5, 4), nullable=False, default=Decimal('1.0000'))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_execution = Column(DateTime, nullable=True)
    
    # Relationships
    fund = relationship("FundModel", back_populates="strategies")
    
    @validates('allocation_pct', 'max_allocation_pct')
    def validate_allocation(self, key, value):
        """Validate allocation percentages."""
        if not (0 <= value <= 1):
            raise ValueError(f"{key} must be between 0 and 1")
        return value
    
    def __repr__(self):
        return f"<Strategy(id={self.id}, name={self.name}, status={self.status})>"


class InvestmentModel(Base):
    """Investment model for tracking investor investments."""
    
    __tablename__ = "investments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=False)
    
    # Investment details
    amount = Column(SQLDecimal(20, 2), nullable=False)
    shares = Column(SQLDecimal(20, 8), nullable=False)
    share_price = Column(SQLDecimal(20, 8), nullable=False)
    
    # Current value
    current_value = Column(SQLDecimal(20, 2), nullable=False, default=Decimal('0.00'))
    unrealized_pnl = Column(SQLDecimal(20, 2), nullable=False, default=Decimal('0.00'))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    investor = relationship("UserModel", back_populates="investments")
    fund = relationship("FundModel")
    
    # Indexes
    __table_args__ = (
        Index('idx_investment_investor', 'investor_id'),
        Index('idx_investment_fund', 'fund_id'),
        UniqueConstraint('investor_id', 'fund_id', name='uq_investor_fund'),
    )
    
    def __repr__(self):
        return f"<Investment(id={self.id}, investor_id={self.investor_id}, amount={self.amount})>"


class RiskModel(Base):
    """Risk model for tracking risk metrics."""
    
    __tablename__ = "risks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=False)
    date = Column(Date, nullable=False)
    
    # Risk metrics
    var_95 = Column(SQLDecimal(10, 6), nullable=True)  # Value at Risk 95%
    var_99 = Column(SQLDecimal(10, 6), nullable=True)  # Value at Risk 99%
    cvar_95 = Column(SQLDecimal(10, 6), nullable=True)  # Conditional VaR 95%
    expected_shortfall = Column(SQLDecimal(10, 6), nullable=True)
    
    # Portfolio risk
    portfolio_volatility = Column(SQLDecimal(10, 6), nullable=False, default=Decimal('0.000000'))
    portfolio_beta = Column(SQLDecimal(10, 6), nullable=True)
    correlation_matrix = Column(JSONB, nullable=True)
    
    # Stress test results
    stress_test_results = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    fund = relationship("FundModel")
    
    # Indexes
    __table_args__ = (
        Index('idx_risk_fund_date', 'fund_id', 'date'),
        UniqueConstraint('fund_id', 'date', name='uq_risk_fund_date'),
    )
    
    def __repr__(self):
        return f"<Risk(id={self.id}, fund_id={self.fund_id}, date={self.date})>"
