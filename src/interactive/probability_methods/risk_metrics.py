# -*- coding: utf-8 -*-
"""
Advanced Risk Metrics for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive risk metrics and analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
import scipy.stats as stats
from scipy.optimize import minimize

class AdvancedRiskMetrics:
    """
    Advanced risk metrics system for comprehensive risk assessment.
    
    Features:
    - Maximum Drawdown Duration
    - Tail Risk Metrics
    - Regime Change Detection
    - Correlation Breakdown Analysis
    - Liquidity Risk Assessment
    - Stress Testing
    """
    
    def __init__(self):
        """Initialize the advanced risk metrics system."""
        self.risk_metrics = {}
        self.regime_models = {}
        self.correlation_models = {}
        self.liquidity_models = {}
    
    def calculate_maximum_drawdown_duration(self, returns: pd.Series) -> Dict[str, Any]:
        """
        Calculate maximum drawdown duration and recovery time.
        
        Args:
            returns: Time series of returns
            
        Returns:
            Maximum drawdown duration metrics
        """
        try:
            # Calculate cumulative returns
            cumulative_returns = (1 + returns).cumprod()
            
            # Calculate running maximum
            running_max = cumulative_returns.expanding().max()
            
            # Calculate drawdown
            drawdown = (cumulative_returns - running_max) / running_max
            
            # Find maximum drawdown
            max_dd = drawdown.min()
            max_dd_date = drawdown.idxmin()
            
            # Find drawdown periods
            drawdown_periods = self._find_drawdown_periods(drawdown)
            
            # Calculate maximum drawdown duration
            max_dd_duration = 0
            max_dd_start = None
            max_dd_end = None
            
            for period in drawdown_periods:
                duration = (period['end'] - period['start']).days
                if duration > max_dd_duration:
                    max_dd_duration = duration
                    max_dd_start = period['start']
                    max_dd_end = period['end']
            
            # Calculate recovery time
            recovery_time = self._calculate_recovery_time(cumulative_returns, max_dd_date)
            
            result = {
                "status": "success",
                "maximum_drawdown": max_dd,
                "max_dd_date": max_dd_date,
                "max_dd_duration_days": max_dd_duration,
                "max_dd_start": max_dd_start,
                "max_dd_end": max_dd_end,
                "recovery_time_days": recovery_time,
                "n_drawdown_periods": len(drawdown_periods),
                "avg_drawdown_duration": np.mean([(p['end'] - p['start']).days for p in drawdown_periods]) if drawdown_periods else 0
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Maximum drawdown duration calculation failed: {str(e)}"}
    
    def calculate_tail_risk_metrics(self, returns: pd.Series, confidence_levels: List[float] = [0.95, 0.99, 0.995]) -> Dict[str, Any]:
        """
        Calculate comprehensive tail risk metrics.
        
        Args:
            returns: Time series of returns
            confidence_levels: List of confidence levels for VaR/ES
            
        Returns:
            Tail risk metrics
        """
        try:
            # Calculate VaR and ES
            var_es = self._calculate_var_es(returns, confidence_levels)
            
            # Calculate tail ratio
            tail_ratio = self._calculate_tail_ratio(returns)
            
            # Calculate expected shortfall ratio
            es_ratio = self._calculate_es_ratio(returns, confidence_levels)
            
            # Calculate tail dependence
            tail_dependence = self._calculate_tail_dependence(returns)
            
            # Calculate extreme value index
            evi = self._calculate_extreme_value_index(returns)
            
            result = {
                "status": "success",
                "var_es": var_es,
                "tail_ratio": tail_ratio,
                "es_ratio": es_ratio,
                "tail_dependence": tail_dependence,
                "extreme_value_index": evi,
                "skewness": stats.skew(returns),
                "kurtosis": stats.kurtosis(returns),
                "jarque_bera_stat": self._calculate_jarque_bera(returns)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Tail risk metrics calculation failed: {str(e)}"}
    
    def detect_regime_changes(self, returns: pd.Series, window_size: int = 252, 
                            significance_level: float = 0.05) -> Dict[str, Any]:
        """
        Detect regime changes in return series.
        
        Args:
            returns: Time series of returns
            window_size: Rolling window size
            significance_level: Significance level for change detection
            
        Returns:
            Regime change detection results
        """
        try:
            # Calculate rolling statistics
            rolling_mean = returns.rolling(window=window_size).mean()
            rolling_std = returns.rolling(window=window_size).std()
            rolling_skew = returns.rolling(window=window_size).skew()
            
            # Detect changes in mean
            mean_changes = self._detect_changes(rolling_mean, significance_level)
            
            # Detect changes in volatility
            vol_changes = self._detect_changes(rolling_std, significance_level)
            
            # Detect changes in skewness
            skew_changes = self._detect_changes(rolling_skew, significance_level)
            
            # Combine all changes
            all_changes = self._combine_changes(mean_changes, vol_changes, skew_changes)
            
            # Identify regimes
            regimes = self._identify_regimes(returns, all_changes)
            
            result = {
                "status": "success",
                "n_regime_changes": len(all_changes),
                "change_dates": all_changes,
                "regimes": regimes,
                "mean_changes": mean_changes,
                "vol_changes": vol_changes,
                "skew_changes": skew_changes,
                "window_size": window_size,
                "significance_level": significance_level
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Regime change detection failed: {str(e)}"}
    
    def analyze_correlation_breakdown(self, returns: pd.DataFrame, 
                                    crisis_periods: Optional[List[Tuple[str, str]]] = None) -> Dict[str, Any]:
        """
        Analyze correlation breakdown during crisis periods.
        
        Args:
            returns: DataFrame of asset returns
            crisis_periods: List of crisis period tuples (start, end)
            
        Returns:
            Correlation breakdown analysis
        """
        try:
            # Calculate full period correlation
            full_correlation = returns.corr()
            
            # Identify crisis periods if not provided
            if crisis_periods is None:
                crisis_periods = self._identify_crisis_periods(returns)
            
            # Calculate crisis period correlations
            crisis_correlations = {}
            for i, (start, end) in enumerate(crisis_periods):
                crisis_data = returns.loc[start:end]
                if len(crisis_data) > 10:  # Minimum observations
                    crisis_correlations[f"crisis_{i+1}"] = crisis_data.corr()
            
            # Calculate correlation breakdown metrics
            breakdown_metrics = self._calculate_correlation_breakdown(full_correlation, crisis_correlations)
            
            # Calculate dynamic correlation
            dynamic_correlation = self._calculate_dynamic_correlation(returns)
            
            result = {
                "status": "success",
                "full_period_correlation": full_correlation.to_dict(),
                "crisis_correlations": {k: v.to_dict() for k, v in crisis_correlations.items()},
                "breakdown_metrics": breakdown_metrics,
                "dynamic_correlation": dynamic_correlation,
                "crisis_periods": crisis_periods
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Correlation breakdown analysis failed: {str(e)}"}
    
    def assess_liquidity_risk(self, price_data: pd.DataFrame, volume_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Assess liquidity risk using price and volume data.
        
        Args:
            price_data: DataFrame of asset prices
            volume_data: DataFrame of trading volumes
            
        Returns:
            Liquidity risk assessment
        """
        try:
            # Calculate liquidity metrics
            liquidity_metrics = {}
            
            for asset in price_data.columns:
                if asset in volume_data.columns:
                    # Calculate Amihud illiquidity ratio
                    amihud_ratio = self._calculate_amihud_ratio(price_data[asset], volume_data[asset])
                    
                    # Calculate turnover ratio
                    turnover_ratio = self._calculate_turnover_ratio(volume_data[asset])
                    
                    # Calculate bid-ask spread proxy
                    spread_proxy = self._calculate_spread_proxy(price_data[asset])
                    
                    # Calculate liquidity risk score
                    liquidity_score = self._calculate_liquidity_score(amihud_ratio, turnover_ratio, spread_proxy)
                    
                    liquidity_metrics[asset] = {
                        "amihud_ratio": amihud_ratio,
                        "turnover_ratio": turnover_ratio,
                        "spread_proxy": spread_proxy,
                        "liquidity_score": liquidity_score
                    }
            
            # Calculate portfolio liquidity risk
            portfolio_liquidity = self._calculate_portfolio_liquidity_risk(liquidity_metrics)
            
            result = {
                "status": "success",
                "asset_liquidity_metrics": liquidity_metrics,
                "portfolio_liquidity_risk": portfolio_liquidity,
                "liquidity_risk_level": self._classify_liquidity_risk(portfolio_liquidity)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Liquidity risk assessment failed: {str(e)}"}
    
    def _find_drawdown_periods(self, drawdown: pd.Series) -> List[Dict[str, Any]]:
        """Find all drawdown periods."""
        periods = []
        in_drawdown = False
        start_date = None
        
        for date, value in drawdown.items():
            if value < 0 and not in_drawdown:
                in_drawdown = True
                start_date = date
            elif value >= 0 and in_drawdown:
                in_drawdown = False
                periods.append({
                    "start": start_date,
                    "end": date,
                    "max_drawdown": drawdown.loc[start_date:date].min()
                })
        
        # Handle case where drawdown continues to end
        if in_drawdown:
            periods.append({
                "start": start_date,
                "end": drawdown.index[-1],
                "max_drawdown": drawdown.loc[start_date:].min()
            })
        
        return periods
    
    def _calculate_recovery_time(self, cumulative_returns: pd.Series, max_dd_date: pd.Timestamp) -> int:
        """Calculate time to recovery from maximum drawdown."""
        max_dd_value = cumulative_returns.loc[max_dd_date]
        
        # Find when cumulative returns exceed the pre-drawdown level
        recovery_data = cumulative_returns.loc[max_dd_date:]
        recovery_idx = (recovery_data >= max_dd_value).idxmax()
        
        if recovery_idx is not None:
            return (recovery_idx - max_dd_date).days
        else:
            return -1  # No recovery found
    
    def _calculate_var_es(self, returns: pd.Series, confidence_levels: List[float]) -> Dict[str, Dict[str, float]]:
        """Calculate VaR and ES for given confidence levels."""
        var_es = {}
        
        for cl in confidence_levels:
            # Calculate VaR
            var = np.percentile(returns, (1 - cl) * 100)
            
            # Calculate ES
            es = returns[returns <= var].mean()
            
            var_es[cl] = {
                "var": var,
                "es": es
            }
        
        return var_es
    
    def _calculate_tail_ratio(self, returns: pd.Series) -> float:
        """Calculate tail ratio (95% VaR / 5% VaR)."""
        var_95 = np.percentile(returns, 5)
        var_5 = np.percentile(returns, 95)
        
        if var_5 != 0:
            return abs(var_95 / var_5)
        else:
            return np.inf
    
    def _calculate_es_ratio(self, returns: pd.Series, confidence_levels: List[float]) -> Dict[str, float]:
        """Calculate expected shortfall ratios."""
        es_ratios = {}
        
        for cl in confidence_levels:
            var = np.percentile(returns, (1 - cl) * 100)
            es = returns[returns <= var].mean()
            
            if var != 0:
                es_ratios[cl] = abs(es / var)
            else:
                es_ratios[cl] = np.inf
        
        return es_ratios
    
    def _calculate_tail_dependence(self, returns: pd.Series) -> Dict[str, float]:
        """Calculate tail dependence metrics."""
        # Calculate lower and upper tail dependence
        threshold = 0.05
        n = len(returns)
        k = int(threshold * n)
        
        sorted_returns = returns.sort_values()
        
        # Lower tail dependence
        lower_tail = sorted_returns.iloc[:k]
        lower_tail_dep = (lower_tail < lower_tail.quantile(threshold)).mean()
        
        # Upper tail dependence
        upper_tail = sorted_returns.iloc[-k:]
        upper_tail_dep = (upper_tail > upper_tail.quantile(1 - threshold)).mean()
        
        return {
            "lower_tail_dependence": lower_tail_dep,
            "upper_tail_dependence": upper_tail_dep
        }
    
    def _calculate_extreme_value_index(self, returns: pd.Series) -> float:
        """Calculate extreme value index using Hill estimator."""
        sorted_returns = returns.sort_values(ascending=False)
        k = min(50, len(sorted_returns) // 4)  # Use 25% of data
        
        if k < 2:
            return 0.0
        
        top_k = sorted_returns.iloc[:k]
        log_ratios = np.log(top_k.iloc[:-1] / top_k.iloc[-1])
        
        return np.mean(log_ratios)
    
    def _calculate_jarque_bera(self, returns: pd.Series) -> Dict[str, float]:
        """Calculate Jarque-Bera test for normality."""
        jb_stat, jb_pvalue = stats.jarque_bera(returns)
        
        return {
            "statistic": jb_stat,
            "p_value": jb_pvalue,
            "is_normal": jb_pvalue > 0.05
        }
    
    def _detect_changes(self, series: pd.Series, significance_level: float) -> List[pd.Timestamp]:
        """Detect structural changes in time series."""
        changes = []
        
        # Use CUSUM test for change detection
        n = len(series)
        if n < 20:
            return changes
        
        # Calculate CUSUM statistics
        mean_val = series.mean()
        std_val = series.std()
        
        if std_val == 0:
            return changes
        
        cusum = (series - mean_val).cumsum() / (std_val * np.sqrt(n))
        
        # Detect changes
        threshold = 1.96  # 95% confidence
        for i in range(1, len(cusum)):
            if abs(cusum.iloc[i]) > threshold and abs(cusum.iloc[i-1]) <= threshold:
                changes.append(series.index[i])
        
        return changes
    
    def _combine_changes(self, mean_changes: List, vol_changes: List, skew_changes: List) -> List[pd.Timestamp]:
        """Combine all detected changes."""
        all_changes = set(mean_changes + vol_changes + skew_changes)
        return sorted(list(all_changes))
    
    def _identify_regimes(self, returns: pd.Series, change_dates: List[pd.Timestamp]) -> List[Dict[str, Any]]:
        """Identify regimes based on change dates."""
        regimes = []
        
        if not change_dates:
            # Single regime
            regimes.append({
                "start": returns.index[0],
                "end": returns.index[-1],
                "mean": returns.mean(),
                "std": returns.std(),
                "skewness": stats.skew(returns),
                "kurtosis": stats.kurtosis(returns)
            })
        else:
            # Multiple regimes
            start_date = returns.index[0]
            for change_date in change_dates:
                regime_data = returns.loc[start_date:change_date]
                if len(regime_data) > 10:  # Minimum observations
                    regimes.append({
                        "start": start_date,
                        "end": change_date,
                        "mean": regime_data.mean(),
                        "std": regime_data.std(),
                        "skewness": stats.skew(regime_data),
                        "kurtosis": stats.kurtosis(regime_data)
                    })
                start_date = change_date
            
            # Final regime
            final_regime_data = returns.loc[start_date:]
            if len(final_regime_data) > 10:
                regimes.append({
                    "start": start_date,
                    "end": returns.index[-1],
                    "mean": final_regime_data.mean(),
                    "std": final_regime_data.std(),
                    "skewness": stats.skew(final_regime_data),
                    "kurtosis": stats.kurtosis(final_regime_data)
                })
        
        return regimes
    
    def _identify_crisis_periods(self, returns: pd.DataFrame) -> List[Tuple[str, str]]:
        """Identify crisis periods based on extreme volatility."""
        # Calculate rolling volatility
        vol = returns.rolling(window=20).std()
        
        # Identify high volatility periods
        vol_threshold = vol.quantile(0.95).mean()
        high_vol_periods = vol > vol_threshold
        
        # Find consecutive high volatility periods
        crisis_periods = []
        in_crisis = False
        start_date = None
        
        for date, is_high_vol in high_vol_periods.items():
            if is_high_vol and not in_crisis:
                in_crisis = True
                start_date = date
            elif not is_high_vol and in_crisis:
                in_crisis = False
                if start_date is not None:
                    crisis_periods.append((start_date.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d')))
        
        return crisis_periods
    
    def _calculate_correlation_breakdown(self, full_corr: pd.DataFrame, 
                                       crisis_corrs: Dict[str, pd.DataFrame]) -> Dict[str, float]:
        """Calculate correlation breakdown metrics."""
        breakdown_metrics = {}
        
        for crisis_name, crisis_corr in crisis_corrs.items():
            # Calculate correlation difference
            corr_diff = (crisis_corr - full_corr).abs().mean().mean()
            
            # Calculate correlation increase
            corr_increase = (crisis_corr - full_corr).mean().mean()
            
            breakdown_metrics[crisis_name] = {
                "correlation_difference": corr_diff,
                "correlation_increase": corr_increase
            }
        
        return breakdown_metrics
    
    def _calculate_dynamic_correlation(self, returns: pd.DataFrame) -> pd.DataFrame:
        """Calculate dynamic correlation using rolling windows."""
        window = 60  # 60-day rolling window
        dynamic_corr = returns.rolling(window=window).corr()
        
        return dynamic_corr
    
    def _calculate_amihud_ratio(self, prices: pd.Series, volumes: pd.Series) -> float:
        """Calculate Amihud illiquidity ratio."""
        returns = prices.pct_change().dropna()
        volumes = volumes.reindex(returns.index).fillna(0)
        
        if volumes.sum() == 0:
            return np.inf
        
        amihud_ratio = (abs(returns) / volumes).mean()
        return amihud_ratio
    
    def _calculate_turnover_ratio(self, volumes: pd.Series) -> float:
        """Calculate turnover ratio."""
        if len(volumes) == 0:
            return 0.0
        
        return volumes.mean() / volumes.sum() if volumes.sum() > 0 else 0.0
    
    def _calculate_spread_proxy(self, prices: pd.Series) -> float:
        """Calculate bid-ask spread proxy using high-low range."""
        if len(prices) < 2:
            return 0.0
        
        # Use price volatility as spread proxy
        returns = prices.pct_change().dropna()
        return returns.std() * 2  # Approximate spread
    
    def _calculate_liquidity_score(self, amihud_ratio: float, turnover_ratio: float, spread_proxy: float) -> float:
        """Calculate composite liquidity score."""
        # Normalize metrics (lower is better for amihud and spread)
        amihud_score = 1 / (1 + amihud_ratio) if amihud_ratio > 0 else 0
        turnover_score = turnover_ratio
        spread_score = 1 / (1 + spread_proxy) if spread_proxy > 0 else 0
        
        # Weighted average
        liquidity_score = 0.4 * amihud_score + 0.3 * turnover_score + 0.3 * spread_score
        
        return liquidity_score
    
    def _calculate_portfolio_liquidity_risk(self, liquidity_metrics: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """Calculate portfolio-level liquidity risk."""
        if not liquidity_metrics:
            return {"portfolio_liquidity_score": 0.0, "liquidity_risk_level": "unknown"}
        
        # Calculate weighted average liquidity score
        liquidity_scores = [metrics["liquidity_score"] for metrics in liquidity_metrics.values()]
        portfolio_score = np.mean(liquidity_scores)
        
        return {
            "portfolio_liquidity_score": portfolio_score,
            "min_liquidity_score": min(liquidity_scores),
            "max_liquidity_score": max(liquidity_scores),
            "liquidity_volatility": np.std(liquidity_scores)
        }
    
    def _classify_liquidity_risk(self, portfolio_liquidity: Dict[str, float]) -> str:
        """Classify liquidity risk level."""
        score = portfolio_liquidity.get("portfolio_liquidity_score", 0)
        
        if score >= 0.7:
            return "low"
        elif score >= 0.4:
            return "medium"
        else:
            return "high"
