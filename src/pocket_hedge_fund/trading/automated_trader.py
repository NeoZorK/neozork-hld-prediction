"""
Automated Trader for Pocket Hedge Fund.

This module provides automated trading functionality using ML predictions
and technical analysis signals.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import asyncio
from enum import Enum

from ..ml.price_predictor import PricePredictor
from ..portfolio.portfolio_manager import PortfolioManager
from ..data.data_manager import DataManager
from ..analysis.indicator_integration_simple import IndicatorIntegration

logger = logging.getLogger(__name__)

class TradingSignal(Enum):
    """Trading signal types."""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    CLOSE = "CLOSE"

class TradingStrategy(Enum):
    """Trading strategy types."""
    ML_ONLY = "ml_only"
    TECHNICAL_ONLY = "technical_only"
    COMBINED = "combined"
    CONSERVATIVE = "conservative"
    AGGRESSIVE = "aggressive"

class AutomatedTrader:
    """Automated trading system using ML and technical analysis."""
    
    def __init__(self, fund_id: str, strategy: TradingStrategy = TradingStrategy.COMBINED):
        """Initialize AutomatedTrader."""
        self.fund_id = fund_id
        self.strategy = strategy
        self.is_active = False
        self.trading_enabled = False
        
        # Initialize components
        self.price_predictor = PricePredictor(model_type="ensemble")
        self.portfolio_manager = PortfolioManager(fund_id)
        self.data_manager = DataManager()
        self.indicator_integration = IndicatorIntegration()
        
        # Trading parameters
        self.trading_params = {
            'min_confidence': 0.6,  # Minimum confidence for ML signals
            'min_signal_strength': 0.7,  # Minimum signal strength
            'max_position_size': 0.1,  # Maximum position size (10%)
            'stop_loss_pct': 0.05,  # Stop loss percentage (5%)
            'take_profit_pct': 0.15,  # Take profit percentage (15%)
            'rebalance_threshold': 0.05,  # Rebalance threshold (5%)
            'max_daily_trades': 10,  # Maximum trades per day
            'cooldown_minutes': 30  # Cooldown between trades
        }
        
        # Trading history
        self.trading_history = []
        self.daily_trades = {}
        self.last_trade_time = {}
        
        # Performance tracking
        self.performance_metrics = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_pnl': 0.0,
            'max_drawdown': 0.0,
            'sharpe_ratio': 0.0,
            'win_rate': 0.0
        }
    
    async def initialize(self) -> Dict[str, Any]:
        """Initialize the automated trading system."""
        try:
            logger.info(f"Initializing automated trader for fund {self.fund_id}")
            
            # Load ML models
            model_loaded = await self.price_predictor.load_models()
            if not model_loaded:
                logger.warning("No pre-trained ML models found, will train on first data")
            
            # Initialize portfolio
            portfolio_summary = self.portfolio_manager.get_portfolio_summary()
            
            return {
                'status': 'success',
                'message': 'Automated trader initialized successfully',
                'fund_id': self.fund_id,
                'strategy': self.strategy.value,
                'ml_models_loaded': model_loaded,
                'portfolio_value': portfolio_summary.get('portfolio_value', 0),
                'trading_params': self.trading_params
            }
            
        except Exception as e:
            logger.error(f"Error initializing automated trader: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    async def train_models(self, symbols: List[str], lookback_days: int = 365) -> Dict[str, Any]:
        """Train ML models on historical data."""
        try:
            logger.info(f"Training ML models for symbols: {symbols}")
            
            training_results = {}
            
            for symbol in symbols:
                try:
                    # Get historical data
                    if symbol.startswith('data/'):
                        data = await self.data_manager.get_local_data(symbol)
                    else:
                        data = await self.data_manager.get_yahoo_data(symbol, period=f"{lookback_days}d")
                    
                    if data.empty:
                        logger.warning(f"No data available for {symbol}")
                        continue
                    
                    # Train models
                    result = await self.price_predictor.train_models(data)
                    training_results[symbol] = result
                    
                    logger.info(f"Training completed for {symbol}")
                    
                except Exception as e:
                    logger.error(f"Error training models for {symbol}: {e}")
                    training_results[symbol] = {'error': str(e)}
            
            return {
                'status': 'success',
                'message': 'ML model training completed',
                'training_results': training_results
            }
            
        except Exception as e:
            logger.error(f"Error training models: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    async def generate_trading_signals(self, symbol: str, current_price: float) -> Dict[str, Any]:
        """Generate trading signals using ML and technical analysis."""
        try:
            logger.info(f"Generating trading signals for {symbol}")
            
            signals = {
                'symbol': symbol,
                'timestamp': datetime.now(),
                'current_price': current_price,
                'ml_signal': None,
                'technical_signal': None,
                'combined_signal': None,
                'confidence': 0.0,
                'reasoning': []
            }
            
            # Get latest data for analysis
            if symbol.startswith('data/'):
                data = await self.data_manager.get_local_data(symbol)
            else:
                data = await self.data_manager.get_yahoo_data(symbol, period="30d")
            
            if data.empty:
                return {
                    'status': 'error',
                    'message': f'No data available for {symbol}'
                }
            
            # ML Signal
            if self.strategy in [TradingStrategy.ML_ONLY, TradingStrategy.COMBINED]:
                try:
                    ml_prediction = await self.price_predictor.predict(data)
                    if ml_prediction['status'] == 'success':
                        ensemble_pred = ml_prediction['predictions'].get('ensemble', {})
                        if ensemble_pred and 'prediction' in ensemble_pred:
                            ml_return = ensemble_pred['prediction']
                            ml_confidence = ensemble_pred['confidence']
                            
                            if ml_confidence >= self.trading_params['min_confidence']:
                                if ml_return > 0.02:  # 2% positive return threshold
                                    signals['ml_signal'] = TradingSignal.BUY
                                    signals['reasoning'].append(f"ML predicts {ml_return:.2%} return with {ml_confidence:.2%} confidence")
                                elif ml_return < -0.02:  # 2% negative return threshold
                                    signals['ml_signal'] = TradingSignal.SELL
                                    signals['reasoning'].append(f"ML predicts {ml_return:.2%} return with {ml_confidence:.2%} confidence")
                                else:
                                    signals['ml_signal'] = TradingSignal.HOLD
                                    signals['reasoning'].append(f"ML predicts neutral return: {ml_return:.2%}")
                            else:
                                signals['ml_signal'] = TradingSignal.HOLD
                                signals['reasoning'].append(f"ML confidence too low: {ml_confidence:.2%}")
                        
                except Exception as e:
                    logger.error(f"Error generating ML signal: {e}")
                    signals['reasoning'].append(f"ML signal error: {str(e)}")
            
            # Technical Signal
            if self.strategy in [TradingStrategy.TECHNICAL_ONLY, TradingStrategy.COMBINED]:
                try:
                    await self.indicator_integration.calculate_indicators(data, symbol)
                    technical_signals = self.indicator_integration.get_trading_signals(symbol)
                    
                    if technical_signals['overall_signal'] != 'ERROR':
                        overall_signal = technical_signals['overall_signal']
                        confidence = technical_signals['confidence']
                        
                        if overall_signal == 'BUY':
                            signals['technical_signal'] = TradingSignal.BUY
                        elif overall_signal == 'SELL':
                            signals['technical_signal'] = TradingSignal.SELL
                        else:
                            signals['technical_signal'] = TradingSignal.HOLD
                        
                        signals['reasoning'].append(f"Technical analysis: {overall_signal} with {confidence:.2%} confidence")
                        
                except Exception as e:
                    logger.error(f"Error generating technical signal: {e}")
                    signals['reasoning'].append(f"Technical signal error: {str(e)}")
            
            # Combine signals based on strategy
            signals['combined_signal'] = self._combine_signals(signals['ml_signal'], signals['technical_signal'])
            signals['confidence'] = self._calculate_signal_confidence(signals)
            
            return {
                'status': 'success',
                'signals': signals
            }
            
        except Exception as e:
            logger.error(f"Error generating trading signals: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _combine_signals(self, ml_signal: Optional[TradingSignal], technical_signal: Optional[TradingSignal]) -> TradingSignal:
        """Combine ML and technical signals based on strategy."""
        if self.strategy == TradingStrategy.ML_ONLY:
            return ml_signal or TradingSignal.HOLD
        elif self.strategy == TradingStrategy.TECHNICAL_ONLY:
            return technical_signal or TradingSignal.HOLD
        elif self.strategy == TradingStrategy.COMBINED:
            # Both signals must agree for action
            if ml_signal == technical_signal and ml_signal in [TradingSignal.BUY, TradingSignal.SELL]:
                return ml_signal
            else:
                return TradingSignal.HOLD
        elif self.strategy == TradingStrategy.CONSERVATIVE:
            # More conservative - require strong signals
            if ml_signal == TradingSignal.BUY and technical_signal in [TradingSignal.BUY, TradingSignal.HOLD]:
                return TradingSignal.BUY
            elif ml_signal == TradingSignal.SELL and technical_signal in [TradingSignal.SELL, TradingSignal.HOLD]:
                return TradingSignal.SELL
            else:
                return TradingSignal.HOLD
        elif self.strategy == TradingStrategy.AGGRESSIVE:
            # More aggressive - any strong signal
            if ml_signal == TradingSignal.BUY or technical_signal == TradingSignal.BUY:
                return TradingSignal.BUY
            elif ml_signal == TradingSignal.SELL or technical_signal == TradingSignal.SELL:
                return TradingSignal.SELL
            else:
                return TradingSignal.HOLD
        else:
            return TradingSignal.HOLD
    
    def _calculate_signal_confidence(self, signals: Dict[str, Any]) -> float:
        """Calculate overall signal confidence."""
        confidences = []
        
        if signals['ml_signal'] and signals['ml_signal'] != TradingSignal.HOLD:
            # Get ML confidence from prediction
            confidences.append(0.8)  # Placeholder - would get from actual prediction
        
        if signals['technical_signal'] and signals['technical_signal'] != TradingSignal.HOLD:
            # Get technical confidence from indicators
            confidences.append(0.7)  # Placeholder - would get from actual indicators
        
        if confidences:
            return np.mean(confidences)
        else:
            return 0.0
    
    async def execute_trade(self, symbol: str, signal: TradingSignal, current_price: float) -> Dict[str, Any]:
        """Execute a trade based on the signal."""
        try:
            if not self.trading_enabled:
                return {
                    'status': 'error',
                    'message': 'Trading is disabled'
                }
            
            # Check cooldown
            if symbol in self.last_trade_time:
                time_since_last = datetime.now() - self.last_trade_time[symbol]
                if time_since_last.total_seconds() < self.trading_params['cooldown_minutes'] * 60:
                    return {
                        'status': 'error',
                        'message': f'Cooldown active for {symbol}'
                    }
            
            # Check daily trade limit
            today = datetime.now().date()
            daily_trades = self.daily_trades.get(today, 0)
            if daily_trades >= self.trading_params['max_daily_trades']:
                return {
                    'status': 'error',
                    'message': 'Daily trade limit reached'
                }
            
            # Get current portfolio
            portfolio_summary = self.portfolio_manager.get_portfolio_summary()
            portfolio_value = portfolio_summary['portfolio_value']
            
            # Calculate position size
            max_position_value = portfolio_value * self.trading_params['max_position_size']
            position_size = min(max_position_value, portfolio_value * 0.05)  # 5% of portfolio
            
            trade_result = None
            
            if signal == TradingSignal.BUY:
                # Buy position
                quantity = position_size / current_price
                trade_result = await self.portfolio_manager.add_position(
                    symbol=symbol,
                    quantity=quantity,
                    price=current_price,
                    position_type="LONG",
                    stop_loss=current_price * (1 - self.trading_params['stop_loss_pct']),
                    take_profit=current_price * (1 + self.trading_params['take_profit_pct'])
                )
                
            elif signal == TradingSignal.SELL:
                # Close existing position or short
                if symbol in self.portfolio_manager.positions:
                    trade_result = await self.portfolio_manager.close_position(
                        symbol=symbol,
                        price=current_price
                    )
                else:
                    # Short position (if supported)
                    quantity = position_size / current_price
                    trade_result = await self.portfolio_manager.add_position(
                        symbol=symbol,
                        quantity=quantity,
                        price=current_price,
                        position_type="SHORT",
                        stop_loss=current_price * (1 + self.trading_params['stop_loss_pct']),
                        take_profit=current_price * (1 - self.trading_params['take_profit_pct'])
                    )
            
            # Record trade
            if trade_result and trade_result.get('status') == 'success':
                self.trading_history.append({
                    'timestamp': datetime.now(),
                    'symbol': symbol,
                    'signal': signal.value,
                    'price': current_price,
                    'result': trade_result
                })
                
                self.last_trade_time[symbol] = datetime.now()
                self.daily_trades[today] = daily_trades + 1
                
                # Update performance metrics
                self._update_performance_metrics(trade_result)
                
                return {
                    'status': 'success',
                    'message': f'Trade executed: {signal.value} {symbol}',
                    'trade_result': trade_result
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Failed to execute trade: {trade_result.get("message", "Unknown error")}'
                }
            
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _update_performance_metrics(self, trade_result: Dict[str, Any]):
        """Update performance metrics after a trade."""
        try:
            self.performance_metrics['total_trades'] += 1
            
            if 'pnl' in trade_result:
                pnl = trade_result['pnl']
                self.performance_metrics['total_pnl'] += pnl
                
                if pnl > 0:
                    self.performance_metrics['winning_trades'] += 1
                else:
                    self.performance_metrics['losing_trades'] += 1
            
            # Calculate win rate
            if self.performance_metrics['total_trades'] > 0:
                self.performance_metrics['win_rate'] = (
                    self.performance_metrics['winning_trades'] / 
                    self.performance_metrics['total_trades']
                )
            
        except Exception as e:
            logger.error(f"Error updating performance metrics: {e}")
    
    async def run_trading_cycle(self, symbols: List[str]) -> Dict[str, Any]:
        """Run a complete trading cycle for all symbols."""
        try:
            if not self.is_active:
                return {
                    'status': 'error',
                    'message': 'Automated trader is not active'
                }
            
            logger.info(f"Running trading cycle for symbols: {symbols}")
            
            cycle_results = {
                'timestamp': datetime.now(),
                'symbols_processed': 0,
                'signals_generated': 0,
                'trades_executed': 0,
                'results': {}
            }
            
            for symbol in symbols:
                try:
                    # Get current price (simplified - would get from real data source)
                    current_price = 100.0  # Placeholder
                    
                    # Generate signals
                    signal_result = await self.generate_trading_signals(symbol, current_price)
                    
                    if signal_result['status'] == 'success':
                        signals = signal_result['signals']
                        cycle_results['signals_generated'] += 1
                        
                        # Execute trade if signal is strong enough
                        if (signals['combined_signal'] != TradingSignal.HOLD and 
                            signals['confidence'] >= self.trading_params['min_signal_strength']):
                            
                            trade_result = await self.execute_trade(
                                symbol, signals['combined_signal'], current_price
                            )
                            
                            if trade_result['status'] == 'success':
                                cycle_results['trades_executed'] += 1
                        
                        cycle_results['results'][symbol] = {
                            'signals': signals,
                            'trade_result': trade_result if 'trade_result' in locals() else None
                        }
                    
                    cycle_results['symbols_processed'] += 1
                    
                except Exception as e:
                    logger.error(f"Error processing {symbol}: {e}")
                    cycle_results['results'][symbol] = {'error': str(e)}
            
            return {
                'status': 'success',
                'cycle_results': cycle_results
            }
            
        except Exception as e:
            logger.error(f"Error running trading cycle: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary of the automated trader."""
        portfolio_summary = self.portfolio_manager.get_portfolio_summary()
        
        return {
            'fund_id': self.fund_id,
            'strategy': self.strategy.value,
            'is_active': self.is_active,
            'trading_enabled': self.trading_enabled,
            'performance_metrics': self.performance_metrics,
            'portfolio_summary': portfolio_summary,
            'trading_params': self.trading_params,
            'total_trades_today': self.daily_trades.get(datetime.now().date(), 0)
        }
    
    def update_trading_params(self, new_params: Dict[str, Any]) -> Dict[str, Any]:
        """Update trading parameters."""
        try:
            for key, value in new_params.items():
                if key in self.trading_params:
                    self.trading_params[key] = value
                    logger.info(f"Updated {key} to {value}")
            
            return {
                'status': 'success',
                'message': 'Trading parameters updated',
                'updated_params': new_params
            }
            
        except Exception as e:
            logger.error(f"Error updating trading parameters: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def start_trading(self):
        """Start automated trading."""
        self.is_active = True
        self.trading_enabled = True
        logger.info(f"Automated trading started for fund {self.fund_id}")
    
    def stop_trading(self):
        """Stop automated trading."""
        self.is_active = False
        self.trading_enabled = False
        logger.info(f"Automated trading stopped for fund {self.fund_id}")
    
    def pause_trading(self):
        """Pause trading (keep active but don't execute trades)."""
        self.trading_enabled = False
        logger.info(f"Automated trading paused for fund {self.fund_id}")
    
    def resume_trading(self):
        """Resume trading."""
        if self.is_active:
            self.trading_enabled = True
            logger.info(f"Automated trading resumed for fund {self.fund_id}")
