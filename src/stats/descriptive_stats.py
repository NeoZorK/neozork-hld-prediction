"""
Descriptive Statistics Module

This module provides comprehensive descriptive statistics analysis for financial data.
It includes basic statistical measures, data distribution analysis, and variability metrics.

Features:
- Basic Stats: Mean, median, std, min, max, percentiles
- Data Distribution: Skewness, kurtosis analysis
- Variability Analysis: Coefficient of variation, IQR, range
- Data Points Count: Total data points and missing data percentage
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union
from scipy import stats
import logging
from .color_utils import ColorUtils


class DescriptiveStatistics:
    """Handles descriptive statistics calculations and analysis."""
    
    def __init__(self):
        """Initialize the descriptive statistics analyzer."""
        self.logger = logging.getLogger(__name__)
    
    def analyze_data(self, data: pd.DataFrame, numeric_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive descriptive statistics analysis.
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns to analyze. If None, auto-detect.
            
        Returns:
            Dictionary containing all descriptive statistics
        """
        if numeric_columns is None:
            numeric_columns = self._get_numeric_columns(data)
        
        if not numeric_columns:
            self.logger.warning("No numeric columns found for analysis")
            return {}
        
        results = {
            'overview': self._get_data_overview(data, numeric_columns),
            'basic_stats': self._calculate_basic_statistics(data, numeric_columns),
            'distribution_stats': self._calculate_distribution_statistics(data, numeric_columns),
            'variability_stats': self._calculate_variability_statistics(data, numeric_columns),
            'missing_data': self._analyze_missing_data(data, numeric_columns),
            'percentiles': self._calculate_percentiles(data, numeric_columns)
        }
        
        return results
    
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
    
    def _get_data_overview(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
        """
        Get basic data overview information.
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns
            
        Returns:
            Dictionary with overview information
        """
        return {
            'total_rows': len(data),
            'total_columns': len(data.columns),
            'numeric_columns_count': len(numeric_columns),
            'numeric_columns': numeric_columns,
            'memory_usage_mb': data.memory_usage(deep=True).sum() / (1024 * 1024),
            'data_types': data.dtypes.to_dict()
        }
    
    def _calculate_basic_statistics(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Dict[str, float]]:
        """
        Calculate basic statistical measures for each numeric column.
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns
            
        Returns:
            Dictionary with basic statistics for each column
        """
        basic_stats = {}
        
        for col in numeric_columns:
            col_data = data[col].dropna()
            
            if len(col_data) == 0:
                basic_stats[col] = {
                    'count': 0,
                    'mean': np.nan,
                    'median': np.nan,
                    'std': np.nan,
                    'min': np.nan,
                    'max': np.nan
                }
                continue
            
            basic_stats[col] = {
                'count': len(col_data),
                'mean': float(np.mean(col_data)),
                'median': float(np.median(col_data)),
                'std': float(np.std(col_data, ddof=1)),  # Sample standard deviation
                'min': float(np.min(col_data)),
                'max': float(np.max(col_data))
            }
        
        return basic_stats
    
    def _calculate_distribution_statistics(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Dict[str, float]]:
        """
        Calculate distribution-related statistics (skewness, kurtosis).
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns
            
        Returns:
            Dictionary with distribution statistics for each column
        """
        distribution_stats = {}
        
        for col in numeric_columns:
            col_data = data[col].dropna()
            
            if len(col_data) < 3:  # Need at least 3 points for skewness/kurtosis
                distribution_stats[col] = {
                    'skewness': np.nan,
                    'kurtosis': np.nan,
                    'skewness_interpretation': 'Insufficient data',
                    'kurtosis_interpretation': 'Insufficient data'
                }
                continue
            
            # Calculate skewness and kurtosis
            skewness = float(stats.skew(col_data))
            kurtosis = float(stats.kurtosis(col_data))
            
            # Interpret skewness
            if abs(skewness) < 0.5:
                skew_interpretation = "Approximately symmetric"
            elif abs(skewness) < 1.0:
                skew_interpretation = "Moderately skewed"
            else:
                skew_interpretation = "Highly skewed"
            
            if skewness > 0:
                skew_interpretation += " (right-tailed)"
            elif skewness < 0:
                skew_interpretation += " (left-tailed)"
            
            # Interpret kurtosis
            if abs(kurtosis) < 0.5:
                kurt_interpretation = "Approximately normal (mesokurtic)"
            elif kurtosis > 0.5:
                kurt_interpretation = "Heavy-tailed (leptokurtic)"
            else:
                kurt_interpretation = "Light-tailed (platykurtic)"
            
            distribution_stats[col] = {
                'skewness': skewness,
                'kurtosis': kurtosis,
                'skewness_interpretation': skew_interpretation,
                'kurtosis_interpretation': kurt_interpretation
            }
        
        return distribution_stats
    
    def _calculate_variability_statistics(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Dict[str, float]]:
        """
        Calculate variability measures for each numeric column.
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns
            
        Returns:
            Dictionary with variability statistics for each column
        """
        variability_stats = {}
        
        for col in numeric_columns:
            col_data = data[col].dropna()
            
            if len(col_data) == 0:
                variability_stats[col] = {
                    'variance': np.nan,
                    'coefficient_of_variation': np.nan,
                    'iqr': np.nan,
                    'range': np.nan,
                    'cv_interpretation': 'No data'
                }
                continue
            
            # Calculate variability measures
            variance = float(np.var(col_data, ddof=1))  # Sample variance
            mean_val = float(np.mean(col_data))
            std_val = float(np.std(col_data, ddof=1))
            
            # Coefficient of variation
            cv = (std_val / abs(mean_val)) * 100 if mean_val != 0 else np.nan
            
            # Interquartile range
            q75, q25 = np.percentile(col_data, [75, 25])
            iqr = float(q75 - q25)
            
            # Range
            range_val = float(np.max(col_data) - np.min(col_data))
            
            # Interpret coefficient of variation with color
            if np.isnan(cv):
                cv_interpretation = "Cannot calculate (mean is zero)"
            elif cv < 15:
                cv_interpretation = "Low variability"
            elif cv < 35:
                cv_interpretation = "Moderate variability"
            else:
                cv_interpretation = "High variability"
            
            variability_stats[col] = {
                'variance': variance,
                'coefficient_of_variation': cv,
                'iqr': iqr,
                'range': range_val,
                'cv_interpretation': cv_interpretation
            }
        
        return variability_stats
    
    def _analyze_missing_data(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Dict[str, Union[int, float]]]:
        """
        Analyze missing data patterns.
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns
            
        Returns:
            Dictionary with missing data analysis
        """
        missing_data = {}
        
        for col in numeric_columns:
            total_count = len(data)
            missing_count = data[col].isna().sum()
            valid_count = total_count - missing_count
            missing_percentage = (missing_count / total_count) * 100 if total_count > 0 else 0
            
            missing_data[col] = {
                'total_data_points': total_count,
                'valid_data_points': valid_count,
                'missing_data_points': missing_count,
                'missing_percentage': missing_percentage
            }
        
        return missing_data
    
    def _calculate_percentiles(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Dict[str, float]]:
        """
        Calculate various percentiles for each numeric column.
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns
            
        Returns:
            Dictionary with percentiles for each column
        """
        percentiles = {}
        percentile_values = [1, 5, 10, 25, 50, 75, 90, 95, 99]
        
        for col in numeric_columns:
            col_data = data[col].dropna()
            
            if len(col_data) == 0:
                percentiles[col] = {f'p{p}': np.nan for p in percentile_values}
                continue
            
            col_percentiles = {}
            for p in percentile_values:
                col_percentiles[f'p{p}'] = float(np.percentile(col_data, p))
            
            percentiles[col] = col_percentiles
        
        return percentiles
    
    def get_summary_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a summary report of descriptive statistics.
        
        Args:
            results: Results from analyze_data method
            
        Returns:
            Formatted summary report string
        """
        report = []
        report.append("=" * 80)
        report.append("DESCRIPTIVE STATISTICS SUMMARY")
        report.append("=" * 80)
        
        # Overview
        overview = results.get('overview', {})
        report.append(f"Total Rows: {overview.get('total_rows', 0):,}")
        report.append(f"Total Columns: {overview.get('total_columns', 0)}")
        report.append(f"Numeric Columns: {overview.get('numeric_columns_count', 0)}")
        report.append(f"Memory Usage: {overview.get('memory_usage_mb', 0):.2f} MB")
        report.append("")
        
        # Basic statistics for each column
        basic_stats = results.get('basic_stats', {})
        for col, stats in basic_stats.items():
            report.append(f"Column: {col}")
            report.append(f"  Count: {stats.get('count', 0):,}")
            report.append(f"  Mean: {stats.get('mean', 0):.4f}")
            report.append(f"  Median: {stats.get('median', 0):.4f}")
            report.append(f"  Std Dev: {stats.get('std', 0):.4f}")
            report.append(f"  Min: {stats.get('min', 0):.4f}")
            report.append(f"  Max: {stats.get('max', 0):.4f}")
            report.append("")
        
        # Distribution statistics
        dist_stats = results.get('distribution_stats', {})
        if dist_stats:
            report.append("DISTRIBUTION ANALYSIS")
            report.append("-" * 40)
            for col, stats in dist_stats.items():
                report.append(f"Column: {col}")
                report.append(f"  Skewness: {stats.get('skewness', 0):.4f} - {stats.get('skewness_interpretation', 'N/A')}")
                report.append(f"  Kurtosis: {stats.get('kurtosis', 0):.4f} - {stats.get('kurtosis_interpretation', 'N/A')}")
                report.append("")
        
        # Missing data analysis
        missing_data = results.get('missing_data', {})
        if missing_data:
            report.append("MISSING DATA ANALYSIS")
            report.append("-" * 40)
            for col, stats in missing_data.items():
                report.append(f"Column: {col}")
                report.append(f"  Valid Data Points: {stats.get('valid_data_points', 0):,}")
                report.append(f"  Missing Data Points: {stats.get('missing_data_points', 0):,}")
                report.append(f"  Missing Percentage: {stats.get('missing_percentage', 0):.2f}%")
                report.append("")
        
        return "\n".join(report)
