"""
Price Validation Module

This module provides price validation functionality for OHLCV data,
ensuring logical correctness of price relationships and detecting anomalies.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import logging


class PriceValidator:
    """Validates OHLCV price data for logical correctness."""
    
    def __init__(self):
        """Initialize the price validator."""
        self.logger = logging.getLogger(__name__)
    
    def validate_ohlc_relationships(self, data: pd.DataFrame, 
                                 open_col: str = 'Open', high_col: str = 'High',
                                 low_col: str = 'Low', close_col: str = 'Close') -> Dict[str, Any]:
        """
        Validate OHLC price relationships.
        
        Args:
            data: DataFrame with OHLC data
            open_col: Name of the Open column
            high_col: Name of the High column
            low_col: Name of the Low column
            close_col: Name of the Close column
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'total_rows': len(data),
            'valid_rows': 0,
            'invalid_rows': 0,
            'validation_errors': [],
            'error_summary': {},
            'data_quality_score': 0.0
        }
        
        try:
            # Check if required columns exist
            required_cols = [open_col, high_col, low_col, close_col]
            missing_cols = [col for col in required_cols if col not in data.columns]
            
            if missing_cols:
                results['validation_errors'].append(f"Missing columns: {missing_cols}")
                return results
            
            # Get OHLC data
            open_prices = data[open_col].dropna()
            high_prices = data[high_col].dropna()
            low_prices = data[low_col].dropna()
            close_prices = data[close_col].dropna()
            
            # Validate each row
            valid_count = 0
            invalid_count = 0
            error_types = {}
            
            for idx, row in data.iterrows():
                is_valid = True
                row_errors = []
                
                # Check if all OHLC values are present
                if pd.isna(row[open_col]) or pd.isna(row[high_col]) or pd.isna(row[low_col]) or pd.isna(row[close_col]):
                    is_valid = False
                    row_errors.append("Missing OHLC values")
                else:
                    # Validate OHLC relationships
                    open_val = row[open_col]
                    high_val = row[high_col]
                    low_val = row[low_col]
                    close_val = row[close_col]
                    
                    # High should be >= Open
                    if high_val < open_val:
                        is_valid = False
                        row_errors.append("High < Open")
                    
                    # High should be >= Close
                    if high_val < close_val:
                        is_valid = False
                        row_errors.append("High < Close")
                    
                    # Low should be <= Open
                    if low_val > open_val:
                        is_valid = False
                        row_errors.append("Low > Open")
                    
                    # Low should be <= Close
                    if low_val > close_val:
                        is_valid = False
                        row_errors.append("Low > Close")
                    
                    # High should be >= Low
                    if high_val < low_val:
                        is_valid = False
                        row_errors.append("High < Low")
                    
                    # Check for negative prices
                    if any(val < 0 for val in [open_val, high_val, low_val, close_val]):
                        is_valid = False
                        row_errors.append("Negative prices")
                    
                    # Check for zero prices
                    if any(val == 0 for val in [open_val, high_val, low_val, close_val]):
                        is_valid = False
                        row_errors.append("Zero prices")
                
                if is_valid:
                    valid_count += 1
                else:
                    invalid_count += 1
                    for error in row_errors:
                        error_types[error] = error_types.get(error, 0) + 1
            
            results['valid_rows'] = valid_count
            results['invalid_rows'] = invalid_count
            results['error_summary'] = error_types
            
            # Calculate data quality score
            if results['total_rows'] > 0:
                results['data_quality_score'] = (valid_count / results['total_rows']) * 100
            
            # Add validation errors to results
            for error_type, count in error_types.items():
                results['validation_errors'].append(f"{error_type}: {count} occurrences")
            
        except Exception as e:
            self.logger.error(f"Error validating OHLC relationships: {str(e)}")
            results['validation_errors'].append(f"Validation error: {str(e)}")
        
        return results
    
    def detect_price_gaps(self, data: pd.DataFrame, 
                         close_col: str = 'Close', 
                         open_col: str = 'Open',
                         gap_threshold: float = 0.01) -> Dict[str, Any]:
        """
        Detect price gaps between consecutive periods.
        
        Args:
            data: DataFrame with OHLC data
            close_col: Name of the Close column
            open_col: Name of the Open column
            gap_threshold: Minimum gap size to consider significant (as percentage)
            
        Returns:
            Dictionary with gap analysis results
        """
        results = {
            'total_gaps': 0,
            'significant_gaps': 0,
            'gap_up_count': 0,
            'gap_down_count': 0,
            'largest_gap_up': 0.0,
            'largest_gap_down': 0.0,
            'average_gap_size': 0.0,
            'gap_details': []
        }
        
        try:
            if close_col not in data.columns or open_col not in data.columns:
                results['error'] = f"Missing columns: {close_col} or {open_col}"
                return results
            
            # Calculate gaps
            prev_close = data[close_col].shift(1)
            current_open = data[open_col]
            
            # Calculate gap percentage
            gap_percentages = ((current_open - prev_close) / prev_close * 100).dropna()
            
            if len(gap_percentages) == 0:
                return results
            
            # Analyze gaps
            gaps = gap_percentages[gap_percentages != 0]
            results['total_gaps'] = len(gaps)
            
            if len(gaps) > 0:
                # Significant gaps
                significant_gaps = gaps[abs(gaps) >= gap_threshold]
                results['significant_gaps'] = len(significant_gaps)
                
                # Gap direction
                gap_up = gaps[gaps > 0]
                gap_down = gaps[gaps < 0]
                results['gap_up_count'] = len(gap_up)
                results['gap_down_count'] = len(gap_down)
                
                # Largest gaps
                if len(gap_up) > 0:
                    results['largest_gap_up'] = float(gap_up.max())
                if len(gap_down) > 0:
                    results['largest_gap_down'] = float(gap_down.min())
                
                # Average gap size
                results['average_gap_size'] = float(abs(gaps).mean())
                
                # Gap details
                for idx, gap in gaps.items():
                    results['gap_details'].append({
                        'index': idx,
                        'gap_percentage': float(gap),
                        'is_significant': abs(gap) >= gap_threshold,
                        'direction': 'up' if gap > 0 else 'down'
                    })
        
        except Exception as e:
            self.logger.error(f"Error detecting price gaps: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def detect_price_anomalies(self, data: pd.DataFrame,
                              price_cols: List[str] = None,
                              z_score_threshold: float = 3.0) -> Dict[str, Any]:
        """
        Detect price anomalies using statistical methods.
        
        Args:
            data: DataFrame with price data
            price_cols: List of price columns to analyze
            z_score_threshold: Z-score threshold for anomaly detection
            
        Returns:
            Dictionary with anomaly detection results
        """
        results = {
            'total_anomalies': 0,
            'anomaly_details': [],
            'columns_analyzed': [],
            'anomaly_summary': {}
        }
        
        try:
            if price_cols is None:
                # Default price columns
                price_cols = ['Open', 'High', 'Low', 'Close']
            
            # Filter existing columns
            existing_cols = [col for col in price_cols if col in data.columns]
            results['columns_analyzed'] = existing_cols
            
            if not existing_cols:
                results['error'] = "No valid price columns found"
                return results
            
            for col in existing_cols:
                col_data = data[col].dropna()
                
                if len(col_data) < 3:
                    continue
                
                # Calculate z-scores
                mean_val = col_data.mean()
                std_val = col_data.std()
                
                if std_val == 0:
                    continue
                
                z_scores = abs((col_data - mean_val) / std_val)
                anomalies = z_scores[z_scores > z_score_threshold]
                
                col_anomalies = []
                for idx, z_score in anomalies.items():
                    col_anomalies.append({
                        'index': idx,
                        'value': float(col_data.loc[idx]),
                        'z_score': float(z_score),
                        'deviation': float((col_data.loc[idx] - mean_val) / std_val)
                    })
                
                results['anomaly_details'].extend(col_anomalies)
                results['anomaly_summary'][col] = {
                    'count': len(col_anomalies),
                    'percentage': (len(col_anomalies) / len(col_data)) * 100
                }
            
            results['total_anomalies'] = len(results['anomaly_details'])
        
        except Exception as e:
            self.logger.error(f"Error detecting price anomalies: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def validate_price_consistency(self, data: pd.DataFrame,
                                 price_cols: List[str] = None,
                                 consistency_threshold: float = 0.1) -> Dict[str, Any]:
        """
        Validate price consistency across different price columns.
        
        Args:
            data: DataFrame with price data
            price_cols: List of price columns to analyze
            consistency_threshold: Maximum allowed deviation for consistency
            
        Returns:
            Dictionary with consistency validation results
        """
        results = {
            'consistent_rows': 0,
            'inconsistent_rows': 0,
            'consistency_score': 0.0,
            'inconsistency_details': [],
            'columns_analyzed': []
        }
        
        try:
            if price_cols is None:
                price_cols = ['Open', 'High', 'Low', 'Close']
            
            # Filter existing columns
            existing_cols = [col for col in price_cols if col in data.columns]
            results['columns_analyzed'] = existing_cols
            
            if len(existing_cols) < 2:
                results['error'] = "Need at least 2 price columns for consistency check"
                return results
            
            # Calculate price ranges for each row
            price_ranges = []
            for idx, row in data.iterrows():
                row_prices = [row[col] for col in existing_cols if not pd.isna(row[col])]
                
                if len(row_prices) < 2:
                    continue
                
                min_price = min(row_prices)
                max_price = max(row_prices)
                price_range = max_price - min_price
                avg_price = sum(row_prices) / len(row_prices)
                
                # Calculate consistency (lower range relative to average price is better)
                if avg_price > 0:
                    consistency_ratio = price_range / avg_price
                    
                    if consistency_ratio <= consistency_threshold:
                        results['consistent_rows'] += 1
                    else:
                        results['inconsistent_rows'] += 1
                        results['inconsistency_details'].append({
                            'index': idx,
                            'price_range': float(price_range),
                            'avg_price': float(avg_price),
                            'consistency_ratio': float(consistency_ratio),
                            'prices': {col: float(row[col]) for col in existing_cols if not pd.isna(row[col])}
                        })
            
            # Calculate overall consistency score
            total_rows = results['consistent_rows'] + results['inconsistent_rows']
            if total_rows > 0:
                results['consistency_score'] = (results['consistent_rows'] / total_rows) * 100
        
        except Exception as e:
            self.logger.error(f"Error validating price consistency: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def get_price_statistics(self, data: pd.DataFrame,
                           price_cols: List[str] = None) -> Dict[str, Any]:
        """
        Get comprehensive price statistics.
        
        Args:
            data: DataFrame with price data
            price_cols: List of price columns to analyze
            
        Returns:
            Dictionary with price statistics
        """
        results = {
            'price_statistics': {},
            'overall_statistics': {},
            'columns_analyzed': []
        }
        
        try:
            if price_cols is None:
                price_cols = ['Open', 'High', 'Low', 'Close']
            
            # Filter existing columns
            existing_cols = [col for col in price_cols if col in data.columns]
            results['columns_analyzed'] = existing_cols
            
            if not existing_cols:
                results['error'] = "No valid price columns found"
                return results
            
            # Calculate statistics for each column
            for col in existing_cols:
                col_data = data[col].dropna()
                
                if len(col_data) == 0:
                    continue
                
                results['price_statistics'][col] = {
                    'count': len(col_data),
                    'mean': float(col_data.mean()),
                    'median': float(col_data.median()),
                    'std': float(col_data.std()),
                    'min': float(col_data.min()),
                    'max': float(col_data.max()),
                    'range': float(col_data.max() - col_data.min()),
                    'skewness': float(col_data.skew()),
                    'kurtosis': float(col_data.kurtosis()),
                    'q25': float(col_data.quantile(0.25)),
                    'q75': float(col_data.quantile(0.75)),
                    'iqr': float(col_data.quantile(0.75) - col_data.quantile(0.25))
                }
            
            # Calculate overall statistics
            all_prices = []
            for col in existing_cols:
                all_prices.extend(data[col].dropna().tolist())
            
            if all_prices:
                all_prices = pd.Series(all_prices)
                results['overall_statistics'] = {
                    'total_price_points': len(all_prices),
                    'overall_mean': float(all_prices.mean()),
                    'overall_std': float(all_prices.std()),
                    'overall_min': float(all_prices.min()),
                    'overall_max': float(all_prices.max()),
                    'overall_range': float(all_prices.max() - all_prices.min())
                }
        
        except Exception as e:
            self.logger.error(f"Error calculating price statistics: {str(e)}")
            results['error'] = str(e)
        
        return results
