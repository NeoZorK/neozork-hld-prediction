"""
Transaction and Trade Data Models

This module defines data models for transactions, trades, and rebalancing actions.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from decimal import Decimal
from enum import Enum


class TransactionType(Enum):
    """Transaction type enumeration."""
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    INTEREST = "interest"
    FEE = "fee"
    REBALANCE = "rebalance"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class TransactionStatus(Enum):
    """Transaction status enumeration."""
    PENDING = "pending"
    EXECUTED = "executed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    PARTIALLY_FILLED = "partially_filled"


class TradeType(Enum):
    """Trade type enumeration."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"


@dataclass
class Transaction:
    """Transaction data model."""
    id: str
    portfolio_id: str
    transaction_type: TransactionType
    asset_id: str
    quantity: Decimal
    price: Decimal
    total_amount: Decimal
    fees: Decimal
    net_amount: Decimal
    status: TransactionStatus
    execution_date: datetime
    settlement_date: Optional[datetime] = None
    reference_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Trade:
    """Trade data model."""
    id: str
    portfolio_id: str
    asset_id: str
    trade_type: TradeType
    side: str  # buy or sell
    quantity: Decimal
    price: Decimal
    total_amount: Decimal
    fees: Decimal
    net_amount: Decimal
    status: TransactionStatus
    order_id: Optional[str] = None
    execution_time: Optional[datetime] = None
    settlement_time: Optional[datetime] = None
    stop_price: Optional[Decimal] = None
    limit_price: Optional[Decimal] = None
    trailing_distance: Optional[Decimal] = None
    time_in_force: str = "GTC"  # Good Till Cancelled
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RebalanceAction:
    """Rebalancing action data model."""
    id: str
    portfolio_id: str
    rebalance_id: str
    asset_id: str
    action_type: str  # buy, sell, hold
    current_weight: float
    target_weight: float
    weight_difference: float
    required_trade_amount: Decimal
    trade_quantity: Decimal
    estimated_price: Decimal
    estimated_fees: Decimal
    priority: int = 1  # 1 = highest priority
    status: str = "pending"
    execution_order: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RebalancePlan:
    """Rebalancing plan data model."""
    id: str
    portfolio_id: str
    target_allocations: Dict[str, float]
    current_allocations: Dict[str, float]
    rebalance_threshold: float
    max_trades: Optional[int] = None
    estimated_cost: Decimal = Decimal('0')
    estimated_fees: Decimal = Decimal('0')
    actions: List[RebalanceAction] = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)
    executed_at: Optional[datetime] = None


@dataclass
class OrderBook:
    """Order book data model."""
    asset_id: str
    bids: List[Dict[str, Any]]  # List of bid orders
    asks: List[Dict[str, Any]]  # List of ask orders
    last_price: Decimal
    volume_24h: Decimal
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class MarketData:
    """Market data model."""
    asset_id: str
    symbol: str
    price: Decimal
    volume: Decimal
    high_24h: Decimal
    low_24h: Decimal
    change_24h: Decimal
    change_percentage_24h: float
    market_cap: Optional[Decimal] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ExecutionReport:
    """Trade execution report data model."""
    trade_id: str
    order_id: str
    execution_id: str
    asset_id: str
    side: str
    quantity: Decimal
    price: Decimal
    total_amount: Decimal
    fees: Decimal
    net_amount: Decimal
    execution_time: datetime
    settlement_time: Optional[datetime] = None
    venue: Optional[str] = None
    execution_algorithm: Optional[str] = None
    slippage: Optional[Decimal] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TradeSummary:
    """Trade summary data model."""
    portfolio_id: str
    period_start: datetime
    period_end: datetime
    total_trades: int
    total_volume: Decimal
    total_fees: Decimal
    winning_trades: int
    losing_trades: int
    win_rate: float
    average_win: Decimal
    average_loss: Decimal
    profit_factor: float
    largest_win: Decimal
    largest_loss: Decimal
    created_at: datetime = field(default_factory=datetime.utcnow)
