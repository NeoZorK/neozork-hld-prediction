"""
Portfolio Optimizer - Portfolio Optimization Algorithms

This module provides portfolio optimization functionality including
modern portfolio theory, risk parity, and other optimization strategies.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from decimal import Decimal
import numpy as np
import pandas as pd
from scipy.optimize import minimize

from ..models.portfolio_models import Portfolio, Position, AssetType
from ..models.transaction_models import RebalancePlan, RebalanceAction

logger = logging.getLogger(__name__)


class PortfolioOptimizer:
    """Portfolio optimization functionality."""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self.optimization_strategies = {
            'mean_variance': self._mean_variance_optimization,
            'risk_parity': self._risk_parity_optimization,
            'equal_weight': self._equal_weight_optimization,
            'momentum': self._momentum_optimization,
            'minimum_variance': self._minimum_variance_optimization
        }
        
    async def optimize_portfolio(
        self, 
        portfolio: Portfolio, 
        strategy: str = 'mean_variance',
        target_return: Optional[float] = None,
        risk_tolerance: float = 0.5
    ) -> Dict[str, Any]:
        """Optimize portfolio allocation."""
        try:
            if strategy not in self.optimization_strategies:
                raise ValueError(f"Unknown optimization strategy: {strategy}")
            
            # Get historical data
            historical_data = await self._get_historical_data(portfolio)
            
            if not historical_data:
                return self._get_default_optimization_result()
            
            # Calculate expected returns and covariance matrix
            expected_returns = await self._calculate_expected_returns(historical_data)
            covariance_matrix = await self._calculate_covariance_matrix(historical_data)
            
            # Run optimization
            optimal_weights = await self.optimization_strategies[strategy](
                expected_returns, covariance_matrix, target_return, risk_tolerance
            )
            
            # Create optimization result
            result = {
                'strategy': strategy,
                'optimal_weights': optimal_weights,
                'expected_return': float(np.dot(optimal_weights, expected_returns)),
                'expected_volatility': float(np.sqrt(np.dot(optimal_weights, np.dot(covariance_matrix, optimal_weights)))),
                'sharpe_ratio': self._calculate_sharpe_ratio(optimal_weights, expected_returns, covariance_matrix),
                'optimization_metadata': {
                    'target_return': target_return,
                    'risk_tolerance': risk_tolerance,
                    'optimization_date': datetime.now(datetime.UTC).isoformat()
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to optimize portfolio: {e}")
            return self._get_default_optimization_result()
    
    async def create_optimization_plan(
        self, 
        portfolio: Portfolio, 
        strategy: str = 'mean_variance',
        target_return: Optional[float] = None,
        risk_tolerance: float = 0.5
    ) -> RebalancePlan:
        """Create an optimization-based rebalancing plan."""
        try:
            # Get optimization result
            optimization_result = await self.optimize_portfolio(
                portfolio, strategy, target_return, risk_tolerance
            )
            
            # Convert to target allocations
            target_allocations = {}
            for i, asset_id in enumerate(portfolio.get_active_positions()):
                target_allocations[asset_id.asset_id] = optimization_result['optimal_weights'][i]
            
            # Create rebalance plan
            from .rebalancer import PortfolioRebalancer
            rebalancer = PortfolioRebalancer(self.db_manager)
            
            rebalance_plan = await rebalancer.create_rebalance_plan(
                portfolio=portfolio,
                target_allocations=target_allocations,
                strategy='threshold_based',
                rebalance_threshold=0.01
            )
            
            return rebalance_plan
            
        except Exception as e:
            logger.error(f"Failed to create optimization plan: {e}")
            raise
    
    # Optimization strategies
    async def _mean_variance_optimization(
        self, 
        expected_returns: np.ndarray, 
        covariance_matrix: np.ndarray,
        target_return: Optional[float] = None,
        risk_tolerance: float = 0.5
    ) -> np.ndarray:
        """Mean-variance optimization (Markowitz)."""
        try:
            n_assets = len(expected_returns)
            
            # Objective function: minimize portfolio variance
            def objective(weights):
                return np.dot(weights, np.dot(covariance_matrix, weights))
            
            # Constraints
            constraints = [
                {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}  # Weights sum to 1
            ]
            
            if target_return is not None:
                constraints.append({
                    'type': 'eq', 
                    'fun': lambda w: np.dot(w, expected_returns) - target_return
                })
            
            # Bounds: weights between 0 and 1
            bounds = [(0, 1) for _ in range(n_assets)]
            
            # Initial guess: equal weights
            x0 = np.array([1/n_assets] * n_assets)
            
            # Optimize
            result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
            
            if result.success:
                return result.x
            else:
                # Fallback to equal weights
                return np.array([1/n_assets] * n_assets)
                
        except Exception as e:
            logger.error(f"Failed to perform mean-variance optimization: {e}")
            return np.array([1/len(expected_returns)] * len(expected_returns))
    
    async def _risk_parity_optimization(
        self, 
        expected_returns: np.ndarray, 
        covariance_matrix: np.ndarray,
        target_return: Optional[float] = None,
        risk_tolerance: float = 0.5
    ) -> np.ndarray:
        """Risk parity optimization."""
        try:
            n_assets = len(expected_returns)
            
            # Objective function: minimize sum of squared risk contributions
            def objective(weights):
                portfolio_variance = np.dot(weights, np.dot(covariance_matrix, weights))
                risk_contributions = (weights * np.dot(covariance_matrix, weights)) / portfolio_variance
                return np.sum((risk_contributions - 1/n_assets) ** 2)
            
            # Constraints
            constraints = [
                {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}  # Weights sum to 1
            ]
            
            # Bounds: weights between 0 and 1
            bounds = [(0, 1) for _ in range(n_assets)]
            
            # Initial guess: equal weights
            x0 = np.array([1/n_assets] * n_assets)
            
            # Optimize
            result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
            
            if result.success:
                return result.x
            else:
                # Fallback to equal weights
                return np.array([1/n_assets] * n_assets)
                
        except Exception as e:
            logger.error(f"Failed to perform risk parity optimization: {e}")
            return np.array([1/len(expected_returns)] * len(expected_returns))
    
    async def _equal_weight_optimization(
        self, 
        expected_returns: np.ndarray, 
        covariance_matrix: np.ndarray,
        target_return: Optional[float] = None,
        risk_tolerance: float = 0.5
    ) -> np.ndarray:
        """Equal weight optimization."""
        try:
            n_assets = len(expected_returns)
            return np.array([1/n_assets] * n_assets)
            
        except Exception as e:
            logger.error(f"Failed to perform equal weight optimization: {e}")
            return np.array([1/len(expected_returns)] * len(expected_returns))
    
    async def _momentum_optimization(
        self, 
        expected_returns: np.ndarray, 
        covariance_matrix: np.ndarray,
        target_return: Optional[float] = None,
        risk_tolerance: float = 0.5
    ) -> np.ndarray:
        """Momentum-based optimization."""
        try:
            # Weight assets by their recent performance
            # This is a simplified implementation
            n_assets = len(expected_returns)
            
            # Use expected returns as momentum scores
            momentum_scores = expected_returns
            
            # Normalize to get weights
            if np.sum(momentum_scores) > 0:
                weights = momentum_scores / np.sum(momentum_scores)
            else:
                weights = np.array([1/n_assets] * n_assets)
            
            return weights
            
        except Exception as e:
            logger.error(f"Failed to perform momentum optimization: {e}")
            return np.array([1/len(expected_returns)] * len(expected_returns))
    
    async def _minimum_variance_optimization(
        self, 
        expected_returns: np.ndarray, 
        covariance_matrix: np.ndarray,
        target_return: Optional[float] = None,
        risk_tolerance: float = 0.5
    ) -> np.ndarray:
        """Minimum variance optimization."""
        try:
            n_assets = len(expected_returns)
            
            # Objective function: minimize portfolio variance
            def objective(weights):
                return np.dot(weights, np.dot(covariance_matrix, weights))
            
            # Constraints
            constraints = [
                {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}  # Weights sum to 1
            ]
            
            # Bounds: weights between 0 and 1
            bounds = [(0, 1) for _ in range(n_assets)]
            
            # Initial guess: equal weights
            x0 = np.array([1/n_assets] * n_assets)
            
            # Optimize
            result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
            
            if result.success:
                return result.x
            else:
                # Fallback to equal weights
                return np.array([1/n_assets] * n_assets)
                
        except Exception as e:
            logger.error(f"Failed to perform minimum variance optimization: {e}")
            return np.array([1/len(expected_returns)] * len(expected_returns))
    
    # Helper methods
    def _calculate_sharpe_ratio(
        self, 
        weights: np.ndarray, 
        expected_returns: np.ndarray, 
        covariance_matrix: np.ndarray,
        risk_free_rate: float = 0.02
    ) -> float:
        """Calculate Sharpe ratio."""
        try:
            portfolio_return = np.dot(weights, expected_returns)
            portfolio_variance = np.dot(weights, np.dot(covariance_matrix, weights))
            portfolio_volatility = np.sqrt(portfolio_variance)
            
            if portfolio_volatility == 0:
                return 0.0
            
            return float((portfolio_return - risk_free_rate) / portfolio_volatility)
            
        except Exception as e:
            logger.error(f"Failed to calculate Sharpe ratio: {e}")
            return 0.0
    
    def _get_default_optimization_result(self) -> Dict[str, Any]:
        """Get default optimization result."""
        return {
            'strategy': 'equal_weight',
            'optimal_weights': [],
            'expected_return': 0.0,
            'expected_volatility': 0.0,
            'sharpe_ratio': 0.0,
            'optimization_metadata': {
                'target_return': None,
                'risk_tolerance': 0.5,
                'optimization_date': datetime.now(datetime.UTC).isoformat()
            }
        }
    
    # Placeholder methods for data retrieval
    async def _get_historical_data(self, portfolio: Portfolio) -> Optional[pd.DataFrame]:
        """Get historical data for portfolio assets."""
        # This would retrieve historical price data for all assets in the portfolio
        return None
    
    async def _calculate_expected_returns(self, historical_data: pd.DataFrame) -> np.ndarray:
        """Calculate expected returns from historical data."""
        # This would calculate expected returns based on historical performance
        return np.array([])
    
    async def _calculate_covariance_matrix(self, historical_data: pd.DataFrame) -> np.ndarray:
        """Calculate covariance matrix from historical data."""
        # This would calculate the covariance matrix of asset returns
        return np.array([])
