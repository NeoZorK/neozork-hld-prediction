"""Adaptive Strategy Manager - Dynamic strategy selection and market regime detection"""

import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid
import numpy as np

logger = logging.getLogger(__name__)


class MarketRegime(Enum):
    """Market regime enumeration."""
    TRENDING_UP = "trending_up"
    TRENDING_DOWN = "trending_down"
    SIDEWAYS = "sideways"
    HIGH_VOLATILITY = "high_volatility"
    LOW_VOLATILITY = "low_volatility"


class StrategyType(Enum):
    """Strategy type enumeration."""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    ARBITRAGE = "arbitrage"
    MARKET_MAKING = "market_making"
    TREND_FOLLOWING = "trend_following"


class SignalStrength(Enum):
    """Signal strength enumeration."""
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


@dataclass
class MarketRegimeData:
    """Market regime data class."""
    regime: MarketRegime
    confidence: float
    duration: int
    volatility: float
    trend_strength: float
    detected_at: datetime


@dataclass
class StrategySignal:
    """Strategy signal data class."""
    strategy_id: str
    strategy_type: StrategyType
    signal_type: str
    strength: SignalStrength
    confidence: float
    expected_return: float
    risk_score: float
    market_regime: MarketRegime
    generated_at: datetime
    metadata: Dict[str, Any]


class AdaptiveStrategyManager:
    """Dynamic strategy selection and market regime detection system."""
    
    def __init__(self):
        self.market_regimes: List[MarketRegimeData] = []
        self.strategy_signals: List[StrategySignal] = []
        self.strategy_performance: Dict[str, Dict[str, Any]] = {}
        
    async def detect_market_regime(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect current market regime."""
        try:
            # Extract features for regime detection
            features = await self._extract_regime_features(market_data)
            
            if 'error' in features:
                return features
            
            # Detect regime using simple rules
            regime_result = await self._detect_regime_simple(features)
            
            # Create regime data
            regime_data = MarketRegimeData(
                regime=regime_result['regime'],
                confidence=regime_result['confidence'],
                duration=regime_result['duration'],
                volatility=features['volatility'],
                trend_strength=features['trend_strength'],
                detected_at=datetime.now()
            )
            
            # Store regime data
            self.market_regimes.append(regime_data)
            
            # Keep only recent regimes (last 100)
            if len(self.market_regimes) > 100:
                self.market_regimes = self.market_regimes[-100:]
            
            logger.info(f"Detected market regime: {regime_data.regime.value} (confidence: {regime_data.confidence:.2f})")
            return {
                'status': 'success',
                'regime_data': regime_data.__dict__,
                'regime': regime_data.regime.value,
                'confidence': regime_data.confidence
            }
            
        except Exception as e:
            logger.error(f"Failed to detect market regime: {e}")
            return {'error': str(e)}
    
    async def select_optimal_strategy(self, market_regime: MarketRegime, 
                                    available_strategies: List[str]) -> Dict[str, Any]:
        """Select optimal strategy for current market regime."""
        try:
            # Get strategy performance history
            performance_data = await self._get_strategy_performance_data(available_strategies)
            
            # Select best strategy for regime
            selection_result = await self._select_strategy_simple(market_regime, performance_data)
            
            if 'error' in selection_result:
                return selection_result
            
            selected_strategy = selection_result['selected_strategy']
            confidence = selection_result['confidence']
            
            logger.info(f"Selected strategy: {selected_strategy} for regime {market_regime.value}")
            return {
                'status': 'success',
                'selected_strategy': selected_strategy,
                'confidence': confidence,
                'market_regime': market_regime.value,
                'selection_reason': selection_result.get('reason', 'Performance-based selection')
            }
            
        except Exception as e:
            logger.error(f"Failed to select optimal strategy: {e}")
            return {'error': str(e)}
    
    async def generate_trading_signals(self, strategy_id: str, market_data: Dict[str, Any],
                                     market_regime: MarketRegime) -> Dict[str, Any]:
        """Generate trading signals for selected strategy."""
        try:
            # Generate signals using strategy
            signal_result = await self._generate_signals_simple(strategy_id, market_data, market_regime)
            
            if 'error' in signal_result:
                return signal_result
            
            # Create strategy signal
            strategy_signal = StrategySignal(
                strategy_id=strategy_id,
                strategy_type=signal_result['strategy_type'],
                signal_type=signal_result['signal_type'],
                strength=signal_result['strength'],
                confidence=signal_result['confidence'],
                expected_return=signal_result['expected_return'],
                risk_score=signal_result['risk_score'],
                market_regime=market_regime,
                generated_at=datetime.now(),
                metadata=signal_result.get('metadata', {})
            )
            
            # Store signal
            self.strategy_signals.append(strategy_signal)
            
            # Keep only recent signals (last 1000)
            if len(self.strategy_signals) > 1000:
                self.strategy_signals = self.strategy_signals[-1000:]
            
            logger.info(f"Generated signal: {signal_result['signal_type']} for strategy {strategy_id}")
            return {
                'status': 'success',
                'signal': strategy_signal.__dict__,
                'signal_type': signal_result['signal_type'],
                'strength': signal_result['strength'].value,
                'confidence': signal_result['confidence']
            }
            
        except Exception as e:
            logger.error(f"Failed to generate trading signals: {e}")
            return {'error': str(e)}
    
    async def adapt_strategy_parameters(self, strategy_id: str, 
                                      performance_feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt strategy parameters based on performance feedback."""
        try:
            # Analyze performance feedback
            adaptation_result = await self._analyze_performance_feedback(strategy_id, performance_feedback)
            
            if 'error' in adaptation_result:
                return adaptation_result
            
            # Update strategy parameters
            updated_parameters = adaptation_result['updated_parameters']
            
            # Store updated parameters
            if strategy_id not in self.strategy_performance:
                self.strategy_performance[strategy_id] = {}
            
            self.strategy_performance[strategy_id]['parameters'] = updated_parameters
            self.strategy_performance[strategy_id]['last_updated'] = datetime.now()
            
            logger.info(f"Adapted parameters for strategy {strategy_id}")
            return {
                'status': 'success',
                'strategy_id': strategy_id,
                'updated_parameters': updated_parameters,
                'adaptation_reason': adaptation_result.get('reason', 'Performance optimization')
            }
            
        except Exception as e:
            logger.error(f"Failed to adapt strategy parameters: {e}")
            return {'error': str(e)}
    
    async def _extract_regime_features(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features for market regime detection."""
        try:
            # Calculate technical indicators
            prices = market_data.get('prices', [])
            volumes = market_data.get('volumes', [])
            
            if len(prices) < 20:
                return {'error': 'Insufficient data for regime detection'}
            
            # Calculate volatility
            returns = np.diff(prices) / prices[:-1]
            volatility = np.std(returns) * np.sqrt(252)  # Annualized
            
            # Calculate trend strength
            sma_20 = np.mean(prices[-20:])
            sma_50 = np.mean(prices[-50:]) if len(prices) >= 50 else sma_20
            trend_strength = (sma_20 - sma_50) / sma_50
            
            # Calculate volume profile
            avg_volume = np.mean(volumes[-20:]) if volumes else 1.0
            volume_profile = {
                'current_volume': volumes[-1] if volumes else 1.0,
                'avg_volume': avg_volume,
                'volume_ratio': (volumes[-1] / avg_volume) if volumes else 1.0
            }
            
            return {
                'volatility': volatility,
                'trend_strength': trend_strength,
                'volume_profile': volume_profile,
                'price_momentum': (prices[-1] - prices[-5]) / prices[-5] if len(prices) >= 5 else 0,
                'rsi': self._calculate_rsi(prices),
                'bollinger_position': self._calculate_bollinger_position(prices)
            }
            
        except Exception as e:
            logger.error(f"Failed to extract regime features: {e}")
            return {'error': str(e)}
    
    async def _detect_regime_simple(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Simple rule-based regime detection."""
        try:
            volatility = features.get('volatility', 0.2)
            trend_strength = features.get('trend_strength', 0.0)
            
            if volatility > 0.3:
                regime = MarketRegime.HIGH_VOLATILITY
                confidence = 0.8
            elif trend_strength > 0.1:
                regime = MarketRegime.TRENDING_UP
                confidence = 0.7
            elif trend_strength < -0.1:
                regime = MarketRegime.TRENDING_DOWN
                confidence = 0.7
            else:
                regime = MarketRegime.SIDEWAYS
                confidence = 0.6
            
            return {
                'regime': regime,
                'confidence': confidence,
                'duration': 1
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _get_strategy_performance_data(self, available_strategies: List[str]) -> Dict[str, Any]:
        """Get performance data for available strategies."""
        try:
            performance_data = {}
            
            for strategy_id in available_strategies:
                if strategy_id in self.strategy_performance:
                    performance_data[strategy_id] = self.strategy_performance[strategy_id]
                else:
                    # Initialize with default performance
                    performance_data[strategy_id] = {
                        'total_return': 0.0,
                        'sharpe_ratio': 0.0,
                        'max_drawdown': 0.0,
                        'win_rate': 0.5,
                        'regime_performance': {}
                    }
            
            return performance_data
            
        except Exception as e:
            logger.error(f"Failed to get strategy performance data: {e}")
            return {'error': str(e)}
    
    async def _select_strategy_simple(self, market_regime: MarketRegime, 
                                    performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simple strategy selection logic."""
        try:
            regime_strategies = {
                MarketRegime.TRENDING_UP: 'momentum_strategy',
                MarketRegime.TRENDING_DOWN: 'short_momentum',
                MarketRegime.SIDEWAYS: 'mean_reversion',
                MarketRegime.HIGH_VOLATILITY: 'volatility_strategy'
            }
            
            selected_strategy = regime_strategies.get(market_regime, 'mean_reversion')
            
            return {
                'selected_strategy': selected_strategy,
                'confidence': 0.7,
                'reason': f'Selected for {market_regime.value} regime'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _generate_signals_simple(self, strategy_id: str, market_data: Dict[str, Any],
                                     market_regime: MarketRegime) -> Dict[str, Any]:
        """Simple signal generation logic."""
        try:
            # TODO: Implement actual signal generation
            return {
                'strategy_type': StrategyType.MOMENTUM,
                'signal_type': 'buy',
                'strength': SignalStrength.MODERATE,
                'confidence': 0.6,
                'expected_return': 0.02,
                'risk_score': 0.3,
                'metadata': {'strategy_id': strategy_id}
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _analyze_performance_feedback(self, strategy_id: str, 
                                          performance_feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance feedback and determine parameter adjustments."""
        try:
            current_params = self.strategy_performance.get(strategy_id, {}).get('parameters', {})
            
            # Simple parameter adjustment based on performance
            if performance_feedback.get('total_return', 0) < 0:
                # Reduce risk parameters if performance is poor
                updated_params = {
                    'risk_multiplier': current_params.get('risk_multiplier', 1.0) * 0.9,
                    'position_size': current_params.get('position_size', 1.0) * 0.8
                }
            else:
                # Increase risk parameters if performance is good
                updated_params = {
                    'risk_multiplier': current_params.get('risk_multiplier', 1.0) * 1.1,
                    'position_size': current_params.get('position_size', 1.0) * 1.05
                }
            
            return {
                'updated_parameters': updated_params,
                'reason': 'Performance-based parameter adjustment'
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze performance feedback: {e}")
            return {'error': str(e)}
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate RSI indicator."""
        try:
            if len(prices) < period + 1:
                return 50.0  # Neutral RSI
            
            deltas = np.diff(prices)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            avg_gain = np.mean(gains[-period:])
            avg_loss = np.mean(losses[-period:])
            
            if avg_loss == 0:
                return 100.0
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
            
        except Exception:
            return 50.0
    
    def _calculate_bollinger_position(self, prices: List[float], period: int = 20) -> float:
        """Calculate Bollinger Bands position."""
        try:
            if len(prices) < period:
                return 0.5  # Middle position
            
            sma = np.mean(prices[-period:])
            std = np.std(prices[-period:])
            
            upper_band = sma + (2 * std)
            lower_band = sma - (2 * std)
            
            current_price = prices[-1]
            
            if upper_band == lower_band:
                return 0.5
            
            position = (current_price - lower_band) / (upper_band - lower_band)
            return max(0, min(1, position))
            
        except Exception:
            return 0.5
    
    def get_adaptive_strategy_summary(self) -> Dict[str, Any]:
        """Get adaptive strategy manager summary."""
        return {
            'total_regimes_detected': len(self.market_regimes),
            'total_signals_generated': len(self.strategy_signals),
            'strategies_tracked': len(self.strategy_performance),
            'current_regime': self.market_regimes[-1].regime.value if self.market_regimes else None,
            'last_signal_time': self.strategy_signals[-1].generated_at if self.strategy_signals else None
        }