"""
Performance Insights for advanced analytics.

This module provides performance insights functionality for analytics.
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime, timedelta
import numpy as np

logger = logging.getLogger(__name__)


class PerformanceInsights:
    """Performance insights for analytics."""
    
    def __init__(self):
        """Initialize performance insights."""
        self.insights: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Any] = {}
        self.logger = logger
    
    def analyze_performance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance metrics from data."""
        try:
            analysis = {
                'timestamp': datetime.now().isoformat(),
                'metrics': {},
                'insights': [],
                'recommendations': []
            }
            
            # Calculate basic metrics
            if 'returns' in data:
                returns = data['returns']
                analysis['metrics']['total_return'] = self._calculate_total_return(returns)
                analysis['metrics']['volatility'] = self._calculate_volatility(returns)
                analysis['metrics']['sharpe_ratio'] = self._calculate_sharpe_ratio(returns)
                analysis['metrics']['max_drawdown'] = self._calculate_max_drawdown(returns)
            
            # Generate insights
            analysis['insights'] = self._generate_insights(analysis['metrics'])
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_recommendations(analysis['metrics'])
            
            self.insights.append(analysis)
            self.logger.info("Performance analysis completed")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing performance: {e}")
            return {}
    
    def _calculate_total_return(self, returns: List[float]) -> float:
        """Calculate total return."""
        try:
            if not returns:
                return 0.0
            return (1 + np.array(returns)).prod() - 1
        except Exception as e:
            self.logger.error(f"Error calculating total return: {e}")
            return 0.0
    
    def _calculate_volatility(self, returns: List[float]) -> float:
        """Calculate volatility (standard deviation)."""
        try:
            if not returns:
                return 0.0
            return np.std(returns)
        except Exception as e:
            self.logger.error(f"Error calculating volatility: {e}")
            return 0.0
    
    def _calculate_sharpe_ratio(self, returns: List[float], risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio."""
        try:
            if not returns:
                return 0.0
            
            excess_returns = np.array(returns) - risk_free_rate / 252  # Daily risk-free rate
            if np.std(excess_returns) == 0:
                return 0.0
            
            return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
        except Exception as e:
            self.logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0.0
    
    def _calculate_max_drawdown(self, returns: List[float]) -> float:
        """Calculate maximum drawdown."""
        try:
            if not returns:
                return 0.0
            
            cumulative = (1 + np.array(returns)).cumprod()
            running_max = np.maximum.accumulate(cumulative)
            drawdown = (cumulative - running_max) / running_max
            return np.min(drawdown)
        except Exception as e:
            self.logger.error(f"Error calculating max drawdown: {e}")
            return 0.0
    
    def _generate_insights(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate insights from metrics."""
        insights = []
        
        try:
            if 'sharpe_ratio' in metrics:
                sharpe = metrics['sharpe_ratio']
                if sharpe > 1.0:
                    insights.append("Excellent risk-adjusted returns (Sharpe > 1.0)")
                elif sharpe > 0.5:
                    insights.append("Good risk-adjusted returns (Sharpe > 0.5)")
                elif sharpe > 0:
                    insights.append("Positive risk-adjusted returns")
                else:
                    insights.append("Poor risk-adjusted returns")
            
            if 'volatility' in metrics:
                vol = metrics['volatility']
                if vol < 0.1:
                    insights.append("Low volatility portfolio")
                elif vol < 0.2:
                    insights.append("Moderate volatility portfolio")
                else:
                    insights.append("High volatility portfolio")
            
            if 'max_drawdown' in metrics:
                dd = abs(metrics['max_drawdown'])
                if dd < 0.05:
                    insights.append("Low maximum drawdown")
                elif dd < 0.15:
                    insights.append("Moderate maximum drawdown")
                else:
                    insights.append("High maximum drawdown")
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {e}")
        
        return insights
    
    def _generate_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate recommendations from metrics."""
        recommendations = []
        
        try:
            if 'sharpe_ratio' in metrics and metrics['sharpe_ratio'] < 0.5:
                recommendations.append("Consider improving risk-adjusted returns")
            
            if 'volatility' in metrics and metrics['volatility'] > 0.2:
                recommendations.append("Consider reducing portfolio volatility")
            
            if 'max_drawdown' in metrics and abs(metrics['max_drawdown']) > 0.15:
                recommendations.append("Consider implementing risk management strategies")
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
        
        return recommendations
    
    def get_insights(self) -> List[Dict[str, Any]]:
        """Get all insights."""
        return self.insights.copy()
    
    def get_latest_insights(self) -> Optional[Dict[str, Any]]:
        """Get the latest insights."""
        if self.insights:
            return self.insights[-1]
        return None
    
    def clear_insights(self) -> None:
        """Clear all insights."""
        self.insights.clear()
        self.logger.info("All insights cleared")
