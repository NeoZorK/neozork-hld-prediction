"""
Enhanced Data Transformation Module

This module provides advanced data transformation capabilities specifically designed
to handle high skewness and kurtosis in financial data. It includes additional
transformation methods and improved algorithms for better distribution normalization.

Features:
- Advanced Box-Cox with multiple lambda optimization strategies
- Robust log transformations with better handling of extreme values
- Power transformations with automatic parameter selection
- Quantile-based transformations for outlier-resistant normalization
- Combined transformations for complex distributions
- Financial-specific transformations (log returns, percentage changes)
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
from scipy import stats
from scipy.stats import boxcox, yeojohnson
from scipy.optimize import minimize_scalar
from sklearn.preprocessing import PowerTransformer, QuantileTransformer, RobustScaler
import logging
import warnings
warnings.filterwarnings('ignore')


class EnhancedDataTransformation:
    """Enhanced data transformation with advanced methods for financial data."""
    
    def __init__(self):
        """Initialize the enhanced data transformer."""
        self.logger = logging.getLogger(__name__)
        self.transformation_cache = {}
        
    def transform_data_enhanced(self, data: pd.DataFrame, 
                               transformations: Dict[str, List[str]], 
                               numeric_columns: Optional[List[str]] = None,
                               target_skewness: float = 0.0,
                               target_kurtosis: float = 0.0) -> Dict[str, Any]:
        """
        Apply enhanced transformations with improved algorithms.
        
        Args:
            data: DataFrame to transform
            transformations: Dictionary mapping column names to list of transformations
            numeric_columns: List of numeric columns. If None, auto-detect.
            target_skewness: Target skewness value (default: 0.0 for normal)
            target_kurtosis: Target kurtosis value (default: 0.0 for normal)
            
        Returns:
            Dictionary containing transformed data and detailed transformation info
        """
        if numeric_columns is None:
            numeric_columns = self._get_numeric_columns(data)
        
        if not numeric_columns:
            self.logger.warning("No numeric columns found for transformation")
            return {'transformed_data': data, 'transformation_details': {}}
        
        transformed_data = data.copy()
        transformation_details = {}
        
        for col in numeric_columns:
            if col not in transformations:
                continue
                
            col_data = data[col].dropna()
            if len(col_data) == 0:
                continue
                
            col_details = {}
            
            for transformation in transformations[col]:
                try:
                    transformed_col, details = self._apply_enhanced_transformation(
                        col_data, transformation, col, target_skewness, target_kurtosis
                    )
                    
                    if transformed_col is not None:
                        new_col_name = f"{col}_{transformation}"
                        transformed_data[new_col_name] = transformed_col
                        col_details[transformation] = details
                        
                except Exception as e:
                    self.logger.error(f"Error applying {transformation} to {col}: {e}")
                    col_details[transformation] = {
                        'success': False,
                        'error': str(e),
                        'transformation': transformation
                    }
            
            transformation_details[col] = col_details
        
        return {
            'transformed_data': transformed_data,
            'transformation_details': transformation_details
        }
    
    def _apply_enhanced_transformation(self, data: np.ndarray, transformation: str, 
                                     column_name: str, target_skewness: float = 0.0,
                                     target_kurtosis: float = 0.0) -> Tuple[Optional[np.ndarray], Dict[str, Any]]:
        """Apply enhanced transformation with improved algorithms."""
        details = {
            'transformation': transformation,
            'column': column_name,
            'original_shape': data.shape,
            'success': True,
            'target_skewness': target_skewness,
            'target_kurtosis': target_kurtosis
        }
        
        try:
            if transformation == 'enhanced_log':
                return self._enhanced_log_transformation(data, details)
            elif transformation == 'robust_box_cox':
                return self._robust_box_cox_transformation(data, details, target_skewness)
            elif transformation == 'power_transform':
                return self._power_transform_transformation(data, details)
            elif transformation == 'quantile_transform':
                return self._quantile_transform_transformation(data, details)
            elif transformation == 'log_returns':
                return self._log_returns_transformation(data, details)
            elif transformation == 'robust_log':
                return self._robust_log_transformation(data, details)
            elif transformation == 'adaptive_box_cox':
                return self._adaptive_box_cox_transformation(data, details, target_skewness, target_kurtosis)
            elif transformation == 'winsorized_log':
                return self._winsorized_log_transformation(data, details)
            elif transformation == 'financial_normalize':
                return self._financial_normalize_transformation(data, details)
            else:
                # Fallback to standard transformations
                return self._apply_standard_transformation(data, transformation, details)
        
        except Exception as e:
            details['success'] = False
            details['error'] = str(e)
            return None, details
    
    def _enhanced_log_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Enhanced log transformation with better handling of extreme values."""
        # Handle non-positive values with adaptive shifting
        min_val = np.min(data)
        if min_val <= 0:
            # Use more sophisticated shifting strategy
            constant = self._calculate_optimal_shift(data)
            data_shifted = data + constant
            details['shift_constant'] = constant
            details['shift_method'] = 'optimal_adaptive'
        else:
            data_shifted = data
            details['shift_constant'] = 0
            details['shift_method'] = 'none'
        
        # Apply log transformation
        transformed = np.log(data_shifted)
        
        # Calculate comprehensive statistics
        self._calculate_transformation_stats(data, transformed, details)
        details['success'] = True
        
        return transformed, details
    
    def _robust_box_cox_transformation(self, data: np.ndarray, details: Dict[str, Any], 
                                     target_skewness: float) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Robust Box-Cox transformation with multiple optimization strategies."""
        # Handle non-positive values
        if np.any(data <= 0):
            constant = self._calculate_optimal_shift(data)
            data_shifted = data + constant
            details['shift_constant'] = constant
        else:
            data_shifted = data
            details['shift_constant'] = 0
        
        try:
            # Try multiple Box-Cox optimization strategies
            best_lambda = self._optimize_box_cox_lambda(data_shifted, target_skewness)
            
            if best_lambda == 0:
                transformed = np.log(data_shifted)
                details['lambda'] = 0
                details['method'] = 'log_approximation'
            else:
                transformed = (np.power(data_shifted, best_lambda) - 1) / best_lambda
                details['lambda'] = best_lambda
                details['method'] = 'optimized_box_cox'
            
            self._calculate_transformation_stats(data, transformed, details)
            details['success'] = True
            
        except Exception as e:
            details['error'] = f"Robust Box-Cox transformation failed: {str(e)}"
            details['success'] = False
            return None, details
        
        return transformed, details
    
    def _power_transform_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Power transformation using scikit-learn's PowerTransformer."""
        try:
            # Reshape data for PowerTransformer
            data_reshaped = data.reshape(-1, 1)
            
            # Apply PowerTransformer (Yeo-Johnson by default)
            transformer = PowerTransformer(method='yeo-johnson', standardize=False)
            transformed_reshaped = transformer.fit_transform(data_reshaped)
            transformed = transformed_reshaped.flatten()
            
            # Store transformer parameters
            details['lambdas'] = transformer.lambdas_.tolist()
            details['method'] = 'yeo_johnson_power_transform'
            
            self._calculate_transformation_stats(data, transformed, details)
            details['success'] = True
            
        except Exception as e:
            details['error'] = f"Power transform failed: {str(e)}"
            details['success'] = False
            return None, details
        
        return transformed, details
    
    def _quantile_transform_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Quantile transformation for robust normalization."""
        try:
            # Reshape data for QuantileTransformer
            data_reshaped = data.reshape(-1, 1)
            
            # Apply QuantileTransformer
            transformer = QuantileTransformer(output_distribution='normal', random_state=42)
            transformed_reshaped = transformer.fit_transform(data_reshaped)
            transformed = transformed_reshaped.flatten()
            
            details['method'] = 'quantile_normal'
            details['n_quantiles'] = transformer.n_quantiles_
            
            self._calculate_transformation_stats(data, transformed, details)
            details['success'] = True
            
        except Exception as e:
            details['error'] = f"Quantile transform failed: {str(e)}"
            details['success'] = False
            return None, details
        
        return transformed, details
    
    def _log_returns_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Log returns transformation for financial data."""
        try:
            # Calculate log returns
            log_returns = np.diff(np.log(data))
            
            # Pad with NaN to maintain original length
            transformed = np.full_like(data, np.nan)
            transformed[1:] = log_returns
            
            details['method'] = 'log_returns'
            details['note'] = 'First value is NaN (no previous value for return calculation)'
            
            # Calculate stats only for valid returns
            valid_returns = log_returns[~np.isnan(log_returns)]
            if len(valid_returns) > 0:
                self._calculate_transformation_stats(data, valid_returns, details)
            else:
                self._calculate_transformation_stats(data, transformed, details)
            
            details['success'] = True
            
        except Exception as e:
            details['error'] = f"Log returns transformation failed: {str(e)}"
            details['success'] = False
            return None, details
        
        return transformed, details
    
    def _robust_log_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Robust log transformation with outlier handling."""
        try:
            # Winsorize extreme values before log transformation
            winsorized_data = self._winsorize_data(data, limits=(0.01, 0.01))
            
            # Handle non-positive values
            min_val = np.min(winsorized_data)
            if min_val <= 0:
                constant = abs(min_val) + 1e-10
                data_shifted = winsorized_data + constant
                details['shift_constant'] = constant
            else:
                data_shifted = winsorized_data
                details['shift_constant'] = 0
            
            # Apply log transformation
            transformed = np.log(data_shifted)
            
            details['method'] = 'robust_log_with_winsorization'
            details['winsorization_limits'] = (0.01, 0.01)
            
            self._calculate_transformation_stats(data, transformed, details)
            details['success'] = True
            
        except Exception as e:
            details['error'] = f"Robust log transformation failed: {str(e)}"
            details['success'] = False
            return None, details
        
        return transformed, details
    
    def _adaptive_box_cox_transformation(self, data: np.ndarray, details: Dict[str, Any],
                                       target_skewness: float, target_kurtosis: float) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Adaptive Box-Cox transformation that optimizes for both skewness and kurtosis."""
        try:
            # Handle non-positive values
            if np.any(data <= 0):
                constant = self._calculate_optimal_shift(data)
                data_shifted = data + constant
                details['shift_constant'] = constant
            else:
                data_shifted = data
                details['shift_constant'] = 0
            
            # Optimize lambda for both skewness and kurtosis
            best_lambda = self._optimize_adaptive_box_cox(data_shifted, target_skewness, target_kurtosis)
            
            if best_lambda == 0:
                transformed = np.log(data_shifted)
                details['lambda'] = 0
                details['method'] = 'adaptive_log'
            else:
                transformed = (np.power(data_shifted, best_lambda) - 1) / best_lambda
                details['lambda'] = best_lambda
                details['method'] = 'adaptive_box_cox'
            
            details['target_skewness'] = target_skewness
            details['target_kurtosis'] = target_kurtosis
            
            self._calculate_transformation_stats(data, transformed, details)
            details['success'] = True
            
        except Exception as e:
            details['error'] = f"Adaptive Box-Cox transformation failed: {str(e)}"
            details['success'] = False
            return None, details
        
        return transformed, details
    
    def _winsorized_log_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Winsorized log transformation for handling extreme outliers."""
        try:
            # Apply more aggressive winsorization
            winsorized_data = self._winsorize_data(data, limits=(0.05, 0.05))
            
            # Handle non-positive values
            min_val = np.min(winsorized_data)
            if min_val <= 0:
                constant = abs(min_val) + 1e-10
                data_shifted = winsorized_data + constant
                details['shift_constant'] = constant
            else:
                data_shifted = winsorized_data
                details['shift_constant'] = 0
            
            # Apply log transformation
            transformed = np.log(data_shifted)
            
            details['method'] = 'winsorized_log'
            details['winsorization_limits'] = (0.05, 0.05)
            
            self._calculate_transformation_stats(data, transformed, details)
            details['success'] = True
            
        except Exception as e:
            details['error'] = f"Winsorized log transformation failed: {str(e)}"
            details['success'] = False
            return None, details
        
        return transformed, details
    
    def _financial_normalize_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Financial-specific normalization combining multiple techniques."""
        try:
            # Step 1: Calculate percentage changes
            pct_changes = np.diff(data) / data[:-1] * 100
            
            # Step 2: Apply robust scaling
            robust_scaler = RobustScaler()
            pct_changes_reshaped = pct_changes.reshape(-1, 1)
            scaled_changes = robust_scaler.fit_transform(pct_changes_reshaped).flatten()
            
            # Step 3: Apply log transformation to scaled changes
            # Add small constant to handle any remaining zeros
            scaled_changes_shifted = scaled_changes + 1e-10
            log_scaled = np.log(np.abs(scaled_changes_shifted)) * np.sign(scaled_changes)
            
            # Pad with NaN to maintain original length
            transformed = np.full_like(data, np.nan)
            transformed[1:] = log_scaled
            
            details['method'] = 'financial_normalize'
            details['steps'] = ['pct_change', 'robust_scale', 'log_transform']
            details['note'] = 'First value is NaN (no previous value for change calculation)'
            
            # Calculate stats for valid data
            valid_data = log_scaled[~np.isnan(log_scaled)]
            if len(valid_data) > 0:
                self._calculate_transformation_stats(data, valid_data, details)
            else:
                self._calculate_transformation_stats(data, transformed, details)
            
            details['success'] = True
            
        except Exception as e:
            details['error'] = f"Financial normalize transformation failed: {str(e)}"
            details['success'] = False
            return None, details
        
        return transformed, details
    
    def _calculate_optimal_shift(self, data: np.ndarray) -> float:
        """Calculate optimal shift constant for log transformation."""
        min_val = np.min(data)
        if min_val > 0:
            return 0
        
        # Use 1% of the data range as shift
        data_range = np.max(data) - min_val
        return abs(min_val) + data_range * 0.01
    
    def _optimize_box_cox_lambda(self, data: np.ndarray, target_skewness: float) -> float:
        """Optimize Box-Cox lambda parameter for target skewness."""
        def skewness_objective(lambda_val):
            if lambda_val == 0:
                transformed = np.log(data)
            else:
                transformed = (np.power(data, lambda_val) - 1) / lambda_val
            return abs(stats.skew(transformed) - target_skewness)
        
        try:
            result = minimize_scalar(skewness_objective, bounds=(-2, 2), method='bounded')
            return result.x
        except:
            # Fallback to standard Box-Cox
            _, lambda_val = boxcox(data)
            return lambda_val
    
    def _optimize_adaptive_box_cox(self, data: np.ndarray, target_skewness: float, 
                                 target_kurtosis: float) -> float:
        """Optimize Box-Cox lambda for both skewness and kurtosis."""
        def combined_objective(lambda_val):
            if lambda_val == 0:
                transformed = np.log(data)
            else:
                transformed = (np.power(data, lambda_val) - 1) / lambda_val
            
            skew_diff = abs(stats.skew(transformed) - target_skewness)
            kurt_diff = abs(stats.kurtosis(transformed) - target_kurtosis)
            
            # Weighted combination (skewness is usually more important)
            return 0.7 * skew_diff + 0.3 * kurt_diff
        
        try:
            result = minimize_scalar(combined_objective, bounds=(-2, 2), method='bounded')
            return result.x
        except:
            return self._optimize_box_cox_lambda(data, target_skewness)
    
    def _winsorize_data(self, data: np.ndarray, limits: Tuple[float, float] = (0.01, 0.01)) -> np.ndarray:
        """Winsorize data by capping extreme values."""
        lower_limit = np.percentile(data, limits[0] * 100)
        upper_limit = np.percentile(data, (1 - limits[1]) * 100)
        
        winsorized = np.clip(data, lower_limit, upper_limit)
        return winsorized
    
    def _calculate_transformation_stats(self, original: np.ndarray, transformed: np.ndarray, 
                                      details: Dict[str, Any]) -> None:
        """Calculate comprehensive transformation statistics."""
        # Basic statistics
        details['original_mean'] = float(np.mean(original))
        details['original_std'] = float(np.std(original))
        details['original_skewness'] = float(stats.skew(original))
        details['original_kurtosis'] = float(stats.kurtosis(original))
        
        # Transformed statistics (only for non-NaN values)
        valid_transformed = transformed[~np.isnan(transformed)]
        if len(valid_transformed) > 0:
            details['transformed_mean'] = float(np.mean(valid_transformed))
            details['transformed_std'] = float(np.std(valid_transformed))
            details['transformed_skewness'] = float(stats.skew(valid_transformed))
            details['transformed_kurtosis'] = float(stats.kurtosis(valid_transformed))
            
            # Improvement metrics
            details['skewness_improvement'] = abs(details['original_skewness']) - abs(details['transformed_skewness'])
            details['kurtosis_improvement'] = abs(details['original_kurtosis']) - abs(details['transformed_kurtosis'])
            
            # Overall improvement score
            details['improvement_score'] = self._calculate_improvement_score(
                details['original_skewness'], details['transformed_skewness'],
                details['original_kurtosis'], details['transformed_kurtosis']
            )
        else:
            details['transformed_mean'] = np.nan
            details['transformed_std'] = np.nan
            details['transformed_skewness'] = np.nan
            details['transformed_kurtosis'] = np.nan
            details['skewness_improvement'] = 0
            details['kurtosis_improvement'] = 0
            details['improvement_score'] = 0
    
    def _calculate_improvement_score(self, orig_skew: float, trans_skew: float,
                                   orig_kurt: float, trans_kurt: float) -> float:
        """Calculate overall improvement score for transformation."""
        # Normalize improvements to 0-1 scale
        skew_improvement = max(0, (abs(orig_skew) - abs(trans_skew)) / max(abs(orig_skew), 0.001))
        kurt_improvement = max(0, (abs(orig_kurt) - abs(trans_kurt)) / max(abs(orig_kurt), 0.001))
        
        # Weighted combination (skewness is more important for financial data)
        score = 0.7 * skew_improvement + 0.3 * kurt_improvement
        return min(score, 1.0)
    
    def _apply_standard_transformation(self, data: np.ndarray, transformation: str, 
                                     details: Dict[str, Any]) -> Tuple[Optional[np.ndarray], Dict[str, Any]]:
        """Apply standard transformation methods as fallback."""
        # This would call the original transformation methods
        # For now, return a simple log transformation
        try:
            if np.any(data <= 0):
                constant = abs(np.min(data)) + 1
                data_shifted = data + constant
                details['shift_constant'] = constant
            else:
                data_shifted = data
                details['shift_constant'] = 0
            
            transformed = np.log(data_shifted)
            self._calculate_transformation_stats(data, transformed, details)
            details['success'] = True
            
            return transformed, details
            
        except Exception as e:
            details['success'] = False
            details['error'] = str(e)
            return None, details
    
    def _get_numeric_columns(self, data: pd.DataFrame) -> List[str]:
        """Get list of numeric columns from DataFrame."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Filter out columns that are all NaN or have no variance
        valid_numeric_cols = []
        for col in numeric_cols:
            if not data[col].isna().all() and data[col].nunique() > 1:
                valid_numeric_cols.append(col)
        
        return valid_numeric_cols
    
    def get_enhanced_transformation_recommendations(self, data: pd.DataFrame, 
                                                  numeric_columns: Optional[List[str]] = None) -> Dict[str, List[str]]:
        """Get enhanced transformation recommendations based on data characteristics."""
        if numeric_columns is None:
            numeric_columns = self._get_numeric_columns(data)
        
        recommendations = {}
        
        for col in numeric_columns:
            col_data = data[col].dropna()
            if len(col_data) == 0:
                continue
            
            skewness = stats.skew(col_data)
            kurtosis = stats.kurtosis(col_data)
            
            col_recommendations = []
            
            # High skewness recommendations
            if abs(skewness) > 2.0:
                col_recommendations.extend(['robust_box_cox', 'adaptive_box_cox', 'quantile_transform'])
            elif abs(skewness) > 1.0:
                col_recommendations.extend(['enhanced_log', 'robust_log', 'power_transform'])
            elif abs(skewness) > 0.5:
                col_recommendations.extend(['winsorized_log', 'power_transform'])
            
            # High kurtosis recommendations
            if abs(kurtosis) > 5.0:
                col_recommendations.extend(['quantile_transform', 'adaptive_box_cox'])
            elif abs(kurtosis) > 2.0:
                col_recommendations.extend(['robust_box_cox', 'winsorized_log'])
            
            # Financial data specific recommendations
            if col.lower() in ['volume', 'amount', 'value']:
                col_recommendations.extend(['financial_normalize', 'log_returns'])
            
            # Remove duplicates while preserving order
            col_recommendations = list(dict.fromkeys(col_recommendations))
            
            if col_recommendations:
                recommendations[col] = col_recommendations
            else:
                recommendations[col] = ['enhanced_log']  # Default recommendation
        
        return recommendations
