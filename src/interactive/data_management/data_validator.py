# -*- coding: utf-8 -*-
"""
Data Validator for NeoZork Interactive ML Trading Strategy Development.

This module handles data validation and quality checks.
"""

import pandas as pd
import numpy as np
import time
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

class DataValidator:
    """
    Data validator for comprehensive data quality checks.
    
    Features:
    - Data type validation
    - Range validation
    - Missing data detection
    - Outlier detection
    - Data consistency checks
    - Schema validation
    """
    
    def __init__(self):
        """Initialize the data validator."""
        self.validation_rules = {}
        self.quality_metrics = {}
    
    def validate_data(self, data: pd.DataFrame, validation_type: str = "basic") -> Dict[str, Any]:
        """
        Validate data according to specified validation type.
        
        Args:
            data: DataFrame to validate
            validation_type: Type of validation to perform
            
        Returns:
            Dictionary containing validation results
        """
        try:
            validation_results = {
                "validation_type": validation_type,
                "data_shape": data.shape,
                "columns": list(data.columns),
                "dtypes": data.dtypes.to_dict(),
                "missing_values": data.isnull().sum().to_dict(),
                "duplicate_rows": data.duplicated().sum(),
                "memory_usage": data.memory_usage(deep=True).sum(),
                "validation_time": time.time()
            }
            
            # Basic validation
            if validation_type == "basic":
                validation_results.update({
                    "total_rows": len(data),
                    "total_columns": len(data.columns),
                    "missing_percentage": (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100,
                    "duplicate_percentage": (data.duplicated().sum() / len(data)) * 100
                })
            
            # Advanced validation
            elif validation_type == "advanced":
                validation_results.update({
                    "numeric_columns": list(data.select_dtypes(include=[np.number]).columns),
                    "categorical_columns": list(data.select_dtypes(include=['object']).columns),
                    "datetime_columns": list(data.select_dtypes(include=['datetime64']).columns),
                    "outliers_detected": self._detect_outliers_basic(data),
                    "data_quality_score": self._calculate_quality_score(data)
                })
            
            result = {
                "status": "success",
                "validation_results": validation_results,
                "message": f"Data validation completed successfully for {validation_type} validation"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Data validation failed: {str(e)}"}
    
    def check_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Check overall data quality.
        
        Args:
            data: DataFrame to check
            
        Returns:
            Dictionary containing quality metrics
        """
        try:
            # Calculate quality metrics
            quality_metrics = {
                "completeness": 1 - (data.isnull().sum().sum() / (len(data) * len(data.columns))),
                "uniqueness": 1 - (data.duplicated().sum() / len(data)),
                "consistency": self._calculate_consistency_score(data),
                "accuracy": self._calculate_accuracy_score(data),
                "overall_score": 0.0
            }
            
            # Calculate overall score
            quality_metrics["overall_score"] = np.mean([
                quality_metrics["completeness"],
                quality_metrics["uniqueness"],
                quality_metrics["consistency"],
                quality_metrics["accuracy"]
            ])
            
            result = {
                "status": "success",
                "quality_metrics": quality_metrics,
                "data_shape": data.shape,
                "message": "Data quality check completed successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Data quality check failed: {str(e)}"}
    
    def detect_outliers(self, data: pd.DataFrame, method: str = "iqr") -> Dict[str, Any]:
        """
        Detect outliers in the data.
        
        Args:
            data: DataFrame to analyze
            method: Method for outlier detection
            
        Returns:
            Dictionary containing outlier information
        """
        try:
            numeric_data = data.select_dtypes(include=[np.number])
            outliers = {}
            
            for column in numeric_data.columns:
                if method == "iqr":
                    Q1 = numeric_data[column].quantile(0.25)
                    Q3 = numeric_data[column].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers[column] = ((numeric_data[column] < lower_bound) | (numeric_data[column] > upper_bound)).sum()
                elif method == "zscore":
                    z_scores = np.abs((numeric_data[column] - numeric_data[column].mean()) / numeric_data[column].std())
                    outliers[column] = (z_scores > 3).sum()
                else:
                    outliers[column] = 0
            
            total_outliers = sum(outliers.values())
            outlier_percentage = (total_outliers / (len(data) * len(numeric_data.columns))) * 100
            
            result = {
                "status": "success",
                "method": method,
                "outliers_per_column": outliers,
                "total_outliers": total_outliers,
                "outlier_percentage": outlier_percentage,
                "message": f"Outlier detection completed using {method} method"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Outlier detection failed: {str(e)}"}
    
    def _detect_outliers_basic(self, data: pd.DataFrame) -> int:
        """Basic outlier detection for validation."""
        try:
            numeric_data = data.select_dtypes(include=[np.number])
            total_outliers = 0
            
            for column in numeric_data.columns:
                Q1 = numeric_data[column].quantile(0.25)
                Q3 = numeric_data[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = ((numeric_data[column] < lower_bound) | (numeric_data[column] > upper_bound)).sum()
                total_outliers += outliers
            
            return total_outliers
        except:
            return 0
    
    def _calculate_quality_score(self, data: pd.DataFrame) -> float:
        """Calculate overall data quality score."""
        try:
            completeness = 1 - (data.isnull().sum().sum() / (len(data) * len(data.columns)))
            uniqueness = 1 - (data.duplicated().sum() / len(data))
            return (completeness + uniqueness) / 2
        except:
            return 0.0
    
    def _calculate_consistency_score(self, data: pd.DataFrame) -> float:
        """Calculate data consistency score."""
        try:
            # Simple consistency check based on data types
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            categorical_cols = data.select_dtypes(include=['object']).columns
            
            # Check for mixed types in columns
            consistency_score = 1.0
            for col in data.columns:
                if data[col].dtype == 'object':
                    # Check if column contains only numeric strings
                    try:
                        pd.to_numeric(data[col], errors='raise')
                        consistency_score -= 0.1  # Penalty for mixed types
                    except:
                        pass
            
            return max(0.0, consistency_score)
        except:
            return 0.5
    
    def _calculate_accuracy_score(self, data: pd.DataFrame) -> float:
        """Calculate data accuracy score."""
        try:
            # Simple accuracy check based on reasonable value ranges
            numeric_data = data.select_dtypes(include=[np.number])
            accuracy_score = 1.0
            
            for column in numeric_data.columns:
                # Check for infinite values
                if np.isinf(numeric_data[column]).any():
                    accuracy_score -= 0.1
                
                # Check for extremely large values (potential errors)
                if numeric_data[column].abs().max() > 1e10:
                    accuracy_score -= 0.05
            
            return max(0.0, accuracy_score)
        except:
            return 0.5
    
    def validate_schema(self, data: pd.DataFrame, expected_schema: Dict[str, str]) -> bool:
        """
        Validate data schema against expected schema.
        
        Args:
            data: DataFrame to validate
            expected_schema: Expected column types
            
        Returns:
            True if schema is valid, False otherwise
        """
        print_warning("This feature will be implemented in the next phase...")
        return False
