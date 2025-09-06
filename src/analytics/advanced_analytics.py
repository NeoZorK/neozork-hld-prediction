# -*- coding: utf-8 -*-
"""
Advanced Analytics and Visualization for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive analytics and visualization capabilities.
"""

import numpy as np
import pandas as pd
import logging
import time
from typing import Dict, Any, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticsType(Enum):
    """Analytics types."""
    PERFORMANCE_ANALYSIS = "performance_analysis"
    RISK_ANALYSIS = "risk_analysis"
    CORRELATION_ANALYSIS = "correlation_analysis"
    REGIME_ANALYSIS = "regime_analysis"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    MARKET_MICROSTRUCTURE = "market_microstructure"
    PORTFOLIO_ANALYSIS = "portfolio_analysis"
    BACKTESTING_ANALYSIS = "backtesting_analysis"
    PREDICTIVE_ANALYSIS = "predictive_analysis"
    STATISTICAL_ANALYSIS = "statistical_analysis"

class VisualizationType(Enum):
    """Visualization types."""
    LINE_CHART = "line_chart"
    CANDLESTICK_CHART = "candlestick_chart"
    HEATMAP = "heatmap"
    SCATTER_PLOT = "scatter_plot"
    HISTOGRAM = "histogram"
    BOX_PLOT = "box_plot"
    CORRELATION_MATRIX = "correlation_matrix"
    DASHBOARD = "dashboard"
    INTERACTIVE_CHART = "interactive_chart"
    REAL_TIME_CHART = "real_time_chart"

class ChartTheme(Enum):
    """Chart themes."""
    DARK = "dark"
    LIGHT = "light"
    MINIMAL = "minimal"
    COLORFUL = "colorful"
    PROFESSIONAL = "professional"

@dataclass
class AnalyticsConfig:
    """Analytics configuration."""
    analytics_type: AnalyticsType
    time_period: str = "1Y"
    symbols: List[str] = field(default_factory=list)
    indicators: List[str] = field(default_factory=list)
    custom_metrics: List[str] = field(default_factory=list)
    visualization_type: VisualizationType = VisualizationType.LINE_CHART
    theme: ChartTheme = ChartTheme.DARK

@dataclass
class AnalyticsResult:
    """Analytics result."""
    analytics_type: AnalyticsType
    data: Dict[str, Any]
    metrics: Dict[str, float]
    insights: List[str]
    recommendations: List[str]
    visualization_data: Dict[str, Any] = field(default_factory=dict)

class AdvancedAnalytics:
    """Advanced analytics and visualization system."""
    
    def __init__(self):
        self.analytics_history = []
        self.visualization_cache = {}
        self.custom_metrics = {}
        
    def perform_performance_analysis(self, data: pd.DataFrame, 
                                   config: AnalyticsConfig) -> AnalyticsResult:
        """Perform comprehensive performance analysis."""
        try:
            results = {}
            metrics = {}
            insights = []
            recommendations = []
            
            # Calculate basic performance metrics
            if 'price' in data.columns:
                returns = data['price'].pct_change().dropna()
                
                # Performance metrics
                total_return = (data['price'].iloc[-1] / data['price'].iloc[0] - 1) * 100
                annualized_return = ((1 + total_return/100) ** (252/len(data)) - 1) * 100
                volatility = returns.std() * np.sqrt(252) * 100
                sharpe_ratio = annualized_return / volatility if volatility > 0 else 0
                
                # Risk metrics
                max_drawdown = self._calculate_max_drawdown(data['price'])
                var_95 = np.percentile(returns, 5) * 100
                cvar_95 = returns[returns <= np.percentile(returns, 5)].mean() * 100
                
                # Additional metrics
                win_rate = (returns > 0).mean() * 100
                profit_factor = returns[returns > 0].sum() / abs(returns[returns < 0].sum()) if returns[returns < 0].sum() != 0 else float('inf')
                calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
                
                metrics.update({
                    'total_return': total_return,
                    'annualized_return': annualized_return,
                    'volatility': volatility,
                    'sharpe_ratio': sharpe_ratio,
                    'max_drawdown': max_drawdown,
                    'var_95': var_95,
                    'cvar_95': cvar_95,
                    'win_rate': win_rate,
                    'profit_factor': profit_factor,
                    'calmar_ratio': calmar_ratio
                })
                
                # Generate insights
                if sharpe_ratio > 1.0:
                    insights.append("Excellent risk-adjusted returns with Sharpe ratio > 1.0")
                elif sharpe_ratio > 0.5:
                    insights.append("Good risk-adjusted returns")
                else:
                    insights.append("Poor risk-adjusted returns")
                
                if max_drawdown < -10:
                    insights.append("High maximum drawdown indicates significant risk")
                
                if win_rate > 60:
                    insights.append("High win rate indicates consistent profitability")
                
                # Generate recommendations
                if sharpe_ratio < 0.5:
                    recommendations.append("Consider improving risk management to increase Sharpe ratio")
                
                if max_drawdown < -15:
                    recommendations.append("Implement stop-loss strategies to limit drawdowns")
                
                if volatility > 30:
                    recommendations.append("High volatility - consider position sizing adjustments")
            
            # Technical indicators analysis
            if config.indicators:
                indicator_analysis = self._analyze_technical_indicators(data, config.indicators)
                results['technical_indicators'] = indicator_analysis
                
                # Add indicator-based insights
                for indicator, analysis in indicator_analysis.items():
                    if 'signal' in analysis:
                        if analysis['signal'] == 'bullish':
                            insights.append(f"{indicator} shows bullish signal")
                        elif analysis['signal'] == 'bearish':
                            insights.append(f"{indicator} shows bearish signal")
            
            # Prepare visualization data
            visualization_data = {
                'price_data': data['price'].tolist() if 'price' in data.columns else [],
                'returns_data': returns.tolist() if 'price' in data.columns else [],
                'timestamps': data.index.tolist() if hasattr(data.index, 'tolist') else list(range(len(data))),
                'metrics': metrics
            }
            
            result = AnalyticsResult(
                analytics_type=AnalyticsType.PERFORMANCE_ANALYSIS,
                data=results,
                metrics=metrics,
                insights=insights,
                recommendations=recommendations,
                visualization_data=visualization_data
            )
            
            # Store in history
            self.analytics_history.append(result)
            
            logger.info("Performance analysis completed successfully")
            
            return result
            
        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
            return AnalyticsResult(
                analytics_type=AnalyticsType.PERFORMANCE_ANALYSIS,
                data={},
                metrics={},
                insights=[],
                recommendations=[]
            )
    
    def perform_risk_analysis(self, data: pd.DataFrame, 
                            config: AnalyticsConfig) -> AnalyticsResult:
        """Perform comprehensive risk analysis."""
        try:
            results = {}
            metrics = {}
            insights = []
            recommendations = []
            
            if 'price' in data.columns:
                returns = data['price'].pct_change().dropna()
                
                # Risk metrics
                volatility = returns.std() * np.sqrt(252)
                var_95 = np.percentile(returns, 5)
                var_99 = np.percentile(returns, 1)
                cvar_95 = returns[returns <= var_95].mean()
                cvar_99 = returns[returns <= var_99].mean()
                
                # Tail risk
                tail_ratio = abs(cvar_95) / volatility if volatility > 0 else 0
                
                # Skewness and Kurtosis
                skewness = returns.skew()
                kurtosis = returns.kurtosis()
                
                # Downside deviation
                downside_returns = returns[returns < 0]
                downside_deviation = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
                
                # Sortino ratio
                sortino_ratio = returns.mean() * 252 / downside_deviation if downside_deviation > 0 else 0
                
                metrics.update({
                    'volatility': volatility,
                    'var_95': var_95,
                    'var_99': var_99,
                    'cvar_95': cvar_95,
                    'cvar_99': cvar_99,
                    'tail_ratio': tail_ratio,
                    'skewness': skewness,
                    'kurtosis': kurtosis,
                    'downside_deviation': downside_deviation,
                    'sortino_ratio': sortino_ratio
                })
                
                # Risk insights
                if volatility > 0.3:
                    insights.append("High volatility indicates significant price risk")
                
                if abs(skewness) > 1:
                    insights.append("High skewness indicates asymmetric return distribution")
                
                if kurtosis > 3:
                    insights.append("High kurtosis indicates fat tails and extreme events")
                
                if tail_ratio > 1.5:
                    insights.append("High tail risk - extreme losses are more likely")
                
                # Risk recommendations
                if volatility > 0.4:
                    recommendations.append("Consider reducing position size due to high volatility")
                
                if cvar_95 < -0.05:
                    recommendations.append("Implement stricter risk controls - high tail risk")
                
                if sortino_ratio < 0.5:
                    recommendations.append("Poor downside risk-adjusted returns - review strategy")
            
            # Correlation analysis if multiple assets
            if len(data.columns) > 1:
                correlation_matrix = data.corr()
                results['correlation_matrix'] = correlation_matrix.to_dict()
                
                # Find high correlations
                high_correlations = []
                for i in range(len(correlation_matrix.columns)):
                    for j in range(i+1, len(correlation_matrix.columns)):
                        corr = correlation_matrix.iloc[i, j]
                        if abs(corr) > 0.7:
                            high_correlations.append({
                                'asset1': correlation_matrix.columns[i],
                                'asset2': correlation_matrix.columns[j],
                                'correlation': corr
                            })
                
                if high_correlations:
                    insights.append(f"High correlations detected between {len(high_correlations)} asset pairs")
                    recommendations.append("Consider diversification to reduce correlation risk")
            
            # Prepare visualization data
            visualization_data = {
                'returns_histogram': returns.tolist() if 'price' in data.columns else [],
                'correlation_matrix': results.get('correlation_matrix', {}),
                'risk_metrics': metrics
            }
            
            result = AnalyticsResult(
                analytics_type=AnalyticsType.RISK_ANALYSIS,
                data=results,
                metrics=metrics,
                insights=insights,
                recommendations=recommendations,
                visualization_data=visualization_data
            )
            
            self.analytics_history.append(result)
            
            logger.info("Risk analysis completed successfully")
            
            return result
            
        except Exception as e:
            logger.error(f"Risk analysis failed: {e}")
            return AnalyticsResult(
                analytics_type=AnalyticsType.RISK_ANALYSIS,
                data={},
                metrics={},
                insights=[],
                recommendations=[]
            )
    
    def perform_sentiment_analysis(self, sentiment_data: List[Dict[str, Any]], 
                                 config: AnalyticsConfig) -> AnalyticsResult:
        """Perform sentiment analysis."""
        try:
            results = {}
            metrics = {}
            insights = []
            recommendations = []
            
            if not sentiment_data:
                return AnalyticsResult(
                    analytics_type=AnalyticsType.SENTIMENT_ANALYSIS,
                    data={},
                    metrics={},
                    insights=["No sentiment data available"],
                    recommendations=[]
                )
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(sentiment_data)
            
            # Sentiment metrics
            avg_sentiment = df['sentiment_score'].mean()
            sentiment_std = df['sentiment_score'].std()
            sentiment_volatility = sentiment_std / abs(avg_sentiment) if avg_sentiment != 0 else 0
            
            # Sentiment distribution
            sentiment_counts = df['sentiment_type'].value_counts()
            sentiment_distribution = sentiment_counts.to_dict()
            
            # Time-based sentiment analysis
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['hour'] = df['timestamp'].dt.hour
                df['day_of_week'] = df['timestamp'].dt.dayofweek
                
                hourly_sentiment = df.groupby('hour')['sentiment_score'].mean()
                daily_sentiment = df.groupby('day_of_week')['sentiment_score'].mean()
                
                results['hourly_sentiment'] = hourly_sentiment.to_dict()
                results['daily_sentiment'] = daily_sentiment.to_dict()
            
            # Source analysis
            if 'source' in df.columns:
                source_sentiment = df.groupby('source')['sentiment_score'].agg(['mean', 'count'])
                results['source_analysis'] = source_sentiment.to_dict()
            
            metrics.update({
                'average_sentiment': avg_sentiment,
                'sentiment_volatility': sentiment_volatility,
                'total_sentiments': len(df),
                'positive_ratio': sentiment_distribution.get('positive', 0) / len(df),
                'negative_ratio': sentiment_distribution.get('negative', 0) / len(df),
                'neutral_ratio': sentiment_distribution.get('neutral', 0) / len(df)
            })
            
            # Sentiment insights
            if avg_sentiment > 0.3:
                insights.append("Overall positive market sentiment")
            elif avg_sentiment < -0.3:
                insights.append("Overall negative market sentiment")
            else:
                insights.append("Neutral market sentiment")
            
            if sentiment_volatility > 0.5:
                insights.append("High sentiment volatility indicates uncertainty")
            
            if metrics['positive_ratio'] > 0.6:
                insights.append("Strong positive sentiment dominance")
            elif metrics['negative_ratio'] > 0.6:
                insights.append("Strong negative sentiment dominance")
            
            # Sentiment recommendations
            if avg_sentiment < -0.5:
                recommendations.append("Consider defensive positioning due to negative sentiment")
            elif avg_sentiment > 0.5:
                recommendations.append("Positive sentiment may indicate buying opportunities")
            
            if sentiment_volatility > 0.7:
                recommendations.append("High sentiment volatility - use smaller position sizes")
            
            # Prepare visualization data
            visualization_data = {
                'sentiment_scores': df['sentiment_score'].tolist(),
                'sentiment_distribution': sentiment_distribution,
                'hourly_sentiment': results.get('hourly_sentiment', {}),
                'daily_sentiment': results.get('daily_sentiment', {}),
                'metrics': metrics
            }
            
            result = AnalyticsResult(
                analytics_type=AnalyticsType.SENTIMENT_ANALYSIS,
                data=results,
                metrics=metrics,
                insights=insights,
                recommendations=recommendations,
                visualization_data=visualization_data
            )
            
            self.analytics_history.append(result)
            
            logger.info("Sentiment analysis completed successfully")
            
            return result
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return AnalyticsResult(
                analytics_type=AnalyticsType.SENTIMENT_ANALYSIS,
                data={},
                metrics={},
                insights=[],
                recommendations=[]
            )
    
    def perform_portfolio_analysis(self, portfolio_data: Dict[str, pd.DataFrame], 
                                 config: AnalyticsConfig) -> AnalyticsResult:
        """Perform portfolio analysis."""
        try:
            results = {}
            metrics = {}
            insights = []
            recommendations = []
            
            # Portfolio performance
            portfolio_returns = []
            portfolio_weights = {}
            
            for symbol, data in portfolio_data.items():
                if 'price' in data.columns:
                    returns = data['price'].pct_change().dropna()
                    portfolio_returns.append(returns)
                    portfolio_weights[symbol] = 1.0 / len(portfolio_data)  # Equal weight for now
            
            if portfolio_returns:
                # Calculate portfolio metrics
                portfolio_returns_df = pd.concat(portfolio_returns, axis=1)
                portfolio_returns_df.columns = list(portfolio_data.keys())
                
                # Equal-weighted portfolio returns
                portfolio_return = portfolio_returns_df.mean(axis=1)
                
                # Portfolio metrics
                total_return = (portfolio_return + 1).prod() - 1
                annualized_return = (1 + total_return) ** (252/len(portfolio_return)) - 1
                portfolio_volatility = portfolio_return.std() * np.sqrt(252)
                portfolio_sharpe = annualized_return / portfolio_volatility if portfolio_volatility > 0 else 0
                
                # Diversification metrics
                correlation_matrix = portfolio_returns_df.corr()
                avg_correlation = correlation_matrix.values[np.triu_indices_from(correlation_matrix.values, k=1)].mean()
                
                # Concentration risk
                weights_array = np.array(list(portfolio_weights.values()))
                herfindahl_index = np.sum(weights_array ** 2)
                effective_assets = 1 / herfindahl_index
                
                metrics.update({
                    'total_return': total_return,
                    'annualized_return': annualized_return,
                    'portfolio_volatility': portfolio_volatility,
                    'portfolio_sharpe': portfolio_sharpe,
                    'avg_correlation': avg_correlation,
                    'herfindahl_index': herfindahl_index,
                    'effective_assets': effective_assets,
                    'num_assets': len(portfolio_data)
                })
                
                # Portfolio insights
                if portfolio_sharpe > 1.0:
                    insights.append("Excellent portfolio risk-adjusted returns")
                elif portfolio_sharpe > 0.5:
                    insights.append("Good portfolio risk-adjusted returns")
                else:
                    insights.append("Poor portfolio risk-adjusted returns")
                
                if avg_correlation > 0.7:
                    insights.append("High correlation between assets reduces diversification benefits")
                
                if effective_assets < len(portfolio_data) * 0.7:
                    insights.append("Portfolio concentration risk detected")
                
                # Portfolio recommendations
                if avg_correlation > 0.8:
                    recommendations.append("Consider adding uncorrelated assets to improve diversification")
                
                if portfolio_volatility > 0.3:
                    recommendations.append("High portfolio volatility - consider risk management")
                
                if effective_assets < 3:
                    recommendations.append("Low effective number of assets - consider rebalancing")
            
            # Prepare visualization data
            visualization_data = {
                'portfolio_returns': portfolio_return.tolist() if portfolio_returns else [],
                'correlation_matrix': correlation_matrix.to_dict() if portfolio_returns else {},
                'portfolio_weights': portfolio_weights,
                'metrics': metrics
            }
            
            result = AnalyticsResult(
                analytics_type=AnalyticsType.PORTFOLIO_ANALYSIS,
                data=results,
                metrics=metrics,
                insights=insights,
                recommendations=recommendations,
                visualization_data=visualization_data
            )
            
            self.analytics_history.append(result)
            
            logger.info("Portfolio analysis completed successfully")
            
            return result
            
        except Exception as e:
            logger.error(f"Portfolio analysis failed: {e}")
            return AnalyticsResult(
                analytics_type=AnalyticsType.PORTFOLIO_ANALYSIS,
                data={},
                metrics={},
                insights=[],
                recommendations=[]
            )
    
    def _calculate_max_drawdown(self, prices: pd.Series) -> float:
        """Calculate maximum drawdown."""
        try:
            peak = prices.expanding().max()
            drawdown = (prices - peak) / peak
            return drawdown.min() * 100
        except Exception as e:
            logger.error(f"Failed to calculate max drawdown: {e}")
            return 0.0
    
    def _analyze_technical_indicators(self, data: pd.DataFrame, indicators: List[str]) -> Dict[str, Any]:
        """Analyze technical indicators."""
        try:
            results = {}
            
            for indicator in indicators:
                if indicator == 'rsi' and 'price' in data.columns:
                    # Calculate RSI
                    delta = data['price'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs))
                    
                    current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
                    
                    if current_rsi > 70:
                        signal = 'bearish'
                    elif current_rsi < 30:
                        signal = 'bullish'
                    else:
                        signal = 'neutral'
                    
                    results['rsi'] = {
                        'value': current_rsi,
                        'signal': signal,
                        'overbought': current_rsi > 70,
                        'oversold': current_rsi < 30
                    }
                
                elif indicator == 'macd' and 'price' in data.columns:
                    # Calculate MACD
                    ema_12 = data['price'].ewm(span=12).mean()
                    ema_26 = data['price'].ewm(span=26).mean()
                    macd_line = ema_12 - ema_26
                    signal_line = macd_line.ewm(span=9).mean()
                    histogram = macd_line - signal_line
                    
                    current_macd = macd_line.iloc[-1] if not pd.isna(macd_line.iloc[-1]) else 0
                    current_signal = signal_line.iloc[-1] if not pd.isna(signal_line.iloc[-1]) else 0
                    current_histogram = histogram.iloc[-1] if not pd.isna(histogram.iloc[-1]) else 0
                    
                    if current_macd > current_signal and current_histogram > 0:
                        signal = 'bullish'
                    elif current_macd < current_signal and current_histogram < 0:
                        signal = 'bearish'
                    else:
                        signal = 'neutral'
                    
                    results['macd'] = {
                        'macd_line': current_macd,
                        'signal_line': current_signal,
                        'histogram': current_histogram,
                        'signal': signal
                    }
                
                elif indicator == 'bollinger_bands' and 'price' in data.columns:
                    # Calculate Bollinger Bands
                    sma_20 = data['price'].rolling(window=20).mean()
                    std_20 = data['price'].rolling(window=20).std()
                    upper_band = sma_20 + (std_20 * 2)
                    lower_band = sma_20 - (std_20 * 2)
                    
                    current_price = data['price'].iloc[-1]
                    current_upper = upper_band.iloc[-1] if not pd.isna(upper_band.iloc[-1]) else current_price
                    current_lower = lower_band.iloc[-1] if not pd.isna(lower_band.iloc[-1]) else current_price
                    current_sma = sma_20.iloc[-1] if not pd.isna(sma_20.iloc[-1]) else current_price
                    
                    if current_price > current_upper:
                        signal = 'bearish'
                    elif current_price < current_lower:
                        signal = 'bullish'
                    else:
                        signal = 'neutral'
                    
                    results['bollinger_bands'] = {
                        'upper_band': current_upper,
                        'lower_band': current_lower,
                        'middle_band': current_sma,
                        'current_price': current_price,
                        'signal': signal,
                        'position': (current_price - current_lower) / (current_upper - current_lower) if current_upper != current_lower else 0.5
                    }
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to analyze technical indicators: {e}")
            return {}
    
    def create_visualization(self, result: AnalyticsResult, 
                           config: AnalyticsConfig) -> Dict[str, Any]:
        """Create visualization for analytics result."""
        try:
            visualization = {
                'type': config.visualization_type.value,
                'theme': config.theme.value,
                'data': result.visualization_data,
                'title': f"{result.analytics_type.value.replace('_', ' ').title()} Analysis",
                'metrics': result.metrics,
                'insights': result.insights,
                'recommendations': result.recommendations
            }
            
            # Add specific visualization configurations
            if config.visualization_type == VisualizationType.LINE_CHART:
                visualization['chart_config'] = {
                    'x_axis': 'time',
                    'y_axis': 'value',
                    'show_grid': True,
                    'show_legend': True
                }
            elif config.visualization_type == VisualizationType.HEATMAP:
                visualization['chart_config'] = {
                    'color_scheme': 'viridis',
                    'show_values': True,
                    'show_annotations': True
                }
            elif config.visualization_type == VisualizationType.DASHBOARD:
                visualization['dashboard_config'] = {
                    'layout': 'grid',
                    'widgets': ['metrics', 'charts', 'insights'],
                    'refresh_rate': 30  # seconds
                }
            
            # Cache visualization
            cache_key = f"{result.analytics_type.value}_{config.visualization_type.value}_{int(time.time())}"
            self.visualization_cache[cache_key] = visualization
            
            logger.info(f"Visualization created for {result.analytics_type.value}")
            
            return {
                'status': 'success',
                'visualization': visualization,
                'cache_key': cache_key,
                'message': f'Visualization created successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to create visualization: {e}")
            return {
                'status': 'error',
                'message': f'Failed to create visualization: {str(e)}'
            }
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get summary of all analytics performed."""
        try:
            summary = {
                'total_analyses': len(self.analytics_history),
                'analytics_by_type': {},
                'total_visualizations': len(self.visualization_cache),
                'recent_analyses': []
            }
            
            # Group by analytics type
            for result in self.analytics_history:
                analytics_type = result.analytics_type.value
                if analytics_type not in summary['analytics_by_type']:
                    summary['analytics_by_type'][analytics_type] = 0
                summary['analytics_by_type'][analytics_type] += 1
            
            # Recent analyses
            recent_results = sorted(self.analytics_history, key=lambda x: x.analytics_type.value)[-5:]
            for result in recent_results:
                summary['recent_analyses'].append({
                    'type': result.analytics_type.value,
                    'insights_count': len(result.insights),
                    'recommendations_count': len(result.recommendations),
                    'metrics_count': len(result.metrics)
                })
            
            return {
                'status': 'success',
                'summary': summary,
                'message': f'Retrieved summary for {len(self.analytics_history)} analyses'
            }
            
        except Exception as e:
            logger.error(f"Failed to get analytics summary: {e}")
            return {
                'status': 'error',
                'message': f'Failed to get analytics summary: {str(e)}'
            }

# Example usage and testing
def test_advanced_analytics():
    """Test advanced analytics and visualization system."""
    print("🧪 Testing Advanced Analytics and Visualization System...")
    
    # Create analytics system
    analytics = AdvancedAnalytics()
    
    # Generate sample data
    np.random.seed(42)
    n_observations = 1000
    
    # Create sample price data
    dates = pd.date_range(start='2020-01-01', periods=n_observations, freq='D')
    price_data = pd.DataFrame({
        'price': 100 + np.cumsum(np.random.randn(n_observations) * 0.02),
        'volume': np.random.randint(1000, 10000, n_observations)
    }, index=dates)
    
    print(f"  • Sample data created: {price_data.shape[0]} observations")
    
    # Test performance analysis
    print("  • Testing performance analysis...")
    
    config = AnalyticsConfig(
        analytics_type=AnalyticsType.PERFORMANCE_ANALYSIS,
        indicators=['rsi', 'macd', 'bollinger_bands'],
        visualization_type=VisualizationType.LINE_CHART,
        theme=ChartTheme.DARK
    )
    
    performance_result = analytics.perform_performance_analysis(price_data, config)
    print(f"    ✅ Performance analysis completed:")
    print(f"        - Total return: {performance_result.metrics.get('total_return', 0):.2f}%")
    print(f"        - Sharpe ratio: {performance_result.metrics.get('sharpe_ratio', 0):.3f}")
    print(f"        - Max drawdown: {performance_result.metrics.get('max_drawdown', 0):.2f}%")
    print(f"        - Insights: {len(performance_result.insights)}")
    print(f"        - Recommendations: {len(performance_result.recommendations)}")
    
    # Test risk analysis
    print("  • Testing risk analysis...")
    
    risk_config = AnalyticsConfig(
        analytics_type=AnalyticsType.RISK_ANALYSIS,
        visualization_type=VisualizationType.HEATMAP,
        theme=ChartTheme.PROFESSIONAL
    )
    
    risk_result = analytics.perform_risk_analysis(price_data, risk_config)
    print(f"    ✅ Risk analysis completed:")
    print(f"        - Volatility: {risk_result.metrics.get('volatility', 0):.3f}")
    print(f"        - VaR 95%: {risk_result.metrics.get('var_95', 0):.3f}")
    print(f"        - Sortino ratio: {risk_result.metrics.get('sortino_ratio', 0):.3f}")
    print(f"        - Insights: {len(risk_result.insights)}")
    
    # Test sentiment analysis
    print("  • Testing sentiment analysis...")
    
    # Generate sample sentiment data
    sentiment_data = []
    for i in range(100):
        sentiment_data.append({
            'timestamp': datetime.now() - timedelta(hours=i),
            'sentiment_score': np.random.uniform(-1, 1),
            'sentiment_type': np.random.choice(['positive', 'negative', 'neutral']),
            'source': np.random.choice(['twitter', 'reddit', 'news']),
            'confidence': np.random.uniform(0.5, 1.0)
        })
    
    sentiment_config = AnalyticsConfig(
        analytics_type=AnalyticsType.SENTIMENT_ANALYSIS,
        visualization_type=VisualizationType.SCATTER_PLOT,
        theme=ChartTheme.COLORFUL
    )
    
    sentiment_result = analytics.perform_sentiment_analysis(sentiment_data, sentiment_config)
    print(f"    ✅ Sentiment analysis completed:")
    print(f"        - Average sentiment: {sentiment_result.metrics.get('average_sentiment', 0):.3f}")
    print(f"        - Sentiment volatility: {sentiment_result.metrics.get('sentiment_volatility', 0):.3f}")
    print(f"        - Total sentiments: {sentiment_result.metrics.get('total_sentiments', 0)}")
    print(f"        - Insights: {len(sentiment_result.insights)}")
    
    # Test portfolio analysis
    print("  • Testing portfolio analysis...")
    
    # Generate sample portfolio data
    portfolio_data = {}
    symbols = ['BTC', 'ETH', 'ADA']
    for symbol in symbols:
        portfolio_data[symbol] = pd.DataFrame({
            'price': 100 + np.cumsum(np.random.randn(n_observations) * 0.02)
        }, index=dates)
    
    portfolio_config = AnalyticsConfig(
        analytics_type=AnalyticsType.PORTFOLIO_ANALYSIS,
        symbols=symbols,
        visualization_type=VisualizationType.DASHBOARD,
        theme=ChartTheme.MINIMAL
    )
    
    portfolio_result = analytics.perform_portfolio_analysis(portfolio_data, portfolio_config)
    print(f"    ✅ Portfolio analysis completed:")
    print(f"        - Portfolio return: {portfolio_result.metrics.get('total_return', 0):.3f}")
    print(f"        - Portfolio Sharpe: {portfolio_result.metrics.get('portfolio_sharpe', 0):.3f}")
    print(f"        - Effective assets: {portfolio_result.metrics.get('effective_assets', 0):.1f}")
    print(f"        - Insights: {len(portfolio_result.insights)}")
    
    # Test visualization creation
    print("  • Testing visualization creation...")
    
    viz_result = analytics.create_visualization(performance_result, config)
    if viz_result['status'] == 'success':
        print(f"    ✅ Visualization created: {viz_result['visualization']['title']}")
        print(f"        - Type: {viz_result['visualization']['type']}")
        print(f"        - Theme: {viz_result['visualization']['theme']}")
        print(f"        - Cache key: {viz_result['cache_key']}")
    else:
        print(f"    ❌ Visualization creation failed: {viz_result['message']}")
    
    # Test analytics summary
    print("  • Testing analytics summary...")
    
    summary = analytics.get_analytics_summary()
    if summary['status'] == 'success':
        print(f"    ✅ Analytics summary:")
        print(f"        - Total analyses: {summary['summary']['total_analyses']}")
        print(f"        - Total visualizations: {summary['summary']['total_visualizations']}")
        print(f"        - Analytics types: {list(summary['summary']['analytics_by_type'].keys())}")
    else:
        print(f"    ❌ Analytics summary failed: {summary['message']}")
    
    print("✅ Advanced Analytics and Visualization System test completed!")
    
    return analytics

if __name__ == "__main__":
    test_advanced_analytics()
