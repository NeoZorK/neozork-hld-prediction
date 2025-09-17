"""
Advanced Risk Management System
Dynamic hedging, portfolio optimization, stress testing
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

class RiskType(Enum):
    """Risk type enumeration"""
    MARKET = "market"
    CREDIT = "credit"
    LIQUIDITY = "liquidity"
    OPERATIONAL = "operational"
    CONCENTRATION = "concentration"
    CURRENCY = "currency"
    INTEREST_RATE = "interest_rate"
    VOLATILITY = "volatility"

class HedgeType(Enum):
    """Hedge type enumeration"""
    STATIC = "static"
    DYNAMIC = "dynamic"
    DELTA_NEUTRAL = "delta_neutral"
    GAMMA_NEUTRAL = "gamma_neutral"
    VEGA_NEUTRAL = "vega_neutral"
    PORTFOLIO_INSURANCE = "portfolio_insurance"

class OptimizationMethod(Enum):
    """Optimization method enumeration"""
    MEAN_VARIANCE = "mean_variance"
    BLACK_LITTERMAN = "black_litterman"
    RISK_PARITY = "risk_parity"
    MAXIMUM_SHARPE = "maximum_sharpe"
    MINIMUM_VARIANCE = "minimum_variance"
    EQUAL_WEIGHT = "equal_weight"
    KELLY_OPTIMAL = "kelly_optimal"

class StressTestType(Enum):
    """Stress test type enumeration"""
    HISTORICAL = "historical"
    MONTE_CARLO = "monte_carlo"
    SCENARIO = "scenario"
    SENSITIVITY = "sensitivity"
    REGIME_CHANGE = "regime_change"

@dataclass
class RiskMetrics:
    """Risk metrics"""
    portfolio_id: str
    var_95: float
    var_99: float
    cvar_95: float
    cvar_99: float
    max_drawdown: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    beta: float
    tracking_error: float
    information_ratio: float
    volatility: float
    skewness: float
    kurtosis: float
    calculated_at: datetime

@dataclass
class HedgePosition:
    """Hedge position"""
    hedge_id: str
    portfolio_id: str
    hedge_type: HedgeType
    underlying_asset: str
    hedge_asset: str
    hedge_ratio: float
    notional_amount: float
    current_value: float
    delta: float
    gamma: float
    vega: float
    theta: float
    created_at: datetime
    updated_at: datetime

@dataclass
class OptimizationResult:
    """Portfolio optimization result"""
    optimization_id: str
    method: OptimizationMethod
    target_return: float
    target_volatility: float
    optimal_weights: Dict[str, float]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float
    diversification_ratio: float
    concentration_risk: float
    created_at: datetime

@dataclass
class StressTestResult:
    """Stress test result"""
    stress_test_id: str
    stress_test_type: StressTestType
    scenario_name: str
    portfolio_value_before: float
    portfolio_value_after: float
    portfolio_loss: float
    loss_percentage: float
    var_breach: bool
    max_drawdown: float
    recovery_time: Optional[float]
    created_at: datetime

class DynamicHedgingEngine:
    """Dynamic hedging engine"""
    
    def __init__(self):
        self.hedge_positions = {}
        self.hedge_history = []
        self.hedge_ratios = {}
        
    async def create_hedge_position(self, portfolio_id: str, hedge_type: HedgeType,
                                  underlying_asset: str, hedge_asset: str,
                                  notional_amount: float) -> str:
        """Create a hedge position"""
        hedge_id = str(uuid.uuid4())
        
        # Calculate initial hedge ratio
        hedge_ratio = await self._calculate_hedge_ratio(hedge_type, underlying_asset, hedge_asset)
        
        # Create hedge position
        hedge_position = HedgePosition(
            hedge_id=hedge_id,
            portfolio_id=portfolio_id,
            hedge_type=hedge_type,
            underlying_asset=underlying_asset,
            hedge_asset=hedge_asset,
            hedge_ratio=hedge_ratio,
            notional_amount=notional_amount,
            current_value=notional_amount * hedge_ratio,
            delta=0.0,
            gamma=0.0,
            vega=0.0,
            theta=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.hedge_positions[hedge_id] = hedge_position
        self.hedge_ratios[hedge_id] = hedge_ratio
        
        logger.info(f"Created hedge position: {hedge_type.value} for {underlying_asset}")
        return hedge_id
    
    async def _calculate_hedge_ratio(self, hedge_type: HedgeType, underlying_asset: str, hedge_asset: str) -> float:
        """Calculate hedge ratio"""
        if hedge_type == HedgeType.DELTA_NEUTRAL:
            return np.random.uniform(0.8, 1.2)
        elif hedge_type == HedgeType.GAMMA_NEUTRAL:
            return np.random.uniform(0.5, 1.5)
        elif hedge_type == HedgeType.VEGA_NEUTRAL:
            return np.random.uniform(0.7, 1.3)
        else:
            return 1.0
    
    async def update_hedge_ratio(self, hedge_id: str, market_data: Dict[str, Any]) -> bool:
        """Update hedge ratio based on market conditions"""
        if hedge_id not in self.hedge_positions:
            return False
        
        hedge_position = self.hedge_positions[hedge_id]
        
        if hedge_position.hedge_type == HedgeType.DYNAMIC:
            volatility = market_data.get('volatility', 0.2)
            correlation = market_data.get('correlation', 0.8)
            
            new_hedge_ratio = correlation * (1 + volatility * 0.1)
            hedge_position.hedge_ratio = new_hedge_ratio
            hedge_position.current_value = hedge_position.notional_amount * new_hedge_ratio
            
            hedge_position.delta = np.random.uniform(-1, 1)
            hedge_position.gamma = np.random.uniform(-0.1, 0.1)
            hedge_position.vega = np.random.uniform(-0.05, 0.05)
            hedge_position.theta = np.random.uniform(-0.01, 0.01)
            
            hedge_position.updated_at = datetime.now()
            
            self.hedge_history.append({
                'hedge_id': hedge_id,
                'old_ratio': self.hedge_ratios[hedge_id],
                'new_ratio': new_hedge_ratio,
                'timestamp': datetime.now(),
                'market_data': market_data
            })
            
            self.hedge_ratios[hedge_id] = new_hedge_ratio
            
            logger.info(f"Updated hedge ratio for {hedge_id}: {new_hedge_ratio:.4f}")
            return True
        
        return False
    
    async def calculate_hedge_effectiveness(self, hedge_id: str, portfolio_returns: List[float],
                                          hedge_returns: List[float]) -> Dict[str, float]:
        """Calculate hedge effectiveness"""
        if len(portfolio_returns) != len(hedge_returns) or len(portfolio_returns) < 2:
            return {'effectiveness': 0.0, 'correlation': 0.0}
        
        correlation = np.corrcoef(portfolio_returns, hedge_returns)[0, 1]
        
        portfolio_returns = np.array(portfolio_returns)
        hedge_returns = np.array(hedge_returns)
        
        slope = np.corrcoef(portfolio_returns, hedge_returns)[0, 1] * (np.std(portfolio_returns) / np.std(hedge_returns))
        intercept = np.mean(portfolio_returns) - slope * np.mean(hedge_returns)
        
        predicted_returns = slope * hedge_returns + intercept
        ss_res = np.sum((portfolio_returns - predicted_returns) ** 2)
        ss_tot = np.sum((portfolio_returns - np.mean(portfolio_returns)) ** 2)
        
        effectiveness = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return {
            'effectiveness': effectiveness,
            'correlation': correlation,
            'slope': slope,
            'intercept': intercept
        }
    
    async def get_hedge_summary(self, portfolio_id: str) -> Dict[str, Any]:
        """Get hedge summary for portfolio"""
        portfolio_hedges = [h for h in self.hedge_positions.values() if h.portfolio_id == portfolio_id]
        
        if not portfolio_hedges:
            return {'total_hedges': 0}
        
        total_notional = sum(h.notional_amount for h in portfolio_hedges)
        total_value = sum(h.current_value for h in portfolio_hedges)
        
        hedge_types = {}
        for hedge in portfolio_hedges:
            hedge_type = hedge.hedge_type.value
            hedge_types[hedge_type] = hedge_types.get(hedge_type, 0) + 1
        
        return {
            'total_hedges': len(portfolio_hedges),
            'total_notional': total_notional,
            'total_value': total_value,
            'hedge_types': hedge_types,
            'avg_hedge_ratio': np.mean([h.hedge_ratio for h in portfolio_hedges]),
            'total_delta': sum(h.delta for h in portfolio_hedges),
            'total_gamma': sum(h.gamma for h in portfolio_hedges),
            'total_vega': sum(h.vega for h in portfolio_hedges)
        }

class PortfolioOptimizer:
    """Portfolio optimization engine"""
    
    def __init__(self):
        self.optimization_history = []
        self.optimization_results = {}
        
    async def optimize_portfolio(self, returns: pd.DataFrame, method: OptimizationMethod,
                               target_return: Optional[float] = None,
                               target_volatility: Optional[float] = None,
                               risk_free_rate: float = 0.02) -> OptimizationResult:
        """Optimize portfolio using specified method"""
        optimization_id = str(uuid.uuid4())
        
        expected_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252
        
        n_assets = len(returns.columns)
        
        if method == OptimizationMethod.MEAN_VARIANCE:
            weights = await self._mean_variance_optimization(expected_returns, cov_matrix, target_return)
        elif method == OptimizationMethod.RISK_PARITY:
            weights = await self._risk_parity_optimization(cov_matrix)
        elif method == OptimizationMethod.MAXIMUM_SHARPE:
            weights = await self._maximum_sharpe_optimization(expected_returns, cov_matrix, risk_free_rate)
        elif method == OptimizationMethod.MINIMUM_VARIANCE:
            weights = await self._minimum_variance_optimization(cov_matrix)
        elif method == OptimizationMethod.EQUAL_WEIGHT:
            weights = {asset: 1.0/n_assets for asset in returns.columns}
        else:
            raise ValueError(f"Unsupported optimization method: {method}")
        
        portfolio_return = sum(weights[asset] * expected_returns[asset] for asset in returns.columns)
        portfolio_variance = sum(
            weights[asset1] * weights[asset2] * cov_matrix.loc[asset1, asset2]
            for asset1 in returns.columns for asset2 in returns.columns
        )
        portfolio_volatility = np.sqrt(portfolio_variance)
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0
        
        weighted_volatilities = sum(weights[asset] * np.sqrt(cov_matrix.loc[asset, asset]) for asset in returns.columns)
        diversification_ratio = weighted_volatilities / portfolio_volatility if portfolio_volatility > 0 else 0
        
        concentration_risk = sum(w**2 for w in weights.values())
        
        result = OptimizationResult(
            optimization_id=optimization_id,
            method=method,
            target_return=target_return or portfolio_return,
            target_volatility=target_volatility or portfolio_volatility,
            optimal_weights=weights,
            expected_return=portfolio_return,
            expected_volatility=portfolio_volatility,
            sharpe_ratio=sharpe_ratio,
            diversification_ratio=diversification_ratio,
            concentration_risk=concentration_risk,
            created_at=datetime.now()
        )
        
        self.optimization_results[optimization_id] = result
        self.optimization_history.append(result)
        
        logger.info(f"Portfolio optimized using {method.value}: Sharpe ratio = {sharpe_ratio:.4f}")
        return result
    
    async def _mean_variance_optimization(self, expected_returns: pd.Series, cov_matrix: pd.DataFrame,
                                        target_return: Optional[float]) -> Dict[str, float]:
        """Mean-variance optimization"""
        n_assets = len(expected_returns)
        
        if target_return is None:
            target_return = expected_returns.mean()
        
        base_weight = 1.0 / n_assets
        weights = {}
        
        for i, asset in enumerate(expected_returns.index):
            adjustment = (expected_returns[asset] - expected_returns.mean()) / expected_returns.std() * 0.1
            weights[asset] = max(0, base_weight + adjustment)
        
        total_weight = sum(weights.values())
        weights = {asset: weight/total_weight for asset, weight in weights.items()}
        
        return weights
    
    async def _risk_parity_optimization(self, cov_matrix: pd.DataFrame) -> Dict[str, float]:
        """Risk parity optimization"""
        volatilities = np.sqrt(np.diag(cov_matrix))
        inv_vol_weights = 1.0 / volatilities
        inv_vol_weights = inv_vol_weights / np.sum(inv_vol_weights)
        
        weights = {asset: weight for asset, weight in zip(cov_matrix.index, inv_vol_weights)}
        return weights
    
    async def _maximum_sharpe_optimization(self, expected_returns: pd.Series, cov_matrix: pd.DataFrame,
                                         risk_free_rate: float) -> Dict[str, float]:
        """Maximum Sharpe ratio optimization"""
        excess_returns = expected_returns - risk_free_rate
        
        volatilities = np.sqrt(np.diag(cov_matrix))
        sharpe_weights = excess_returns / volatilities
        sharpe_weights = sharpe_weights / np.sum(sharpe_weights)
        
        weights = {asset: weight for asset, weight in zip(cov_matrix.index, sharpe_weights)}
        return weights
    
    async def _minimum_variance_optimization(self, cov_matrix: pd.DataFrame) -> Dict[str, float]:
        """Minimum variance optimization"""
        volatilities = np.sqrt(np.diag(cov_matrix))
        inv_vol_weights = 1.0 / volatilities
        inv_vol_weights = inv_vol_weights / np.sum(inv_vol_weights)
        
        weights = {asset: weight for asset, weight in zip(cov_matrix.index, inv_vol_weights)}
        return weights

class StressTestingEngine:
    """Stress testing engine"""
    
    def __init__(self):
        self.stress_tests = {}
        self.stress_scenarios = {}
        
    async def create_stress_scenario(self, scenario_name: str, scenario_type: StressTestType,
                                   parameters: Dict[str, Any]) -> str:
        """Create a stress test scenario"""
        scenario_id = str(uuid.uuid4())
        
        scenario = {
            'scenario_id': scenario_id,
            'scenario_name': scenario_name,
            'scenario_type': scenario_type,
            'parameters': parameters,
            'created_at': datetime.now()
        }
        
        self.stress_scenarios[scenario_id] = scenario
        logger.info(f"Created stress scenario: {scenario_name}")
        return scenario_id
    
    async def run_stress_test(self, portfolio_data: Dict[str, Any], scenario_id: str) -> StressTestResult:
        """Run stress test on portfolio"""
        if scenario_id not in self.stress_scenarios:
            raise ValueError(f"Stress scenario {scenario_id} not found")
        
        scenario = self.stress_scenarios[scenario_id]
        stress_test_id = str(uuid.uuid4())
        
        portfolio_value_before = portfolio_data.get('total_value', 1000000)
        portfolio_value_after = await self._apply_stress_scenario(portfolio_data, scenario)
        
        portfolio_loss = portfolio_value_before - portfolio_value_after
        loss_percentage = (portfolio_loss / portfolio_value_before) * 100
        
        var_95 = portfolio_data.get('var_95', portfolio_value_before * 0.05)
        var_breach = portfolio_loss > var_95
        
        max_drawdown = loss_percentage / 100
        
        recovery_time = None
        if loss_percentage > 10:
            recovery_time = np.random.uniform(30, 365)
        
        result = StressTestResult(
            stress_test_id=stress_test_id,
            stress_test_type=scenario['scenario_type'],
            scenario_name=scenario['scenario_name'],
            portfolio_value_before=portfolio_value_before,
            portfolio_value_after=portfolio_value_after,
            portfolio_loss=portfolio_loss,
            loss_percentage=loss_percentage,
            var_breach=var_breach,
            max_drawdown=max_drawdown,
            recovery_time=recovery_time,
            created_at=datetime.now()
        )
        
        self.stress_tests[stress_test_id] = result
        logger.info(f"Stress test completed: {scenario['scenario_name']} - {loss_percentage:.2f}% loss")
        return result
    
    async def _apply_stress_scenario(self, portfolio_data: Dict[str, Any], scenario: Dict[str, Any]) -> float:
        """Apply stress scenario to portfolio"""
        portfolio_value = portfolio_data.get('total_value', 1000000)
        scenario_type = scenario['scenario_type']
        parameters = scenario['parameters']
        
        if scenario_type == StressTestType.HISTORICAL:
            historical_shock = parameters.get('historical_shock', 0.2)
            return portfolio_value * (1 - historical_shock)
        elif scenario_type == StressTestType.MONTE_CARLO:
            volatility_shock = parameters.get('volatility_shock', 0.3)
            shock = np.random.normal(0, volatility_shock)
            return portfolio_value * (1 - abs(shock))
        elif scenario_type == StressTestType.SCENARIO:
            market_shock = parameters.get('market_shock', 0.15)
            sector_shock = parameters.get('sector_shock', 0.25)
            total_shock = (market_shock + sector_shock) / 2
            return portfolio_value * (1 - total_shock)
        elif scenario_type == StressTestType.SENSITIVITY:
            sensitivity_factor = parameters.get('sensitivity_factor', 0.1)
            return portfolio_value * (1 - sensitivity_factor)
        elif scenario_type == StressTestType.REGIME_CHANGE:
            regime_shock = parameters.get('regime_shock', 0.2)
            return portfolio_value * (1 - regime_shock)
        else:
            return portfolio_value * 0.9
    
    async def run_comprehensive_stress_tests(self, portfolio_data: Dict[str, Any]) -> List[StressTestResult]:
        """Run comprehensive stress tests"""
        scenarios = [
            ('Market Crash 2008', StressTestType.HISTORICAL, {'historical_shock': 0.4}),
            ('High Volatility', StressTestType.MONTE_CARLO, {'volatility_shock': 0.5}),
            ('Sector Crisis', StressTestType.SCENARIO, {'market_shock': 0.2, 'sector_shock': 0.4}),
            ('Interest Rate Shock', StressTestType.SENSITIVITY, {'sensitivity_factor': 0.15}),
            ('Regime Change', StressTestType.REGIME_CHANGE, {'regime_shock': 0.25})
        ]
        
        results = []
        
        for scenario_name, scenario_type, parameters in scenarios:
            try:
                scenario_id = await self.create_stress_scenario(scenario_name, scenario_type, parameters)
                result = await self.run_stress_test(portfolio_data, scenario_id)
                results.append(result)
            except Exception as e:
                logger.error(f"Error running stress test {scenario_name}: {e}")
        
        return results
    
    async def get_stress_test_summary(self) -> Dict[str, Any]:
        """Get stress test summary"""
        if not self.stress_tests:
            return {'total_tests': 0}
        
        results = list(self.stress_tests.values())
        
        avg_loss = np.mean([r.loss_percentage for r in results])
        max_loss = np.max([r.loss_percentage for r in results])
        var_breaches = sum(1 for r in results if r.var_breach)
        
        return {
            'total_tests': len(results),
            'average_loss': avg_loss,
            'maximum_loss': max_loss,
            'var_breaches': var_breaches,
            'breach_rate': var_breaches / len(results) if results else 0,
            'scenarios_tested': len(self.stress_scenarios)
        }

class AdvancedRiskManager:
    """Main advanced risk management system"""
    
    def __init__(self):
        self.hedging_engine = DynamicHedgingEngine()
        self.portfolio_optimizer = PortfolioOptimizer()
        self.stress_testing_engine = StressTestingEngine()
        self.risk_metrics_history = []
        
    async def calculate_risk_metrics(self, portfolio_data: Dict[str, Any], 
                                   returns: pd.Series) -> RiskMetrics:
        """Calculate comprehensive risk metrics"""
        portfolio_id = portfolio_data.get('portfolio_id', 'default')
        
        var_95 = np.percentile(returns, 5)
        var_99 = np.percentile(returns, 1)
        cvar_95 = returns[returns <= var_95].mean()
        cvar_99 = returns[returns <= var_99].mean()
        
        cumulative_returns = (1 + returns).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdowns = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdowns.min()
        
        mean_return = returns.mean() * 252
        volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = mean_return / volatility if volatility > 0 else 0
        
        downside_returns = returns[returns < 0]
        downside_volatility = downside_returns.std() * np.sqrt(252)
        sortino_ratio = mean_return / downside_volatility if downside_volatility > 0 else 0
        
        calmar_ratio = mean_return / abs(max_drawdown) if max_drawdown != 0 else 0
        
        beta = 1.0
        tracking_error = volatility * 0.8
        information_ratio = (mean_return - 0.02) / tracking_error if tracking_error > 0 else 0
        
        skewness = returns.skew()
        kurtosis = returns.kurtosis()
        
        risk_metrics = RiskMetrics(
            portfolio_id=portfolio_id,
            var_95=var_95,
            var_99=var_99,
            cvar_95=cvar_95,
            cvar_99=cvar_99,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            beta=beta,
            tracking_error=tracking_error,
            information_ratio=information_ratio,
            volatility=volatility,
            skewness=skewness,
            kurtosis=kurtosis,
            calculated_at=datetime.now()
        )
        
        self.risk_metrics_history.append(risk_metrics)
        logger.info(f"Calculated risk metrics for portfolio {portfolio_id}")
        return risk_metrics
    
    async def create_hedge_strategy(self, portfolio_id: str, risk_metrics: RiskMetrics,
                                  hedge_type: HedgeType) -> str:
        """Create hedge strategy based on risk metrics"""
        if risk_metrics.var_95 < -0.05:
            notional_amount = 1000000
        elif risk_metrics.var_95 < -0.02:
            notional_amount = 500000
        else:
            notional_amount = 100000
        
        hedge_id = await self.hedging_engine.create_hedge_position(
            portfolio_id=portfolio_id,
            hedge_type=hedge_type,
            underlying_asset='PORTFOLIO',
            hedge_asset='HEDGE_INSTRUMENT',
            notional_amount=notional_amount
        )
        
        logger.info(f"Created hedge strategy for portfolio {portfolio_id}")
        return hedge_id
    
    async def optimize_portfolio_risk(self, returns: pd.DataFrame, 
                                    target_volatility: float = 0.15) -> OptimizationResult:
        """Optimize portfolio for risk management"""
        result = await self.portfolio_optimizer.optimize_portfolio(
            returns=returns,
            method=OptimizationMethod.MINIMUM_VARIANCE,
            target_volatility=target_volatility
        )
        
        logger.info(f"Portfolio optimized for risk: volatility = {result.expected_volatility:.4f}")
        return result
    
    async def run_risk_assessment(self, portfolio_data: Dict[str, Any], 
                                returns: pd.Series) -> Dict[str, Any]:
        """Run comprehensive risk assessment"""
        risk_metrics = await self.calculate_risk_metrics(portfolio_data, returns)
        stress_results = await self.stress_testing_engine.run_comprehensive_stress_tests(portfolio_data)
        hedge_summary = await self.hedging_engine.get_hedge_summary(portfolio_data.get('portfolio_id', 'default'))
        stress_summary = await self.stress_testing_engine.get_stress_test_summary()
        
        assessment = {
            'risk_metrics': asdict(risk_metrics),
            'stress_tests': [asdict(result) for result in stress_results],
            'hedge_summary': hedge_summary,
            'stress_summary': stress_summary,
            'risk_level': self._assess_risk_level(risk_metrics),
            'recommendations': self._generate_risk_recommendations(risk_metrics, stress_results)
        }
        
        logger.info(f"Risk assessment completed for portfolio {portfolio_data.get('portfolio_id', 'default')}")
        return assessment
    
    def _assess_risk_level(self, risk_metrics: RiskMetrics) -> str:
        """Assess overall risk level"""
        risk_score = 0
        
        if risk_metrics.var_95 < -0.1:
            risk_score += 3
        elif risk_metrics.var_95 < -0.05:
            risk_score += 2
        elif risk_metrics.var_95 < -0.02:
            risk_score += 1
        
        if risk_metrics.max_drawdown < -0.2:
            risk_score += 3
        elif risk_metrics.max_drawdown < -0.1:
            risk_score += 2
        elif risk_metrics.max_drawdown < -0.05:
            risk_score += 1
        
        if risk_metrics.volatility > 0.3:
            risk_score += 2
        elif risk_metrics.volatility > 0.2:
            risk_score += 1
        
        if risk_score >= 6:
            return 'HIGH'
        elif risk_score >= 3:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _generate_risk_recommendations(self, risk_metrics: RiskMetrics, 
                                     stress_results: List[StressTestResult]) -> List[str]:
        """Generate risk management recommendations"""
        recommendations = []
        
        if risk_metrics.var_95 < -0.05:
            recommendations.append("Consider reducing position sizes due to high VaR")
        
        if risk_metrics.max_drawdown < -0.1:
            recommendations.append("Implement stop-loss mechanisms to limit drawdowns")
        
        if risk_metrics.volatility > 0.25:
            recommendations.append("Consider volatility hedging strategies")
        
        high_loss_tests = [r for r in stress_results if r.loss_percentage > 20]
        if high_loss_tests:
            recommendations.append("Portfolio vulnerable to stress scenarios - consider diversification")
        
        if risk_metrics.sharpe_ratio < 0.5:
            recommendations.append("Low risk-adjusted returns - review strategy allocation")
        
        return recommendations
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """Get risk management system summary"""
        return {
            'total_hedges': len(self.hedging_engine.hedge_positions),
            'hedge_adjustments': len(self.hedging_engine.hedge_history),
            'optimization_runs': len(self.portfolio_optimizer.optimization_history),
            'stress_tests': len(self.stress_testing_engine.stress_tests),
            'risk_assessments': len(self.risk_metrics_history),
            'last_update': datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of AdvancedRiskManager"""
    risk_manager = AdvancedRiskManager()
    
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    n_assets = 5
    returns_data = {}
    for i in range(n_assets):
        asset_returns = np.random.normal(0.001, 0.02, len(dates))
        returns_data[f'Asset_{i+1}'] = asset_returns
    
    returns_df = pd.DataFrame(returns_data, index=dates)
    portfolio_returns = returns_df.mean(axis=1)
    
    portfolio_data = {
        'portfolio_id': 'test_portfolio',
        'total_value': 1000000,
        'var_95': -0.03,
        'var_99': -0.05
    }
    
    risk_metrics = await risk_manager.calculate_risk_metrics(portfolio_data, portfolio_returns)
    print(f"Risk metrics calculated: VaR 95% = {risk_metrics.var_95:.4f}")
    
    hedge_id = await risk_manager.create_hedge_strategy(
        portfolio_data['portfolio_id'], risk_metrics, HedgeType.DYNAMIC
    )
    print(f"Created hedge strategy: {hedge_id}")
    
    optimization_result = await risk_manager.optimize_portfolio_risk(returns_df)
    print(f"Portfolio optimized: Sharpe ratio = {optimization_result.sharpe_ratio:.4f}")
    
    risk_assessment = await risk_manager.run_risk_assessment(portfolio_data, portfolio_returns)
    print(f"Risk assessment: {risk_assessment['risk_level']} risk level")
    print(f"Recommendations: {len(risk_assessment['recommendations'])} recommendations")
    
    summary = risk_manager.get_risk_summary()
    print(f"Risk management summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())
