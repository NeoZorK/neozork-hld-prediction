"""
Market Insights

Generates market-specific insights and analysis.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
import numpy as np

from ..models.analytics_models import (
    MarketData, AnalyticsInsight, MarketRegime, 
    VolatilityMetrics, TrendAnalysis
)

logger = logging.getLogger(__name__)


class MarketInsights:
    """
    Generates market-specific insights and analysis.
    """
    
    def __init__(self):
        """Initialize market insights generator."""
        self.insight_thresholds = self._setup_insight_thresholds()
        self.market_indicators = {}
    
    def _setup_insight_thresholds(self) -> Dict[str, Any]:
        """Setup thresholds for market insights."""
        return {
            'volatility': {
                'low': 0.1,
                'medium': 0.2,
                'high': 0.3,
                'extreme': 0.5
            },
            'trend': {
                'weak': 0.02,
                'moderate': 0.05,
                'strong': 0.1
            },
            'volume': {
                'low': 0.5,
                'normal': 1.0,
                'high': 2.0,
                'extreme': 5.0
            },
            'correlation': {
                'low': 0.3,
                'medium': 0.6,
                'high': 0.8
            }
        }
    
    async def generate_market_insights(
        self,
        symbol: str,
        market_data: List[MarketData],
        additional_data: Optional[Dict[str, Any]] = None
    ) -> List[AnalyticsInsight]:
        """
        Generate comprehensive market insights.
        
        Args:
            symbol: Asset symbol
            market_data: Market data
            additional_data: Additional market data
            
        Returns:
            List of market insights
        """
        try:
            insights = []
            
            if not market_data:
                return insights
            
            # Generate volatility insights
            volatility_insights = await self._generate_volatility_insights(symbol, market_data)
            insights.extend(volatility_insights)
            
            # Generate trend insights
            trend_insights = await self._generate_trend_insights(symbol, market_data)
            insights.extend(trend_insights)
            
            # Generate volume insights
            volume_insights = await self._generate_volume_insights(symbol, market_data)
            insights.extend(volume_insights)
            
            # Generate market regime insights
            regime_insights = await self._generate_regime_insights(symbol, market_data)
            insights.extend(regime_insights)
            
            # Generate support/resistance insights
            sr_insights = await self._generate_support_resistance_insights(symbol, market_data)
            insights.extend(sr_insights)
            
            # Generate market structure insights
            structure_insights = await self._generate_market_structure_insights(symbol, market_data)
            insights.extend(structure_insights)
            
            # Filter insights by confidence
            filtered_insights = [insight for insight in insights 
                               if insight.confidence >= Decimal('0.3')]
            
            logger.info(f"Generated {len(filtered_insights)} market insights for {symbol}")
            return filtered_insights
            
        except Exception as e:
            logger.error(f"Failed to generate market insights for {symbol}: {e}")
            raise
    
    async def _generate_volatility_insights(
        self, 
        symbol: str, 
        market_data: List[MarketData]
    ) -> List[AnalyticsInsight]:
        """Generate volatility-based insights."""
        insights = []
        
        try:
            if len(market_data) < 20:
                return insights
            
            # Calculate volatility metrics
            returns = self._calculate_returns(market_data)
            current_volatility = np.std(returns[-20:]) * np.sqrt(252)  # Annualized
            historical_volatility = np.std(returns) * np.sqrt(252)
            
            volatility_ratio = current_volatility / historical_volatility if historical_volatility > 0 else 1.0
            
            # Generate volatility insights
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
                        "Monitor for potential breakout opportunities",
                        "Use volatility-based position sizing"
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
                        "Monitor for trend continuation signals",
                        "Consider options strategies for low volatility"
                    ]
                )
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate volatility insights: {e}")
            return insights
    
    async def _generate_trend_insights(
        self, 
        symbol: str, 
        market_data: List[MarketData]
    ) -> List[AnalyticsInsight]:
        """Generate trend-based insights."""
        insights = []
        
        try:
            if len(market_data) < 10:
                return insights
            
            # Analyze trend
            trend_analysis = await self._analyze_trend(market_data)
            
            if trend_analysis['strength'] > self.insight_thresholds['trend']['moderate']:
                confidence = min(trend_analysis['strength'] * 10, 1.0)
                impact = 'high' if trend_analysis['strength'] > self.insight_thresholds['trend']['strong'] else 'medium'
                
                insight = AnalyticsInsight(
                    insight_type='trend_analysis',
                    title=f"{symbol} Strong {trend_analysis['direction'].title()} Trend",
                    description=f"Strong {trend_analysis['direction']} trend detected with {trend_analysis['strength']:.2%} strength over {trend_analysis['duration']} periods",
                    confidence=Decimal(str(confidence)),
                    impact=impact,
                    timeframe='medium_term',
                    symbols=[symbol],
                    generated_at=datetime.now(),
                    source_data=['price_data', 'trend_analysis'],
                    recommendations=self._get_trend_recommendations(trend_analysis)
                )
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate trend insights: {e}")
            return insights
    
    async def _generate_volume_insights(
        self, 
        symbol: str, 
        market_data: List[MarketData]
    ) -> List[AnalyticsInsight]:
        """Generate volume-based insights."""
        insights = []
        
        try:
            if len(market_data) < 20:
                return insights
            
            # Calculate volume metrics
            volumes = [float(data.volume) for data in market_data]
            current_volume = volumes[-1]
            avg_volume = np.mean(volumes[-20:])
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
            
            # Generate volume insights
            if volume_ratio > self.insight_thresholds['volume']['high']:
                confidence = min(volume_ratio / 3, 1.0)
                insight = AnalyticsInsight(
                    insight_type='volume_analysis',
                    title=f"{symbol} High Volume Activity",
                    description=f"Current volume ({current_volume:,.0f}) is {volume_ratio:.1f}x higher than 20-day average",
                    confidence=Decimal(str(confidence)),
                    impact='medium',
                    timeframe='short_term',
                    symbols=[symbol],
                    generated_at=datetime.now(),
                    source_data=['volume_data', 'volume_analysis'],
                    recommendations=[
                        "Monitor for potential price movement",
                        "Look for news or events driving volume",
                        "Consider volume-based entry/exit strategies",
                        "Watch for volume confirmation of price moves"
                    ]
                )
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate volume insights: {e}")
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
            regime_analysis = await self._analyze_market_regime(market_data)
            
            if regime_analysis['confidence'] > 0.6:
                insight = AnalyticsInsight(
                    insight_type='market_regime',
                    title=f"{symbol} Market Regime: {regime_analysis['regime'].title()}",
                    description=f"Market appears to be in {regime_analysis['regime']} regime with {regime_analysis['confidence']:.1%} confidence",
                    confidence=regime_analysis['confidence'],
                    impact='medium',
                    timeframe='medium_term',
                    symbols=[symbol],
                    generated_at=datetime.now(),
                    source_data=['price_data', 'regime_analysis'],
                    recommendations=self._get_regime_recommendations(regime_analysis['regime'])
                )
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate regime insights: {e}")
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
            prices = [float(data.close_price) for data in market_data]
            support_levels, resistance_levels = self._find_support_resistance(prices)
            
            current_price = prices[-1]
            
            # Check for support/resistance tests
            for level in support_levels:
                if abs(current_price - level) / level < 0.02:  # Within 2%
                    insight = AnalyticsInsight(
                        insight_type='support_resistance',
                        title=f"{symbol} Testing Support Level",
                        description=f"Price testing key support at {level:.2f}",
                        confidence=Decimal('0.7'),
                        impact='medium',
                        timeframe='short_term',
                        symbols=[symbol],
                        generated_at=datetime.now(),
                        source_data=['price_data', 'support_resistance_analysis'],
                        recommendations=[
                            "Monitor for bounce or breakdown",
                            "Set stop-loss below support",
                            "Prepare for potential reversal",
                            "Look for volume confirmation"
                        ]
                    )
                    insights.append(insight)
            
            for level in resistance_levels:
                if abs(current_price - level) / level < 0.02:  # Within 2%
                    insight = AnalyticsInsight(
                        insight_type='support_resistance',
                        title=f"{symbol} Testing Resistance Level",
                        description=f"Price testing key resistance at {level:.2f}",
                        confidence=Decimal('0.7'),
                        impact='medium',
                        timeframe='short_term',
                        symbols=[symbol],
                        generated_at=datetime.now(),
                        source_data=['price_data', 'support_resistance_analysis'],
                        recommendations=[
                            "Monitor for breakout or rejection",
                            "Consider taking profits at resistance",
                            "Prepare for potential continuation",
                            "Watch for volume confirmation"
                        ]
                    )
                    insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate support/resistance insights: {e}")
            return insights
    
    async def _generate_market_structure_insights(
        self, 
        symbol: str, 
        market_data: List[MarketData]
    ) -> List[AnalyticsInsight]:
        """Generate market structure insights."""
        insights = []
        
        try:
            if len(market_data) < 20:
                return insights
            
            # Analyze market structure
            structure_analysis = await self._analyze_market_structure(market_data)
            
            if structure_analysis['pattern'] != 'normal':
                insight = AnalyticsInsight(
                    insight_type='market_structure',
                    title=f"{symbol} Market Structure: {structure_analysis['pattern'].title()}",
                    description=f"Market showing {structure_analysis['pattern']} structure pattern",
                    confidence=Decimal(str(structure_analysis['confidence'])),
                    impact='medium',
                    timeframe='short_term',
                    symbols=[symbol],
                    generated_at=datetime.now(),
                    source_data=['price_data', 'market_structure_analysis'],
                    recommendations=self._get_structure_recommendations(structure_analysis['pattern'])
                )
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate market structure insights: {e}")
            return insights
    
    def _calculate_returns(self, market_data: List[MarketData]) -> List[float]:
        """Calculate returns from market data."""
        prices = [float(data.close_price) for data in market_data]
        returns = []
        for i in range(1, len(prices)):
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
        return returns
    
    async def _analyze_trend(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Analyze trend direction and strength."""
        try:
            prices = [float(data.close_price) for data in market_data]
            
            if len(prices) < 5:
                return {'direction': 'neutral', 'strength': 0.0, 'duration': 0}
            
            # Simple linear regression slope
            x = np.arange(len(prices))
            slope = np.polyfit(x, prices, 1)[0]
            trend_strength = abs(slope / prices[0])  # Normalize by initial price
            
            # Determine direction
            if slope > 0:
                direction = 'uptrend'
            elif slope < 0:
                direction = 'downtrend'
            else:
                direction = 'sideways'
            
            # Calculate duration
            duration = len(prices)
            
            return {
                'direction': direction,
                'strength': trend_strength,
                'duration': duration,
                'slope': slope
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze trend: {e}")
            return {'direction': 'neutral', 'strength': 0.0, 'duration': 0}
    
    async def _analyze_market_regime(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Analyze current market regime."""
        try:
            returns = self._calculate_returns(market_data)
            volatility = np.std(returns) * np.sqrt(252)
            
            # Determine regime based on volatility
            if volatility > self.insight_thresholds['volatility']['high']:
                regime = 'volatile'
                confidence = Decimal('0.8')
            elif volatility < self.insight_thresholds['volatility']['low']:
                regime = 'calm'
                confidence = Decimal('0.7')
            else:
                regime = 'normal'
                confidence = Decimal('0.6')
            
            return {
                'regime': regime,
                'confidence': confidence,
                'volatility': volatility
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze market regime: {e}")
            return {'regime': 'unknown', 'confidence': Decimal('0.0'), 'volatility': 0.0}
    
    def _find_support_resistance(self, prices: List[float]) -> Tuple[List[float], List[float]]:
        """Find support and resistance levels."""
        try:
            support_levels = []
            resistance_levels = []
            
            # Find local minima and maxima
            for i in range(2, len(prices) - 2):
                if prices[i] < prices[i-1] and prices[i] < prices[i+1]:
                    support_levels.append(prices[i])
                elif prices[i] > prices[i-1] and prices[i] > prices[i+1]:
                    resistance_levels.append(prices[i])
            
            # Remove duplicates and sort
            support_levels = sorted(list(set(support_levels)))
            resistance_levels = sorted(list(set(resistance_levels)))
            
            return support_levels, resistance_levels
            
        except Exception as e:
            logger.error(f"Failed to find support/resistance: {e}")
            return [], []
    
    async def _analyze_market_structure(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Analyze market structure patterns."""
        try:
            prices = [float(data.close_price) for data in market_data]
            highs = [float(data.high_price) for data in market_data]
            lows = [float(data.low_price) for data in market_data]
            
            # Analyze patterns
            pattern = 'normal'
            confidence = 0.5
            
            # Check for ascending/descending triangles
            if self._is_ascending_triangle(highs, lows):
                pattern = 'ascending_triangle'
                confidence = 0.7
            elif self._is_descending_triangle(highs, lows):
                pattern = 'descending_triangle'
                confidence = 0.7
            elif self._is_symmetrical_triangle(highs, lows):
                pattern = 'symmetrical_triangle'
                confidence = 0.6
            
            return {
                'pattern': pattern,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze market structure: {e}")
            return {'pattern': 'normal', 'confidence': 0.5}
    
    def _is_ascending_triangle(self, highs: List[float], lows: List[float]) -> bool:
        """Check for ascending triangle pattern."""
        if len(highs) < 10:
            return False
        
        # Simplified check - in practice, use more sophisticated algorithms
        recent_highs = highs[-5:]
        recent_lows = lows[-5:]
        
        # Check if highs are relatively flat and lows are rising
        high_variance = np.var(recent_highs)
        low_trend = np.polyfit(range(len(recent_lows)), recent_lows, 1)[0]
        
        return high_variance < 0.01 and low_trend > 0
    
    def _is_descending_triangle(self, highs: List[float], lows: List[float]) -> bool:
        """Check for descending triangle pattern."""
        if len(highs) < 10:
            return False
        
        recent_highs = highs[-5:]
        recent_lows = lows[-5:]
        
        # Check if lows are relatively flat and highs are falling
        low_variance = np.var(recent_lows)
        high_trend = np.polyfit(range(len(recent_highs)), recent_highs, 1)[0]
        
        return low_variance < 0.01 and high_trend < 0
    
    def _is_symmetrical_triangle(self, highs: List[float], lows: List[float]) -> bool:
        """Check for symmetrical triangle pattern."""
        if len(highs) < 10:
            return False
        
        recent_highs = highs[-5:]
        recent_lows = lows[-5:]
        
        # Check if both highs and lows are converging
        high_trend = np.polyfit(range(len(recent_highs)), recent_highs, 1)[0]
        low_trend = np.polyfit(range(len(recent_lows)), recent_lows, 1)[0]
        
        return high_trend < 0 and low_trend > 0
    
    def _get_trend_recommendations(self, trend_analysis: Dict[str, Any]) -> List[str]:
        """Get recommendations based on trend analysis."""
        direction = trend_analysis['direction']
        
        if direction == 'uptrend':
            return [
                "Consider trend-following strategies",
                "Look for pullback entry opportunities",
                "Set trailing stop-losses",
                "Monitor for trend continuation signals"
            ]
        elif direction == 'downtrend':
            return [
                "Consider short-selling opportunities",
                "Implement defensive strategies",
                "Reduce position sizes",
                "Look for trend reversal signals"
            ]
        else:
            return [
                "Consider range-bound strategies",
                "Look for breakout opportunities",
                "Implement mean reversion strategies",
                "Monitor for trend development"
            ]
    
    def _get_regime_recommendations(self, regime: str) -> List[str]:
        """Get recommendations based on market regime."""
        if regime == 'volatile':
            return [
                "Implement strict risk management",
                "Consider volatility-based strategies",
                "Reduce position sizes",
                "Use wider stop-losses"
            ]
        elif regime == 'calm':
            return [
                "Consider trend-following strategies",
                "Look for breakout opportunities",
                "Prepare for volatility expansion",
                "Monitor for regime changes"
            ]
        else:
            return [
                "Maintain balanced approach",
                "Monitor for regime changes",
                "Implement diversified strategies",
                "Use standard risk management"
            ]
    
    def _get_structure_recommendations(self, pattern: str) -> List[str]:
        """Get recommendations based on market structure pattern."""
        if pattern == 'ascending_triangle':
            return [
                "Prepare for potential bullish breakout",
                "Monitor volume for confirmation",
                "Set stop-loss below triangle support",
                "Target price above resistance"
            ]
        elif pattern == 'descending_triangle':
            return [
                "Prepare for potential bearish breakdown",
                "Monitor volume for confirmation",
                "Set stop-loss above triangle resistance",
                "Target price below support"
            ]
        elif pattern == 'symmetrical_triangle':
            return [
                "Prepare for directional breakout",
                "Monitor volume for confirmation",
                "Set stop-loss outside triangle",
                "Wait for clear direction"
            ]
        else:
            return [
                "Monitor for pattern development",
                "Use standard technical analysis",
                "Implement appropriate risk management"
            ]
