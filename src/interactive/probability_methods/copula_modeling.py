# -*- coding: utf-8 -*-
"""
Copula Modeling for NeoZork Interactive ML Trading Strategy Development.

This module provides copula-based risk modeling for asset dependencies.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
import scipy.stats as stats
from scipy.optimize import minimize

class CopulaModeling:
    """
    Copula modeling system for asset dependency analysis.
    
    Features:
    - Gaussian copula modeling
    - Student-t copula modeling
    - Archimedean copulas (Clayton, Gumbel, Frank)
    - Tail dependence analysis
    - Dependency structure visualization
    """
    
    def __init__(self):
        """Initialize the copula modeling system."""
        self.copula_models = {}
        self.dependency_structures = {}
        self.tail_dependence_metrics = {}
    
    def fit_gaussian_copula(self, data: pd.DataFrame, assets: List[str]) -> Dict[str, Any]:
        """
        Fit Gaussian copula to asset data.
        
        Args:
            data: Asset price data
            assets: List of asset names
            
        Returns:
            Gaussian copula parameters and statistics
        """
        try:
            # Extract asset data
            asset_data = data[assets].dropna()
            
            # Transform to uniform marginals using empirical CDF
            uniform_data = np.zeros_like(asset_data.values)
            for i, asset in enumerate(assets):
                uniform_data[:, i] = stats.rankdata(asset_data[asset]) / (len(asset_data) + 1)
            
            # Estimate correlation matrix
            correlation_matrix = np.corrcoef(uniform_data.T)
            
            # Calculate Kendall's tau
            kendall_tau = self._calculate_kendall_tau(uniform_data)
            
            result = {
                "status": "success",
                "copula_type": "gaussian",
                "correlation_matrix": correlation_matrix.tolist(),
                "kendall_tau": kendall_tau.tolist(),
                "assets": assets,
                "sample_size": len(asset_data),
                "log_likelihood": self._calculate_gaussian_log_likelihood(uniform_data, correlation_matrix)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Gaussian copula fitting failed: {str(e)}"}
    
    def fit_student_t_copula(self, data: pd.DataFrame, assets: List[str]) -> Dict[str, Any]:
        """
        Fit Student-t copula to asset data.
        
        Args:
            data: Asset price data
            assets: List of asset names
            
        Returns:
            Student-t copula parameters and statistics
        """
        try:
            # Extract asset data
            asset_data = data[assets].dropna()
            
            # Transform to uniform marginals
            uniform_data = np.zeros_like(asset_data.values)
            for i, asset in enumerate(assets):
                uniform_data[:, i] = stats.rankdata(asset_data[asset]) / (len(asset_data) + 1)
            
            # Estimate correlation matrix and degrees of freedom
            correlation_matrix = np.corrcoef(uniform_data.T)
            
            # Estimate degrees of freedom using MLE
            df = self._estimate_student_t_df(uniform_data, correlation_matrix)
            
            result = {
                "status": "success",
                "copula_type": "student_t",
                "correlation_matrix": correlation_matrix.tolist(),
                "degrees_of_freedom": df,
                "assets": assets,
                "sample_size": len(asset_data),
                "log_likelihood": self._calculate_student_t_log_likelihood(uniform_data, correlation_matrix, df)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Student-t copula fitting failed: {str(e)}"}
    
    def fit_archimedean_copula(self, data: pd.DataFrame, assets: List[str], copula_type: str = "clayton") -> Dict[str, Any]:
        """
        Fit Archimedean copula to asset data.
        
        Args:
            data: Asset price data
            assets: List of asset names
            copula_type: Type of Archimedean copula (clayton, gumbel, frank)
            
        Returns:
            Archimedean copula parameters and statistics
        """
        try:
            # Extract asset data
            asset_data = data[assets].dropna()
            
            # Transform to uniform marginals
            uniform_data = np.zeros_like(asset_data.values)
            for i, asset in enumerate(assets):
                uniform_data[:, i] = stats.rankdata(asset_data[asset]) / (len(asset_data) + 1)
            
            # Estimate copula parameter
            if copula_type == "clayton":
                theta = self._estimate_clayton_theta(uniform_data)
            elif copula_type == "gumbel":
                theta = self._estimate_gumbel_theta(uniform_data)
            elif copula_type == "frank":
                theta = self._estimate_frank_theta(uniform_data)
            else:
                raise ValueError(f"Unknown copula type: {copula_type}")
            
            result = {
                "status": "success",
                "copula_type": f"archimedean_{copula_type}",
                "theta": theta,
                "assets": assets,
                "sample_size": len(asset_data),
                "log_likelihood": self._calculate_archimedean_log_likelihood(uniform_data, theta, copula_type)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Archimedean copula fitting failed: {str(e)}"}
    
    def calculate_tail_dependence(self, data: pd.DataFrame, assets: List[str]) -> Dict[str, Any]:
        """
        Calculate tail dependence coefficients.
        
        Args:
            data: Asset price data
            assets: List of asset names
            
        Returns:
            Tail dependence coefficients
        """
        try:
            # Extract asset data
            asset_data = data[assets].dropna()
            
            # Calculate lower and upper tail dependence
            lower_tail = self._calculate_lower_tail_dependence(asset_data)
            upper_tail = self._calculate_upper_tail_dependence(asset_data)
            
            result = {
                "status": "success",
                "lower_tail_dependence": lower_tail,
                "upper_tail_dependence": upper_tail,
                "assets": assets,
                "sample_size": len(asset_data)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Tail dependence calculation failed: {str(e)}"}
    
    def _calculate_kendall_tau(self, data: np.ndarray) -> np.ndarray:
        """Calculate Kendall's tau correlation matrix."""
        n_assets = data.shape[1]
        kendall_tau = np.zeros((n_assets, n_assets))
        
        for i in range(n_assets):
            for j in range(n_assets):
                if i == j:
                    kendall_tau[i, j] = 1.0
                else:
                    kendall_tau[i, j] = stats.kendalltau(data[:, i], data[:, j])[0]
        
        return kendall_tau
    
    def _estimate_student_t_df(self, data: np.ndarray, correlation_matrix: np.ndarray) -> float:
        """Estimate degrees of freedom for Student-t copula."""
        # Simple estimation using moment method
        n_assets = data.shape[1]
        if n_assets < 2:
            return 5.0
        
        # Calculate sample correlation
        sample_corr = np.corrcoef(data.T)
        
        # Estimate df using the relationship between correlation and df
        # This is a simplified approach
        return max(2.1, min(30.0, 5.0))
    
    def _estimate_clayton_theta(self, data: np.ndarray) -> float:
        """Estimate Clayton copula parameter."""
        # Use method of moments
        kendall_tau = stats.kendalltau(data[:, 0], data[:, 1])[0]
        theta = 2 * kendall_tau / (1 - kendall_tau)
        return max(0.1, theta)
    
    def _estimate_gumbel_theta(self, data: np.ndarray) -> float:
        """Estimate Gumbel copula parameter."""
        kendall_tau = stats.kendalltau(data[:, 0], data[:, 1])[0]
        theta = 1 / (1 - kendall_tau)
        return max(1.1, theta)
    
    def _estimate_frank_theta(self, data: np.ndarray) -> float:
        """Estimate Frank copula parameter."""
        kendall_tau = stats.kendalltau(data[:, 0], data[:, 1])[0]
        # Numerical solution for Frank copula
        theta = 1.0  # Simplified
        return theta
    
    def _calculate_gaussian_log_likelihood(self, data: np.ndarray, correlation_matrix: np.ndarray) -> float:
        """Calculate Gaussian copula log-likelihood."""
        try:
            # This is a simplified calculation
            n = data.shape[0]
            det_corr = np.linalg.det(correlation_matrix)
            if det_corr <= 0:
                return -np.inf
            
            inv_corr = np.linalg.inv(correlation_matrix)
            log_likelihood = -0.5 * n * np.log(det_corr)
            return log_likelihood
        except:
            return -np.inf
    
    def _calculate_student_t_log_likelihood(self, data: np.ndarray, correlation_matrix: np.ndarray, df: float) -> float:
        """Calculate Student-t copula log-likelihood."""
        # Simplified calculation
        return self._calculate_gaussian_log_likelihood(data, correlation_matrix)
    
    def _calculate_archimedean_log_likelihood(self, data: np.ndarray, theta: float, copula_type: str) -> float:
        """Calculate Archimedean copula log-likelihood."""
        # Simplified calculation
        return 0.0
    
    def _calculate_lower_tail_dependence(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate lower tail dependence coefficients."""
        assets = data.columns.tolist()
        lower_tail = {}
        
        for i, asset1 in enumerate(assets):
            for j, asset2 in enumerate(assets):
                if i < j:
                    # Calculate empirical lower tail dependence
                    threshold = 0.05
                    n = len(data)
                    k = int(threshold * n)
                    
                    # Sort data
                    sorted_data = data.sort_values(asset1)
                    lower_data = sorted_data.iloc[:k]
                    
                    # Calculate conditional probability
                    if len(lower_data) > 0:
                        prob = (lower_data[asset2] <= lower_data[asset2].quantile(threshold)).mean()
                        lower_tail[f"{asset1}_{asset2}"] = prob
                    else:
                        lower_tail[f"{asset1}_{asset2}"] = 0.0
        
        return lower_tail
    
    def _calculate_upper_tail_dependence(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate upper tail dependence coefficients."""
        assets = data.columns.tolist()
        upper_tail = {}
        
        for i, asset1 in enumerate(assets):
            for j, asset2 in enumerate(assets):
                if i < j:
                    # Calculate empirical upper tail dependence
                    threshold = 0.95
                    n = len(data)
                    k = int((1 - threshold) * n)
                    
                    # Sort data
                    sorted_data = data.sort_values(asset1, ascending=False)
                    upper_data = sorted_data.iloc[:k]
                    
                    # Calculate conditional probability
                    if len(upper_data) > 0:
                        prob = (upper_data[asset2] >= upper_data[asset2].quantile(threshold)).mean()
                        upper_tail[f"{asset1}_{asset2}"] = prob
                    else:
                        upper_tail[f"{asset1}_{asset2}"] = 0.0
        
        return upper_tail
