# -*- coding: utf-8 -*-
"""
Performance Attribution for NeoZork Interactive ML Trading Strategy Development.

This module provides performance attribution capabilities for strategy analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
import warnings

class PerformanceAttribution:
    """
    Performance attribution system for strategy analysis.
    
    Features:
    - Return Attribution
    - Risk Attribution
    - Factor Attribution
    - Sector Attribution
    - Time Attribution
    """
    
    def __init__(self):
        """Initialize the Performance Attribution system."""
        self.attribution_results = {}
        self.performance_metrics = {}
        self.attribution_models = {}
    
    def perform_return_attribution(self, strategy_returns: pd.Series, 
                                 benchmark_returns: pd.Series,
                                 attribution_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform return attribution analysis.
        
        Args:
            strategy_returns: Strategy returns
            benchmark_returns: Benchmark returns
            attribution_config: Attribution configuration
            
        Returns:
            Return attribution results
        """
        try:
            # Calculate excess returns
            excess_returns = strategy_returns - benchmark_returns
            
            # Calculate attribution components
            attribution_components = self._calculate_attribution_components(
                strategy_returns, benchmark_returns, attribution_config
            )
            
            # Calculate performance metrics
            performance_metrics = self._calculate_performance_metrics(
                strategy_returns, benchmark_returns, excess_returns
            )
            
            result = {
                "status": "success",
                "excess_returns": excess_returns,
                "attribution_components": attribution_components,
                "performance_metrics": performance_metrics,
                "n_periods": len(strategy_returns)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Return attribution failed: {str(e)}"}
    
    def perform_risk_attribution(self, strategy_returns: pd.Series, 
                               benchmark_returns: pd.Series,
                               risk_factors: Dict[str, pd.Series]) -> Dict[str, Any]:
        """
        Perform risk attribution analysis.
        
        Args:
            strategy_returns: Strategy returns
            benchmark_returns: Benchmark returns
            risk_factors: Dictionary of risk factors
            
        Returns:
            Risk attribution results
        """
        try:
            # Calculate risk metrics
            strategy_risk = self._calculate_risk_metrics(strategy_returns)
            benchmark_risk = self._calculate_risk_metrics(benchmark_returns)
            
            # Calculate factor exposures
            factor_exposures = self._calculate_factor_exposures(strategy_returns, risk_factors)
            
            # Calculate risk attribution
            risk_attribution = self._calculate_risk_attribution(
                strategy_risk, benchmark_risk, factor_exposures
            )
            
            result = {
                "status": "success",
                "strategy_risk": strategy_risk,
                "benchmark_risk": benchmark_risk,
                "factor_exposures": factor_exposures,
                "risk_attribution": risk_attribution
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Risk attribution failed: {str(e)}"}
    
    def perform_factor_attribution(self, strategy_returns: pd.Series, 
                                 factor_returns: Dict[str, pd.Series],
                                 attribution_method: str = "regression") -> Dict[str, Any]:
        """
        Perform factor attribution analysis.
        
        Args:
            strategy_returns: Strategy returns
            factor_returns: Dictionary of factor returns
            attribution_method: Attribution method (regression, decomposition)
            
        Returns:
            Factor attribution results
        """
        try:
            if attribution_method == "regression":
                attribution_results = self._regression_attribution(strategy_returns, factor_returns)
            elif attribution_method == "decomposition":
                attribution_results = self._decomposition_attribution(strategy_returns, factor_returns)
            else:
                attribution_results = self._default_attribution(strategy_returns, factor_returns)
            
            # Calculate factor contributions
            factor_contributions = self._calculate_factor_contributions(
                strategy_returns, factor_returns, attribution_results
            )
            
            result = {
                "status": "success",
                "attribution_method": attribution_method,
                "attribution_results": attribution_results,
                "factor_contributions": factor_contributions,
                "n_factors": len(factor_returns)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Factor attribution failed: {str(e)}"}
    
    def perform_sector_attribution(self, strategy_returns: pd.Series, 
                                 sector_returns: Dict[str, pd.Series],
                                 sector_weights: Dict[str, float]) -> Dict[str, Any]:
        """
        Perform sector attribution analysis.
        
        Args:
            strategy_returns: Strategy returns
            sector_returns: Dictionary of sector returns
            sector_weights: Dictionary of sector weights
            
        Returns:
            Sector attribution results
        """
        try:
            # Calculate sector contributions
            sector_contributions = self._calculate_sector_contributions(
                strategy_returns, sector_returns, sector_weights
            )
            
            # Calculate sector performance
            sector_performance = self._calculate_sector_performance(
                sector_returns, sector_weights
            )
            
            # Calculate sector attribution
            sector_attribution = self._calculate_sector_attribution(
                sector_contributions, sector_performance
            )
            
            result = {
                "status": "success",
                "sector_contributions": sector_contributions,
                "sector_performance": sector_performance,
                "sector_attribution": sector_attribution,
                "n_sectors": len(sector_returns)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Sector attribution failed: {str(e)}"}
    
    def perform_time_attribution(self, strategy_returns: pd.Series, 
                               time_periods: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Perform time attribution analysis.
        
        Args:
            strategy_returns: Strategy returns
            time_periods: List of time periods (start_date, end_date)
            
        Returns:
            Time attribution results
        """
        try:
            time_attribution = {}
            
            for period_name, (start_date, end_date) in time_periods:
                # Filter returns for period
                period_returns = strategy_returns[(strategy_returns.index >= start_date) & 
                                                (strategy_returns.index <= end_date)]
                
                if len(period_returns) == 0:
                    continue
                
                # Calculate period metrics
                period_metrics = self._calculate_period_metrics(period_returns)
                
                time_attribution[period_name] = {
                    "period": (start_date, end_date),
                    "returns": period_returns,
                    "metrics": period_metrics,
                    "n_observations": len(period_returns)
                }
            
            # Calculate time attribution analysis
            time_analysis = self._analyze_time_attribution(time_attribution)
            
            result = {
                "status": "success",
                "time_attribution": time_attribution,
                "time_analysis": time_analysis,
                "n_periods": len(time_periods)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Time attribution failed: {str(e)}"}
    
    def _calculate_attribution_components(self, strategy_returns: pd.Series, 
                                        benchmark_returns: pd.Series,
                                        attribution_config: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate attribution components."""
        try:
            # Calculate excess returns
            excess_returns = strategy_returns - benchmark_returns
            
            # Calculate attribution components
            components = {
                "excess_return": excess_returns.sum(),
                "strategy_return": strategy_returns.sum(),
                "benchmark_return": benchmark_returns.sum(),
                "excess_volatility": strategy_returns.std() - benchmark_returns.std(),
                "tracking_error": excess_returns.std(),
                "information_ratio": excess_returns.mean() / excess_returns.std() if excess_returns.std() != 0 else 0
            }
            
            return components
            
        except Exception as e:
            return {}
    
    def _calculate_performance_metrics(self, strategy_returns: pd.Series, 
                                     benchmark_returns: pd.Series,
                                     excess_returns: pd.Series) -> Dict[str, Any]:
        """Calculate performance metrics."""
        try:
            metrics = {
                "strategy_total_return": (1 + strategy_returns).prod() - 1,
                "benchmark_total_return": (1 + benchmark_returns).prod() - 1,
                "excess_total_return": (1 + excess_returns).prod() - 1,
                "strategy_volatility": strategy_returns.std() * np.sqrt(252),
                "benchmark_volatility": benchmark_returns.std() * np.sqrt(252),
                "strategy_sharpe": strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() != 0 else 0,
                "benchmark_sharpe": benchmark_returns.mean() / benchmark_returns.std() * np.sqrt(252) if benchmark_returns.std() != 0 else 0,
                "information_ratio": excess_returns.mean() / excess_returns.std() * np.sqrt(252) if excess_returns.std() != 0 else 0,
                "max_drawdown": self._calculate_max_drawdown((1 + strategy_returns).cumprod()),
                "benchmark_max_drawdown": self._calculate_max_drawdown((1 + benchmark_returns).cumprod())
            }
            
            return metrics
            
        except Exception as e:
            return {}
    
    def _calculate_max_drawdown(self, cumulative_returns: pd.Series) -> float:
        """Calculate maximum drawdown."""
        try:
            peak = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - peak) / peak
            return drawdown.min()
        except Exception as e:
            return 0.0
    
    def _calculate_risk_metrics(self, returns: pd.Series) -> Dict[str, Any]:
        """Calculate risk metrics."""
        try:
            risk_metrics = {
                "volatility": returns.std() * np.sqrt(252),
                "var_95": np.percentile(returns, 5),
                "var_99": np.percentile(returns, 1),
                "cvar_95": returns[returns <= np.percentile(returns, 5)].mean(),
                "cvar_99": returns[returns <= np.percentile(returns, 1)].mean(),
                "max_drawdown": self._calculate_max_drawdown((1 + returns).cumprod()),
                "skewness": returns.skew(),
                "kurtosis": returns.kurtosis()
            }
            
            return risk_metrics
            
        except Exception as e:
            return {}
    
    def _calculate_factor_exposures(self, strategy_returns: pd.Series, 
                                  risk_factors: Dict[str, pd.Series]) -> Dict[str, float]:
        """Calculate factor exposures."""
        try:
            exposures = {}
            
            for factor_name, factor_returns in risk_factors.items():
                # Calculate correlation as proxy for exposure
                correlation = strategy_returns.corr(factor_returns)
                exposures[factor_name] = correlation if not np.isnan(correlation) else 0.0
            
            return exposures
            
        except Exception as e:
            return {}
    
    def _calculate_risk_attribution(self, strategy_risk: Dict[str, Any], 
                                  benchmark_risk: Dict[str, Any],
                                  factor_exposures: Dict[str, float]) -> Dict[str, Any]:
        """Calculate risk attribution."""
        try:
            risk_attribution = {
                "strategy_volatility": strategy_risk.get("volatility", 0),
                "benchmark_volatility": benchmark_risk.get("volatility", 0),
                "volatility_difference": strategy_risk.get("volatility", 0) - benchmark_risk.get("volatility", 0),
                "factor_exposures": factor_exposures,
                "risk_contribution": {}
            }
            
            # Calculate risk contribution from factors
            for factor_name, exposure in factor_exposures.items():
                risk_contribution = exposure * strategy_risk.get("volatility", 0)
                risk_attribution["risk_contribution"][factor_name] = risk_contribution
            
            return risk_attribution
            
        except Exception as e:
            return {}
    
    def _regression_attribution(self, strategy_returns: pd.Series, 
                              factor_returns: Dict[str, pd.Series]) -> Dict[str, Any]:
        """Perform regression-based attribution."""
        try:
            # Prepare data for regression
            X = pd.DataFrame(factor_returns)
            y = strategy_returns
            
            # Align data
            aligned_data = pd.concat([y, X], axis=1).dropna()
            y_aligned = aligned_data.iloc[:, 0]
            X_aligned = aligned_data.iloc[:, 1:]
            
            # Perform regression
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(X_aligned, y_aligned)
            
            # Calculate attribution
            attribution = {
                "coefficients": dict(zip(X_aligned.columns, model.coef_)),
                "intercept": model.intercept_,
                "r_squared": model.score(X_aligned, y_aligned),
                "residuals": y_aligned - model.predict(X_aligned)
            }
            
            return attribution
            
        except Exception as e:
            return {}
    
    def _decomposition_attribution(self, strategy_returns: pd.Series, 
                                 factor_returns: Dict[str, pd.Series]) -> Dict[str, Any]:
        """Perform decomposition-based attribution."""
        try:
            # Calculate factor contributions
            factor_contributions = {}
            
            for factor_name, factor_returns_series in factor_returns.items():
                # Calculate contribution as correlation * factor returns
                correlation = strategy_returns.corr(factor_returns_series)
                if not np.isnan(correlation):
                    factor_contributions[factor_name] = correlation * factor_returns_series
                else:
                    factor_contributions[factor_name] = pd.Series(0, index=strategy_returns.index)
            
            # Calculate residual
            total_factor_contribution = sum(factor_contributions.values())
            residual = strategy_returns - total_factor_contribution
            
            attribution = {
                "factor_contributions": factor_contributions,
                "residual": residual,
                "total_factor_contribution": total_factor_contribution
            }
            
            return attribution
            
        except Exception as e:
            return {}
    
    def _default_attribution(self, strategy_returns: pd.Series, 
                           factor_returns: Dict[str, pd.Series]) -> Dict[str, Any]:
        """Default attribution method."""
        try:
            attribution = {}
            
            for factor_name, factor_returns_series in factor_returns.items():
                correlation = strategy_returns.corr(factor_returns_series)
                attribution[factor_name] = correlation if not np.isnan(correlation) else 0.0
            
            return attribution
            
        except Exception as e:
            return {}
    
    def _calculate_factor_contributions(self, strategy_returns: pd.Series, 
                                      factor_returns: Dict[str, pd.Series],
                                      attribution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate factor contributions."""
        try:
            contributions = {}
            
            if "coefficients" in attribution_results:
                # Regression-based contributions
                for factor_name, coefficient in attribution_results["coefficients"].items():
                    if factor_name in factor_returns:
                        contributions[factor_name] = coefficient * factor_returns[factor_name]
            elif "factor_contributions" in attribution_results:
                # Decomposition-based contributions
                contributions = attribution_results["factor_contributions"]
            else:
                # Default contributions
                for factor_name, factor_returns_series in factor_returns.items():
                    correlation = strategy_returns.corr(factor_returns_series)
                    contributions[factor_name] = correlation * factor_returns_series if not np.isnan(correlation) else pd.Series(0, index=strategy_returns.index)
            
            return contributions
            
        except Exception as e:
            return {}
    
    def _calculate_sector_contributions(self, strategy_returns: pd.Series, 
                                      sector_returns: Dict[str, pd.Series],
                                      sector_weights: Dict[str, float]) -> Dict[str, Any]:
        """Calculate sector contributions."""
        try:
            contributions = {}
            
            for sector_name, sector_returns_series in sector_returns.items():
                weight = sector_weights.get(sector_name, 0.0)
                contribution = weight * sector_returns_series
                contributions[sector_name] = contribution
            
            return contributions
            
        except Exception as e:
            return {}
    
    def _calculate_sector_performance(self, sector_returns: Dict[str, pd.Series], 
                                    sector_weights: Dict[str, float]) -> Dict[str, Any]:
        """Calculate sector performance."""
        try:
            performance = {}
            
            for sector_name, sector_returns_series in sector_returns.items():
                weight = sector_weights.get(sector_name, 0.0)
                total_return = (1 + sector_returns_series).prod() - 1
                volatility = sector_returns_series.std() * np.sqrt(252)
                sharpe = sector_returns_series.mean() / sector_returns_series.std() * np.sqrt(252) if sector_returns_series.std() != 0 else 0
                
                performance[sector_name] = {
                    "weight": weight,
                    "total_return": total_return,
                    "volatility": volatility,
                    "sharpe_ratio": sharpe,
                    "contribution": weight * total_return
                }
            
            return performance
            
        except Exception as e:
            return {}
    
    def _calculate_sector_attribution(self, sector_contributions: Dict[str, Any], 
                                    sector_performance: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate sector attribution."""
        try:
            attribution = {
                "sector_contributions": sector_contributions,
                "sector_performance": sector_performance,
                "total_contribution": sum(sector_contributions.values()) if sector_contributions else pd.Series(0, index=pd.date_range('2020-01-01', periods=1)),
                "attribution_analysis": {}
            }
            
            # Calculate attribution analysis
            for sector_name, performance in sector_performance.items():
                attribution["attribution_analysis"][sector_name] = {
                    "weight": performance.get("weight", 0),
                    "return": performance.get("total_return", 0),
                    "contribution": performance.get("contribution", 0),
                    "volatility": performance.get("volatility", 0)
                }
            
            return attribution
            
        except Exception as e:
            return {}
    
    def _calculate_period_metrics(self, period_returns: pd.Series) -> Dict[str, Any]:
        """Calculate period metrics."""
        try:
            metrics = {
                "total_return": (1 + period_returns).prod() - 1,
                "volatility": period_returns.std() * np.sqrt(252),
                "sharpe_ratio": period_returns.mean() / period_returns.std() * np.sqrt(252) if period_returns.std() != 0 else 0,
                "max_drawdown": self._calculate_max_drawdown((1 + period_returns).cumprod()),
                "var_95": np.percentile(period_returns, 5),
                "skewness": period_returns.skew(),
                "kurtosis": period_returns.kurtosis()
            }
            
            return metrics
            
        except Exception as e:
            return {}
    
    def _analyze_time_attribution(self, time_attribution: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze time attribution."""
        try:
            analysis = {
                "period_analysis": {},
                "overall_metrics": {}
            }
            
            # Analyze each period
            for period_name, period_data in time_attribution.items():
                metrics = period_data.get("metrics", {})
                analysis["period_analysis"][period_name] = {
                    "total_return": metrics.get("total_return", 0),
                    "volatility": metrics.get("volatility", 0),
                    "sharpe_ratio": metrics.get("sharpe_ratio", 0),
                    "max_drawdown": metrics.get("max_drawdown", 0)
                }
            
            # Calculate overall metrics
            all_returns = []
            for period_data in time_attribution.values():
                returns = period_data.get("returns", pd.Series())
                all_returns.extend(returns.tolist())
            
            if all_returns:
                all_returns_series = pd.Series(all_returns)
                analysis["overall_metrics"] = {
                    "total_return": (1 + all_returns_series).prod() - 1,
                    "volatility": all_returns_series.std() * np.sqrt(252),
                    "sharpe_ratio": all_returns_series.mean() / all_returns_series.std() * np.sqrt(252) if all_returns_series.std() != 0 else 0,
                    "max_drawdown": self._calculate_max_drawdown((1 + all_returns_series).cumprod())
                }
            
            return analysis
            
        except Exception as e:
            return {}
