"""
Optimized Analysis Module for Large Datasets

This module provides optimized analysis methods for large time series datasets,
including data sampling, chunked processing, and performance optimizations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import time
import warnings
warnings.filterwarnings('ignore')


class OptimizedAnalysis:
    """Optimized analysis methods for large datasets."""
    
    def __init__(self, max_sample_size: int = 10000, chunk_size: int = 50000):
        """
        Initialize optimized analysis.
        
        Args:
            max_sample_size: Maximum number of rows to sample for analysis
            chunk_size: Size of chunks for processing large datasets
        """
        self.max_sample_size = max_sample_size
        self.chunk_size = chunk_size
    
    def get_analysis_sample(self, data: pd.DataFrame, column: str, 
                          sample_size: Optional[int] = None) -> pd.Series:
        """
        Get optimized sample for analysis.
        
        Args:
            data: Input dataframe
            column: Column name to sample
            sample_size: Custom sample size (defaults to max_sample_size)
            
        Returns:
            Sampled data series
        """
        if sample_size is None:
            sample_size = self.max_sample_size
        
        col_data = data[column].dropna()
        
        if len(col_data) <= sample_size:
            return col_data
        
        # For large datasets, use systematic sampling
        step = len(col_data) // sample_size
        sampled_indices = range(0, len(col_data), step)[:sample_size]
        return col_data.iloc[sampled_indices]
    
    def fast_adf_test(self, data: pd.Series, column_name: str) -> Dict[str, Any]:
        """
        Fast ADF test using sampling for large datasets.
        
        Args:
            data: Input data series
            column_name: Name of the column
            
        Returns:
            ADF test results
        """
        from statsmodels.tsa.stattools import adfuller
        
        # Use sampling for large datasets
        if len(data) > self.max_sample_size:
            sample_data = self.get_analysis_sample(pd.DataFrame({column_name: data}), column_name)
        else:
            sample_data = data
        
        try:
            adf_result = adfuller(sample_data, autolag='AIC')
            return {
                'adf_statistic': adf_result[0],
                'p_value': adf_result[1],
                'critical_values': adf_result[4],
                'sample_size': len(sample_data),
                'original_size': len(data),
                'sampled': len(data) > self.max_sample_size
            }
        except Exception as e:
            return {
                'error': str(e),
                'sample_size': len(sample_data),
                'original_size': len(data),
                'sampled': len(data) > self.max_sample_size
            }
    
    def fast_basic_stats(self, data: pd.Series) -> Dict[str, Any]:
        """
        Fast basic statistics calculation.
        
        Args:
            data: Input data series
            
        Returns:
            Basic statistics
        """
        return {
            'count': len(data),
            'mean': float(data.mean()),
            'std': float(data.std()),
            'min': float(data.min()),
            'max': float(data.max()),
            'skewness': float(data.skew()),
            'kurtosis': float(data.kurtosis())
        }
    
    def fast_autocorrelation(self, data: pd.Series, max_lags: int = 10) -> Dict[str, Any]:
        """
        Fast autocorrelation calculation using sampling.
        
        Args:
            data: Input data series
            max_lags: Maximum number of lags to calculate
            
        Returns:
            Autocorrelation results
        """
        # Use sampling for large datasets
        if len(data) > self.max_sample_size:
            sample_data = self.get_analysis_sample(pd.DataFrame({'data': data}), 'data')
        else:
            sample_data = data
        
        try:
            autocorr = sample_data.autocorr(lag=1)
            return {
                'lag_1_autocorr': autocorr,
                'sample_size': len(sample_data),
                'original_size': len(data),
                'sampled': len(data) > self.max_sample_size
            }
        except Exception as e:
            return {
                'error': str(e),
                'sample_size': len(sample_data),
                'original_size': len(data),
                'sampled': len(data) > self.max_sample_size
            }
    
    def estimate_processing_time(self, data_shape: Tuple[int, int], 
                               num_columns: int) -> Dict[str, Any]:
        """
        Estimate processing time for large datasets.
        
        Args:
            data_shape: Shape of the data (rows, columns)
            num_columns: Number of columns to analyze
            
        Returns:
            Time estimates
        """
        rows, cols = data_shape
        
        # Base time estimates (in seconds)
        base_times = {
            'adf_test': 0.1,  # per column
            'basic_stats': 0.05,  # per column
            'autocorr': 0.08,  # per column
            'seasonality': 0.2,  # per column
            'financial': 0.15,  # per column
        }
        
        # Scale factors based on data size
        if rows > 100000:
            scale_factor = 1.5  # 50% slower for very large datasets
        elif rows > 50000:
            scale_factor = 1.2  # 20% slower for large datasets
        else:
            scale_factor = 1.0
        
        # Calculate estimates
        estimates = {}
        for analysis_type, base_time in base_times.items():
            estimates[analysis_type] = base_time * num_columns * scale_factor
        
        total_time = sum(estimates.values())
        
        return {
            'estimated_total_time': total_time,
            'estimated_time_per_column': total_time / num_columns,
            'scale_factor': scale_factor,
            'breakdown': estimates,
            'recommendations': self._get_performance_recommendations(rows, cols)
        }
    
    def _get_performance_recommendations(self, rows: int, cols: int) -> List[str]:
        """Get performance recommendations based on data size."""
        recommendations = []
        
        if rows > 200000:
            recommendations.append("Consider using data sampling (max 10,000 rows)")
            recommendations.append("Process in chunks for very large datasets")
            recommendations.append("Use parallel processing if available")
        
        if rows > 100000:
            recommendations.append("Enable fast analysis mode")
            recommendations.append("Consider reducing analysis complexity")
        
        if cols > 20:
            recommendations.append("Focus on most important columns first")
            recommendations.append("Use column filtering")
        
        return recommendations


def analyze_large_dataset_performance(file_path: str) -> Dict[str, Any]:
    """
    Analyze performance characteristics of a large dataset.
    
    Args:
        file_path: Path to the dataset file
        
    Returns:
        Performance analysis results
    """
    print(f"🔍 Analyzing dataset performance: {file_path}")
    
    # Load data
    start_time = time.time()
    df = pd.read_parquet(file_path)
    load_time = time.time() - start_time
    
    # Get basic info
    rows, cols = df.shape
    memory_usage = df.memory_usage(deep=True).sum() / 1024**2  # MB
    
    # Create optimizer
    optimizer = OptimizedAnalysis()
    
    # Estimate processing time
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    time_estimates = optimizer.estimate_processing_time(df.shape, len(numeric_columns))
    
    # Test actual performance on a sample
    print("📊 Testing actual performance...")
    test_column = numeric_columns[0] if numeric_columns else None
    
    if test_column:
        test_data = df[test_column].dropna()
        
        # Test ADF
        adf_start = time.time()
        adf_result = optimizer.fast_adf_test(test_data, test_column)
        adf_time = time.time() - adf_start
        
        # Test basic stats
        stats_start = time.time()
        stats_result = optimizer.fast_basic_stats(test_data)
        stats_time = time.time() - stats_start
        
        # Test autocorr
        corr_start = time.time()
        corr_result = optimizer.fast_autocorrelation(test_data)
        corr_time = time.time() - corr_start
        
        actual_times = {
            'adf_test': adf_time,
            'basic_stats': stats_time,
            'autocorrelation': corr_time
        }
    else:
        actual_times = {}
    
    return {
        'file_path': file_path,
        'data_shape': (rows, cols),
        'memory_usage_mb': memory_usage,
        'load_time': load_time,
        'numeric_columns': len(numeric_columns),
        'time_estimates': time_estimates,
        'actual_times': actual_times,
        'optimization_applied': {
            'sampling_enabled': rows > optimizer.max_sample_size,
            'max_sample_size': optimizer.max_sample_size,
            'chunk_size': optimizer.chunk_size
        }
    }
