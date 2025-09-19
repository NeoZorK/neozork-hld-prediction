"""
Cleaning Procedures Module

This module implements seven different data cleaning procedures:
1. Time Series Gaps Detection
2. Duplicates Detection
3. NaN Values Detection
4. Zero Values Detection
5. Negative Values Detection
6. Infinity Values Detection
7. Outliers Detection

Each procedure can detect issues and fix them automatically.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from scipy import stats
from sklearn.ensemble import IsolationForest


class CleaningProcedures:
    """Implements various data cleaning procedures for financial time series."""
    
    def __init__(self):
        """Initialize the cleaning procedures."""
        self.logger = logging.getLogger(__name__)
    
    def detect_gaps(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect gaps in time series data.
        
        Args:
            data: DataFrame with time series data
            
        Returns:
            List of gap information dictionaries
        """
        gaps = []
        
        # Find datetime columns
        datetime_cols = self._find_datetime_columns(data)
        
        if not datetime_cols:
            return gaps
        
        for col in datetime_cols:
            try:
                # Convert to datetime
                dates = pd.to_datetime(data[col], errors='coerce')
                valid_dates = dates.dropna().sort_values()
                
                if len(valid_dates) < 2:
                    continue
                
                # Calculate expected frequency
                time_diffs = valid_dates.diff().dropna()
                if len(time_diffs) == 0:
                    continue
                
                # Use median as expected frequency
                expected_freq = time_diffs.median()
                
                # Check if expected_freq is valid (not zero or NaN)
                if pd.isna(expected_freq) or expected_freq.total_seconds() == 0:
                    continue
                
                # Find gaps
                for i in range(1, len(valid_dates)):
                    actual_diff = valid_dates.iloc[i] - valid_dates.iloc[i-1]
                    if actual_diff > expected_freq * 1.5:  # 50% tolerance
                        gaps.append({
                            'column': col,
                            'gap_start': valid_dates.iloc[i-1],
                            'gap_end': valid_dates.iloc[i],
                            'gap_duration': actual_diff,
                            'expected_duration': expected_freq,
                            'gap_size': actual_diff / expected_freq
                        })
            except Exception as e:
                self.logger.warning(f"Error detecting gaps in column {col}: {e}")
        
        return gaps
    
    def detect_duplicates(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect duplicate rows in the data.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of duplicate information dictionaries
        """
        duplicates = []
        
        # Find exact duplicates
        duplicate_mask = data.duplicated(keep=False)
        duplicate_indices = data[duplicate_mask].index.tolist()
        
        if len(duplicate_indices) > 0:
            # Group duplicates
            duplicate_groups = {}
            for idx in duplicate_indices:
                row_hash = hash(tuple(data.loc[idx].values))
                if row_hash not in duplicate_groups:
                    duplicate_groups[row_hash] = []
                duplicate_groups[row_hash].append(idx)
            
            for group in duplicate_groups.values():
                if len(group) > 1:
                    duplicates.append({
                        'indices': group,
                        'count': len(group),
                        'sample_data': data.loc[group[0]].to_dict()
                    })
        
        return duplicates
    
    def detect_nan(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect NaN values in the data.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of NaN information dictionaries
        """
        nan_issues = []
        
        for col in data.columns:
            nan_count = data[col].isna().sum()
            if nan_count > 0:
                nan_indices = data[data[col].isna()].index.tolist()
                nan_issues.append({
                    'column': col,
                    'count': nan_count,
                    'percentage': (nan_count / len(data)) * 100,
                    'indices': nan_indices[:10],  # First 10 indices
                    'total_indices': len(nan_indices)
                })
        
        return nan_issues
    
    def detect_zeros(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect zero values in numeric columns.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of zero values information dictionaries
        """
        zero_issues = []
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            zero_count = (data[col] == 0).sum()
            if zero_count > 0:
                zero_indices = data[data[col] == 0].index.tolist()
                zero_issues.append({
                    'column': col,
                    'count': zero_count,
                    'percentage': (zero_count / len(data)) * 100,
                    'indices': zero_indices[:10],  # First 10 indices
                    'total_indices': len(zero_indices),
                    'warning': 'Some financial data may legitimately contain zero values'
                })
        
        return zero_issues
    
    def detect_negative(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect negative values in numeric columns.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of negative values information dictionaries
        """
        negative_issues = []
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            negative_count = (data[col] < 0).sum()
            if negative_count > 0:
                negative_indices = data[data[col] < 0].index.tolist()
                negative_issues.append({
                    'column': col,
                    'count': negative_count,
                    'percentage': (negative_count / len(data)) * 100,
                    'indices': negative_indices[:10],  # First 10 indices
                    'total_indices': len(negative_indices),
                    'warning': 'Some financial data may legitimately contain negative values (e.g., returns, changes)'
                })
        
        return negative_issues
    
    def detect_infinity(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect infinite values in numeric columns.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of infinity values information dictionaries
        """
        infinity_issues = []
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            inf_count = np.isinf(data[col]).sum()
            if inf_count > 0:
                inf_indices = data[np.isinf(data[col])].index.tolist()
                infinity_issues.append({
                    'column': col,
                    'count': inf_count,
                    'percentage': (inf_count / len(data)) * 100,
                    'indices': inf_indices[:10],  # First 10 indices
                    'total_indices': len(inf_indices)
                })
        
        return infinity_issues
    
    def detect_outliers(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect outliers in numeric columns using multiple methods.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of outliers information dictionaries
        """
        outliers = []
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            col_data = data[col].dropna()
            if len(col_data) < 10:  # Need sufficient data for outlier detection
                continue
            
            outlier_info = {
                'column': col,
                'methods': {}
            }
            
            # Method 1: IQR (Interquartile Range)
            try:
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                iqr_outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                outlier_info['methods']['IQR'] = {
                    'count': len(iqr_outliers),
                    'indices': iqr_outliers.index.tolist()[:10],
                    'total_indices': len(iqr_outliers)
                }
            except Exception as e:
                self.logger.warning(f"Error in IQR outlier detection for {col}: {e}")
            
            # Method 2: Z-Score
            try:
                z_scores = np.abs(stats.zscore(col_data))
                z_outliers = col_data[z_scores > 3]
                outlier_info['methods']['Z-Score'] = {
                    'count': len(z_outliers),
                    'indices': z_outliers.index.tolist()[:10],
                    'total_indices': len(z_outliers)
                }
            except Exception as e:
                self.logger.warning(f"Error in Z-Score outlier detection for {col}: {e}")
            
            # Method 3: Isolation Forest
            try:
                if len(col_data) > 20:  # Need sufficient data for Isolation Forest
                    iso_forest = IsolationForest(contamination=0.1, random_state=42)
                    outlier_labels = iso_forest.fit_predict(col_data.values.reshape(-1, 1))
                    iso_outliers = col_data[outlier_labels == -1]
                    outlier_info['methods']['Isolation Forest'] = {
                        'count': len(iso_outliers),
                        'indices': iso_outliers.index.tolist()[:10],
                        'total_indices': len(iso_outliers)
                    }
            except Exception as e:
                self.logger.warning(f"Error in Isolation Forest outlier detection for {col}: {e}")
            
            # Only add if any method found outliers
            if any(method['count'] > 0 for method in outlier_info['methods'].values()):
                outliers.append(outlier_info)
        
        return outliers
    
    def fix_issues(self, data: pd.DataFrame, procedure: str, issues: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Fix detected issues based on the procedure type.
        
        Args:
            data: DataFrame to fix
            procedure: Type of procedure (gaps, duplicates, nan, etc.)
            issues: List of detected issues
            
        Returns:
            Fixed DataFrame
        """
        fixed_data = data.copy()
        
        if procedure == 'gaps':
            fixed_data = self._fix_gaps(fixed_data, issues)
        elif procedure == 'duplicates':
            fixed_data = self._fix_duplicates(fixed_data, issues)
        elif procedure == 'nan':
            fixed_data = self._fix_nan(fixed_data, issues)
        elif procedure == 'zeros':
            fixed_data = self._fix_zeros(fixed_data, issues)
        elif procedure == 'negative':
            fixed_data = self._fix_negative(fixed_data, issues)
        elif procedure == 'infinity':
            fixed_data = self._fix_infinity(fixed_data, issues)
        elif procedure == 'outliers':
            fixed_data = self._fix_outliers(fixed_data, issues)
        
        return fixed_data
    
    def _fix_gaps(self, data: pd.DataFrame, gaps: List[Dict[str, Any]]) -> pd.DataFrame:
        """Fix time series gaps by interpolation."""
        # For now, just return the data as-is
        # Gap fixing would require more complex logic based on data type
        return data
    
    def _fix_duplicates(self, data: pd.DataFrame, duplicates: List[Dict[str, Any]]) -> pd.DataFrame:
        """Remove duplicate rows."""
        return data.drop_duplicates()
    
    def _fix_nan(self, data: pd.DataFrame, nan_issues: List[Dict[str, Any]]) -> pd.DataFrame:
        """Fix NaN values using forward fill, then backward fill."""
        fixed_data = data.copy()
        
        for issue in nan_issues:
            col = issue['column']
            # Forward fill first, then backward fill
            fixed_data[col] = fixed_data[col].ffill().bfill()
        
        return fixed_data
    
    def _fix_zeros(self, data: pd.DataFrame, zero_issues: List[Dict[str, Any]]) -> pd.DataFrame:
        """Replace zeros with NaN for further processing."""
        fixed_data = data.copy()
        
        for issue in zero_issues:
            col = issue['column']
            # Replace zeros with NaN
            fixed_data[col] = fixed_data[col].replace(0, np.nan)
        
        return fixed_data
    
    def _fix_negative(self, data: pd.DataFrame, negative_issues: List[Dict[str, Any]]) -> pd.DataFrame:
        """Replace negative values with NaN for further processing."""
        fixed_data = data.copy()
        
        for issue in negative_issues:
            col = issue['column']
            # Replace negative values with NaN
            fixed_data[col] = fixed_data[col].where(fixed_data[col] >= 0, np.nan)
        
        return fixed_data
    
    def _fix_infinity(self, data: pd.DataFrame, infinity_issues: List[Dict[str, Any]]) -> pd.DataFrame:
        """Replace infinite values with NaN."""
        fixed_data = data.copy()
        
        for issue in infinity_issues:
            col = issue['column']
            # Replace infinite values with NaN
            fixed_data[col] = fixed_data[col].replace([np.inf, -np.inf], np.nan)
        
        return fixed_data
    
    def _fix_outliers(self, data: pd.DataFrame, outliers: List[Dict[str, Any]]) -> pd.DataFrame:
        """Replace outliers with NaN."""
        fixed_data = data.copy()
        
        for outlier_info in outliers:
            col = outlier_info['column']
            
            # Use IQR method for fixing
            if 'IQR' in outlier_info['methods']:
                col_data = fixed_data[col].dropna()
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Replace outliers with NaN
                fixed_data[col] = fixed_data[col].where(
                    (fixed_data[col] >= lower_bound) & (fixed_data[col] <= upper_bound),
                    np.nan
                )
        
        return fixed_data
    
    def _find_datetime_columns(self, data: pd.DataFrame) -> List[str]:
        """Find columns that contain datetime data."""
        datetime_cols = []
        
        for col in data.columns:
            col_lower = col.lower()
            
            # Skip obvious numeric columns
            if col_lower in ['open', 'high', 'low', 'close', 'volume', 'hl', 'pressure', 'pv', 'pprice1', 'pprice2']:
                continue
            
            # Check for datetime keywords in column name
            if any(keyword in col_lower for keyword in ['time', 'date', 'timestamp', 'datetime']):
                datetime_cols.append(col)
            elif data[col].dtype in ['datetime64[ns]', 'datetime64[ns, UTC]']:
                datetime_cols.append(col)
            else:
                # Try to detect if column contains datetime strings
                try:
                    sample = data[col].dropna().head(5)
                    if len(sample) > 0:
                        # Check if it's already a datetime index
                        if isinstance(data.index, pd.DatetimeIndex):
                            continue
                        # Try to parse as datetime
                        pd.to_datetime(sample.iloc[0])
                        datetime_cols.append(col)
                except Exception:
                    pass
        
        return datetime_cols
