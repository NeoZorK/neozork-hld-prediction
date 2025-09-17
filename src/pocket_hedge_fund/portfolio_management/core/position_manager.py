"""
Position Manager - Position Management Operations

This module provides position management functionality including adding,
updating, and closing positions.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
from decimal import Decimal
import uuid

from ..models.portfolio_models import Portfolio, Position, Asset, AssetType, PositionType, PositionStatus
from ..models.transaction_models import Transaction, TransactionType, TransactionStatus

logger = logging.getLogger(__name__)


class PositionManager:
    """Position management functionality."""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        
    async def add_position(
        self,
        portfolio: Portfolio,
        asset: Asset,
        position_type: PositionType,
        quantity: Decimal,
        entry_price: Decimal,
        stop_loss: Optional[Decimal] = None,
        take_profit: Optional[Decimal] = None,
        risk_level: float = 0.02
    ) -> Position:
        """Add a new position to the portfolio."""
        try:
            # Check if position already exists
            existing_position = portfolio.get_position_by_asset_id(asset.id)
            if existing_position:
                raise ValueError(f"Position for asset {asset.id} already exists")
            
            # Create new position
            position_id = str(uuid.uuid4())
            market_value = quantity * entry_price
            
            position = Position(
                id=position_id,
                portfolio_id=portfolio.id,
                asset_id=asset.id,
                asset=asset,
                position_type=position_type,
                quantity=quantity,
                entry_price=entry_price,
                current_price=entry_price,
                market_value=market_value,
                unrealized_pnl=Decimal('0'),
                realized_pnl=Decimal('0'),
                entry_date=datetime.now(timezone.utc),
                stop_loss=stop_loss,
                take_profit=take_profit,
                risk_level=risk_level
            )
            
            # Add to portfolio
            portfolio.positions.append(position)
            
            # Update portfolio metrics
            portfolio.update_metrics()
            
            # Save to database if available
            if self.db_manager:
                await self._save_position_to_db(position)
                await self._create_transaction_record(position, TransactionType.BUY)
            
            logger.info(f"Added position {position_id} for asset {asset.id}")
            return position
            
        except Exception as e:
            logger.error(f"Failed to add position: {e}")
            raise
    
    async def update_position(
        self,
        position: Position,
        quantity: Optional[Decimal] = None,
        stop_loss: Optional[Decimal] = None,
        take_profit: Optional[Decimal] = None,
        risk_level: Optional[float] = None
    ) -> bool:
        """Update an existing position."""
        try:
            updated = False
            
            if quantity is not None:
                position.quantity = quantity
                position.market_value = quantity * position.current_price
                updated = True
            
            if stop_loss is not None:
                position.stop_loss = stop_loss
                updated = True
            
            if take_profit is not None:
                position.take_profit = take_profit
                updated = True
            
            if risk_level is not None:
                position.risk_level = risk_level
                updated = True
            
            if updated:
                position.updated_at = datetime.now(timezone.utc)
                
                # Save to database if available
                if self.db_manager:
                    await self._update_position_in_db(position)
            
            logger.info(f"Updated position {position.id}")
            return updated
            
        except Exception as e:
            logger.error(f"Failed to update position {position.id}: {e}")
            return False
    
    async def close_position(
        self,
        position: Position,
        close_price: Optional[Decimal] = None,
        close_quantity: Optional[Decimal] = None
    ) -> Transaction:
        """Close a position."""
        try:
            if position.status != PositionStatus.ACTIVE:
                raise ValueError(f"Position {position.id} is not active")
            
            # Use current price if close price not provided
            if close_price is None:
                close_price = position.current_price
            
            # Use full quantity if close quantity not provided
            if close_quantity is None:
                close_quantity = position.quantity
            
            # Calculate realized P&L
            if position.position_type == PositionType.LONG:
                realized_pnl = (close_price - position.entry_price) * close_quantity
            else:  # SHORT
                realized_pnl = (position.entry_price - close_price) * close_quantity
            
            # Update position
            position.realized_pnl += realized_pnl
            position.quantity -= close_quantity
            
            if position.quantity <= 0:
                position.status = PositionStatus.CLOSED
                position.closed_at = datetime.now(timezone.utc)
            else:
                # Partial close - update entry price using weighted average
                remaining_value = position.quantity * position.entry_price
                closed_value = close_quantity * close_price
                position.entry_price = (remaining_value + closed_value) / position.quantity
            
            position.updated_at = datetime.now(timezone.utc)
            
            # Create transaction record
            transaction = Transaction(
                id=str(uuid.uuid4()),
                portfolio_id=position.portfolio_id,
                transaction_type=TransactionType.SELL,
                asset_id=position.asset_id,
                quantity=close_quantity,
                price=close_price,
                total_amount=close_quantity * close_price,
                fees=Decimal('0'),  # Would be calculated based on broker
                net_amount=close_quantity * close_price,
                status=TransactionStatus.EXECUTED,
                execution_date=datetime.now(timezone.utc)
            )
            
            # Save to database if available
            if self.db_manager:
                await self._update_position_in_db(position)
                await self._save_transaction_to_db(transaction)
            
            logger.info(f"Closed position {position.id}, realized P&L: {realized_pnl}")
            return transaction
            
        except Exception as e:
            logger.error(f"Failed to close position {position.id}: {e}")
            raise
    
    async def update_position_prices(
        self,
        portfolio: Portfolio,
        price_updates: Dict[str, Decimal]
    ) -> bool:
        """Update position prices with current market prices."""
        try:
            updated_positions = []
            
            for position in portfolio.get_active_positions():
                if position.asset_id in price_updates:
                    old_price = position.current_price
                    new_price = price_updates[position.asset_id]
                    
                    # Update position
                    position.current_price = new_price
                    position.market_value = position.quantity * new_price
                    
                    # Calculate unrealized P&L
                    if position.position_type == PositionType.LONG:
                        position.unrealized_pnl = (new_price - position.entry_price) * position.quantity
                    else:  # SHORT
                        position.unrealized_pnl = (position.entry_price - new_price) * position.quantity
                    
                    position.updated_at = datetime.now(timezone.utc)
                    updated_positions.append(position)
            
            # Update portfolio metrics
            portfolio.update_metrics()
            
            # Save to database if available
            if self.db_manager:
                for position in updated_positions:
                    await self._update_position_in_db(position)
            
            logger.info(f"Updated prices for {len(updated_positions)} positions")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update position prices: {e}")
            return False
    
    async def check_stop_loss_take_profit(
        self,
        portfolio: Portfolio,
        price_updates: Dict[str, Decimal]
    ) -> List[Position]:
        """Check for stop loss and take profit triggers."""
        try:
            triggered_positions = []
            
            for position in portfolio.get_active_positions():
                if position.asset_id not in price_updates:
                    continue
                
                current_price = price_updates[position.asset_id]
                should_close = False
                close_reason = ""
                
                # Check stop loss
                if position.stop_loss is not None:
                    if position.position_type == PositionType.LONG and current_price <= position.stop_loss:
                        should_close = True
                        close_reason = "stop_loss"
                    elif position.position_type == PositionType.SHORT and current_price >= position.stop_loss:
                        should_close = True
                        close_reason = "stop_loss"
                
                # Check take profit
                if position.take_profit is not None and not should_close:
                    if position.position_type == PositionType.LONG and current_price >= position.take_profit:
                        should_close = True
                        close_reason = "take_profit"
                    elif position.position_type == PositionType.SHORT and current_price <= position.take_profit:
                        should_close = True
                        close_reason = "take_profit"
                
                if should_close:
                    triggered_positions.append({
                        'position': position,
                        'close_reason': close_reason,
                        'trigger_price': current_price
                    })
            
            return triggered_positions
            
        except Exception as e:
            logger.error(f"Failed to check stop loss/take profit: {e}")
            return []
    
    async def get_position_performance(self, position: Position) -> Dict[str, Any]:
        """Get position performance metrics."""
        try:
            total_pnl = position.unrealized_pnl + position.realized_pnl
            return_percentage = 0
            
            if position.entry_price > 0:
                if position.position_type == PositionType.LONG:
                    return_percentage = float((position.current_price - position.entry_price) / position.entry_price * 100)
                else:  # SHORT
                    return_percentage = float((position.entry_price - position.current_price) / position.entry_price * 100)
            
            days_held = (datetime.now(timezone.utc) - position.entry_date).days
            
            return {
                'position_id': position.id,
                'asset_id': position.asset_id,
                'asset_name': position.asset.name,
                'position_type': position.position_type.value,
                'quantity': float(position.quantity),
                'entry_price': float(position.entry_price),
                'current_price': float(position.current_price),
                'market_value': float(position.market_value),
                'unrealized_pnl': float(position.unrealized_pnl),
                'realized_pnl': float(position.realized_pnl),
                'total_pnl': float(total_pnl),
                'return_percentage': return_percentage,
                'weight_percentage': position.weight_percentage,
                'days_held': days_held,
                'entry_date': position.entry_date.isoformat(),
                'status': position.status.value
            }
            
        except Exception as e:
            logger.error(f"Failed to get position performance: {e}")
            return {}
    
    # Database helper methods
    async def _save_position_to_db(self, position: Position):
        """Save position to database."""
        if not self.db_manager:
            return
        
        query = """
            INSERT INTO portfolio_positions (
                id, portfolio_id, asset_id, asset_name, asset_type, position_type,
                quantity, entry_price, current_price, market_value, unrealized_pnl,
                realized_pnl, entry_date, stop_loss, take_profit, risk_level, status
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
        """
        
        await self.db_manager.execute_command(query, {
            '1': position.id,
            '2': position.portfolio_id,
            '3': position.asset_id,
            '4': position.asset.name,
            '5': position.asset.asset_type.value,
            '6': position.position_type.value,
            '7': position.quantity,
            '8': position.entry_price,
            '9': position.current_price,
            '10': position.market_value,
            '11': position.unrealized_pnl,
            '12': position.realized_pnl,
            '13': position.entry_date,
            '14': position.stop_loss,
            '15': position.take_profit,
            '16': position.risk_level,
            '17': position.status.value
        })
    
    async def _update_position_in_db(self, position: Position):
        """Update position in database."""
        if not self.db_manager:
            return
        
        query = """
            UPDATE portfolio_positions SET
                quantity = $2, current_price = $3, market_value = $4,
                unrealized_pnl = $5, realized_pnl = $6, stop_loss = $7,
                take_profit = $8, risk_level = $9, status = $10, updated_at = $11
            WHERE id = $1
        """
        
        await self.db_manager.execute_command(query, {
            '1': position.id,
            '2': position.quantity,
            '3': position.current_price,
            '4': position.market_value,
            '5': position.unrealized_pnl,
            '6': position.realized_pnl,
            '7': position.stop_loss,
            '8': position.take_profit,
            '9': position.risk_level,
            '10': position.status.value,
            '11': position.updated_at
        })
    
    async def _create_transaction_record(self, position: Position, transaction_type: TransactionType):
        """Create transaction record."""
        if not self.db_manager:
            return
        
        transaction = Transaction(
            id=str(uuid.uuid4()),
            portfolio_id=position.portfolio_id,
            transaction_type=transaction_type,
            asset_id=position.asset_id,
            quantity=position.quantity,
            price=position.entry_price,
            total_amount=position.market_value,
            fees=Decimal('0'),
            net_amount=position.market_value,
            status=TransactionStatus.EXECUTED,
            execution_date=position.entry_date
        )
        
        await self._save_transaction_to_db(transaction)
    
    async def _save_transaction_to_db(self, transaction: Transaction):
        """Save transaction to database."""
        if not self.db_manager:
            return
        
        query = """
            INSERT INTO transactions (
                id, portfolio_id, transaction_type, asset_id, quantity, price,
                total_amount, fees, net_amount, status, execution_date
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """
        
        await self.db_manager.execute_command(query, {
            '1': transaction.id,
            '2': transaction.portfolio_id,
            '3': transaction.transaction_type.value,
            '4': transaction.asset_id,
            '5': transaction.quantity,
            '6': transaction.price,
            '7': transaction.total_amount,
            '8': transaction.fees,
            '9': transaction.net_amount,
            '10': transaction.status.value,
            '11': transaction.execution_date
        })
