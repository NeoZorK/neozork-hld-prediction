"""
Performance Analyzer for Pocket Hedge Fund.

This module provides advanced analytics and performance monitoring
for the ML trading system.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics container."""
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    best_trade: float
    worst_trade: float
    avg_trade_duration: float
    recovery_time: float
    var_95: float
    var_99: float
    expected_shortfall: float

@dataclass
class RiskMetrics:
    """Risk metrics container."""
    beta: float
    alpha: float
    information_ratio: float
    treynor_ratio: float
    jensen_alpha: float
    tracking_error: float
    downside_deviation: float
    upside_capture: float
    downside_capture: float
    max_consecutive_losses: int
    max_consecutive_wins: int
    stability_of_returns: float
    tail_ratio: float

class PerformanceAnalyzer:
    """Advanced performance analyzer for trading systems."""
    
    def __init__(self):
        """Initialize PerformanceAnalyzer."""
        self.risk_free_rate = 0.02  # 2% risk-free rate
        self.benchmark_returns = None
        
    async def analyze_performance(self, trades: List[Dict[str, Any]], 
                                equity_curve: pd.DataFrame,
                                benchmark_data: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Comprehensive performance analysis."""
        try:
            logger.info("Starting comprehensive performance analysis")
            
            # Basic performance metrics
            performance_metrics = await self._calculate_performance_metrics(trades, equity_curve)
            
            # Risk metrics
            risk_metrics = await self._calculate_risk_metrics(equity_curve, benchmark_data)
            
            # Advanced analytics
            advanced_metrics = await self._calculate_advanced_metrics(trades, equity_curve)
            
            # Market regime analysis
            regime_analysis = await self._analyze_market_regimes(equity_curve)
            
            # Portfolio analytics
            portfolio_analytics = await self._analyze_portfolio_characteristics(trades, equity_curve)
            
            return {
                'performance_metrics': performance_metrics,
                'risk_metrics': risk_metrics,
                'advanced_metrics': advanced_metrics,
                'regime_analysis': regime_analysis,
                'portfolio_analytics': portfolio_analytics,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in performance analysis: {e}")
            raise
    
    async def _calculate_performance_metrics(self, trades: List[Dict[str, Any]], 
                                           equity_curve: pd.DataFrame) -> PerformanceMetrics:
        """Calculate comprehensive performance metrics."""
        try:
            if not trades or equity_curve.empty:
                return self._create_empty_performance_metrics()
            
            # Convert to DataFrames
            trades_df = pd.DataFrame(trades)
            equity_df = equity_curve.copy()
            
            # Basic returns
            total_return = (equity_df['capital'].iloc[-1] - equity_df['capital'].iloc[0]) / equity_df['capital'].iloc[0]
            
            # Annualized return
            days = (equity_df.index[-1] - equity_df.index[0]).days
            years = days / 365.25
            annualized_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
            
            # Volatility
            returns = equity_df['capital'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) if len(returns) > 1 else 0
            
            # Sharpe ratio
            sharpe_ratio = (annualized_return - self.risk_free_rate) / volatility if volatility > 0 else 0
            
            # Sortino ratio
            downside_returns = returns[returns < 0]
            downside_volatility = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 1 else 0
            sortino_ratio = (annualized_return - self.risk_free_rate) / downside_volatility if downside_volatility > 0 else 0
            
            # Maximum drawdown
            peak = equity_df['capital'].expanding().max()
            drawdown = (equity_df['capital'] - peak) / peak
            max_drawdown = drawdown.min()
            
            # Calmar ratio
            calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
            
            # Trade statistics
            total_trades = len(trades_df)
            winning_trades = len(trades_df[trades_df.get('pnl', 0) > 0])
            losing_trades = total_trades - winning_trades
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
            
            # Average win/loss
            winning_trades_df = trades_df[trades_df.get('pnl', 0) > 0]
            losing_trades_df = trades_df[trades_df.get('pnl', 0) <= 0]
            
            avg_win = winning_trades_df['pnl'].mean() if len(winning_trades_df) > 0 else 0
            avg_loss = losing_trades_df['pnl'].mean() if len(losing_trades_df) > 0 else 0
            
            # Profit factor
            gross_profit = winning_trades_df['pnl'].sum() if len(winning_trades_df) > 0 else 0
            gross_loss = abs(losing_trades_df['pnl'].sum()) if len(losing_trades_df) > 0 else 0
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
            
            # Best/worst trades
            best_trade = trades_df['pnl'].max() if not trades_df.empty else 0
            worst_trade = trades_df['pnl'].min() if not trades_df.empty else 0
            
            # Average trade duration
            if 'timestamp' in trades_df.columns:
                trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
                avg_trade_duration = (trades_df['timestamp'].max() - trades_df['timestamp'].min()).days / total_trades if total_trades > 0 else 0
            else:
                avg_trade_duration = 0
            
            # Recovery time (time to recover from max drawdown)
            recovery_time = await self._calculate_recovery_time(equity_df, max_drawdown)
            
            # Value at Risk (VaR)
            var_95 = np.percentile(returns, 5) if len(returns) > 0 else 0
            var_99 = np.percentile(returns, 1) if len(returns) > 0 else 0
            
            # Expected Shortfall (Conditional VaR)
            expected_shortfall = returns[returns <= var_95].mean() if len(returns[returns <= var_95]) > 0 else 0
            
            return PerformanceMetrics(
                total_return=float(total_return),
                annualized_return=float(annualized_return),
                volatility=float(volatility),
                sharpe_ratio=float(sharpe_ratio),
                sortino_ratio=float(sortino_ratio),
                calmar_ratio=float(calmar_ratio),
                max_drawdown=float(max_drawdown),
                win_rate=float(win_rate),
                profit_factor=float(profit_factor),
                total_trades=int(total_trades),
                winning_trades=int(winning_trades),
                losing_trades=int(losing_trades),
                avg_win=float(avg_win),
                avg_loss=float(avg_loss),
                best_trade=float(best_trade),
                worst_trade=float(worst_trade),
                avg_trade_duration=float(avg_trade_duration),
                recovery_time=float(recovery_time),
                var_95=float(var_95),
                var_99=float(var_99),
                expected_shortfall=float(expected_shortfall)
            )
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return self._create_empty_performance_metrics()
    
    async def _calculate_risk_metrics(self, equity_curve: pd.DataFrame, 
                                    benchmark_data: Optional[pd.DataFrame] = None) -> RiskMetrics:
        """Calculate advanced risk metrics."""
        try:
            if equity_curve.empty:
                return self._create_empty_risk_metrics()
            
            returns = equity_curve['capital'].pct_change().dropna()
            
            if len(returns) < 2:
                return self._create_empty_risk_metrics()
            
            # Beta calculation (if benchmark provided)
            if benchmark_data is not None and not benchmark_data.empty:
                benchmark_returns = benchmark_data['close'].pct_change().dropna()
                if len(benchmark_returns) > 0:
                    covariance = np.cov(returns, benchmark_returns)[0, 1]
                    benchmark_variance = np.var(benchmark_returns)
                    beta = covariance / benchmark_variance if benchmark_variance > 0 else 0
                    
                    # Alpha calculation
                    alpha = returns.mean() - (self.risk_free_rate + beta * (benchmark_returns.mean() - self.risk_free_rate))
                    
                    # Information ratio
                    tracking_error = np.std(returns - benchmark_returns)
                    information_ratio = (returns.mean() - benchmark_returns.mean()) / tracking_error if tracking_error > 0 else 0
                else:
                    beta = alpha = information_ratio = 0
            else:
                beta = alpha = information_ratio = 0
            
            # Treynor ratio
            treynor_ratio = (returns.mean() - self.risk_free_rate) / beta if beta != 0 else 0
            
            # Jensen's alpha
            jensen_alpha = alpha
            
            # Tracking error
            tracking_error = np.std(returns) if len(returns) > 1 else 0
            
            # Downside deviation
            downside_returns = returns[returns < 0]
            downside_deviation = np.std(downside_returns) if len(downside_returns) > 1 else 0
            
            # Upside/Downside capture ratios
            if benchmark_data is not None and not benchmark_data.empty:
                benchmark_returns = benchmark_data['close'].pct_change().dropna()
                if len(benchmark_returns) > 0:
                    # Align returns
                    common_dates = returns.index.intersection(benchmark_returns.index)
                    if len(common_dates) > 0:
                        aligned_returns = returns.loc[common_dates]
                        aligned_benchmark = benchmark_returns.loc[common_dates]
                        
                        # Upside capture
                        upside_periods = aligned_benchmark > 0
                        if upside_periods.sum() > 0:
                            upside_capture = aligned_returns[upside_periods].mean() / aligned_benchmark[upside_periods].mean()
                        else:
                            upside_capture = 0
                        
                        # Downside capture
                        downside_periods = aligned_benchmark < 0
                        if downside_periods.sum() > 0:
                            downside_capture = aligned_returns[downside_periods].mean() / aligned_benchmark[downside_periods].mean()
                        else:
                            downside_capture = 0
                    else:
                        upside_capture = downside_capture = 0
                else:
                    upside_capture = downside_capture = 0
            else:
                upside_capture = downside_capture = 0
            
            # Consecutive wins/losses
            consecutive_wins, consecutive_losses = await self._calculate_consecutive_trades(returns)
            
            # Stability of returns
            stability = 1 - (returns.std() / abs(returns.mean())) if returns.mean() != 0 else 0
            
            # Tail ratio
            tail_ratio = abs(np.percentile(returns, 95)) / abs(np.percentile(returns, 5)) if np.percentile(returns, 5) != 0 else 0
            
            return RiskMetrics(
                beta=float(beta),
                alpha=float(alpha),
                information_ratio=float(information_ratio),
                treynor_ratio=float(treynor_ratio),
                jensen_alpha=float(jensen_alpha),
                tracking_error=float(tracking_error),
                downside_deviation=float(downside_deviation),
                upside_capture=float(upside_capture),
                downside_capture=float(downside_capture),
                max_consecutive_losses=int(consecutive_losses),
                max_consecutive_wins=int(consecutive_wins),
                stability_of_returns=float(stability),
                tail_ratio=float(tail_ratio)
            )
            
        except Exception as e:
            logger.error(f"Error calculating risk metrics: {e}")
            return self._create_empty_risk_metrics()
    
    async def _calculate_advanced_metrics(self, trades: List[Dict[str, Any]], 
                                        equity_curve: pd.DataFrame) -> Dict[str, Any]:
        """Calculate advanced analytics metrics."""
        try:
            if not trades or equity_curve.empty:
                return {}
            
            trades_df = pd.DataFrame(trades)
            returns = equity_curve['capital'].pct_change().dropna()
            
            # Kelly Criterion
            win_rate = len(trades_df[trades_df.get('pnl', 0) > 0]) / len(trades_df) if len(trades_df) > 0 else 0
            avg_win = trades_df[trades_df.get('pnl', 0) > 0]['pnl'].mean() if len(trades_df[trades_df.get('pnl', 0) > 0]) > 0 else 0
            avg_loss = abs(trades_df[trades_df.get('pnl', 0) <= 0]['pnl'].mean()) if len(trades_df[trades_df.get('pnl', 0) <= 0]) > 0 else 0
            
            if avg_loss > 0:
                kelly_criterion = win_rate - ((1 - win_rate) / (avg_win / avg_loss))
            else:
                kelly_criterion = 0
            
            # Skewness and Kurtosis
            skewness = returns.skew() if len(returns) > 2 else 0
            kurtosis = returns.kurtosis() if len(returns) > 2 else 0
            
            # Hurst Exponent (trend persistence)
            hurst_exponent = await self._calculate_hurst_exponent(returns)
            
            # Fractal Dimension
            fractal_dimension = await self._calculate_fractal_dimension(equity_curve['capital'])
            
            # Drawdown analysis
            drawdown_analysis = await self._analyze_drawdowns(equity_curve)
            
            # Return distribution analysis
            distribution_analysis = await self._analyze_return_distribution(returns)
            
            return {
                'kelly_criterion': float(kelly_criterion),
                'skewness': float(skewness),
                'kurtosis': float(kurtosis),
                'hurst_exponent': float(hurst_exponent),
                'fractal_dimension': float(fractal_dimension),
                'drawdown_analysis': drawdown_analysis,
                'distribution_analysis': distribution_analysis
            }
            
        except Exception as e:
            logger.error(f"Error calculating advanced metrics: {e}")
            return {}
    
    async def _analyze_market_regimes(self, equity_curve: pd.DataFrame) -> Dict[str, Any]:
        """Analyze performance across different market regimes."""
        try:
            if equity_curve.empty:
                return {}
            
            returns = equity_curve['capital'].pct_change().dropna()
            
            if len(returns) < 10:
                return {}
            
            # Define market regimes based on volatility
            volatility_threshold = returns.std()
            high_vol_periods = returns.abs() > volatility_threshold
            low_vol_periods = returns.abs() <= volatility_threshold
            
            # Performance in different regimes
            high_vol_performance = returns[high_vol_periods].mean() if high_vol_periods.sum() > 0 else 0
            low_vol_performance = returns[low_vol_periods].mean() if low_vol_periods.sum() > 0 else 0
            
            # Trend analysis
            trend_analysis = await self._analyze_trends(equity_curve)
            
            return {
                'high_volatility_performance': float(high_vol_performance),
                'low_volatility_performance': float(low_vol_performance),
                'volatility_threshold': float(volatility_threshold),
                'trend_analysis': trend_analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market regimes: {e}")
            return {}
    
    async def _analyze_portfolio_characteristics(self, trades: List[Dict[str, Any]], 
                                               equity_curve: pd.DataFrame) -> Dict[str, Any]:
        """Analyze portfolio characteristics and diversification."""
        try:
            if not trades:
                return {}
            
            trades_df = pd.DataFrame(trades)
            
            # Symbol diversification
            if 'symbol' in trades_df.columns:
                symbol_counts = trades_df['symbol'].value_counts()
                diversification_ratio = 1 - (symbol_counts.max() / len(trades_df)) if len(trades_df) > 0 else 0
                top_symbols = symbol_counts.head(5).to_dict()
            else:
                diversification_ratio = 0
                top_symbols = {}
            
            # Trade frequency analysis
            if 'timestamp' in trades_df.columns:
                trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
                trades_df['date'] = trades_df['timestamp'].dt.date
                daily_trades = trades_df.groupby('date').size()
                avg_daily_trades = daily_trades.mean()
                max_daily_trades = daily_trades.max()
            else:
                avg_daily_trades = max_daily_trades = 0
            
            # Position sizing analysis
            if 'quantity' in trades_df.columns and 'price' in trades_df.columns:
                position_sizes = trades_df['quantity'] * trades_df['price']
                avg_position_size = position_sizes.mean()
                position_size_std = position_sizes.std()
            else:
                avg_position_size = position_size_std = 0
            
            return {
                'diversification_ratio': float(diversification_ratio),
                'top_symbols': top_symbols,
                'avg_daily_trades': float(avg_daily_trades),
                'max_daily_trades': int(max_daily_trades),
                'avg_position_size': float(avg_position_size),
                'position_size_std': float(position_size_std)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing portfolio characteristics: {e}")
            return {}
    
    async def _calculate_recovery_time(self, equity_curve: pd.DataFrame, max_drawdown: float) -> float:
        """Calculate average recovery time from drawdowns."""
        try:
            if equity_curve.empty or max_drawdown == 0:
                return 0
            
            peak = equity_curve['capital'].expanding().max()
            drawdown = (equity_curve['capital'] - peak) / peak
            
            # Find drawdown periods
            in_drawdown = drawdown < 0
            drawdown_periods = []
            
            start_drawdown = None
            for i, is_dd in enumerate(in_drawdown):
                if is_dd and start_drawdown is None:
                    start_drawdown = i
                elif not is_dd and start_drawdown is not None:
                    drawdown_periods.append(i - start_drawdown)
                    start_drawdown = None
            
            return float(np.mean(drawdown_periods)) if drawdown_periods else 0
            
        except Exception as e:
            logger.error(f"Error calculating recovery time: {e}")
            return 0
    
    async def _calculate_consecutive_trades(self, returns: pd.Series) -> Tuple[int, int]:
        """Calculate maximum consecutive wins and losses."""
        try:
            if len(returns) == 0:
                return 0, 0
            
            wins = returns > 0
            losses = returns < 0
            
            # Consecutive wins
            max_consecutive_wins = 0
            current_wins = 0
            for win in wins:
                if win:
                    current_wins += 1
                    max_consecutive_wins = max(max_consecutive_wins, current_wins)
                else:
                    current_wins = 0
            
            # Consecutive losses
            max_consecutive_losses = 0
            current_losses = 0
            for loss in losses:
                if loss:
                    current_losses += 1
                    max_consecutive_losses = max(max_consecutive_losses, current_losses)
                else:
                    current_losses = 0
            
            return max_consecutive_wins, max_consecutive_losses
            
        except Exception as e:
            logger.error(f"Error calculating consecutive trades: {e}")
            return 0, 0
    
    async def _calculate_hurst_exponent(self, returns: pd.Series) -> float:
        """Calculate Hurst exponent for trend persistence."""
        try:
            if len(returns) < 10:
                return 0.5
            
            # Simplified Hurst calculation
            n = len(returns)
            mean_return = returns.mean()
            
            # Calculate cumulative deviations
            cumulative_deviations = (returns - mean_return).cumsum()
            
            # Calculate range
            R = cumulative_deviations.max() - cumulative_deviations.min()
            
            # Calculate standard deviation
            S = returns.std()
            
            # Hurst exponent
            if S > 0:
                hurst = np.log(R / S) / np.log(n)
                return float(np.clip(hurst, 0, 1))  # Clamp between 0 and 1
            else:
                return 0.5
                
        except Exception as e:
            logger.error(f"Error calculating Hurst exponent: {e}")
            return 0.5
    
    async def _calculate_fractal_dimension(self, prices: pd.Series) -> float:
        """Calculate fractal dimension of price series."""
        try:
            if len(prices) < 10:
                return 1.0
            
            # Simplified box-counting method
            n = len(prices)
            scales = [2, 4, 8, 16, 32]
            counts = []
            
            for scale in scales:
                if scale >= n:
                    continue
                
                # Count boxes needed
                min_price = prices.min()
                max_price = prices.max()
                box_height = (max_price - min_price) / scale
                
                if box_height == 0:
                    continue
                
                count = 0
                for i in range(0, n, scale):
                    box_start = i
                    box_end = min(i + scale, n)
                    box_prices = prices.iloc[box_start:box_end]
                    
                    if len(box_prices) > 0:
                        box_min = box_prices.min()
                        box_max = box_prices.max()
                        boxes_needed = int(np.ceil((box_max - box_min) / box_height)) if box_height > 0 else 1
                        count += boxes_needed
                
                counts.append(count)
            
            if len(counts) < 2:
                return 1.0
            
            # Calculate fractal dimension
            log_scales = np.log(scales[:len(counts)])
            log_counts = np.log(counts)
            
            if len(log_scales) > 1 and np.std(log_scales) > 0:
                fractal_dim = -np.polyfit(log_scales, log_counts, 1)[0]
                return float(np.clip(fractal_dim, 1.0, 2.0))
            else:
                return 1.0
                
        except Exception as e:
            logger.error(f"Error calculating fractal dimension: {e}")
            return 1.0
    
    async def _analyze_drawdowns(self, equity_curve: pd.DataFrame) -> Dict[str, Any]:
        """Analyze drawdown characteristics."""
        try:
            if equity_curve.empty:
                return {}
            
            peak = equity_curve['capital'].expanding().max()
            drawdown = (equity_curve['capital'] - peak) / peak
            
            # Drawdown statistics
            max_drawdown = drawdown.min()
            avg_drawdown = drawdown[drawdown < 0].mean() if (drawdown < 0).any() else 0
            drawdown_duration = (drawdown < 0).sum()
            
            return {
                'max_drawdown': float(max_drawdown),
                'avg_drawdown': float(avg_drawdown),
                'drawdown_duration': int(drawdown_duration),
                'drawdown_frequency': float((drawdown < 0).sum() / len(drawdown))
            }
            
        except Exception as e:
            logger.error(f"Error analyzing drawdowns: {e}")
            return {}
    
    async def _analyze_return_distribution(self, returns: pd.Series) -> Dict[str, Any]:
        """Analyze return distribution characteristics."""
        try:
            if len(returns) == 0:
                return {}
            
            # Distribution statistics
            mean_return = returns.mean()
            std_return = returns.std()
            skewness = returns.skew()
            kurtosis = returns.kurtosis()
            
            # Percentiles
            percentiles = {
                'p1': float(returns.quantile(0.01)),
                'p5': float(returns.quantile(0.05)),
                'p10': float(returns.quantile(0.10)),
                'p25': float(returns.quantile(0.25)),
                'p50': float(returns.quantile(0.50)),
                'p75': float(returns.quantile(0.75)),
                'p90': float(returns.quantile(0.90)),
                'p95': float(returns.quantile(0.95)),
                'p99': float(returns.quantile(0.99))
            }
            
            return {
                'mean': float(mean_return),
                'std': float(std_return),
                'skewness': float(skewness),
                'kurtosis': float(kurtosis),
                'percentiles': percentiles
            }
            
        except Exception as e:
            logger.error(f"Error analyzing return distribution: {e}")
            return {}
    
    async def _analyze_trends(self, equity_curve: pd.DataFrame) -> Dict[str, Any]:
        """Analyze trend characteristics."""
        try:
            if equity_curve.empty:
                return {}
            
            prices = equity_curve['capital']
            
            # Simple trend analysis
            if len(prices) < 2:
                return {}
            
            # Linear trend
            x = np.arange(len(prices))
            slope, intercept = np.polyfit(x, prices, 1)
            
            # Trend strength
            trend_strength = abs(slope) / prices.std() if prices.std() > 0 else 0
            
            return {
                'slope': float(slope),
                'intercept': float(intercept),
                'trend_strength': float(trend_strength),
                'trend_direction': 'up' if slope > 0 else 'down'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return {}
    
    def _create_empty_performance_metrics(self) -> PerformanceMetrics:
        """Create empty performance metrics."""
        return PerformanceMetrics(
            total_return=0.0, annualized_return=0.0, volatility=0.0,
            sharpe_ratio=0.0, sortino_ratio=0.0, calmar_ratio=0.0,
            max_drawdown=0.0, win_rate=0.0, profit_factor=0.0,
            total_trades=0, winning_trades=0, losing_trades=0,
            avg_win=0.0, avg_loss=0.0, best_trade=0.0, worst_trade=0.0,
            avg_trade_duration=0.0, recovery_time=0.0,
            var_95=0.0, var_99=0.0, expected_shortfall=0.0
        )
    
    def _create_empty_risk_metrics(self) -> RiskMetrics:
        """Create empty risk metrics."""
        return RiskMetrics(
            beta=0.0, alpha=0.0, information_ratio=0.0, treynor_ratio=0.0,
            jensen_alpha=0.0, tracking_error=0.0, downside_deviation=0.0,
            upside_capture=0.0, downside_capture=0.0,
            max_consecutive_losses=0, max_consecutive_wins=0,
            stability_of_returns=0.0, tail_ratio=0.0
        )
