# -*- coding: utf-8 -*-
"""
Stress Testing for NeoZork Interactive ML Trading Strategy Development.

This module provides stress testing capabilities for risk assessment.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
import warnings

class StressTesting:
    """
    Stress testing system for risk assessment.
    
    Features:
    - Historical Stress Testing
    - Monte Carlo Stress Testing
    - Scenario Analysis
    - VaR Stress Testing
    - Liquidity Stress Testing
    """
    
    def __init__(self):
        """Initialize the Stress Testing system."""
        self.stress_scenarios = {}
        self.stress_results = {}
        self.risk_metrics = {}
        self.scenario_analysis = {}
    
    def perform_historical_stress_test(self, data: pd.DataFrame, 
                                     strategy_config: Dict[str, Any],
                                     stress_periods: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Perform historical stress testing.
        
        Args:
            data: Historical data
            strategy_config: Strategy configuration
            stress_periods: List of stress periods (start_date, end_date)
            
        Returns:
            Historical stress test results
        """
        try:
            stress_results = {}
            
            for period_name, (start_date, end_date) in stress_periods:
                # Filter data for stress period
                period_data = data[(data.index >= start_date) & (data.index <= end_date)]
                
                if len(period_data) == 0:
                    continue
                
                # Calculate stress metrics
                stress_metrics = self._calculate_stress_metrics(period_data, strategy_config)
                
                stress_results[period_name] = {
                    "period": (start_date, end_date),
                    "data_length": len(period_data),
                    "stress_metrics": stress_metrics
                }
            
            # Analyze stress results
            analysis = self._analyze_stress_results(stress_results)
            
            result = {
                "status": "success",
                "stress_results": stress_results,
                "analysis": analysis,
                "n_periods": len(stress_periods)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Historical stress test failed: {str(e)}"}
    
    def perform_monte_carlo_stress_test(self, data: pd.DataFrame, 
                                      strategy_config: Dict[str, Any],
                                      monte_carlo_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform Monte Carlo stress testing.
        
        Args:
            data: Historical data
            strategy_config: Strategy configuration
            monte_carlo_params: Monte Carlo parameters
            
        Returns:
            Monte Carlo stress test results
        """
        try:
            n_simulations = monte_carlo_params.get("n_simulations", 1000)
            stress_scenarios = monte_carlo_params.get("stress_scenarios", ["market_crash", "high_volatility", "liquidity_crisis"])
            
            simulation_results = {}
            
            for scenario in stress_scenarios:
                scenario_results = []
                
                for sim in range(n_simulations):
                    # Generate stress scenario
                    stress_data = self._generate_stress_scenario(data, scenario, monte_carlo_params)
                    
                    # Calculate stress metrics
                    stress_metrics = self._calculate_stress_metrics(stress_data, strategy_config)
                    scenario_results.append(stress_metrics)
                
                simulation_results[scenario] = scenario_results
            
            # Analyze Monte Carlo results
            analysis = self._analyze_monte_carlo_stress(simulation_results)
            
            result = {
                "status": "success",
                "n_simulations": n_simulations,
                "scenarios": stress_scenarios,
                "simulation_results": simulation_results,
                "analysis": analysis
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Monte Carlo stress test failed: {str(e)}"}
    
    def perform_scenario_analysis(self, data: pd.DataFrame, 
                                strategy_config: Dict[str, Any],
                                scenarios: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform scenario analysis.
        
        Args:
            data: Historical data
            strategy_config: Strategy configuration
            scenarios: Dictionary of scenarios with parameters
            
        Returns:
            Scenario analysis results
        """
        try:
            scenario_results = {}
            
            for scenario_name, scenario_params in scenarios.items():
                # Generate scenario data
                scenario_data = self._generate_scenario_data(data, scenario_params)
                
                # Calculate scenario metrics
                scenario_metrics = self._calculate_stress_metrics(scenario_data, strategy_config)
                
                scenario_results[scenario_name] = {
                    "scenario_params": scenario_params,
                    "metrics": scenario_metrics,
                    "data_length": len(scenario_data)
                }
            
            # Analyze scenarios
            analysis = self._analyze_scenarios(scenario_results)
            
            result = {
                "status": "success",
                "scenarios": list(scenarios.keys()),
                "scenario_results": scenario_results,
                "analysis": analysis
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Scenario analysis failed: {str(e)}"}
    
    def perform_var_stress_test(self, data: pd.DataFrame, 
                               strategy_config: Dict[str, Any],
                               var_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform VaR stress testing.
        
        Args:
            data: Historical data
            strategy_config: Strategy configuration
            var_params: VaR parameters
            
        Returns:
            VaR stress test results
        """
        try:
            confidence_levels = var_params.get("confidence_levels", [0.95, 0.99, 0.999])
            time_horizons = var_params.get("time_horizons", [1, 5, 10])  # days
            
            var_results = {}
            
            for conf_level in confidence_levels:
                for horizon in time_horizons:
                    # Calculate VaR
                    var_value = self._calculate_var(data, conf_level, horizon)
                    
                    # Calculate stress VaR (extreme scenarios)
                    stress_var = self._calculate_stress_var(data, conf_level, horizon)
                    
                    var_results[f"var_{conf_level}_{horizon}d"] = {
                        "confidence_level": conf_level,
                        "time_horizon": horizon,
                        "var_value": var_value,
                        "stress_var": stress_var,
                        "var_ratio": stress_var / var_value if var_value != 0 else 0
                    }
            
            # Analyze VaR results
            analysis = self._analyze_var_results(var_results)
            
            result = {
                "status": "success",
                "var_results": var_results,
                "analysis": analysis
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"VaR stress test failed: {str(e)}"}
    
    def perform_liquidity_stress_test(self, data: pd.DataFrame, 
                                    strategy_config: Dict[str, Any],
                                    liquidity_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform liquidity stress testing.
        
        Args:
            data: Historical data
            strategy_config: Strategy configuration
            liquidity_params: Liquidity parameters
            
        Returns:
            Liquidity stress test results
        """
        try:
            # Simulate liquidity stress scenarios
            stress_scenarios = liquidity_params.get("stress_scenarios", ["normal", "stressed", "crisis"])
            
            liquidity_results = {}
            
            for scenario in stress_scenarios:
                # Generate liquidity stress data
                stress_data = self._generate_liquidity_stress(data, scenario, liquidity_params)
                
                # Calculate liquidity metrics
                liquidity_metrics = self._calculate_liquidity_metrics(stress_data, strategy_config)
                
                liquidity_results[scenario] = {
                    "scenario": scenario,
                    "metrics": liquidity_metrics
                }
            
            # Analyze liquidity results
            analysis = self._analyze_liquidity_results(liquidity_results)
            
            result = {
                "status": "success",
                "liquidity_results": liquidity_results,
                "analysis": analysis
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Liquidity stress test failed: {str(e)}"}
    
    def _calculate_stress_metrics(self, data: pd.DataFrame, strategy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate stress metrics for given data."""
        try:
            # Calculate returns
            returns = data.pct_change().dropna()
            
            # Basic metrics
            total_return = (1 + returns).prod() - 1
            volatility = returns.std() * np.sqrt(252)
            sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252) if returns.std() != 0 else 0
            
            # Risk metrics
            max_drawdown = self._calculate_max_drawdown((1 + returns).cumprod())
            var_95 = np.percentile(returns, 5)
            var_99 = np.percentile(returns, 1)
            cvar_95 = returns[returns <= var_95].mean()
            cvar_99 = returns[returns <= var_99].mean()
            
            # Stress-specific metrics
            worst_day = returns.min()
            best_day = returns.max()
            consecutive_losses = self._calculate_consecutive_losses(returns)
            
            metrics = {
                "total_return": total_return,
                "volatility": volatility,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown,
                "var_95": var_95,
                "var_99": var_99,
                "cvar_95": cvar_95,
                "cvar_99": cvar_99,
                "worst_day": worst_day,
                "best_day": best_day,
                "consecutive_losses": consecutive_losses,
                "n_observations": len(returns)
            }
            
            return metrics
            
        except Exception as e:
            return {"total_return": 0.0, "volatility": 0.0, "sharpe_ratio": 0.0}
    
    def _calculate_max_drawdown(self, cumulative_returns: pd.Series) -> float:
        """Calculate maximum drawdown."""
        try:
            peak = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - peak) / peak
            return drawdown.min()
        except Exception as e:
            return 0.0
    
    def _calculate_consecutive_losses(self, returns: pd.Series) -> int:
        """Calculate maximum consecutive losses."""
        try:
            losses = (returns < 0).astype(int)
            consecutive_losses = 0
            max_consecutive = 0
            
            for loss in losses:
                if loss == 1:
                    consecutive_losses += 1
                    max_consecutive = max(max_consecutive, consecutive_losses)
                else:
                    consecutive_losses = 0
            
            return max_consecutive
        except Exception as e:
            return 0
    
    def _analyze_stress_results(self, stress_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze stress test results."""
        try:
            if not stress_results:
                return {}
            
            # Extract metrics
            total_returns = [result["stress_metrics"].get("total_return", 0) for result in stress_results.values()]
            volatilities = [result["stress_metrics"].get("volatility", 0) for result in stress_results.values()]
            max_drawdowns = [result["stress_metrics"].get("max_drawdown", 0) for result in stress_results.values()]
            
            analysis = {
                "worst_return": min(total_returns),
                "best_return": max(total_returns),
                "avg_return": np.mean(total_returns),
                "worst_volatility": max(volatilities),
                "worst_drawdown": min(max_drawdowns),
                "avg_drawdown": np.mean(max_drawdowns),
                "n_periods": len(stress_results)
            }
            
            return analysis
            
        except Exception as e:
            return {}
    
    def _generate_stress_scenario(self, data: pd.DataFrame, scenario: str, 
                                 monte_carlo_params: Dict[str, Any]) -> pd.DataFrame:
        """Generate stress scenario data."""
        try:
            if scenario == "market_crash":
                # Simulate market crash with extreme negative returns
                returns = data.pct_change().dropna()
                stress_returns = returns * np.random.uniform(2, 5)  # Amplify negative returns
                stress_data = data.copy()
                stress_data.iloc[1:] = stress_data.iloc[0] * (1 + stress_returns).cumprod()
                
            elif scenario == "high_volatility":
                # Simulate high volatility period
                returns = data.pct_change().dropna()
                stress_returns = returns * np.random.uniform(1.5, 3)  # Increase volatility
                stress_data = data.copy()
                stress_data.iloc[1:] = stress_data.iloc[0] * (1 + stress_returns).cumprod()
                
            elif scenario == "liquidity_crisis":
                # Simulate liquidity crisis with gaps and extreme spreads
                stress_data = data.copy()
                # Add random gaps and extreme movements
                for i in range(1, len(stress_data)):
                    if np.random.random() < 0.1:  # 10% chance of gap
                        stress_data.iloc[i] = stress_data.iloc[i-1] * np.random.uniform(0.8, 1.2)
                    else:
                        stress_data.iloc[i] = stress_data.iloc[i-1] * (1 + np.random.normal(0, 0.05))
                
            else:
                # Default: random stress
                stress_data = data.copy()
                noise = np.random.normal(0, 0.02, len(data))
                stress_data = stress_data * (1 + noise)
            
            return stress_data
            
        except Exception as e:
            return data
    
    def _analyze_monte_carlo_stress(self, simulation_results: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Analyze Monte Carlo stress test results."""
        try:
            analysis = {}
            
            for scenario, results in simulation_results.items():
                if not results:
                    continue
                
                # Extract metrics
                total_returns = [r.get("total_return", 0) for r in results]
                max_drawdowns = [r.get("max_drawdown", 0) for r in results]
                volatilities = [r.get("volatility", 0) for r in results]
                
                analysis[scenario] = {
                    "worst_return": min(total_returns),
                    "best_return": max(total_returns),
                    "avg_return": np.mean(total_returns),
                    "std_return": np.std(total_returns),
                    "worst_drawdown": min(max_drawdowns),
                    "avg_drawdown": np.mean(max_drawdowns),
                    "worst_volatility": max(volatilities),
                    "avg_volatility": np.mean(volatilities),
                    "n_simulations": len(results)
                }
            
            return analysis
            
        except Exception as e:
            return {}
    
    def _generate_scenario_data(self, data: pd.DataFrame, scenario_params: Dict[str, Any]) -> pd.DataFrame:
        """Generate scenario data based on parameters."""
        try:
            scenario_data = data.copy()
            
            # Apply scenario parameters
            if "return_multiplier" in scenario_params:
                returns = data.pct_change().dropna()
                modified_returns = returns * scenario_params["return_multiplier"]
                scenario_data.iloc[1:] = scenario_data.iloc[0] * (1 + modified_returns).cumprod()
            
            if "volatility_multiplier" in scenario_params:
                returns = data.pct_change().dropna()
                modified_returns = returns * scenario_params["volatility_multiplier"]
                scenario_data.iloc[1:] = scenario_data.iloc[0] * (1 + modified_returns).cumprod()
            
            return scenario_data
            
        except Exception as e:
            return data
    
    def _analyze_scenarios(self, scenario_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze scenario results."""
        try:
            analysis = {}
            
            for scenario_name, result in scenario_results.items():
                metrics = result.get("metrics", {})
                analysis[scenario_name] = {
                    "total_return": metrics.get("total_return", 0),
                    "volatility": metrics.get("volatility", 0),
                    "max_drawdown": metrics.get("max_drawdown", 0),
                    "sharpe_ratio": metrics.get("sharpe_ratio", 0)
                }
            
            return analysis
            
        except Exception as e:
            return {}
    
    def _calculate_var(self, data: pd.DataFrame, confidence_level: float, horizon: int) -> float:
        """Calculate Value at Risk."""
        try:
            returns = data.pct_change().dropna()
            var_percentile = (1 - confidence_level) * 100
            var_value = np.percentile(returns, var_percentile) * np.sqrt(horizon)
            return var_value
        except Exception as e:
            return 0.0
    
    def _calculate_stress_var(self, data: pd.DataFrame, confidence_level: float, horizon: int) -> float:
        """Calculate stress VaR."""
        try:
            returns = data.pct_change().dropna()
            # Use extreme scenarios (worst 1% of returns)
            extreme_returns = returns[returns <= returns.quantile(0.01)]
            if len(extreme_returns) == 0:
                return 0.0
            
            var_percentile = (1 - confidence_level) * 100
            stress_var = np.percentile(extreme_returns, var_percentile) * np.sqrt(horizon)
            return stress_var
        except Exception as e:
            return 0.0
    
    def _analyze_var_results(self, var_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze VaR results."""
        try:
            analysis = {
                "var_values": [result["var_value"] for result in var_results.values()],
                "stress_var_values": [result["stress_var"] for result in var_results.values()],
                "var_ratios": [result["var_ratio"] for result in var_results.values()],
                "max_var": max([result["var_value"] for result in var_results.values()]),
                "max_stress_var": max([result["stress_var"] for result in var_results.values()]),
                "n_scenarios": len(var_results)
            }
            
            return analysis
            
        except Exception as e:
            return {}
    
    def _generate_liquidity_stress(self, data: pd.DataFrame, scenario: str, 
                                  liquidity_params: Dict[str, Any]) -> pd.DataFrame:
        """Generate liquidity stress data."""
        try:
            if scenario == "normal":
                return data
            elif scenario == "stressed":
                # Simulate stressed liquidity with wider spreads
                stress_data = data.copy()
                # Add random gaps and wider spreads
                for i in range(1, len(stress_data)):
                    if np.random.random() < 0.05:  # 5% chance of gap
                        stress_data.iloc[i] = stress_data.iloc[i-1] * np.random.uniform(0.9, 1.1)
                    else:
                        stress_data.iloc[i] = stress_data.iloc[i-1] * (1 + np.random.normal(0, 0.03))
            elif scenario == "crisis":
                # Simulate liquidity crisis with extreme gaps
                stress_data = data.copy()
                # Add frequent gaps and extreme movements
                for i in range(1, len(stress_data)):
                    if np.random.random() < 0.2:  # 20% chance of gap
                        stress_data.iloc[i] = stress_data.iloc[i-1] * np.random.uniform(0.8, 1.2)
                    else:
                        stress_data.iloc[i] = stress_data.iloc[i-1] * (1 + np.random.normal(0, 0.05))
            else:
                return data
            
            return stress_data
            
        except Exception as e:
            return data
    
    def _calculate_liquidity_metrics(self, data: pd.DataFrame, strategy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate liquidity metrics."""
        try:
            returns = data.pct_change().dropna()
            
            # Basic liquidity metrics
            volatility = returns.std() * np.sqrt(252)
            max_drawdown = self._calculate_max_drawdown((1 + returns).cumprod())
            
            # Liquidity-specific metrics
            gaps = self._calculate_gaps(data)
            spread_volatility = self._calculate_spread_volatility(data)
            
            metrics = {
                "volatility": volatility,
                "max_drawdown": max_drawdown,
                "n_gaps": gaps,
                "spread_volatility": spread_volatility,
                "liquidity_score": self._calculate_liquidity_score(gaps, spread_volatility)
            }
            
            return metrics
            
        except Exception as e:
            return {"volatility": 0.0, "max_drawdown": 0.0, "liquidity_score": 0.0}
    
    def _calculate_gaps(self, data: pd.DataFrame) -> int:
        """Calculate number of gaps in data."""
        try:
            returns = data.pct_change().dropna()
            # Count extreme returns as gaps
            threshold = returns.std() * 3
            gaps = np.sum(np.abs(returns) > threshold)
            return gaps
        except Exception as e:
            return 0
    
    def _calculate_spread_volatility(self, data: pd.DataFrame) -> float:
        """Calculate spread volatility."""
        try:
            returns = data.pct_change().dropna()
            return returns.std()
        except Exception as e:
            return 0.0
    
    def _calculate_liquidity_score(self, gaps: int, spread_volatility: float) -> float:
        """Calculate liquidity score (higher is better)."""
        try:
            # Simple liquidity score
            gap_penalty = min(gaps / 10, 1.0)  # Penalty for gaps
            volatility_penalty = min(spread_volatility * 10, 1.0)  # Penalty for high volatility
            liquidity_score = 1.0 - (gap_penalty + volatility_penalty) / 2
            return max(0.0, liquidity_score)
        except Exception as e:
            return 0.0
    
    def _analyze_liquidity_results(self, liquidity_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze liquidity stress test results."""
        try:
            analysis = {}
            
            for scenario, result in liquidity_results.items():
                metrics = result.get("metrics", {})
                analysis[scenario] = {
                    "liquidity_score": metrics.get("liquidity_score", 0),
                    "volatility": metrics.get("volatility", 0),
                    "n_gaps": metrics.get("n_gaps", 0),
                    "spread_volatility": metrics.get("spread_volatility", 0)
                }
            
            return analysis
            
        except Exception as e:
            return {}
