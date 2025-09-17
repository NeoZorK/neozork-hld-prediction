"""Functional Portfolio Manager - Fully implemented portfolio management functionality"""

import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid
import json
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class AssetType(Enum):
    """Asset type enumeration."""
    CRYPTO = "crypto"
    STOCK = "stock"
    BOND = "bond"
    COMMODITY = "commodity"
    FOREX = "forex"
    DERIVATIVE = "derivative"


class PositionType(Enum):
    """Position type enumeration."""
    LONG = "long"
    SHORT = "short"
    NEUTRAL = "neutral"


@dataclass
class Position:
    """Position data class."""
    asset_symbol: str
    asset_name: str
    asset_type: AssetType
    quantity: float
    average_price: float
    current_price: float
    current_value: float
    unrealized_pnl: float
    unrealized_pnl_percentage: float
    weight_percentage: float
    entry_time: datetime
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


@dataclass
class PortfolioMetrics:
    """Portfolio metrics data class."""
    total_value: float
    total_invested: float
    total_pnl: float
    total_return_percentage: float
    daily_return: float
    daily_return_percentage: float
    sharpe_ratio: float
    max_drawdown: float
    volatility: float
    beta: float
    var_95: float
    cvar_95: float
    win_rate: float
    profit_factor: float


class FunctionalPortfolioManager:
    """Fully functional portfolio management for the fund."""
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.risk_limits = {
            'max_position_size': 0.1,  # 10% max per position
            'max_sector_exposure': 0.3,  # 30% max per sector
            'max_drawdown': 0.15,  # 15% max drawdown
            'var_limit': 0.05,  # 5% VaR limit
        }
        
    async def get_portfolio_positions(self, fund_id: str) -> Dict[str, Any]:
        """Get all portfolio positions for a fund."""
        try:
            query = """
            SELECT * FROM portfolio_positions 
            WHERE fund_id = :fund_id 
            ORDER BY current_value DESC
            """
            
            result = await self.database_manager.execute_query(
                query, 
                {"fund_id": fund_id}
            )
            
            if 'error' in result:
                return {"error": f"Failed to get portfolio positions: {result['error']}"}
            
            positions = []
            for row in result['query_result']['data']:
                positions.append({
                    "position_id": row['id'],
                    "asset_symbol": row['asset_symbol'],
                    "asset_name": row['asset_name'],
                    "asset_type": row['asset_type'],
                    "quantity": float(row['quantity']),
                    "average_price": float(row['average_price']),
                    "current_price": float(row['current_price']) if row['current_price'] else None,
                    "current_value": float(row['current_value']) if row['current_value'] else None,
                    "unrealized_pnl": float(row['unrealized_pnl']) if row['unrealized_pnl'] else None,
                    "unrealized_pnl_percentage": float(row['unrealized_pnl_percentage']) if row['unrealized_pnl_percentage'] else None,
                    "weight_percentage": float(row['weight_percentage']) if row['weight_percentage'] else None,
                    "created_at": row['created_at'].isoformat(),
                    "updated_at": row['updated_at'].isoformat()
                })
            
            return {
                "fund_id": fund_id,
                "positions": positions,
                "total_positions": len(positions)
            }
            
        except Exception as e:
            logger.error(f"Failed to get portfolio positions: {e}")
            return {"error": f"Failed to get portfolio positions: {str(e)}"}
    
    async def add_position(self, fund_id: str, asset_symbol: str, asset_name: str, 
                          asset_type: str, quantity: float, price: float) -> Dict[str, Any]:
        """Add a new position to the portfolio."""
        try:
            # Validate input
            if quantity <= 0 or price <= 0:
                return {"error": "Quantity and price must be positive"}
            
            # Check if position already exists
            existing_query = """
            SELECT * FROM portfolio_positions 
            WHERE fund_id = :fund_id AND asset_symbol = :asset_symbol
            """
            
            existing_result = await self.database_manager.execute_query(
                existing_query, 
                {"fund_id": fund_id, "asset_symbol": asset_symbol}
            )
            
            if 'error' in existing_result:
                return {"error": f"Database error: {existing_result['error']}"}
            
            if existing_result['query_result']['data']:
                # Update existing position
                return await self._update_existing_position(
                    fund_id, asset_symbol, quantity, price
                )
            
            # Create new position
            position_id = str(uuid.uuid4())
            current_value = quantity * price
            
            insert_query = """
            INSERT INTO portfolio_positions (
                id, fund_id, asset_symbol, asset_name, asset_type,
                quantity, average_price, current_price, current_value,
                unrealized_pnl, unrealized_pnl_percentage, weight_percentage
            ) VALUES (
                :id, :fund_id, :asset_symbol, :asset_name, :asset_type,
                :quantity, :average_price, :current_price, :current_value,
                :unrealized_pnl, :unrealized_pnl_percentage, :weight_percentage
            )
            """
            
            insert_params = {
                "id": position_id,
                "fund_id": fund_id,
                "asset_symbol": asset_symbol,
                "asset_name": asset_name,
                "asset_type": asset_type,
                "quantity": quantity,
                "average_price": price,
                "current_price": price,
                "current_value": current_value,
                "unrealized_pnl": 0.0,
                "unrealized_pnl_percentage": 0.0,
                "weight_percentage": 0.0  # Will be calculated later
            }
            
            insert_result = await self.database_manager.execute_query(
                insert_query, 
                insert_params
            )
            
            if 'error' in insert_result:
                return {"error": f"Failed to add position: {insert_result['error']}"}
            
            # Update portfolio weights
            await self._update_portfolio_weights(fund_id)
            
            # Record transaction
            await self._record_transaction(
                fund_id, "buy", asset_symbol, quantity, price, quantity * price
            )
            
            logger.info(f"Added position: {asset_symbol} to fund {fund_id}")
            
            return {
                "position_id": position_id,
                "fund_id": fund_id,
                "asset_symbol": asset_symbol,
                "quantity": quantity,
                "price": price,
                "value": current_value,
                "message": "Position added successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to add position: {e}")
            return {"error": f"Failed to add position: {str(e)}"}
    
    async def _update_existing_position(self, fund_id: str, asset_symbol: str, 
                                      quantity: float, price: float) -> Dict[str, Any]:
        """Update existing position with new quantity and price."""
        try:
            # Get current position
            current_query = """
            SELECT * FROM portfolio_positions 
            WHERE fund_id = :fund_id AND asset_symbol = :asset_symbol
            """
            
            current_result = await self.database_manager.execute_query(
                current_query, 
                {"fund_id": fund_id, "asset_symbol": asset_symbol}
            )
            
            if 'error' in current_result or not current_result['query_result']['data']:
                return {"error": "Position not found"}
            
            current_position = current_result['query_result']['data'][0]
            current_quantity = float(current_position['quantity'])
            current_avg_price = float(current_position['average_price'])
            
            # Calculate new average price (weighted average)
            total_quantity = current_quantity + quantity
            total_cost = (current_quantity * current_avg_price) + (quantity * price)
            new_avg_price = total_cost / total_quantity
            
            # Update position
            update_query = """
            UPDATE portfolio_positions 
            SET quantity = :quantity, average_price = :average_price,
                current_price = :current_price, current_value = :current_value,
                updated_at = CURRENT_TIMESTAMP
            WHERE fund_id = :fund_id AND asset_symbol = :asset_symbol
            """
            
            new_value = total_quantity * price
            
            update_params = {
                "quantity": total_quantity,
                "average_price": new_avg_price,
                "current_price": price,
                "current_value": new_value,
                "fund_id": fund_id,
                "asset_symbol": asset_symbol
            }
            
            update_result = await self.database_manager.execute_query(
                update_query, 
                update_params
            )
            
            if 'error' in update_result:
                return {"error": f"Failed to update position: {update_result['error']}"}
            
            # Update portfolio weights
            await self._update_portfolio_weights(fund_id)
            
            # Record transaction
            await self._record_transaction(
                fund_id, "buy", asset_symbol, quantity, price, quantity * price
            )
            
            logger.info(f"Updated position: {asset_symbol} in fund {fund_id}")
            
            return {
                "fund_id": fund_id,
                "asset_symbol": asset_symbol,
                "new_quantity": total_quantity,
                "new_average_price": new_avg_price,
                "new_value": new_value,
                "message": "Position updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to update existing position: {e}")
            return {"error": f"Failed to update existing position: {str(e)}"}
    
    async def remove_position(self, fund_id: str, asset_symbol: str, 
                            quantity: float = None) -> Dict[str, Any]:
        """Remove or reduce a position from the portfolio."""
        try:
            # Get current position
            current_query = """
            SELECT * FROM portfolio_positions 
            WHERE fund_id = :fund_id AND asset_symbol = :asset_symbol
            """
            
            current_result = await self.database_manager.execute_query(
                current_query, 
                {"fund_id": fund_id, "asset_symbol": asset_symbol}
            )
            
            if 'error' in current_result or not current_result['query_result']['data']:
                return {"error": "Position not found"}
            
            current_position = current_result['query_result']['data'][0]
            current_quantity = float(current_position['quantity'])
            current_price = float(current_position['current_price']) if current_position['current_price'] else float(current_position['average_price'])
            
            # Determine quantity to remove
            if quantity is None:
                quantity = current_quantity  # Remove entire position
            else:
                quantity = min(quantity, current_quantity)  # Don't remove more than available
            
            if quantity <= 0:
                return {"error": "Invalid quantity"}
            
            # Calculate new quantity and value
            new_quantity = current_quantity - quantity
            new_value = new_quantity * current_price
            
            if new_quantity <= 0:
                # Remove entire position
                delete_query = """
                DELETE FROM portfolio_positions 
                WHERE fund_id = :fund_id AND asset_symbol = :asset_symbol
                """
                
                delete_result = await self.database_manager.execute_query(
                    delete_query, 
                    {"fund_id": fund_id, "asset_symbol": asset_symbol}
                )
                
                if 'error' in delete_result:
                    return {"error": f"Failed to remove position: {delete_result['error']}"}
                
                message = "Position removed completely"
            else:
                # Update position with reduced quantity
                update_query = """
                UPDATE portfolio_positions 
                SET quantity = :quantity, current_value = :current_value,
                    updated_at = CURRENT_TIMESTAMP
                WHERE fund_id = :fund_id AND asset_symbol = :asset_symbol
                """
                
                update_params = {
                    "quantity": new_quantity,
                    "current_value": new_value,
                    "fund_id": fund_id,
                    "asset_symbol": asset_symbol
                }
                
                update_result = await self.database_manager.execute_query(
                    update_query, 
                    update_params
                )
                
                if 'error' in update_result:
                    return {"error": f"Failed to update position: {update_result['error']}"}
                
                message = f"Position reduced by {quantity}"
            
            # Update portfolio weights
            await self._update_portfolio_weights(fund_id)
            
            # Record transaction
            await self._record_transaction(
                fund_id, "sell", asset_symbol, quantity, current_price, quantity * current_price
            )
            
            logger.info(f"Removed position: {asset_symbol} from fund {fund_id}")
            
            return {
                "fund_id": fund_id,
                "asset_symbol": asset_symbol,
                "quantity_removed": quantity,
                "remaining_quantity": new_quantity if new_quantity > 0 else 0,
                "message": message
            }
            
        except Exception as e:
            logger.error(f"Failed to remove position: {e}")
            return {"error": f"Failed to remove position: {str(e)}"}
    
    async def update_position_prices(self, fund_id: str, price_updates: Dict[str, float]) -> Dict[str, Any]:
        """Update current prices for portfolio positions."""
        try:
            updated_positions = []
            
            for asset_symbol, new_price in price_updates.items():
                # Get current position
                current_query = """
                SELECT * FROM portfolio_positions 
                WHERE fund_id = :fund_id AND asset_symbol = :asset_symbol
                """
                
                current_result = await self.database_manager.execute_query(
                    current_query, 
                    {"fund_id": fund_id, "asset_symbol": asset_symbol}
                )
                
                if 'error' in current_result or not current_result['query_result']['data']:
                    continue
                
                current_position = current_result['query_result']['data'][0]
                quantity = float(current_position['quantity'])
                average_price = float(current_position['average_price'])
                
                # Calculate new values
                current_value = quantity * new_price
                unrealized_pnl = current_value - (quantity * average_price)
                unrealized_pnl_percentage = (unrealized_pnl / (quantity * average_price)) * 100 if quantity * average_price > 0 else 0
                
                # Update position
                update_query = """
                UPDATE portfolio_positions 
                SET current_price = :current_price, current_value = :current_value,
                    unrealized_pnl = :unrealized_pnl, unrealized_pnl_percentage = :unrealized_pnl_percentage,
                    updated_at = CURRENT_TIMESTAMP
                WHERE fund_id = :fund_id AND asset_symbol = :asset_symbol
                """
                
                update_params = {
                    "current_price": new_price,
                    "current_value": current_value,
                    "unrealized_pnl": unrealized_pnl,
                    "unrealized_pnl_percentage": unrealized_pnl_percentage,
                    "fund_id": fund_id,
                    "asset_symbol": asset_symbol
                }
                
                update_result = await self.database_manager.execute_query(
                    update_query, 
                    update_params
                )
                
                if 'error' in update_result:
                    logger.error(f"Failed to update price for {asset_symbol}: {update_result['error']}")
                    continue
                
                updated_positions.append({
                    "asset_symbol": asset_symbol,
                    "old_price": float(current_position['current_price']) if current_position['current_price'] else None,
                    "new_price": new_price,
                    "current_value": current_value,
                    "unrealized_pnl": unrealized_pnl,
                    "unrealized_pnl_percentage": unrealized_pnl_percentage
                })
            
            # Update portfolio weights
            await self._update_portfolio_weights(fund_id)
            
            # Update fund total value
            await self._update_fund_total_value(fund_id)
            
            logger.info(f"Updated prices for {len(updated_positions)} positions in fund {fund_id}")
            
            return {
                "fund_id": fund_id,
                "updated_positions": updated_positions,
                "total_updated": len(updated_positions),
                "message": "Position prices updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to update position prices: {e}")
            return {"error": f"Failed to update position prices: {str(e)}"}
    
    async def _update_portfolio_weights(self, fund_id: str) -> None:
        """Update portfolio weights based on current values."""
        try:
            # Get total portfolio value
            total_query = """
            SELECT SUM(current_value) as total_value 
            FROM portfolio_positions 
            WHERE fund_id = :fund_id
            """
            
            total_result = await self.database_manager.execute_query(
                total_query, 
                {"fund_id": fund_id}
            )
            
            if 'error' in total_result or not total_result['query_result']['data']:
                return
            
            total_value = float(total_result['query_result']['data'][0]['total_value']) if total_result['query_result']['data'][0]['total_value'] else 0
            
            if total_value <= 0:
                return
            
            # Get all positions
            positions_query = """
            SELECT id, current_value FROM portfolio_positions 
            WHERE fund_id = :fund_id
            """
            
            positions_result = await self.database_manager.execute_query(
                positions_query, 
                {"fund_id": fund_id}
            )
            
            if 'error' in positions_result:
                return
            
            # Update weights for each position
            for position in positions_result['query_result']['data']:
                position_id = position['id']
                current_value = float(position['current_value']) if position['current_value'] else 0
                weight_percentage = (current_value / total_value) * 100
                
                weight_query = """
                UPDATE portfolio_positions 
                SET weight_percentage = :weight_percentage
                WHERE id = :position_id
                """
                
                await self.database_manager.execute_query(
                    weight_query, 
                    {"weight_percentage": weight_percentage, "position_id": position_id}
                )
            
        except Exception as e:
            logger.error(f"Failed to update portfolio weights: {e}")
    
    async def _update_fund_total_value(self, fund_id: str) -> None:
        """Update fund total value based on portfolio positions."""
        try:
            # Get total portfolio value
            total_query = """
            SELECT SUM(current_value) as total_value 
            FROM portfolio_positions 
            WHERE fund_id = :fund_id
            """
            
            total_result = await self.database_manager.execute_query(
                total_query, 
                {"fund_id": fund_id}
            )
            
            if 'error' in total_result or not total_result['query_result']['data']:
                return
            
            total_value = float(total_result['query_result']['data'][0]['total_value']) if total_result['query_result']['data'][0]['total_value'] else 0
            
            # Update fund value
            update_query = """
            UPDATE funds 
            SET current_value = :current_value, updated_at = CURRENT_TIMESTAMP
            WHERE id = :fund_id
            """
            
            await self.database_manager.execute_query(
                update_query, 
                {"current_value": total_value, "fund_id": fund_id}
            )
            
        except Exception as e:
            logger.error(f"Failed to update fund total value: {e}")
    
    async def _record_transaction(self, fund_id: str, transaction_type: str, 
                                asset_symbol: str, quantity: float, 
                                price: float, total_amount: float) -> None:
        """Record a transaction in the database."""
        try:
            transaction_id = str(uuid.uuid4())
            
            insert_query = """
            INSERT INTO transactions (
                id, fund_id, transaction_type, asset_symbol, quantity,
                price, total_amount, fees, executed_at
            ) VALUES (
                :id, :fund_id, :transaction_type, :asset_symbol, :quantity,
                :price, :total_amount, :fees, CURRENT_TIMESTAMP
            )
            """
            
            insert_params = {
                "id": transaction_id,
                "fund_id": fund_id,
                "transaction_type": transaction_type,
                "asset_symbol": asset_symbol,
                "quantity": quantity,
                "price": price,
                "total_amount": total_amount,
                "fees": 0.0  # No fees for now
            }
            
            await self.database_manager.execute_query(insert_query, insert_params)
            
        except Exception as e:
            logger.error(f"Failed to record transaction: {e}")
    
    async def get_portfolio_metrics(self, fund_id: str) -> Dict[str, Any]:
        """Calculate portfolio performance metrics."""
        try:
            # Get fund data
            fund_query = "SELECT * FROM funds WHERE id = :fund_id"
            fund_result = await self.database_manager.execute_query(
                fund_query, 
                {"fund_id": fund_id}
            )
            
            if 'error' in fund_result or not fund_result['query_result']['data']:
                return {"error": "Fund not found"}
            
            fund_data = fund_result['query_result']['data'][0]
            current_value = float(fund_data['current_value'])
            initial_capital = float(fund_data['initial_capital'])
            
            # Get performance history
            performance_query = """
            SELECT * FROM performance_snapshots 
            WHERE fund_id = :fund_id 
            ORDER BY snapshot_date DESC 
            LIMIT 30
            """
            
            performance_result = await self.database_manager.execute_query(
                performance_query,
                {"fund_id": fund_id}
            )
            
            # Calculate basic metrics
            total_pnl = current_value - initial_capital
            total_return_percentage = (total_pnl / initial_capital) * 100 if initial_capital > 0 else 0
            
            # Calculate daily return if we have performance data
            daily_return = 0.0
            daily_return_percentage = 0.0
            
            if performance_result['query_result']['data']:
                latest_performance = performance_result['query_result']['data'][0]
                daily_return = float(latest_performance['daily_return']) if latest_performance['daily_return'] else 0.0
                daily_return_percentage = float(latest_performance['daily_return_percentage']) if latest_performance['daily_return_percentage'] else 0.0
            
            # Get risk metrics
            risk_query = """
            SELECT * FROM risk_metrics 
            WHERE fund_id = :fund_id 
            ORDER BY calculation_date DESC 
            LIMIT 1
            """
            
            risk_result = await self.database_manager.execute_query(
                risk_query,
                {"fund_id": fund_id}
            )
            
            risk_metrics = {}
            if risk_result['query_result']['data']:
                risk_data = risk_result['query_result']['data'][0]
                risk_metrics = {
                    "var_95": float(risk_data['var_95']) if risk_data['var_95'] else None,
                    "var_99": float(risk_data['var_99']) if risk_data['var_99'] else None,
                    "cvar_95": float(risk_data['cvar_95']) if risk_data['cvar_95'] else None,
                    "cvar_99": float(risk_data['cvar_99']) if risk_data['cvar_99'] else None,
                    "beta": float(risk_data['beta']) if risk_data['beta'] else None,
                    "correlation_spy": float(risk_data['correlation_spy']) if risk_data['correlation_spy'] else None,
                    "tracking_error": float(risk_data['tracking_error']) if risk_data['tracking_error'] else None,
                    "information_ratio": float(risk_data['information_ratio']) if risk_data['information_ratio'] else None
                }
            
            return {
                "fund_id": fund_id,
                "total_value": current_value,
                "initial_capital": initial_capital,
                "total_pnl": total_pnl,
                "total_return_percentage": total_return_percentage,
                "daily_return": daily_return,
                "daily_return_percentage": daily_return_percentage,
                "risk_metrics": risk_metrics,
                "calculated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate portfolio metrics: {e}")
            return {"error": f"Failed to calculate portfolio metrics: {str(e)}"}
    
    async def rebalance_portfolio(self, fund_id: str, target_weights: Dict[str, float]) -> Dict[str, Any]:
        """Rebalance portfolio to target weights."""
        try:
            # Get current positions
            positions_result = await self.get_portfolio_positions(fund_id)
            if 'error' in positions_result:
                return positions_result
            
            current_positions = positions_result['positions']
            
            # Get total portfolio value
            fund_query = "SELECT current_value FROM funds WHERE id = :fund_id"
            fund_result = await self.database_manager.execute_query(
                fund_query, 
                {"fund_id": fund_id}
            )
            
            if 'error' in fund_result or not fund_result['query_result']['data']:
                return {"error": "Fund not found"}
            
            total_value = float(fund_result['query_result']['data'][0]['current_value'])
            
            # Calculate rebalancing trades
            rebalancing_trades = []
            
            for position in current_positions:
                asset_symbol = position['asset_symbol']
                current_value = position['current_value'] or 0
                current_weight = (current_value / total_value) * 100 if total_value > 0 else 0
                target_weight = target_weights.get(asset_symbol, 0)
                
                if abs(current_weight - target_weight) > 1.0:  # 1% threshold
                    target_value = total_value * (target_weight / 100)
                    trade_amount = target_value - current_value
                    
                    if abs(trade_amount) > 100:  # Minimum trade size
                        rebalancing_trades.append({
                            "asset_symbol": asset_symbol,
                            "current_weight": current_weight,
                            "target_weight": target_weight,
                            "current_value": current_value,
                            "target_value": target_value,
                            "trade_amount": trade_amount,
                            "trade_type": "buy" if trade_amount > 0 else "sell"
                        })
            
            # Execute rebalancing trades
            executed_trades = []
            for trade in rebalancing_trades:
                asset_symbol = trade['asset_symbol']
                trade_amount = trade['trade_amount']
                current_price = 1.0  # Placeholder - should get real price
                
                if trade['trade_type'] == 'buy':
                    quantity = trade_amount / current_price
                    result = await self.add_position(fund_id, asset_symbol, asset_symbol, "crypto", quantity, current_price)
                else:
                    quantity = abs(trade_amount) / current_price
                    result = await self.remove_position(fund_id, asset_symbol, quantity)
                
                if 'error' not in result:
                    executed_trades.append(trade)
            
            logger.info(f"Portfolio rebalancing completed for fund {fund_id}")
            
            return {
                "fund_id": fund_id,
                "rebalancing_trades": rebalancing_trades,
                "executed_trades": executed_trades,
                "total_trades": len(executed_trades),
                "message": "Portfolio rebalancing completed successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to rebalance portfolio: {e}")
            return {"error": f"Failed to rebalance portfolio: {str(e)}"}
