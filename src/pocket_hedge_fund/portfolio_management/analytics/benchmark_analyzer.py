"""
Benchmark Analyzer - Benchmark Comparison and Analysis

This module provides benchmark comparison functionality including relative
performance analysis, tracking error calculation, and benchmark selection.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, date, timedelta
from decimal import Decimal
import numpy as np
import pandas as pd

from ..models.portfolio_models import Portfolio
from ..models.performance_models import BenchmarkComparison

logger = logging.getLogger(__name__)


class BenchmarkAnalyzer:
    """Benchmark comparison and analysis functionality."""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self.available_benchmarks = {
            'SP500': 'S&P 500 Index',
            'NASDAQ': 'NASDAQ Composite',
            'DOW': 'Dow Jones Industrial Average',
            'RUSSELL2000': 'Russell 2000 Index',
            'CRYPTO': 'Crypto Market Index',
            'BOND': 'US Aggregate Bond Index',
            'GOLD': 'Gold Spot Price',
            'CUSTOM': 'Custom Benchmark'
        }
        
    async def compare_to_benchmark(
        self, 
        portfolio: Portfolio, 
        benchmark_name: str,
        period: str = "1Y"
    ) -> BenchmarkComparison:
        """Compare portfolio performance to benchmark."""
        try:
            # Get historical data
            portfolio_data = await self._get_portfolio_historical_data(portfolio.id, period)
            benchmark_data = await self._get_benchmark_historical_data(benchmark_name, period)
            
            if not portfolio_data or not benchmark_data:
                return self._get_default_benchmark_comparison(benchmark_name)
            
            # Calculate returns
            portfolio_returns = self._calculate_returns(portfolio_data)
            benchmark_returns = self._calculate_returns(benchmark_data)
            
            # Align data
            aligned_data = self._align_data(portfolio_returns, benchmark_returns)
            if not aligned_data:
                return self._get_default_benchmark_comparison(benchmark_name)
            
            portfolio_aligned = aligned_data['portfolio']
            benchmark_aligned = aligned_data['benchmark']
            
            # Calculate comparison metrics
            portfolio_return = self._calculate_total_return(portfolio_aligned)
            benchmark_return = self._calculate_total_return(benchmark_aligned)
            excess_return = portfolio_return - benchmark_return
            
            # Calculate risk metrics
            tracking_error = self._calculate_tracking_error(portfolio_aligned, benchmark_aligned)
            information_ratio = self._calculate_information_ratio(portfolio_aligned, benchmark_aligned)
            
            # Calculate beta and alpha
            beta = self._calculate_beta(portfolio_aligned, benchmark_aligned)
            alpha = self._calculate_alpha(portfolio_aligned, benchmark_aligned, beta)
            
            # Calculate correlation
            correlation = self._calculate_correlation(portfolio_aligned, benchmark_aligned)
            
            # Calculate rolling metrics
            rolling_alpha = self._calculate_rolling_alpha(portfolio_aligned, benchmark_aligned)
            rolling_beta = self._calculate_rolling_beta(portfolio_aligned, benchmark_aligned)
            rolling_correlation = self._calculate_rolling_correlation(portfolio_aligned, benchmark_aligned)
            
            return BenchmarkComparison(
                benchmark_name=benchmark_name,
                benchmark_return=benchmark_return,
                portfolio_return=portfolio_return,
                excess_return=excess_return,
                tracking_error=tracking_error,
                information_ratio=information_ratio,
                beta=beta,
                alpha=alpha,
                correlation=correlation,
                rolling_alpha=rolling_alpha,
                rolling_beta=rolling_beta,
                rolling_correlation=rolling_correlation,
                period_start=portfolio_data[0]['date'] if portfolio_data else date.today(),
                period_end=portfolio_data[-1]['date'] if portfolio_data else date.today()
            )
            
        except Exception as e:
            logger.error(f"Failed to compare to benchmark: {e}")
            return self._get_default_benchmark_comparison(benchmark_name)
    
    async def get_benchmark_analysis(
        self, 
        portfolio: Portfolio, 
        benchmark_name: str,
        period: str = "1Y"
    ) -> Dict[str, Any]:
        """Get comprehensive benchmark analysis."""
        try:
            # Get benchmark comparison
            comparison = await self.compare_to_benchmark(portfolio, benchmark_name, period)
            
            # Get additional analysis
            relative_performance = self._analyze_relative_performance(comparison)
            risk_adjusted_metrics = self._analyze_risk_adjusted_metrics(comparison)
            consistency_metrics = self._analyze_consistency_metrics(comparison)
            
            return {
                'comparison': comparison,
                'relative_performance': relative_performance,
                'risk_adjusted_metrics': risk_adjusted_metrics,
                'consistency_metrics': consistency_metrics,
                'summary': self._generate_benchmark_summary(comparison)
            }
            
        except Exception as e:
            logger.error(f"Failed to get benchmark analysis: {e}")
            return {}
    
    async def get_multiple_benchmark_comparison(
        self, 
        portfolio: Portfolio, 
        benchmark_names: List[str],
        period: str = "1Y"
    ) -> Dict[str, BenchmarkComparison]:
        """Compare portfolio to multiple benchmarks."""
        try:
            comparisons = {}
            
            for benchmark_name in benchmark_names:
                comparison = await self.compare_to_benchmark(portfolio, benchmark_name, period)
                comparisons[benchmark_name] = comparison
            
            return comparisons
            
        except Exception as e:
            logger.error(f"Failed to get multiple benchmark comparison: {e}")
            return {}
    
    async def get_benchmark_ranking(
        self, 
        portfolio: Portfolio, 
        period: str = "1Y"
    ) -> List[Dict[str, Any]]:
        """Get benchmark ranking based on various metrics."""
        try:
            rankings = []
            
            for benchmark_name in self.available_benchmarks.keys():
                comparison = await self.compare_to_benchmark(portfolio, benchmark_name, period)
                
                ranking = {
                    'benchmark_name': benchmark_name,
                    'benchmark_description': self.available_benchmarks[benchmark_name],
                    'excess_return': comparison.excess_return,
                    'information_ratio': comparison.information_ratio,
                    'alpha': comparison.alpha,
                    'beta': comparison.beta,
                    'correlation': comparison.correlation,
                    'tracking_error': comparison.tracking_error
                }
                
                rankings.append(ranking)
            
            # Sort by information ratio (descending)
            rankings.sort(key=lambda x: x['information_ratio'], reverse=True)
            
            return rankings
            
        except Exception as e:
            logger.error(f"Failed to get benchmark ranking: {e}")
            return []
    
    async def suggest_optimal_benchmark(
        self, 
        portfolio: Portfolio, 
        period: str = "1Y"
    ) -> Dict[str, Any]:
        """Suggest optimal benchmark based on portfolio characteristics."""
        try:
            # Get portfolio characteristics
            portfolio_characteristics = self._analyze_portfolio_characteristics(portfolio)
            
            # Get benchmark rankings
            rankings = await self.get_benchmark_ranking(portfolio, period)
            
            # Score benchmarks based on portfolio characteristics
            scored_benchmarks = []
            
            for ranking in rankings:
                score = self._calculate_benchmark_score(ranking, portfolio_characteristics)
                scored_benchmarks.append({
                    **ranking,
                    'score': score
                })
            
            # Sort by score
            scored_benchmarks.sort(key=lambda x: x['score'], reverse=True)
            
            return {
                'recommended_benchmark': scored_benchmarks[0] if scored_benchmarks else None,
                'all_scores': scored_benchmarks,
                'portfolio_characteristics': portfolio_characteristics,
                'reasoning': self._generate_benchmark_recommendation_reasoning(
                    scored_benchmarks[0] if scored_benchmarks else None,
                    portfolio_characteristics
                )
            }
            
        except Exception as e:
            logger.error(f"Failed to suggest optimal benchmark: {e}")
            return {}
    
    def _calculate_returns(self, data: List[Dict[str, Any]]) -> pd.Series:
        """Calculate returns from historical data."""
        try:
            values = [d['value'] for d in data]
            returns = pd.Series(values).pct_change().dropna()
            return returns
        except Exception as e:
            logger.error(f"Failed to calculate returns: {e}")
            return pd.Series()
    
    def _align_data(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> Optional[Dict[str, pd.Series]]:
        """Align portfolio and benchmark data."""
        try:
            # Find common dates
            common_dates = portfolio_returns.index.intersection(benchmark_returns.index)
            
            if len(common_dates) == 0:
                return None
            
            return {
                'portfolio': portfolio_returns.loc[common_dates],
                'benchmark': benchmark_returns.loc[common_dates]
            }
        except Exception as e:
            logger.error(f"Failed to align data: {e}")
            return None
    
    def _calculate_total_return(self, returns: pd.Series) -> float:
        """Calculate total return."""
        try:
            return float((1 + returns).prod() - 1) * 100
        except Exception as e:
            logger.error(f"Failed to calculate total return: {e}")
            return 0.0
    
    def _calculate_tracking_error(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """Calculate tracking error."""
        try:
            excess_returns = portfolio_returns - benchmark_returns
            return float(excess_returns.std() * np.sqrt(252)) * 100
        except Exception as e:
            logger.error(f"Failed to calculate tracking error: {e}")
            return 0.0
    
    def _calculate_information_ratio(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """Calculate information ratio."""
        try:
            excess_returns = portfolio_returns - benchmark_returns
            tracking_error = excess_returns.std()
            
            if tracking_error == 0:
                return 0.0
            
            return float(excess_returns.mean() / tracking_error * np.sqrt(252))
        except Exception as e:
            logger.error(f"Failed to calculate information ratio: {e}")
            return 0.0
    
    def _calculate_beta(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """Calculate beta."""
        try:
            covariance = np.cov(portfolio_returns, benchmark_returns)[0, 1]
            benchmark_variance = np.var(benchmark_returns)
            
            if benchmark_variance == 0:
                return 1.0
            
            return float(covariance / benchmark_variance)
        except Exception as e:
            logger.error(f"Failed to calculate beta: {e}")
            return 1.0
    
    def _calculate_alpha(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series, beta: float) -> float:
        """Calculate alpha."""
        try:
            portfolio_mean = portfolio_returns.mean()
            benchmark_mean = benchmark_returns.mean()
            
            # Alpha = Portfolio Return - (Risk-free Rate + Beta * (Benchmark Return - Risk-free Rate))
            # Simplified: Alpha = Portfolio Return - Beta * Benchmark Return
            alpha = portfolio_mean - beta * benchmark_mean
            
            return float(alpha * 252) * 100  # Annualized
        except Exception as e:
            logger.error(f"Failed to calculate alpha: {e}")
            return 0.0
    
    def _calculate_correlation(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """Calculate correlation."""
        try:
            return float(portfolio_returns.corr(benchmark_returns))
        except Exception as e:
            logger.error(f"Failed to calculate correlation: {e}")
            return 0.0
    
    def _calculate_rolling_alpha(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series, window: int = 30) -> List[float]:
        """Calculate rolling alpha."""
        try:
            rolling_alpha = []
            
            for i in range(window, len(portfolio_returns)):
                window_portfolio = portfolio_returns.iloc[i-window:i]
                window_benchmark = benchmark_returns.iloc[i-window:i]
                
                beta = self._calculate_beta(window_portfolio, window_benchmark)
                alpha = self._calculate_alpha(window_portfolio, window_benchmark, beta)
                
                rolling_alpha.append(alpha)
            
            return rolling_alpha
        except Exception as e:
            logger.error(f"Failed to calculate rolling alpha: {e}")
            return []
    
    def _calculate_rolling_beta(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series, window: int = 30) -> List[float]:
        """Calculate rolling beta."""
        try:
            rolling_beta = []
            
            for i in range(window, len(portfolio_returns)):
                window_portfolio = portfolio_returns.iloc[i-window:i]
                window_benchmark = benchmark_returns.iloc[i-window:i]
                
                beta = self._calculate_beta(window_portfolio, window_benchmark)
                rolling_beta.append(beta)
            
            return rolling_beta
        except Exception as e:
            logger.error(f"Failed to calculate rolling beta: {e}")
            return []
    
    def _calculate_rolling_correlation(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series, window: int = 30) -> List[float]:
        """Calculate rolling correlation."""
        try:
            rolling_correlation = []
            
            for i in range(window, len(portfolio_returns)):
                window_portfolio = portfolio_returns.iloc[i-window:i]
                window_benchmark = benchmark_returns.iloc[i-window:i]
                
                correlation = self._calculate_correlation(window_portfolio, window_benchmark)
                rolling_correlation.append(correlation)
            
            return rolling_correlation
        except Exception as e:
            logger.error(f"Failed to calculate rolling correlation: {e}")
            return []
    
    def _analyze_relative_performance(self, comparison: BenchmarkComparison) -> Dict[str, Any]:
        """Analyze relative performance."""
        return {
            'outperformed': comparison.excess_return > 0,
            'excess_return': comparison.excess_return,
            'outperformance_consistency': 'High' if comparison.information_ratio > 0.5 else 'Low',
            'risk_adjusted_outperformance': comparison.information_ratio
        }
    
    def _analyze_risk_adjusted_metrics(self, comparison: BenchmarkComparison) -> Dict[str, Any]:
        """Analyze risk-adjusted metrics."""
        return {
            'information_ratio': comparison.information_ratio,
            'tracking_error': comparison.tracking_error,
            'beta': comparison.beta,
            'alpha': comparison.alpha,
            'correlation': comparison.correlation
        }
    
    def _analyze_consistency_metrics(self, comparison: BenchmarkComparison) -> Dict[str, Any]:
        """Analyze consistency metrics."""
        return {
            'rolling_alpha_volatility': np.std(comparison.rolling_alpha) if comparison.rolling_alpha else 0,
            'rolling_beta_volatility': np.std(comparison.rolling_beta) if comparison.rolling_beta else 0,
            'correlation_stability': np.std(comparison.rolling_correlation) if comparison.rolling_correlation else 0
        }
    
    def _generate_benchmark_summary(self, comparison: BenchmarkComparison) -> Dict[str, Any]:
        """Generate benchmark summary."""
        return {
            'performance_summary': f"Portfolio {'outperformed' if comparison.excess_return > 0 else 'underperformed'} benchmark by {abs(comparison.excess_return):.2f}%",
            'risk_summary': f"Tracking error of {comparison.tracking_error:.2f}% with information ratio of {comparison.information_ratio:.2f}",
            'correlation_summary': f"Correlation with benchmark: {comparison.correlation:.2f}",
            'beta_summary': f"Beta: {comparison.beta:.2f}, Alpha: {comparison.alpha:.2f}%"
        }
    
    def _analyze_portfolio_characteristics(self, portfolio: Portfolio) -> Dict[str, Any]:
        """Analyze portfolio characteristics."""
        return {
            'asset_allocation': portfolio.get_asset_allocation(),
            'sector_allocation': portfolio.get_sector_allocation(),
            'num_positions': len(portfolio.get_active_positions()),
            'concentration': max(pos.weight_percentage for pos in portfolio.get_active_positions()) if portfolio.get_active_positions() else 0
        }
    
    def _calculate_benchmark_score(self, ranking: Dict[str, Any], characteristics: Dict[str, Any]) -> float:
        """Calculate benchmark score based on portfolio characteristics."""
        score = 0.0
        
        # Information ratio weight
        score += ranking['information_ratio'] * 0.3
        
        # Alpha weight
        score += ranking['alpha'] * 0.2
        
        # Correlation weight (prefer moderate correlation)
        correlation_score = 1 - abs(ranking['correlation'] - 0.7)  # Prefer correlation around 0.7
        score += correlation_score * 0.2
        
        # Beta weight (prefer beta close to 1)
        beta_score = 1 - abs(ranking['beta'] - 1.0)
        score += beta_score * 0.2
        
        # Tracking error weight (prefer lower tracking error)
        tracking_error_score = max(0, 1 - ranking['tracking_error'] / 10)  # Normalize
        score += tracking_error_score * 0.1
        
        return score
    
    def _generate_benchmark_recommendation_reasoning(self, recommended: Optional[Dict[str, Any]], characteristics: Dict[str, Any]) -> str:
        """Generate reasoning for benchmark recommendation."""
        if not recommended:
            return "No suitable benchmark found."
        
        reasoning = f"Recommended {recommended['benchmark_name']} because: "
        reasoning += f"Information ratio of {recommended['information_ratio']:.2f}, "
        reasoning += f"Alpha of {recommended['alpha']:.2f}%, "
        reasoning += f"Beta of {recommended['beta']:.2f}, "
        reasoning += f"and correlation of {recommended['correlation']:.2f}."
        
        return reasoning
    
    def _get_default_benchmark_comparison(self, benchmark_name: str) -> BenchmarkComparison:
        """Get default benchmark comparison."""
        return BenchmarkComparison(
            benchmark_name=benchmark_name,
            benchmark_return=0.0,
            portfolio_return=0.0,
            excess_return=0.0,
            tracking_error=0.0,
            information_ratio=0.0,
            beta=1.0,
            alpha=0.0,
            correlation=0.0,
            rolling_alpha=[],
            rolling_beta=[],
            rolling_correlation=[],
            period_start=date.today(),
            period_end=date.today()
        )
    
    # Placeholder methods for database operations
    async def _get_portfolio_historical_data(self, portfolio_id: str, period: str) -> List[Dict[str, Any]]:
        """Get historical portfolio data."""
        return []
    
    async def _get_benchmark_historical_data(self, benchmark_name: str, period: str) -> List[Dict[str, Any]]:
        """Get historical benchmark data."""
        return []
