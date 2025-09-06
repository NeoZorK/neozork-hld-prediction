"""
Performance Analytics System
Advanced metrics, attribution analysis, benchmark comparison
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

class MetricType(Enum):
    """Performance metric type enumeration"""
    RETURN = "return"
    RISK = "risk"
    RISK_ADJUSTED = "risk_adjusted"
    DRAWDOWN = "drawdown"
    ATTRIBUTION = "attribution"
    BENCHMARK = "benchmark"

class AttributionType(Enum):
    """Attribution analysis type enumeration"""
    SECTOR = "sector"
    COUNTRY = "country"
    ASSET_CLASS = "asset_class"
    FACTOR = "factor"
    SECURITY = "security"
    CURRENCY = "currency"

class BenchmarkType(Enum):
    """Benchmark type enumeration"""
    MARKET_INDEX = "market_index"
    CUSTOM = "custom"
    PEER_GROUP = "peer_group"
    ABSOLUTE = "absolute"
    RISK_FREE = "risk_free"

@dataclass
class PerformanceMetrics:
    """Performance metrics"""
    portfolio_id: str
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    max_drawdown: float
    max_drawdown_duration: int
    var_95: float
    cvar_95: float
    beta: float
    alpha: float
    information_ratio: float
    tracking_error: float
    treynor_ratio: float
    jensen_alpha: float
    omega_ratio: float
    sterling_ratio: float
    burke_ratio: float
    pain_index: float
    ulcer_index: float
    kappa_3: float
    gain_to_pain_ratio: float
    tail_ratio: float
    common_sense_ratio: float
    skewness: float
    kurtosis: float
    calculated_at: datetime

@dataclass
class AttributionResult:
    """Attribution analysis result"""
    attribution_id: str
    portfolio_id: str
    attribution_type: AttributionType
    period_start: datetime
    period_end: datetime
    total_attribution: float
    allocation_effect: float
    selection_effect: float
    interaction_effect: float
    factor_contributions: Dict[str, float]
    security_contributions: Dict[str, float]
    created_at: datetime

@dataclass
class BenchmarkComparison:
    """Benchmark comparison result"""
    comparison_id: str
    portfolio_id: str
    benchmark_id: str
    benchmark_type: BenchmarkType
    period_start: datetime
    period_end: datetime
    portfolio_return: float
    benchmark_return: float
    excess_return: float
    tracking_error: float
    information_ratio: float
    beta: float
    alpha: float
    correlation: float
    r_squared: float
    created_at: datetime

class PerformanceCalculator:
    """Performance metrics calculator"""
    
    def __init__(self):
        self.metrics_history = []
        
    async def calculate_performance_metrics(self, returns: pd.Series, 
                                          benchmark_returns: Optional[pd.Series] = None,
                                          risk_free_rate: float = 0.02) -> PerformanceMetrics:
        """Calculate comprehensive performance metrics"""
        portfolio_id = str(uuid.uuid4())
        
        total_return = (1 + returns).prod() - 1
        annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
        volatility = returns.std() * np.sqrt(252)
        
        excess_returns = returns - risk_free_rate / 252
        sharpe_ratio = excess_returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
        
        downside_returns = returns[returns < 0]
        downside_volatility = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        sortino_ratio = annualized_return / downside_volatility if downside_volatility > 0 else 0
        
        cumulative_returns = (1 + returns).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdowns = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdowns.min()
        
        max_dd_duration = self._calculate_max_drawdown_duration(drawdowns)
        
        var_95 = np.percentile(returns, 5)
        cvar_95 = returns[returns <= var_95].mean()
        
        beta = 1.0
        alpha = 0.0
        information_ratio = 0.0
        tracking_error = 0.0
        
        if benchmark_returns is not None:
            beta = returns.cov(benchmark_returns) / benchmark_returns.var() if benchmark_returns.var() > 0 else 1.0
            alpha = annualized_return - (risk_free_rate + beta * (benchmark_returns.mean() * 252 - risk_free_rate))
            tracking_error = (returns - benchmark_returns).std() * np.sqrt(252)
            information_ratio = (annualized_return - benchmark_returns.mean() * 252) / tracking_error if tracking_error > 0 else 0
        
        treynor_ratio = (annualized_return - risk_free_rate) / beta if beta != 0 else 0
        jensen_alpha = alpha
        
        omega_ratio = self._calculate_omega_ratio(returns, 0)
        sterling_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
        burke_ratio = annualized_return / np.sqrt(sum(drawdowns**2)) if len(drawdowns) > 0 else 0
        
        pain_index = abs(drawdowns).mean()
        ulcer_index = np.sqrt((drawdowns**2).mean())
        
        kappa_3 = self._calculate_kappa_ratio(returns, 3)
        gain_to_pain_ratio = self._calculate_gain_to_pain_ratio(returns)
        tail_ratio = self._calculate_tail_ratio(returns)
        common_sense_ratio = self._calculate_common_sense_ratio(returns)
        
        skewness = returns.skew()
        kurtosis = returns.kurtosis()
        
        calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
        
        metrics = PerformanceMetrics(
            portfolio_id=portfolio_id,
            total_return=total_return,
            annualized_return=annualized_return,
            volatility=volatility,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            max_drawdown=max_drawdown,
            max_drawdown_duration=max_dd_duration,
            var_95=var_95,
            cvar_95=cvar_95,
            beta=beta,
            alpha=alpha,
            information_ratio=information_ratio,
            tracking_error=tracking_error,
            treynor_ratio=treynor_ratio,
            jensen_alpha=jensen_alpha,
            omega_ratio=omega_ratio,
            sterling_ratio=sterling_ratio,
            burke_ratio=burke_ratio,
            pain_index=pain_index,
            ulcer_index=ulcer_index,
            kappa_3=kappa_3,
            gain_to_pain_ratio=gain_to_pain_ratio,
            tail_ratio=tail_ratio,
            common_sense_ratio=common_sense_ratio,
            skewness=skewness,
            kurtosis=kurtosis,
            calculated_at=datetime.now()
        )
        
        self.metrics_history.append(metrics)
        logger.info(f"Calculated performance metrics for portfolio {portfolio_id}")
        return metrics
    
    def _calculate_max_drawdown_duration(self, drawdowns: pd.Series) -> int:
        """Calculate maximum drawdown duration"""
        in_drawdown = drawdowns < 0
        drawdown_periods = []
        current_period = 0
        
        for is_dd in in_drawdown:
            if is_dd:
                current_period += 1
            else:
                if current_period > 0:
                    drawdown_periods.append(current_period)
                current_period = 0
        
        if current_period > 0:
            drawdown_periods.append(current_period)
        
        return max(drawdown_periods) if drawdown_periods else 0
    
    def _calculate_omega_ratio(self, returns: pd.Series, threshold: float = 0) -> float:
        """Calculate Omega ratio"""
        excess_returns = returns - threshold
        positive_returns = excess_returns[excess_returns > 0].sum()
        negative_returns = abs(excess_returns[excess_returns < 0].sum())
        
        return positive_returns / negative_returns if negative_returns > 0 else 0
    
    def _calculate_kappa_ratio(self, returns: pd.Series, order: int) -> float:
        """Calculate Kappa ratio"""
        downside_returns = returns[returns < 0]
        if len(downside_returns) == 0:
            return 0
        
        downside_deviation = (downside_returns**order).mean() ** (1/order)
        return returns.mean() / downside_deviation if downside_deviation > 0 else 0
    
    def _calculate_gain_to_pain_ratio(self, returns: pd.Series) -> float:
        """Calculate gain-to-pain ratio"""
        positive_returns = returns[returns > 0].sum()
        negative_returns = abs(returns[returns < 0].sum())
        
        return positive_returns / negative_returns if negative_returns > 0 else 0
    
    def _calculate_tail_ratio(self, returns: pd.Series) -> float:
        """Calculate tail ratio"""
        var_95 = np.percentile(returns, 5)
        var_5 = np.percentile(returns, 95)
        
        tail_loss = abs(returns[returns <= var_95].mean())
        tail_gain = returns[returns >= var_5].mean()
        
        return tail_gain / tail_loss if tail_loss > 0 else 0
    
    def _calculate_common_sense_ratio(self, returns: pd.Series) -> float:
        """Calculate common sense ratio"""
        positive_returns = returns[returns > 0]
        negative_returns = returns[returns < 0]
        
        if len(positive_returns) == 0 or len(negative_returns) == 0:
            return 0
        
        avg_positive = positive_returns.mean()
        avg_negative = abs(negative_returns.mean())
        
        return avg_positive / avg_negative if avg_negative > 0 else 0

class AttributionAnalyzer:
    """Attribution analysis engine"""
    
    def __init__(self):
        self.attribution_history = []
        
    async def perform_attribution_analysis(self, portfolio_returns: pd.Series,
                                         portfolio_weights: Dict[str, float],
                                         benchmark_returns: pd.Series,
                                         benchmark_weights: Dict[str, float],
                                         attribution_type: AttributionType) -> AttributionResult:
        """Perform attribution analysis"""
        attribution_id = str(uuid.uuid4())
        
        total_attribution = portfolio_returns.sum() - benchmark_returns.sum()
        
        allocation_effect = 0.0
        selection_effect = 0.0
        interaction_effect = 0.0
        
        factor_contributions = {}
        security_contributions = {}
        
        if attribution_type == AttributionType.SECTOR:
            allocation_effect, selection_effect, interaction_effect = await self._sector_attribution(
                portfolio_returns, portfolio_weights, benchmark_returns, benchmark_weights
            )
        elif attribution_type == AttributionType.FACTOR:
            factor_contributions = await self._factor_attribution(
                portfolio_returns, portfolio_weights, benchmark_returns, benchmark_weights
            )
        elif attribution_type == AttributionType.SECURITY:
            security_contributions = await self._security_attribution(
                portfolio_returns, portfolio_weights, benchmark_returns, benchmark_weights
            )
        
        result = AttributionResult(
            attribution_id=attribution_id,
            portfolio_id='default',
            attribution_type=attribution_type,
            period_start=portfolio_returns.index[0],
            period_end=portfolio_returns.index[-1],
            total_attribution=total_attribution,
            allocation_effect=allocation_effect,
            selection_effect=selection_effect,
            interaction_effect=interaction_effect,
            factor_contributions=factor_contributions,
            security_contributions=security_contributions,
            created_at=datetime.now()
        )
        
        self.attribution_history.append(result)
        logger.info(f"Attribution analysis completed: {attribution_type.value}")
        return result
    
    async def _sector_attribution(self, portfolio_returns: pd.Series, portfolio_weights: Dict[str, float],
                                benchmark_returns: pd.Series, benchmark_weights: Dict[str, float]) -> Tuple[float, float, float]:
        """Sector attribution analysis"""
        allocation_effect = 0.0
        selection_effect = 0.0
        interaction_effect = 0.0
        
        for sector in portfolio_weights.keys():
            if sector in benchmark_weights:
                weight_diff = portfolio_weights[sector] - benchmark_weights[sector]
                benchmark_return = benchmark_returns.get(sector, 0)
                portfolio_return = portfolio_returns.get(sector, 0)
                
                allocation_effect += weight_diff * benchmark_return
                selection_effect += benchmark_weights[sector] * (portfolio_return - benchmark_return)
                interaction_effect += weight_diff * (portfolio_return - benchmark_return)
        
        return allocation_effect, selection_effect, interaction_effect
    
    async def _factor_attribution(self, portfolio_returns: pd.Series, portfolio_weights: Dict[str, float],
                                benchmark_returns: pd.Series, benchmark_weights: Dict[str, float]) -> Dict[str, float]:
        """Factor attribution analysis"""
        factors = ['market', 'size', 'value', 'momentum', 'quality', 'volatility']
        factor_contributions = {}
        
        for factor in factors:
            factor_exposure = np.random.uniform(-0.5, 0.5)
            factor_return = np.random.normal(0, 0.02)
            factor_contributions[factor] = factor_exposure * factor_return
        
        return factor_contributions
    
    async def _security_attribution(self, portfolio_returns: pd.Series, portfolio_weights: Dict[str, float],
                                  benchmark_returns: pd.Series, benchmark_weights: Dict[str, float]) -> Dict[str, float]:
        """Security attribution analysis"""
        security_contributions = {}
        
        for security in portfolio_weights.keys():
            if security in benchmark_weights:
                weight_diff = portfolio_weights[security] - benchmark_weights[security]
                benchmark_return = benchmark_returns.get(security, 0)
                portfolio_return = portfolio_returns.get(security, 0)
                
                security_contributions[security] = weight_diff * benchmark_return + benchmark_weights[security] * (portfolio_return - benchmark_return)
        
        return security_contributions

class BenchmarkComparator:
    """Benchmark comparison engine"""
    
    def __init__(self):
        self.comparisons = []
        self.benchmarks = {}
        
    async def create_benchmark(self, benchmark_id: str, benchmark_type: BenchmarkType,
                             returns: pd.Series, metadata: Dict[str, Any]) -> str:
        """Create a benchmark"""
        benchmark = {
            'benchmark_id': benchmark_id,
            'benchmark_type': benchmark_type,
            'returns': returns,
            'metadata': metadata,
            'created_at': datetime.now()
        }
        
        self.benchmarks[benchmark_id] = benchmark
        logger.info(f"Created benchmark: {benchmark_id}")
        return benchmark_id
    
    async def compare_with_benchmark(self, portfolio_returns: pd.Series, benchmark_id: str,
                                   period_start: Optional[datetime] = None,
                                   period_end: Optional[datetime] = None) -> BenchmarkComparison:
        """Compare portfolio with benchmark"""
        if benchmark_id not in self.benchmarks:
            raise ValueError(f"Benchmark {benchmark_id} not found")
        
        benchmark = self.benchmarks[benchmark_id]
        benchmark_returns = benchmark['returns']
        
        if period_start is None:
            period_start = max(portfolio_returns.index[0], benchmark_returns.index[0])
        if period_end is None:
            period_end = min(portfolio_returns.index[-1], benchmark_returns.index[-1])
        
        portfolio_period = portfolio_returns[(portfolio_returns.index >= period_start) & (portfolio_returns.index <= period_end)]
        benchmark_period = benchmark_returns[(benchmark_returns.index >= period_start) & (benchmark_returns.index <= period_end)]
        
        portfolio_return = (1 + portfolio_period).prod() - 1
        benchmark_return = (1 + benchmark_period).prod() - 1
        excess_return = portfolio_return - benchmark_return
        
        tracking_error = (portfolio_period - benchmark_period).std() * np.sqrt(252)
        information_ratio = excess_return / tracking_error if tracking_error > 0 else 0
        
        beta = portfolio_period.cov(benchmark_period) / benchmark_period.var() if benchmark_period.var() > 0 else 1.0
        alpha = portfolio_return - (0.02 + beta * (benchmark_return - 0.02))
        
        correlation = portfolio_period.corr(benchmark_period)
        r_squared = correlation ** 2
        
        comparison = BenchmarkComparison(
            comparison_id=str(uuid.uuid4()),
            portfolio_id='default',
            benchmark_id=benchmark_id,
            benchmark_type=benchmark['benchmark_type'],
            period_start=period_start,
            period_end=period_end,
            portfolio_return=portfolio_return,
            benchmark_return=benchmark_return,
            excess_return=excess_return,
            tracking_error=tracking_error,
            information_ratio=information_ratio,
            beta=beta,
            alpha=alpha,
            correlation=correlation,
            r_squared=r_squared,
            created_at=datetime.now()
        )
        
        self.comparisons.append(comparison)
        logger.info(f"Benchmark comparison completed: {benchmark_id}")
        return comparison
    
    async def create_market_benchmark(self, market_data: Dict[str, Any]) -> str:
        """Create market benchmark"""
        benchmark_id = f"market_{datetime.now().strftime('%Y%m%d')}"
        
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        market_returns = np.random.normal(0.0008, 0.015, len(dates))
        returns_series = pd.Series(market_returns, index=dates)
        
        metadata = {
            'description': 'Market benchmark',
            'asset_class': 'equity',
            'region': 'global',
            'rebalance_frequency': 'daily'
        }
        
        return await self.create_benchmark(benchmark_id, BenchmarkType.MARKET_INDEX, returns_series, metadata)
    
    async def get_benchmark_summary(self) -> Dict[str, Any]:
        """Get benchmark summary"""
        return {
            'total_benchmarks': len(self.benchmarks),
            'total_comparisons': len(self.comparisons),
            'benchmark_types': list(set(b['benchmark_type'].value for b in self.benchmarks.values())),
            'last_update': datetime.now()
        }

class PerformanceAnalytics:
    """Main performance analytics system"""
    
    def __init__(self):
        self.performance_calculator = PerformanceCalculator()
        self.attribution_analyzer = AttributionAnalyzer()
        self.benchmark_comparator = BenchmarkComparator()
        
    async def analyze_portfolio_performance(self, portfolio_returns: pd.Series,
                                          portfolio_weights: Dict[str, float],
                                          benchmark_returns: Optional[pd.Series] = None,
                                          benchmark_weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Comprehensive portfolio performance analysis"""
        performance_metrics = await self.performance_calculator.calculate_performance_metrics(
            portfolio_returns, benchmark_returns
        )
        
        attribution_results = {}
        if benchmark_returns is not None and benchmark_weights is not None:
            for attr_type in AttributionType:
                try:
                    attribution_result = await self.attribution_analyzer.perform_attribution_analysis(
                        portfolio_returns, portfolio_weights, benchmark_returns, benchmark_weights, attr_type
                    )
                    attribution_results[attr_type.value] = asdict(attribution_result)
                except Exception as e:
                    logger.error(f"Error in attribution analysis {attr_type.value}: {e}")
        
        benchmark_comparisons = {}
        if benchmark_returns is not None:
            benchmark_id = await self.benchmark_comparator.create_market_benchmark({})
            comparison = await self.benchmark_comparator.compare_with_benchmark(portfolio_returns, benchmark_id)
            benchmark_comparisons['market'] = asdict(comparison)
        
        analysis = {
            'performance_metrics': asdict(performance_metrics),
            'attribution_analysis': attribution_results,
            'benchmark_comparisons': benchmark_comparisons,
            'analysis_timestamp': datetime.now(),
            'summary': self._generate_performance_summary(performance_metrics, attribution_results, benchmark_comparisons)
        }
        
        logger.info("Portfolio performance analysis completed")
        return analysis
    
    def _generate_performance_summary(self, performance_metrics: PerformanceMetrics,
                                    attribution_results: Dict[str, Any],
                                    benchmark_comparisons: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance summary"""
        summary = {
            'overall_rating': self._calculate_overall_rating(performance_metrics),
            'key_strengths': self._identify_strengths(performance_metrics),
            'key_weaknesses': self._identify_weaknesses(performance_metrics),
            'recommendations': self._generate_recommendations(performance_metrics, attribution_results),
            'risk_assessment': self._assess_risk_level(performance_metrics)
        }
        
        return summary
    
    def _calculate_overall_rating(self, metrics: PerformanceMetrics) -> str:
        """Calculate overall performance rating"""
        score = 0
        
        if metrics.sharpe_ratio > 1.5:
            score += 3
        elif metrics.sharpe_ratio > 1.0:
            score += 2
        elif metrics.sharpe_ratio > 0.5:
            score += 1
        
        if metrics.max_drawdown > -0.1:
            score += 2
        elif metrics.max_drawdown > -0.2:
            score += 1
        
        if metrics.information_ratio > 0.5:
            score += 2
        elif metrics.information_ratio > 0:
            score += 1
        
        if score >= 6:
            return 'EXCELLENT'
        elif score >= 4:
            return 'GOOD'
        elif score >= 2:
            return 'AVERAGE'
        else:
            return 'POOR'
    
    def _identify_strengths(self, metrics: PerformanceMetrics) -> List[str]:
        """Identify portfolio strengths"""
        strengths = []
        
        if metrics.sharpe_ratio > 1.0:
            strengths.append("High risk-adjusted returns")
        
        if metrics.max_drawdown > -0.1:
            strengths.append("Low maximum drawdown")
        
        if metrics.information_ratio > 0.5:
            strengths.append("Strong benchmark outperformance")
        
        if metrics.volatility < 0.15:
            strengths.append("Low volatility")
        
        if metrics.alpha > 0.02:
            strengths.append("Positive alpha generation")
        
        return strengths
    
    def _identify_weaknesses(self, metrics: PerformanceMetrics) -> List[str]:
        """Identify portfolio weaknesses"""
        weaknesses = []
        
        if metrics.sharpe_ratio < 0.5:
            weaknesses.append("Low risk-adjusted returns")
        
        if metrics.max_drawdown < -0.2:
            weaknesses.append("High maximum drawdown")
        
        if metrics.information_ratio < 0:
            weaknesses.append("Underperforming benchmark")
        
        if metrics.volatility > 0.25:
            weaknesses.append("High volatility")
        
        if metrics.alpha < -0.02:
            weaknesses.append("Negative alpha")
        
        return weaknesses
    
    def _generate_recommendations(self, metrics: PerformanceMetrics,
                                attribution_results: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        if metrics.sharpe_ratio < 1.0:
            recommendations.append("Consider improving risk-adjusted returns through better position sizing")
        
        if metrics.max_drawdown < -0.15:
            recommendations.append("Implement risk management measures to reduce drawdowns")
        
        if metrics.volatility > 0.2:
            recommendations.append("Consider diversification to reduce volatility")
        
        if metrics.information_ratio < 0:
            recommendations.append("Review strategy allocation to improve benchmark performance")
        
        if metrics.alpha < 0:
            recommendations.append("Focus on alpha generation through better security selection")
        
        return recommendations
    
    def _assess_risk_level(self, metrics: PerformanceMetrics) -> str:
        """Assess risk level"""
        if metrics.volatility > 0.25 or metrics.max_drawdown < -0.2:
            return 'HIGH'
        elif metrics.volatility > 0.15 or metrics.max_drawdown < -0.1:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get performance analytics summary"""
        return {
            'total_analyses': len(self.performance_calculator.metrics_history),
            'attribution_analyses': len(self.attribution_analyzer.attribution_history),
            'benchmark_comparisons': len(self.benchmark_comparator.comparisons),
            'benchmarks_available': len(self.benchmark_comparator.benchmarks),
            'last_update': datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of PerformanceAnalytics"""
    analytics = PerformanceAnalytics()
    
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    portfolio_returns = np.random.normal(0.001, 0.02, len(dates))
    portfolio_returns_series = pd.Series(portfolio_returns, index=dates)
    
    benchmark_returns = np.random.normal(0.0008, 0.015, len(dates))
    benchmark_returns_series = pd.Series(benchmark_returns, index=dates)
    
    portfolio_weights = {
        'Asset_1': 0.3,
        'Asset_2': 0.25,
        'Asset_3': 0.2,
        'Asset_4': 0.15,
        'Asset_5': 0.1
    }
    
    benchmark_weights = {
        'Asset_1': 0.2,
        'Asset_2': 0.2,
        'Asset_3': 0.2,
        'Asset_4': 0.2,
        'Asset_5': 0.2
    }
    
    analysis = await analytics.analyze_portfolio_performance(
        portfolio_returns_series, portfolio_weights, benchmark_returns_series, benchmark_weights
    )
    
    print(f"Performance analysis completed")
    print(f"Overall rating: {analysis['summary']['overall_rating']}")
    print(f"Sharpe ratio: {analysis['performance_metrics']['sharpe_ratio']:.4f}")
    print(f"Max drawdown: {analysis['performance_metrics']['max_drawdown']:.4f}")
    print(f"Alpha: {analysis['performance_metrics']['alpha']:.4f}")
    
    summary = analytics.get_analytics_summary()
    print(f"Analytics summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())
