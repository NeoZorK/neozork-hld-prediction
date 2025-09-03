# -*- coding: utf-8 -*-
# src/batch_eda/outlier_handler.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outlier Handler Module for NeoZorK HLD Prediction

This module provides comprehensive outlier detection and treatment methods
with safety features including backup creation and validation.

Author: NeoZorK HLD Prediction Team
"""

import pandas as pd
import numpy as np
import shutil
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OutlierHandler:
    """
    Comprehensive outlier detection and treatment handler.
    
    Provides multiple methods for outlier detection and treatment with
    safety features including backup creation and validation.
    """
    
    def __init__(self, data: pd.DataFrame, backup_dir: str = "../data/backups"):
        """
        Initialize the outlier handler.
        
        Args:
            data: Input DataFrame
            backup_dir: Directory for backup files
        """
        self.original_data = data.copy()
        self.current_data = data.copy()
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.treatment_history = []
        
    def create_backup(self, suffix: str = "") -> str:
        """
        Create a backup of current data.
        
        Args:
            suffix: Optional suffix for backup filename
            
        Returns:
            Path to backup file
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_filename = f"outlier_backup_{timestamp}{suffix}.parquet"
        backup_path = self.backup_dir / backup_filename
        
        try:
            self.current_data.to_parquet(backup_path)
            logger.info(f"✅ Backup created: {backup_path}")
            return str(backup_path)
        except Exception as e:
            logger.error(f"❌ Failed to create backup: {e}")
            raise
    
    def detect_outliers_iqr(self, column: str, multiplier: float = 1.5) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Detect outliers using IQR method.
        
        Args:
            column: Column name to analyze
            multiplier: IQR multiplier (default 1.5)
            
        Returns:
            Tuple of (outlier_mask, statistics)
        """
        data = self.current_data[column].dropna()
        
        if len(data) == 0:
            return pd.Series([False] * len(self.current_data)), {}
        
        # Check if data is numeric
        if not pd.api.types.is_numeric_dtype(data):
            logger.warning(f"⚠️  Column {column} is not numeric, skipping outlier detection")
            return pd.Series([False] * len(self.current_data)), {}
        
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        
        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr
        
        outlier_mask = (self.current_data[column] < lower_bound) | (self.current_data[column] > upper_bound)
        
        stats = {
            'q1': q1,
            'q3': q3,
            'iqr': iqr,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outlier_count': outlier_mask.sum(),
            'outlier_percentage': (outlier_mask.sum() / len(self.current_data)) * 100
        }
        
        return outlier_mask, stats
    
    def detect_outliers_zscore(self, column: str, threshold: float = 3.0) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Detect outliers using Z-score method.
        
        Args:
            column: Column name to analyze
            threshold: Z-score threshold (default 3.0)
            
        Returns:
            Tuple of (outlier_mask, statistics)
        """
        data = self.current_data[column].dropna()
        
        if len(data) == 0:
            return pd.Series([False] * len(self.current_data)), {}
        
        z_scores = np.abs((data - data.mean()) / data.std())
        outlier_mask = z_scores > threshold
        
        # Map back to original DataFrame indices
        full_mask = pd.Series([False] * len(self.current_data), index=self.current_data.index)
        full_mask.loc[data.index] = outlier_mask
        
        stats = {
            'mean': data.mean(),
            'std': data.std(),
            'threshold': threshold,
            'outlier_count': outlier_mask.sum(),
            'outlier_percentage': (outlier_mask.sum() / len(data)) * 100
        }
        
        return full_mask, stats
    
    def detect_outliers_isolation_forest(self, columns: List[str], contamination: float = 0.1) -> Tuple[pd.Series, Dict[str, Any]]:
        """
        Detect outliers using Isolation Forest.
        
        Args:
            columns: List of columns to analyze
            contamination: Expected proportion of outliers
            
        Returns:
            Tuple of (outlier_mask, statistics)
        """
        try:
            from sklearn.ensemble import IsolationForest
            
            # Select numeric columns
            numeric_data = self.current_data[columns].select_dtypes(include=[np.number])
            
            if numeric_data.empty:
                return pd.Series([False] * len(self.current_data)), {}
            
            # Handle missing values
            numeric_data_clean = numeric_data.dropna()
            
            if len(numeric_data_clean) == 0:
                return pd.Series([False] * len(self.current_data)), {}
            
            # Fit isolation forest
            iso_forest = IsolationForest(contamination=contamination, random_state=42)
            predictions = iso_forest.fit_predict(numeric_data_clean)
            
            # Create outlier mask (predictions of -1 indicate outliers)
            outlier_mask = predictions == -1
            
            # Map back to original DataFrame indices
            full_mask = pd.Series([False] * len(self.current_data), index=self.current_data.index)
            full_mask.loc[numeric_data_clean.index] = outlier_mask
            
            stats = {
                'contamination': contamination,
                'outlier_count': outlier_mask.sum(),
                'outlier_percentage': (outlier_mask.sum() / len(numeric_data_clean)) * 100,
                'columns_analyzed': list(numeric_data.columns)
            }
            
            return full_mask, stats
            
        except ImportError:
            logger.warning("⚠️  scikit-learn not available, skipping Isolation Forest")
            return pd.Series([False] * len(self.current_data)), {}
    
    def treat_outliers_removal(self, columns: List[str], method: str = 'iqr', **kwargs) -> Dict[str, Any]:
        """
        Remove outliers from specified columns.
        
        Args:
            columns: List of columns to treat
            method: Detection method ('iqr', 'zscore', 'isolation_forest')
            **kwargs: Additional parameters for detection method
            
        Returns:
            Treatment results
        """
        backup_path = self.create_backup("_before_removal")
        
        results = {
            'method': 'removal',
            'detection_method': method,
            'columns_treated': columns,
            'backup_path': backup_path,
            'rows_removed': 0,
            'details': {}
        }
        
        total_rows_before = len(self.current_data)
        
        for column in columns:
            if column not in self.current_data.columns:
                logger.warning(f"⚠️  Column {column} not found, skipping")
                continue
            
            # Detect outliers
            if method == 'iqr':
                outlier_mask, stats = self.detect_outliers_iqr(column, **kwargs)
            elif method == 'zscore':
                outlier_mask, stats = self.detect_outliers_zscore(column, **kwargs)
            elif method == 'isolation_forest':
                outlier_mask, stats = self.detect_outliers_isolation_forest([column], **kwargs)
            else:
                logger.error(f"❌ Unknown method: {method}")
                continue
            
            # Remove outliers
            rows_to_remove = outlier_mask.sum()
            if rows_to_remove > 0:
                self.current_data = self.current_data[~outlier_mask]
                results['details'][column] = {
                    'outliers_removed': rows_to_remove,
                    'percentage_removed': (rows_to_remove / total_rows_before) * 100,
                    'detection_stats': stats
                }
                logger.info(f"✅ Removed {rows_to_remove} outliers from {column}")
        
        results['rows_removed'] = total_rows_before - len(self.current_data)
        self.treatment_history.append(results)
        
        return results
    
    def treat_outliers_capping(self, columns: List[str], method: str = 'iqr', 
                              cap_method: str = 'percentile', **kwargs) -> Dict[str, Any]:
        """
        Cap outliers to specified bounds.
        
        Args:
            columns: List of columns to treat
            method: Detection method ('iqr', 'zscore')
            cap_method: Capping method ('percentile', 'iqr', 'manual')
            **kwargs: Additional parameters
            
        Returns:
            Treatment results
        """
        backup_path = self.create_backup("_before_capping")
        
        results = {
            'method': 'capping',
            'detection_method': method,
            'cap_method': cap_method,
            'columns_treated': columns,
            'backup_path': backup_path,
            'values_capped': 0,
            'details': {}
        }
        
        for column in columns:
            if column not in self.current_data.columns:
                logger.warning(f"⚠️  Column {column} not found, skipping")
                continue
            
            # Detect outliers
            if method == 'iqr':
                # Filter out manual capping parameters
                detection_kwargs = {k: v for k, v in kwargs.items() 
                                  if k not in ['lower_cap', 'upper_cap']}
                outlier_mask, stats = self.detect_outliers_iqr(column, **detection_kwargs)
            elif method == 'zscore':
                outlier_mask, stats = self.detect_outliers_zscore(column, **kwargs)
            else:
                logger.error(f"❌ Method {method} not supported for capping")
                continue
            
            # Determine cap values
            if cap_method == 'percentile':
                lower_cap = self.current_data[column].quantile(0.01)  # 1st percentile
                upper_cap = self.current_data[column].quantile(0.99)  # 99th percentile
            elif cap_method == 'iqr':
                lower_cap = stats['lower_bound']
                upper_cap = stats['upper_bound']
            elif cap_method == 'manual':
                lower_cap = kwargs.get('lower_cap', stats['lower_bound'])
                upper_cap = kwargs.get('upper_cap', stats['upper_bound'])
            else:
                logger.error(f"❌ Unknown cap method: {cap_method}")
                continue
            
            # Apply capping
            values_capped = 0
            if outlier_mask.sum() > 0:
                # Cap lower outliers
                lower_outliers = (self.current_data[column] < lower_cap) & outlier_mask
                self.current_data.loc[lower_outliers, column] = lower_cap
                values_capped += lower_outliers.sum()
                
                # Cap upper outliers
                upper_outliers = (self.current_data[column] > upper_cap) & outlier_mask
                self.current_data.loc[upper_outliers, column] = upper_cap
                values_capped += upper_outliers.sum()
            
            results['details'][column] = {
                'values_capped': values_capped,
                'lower_cap': lower_cap,
                'upper_cap': upper_cap,
                'detection_stats': stats
            }
            
            if values_capped > 0:
                logger.info(f"✅ Capped {values_capped} outliers in {column}")
        
        results['values_capped'] = sum(detail['values_capped'] for detail in results['details'].values())
        self.treatment_history.append(results)
        
        return results
    
    def treat_outliers_winsorization(self, columns: List[str], limits: Tuple[float, float] = (0.05, 0.05)) -> Dict[str, Any]:
        """
        Apply winsorization to specified columns.
        
        Args:
            columns: List of columns to treat
            limits: Tuple of (lower_limit, upper_limit) as fractions
            
        Returns:
            Treatment results
        """
        backup_path = self.create_backup("_before_winsorization")
        
        results = {
            'method': 'winsorization',
            'limits': limits,
            'columns_treated': columns,
            'backup_path': backup_path,
            'details': {}
        }
        
        for column in columns:
            if column not in self.current_data.columns:
                logger.warning(f"⚠️  Column {column} not found, skipping")
                continue
            
            # Calculate limits
            lower_limit = self.current_data[column].quantile(limits[0])
            upper_limit = self.current_data[column].quantile(1 - limits[1])
            
            # Apply winsorization
            values_changed = 0
            
            # Lower winsorization
            lower_mask = self.current_data[column] < lower_limit
            self.current_data.loc[lower_mask, column] = lower_limit
            values_changed += lower_mask.sum()
            
            # Upper winsorization
            upper_mask = self.current_data[column] > upper_limit
            self.current_data.loc[upper_mask, column] = upper_limit
            values_changed += upper_mask.sum()
            
            results['details'][column] = {
                'values_changed': values_changed,
                'lower_limit': lower_limit,
                'upper_limit': upper_limit
            }
            
            if values_changed > 0:
                logger.info(f"✅ Winsorized {values_changed} values in {column}")
        
        self.treatment_history.append(results)
        
        return results
    
    def validate_treatment(self) -> Dict[str, Any]:
        """
        Validate the treatment results.
        
        Returns:
            Validation results
        """
        validation_results = {
            'data_integrity': True,
            'shape_changed': False,
            'missing_values': False,
            'infinite_values': False,
            'warnings': []
        }
        
        # Check data integrity
        if self.current_data is None:
            validation_results['data_integrity'] = False
            validation_results['warnings'].append("Data is None after treatment")
        
        # Check shape changes
        if len(self.current_data) != len(self.original_data):
            validation_results['shape_changed'] = True
            validation_results['warnings'].append(f"Data shape changed from {len(self.original_data)} to {len(self.current_data)} rows")
        
        # Check for missing values
        if self.current_data.isnull().any().any():
            validation_results['missing_values'] = True
            validation_results['warnings'].append("Missing values detected after treatment")
        
        # Check for infinite values
        if np.isinf(self.current_data.select_dtypes(include=[np.number])).any().any():
            validation_results['infinite_values'] = True
            validation_results['warnings'].append("Infinite values detected after treatment")
        
        return validation_results
    
    def get_treatment_summary(self) -> Dict[str, Any]:
        """
        Get summary of all treatments applied.
        
        Returns:
            Treatment summary
        """
        summary = {
            'total_treatments': len(self.treatment_history),
            'original_shape': self.original_data.shape,
            'current_shape': self.current_data.shape,
            'treatments': self.treatment_history,
            'validation': self.validate_treatment()
        }
        
        return summary
    
    def restore_from_backup(self, backup_path: str) -> bool:
        """
        Restore data from backup.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                logger.error(f"❌ Backup file not found: {backup_path}")
                return False
            
            self.current_data = pd.read_parquet(backup_path)
            logger.info(f"✅ Data restored from backup: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to restore from backup: {e}")
            return False
    
    def get_outlier_report(self, columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate comprehensive outlier report.
        
        Args:
            columns: List of columns to analyze (None for all numeric columns)
            
        Returns:
            Outlier report
        """
        if columns is None:
            columns = list(self.current_data.select_dtypes(include=[np.number]).columns)
        
        report = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'columns_analyzed': columns,
            'methods': ['iqr', 'zscore'],
            'results': {}
        }
        
        for column in columns:
            if column not in self.current_data.columns:
                continue
            
            column_report = {}
            
            # IQR method
            iqr_mask, iqr_stats = self.detect_outliers_iqr(column)
            column_report['iqr'] = {
                'outlier_count': iqr_mask.sum(),
                'outlier_percentage': (iqr_mask.sum() / len(self.current_data)) * 100,
                'bounds': {
                    'lower': iqr_stats.get('lower_bound', None),
                    'upper': iqr_stats.get('upper_bound', None)
                }
            }
            
            # Z-score method
            zscore_mask, zscore_stats = self.detect_outliers_zscore(column)
            column_report['zscore'] = {
                'outlier_count': zscore_mask.sum(),
                'outlier_percentage': (zscore_mask.sum() / len(self.current_data)) * 100,
                'threshold': zscore_stats.get('threshold', 3.0)
            }
            
            report['results'][column] = column_report
        
        return report
