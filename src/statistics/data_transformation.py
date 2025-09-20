"""
Data Transformation Module

This module provides comprehensive data transformation capabilities for financial data.
It includes various transformation methods to improve data distribution characteristics.

Features:
- Log transformation: For positive skewness
- Square root transformation: For mild positive skewness
- Box-Cox transformation: Optimal transformation
- Yeo-Johnson transformation: For data with zeros/negatives
- Standardization: Z-score normalization
- Min-Max scaling: Scaling to [0,1] range
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
from scipy import stats
from scipy.stats import boxcox, yeojohnson
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import logging


class DataTransformation:
    """Handles data transformation operations."""
    
    def __init__(self):
        """Initialize the data transformer."""
        self.logger = logging.getLogger(__name__)
        self.scaler_standard = StandardScaler()
        self.scaler_minmax = MinMaxScaler()
    
    def transform_data(self, data: pd.DataFrame, transformations: Dict[str, List[str]], 
                      numeric_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Apply specified transformations to data.
        
        Args:
            data: DataFrame to transform
            transformations: Dictionary mapping column names to list of transformations
            numeric_columns: List of numeric columns. If None, auto-detect.
            
        Returns:
            Dictionary containing transformed data and transformation details
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
            
            col_transformations = transformations[col]
            col_data = data[col].dropna()
            
            if len(col_data) == 0:
                continue
            
            col_details = {}
            
            for transformation in col_transformations:
                try:
                    transformed_col, details = self._apply_transformation(
                        col_data, transformation, col
                    )
                    
                    if transformed_col is not None:
                        # Create new column name
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
    
    def _get_numeric_columns(self, data: pd.DataFrame) -> List[str]:
        """
        Get list of numeric columns from DataFrame.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of numeric column names
        """
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Filter out columns that are all NaN or have no variance
        valid_numeric_cols = []
        for col in numeric_cols:
            if not data[col].isna().all() and data[col].nunique() > 1:
                valid_numeric_cols.append(col)
        
        return valid_numeric_cols
    
    def _apply_transformation(self, data: np.ndarray, transformation: str, 
                            column_name: str) -> Tuple[Optional[np.ndarray], Dict[str, Any]]:
        """
        Apply a specific transformation to data.
        
        Args:
            data: Array of data to transform
            transformation: Name of transformation to apply
            column_name: Name of the column being transformed
            
        Returns:
            Tuple of (transformed_data, transformation_details)
        """
        details = {
            'transformation': transformation,
            'column': column_name,
            'original_shape': data.shape,
            'success': True
        }
        
        try:
            if transformation == 'log':
                return self._log_transformation(data, details)
            elif transformation == 'sqrt':
                return self._sqrt_transformation(data, details)
            elif transformation == 'square':
                return self._square_transformation(data, details)
            elif transformation == 'box_cox':
                return self._box_cox_transformation(data, details)
            elif transformation == 'yeo_johnson':
                return self._yeo_johnson_transformation(data, details)
            elif transformation == 'standardize':
                return self._standardize_transformation(data, details)
            elif transformation == 'minmax':
                return self._minmax_transformation(data, details)
            else:
                raise ValueError(f"Unknown transformation: {transformation}")
        
        except Exception as e:
            details['success'] = False
            details['error'] = str(e)
            return None, details
    
    def _log_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Apply log transformation."""
        # Check for non-positive values
        if np.any(data <= 0):
            # Add constant to make all values positive
            min_val = np.min(data)
            if min_val <= 0:
                constant = abs(min_val) + 1
                data_shifted = data + constant
                details['shift_constant'] = constant
                details['note'] = f"Added constant {constant} to handle non-positive values"
            else:
                data_shifted = data
                details['shift_constant'] = 0
        else:
            data_shifted = data
            details['shift_constant'] = 0
        
        # Apply log transformation
        transformed = np.log(data_shifted)
        
        # Calculate statistics
        details['original_mean'] = float(np.mean(data))
        details['original_std'] = float(np.std(data))
        details['transformed_mean'] = float(np.mean(transformed))
        details['transformed_std'] = float(np.std(transformed))
        details['original_skewness'] = float(stats.skew(data))
        details['transformed_skewness'] = float(stats.skew(transformed))
        
        return transformed, details
    
    def _sqrt_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Apply square root transformation."""
        # Check for negative values
        if np.any(data < 0):
            # Add constant to make all values non-negative
            min_val = np.min(data)
            constant = abs(min_val)
            data_shifted = data + constant
            details['shift_constant'] = constant
            details['note'] = f"Added constant {constant} to handle negative values"
        else:
            data_shifted = data
            details['shift_constant'] = 0
        
        # Apply square root transformation
        transformed = np.sqrt(data_shifted)
        
        # Calculate statistics
        details['original_mean'] = float(np.mean(data))
        details['original_std'] = float(np.std(data))
        details['transformed_mean'] = float(np.mean(transformed))
        details['transformed_std'] = float(np.std(transformed))
        details['original_skewness'] = float(stats.skew(data))
        details['transformed_skewness'] = float(stats.skew(transformed))
        
        return transformed, details
    
    def _square_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Apply square transformation."""
        # Apply square transformation
        transformed = np.square(data)
        
        # Calculate statistics
        details['original_mean'] = float(np.mean(data))
        details['original_std'] = float(np.std(data))
        details['transformed_mean'] = float(np.mean(transformed))
        details['transformed_std'] = float(np.std(transformed))
        details['original_skewness'] = float(stats.skew(data))
        details['transformed_skewness'] = float(stats.skew(transformed))
        
        return transformed, details
    
    def _box_cox_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Apply Box-Cox transformation."""
        # Box-Cox requires positive values
        if np.any(data <= 0):
            # Add constant to make all values positive
            min_val = np.min(data)
            constant = abs(min_val) + 1
            data_shifted = data + constant
            details['shift_constant'] = constant
            details['note'] = f"Added constant {constant} to handle non-positive values"
        else:
            data_shifted = data
            details['shift_constant'] = 0
        
        try:
            # Apply Box-Cox transformation
            transformed, lambda_value = boxcox(data_shifted)
            details['lambda'] = float(lambda_value)
            
            # Calculate statistics
            details['original_mean'] = float(np.mean(data))
            details['original_std'] = float(np.std(data))
            details['transformed_mean'] = float(np.mean(transformed))
            details['transformed_std'] = float(np.std(transformed))
            details['original_skewness'] = float(stats.skew(data))
            details['transformed_skewness'] = float(stats.skew(transformed))
            
        except Exception as e:
            details['error'] = f"Box-Cox transformation failed: {str(e)}"
            details['success'] = False
            return None, details
        
        return transformed, details
    
    def _yeo_johnson_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Apply Yeo-Johnson transformation."""
        try:
            # Apply Yeo-Johnson transformation
            transformed, lambda_value = yeojohnson(data)
            details['lambda'] = float(lambda_value)
            
            # Calculate statistics
            details['original_mean'] = float(np.mean(data))
            details['original_std'] = float(np.std(data))
            details['transformed_mean'] = float(np.mean(transformed))
            details['transformed_std'] = float(np.std(transformed))
            details['original_skewness'] = float(stats.skew(data))
            details['transformed_skewness'] = float(stats.skew(transformed))
            
        except Exception as e:
            details['error'] = f"Yeo-Johnson transformation failed: {str(e)}"
            details['success'] = False
            return None, details
        
        return transformed, details
    
    def _standardize_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Apply standardization (z-score normalization)."""
        # Calculate mean and std
        mean_val = np.mean(data)
        std_val = np.std(data)
        
        if std_val == 0:
            details['error'] = "Cannot standardize: standard deviation is zero"
            details['success'] = False
            return None, details
        
        # Apply standardization
        transformed = (data - mean_val) / std_val
        
        # Calculate statistics
        details['original_mean'] = float(mean_val)
        details['original_std'] = float(std_val)
        details['transformed_mean'] = float(np.mean(transformed))
        details['transformed_std'] = float(np.std(transformed))
        details['original_skewness'] = float(stats.skew(data))
        details['transformed_skewness'] = float(stats.skew(transformed))
        
        return transformed, details
    
    def _minmax_transformation(self, data: np.ndarray, details: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Apply min-max scaling."""
        # Calculate min and max
        min_val = np.min(data)
        max_val = np.max(data)
        
        if max_val == min_val:
            details['error'] = "Cannot scale: min and max values are equal"
            details['success'] = False
            return None, details
        
        # Apply min-max scaling
        transformed = (data - min_val) / (max_val - min_val)
        
        # Calculate statistics
        details['original_min'] = float(min_val)
        details['original_max'] = float(max_val)
        details['transformed_min'] = float(np.min(transformed))
        details['transformed_max'] = float(np.max(transformed))
        details['original_skewness'] = float(stats.skew(data))
        details['transformed_skewness'] = float(stats.skew(transformed))
        
        return transformed, details
    
    def compare_transformations(self, original_data: pd.DataFrame, 
                              transformation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare original data with transformed data.
        
        Args:
            original_data: Original DataFrame
            transformation_results: Results from transform_data method
            
        Returns:
            Dictionary with comparison statistics
        """
        transformed_data = transformation_results['transformed_data']
        transformation_details = transformation_results['transformation_details']
        
        comparison = {}
        
        for col, details in transformation_details.items():
            if col not in original_data.columns:
                continue
            
            original_col = original_data[col].dropna()
            col_comparison = {}
            
            for transformation, trans_details in details.items():
                if not trans_details.get('success', False):
                    continue
                
                new_col_name = f"{col}_{transformation}"
                if new_col_name not in transformed_data.columns:
                    continue
                
                transformed_col = transformed_data[new_col_name].dropna()
                
                # Calculate comparison statistics
                col_comparison[transformation] = {
                    'original_stats': {
                        'mean': float(np.mean(original_col)),
                        'std': float(np.std(original_col)),
                        'skewness': float(stats.skew(original_col)),
                        'kurtosis': float(stats.kurtosis(original_col)),
                        'min': float(np.min(original_col)),
                        'max': float(np.max(original_col))
                    },
                    'transformed_stats': {
                        'mean': float(np.mean(transformed_col)),
                        'std': float(np.std(transformed_col)),
                        'skewness': float(stats.skew(transformed_col)),
                        'kurtosis': float(stats.kurtosis(transformed_col)),
                        'min': float(np.min(transformed_col)),
                        'max': float(np.max(transformed_col))
                    },
                    'improvement': {
                        'skewness_improvement': abs(stats.skew(original_col)) - abs(stats.skew(transformed_col)),
                        'kurtosis_improvement': abs(stats.kurtosis(original_col)) - abs(stats.kurtosis(transformed_col))
                    }
                }
            
            comparison[col] = col_comparison
        
        return comparison
    
    def get_transformation_summary(self, transformation_results: Dict[str, Any]) -> str:
        """
        Generate a summary report of transformations.
        
        Args:
            transformation_results: Results from transform_data method
            
        Returns:
            Formatted summary report string
        """
        report = []
        report.append("=" * 80)
        report.append("DATA TRANSFORMATION SUMMARY")
        report.append("=" * 80)
        
        transformation_details = transformation_results.get('transformation_details', {})
        
        for col, details in transformation_details.items():
            report.append(f"Column: {col}")
            report.append("-" * 40)
            
            for transformation, trans_details in details.items():
                if not trans_details.get('success', False):
                    report.append(f"  {transformation}: FAILED - {trans_details.get('error', 'Unknown error')}")
                    continue
                
                report.append(f"  {transformation}:")
                report.append(f"    Original Mean: {trans_details.get('original_mean', 0):.4f}")
                report.append(f"    Transformed Mean: {trans_details.get('transformed_mean', 0):.4f}")
                report.append(f"    Original Skewness: {trans_details.get('original_skewness', 0):.4f}")
                report.append(f"    Transformed Skewness: {trans_details.get('transformed_skewness', 0):.4f}")
                
                if 'lambda' in trans_details:
                    report.append(f"    Lambda: {trans_details['lambda']:.4f}")
                
                if 'shift_constant' in trans_details and trans_details['shift_constant'] > 0:
                    report.append(f"    Shift Constant: {trans_details['shift_constant']:.4f}")
                
                if 'note' in trans_details:
                    report.append(f"    Note: {trans_details['note']}")
                
                report.append("")
        
        return "\n".join(report)
