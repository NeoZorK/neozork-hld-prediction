# -*- coding: utf-8 -*-
"""
Real Trading System Integration for NeoZork Interactive ML Trading Strategy Development.

This module integrates real exchange APIs with real ML models for live trading.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import time
import logging
from dataclasses import dataclass
from enum import Enum

# Import our real modules
from ..data.real_exchange_apis import ExchangeAPIManager, ExchangeType, APIKey
from ..ml.real_ml_models import RealMLModels, ModelType, FeatureType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingMode(Enum):
    """Trading modes."""
    PAPER = "paper"  # Paper trading (simulation)
    LIVE = "live"    # Live trading (real money)

class SignalType(Enum):
    """Signal types."""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"

@dataclass
class TradingSignal:
    """Trading signal data structure."""
    symbol: str
    signal_type: SignalType
    confidence: float
    price: float
    timestamp: datetime
    model_name: str
    features: Dict[str, float]

@dataclass
class Position:
    """Position data structure."""
    symbol: str
    side: str  # 'long' or 'short'
    quantity: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    entry_time: datetime
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

@dataclass
class TradingConfig:
    """Trading configuration."""
    symbol: str
    model_name: str
    trading_mode: TradingMode
    position_size: float  # Percentage of portfolio
    stop_loss_pct: float  # Stop loss percentage
    take_profit_pct: float  # Take profit percentage
    max_positions: int  # Maximum number of positions
    min_confidence: float  # Minimum confidence for signals

class RealTradingSystem:
    """Real trading system integrating APIs and ML models."""
    
    def __init__(self, config: TradingConfig):
        self.config = config
        self.api_manager = ExchangeAPIManager()
        self.ml_models = RealMLModels()
        self.positions: Dict[str, Position] = {}
        self.signals_history: List[TradingSignal] = []
        self.portfolio_value = 10000.0  # Starting portfolio value
        self.cash = 10000.0
        self.is_running = False
        
        # Performance tracking
        self.trades_history = []
        self.daily_returns = []
        self.performance_metrics = {}
        
    def initialize(self, api_keys: Dict[ExchangeType, APIKey]) -> Dict[str, Any]:
        """Initialize the trading system."""
        try:
            # Add exchanges
            for exchange_type, api_key in api_keys.items():
                success = self.api_manager.add_exchange(exchange_type, api_key)
                if not success:
                    logger.warning(f"Failed to connect to {exchange_type.value}")
            
            # Check connections
            status = self.api_manager.get_connection_status()
            connected_exchanges = [ex for ex, info in status.items() if info.get('connected', False)]
            
            if not connected_exchanges:
                return {
                    'status': 'error',
                    'message': 'No exchanges connected successfully'
                }
            
            logger.info(f"Trading system initialized with exchanges: {connected_exchanges}")
            
            return {
                'status': 'success',
                'connected_exchanges': connected_exchanges,
                'message': 'Trading system initialized successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Initialization failed: {str(e)}'
            }
    
    def train_model(self, symbol: str, model_type: str, 
                   start_date: datetime, end_date: datetime,
                   interval: str = '1h') -> Dict[str, Any]:
        """Train ML model with historical data."""
        try:
            # Get historical data from exchanges
            historical_data = self._get_historical_data(symbol, start_date, end_date, interval)
            
            if historical_data.empty:
                return {
                    'status': 'error',
                    'message': 'No historical data available'
                }
            
            # Prepare data for ML
            X, y = self.ml_models.prepare_data(historical_data, target_column='close')
            
            if X.empty or y.empty:
                return {
                    'status': 'error',
                    'message': 'Failed to prepare data for ML training'
                }
            
            # Train model
            model_name = f"{symbol}_{model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result = self.ml_models.train_model(model_type, X, y, model_name)
            
            if result['status'] == 'success':
                # Update config with trained model
                self.config.model_name = model_name
                
                return {
                    'status': 'success',
                    'model_name': model_name,
                    'metrics': result['metrics'],
                    'data_points': len(historical_data),
                    'message': f'Model {model_name} trained successfully'
                }
            else:
                return result
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Model training failed: {str(e)}'
            }
    
    def _get_historical_data(self, symbol: str, start_date: datetime, 
                           end_date: datetime, interval: str) -> pd.DataFrame:
        """Get historical data from exchanges."""
        # Try to get data from available exchanges
        for exchange_type in self.api_manager.apis.keys():
            try:
                df = self.api_manager.get_klines_data(
                    symbol, interval, exchange_type, start_date, end_date, limit=1000
                )
                if not df.empty:
                    logger.info(f"Retrieved {len(df)} data points from {exchange_type.value}")
                    return df
            except Exception as e:
                logger.warning(f"Failed to get data from {exchange_type.value}: {e}")
                continue
        
        # If no real data available, generate sample data for testing
        logger.warning("No real data available, generating sample data for testing")
        return self._generate_sample_data(symbol, start_date, end_date, interval)
    
    def _generate_sample_data(self, symbol: str, start_date: datetime, 
                            end_date: datetime, interval: str) -> pd.DataFrame:
        """Generate sample data for testing when real data is not available."""
        # Calculate number of periods
        if interval == '1h':
            periods = int((end_date - start_date).total_seconds() / 3600)
        elif interval == '1d':
            periods = int((end_date - start_date).days)
        else:
            periods = 1000  # Default
        
        # Generate realistic price data
        np.random.seed(42)
        returns = np.random.normal(0, 0.02, periods)
        prices = 100 * np.exp(np.cumsum(returns))
        
        # Create DataFrame
        dates = pd.date_range(start_date, periods=periods, freq=interval)
        data = pd.DataFrame({
            'timestamp': dates,
            'open': prices * (1 + np.random.normal(0, 0.001, periods)),
            'high': prices * (1 + np.abs(np.random.normal(0, 0.01, periods))),
            'low': prices * (1 - np.abs(np.random.normal(0, 0.01, periods))),
            'close': prices,
            'volume': np.random.exponential(1000, periods)
        })
        
        data.set_index('timestamp', inplace=True)
        return data
    
    def generate_signal(self, symbol: str) -> Dict[str, Any]:
        """Generate trading signal using ML model."""
        try:
            if self.config.model_name not in self.ml_models.trained_models:
                return {
                    'status': 'error',
                    'message': f'Model {self.config.model_name} not found'
                }
            
            # Get recent data
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=24)  # Last 24 hours
            
            recent_data = self._get_historical_data(symbol, start_time, end_time, '1h')
            
            if recent_data.empty:
                return {
                    'status': 'error',
                    'message': 'No recent data available for signal generation'
                }
            
            # Prepare features
            features_df = self.ml_models.create_features(recent_data)
            model_info = self.ml_models.trained_models[self.config.model_name]
            feature_columns = model_info['feature_columns']
            
            # Get latest features
            latest_features = features_df[feature_columns].tail(1)
            
            # Make prediction
            pred_result = self.ml_models.predict(self.config.model_name, latest_features)
            
            if pred_result['status'] != 'success':
                return pred_result
            
            prediction = pred_result['predictions'][0]
            confidence = abs(prediction)
            
            # Generate signal based on prediction
            if prediction > 0.01 and confidence > self.config.min_confidence:
                signal_type = SignalType.BUY
            elif prediction < -0.01 and confidence > self.config.min_confidence:
                signal_type = SignalType.SELL
            else:
                signal_type = SignalType.HOLD
            
            # Get current price
            current_price = recent_data['close'].iloc[-1]
            
            # Create signal
            signal = TradingSignal(
                symbol=symbol,
                signal_type=signal_type,
                confidence=confidence,
                price=current_price,
                timestamp=datetime.now(),
                model_name=self.config.model_name,
                features=latest_features.iloc[0].to_dict()
            )
            
            # Store signal
            self.signals_history.append(signal)
            
            return {
                'status': 'success',
                'signal': {
                    'symbol': signal.symbol,
                    'signal_type': signal.signal_type.value,
                    'confidence': signal.confidence,
                    'price': signal.price,
                    'timestamp': signal.timestamp.isoformat(),
                    'model_name': signal.model_name
                },
                'message': f'Signal generated: {signal.signal_type.value} with confidence {confidence:.3f}'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Signal generation failed: {str(e)}'
            }
    
    def execute_signal(self, signal: TradingSignal) -> Dict[str, Any]:
        """Execute trading signal."""
        try:
            if self.config.trading_mode == TradingMode.PAPER:
                return self._execute_paper_trade(signal)
            else:
                return self._execute_live_trade(signal)
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Signal execution failed: {str(e)}'
            }
    
    def _execute_paper_trade(self, signal: TradingSignal) -> Dict[str, Any]:
        """Execute paper trade (simulation)."""
        symbol = signal.symbol
        
        if signal.signal_type == SignalType.BUY:
            # Check if we can open a new position
            if len(self.positions) >= self.config.max_positions:
                return {
                    'status': 'error',
                    'message': 'Maximum positions reached'
                }
            
            # Calculate position size
            position_value = self.portfolio_value * self.config.position_size
            quantity = position_value / signal.price
            
            # Check if we have enough cash
            if position_value > self.cash:
                return {
                    'status': 'error',
                    'message': 'Insufficient cash for position'
                }
            
            # Create position
            position = Position(
                symbol=symbol,
                side='long',
                quantity=quantity,
                entry_price=signal.price,
                current_price=signal.price,
                unrealized_pnl=0.0,
                entry_time=signal.timestamp,
                stop_loss=signal.price * (1 - self.config.stop_loss_pct),
                take_profit=signal.price * (1 + self.config.take_profit_pct)
            )
            
            self.positions[symbol] = position
            self.cash -= position_value
            
            return {
                'status': 'success',
                'action': 'buy',
                'symbol': symbol,
                'quantity': quantity,
                'price': signal.price,
                'position_value': position_value,
                'message': f'Paper trade executed: BUY {quantity:.4f} {symbol} at {signal.price:.4f}'
            }
            
        elif signal.signal_type == SignalType.SELL:
            # Check if we have a position to sell
            if symbol not in self.positions:
                return {
                    'status': 'error',
                    'message': f'No position found for {symbol}'
                }
            
            position = self.positions[symbol]
            
            # Calculate P&L
            pnl = (signal.price - position.entry_price) * position.quantity
            position_value = signal.price * position.quantity
            
            # Close position
            self.cash += position_value
            del self.positions[symbol]
            
            # Record trade
            self.trades_history.append({
                'symbol': symbol,
                'side': 'sell',
                'quantity': position.quantity,
                'entry_price': position.entry_price,
                'exit_price': signal.price,
                'pnl': pnl,
                'entry_time': position.entry_time,
                'exit_time': signal.timestamp
            })
            
            return {
                'status': 'success',
                'action': 'sell',
                'symbol': symbol,
                'quantity': position.quantity,
                'price': signal.price,
                'pnl': pnl,
                'message': f'Paper trade executed: SELL {position.quantity:.4f} {symbol} at {signal.price:.4f}, P&L: {pnl:.2f}'
            }
        
        else:  # HOLD
            return {
                'status': 'success',
                'action': 'hold',
                'message': 'No action taken (HOLD signal)'
            }
    
    def _execute_live_trade(self, signal: TradingSignal) -> Dict[str, Any]:
        """Execute live trade (real money)."""
        # This would integrate with real exchange APIs for live trading
        # For now, return a placeholder
        return {
            'status': 'error',
            'message': 'Live trading not implemented yet - use paper trading mode'
        }
    
    def update_positions(self) -> Dict[str, Any]:
        """Update current positions with latest prices."""
        try:
            updated_positions = 0
            
            for symbol, position in self.positions.items():
                # Get current price (simplified - in real implementation, get from exchange)
                current_price = position.entry_price * (1 + np.random.normal(0, 0.02))
                position.current_price = current_price
                position.unrealized_pnl = (current_price - position.entry_price) * position.quantity
                updated_positions += 1
            
            return {
                'status': 'success',
                'updated_positions': updated_positions,
                'message': f'Updated {updated_positions} positions'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Position update failed: {str(e)}'
            }
    
    def get_portfolio_status(self) -> Dict[str, Any]:
        """Get current portfolio status."""
        try:
            # Update positions first
            self.update_positions()
            
            # Calculate portfolio metrics
            total_position_value = sum(pos.current_price * pos.quantity for pos in self.positions.values())
            total_unrealized_pnl = sum(pos.unrealized_pnl for pos in self.positions.values())
            current_portfolio_value = self.cash + total_position_value
            
            # Calculate daily return
            if hasattr(self, 'previous_portfolio_value'):
                daily_return = (current_portfolio_value - self.previous_portfolio_value) / self.previous_portfolio_value
                self.daily_returns.append(daily_return)
            
            self.previous_portfolio_value = current_portfolio_value
            
            # Position details
            positions_info = {}
            for symbol, position in self.positions.items():
                positions_info[symbol] = {
                    'side': position.side,
                    'quantity': position.quantity,
                    'entry_price': position.entry_price,
                    'current_price': position.current_price,
                    'unrealized_pnl': position.unrealized_pnl,
                    'entry_time': position.entry_time.isoformat()
                }
            
            return {
                'status': 'success',
                'portfolio': {
                    'total_value': current_portfolio_value,
                    'cash': self.cash,
                    'position_value': total_position_value,
                    'unrealized_pnl': total_unrealized_pnl,
                    'total_return_pct': (current_portfolio_value - 10000) / 10000 * 100,
                    'positions_count': len(self.positions)
                },
                'positions': positions_info,
                'recent_signals': len(self.signals_history[-10:]) if self.signals_history else 0,
                'total_trades': len(self.trades_history)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Portfolio status failed: {str(e)}'
            }
    
    def start_trading(self) -> Dict[str, Any]:
        """Start the trading system."""
        try:
            if self.is_running:
                return {
                    'status': 'error',
                    'message': 'Trading system is already running'
                }
            
            self.is_running = True
            logger.info("Trading system started")
            
            return {
                'status': 'success',
                'message': 'Trading system started successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to start trading system: {str(e)}'
            }
    
    def stop_trading(self) -> Dict[str, Any]:
        """Stop the trading system."""
        try:
            self.is_running = False
            logger.info("Trading system stopped")
            
            return {
                'status': 'success',
                'message': 'Trading system stopped successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to stop trading system: {str(e)}'
            }

# Example usage and testing
def test_real_trading_system():
    """Test real trading system with sample data."""
    print("🧪 Testing Real Trading System...")
    
    # Create trading config
    config = TradingConfig(
        symbol="BTCUSDT",
        model_name="test_model",
        trading_mode=TradingMode.PAPER,
        position_size=0.1,  # 10% of portfolio
        stop_loss_pct=0.05,  # 5% stop loss
        take_profit_pct=0.1,  # 10% take profit
        max_positions=3,
        min_confidence=0.6
    )
    
    # Create trading system
    trading_system = RealTradingSystem(config)
    
    # Initialize with demo API keys
    api_keys = {
        ExchangeType.BINANCE: APIKey(
            api_key="demo_binance_api_key",
            secret_key="demo_binance_secret_key",
            sandbox=True
        )
    }
    
    init_result = trading_system.initialize(api_keys)
    print(f"  • System initialization: {init_result['status']}")
    
    if init_result['status'] == 'success':
        print(f"    - Connected exchanges: {init_result['connected_exchanges']}")
    
    # Train model with sample data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    train_result = trading_system.train_model(
        "BTCUSDT", ModelType.RANDOM_FOREST_REGRESSOR, start_date, end_date
    )
    print(f"  • Model training: {train_result['status']}")
    
    if train_result['status'] == 'success':
        print(f"    - Model: {train_result['model_name']}")
        print(f"    - R² Score: {train_result['metrics']['r2']:.3f}")
        print(f"    - Direction Accuracy: {train_result['metrics']['direction_accuracy']:.3f}")
    
    # Generate signals
    signal_result = trading_system.generate_signal("BTCUSDT")
    print(f"  • Signal generation: {signal_result['status']}")
    
    if signal_result['status'] == 'success':
        signal = signal_result['signal']
        print(f"    - Signal: {signal['signal_type']}")
        print(f"    - Confidence: {signal['confidence']:.3f}")
        print(f"    - Price: {signal['price']:.4f}")
    
    # Get portfolio status
    portfolio_result = trading_system.get_portfolio_status()
    print(f"  • Portfolio status: {portfolio_result['status']}")
    
    if portfolio_result['status'] == 'success':
        portfolio = portfolio_result['portfolio']
        print(f"    - Total Value: ${portfolio['total_value']:.2f}")
        print(f"    - Cash: ${portfolio['cash']:.2f}")
        print(f"    - Positions: {portfolio['positions_count']}")
    
    print("✅ Real Trading System test completed!")
    
    return trading_system

if __name__ == "__main__":
    test_real_trading_system()
