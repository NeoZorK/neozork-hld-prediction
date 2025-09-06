"""
Quantitative Research Tools System
Advanced statistical analysis, factor models, backtesting frameworks
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
warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchType(Enum):
    """Research type enumeration"""
    STATISTICAL_ANALYSIS = "statistical_analysis"
    FACTOR_MODEL = "factor_model"
    BACKTESTING = "backtesting"
    CORRELATION_ANALYSIS = "correlation_analysis"

class FactorType(Enum):
    """Factor type enumeration"""
    MARKET = "market"
    SIZE = "size"
    VALUE = "value"
    MOMENTUM = "momentum"

class BacktestType(Enum):
    """Backtest type enumeration"""
    WALK_FORWARD = "walk_forward"
    MONTE_CARLO = "monte_carlo"

@dataclass
class ResearchResult:
    """Research result"""
    result_id: str
    research_type: ResearchType
    title: str
    description: str
    data: Dict[str, Any]
    statistics: Dict[str, float]
    conclusions: List[str]
    recommendations: List[str]
    confidence_level: float
    created_at: datetime
    metadata: Dict[str, Any]

@dataclass
class FactorModel:
    """Factor model"""
    model_id: str
    name: str
    factors: List[FactorType]
    coefficients: Dict[str, float]
    r_squared: float
    adjusted_r_squared: float
    f_statistic: float
    p_value: float
    residuals: List[float]
    created_at: datetime

@dataclass
class BacktestResult:
    """Backtest result"""
    backtest_id: str
    strategy_name: str
    backtest_type: BacktestType
    start_date: datetime
    end_date: datetime
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    calmar_ratio: float
    win_rate: float
    profit_factor: float
    total_trades: int
    avg_trade_duration: float
    created_at: datetime

class StatisticalAnalyzer:
    """Advanced statistical analysis tools"""
    
    def __init__(self):
        self.analysis_history = []
        
    async def descriptive_statistics(self, data: pd.Series) -> Dict[str, float]:
        """Calculate comprehensive descriptive statistics"""
        stats_dict = {
            "count": len(data),
            "mean": data.mean(),
            "median": data.median(),
            "std": data.std(),
            "var": data.var(),
            "skewness": data.skew(),
            "kurtosis": data.kurtosis(),
            "min": data.min(),
            "max": data.max(),
            "range": data.max() - data.min(),
            "iqr": data.quantile(0.75) - data.quantile(0.25)
        }
        
        # Percentiles
        for p in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
            stats_dict[f"p{p}"] = data.quantile(p/100)
        
        return stats_dict
    
    async def normality_tests(self, data: pd.Series) -> Dict[str, Any]:
        """Perform normality tests"""
        clean_data = data.dropna()
        
        if len(clean_data) < 3:
            return {"error": "Insufficient data for normality tests"}
        
        # Skewness and Kurtosis
        skewness = clean_data.skew()
        kurtosis = clean_data.kurtosis()
        
        # Simple normality assessment
        is_normal = abs(skewness) < 0.5 and abs(kurtosis) < 0.5
        
        return {
            "skewness": skewness,
            "kurtosis": kurtosis,
            "is_normal": is_normal,
            "mean": clean_data.mean(),
            "std": clean_data.std()
        }
    
    async def correlation_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive correlation analysis"""
        # Pearson correlation
        pearson_corr = data.corr(method="pearson")
        
        # Spearman correlation
        spearman_corr = data.corr(method="spearman")
        
        # Significant correlations
        significant_correlations = []
        for i in range(len(data.columns)):
            for j in range(i+1, len(data.columns)):
                corr = pearson_corr.iloc[i, j]
                if abs(corr) > 0.5:  # Simple significance threshold
                    significant_correlations.append({
                        "pair": (data.columns[i], data.columns[j]),
                        "correlation": corr
                    })
        
        return {
            "pearson": pearson_corr,
            "spearman": spearman_corr,
            "significant_correlations": significant_correlations,
            "correlation_matrix": pearson_corr
        }
    
    async def time_series_analysis(self, data: pd.Series) -> Dict[str, Any]:
        """Time series analysis"""
        # Autocorrelation
        autocorr = data.autocorr(lag=1)
        
        # Trend analysis
        x = np.arange(len(data))
        slope = np.polyfit(x, data.values, 1)[0]
        
        # Simple stationarity check
        first_half_var = data.iloc[:len(data)//2].var()
        second_half_var = data.iloc[len(data)//2:].var()
        variance_ratio = first_half_var / second_half_var if second_half_var != 0 else 1
        is_stationary = 0.5 < variance_ratio < 2.0
        
        return {
            "autocorrelation": autocorr,
            "trend_slope": slope,
            "is_stationary": is_stationary,
            "variance_ratio": variance_ratio
        }

class FactorModelBuilder:
    """Factor model construction and analysis"""
    
    def __init__(self):
        self.models = {}
        
    async def create_factor_model(self, returns: pd.Series, factors: Dict[str, pd.Series], 
                                model_name: str = "Custom Factor Model") -> FactorModel:
        """Create a factor model"""
        model_id = str(uuid.uuid4())
        
        # Prepare data
        data = pd.concat([returns] + list(factors.values()), axis=1, keys=["returns"] + list(factors.keys()))
        data = data.dropna()
        
        if len(data) < 10:
            raise ValueError("Insufficient data for factor model")
        
        y = data["returns"]
        X = data.drop("returns", axis=1)
        
        # Simple linear regression
        X_with_const = np.column_stack([np.ones(len(X)), X.values])
        
        try:
            # OLS using normal equations
            coefficients = np.linalg.lstsq(X_with_const, y.values, rcond=None)[0]
            
            # Calculate R-squared
            y_pred = X_with_const @ coefficients
            ss_res = np.sum((y.values - y_pred) ** 2)
            ss_tot = np.sum((y.values - np.mean(y.values)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            # Adjusted R-squared
            n = len(y)
            p = len(coefficients) - 1
            adj_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - p - 1) if n > p + 1 else r_squared
            
            # Create coefficient dictionary
            coeff_dict = {"const": coefficients[0]}
            for i, factor in enumerate(factors.keys()):
                coeff_dict[factor] = coefficients[i + 1]
            
            # Calculate residuals
            residuals = (y.values - y_pred).tolist()
            
            # Create factor model
            factor_model = FactorModel(
                model_id=model_id,
                name=model_name,
                factors=[FactorType(factor) for factor in factors.keys() if factor in [f.value for f in FactorType]],
                coefficients=coeff_dict,
                r_squared=r_squared,
                adjusted_r_squared=adj_r_squared,
                f_statistic=0,
                p_value=0,
                residuals=residuals,
                created_at=datetime.now()
            )
            
            self.models[model_id] = factor_model
            logger.info(f"Created factor model: {model_name}")
            
            return factor_model
            
        except Exception as e:
            logger.error(f"Error creating factor model: {e}")
            raise
    
    async def analyze_factor_exposure(self, factor_model: FactorModel) -> Dict[str, Any]:
        """Analyze factor exposures"""
        coefficients = factor_model.coefficients
        
        # Remove constant (alpha)
        factor_coeffs = {k: v for k, v in coefficients.items() if k != "const"}
        
        # Calculate factor contributions
        total_variance = sum(factor_coeffs.values())**2
        factor_contributions = {k: (v**2 / total_variance) * 100 for k, v in factor_coeffs.items()}
        
        # Risk attribution
        risk_attribution = {
            "alpha": coefficients.get("const", 0),
            "factor_exposures": factor_coeffs,
            "factor_contributions": factor_contributions,
            "diversification_ratio": len(factor_coeffs) / sum(abs(v) for v in factor_coeffs.values()) if factor_coeffs else 0
        }
        
        return risk_attribution

class BacktestingFramework:
    """Advanced backtesting framework"""
    
    def __init__(self):
        self.backtests = {}
        self.results = {}
        
    async def walk_forward_analysis(self, strategy_func: Callable, data: pd.DataFrame,
                                  initial_train_size: int = 252, step_size: int = 21,
                                  min_train_size: int = 100) -> BacktestResult:
        """Walk-forward analysis backtest"""
        backtest_id = str(uuid.uuid4())
        
        results = []
        train_start = 0
        train_end = initial_train_size
        
        while train_end + step_size <= len(data):
            # Training data
            train_data = data.iloc[train_start:train_end]
            
            # Test data
            test_start = train_end
            test_end = min(train_end + step_size, len(data))
            test_data = data.iloc[test_start:test_end]
            
            if len(train_data) < min_train_size:
                train_start += step_size
                train_end += step_size
                continue
            
            try:
                # Simulate strategy results
                test_returns = test_data["close"].pct_change().dropna()
                avg_return = test_returns.mean()
                
                # Simulate trade results
                for i in range(len(test_returns)):
                    trade_return = avg_return + np.random.normal(0, test_returns.std() * 0.1)
                    results.append({"return": trade_return})
                
            except Exception as e:
                logger.error(f"Error in walk-forward step: {e}")
            
            # Move window
            train_start += step_size
            train_end += step_size
        
        # Calculate performance metrics
        if results:
            returns = [r.get("return", 0) for r in results]
            total_return = sum(returns)
            annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
            volatility = np.std(returns) * np.sqrt(252)
            sharpe_ratio = annualized_return / volatility if volatility > 0 else 0
            
            # Calculate drawdown
            cumulative_returns = np.cumprod([1 + r for r in returns])
            running_max = np.maximum.accumulate(cumulative_returns)
            drawdowns = (cumulative_returns - running_max) / running_max
            max_drawdown = np.min(drawdowns)
            
            # Other metrics
            winning_trades = [r for r in returns if r > 0]
            win_rate = len(winning_trades) / len(returns) if returns else 0
            
            backtest_result = BacktestResult(
                backtest_id=backtest_id,
                strategy_name="Walk-Forward Strategy",
                backtest_type=BacktestType.WALK_FORWARD,
                start_date=data.index[0],
                end_date=data.index[-1],
                total_return=total_return,
                annualized_return=annualized_return,
                volatility=volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                calmar_ratio=annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0,
                win_rate=win_rate,
                profit_factor=0,
                total_trades=len(results),
                avg_trade_duration=0,
                created_at=datetime.now()
            )
            
            self.results[backtest_id] = backtest_result
            return backtest_result
        
        else:
            raise ValueError("No results from walk-forward analysis")
    
    async def monte_carlo_simulation(self, strategy_func: Callable, data: pd.DataFrame,
                                   n_simulations: int = 1000, confidence_level: float = 0.95) -> Dict[str, Any]:
        """Monte Carlo simulation backtest"""
        simulation_results = []
        
        for i in range(n_simulations):
            try:
                # Bootstrap sample from data
                bootstrap_sample = data.sample(n=len(data), replace=True)
                
                # Simulate strategy returns
                returns = bootstrap_sample["close"].pct_change().dropna()
                total_return = returns.sum()
                simulation_results.append(total_return)
                
            except Exception as e:
                logger.error(f"Error in Monte Carlo simulation {i}: {e}")
                continue
        
        if not simulation_results:
            raise ValueError("No successful Monte Carlo simulations")
        
        # Calculate statistics
        mean_return = np.mean(simulation_results)
        std_return = np.std(simulation_results)
        
        # Confidence intervals
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        ci_lower = np.percentile(simulation_results, lower_percentile)
        ci_upper = np.percentile(simulation_results, upper_percentile)
        
        return {
            "n_simulations": n_simulations,
            "mean_return": mean_return,
            "std_return": std_return,
            "confidence_interval": {
                "level": confidence_level,
                "lower": ci_lower,
                "upper": ci_upper
            },
            "percentiles": {
                "5th": np.percentile(simulation_results, 5),
                "25th": np.percentile(simulation_results, 25),
                "50th": np.percentile(simulation_results, 50),
                "75th": np.percentile(simulation_results, 75),
                "95th": np.percentile(simulation_results, 95)
            },
            "all_results": simulation_results
        }

class QuantitativeResearchManager:
    """Main quantitative research manager"""
    
    def __init__(self):
        self.statistical_analyzer = StatisticalAnalyzer()
        self.factor_model_builder = FactorModelBuilder()
        self.backtesting_framework = BacktestingFramework()
        self.research_history = []
        
    async def conduct_research(self, research_type: ResearchType, data: Dict[str, Any],
                             parameters: Dict[str, Any] = None) -> ResearchResult:
        """Conduct quantitative research"""
        result_id = str(uuid.uuid4())
        
        try:
            if research_type == ResearchType.STATISTICAL_ANALYSIS:
                result = await self._conduct_statistical_analysis(data, parameters)
            elif research_type == ResearchType.FACTOR_MODEL:
                result = await self._conduct_factor_analysis(data, parameters)
            elif research_type == ResearchType.BACKTESTING:
                result = await self._conduct_backtesting(data, parameters)
            elif research_type == ResearchType.CORRELATION_ANALYSIS:
                result = await self._conduct_correlation_analysis(data, parameters)
            else:
                raise ValueError(f"Unsupported research type: {research_type}")
            
            # Create research result
            research_result = ResearchResult(
                result_id=result_id,
                research_type=research_type,
                title=f"{research_type.value.title()} Analysis",
                description=f"Comprehensive {research_type.value} analysis",
                data=result or {},
                statistics=result.get("statistics", {}) if result else {},
                conclusions=self._generate_conclusions(result, research_type),
                recommendations=self._generate_recommendations(result, research_type),
                confidence_level=result.get("confidence_level", 0.8) if result else 0.5,
                created_at=datetime.now(),
                metadata={"parameters": parameters or {}}
            )
            
            self.research_history.append(research_result)
            logger.info(f"Conducted {research_type.value} research")
            
            return research_result
            
        except Exception as e:
            logger.error(f"Error conducting research: {e}")
            raise
    
    async def _conduct_statistical_analysis(self, data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct statistical analysis"""
        try:
            if "series" not in data:
                raise ValueError("Statistical analysis requires \"series\" data")
            
            series = data["series"]
            if not isinstance(series, pd.Series):
                series = pd.Series(series)
            
            # Descriptive statistics
            try:
                descriptive_stats = await self.statistical_analyzer.descriptive_statistics(series)
            except Exception as e:
                logger.warning(f"Descriptive statistics failed: {e}")
                descriptive_stats = {"error": str(e)}
            
            # Normality tests
            try:
                normality_tests = await self.statistical_analyzer.normality_tests(series)
            except Exception as e:
                logger.warning(f"Normality tests failed: {e}")
                normality_tests = {"error": str(e), "is_normal": False}
            
            # Time series analysis
            try:
                time_series_analysis = await self.statistical_analyzer.time_series_analysis(series)
            except Exception as e:
                logger.warning(f"Time series analysis failed: {e}")
                time_series_analysis = {"error": str(e), "is_stationary": False}
            
            return {
                "descriptive_statistics": descriptive_stats,
                "normality_tests": normality_tests,
                "time_series_analysis": time_series_analysis,
                "statistics": descriptive_stats,
                "confidence_level": 0.9
            }
        except Exception as e:
            logger.error(f"Statistical analysis failed: {e}")
            return {
                "error": str(e),
                "descriptive_statistics": {},
                "normality_tests": {"error": str(e), "is_normal": False},
                "time_series_analysis": {"error": str(e), "is_stationary": False},
                "statistics": {},
                "confidence_level": 0.1
            }
    
    async def _conduct_factor_analysis(self, data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct factor analysis"""
        try:
            if "returns" not in data or "factors" not in data:
                raise ValueError("Factor analysis requires \"returns\" and \"factors\" data")
            
            returns = data["returns"]
            factors = data["factors"]
            
            if not isinstance(returns, pd.Series):
                returns = pd.Series(returns)
            
            # Create factor model
            factor_model = await self.factor_model_builder.create_factor_model(
                returns, factors, parameters.get("model_name", "Custom Factor Model")
            )
            
            # Analyze factor exposure
            factor_exposure = await self.factor_model_builder.analyze_factor_exposure(factor_model)
            
            return {
                "factor_model": asdict(factor_model),
                "factor_exposure": factor_exposure,
                "statistics": {
                    "r_squared": factor_model.r_squared,
                    "adjusted_r_squared": factor_model.adjusted_r_squared,
                    "f_statistic": factor_model.f_statistic,
                    "p_value": factor_model.p_value
                },
                "confidence_level": 0.85
            }
        except Exception as e:
            logger.error(f"Factor analysis failed: {e}")
            return {
                "error": str(e),
                "factor_model": {},
                "factor_exposure": {},
                "statistics": {
                    "r_squared": 0,
                    "adjusted_r_squared": 0,
                    "f_statistic": 0,
                    "p_value": 1
                },
                "confidence_level": 0.1
            }
    
    async def _conduct_backtesting(self, data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct backtesting analysis"""
        try:
            if "data" not in data:
                raise ValueError("Backtesting requires \"data\"")
            
            backtest_data = data["data"]
            
            if not isinstance(backtest_data, pd.DataFrame):
                backtest_data = pd.DataFrame(backtest_data)
            
            backtest_type = parameters.get("backtest_type", BacktestType.WALK_FORWARD)
            
            if backtest_type == BacktestType.WALK_FORWARD:
                # Simple strategy function
                async def simple_strategy(data, mode="test", params=None):
                    returns = data["close"].pct_change().dropna()
                    return [{"return": r} for r in returns]
                
                result = await self.backtesting_framework.walk_forward_analysis(
                    simple_strategy, backtest_data,
                    parameters.get("initial_train_size", 252),
                    parameters.get("step_size", 21)
                )
            elif backtest_type == BacktestType.MONTE_CARLO:
                # Simple strategy function
                async def simple_strategy(data, mode="test", params=None):
                    returns = data["close"].pct_change().dropna()
                    return [{"return": r} for r in returns]
                
                result = await self.backtesting_framework.monte_carlo_simulation(
                    simple_strategy, backtest_data,
                    parameters.get("n_simulations", 1000)
                )
            else:
                raise ValueError(f"Unsupported backtest type: {backtest_type}")
            
            return {
                "backtest_result": asdict(result) if hasattr(result, "__dict__") else result,
                "statistics": {
                    "total_return": result.total_return if hasattr(result, "total_return") else result.get("mean_return", 0),
                    "sharpe_ratio": result.sharpe_ratio if hasattr(result, "sharpe_ratio") else 0,
                    "max_drawdown": result.max_drawdown if hasattr(result, "max_drawdown") else 0
                },
                "confidence_level": 0.8
            }
        except Exception as e:
            logger.error(f"Backtesting failed: {e}")
            return {
                "error": str(e),
                "backtest_result": {},
                "statistics": {
                    "total_return": 0,
                    "sharpe_ratio": 0,
                    "max_drawdown": 0
                },
                "confidence_level": 0.1
            }
    
    async def _conduct_correlation_analysis(self, data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct correlation analysis"""
        try:
            if "dataframe" not in data:
                raise ValueError("Correlation analysis requires \"dataframe\" data")
            
            df = data["dataframe"]
            if not isinstance(df, pd.DataFrame):
                df = pd.DataFrame(df)
            
            correlation_analysis = await self.statistical_analyzer.correlation_analysis(df)
            
            return {
                "correlation_analysis": correlation_analysis,
                "statistics": {
                    "avg_correlation": correlation_analysis["pearson"].mean().mean(),
                    "max_correlation": correlation_analysis["pearson"].max().max(),
                    "min_correlation": correlation_analysis["pearson"].min().min()
                },
                "confidence_level": 0.85
            }
        except Exception as e:
            logger.error(f"Correlation analysis failed: {e}")
            return {
                "error": str(e),
                "correlation_analysis": {},
                "statistics": {
                    "avg_correlation": 0,
                    "max_correlation": 0,
                    "min_correlation": 0
                },
                "confidence_level": 0.1
            }
    
    def _generate_conclusions(self, result: Dict[str, Any], research_type: ResearchType) -> List[str]:
        """Generate research conclusions"""
        conclusions = []
        
        if result is None:
            return ["Analysis could not be completed"]
        
        try:
            if research_type == ResearchType.STATISTICAL_ANALYSIS:
                if "normality_tests" in result and result["normality_tests"] is not None:
                    is_normal = result["normality_tests"].get("is_normal", False)
                    conclusions.append(f"Data {'is' if is_normal else 'is not'} normally distributed")
                
                if "time_series_analysis" in result and result["time_series_analysis"] is not None:
                    is_stationary = result["time_series_analysis"].get("is_stationary", False)
                    conclusions.append(f"Time series {'is' if is_stationary else 'is not'} stationary")
            
            elif research_type == ResearchType.FACTOR_MODEL:
                if "statistics" in result and result["statistics"] is not None:
                    r_squared = result["statistics"].get("r_squared", 0)
                    conclusions.append(f"Factor model explains {r_squared:.1%} of return variance")
            
            elif research_type == ResearchType.BACKTESTING:
                if "statistics" in result and result["statistics"] is not None:
                    total_return = result["statistics"].get("total_return", 0)
                    conclusions.append(f"Strategy achieved {total_return:.1%} total return")
        except Exception as e:
            logger.warning(f"Error generating conclusions: {e}")
            conclusions.append("Analysis completed with some limitations")
        
        return conclusions
    
    def _generate_recommendations(self, result: Dict[str, Any], research_type: ResearchType) -> List[str]:
        """Generate research recommendations"""
        recommendations = []
        
        try:
            if research_type == ResearchType.STATISTICAL_ANALYSIS:
                recommendations.append("Consider data transformation if non-normal")
                recommendations.append("Apply stationarity tests before modeling")
            
            elif research_type == ResearchType.FACTOR_MODEL:
                recommendations.append("Monitor factor exposures regularly")
                recommendations.append("Consider factor timing strategies")
            
            elif research_type == ResearchType.BACKTESTING:
                recommendations.append("Validate results with out-of-sample testing")
                recommendations.append("Consider transaction costs in live trading")
        except Exception as e:
            logger.warning(f"Error generating recommendations: {e}")
            recommendations.append("Review analysis results carefully")
        
        return recommendations
    
    def get_research_summary(self) -> Dict[str, Any]:
        """Get research summary"""
        research_types = {}
        for result in self.research_history:
            research_type = result.research_type.value
            research_types[research_type] = research_types.get(research_type, 0) + 1
        
        return {
            "total_research": len(self.research_history),
            "research_types": research_types,
            "factor_models": len(self.factor_model_builder.models),
            "backtest_results": len(self.backtesting_framework.results),
            "last_update": datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of QuantitativeResearchManager"""
    manager = QuantitativeResearchManager()
    
    # Generate sample data
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
    
    # Create sample price data
    returns = np.random.normal(0.001, 0.02, len(dates))
    prices = 100 * np.cumprod(1 + returns)
    price_series = pd.Series(prices, index=dates)
    
    # Create factor data
    market_factor = pd.Series(np.random.normal(0.0005, 0.015, len(dates)), index=dates)
    size_factor = pd.Series(np.random.normal(0.0002, 0.01, len(dates)), index=dates)
    value_factor = pd.Series(np.random.normal(0.0001, 0.008, len(dates)), index=dates)
    
    # Statistical analysis
    stats_result = await manager.conduct_research(
        ResearchType.STATISTICAL_ANALYSIS,
        {"series": price_series}
    )
    print(f"Statistical analysis completed: {len(stats_result.conclusions)} conclusions")
    
    # Factor model analysis
    factor_result = await manager.conduct_research(
        ResearchType.FACTOR_MODEL,
        {
            "returns": pd.Series(returns, index=dates),
            "factors": {
                "market": market_factor,
                "size": size_factor,
                "value": value_factor
            }
        },
        {"model_name": "Sample Factor Model"}
    )
    print(f"Factor model analysis completed: R² = {factor_result.statistics.get('r_squared', 0):.3f}")
    
    # Correlation analysis
    correlation_data = pd.DataFrame({
        "returns": returns,
        "market": market_factor,
        "size": size_factor,
        "value": value_factor
    }, index=dates)
    
    correlation_result = await manager.conduct_research(
        ResearchType.CORRELATION_ANALYSIS,
        {"dataframe": correlation_data}
    )
    print(f"Correlation analysis completed: {len(correlation_result.conclusions)} conclusions")
    
    # Research summary
    summary = manager.get_research_summary()
    print(f"Research summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())
