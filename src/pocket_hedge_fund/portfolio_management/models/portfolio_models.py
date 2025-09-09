"""
Portfolio Data Models

This module defines the core data models for portfolio management including
Portfolio, Position, Asset, and related structures.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from decimal import Decimal


class AssetType(Enum):
    """Asset type enumeration."""
    CRYPTO = "crypto"
    STOCK = "stock"
    BOND = "bond"
    COMMODITY = "commodity"
    FOREX = "forex"
    DERIVATIVE = "derivative"
    REAL_ESTATE = "real_estate"
    CASH = "cash"


class PositionType(Enum):
    """Position type enumeration."""
    LONG = "long"
    SHORT = "short"
    NEUTRAL = "neutral"


class PositionStatus(Enum):
    """Position status enumeration."""
    ACTIVE = "active"
    CLOSED = "closed"
    PENDING = "pending"
    SUSPENDED = "suspended"


@dataclass
class Asset:
    """Asset data model."""
    id: str
    symbol: str
    name: str
    asset_type: AssetType
    exchange: Optional[str] = None
    currency: str = "USD"
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Position:
    """Position data model."""
    id: str
    portfolio_id: str
    asset_id: str
    asset: Asset
    position_type: PositionType
    quantity: Decimal
    entry_price: Decimal
    current_price: Decimal
    market_value: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
    entry_date: datetime
    status: PositionStatus = PositionStatus.ACTIVE
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None
    risk_level: float = 0.02
    weight_percentage: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    closed_at: Optional[datetime] = None


@dataclass
class PortfolioMetrics:
    """Portfolio metrics data model."""
    total_value: Decimal
    total_invested: Decimal
    total_pnl: Decimal
    total_return_percentage: float
    daily_pnl: Decimal
    daily_return_percentage: float
    positions_count: int
    active_positions: int
    cash_balance: Decimal
    leverage: float
    margin_used: Decimal
    free_margin: Decimal
    last_updated: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Portfolio:
    """Portfolio data model."""
    id: str
    investor_id: str
    fund_id: str
    name: str
    description: Optional[str] = None
    initial_capital: Decimal = Decimal('0')
    current_capital: Decimal = Decimal('0')
    positions: List[Position] = field(default_factory=list)
    metrics: Optional[PortfolioMetrics] = None
    risk_limits: Dict[str, float] = field(default_factory=dict)
    rebalancing_frequency: int = 7  # days
    last_rebalance: Optional[datetime] = None
    next_rebalance: Optional[datetime] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def get_position_by_asset_id(self, asset_id: str) -> Optional[Position]:
        """Get position by asset ID."""
        for position in self.positions:
            if position.asset_id == asset_id and position.status == PositionStatus.ACTIVE:
                return position
        return None

    def get_active_positions(self) -> List[Position]:
        """Get all active positions."""
        return [pos for pos in self.positions if pos.status == PositionStatus.ACTIVE]

    def get_positions_by_type(self, position_type: PositionType) -> List[Position]:
        """Get positions by type."""
        return [pos for pos in self.positions 
                if pos.position_type == position_type and pos.status == PositionStatus.ACTIVE]

    def get_positions_by_asset_type(self, asset_type: AssetType) -> List[Position]:
        """Get positions by asset type."""
        return [pos for pos in self.positions 
                if pos.asset.asset_type == asset_type and pos.status == PositionStatus.ACTIVE]

    def calculate_total_value(self) -> Decimal:
        """Calculate total portfolio value."""
        return sum(pos.market_value for pos in self.get_active_positions())

    def calculate_total_pnl(self) -> Decimal:
        """Calculate total P&L."""
        return sum(pos.unrealized_pnl + pos.realized_pnl for pos in self.positions)

    def calculate_weight_percentages(self) -> Dict[str, float]:
        """Calculate position weight percentages."""
        total_value = self.calculate_total_value()
        if total_value == 0:
            return {}
        
        weights = {}
        for position in self.get_active_positions():
            weights[position.asset_id] = float(position.market_value / total_value * 100)
        return weights

    def get_asset_allocation(self) -> Dict[AssetType, float]:
        """Get asset allocation breakdown."""
        total_value = self.calculate_total_value()
        if total_value == 0:
            return {}
        
        allocation = {}
        for position in self.get_active_positions():
            asset_type = position.asset.asset_type
            if asset_type not in allocation:
                allocation[asset_type] = 0
            allocation[asset_type] += float(position.market_value / total_value * 100)
        
        return allocation

    def get_sector_allocation(self) -> Dict[str, float]:
        """Get sector allocation breakdown."""
        total_value = self.calculate_total_value()
        if total_value == 0:
            return {}
        
        allocation = {}
        for position in self.get_active_positions():
            sector = position.asset.sector or "Unknown"
            if sector not in allocation:
                allocation[sector] = 0
            allocation[sector] += float(position.market_value / total_value * 100)
        
        return allocation

    def update_metrics(self):
        """Update portfolio metrics."""
        active_positions = self.get_active_positions()
        total_value = self.calculate_total_value()
        total_invested = sum(pos.quantity * pos.entry_price for pos in active_positions)
        total_pnl = self.calculate_total_pnl()
        
        total_return_percentage = 0
        if total_invested > 0:
            total_return_percentage = float((total_pnl / total_invested) * 100)
        
        # Calculate daily metrics (simplified)
        daily_pnl = Decimal('0')  # Would be calculated from daily performance
        daily_return_percentage = 0
        if total_value > 0:
            daily_return_percentage = float((daily_pnl / total_value) * 100)
        
        self.metrics = PortfolioMetrics(
            total_value=total_value,
            total_invested=total_invested,
            total_pnl=total_pnl,
            total_return_percentage=total_return_percentage,
            daily_pnl=daily_pnl,
            daily_return_percentage=daily_return_percentage,
            positions_count=len(self.positions),
            active_positions=len(active_positions),
            cash_balance=Decimal('0'),  # Would be calculated from cash positions
            leverage=1.0,  # Would be calculated from margin usage
            margin_used=Decimal('0'),
            free_margin=Decimal('0')
        )
        
        # Update position weight percentages
        for position in active_positions:
            if total_value > 0:
                position.weight_percentage = float(position.market_value / total_value * 100)
