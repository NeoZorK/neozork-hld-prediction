"""
Portfolio Manager - Core Portfolio Management

This module provides the core portfolio management functionality including
portfolio creation, updates, and basic operations.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from decimal import Decimal

from ..models.portfolio_models import Portfolio, Position, Asset, AssetType, PositionType, PositionStatus
from ..models.performance_models import PerformanceMetrics, RiskMetrics
from ..models.transaction_models import Transaction, TransactionType, TransactionStatus

logger = logging.getLogger(__name__)


class PortfolioManager:
    """Core portfolio management functionality."""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self.portfolios: Dict[str, Portfolio] = {}
        
    async def create_portfolio(
        self, 
        investor_id: str, 
        fund_id: str, 
        name: str,
        initial_capital: Decimal = Decimal('0'),
        description: Optional[str] = None
    ) -> Portfolio:
        """Create a new portfolio."""
        try:
            portfolio_id = f"portfolio_{investor_id}_{fund_id}_{datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M%S')}"
            
            portfolio = Portfolio(
                id=portfolio_id,
                investor_id=investor_id,
                fund_id=fund_id,
                name=name,
                description=description,
                initial_capital=initial_capital,
                current_capital=initial_capital
            )
            
            # Set default risk limits
            portfolio.risk_limits = {
                'max_position_size': 0.1,  # 10% max per position
                'max_sector_exposure': 0.3,  # 30% max per sector
                'max_drawdown': 0.15,  # 15% max drawdown
                'var_limit': 0.05,  # 5% VaR limit
                'leverage_limit': 2.0  # 2x max leverage
            }
            
            # Save to database if available
            if self.db_manager:
                await self._save_portfolio_to_db(portfolio)
            
            self.portfolios[portfolio_id] = portfolio
            
            logger.info(f"Created portfolio {portfolio_id} for investor {investor_id}")
            return portfolio
            
        except Exception as e:
            logger.error(f"Failed to create portfolio: {e}")
            raise
    
    async def get_portfolio(self, portfolio_id: str) -> Optional[Portfolio]:
        """Get portfolio by ID."""
        try:
            if portfolio_id in self.portfolios:
                return self.portfolios[portfolio_id]
            
            # Load from database if available
            if self.db_manager:
                portfolio = await self._load_portfolio_from_db(portfolio_id)
                if portfolio:
                    self.portfolios[portfolio_id] = portfolio
                    return portfolio
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get portfolio {portfolio_id}: {e}")
            return None
    
    async def update_portfolio(self, portfolio: Portfolio) -> bool:
        """Update portfolio."""
        try:
            portfolio.updated_at = datetime.now(datetime.UTC)
            
            # Update metrics
            portfolio.update_metrics()
            
            # Save to database if available
            if self.db_manager:
                await self._update_portfolio_in_db(portfolio)
            
            self.portfolios[portfolio.id] = portfolio
            
            logger.info(f"Updated portfolio {portfolio.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update portfolio {portfolio.id}: {e}")
            return False
    
    async def delete_portfolio(self, portfolio_id: str) -> bool:
        """Delete portfolio."""
        try:
            if portfolio_id in self.portfolios:
                del self.portfolios[portfolio_id]
            
            # Delete from database if available
            if self.db_manager:
                await self._delete_portfolio_from_db(portfolio_id)
            
            logger.info(f"Deleted portfolio {portfolio_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete portfolio {portfolio_id}: {e}")
            return False
    
    async def get_portfolio_by_fund(self, fund_id: str) -> List[Portfolio]:
        """Get all portfolios for a fund."""
        try:
            portfolios = []
            
            # Check in-memory portfolios
            for portfolio in self.portfolios.values():
                if portfolio.fund_id == fund_id:
                    portfolios.append(portfolio)
            
            # Load from database if available
            if self.db_manager:
                db_portfolios = await self._load_portfolios_by_fund_from_db(fund_id)
                for portfolio in db_portfolios:
                    if portfolio.id not in self.portfolios:
                        self.portfolios[portfolio.id] = portfolio
                        portfolios.append(portfolio)
            
            return portfolios
            
        except Exception as e:
            logger.error(f"Failed to get portfolios for fund {fund_id}: {e}")
            return []
    
    async def get_portfolio_by_investor(self, investor_id: str) -> List[Portfolio]:
        """Get all portfolios for an investor."""
        try:
            portfolios = []
            
            # Check in-memory portfolios
            for portfolio in self.portfolios.values():
                if portfolio.investor_id == investor_id:
                    portfolios.append(portfolio)
            
            # Load from database if available
            if self.db_manager:
                db_portfolios = await self._load_portfolios_by_investor_from_db(investor_id)
                for portfolio in db_portfolios:
                    if portfolio.id not in self.portfolios:
                        self.portfolios[portfolio.id] = portfolio
                        portfolios.append(portfolio)
            
            return portfolios
            
        except Exception as e:
            logger.error(f"Failed to get portfolios for investor {investor_id}: {e}")
            return []
    
    async def calculate_portfolio_metrics(self, portfolio: Portfolio) -> Dict[str, Any]:
        """Calculate comprehensive portfolio metrics."""
        try:
            portfolio.update_metrics()
            
            if not portfolio.metrics:
                return {}
            
            metrics = {
                'total_value': float(portfolio.metrics.total_value),
                'total_invested': float(portfolio.metrics.total_invested),
                'total_pnl': float(portfolio.metrics.total_pnl),
                'total_return_percentage': portfolio.metrics.total_return_percentage,
                'daily_pnl': float(portfolio.metrics.daily_pnl),
                'daily_return_percentage': portfolio.metrics.daily_return_percentage,
                'positions_count': portfolio.metrics.positions_count,
                'active_positions': portfolio.metrics.active_positions,
                'cash_balance': float(portfolio.metrics.cash_balance),
                'leverage': portfolio.metrics.leverage,
                'asset_allocation': portfolio.get_asset_allocation(),
                'sector_allocation': portfolio.get_sector_allocation(),
                'position_weights': portfolio.calculate_weight_percentages()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate portfolio metrics: {e}")
            return {}
    
    async def validate_portfolio_limits(self, portfolio: Portfolio) -> Dict[str, Any]:
        """Validate portfolio against risk limits."""
        try:
            violations = []
            warnings = []
            
            # Check position size limits
            max_position_size = portfolio.risk_limits.get('max_position_size', 0.1)
            for position in portfolio.get_active_positions():
                if position.weight_percentage > max_position_size * 100:
                    violations.append({
                        'type': 'position_size',
                        'asset_id': position.asset_id,
                        'current_weight': position.weight_percentage,
                        'limit': max_position_size * 100
                    })
            
            # Check sector exposure limits
            max_sector_exposure = portfolio.risk_limits.get('max_sector_exposure', 0.3)
            sector_allocation = portfolio.get_sector_allocation()
            for sector, weight in sector_allocation.items():
                if weight > max_sector_exposure * 100:
                    violations.append({
                        'type': 'sector_exposure',
                        'sector': sector,
                        'current_weight': weight,
                        'limit': max_sector_exposure * 100
                    })
            
            # Check leverage limits
            max_leverage = portfolio.risk_limits.get('leverage_limit', 2.0)
            if portfolio.metrics and portfolio.metrics.leverage > max_leverage:
                violations.append({
                    'type': 'leverage',
                    'current_leverage': portfolio.metrics.leverage,
                    'limit': max_leverage
                })
            
            return {
                'is_valid': len(violations) == 0,
                'violations': violations,
                'warnings': warnings
            }
            
        except Exception as e:
            logger.error(f"Failed to validate portfolio limits: {e}")
            return {'is_valid': False, 'violations': [], 'warnings': []}
    
    # Database helper methods
    async def _save_portfolio_to_db(self, portfolio: Portfolio):
        """Save portfolio to database."""
        if not self.db_manager:
            return
        
        query = """
            INSERT INTO portfolios (
                id, investor_id, fund_id, name, description, initial_capital,
                current_capital, risk_limits, rebalancing_frequency, is_active,
                created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        """
        
        await self.db_manager.execute_command(query, {
            '1': portfolio.id,
            '2': portfolio.investor_id,
            '3': portfolio.fund_id,
            '4': portfolio.name,
            '5': portfolio.description,
            '6': portfolio.initial_capital,
            '7': portfolio.current_capital,
            '8': str(portfolio.risk_limits),
            '9': portfolio.rebalancing_frequency,
            '10': portfolio.is_active,
            '11': portfolio.created_at,
            '12': portfolio.updated_at
        })
    
    async def _load_portfolio_from_db(self, portfolio_id: str) -> Optional[Portfolio]:
        """Load portfolio from database."""
        if not self.db_manager:
            return None
        
        query = "SELECT * FROM portfolios WHERE id = $1"
        result = await self.db_manager.execute_query(query, {'1': portfolio_id})
        
        if not result:
            return None
        
        data = result[0]
        # Convert database row to Portfolio object
        # This would need proper implementation based on your database schema
        return None  # Placeholder
    
    async def _update_portfolio_in_db(self, portfolio: Portfolio):
        """Update portfolio in database."""
        if not self.db_manager:
            return
        
        query = """
            UPDATE portfolios SET
                name = $2, description = $3, current_capital = $4,
                risk_limits = $5, rebalancing_frequency = $6, is_active = $7,
                updated_at = $8
            WHERE id = $1
        """
        
        await self.db_manager.execute_command(query, {
            '1': portfolio.id,
            '2': portfolio.name,
            '3': portfolio.description,
            '4': portfolio.current_capital,
            '5': str(portfolio.risk_limits),
            '6': portfolio.rebalancing_frequency,
            '7': portfolio.is_active,
            '8': portfolio.updated_at
        })
    
    async def _delete_portfolio_from_db(self, portfolio_id: str):
        """Delete portfolio from database."""
        if not self.db_manager:
            return
        
        query = "DELETE FROM portfolios WHERE id = $1"
        await self.db_manager.execute_command(query, {'1': portfolio_id})
    
    async def _load_portfolios_by_fund_from_db(self, fund_id: str) -> List[Portfolio]:
        """Load portfolios by fund from database."""
        if not self.db_manager:
            return []
        
        query = "SELECT * FROM portfolios WHERE fund_id = $1"
        result = await self.db_manager.execute_query(query, {'1': fund_id})
        
        portfolios = []
        for data in result:
            # Convert database row to Portfolio object
            # This would need proper implementation
            pass
        
        return portfolios
    
    async def _load_portfolios_by_investor_from_db(self, investor_id: str) -> List[Portfolio]:
        """Load portfolios by investor from database."""
        if not self.db_manager:
            return []
        
        query = "SELECT * FROM portfolios WHERE investor_id = $1"
        result = await self.db_manager.execute_query(query, {'1': investor_id})
        
        portfolios = []
        for data in result:
            # Convert database row to Portfolio object
            # This would need proper implementation
            pass
        
        return portfolios
