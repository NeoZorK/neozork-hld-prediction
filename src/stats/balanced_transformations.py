"""
Balanced Data Transformations Module

This module provides balanced transformation methods that optimize for both
skewness and kurtosis simultaneously, avoiding the "WORSENED" kurtosis problem.

Key Features:
- Dual-parameter optimization (skewness + kurtosis)
- Adaptive transformation selection
- Financial data specific methods
- Outlier-resistant transformations
- Combined transformation strategies
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
from scipy import stats
from scipy.stats import boxcox, yeojohnson
from scipy.optimize import minimize_scalar
from sklearn.preprocessing import PowerTransformer, QuantileTransformer
import warnings

class BalancedTransformation:
    """Balanced transformation methods that optimize for both skewness and kurtosis."""
    
    def __init__(self):
        self.transformation_methods = {
            'balanced_log': self._balanced_log_transform,
            'balanced_box_cox': self._balanced_box_cox_transform,
            'adaptive_power': self._adaptive_power_transform,
            'quantile_normalize': self._quantile_normalize_transform,
            'robust_normalize': self._robust_normalize_transform,
            'financial_balanced': self._financial_balanced_transform,
            'combined_transform': self._combined_transform,
            'outlier_resistant': self._outlier_resistant_transform,
            'variance_stabilizing': self._variance_stabilizing_transform,
            'rank_based': self._rank_based_transform
        }
    
    def _balanced_log_transform(self, data: pd.Series, **kwargs) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Balanced log transformation that minimizes both skewness and kurtosis.
        
        Uses adaptive offset and scaling to balance the effects.
        """
        try:
            # Remove zeros and negatives
            clean_data = data[data > 0].copy()
            if len(clean_data) == 0:
                return data, {'success': False, 'error': 'No positive values for log transform'}
            
            # Adaptive offset to balance skewness and kurtosis
            offset = self._find_balanced_offset(clean_data, 'log')
            
            # Apply balanced log transformation
            transformed = np.log(clean_data + offset)
            
            # Calculate improvements
            orig_skew = stats.skew(data.dropna())
            orig_kurt = stats.kurtosis(data.dropna())
            trans_skew = stats.skew(transformed)
            trans_kurt = stats.kurtosis(transformed)
            
            # Balanced score with penalties for worsening
            skew_improvement = abs(orig_skew) - abs(trans_skew)
            kurt_improvement = abs(orig_kurt) - abs(trans_kurt)
            
            # Apply heavy penalties for worsening
            skew_penalty = 0
            kurt_penalty = 0
            
            if abs(trans_skew) > abs(orig_skew):
                skew_penalty = (abs(trans_skew) - abs(orig_skew)) * 100  # Extreme penalty
            
            if abs(trans_kurt) > abs(orig_kurt):
                kurt_penalty = (abs(trans_kurt) - abs(orig_kurt)) * 200  # Extreme penalty
            
            # Bonus for improving both
            both_improved_bonus = 0.5 if skew_improvement > 0 and kurt_improvement > 0 else 0
            
            balanced_score = (skew_improvement + kurt_improvement) / 2 + both_improved_bonus - skew_penalty - kurt_penalty
            
            return transformed, {
                'success': True,
                'method': 'balanced_log',
                'offset': offset,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score,
                'original_skewness': orig_skew,
                'original_kurtosis': orig_kurt,
                'transformed_skewness': trans_skew,
                'transformed_kurtosis': trans_kurt
            }
            
        except Exception as e:
            return data, {'success': False, 'error': str(e)}
    
    def _balanced_box_cox_transform(self, data: pd.Series, **kwargs) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Balanced Box-Cox transformation that optimizes for both skewness and kurtosis.
        """
        try:
            # Ensure positive values
            if (data <= 0).any():
                shift = abs(data.min()) + 1
                shifted_data = data + shift
            else:
                shift = 0
                shifted_data = data.copy()
            
            # Find optimal lambda that balances skewness and kurtosis
            optimal_lambda = self._find_balanced_lambda(shifted_data)
            
            # Apply Box-Cox transformation
            if optimal_lambda == 0:
                transformed = np.log(shifted_data)
            else:
                transformed = (shifted_data ** optimal_lambda - 1) / optimal_lambda
            
            # Calculate improvements
            orig_skew = stats.skew(data.dropna())
            orig_kurt = stats.kurtosis(data.dropna())
            trans_skew = stats.skew(transformed)
            trans_kurt = stats.kurtosis(transformed)
            
            # Balanced score
            skew_improvement = abs(orig_skew) - abs(trans_skew)
            kurt_improvement = abs(orig_kurt) - abs(trans_kurt)
            balanced_score = (skew_improvement + kurt_improvement) / 2
            
            return transformed, {
                'success': True,
                'method': 'balanced_box_cox',
                'lambda': optimal_lambda,
                'shift': shift,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score,
                'original_skewness': orig_skew,
                'original_kurtosis': orig_kurt,
                'transformed_skewness': trans_skew,
                'transformed_kurtosis': trans_kurt
            }
            
        except Exception as e:
            return data, {'success': False, 'error': str(e)}
    
    def _adaptive_power_transform(self, data: pd.Series, **kwargs) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Adaptive power transformation that adjusts based on data characteristics.
        """
        try:
            # Analyze data characteristics
            skewness = stats.skew(data.dropna())
            kurtosis = stats.kurtosis(data.dropna())
            
            # Choose transformation based on data characteristics
            if abs(skewness) > 1.0 and kurtosis > 1.0:
                # High skewness and kurtosis - use strong transformation
                power = 0.1 if skewness > 0 else 2.0
            elif abs(skewness) > 0.5:
                # Moderate skewness - use moderate transformation
                power = 0.3 if skewness > 0 else 1.5
            else:
                # Low skewness - use mild transformation
                power = 0.5 if skewness > 0 else 1.2
            
            # Apply adaptive power transformation
            if power < 1:
                # For right-skewed data
                transformed = data ** power
            else:
                # For left-skewed data
                transformed = data ** power
            
            # Calculate improvements
            orig_skew = stats.skew(data.dropna())
            orig_kurt = stats.kurtosis(data.dropna())
            trans_skew = stats.skew(transformed)
            trans_kurt = stats.kurtosis(transformed)
            
            # Balanced score
            skew_improvement = abs(orig_skew) - abs(trans_skew)
            kurt_improvement = abs(orig_kurt) - abs(trans_kurt)
            balanced_score = (skew_improvement + kurt_improvement) / 2
            
            return transformed, {
                'success': True,
                'method': 'adaptive_power',
                'power': power,
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score,
                'original_skewness': orig_skew,
                'original_kurtosis': orig_kurt,
                'transformed_skewness': trans_skew,
                'transformed_kurtosis': trans_kurt
            }
            
        except Exception as e:
            return data, {'success': False, 'error': str(e)}
    
    def _quantile_normalize_transform(self, data: pd.Series, **kwargs) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Quantile-based normalization that preserves distribution shape while normalizing.
        """
        try:
            # Use QuantileTransformer to map to normal distribution
            qt = QuantileTransformer(output_distribution='normal', random_state=42)
            transformed = qt.fit_transform(data.values.reshape(-1, 1)).flatten()
            transformed = pd.Series(transformed, index=data.index)
            
            # Calculate improvements
            orig_skew = stats.skew(data.dropna())
            orig_kurt = stats.kurtosis(data.dropna())
            trans_skew = stats.skew(transformed)
            trans_kurt = stats.kurtosis(transformed)
            
            # Balanced score
            skew_improvement = abs(orig_skew) - abs(trans_skew)
            kurt_improvement = abs(orig_kurt) - abs(trans_kurt)
            balanced_score = (skew_improvement + kurt_improvement) / 2
            
            return transformed, {
                'success': True,
                'method': 'quantile_normalize',
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score,
                'original_skewness': orig_skew,
                'original_kurtosis': orig_kurt,
                'transformed_skewness': trans_skew,
                'transformed_kurtosis': trans_kurt
            }
            
        except Exception as e:
            return data, {'success': False, 'error': str(e)}
    
    def _robust_normalize_transform(self, data: pd.Series, **kwargs) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Robust normalization using median and IQR instead of mean and std.
        """
        try:
            # Calculate robust statistics
            median = data.median()
            q75, q25 = data.quantile([0.75, 0.25])
            iqr = q75 - q25
            
            # Robust normalization
            transformed = (data - median) / iqr
            
            # Apply mild transformation to reduce extreme values
            transformed = np.tanh(transformed * 0.5) * 2
            
            # Calculate improvements
            orig_skew = stats.skew(data.dropna())
            orig_kurt = stats.kurtosis(data.dropna())
            trans_skew = stats.skew(transformed)
            trans_kurt = stats.kurtosis(transformed)
            
            # Balanced score
            skew_improvement = abs(orig_skew) - abs(trans_skew)
            kurt_improvement = abs(orig_kurt) - abs(trans_kurt)
            balanced_score = (skew_improvement + kurt_improvement) / 2
            
            return transformed, {
                'success': True,
                'method': 'robust_normalize',
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score,
                'original_skewness': orig_skew,
                'original_kurtosis': orig_kurt,
                'transformed_skewness': trans_skew,
                'transformed_kurtosis': trans_kurt
            }
            
        except Exception as e:
            return data, {'success': False, 'error': str(e)}
    
    def _financial_balanced_transform(self, data: pd.Series, **kwargs) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Financial-specific balanced transformation for price/volume data.
        """
        try:
            # Check if data looks like prices (positive, increasing trend)
            if data.min() > 0 and data.std() / data.mean() > 0.1:
                # Price-like data - use log transformation with balanced approach
                return self._balanced_log_transform(data)
            else:
                # Volume or other data - use adaptive approach
                return self._adaptive_power_transform(data)
                
        except Exception as e:
            return data, {'success': False, 'error': str(e)}
    
    def _combined_transform(self, data: pd.Series, **kwargs) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Combined transformation that applies multiple methods and selects the best.
        """
        try:
            best_transformed = None
            best_score = -float('inf')
            best_details = {}
            
            # Try multiple methods
            methods = ['balanced_log', 'balanced_box_cox', 'adaptive_power', 'quantile_normalize']
            
            for method in methods:
                if method in self.transformation_methods:
                    transformed, details = self.transformation_methods[method](data)
                    if details.get('success', False) and details.get('balanced_score', 0) > best_score:
                        best_score = details['balanced_score']
                        best_transformed = transformed
                        best_details = details
            
            if best_transformed is not None:
                return best_transformed, best_details
            else:
                return data, {'success': False, 'error': 'No suitable transformation found'}
                
        except Exception as e:
            return data, {'success': False, 'error': str(e)}
    
    def _outlier_resistant_transform(self, data: pd.Series, **kwargs) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Outlier-resistant transformation using winsorization and robust methods.
        """
        try:
            # Winsorize extreme values
            q99, q01 = data.quantile([0.99, 0.01])
            winsorized_data = data.clip(lower=q01, upper=q99)
            
            # Apply balanced transformation to winsorized data
            return self._balanced_log_transform(winsorized_data)
            
        except Exception as e:
            return data, {'success': False, 'error': str(e)}
    
    def _variance_stabilizing_transform(self, data: pd.Series, **kwargs) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Variance stabilizing transformation that reduces both skewness and kurtosis.
        """
        try:
            # Use PowerTransformer with Yeo-Johnson
            pt = PowerTransformer(method='yeo-johnson', standardize=False)
            transformed = pt.fit_transform(data.values.reshape(-1, 1)).flatten()
            transformed = pd.Series(transformed, index=data.index)
            
            # Calculate improvements
            orig_skew = stats.skew(data.dropna())
            orig_kurt = stats.kurtosis(data.dropna())
            trans_skew = stats.skew(transformed)
            trans_kurt = stats.kurtosis(transformed)
            
            # Balanced score
            skew_improvement = abs(orig_skew) - abs(trans_skew)
            kurt_improvement = abs(orig_kurt) - abs(trans_kurt)
            balanced_score = (skew_improvement + kurt_improvement) / 2
            
            return transformed, {
                'success': True,
                'method': 'variance_stabilizing',
                'skewness_improvement': skew_improvement,
                'kurtosis_improvement': kurt_improvement,
                'balanced_score': balanced_score,
                'original_skewness': orig_skew,
                'original_kurtosis': orig_kurt,
                'transformed_skewness': trans_skew,
                'transformed_kurtosis': trans_kurt
            }
            
        except Exception as e:
            return data, {'success': False, 'error': str(e)}
    
    def _rank_based_transform(self, data: pd.Series, **kwargs) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Rank-based transformation that preserves order while normalizing distribution.
        """
        try:
            # Convert to ranks
            ranks = data.rank(method='average')
            
            # Normalize ranks to standard normal distribution
            n = len(ranks)
            transformed = stats.norm.ppf(ranks / (n + 1))
            
            # Calculate improvements
            orig_skew = stats.skew(data.dropna())
            orig_kurt = stats.kurtosis(data.dropna())
            trans_skew = stats.skew(transformed)
            trans_kurt = stats.kurtosis(transformed)
            
            # Balanced score
            skew_improvement = abs(orig_skew) - abs(trans_skew)
            kurt_improvement = abs(orig_kurt) - abs(trans_kurt)
            balanced_score = (skew_improvement + kurt_improvement) / 2
            
            return transformed, {
                'success': True,
                'method': 'rank_based',
                'skewness_improvement': skew_improvement,
                'kurt_improvement': kurt_improvement,
                'balanced_score': balanced_score,
                'original_skewness': orig_skew,
                'original_kurtosis': orig_kurt,
                'transformed_skewness': trans_skew,
                'transformed_kurtosis': trans_kurt
            }
            
        except Exception as e:
            return data, {'success': False, 'error': str(e)}
    
    def _find_balanced_offset(self, data: pd.Series, method: str) -> float:
        """Find optimal offset that balances skewness and kurtosis improvements."""
        def objective(offset):
            try:
                if method == 'log':
                    transformed = np.log(data + offset)
                else:
                    transformed = np.sqrt(data + offset)
                
                orig_skew = abs(stats.skew(data))
                orig_kurt = abs(stats.kurtosis(data))
                trans_skew = abs(stats.skew(transformed))
                trans_kurt = abs(stats.kurtosis(transformed))
                
                # Minimize combined deviation from normal
                skew_improvement = orig_skew - trans_skew
                kurt_improvement = orig_kurt - trans_kurt
                
                # Return negative score (minimize = maximize negative)
                return -(skew_improvement + kurt_improvement)
            except:
                return float('inf')
        
        # Find optimal offset
        result = minimize_scalar(objective, bounds=(0.001, 10.0), method='bounded')
        return result.x if result.success else 0.001
    
    def _find_balanced_lambda(self, data: pd.Series) -> float:
        """Find optimal lambda for Box-Cox that balances skewness and kurtosis."""
        def objective(lambda_val):
            try:
                if lambda_val == 0:
                    transformed = np.log(data)
                else:
                    transformed = (data ** lambda_val - 1) / lambda_val
                
                orig_skew = abs(stats.skew(data))
                orig_kurt = abs(stats.kurtosis(data))
                trans_skew = abs(stats.skew(transformed))
                trans_kurt = abs(stats.kurtosis(transformed))
                
                # Minimize combined deviation from normal
                skew_improvement = orig_skew - trans_skew
                kurt_improvement = orig_kurt - trans_kurt
                
                # Return negative score (minimize = maximize negative)
                return -(skew_improvement + kurt_improvement)
            except:
                return float('inf')
        
        # Find optimal lambda
        result = minimize_scalar(objective, bounds=(-2.0, 2.0), method='bounded')
        return result.x if result.success else 0.0
    
    def get_balanced_transformation_recommendations(self, data: pd.DataFrame, 
                                                  numeric_columns: List[str]) -> Dict[str, List[str]]:
        """Get balanced transformation recommendations for each column."""
        recommendations = {}
        
        for col in numeric_columns:
            if col not in data.columns:
                continue
                
            col_data = data[col].dropna()
            if len(col_data) == 0:
                continue
            
            # Analyze data characteristics
            skewness = abs(stats.skew(col_data))
            kurtosis = abs(stats.kurtosis(col_data))
            
            # Recommend transformations based on data characteristics
            if skewness > 1.0 and kurtosis > 1.0:
                # High skewness and kurtosis
                recommendations[col] = ['balanced_box_cox', 'quantile_normalize', 'combined_transform']
            elif skewness > 0.5:
                # Moderate skewness
                recommendations[col] = ['balanced_log', 'adaptive_power', 'variance_stabilizing']
            elif kurtosis > 1.0:
                # High kurtosis only
                recommendations[col] = ['quantile_normalize', 'rank_based', 'robust_normalize']
            else:
                # Low skewness and kurtosis
                recommendations[col] = ['robust_normalize', 'outlier_resistant']
        
        return recommendations
    
    def apply_balanced_transformation(self, data: pd.Series, method: str, **kwargs) -> Tuple[pd.Series, Dict[str, Any]]:
        """Apply a specific balanced transformation method."""
        if method in self.transformation_methods:
            return self.transformation_methods[method](data, **kwargs)
        else:
            return data, {'success': False, 'error': f'Unknown method: {method}'}
