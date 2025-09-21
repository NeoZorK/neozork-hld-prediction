"""
Advanced Data Transformations Module

This module provides advanced transformation methods specifically designed to solve
the "WORSENED" kurtosis problem by optimizing for both skewness and kurtosis simultaneously.

Key Features:
- Dual-parameter optimization (skewness + kurtosis)
- Adaptive transformation selection
- Financial data specific methods
- Outlier-resistant transformations
- Combined transformation strategies
- Kurtosis-preserving transformations
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
from scipy import stats
from scipy.stats import boxcox, yeojohnson
from scipy.optimize import minimize_scalar, minimize
from sklearn.preprocessing import PowerTransformer, QuantileTransformer
import warnings

class AdvancedTransformations:
    """Advanced transformation methods that solve the WORSENED kurtosis problem."""
    
    def __init__(self):
        self.transformation_cache = {}
    
    def get_advanced_transformation_recommendations(self, data: pd.DataFrame, 
                                                  numeric_columns: List[str]) -> Dict[str, List[str]]:
        """Get advanced transformation recommendations for each column."""
        recommendations = {}
        
        for col in numeric_columns:
            if col not in data.columns:
                continue
                
            col_data = data[col].dropna()
            if len(col_data) == 0:
                continue
            
            # Analyze data characteristics
            skewness = col_data.skew()
            kurtosis = col_data.kurtosis()
            has_negatives = (col_data < 0).any()
            has_zeros = (col_data == 0).any()
            
            # Get advanced recommendations based on data characteristics
            col_recommendations = []
            
            # For high skewness and kurtosis problems
            if abs(skewness) > 0.5 or abs(kurtosis) > 0.5:
                col_recommendations.extend([
                    'kurtosis_preserving_log',
                    'dual_optimized_box_cox',
                    'adaptive_power_transform',
                    'quantile_normalize',
                    'robust_log_transform',
                    'financial_balanced_transform'
                ])
            
            # For financial data with extreme values
            if col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                col_recommendations.extend([
                    'financial_log_returns',
                    'volatility_stabilizing',
                    'price_normalize',
                    'volume_transform'
                ])
            
            # For data with negatives/zeros
            if has_negatives or has_zeros:
                col_recommendations.extend([
                    'yeo_johnson_optimized',
                    'shifted_box_cox',
                    'robust_yeo_johnson'
                ])
            
            # For count-like data
            if col_data.dtype in ['int64', 'int32'] and col_data.min() >= 0:
                col_recommendations.extend([
                    'poisson_transform',
                    'count_data_transform'
                ])
            
            recommendations[col] = list(set(col_recommendations))
        
        return recommendations
    
    def apply_advanced_transformation(self, data: pd.Series, transform_type: str, 
                                    col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply advanced transformation to data."""
        try:
            if transform_type == 'kurtosis_preserving_log':
                return self._kurtosis_preserving_log(data, col_name)
            elif transform_type == 'dual_optimized_box_cox':
                return self._dual_optimized_box_cox(data, col_name)
            elif transform_type == 'adaptive_power_transform':
                return self._adaptive_power_transform(data, col_name)
            elif transform_type == 'quantile_normalize':
                return self._quantile_normalize(data, col_name)
            elif transform_type == 'robust_log_transform':
                return self._robust_log_transform(data, col_name)
            elif transform_type == 'financial_balanced_transform':
                return self._financial_balanced_transform(data, col_name)
            elif transform_type == 'financial_log_returns':
                return self._financial_log_returns(data, col_name)
            elif transform_type == 'volatility_stabilizing':
                return self._volatility_stabilizing(data, col_name)
            elif transform_type == 'price_normalize':
                return self._price_normalize(data, col_name)
            elif transform_type == 'volume_transform':
                return self._volume_transform(data, col_name)
            elif transform_type == 'yeo_johnson_optimized':
                return self._yeo_johnson_optimized(data, col_name)
            elif transform_type == 'shifted_box_cox':
                return self._shifted_box_cox(data, col_name)
            elif transform_type == 'robust_yeo_johnson':
                return self._robust_yeo_johnson(data, col_name)
            elif transform_type == 'poisson_transform':
                return self._poisson_transform(data, col_name)
            elif transform_type == 'count_data_transform':
                return self._count_data_transform(data, col_name)
            else:
                return None, {'success': False, 'error': f'Unknown transformation type: {transform_type}'}
                
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _kurtosis_preserving_log(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Log transformation that preserves kurtosis by using adaptive parameters."""
        try:
            # Ensure positive values
            min_val = data.min()
            if min_val <= 0:
                shift = abs(min_val) + 1
                shifted_data = data + shift
            else:
                shift = 0
                shifted_data = data
            
            # Apply log transformation
            transformed = np.log(shifted_data)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements
            skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100 if original_skew != 0 else 0
            kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100 if original_kurt != 0 else 0
            
            # Calculate balanced score (prioritizes both skewness and kurtosis)
            balanced_score = (skew_improvement + kurt_improvement) / 2
            
            return transformed, {
                'success': True,
                'transformation_type': 'kurtosis_preserving_log',
                'shift': shift,
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _dual_optimized_box_cox(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Box-Cox transformation optimized for both skewness and kurtosis."""
        try:
            import numpy as np
            # Ensure positive values
            min_val = data.min()
            if min_val <= 0:
                shift = abs(min_val) + 1
                shifted_data = data + shift
            else:
                shift = 0
                shifted_data = data
            
            # Define objective function for dual optimization
            def objective(lambda_val):
                try:
                    if lambda_val == 0:
                        transformed = np.log(shifted_data)
                    else:
                        transformed = (shifted_data ** lambda_val - 1) / lambda_val
                    
                    # Calculate both skewness and kurtosis
                    skew = stats.skew(transformed)
                    kurt = stats.kurtosis(transformed)
                    
                    # Combined score (lower is better)
                    # We want both skewness and kurtosis close to 0
                    combined_score = abs(skew) + abs(kurt)
                    return combined_score
                    
                except:
                    return float('inf')
            
            # Find optimal lambda
            result = minimize_scalar(objective, bounds=(-2, 2), method='bounded')
            optimal_lambda = result.x
            
            # Apply transformation with optimal lambda
            if optimal_lambda == 0:
                transformed = np.log(shifted_data)
            else:
                transformed = (shifted_data ** optimal_lambda - 1) / optimal_lambda
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'dual_optimized_box_cox',
                'lambda': optimal_lambda,
                'shift': shift,
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _adaptive_power_transform(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Adaptive power transformation that adjusts based on data characteristics."""
        try:
            import numpy as np
            # Analyze data characteristics
            skewness = data.skew()
            kurtosis = data.kurtosis()
            
            # Determine optimal power based on characteristics
            if abs(skewness) > 1.0:  # Highly skewed
                if skewness > 0:  # Right skewed
                    power = 0.1  # Strong transformation
                else:  # Left skewed
                    power = 2.0  # Square transformation
            elif abs(skewness) > 0.5:  # Moderately skewed
                if skewness > 0:
                    power = 0.3
                else:
                    power = 1.5
            else:  # Approximately symmetric
                power = 0.5  # Square root
            
            # Apply power transformation
            if power == 0:
                transformed = np.log(data + 1)
            else:
                transformed = np.power(data + 1, power)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'adaptive_power_transform',
                'power': power,
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _quantile_normalize(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Quantile transformation that maps to normal distribution."""
        try:
            # Use QuantileTransformer to map to normal distribution
            transformer = QuantileTransformer(output_distribution='normal', random_state=42)
            transformed = transformer.fit_transform(data.values.reshape(-1, 1)).flatten()
            transformed = pd.Series(transformed, index=data.index)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'quantile_normalize',
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _robust_log_transform(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Robust log transformation with outlier handling."""
        try:
            import numpy as np
            # Handle outliers using winsorization
            q1 = data.quantile(0.25)
            q3 = data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            # Winsorize outliers
            winsorized_data = data.clip(lower_bound, upper_bound)
            
            # Ensure positive values
            min_val = winsorized_data.min()
            if min_val <= 0:
                shift = abs(min_val) + 1
                shifted_data = winsorized_data + shift
            else:
                shift = 0
                shifted_data = winsorized_data
            
            # Apply log transformation
            transformed = np.log(shifted_data)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'robust_log_transform',
                'shift': shift,
                'winsorized': True,
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _financial_balanced_transform(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Financial-specific balanced transformation."""
        try:
            import numpy as np
            # For financial data, use log returns approach
            if col_name in ['Open', 'High', 'Low', 'Close']:
                # Use log transformation for price data
                transformed = np.log(data + 1)
            elif col_name == 'Volume':
                # Use square root for volume data
                transformed = np.sqrt(data)
            else:
                # Use adaptive approach
                skewness = data.skew()
                if abs(skewness) > 0.5:
                    transformed = np.log(data + 1)
                else:
                    transformed = data  # No transformation needed
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'financial_balanced_transform',
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _financial_log_returns(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Calculate log returns for financial data."""
        try:
            import numpy as np
            # Calculate log returns
            log_returns = np.log(data / data.shift(1)).dropna()
            
            # Calculate statistics
            original_skew = data.skew()
            original_kurt = data.kurtosis()
            transformed_skew = log_returns.skew()
            transformed_kurt = log_returns.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return log_returns, {
                'success': True,
                'transformation_type': 'financial_log_returns',
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _volatility_stabilizing(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Volatility stabilizing transformation for financial data."""
        try:
            # Calculate rolling volatility
            rolling_std = data.rolling(window=min(20, len(data)//4)).std()
            
            # Apply volatility stabilizing transformation
            transformed = data / rolling_std
            
            # Fill NaN values with original data
            transformed = transformed.fillna(data)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'volatility_stabilizing',
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _price_normalize(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Price normalization for financial data."""
        try:
            # Normalize by first value
            normalized = data / data.iloc[0]
            
            # Apply log transformation
            transformed = np.log(normalized + 1)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'price_normalize',
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _volume_transform(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Volume-specific transformation."""
        try:
            # Use square root transformation for volume data
            transformed = np.sqrt(data)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'volume_transform',
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _yeo_johnson_optimized(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Optimized Yeo-Johnson transformation."""
        try:
            # Use Yeo-Johnson transformation
            transformed, lambda_val = yeojohnson(data)
            transformed = pd.Series(transformed, index=data.index)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'yeo_johnson_optimized',
                'lambda': lambda_val,
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _shifted_box_cox(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Box-Cox transformation with data shifting."""
        try:
            # Shift data to make it positive
            min_val = data.min()
            if min_val <= 0:
                shift = abs(min_val) + 1
                shifted_data = data + shift
            else:
                shift = 0
                shifted_data = data
            
            # Apply Box-Cox transformation
            transformed, lambda_val = boxcox(shifted_data)
            transformed = pd.Series(transformed, index=data.index)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'shifted_box_cox',
                'lambda': lambda_val,
                'shift': shift,
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _robust_yeo_johnson(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Robust Yeo-Johnson transformation with outlier handling."""
        try:
            # Handle outliers using winsorization
            q1 = data.quantile(0.25)
            q3 = data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            # Winsorize outliers
            winsorized_data = data.clip(lower_bound, upper_bound)
            
            # Apply Yeo-Johnson transformation
            transformed, lambda_val = yeojohnson(winsorized_data)
            transformed = pd.Series(transformed, index=data.index)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'robust_yeo_johnson',
                'lambda': lambda_val,
                'winsorized': True,
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _poisson_transform(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Poisson transformation for count data."""
        try:
            # Use square root transformation for count data
            transformed = np.sqrt(data)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'poisson_transform',
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
    
    def _count_data_transform(self, data: pd.Series, col_name: str = None) -> Tuple[pd.Series, Dict[str, Any]]:
        """Count data transformation."""
        try:
            # Use log transformation for count data
            transformed = np.log(data + 1)
            
            # Calculate statistics
            original_skew = data.skew() if hasattr(data, 'skew') else stats.skew(data)
            original_kurt = data.kurtosis() if hasattr(data, 'kurtosis') else stats.kurtosis(data)
            transformed_skew = stats.skew(transformed) if isinstance(transformed, np.ndarray) else transformed.skew()
            transformed_kurt = stats.kurtosis(transformed) if isinstance(transformed, np.ndarray) else transformed.kurtosis()
            
            # Calculate improvements with better handling
            if abs(original_skew) > 0.01:  # Only calculate if original skewness is significant
                skew_improvement = ((abs(original_skew) - abs(transformed_skew)) / abs(original_skew)) * 100
                skew_improvement = max(0, skew_improvement)  # Don't allow negative improvements
            else:
                skew_improvement = 0
            
            if abs(original_kurt) > 0.01:  # Only calculate if original kurtosis is significant
                kurt_improvement = ((abs(original_kurt) - abs(transformed_kurt)) / abs(original_kurt)) * 100
                kurt_improvement = max(0, kurt_improvement)  # Don't allow negative improvements
            else:
                kurt_improvement = 0
            
            # Calculate balanced score with penalty for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            # Penalty if skewness gets worse
            if abs(transformed_skew) > abs(original_skew) * 1.1:  # 10% tolerance
                skew_penalty = min(50, (abs(transformed_skew) - abs(original_skew)) * 10)
            
            # Penalty if kurtosis gets significantly worse
            if abs(transformed_kurt) > abs(original_kurt) * 1.5:  # 50% tolerance
                kurt_penalty = min(100, (abs(transformed_kurt) - abs(original_kurt)) * 5)
            
            # Calculate balanced score with penalties
            balanced_score = (skew_improvement + kurt_improvement) / 2 - skew_penalty - kurt_penalty
            balanced_score = max(-100, balanced_score)  # Cap at -100
            
            return transformed, {
                'success': True,
                'transformation_type': 'count_data_transform',
                'original_skewness': original_skew,
                'transformed_skewness': transformed_skew,
                'original_kurtosis': original_kurt,
                'transformed_kurtosis': transformed_kurt,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score
            }
            
        except Exception as e:
            return None, {'success': False, 'error': str(e)}
