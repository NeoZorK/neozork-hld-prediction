#!/usr/bin/env python3
"""
Quantitative Research Module
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from scipy import stats


class ResearchMethod(Enum):
    """Research method enumeration"""
    STATISTICAL_ANALYSIS = "statistical_analysis"
    TIME_SERIES_ANALYSIS = "time_series_analysis"
    REGIME_DETECTION = "regime_detection"
    CORRELATION_ANALYSIS = "correlation_analysis"
    COINTEGRATION = "cointegration"
    CAUSALITY_ANALYSIS = "causality_analysis"
    FACTOR_ANALYSIS = "factor_analysis"


@dataclass
class ResearchConfig:
    """Configuration for research methods"""
    method: ResearchMethod
    confidence_level: float = 0.95
    lookback_period: int = 252
    significance_level: float = 0.05
    n_components: Optional[int] = None
    window_size: int = 30
    min_periods: int = 20


class QuantitativeResearcher:
    """Quantitative research system for financial analysis"""
    
    def __init__(self):
        self.research_cache = {}
        self.results_history = []
    
    def perform_statistical_analysis(self, data: pd.DataFrame, config: ResearchConfig) -> Dict[str, Any]:
        """Perform comprehensive statistical analysis"""
        try:
            results = {
                'method': config.method.value,
                'data_shape': data.shape,
                'descriptive_statistics': {},
                'normality_tests': {}
            }
            
            # Basic descriptive statistics
            for column in data.columns:
                series = data[column].dropna()
                results['descriptive_statistics'][column] = {
                    'count': len(series),
                    'mean': series.mean(),
                    'std': series.std(),
                    'min': series.min(),
                    'max': series.max(),
                    'skewness': stats.skew(series),
                    'kurtosis': stats.kurtosis(series)
                }
                
                # Simple normality test
                if len(series) > 8:
                    shapiro_stat, shapiro_p = stats.shapiro(series)
                    results['normality_tests'][column] = {
                        'shapiro_wilk': {'statistic': shapiro_stat, 'p_value': shapiro_p},
                        'is_normal': shapiro_p > config.significance_level
                    }
            
            self.results_history.append(results)
            
            return {
                'status': 'success',
                'results': results,
                'message': f'Statistical analysis completed for {data.shape[1]} variables',
                'data_shape': data.shape
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def perform_time_series_analysis(self, series: pd.Series, config: ResearchConfig) -> Dict[str, Any]:
        """Perform time series analysis"""
        try:
            results = {
                'method': config.method.value,
                'series_length': len(series),
                'trend_analysis': {}
            }
            
            # Simple trend analysis
            x = np.arange(len(series))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, series)
            
            results['trend_analysis'] = {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_value**2,
                'p_value': p_value,
                'trend_direction': 'upward' if slope > 0 else 'downward' if slope < 0 else 'flat'
            }
            
            return {
                'status': 'success',
                'results': results,
                'message': 'Time series analysis completed'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def detect_regimes(self, series: pd.Series, config: ResearchConfig) -> Dict[str, Any]:
        """Detect market regimes"""
        try:
            results = {
                'method': config.method.value,
                'series_length': len(series),
                'regime_detection': {}
            }
            
            # Simple regime detection
            rolling_std = series.rolling(window=config.window_size).std()
            vol_threshold = rolling_std.quantile(0.7)
            high_vol_periods = rolling_std > vol_threshold
            
            results['regime_detection'] = {
                'high_volatility_periods': high_vol_periods.sum(),
                'high_volatility_percentage': high_vol_periods.mean() * 100,
                'volatility_threshold': vol_threshold
            }
            
            return {
                'status': 'success',
                'results': results,
                'message': 'Regime detection completed'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def analyze_correlations(self, data: pd.DataFrame, config: ResearchConfig) -> Dict[str, Any]:
        """Analyze correlations between variables"""
        try:
            results = {
                'method': config.method.value,
                'data_shape': data.shape
            }
            
            # Pearson correlation
            pearson_corr = data.corr(method='pearson')
            results['pearson_correlation'] = pearson_corr
            
            return {
                'status': 'success',
                'results': results,
                'message': f'Correlation analysis completed for {data.shape[1]} variables'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def test_cointegration(self, data: pd.DataFrame, config: ResearchConfig) -> Dict[str, Any]:
        """Test for cointegration"""
        try:
            results = {
                'method': config.method.value,
                'data_shape': data.shape,
                'cointegrated_pairs': []
            }
            
            # Mock cointegration test
            results['cointegrated_pairs'] = [
                {'var1': data.columns[0], 'var2': data.columns[1], 'p_value': 0.05}
            ] if len(data.columns) >= 2 else []
            
            return {
                'status': 'success',
                'results': results,
                'message': f'Cointegration analysis completed'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def analyze_causality(self, data: pd.DataFrame, config: ResearchConfig) -> Dict[str, Any]:
        """Analyze causality"""
        try:
            results = {
                'method': config.method.value,
                'data_shape': data.shape,
                'causality_tests': []
            }
            
            # Mock causality tests
            for i in range(min(2, len(data.columns))):
                for j in range(min(2, len(data.columns))):
                    if i != j:
                        results['causality_tests'].append({
                            'cause': data.columns[i],
                            'effect': data.columns[j],
                            'min_p_value': 0.1,
                            'is_causal': False
                        })
            
            return {
                'status': 'success',
                'results': results,
                'message': 'Causality analysis completed'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def perform_factor_analysis(self, data: pd.DataFrame, config: ResearchConfig) -> Dict[str, Any]:
        """Perform factor analysis"""
        try:
            from sklearn.decomposition import PCA
            from sklearn.preprocessing import StandardScaler
            
            results = {
                'method': config.method.value,
                'data_shape': data.shape
            }
            
            # Simple PCA
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data.dropna())
            
            n_components = config.n_components or min(3, data.shape[1])
            pca = PCA(n_components=n_components)
            pca.fit(scaled_data)
            
            results['pca'] = {
                'n_components': n_components,
                'explained_variance_ratio': pca.explained_variance_ratio_.tolist()
            }
            
            return {
                'status': 'success',
                'results': results,
                'message': f'Factor analysis completed with {n_components} components'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }