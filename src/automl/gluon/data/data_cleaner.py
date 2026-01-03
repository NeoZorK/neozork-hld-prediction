#!/usr/bin/env python3
"""
Data Cleaner for AutoGluon Pipeline
clean данных for пайплайна AutoGluon

This module handles data cleaning and preprocessing to ensure
high-quality data for AutoGluon training.
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)

class DataCleaner:
 """
 Data cleaner for AutoGluon pipeline.
 clean данных for пайплайна AutoGluon.
 """

 def __init__(self):
 """Initialize data cleaner."""
 self.logger = logger

 def clean_data(self, data: pd.DataFrame, target_column: str = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
 """
 Clean data by removing infinity, NaN values, and other issues.
 Очистить данные, удалив бесконечные значения, NaN and другие проблемы.

 Args:
 data: Input dataframe
 target_column: Target column name (optional)

 Returns:
 Tuple of (cleaned_data, cleaning_report)
 """
 self.logger.info("🧹 starting data cleaning...")

 original_shape = data.shape
 cleaning_report = {
 'original_shape': original_shape,
 'original_rows': original_shape[0],
 'original_cols': original_shape[1],
 'infinity_removed': 0,
 'nan_removed': 0,
 'duplicates_removed': 0,
 'outliers_removed': 0,
 'final_shape': None,
 'final_rows': 0,
 'final_cols': 0
 }

 # start with a copy
 cleaned_data = data.copy()

 # Step 1: Remove infinity values
 self.logger.info("🔍 Step 1: Removing infinity values...")
 inf_mask = np.isinf(cleaned_data.select_dtypes(include=[np.number])).any(axis=1)
 inf_count = inf_mask.sum()
 if inf_count > 0:
 cleaned_data = cleaned_data[~inf_mask]
 cleaning_report['infinity_removed'] = inf_count
 self.logger.info(f"✅ Removed {inf_count} rows with infinity values")

 # Step 2: Handle NaN values
 self.logger.info("🔍 Step 2: Handling NaN values...")
 nan_count = cleaned_data.isnull().sum().sum()
 if nan_count > 0:
 # For numeric columns, fill with median
 numeric_cols = cleaned_data.select_dtypes(include=[np.number]).columns
 for col in numeric_cols:
 if cleaned_data[col].isnull().any():
 median_val = cleaned_data[col].median()
 cleaned_data[col].fillna(median_val, inplace=True)

 # For categorical columns, fill with mode
 categorical_cols = cleaned_data.select_dtypes(include=['object']).columns
 for col in categorical_cols:
 if cleaned_data[col].isnull().any():
 mode_val = cleaned_data[col].mode().iloc[0] if not cleaned_data[col].mode().empty else 'Unknown'
 cleaned_data[col].fillna(mode_val, inplace=True)

 cleaning_report['nan_removed'] = nan_count
 self.logger.info(f"✅ Handled {nan_count} NaN values")

 # Step 3: Remove duplicates
 self.logger.info("🔍 Step 3: Removing duplicates...")
 duplicate_count = cleaned_data.duplicated().sum()
 if duplicate_count > 0:
 cleaned_data = cleaned_data.drop_duplicates()
 cleaning_report['duplicates_removed'] = duplicate_count
 self.logger.info(f"✅ Removed {duplicate_count} duplicate rows")

 # Step 4: Remove extreme outliers (optional)
 self.logger.info("🔍 Step 4: Removing extreme outliers...")
 outlier_count = 0
 numeric_cols = cleaned_data.select_dtypes(include=[np.number]).columns

 for col in numeric_cols:
 if col == target_column:
 continue # Don't remove outliers from target column

 Q1 = cleaned_data[col].quantile(0.25)
 Q3 = cleaned_data[col].quantile(0.75)
 IQR = Q3 - Q1
 lower_bound = Q1 - 3 * IQR # More conservative than 1.5 * IQR
 upper_bound = Q3 + 3 * IQR

 outlier_mask = (cleaned_data[col] < lower_bound) | (cleaned_data[col] > upper_bound)
 if outlier_mask.any():
 outlier_count += outlier_mask.sum()
 cleaned_data = cleaned_data[~outlier_mask]

 if outlier_count > 0:
 cleaning_report['outliers_removed'] = outlier_count
 self.logger.info(f"✅ Removed {outlier_count} extreme outliers")

 # Step 5: Ensure data types are appropriate
 self.logger.info("🔍 Step 5: Ensuring appropriate data types...")
 for col in cleaned_data.columns:
 if cleaned_data[col].dtype == 'object':
 # Try to convert to numeric if possible
 try:
 cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='ignore')
 except:
 pass

 # Final report
 final_shape = cleaned_data.shape
 cleaning_report['final_shape'] = final_shape
 cleaning_report['final_rows'] = final_shape[0]
 cleaning_report['final_cols'] = final_shape[1]

 self.logger.info(f"✅ Data cleaning completed!")
 self.logger.info(f"📊 Original: {original_shape[0]} rows, {original_shape[1]} cols")
 self.logger.info(f"📊 Final: {final_shape[0]} rows, {final_shape[1]} cols")
 self.logger.info(f"📊 Removed: {original_shape[0] - final_shape[0]} rows total")

 return cleaned_data, cleaning_report

 def validate_data(self, data: pd.DataFrame, target_column: str = None) -> Dict[str, Any]:
 """
 Validate data quality after cleaning.
 Проверить качество данных после очистки.

 Args:
 data: Dataframe to validate
 target_column: Target column name (optional)

 Returns:
 Validation report
 """
 self.logger.info("🔍 Validating data quality...")

 validation_report = {
 'has_infinity': False,
 'has_nan': False,
 'has_duplicates': False,
 'numeric_cols': 0,
 'categorical_cols': 0,
 'total_rows': len(data),
 'total_cols': len(data.columns),
 'memory_usage_mb': data.memory_usage(deep=True).sum() / 1024 / 1024
 }

 # Check for infinity
 if np.isinf(data.select_dtypes(include=[np.number])).any().any():
 validation_report['has_infinity'] = True
 self.logger.warning("⚠️ Data still contains infinity values")

 # Check for NaN
 if data.isnull().any().any():
 validation_report['has_nan'] = True
 self.logger.warning("⚠️ Data still contains NaN values")

 # Check for duplicates
 if data.duplicated().any():
 validation_report['has_duplicates'] = True
 self.logger.warning("⚠️ Data still contains duplicates")

 # Count column types
 validation_report['numeric_cols'] = len(data.select_dtypes(include=[np.number]).columns)
 validation_report['categorical_cols'] = len(data.select_dtypes(include=['object']).columns)

 # Check target column if provided
 if target_column and target_column in data.columns:
 target_info = {
 'target_unique_values': data[target_column].nunique(),
 'target_missing': data[target_column].isnull().sum(),
 'target_type': str(data[target_column].dtype)
 }
 validation_report['target_info'] = target_info

 self.logger.info(f"✅ Validation completed: {validation_report['total_rows']} rows, {validation_report['total_cols']} cols")
 self.logger.info(f"📊 Memory usage: {validation_report['memory_usage_mb']:.2f} MB")

 return validation_report
