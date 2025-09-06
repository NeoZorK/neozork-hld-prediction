"""
Intelligent Automation System
Automated decision making, self-optimizing systems
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

class AutomationType(Enum):
    """Automation type enumeration"""
    DECISION_MAKING = "decision_making"
    PARAMETER_OPTIMIZATION = "parameter_optimization"
    STRATEGY_ADAPTATION = "strategy_adaptation"
    RISK_MANAGEMENT = "risk_management"
    PORTFOLIO_REBALANCING = "portfolio_rebalancing"
    TRADE_EXECUTION = "trade_execution"
    MONITORING_ALERTS = "monitoring_alerts"
    SYSTEM_MAINTENANCE = "system_maintenance"

class DecisionType(Enum):
    """Decision type enumeration"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    ADJUST_POSITION = "adjust_position"
    CLOSE_POSITION = "close_position"
    OPEN_POSITION = "open_position"
    HEDGE_POSITION = "hedge_position"

class OptimizationObjective(Enum):
    """Optimization objective enumeration"""
    MAXIMIZE_RETURNS = "maximize_returns"
    MINIMIZE_RISK = "minimize_risk"
    MAXIMIZE_SHARPE = "maximize_sharpe"
    MINIMIZE_DRAWDOWN = "minimize_drawdown"
    MAXIMIZE_CALMAR = "maximize_calmar"
    BALANCED = "balanced"

class AutomationStatus(Enum):
    """Automation status enumeration"""
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"
    MAINTENANCE = "maintenance"

@dataclass
class AutomationRule:
    """Automation rule"""
    rule_id: str
    rule_type: AutomationType
    name: str
    description: str
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    priority: int
    enabled: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class AutomationDecision:
    """Automation decision"""
    decision_id: str
    rule_id: str
    decision_type: DecisionType
    confidence: float
    reasoning: str
    parameters: Dict[str, Any]
    timestamp: datetime
    executed: bool
    execution_result: Optional[Dict[str, Any]]

@dataclass
class OptimizationResult:
    """Optimization result"""
    optimization_id: str
    objective: OptimizationObjective
    parameters: Dict[str, Any]
    performance_metrics: Dict[str, float]
    improvement: float
    timestamp: datetime
    iterations: int
    convergence: bool

class DecisionEngine:
    """Automated decision making engine"""
    
    def __init__(self):
        self.rules = {}
        self.decisions = {}
        self.decision_history = []
        self.performance_metrics = {}
        
    async def add_rule(self, rule: AutomationRule) -> str:
        """Add automation rule"""
        self.rules[rule.rule_id] = rule
        logger.info(f"Added automation rule: {rule.name}")
        return rule.rule_id
    
    async def evaluate_conditions(self, rule_id: str, market_data: Dict[str, Any], 
                                 portfolio_data: Dict[str, Any]) -> bool:
        """Evaluate rule conditions"""
        if rule_id not in self.rules:
            return False
        
        rule = self.rules[rule_id]
        if not rule.enabled:
            return False
        
        # Simulate condition evaluation
        conditions_met = 0
        total_conditions = len(rule.conditions)
        
        for condition in rule.conditions:
            condition_type = condition.get("type", "price_threshold")
            
            if condition_type == "price_threshold":
                current_price = market_data.get("price", 0)
                threshold = condition.get("threshold", 0)
                operator = condition.get("operator", "greater_than")
                
                if operator == "greater_than" and current_price > threshold:
                    conditions_met += 1
                elif operator == "less_than" and current_price < threshold:
                    conditions_met += 1
                elif operator == "equals" and current_price == threshold:
                    conditions_met += 1
            
            elif condition_type == "volume_threshold":
                current_volume = market_data.get("volume", 0)
                threshold = condition.get("threshold", 0)
                operator = condition.get("operator", "greater_than")
                
                if operator == "greater_than" and current_volume > threshold:
                    conditions_met += 1
                elif operator == "less_than" and current_volume < threshold:
                    conditions_met += 1
            
            elif condition_type == "technical_indicator":
                indicator_value = market_data.get(condition.get("indicator", "rsi"), 50)
                threshold = condition.get("threshold", 50)
                operator = condition.get("operator", "greater_than")
                
                if operator == "greater_than" and indicator_value > threshold:
                    conditions_met += 1
                elif operator == "less_than" and indicator_value < threshold:
                    conditions_met += 1
            
            elif condition_type == "portfolio_metric":
                metric_value = portfolio_data.get(condition.get("metric", "total_value"), 0)
                threshold = condition.get("threshold", 0)
                operator = condition.get("operator", "greater_than")
                
                if operator == "greater_than" and metric_value > threshold:
                    conditions_met += 1
                elif operator == "less_than" and metric_value < threshold:
                    conditions_met += 1
        
        # Check if all conditions are met
        return conditions_met == total_conditions
    
    async def make_decision(self, rule_id: str, market_data: Dict[str, Any], 
                           portfolio_data: Dict[str, Any]) -> Optional[AutomationDecision]:
        """Make automated decision"""
        if not await self.evaluate_conditions(rule_id, market_data, portfolio_data):
            return None
        
        rule = self.rules[rule_id]
        
        # Simulate decision making
        decision_type = DecisionType.HOLD
        confidence = np.random.uniform(0.6, 0.95)
        
        # Determine decision type based on rule actions
        for action in rule.actions:
            action_type = action.get("type", "hold")
            
            if action_type == "buy":
                decision_type = DecisionType.BUY
                confidence = np.random.uniform(0.7, 0.9)
            elif action_type == "sell":
                decision_type = DecisionType.SELL
                confidence = np.random.uniform(0.7, 0.9)
            elif action_type == "adjust_position":
                decision_type = DecisionType.ADJUST_POSITION
                confidence = np.random.uniform(0.6, 0.8)
        
        decision = AutomationDecision(
            decision_id=str(uuid.uuid4()),
            rule_id=rule_id,
            decision_type=decision_type,
            confidence=confidence,
            reasoning=f"Rule '{rule.name}' triggered with {confidence:.2f} confidence",
            parameters={
                "market_data": market_data,
                "portfolio_data": portfolio_data,
                "rule_priority": rule.priority
            },
            timestamp=datetime.now(),
            executed=False,
            execution_result=None
        )
        
        self.decisions[decision.decision_id] = decision
        self.decision_history.append(decision)
        
        logger.info(f"Made decision: {decision_type.value} with confidence {confidence:.2f}")
        return decision
    
    async def execute_decision(self, decision_id: str) -> Dict[str, Any]:
        """Execute automation decision"""
        if decision_id not in self.decisions:
            raise ValueError(f"Decision {decision_id} not found")
        
        decision = self.decisions[decision_id]
        
        # Simulate decision execution
        execution_result = {
            "success": True,
            "execution_time": datetime.now(),
            "order_id": str(uuid.uuid4()),
            "quantity": np.random.uniform(0.1, 1.0),
            "price": np.random.uniform(100, 200),
            "fees": np.random.uniform(0.001, 0.005),
            "slippage": np.random.uniform(0.0, 0.002)
        }
        
        decision.executed = True
        decision.execution_result = execution_result
        
        logger.info(f"Executed decision {decision_id}: {decision.decision_type.value}")
        return execution_result
    
    async def get_decision_performance(self, rule_id: str) -> Dict[str, Any]:
        """Get decision performance for a rule"""
        rule_decisions = [d for d in self.decision_history if d.rule_id == rule_id]
        
        if not rule_decisions:
            return {"error": "No decisions found for rule"}
        
        executed_decisions = [d for d in rule_decisions if d.executed]
        
        performance = {
            "total_decisions": len(rule_decisions),
            "executed_decisions": len(executed_decisions),
            "execution_rate": len(executed_decisions) / len(rule_decisions) if rule_decisions else 0,
            "average_confidence": np.mean([d.confidence for d in rule_decisions]),
            "decision_types": {},
            "success_rate": 0.0
        }
        
        # Count decision types
        for decision in rule_decisions:
            decision_type = decision.decision_type.value
            performance["decision_types"][decision_type] = performance["decision_types"].get(decision_type, 0) + 1
        
        # Calculate success rate (simplified)
        if executed_decisions:
            successful_executions = sum(1 for d in executed_decisions if d.execution_result and d.execution_result.get("success", False))
            performance["success_rate"] = successful_executions / len(executed_decisions)
        
        return performance

class ParameterOptimizer:
    """Parameter optimization engine"""
    
    def __init__(self):
        self.optimization_history = []
        self.current_parameters = {}
        self.performance_tracker = {}
        
    async def optimize_parameters(self, objective: OptimizationObjective, 
                                 parameter_space: Dict[str, List[Any]], 
                                 evaluation_function: Callable, 
                                 max_iterations: int = 100) -> OptimizationResult:
        """Optimize parameters using various algorithms"""
        optimization_id = str(uuid.uuid4())
        
        logger.info(f"Starting parameter optimization for {objective.value}")
        
        best_parameters = {}
        best_performance = float('-inf') if objective in [OptimizationObjective.MAXIMIZE_RETURNS, 
                                                         OptimizationObjective.MAXIMIZE_SHARPE,
                                                         OptimizationObjective.MAXIMIZE_CALMAR] else float('inf')
        
        convergence = False
        iteration = 0
        
        for iteration in range(max_iterations):
            # Generate parameter combination
            parameters = {}
            for param_name, param_values in parameter_space.items():
                if isinstance(param_values, list):
                    parameters[param_name] = np.random.choice(param_values)
                else:
                    # Assume it's a range
                    parameters[param_name] = np.random.uniform(param_values[0], param_values[1])
            
            # Evaluate performance
            try:
                performance = await evaluation_function(parameters)
                
                # Check if this is the best performance so far
                is_better = False
                if objective in [OptimizationObjective.MAXIMIZE_RETURNS, 
                               OptimizationObjective.MAXIMIZE_SHARPE,
                               OptimizationObjective.MAXIMIZE_CALMAR]:
                    is_better = performance > best_performance
                else:
                    is_better = performance < best_performance
                
                if is_better:
                    best_parameters = parameters.copy()
                    best_performance = performance
                
                # Check for convergence (simplified)
                if iteration > 20 and abs(performance - best_performance) < 0.001:
                    convergence = True
                    break
                    
            except Exception as e:
                logger.error(f"Error evaluating parameters: {e}")
                continue
        
        # Calculate improvement
        improvement = 0.0
        if self.performance_tracker:
            previous_best = max(self.performance_tracker.values()) if self.performance_tracker else 0
            improvement = best_performance - previous_best
        
        result = OptimizationResult(
            optimization_id=optimization_id,
            objective=objective,
            parameters=best_parameters,
            performance_metrics={"performance": best_performance},
            improvement=improvement,
            timestamp=datetime.now(),
            iterations=iteration + 1,
            convergence=convergence
        )
        
        self.optimization_history.append(result)
        self.current_parameters.update(best_parameters)
        self.performance_tracker[optimization_id] = best_performance
        
        logger.info(f"Optimization completed: {best_performance:.4f} performance in {iteration + 1} iterations")
        return result
    
    async def adaptive_optimization(self, objective: OptimizationObjective, 
                                   parameter_space: Dict[str, List[Any]], 
                                   evaluation_function: Callable,
                                   adaptation_rate: float = 0.1) -> OptimizationResult:
        """Adaptive parameter optimization"""
        optimization_id = str(uuid.uuid4())
        
        # Start with current parameters or random
        current_params = self.current_parameters.copy()
        if not current_params:
            for param_name, param_values in parameter_space.items():
                if isinstance(param_values, list):
                    current_params[param_name] = np.random.choice(param_values)
                else:
                    current_params[param_name] = np.random.uniform(param_values[0], param_values[1])
        
        best_parameters = current_params.copy()
        best_performance = await evaluation_function(current_params)
        
        iteration = 0
        max_iterations = 50
        
        while iteration < max_iterations:
            # Generate adaptive parameters
            new_params = {}
            for param_name, current_value in current_params.items():
                param_space = parameter_space[param_name]
                
                if isinstance(param_space, list):
                    # Discrete parameter space
                    current_index = param_space.index(current_value) if current_value in param_space else 0
                    # Move to adjacent values with some probability
                    if np.random.random() < adaptation_rate:
                        if current_index > 0 and np.random.random() < 0.5:
                            new_params[param_name] = param_space[current_index - 1]
                        elif current_index < len(param_space) - 1:
                            new_params[param_name] = param_space[current_index + 1]
                        else:
                            new_params[param_name] = current_value
                    else:
                        new_params[param_name] = current_value
                else:
                    # Continuous parameter space
                    if np.random.random() < adaptation_rate:
                        # Add small random change
                        change = np.random.normal(0, (param_space[1] - param_space[0]) * 0.1)
                        new_value = current_value + change
                        # Clamp to parameter space
                        new_value = max(param_space[0], min(param_space[1], new_value))
                        new_params[param_name] = new_value
                    else:
                        new_params[param_name] = current_value
            
            # Evaluate new parameters
            try:
                performance = await evaluation_function(new_params)
                
                # Accept if better, or with some probability if worse (simulated annealing)
                if performance > best_performance or np.random.random() < 0.1:
                    current_params = new_params.copy()
                    if performance > best_performance:
                        best_parameters = new_params.copy()
                        best_performance = performance
                
            except Exception as e:
                logger.error(f"Error evaluating adaptive parameters: {e}")
            
            iteration += 1
        
        result = OptimizationResult(
            optimization_id=optimization_id,
            objective=objective,
            parameters=best_parameters,
            performance_metrics={"performance": best_performance},
            improvement=best_performance - (self.performance_tracker.get(list(self.performance_tracker.keys())[-1], 0) if self.performance_tracker else 0),
            timestamp=datetime.now(),
            iterations=iteration,
            convergence=True
        )
        
        self.optimization_history.append(result)
        self.current_parameters.update(best_parameters)
        self.performance_tracker[optimization_id] = best_performance
        
        return result

class SelfOptimizingSystem:
    """Self-optimizing system manager"""
    
    def __init__(self):
        self.decision_engine = DecisionEngine()
        self.parameter_optimizer = ParameterOptimizer()
        self.automation_rules = {}
        self.system_metrics = {}
        self.optimization_schedule = {}
        
    async def create_automation_rule(self, rule_type: AutomationType, name: str, 
                                   description: str, conditions: List[Dict[str, Any]], 
                                   actions: List[Dict[str, Any]], priority: int = 1) -> str:
        """Create automation rule"""
        rule = AutomationRule(
            rule_id=str(uuid.uuid4()),
            rule_type=rule_type,
            name=name,
            description=description,
            conditions=conditions,
            actions=actions,
            priority=priority,
            enabled=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        rule_id = await self.decision_engine.add_rule(rule)
        self.automation_rules[rule_id] = rule
        
        logger.info(f"Created automation rule: {name}")
        return rule_id
    
    async def run_automation_cycle(self, market_data: Dict[str, Any], 
                                  portfolio_data: Dict[str, Any]) -> List[AutomationDecision]:
        """Run one automation cycle"""
        decisions = []
        
        # Sort rules by priority
        sorted_rules = sorted(self.automation_rules.items(), 
                            key=lambda x: x[1].priority, reverse=True)
        
        for rule_id, rule in sorted_rules:
            if rule.enabled:
                decision = await self.decision_engine.make_decision(
                    rule_id, market_data, portfolio_data
                )
                if decision:
                    decisions.append(decision)
        
        logger.info(f"Automation cycle completed: {len(decisions)} decisions made")
        return decisions
    
    async def execute_decisions(self, decisions: List[AutomationDecision]) -> List[Dict[str, Any]]:
        """Execute automation decisions"""
        execution_results = []
        
        for decision in decisions:
            try:
                result = await self.decision_engine.execute_decision(decision.decision_id)
                execution_results.append(result)
            except Exception as e:
                logger.error(f"Error executing decision {decision.decision_id}: {e}")
                execution_results.append({
                    "success": False,
                    "error": str(e),
                    "decision_id": decision.decision_id
                })
        
        return execution_results
    
    async def optimize_system_parameters(self, objective: OptimizationObjective) -> OptimizationResult:
        """Optimize system parameters"""
        # Define parameter space for system optimization
        parameter_space = {
            "decision_threshold": [0.6, 0.7, 0.8, 0.9],
            "risk_tolerance": [0.1, 0.2, 0.3, 0.4, 0.5],
            "position_size": [0.01, 0.02, 0.05, 0.1, 0.2],
            "rebalance_frequency": [1, 7, 14, 30],  # days
            "stop_loss": [0.02, 0.05, 0.1, 0.15],
            "take_profit": [0.05, 0.1, 0.2, 0.3]
        }
        
        async def evaluate_system_performance(parameters: Dict[str, Any]) -> float:
            """Evaluate system performance with given parameters"""
            # Simulate performance evaluation
            base_performance = 0.1
            
            # Adjust performance based on parameters
            performance = base_performance
            
            # Higher decision threshold generally leads to better decisions
            performance += parameters.get("decision_threshold", 0.7) * 0.1
            
            # Moderate risk tolerance is optimal
            risk_tolerance = parameters.get("risk_tolerance", 0.3)
            performance += 0.2 - abs(risk_tolerance - 0.3) * 0.5
            
            # Optimal position size
            position_size = parameters.get("position_size", 0.05)
            performance += 0.1 - abs(position_size - 0.05) * 2
            
            # Add some randomness
            performance += np.random.normal(0, 0.05)
            
            return performance
        
        result = await self.parameter_optimizer.optimize_parameters(
            objective, parameter_space, evaluate_system_performance
        )
        
        logger.info(f"System optimization completed: {result.performance_metrics['performance']:.4f}")
        return result
    
    async def adaptive_parameter_update(self, performance_feedback: Dict[str, float]) -> bool:
        """Adaptively update parameters based on performance feedback"""
        try:
            # Analyze performance feedback
            current_performance = performance_feedback.get("current_performance", 0.0)
            target_performance = performance_feedback.get("target_performance", 0.15)
            
            if current_performance < target_performance * 0.8:
                # Performance is below target, trigger optimization
                logger.info("Performance below target, triggering adaptive optimization")
                
                result = await self.optimize_system_parameters(OptimizationObjective.MAXIMIZE_RETURNS)
                
                # Update system parameters
                self.system_metrics.update(result.parameters)
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error in adaptive parameter update: {e}")
            return False
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        active_rules = len([r for r in self.automation_rules.values() if r.enabled])
        total_decisions = len(self.decision_engine.decision_history)
        recent_decisions = len([d for d in self.decision_engine.decision_history 
                              if d.timestamp > datetime.now() - timedelta(hours=24)])
        
        return {
            "status": "active",
            "active_rules": active_rules,
            "total_rules": len(self.automation_rules),
            "total_decisions": total_decisions,
            "recent_decisions": recent_decisions,
            "optimization_history": len(self.parameter_optimizer.optimization_history),
            "current_parameters": self.system_metrics,
            "last_update": datetime.now()
        }
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        metrics = {}
        
        # Decision performance
        for rule_id, rule in self.automation_rules.items():
            performance = await self.decision_engine.get_decision_performance(rule_id)
            metrics[f"rule_{rule.name}"] = performance
        
        # Optimization performance
        if self.parameter_optimizer.optimization_history:
            latest_optimization = self.parameter_optimizer.optimization_history[-1]
            metrics["latest_optimization"] = {
                "performance": latest_optimization.performance_metrics["performance"],
                "improvement": latest_optimization.improvement,
                "iterations": latest_optimization.iterations,
                "convergence": latest_optimization.convergence
            }
        
        return metrics
    
    def get_summary(self) -> Dict[str, Any]:
        """Get system summary"""
        return {
            "total_automation_rules": len(self.automation_rules),
            "active_automation_rules": len([r for r in self.automation_rules.values() if r.enabled]),
            "total_decisions": len(self.decision_engine.decision_history),
            "optimization_runs": len(self.parameter_optimizer.optimization_history),
            "current_parameters": len(self.system_metrics),
            "system_status": "operational",
            "last_update": datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of SelfOptimizingSystem"""
    system = SelfOptimizingSystem()
    
    # Create automation rules
    buy_rule_id = await system.create_automation_rule(
        rule_type=AutomationType.DECISION_MAKING,
        name="RSI Oversold Buy",
        description="Buy when RSI is oversold",
        conditions=[
            {"type": "technical_indicator", "indicator": "rsi", "threshold": 30, "operator": "less_than"}
        ],
        actions=[{"type": "buy", "quantity": 0.1}],
        priority=1
    )
    
    sell_rule_id = await system.create_automation_rule(
        rule_type=AutomationType.DECISION_MAKING,
        name="RSI Overbought Sell",
        description="Sell when RSI is overbought",
        conditions=[
            {"type": "technical_indicator", "indicator": "rsi", "threshold": 70, "operator": "greater_than"}
        ],
        actions=[{"type": "sell", "quantity": 0.1}],
        priority=2
    )
    
    # Simulate market data
    market_data = {
        "price": 150.0,
        "volume": 10000,
        "rsi": 25,  # Oversold
        "macd": 0.5,
        "bollinger_position": 0.2
    }
    
    portfolio_data = {
        "total_value": 10000,
        "cash": 5000,
        "positions": {"BTC": 0.1, "ETH": 0.2},
        "unrealized_pnl": 500
    }
    
    # Run automation cycle
    decisions = await system.run_automation_cycle(market_data, portfolio_data)
    print(f"Made {len(decisions)} decisions")
    
    # Execute decisions
    if decisions:
        execution_results = await system.execute_decisions(decisions)
        print(f"Executed {len(execution_results)} decisions")
    
    # Optimize system parameters
    optimization_result = await system.optimize_system_parameters(OptimizationObjective.MAXIMIZE_RETURNS)
    print(f"Optimization result: {optimization_result.performance_metrics['performance']:.4f}")
    
    # Get system status
    status = await system.get_system_status()
    print(f"System status: {status}")
    
    # Get performance metrics
    metrics = await system.get_performance_metrics()
    print(f"Performance metrics: {len(metrics)} metrics calculated")
    
    # System summary
    summary = system.get_summary()
    print(f"System summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())
