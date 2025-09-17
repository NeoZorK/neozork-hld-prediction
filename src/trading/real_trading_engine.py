# -*- coding: utf-8 -*-
"""
Real Trading Engine for NeoZork Interactive ML Trading Strategy Development.

This module provides real trading capabilities with live data and comprehensive backtesting.
"""

import asyncio
import time
import logging
import threading
import queue
from typing import Dict, Any, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import pandas as pd
import numpy as np
import json
from decimal import Decimal
import aiohttp
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingMode(Enum):
    """Trading modes."""
    PAPER = "paper"
    LIVE = "live"
    BACKTEST = "backtest"

class OrderType(Enum):
    """Order types."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderSide(Enum):
    """Order sides."""
    BUY = "buy"
    SELL = "sell"

class OrderStatus(Enum):
    """Order statuses."""
    PENDING = "pending"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

@dataclass
class Order:
    """Order structure."""
    id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: float = 0.0
    average_price: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Position:
    """Position structure."""
    symbol: str
    quantity: float
    average_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Trade:
    """Trade structure."""
    id: str
    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    timestamp: datetime
    commission: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

class BacktestEngine:
    """Backtesting engine for historical data analysis."""
    
    def __init__(self, initial_capital: float = 10000.0, commission: float = 0.001):
        self.initial_capital = initial_capital
        self.commission = commission
        self.cash = initial_capital
        self.positions = {}
        self.orders = []
        self.trades = []
        self.portfolio_history = []
        self.current_time = None
        
    def run_backtest(self, data: pd.DataFrame, strategy: Callable, 
                    start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Run backtest with historical data."""
        try:
            logger.info(f"Starting backtest from {start_date} to {end_date}")
            
            # Filter data by date range
            mask = (data.index >= start_date) & (data.index <= end_date)
            backtest_data = data[mask].copy()
            
            if backtest_data.empty:
                return {
                    'status': 'error',
                    'message': 'No data available for the specified date range'
                }
            
            # Initialize portfolio
            self._initialize_portfolio()
            
            # Run strategy for each time step
            for timestamp, row in backtest_data.iterrows():
                self.current_time = timestamp
                
                # Update current prices
                self._update_prices(row)
                
                # Execute strategy
                try:
                    strategy(self, row, timestamp)
                except Exception as e:
                    logger.warning(f"Strategy error at {timestamp}: {e}")
                
                # Process pending orders
                self._process_orders(row)
                
                # Update portfolio
                self._update_portfolio()
                
                # Record portfolio state
                self._record_portfolio_state(timestamp)
            
            # Calculate final results
            results = self._calculate_backtest_results()
            
            logger.info(f"Backtest completed. Final portfolio value: ${results['final_value']:.2f}")
            return {
                'status': 'success',
                'results': results,
                'message': 'Backtest completed successfully'
            }
            
        except Exception as e:
            logger.error(f"Backtest failed: {e}")
            return {
                'status': 'error',
                'message': f'Backtest failed: {str(e)}'
            }
    
    def _initialize_portfolio(self):
        """Initialize portfolio for backtest."""
        self.cash = self.initial_capital
        self.positions = {}
        self.orders = []
        self.trades = []
        self.portfolio_history = []
    
    def _update_prices(self, row: pd.Series):
        """Update current prices for all positions."""
        for symbol in self.positions:
            if symbol in row.index:
                self.positions[symbol].current_price = row[symbol]
    
    def _process_orders(self, row: pd.Series):
        """Process pending orders."""
        for order in self.orders[:]:  # Copy to avoid modification during iteration
            if order.status == OrderStatus.PENDING:
                if self._should_fill_order(order, row):
                    self._fill_order(order, row)
    
    def _should_fill_order(self, order: Order, row: pd.Series) -> bool:
        """Check if order should be filled."""
        if order.symbol not in row.index:
            return False
        
        current_price = row[order.symbol]
        
        if order.order_type == OrderType.MARKET:
            return True
        elif order.order_type == OrderType.LIMIT:
            if order.side == OrderSide.BUY:
                return current_price <= order.price
            else:
                return current_price >= order.price
        elif order.order_type == OrderType.STOP:
            if order.side == OrderSide.BUY:
                return current_price >= order.stop_price
            else:
                return current_price <= order.stop_price
        
        return False
    
    def _fill_order(self, order: Order, row: pd.Series):
        """Fill an order."""
        current_price = row[order.symbol]
        
        # Calculate commission
        commission = order.quantity * current_price * self.commission
        
        # Check if we have enough cash/position
        if order.side == OrderSide.BUY:
            total_cost = order.quantity * current_price + commission
            if total_cost > self.cash:
                order.status = OrderStatus.REJECTED
                return
            self.cash -= total_cost
        else:
            if order.symbol not in self.positions or self.positions[order.symbol].quantity < order.quantity:
                order.status = OrderStatus.REJECTED
                return
            self.cash += order.quantity * current_price - commission
        
        # Update position
        if order.symbol not in self.positions:
            self.positions[order.symbol] = Position(
                symbol=order.symbol,
                quantity=0,
                average_price=0,
                current_price=current_price,
                unrealized_pnl=0
            )
        
        position = self.positions[order.symbol]
        
        if order.side == OrderSide.BUY:
            # Update average price
            total_quantity = position.quantity + order.quantity
            total_value = position.quantity * position.average_price + order.quantity * current_price
            position.average_price = total_value / total_quantity if total_quantity > 0 else current_price
            position.quantity += order.quantity
        else:
            # Calculate realized P&L
            realized_pnl = (current_price - position.average_price) * order.quantity - commission
            position.realized_pnl += realized_pnl
            position.quantity -= order.quantity
            
            # Remove position if quantity is zero
            if position.quantity <= 0:
                del self.positions[order.symbol]
        
        # Create trade record
        trade = Trade(
            id=f"trade_{len(self.trades) + 1}",
            order_id=order.id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            price=current_price,
            timestamp=self.current_time,
            commission=commission
        )
        self.trades.append(trade)
        
        # Update order
        order.status = OrderStatus.FILLED
        order.filled_quantity = order.quantity
        order.average_price = current_price
        order.updated_at = self.current_time
    
    def _update_portfolio(self):
        """Update portfolio positions."""
        for position in self.positions.values():
            position.unrealized_pnl = (position.current_price - position.average_price) * position.quantity
    
    def _record_portfolio_state(self, timestamp: datetime):
        """Record current portfolio state."""
        total_value = self.cash
        total_unrealized_pnl = 0
        
        for position in self.positions.values():
            position_value = position.quantity * position.current_price
            total_value += position_value
            total_unrealized_pnl += position.unrealized_pnl
        
        portfolio_state = {
            'timestamp': timestamp,
            'cash': self.cash,
            'total_value': total_value,
            'unrealized_pnl': total_unrealized_pnl,
            'realized_pnl': sum(pos.realized_pnl for pos in self.positions.values()),
            'positions_count': len(self.positions),
            'return_pct': (total_value - self.initial_capital) / self.initial_capital * 100
        }
        
        self.portfolio_history.append(portfolio_state)
    
    def _calculate_backtest_results(self) -> Dict[str, Any]:
        """Calculate backtest performance metrics."""
        if not self.portfolio_history:
            return {}
        
        df = pd.DataFrame(self.portfolio_history)
        df.set_index('timestamp', inplace=True)
        
        # Basic metrics
        initial_value = self.initial_capital
        final_value = df['total_value'].iloc[-1]
        total_return = (final_value - initial_value) / initial_value * 100
        
        # Calculate returns
        df['returns'] = df['total_value'].pct_change()
        
        # Risk metrics
        volatility = df['returns'].std() * np.sqrt(252)  # Annualized
        sharpe_ratio = df['returns'].mean() / df['returns'].std() * np.sqrt(252) if df['returns'].std() != 0 else 0
        
        # Drawdown
        df['cumulative'] = (1 + df['returns']).cumprod()
        df['running_max'] = df['cumulative'].expanding().max()
        df['drawdown'] = (df['cumulative'] - df['running_max']) / df['running_max']
        max_drawdown = df['drawdown'].min() * 100
        
        # Trade statistics
        total_trades = len(self.trades)
        winning_trades = len([t for t in self.trades if t.side == OrderSide.SELL and 
                             any(pos.symbol == t.symbol and pos.realized_pnl > 0 for pos in self.positions.values())])
        win_rate = winning_trades / total_trades * 100 if total_trades > 0 else 0
        
        return {
            'initial_capital': initial_value,
            'final_value': final_value,
            'total_return_pct': total_return,
            'volatility_pct': volatility * 100,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown_pct': max_drawdown,
            'total_trades': total_trades,
            'win_rate_pct': win_rate,
            'portfolio_history': df.to_dict('records')
        }
    
    def place_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                   quantity: float, price: Optional[float] = None, 
                   stop_price: Optional[float] = None) -> Order:
        """Place an order."""
        order = Order(
            id=f"order_{len(self.orders) + 1}_{int(time.time())}",
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )
        
        self.orders.append(order)
        logger.info(f"Order placed: {order.side.value} {order.quantity} {order.symbol} at {order.price or 'market'}")
        
        return order

class LiveTradingEngine:
    """Live trading engine for real money trading."""
    
    def __init__(self, api_keys: Dict[str, Dict[str, str]], 
                 initial_capital: float = 10000.0, commission: float = 0.001):
        self.api_keys = api_keys
        self.initial_capital = initial_capital
        self.commission = commission
        self.cash = initial_capital
        self.positions = {}
        self.orders = []
        self.trades = []
        self.is_running = False
        self.trading_thread = None
        self.order_queue = queue.Queue()
        self.exchanges = {}
        
    async def initialize_exchanges(self) -> Dict[str, Any]:
        """Initialize connections to exchanges."""
        try:
            # Initialize Binance
            if "binance" in self.api_keys:
                from binance.client import Client as BinanceClient
                binance_key = self.api_keys["binance"]
                self.exchanges["binance"] = BinanceClient(
                    binance_key["api_key"],
                    binance_key["api_secret"],
                    testnet=True  # Use testnet for safety
                )
                logger.info("Binance exchange initialized")
            
            # Initialize Bybit
            if "bybit" in self.api_keys:
                from pybit.unified_trading import HTTP as BybitClient
                bybit_key = self.api_keys["bybit"]
                self.exchanges["bybit"] = BybitClient(
                    testnet=True,
                    api_key=bybit_key["api_key"],
                    api_secret=bybit_key["api_secret"]
                )
                logger.info("Bybit exchange initialized")
            
            return {
                'status': 'success',
                'exchanges': list(self.exchanges.keys()),
                'message': f'Initialized {len(self.exchanges)} exchanges'
            }
            
        except Exception as e:
            logger.error(f"Failed to initialize exchanges: {e}")
            return {
                'status': 'error',
                'message': f'Failed to initialize exchanges: {str(e)}'
            }
    
    async def get_account_balance(self, exchange: str) -> Dict[str, Any]:
        """Get account balance from exchange."""
        try:
            if exchange == "binance" and exchange in self.exchanges:
                account = self.exchanges[exchange].get_account()
                balances = {}
                for balance in account['balances']:
                    if float(balance['free']) > 0 or float(balance['locked']) > 0:
                        balances[balance['asset']] = {
                            'free': float(balance['free']),
                            'locked': float(balance['locked']),
                            'total': float(balance['free']) + float(balance['locked'])
                        }
                return {
                    'status': 'success',
                    'balances': balances,
                    'message': 'Account balance retrieved'
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Exchange {exchange} not supported or not initialized'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to get account balance: {str(e)}'
            }
    
    async def place_live_order(self, exchange: str, symbol: str, side: str, 
                             order_type: str, quantity: float, 
                             price: Optional[float] = None) -> Dict[str, Any]:
        """Place a live order on exchange."""
        try:
            if exchange not in self.exchanges:
                return {
                    'status': 'error',
                    'message': f'Exchange {exchange} not initialized'
                }
            
            if exchange == "binance":
                client = self.exchanges[exchange]
                
                # Convert order parameters
                side_upper = side.upper()
                order_type_upper = order_type.upper()
                
                if order_type_upper == "MARKET":
                    if side_upper == "BUY":
                        order = client.order_market_buy(symbol=symbol, quantity=quantity)
                    else:
                        order = client.order_market_sell(symbol=symbol, quantity=quantity)
                elif order_type_upper == "LIMIT":
                    if side_upper == "BUY":
                        order = client.order_limit_buy(symbol=symbol, quantity=quantity, price=price)
                    else:
                        order = client.order_limit_sell(symbol=symbol, quantity=quantity, price=price)
                else:
                    return {
                        'status': 'error',
                        'message': f'Order type {order_type} not supported'
                    }
                
                return {
                    'status': 'success',
                    'order_id': order['orderId'],
                    'symbol': order['symbol'],
                    'side': order['side'],
                    'quantity': float(order['origQty']),
                    'price': float(order.get('price', 0)),
                    'status': order['status'],
                    'message': 'Order placed successfully'
                }
            
            else:
                return {
                    'status': 'error',
                    'message': f'Exchange {exchange} not supported for live trading'
                }
                
        except Exception as e:
            logger.error(f"Failed to place live order: {e}")
            return {
                'status': 'error',
                'message': f'Failed to place live order: {str(e)}'
            }
    
    def start_trading(self):
        """Start live trading."""
        if not self.is_running:
            self.is_running = True
            self.trading_thread = threading.Thread(target=self._trading_loop, daemon=True)
            self.trading_thread.start()
            logger.info("Live trading started")
    
    def stop_trading(self):
        """Stop live trading."""
        self.is_running = False
        if self.trading_thread:
            self.trading_thread.join(timeout=5)
        logger.info("Live trading stopped")
    
    def _trading_loop(self):
        """Main trading loop."""
        while self.is_running:
            try:
                # Process order queue
                while not self.order_queue.empty():
                    try:
                        order_data = self.order_queue.get_nowait()
                        asyncio.run(self._process_order(order_data))
                    except queue.Empty:
                        break
                
                # Update positions
                asyncio.run(self._update_positions())
                
                time.sleep(1)  # Update every second
                
            except Exception as e:
                logger.error(f"Error in trading loop: {e}")
                time.sleep(5)
    
    async def _process_order(self, order_data: Dict[str, Any]):
        """Process an order from the queue."""
        try:
            result = await self.place_live_order(
                exchange=order_data['exchange'],
                symbol=order_data['symbol'],
                side=order_data['side'],
                order_type=order_data['order_type'],
                quantity=order_data['quantity'],
                price=order_data.get('price')
            )
            
            if result['status'] == 'success':
                logger.info(f"Order executed: {result['order_id']}")
            else:
                logger.error(f"Order failed: {result['message']}")
                
        except Exception as e:
            logger.error(f"Error processing order: {e}")
    
    async def _update_positions(self):
        """Update current positions."""
        try:
            for exchange in self.exchanges:
                balance_result = await self.get_account_balance(exchange)
                if balance_result['status'] == 'success':
                    # Update positions based on balance
                    for asset, balance in balance_result['balances'].items():
                        if balance['total'] > 0:
                            if asset not in self.positions:
                                self.positions[asset] = Position(
                                    symbol=asset,
                                    quantity=balance['total'],
                                    average_price=0,  # Would need to track this
                                    current_price=0,  # Would need to get current price
                                    unrealized_pnl=0
                                )
                            else:
                                self.positions[asset].quantity = balance['total']
                                
        except Exception as e:
            logger.error(f"Error updating positions: {e}")

class RealTradingSystem:
    """Main real trading system integrating backtesting and live trading."""
    
    def __init__(self, api_keys: Dict[str, Dict[str, str]] = None, 
                 initial_capital: float = 10000.0):
        self.api_keys = api_keys or {}
        self.initial_capital = initial_capital
        
        # Initialize engines
        self.backtest_engine = BacktestEngine(initial_capital)
        self.live_engine = LiveTradingEngine(api_keys, initial_capital) if api_keys else None
        
        # Trading state
        self.current_mode = TradingMode.PAPER
        self.strategies = {}
        self.performance_metrics = {}
        
    async def initialize(self) -> Dict[str, Any]:
        """Initialize the trading system."""
        try:
            results = []
            
            # Initialize live trading if API keys provided
            if self.live_engine:
                live_result = await self.live_engine.initialize_exchanges()
                results.append(live_result)
            
            return {
                'status': 'success',
                'initialized_components': ['backtest_engine'] + (['live_engine'] if self.live_engine else []),
                'details': results,
                'message': 'Trading system initialized successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to initialize trading system: {str(e)}'
            }
    
    def run_backtest(self, data: pd.DataFrame, strategy: Callable, 
                    start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Run a backtest with historical data."""
        return self.backtest_engine.run_backtest(data, strategy, start_date, end_date)
    
    def add_strategy(self, name: str, strategy: Callable):
        """Add a trading strategy."""
        self.strategies[name] = strategy
        logger.info(f"Strategy '{name}' added")
    
    def get_portfolio_status(self) -> Dict[str, Any]:
        """Get current portfolio status."""
        if self.current_mode == TradingMode.BACKTEST:
            # Return backtest portfolio status
            total_value = self.backtest_engine.cash
            for position in self.backtest_engine.positions.values():
                total_value += position.quantity * position.current_price
            
            return {
                'status': 'success',
                'mode': self.current_mode.value,
                'cash': self.backtest_engine.cash,
                'total_value': total_value,
                'positions': {symbol: {
                    'quantity': pos.quantity,
                    'average_price': pos.average_price,
                    'current_price': pos.current_price,
                    'unrealized_pnl': pos.unrealized_pnl
                } for symbol, pos in self.backtest_engine.positions.items()},
                'total_return_pct': (total_value - self.initial_capital) / self.initial_capital * 100
            }
        
        elif self.current_mode == TradingMode.LIVE and self.live_engine:
            # Return live portfolio status
            total_value = self.live_engine.cash
            for position in self.live_engine.positions.values():
                total_value += position.quantity * position.current_price
            
            return {
                'status': 'success',
                'mode': self.current_mode.value,
                'cash': self.live_engine.cash,
                'total_value': total_value,
                'positions': {symbol: {
                    'quantity': pos.quantity,
                    'average_price': pos.average_price,
                    'current_price': pos.current_price,
                    'unrealized_pnl': pos.unrealized_pnl
                } for symbol, pos in self.live_engine.positions.items()},
                'total_return_pct': (total_value - self.initial_capital) / self.initial_capital * 100
            }
        
        else:
            return {
                'status': 'error',
                'message': 'No active trading mode'
            }
    
    def start_live_trading(self):
        """Start live trading."""
        if self.live_engine:
            self.current_mode = TradingMode.LIVE
            self.live_engine.start_trading()
            return {
                'status': 'success',
                'message': 'Live trading started'
            }
        else:
            return {
                'status': 'error',
                'message': 'Live trading not available (no API keys)'
            }
    
    def stop_live_trading(self):
        """Stop live trading."""
        if self.live_engine:
            self.live_engine.stop_trading()
            return {
                'status': 'success',
                'message': 'Live trading stopped'
            }
        else:
            return {
                'status': 'error',
                'message': 'Live trading not available'
            }

# Example trading strategy
def simple_momentum_strategy(engine: BacktestEngine, row: pd.Series, timestamp: datetime):
    """Simple momentum trading strategy."""
    # This is a basic example - in real implementation, you'd use ML predictions
    
    # Example: Buy if price is above 20-period moving average
    if 'close' in row.index:
        current_price = row['close']
        
        # Simple moving average (would need historical data in real implementation)
        # For demo, we'll use a simple threshold
        if current_price > 100:  # Example threshold
            # Place buy order
            engine.place_order(
                symbol='BTCUSDT',
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                quantity=0.1
            )
        elif current_price < 95:  # Example threshold
            # Place sell order
            engine.place_order(
                symbol='BTCUSDT',
                side=OrderSide.SELL,
                order_type=OrderType.MARKET,
                quantity=0.1
            )

# Example usage and testing
async def test_real_trading_system():
    """Test real trading system."""
    print("🧪 Testing Real Trading System...")
    
    # Create trading system
    trading_system = RealTradingSystem()
    
    # Initialize
    init_result = await trading_system.initialize()
    print(f"  • System initialization: {'✅' if init_result['status'] == 'success' else '❌'}")
    
    # Add strategy
    trading_system.add_strategy("momentum", simple_momentum_strategy)
    print("  • Strategy added: ✅")
    
    # Generate sample data for backtest
    dates = pd.date_range('2023-01-01', periods=100, freq='1h')
    prices = 100 + np.cumsum(np.random.normal(0, 1, 100))
    
    data = pd.DataFrame({
        'close': prices,
        'high': prices * 1.01,
        'low': prices * 0.99,
        'volume': np.random.uniform(1000, 5000, 100)
    }, index=dates)
    
    print(f"  • Sample data created: {len(data)} rows")
    
    # Run backtest
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 5)
    
    backtest_result = trading_system.run_backtest(
        data, simple_momentum_strategy, start_date, end_date
    )
    
    if backtest_result['status'] == 'success':
        results = backtest_result['results']
        print(f"  • Backtest completed: ✅")
        print(f"    - Initial Capital: ${results['initial_capital']:.2f}")
        print(f"    - Final Value: ${results['final_value']:.2f}")
        print(f"    - Total Return: {results['total_return_pct']:.2f}%")
        print(f"    - Sharpe Ratio: {results['sharpe_ratio']:.3f}")
        print(f"    - Max Drawdown: {results['max_drawdown_pct']:.2f}%")
        print(f"    - Total Trades: {results['total_trades']}")
        print(f"    - Win Rate: {results['win_rate_pct']:.2f}%")
    else:
        print(f"  • Backtest failed: ❌ {backtest_result['message']}")
    
    # Get portfolio status
    portfolio_status = trading_system.get_portfolio_status()
    if portfolio_status['status'] == 'success':
        print(f"  • Portfolio status: ✅")
        print(f"    - Mode: {portfolio_status['mode']}")
        print(f"    - Total Value: ${portfolio_status['total_value']:.2f}")
        print(f"    - Cash: ${portfolio_status['cash']:.2f}")
        print(f"    - Positions: {len(portfolio_status['positions'])}")
        print(f"    - Return: {portfolio_status['total_return_pct']:.2f}%")
    
    print("✅ Real Trading System test completed!")
    
    return trading_system

if __name__ == "__main__":
    asyncio.run(test_real_trading_system())
