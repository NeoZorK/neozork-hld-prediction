"""
Performance Analyzer - Portfolio Performance Analysis

This module provides comprehensive portfolio performance analysis including
return calculations, risk metrics, and performance attribution.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, date, timedelta
from decimal import Decimal
import numpy as np
import pandas as pd

from ..models.portfolio_models import Portfolio, Position
from ..models.performance_models import PerformanceMetrics, RiskMetrics

logger = logging.getLogger(__name__)


class PerformanceAnalyzer:
    """Portfolio performance analysis functionality."""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        
    async def calculate_performance_metrics(
        self, 
        portfolio: Portfolio, 
        period: str = "1Y"
    ) -> PerformanceMetrics:
        """Calculate comprehensive performance metrics."""
        try:
            # Get historical data for the period
            historical_data = await self._get_historical_data(portfolio.id, period)
            
            if not historical_data:
                return self._get_default_metrics()
            
            # Calculate returns
            returns = self._calculate_returns(historical_data)
            
            # Calculate performance metrics
            total_return = self._calculate_total_return(returns)
            annualized_return = self._calculate_annualized_return(returns, period)
            volatility = self._calculate_volatility(returns)
            sharpe_ratio = self._calculate_sharpe_ratio(returns)
            sortino_ratio = self._calculate_sortino_ratio(returns)
            calmar_ratio = self._calculate_calmar_ratio(returns, total_return)
            
            # Calculate drawdown metrics
            max_drawdown = self._calculate_max_drawdown(returns)
            current_drawdown = self._calculate_current_drawdown(returns)
            drawdown_duration = self._calculate_drawdown_duration(returns)
            
            # Calculate other metrics
            win_rate = self._calculate_win_rate(returns)
            profit_factor = self._calculate_profit_factor(returns)
            
            # Calculate alpha and beta (simplified)
            alpha, beta = self._calculate_alpha_beta(returns)
            
            # Calculate tracking error
            tracking_error = self._calculate_tracking_error(returns)
            information_ratio = self._calculate_information_ratio(returns)
            
            return PerformanceMetrics(
                total_return=total_return,
                annualized_return=annualized_return,
                monthly_return=self._calculate_monthly_return(returns),
                daily_return=self._calculate_daily_return(returns),
                sharpe_ratio=sharpe_ratio,
                sortino_ratio=sortino_ratio,
                calmar_ratio=calmar_ratio,
                information_ratio=information_ratio,
                volatility=volatility,
                annualized_volatility=volatility * np.sqrt(252),
                tracking_error=tracking_error,
                max_drawdown=max_drawdown,
                current_drawdown=current_drawdown,
                drawdown_duration=drawdown_duration,
                win_rate=win_rate,
                profit_factor=profit_factor,
                alpha=alpha,
                beta=beta,
                period_start=historical_data[0]['date'] if historical_data else date.today(),
                period_end=historical_data[-1]['date'] if historical_data else date.today()
            )
            
        except Exception as e:
            logger.error(f"Failed to calculate performance metrics: {e}")
            return self._get_default_metrics()
    
    async def calculate_risk_metrics(
        self, 
        portfolio: Portfolio, 
        period: str = "1Y"
    ) -> RiskMetrics:
        """Calculate comprehensive risk metrics."""
        try:
            # Get historical data
            historical_data = await self._get_historical_data(portfolio.id, period)
            
            if not historical_data:
                return self._get_default_risk_metrics()
            
            returns = self._calculate_returns(historical_data)
            
            # Calculate VaR and CVaR
            var_95, var_99 = self._calculate_var(returns)
            cvar_95, cvar_99 = self._calculate_cvar(returns)
            
            # Calculate risk ratios
            sharpe_ratio = self._calculate_sharpe_ratio(returns)
            sortino_ratio = self._calculate_sortino_ratio(returns)
            calmar_ratio = self._calculate_calmar_ratio(returns, self._calculate_total_return(returns))
            
            # Calculate volatility and beta
            volatility = self._calculate_volatility(returns)
            beta = self._calculate_beta(returns)
            correlation_to_market = self._calculate_correlation_to_market(returns)
            
            # Calculate concentration risk
            herfindahl_index = self._calculate_herfindahl_index(portfolio)
            max_position_weight = self._calculate_max_position_weight(portfolio)
            sector_concentration = self._calculate_sector_concentration(portfolio)
            
            # Stress test results
            stress_test_results = await self._run_stress_tests(portfolio, returns)
            
            # Risk limits and breaches
            risk_limits = portfolio.risk_limits
            limit_breaches = await self._check_risk_limits(portfolio)
            
            return RiskMetrics(
                var_95=var_95,
                var_99=var_99,
                cvar_95=cvar_95,
                cvar_99=cvar_99,
                sharpe_ratio=sharpe_ratio,
                sortino_ratio=sortino_ratio,
                calmar_ratio=calmar_ratio,
                volatility=volatility,
                beta=beta,
                correlation_to_market=correlation_to_market,
                herfindahl_index=herfindahl_index,
                max_position_weight=max_position_weight,
                sector_concentration=sector_concentration,
                stress_test_results=stress_test_results,
                risk_limits=risk_limits,
                limit_breaches=limit_breaches
            )
            
        except Exception as e:
            logger.error(f"Failed to calculate risk metrics: {e}")
            return self._get_default_risk_metrics()
    
    async def get_performance_attribution(
        self, 
        portfolio: Portfolio, 
        period: str = "1Y"
    ) -> Dict[str, Any]:
        """Get performance attribution analysis."""
        try:
            # Get historical data
            historical_data = await self._get_historical_data(portfolio.id, period)
            
            if not historical_data:
                return {}
            
            # Calculate position-level attribution
            position_attribution = self._calculate_position_attribution(portfolio, historical_data)
            
            # Calculate sector attribution
            sector_attribution = self._calculate_sector_attribution(portfolio, historical_data)
            
            # Calculate asset class attribution
            asset_class_attribution = self._calculate_asset_class_attribution(portfolio, historical_data)
            
            # Get top and bottom contributors
            top_contributors = self._get_top_contributors(position_attribution)
            bottom_contributors = self._get_bottom_contributors(position_attribution)
            
            return {
                'position_attribution': position_attribution,
                'sector_attribution': sector_attribution,
                'asset_class_attribution': asset_class_attribution,
                'top_contributors': top_contributors,
                'bottom_contributors': bottom_contributors,
                'total_attribution': sum(pos['contribution'] for pos in position_attribution.values())
            }
            
        except Exception as e:
            logger.error(f"Failed to get performance attribution: {e}")
            return {}
    
    async def get_rolling_metrics(
        self, 
        portfolio: Portfolio, 
        window: int = 30,
        period: str = "1Y"
    ) -> Dict[str, List[float]]:
        """Get rolling performance metrics."""
        try:
            # Get historical data
            historical_data = await self._get_historical_data(portfolio.id, period)
            
            if not historical_data:
                return {}
            
            returns = self._calculate_returns(historical_data)
            
            # Calculate rolling metrics
            rolling_returns = returns.rolling(window=window).mean()
            rolling_volatility = returns.rolling(window=window).std()
            rolling_sharpe = rolling_returns / rolling_volatility
            
            return {
                'rolling_returns': rolling_returns.tolist(),
                'rolling_volatility': rolling_volatility.tolist(),
                'rolling_sharpe': rolling_sharpe.tolist(),
                'dates': [d['date'] for d in historical_data[window-1:]]
            }
            
        except Exception as e:
            logger.error(f"Failed to get rolling metrics: {e}")
            return {}
    
    # Helper methods for calculations
    def _calculate_returns(self, historical_data: List[Dict[str, Any]]) -> pd.Series:
        """Calculate returns from historical data."""
        try:
            values = [d['total_value'] for d in historical_data]
            returns = pd.Series(values).pct_change().dropna()
            return returns
        except Exception as e:
            logger.error(f"Failed to calculate returns: {e}")
            return pd.Series()
    
    def _calculate_total_return(self, returns: pd.Series) -> float:
        """Calculate total return."""
        try:
            return float((1 + returns).prod() - 1) * 100
        except Exception as e:
            logger.error(f"Failed to calculate total return: {e}")
            return 0.0
    
    def _calculate_annualized_return(self, returns: pd.Series, period: str) -> float:
        """Calculate annualized return."""
        try:
            total_return = self._calculate_total_return(returns)
            periods_per_year = self._get_periods_per_year(period)
            return float((1 + total_return/100) ** (periods_per_year / len(returns)) - 1) * 100
        except Exception as e:
            logger.error(f"Failed to calculate annualized return: {e}")
            return 0.0
    
    def _calculate_volatility(self, returns: pd.Series) -> float:
        """Calculate volatility."""
        try:
            return float(returns.std() * np.sqrt(252)) * 100
        except Exception as e:
            logger.error(f"Failed to calculate volatility: {e}")
            return 0.0
    
    def _calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio."""
        try:
            excess_returns = returns - risk_free_rate/252
            return float(excess_returns.mean() / returns.std() * np.sqrt(252))
        except Exception as e:
            logger.error(f"Failed to calculate Sharpe ratio: {e}")
            return 0.0
    
    def _calculate_sortino_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sortino ratio."""
        try:
            excess_returns = returns - risk_free_rate/252
            downside_returns = returns[returns < 0]
            downside_deviation = downside_returns.std()
            
            if downside_deviation == 0:
                return 0.0
            
            return float(excess_returns.mean() / downside_deviation * np.sqrt(252))
        except Exception as e:
            logger.error(f"Failed to calculate Sortino ratio: {e}")
            return 0.0
    
    def _calculate_calmar_ratio(self, returns: pd.Series, total_return: float) -> float:
        """Calculate Calmar ratio."""
        try:
            max_drawdown = self._calculate_max_drawdown(returns)
            if max_drawdown == 0:
                return 0.0
            
            return float(total_return / 100 / abs(max_drawdown / 100))
        except Exception as e:
            logger.error(f"Failed to calculate Calmar ratio: {e}")
            return 0.0
    
    def _calculate_max_drawdown(self, returns: pd.Series) -> float:
        """Calculate maximum drawdown."""
        try:
            cumulative = (1 + returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            return float(drawdown.min()) * 100
        except Exception as e:
            logger.error(f"Failed to calculate max drawdown: {e}")
            return 0.0
    
    def _calculate_current_drawdown(self, returns: pd.Series) -> float:
        """Calculate current drawdown."""
        try:
            cumulative = (1 + returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            return float(drawdown.iloc[-1]) * 100
        except Exception as e:
            logger.error(f"Failed to calculate current drawdown: {e}")
            return 0.0
    
    def _calculate_drawdown_duration(self, returns: pd.Series) -> int:
        """Calculate drawdown duration in days."""
        try:
            cumulative = (1 + returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            
            # Find current drawdown period
            in_drawdown = drawdown < 0
            current_duration = 0
            
            for i in range(len(in_drawdown) - 1, -1, -1):
                if in_drawdown.iloc[i]:
                    current_duration += 1
                else:
                    break
            
            return current_duration
        except Exception as e:
            logger.error(f"Failed to calculate drawdown duration: {e}")
            return 0
    
    def _calculate_win_rate(self, returns: pd.Series) -> float:
        """Calculate win rate."""
        try:
            positive_returns = returns[returns > 0]
            return float(len(positive_returns) / len(returns)) * 100
        except Exception as e:
            logger.error(f"Failed to calculate win rate: {e}")
            return 0.0
    
    def _calculate_profit_factor(self, returns: pd.Series) -> float:
        """Calculate profit factor."""
        try:
            positive_returns = returns[returns > 0].sum()
            negative_returns = abs(returns[returns < 0].sum())
            
            if negative_returns == 0:
                return float('inf') if positive_returns > 0 else 0.0
            
            return float(positive_returns / negative_returns)
        except Exception as e:
            logger.error(f"Failed to calculate profit factor: {e}")
            return 0.0
    
    def _calculate_alpha_beta(self, returns: pd.Series) -> Tuple[float, float]:
        """Calculate alpha and beta (simplified)."""
        try:
            # This would require benchmark data
            # For now, return default values
            return 0.0, 1.0
        except Exception as e:
            logger.error(f"Failed to calculate alpha/beta: {e}")
            return 0.0, 1.0
    
    def _calculate_tracking_error(self, returns: pd.Series) -> float:
        """Calculate tracking error."""
        try:
            # This would require benchmark data
            return 0.0
        except Exception as e:
            logger.error(f"Failed to calculate tracking error: {e}")
            return 0.0
    
    def _calculate_information_ratio(self, returns: pd.Series) -> float:
        """Calculate information ratio."""
        try:
            # This would require benchmark data
            return 0.0
        except Exception as e:
            logger.error(f"Failed to calculate information ratio: {e}")
            return 0.0
    
    def _calculate_var(self, returns: pd.Series) -> Tuple[float, float]:
        """Calculate Value at Risk."""
        try:
            var_95 = float(np.percentile(returns, 5)) * 100
            var_99 = float(np.percentile(returns, 1)) * 100
            return var_95, var_99
        except Exception as e:
            logger.error(f"Failed to calculate VaR: {e}")
            return 0.0, 0.0
    
    def _calculate_cvar(self, returns: pd.Series) -> Tuple[float, float]:
        """Calculate Conditional Value at Risk."""
        try:
            var_95_threshold = np.percentile(returns, 5)
            var_99_threshold = np.percentile(returns, 1)
            
            cvar_95 = float(returns[returns <= var_95_threshold].mean()) * 100
            cvar_99 = float(returns[returns <= var_99_threshold].mean()) * 100
            
            return cvar_95, cvar_99
        except Exception as e:
            logger.error(f"Failed to calculate CVaR: {e}")
            return 0.0, 0.0
    
    def _get_periods_per_year(self, period: str) -> int:
        """Get number of periods per year based on period string."""
        period_map = {
            "1D": 252,
            "1W": 52,
            "1M": 12,
            "3M": 4,
            "6M": 2,
            "1Y": 1,
            "2Y": 0.5,
            "5Y": 0.2
        }
        return period_map.get(period, 252)
    
    def _get_default_metrics(self) -> PerformanceMetrics:
        """Get default performance metrics."""
        return PerformanceMetrics(
            total_return=0.0,
            annualized_return=0.0,
            monthly_return=0.0,
            daily_return=0.0,
            sharpe_ratio=0.0,
            sortino_ratio=0.0,
            calmar_ratio=0.0,
            information_ratio=0.0,
            volatility=0.0,
            annualized_volatility=0.0,
            tracking_error=0.0,
            max_drawdown=0.0,
            current_drawdown=0.0,
            drawdown_duration=0,
            win_rate=0.0,
            profit_factor=0.0,
            alpha=0.0,
            beta=1.0,
            period_start=date.today(),
            period_end=date.today()
        )
    
    def _get_default_risk_metrics(self) -> RiskMetrics:
        """Get default risk metrics."""
        return RiskMetrics(
            var_95=0.0,
            var_99=0.0,
            cvar_95=0.0,
            cvar_99=0.0,
            sharpe_ratio=0.0,
            sortino_ratio=0.0,
            calmar_ratio=0.0,
            volatility=0.0,
            beta=1.0,
            correlation_to_market=0.0,
            herfindahl_index=0.0,
            max_position_weight=0.0,
            sector_concentration={},
            stress_test_results={},
            risk_limits={},
            limit_breaches=[]
        )
    
    # Placeholder methods for database operations
    async def _get_historical_data(self, portfolio_id: str, period: str) -> List[Dict[str, Any]]:
        """Get historical portfolio data."""
        # This would query the database for historical portfolio values
        return []
    
    def _calculate_herfindahl_index(self, portfolio: Portfolio) -> float:
        """Calculate Herfindahl-Hirschman Index."""
        weights = [pos.weight_percentage for pos in portfolio.get_active_positions()]
        return sum(w**2 for w in weights) / 10000  # Convert to 0-1 scale
    
    def _calculate_max_position_weight(self, portfolio: Portfolio) -> float:
        """Calculate maximum position weight."""
        weights = [pos.weight_percentage for pos in portfolio.get_active_positions()]
        return max(weights) if weights else 0.0
    
    def _calculate_sector_concentration(self, portfolio: Portfolio) -> Dict[str, float]:
        """Calculate sector concentration."""
        return portfolio.get_sector_allocation()
    
    async def _run_stress_tests(self, portfolio: Portfolio, returns: pd.Series) -> Dict[str, Any]:
        """Run stress tests."""
        return {}
    
    async def _check_risk_limits(self, portfolio: Portfolio) -> List[Dict[str, Any]]:
        """Check risk limit breaches."""
        return []
    
    def _calculate_position_attribution(self, portfolio: Portfolio, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate position-level attribution."""
        return {}
    
    def _calculate_sector_attribution(self, portfolio: Portfolio, historical_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate sector attribution."""
        return {}
    
    def _calculate_asset_class_attribution(self, portfolio: Portfolio, historical_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate asset class attribution."""
        return {}
    
    def _get_top_contributors(self, attribution: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get top contributors."""
        return []
    
    def _get_bottom_contributors(self, attribution: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get bottom contributors."""
        return []
    
    def _calculate_monthly_return(self, returns: pd.Series) -> float:
        """Calculate monthly return."""
        return 0.0
    
    def _calculate_daily_return(self, returns: pd.Series) -> float:
        """Calculate daily return."""
        return 0.0
    
    def _calculate_beta(self, returns: pd.Series) -> float:
        """Calculate beta."""
        return 1.0
    
    def _calculate_correlation_to_market(self, returns: pd.Series) -> float:
        """Calculate correlation to market."""
        return 0.0
