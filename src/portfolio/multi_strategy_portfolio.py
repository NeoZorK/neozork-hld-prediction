# -*- coding: utf-8 -*-
"""
Multi-Strategy Portfolio Management System for NeoZork Interactive ML Trading Strategy Development.

This module provides advanced portfolio management with multiple trading strategies.
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, Any, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StrategyType(Enum):
    """Strategy types."""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    ARBITRAGE = "arbitrage"
    MARKET_MAKING = "market_making"
    TREND_FOLLOWING = "trend_following"
    CONTRARIAN = "contrarian"
    ML_BASED = "ml_based"
    PAIRS_TRADING = "pairs_trading"

class AllocationMethod(Enum):
    """Portfolio allocation methods."""
    EQUAL_WEIGHT = "equal_weight"
    RISK_PARITY = "risk_parity"
    KELLY_OPTIMAL = "kelly_optimal"
    MEAN_VARIANCE = "mean_variance"
    BLACK_LITTERMAN = "black_litterman"
    HIERARCHICAL_RISK_PARITY = "hierarchical_risk_parity"
    MAXIMUM_SHARPE = "maximum_sharpe"
    MINIMUM_VARIANCE = "minimum_variance"

class RebalancingFrequency(Enum):
    """Rebalancing frequencies."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    DYNAMIC = "dynamic"

@dataclass
class Strategy:
    """Trading strategy definition."""
    name: str
    strategy_type: StrategyType
    weight: float = 0.0
    max_weight: float = 0.3
    min_weight: float = 0.0
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    is_active: bool = True
    last_rebalance: datetime = field(default_factory=datetime.now)
    trades_count: int = 0
    total_pnl: float = 0.0

@dataclass
class PortfolioAllocation:
    """Portfolio allocation result."""
    strategy_weights: Dict[str, float]
    total_weight: float
    risk_metrics: Dict[str, float]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float
    max_drawdown: float
    allocation_timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class StrategyPerformance:
    """Strategy performance metrics."""
    strategy_name: str
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    calmar_ratio: float
    sortino_ratio: float
    trades_count: int
    avg_trade_duration: float

class MultiStrategyPortfolioManager:
    """Multi-strategy portfolio management system."""
    
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.strategies = {}
        self.allocations = []
        self.performance_history = []
        self.rebalancing_frequency = RebalancingFrequency.WEEKLY
        self.allocation_method = AllocationMethod.RISK_PARITY
        self.max_strategies = 10
        self.min_strategy_weight = 0.05
        self.max_strategy_weight = 0.4
        
    def add_strategy(self, strategy: Strategy) -> Dict[str, Any]:
        """Add a trading strategy to the portfolio."""
        try:
            if len(self.strategies) >= self.max_strategies:
                return {
                    'status': 'error',
                    'message': f'Maximum number of strategies ({self.max_strategies}) reached'
                }
            
            if strategy.name in self.strategies:
                return {
                    'status': 'error',
                    'message': f'Strategy {strategy.name} already exists'
                }
            
            # Validate strategy weight
            if strategy.weight < 0 or strategy.weight > 1:
                return {
                    'status': 'error',
                    'message': 'Strategy weight must be between 0 and 1'
                }
            
            self.strategies[strategy.name] = strategy
            logger.info(f"Strategy {strategy.name} added to portfolio")
            
            return {
                'status': 'success',
                'strategy_name': strategy.name,
                'strategy_type': strategy.strategy_type.value,
                'weight': strategy.weight,
                'message': f'Strategy {strategy.name} added successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to add strategy: {e}")
            return {
                'status': 'error',
                'message': f'Failed to add strategy: {str(e)}'
            }
    
    def remove_strategy(self, strategy_name: str) -> Dict[str, Any]:
        """Remove a strategy from the portfolio."""
        try:
            if strategy_name not in self.strategies:
                return {
                    'status': 'error',
                    'message': f'Strategy {strategy_name} not found'
                }
            
            del self.strategies[strategy_name]
            logger.info(f"Strategy {strategy_name} removed from portfolio")
            
            return {
                'status': 'success',
                'strategy_name': strategy_name,
                'message': f'Strategy {strategy_name} removed successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to remove strategy: {e}")
            return {
                'status': 'error',
                'message': f'Failed to remove strategy: {str(e)}'
            }
    
    def update_strategy_performance(self, strategy_name: str, 
                                  performance_metrics: Dict[str, float]) -> Dict[str, Any]:
        """Update strategy performance metrics."""
        try:
            if strategy_name not in self.strategies:
                return {
                    'status': 'error',
                    'message': f'Strategy {strategy_name} not found'
                }
            
            strategy = self.strategies[strategy_name]
            strategy.performance_metrics.update(performance_metrics)
            
            # Update strategy PnL if provided
            if 'total_pnl' in performance_metrics:
                strategy.total_pnl = performance_metrics['total_pnl']
            
            if 'trades_count' in performance_metrics:
                strategy.trades_count = performance_metrics['trades_count']
            
            logger.info(f"Performance updated for strategy {strategy_name}")
            
            return {
                'status': 'success',
                'strategy_name': strategy_name,
                'updated_metrics': list(performance_metrics.keys()),
                'message': f'Performance updated for strategy {strategy_name}'
            }
            
        except Exception as e:
            logger.error(f"Failed to update strategy performance: {e}")
            return {
                'status': 'error',
                'message': f'Failed to update strategy performance: {str(e)}'
            }
    
    def calculate_portfolio_allocation(self, method: AllocationMethod = None) -> PortfolioAllocation:
        """Calculate optimal portfolio allocation."""
        try:
            if not self.strategies:
                return self._empty_allocation()
            
            method = method or self.allocation_method
            
            if method == AllocationMethod.EQUAL_WEIGHT:
                weights = self._equal_weight_allocation()
            elif method == AllocationMethod.RISK_PARITY:
                weights = self._risk_parity_allocation()
            elif method == AllocationMethod.KELLY_OPTIMAL:
                weights = self._kelly_optimal_allocation()
            elif method == AllocationMethod.MEAN_VARIANCE:
                weights = self._mean_variance_allocation()
            elif method == AllocationMethod.BLACK_LITTERMAN:
                weights = self._black_litterman_allocation()
            elif method == AllocationMethod.HIERARCHICAL_RISK_PARITY:
                weights = self._hierarchical_risk_parity_allocation()
            elif method == AllocationMethod.MAXIMUM_SHARPE:
                weights = self._maximum_sharpe_allocation()
            elif method == AllocationMethod.MINIMUM_VARIANCE:
                weights = self._minimum_variance_allocation()
            else:
                weights = self._equal_weight_allocation()
            
            # Calculate portfolio metrics
            risk_metrics = self._calculate_portfolio_risk_metrics(weights)
            expected_return = self._calculate_expected_return(weights)
            expected_volatility = self._calculate_expected_volatility(weights)
            sharpe_ratio = expected_return / expected_volatility if expected_volatility > 0 else 0
            max_drawdown = self._calculate_max_drawdown(weights)
            
            allocation = PortfolioAllocation(
                strategy_weights=weights,
                total_weight=sum(weights.values()),
                risk_metrics=risk_metrics,
                expected_return=expected_return,
                expected_volatility=expected_volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown
            )
            
            # Store allocation
            self.allocations.append(allocation)
            
            return allocation
            
        except Exception as e:
            logger.error(f"Failed to calculate portfolio allocation: {e}")
            return self._empty_allocation()
    
    def _empty_allocation(self) -> PortfolioAllocation:
        """Return empty allocation."""
        return PortfolioAllocation(
            strategy_weights={},
            total_weight=0.0,
            risk_metrics={},
            expected_return=0.0,
            expected_volatility=0.0,
            sharpe_ratio=0.0,
            max_drawdown=0.0
        )
    
    def _equal_weight_allocation(self) -> Dict[str, float]:
        """Equal weight allocation."""
        try:
            active_strategies = [name for name, strategy in self.strategies.items() if strategy.is_active]
            if not active_strategies:
                return {}
            
            equal_weight = 1.0 / len(active_strategies)
            return {name: equal_weight for name in active_strategies}
            
        except Exception as e:
            logger.error(f"Failed to calculate equal weight allocation: {e}")
            return {}
    
    def _risk_parity_allocation(self) -> Dict[str, float]:
        """Risk parity allocation."""
        try:
            active_strategies = {name: strategy for name, strategy in self.strategies.items() if strategy.is_active}
            if not active_strategies:
                return {}
            
            # Calculate inverse volatility weights
            weights = {}
            total_inverse_vol = 0.0
            
            for name, strategy in active_strategies.items():
                volatility = strategy.performance_metrics.get('volatility', 0.2)  # Default 20%
                if volatility > 0:
                    inverse_vol = 1.0 / volatility
                    weights[name] = inverse_vol
                    total_inverse_vol += inverse_vol
                else:
                    weights[name] = 0.1  # Default weight
            
            # Normalize weights
            if total_inverse_vol > 0:
                for name in weights:
                    weights[name] = weights[name] / total_inverse_vol
            
            return weights
            
        except Exception as e:
            logger.error(f"Failed to calculate risk parity allocation: {e}")
            return self._equal_weight_allocation()
    
    def _kelly_optimal_allocation(self) -> Dict[str, float]:
        """Kelly optimal allocation."""
        try:
            active_strategies = {name: strategy for name, strategy in self.strategies.items() if strategy.is_active}
            if not active_strategies:
                return {}
            
            weights = {}
            total_kelly = 0.0
            
            for name, strategy in active_strategies.items():
                # Kelly formula: f = (bp - q) / b
                # where b = odds, p = win probability, q = loss probability
                win_rate = strategy.performance_metrics.get('win_rate', 0.5)
                avg_win = strategy.performance_metrics.get('avg_win', 0.01)
                avg_loss = strategy.performance_metrics.get('avg_loss', 0.01)
                
                if avg_loss > 0:
                    odds = avg_win / avg_loss
                    kelly_fraction = (odds * win_rate - (1 - win_rate)) / odds
                    kelly_fraction = max(0, min(0.25, kelly_fraction))  # Cap at 25%
                    weights[name] = kelly_fraction
                    total_kelly += kelly_fraction
                else:
                    weights[name] = 0.1
            
            # Normalize weights
            if total_kelly > 0:
                for name in weights:
                    weights[name] = weights[name] / total_kelly
            
            return weights
            
        except Exception as e:
            logger.error(f"Failed to calculate Kelly optimal allocation: {e}")
            return self._equal_weight_allocation()
    
    def _mean_variance_allocation(self) -> Dict[str, float]:
        """Mean-variance optimization allocation."""
        try:
            active_strategies = {name: strategy for name, strategy in self.strategies.items() if strategy.is_active}
            if not active_strategies:
                return {}
            
            # Simplified mean-variance optimization
            returns = []
            volatilities = []
            names = list(active_strategies.keys())
            
            for name in names:
                strategy = active_strategies[name]
                expected_return = strategy.performance_metrics.get('annualized_return', 0.1)
                volatility = strategy.performance_metrics.get('volatility', 0.2)
                returns.append(expected_return)
                volatilities.append(volatility)
            
            # Calculate Sharpe ratios and use as weights
            weights = {}
            total_sharpe = 0.0
            
            for i, name in enumerate(names):
                if volatilities[i] > 0:
                    sharpe = returns[i] / volatilities[i]
                    weights[name] = max(0, sharpe)
                    total_sharpe += max(0, sharpe)
                else:
                    weights[name] = 0.1
            
            # Normalize weights
            if total_sharpe > 0:
                for name in weights:
                    weights[name] = weights[name] / total_sharpe
            
            return weights
            
        except Exception as e:
            logger.error(f"Failed to calculate mean-variance allocation: {e}")
            return self._equal_weight_allocation()
    
    def _black_litterman_allocation(self) -> Dict[str, float]:
        """Black-Litterman allocation."""
        try:
            # Simplified Black-Litterman implementation
            # In practice, this would use market cap weights and views
            return self._mean_variance_allocation()
            
        except Exception as e:
            logger.error(f"Failed to calculate Black-Litterman allocation: {e}")
            return self._equal_weight_allocation()
    
    def _hierarchical_risk_parity_allocation(self) -> Dict[str, float]:
        """Hierarchical Risk Parity allocation."""
        try:
            # Simplified HRP implementation
            # In practice, this would use hierarchical clustering
            return self._risk_parity_allocation()
            
        except Exception as e:
            logger.error(f"Failed to calculate hierarchical risk parity allocation: {e}")
            return self._equal_weight_allocation()
    
    def _maximum_sharpe_allocation(self) -> Dict[str, float]:
        """Maximum Sharpe ratio allocation."""
        try:
            active_strategies = {name: strategy for name, strategy in self.strategies.items() if strategy.is_active}
            if not active_strategies:
                return {}
            
            # Find strategy with maximum Sharpe ratio
            max_sharpe = -float('inf')
            best_strategy = None
            
            for name, strategy in active_strategies.items():
                sharpe = strategy.performance_metrics.get('sharpe_ratio', 0)
                if sharpe > max_sharpe:
                    max_sharpe = sharpe
                    best_strategy = name
            
            if best_strategy:
                return {best_strategy: 1.0}
            else:
                return self._equal_weight_allocation()
            
        except Exception as e:
            logger.error(f"Failed to calculate maximum Sharpe allocation: {e}")
            return self._equal_weight_allocation()
    
    def _minimum_variance_allocation(self) -> Dict[str, float]:
        """Minimum variance allocation."""
        try:
            active_strategies = {name: strategy for name, strategy in self.strategies.items() if strategy.is_active}
            if not active_strategies:
                return {}
            
            # Find strategy with minimum variance
            min_variance = float('inf')
            best_strategy = None
            
            for name, strategy in active_strategies.items():
                volatility = strategy.performance_metrics.get('volatility', 1.0)
                variance = volatility ** 2
                if variance < min_variance:
                    min_variance = variance
                    best_strategy = name
            
            if best_strategy:
                return {best_strategy: 1.0}
            else:
                return self._equal_weight_allocation()
            
        except Exception as e:
            logger.error(f"Failed to calculate minimum variance allocation: {e}")
            return self._equal_weight_allocation()
    
    def _calculate_portfolio_risk_metrics(self, weights: Dict[str, float]) -> Dict[str, float]:
        """Calculate portfolio risk metrics."""
        try:
            if not weights:
                return {}
            
            # Calculate weighted risk metrics
            total_var = 0.0
            total_cvar = 0.0
            total_beta = 0.0
            
            for name, weight in weights.items():
                if name in self.strategies:
                    strategy = self.strategies[name]
                    var = strategy.performance_metrics.get('var_95', 0.05)
                    cvar = strategy.performance_metrics.get('cvar_95', 0.08)
                    beta = strategy.performance_metrics.get('beta', 1.0)
                    
                    total_var += weight * var
                    total_cvar += weight * cvar
                    total_beta += weight * beta
            
            return {
                'portfolio_var_95': total_var,
                'portfolio_cvar_95': total_cvar,
                'portfolio_beta': total_beta,
                'concentration_risk': max(weights.values()) if weights else 0.0
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate portfolio risk metrics: {e}")
            return {}
    
    def _calculate_expected_return(self, weights: Dict[str, float]) -> float:
        """Calculate expected portfolio return."""
        try:
            if not weights:
                return 0.0
            
            expected_return = 0.0
            for name, weight in weights.items():
                if name in self.strategies:
                    strategy = self.strategies[name]
                    annual_return = strategy.performance_metrics.get('annualized_return', 0.1)
                    expected_return += weight * annual_return
            
            return expected_return
            
        except Exception as e:
            logger.error(f"Failed to calculate expected return: {e}")
            return 0.0
    
    def _calculate_expected_volatility(self, weights: Dict[str, float]) -> float:
        """Calculate expected portfolio volatility."""
        try:
            if not weights:
                return 0.0
            
            # Simplified volatility calculation (ignoring correlations)
            expected_volatility = 0.0
            for name, weight in weights.items():
                if name in self.strategies:
                    strategy = self.strategies[name]
                    volatility = strategy.performance_metrics.get('volatility', 0.2)
                    expected_volatility += (weight * volatility) ** 2
            
            return np.sqrt(expected_volatility)
            
        except Exception as e:
            logger.error(f"Failed to calculate expected volatility: {e}")
            return 0.0
    
    def _calculate_max_drawdown(self, weights: Dict[str, float]) -> float:
        """Calculate maximum drawdown."""
        try:
            if not weights:
                return 0.0
            
            max_dd = 0.0
            for name, weight in weights.items():
                if name in self.strategies:
                    strategy = self.strategies[name]
                    dd = strategy.performance_metrics.get('max_drawdown', 0.1)
                    max_dd = max(max_dd, dd)
            
            return max_dd
            
        except Exception as e:
            logger.error(f"Failed to calculate max drawdown: {e}")
            return 0.0
    
    def rebalance_portfolio(self, method: AllocationMethod = None) -> Dict[str, Any]:
        """Rebalance portfolio based on current allocation method."""
        try:
            # Calculate new allocation
            allocation = self.calculate_portfolio_allocation(method)
            
            # Update strategy weights
            for name, weight in allocation.strategy_weights.items():
                if name in self.strategies:
                    self.strategies[name].weight = weight
                    self.strategies[name].last_rebalance = datetime.now()
            
            logger.info(f"Portfolio rebalanced using {allocation.strategy_weights}")
            
            return {
                'status': 'success',
                'allocation': allocation,
                'rebalance_timestamp': datetime.now().isoformat(),
                'message': 'Portfolio rebalanced successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to rebalance portfolio: {e}")
            return {
                'status': 'error',
                'message': f'Failed to rebalance portfolio: {str(e)}'
            }
    
    def get_strategy_performance(self, strategy_name: str = None) -> Dict[str, Any]:
        """Get strategy performance metrics."""
        try:
            if strategy_name:
                if strategy_name not in self.strategies:
                    return {
                        'status': 'error',
                        'message': f'Strategy {strategy_name} not found'
                    }
                
                strategy = self.strategies[strategy_name]
                return {
                    'status': 'success',
                    'strategy_name': strategy_name,
                    'performance': StrategyPerformance(
                        strategy_name=strategy_name,
                        total_return=strategy.performance_metrics.get('total_return', 0.0),
                        annualized_return=strategy.performance_metrics.get('annualized_return', 0.0),
                        volatility=strategy.performance_metrics.get('volatility', 0.0),
                        sharpe_ratio=strategy.performance_metrics.get('sharpe_ratio', 0.0),
                        max_drawdown=strategy.performance_metrics.get('max_drawdown', 0.0),
                        win_rate=strategy.performance_metrics.get('win_rate', 0.0),
                        profit_factor=strategy.performance_metrics.get('profit_factor', 0.0),
                        calmar_ratio=strategy.performance_metrics.get('calmar_ratio', 0.0),
                        sortino_ratio=strategy.performance_metrics.get('sortino_ratio', 0.0),
                        trades_count=strategy.trades_count,
                        avg_trade_duration=strategy.performance_metrics.get('avg_trade_duration', 0.0)
                    ),
                    'message': f'Performance retrieved for strategy {strategy_name}'
                }
            else:
                # Return all strategies performance
                all_performance = {}
                for name, strategy in self.strategies.items():
                    all_performance[name] = StrategyPerformance(
                        strategy_name=name,
                        total_return=strategy.performance_metrics.get('total_return', 0.0),
                        annualized_return=strategy.performance_metrics.get('annualized_return', 0.0),
                        volatility=strategy.performance_metrics.get('volatility', 0.0),
                        sharpe_ratio=strategy.performance_metrics.get('sharpe_ratio', 0.0),
                        max_drawdown=strategy.performance_metrics.get('max_drawdown', 0.0),
                        win_rate=strategy.performance_metrics.get('win_rate', 0.0),
                        profit_factor=strategy.performance_metrics.get('profit_factor', 0.0),
                        calmar_ratio=strategy.performance_metrics.get('calmar_ratio', 0.0),
                        sortino_ratio=strategy.performance_metrics.get('sortino_ratio', 0.0),
                        trades_count=strategy.trades_count,
                        avg_trade_duration=strategy.performance_metrics.get('avg_trade_duration', 0.0)
                    )
                
                return {
                    'status': 'success',
                    'all_performance': all_performance,
                    'total_strategies': len(all_performance),
                    'message': f'Performance retrieved for {len(all_performance)} strategies'
                }
                
        except Exception as e:
            logger.error(f"Failed to get strategy performance: {e}")
            return {
                'status': 'error',
                'message': f'Failed to get strategy performance: {str(e)}'
            }
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get comprehensive portfolio summary."""
        try:
            # Calculate current allocation
            current_allocation = self.calculate_portfolio_allocation()
            
            # Get strategy performance
            performance_result = self.get_strategy_performance()
            
            # Calculate portfolio metrics
            total_strategies = len(self.strategies)
            active_strategies = len([s for s in self.strategies.values() if s.is_active])
            total_pnl = sum(strategy.total_pnl for strategy in self.strategies.values())
            total_trades = sum(strategy.trades_count for strategy in self.strategies.values())
            
            return {
                'status': 'success',
                'portfolio_summary': {
                    'total_capital': self.current_capital,
                    'total_strategies': total_strategies,
                    'active_strategies': active_strategies,
                    'total_pnl': total_pnl,
                    'total_trades': total_trades,
                    'current_allocation': current_allocation,
                    'allocation_method': self.allocation_method.value,
                    'rebalancing_frequency': self.rebalancing_frequency.value,
                    'last_rebalance': max([s.last_rebalance for s in self.strategies.values()]) if self.strategies else None
                },
                'strategy_performance': performance_result.get('all_performance', {}),
                'message': 'Portfolio summary generated successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to get portfolio summary: {e}")
            return {
                'status': 'error',
                'message': f'Failed to get portfolio summary: {str(e)}'
            }

# Example usage and testing
def test_multi_strategy_portfolio():
    """Test multi-strategy portfolio management system."""
    print("🧪 Testing Multi-Strategy Portfolio Management System...")
    
    # Create portfolio manager
    portfolio_manager = MultiStrategyPortfolioManager(initial_capital=100000.0)
    
    # Create sample strategies
    strategies = [
        Strategy(
            name="Momentum Strategy",
            strategy_type=StrategyType.MOMENTUM,
            weight=0.0,
            performance_metrics={
                'total_return': 0.15,
                'annualized_return': 0.12,
                'volatility': 0.18,
                'sharpe_ratio': 0.67,
                'max_drawdown': 0.08,
                'win_rate': 0.58,
                'profit_factor': 1.45,
                'calmar_ratio': 1.5,
                'sortino_ratio': 0.89,
                'var_95': 0.04,
                'cvar_95': 0.06,
                'beta': 1.2,
                'avg_trade_duration': 5.2
            }
        ),
        Strategy(
            name="Mean Reversion Strategy",
            strategy_type=StrategyType.MEAN_REVERSION,
            weight=0.0,
            performance_metrics={
                'total_return': 0.08,
                'annualized_return': 0.10,
                'volatility': 0.12,
                'sharpe_ratio': 0.83,
                'max_drawdown': 0.05,
                'win_rate': 0.65,
                'profit_factor': 1.85,
                'calmar_ratio': 2.0,
                'sortino_ratio': 1.12,
                'var_95': 0.03,
                'cvar_95': 0.04,
                'beta': 0.8,
                'avg_trade_duration': 3.8
            }
        ),
        Strategy(
            name="ML-Based Strategy",
            strategy_type=StrategyType.ML_BASED,
            weight=0.0,
            performance_metrics={
                'total_return': 0.22,
                'annualized_return': 0.18,
                'volatility': 0.25,
                'sharpe_ratio': 0.72,
                'max_drawdown': 0.12,
                'win_rate': 0.62,
                'profit_factor': 1.68,
                'calmar_ratio': 1.5,
                'sortino_ratio': 0.95,
                'var_95': 0.06,
                'cvar_95': 0.09,
                'beta': 1.1,
                'avg_trade_duration': 7.5
            }
        )
    ]
    
    # Add strategies to portfolio
    for strategy in strategies:
        result = portfolio_manager.add_strategy(strategy)
        print(f"  • Added {strategy.name}: {'✅' if result['status'] == 'success' else '❌'}")
    
    print(f"  • Total strategies: {len(portfolio_manager.strategies)}")
    
    # Test different allocation methods
    allocation_methods = [
        AllocationMethod.EQUAL_WEIGHT,
        AllocationMethod.RISK_PARITY,
        AllocationMethod.KELLY_OPTIMAL,
        AllocationMethod.MEAN_VARIANCE,
        AllocationMethod.MAXIMUM_SHARPE,
        AllocationMethod.MINIMUM_VARIANCE
    ]
    
    print("  • Testing allocation methods...")
    for method in allocation_methods:
        allocation = portfolio_manager.calculate_portfolio_allocation(method)
        print(f"    ✅ {method.value}: {len(allocation.strategy_weights)} strategies allocated")
        print(f"        - Expected Return: {allocation.expected_return:.2%}")
        print(f"        - Expected Volatility: {allocation.expected_volatility:.2%}")
        print(f"        - Sharpe Ratio: {allocation.sharpe_ratio:.3f}")
        print(f"        - Max Drawdown: {allocation.max_drawdown:.2%}")
    
    # Test rebalancing
    rebalance_result = portfolio_manager.rebalance_portfolio(AllocationMethod.RISK_PARITY)
    if rebalance_result['status'] == 'success':
        print(f"  • Portfolio rebalanced: ✅")
        allocation = rebalance_result['allocation']
        print(f"    - Total Weight: {allocation.total_weight:.2%}")
        print(f"    - Strategy Weights: {allocation.strategy_weights}")
    
    # Get strategy performance
    performance_result = portfolio_manager.get_strategy_performance()
    if performance_result['status'] == 'success':
        print(f"  • Strategy performance: ✅ {performance_result['total_strategies']} strategies")
    
    # Get portfolio summary
    summary_result = portfolio_manager.get_portfolio_summary()
    if summary_result['status'] == 'success':
        print(f"  • Portfolio summary: ✅")
        summary = summary_result['portfolio_summary']
        print(f"    - Total Capital: ${summary['total_capital']:,.2f}")
        print(f"    - Active Strategies: {summary['active_strategies']}")
        print(f"    - Total PnL: ${summary['total_pnl']:,.2f}")
        print(f"    - Total Trades: {summary['total_trades']}")
    
    print("✅ Multi-Strategy Portfolio Management System test completed!")
    
    return portfolio_manager

if __name__ == "__main__":
    test_multi_strategy_portfolio()
