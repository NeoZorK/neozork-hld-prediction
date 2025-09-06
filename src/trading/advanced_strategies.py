"""
Advanced Trading Strategies System
Multi-strategy systems, adaptive algorithms, market regime detection
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import uuid
import json
from abc import ABC, abstractmethod
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StrategyType(Enum):
    """Strategy type enumeration"""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    ARBITRAGE = "arbitrage"
    MARKET_MAKING = "market_making"
    TREND_FOLLOWING = "trend_following"
    BREAKOUT = "breakout"
    SCALPING = "scalping"
    SWING = "swing"
    POSITION = "position"
    HEDGE = "hedge"

class MarketRegime(Enum):
    """Market regime enumeration"""
    TRENDING = "trending"
    RANGING = "ranging"
    VOLATILE = "volatile"
    LOW_VOLATILITY = "low_volatility"
    HIGH_VOLATILITY = "high_volatility"
    BULL_MARKET = "bull_market"
    BEAR_MARKET = "bear_market"
    SIDEWAYS = "sideways"

class SignalType(Enum):
    """Signal type enumeration"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    CLOSE = "close"
    HEDGE = "hedge"
    SCALE_IN = "scale_in"
    SCALE_OUT = "scale_out"

class StrategyStatus(Enum):
    """Strategy status enumeration"""
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"
    MAINTENANCE = "maintenance"

@dataclass
class TradingSignal:
    """Trading signal"""
    signal_id: str
    strategy_id: str
    signal_type: SignalType
    symbol: str
    price: float
    quantity: float
    confidence: float
    reasoning: str
    timestamp: datetime
    metadata: Dict[str, Any]

@dataclass
class StrategyConfig:
    """Strategy configuration"""
    config_id: str
    strategy_type: StrategyType
    name: str
    description: str
    parameters: Dict[str, Any]
    risk_limits: Dict[str, float]
    position_sizing: Dict[str, Any]
    entry_conditions: List[Dict[str, Any]]
    exit_conditions: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

@dataclass
class StrategyPerformance:
    """Strategy performance metrics"""
    strategy_id: str
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    calmar_ratio: float
    sortino_ratio: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    largest_win: float
    largest_loss: float
    volatility: float
    beta: float
    alpha: float
    information_ratio: float
    tracking_error: float
    period: str
    start_date: datetime
    end_date: datetime

class MarketRegimeDetector:
    """Market regime detection system"""
    
    def __init__(self):
        self.regime_models = {}
        self.current_regime = MarketRegime.SIDEWAYS
        self.regime_history = []
        self.transition_probabilities = {}
        
    async def detect_regime(self, data: pd.DataFrame, lookback_period: int = 50) -> MarketRegime:
        """Detect current market regime"""
        if len(data) < lookback_period:
            return MarketRegime.SIDEWAYS
        
        # Calculate regime indicators
        returns = data['close'].pct_change().dropna()
        volatility = returns.rolling(window=20).std()
        trend_strength = self._calculate_trend_strength(data, lookback_period)
        momentum = self._calculate_momentum(data, lookback_period)
        
        # Regime classification logic
        current_volatility = volatility.iloc[-1]
        avg_volatility = volatility.mean()
        
        # High volatility regime
        if current_volatility > avg_volatility * 1.5:
            regime = MarketRegime.HIGH_VOLATILITY
        # Low volatility regime
        elif current_volatility < avg_volatility * 0.5:
            regime = MarketRegime.LOW_VOLATILITY
        # Trending regime
        elif abs(trend_strength) > 0.6:
            if trend_strength > 0:
                regime = MarketRegime.BULL_MARKET
            else:
                regime = MarketRegime.BEAR_MARKET
        # Ranging regime
        elif abs(trend_strength) < 0.3:
            regime = MarketRegime.RANGING
        else:
            regime = MarketRegime.SIDEWAYS
        
        # Update regime history
        self.regime_history.append({
            'regime': regime,
            'timestamp': datetime.now(),
            'volatility': current_volatility,
            'trend_strength': trend_strength,
            'momentum': momentum
        })
        
        self.current_regime = regime
        logger.info(f"Detected market regime: {regime.value}")
        return regime
    
    def _calculate_trend_strength(self, data: pd.DataFrame, period: int) -> float:
        """Calculate trend strength"""
        if len(data) < period:
            return 0.0
        
        # Linear regression slope
        x = np.arange(period)
        y = data['close'].iloc[-period:].values
        
        if len(y) != period:
            return 0.0
        
        # Calculate slope
        slope = np.polyfit(x, y, 1)[0]
        
        # Normalize by price level
        normalized_slope = slope / y[-1]
        
        return normalized_slope
    
    def _calculate_momentum(self, data: pd.DataFrame, period: int) -> float:
        """Calculate momentum indicator"""
        if len(data) < period:
            return 0.0
        
        # Rate of change
        current_price = data['close'].iloc[-1]
        past_price = data['close'].iloc[-period]
        
        momentum = (current_price - past_price) / past_price
        return momentum
    
    async def get_regime_probabilities(self, data: pd.DataFrame) -> Dict[MarketRegime, float]:
        """Get regime transition probabilities"""
        if len(self.regime_history) < 10:
            # Default probabilities
            return {
                MarketRegime.TRENDING: 0.3,
                MarketRegime.RANGING: 0.4,
                MarketRegime.VOLATILE: 0.2,
                MarketRegime.LOW_VOLATILITY: 0.1
            }
        
        # Calculate transition probabilities based on history
        regime_counts = {}
        for entry in self.regime_history[-50:]:  # Last 50 observations
            regime = entry['regime']
            regime_counts[regime] = regime_counts.get(regime, 0) + 1
        
        total = sum(regime_counts.values())
        probabilities = {}
        
        for regime in MarketRegime:
            probabilities[regime] = regime_counts.get(regime, 0) / total
        
        return probabilities
    
    async def predict_regime_transition(self, data: pd.DataFrame) -> Tuple[MarketRegime, float]:
        """Predict next regime transition"""
        current_regime = await self.detect_regime(data)
        probabilities = await self.get_regime_probabilities(data)
        
        # Find most likely next regime
        next_regime = max(probabilities, key=probabilities.get)
        confidence = probabilities[next_regime]
        
        return next_regime, confidence

class AdaptiveStrategy:
    """Base class for adaptive trading strategies"""
    
    def __init__(self, config: StrategyConfig):
        self.config = config
        self.status = StrategyStatus.ACTIVE
        self.positions = {}
        self.signals = []
        self.performance_history = []
        self.adaptation_history = []
        
    @abstractmethod
    async def generate_signal(self, data: pd.DataFrame, market_regime: MarketRegime) -> Optional[TradingSignal]:
        """Generate trading signal"""
        pass
    
    @abstractmethod
    async def adapt_parameters(self, performance_feedback: Dict[str, float]) -> bool:
        """Adapt strategy parameters based on performance"""
        pass
    
    async def calculate_position_size(self, signal: TradingSignal, portfolio_value: float) -> float:
        """Calculate position size based on risk management"""
        risk_per_trade = self.config.risk_limits.get('risk_per_trade', 0.02)
        stop_loss = self.config.risk_limits.get('stop_loss', 0.05)
        
        # Kelly Criterion position sizing
        if 'win_rate' in self.config.parameters and 'avg_win_loss_ratio' in self.config.parameters:
            win_rate = self.config.parameters['win_rate']
            avg_win_loss_ratio = self.config.parameters['avg_win_loss_ratio']
            
            kelly_fraction = (win_rate * avg_win_loss_ratio - (1 - win_rate)) / avg_win_loss_ratio
            kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
        else:
            kelly_fraction = 0.1  # Default 10%
        
        # Risk-based position sizing
        risk_amount = portfolio_value * risk_per_trade
        position_size = risk_amount / (signal.price * stop_loss)
        
        # Apply Kelly fraction
        final_position_size = position_size * kelly_fraction
        
        return min(final_position_size, portfolio_value * 0.2)  # Max 20% of portfolio
    
    async def update_performance(self, trade_result: Dict[str, Any]) -> None:
        """Update strategy performance"""
        self.performance_history.append({
            'timestamp': datetime.now(),
            'trade_result': trade_result,
            'strategy_id': self.config.config_id
        })
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.performance_history:
            return {}
        
        returns = [entry['trade_result'].get('return', 0) for entry in self.performance_history]
        
        if not returns:
            return {}
        
        total_return = sum(returns)
        win_rate = len([r for r in returns if r > 0]) / len(returns)
        avg_return = np.mean(returns)
        volatility = np.std(returns)
        
        return {
            'total_return': total_return,
            'win_rate': win_rate,
            'avg_return': avg_return,
            'volatility': volatility,
            'total_trades': len(returns),
            'sharpe_ratio': avg_return / volatility if volatility > 0 else 0
        }

class MomentumStrategy(AdaptiveStrategy):
    """Momentum trading strategy"""
    
    async def generate_signal(self, data: pd.DataFrame, market_regime: MarketRegime) -> Optional[TradingSignal]:
        """Generate momentum signal"""
        if len(data) < 50:
            return None
        
        # Calculate momentum indicators
        rsi = self._calculate_rsi(data, 14)
        macd = self._calculate_macd(data)
        price_momentum = self._calculate_price_momentum(data, 20)
        
        # Entry conditions
        if (rsi > 50 and macd['macd'] > macd['signal'] and price_momentum > 0.02 and 
            market_regime in [MarketRegime.TRENDING, MarketRegime.BULL_MARKET]):
            
            signal = TradingSignal(
                signal_id=str(uuid.uuid4()),
                strategy_id=self.config.config_id,
                signal_type=SignalType.BUY,
                symbol=data.index.name or "UNKNOWN",
                price=data['close'].iloc[-1],
                quantity=0.0,  # Will be calculated later
                confidence=min(0.9, (rsi - 50) / 50 + 0.5),
                reasoning=f"Momentum buy: RSI={rsi:.2f}, MACD bullish, momentum={price_momentum:.3f}",
                timestamp=datetime.now(),
                metadata={'rsi': rsi, 'macd': macd, 'momentum': price_momentum}
            )
            return signal
        
        # Exit conditions
        elif (rsi < 30 or macd['macd'] < macd['signal'] or price_momentum < -0.02):
            signal = TradingSignal(
                signal_id=str(uuid.uuid4()),
                strategy_id=self.config.config_id,
                signal_type=SignalType.SELL,
                symbol=data.index.name or "UNKNOWN",
                price=data['close'].iloc[-1],
                quantity=0.0,
                confidence=0.8,
                reasoning=f"Momentum sell: RSI={rsi:.2f}, MACD bearish, momentum={price_momentum:.3f}",
                timestamp=datetime.now(),
                metadata={'rsi': rsi, 'macd': macd, 'momentum': price_momentum}
            )
            return signal
        
        return None
    
    def _calculate_rsi(self, data: pd.DataFrame, period: int) -> float:
        """Calculate RSI"""
        if len(data) < period + 1:
            return 50.0
        
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50.0
    
    def _calculate_macd(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate MACD"""
        if len(data) < 26:
            return {'macd': 0, 'signal': 0, 'histogram': 0}
        
        ema_12 = data['close'].ewm(span=12).mean()
        ema_26 = data['close'].ewm(span=26).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal
        
        return {
            'macd': macd.iloc[-1],
            'signal': signal.iloc[-1],
            'histogram': histogram.iloc[-1]
        }
    
    def _calculate_price_momentum(self, data: pd.DataFrame, period: int) -> float:
        """Calculate price momentum"""
        if len(data) < period:
            return 0.0
        
        current_price = data['close'].iloc[-1]
        past_price = data['close'].iloc[-period]
        
        return (current_price - past_price) / past_price
    
    async def adapt_parameters(self, performance_feedback: Dict[str, float]) -> bool:
        """Adapt momentum strategy parameters"""
        try:
            # Adjust RSI thresholds based on performance
            if performance_feedback.get('win_rate', 0.5) < 0.4:
                # Lower RSI threshold for more signals
                self.config.parameters['rsi_oversold'] = max(20, self.config.parameters.get('rsi_oversold', 30) - 5)
                self.config.parameters['rsi_overbought'] = min(80, self.config.parameters.get('rsi_overbought', 70) + 5)
            elif performance_feedback.get('win_rate', 0.5) > 0.7:
                # Higher RSI threshold for fewer, higher quality signals
                self.config.parameters['rsi_oversold'] = min(40, self.config.parameters.get('rsi_oversold', 30) + 5)
                self.config.parameters['rsi_overbought'] = max(60, self.config.parameters.get('rsi_overbought', 70) - 5)
            
            # Adjust momentum threshold
            if performance_feedback.get('volatility', 0.1) > 0.15:
                # Increase momentum threshold in high volatility
                self.config.parameters['momentum_threshold'] = self.config.parameters.get('momentum_threshold', 0.02) * 1.5
            else:
                # Decrease momentum threshold in low volatility
                self.config.parameters['momentum_threshold'] = self.config.parameters.get('momentum_threshold', 0.02) * 0.8
            
            self.adaptation_history.append({
                'timestamp': datetime.now(),
                'performance_feedback': performance_feedback,
                'new_parameters': self.config.parameters.copy()
            })
            
            logger.info("Momentum strategy parameters adapted")
            return True
            
        except Exception as e:
            logger.error(f"Error adapting momentum strategy: {e}")
            return False

class MeanReversionStrategy(AdaptiveStrategy):
    """Mean reversion trading strategy"""
    
    async def generate_signal(self, data: pd.DataFrame, market_regime: MarketRegime) -> Optional[TradingSignal]:
        """Generate mean reversion signal"""
        if len(data) < 50:
            return None
        
        # Calculate mean reversion indicators
        bollinger_bands = self._calculate_bollinger_bands(data, 20, 2)
        z_score = self._calculate_z_score(data, 20)
        rsi = self._calculate_rsi(data, 14)
        
        # Entry conditions (oversold)
        if (data['close'].iloc[-1] < bollinger_bands['lower'] and 
            z_score < -2 and rsi < 30 and 
            market_regime in [MarketRegime.RANGING, MarketRegime.SIDEWAYS]):
            
            signal = TradingSignal(
                signal_id=str(uuid.uuid4()),
                strategy_id=self.config.config_id,
                signal_type=SignalType.BUY,
                symbol=data.index.name or "UNKNOWN",
                price=data['close'].iloc[-1],
                quantity=0.0,
                confidence=min(0.9, abs(z_score) / 3),
                reasoning=f"Mean reversion buy: Price below BB lower, Z-score={z_score:.2f}, RSI={rsi:.2f}",
                timestamp=datetime.now(),
                metadata={'bollinger_bands': bollinger_bands, 'z_score': z_score, 'rsi': rsi}
            )
            return signal
        
        # Exit conditions (overbought)
        elif (data['close'].iloc[-1] > bollinger_bands['upper'] and 
              z_score > 2 and rsi > 70):
            
            signal = TradingSignal(
                signal_id=str(uuid.uuid4()),
                strategy_id=self.config.config_id,
                signal_type=SignalType.SELL,
                symbol=data.index.name or "UNKNOWN",
                price=data['close'].iloc[-1],
                quantity=0.0,
                confidence=min(0.9, abs(z_score) / 3),
                reasoning=f"Mean reversion sell: Price above BB upper, Z-score={z_score:.2f}, RSI={rsi:.2f}",
                timestamp=datetime.now(),
                metadata={'bollinger_bands': bollinger_bands, 'z_score': z_score, 'rsi': rsi}
            )
            return signal
        
        return None
    
    def _calculate_bollinger_bands(self, data: pd.DataFrame, period: int, std_dev: float) -> Dict[str, float]:
        """Calculate Bollinger Bands"""
        if len(data) < period:
            return {'upper': 0, 'middle': 0, 'lower': 0}
        
        sma = data['close'].rolling(window=period).mean()
        std = data['close'].rolling(window=period).std()
        
        return {
            'upper': sma.iloc[-1] + (std.iloc[-1] * std_dev),
            'middle': sma.iloc[-1],
            'lower': sma.iloc[-1] - (std.iloc[-1] * std_dev)
        }
    
    def _calculate_z_score(self, data: pd.DataFrame, period: int) -> float:
        """Calculate Z-score"""
        if len(data) < period:
            return 0.0
        
        current_price = data['close'].iloc[-1]
        mean_price = data['close'].rolling(window=period).mean().iloc[-1]
        std_price = data['close'].rolling(window=period).std().iloc[-1]
        
        if std_price == 0:
            return 0.0
        
        return (current_price - mean_price) / std_price
    
    def _calculate_rsi(self, data: pd.DataFrame, period: int) -> float:
        """Calculate RSI"""
        if len(data) < period + 1:
            return 50.0
        
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50.0
    
    async def adapt_parameters(self, performance_feedback: Dict[str, float]) -> bool:
        """Adapt mean reversion strategy parameters"""
        try:
            # Adjust Z-score thresholds based on performance
            if performance_feedback.get('win_rate', 0.5) < 0.4:
                # More aggressive entry (lower Z-score threshold)
                self.config.parameters['z_score_threshold'] = max(1.5, self.config.parameters.get('z_score_threshold', 2.0) - 0.5)
            elif performance_feedback.get('win_rate', 0.5) > 0.7:
                # More conservative entry (higher Z-score threshold)
                self.config.parameters['z_score_threshold'] = min(3.0, self.config.parameters.get('z_score_threshold', 2.0) + 0.5)
            
            # Adjust Bollinger Band period based on volatility
            if performance_feedback.get('volatility', 0.1) > 0.15:
                # Shorter period for high volatility
                self.config.parameters['bb_period'] = max(10, self.config.parameters.get('bb_period', 20) - 5)
            else:
                # Longer period for low volatility
                self.config.parameters['bb_period'] = min(30, self.config.parameters.get('bb_period', 20) + 5)
            
            self.adaptation_history.append({
                'timestamp': datetime.now(),
                'performance_feedback': performance_feedback,
                'new_parameters': self.config.parameters.copy()
            })
            
            logger.info("Mean reversion strategy parameters adapted")
            return True
            
        except Exception as e:
            logger.error(f"Error adapting mean reversion strategy: {e}")
            return False

class MultiStrategyManager:
    """Multi-strategy trading system manager"""
    
    def __init__(self):
        self.strategies = {}
        self.regime_detector = MarketRegimeDetector()
        self.portfolio_manager = None
        self.risk_manager = None
        self.performance_tracker = {}
        self.signal_history = []
        
    async def add_strategy(self, strategy: AdaptiveStrategy) -> str:
        """Add strategy to the system"""
        strategy_id = strategy.config.config_id
        self.strategies[strategy_id] = strategy
        self.performance_tracker[strategy_id] = []
        
        logger.info(f"Added strategy: {strategy.config.name}")
        return strategy_id
    
    async def remove_strategy(self, strategy_id: str) -> bool:
        """Remove strategy from the system"""
        if strategy_id in self.strategies:
            del self.strategies[strategy_id]
            if strategy_id in self.performance_tracker:
                del self.performance_tracker[strategy_id]
            logger.info(f"Removed strategy: {strategy_id}")
            return True
        return False
    
    async def run_strategies(self, data: pd.DataFrame, portfolio_value: float) -> List[TradingSignal]:
        """Run all strategies and generate signals"""
        # Detect market regime
        market_regime = await self.regime_detector.detect_regime(data)
        
        all_signals = []
        
        for strategy_id, strategy in self.strategies.items():
            if strategy.status != StrategyStatus.ACTIVE:
                continue
            
            try:
                # Generate signal
                signal = await strategy.generate_signal(data, market_regime)
                
                if signal:
                    # Calculate position size
                    signal.quantity = await strategy.calculate_position_size(signal, portfolio_value)
                    
                    # Add to signal history
                    self.signal_history.append(signal)
                    all_signals.append(signal)
                    
                    logger.info(f"Strategy {strategy.config.name} generated {signal.signal_type.value} signal")
                
            except Exception as e:
                logger.error(f"Error running strategy {strategy_id}: {e}")
                strategy.status = StrategyStatus.ERROR
        
        return all_signals
    
    async def adapt_strategies(self, performance_data: Dict[str, Dict[str, float]]) -> None:
        """Adapt all strategies based on performance"""
        for strategy_id, strategy in self.strategies.items():
            if strategy_id in performance_data:
                try:
                    await strategy.adapt_parameters(performance_data[strategy_id])
                except Exception as e:
                    logger.error(f"Error adapting strategy {strategy_id}: {e}")
    
    async def get_strategy_performance(self, strategy_id: str) -> Optional[StrategyPerformance]:
        """Get strategy performance metrics"""
        if strategy_id not in self.strategies:
            return None
        
        strategy = self.strategies[strategy_id]
        performance_summary = strategy.get_performance_summary()
        
        if not performance_summary:
            return None
        
        # Calculate additional metrics
        returns = [entry['trade_result'].get('return', 0) for entry in strategy.performance_history]
        
        if not returns:
            return None
        
        # Calculate Sharpe ratio
        risk_free_rate = 0.02  # 2% annual
        excess_returns = [r - risk_free_rate/252 for r in returns]  # Daily risk-free rate
        sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) if np.std(excess_returns) > 0 else 0
        
        # Calculate maximum drawdown
        cumulative_returns = np.cumprod([1 + r for r in returns])
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdowns = (cumulative_returns - running_max) / running_max
        max_drawdown = np.min(drawdowns)
        
        # Calculate other metrics
        winning_trades = [r for r in returns if r > 0]
        losing_trades = [r for r in returns if r < 0]
        
        win_rate = len(winning_trades) / len(returns) if returns else 0
        avg_win = np.mean(winning_trades) if winning_trades else 0
        avg_loss = np.mean(losing_trades) if losing_trades else 0
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        
        return StrategyPerformance(
            strategy_id=strategy_id,
            total_return=performance_summary['total_return'],
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            profit_factor=profit_factor,
            calmar_ratio=performance_summary['total_return'] / abs(max_drawdown) if max_drawdown != 0 else 0,
            sortino_ratio=0,  # Would need downside deviation calculation
            total_trades=len(returns),
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            avg_win=avg_win,
            avg_loss=avg_loss,
            largest_win=max(winning_trades) if winning_trades else 0,
            largest_loss=min(losing_trades) if losing_trades else 0,
            volatility=performance_summary['volatility'],
            beta=0,  # Would need benchmark comparison
            alpha=0,  # Would need benchmark comparison
            information_ratio=0,  # Would need benchmark comparison
            tracking_error=0,  # Would need benchmark comparison
            period="custom",
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now()
        )
    
    async def get_portfolio_performance(self) -> Dict[str, Any]:
        """Get overall portfolio performance"""
        total_return = 0
        total_trades = 0
        strategy_returns = {}
        
        for strategy_id, strategy in self.strategies.items():
            performance = await self.get_strategy_performance(strategy_id)
            if performance:
                strategy_returns[strategy_id] = performance.total_return
                total_return += performance.total_return
                total_trades += performance.total_trades
        
        # Calculate portfolio metrics
        portfolio_metrics = {
            'total_return': total_return,
            'total_trades': total_trades,
            'strategy_count': len(self.strategies),
            'active_strategies': len([s for s in self.strategies.values() if s.status == StrategyStatus.ACTIVE]),
            'strategy_returns': strategy_returns,
            'current_regime': self.regime_detector.current_regime.value,
            'regime_history_length': len(self.regime_detector.regime_history)
        }
        
        return portfolio_metrics
    
    def get_summary(self) -> Dict[str, Any]:
        """Get system summary"""
        return {
            'total_strategies': len(self.strategies),
            'active_strategies': len([s for s in self.strategies.values() if s.status == StrategyStatus.ACTIVE]),
            'total_signals': len(self.signal_history),
            'current_regime': self.regime_detector.current_regime.value,
            'regime_history': len(self.regime_detector.regime_history),
            'last_update': datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of MultiStrategyManager"""
    manager = MultiStrategyManager()
    
    # Create strategy configurations
    momentum_config = StrategyConfig(
        config_id=str(uuid.uuid4()),
        strategy_type=StrategyType.MOMENTUM,
        name="Momentum Strategy",
        description="Momentum-based trading strategy",
        parameters={'rsi_oversold': 30, 'rsi_overbought': 70, 'momentum_threshold': 0.02},
        risk_limits={'risk_per_trade': 0.02, 'stop_loss': 0.05, 'max_position': 0.2},
        position_sizing={'method': 'kelly', 'max_kelly': 0.25},
        entry_conditions=[{'type': 'rsi', 'condition': 'oversold'}],
        exit_conditions=[{'type': 'rsi', 'condition': 'overbought'}],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    mean_reversion_config = StrategyConfig(
        config_id=str(uuid.uuid4()),
        strategy_type=StrategyType.MEAN_REVERSION,
        name="Mean Reversion Strategy",
        description="Mean reversion trading strategy",
        parameters={'z_score_threshold': 2.0, 'bb_period': 20, 'bb_std': 2.0},
        risk_limits={'risk_per_trade': 0.015, 'stop_loss': 0.03, 'max_position': 0.15},
        position_sizing={'method': 'fixed', 'position_size': 0.1},
        entry_conditions=[{'type': 'bollinger_bands', 'condition': 'below_lower'}],
        exit_conditions=[{'type': 'bollinger_bands', 'condition': 'above_upper'}],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Create strategies
    momentum_strategy = MomentumStrategy(momentum_config)
    mean_reversion_strategy = MeanReversionStrategy(mean_reversion_config)
    
    # Add strategies to manager
    momentum_id = await manager.add_strategy(momentum_strategy)
    mean_reversion_id = await manager.add_strategy(mean_reversion_strategy)
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='H')
    np.random.seed(42)
    
    data = pd.DataFrame({
        'open': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1),
        'high': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1) + np.random.uniform(0, 2, len(dates)),
        'low': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1) - np.random.uniform(0, 2, len(dates)),
        'close': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1),
        'volume': np.random.uniform(1000, 10000, len(dates))
    }, index=dates)
    
    # Run strategies
    signals = await manager.run_strategies(data, 10000)
    print(f"Generated {len(signals)} signals")
    
    # Get performance
    momentum_performance = await manager.get_strategy_performance(momentum_id)
    mean_reversion_performance = await manager.get_strategy_performance(mean_reversion_id)
    
    if momentum_performance:
        print(f"Momentum strategy: {momentum_performance.total_return:.4f} return, {momentum_performance.win_rate:.2f} win rate")
    
    if mean_reversion_performance:
        print(f"Mean reversion strategy: {mean_reversion_performance.total_return:.4f} return, {mean_reversion_performance.win_rate:.2f} win rate")
    
    # Portfolio performance
    portfolio_performance = await manager.get_portfolio_performance()
    print(f"Portfolio performance: {portfolio_performance}")
    
    # System summary
    summary = manager.get_summary()
    print(f"System summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())
