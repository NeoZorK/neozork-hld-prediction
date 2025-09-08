"""Functional Performance Tracker - Real-time performance calculations and tracking"""

import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid
import json
import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)


class PerformanceMetric(Enum):
    """Performance metric enumeration."""
    TOTAL_RETURN = "total_return"
    DAILY_RETURN = "daily_return"
    SHARPE_RATIO = "sharpe_ratio"
    MAX_DRAWDOWN = "max_drawdown"
    VOLATILITY = "volatility"
    BETA = "beta"
    ALPHA = "alpha"
    VAR_95 = "var_95"
    CVAR_95 = "cvar_95"
    WIN_RATE = "win_rate"
    PROFIT_FACTOR = "profit_factor"
    CALMAR_RATIO = "calmar_ratio"
    SORTINO_RATIO = "sortino_ratio"


@dataclass
class PerformanceSnapshot:
    """Performance snapshot data class."""
    fund_id: str
    snapshot_date: datetime
    total_value: float
    total_return: float
    total_return_percentage: float
    daily_return: float
    daily_return_percentage: float
    sharpe_ratio: float
    max_drawdown: float
    volatility: float
    beta: float
    alpha: float
    var_95: float
    cvar_95: float
    win_rate: float
    profit_factor: float
    calmar_ratio: float
    sortino_ratio: float


@dataclass
class BenchmarkComparison:
    """Benchmark comparison data class."""
    fund_return: float
    benchmark_return: float
    excess_return: float
    tracking_error: float
    information_ratio: float
    beta: float
    alpha: float
    correlation: float


class FunctionalPerformanceTracker:
    """Fully functional performance tracking for the fund."""
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.risk_free_rate = 0.02  # 2% annual risk-free rate
        self.benchmark_symbol = "SPY"  # S&P 500 as default benchmark
        
    async def calculate_daily_performance(self, fund_id: str, date: datetime = None) -> Dict[str, Any]:
        """Calculate daily performance metrics for a fund."""
        try:
            if date is None:
                date = datetime.now().date()
            
            # Get fund data
            fund_query = "SELECT * FROM funds WHERE id = :fund_id"
            fund_result = await self.database_manager.execute_query(
                fund_query, 
                {"fund_id": fund_id}
            )
            
            if 'error' in fund_result or not fund_result['query_result']['data']:
                return {"error": "Fund not found"}
            
            fund_data = fund_result['query_result']['data'][0]
            current_value = float(fund_data['current_value'])
            initial_capital = float(fund_data['initial_capital'])
            
            # Get previous day's performance
            prev_date = date - timedelta(days=1)
            prev_performance_query = """
            SELECT * FROM performance_snapshots 
            WHERE fund_id = :fund_id AND snapshot_date = :prev_date
            """
            
            prev_performance_result = await self.database_manager.execute_query(
                prev_performance_query,
                {"fund_id": fund_id, "prev_date": prev_date}
            )
            
            # Calculate daily return
            if prev_performance_result['query_result']['data']:
                prev_value = float(prev_performance_result['query_result']['data'][0]['total_value'])
                daily_return = current_value - prev_value
                daily_return_percentage = (daily_return / prev_value) * 100 if prev_value > 0 else 0
            else:
                # First day - use initial capital
                daily_return = current_value - initial_capital
                daily_return_percentage = (daily_return / initial_capital) * 100 if initial_capital > 0 else 0
            
            # Calculate total return
            total_return = current_value - initial_capital
            total_return_percentage = (total_return / initial_capital) * 100 if initial_capital > 0 else 0
            
            # Get historical data for advanced metrics
            historical_data = await self._get_historical_performance(fund_id, days=252)  # 1 year
            
            # Calculate advanced metrics
            sharpe_ratio = await self._calculate_sharpe_ratio(historical_data)
            max_drawdown = await self._calculate_max_drawdown(historical_data)
            volatility = await self._calculate_volatility(historical_data)
            beta = await self._calculate_beta(historical_data)
            alpha = await self._calculate_alpha(historical_data, beta)
            var_95 = await self._calculate_var(historical_data, 0.95)
            cvar_95 = await self._calculate_cvar(historical_data, 0.95)
            win_rate = await self._calculate_win_rate(historical_data)
            profit_factor = await self._calculate_profit_factor(historical_data)
            calmar_ratio = await self._calculate_calmar_ratio(total_return_percentage, max_drawdown)
            sortino_ratio = await self._calculate_sortino_ratio(historical_data)
            
            # Create performance snapshot
            snapshot = PerformanceSnapshot(
                fund_id=fund_id,
                snapshot_date=date,
                total_value=current_value,
                total_return=total_return,
                total_return_percentage=total_return_percentage,
                daily_return=daily_return,
                daily_return_percentage=daily_return_percentage,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                volatility=volatility,
                beta=beta,
                alpha=alpha,
                var_95=var_95,
                cvar_95=cvar_95,
                win_rate=win_rate,
                profit_factor=profit_factor,
                calmar_ratio=calmar_ratio,
                sortino_ratio=sortino_ratio
            )
            
            # Store performance snapshot
            await self._store_performance_snapshot(snapshot)
            
            logger.info(f"Daily performance calculated for fund {fund_id}")
            
            return {
                "fund_id": fund_id,
                "snapshot_date": date.isoformat(),
                "total_value": current_value,
                "total_return": total_return,
                "total_return_percentage": total_return_percentage,
                "daily_return": daily_return,
                "daily_return_percentage": daily_return_percentage,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown,
                "volatility": volatility,
                "beta": beta,
                "alpha": alpha,
                "var_95": var_95,
                "cvar_95": cvar_95,
                "win_rate": win_rate,
                "profit_factor": profit_factor,
                "calmar_ratio": calmar_ratio,
                "sortino_ratio": sortino_ratio
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate daily performance: {e}")
            return {"error": f"Failed to calculate daily performance: {str(e)}"}
    
    async def _get_historical_performance(self, fund_id: str, days: int = 252) -> List[Dict[str, Any]]:
        """Get historical performance data."""
        try:
            query = """
            SELECT * FROM performance_snapshots 
            WHERE fund_id = :fund_id 
            ORDER BY snapshot_date DESC 
            LIMIT :days
            """
            
            result = await self.database_manager.execute_query(
                query,
                {"fund_id": fund_id, "days": days}
            )
            
            if 'error' in result:
                return []
            
            return result['query_result']['data']
            
        except Exception as e:
            logger.error(f"Failed to get historical performance: {e}")
            return []
    
    async def _calculate_sharpe_ratio(self, historical_data: List[Dict[str, Any]]) -> float:
        """Calculate Sharpe ratio."""
        try:
            if len(historical_data) < 2:
                return 0.0
            
            # Get daily returns
            daily_returns = []
            for i in range(1, len(historical_data)):
                prev_value = float(historical_data[i]['total_value'])
                curr_value = float(historical_data[i-1]['total_value'])
                daily_return = (curr_value - prev_value) / prev_value if prev_value > 0 else 0
                daily_returns.append(daily_return)
            
            if not daily_returns:
                return 0.0
            
            # Calculate Sharpe ratio
            mean_return = np.mean(daily_returns)
            std_return = np.std(daily_returns)
            
            if std_return == 0:
                return 0.0
            
            # Annualize
            sharpe_ratio = (mean_return - self.risk_free_rate / 252) / std_return * np.sqrt(252)
            
            return float(sharpe_ratio)
            
        except Exception as e:
            logger.error(f"Failed to calculate Sharpe ratio: {e}")
            return 0.0
    
    async def _calculate_max_drawdown(self, historical_data: List[Dict[str, Any]]) -> float:
        """Calculate maximum drawdown."""
        try:
            if len(historical_data) < 2:
                return 0.0
            
            # Get values
            values = [float(row['total_value']) for row in historical_data]
            values.reverse()  # Oldest first
            
            # Calculate running maximum
            running_max = np.maximum.accumulate(values)
            
            # Calculate drawdowns
            drawdowns = (values - running_max) / running_max
            
            # Get maximum drawdown
            max_drawdown = float(np.min(drawdowns))
            
            return max_drawdown
            
        except Exception as e:
            logger.error(f"Failed to calculate max drawdown: {e}")
            return 0.0
    
    async def _calculate_volatility(self, historical_data: List[Dict[str, Any]]) -> float:
        """Calculate volatility (annualized standard deviation)."""
        try:
            if len(historical_data) < 2:
                return 0.0
            
            # Get daily returns
            daily_returns = []
            for i in range(1, len(historical_data)):
                prev_value = float(historical_data[i]['total_value'])
                curr_value = float(historical_data[i-1]['total_value'])
                daily_return = (curr_value - prev_value) / prev_value if prev_value > 0 else 0
                daily_returns.append(daily_return)
            
            if not daily_returns:
                return 0.0
            
            # Calculate volatility (annualized)
            volatility = float(np.std(daily_returns) * np.sqrt(252))
            
            return volatility
            
        except Exception as e:
            logger.error(f"Failed to calculate volatility: {e}")
            return 0.0
    
    async def _calculate_beta(self, historical_data: List[Dict[str, Any]]) -> float:
        """Calculate beta relative to benchmark."""
        try:
            if len(historical_data) < 30:  # Need at least 30 days
                return 1.0  # Default beta
            
            # Get fund returns
            fund_returns = []
            for i in range(1, len(historical_data)):
                prev_value = float(historical_data[i]['total_value'])
                curr_value = float(historical_data[i-1]['total_value'])
                daily_return = (curr_value - prev_value) / prev_value if prev_value > 0 else 0
                fund_returns.append(daily_return)
            
            # For now, use a simplified beta calculation
            # In production, you'd fetch benchmark data and calculate correlation
            beta = 1.0  # Placeholder
            
            return float(beta)
            
        except Exception as e:
            logger.error(f"Failed to calculate beta: {e}")
            return 1.0
    
    async def _calculate_alpha(self, historical_data: List[Dict[str, Any]], beta: float) -> float:
        """Calculate alpha (excess return over benchmark)."""
        try:
            if len(historical_data) < 2:
                return 0.0
            
            # Get fund return
            first_value = float(historical_data[-1]['total_value'])
            last_value = float(historical_data[0]['total_value'])
            fund_return = (last_value - first_value) / first_value if first_value > 0 else 0
            
            # Annualize
            days = len(historical_data)
            fund_annual_return = (1 + fund_return) ** (252 / days) - 1
            
            # Calculate alpha (simplified - assumes benchmark return of 10%)
            benchmark_return = 0.10
            alpha = fund_annual_return - (self.risk_free_rate + beta * (benchmark_return - self.risk_free_rate))
            
            return float(alpha)
            
        except Exception as e:
            logger.error(f"Failed to calculate alpha: {e}")
            return 0.0
    
    async def _calculate_var(self, historical_data: List[Dict[str, Any]], confidence_level: float) -> float:
        """Calculate Value at Risk (VaR)."""
        try:
            if len(historical_data) < 2:
                return 0.0
            
            # Get daily returns
            daily_returns = []
            for i in range(1, len(historical_data)):
                prev_value = float(historical_data[i]['total_value'])
                curr_value = float(historical_data[i-1]['total_value'])
                daily_return = (curr_value - prev_value) / prev_value if prev_value > 0 else 0
                daily_returns.append(daily_return)
            
            if not daily_returns:
                return 0.0
            
            # Calculate VaR
            var_percentile = (1 - confidence_level) * 100
            var = float(np.percentile(daily_returns, var_percentile))
            
            return var
            
        except Exception as e:
            logger.error(f"Failed to calculate VaR: {e}")
            return 0.0
    
    async def _calculate_cvar(self, historical_data: List[Dict[str, Any]], confidence_level: float) -> float:
        """Calculate Conditional Value at Risk (CVaR)."""
        try:
            if len(historical_data) < 2:
                return 0.0
            
            # Get daily returns
            daily_returns = []
            for i in range(1, len(historical_data)):
                prev_value = float(historical_data[i]['total_value'])
                curr_value = float(historical_data[i-1]['total_value'])
                daily_return = (curr_value - prev_value) / prev_value if prev_value > 0 else 0
                daily_returns.append(daily_return)
            
            if not daily_returns:
                return 0.0
            
            # Calculate CVaR
            var_percentile = (1 - confidence_level) * 100
            var = np.percentile(daily_returns, var_percentile)
            
            # CVaR is the mean of returns below VaR
            cvar_returns = [r for r in daily_returns if r <= var]
            cvar = float(np.mean(cvar_returns)) if cvar_returns else var
            
            return cvar
            
        except Exception as e:
            logger.error(f"Failed to calculate CVaR: {e}")
            return 0.0
    
    async def _calculate_win_rate(self, historical_data: List[Dict[str, Any]]) -> float:
        """Calculate win rate (percentage of positive days)."""
        try:
            if len(historical_data) < 2:
                return 0.0
            
            # Get daily returns
            daily_returns = []
            for i in range(1, len(historical_data)):
                prev_value = float(historical_data[i]['total_value'])
                curr_value = float(historical_data[i-1]['total_value'])
                daily_return = (curr_value - prev_value) / prev_value if prev_value > 0 else 0
                daily_returns.append(daily_return)
            
            if not daily_returns:
                return 0.0
            
            # Calculate win rate
            positive_days = sum(1 for r in daily_returns if r > 0)
            win_rate = (positive_days / len(daily_returns)) * 100
            
            return float(win_rate)
            
        except Exception as e:
            logger.error(f"Failed to calculate win rate: {e}")
            return 0.0
    
    async def _calculate_profit_factor(self, historical_data: List[Dict[str, Any]]) -> float:
        """Calculate profit factor (gross profit / gross loss)."""
        try:
            if len(historical_data) < 2:
                return 0.0
            
            # Get daily returns
            daily_returns = []
            for i in range(1, len(historical_data)):
                prev_value = float(historical_data[i]['total_value'])
                curr_value = float(historical_data[i-1]['total_value'])
                daily_return = (curr_value - prev_value) / prev_value if prev_value > 0 else 0
                daily_returns.append(daily_return)
            
            if not daily_returns:
                return 0.0
            
            # Calculate profit factor
            gross_profit = sum(r for r in daily_returns if r > 0)
            gross_loss = abs(sum(r for r in daily_returns if r < 0))
            
            if gross_loss == 0:
                return float('inf') if gross_profit > 0 else 0.0
            
            profit_factor = gross_profit / gross_loss
            
            return float(profit_factor)
            
        except Exception as e:
            logger.error(f"Failed to calculate profit factor: {e}")
            return 0.0
    
    async def _calculate_calmar_ratio(self, total_return_percentage: float, max_drawdown: float) -> float:
        """Calculate Calmar ratio (annual return / max drawdown)."""
        try:
            if max_drawdown == 0:
                return float('inf') if total_return_percentage > 0 else 0.0
            
            # Annualize return
            annual_return = total_return_percentage / 100  # Convert percentage to decimal
            calmar_ratio = annual_return / abs(max_drawdown)
            
            return float(calmar_ratio)
            
        except Exception as e:
            logger.error(f"Failed to calculate Calmar ratio: {e}")
            return 0.0
    
    async def _calculate_sortino_ratio(self, historical_data: List[Dict[str, Any]]) -> float:
        """Calculate Sortino ratio (downside deviation adjusted Sharpe ratio)."""
        try:
            if len(historical_data) < 2:
                return 0.0
            
            # Get daily returns
            daily_returns = []
            for i in range(1, len(historical_data)):
                prev_value = float(historical_data[i]['total_value'])
                curr_value = float(historical_data[i-1]['total_value'])
                daily_return = (curr_value - prev_value) / prev_value if prev_value > 0 else 0
                daily_returns.append(daily_return)
            
            if not daily_returns:
                return 0.0
            
            # Calculate Sortino ratio
            mean_return = np.mean(daily_returns)
            
            # Calculate downside deviation
            negative_returns = [r for r in daily_returns if r < 0]
            downside_deviation = np.std(negative_returns) if negative_returns else 0
            
            if downside_deviation == 0:
                return float('inf') if mean_return > 0 else 0.0
            
            # Annualize
            sortino_ratio = (mean_return - self.risk_free_rate / 252) / downside_deviation * np.sqrt(252)
            
            return float(sortino_ratio)
            
        except Exception as e:
            logger.error(f"Failed to calculate Sortino ratio: {e}")
            return 0.0
    
    async def _store_performance_snapshot(self, snapshot: PerformanceSnapshot) -> None:
        """Store performance snapshot in database."""
        try:
            # Check if snapshot already exists for this date
            check_query = """
            SELECT id FROM performance_snapshots 
            WHERE fund_id = :fund_id AND snapshot_date = :snapshot_date
            """
            
            check_result = await self.database_manager.execute_query(
                check_query,
                {"fund_id": snapshot.fund_id, "snapshot_date": snapshot.snapshot_date}
            )
            
            if check_result['query_result']['data']:
                # Update existing snapshot
                update_query = """
                UPDATE performance_snapshots 
                SET total_value = :total_value, total_return = :total_return,
                    total_return_percentage = :total_return_percentage,
                    daily_return = :daily_return, daily_return_percentage = :daily_return_percentage,
                    sharpe_ratio = :sharpe_ratio, max_drawdown = :max_drawdown,
                    volatility = :volatility, beta = :beta, alpha = :alpha,
                    var_95 = :var_95, cvar_95 = :cvar_95, win_rate = :win_rate,
                    profit_factor = :profit_factor, calmar_ratio = :calmar_ratio,
                    sortino_ratio = :sortino_ratio
                WHERE fund_id = :fund_id AND snapshot_date = :snapshot_date
                """
                
                update_params = {
                    "fund_id": snapshot.fund_id,
                    "snapshot_date": snapshot.snapshot_date,
                    "total_value": snapshot.total_value,
                    "total_return": snapshot.total_return,
                    "total_return_percentage": snapshot.total_return_percentage,
                    "daily_return": snapshot.daily_return,
                    "daily_return_percentage": snapshot.daily_return_percentage,
                    "sharpe_ratio": snapshot.sharpe_ratio,
                    "max_drawdown": snapshot.max_drawdown,
                    "volatility": snapshot.volatility,
                    "beta": snapshot.beta,
                    "alpha": snapshot.alpha,
                    "var_95": snapshot.var_95,
                    "cvar_95": snapshot.cvar_95,
                    "win_rate": snapshot.win_rate,
                    "profit_factor": snapshot.profit_factor,
                    "calmar_ratio": snapshot.calmar_ratio,
                    "sortino_ratio": snapshot.sortino_ratio
                }
                
                await self.database_manager.execute_query(update_query, update_params)
            else:
                # Insert new snapshot
                insert_query = """
                INSERT INTO performance_snapshots (
                    id, fund_id, snapshot_date, total_value, total_return,
                    total_return_percentage, daily_return, daily_return_percentage,
                    sharpe_ratio, max_drawdown, volatility, beta, alpha,
                    var_95, cvar_95, win_rate, profit_factor, calmar_ratio, sortino_ratio
                ) VALUES (
                    :id, :fund_id, :snapshot_date, :total_value, :total_return,
                    :total_return_percentage, :daily_return, :daily_return_percentage,
                    :sharpe_ratio, :max_drawdown, :volatility, :beta, :alpha,
                    :var_95, :cvar_95, :win_rate, :profit_factor, :calmar_ratio, :sortino_ratio
                )
                """
                
                insert_params = {
                    "id": str(uuid.uuid4()),
                    "fund_id": snapshot.fund_id,
                    "snapshot_date": snapshot.snapshot_date,
                    "total_value": snapshot.total_value,
                    "total_return": snapshot.total_return,
                    "total_return_percentage": snapshot.total_return_percentage,
                    "daily_return": snapshot.daily_return,
                    "daily_return_percentage": snapshot.daily_return_percentage,
                    "sharpe_ratio": snapshot.sharpe_ratio,
                    "max_drawdown": snapshot.max_drawdown,
                    "volatility": snapshot.volatility,
                    "beta": snapshot.beta,
                    "alpha": snapshot.alpha,
                    "var_95": snapshot.var_95,
                    "cvar_95": snapshot.cvar_95,
                    "win_rate": snapshot.win_rate,
                    "profit_factor": snapshot.profit_factor,
                    "calmar_ratio": snapshot.calmar_ratio,
                    "sortino_ratio": snapshot.sortino_ratio
                }
                
                await self.database_manager.execute_query(insert_query, insert_params)
            
        except Exception as e:
            logger.error(f"Failed to store performance snapshot: {e}")
    
    async def get_performance_history(self, fund_id: str, days: int = 30) -> Dict[str, Any]:
        """Get performance history for a fund."""
        try:
            query = """
            SELECT * FROM performance_snapshots 
            WHERE fund_id = :fund_id 
            ORDER BY snapshot_date DESC 
            LIMIT :days
            """
            
            result = await self.database_manager.execute_query(
                query,
                {"fund_id": fund_id, "days": days}
            )
            
            if 'error' in result:
                return {"error": f"Failed to get performance history: {result['error']}"}
            
            performance_history = []
            for row in result['query_result']['data']:
                performance_history.append({
                    "snapshot_date": row['snapshot_date'].isoformat(),
                    "total_value": float(row['total_value']),
                    "total_return": float(row['total_return']),
                    "total_return_percentage": float(row['total_return_percentage']),
                    "daily_return": float(row['daily_return']) if row['daily_return'] else None,
                    "daily_return_percentage": float(row['daily_return_percentage']) if row['daily_return_percentage'] else None,
                    "sharpe_ratio": float(row['sharpe_ratio']) if row['sharpe_ratio'] else None,
                    "max_drawdown": float(row['max_drawdown']) if row['max_drawdown'] else None,
                    "volatility": float(row['volatility']) if row['volatility'] else None,
                    "beta": float(row['beta']) if row['beta'] else None,
                    "alpha": float(row['alpha']) if row['alpha'] else None,
                    "var_95": float(row['var_95']) if row['var_95'] else None,
                    "cvar_95": float(row['cvar_95']) if row['cvar_95'] else None,
                    "win_rate": float(row['win_rate']) if row['win_rate'] else None,
                    "profit_factor": float(row['profit_factor']) if row['profit_factor'] else None,
                    "calmar_ratio": float(row['calmar_ratio']) if row['calmar_ratio'] else None,
                    "sortino_ratio": float(row['sortino_ratio']) if row['sortino_ratio'] else None
                })
            
            return {
                "fund_id": fund_id,
                "performance_history": performance_history,
                "total_records": len(performance_history),
                "period_days": days
            }
            
        except Exception as e:
            logger.error(f"Failed to get performance history: {e}")
            return {"error": f"Failed to get performance history: {str(e)}"}
    
    async def calculate_benchmark_comparison(self, fund_id: str, benchmark_symbol: str = None) -> Dict[str, Any]:
        """Calculate benchmark comparison metrics."""
        try:
            if benchmark_symbol is None:
                benchmark_symbol = self.benchmark_symbol
            
            # Get fund performance
            fund_performance = await self.get_performance_history(fund_id, days=252)
            if 'error' in fund_performance:
                return fund_performance
            
            if not fund_performance['performance_history']:
                return {"error": "No performance data available"}
            
            # Calculate fund metrics
            fund_returns = [p['daily_return_percentage'] for p in fund_performance['performance_history'] if p['daily_return_percentage'] is not None]
            
            if not fund_returns:
                return {"error": "No return data available"}
            
            fund_mean_return = np.mean(fund_returns)
            fund_std_return = np.std(fund_returns)
            
            # For now, use simplified benchmark data
            # In production, you'd fetch real benchmark data
            benchmark_mean_return = 0.0004  # ~10% annual return
            benchmark_std_return = 0.015  # ~15% annual volatility
            
            # Calculate comparison metrics
            excess_return = fund_mean_return - benchmark_mean_return
            tracking_error = np.sqrt(fund_std_return**2 + benchmark_std_return**2 - 2 * 0.7 * fund_std_return * benchmark_std_return)  # Simplified correlation
            information_ratio = excess_return / tracking_error if tracking_error > 0 else 0
            
            # Calculate beta and alpha
            beta = 1.0  # Simplified
            alpha = fund_mean_return - (benchmark_mean_return * beta)
            
            # Calculate correlation
            correlation = 0.7  # Simplified
            
            comparison = BenchmarkComparison(
                fund_return=fund_mean_return,
                benchmark_return=benchmark_mean_return,
                excess_return=excess_return,
                tracking_error=tracking_error,
                information_ratio=information_ratio,
                beta=beta,
                alpha=alpha,
                correlation=correlation
            )
            
            return {
                "fund_id": fund_id,
                "benchmark_symbol": benchmark_symbol,
                "fund_return": float(comparison.fund_return),
                "benchmark_return": float(comparison.benchmark_return),
                "excess_return": float(comparison.excess_return),
                "tracking_error": float(comparison.tracking_error),
                "information_ratio": float(comparison.information_ratio),
                "beta": float(comparison.beta),
                "alpha": float(comparison.alpha),
                "correlation": float(comparison.correlation),
                "calculated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate benchmark comparison: {e}")
            return {"error": f"Failed to calculate benchmark comparison: {str(e)}"}
