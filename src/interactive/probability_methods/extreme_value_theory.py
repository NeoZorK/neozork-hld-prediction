# -*- coding: utf-8 -*-
"""
Extreme Value Theory for NeoZork Interactive ML Trading Strategy Development.

This module provides extreme value theory analysis for market risk assessment.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
import scipy.stats as stats
from scipy.optimize import minimize
import warnings

class ExtremeValueTheory:
    """
    Extreme Value Theory system for analyzing extreme market events.
    
    Features:
    - Generalized Extreme Value (GEV) distribution fitting
    - Peak Over Threshold (POT) method
    - Value at Risk (VaR) and Expected Shortfall (ES) estimation
    - Return level estimation
    - Extreme value index estimation
    """
    
    def __init__(self):
        """Initialize the EVT system."""
        self.gev_models = {}
        self.pot_models = {}
        self.extreme_events = {}
        self.return_levels = {}
    
    def fit_gev_distribution(self, data: pd.Series, block_size: int = 252) -> Dict[str, Any]:
        """
        Fit Generalized Extreme Value distribution to block maxima.
        
        Args:
            data: Time series data
            block_size: Size of blocks for maxima extraction
            
        Returns:
            GEV distribution parameters and statistics
        """
        try:
            # Extract block maxima
            block_maxima = self._extract_block_maxima(data, block_size)
            
            if len(block_maxima) < 10:
                return {"status": "error", "message": "Insufficient data for GEV fitting"}
            
            # Fit GEV distribution using method of moments
            gev_params = self._fit_gev_moments(block_maxima)
            
            # Calculate goodness of fit
            ks_stat, ks_pvalue = stats.kstest(block_maxima, 
                                            lambda x: self._gev_cdf(x, gev_params['loc'], 
                                                                  gev_params['scale'], 
                                                                  gev_params['shape']))
            
            # Calculate return levels
            return_levels = self._calculate_return_levels(gev_params, [10, 50, 100, 500, 1000])
            
            result = {
                "status": "success",
                "distribution": "gev",
                "parameters": gev_params,
                "block_size": block_size,
                "n_blocks": len(block_maxima),
                "ks_statistic": ks_stat,
                "ks_pvalue": ks_pvalue,
                "return_levels": return_levels,
                "block_maxima": block_maxima.tolist()
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"GEV fitting failed: {str(e)}"}
    
    def fit_pot_model(self, data: pd.Series, threshold: Optional[float] = None, 
                     threshold_percentile: float = 95.0) -> Dict[str, Any]:
        """
        Fit Peak Over Threshold model using Generalized Pareto Distribution.
        
        Args:
            data: Time series data
            threshold: Fixed threshold value
            threshold_percentile: Percentile for automatic threshold selection
            
        Returns:
            POT model parameters and statistics
        """
        try:
            # Determine threshold
            if threshold is None:
                threshold = np.percentile(data, threshold_percentile)
            
            # Extract exceedances
            exceedances = data[data > threshold] - threshold
            
            if len(exceedances) < 10:
                return {"status": "error", "message": "Insufficient exceedances for POT fitting"}
            
            # Fit GPD using method of moments
            gpd_params = self._fit_gpd_moments(exceedances)
            
            # Calculate VaR and ES
            var_levels = [0.95, 0.99, 0.995, 0.999]
            var_es = self._calculate_var_es(gpd_params, threshold, var_levels)
            
            # Calculate mean excess function
            mef = self._calculate_mean_excess_function(data, threshold)
            
            result = {
                "status": "success",
                "model": "pot",
                "threshold": threshold,
                "threshold_percentile": threshold_percentile,
                "n_exceedances": len(exceedances),
                "gpd_parameters": gpd_params,
                "var_es": var_es,
                "mean_excess_function": mef,
                "exceedances": exceedances.tolist()
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"POT fitting failed: {str(e)}"}
    
    def calculate_extreme_value_index(self, data: pd.Series, k: int = 10) -> Dict[str, Any]:
        """
        Calculate extreme value index using Hill estimator.
        
        Args:
            data: Time series data
            k: Number of upper order statistics to use
            
        Returns:
            Extreme value index and related statistics
        """
        try:
            # Sort data in descending order
            sorted_data = np.sort(data)[::-1]
            
            if k >= len(sorted_data):
                k = len(sorted_data) - 1
            
            # Calculate Hill estimator
            hill_estimator = self._calculate_hill_estimator(sorted_data, k)
            
            # Calculate confidence intervals
            ci_lower, ci_upper = self._calculate_hill_ci(sorted_data, k, hill_estimator)
            
            # Calculate Pickands estimator for comparison
            pickands_estimator = self._calculate_pickands_estimator(sorted_data, k)
            
            result = {
                "status": "success",
                "hill_estimator": hill_estimator,
                "pickands_estimator": pickands_estimator,
                "k": k,
                "confidence_interval": [ci_lower, ci_upper],
                "tail_index": 1 / hill_estimator if hill_estimator > 0 else np.inf
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Extreme value index calculation failed: {str(e)}"}
    
    def estimate_return_periods(self, data: pd.Series, return_levels: List[float]) -> Dict[str, Any]:
        """
        Estimate return periods for given return levels.
        
        Args:
            data: Time series data
            return_levels: List of return levels to analyze
            
        Returns:
            Return periods for each level
        """
        try:
            return_periods = {}
            
            for level in return_levels:
                # Count exceedances
                exceedances = (data > level).sum()
                total_observations = len(data)
                
                # Calculate return period
                if exceedances > 0:
                    return_period = total_observations / exceedances
                else:
                    return_period = np.inf
                
                return_periods[level] = {
                    "return_period": return_period,
                    "exceedances": exceedances,
                    "exceedance_probability": exceedances / total_observations
                }
            
            result = {
                "status": "success",
                "return_periods": return_periods,
                "total_observations": total_observations
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Return period estimation failed: {str(e)}"}
    
    def _extract_block_maxima(self, data: pd.Series, block_size: int) -> np.ndarray:
        """Extract block maxima from time series."""
        n_blocks = len(data) // block_size
        block_maxima = []
        
        for i in range(n_blocks):
            start_idx = i * block_size
            end_idx = start_idx + block_size
            block_data = data.iloc[start_idx:end_idx]
            if len(block_data) > 0:
                block_maxima.append(block_data.max())
        
        return np.array(block_maxima)
    
    def _fit_gev_moments(self, data: np.ndarray) -> Dict[str, float]:
        """Fit GEV distribution using method of moments."""
        # Calculate sample moments
        mean_val = np.mean(data)
        var_val = np.var(data)
        skew_val = stats.skew(data)
        
        # Estimate shape parameter using skewness
        if skew_val > 0:
            shape = 0.1  # Positive shape (Fréchet type)
        elif skew_val < 0:
            shape = -0.1  # Negative shape (Weibull type)
        else:
            shape = 0.0  # Gumbel type
        
        # Estimate scale and location
        if abs(shape) < 1e-6:  # Gumbel case
            scale = np.sqrt(6 * var_val) / np.pi
            loc = mean_val - 0.5772 * scale
        else:
            # Approximate estimation for non-zero shape
            scale = np.sqrt(var_val) * (1 + shape)
            loc = mean_val - scale * (1 - np.exp(-shape)) / shape
        
        return {
            "loc": loc,
            "scale": scale,
            "shape": shape
        }
    
    def _fit_gpd_moments(self, exceedances: np.ndarray) -> Dict[str, float]:
        """Fit GPD using method of moments."""
        if len(exceedances) == 0:
            return {"scale": 0.0, "shape": 0.0}
        
        # Calculate sample moments
        mean_excess = np.mean(exceedances)
        var_excess = np.var(exceedances)
        
        # Estimate shape parameter
        if var_excess > 0:
            shape = 0.5 * (1 - mean_excess**2 / var_excess)
        else:
            shape = 0.0
        
        # Estimate scale parameter
        if shape != 0:
            scale = mean_excess * (1 - shape)
        else:
            scale = mean_excess
        
        return {
            "scale": scale,
            "shape": shape
        }
    
    def _gev_cdf(self, x: np.ndarray, loc: float, scale: float, shape: float) -> np.ndarray:
        """Calculate GEV CDF."""
        if abs(shape) < 1e-6:  # Gumbel case
            return np.exp(-np.exp(-(x - loc) / scale))
        else:
            y = 1 + shape * (x - loc) / scale
            y = np.maximum(y, 1e-10)  # Avoid negative values
            return np.exp(-y**(-1/shape))
    
    def _calculate_return_levels(self, gev_params: Dict[str, float], 
                                return_periods: List[int]) -> Dict[int, float]:
        """Calculate return levels for given return periods."""
        loc = gev_params['loc']
        scale = gev_params['scale']
        shape = gev_params['shape']
        
        return_levels = {}
        
        for period in return_periods:
            # Calculate return level
            if abs(shape) < 1e-6:  # Gumbel case
                return_level = loc - scale * np.log(-np.log(1 - 1/period))
            else:
                return_level = loc + scale * ((np.log(period))**(-shape) - 1) / shape
            
            return_levels[period] = return_level
        
        return return_levels
    
    def _calculate_var_es(self, gpd_params: Dict[str, float], threshold: float, 
                         confidence_levels: List[float]) -> Dict[str, Dict[str, float]]:
        """Calculate VaR and ES using POT model."""
        scale = gpd_params['scale']
        shape = gpd_params['shape']
        
        var_es = {}
        
        for cl in confidence_levels:
            # Calculate VaR
            if shape != 0:
                var = threshold + scale * ((1 - cl)**(-shape) - 1) / shape
            else:
                var = threshold - scale * np.log(1 - cl)
            
            # Calculate ES
            if shape < 1:
                es = var + scale / (1 - shape)
            else:
                es = var  # ES not defined for shape >= 1
            
            var_es[cl] = {
                "var": var,
                "es": es
            }
        
        return var_es
    
    def _calculate_mean_excess_function(self, data: pd.Series, threshold: float) -> Dict[str, float]:
        """Calculate mean excess function."""
        exceedances = data[data > threshold] - threshold
        
        if len(exceedances) == 0:
            return {"mean_excess": 0.0, "n_exceedances": 0}
        
        return {
            "mean_excess": np.mean(exceedances),
            "n_exceedances": len(exceedances)
        }
    
    def _calculate_hill_estimator(self, sorted_data: np.ndarray, k: int) -> float:
        """Calculate Hill estimator for extreme value index."""
        if k >= len(sorted_data) or k <= 0:
            return 0.0
        
        # Use k largest observations
        top_k = sorted_data[:k]
        
        # Calculate Hill estimator
        if len(top_k) < 2:
            return 0.0
        
        log_ratios = np.log(top_k[:-1] / top_k[-1])
        hill_estimator = np.mean(log_ratios)
        
        return hill_estimator
    
    def _calculate_hill_ci(self, sorted_data: np.ndarray, k: int, hill_estimator: float) -> Tuple[float, float]:
        """Calculate confidence interval for Hill estimator."""
        if k < 2:
            return 0.0, 0.0
        
        # Asymptotic confidence interval
        se = hill_estimator / np.sqrt(k)
        z_alpha = 1.96  # 95% confidence interval
        
        ci_lower = hill_estimator - z_alpha * se
        ci_upper = hill_estimator + z_alpha * se
        
        return ci_lower, ci_upper
    
    def _calculate_pickands_estimator(self, sorted_data: np.ndarray, k: int) -> float:
        """Calculate Pickands estimator for extreme value index."""
        if k < 4:
            return 0.0
        
        # Use k largest observations
        top_k = sorted_data[:k]
        
        # Calculate Pickands estimator
        if len(top_k) < 4:
            return 0.0
        
        # Use 25th and 75th percentiles of top k
        q25_idx = int(0.25 * len(top_k))
        q75_idx = int(0.75 * len(top_k))
        
        if q25_idx >= q75_idx or q75_idx >= len(top_k):
            return 0.0
        
        pickands_estimator = (1 / np.log(2)) * np.log((top_k[q25_idx] - top_k[-1]) / (top_k[q75_idx] - top_k[-1]))
        
        return pickands_estimator
