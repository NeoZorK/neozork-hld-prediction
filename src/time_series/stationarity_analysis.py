"""
Stationarity Analysis Module

This module provides comprehensive stationarity analysis for time series data,
including Augmented Dickey-Fuller (ADF) tests, critical values analysis,
and stationarity recommendations.

Features:
- ADF Test: Augmented Dickey-Fuller test for stationarity
- Critical Values: Critical values at different significance levels (1%, 5%, 10%)
- Stationarity Recommendations: Recommendations for achieving stationarity through differencing
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import stats
import warnings
import time
warnings.filterwarnings('ignore')


class StationarityAnalysis:
    """Handles stationarity analysis for time series data."""
    
    def __init__(self):
        """Initialize the stationarity analysis handler."""
        self.significance_levels = [0.01, 0.05, 0.10]  # 1%, 5%, 10%
        self.critical_values = {
            0.01: {'1%': -3.43, '5%': -2.86, '10%': -2.57},
            0.05: {'1%': -3.43, '5%': -2.86, '10%': -2.57},
            0.10: {'1%': -3.43, '5%': -2.86, '10%': -2.57}
        }
    
    def analyze_stationarity(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
        """
        Perform comprehensive stationarity analysis on time series data.
        
        Args:
            data: DataFrame with time series data
            numeric_columns: List of numeric column names to analyze
            
        Returns:
            Dictionary containing stationarity analysis results
        """
        results = {
            'adf_tests': {},
            'critical_values': {},
            'stationarity_recommendations': {},
            'overall_assessment': {}
        }
        
        for col in numeric_columns:
            if col not in data.columns:
                continue
                
            col_data = data[col].dropna()
            if len(col_data) < 10:  # Need minimum data points
                continue
            
            # Create progress tracker for this column
            from .progress_tracker import ColumnProgressTracker
            progress_tracker = ColumnProgressTracker(col, "stationarity", 3)
            progress_tracker.start_analysis()
            
            # Perform ADF test
            progress_tracker.update_step("ADF Test")
            adf_results = self._perform_adf_test(col_data, col)
            results['adf_tests'][col] = adf_results
            time.sleep(0.1)  # Simulate processing time
            
            # Get critical values
            progress_tracker.update_step("Critical Values")
            critical_vals = self._get_critical_values(col_data, col)
            results['critical_values'][col] = critical_vals
            time.sleep(0.1)  # Simulate processing time
            
            # Generate recommendations
            progress_tracker.update_step("Recommendations")
            recommendations = self._generate_stationarity_recommendations(
                adf_results, critical_vals, col_data, col
            )
            results['stationarity_recommendations'][col] = recommendations
            time.sleep(0.1)  # Simulate processing time
            
            # Complete analysis
            progress_tracker.complete_analysis()
        
        # Overall assessment
        results['overall_assessment'] = self._generate_overall_assessment(results)
        
        return results
    
    def _perform_adf_test(self, data: pd.Series, column_name: str) -> Dict[str, Any]:
        """
        Perform Augmented Dickey-Fuller test.
        
        Args:
            data: Time series data
            column_name: Name of the column being analyzed
            
        Returns:
            Dictionary with ADF test results
        """
        try:
            # Perform ADF test with different specifications
            adf_results = {}
            
            # Standard ADF test
            adf_stat, p_value, used_lag, nobs, critical_values, icbest = adfuller(
                data, autolag='AIC'
            )
            
            adf_results['standard'] = {
                'adf_statistic': adf_stat,
                'p_value': p_value,
                'used_lag': used_lag,
                'nobs': nobs,
                'critical_values': {
                    '1%': critical_values['1%'],
                    '5%': critical_values['5%'],
                    '10%': critical_values['10%']
                },
                'icbest': icbest,
                'is_stationary': p_value < 0.05
            }
            
            # ADF test with trend
            adf_stat_trend, p_value_trend, used_lag_trend, nobs_trend, critical_values_trend, icbest_trend = adfuller(
                data, regression='ct', autolag='AIC'
            )
            
            adf_results['with_trend'] = {
                'adf_statistic': adf_stat_trend,
                'p_value': p_value_trend,
                'used_lag': used_lag_trend,
                'nobs': nobs_trend,
                'critical_values': {
                    '1%': critical_values_trend['1%'],
                    '5%': critical_values_trend['5%'],
                    '10%': critical_values_trend['10%']
                },
                'icbest': icbest_trend,
                'is_stationary': p_value_trend < 0.05
            }
            
            # ADF test with constant only
            adf_stat_const, p_value_const, used_lag_const, nobs_const, critical_values_const, icbest_const = adfuller(
                data, regression='c', autolag='AIC'
            )
            
            adf_results['with_constant'] = {
                'adf_statistic': adf_stat_const,
                'p_value': p_value_const,
                'used_lag': used_lag_const,
                'nobs': nobs_const,
                'critical_values': {
                    '1%': critical_values_const['1%'],
                    '5%': critical_values_const['5%'],
                    '10%': critical_values_const['10%']
                },
                'icbest': icbest_const,
                'is_stationary': p_value_const < 0.05
            }
            
            # Determine best specification
            best_spec = self._determine_best_adf_specification(adf_results)
            adf_results['best_specification'] = best_spec
            
            return adf_results
            
        except Exception as e:
            return {
                'error': str(e),
                'standard': None,
                'with_trend': None,
                'with_constant': None,
                'best_specification': None
            }
    
    def _determine_best_adf_specification(self, adf_results: Dict[str, Any]) -> str:
        """
        Determine the best ADF test specification based on results.
        
        Args:
            adf_results: Dictionary with ADF test results
            
        Returns:
            String indicating the best specification
        """
        if 'error' in adf_results:
            return 'error'
        
        # Compare p-values to determine best specification
        p_values = {}
        for spec in ['standard', 'with_trend', 'with_constant']:
            if adf_results[spec] and 'p_value' in adf_results[spec]:
                p_values[spec] = adf_results[spec]['p_value']
        
        if not p_values:
            return 'none'
        
        # Choose the specification with the lowest p-value (most significant)
        best_spec = min(p_values, key=p_values.get)
        return best_spec
    
    def _get_critical_values(self, data: pd.Series, column_name: str) -> Dict[str, Any]:
        """
        Get critical values for different significance levels.
        
        Args:
            data: Time series data
            column_name: Name of the column being analyzed
            
        Returns:
            Dictionary with critical values information
        """
        try:
            # Sample size dependent critical values
            n = len(data)
            
            # Approximate critical values based on sample size
            if n < 25:
                critical_vals = {
                    '1%': -3.75,
                    '5%': -3.00,
                    '10%': -2.63
                }
            elif n < 50:
                critical_vals = {
                    '1%': -3.58,
                    '5%': -2.93,
                    '10%': -2.60
                }
            elif n < 100:
                critical_vals = {
                    '1%': -3.51,
                    '5%': -2.89,
                    '10%': -2.58
                }
            else:
                critical_vals = {
                    '1%': -3.43,
                    '5%': -2.86,
                    '10%': -2.57
                }
            
            return {
                'sample_size': n,
                'critical_values': critical_vals,
                'interpretation': {
                    '1%': 'Very strong evidence against stationarity',
                    '5%': 'Strong evidence against stationarity',
                    '10%': 'Moderate evidence against stationarity'
                }
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'sample_size': len(data),
                'critical_values': None,
                'interpretation': None
            }
    
    def _generate_stationarity_recommendations(self, adf_results: Dict[str, Any], 
                                             critical_vals: Dict[str, Any], 
                                             data: pd.Series, column_name: str) -> Dict[str, Any]:
        """
        Generate stationarity recommendations based on test results.
        
        Args:
            adf_results: ADF test results
            critical_vals: Critical values information
            data: Time series data
            column_name: Name of the column being analyzed
            
        Returns:
            Dictionary with stationarity recommendations
        """
        recommendations = {
            'is_stationary': False,
            'confidence_level': 'unknown',
            'recommended_actions': [],
            'differencing_suggestions': [],
            'transformation_suggestions': []
        }
        
        if 'error' in adf_results:
            recommendations['error'] = adf_results['error']
            return recommendations
        
        # Check if any specification shows stationarity
        best_spec = adf_results.get('best_specification', 'standard')
        if best_spec in adf_results and adf_results[best_spec]:
            best_result = adf_results[best_spec]
            p_value = best_result['p_value']
            adf_stat = best_result['adf_statistic']
            
            # Determine stationarity
            if p_value < 0.01:
                recommendations['is_stationary'] = True
                recommendations['confidence_level'] = 'very_high'
                recommendations['recommended_actions'].append(
                    "Data is stationary at 1% significance level - excellent for time series modeling"
                )
            elif p_value < 0.05:
                recommendations['is_stationary'] = True
                recommendations['confidence_level'] = 'high'
                recommendations['recommended_actions'].append(
                    "Data is stationary at 5% significance level - good for time series modeling"
                )
            elif p_value < 0.10:
                recommendations['is_stationary'] = True
                recommendations['confidence_level'] = 'moderate'
                recommendations['recommended_actions'].append(
                    "Data is stationary at 10% significance level - acceptable for time series modeling"
                )
            else:
                recommendations['is_stationary'] = False
                recommendations['confidence_level'] = 'low'
                recommendations['recommended_actions'].append(
                    "Data is not stationary - transformation or differencing required"
                )
                
                # Suggest differencing
                recommendations['differencing_suggestions'].extend([
                    "Try first-order differencing: data.diff()",
                    "Try second-order differencing if first-order is insufficient: data.diff().diff()",
                    "Consider seasonal differencing for seasonal data"
                ])
                
                # Suggest transformations
                if (data > 0).all():
                    recommendations['transformation_suggestions'].extend([
                        "Log transformation: np.log(data)",
                        "Square root transformation: np.sqrt(data)",
                        "Box-Cox transformation for optimal results"
                    ])
                else:
                    recommendations['transformation_suggestions'].extend([
                        "Yeo-Johnson transformation (handles negative values)",
                        "Data shifting before log transformation",
                        "Consider removing outliers before transformation"
                    ])
        
        # Additional recommendations based on data characteristics
        if not recommendations['is_stationary']:
            # Check for trend
            if self._has_trend(data):
                recommendations['recommended_actions'].append(
                    "Strong trend detected - consider detrending or differencing"
                )
            
            # Check for seasonality
            if self._has_seasonality(data):
                recommendations['recommended_actions'].append(
                    "Seasonal patterns detected - consider seasonal differencing"
                )
            
            # Check for heteroscedasticity
            if self._has_heteroscedasticity(data):
                recommendations['recommended_actions'].append(
                    "Variance changes over time - consider variance stabilizing transformations"
                )
        
        return recommendations
    
    def _has_trend(self, data: pd.Series) -> bool:
        """Check if data has a significant trend."""
        try:
            # Simple linear trend test
            x = np.arange(len(data))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)
            return p_value < 0.05 and abs(r_value) > 0.3
        except:
            return False
    
    def _has_seasonality(self, data: pd.Series) -> bool:
        """Check if data has seasonal patterns."""
        try:
            if len(data) < 24:  # Need minimum data for seasonality detection
                return False
            
            # Try seasonal decomposition
            decomposition = seasonal_decompose(data, model='additive', period=min(12, len(data)//2))
            seasonal_std = decomposition.seasonal.std()
            residual_std = decomposition.resid.std()
            
            # If seasonal component has significant variation
            return seasonal_std > 0.1 * residual_std
        except:
            return False
    
    def _has_heteroscedasticity(self, data: pd.Series) -> bool:
        """Check if data has changing variance over time."""
        try:
            if len(data) < 20:
                return False
            
            # Split data into two halves and compare variances
            mid_point = len(data) // 2
            first_half = data[:mid_point]
            second_half = data[mid_point:]
            
            var1 = first_half.var()
            var2 = second_half.var()
            
            # If variance differs significantly
            return abs(var1 - var2) > 0.5 * (var1 + var2)
        except:
            return False
    
    def _generate_overall_assessment(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate overall assessment of stationarity across all columns.
        
        Args:
            results: Complete stationarity analysis results
            
        Returns:
            Dictionary with overall assessment
        """
        adf_tests = results.get('adf_tests', {})
        recommendations = results.get('stationarity_recommendations', {})
        
        total_columns = len(adf_tests)
        stationary_columns = 0
        non_stationary_columns = 0
        error_columns = 0
        
        for col, rec in recommendations.items():
            if 'error' in rec:
                error_columns += 1
            elif rec.get('is_stationary', False):
                stationary_columns += 1
            else:
                non_stationary_columns += 1
        
        stationarity_rate = stationary_columns / total_columns if total_columns > 0 else 0
        
        assessment = {
            'total_columns': total_columns,
            'stationary_columns': stationary_columns,
            'non_stationary_columns': non_stationary_columns,
            'error_columns': error_columns,
            'stationarity_rate': stationarity_rate,
            'overall_quality': 'excellent' if stationarity_rate > 0.8 else
                             'good' if stationarity_rate > 0.6 else
                             'fair' if stationarity_rate > 0.4 else 'poor',
            'recommendations': []
        }
        
        # Generate overall recommendations
        if assessment['stationarity_rate'] > 0.8:
            assessment['recommendations'].append(
                "Excellent: Most data is stationary and ready for time series modeling"
            )
        elif assessment['stationarity_rate'] > 0.6:
            assessment['recommendations'].append(
                "Good: Majority of data is stationary, some columns may need transformation"
            )
        elif assessment['stationarity_rate'] > 0.4:
            assessment['recommendations'].append(
                "Fair: About half of data is stationary, consider comprehensive transformation"
            )
        else:
            assessment['recommendations'].append(
                "Poor: Most data is non-stationary, extensive preprocessing required"
            )
        
        if error_columns > 0:
            assessment['recommendations'].append(
                f"Warning: {error_columns} columns had analysis errors - check data quality"
            )
        
        return assessment
