# -*- coding: utf-8 -*-
"""
Advanced Risk Management System for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive risk management and position sizing capabilities.
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, Any, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import scipy.stats as stats
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskMetric(Enum):
    """Risk metric types."""
    VAR = "var"
    CVAR = "cvar"
    MAX_DRAWDOWN = "max_drawdown"
    SHARPE_RATIO = "sharpe_ratio"
    SORTINO_RATIO = "sortino_ratio"
    CALMAR_RATIO = "calmar_ratio"
    VOLATILITY = "volatility"
    BETA = "beta"
    CORRELATION = "correlation"

class PositionSizingMethod(Enum):
    """Position sizing methods."""
    FIXED = "fixed"
    KELLY = "kelly"
    VOLATILITY_TARGET = "volatility_target"
    RISK_PARITY = "risk_parity"
    MAXIMUM_DRAWDOWN = "maximum_drawdown"
    EQUAL_WEIGHT = "equal_weight"

class RiskLevel(Enum):
    """Risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass
class RiskLimits:
    """Risk limits configuration."""
    max_position_size: float = 0.1  # 10% of portfolio
    max_daily_loss: float = 0.02   # 2% daily loss limit
    max_drawdown: float = 0.15     # 15% maximum drawdown
    max_correlation: float = 0.7   # Maximum correlation between positions
    max_leverage: float = 1.0      # Maximum leverage
    var_limit: float = 0.05        # 5% VaR limit
    cvar_limit: float = 0.08       # 8% CVaR limit

@dataclass
class Position:
    """Position information."""
    symbol: str
    quantity: float
    entry_price: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    realized_pnl: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    risk_metrics: Dict[str, float] = field(default_factory=dict)

@dataclass
class PortfolioRisk:
    """Portfolio risk metrics."""
    total_value: float
    total_pnl: float
    var_95: float
    var_99: float
    cvar_95: float
    cvar_99: float
    max_drawdown: float
    current_drawdown: float
    volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    beta: float
    correlation_matrix: pd.DataFrame
    risk_contribution: Dict[str, float]

class AdvancedRiskManager:
    """Advanced risk management system."""
    
    def __init__(self, risk_limits: RiskLimits = None):
        self.risk_limits = risk_limits or RiskLimits()
        self.positions = {}
        self.portfolio_history = []
        self.risk_metrics_history = []
        self.correlation_matrix = None
        self.beta_coefficients = {}
        
    def add_position(self, position: Position):
        """Add a position to the portfolio."""
        self.positions[position.symbol] = position
        logger.info(f"Position added: {position.symbol} - {position.quantity} @ {position.current_price}")
    
    def remove_position(self, symbol: str):
        """Remove a position from the portfolio."""
        if symbol in self.positions:
            del self.positions[symbol]
            logger.info(f"Position removed: {symbol}")
    
    def update_position(self, symbol: str, current_price: float):
        """Update position with current price."""
        if symbol in self.positions:
            position = self.positions[symbol]
            position.current_price = current_price
            position.market_value = position.quantity * current_price
            position.unrealized_pnl = (current_price - position.entry_price) * position.quantity
            
            # Update risk metrics
            position.risk_metrics = self._calculate_position_risk_metrics(position)
    
    def calculate_portfolio_risk(self, market_data: pd.DataFrame = None) -> PortfolioRisk:
        """Calculate comprehensive portfolio risk metrics."""
        try:
            if not self.positions:
                return self._empty_portfolio_risk()
            
            # Calculate basic portfolio metrics
            total_value = sum(pos.market_value for pos in self.positions.values())
            total_pnl = sum(pos.unrealized_pnl + pos.realized_pnl for pos in self.positions.values())
            
            # Calculate returns if market data provided
            if market_data is not None:
                returns = self._calculate_portfolio_returns(market_data)
            else:
                # Use position returns as proxy
                returns = self._calculate_position_returns()
            
            # Calculate risk metrics
            var_95, var_99 = self._calculate_var(returns)
            cvar_95, cvar_99 = self._calculate_cvar(returns)
            max_drawdown, current_drawdown = self._calculate_drawdown(returns)
            volatility = self._calculate_volatility(returns)
            sharpe_ratio = self._calculate_sharpe_ratio(returns)
            sortino_ratio = self._calculate_sortino_ratio(returns)
            calmar_ratio = self._calculate_calmar_ratio(returns, max_drawdown)
            
            # Calculate correlation matrix
            correlation_matrix = self._calculate_correlation_matrix()
            
            # Calculate risk contribution
            risk_contribution = self._calculate_risk_contribution()
            
            # Calculate beta
            beta = self._calculate_portfolio_beta()
            
            portfolio_risk = PortfolioRisk(
                total_value=total_value,
                total_pnl=total_pnl,
                var_95=var_95,
                var_99=var_99,
                cvar_95=cvar_95,
                cvar_99=cvar_99,
                max_drawdown=max_drawdown,
                current_drawdown=current_drawdown,
                volatility=volatility,
                sharpe_ratio=sharpe_ratio,
                sortino_ratio=sortino_ratio,
                calmar_ratio=calmar_ratio,
                beta=beta,
                correlation_matrix=correlation_matrix,
                risk_contribution=risk_contribution
            )
            
            # Store in history
            self.risk_metrics_history.append({
                'timestamp': datetime.now(),
                'metrics': portfolio_risk
            })
            
            return portfolio_risk
            
        except Exception as e:
            logger.error(f"Failed to calculate portfolio risk: {e}")
            return self._empty_portfolio_risk()
    
    def _empty_portfolio_risk(self) -> PortfolioRisk:
        """Return empty portfolio risk metrics."""
        return PortfolioRisk(
            total_value=0.0,
            total_pnl=0.0,
            var_95=0.0,
            var_99=0.0,
            cvar_95=0.0,
            cvar_99=0.0,
            max_drawdown=0.0,
            current_drawdown=0.0,
            volatility=0.0,
            sharpe_ratio=0.0,
            sortino_ratio=0.0,
            calmar_ratio=0.0,
            beta=0.0,
            correlation_matrix=pd.DataFrame(),
            risk_contribution={}
        )
    
    def _calculate_portfolio_returns(self, market_data: pd.DataFrame) -> pd.Series:
        """Calculate portfolio returns from market data."""
        try:
            # Calculate weighted returns for each position
            weighted_returns = []
            
            for symbol, position in self.positions.items():
                if symbol in market_data.columns:
                    returns = market_data[symbol].pct_change().dropna()
                    weight = position.market_value / sum(pos.market_value for pos in self.positions.values())
                    weighted_returns.append(returns * weight)
            
            if weighted_returns:
                portfolio_returns = pd.concat(weighted_returns, axis=1).sum(axis=1)
                return portfolio_returns.dropna()
            else:
                return pd.Series(dtype=float)
                
        except Exception as e:
            logger.error(f"Failed to calculate portfolio returns: {e}")
            return pd.Series(dtype=float)
    
    def _calculate_position_returns(self) -> pd.Series:
        """Calculate position returns as proxy for portfolio returns."""
        try:
            returns = []
            for position in self.positions.values():
                if position.entry_price > 0:
                    return_pct = (position.current_price - position.entry_price) / position.entry_price
                    returns.append(return_pct)
            
            return pd.Series(returns) if returns else pd.Series(dtype=float)
            
        except Exception as e:
            logger.error(f"Failed to calculate position returns: {e}")
            return pd.Series(dtype=float)
    
    def _calculate_var(self, returns: pd.Series, confidence_levels: List[float] = [0.95, 0.99]) -> Tuple[float, float]:
        """Calculate Value at Risk (VaR)."""
        try:
            if len(returns) == 0:
                return 0.0, 0.0
            
            var_95 = np.percentile(returns, (1 - 0.95) * 100)
            var_99 = np.percentile(returns, (1 - 0.99) * 100)
            
            return abs(var_95), abs(var_99)
            
        except Exception as e:
            logger.error(f"Failed to calculate VaR: {e}")
            return 0.0, 0.0
    
    def _calculate_cvar(self, returns: pd.Series, confidence_levels: List[float] = [0.95, 0.99]) -> Tuple[float, float]:
        """Calculate Conditional Value at Risk (CVaR)."""
        try:
            if len(returns) == 0:
                return 0.0, 0.0
            
            var_95 = np.percentile(returns, (1 - 0.95) * 100)
            var_99 = np.percentile(returns, (1 - 0.99) * 100)
            
            cvar_95 = returns[returns <= var_95].mean() if len(returns[returns <= var_95]) > 0 else 0.0
            cvar_99 = returns[returns <= var_99].mean() if len(returns[returns <= var_99]) > 0 else 0.0
            
            return abs(cvar_95), abs(cvar_99)
            
        except Exception as e:
            logger.error(f"Failed to calculate CVaR: {e}")
            return 0.0, 0.0
    
    def _calculate_drawdown(self, returns: pd.Series) -> Tuple[float, float]:
        """Calculate maximum and current drawdown."""
        try:
            if len(returns) == 0:
                return 0.0, 0.0
            
            cumulative = (1 + returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            
            max_drawdown = drawdown.min()
            current_drawdown = drawdown.iloc[-1] if len(drawdown) > 0 else 0.0
            
            return abs(max_drawdown), abs(current_drawdown)
            
        except Exception as e:
            logger.error(f"Failed to calculate drawdown: {e}")
            return 0.0, 0.0
    
    def _calculate_volatility(self, returns: pd.Series) -> float:
        """Calculate portfolio volatility."""
        try:
            if len(returns) == 0:
                return 0.0
            
            return returns.std() * np.sqrt(252)  # Annualized
            
        except Exception as e:
            logger.error(f"Failed to calculate volatility: {e}")
            return 0.0
    
    def _calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio."""
        try:
            if len(returns) == 0 or returns.std() == 0:
                return 0.0
            
            excess_returns = returns.mean() - risk_free_rate / 252
            return excess_returns / returns.std() * np.sqrt(252)
            
        except Exception as e:
            logger.error(f"Failed to calculate Sharpe ratio: {e}")
            return 0.0
    
    def _calculate_sortino_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sortino ratio."""
        try:
            if len(returns) == 0:
                return 0.0
            
            excess_returns = returns.mean() - risk_free_rate / 252
            downside_returns = returns[returns < 0]
            
            if len(downside_returns) == 0 or downside_returns.std() == 0:
                return 0.0
            
            downside_deviation = downside_returns.std() * np.sqrt(252)
            return excess_returns / downside_deviation * np.sqrt(252)
            
        except Exception as e:
            logger.error(f"Failed to calculate Sortino ratio: {e}")
            return 0.0
    
    def _calculate_calmar_ratio(self, returns: pd.Series, max_drawdown: float) -> float:
        """Calculate Calmar ratio."""
        try:
            if len(returns) == 0 or max_drawdown == 0:
                return 0.0
            
            annual_return = returns.mean() * 252
            return annual_return / max_drawdown
            
        except Exception as e:
            logger.error(f"Failed to calculate Calmar ratio: {e}")
            return 0.0
    
    def _calculate_correlation_matrix(self) -> pd.DataFrame:
        """Calculate correlation matrix between positions."""
        try:
            if len(self.positions) < 2:
                return pd.DataFrame()
            
            # Create returns matrix for correlation calculation
            returns_data = {}
            for symbol, position in self.positions.items():
                # Use position PnL as proxy for returns
                returns_data[symbol] = [position.unrealized_pnl / position.market_value if position.market_value > 0 else 0]
            
            returns_df = pd.DataFrame(returns_data)
            correlation_matrix = returns_df.corr()
            
            return correlation_matrix
            
        except Exception as e:
            logger.error(f"Failed to calculate correlation matrix: {e}")
            return pd.DataFrame()
    
    def _calculate_risk_contribution(self) -> Dict[str, float]:
        """Calculate risk contribution of each position."""
        try:
            risk_contribution = {}
            total_risk = 0.0
            
            for symbol, position in self.positions.items():
                # Calculate individual position risk
                position_risk = abs(position.unrealized_pnl) / position.market_value if position.market_value > 0 else 0
                risk_contribution[symbol] = position_risk
                total_risk += position_risk
            
            # Normalize to percentages
            if total_risk > 0:
                for symbol in risk_contribution:
                    risk_contribution[symbol] = (risk_contribution[symbol] / total_risk) * 100
            
            return risk_contribution
            
        except Exception as e:
            logger.error(f"Failed to calculate risk contribution: {e}")
            return {}
    
    def _calculate_portfolio_beta(self) -> float:
        """Calculate portfolio beta."""
        try:
            if not self.beta_coefficients:
                return 1.0  # Default beta
            
            # Calculate weighted beta
            total_value = sum(pos.market_value for pos in self.positions.values())
            if total_value == 0:
                return 1.0
            
            weighted_beta = 0.0
            for symbol, position in self.positions.items():
                beta = self.beta_coefficients.get(symbol, 1.0)
                weight = position.market_value / total_value
                weighted_beta += beta * weight
            
            return weighted_beta
            
        except Exception as e:
            logger.error(f"Failed to calculate portfolio beta: {e}")
            return 1.0
    
    def _calculate_position_risk_metrics(self, position: Position) -> Dict[str, float]:
        """Calculate risk metrics for individual position."""
        try:
            metrics = {}
            
            # Position size as percentage of portfolio
            total_value = sum(pos.market_value for pos in self.positions.values())
            if total_value > 0:
                metrics['position_size_pct'] = (position.market_value / total_value) * 100
            
            # PnL as percentage
            if position.entry_price > 0:
                metrics['pnl_pct'] = (position.unrealized_pnl / (position.entry_price * position.quantity)) * 100
            
            # Risk metrics
            metrics['unrealized_pnl'] = position.unrealized_pnl
            metrics['market_value'] = position.market_value
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate position risk metrics: {e}")
            return {}
    
    def check_risk_limits(self, portfolio_risk: PortfolioRisk) -> Dict[str, Any]:
        """Check if portfolio violates risk limits."""
        try:
            violations = []
            warnings = []
            
            # Check maximum drawdown
            if portfolio_risk.max_drawdown > self.risk_limits.max_drawdown:
                violations.append(f"Maximum drawdown {portfolio_risk.max_drawdown:.2%} exceeds limit {self.risk_limits.max_drawdown:.2%}")
            
            # Check VaR limits
            if portfolio_risk.var_95 > self.risk_limits.var_limit:
                violations.append(f"VaR 95% {portfolio_risk.var_95:.2%} exceeds limit {self.risk_limits.var_limit:.2%}")
            
            if portfolio_risk.cvar_95 > self.risk_limits.cvar_limit:
                violations.append(f"CVaR 95% {portfolio_risk.cvar_95:.2%} exceeds limit {self.risk_limits.cvar_limit:.2%}")
            
            # Check position sizes
            for symbol, position in self.positions.items():
                position_size = position.market_value / portfolio_risk.total_value if portfolio_risk.total_value > 0 else 0
                if position_size > self.risk_limits.max_position_size:
                    violations.append(f"Position {symbol} size {position_size:.2%} exceeds limit {self.risk_limits.max_position_size:.2%}")
            
            # Check correlations
            if not portfolio_risk.correlation_matrix.empty:
                for i, symbol1 in enumerate(portfolio_risk.correlation_matrix.index):
                    for j, symbol2 in enumerate(portfolio_risk.correlation_matrix.columns):
                        if i < j:  # Avoid duplicates
                            correlation = abs(portfolio_risk.correlation_matrix.loc[symbol1, symbol2])
                            if correlation > self.risk_limits.max_correlation:
                                warnings.append(f"High correlation {correlation:.2f} between {symbol1} and {symbol2}")
            
            return {
                'status': 'success',
                'violations': violations,
                'warnings': warnings,
                'risk_level': self._determine_risk_level(portfolio_risk),
                'message': f'Risk check completed: {len(violations)} violations, {len(warnings)} warnings'
            }
            
        except Exception as e:
            logger.error(f"Failed to check risk limits: {e}")
            return {
                'status': 'error',
                'message': f'Failed to check risk limits: {str(e)}'
            }
    
    def _determine_risk_level(self, portfolio_risk: PortfolioRisk) -> RiskLevel:
        """Determine overall risk level."""
        try:
            risk_score = 0
            
            # Drawdown risk
            if portfolio_risk.max_drawdown > 0.1:
                risk_score += 2
            elif portfolio_risk.max_drawdown > 0.05:
                risk_score += 1
            
            # VaR risk
            if portfolio_risk.var_95 > 0.05:
                risk_score += 2
            elif portfolio_risk.var_95 > 0.03:
                risk_score += 1
            
            # Volatility risk
            if portfolio_risk.volatility > 0.3:
                risk_score += 2
            elif portfolio_risk.volatility > 0.2:
                risk_score += 1
            
            # Determine risk level
            if risk_score >= 5:
                return RiskLevel.VERY_HIGH
            elif risk_score >= 3:
                return RiskLevel.HIGH
            elif risk_score >= 1:
                return RiskLevel.MEDIUM
            else:
                return RiskLevel.LOW
                
        except Exception as e:
            logger.error(f"Failed to determine risk level: {e}")
            return RiskLevel.MEDIUM
    
    def optimize_position_sizing(self, method: PositionSizingMethod, 
                               target_risk: float = 0.02) -> Dict[str, float]:
        """Optimize position sizing using various methods."""
        try:
            if not self.positions:
                return {}
            
            if method == PositionSizingMethod.EQUAL_WEIGHT:
                return self._equal_weight_sizing()
            elif method == PositionSizingMethod.VOLATILITY_TARGET:
                return self._volatility_target_sizing(target_risk)
            elif method == PositionSizingMethod.RISK_PARITY:
                return self._risk_parity_sizing()
            elif method == PositionSizingMethod.KELLY:
                return self._kelly_sizing()
            else:
                return self._fixed_sizing()
                
        except Exception as e:
            logger.error(f"Failed to optimize position sizing: {e}")
            return {}
    
    def _equal_weight_sizing(self) -> Dict[str, float]:
        """Equal weight position sizing."""
        try:
            num_positions = len(self.positions)
            if num_positions == 0:
                return {}
            
            equal_weight = 1.0 / num_positions
            return {symbol: equal_weight for symbol in self.positions.keys()}
            
        except Exception as e:
            logger.error(f"Failed to calculate equal weight sizing: {e}")
            return {}
    
    def _volatility_target_sizing(self, target_risk: float) -> Dict[str, float]:
        """Volatility target position sizing."""
        try:
            # This is a simplified implementation
            # In practice, you'd use historical volatility data
            weights = {}
            total_volatility = 0.0
            
            for symbol, position in self.positions.items():
                # Use position PnL volatility as proxy
                volatility = abs(position.unrealized_pnl) / position.market_value if position.market_value > 0 else 0.1
                weights[symbol] = target_risk / volatility if volatility > 0 else 0.1
                total_volatility += weights[symbol]
            
            # Normalize weights
            if total_volatility > 0:
                for symbol in weights:
                    weights[symbol] = weights[symbol] / total_volatility
            
            return weights
            
        except Exception as e:
            logger.error(f"Failed to calculate volatility target sizing: {e}")
            return {}
    
    def _risk_parity_sizing(self) -> Dict[str, float]:
        """Risk parity position sizing."""
        try:
            # Simplified risk parity implementation
            weights = {}
            total_risk = 0.0
            
            for symbol, position in self.positions.items():
                # Use position risk as inverse weight
                risk = abs(position.unrealized_pnl) / position.market_value if position.market_value > 0 else 0.1
                weights[symbol] = 1.0 / risk if risk > 0 else 1.0
                total_risk += weights[symbol]
            
            # Normalize weights
            if total_risk > 0:
                for symbol in weights:
                    weights[symbol] = weights[symbol] / total_risk
            
            return weights
            
        except Exception as e:
            logger.error(f"Failed to calculate risk parity sizing: {e}")
            return {}
    
    def _kelly_sizing(self) -> Dict[str, float]:
        """Kelly criterion position sizing."""
        try:
            # Simplified Kelly implementation
            weights = {}
            
            for symbol, position in self.positions.items():
                # Use position PnL as win/loss ratio
                if position.entry_price > 0:
                    win_rate = max(0.5, min(0.8, (position.unrealized_pnl / (position.entry_price * position.quantity)) + 0.5))
                    avg_win = abs(position.unrealized_pnl) if position.unrealized_pnl > 0 else 0.01
                    avg_loss = abs(position.unrealized_pnl) if position.unrealized_pnl < 0 else 0.01
                    
                    kelly_fraction = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
                    weights[symbol] = max(0, min(0.25, kelly_fraction))  # Cap at 25%
                else:
                    weights[symbol] = 0.1
            
            return weights
            
        except Exception as e:
            logger.error(f"Failed to calculate Kelly sizing: {e}")
            return {}
    
    def _fixed_sizing(self) -> Dict[str, float]:
        """Fixed position sizing."""
        try:
            fixed_weight = self.risk_limits.max_position_size
            return {symbol: fixed_weight for symbol in self.positions.keys()}
            
        except Exception as e:
            logger.error(f"Failed to calculate fixed sizing: {e}")
            return {}
    
    def get_risk_report(self) -> Dict[str, Any]:
        """Generate comprehensive risk report."""
        try:
            portfolio_risk = self.calculate_portfolio_risk()
            risk_check = self.check_risk_limits(portfolio_risk)
            
            return {
                'status': 'success',
                'portfolio_risk': {
                    'total_value': portfolio_risk.total_value,
                    'total_pnl': portfolio_risk.total_pnl,
                    'var_95': portfolio_risk.var_95,
                    'var_99': portfolio_risk.var_99,
                    'cvar_95': portfolio_risk.cvar_95,
                    'cvar_99': portfolio_risk.cvar_99,
                    'max_drawdown': portfolio_risk.max_drawdown,
                    'current_drawdown': portfolio_risk.current_drawdown,
                    'volatility': portfolio_risk.volatility,
                    'sharpe_ratio': portfolio_risk.sharpe_ratio,
                    'sortino_ratio': portfolio_risk.sortino_ratio,
                    'calmar_ratio': portfolio_risk.calmar_ratio,
                    'beta': portfolio_risk.beta
                },
                'risk_check': risk_check,
                'positions': {
                    symbol: {
                        'quantity': pos.quantity,
                        'market_value': pos.market_value,
                        'unrealized_pnl': pos.unrealized_pnl,
                        'risk_metrics': pos.risk_metrics
                    }
                    for symbol, pos in self.positions.items()
                },
                'risk_contribution': portfolio_risk.risk_contribution,
                'message': 'Risk report generated successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to generate risk report: {e}")
            return {
                'status': 'error',
                'message': f'Failed to generate risk report: {str(e)}'
            }

# Example usage and testing
def test_advanced_risk_management():
    """Test advanced risk management system."""
    print("🧪 Testing Advanced Risk Management System...")
    
    # Create risk manager
    risk_limits = RiskLimits(
        max_position_size=0.15,
        max_daily_loss=0.03,
        max_drawdown=0.20,
        max_correlation=0.8,
        var_limit=0.06,
        cvar_limit=0.10
    )
    
    risk_manager = AdvancedRiskManager(risk_limits)
    
    # Add sample positions
    positions = [
        Position(
            symbol="BTCUSDT",
            quantity=0.5,
            entry_price=45000,
            current_price=46000,
            market_value=23000,
            unrealized_pnl=500
        ),
        Position(
            symbol="ETHUSDT",
            quantity=10,
            entry_price=3000,
            current_price=3100,
            market_value=31000,
            unrealized_pnl=1000
        ),
        Position(
            symbol="ADAUSDT",
            quantity=1000,
            entry_price=0.5,
            current_price=0.48,
            market_value=480,
            unrealized_pnl=-20
        )
    ]
    
    for position in positions:
        risk_manager.add_position(position)
    
    print(f"  • Added {len(positions)} positions: ✅")
    
    # Calculate portfolio risk
    portfolio_risk = risk_manager.calculate_portfolio_risk()
    print(f"  • Portfolio risk calculated: ✅")
    print(f"    - Total Value: ${portfolio_risk.total_value:,.2f}")
    print(f"    - Total PnL: ${portfolio_risk.total_pnl:,.2f}")
    print(f"    - VaR 95%: {portfolio_risk.var_95:.2%}")
    print(f"    - CVaR 95%: {portfolio_risk.cvar_95:.2%}")
    print(f"    - Max Drawdown: {portfolio_risk.max_drawdown:.2%}")
    print(f"    - Volatility: {portfolio_risk.volatility:.2%}")
    print(f"    - Sharpe Ratio: {portfolio_risk.sharpe_ratio:.3f}")
    
    # Check risk limits
    risk_check = risk_manager.check_risk_limits(portfolio_risk)
    print(f"  • Risk limits check: ✅")
    print(f"    - Risk Level: {risk_check['risk_level'].value}")
    print(f"    - Violations: {len(risk_check['violations'])}")
    print(f"    - Warnings: {len(risk_check['warnings'])}")
    
    # Test position sizing optimization
    print("  • Testing position sizing optimization...")
    
    sizing_methods = [
        PositionSizingMethod.EQUAL_WEIGHT,
        PositionSizingMethod.VOLATILITY_TARGET,
        PositionSizingMethod.RISK_PARITY,
        PositionSizingMethod.KELLY
    ]
    
    for method in sizing_methods:
        weights = risk_manager.optimize_position_sizing(method)
        print(f"    ✅ {method.value}: {len(weights)} positions optimized")
    
    # Generate risk report
    risk_report = risk_manager.get_risk_report()
    if risk_report['status'] == 'success':
        print(f"  • Risk report generated: ✅")
        print(f"    - Positions: {len(risk_report['positions'])}")
        print(f"    - Risk contribution calculated: ✅")
    
    print("✅ Advanced Risk Management System test completed!")
    
    return risk_manager

if __name__ == "__main__":
    test_advanced_risk_management()
