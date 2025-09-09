"""
Portfolio Operations - Core Portfolio Operations

This module provides core portfolio operations including portfolio calculations,
validations, and utility functions.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import math

from ..models.portfolio_models import Portfolio, Position, AssetType, PositionType, PositionStatus

logger = logging.getLogger(__name__)


class PortfolioOperations:
    """Core portfolio operations and calculations."""
    
    def __init__(self):
        pass
    
    def calculate_portfolio_value(self, portfolio: Portfolio) -> Decimal:
        """Calculate total portfolio value."""
        try:
            total_value = Decimal('0')
            for position in portfolio.get_active_positions():
                total_value += position.market_value
            return total_value
        except Exception as e:
            logger.error(f"Failed to calculate portfolio value: {e}")
            return Decimal('0')
    
    def calculate_portfolio_pnl(self, portfolio: Portfolio) -> Decimal:
        """Calculate total portfolio P&L."""
        try:
            total_pnl = Decimal('0')
            for position in portfolio.positions:
                total_pnl += position.unrealized_pnl + position.realized_pnl
            return total_pnl
        except Exception as e:
            logger.error(f"Failed to calculate portfolio P&L: {e}")
            return Decimal('0')
    
    def calculate_portfolio_return(self, portfolio: Portfolio) -> float:
        """Calculate total portfolio return percentage."""
        try:
            total_invested = sum(pos.quantity * pos.entry_price for pos in portfolio.get_active_positions())
            if total_invested == 0:
                return 0.0
            
            total_pnl = self.calculate_portfolio_pnl(portfolio)
            return float((total_pnl / total_invested) * 100)
        except Exception as e:
            logger.error(f"Failed to calculate portfolio return: {e}")
            return 0.0
    
    def calculate_daily_return(self, portfolio: Portfolio, previous_value: Decimal) -> float:
        """Calculate daily return percentage."""
        try:
            current_value = self.calculate_portfolio_value(portfolio)
            if previous_value == 0:
                return 0.0
            
            return float(((current_value - previous_value) / previous_value) * 100)
        except Exception as e:
            logger.error(f"Failed to calculate daily return: {e}")
            return 0.0
    
    def calculate_position_weights(self, portfolio: Portfolio) -> Dict[str, float]:
        """Calculate position weight percentages."""
        try:
            total_value = self.calculate_portfolio_value(portfolio)
            if total_value == 0:
                return {}
            
            weights = {}
            for position in portfolio.get_active_positions():
                weight = float((position.market_value / total_value) * 100)
                weights[position.asset_id] = weight
            
            return weights
        except Exception as e:
            logger.error(f"Failed to calculate position weights: {e}")
            return {}
    
    def calculate_asset_allocation(self, portfolio: Portfolio) -> Dict[AssetType, float]:
        """Calculate asset allocation breakdown."""
        try:
            total_value = self.calculate_portfolio_value(portfolio)
            if total_value == 0:
                return {}
            
            allocation = {}
            for position in portfolio.get_active_positions():
                asset_type = position.asset.asset_type
                if asset_type not in allocation:
                    allocation[asset_type] = 0
                allocation[asset_type] += float((position.market_value / total_value) * 100)
            
            return allocation
        except Exception as e:
            logger.error(f"Failed to calculate asset allocation: {e}")
            return {}
    
    def calculate_sector_allocation(self, portfolio: Portfolio) -> Dict[str, float]:
        """Calculate sector allocation breakdown."""
        try:
            total_value = self.calculate_portfolio_value(portfolio)
            if total_value == 0:
                return {}
            
            allocation = {}
            for position in portfolio.get_active_positions():
                sector = position.asset.sector or "Unknown"
                if sector not in allocation:
                    allocation[sector] = 0
                allocation[sector] += float((position.market_value / total_value) * 100)
            
            return allocation
        except Exception as e:
            logger.error(f"Failed to calculate sector allocation: {e}")
            return {}
    
    def calculate_concentration_risk(self, portfolio: Portfolio) -> Dict[str, float]:
        """Calculate concentration risk metrics."""
        try:
            weights = self.calculate_position_weights(portfolio)
            if not weights:
                return {}
            
            # Herfindahl-Hirschman Index
            hhi = sum(weight ** 2 for weight in weights.values())
            
            # Maximum position weight
            max_weight = max(weights.values()) if weights else 0
            
            # Number of positions
            num_positions = len(weights)
            
            # Effective number of positions
            effective_positions = 1 / hhi if hhi > 0 else 0
            
            return {
                'herfindahl_index': hhi,
                'max_position_weight': max_weight,
                'num_positions': num_positions,
                'effective_positions': effective_positions,
                'concentration_ratio': max_weight
            }
        except Exception as e:
            logger.error(f"Failed to calculate concentration risk: {e}")
            return {}
    
    def calculate_leverage(self, portfolio: Portfolio) -> float:
        """Calculate portfolio leverage."""
        try:
            # This is a simplified calculation
            # In practice, leverage would be calculated based on margin usage
            total_value = self.calculate_portfolio_value(portfolio)
            cash_balance = portfolio.metrics.cash_balance if portfolio.metrics else Decimal('0')
            
            if cash_balance == 0:
                return 1.0
            
            return float(total_value / cash_balance)
        except Exception as e:
            logger.error(f"Failed to calculate leverage: {e}")
            return 1.0
    
    def validate_position_size_limits(self, portfolio: Portfolio) -> List[Dict[str, Any]]:
        """Validate position size limits."""
        try:
            violations = []
            max_position_size = portfolio.risk_limits.get('max_position_size', 0.1)
            
            weights = self.calculate_position_weights(portfolio)
            for asset_id, weight in weights.items():
                if weight > max_position_size * 100:
                    violations.append({
                        'type': 'position_size',
                        'asset_id': asset_id,
                        'current_weight': weight,
                        'limit': max_position_size * 100,
                        'excess': weight - (max_position_size * 100)
                    })
            
            return violations
        except Exception as e:
            logger.error(f"Failed to validate position size limits: {e}")
            return []
    
    def validate_sector_limits(self, portfolio: Portfolio) -> List[Dict[str, Any]]:
        """Validate sector exposure limits."""
        try:
            violations = []
            max_sector_exposure = portfolio.risk_limits.get('max_sector_exposure', 0.3)
            
            sector_allocation = self.calculate_sector_allocation(portfolio)
            for sector, weight in sector_allocation.items():
                if weight > max_sector_exposure * 100:
                    violations.append({
                        'type': 'sector_exposure',
                        'sector': sector,
                        'current_weight': weight,
                        'limit': max_sector_exposure * 100,
                        'excess': weight - (max_sector_exposure * 100)
                    })
            
            return violations
        except Exception as e:
            logger.error(f"Failed to validate sector limits: {e}")
            return []
    
    def validate_leverage_limits(self, portfolio: Portfolio) -> List[Dict[str, Any]]:
        """Validate leverage limits."""
        try:
            violations = []
            max_leverage = portfolio.risk_limits.get('leverage_limit', 2.0)
            
            current_leverage = self.calculate_leverage(portfolio)
            if current_leverage > max_leverage:
                violations.append({
                    'type': 'leverage',
                    'current_leverage': current_leverage,
                    'limit': max_leverage,
                    'excess': current_leverage - max_leverage
                })
            
            return violations
        except Exception as e:
            logger.error(f"Failed to validate leverage limits: {e}")
            return []
    
    def validate_all_limits(self, portfolio: Portfolio) -> Dict[str, Any]:
        """Validate all portfolio limits."""
        try:
            position_violations = self.validate_position_size_limits(portfolio)
            sector_violations = self.validate_sector_limits(portfolio)
            leverage_violations = self.validate_leverage_limits(portfolio)
            
            all_violations = position_violations + sector_violations + leverage_violations
            
            return {
                'is_valid': len(all_violations) == 0,
                'violations': all_violations,
                'position_violations': position_violations,
                'sector_violations': sector_violations,
                'leverage_violations': leverage_violations
            }
        except Exception as e:
            logger.error(f"Failed to validate all limits: {e}")
            return {'is_valid': False, 'violations': []}
    
    def calculate_rebalancing_needs(
        self, 
        portfolio: Portfolio, 
        target_allocations: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Calculate rebalancing needs based on target allocations."""
        try:
            current_weights = self.calculate_position_weights(portfolio)
            rebalancing_actions = []
            
            # Check each target allocation
            for asset_id, target_weight in target_allocations.items():
                current_weight = current_weights.get(asset_id, 0)
                weight_diff = target_weight - current_weight
                
                if abs(weight_diff) > 0.01:  # 1% threshold
                    total_value = self.calculate_portfolio_value(portfolio)
                    required_trade_value = total_value * (weight_diff / 100)
                    
                    rebalancing_actions.append({
                        'asset_id': asset_id,
                        'current_weight': current_weight,
                        'target_weight': target_weight,
                        'weight_difference': weight_diff,
                        'required_trade_value': float(required_trade_value),
                        'action': 'buy' if weight_diff > 0 else 'sell'
                    })
            
            return rebalancing_actions
        except Exception as e:
            logger.error(f"Failed to calculate rebalancing needs: {e}")
            return []
    
    def calculate_portfolio_statistics(self, portfolio: Portfolio) -> Dict[str, Any]:
        """Calculate comprehensive portfolio statistics."""
        try:
            total_value = self.calculate_portfolio_value(portfolio)
            total_pnl = self.calculate_portfolio_pnl(portfolio)
            total_return = self.calculate_portfolio_return(portfolio)
            
            weights = self.calculate_position_weights(portfolio)
            asset_allocation = self.calculate_asset_allocation(portfolio)
            sector_allocation = self.calculate_sector_allocation(portfolio)
            concentration_risk = self.calculate_concentration_risk(portfolio)
            leverage = self.calculate_leverage(portfolio)
            
            return {
                'total_value': float(total_value),
                'total_pnl': float(total_pnl),
                'total_return_percentage': total_return,
                'position_weights': weights,
                'asset_allocation': {k.value: v for k, v in asset_allocation.items()},
                'sector_allocation': sector_allocation,
                'concentration_risk': concentration_risk,
                'leverage': leverage,
                'positions_count': len(portfolio.get_active_positions()),
                'total_positions': len(portfolio.positions)
            }
        except Exception as e:
            logger.error(f"Failed to calculate portfolio statistics: {e}")
            return {}
    
    def get_top_positions(self, portfolio: Portfolio, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top positions by market value."""
        try:
            positions = portfolio.get_active_positions()
            sorted_positions = sorted(positions, key=lambda p: p.market_value, reverse=True)
            
            top_positions = []
            for position in sorted_positions[:limit]:
                top_positions.append({
                    'asset_id': position.asset_id,
                    'asset_name': position.asset.name,
                    'market_value': float(position.market_value),
                    'weight_percentage': position.weight_percentage,
                    'unrealized_pnl': float(position.unrealized_pnl),
                    'return_percentage': float((position.current_price - position.entry_price) / position.entry_price * 100) if position.entry_price > 0 else 0
                })
            
            return top_positions
        except Exception as e:
            logger.error(f"Failed to get top positions: {e}")
            return []
    
    def get_bottom_positions(self, portfolio: Portfolio, limit: int = 5) -> List[Dict[str, Any]]:
        """Get bottom positions by market value."""
        try:
            positions = portfolio.get_active_positions()
            sorted_positions = sorted(positions, key=lambda p: p.market_value)
            
            bottom_positions = []
            for position in sorted_positions[:limit]:
                bottom_positions.append({
                    'asset_id': position.asset_id,
                    'asset_name': position.asset.name,
                    'market_value': float(position.market_value),
                    'weight_percentage': position.weight_percentage,
                    'unrealized_pnl': float(position.unrealized_pnl),
                    'return_percentage': float((position.current_price - position.entry_price) / position.entry_price * 100) if position.entry_price > 0 else 0
                })
            
            return bottom_positions
        except Exception as e:
            logger.error(f"Failed to get bottom positions: {e}")
            return []
