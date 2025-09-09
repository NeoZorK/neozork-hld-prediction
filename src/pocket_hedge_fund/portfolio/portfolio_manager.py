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
    
    async def update_position_prices(self, current_prices: Dict[str, float]) -> Dict[str, Any]:
        """Update current prices for all positions."""
        try:
            updated_positions = {}
            total_pnl = 0.0
            
            for symbol, position in self.positions.items():
                if symbol in current_prices:
                    current_price = current_prices[symbol]
                    
                    # Calculate unrealized P&L
                    if position['position_type'] == 'LONG':
                        unrealized_pnl = (current_price - position['price']) * position['quantity']
                    else:  # SHORT
                        unrealized_pnl = (position['price'] - current_price) * position['quantity']
                    
                    total_pnl += unrealized_pnl
                    
                    # Update position
                    updated_position = position.copy()
                    updated_position['current_price'] = current_price
                    updated_position['unrealized_pnl'] = unrealized_pnl
                    updated_position['last_updated'] = datetime.now()
                    
                    updated_positions[symbol] = updated_position
                    
                    # Check stop loss and take profit
                    await self._check_risk_limits(symbol, current_price, unrealized_pnl)
            
            self.positions = updated_positions
            
            return {
                'status': 'success',
                'total_unrealized_pnl': total_pnl,
                'positions_updated': len(updated_positions)
            }
            
        except Exception as e:
            logger.error(f"Error updating position prices: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    async def _check_risk_limits(self, symbol: str, current_price: float, unrealized_pnl: float):
        """Check risk limits and trigger actions if needed."""
        try:
            position = self.positions[symbol]
            position_value = position['quantity'] * current_price
            
            # Check stop loss
            if position.get('stop_loss'):
                if position['position_type'] == 'LONG' and current_price <= position['stop_loss']:
                    logger.warning(f"Stop loss triggered for {symbol}")
                    await self.close_position(symbol, price=current_price)
                    return
            
            # Check take profit
            if position.get('take_profit'):
                if position['position_type'] == 'LONG' and current_price >= position['take_profit']:
                    logger.info(f"Take profit triggered for {symbol}")
                    await self.close_position(symbol, price=current_price)
                    return
            
            # Check portfolio-level risk limits
            portfolio_value = self.get_portfolio_value()
            if portfolio_value > 0:
                drawdown = (self.initial_capital - portfolio_value) / self.initial_capital
                if drawdown > self.risk_limits['max_drawdown']:
                    logger.warning(f"Maximum drawdown exceeded: {drawdown:.2%}")
                    # Could trigger portfolio-wide risk management actions
            
        except Exception as e:
            logger.error(f"Error checking risk limits for {symbol}: {e}")
    
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
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Calculate performance metrics for the portfolio."""
        try:
            portfolio_value = self.get_portfolio_value()
            total_return = (portfolio_value - self.initial_capital) / self.initial_capital
            
            # Calculate daily returns from history
            if len(self.portfolio_history) > 1:
                daily_returns = []
                for i in range(1, len(self.portfolio_history)):
                    prev_value = self.portfolio_history[i-1]['capital_after']
                    curr_value = self.portfolio_history[i]['capital_after']
                    if prev_value > 0:
                        daily_return = (curr_value - prev_value) / prev_value
                        daily_returns.append(daily_return)
                
                if daily_returns:
                    returns_series = pd.Series(daily_returns)
                    volatility = returns_series.std() * np.sqrt(252)  # Annualized
                    sharpe_ratio = (returns_series.mean() * 252) / volatility if volatility > 0 else 0
                else:
                    volatility = 0
                    sharpe_ratio = 0
            else:
                volatility = 0
                sharpe_ratio = 0
            
            return {
                'total_return': total_return,
                'annualized_volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'portfolio_value': portfolio_value,
                'number_of_trades': len(self.portfolio_history),
                'max_drawdown': self._calculate_max_drawdown()
            }
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {}
    
    def _calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown from portfolio history."""
        try:
            if not self.portfolio_history:
                return 0.0
            
            values = [entry['capital_after'] for entry in self.portfolio_history]
            peak = values[0]
            max_dd = 0.0
            
            for value in values:
                if value > peak:
                    peak = value
                drawdown = (peak - value) / peak
                if drawdown > max_dd:
                    max_dd = drawdown
            
            return max_dd
            
        except Exception as e:
            logger.error(f"Error calculating max drawdown: {e}")
            return 0.0
    
    async def rebalance_portfolio(self, target_weights: Dict[str, float], 
                                current_prices: Dict[str, float]) -> Dict[str, Any]:
        """Rebalance portfolio to target weights."""
        try:
            logger.info(f"Rebalancing portfolio to target weights")
            
            portfolio_value = self.get_portfolio_value()
            rebalance_actions = []
            
            # Calculate target values
            target_values = {}
            for symbol, weight in target_weights.items():
                target_values[symbol] = portfolio_value * weight
            
            # Calculate current values
            current_values = {}
            for symbol, position in self.positions.items():
                if symbol in current_prices:
                    current_values[symbol] = position['quantity'] * current_prices[symbol]
                else:
                    current_values[symbol] = 0
            
            # Determine rebalancing actions
            for symbol, target_value in target_values.items():
                current_value = current_values.get(symbol, 0)
                difference = target_value - current_value
                
                if abs(difference) > portfolio_value * 0.01:  # 1% threshold
                    if symbol in current_prices:
                        quantity_change = difference / current_prices[symbol]
                        
                        if quantity_change > 0:
                            # Buy more
                            action = await self.add_position(
                                symbol, abs(quantity_change), current_prices[symbol]
                            )
                            rebalance_actions.append({
                                'action': 'BUY',
                                'symbol': symbol,
                                'quantity': abs(quantity_change),
                                'price': current_prices[symbol]
                            })
                        else:
                            # Sell some
                            if symbol in self.positions:
                                sell_quantity = min(abs(quantity_change), self.positions[symbol]['quantity'])
                                action = await self.close_position(
                                    symbol, sell_quantity, current_prices[symbol]
                                )
                                rebalance_actions.append({
                                    'action': 'SELL',
                                    'symbol': symbol,
                                    'quantity': sell_quantity,
                                    'price': current_prices[symbol]
                                })
            
            return {
                'status': 'success',
                'message': f'Portfolio rebalanced with {len(rebalance_actions)} actions',
                'actions': rebalance_actions,
                'new_portfolio_value': self.get_portfolio_value()
            }
            
        except Exception as e:
            logger.error(f"Error rebalancing portfolio: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
