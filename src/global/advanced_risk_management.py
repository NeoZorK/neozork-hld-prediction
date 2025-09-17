"""
Advanced Risk Management System
Portfolio risk, market risk, operational risk, stress testing
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import json
from scipy import stats
from scipy.optimize import minimize
import uuid

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

class RiskLevel(Enum):
    """Risk level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Position:
    """Trading position"""
    position_id: str
    symbol: str
    quantity: float
    entry_price: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    realized_pnl: float
    timestamp: datetime
    risk_metrics: Dict[str, float]

@dataclass
class RiskMetrics:
    """Risk metrics structure"""
    var_95: float
    var_99: float
    cvar_95: float
    cvar_99: float
    max_drawdown: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    volatility: float
    beta: float
    correlation: float
    concentration_risk: float
    liquidity_risk: float

@dataclass
class StressTestScenario:
    """Stress test scenario"""
    scenario_id: str
    name: str
    description: str
    market_shock: Dict[str, float]  # Symbol -> shock percentage
    correlation_changes: Dict[str, float]
    volatility_multiplier: float
    liquidity_impact: float
    probability: float
    severity: RiskLevel

class PortfolioRiskManager:
    """Portfolio risk management"""
    
    def __init__(self):
        self.positions = {}
        self.risk_metrics = {}
        self.correlation_matrix = {}
        self.volatility_data = {}
        self.risk_limits = {
            "max_var_95": 0.05,  # 5% VaR limit
            "max_var_99": 0.02,  # 2% VaR limit
            "max_drawdown": 0.15,  # 15% max drawdown
            "max_concentration": 0.3,  # 30% max position size
            "max_correlation": 0.7  # 70% max correlation
        }
        
    async def add_position(self, position: Position) -> bool:
        """Add position to portfolio"""
        self.positions[position.position_id] = position
        await self.update_risk_metrics()
        logger.info(f"Added position {position.position_id}")
        return True
    
    async def update_position(self, position_id: str, current_price: float) -> bool:
        """Update position with current price"""
        if position_id not in self.positions:
            return False
        
        position = self.positions[position_id]
        position.current_price = current_price
        position.market_value = position.quantity * current_price
        position.unrealized_pnl = (current_price - position.entry_price) * position.quantity
        
        await self.update_risk_metrics()
        return True
    
    async def calculate_var(self, confidence_level: float = 0.95, 
                          lookback_days: int = 252) -> float:
        """Calculate Value at Risk (VaR)"""
        if not self.positions:
            return 0.0
        
        # Get portfolio returns (simplified)
        portfolio_returns = await self.get_portfolio_returns(lookback_days)
        
        if len(portfolio_returns) < 30:  # Need minimum data
            return 0.0
        
        # Calculate VaR using historical simulation
        var_percentile = (1 - confidence_level) * 100
        var = np.percentile(portfolio_returns, var_percentile)
        
        return abs(var)
    
    async def calculate_cvar(self, confidence_level: float = 0.95, 
                           lookback_days: int = 252) -> float:
        """Calculate Conditional Value at Risk (CVaR)"""
        if not self.positions:
            return 0.0
        
        portfolio_returns = await self.get_portfolio_returns(lookback_days)
        
        if len(portfolio_returns) < 30:
            return 0.0
        
        # Calculate CVaR (Expected Shortfall)
        var_threshold = np.percentile(portfolio_returns, (1 - confidence_level) * 100)
        tail_returns = portfolio_returns[portfolio_returns <= var_threshold]
        
        if len(tail_returns) == 0:
            return 0.0
        
        cvar = np.mean(tail_returns)
        return abs(cvar)
    
    async def calculate_max_drawdown(self, lookback_days: int = 252) -> float:
        """Calculate maximum drawdown"""
        if not self.positions:
            return 0.0
        
        portfolio_values = await self.get_portfolio_values(lookback_days)
        
        if len(portfolio_values) < 2:
            return 0.0
        
        # Calculate running maximum
        running_max = np.maximum.accumulate(portfolio_values)
        
        # Calculate drawdown
        drawdown = (portfolio_values - running_max) / running_max
        
        return abs(np.min(drawdown))
    
    async def calculate_sharpe_ratio(self, risk_free_rate: float = 0.02, 
                                   lookback_days: int = 252) -> float:
        """Calculate Sharpe ratio"""
        if not self.positions:
            return 0.0
        
        portfolio_returns = await self.get_portfolio_returns(lookback_days)
        
        if len(portfolio_returns) < 30:
            return 0.0
        
        excess_returns = portfolio_returns - risk_free_rate / 252  # Daily risk-free rate
        sharpe = np.mean(excess_returns) / np.std(portfolio_returns) * np.sqrt(252)
        
        return sharpe
    
    async def calculate_concentration_risk(self) -> float:
        """Calculate concentration risk (Herfindahl index)"""
        if not self.positions:
            return 0.0
        
        total_value = sum(pos.market_value for pos in self.positions.values())
        
        if total_value == 0:
            return 0.0
        
        # Calculate Herfindahl index
        weights = [pos.market_value / total_value for pos in self.positions.values()]
        herfindahl = sum(w**2 for w in weights)
        
        return herfindahl
    
    async def calculate_correlation_risk(self) -> Dict[str, float]:
        """Calculate correlation risk between positions"""
        if len(self.positions) < 2:
            return {}
        
        correlation_risks = {}
        position_list = list(self.positions.values())
        
        for i, pos1 in enumerate(position_list):
            for j, pos2 in enumerate(position_list[i+1:], i+1):
                # Simplified correlation calculation
                correlation = await self.get_correlation(pos1.symbol, pos2.symbol)
                correlation_risks[f"{pos1.symbol}_{pos2.symbol}"] = correlation
        
        return correlation_risks
    
    async def update_risk_metrics(self):
        """Update all risk metrics"""
        if not self.positions:
            return
        
        # Calculate all risk metrics
        var_95 = await self.calculate_var(0.95)
        var_99 = await self.calculate_var(0.99)
        cvar_95 = await self.calculate_cvar(0.95)
        cvar_99 = await self.calculate_cvar(0.99)
        max_drawdown = await self.calculate_max_drawdown()
        sharpe_ratio = await self.calculate_sharpe_ratio()
        concentration_risk = await self.calculate_concentration_risk()
        correlation_risks = await self.calculate_correlation_risk()
        
        # Calculate volatility
        portfolio_returns = await self.get_portfolio_returns()
        volatility = np.std(portfolio_returns) * np.sqrt(252) if len(portfolio_returns) > 1 else 0.0
        
        # Calculate Sortino ratio
        sortino_ratio = await self.calculate_sortino_ratio()
        
        # Calculate Calmar ratio
        calmar_ratio = await self.calculate_calmar_ratio()
        
        self.risk_metrics = RiskMetrics(
            var_95=var_95,
            var_99=var_99,
            cvar_95=cvar_95,
            cvar_99=cvar_99,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            volatility=volatility,
            beta=0.0,  # Simplified
            correlation=0.0,  # Simplified
            concentration_risk=concentration_risk,
            liquidity_risk=0.0  # Simplified
        )
    
    async def get_portfolio_returns(self, lookback_days: int = 252) -> np.ndarray:
        """Get portfolio returns (simplified simulation)"""
        # In real implementation, this would use actual historical data
        # For now, generate synthetic returns
        np.random.seed(42)  # For reproducibility
        returns = np.random.normal(0.001, 0.02, lookback_days)  # 0.1% daily return, 2% volatility
        return returns
    
    async def get_portfolio_values(self, lookback_days: int = 252) -> np.ndarray:
        """Get portfolio values over time"""
        returns = await self.get_portfolio_returns(lookback_days)
        initial_value = 100000  # $100k initial portfolio
        values = [initial_value]
        
        for ret in returns:
            values.append(values[-1] * (1 + ret))
        
        return np.array(values[1:])  # Remove initial value
    
    async def get_correlation(self, symbol1: str, symbol2: str) -> float:
        """Get correlation between two symbols (simplified)"""
        # In real implementation, this would use actual correlation data
        # For now, return a random correlation
        np.random.seed(hash(symbol1 + symbol2) % 2**32)
        return np.random.uniform(-0.5, 0.8)  # Most correlations are positive
    
    async def calculate_sortino_ratio(self, risk_free_rate: float = 0.02) -> float:
        """Calculate Sortino ratio"""
        portfolio_returns = await self.get_portfolio_returns()
        
        if len(portfolio_returns) < 30:
            return 0.0
        
        excess_returns = portfolio_returns - risk_free_rate / 252
        downside_returns = excess_returns[excess_returns < 0]
        
        if len(downside_returns) == 0:
            return 0.0
        
        downside_deviation = np.std(downside_returns)
        sortino = np.mean(excess_returns) / downside_deviation * np.sqrt(252)
        
        return sortino
    
    async def calculate_calmar_ratio(self) -> float:
        """Calculate Calmar ratio"""
        portfolio_returns = await self.get_portfolio_returns()
        max_drawdown = await self.calculate_max_drawdown()
        
        if len(portfolio_returns) < 30 or max_drawdown == 0:
            return 0.0
        
        annual_return = np.mean(portfolio_returns) * 252
        calmar = annual_return / max_drawdown
        
        return calmar

class StressTestManager:
    """Stress testing manager"""
    
    def __init__(self):
        self.scenarios = {}
        self.stress_test_results = {}
        
    async def create_scenario(self, scenario: StressTestScenario) -> bool:
        """Create stress test scenario"""
        self.scenarios[scenario.scenario_id] = scenario
        logger.info(f"Created stress test scenario: {scenario.name}")
        return True
    
    async def run_stress_test(self, scenario_id: str, portfolio_manager: PortfolioRiskManager) -> Dict[str, Any]:
        """Run stress test on portfolio"""
        if scenario_id not in self.scenarios:
            return {"error": "Scenario not found"}
        
        scenario = self.scenarios[scenario_id]
        
        # Apply market shocks to positions
        stressed_positions = {}
        total_pnl_impact = 0.0
        
        for position_id, position in portfolio_manager.positions.items():
            # Apply market shock if symbol is in scenario
            shock = scenario.market_shock.get(position.symbol, 0.0)
            stressed_price = position.current_price * (1 + shock)
            
            # Calculate P&L impact
            pnl_impact = (stressed_price - position.current_price) * position.quantity
            total_pnl_impact += pnl_impact
            
            stressed_positions[position_id] = {
                "original_price": position.current_price,
                "stressed_price": stressed_price,
                "pnl_impact": pnl_impact,
                "shock_percentage": shock * 100
            }
        
        # Calculate stressed risk metrics
        stressed_var = await self.calculate_stressed_var(portfolio_manager, scenario)
        stressed_drawdown = await self.calculate_stressed_drawdown(portfolio_manager, scenario)
        
        result = {
            "scenario_id": scenario_id,
            "scenario_name": scenario.name,
            "total_pnl_impact": total_pnl_impact,
            "stressed_positions": stressed_positions,
            "stressed_var": stressed_var,
            "stressed_drawdown": stressed_drawdown,
            "liquidity_impact": scenario.liquidity_impact,
            "volatility_impact": scenario.volatility_multiplier,
            "run_timestamp": datetime.now()
        }
        
        self.stress_test_results[scenario_id] = result
        return result
    
    async def calculate_stressed_var(self, portfolio_manager: PortfolioRiskManager, 
                                   scenario: StressTestScenario) -> float:
        """Calculate VaR under stress scenario"""
        # Apply volatility multiplier to returns
        base_returns = await portfolio_manager.get_portfolio_returns()
        stressed_returns = base_returns * scenario.volatility_multiplier
        
        # Calculate stressed VaR
        var_percentile = 5  # 95% VaR
        stressed_var = np.percentile(stressed_returns, var_percentile)
        
        return abs(stressed_var)
    
    async def calculate_stressed_drawdown(self, portfolio_manager: PortfolioRiskManager, 
                                        scenario: StressTestScenario) -> float:
        """Calculate drawdown under stress scenario"""
        # Apply market shocks to portfolio values
        base_values = await portfolio_manager.get_portfolio_values()
        
        # Apply average shock to portfolio values
        avg_shock = np.mean(list(scenario.market_shock.values())) if scenario.market_shock else 0.0
        stressed_values = base_values * (1 + avg_shock)
        
        # Calculate stressed drawdown
        running_max = np.maximum.accumulate(stressed_values)
        drawdown = (stressed_values - running_max) / running_max
        
        return abs(np.min(drawdown))
    
    async def run_scenario_analysis(self, portfolio_manager: PortfolioRiskManager) -> Dict[str, Any]:
        """Run analysis across all scenarios"""
        results = {}
        
        for scenario_id, scenario in self.scenarios.items():
            result = await self.run_stress_test(scenario_id, portfolio_manager)
            results[scenario_id] = result
        
        # Calculate summary statistics
        pnl_impacts = [result["total_pnl_impact"] for result in results.values()]
        var_impacts = [result["stressed_var"] for result in results.values()]
        
        summary = {
            "total_scenarios": len(results),
            "worst_case_pnl": min(pnl_impacts) if pnl_impacts else 0.0,
            "best_case_pnl": max(pnl_impacts) if pnl_impacts else 0.0,
            "average_pnl_impact": np.mean(pnl_impacts) if pnl_impacts else 0.0,
            "max_stressed_var": max(var_impacts) if var_impacts else 0.0,
            "analysis_timestamp": datetime.now()
        }
        
        return {
            "scenario_results": results,
            "summary": summary
        }

class RiskLimitManager:
    """Risk limit management and monitoring"""
    
    def __init__(self):
        self.risk_limits = {}
        self.limit_breaches = []
        self.alert_thresholds = {}
        
    async def set_risk_limits(self, limits: Dict[str, float]) -> bool:
        """Set risk limits"""
        self.risk_limits.update(limits)
        logger.info(f"Set risk limits: {limits}")
        return True
    
    async def check_risk_limits(self, risk_metrics: RiskMetrics) -> Dict[str, Any]:
        """Check if risk limits are breached"""
        breaches = []
        warnings = []
        
        # Check VaR limits
        if risk_metrics.var_95 > self.risk_limits.get("max_var_95", 0.05):
            breaches.append({
                "metric": "var_95",
                "current_value": risk_metrics.var_95,
                "limit": self.risk_limits.get("max_var_95", 0.05),
                "severity": "high"
            })
        
        if risk_metrics.var_99 > self.risk_limits.get("max_var_99", 0.02):
            breaches.append({
                "metric": "var_99",
                "current_value": risk_metrics.var_99,
                "limit": self.risk_limits.get("max_var_99", 0.02),
                "severity": "critical"
            })
        
        # Check drawdown limit
        if risk_metrics.max_drawdown > self.risk_limits.get("max_drawdown", 0.15):
            breaches.append({
                "metric": "max_drawdown",
                "current_value": risk_metrics.max_drawdown,
                "limit": self.risk_limits.get("max_drawdown", 0.15),
                "severity": "high"
            })
        
        # Check concentration limit
        if risk_metrics.concentration_risk > self.risk_limits.get("max_concentration", 0.3):
            breaches.append({
                "metric": "concentration_risk",
                "current_value": risk_metrics.concentration_risk,
                "limit": self.risk_limits.get("max_concentration", 0.3),
                "severity": "medium"
            })
        
        # Check warning thresholds (80% of limits)
        warning_thresholds = {k: v * 0.8 for k, v in self.risk_limits.items()}
        
        if risk_metrics.var_95 > warning_thresholds.get("max_var_95", 0.04):
            warnings.append("VaR 95% approaching limit")
        
        if risk_metrics.max_drawdown > warning_thresholds.get("max_drawdown", 0.12):
            warnings.append("Drawdown approaching limit")
        
        # Log breaches
        if breaches:
            self.limit_breaches.extend(breaches)
        
        return {
            "breaches": breaches,
            "warnings": warnings,
            "check_timestamp": datetime.now(),
            "total_breaches": len(breaches)
        }
    
    async def get_risk_dashboard(self, risk_metrics: RiskMetrics) -> Dict[str, Any]:
        """Get risk dashboard data"""
        limit_check = await self.check_risk_limits(risk_metrics)
        
        return {
            "risk_metrics": asdict(risk_metrics),
            "risk_limits": self.risk_limits,
            "limit_status": limit_check,
            "recent_breaches": self.limit_breaches[-10:],  # Last 10 breaches
            "dashboard_timestamp": datetime.now()
        }

class AdvancedRiskManager:
    """Main advanced risk management system"""
    
    def __init__(self):
        self.portfolio_manager = PortfolioRiskManager()
        self.stress_test_manager = StressTestManager()
        self.risk_limit_manager = RiskLimitManager()
        self.risk_reports = {}
        
    async def initialize_risk_system(self):
        """Initialize risk management system"""
        # Set default risk limits
        default_limits = {
            "max_var_95": 0.05,
            "max_var_99": 0.02,
            "max_drawdown": 0.15,
            "max_concentration": 0.3,
            "max_correlation": 0.7,
            "min_sharpe_ratio": 1.0,
            "max_volatility": 0.3
        }
        
        await self.risk_limit_manager.set_risk_limits(default_limits)
        
        # Create default stress test scenarios
        await self.create_default_scenarios()
        
        logger.info("Risk management system initialized")
    
    async def create_default_scenarios(self):
        """Create default stress test scenarios"""
        # Market crash scenario
        market_crash = StressTestScenario(
            scenario_id="market_crash",
            name="Market Crash",
            description="Global market crash with 30% decline",
            market_shock={"BTC": -0.30, "ETH": -0.35, "BNB": -0.25},
            correlation_changes={"BTC_ETH": 0.9},
            volatility_multiplier=2.0,
            liquidity_impact=0.5,
            probability=0.05,
            severity=RiskLevel.CRITICAL
        )
        
        # Volatility spike scenario
        volatility_spike = StressTestScenario(
            scenario_id="volatility_spike",
            name="Volatility Spike",
            description="Sudden increase in market volatility",
            market_shock={"BTC": -0.15, "ETH": -0.20, "BNB": -0.10},
            correlation_changes={},
            volatility_multiplier=3.0,
            liquidity_impact=0.2,
            probability=0.15,
            severity=RiskLevel.HIGH
        )
        
        # Liquidity crisis scenario
        liquidity_crisis = StressTestScenario(
            scenario_id="liquidity_crisis",
            name="Liquidity Crisis",
            description="Severe liquidity shortage",
            market_shock={"BTC": -0.10, "ETH": -0.12, "BNB": -0.08},
            correlation_changes={},
            volatility_multiplier=1.5,
            liquidity_impact=0.8,
            probability=0.10,
            severity=RiskLevel.HIGH
        )
        
        await self.stress_test_manager.create_scenario(market_crash)
        await self.stress_test_manager.create_scenario(volatility_spike)
        await self.stress_test_manager.create_scenario(liquidity_crisis)
    
    async def add_position(self, symbol: str, quantity: float, entry_price: float) -> str:
        """Add position to portfolio"""
        position_id = str(uuid.uuid4())
        
        position = Position(
            position_id=position_id,
            symbol=symbol,
            quantity=quantity,
            entry_price=entry_price,
            current_price=entry_price,
            market_value=quantity * entry_price,
            unrealized_pnl=0.0,
            realized_pnl=0.0,
            timestamp=datetime.now(),
            risk_metrics={}
        )
        
        await self.portfolio_manager.add_position(position)
        return position_id
    
    async def update_portfolio_prices(self, price_updates: Dict[str, float]):
        """Update portfolio with current prices"""
        for position_id, position in self.portfolio_manager.positions.items():
            if position.symbol in price_updates:
                await self.portfolio_manager.update_position(position_id, price_updates[position.symbol])
    
    async def run_comprehensive_risk_analysis(self) -> Dict[str, Any]:
        """Run comprehensive risk analysis"""
        # Update risk metrics
        await self.portfolio_manager.update_risk_metrics()
        
        # Check risk limits
        limit_check = await self.risk_limit_manager.check_risk_limits(self.portfolio_manager.risk_metrics)
        
        # Run stress tests
        stress_test_results = await self.stress_test_manager.run_scenario_analysis(self.portfolio_manager)
        
        # Generate risk dashboard
        risk_dashboard = await self.risk_limit_manager.get_risk_dashboard(self.portfolio_manager.risk_metrics)
        
        analysis = {
            "timestamp": datetime.now(),
            "portfolio_summary": {
                "total_positions": len(self.portfolio_manager.positions),
                "total_value": sum(pos.market_value for pos in self.portfolio_manager.positions.values()),
                "total_pnl": sum(pos.unrealized_pnl for pos in self.portfolio_manager.positions.values())
            },
            "risk_metrics": asdict(self.portfolio_manager.risk_metrics),
            "limit_check": limit_check,
            "stress_test_results": stress_test_results,
            "risk_dashboard": risk_dashboard
        }
        
        # Store analysis
        analysis_id = str(uuid.uuid4())
        self.risk_reports[analysis_id] = analysis
        
        return analysis
    
    async def generate_risk_report(self, report_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate risk report"""
        if report_type == "comprehensive":
            return await self.run_comprehensive_risk_analysis()
        elif report_type == "stress_test":
            return await self.stress_test_manager.run_scenario_analysis(self.portfolio_manager)
        elif report_type == "limit_check":
            await self.portfolio_manager.update_risk_metrics()
            return await self.risk_limit_manager.get_risk_dashboard(self.portfolio_manager.risk_metrics)
        else:
            return {"error": "Invalid report type"}
    
    def get_summary(self) -> Dict[str, Any]:
        """Get risk management system summary"""
        return {
            "total_positions": len(self.portfolio_manager.positions),
            "total_scenarios": len(self.stress_test_manager.scenarios),
            "risk_reports": len(self.risk_reports),
            "limit_breaches": len(self.risk_limit_manager.limit_breaches),
            "last_update": datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of AdvancedRiskManager"""
    manager = AdvancedRiskManager()
    
    # Initialize system
    await manager.initialize_risk_system()
    
    # Add positions
    btc_position = await manager.add_position("BTC", 0.5, 45000.0)
    eth_position = await manager.add_position("ETH", 2.0, 3000.0)
    bnb_position = await manager.add_position("BNB", 10.0, 300.0)
    
    print(f"Added positions: BTC, ETH, BNB")
    
    # Update prices
    price_updates = {
        "BTC": 46000.0,
        "ETH": 3100.0,
        "BNB": 320.0
    }
    await manager.update_portfolio_prices(price_updates)
    
    # Run comprehensive risk analysis
    risk_analysis = await manager.run_comprehensive_risk_analysis()
    
    print(f"Risk Analysis Results:")
    print(f"Total Portfolio Value: ${risk_analysis['portfolio_summary']['total_value']:,.2f}")
    print(f"Total P&L: ${risk_analysis['portfolio_summary']['total_pnl']:,.2f}")
    print(f"VaR 95%: {risk_analysis['risk_metrics']['var_95']:.4f}")
    print(f"Max Drawdown: {risk_analysis['risk_metrics']['max_drawdown']:.4f}")
    print(f"Sharpe Ratio: {risk_analysis['risk_metrics']['sharpe_ratio']:.2f}")
    print(f"Concentration Risk: {risk_analysis['risk_metrics']['concentration_risk']:.4f}")
    
    # Check limit breaches
    breaches = risk_analysis['limit_check']['breaches']
    if breaches:
        print(f"Risk Limit Breaches: {len(breaches)}")
        for breach in breaches:
            print(f"  - {breach['metric']}: {breach['current_value']:.4f} (limit: {breach['limit']:.4f})")
    else:
        print("No risk limit breaches")
    
    # Stress test results
    stress_results = risk_analysis['stress_test_results']['summary']
    print(f"Stress Test Results:")
    print(f"  Worst Case P&L: ${stress_results['worst_case_pnl']:,.2f}")
    print(f"  Best Case P&L: ${stress_results['best_case_pnl']:,.2f}")
    print(f"  Average P&L Impact: ${stress_results['average_pnl_impact']:,.2f}")
    
    # System summary
    summary = manager.get_summary()
    print(f"System Summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())
