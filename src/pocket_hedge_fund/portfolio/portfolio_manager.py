"""
Portfolio Manager for Pocket Hedge Fund.

This module provides portfolio management functionality including
position sizing, risk management, and portfolio optimization.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import asyncio

logger = logging.getLogger(__name__)

class PortfolioManager:
    """Manages portfolio operations for the Pocket Hedge Fund."""
    
    def __init__(self, fund_id: str, initial_capital: float = 100000.0):
        """Initialize PortfolioManager."""
        self.fund_id = fund_id
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = {}
        self.portfolio_history = []
        self.risk_limits = {
            'max_position_size': 0.1,  # 10% max per position
            'max_sector_exposure': 0.3,  # 30% max per sector
            'max_drawdown': 0.15,  # 15% max drawdown
            'stop_loss': 0.05,  # 5% stop loss
            'take_profit': 0.20  # 20% take profit
        }
        
    async def add_position(self, symbol: str, quantity: float, price: float, 
                          position_type: str = "LONG", stop_loss: Optional[float] = None,
                          take_profit: Optional[float] = None) -> Dict[str, Any]:
        """Add a new position to the portfolio."""
        try:
            logger.info(f"Adding position: {symbol} {quantity} @ {price}")
            
            # Validate position size
            position_value = quantity * price
            if position_value > self.current_capital * self.risk_limits['max_position_size']:
                raise ValueError(f"Position size exceeds maximum allowed ({self.risk_limits['max_position_size']*100}%)")
            
            # Check if position already exists
            if symbol in self.positions:
                # Update existing position
                existing_position = self.positions[symbol]
                new_quantity = existing_position['quantity'] + quantity
                new_avg_price = ((existing_position['quantity'] * existing_position['price']) + 
                               (quantity * price)) / new_quantity
                
                self.positions[symbol] = {
                    'symbol': symbol,
                    'quantity': new_quantity,
                    'price': new_avg_price,
                    'position_type': position_type,
                    'stop_loss': stop_loss or existing_position.get('stop_loss'),
                    'take_profit': take_profit or existing_position.get('take_profit'),
                    'entry_time': existing_position['entry_time'],
                    'last_updated': datetime.now()
                }
            else:
                # Create new position
                self.positions[symbol] = {
                    'symbol': symbol,
                    'quantity': quantity,
                    'price': price,
                    'position_type': position_type,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'entry_time': datetime.now(),
                    'last_updated': datetime.now()
                }
            
            # Update capital
            self.current_capital -= position_value
            
            # Record in history
            self.portfolio_history.append({
                'timestamp': datetime.now(),
                'action': 'ADD_POSITION',
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'position_type': position_type,
                'capital_after': self.current_capital
            })
            
            logger.info(f"Position added successfully. Remaining capital: {self.current_capital}")
            
            return {
                'status': 'success',
                'message': f'Position added: {symbol}',
                'position': self.positions[symbol],
                'remaining_capital': self.current_capital
            }
            
        except Exception as e:
            logger.error(f"Error adding position: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    async def close_position(self, symbol: str, quantity: Optional[float] = None, 
                           price: float = None) -> Dict[str, Any]:
        """Close a position or part of it."""
        try:
            if symbol not in self.positions:
                raise ValueError(f"Position {symbol} not found")
            
            position = self.positions[symbol]
            close_quantity = quantity or position['quantity']
            
            if close_quantity > position['quantity']:
                raise ValueError(f"Cannot close more than available quantity")
            
            # Calculate P&L
            if position['position_type'] == 'LONG':
                pnl = (price - position['price']) * close_quantity
            else:  # SHORT
                pnl = (position['price'] - price) * close_quantity
            
            # Update capital
            self.current_capital += (price * close_quantity)
            
            # Update or remove position
            if close_quantity == position['quantity']:
                # Close entire position
                del self.positions[symbol]
                logger.info(f"Position {symbol} closed completely")
            else:
                # Partial close
                self.positions[symbol]['quantity'] -= close_quantity
                self.positions[symbol]['last_updated'] = datetime.now()
                logger.info(f"Position {symbol} partially closed: {close_quantity}")
            
            # Record in history
            self.portfolio_history.append({
                'timestamp': datetime.now(),
                'action': 'CLOSE_POSITION',
                'symbol': symbol,
                'quantity': close_quantity,
                'price': price,
                'pnl': pnl,
                'capital_after': self.current_capital
            })
            
            return {
                'status': 'success',
                'message': f'Position closed: {symbol}',
                'pnl': pnl,
                'remaining_capital': self.current_capital
            }
            
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get comprehensive portfolio summary."""
        try:
            portfolio_value = self.get_portfolio_value()
            total_return = (portfolio_value - self.initial_capital) / self.initial_capital
            
            # Calculate position summaries
            position_summaries = []
            total_unrealized_pnl = 0.0
            
            for symbol, position in self.positions.items():
                current_price = position.get('current_price', position['price'])
                position_value = position['quantity'] * current_price
                
                if 'unrealized_pnl' in position:
                    unrealized_pnl = position['unrealized_pnl']
                else:
                    if position['position_type'] == 'LONG':
                        unrealized_pnl = (current_price - position['price']) * position['quantity']
                    else:
                        unrealized_pnl = (position['price'] - current_price) * position['quantity']
                
                total_unrealized_pnl += unrealized_pnl
                
                position_summaries.append({
                    'symbol': symbol,
                    'quantity': position['quantity'],
                    'entry_price': position['price'],
                    'current_price': current_price,
                    'position_value': position_value,
                    'unrealized_pnl': unrealized_pnl,
                    'position_type': position['position_type'],
                    'weight': position_value / portfolio_value if portfolio_value > 0 else 0
                })
            
            return {
                'fund_id': self.fund_id,
                'timestamp': datetime.now(),
                'initial_capital': self.initial_capital,
                'current_capital': self.current_capital,
                'portfolio_value': portfolio_value,
                'total_return': total_return,
                'total_unrealized_pnl': total_unrealized_pnl,
                'number_of_positions': len(self.positions),
                'positions': position_summaries,
                'risk_limits': self.risk_limits
            }
            
        except Exception as e:
            logger.error(f"Error getting portfolio summary: {e}")
            return {}
    
    def get_portfolio_value(self) -> float:
        """Calculate total portfolio value."""
        try:
            total_value = self.current_capital
            
            for position in self.positions.values():
                if 'current_price' in position:
                    position_value = position['quantity'] * position['current_price']
                    total_value += position_value
                else:
                    # Use entry price if current price not available
                    position_value = position['quantity'] * position['price']
                    total_value += position_value
            
            return total_value
            
        except Exception as e:
            logger.error(f"Error calculating portfolio value: {e}")
            return self.current_capital
