"""
Insight Generator

Generates actionable insights from analytics results.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
import numpy as np

from ..models.analytics_models import (
    MarketData, PredictionResult, AnalyticsInsight, 
    MarketRegime, TrendAnalysis, VolatilityMetrics
)

logger = logging.getLogger(__name__)


class InsightGenerator:
    """
    Generates actionable insights from analytics data.
    """
    
    def __init__(self):
        """Initialize insight generator."""
        self._insight_rules = self._setup_insight_rules()
        self._thresholds = self._setup_thresholds()
    
    def _setup_insight_rules(self) -> Dict[str, Any]:
        """Setup insight generation rules."""
        return {
            'trend_analysis': {
                'min_periods': 5,
                'trend_threshold': 0.02,
                'strong_trend_threshold': 0.05
            },
            'volatility_analysis': {
                'low_volatility_threshold': 0.1,
                'high_volatility_threshold': 0.3,
                'extreme_volatility_threshold': 0.5
            },
            'momentum_analysis': {
                'oversold_threshold': 30,
                'overbought_threshold': 70,
                'strong_momentum_threshold': 0.1
            },
            'support_resistance': {
                'touch_tolerance': 0.02,
                'min_touches': 2,
                'lookback_period': 50
            }
        }
    
    def _setup_thresholds(self) -> Dict[str, float]:
        """Setup insight confidence thresholds."""
        return {
            'high_confidence': 0.8,
            'medium_confidence': 0.6,
            'low_confidence': 0.4,
            'min_confidence': 0.3
        }
    
    async def initialize(self):
        """Initialize insight generator."""
        try:
            logger.info("Insight generator initialized")
        except Exception as e:
            logger.error(f"Failed to initialize insight generator: {e}")
            raise
    
    async def generate_insights(
        self,
        symbol: str,
        market_data: List[MarketData],
        predictions: List[PredictionResult] = None
    ) -> List[AnalyticsInsight]:
        """
        Generate comprehensive insights for a symbol.
        
        Args:
            symbol: Asset symbol
            market_data: Market data for analysis
            predictions: Model predictions
            
        Returns:
            List of generated insights
        """
        try:
            insights = []
            
            if not market_data:
                return insights
            
            # Generate trend insights
            trend_insights = await self._generate_trend_insights(symbol, market_data)
            insights.extend(trend_insights)
            
            # Generate volatility insights
            volatility_insights = await self._generate_volatility_insights(symbol, market_data)
            insights.extend(volatility_insights)
            
            # Generate momentum insights
            momentum_insights = await self._generate_momentum_insights(symbol, market_data)
            insights.extend(momentum_insights)
            
            # Generate support/resistance insights
            sr_insights = await self._generate_support_resistance_insights(symbol, market_data)
            insights.extend(sr_insights)
            
            # Generate prediction-based insights
            if predictions:
                prediction_insights = await self._generate_prediction_insights(symbol, predictions)
                insights.extend(prediction_insights)
            
            # Generate market regime insights
            regime_insights = await self._generate_regime_insights(symbol, market_data)
            insights.extend(regime_insights)
            
            # Filter insights by confidence
            filtered_insights = [insight for insight in insights 
                               if insight.confidence >= self._thresholds['min_confidence']]
            
            logger.info(f"Generated {len(filtered_insights)} insights for {symbol}")
            return filtered_insights
            
        except Exception as e:
            logger.error(f"Failed to generate insights for {symbol}: {e}")
            raise
    
    async def _generate_trend_insights(
        self, 
        symbol: str, 
        market_data: List[MarketData]
    ) -> List[AnalyticsInsight]:
        """Generate trend analysis insights."""
        insights = []
        
        try:
            if len(market_data) < 10:
                return insights
            
            # Calculate trend metrics
            prices = [float(item.close_price) for item in market_data[-20:]]
            trend_direction, trend_strength = self._analyze_trend(prices)
            
            # Generate trend insight
            if abs(trend_strength) > self._insight_rules['trend_analysis']['trend_threshold']:
                confidence = min(abs(trend_strength) * 2, 1.0)
                impact = 'high' if abs(trend_strength) > self._insight_rules['trend_analysis']['strong_trend_threshold'] else 'medium'
                
                insight = AnalyticsInsight(
                    insight_type='trend_analysis',
                    title=f"{symbol} Trend Analysis",
                    description=f"Strong {trend_direction} trend detected with {trend_strength:.2%} strength",
                    confidence=Decimal(str(confidence)),
                    impact=impact,
                    timeframe='short_term',
                    symbols=[symbol],
                    generated_at=datetime.now(),
                    source_data=['price_data', 'technical_analysis'],
                    recommendations=self._get_trend_recommendations(trend_direction, trend_strength)
                )
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate trend insights: {e}")
            return insights
    
    async def _generate_volatility_insights(
        self, 
        symbol: str, 
        market_data: List[MarketData]
    ) -> List[AnalyticsInsight]:
        """Generate volatility analysis insights."""
        insights = []
        
        try:
            if len(market_data) < 20:
                return insights
            
            # Calculate volatility metrics
            returns = self._calculate_returns(market_data)
            current_volatility = np.std(returns[-20:]) * np.sqrt(252)  # Annualized
            historical_volatility = np.std(returns) * np.sqrt(252)
            
            volatility_ratio = current_volatility / historical_volatility
            
            # Generate volatility insight
            if volatility_ratio > 1.5:  # High volatility
                confidence = min(volatility_ratio / 2, 1.0)
                insight = AnalyticsInsight(
                    insight_type='volatility_analysis',
                    title=f"{symbol} High Volatility Alert",
                    description=f"Current volatility ({current_volatility:.2%}) is {volatility_ratio:.1f}x higher than historical average",
                    confidence=Decimal(str(confidence)),
                    impact='high',
                    timeframe='short_term',
                    symbols=[symbol],
                    generated_at=datetime.now(),
                    source_data=['price_data', 'volatility_analysis'],
                    recommendations=[
                        "Consider reducing position size",
                        "Implement tighter stop-losses",
                        "Monitor for potential breakout opportunities"
                    ]
                )
                insights.append(insight)
            
            elif volatility_ratio < 0.5:  # Low volatility
                confidence = min((1 - volatility_ratio) * 2, 1.0)
                insight = AnalyticsInsight(
                    insight_type='volatility_analysis',
                    title=f"{symbol} Low Volatility Period",
                    description=f"Current volatility ({current_volatility:.2%}) is significantly below historical average",
                    confidence=Decimal(str(confidence)),
                    impact='medium',
                    timeframe='medium_term',
                    symbols=[symbol],
                    generated_at=datetime.now(),
                    source_data=['price_data', 'volatility_analysis'],
                    recommendations=[
                        "Consider volatility expansion strategies",
                        "Prepare for potential breakout",
                        "Monitor for trend continuation signals"
                    ]
                )
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate volatility insights: {e}")
            return insights
    
    async def _generate_momentum_insights(
        self, 
        symbol: str, 
        market_data: List[MarketData]
    ) -> List[AnalyticsInsight]:
        """Generate momentum analysis insights."""
        insights = []
        
        try:
            if len(market_data) < 14:
                return insights
            
            # Calculate momentum indicators
            prices = [float(item.close_price) for item in market_data]
            rsi = self._calculate_rsi(prices, 14)
            momentum = self._calculate_momentum(prices, 10)
            
            # Generate momentum insights
            if rsi < self._insight_rules['momentum_analysis']['oversold_threshold']:
                confidence = (self._insight_rules['momentum_analysis']['oversold_threshold'] - rsi) / 30
                insight = AnalyticsInsight(
                    insight_type='momentum_analysis',
                    title=f"{symbol} Oversold Condition",
                    description=f"RSI at {rsi:.1f} indicates oversold conditions",
                    confidence=Decimal(str(confidence)),
                    impact='medium',
                    timeframe='short_term',
                    symbols=[symbol],
                    generated_at=datetime.now(),
                    source_data=['price_data', 'momentum_indicators'],
                    recommendations=[
                        "Consider potential buying opportunity",
                        "Look for bullish reversal signals",
                        "Set appropriate stop-loss levels"
                    ]
                )
                insights.append(insight)
            
            elif rsi > self._insight_rules['momentum_analysis']['overbought_threshold']:
                confidence = (rsi - self._insight_rules['momentum_analysis']['overbought_threshold']) / 30
                insight = AnalyticsInsight(
                    insight_type='momentum_analysis',
                    title=f"{symbol} Overbought Condition",
                    description=f"RSI at {rsi:.1f} indicates overbought conditions",
                    confidence=Decimal(str(confidence)),
                    impact='medium',
                    timeframe='short_term',
                    symbols=[symbol],
                    generated_at=datetime.now(),
                    source_data=['price_data', 'momentum_indicators'],
                    recommendations=[
                        "Consider taking profits",
                        "Look for bearish reversal signals",
                        "Implement risk management strategies"
                    ]
                )
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate momentum insights: {e}")
            return insights
    
    async def _generate_support_resistance_insights(
        self, 
        symbol: str, 
        market_data: List[MarketData]
    ) -> List[AnalyticsInsight]:
        """Generate support/resistance insights."""
        insights = []
        
        try:
            if len(market_data) < 50:
                return insights
            
            # Find support and resistance levels
            prices = [float(item.close_price) for item in market_data]
            support_levels, resistance_levels = self._find_support_resistance(prices)
            
            current_price = prices[-1]
            
            # Check for support/resistance breaks
            for level in support_levels:
                if abs(current_price - level) / level < 0.01:  # Within 1%
                    insight = AnalyticsInsight(
                        insight_type='support_resistance',
                        title=f"{symbol} Support Level Test",
                        description=f"Price testing support at {level:.2f}",
                        confidence=Decimal('0.7'),
                        impact='medium',
                        timeframe='short_term',
                        symbols=[symbol],
                        generated_at=datetime.now(),
                        source_data=['price_data', 'support_resistance_analysis'],
                        recommendations=[
                            "Monitor for bounce or breakdown",
                            "Set stop-loss below support",
                            "Prepare for potential reversal"
                        ]
                    )
                    insights.append(insight)
            
            for level in resistance_levels:
                if abs(current_price - level) / level < 0.01:  # Within 1%
                    insight = AnalyticsInsight(
                        insight_type='support_resistance',
                        title=f"{symbol} Resistance Level Test",
                        description=f"Price testing resistance at {level:.2f}",
                        confidence=Decimal('0.7'),
                        impact='medium',
                        timeframe='short_term',
                        symbols=[symbol],
                        generated_at=datetime.now(),
                        source_data=['price_data', 'support_resistance_analysis'],
                        recommendations=[
                            "Monitor for breakout or rejection",
                            "Consider taking profits at resistance",
                            "Prepare for potential continuation"
                        ]
                    )
                    insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate support/resistance insights: {e}")
            return insights
    
    async def _generate_prediction_insights(
        self, 
        symbol: str, 
        predictions: List[PredictionResult]
    ) -> List[AnalyticsInsight]:
        """Generate insights based on model predictions."""
        insights = []
        
        try:
            for prediction in predictions:
                if prediction.confidence > self._thresholds['high_confidence']:
                    insight = AnalyticsInsight(
                        insight_type='model_prediction',
                        title=f"{symbol} High Confidence Prediction",
                        description=f"Model predicts {prediction.prediction_type} with {prediction.confidence:.1%} confidence",
                        confidence=prediction.confidence,
                        impact='high',
                        timeframe='short_term',
                        symbols=[symbol],
                        generated_at=datetime.now(),
                        source_data=['ml_models', 'prediction_analysis'],
                        recommendations=self._get_prediction_recommendations(prediction)
                    )
                    insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate prediction insights: {e}")
            return insights
    
    async def _generate_regime_insights(
        self, 
        symbol: str, 
        market_data: List[MarketData]
    ) -> List[AnalyticsInsight]:
        """Generate market regime insights."""
        insights = []
        
        try:
            if len(market_data) < 30:
                return insights
            
            # Analyze market regime
            regime = await self._analyze_market_regime(market_data)
            
            if regime['confidence'] > self._thresholds['medium_confidence']:
                insight = AnalyticsInsight(
                    insight_type='market_regime',
                    title=f"{symbol} Market Regime Analysis",
                    description=f"Market appears to be in {regime['regime']} regime with {regime['confidence']:.1%} confidence",
                    confidence=regime['confidence'],
                    impact='medium',
                    timeframe='medium_term',
                    symbols=[symbol],
                    generated_at=datetime.now(),
                    source_data=['price_data', 'regime_analysis'],
                    recommendations=self._get_regime_recommendations(regime['regime'])
                )
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate regime insights: {e}")
            return insights
    
    def _analyze_trend(self, prices: List[float]) -> Tuple[str, float]:
        """Analyze trend direction and strength."""
        if len(prices) < 5:
            return 'neutral', 0.0
        
        # Simple linear regression slope
        x = np.arange(len(prices))
        slope = np.polyfit(x, prices, 1)[0]
        trend_strength = slope / prices[0]  # Normalize by initial price
        
        if trend_strength > 0.02:
            return 'uptrend', trend_strength
        elif trend_strength < -0.02:
            return 'downtrend', abs(trend_strength)
        else:
            return 'sideways', 0.0
    
    def _calculate_returns(self, market_data: List[MarketData]) -> List[float]:
        """Calculate returns from market data."""
        prices = [float(item.close_price) for item in market_data]
        returns = []
        for i in range(1, len(prices)):
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
        return returns
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate RSI indicator."""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_momentum(self, prices: List[float], period: int = 10) -> float:
        """Calculate momentum indicator."""
        if len(prices) < period + 1:
            return 0.0
        
        return (prices[-1] - prices[-period-1]) / prices[-period-1]
    
    def _find_support_resistance(self, prices: List[float]) -> Tuple[List[float], List[float]]:
        """Find support and resistance levels."""
        # Simplified implementation
        # In practice, use more sophisticated algorithms
        support_levels = []
        resistance_levels = []
        
        # Find local minima and maxima
        for i in range(2, len(prices) - 2):
            if prices[i] < prices[i-1] and prices[i] < prices[i+1]:
                support_levels.append(prices[i])
            elif prices[i] > prices[i-1] and prices[i] > prices[i+1]:
                resistance_levels.append(prices[i])
        
        return support_levels, resistance_levels
    
    async def _analyze_market_regime(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Analyze current market regime."""
        # Simplified implementation
        returns = self._calculate_returns(market_data)
        volatility = np.std(returns) * np.sqrt(252)
        
        if volatility > 0.3:
            return {'regime': 'volatile', 'confidence': Decimal('0.8')}
        elif volatility < 0.1:
            return {'regime': 'calm', 'confidence': Decimal('0.7')}
        else:
            return {'regime': 'normal', 'confidence': Decimal('0.6')}
    
    def _get_trend_recommendations(self, trend_direction: str, trend_strength: float) -> List[str]:
        """Get recommendations based on trend analysis."""
        if trend_direction == 'uptrend':
            return [
                "Consider trend-following strategies",
                "Look for pullback entry opportunities",
                "Set trailing stop-losses"
            ]
        elif trend_direction == 'downtrend':
            return [
                "Consider short-selling opportunities",
                "Implement defensive strategies",
                "Reduce position sizes"
            ]
        else:
            return [
                "Consider range-bound strategies",
                "Look for breakout opportunities",
                "Implement mean reversion strategies"
            ]
    
    def _get_prediction_recommendations(self, prediction: PredictionResult) -> List[str]:
        """Get recommendations based on predictions."""
        if prediction.prediction_type == 'price':
            return [
                "Consider position sizing based on prediction confidence",
                "Implement risk management strategies",
                "Monitor for prediction accuracy"
            ]
        elif prediction.prediction_type == 'volatility':
            return [
                "Adjust position sizes based on volatility forecast",
                "Consider volatility-based strategies",
                "Implement appropriate risk controls"
            ]
        else:
            return [
                "Monitor prediction accuracy",
                "Consider prediction in overall strategy",
                "Implement appropriate risk management"
            ]
    
    def _get_regime_recommendations(self, regime: str) -> List[str]:
        """Get recommendations based on market regime."""
        if regime == 'volatile':
            return [
                "Implement strict risk management",
                "Consider volatility-based strategies",
                "Reduce position sizes"
            ]
        elif regime == 'calm':
            return [
                "Consider trend-following strategies",
                "Look for breakout opportunities",
                "Prepare for volatility expansion"
            ]
        else:
            return [
                "Maintain balanced approach",
                "Monitor for regime changes",
                "Implement diversified strategies"
            ]
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            logger.info("Insight generator cleanup completed")
        except Exception as e:
            logger.error(f"Error during insight generator cleanup: {e}")
