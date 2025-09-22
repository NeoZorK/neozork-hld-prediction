"""
Time Series Data Transformation Module

This module provides comprehensive data transformation capabilities for time series data,
including differencing, detrending, and other time series specific transformations.

Features:
- Differencing: First-order and higher-order differencing
- Detrending: Linear and polynomial detrending
- Seasonal adjustment: Seasonal decomposition and adjustment
- Log transformations: Log and log-return transformations
- Box-Cox transformations: Optimal power transformations
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
from scipy import stats
from scipy.special import boxcox1p
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.signal import detrend
import warnings
import time
warnings.filterwarnings('ignore')


class TimeSeriesDataTransformation:
    """Handles data transformation for time series analysis."""
    
    def __init__(self):
        """Initialize the time series data transformation handler."""
        self.supported_transformations = [
            'differencing', 'detrending', 'seasonal_adjustment',
            'log_transform', 'log_returns', 'box_cox', 'yeo_johnson',
            'normalization', 'standardization'
        ]
    
    def transform_data(self, data: pd.DataFrame, transformations: Dict[str, List[str]], 
                      numeric_columns: List[str]) -> Dict[str, Any]:
        """
        Apply transformations to time series data.
        
        Args:
            data: DataFrame with time series data
            transformations: Dictionary mapping column names to transformation lists
            numeric_columns: List of numeric column names to transform
            
        Returns:
            Dictionary containing transformation results
        """
        results = {
            'transformed_data': data.copy(),
            'transformation_details': {},
            'comparison': {},
            'recommendations': {}
        }
        
        for col in numeric_columns:
            if col not in data.columns:
                continue
                
            col_data = data[col].dropna()
            if len(col_data) < 10:  # Need minimum data points
                continue
            
            # Create progress tracker for this column
            from .progress_tracker import ColumnProgressTracker
            progress_tracker = ColumnProgressTracker(col, "data transformation", 2)
            progress_tracker.start_analysis()
            
            # Get transformations for this column
            col_transformations = transformations.get(col, [])
            if not col_transformations:
                progress_tracker.complete_analysis()
                continue
            
            # Apply transformations
            progress_tracker.update_step("Apply Transformations")
            col_results = {}
            for transform_type in col_transformations:
                try:
                    transformed_data, details = self._apply_transformation(
                        col_data, transform_type, col
                    )
                    col_results[transform_type] = {
                        'transformed_data': transformed_data,
                        'details': details,
                        'success': True
                    }
                except Exception as e:
                    col_results[transform_type] = {
                        'transformed_data': None,
                        'details': {'error': f"Transformation failed: {str(e)}"},
                        'success': False
                    }
            
            # Select best transformation
            best_transformation = self._select_best_transformation(col_data, col_results)
            
            # Store all transformation details (including failed ones)
            results['transformation_details'][col] = {}
            for transform_type, result in col_results.items():
                results['transformation_details'][col][transform_type] = {
                    'success': result['success'],
                    'error': result['details'].get('error', 'Unknown error') if not result['success'] else None,
                    'improvement_score': result['details'].get('improvement_score', 0) if result['success'] else 0
                }
            
            if best_transformation and best_transformation in col_results:
                best_result = col_results[best_transformation]
                if best_result['success']:
                    # Update the transformed data
                    results['transformed_data'].loc[col_data.index, col] = best_result['transformed_data']
                    
                    # Create comparison
                    results['comparison'][col] = self._create_transformation_comparison(
                        col_data, best_result['transformed_data'], best_transformation
                    )
            
            # Generate recommendations
            progress_tracker.update_step("Generate Recommendations")
            results['recommendations'][col] = self._generate_transformation_recommendations(
                col_data, col_results, best_transformation
            )
            time.sleep(0.1)  # Simulate processing time
            
            # Complete analysis
            progress_tracker.complete_analysis()
        
        return results
    
    def _apply_transformation(self, data: pd.Series, transform_type: str, 
                            column_name: str) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Apply a specific transformation to the data.
        
        Args:
            data: Time series data to transform
            transform_type: Type of transformation to apply
            column_name: Name of the column being transformed
            
        Returns:
            Tuple of (transformed_data, transformation_details)
        """
        details = {
            'transformation_type': transform_type,
            'original_length': len(data),
            'original_mean': data.mean(),
            'original_std': data.std(),
            'original_skewness': data.skew(),
            'original_kurtosis': data.kurtosis()
        }
        
        if transform_type == 'differencing':
            transformed_data, diff_details = self._apply_differencing(data)
            details.update(diff_details)
            
        elif transform_type == 'detrending':
            transformed_data, detrend_details = self._apply_detrending(data)
            details.update(detrend_details)
            
        elif transform_type == 'seasonal_adjustment':
            transformed_data, seasonal_details = self._apply_seasonal_adjustment(data)
            details.update(seasonal_details)
            
        elif transform_type == 'log_transform':
            transformed_data, log_details = self._apply_log_transform(data)
            details.update(log_details)
            
        elif transform_type == 'log_returns':
            transformed_data, log_ret_details = self._apply_log_returns(data)
            details.update(log_ret_details)
            
        elif transform_type == 'box_cox':
            transformed_data, boxcox_details = self._apply_box_cox(data)
            details.update(boxcox_details)
            
        elif transform_type == 'yeo_johnson':
            transformed_data, yj_details = self._apply_yeo_johnson(data)
            details.update(yj_details)
            
        elif transform_type == 'seasonal_differencing':
            transformed_data, seasonal_diff_details = self._apply_seasonal_differencing(data)
            details.update(seasonal_diff_details)
            
        elif transform_type == 'power_transform':
            transformed_data, power_details = self._apply_power_transform(data)
            details.update(power_details)
            
        elif transform_type == 'normalization':
            transformed_data, norm_details = self._apply_normalization(data)
            details.update(norm_details)
            
        elif transform_type == 'standardization':
            transformed_data, std_details = self._apply_standardization(data)
            details.update(std_details)
            
        else:
            raise ValueError(f"Unsupported transformation type: {transform_type}")
        
        # Calculate transformed statistics
        if transformed_data is not None and len(transformed_data) > 0:
            details.update({
                'transformed_length': len(transformed_data),
                'transformed_mean': transformed_data.mean(),
                'transformed_std': transformed_data.std(),
                'transformed_skewness': transformed_data.skew(),
                'transformed_kurtosis': transformed_data.kurtosis(),
                'improvement_score': self._calculate_improvement_score(data, transformed_data)
            })
        
        return transformed_data, details
    
    def _apply_differencing(self, data: pd.Series) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply differencing transformation."""
        try:
            # First-order differencing
            diff1 = data.diff().dropna()
            
            # Second-order differencing if first-order still has trend
            if len(diff1) > 10:
                diff1_trend = self._has_trend(diff1)
                if diff1_trend:
                    diff2 = diff1.diff().dropna()
                    if len(diff2) > 5:
                        # Check if third-order is needed
                        diff2_trend = self._has_trend(diff2)
                        if diff2_trend and len(diff2) > 10:
                            diff3 = diff2.diff().dropna()
                            if len(diff3) > 3:
                                return diff3, {
                                    'differencing_order': 3,
                                    'first_diff_trend': diff1_trend,
                                    'second_diff_trend': diff2_trend,
                                    'third_diff_trend': self._has_trend(diff3)
                                }
                        return diff2, {
                            'differencing_order': 2,
                            'first_diff_trend': diff1_trend,
                            'second_diff_trend': diff2_trend
                        }
            
            return diff1, {
                'differencing_order': 1,
                'first_diff_trend': self._has_trend(diff1)
            }
        except Exception as e:
            return None, {'error': f"Transformation failed: {str(e)}"}
    
    def _apply_detrending(self, data: pd.Series) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply detrending transformation."""
        try:
            # Linear detrending using scipy.signal.detrend
            detrended_linear = detrend(data.values, type='linear')
            
            # Check if polynomial detrending is needed
            if len(data) > 20:
                detrended_poly = detrend(data.values, type='constant')
                
                # Compare linear vs constant detrending
                linear_std = np.std(detrended_linear)
                poly_std = np.std(detrended_poly)
                
                if poly_std < linear_std * 0.9:  # 10% improvement
                    return pd.Series(detrended_poly, index=data.index), {
                        'detrending_type': 'constant',
                        'polynomial_order': 0,
                        'improvement_over_linear': (linear_std - poly_std) / linear_std
                    }
            
            return pd.Series(detrended_linear, index=data.index), {
                'detrending_type': 'linear',
                'polynomial_order': 1
            }
        except Exception as e:
            return None, {'error': f"Transformation failed: {str(e)}"}
    
    def _apply_seasonal_adjustment(self, data: pd.Series) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply seasonal adjustment transformation."""
        try:
            if len(data) < 24:  # Need minimum data for seasonal decomposition
                return None, {'error': 'Insufficient data for seasonal adjustment'}
            
            # Determine seasonal period
            period = min(12, len(data) // 2)  # Default to 12 or half the data length
            
            # Seasonal decomposition
            decomposition = seasonal_decompose(data, model='additive', period=period)
            
            # Seasonally adjusted data
            seasonal_adjusted = data - decomposition.seasonal
            
            return seasonal_adjusted, {
                'seasonal_period': period,
                'seasonal_strength': np.std(decomposition.seasonal) / np.std(data),
                'trend_strength': np.std(decomposition.trend) / np.std(data),
                'residual_strength': np.std(decomposition.resid) / np.std(data)
            }
        except Exception as e:
            return None, {'error': f"Transformation failed: {str(e)}"}
    
    def _apply_log_transform(self, data: pd.Series) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply log transformation."""
        try:
            if (data <= 0).any():
                # Shift data to make it positive
                min_val = data.min()
                shift = abs(min_val) + 1
                shifted_data = data + shift
                log_transformed = np.log(shifted_data)
                return log_transformed, {
                    'shift_applied': shift,
                    'original_min': min_val,
                    'transformation': 'log_with_shift'
                }
            else:
                log_transformed = np.log(data)
                return log_transformed, {
                    'shift_applied': 0,
                    'transformation': 'log'
                }
        except Exception as e:
            return None, {'error': f"Transformation failed: {str(e)}"}
    
    def _apply_log_returns(self, data: pd.Series) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply log returns transformation."""
        try:
            if len(data) < 2:
                return None, {'error': 'Insufficient data for log returns'}
            
            log_returns = np.log(data / data.shift(1)).dropna()
            return log_returns, {
                'transformation': 'log_returns',
                'return_count': len(log_returns)
            }
        except Exception as e:
            return None, {'error': f"Transformation failed: {str(e)}"}
    
    def _apply_box_cox(self, data: pd.Series) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply Box-Cox transformation."""
        try:
            if (data <= 0).any():
                return None, {'error': 'Box-Cox requires positive values'}
            
            # Find optimal lambda
            boxcox_data, lambda_val = stats.boxcox(data)
            
            return pd.Series(boxcox_data, index=data.index), {
                'lambda': lambda_val,
                'transformation': 'box_cox'
            }
        except Exception as e:
            return None, {'error': f"Transformation failed: {str(e)}"}
    
    def _apply_yeo_johnson(self, data: pd.Series) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply Yeo-Johnson transformation."""
        try:
            # Find optimal lambda
            yj_data, lambda_val = stats.yeojohnson(data)
            
            return pd.Series(yj_data, index=data.index), {
                'lambda': lambda_val,
                'transformation': 'yeo_johnson'
            }
        except Exception as e:
            return None, {'error': f"Transformation failed: {str(e)}"}
    
    def _apply_normalization(self, data: pd.Series) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply min-max normalization."""
        try:
            min_val = data.min()
            max_val = data.max()
            
            if max_val == min_val:
                return pd.Series(np.zeros_like(data), index=data.index), {
                    'transformation': 'normalization',
                    'min_val': min_val,
                    'max_val': max_val,
                    'warning': 'Constant data - normalization results in zeros'
                }
            
            normalized = (data - min_val) / (max_val - min_val)
            return normalized, {
                'transformation': 'normalization',
                'min_val': min_val,
                'max_val': max_val
            }
        except Exception as e:
            return None, {'error': f"Transformation failed: {str(e)}"}
    
    def _apply_standardization(self, data: pd.Series) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply z-score standardization."""
        try:
            mean_val = data.mean()
            std_val = data.std()
            
            if std_val == 0:
                return pd.Series(np.zeros_like(data), index=data.index), {
                    'transformation': 'standardization',
                    'mean_val': mean_val,
                    'std_val': std_val,
                    'warning': 'Constant data - standardization results in zeros'
                }
            
            standardized = (data - mean_val) / std_val
            return standardized, {
                'transformation': 'standardization',
                'mean_val': mean_val,
                'std_val': std_val
            }
        except Exception as e:
            return None, {'error': f"Transformation failed: {str(e)}"}
    
    def _has_trend(self, data: pd.Series) -> bool:
        """Check if data has a significant trend."""
        try:
            if len(data) < 5:
                return False
            
            x = np.arange(len(data))
            slope, _, r_value, p_value, _ = stats.linregress(x, data)
            return p_value < 0.05 and abs(r_value) > 0.3
        except:
            return False
    
    def _calculate_improvement_score(self, original: pd.Series, transformed: pd.Series) -> float:
        """Calculate improvement score for transformation."""
        try:
            # Calculate original and transformed statistics
            orig_skew = abs(original.skew())
            orig_kurt = abs(original.kurtosis())
            trans_skew = abs(transformed.skew())
            trans_kurt = abs(transformed.kurtosis())
            
            # Calculate variance reduction (good for stationarity)
            orig_var = original.var()
            trans_var = transformed.var()
            var_reduction = 0
            if orig_var > 0:
                var_reduction = max(0, (orig_var - trans_var) / orig_var)
            
            # Calculate range reduction (good for normalization)
            orig_range = original.max() - original.min()
            trans_range = transformed.max() - transformed.min()
            range_reduction = 0
            if orig_range > 0:
                range_reduction = max(0, (orig_range - trans_range) / orig_range)
            
            # Calculate improvements based on skewness and kurtosis
            skew_improvement = 0
            kurt_improvement = 0
            
            # Balanced sensitivity to improvements
            if orig_skew > 0.1:  # Original threshold for significance
                skew_improvement = max(0, (orig_skew - trans_skew) / orig_skew)
            
            if orig_kurt > 0.1:  # Original threshold for significance
                kurt_improvement = max(0, (orig_kurt - trans_kurt) / orig_kurt)
            
            # Calculate stationarity improvement (ADF test simulation)
            stationarity_improvement = 0
            if len(transformed) > 10:
                # Simple stationarity check based on variance stability
                orig_rolling_var = original.rolling(window=min(10, len(original)//3)).var().dropna()
                trans_rolling_var = transformed.rolling(window=min(10, len(transformed)//3)).var().dropna()
                
                if len(orig_rolling_var) > 0 and len(trans_rolling_var) > 0:
                    orig_var_stability = 1 - (orig_rolling_var.std() / orig_rolling_var.mean()) if orig_rolling_var.mean() > 0 else 0
                    trans_var_stability = 1 - (trans_rolling_var.std() / trans_rolling_var.mean()) if trans_rolling_var.mean() > 0 else 0
                    stationarity_improvement = max(0, trans_var_stability - orig_var_stability)
            
            # Calculate normality improvement
            normality_improvement = 0
            if len(transformed) > 10:
                # Simple normality check based on skewness and kurtosis
                orig_normality = 1 - (orig_skew + orig_kurt) / 2
                trans_normality = 1 - (trans_skew + trans_kurt) / 2
                normality_improvement = max(0, trans_normality - orig_normality)
            
            # Penalize if things get worse
            skew_penalty = max(0, (trans_skew - orig_skew) * 1.5) if trans_skew > orig_skew else 0
            kurt_penalty = max(0, (trans_kurt - orig_kurt) * 1.5) if trans_kurt > orig_kurt else 0
            
            # Calculate final score with focused metrics
            score = (
                skew_improvement * 0.3 +
                kurt_improvement * 0.3 +
                var_reduction * 0.4
            ) - (skew_penalty + kurt_penalty) * 0.2
            
            return max(0, min(score, 1))  # Clamp between 0 and 1
        except:
            return 0
    
    def _apply_seasonal_differencing(self, data: pd.Series) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply seasonal differencing transformation."""
        try:
            if len(data) < 24:  # Need at least 24 points for seasonal differencing
                return None, {'error': 'Insufficient data for seasonal differencing'}
            
            # Try different seasonal periods
            periods = [12, 6, 4, 3]  # Monthly, bi-monthly, quarterly, etc.
            best_period = None
            best_score = float('inf')
            
            for period in periods:
                if len(data) > period:
                    seasonal_diff = data.diff(period).dropna()
                    if len(seasonal_diff) > 5:
                        # Score based on variance reduction
                        score = seasonal_diff.var() / data.var() if data.var() > 0 else float('inf')
                        if score < best_score:
                            best_score = score
                            best_period = period
            
            if best_period is None:
                return None, {'error': 'No suitable seasonal period found'}
            
            seasonal_diff = data.diff(best_period).dropna()
            return seasonal_diff, {
                'seasonal_period': best_period,
                'variance_reduction': 1 - best_score if best_score < 1 else 0
            }
        except Exception as e:
            return None, {'error': f"Transformation failed: {str(e)}"}
    
    def _apply_power_transform(self, data: pd.Series) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply power transformation (Yeo-Johnson style)."""
        try:
            # Avoid zero and negative values
            if (data <= 0).any():
                data_shifted = data - data.min() + 1e-8
            else:
                data_shifted = data
            
            # Try different power values
            powers = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
            best_power = 1.0
            best_score = float('inf')
            
            for power in powers:
                if power == 1.0:
                    transformed = data_shifted
                else:
                    transformed = np.power(data_shifted, power)
                
                # Score based on normality (lower is better)
                if len(transformed) > 10:
                    score = abs(transformed.skew()) + abs(transformed.kurtosis())
                    if score < best_score:
                        best_score = score
                        best_power = power
            
            if best_power == 1.0:
                transformed = data_shifted
            else:
                transformed = np.power(data_shifted, best_power)
            
            return pd.Series(transformed, index=data.index), {
                'power': best_power,
                'normality_score': best_score
            }
        except Exception as e:
            return None, {'error': f"Transformation failed: {str(e)}"}
    
    def _select_best_transformation(self, original_data: pd.Series, 
                                  transformation_results: Dict[str, Any]) -> Optional[str]:
        """Select the best transformation based on improvement scores and additional criteria."""
        best_transformation = None
        best_score = -1
        
        # Weight different types of transformations based on their typical effectiveness
        transform_weights = {
            'differencing': 1.2,  # Often very effective for non-stationary data
            'seasonal_differencing': 1.3,  # Very effective for seasonal data
            'log_transform': 1.1,  # Good for exponential growth
            'power_transform': 1.15,  # Good for various distributions
            'detrending': 1.0,  # Standard effectiveness
            'box_cox': 1.05,  # Slightly better than basic transforms
            'yeo_johnson': 1.1,  # Good for various distributions
            'normalization': 0.8,  # Basic but useful
            'standardization': 0.8,  # Basic but useful
            'seasonal_adjustment': 1.1,  # Good for seasonal data
            'log_returns': 1.0  # Standard for financial data
        }
        
        for transform_type, result in transformation_results.items():
            if result['success'] and 'improvement_score' in result['details']:
                base_score = result['details']['improvement_score']
                weight = transform_weights.get(transform_type, 1.0)
                weighted_score = base_score * weight
                
                # Bonus for transformations that significantly improve stationarity
                if 'stationarity_improvement' in result['details']:
                    weighted_score += result['details']['stationarity_improvement'] * 0.3
                
                # Bonus for transformations that reduce variance significantly
                if 'variance_reduction' in result['details']:
                    weighted_score += result['details']['variance_reduction'] * 0.2
                
                if weighted_score > best_score:
                    best_score = weighted_score
                    best_transformation = transform_type
        
        return best_transformation
    
    def _create_transformation_comparison(self, original: pd.Series, transformed: pd.Series, 
                                        transform_type: str) -> Dict[str, Any]:
        """Create comparison between original and transformed data."""
        try:
            return {
                'transformation_type': transform_type,
                'original_stats': {
                    'mean': original.mean(),
                    'std': original.std(),
                    'skewness': original.skew(),
                    'kurtosis': original.kurtosis(),
                    'min': original.min(),
                    'max': original.max()
                },
                'transformed_stats': {
                    'mean': transformed.mean(),
                    'std': transformed.std(),
                    'skewness': transformed.skew(),
                    'kurtosis': transformed.kurtosis(),
                    'min': transformed.min(),
                    'max': transformed.max()
                },
                'improvements': {
                    'skewness_change': original.skew() - transformed.skew(),
                    'kurtosis_change': original.kurtosis() - transformed.kurtosis(),
                    'variance_change': (transformed.var() - original.var()) / original.var() if original.var() != 0 else 0
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_transformation_recommendations(self, original_data: pd.Series, 
                                               transformation_results: Dict[str, Any], 
                                               best_transformation: Optional[str]) -> Dict[str, Any]:
        """Generate transformation recommendations."""
        recommendations = {
            'best_transformation': best_transformation,
            'recommended_actions': [],
            'warnings': [],
            'next_steps': []
        }
        
        if best_transformation and best_transformation in transformation_results:
            best_result = transformation_results[best_transformation]
            if best_result['success']:
                details = best_result['details']
                improvement_score = details.get('improvement_score', 0)
                
                if improvement_score > 0.5:
                    recommendations['recommended_actions'].append(
                        f"Excellent transformation with {best_transformation} - significant improvement"
                    )
                elif improvement_score > 0.2:
                    recommendations['recommended_actions'].append(
                        f"Good transformation with {best_transformation} - moderate improvement"
                    )
                else:
                    recommendations['recommended_actions'].append(
                        f"Minimal improvement with {best_transformation} - consider other approaches"
                    )
                
                # Add specific recommendations based on transformation type
                if best_transformation == 'differencing':
                    recommendations['next_steps'].append(
                        "Consider checking for remaining trends after differencing"
                    )
                elif best_transformation == 'log_transform':
                    recommendations['next_steps'].append(
                        "Verify that log transformation improved normality"
                    )
                elif best_transformation == 'box_cox':
                    recommendations['next_steps'].append(
                        f"Box-Cox lambda value: {details.get('lambda', 'N/A')} - use this for future transformations"
                    )
        
        # Check for failed transformations
        failed_transformations = [t for t, r in transformation_results.items() 
                                if not r['success']]
        if failed_transformations:
            recommendations['warnings'].append(
                f"Failed transformations: {', '.join(failed_transformations)}"
            )
        
        return recommendations
