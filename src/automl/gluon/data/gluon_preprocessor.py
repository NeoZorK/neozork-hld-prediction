# -*- coding: utf-8 -*-
"""
AutoGluon preprocessor for minimal data preparation.

This module provides minimal preprocessing wrapper for AutoGluon,
letting AutoGluon handle most of the data cleaning automatically.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
import logging
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class GluonPreprocessor:
    """Minimal preprocessor for AutoGluon integration."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Gluon preprocessor.
        
        Args:
            config: Preprocessing configuration
        """
        self.config = config or {}
        self.preprocessing_steps = []
        
    def prepare_for_gluon(self, df: pd.DataFrame, 
                         target_column: Optional[str] = None) -> pd.DataFrame:
        """
        Minimal preparation of DataFrame for AutoGluon.
        
        AutoGluon will handle most preprocessing automatically.
        This method only does essential preparations.
        
        Args:
            df: Input DataFrame
            target_column: Target column name
            
        Returns:
            Prepared DataFrame
        """
        logger.info("Preparing DataFrame for AutoGluon")
        
        # Create a copy to avoid modifying original
        prepared_df = df.copy()
        
        # Step 1: Handle duplicate columns
        prepared_df = self._handle_duplicate_columns(prepared_df)
        
        # Step 2: Basic datetime handling
        prepared_df = self._handle_datetime_columns(prepared_df)
        
        # Step 3: Handle infinite values
        prepared_df = self._handle_infinite_values(prepared_df)
        
        # Step 4: Basic type consistency
        prepared_df = self._ensure_type_consistency(prepared_df)
        
        # Step 5: Validate target column if specified
        if target_column and target_column in prepared_df.columns:
            prepared_df = self._validate_target_column(prepared_df, target_column)
        
        logger.info(f"Prepared DataFrame: {len(prepared_df)} rows, {len(prepared_df.columns)} columns")
        return prepared_df
    
    def _handle_duplicate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle duplicate column names."""
        if df.columns.duplicated().any():
            logger.warning("Found duplicate columns, renaming them")
            df.columns = pd.io.common.dedup_names(df.columns)
        return df
    
    def _handle_datetime_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle datetime columns."""
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to datetime
                try:
                    df[col] = pd.to_datetime(df[col], errors='ignore')
                except:
                    pass
        return df
    
    def _handle_infinite_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Replace infinite values with NaN."""
        df = df.replace([np.inf, -np.inf], np.nan)
        return df
    
    def _ensure_type_consistency(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure basic type consistency."""
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert numeric columns
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass
        return df
    
    def _validate_target_column(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """Validate target column."""
        if target_column not in df.columns:
            logger.error(f"Target column '{target_column}' not found in DataFrame")
            return df
        
        # Check for missing values in target
        missing_target = df[target_column].isnull().sum()
        if missing_target > 0:
            logger.warning(f"Found {missing_target} missing values in target column")
        
        # Check for constant target
        unique_targets = df[target_column].nunique()
        if unique_targets <= 1:
            logger.warning(f"Target column has only {unique_targets} unique values")
        
        return df
    
    def create_time_series_split(self, df: pd.DataFrame, 
                                train_ratio: float = 0.6,
                                val_ratio: float = 0.2,
                                test_ratio: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Create time series split for train/validation/test.
        
        Args:
            df: Input DataFrame
            train_ratio: Training set ratio
            val_ratio: Validation set ratio
            test_ratio: Test set ratio
            
        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        if not isinstance(df.index, pd.DatetimeIndex):
            logger.warning("DataFrame index is not datetime, using sequential split")
            return self._sequential_split(df, train_ratio, val_ratio, test_ratio)
        
        # Sort by datetime index
        df_sorted = df.sort_index()
        total_len = len(df_sorted)
        
        # Calculate split indices
        train_end = int(total_len * train_ratio)
        val_end = int(total_len * (train_ratio + val_ratio))
        
        # Split the data
        train_df = df_sorted.iloc[:train_end]
        val_df = df_sorted.iloc[train_end:val_end]
        test_df = df_sorted.iloc[val_end:]
        
        logger.info(f"Time series split: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
        
        return train_df, val_df, test_df
    
    def _sequential_split(self, df: pd.DataFrame, 
                         train_ratio: float, val_ratio: float, test_ratio: float) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Sequential split for non-datetime data."""
        total_len = len(df)
        train_end = int(total_len * train_ratio)
        val_end = int(total_len * (train_ratio + val_ratio))
        
        train_df = df.iloc[:train_end]
        val_df = df.iloc[train_end:val_end]
        test_df = df.iloc[val_end:]
        
        logger.info(f"Sequential split: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
        
        return train_df, val_df, test_df
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary information about the DataFrame.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Summary dictionary
        """
        summary = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
            'datetime_columns': df.select_dtypes(include=['datetime64']).columns.tolist()
        }
        
        # Add basic statistics for numeric columns
        if summary['numeric_columns']:
            summary['numeric_stats'] = df[summary['numeric_columns']].describe().to_dict()
        
        return summary
    
    def detect_data_quality_issues(self, df: pd.DataFrame) -> List[str]:
        """
        Detect potential data quality issues.
        
        Args:
            df: Input DataFrame
            
        Returns:
            List of detected issues
        """
        issues = []
        
        # Check for empty DataFrame
        if df.empty:
            issues.append("DataFrame is empty")
            return issues
        
        # Check for completely empty columns
        empty_cols = df.columns[df.isnull().all()].tolist()
        if empty_cols:
            issues.append(f"Empty columns: {empty_cols}")
        
        # Check for duplicate rows
        duplicate_rows = df.duplicated().sum()
        if duplicate_rows > 0:
            issues.append(f"Duplicate rows: {duplicate_rows}")
        
        # Check for high missing value ratio
        missing_ratio = df.isnull().sum() / len(df)
        high_missing_cols = missing_ratio[missing_ratio > 0.5].index.tolist()
        if high_missing_cols:
            issues.append(f"High missing value ratio (>50%): {high_missing_cols}")
        
        # Check for constant columns
        constant_cols = df.columns[df.nunique() <= 1].tolist()
        if constant_cols:
            issues.append(f"Constant columns: {constant_cols}")
        
        # Check for infinite values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        inf_count = np.isinf(df[numeric_cols]).sum().sum()
        if inf_count > 0:
            issues.append(f"Infinite values: {inf_count}")
        
        return issues
