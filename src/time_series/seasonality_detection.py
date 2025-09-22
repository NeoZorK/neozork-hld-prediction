"""
Seasonality Detection Module

This module provides comprehensive seasonality detection for time series data,
including day-of-week patterns, monthly patterns, and cyclical patterns.

Features:
- Day-of-Week Patterns: Analysis of intraday patterns (Monday vs Friday)
- Monthly Patterns: Monthly seasonality analysis (January vs December)
- Cyclical Patterns: Cyclical patterns in data (long-term trends)
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from scipy import stats
from scipy.signal import find_peaks
import warnings
import time
warnings.filterwarnings('ignore')


class SeasonalityDetection:
    """Handles seasonality detection for time series data."""
    
    def __init__(self):
        """Initialize the seasonality detection handler."""
        self.day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                           'July', 'August', 'September', 'October', 'November', 'December']
    
    def analyze_seasonality(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
        """
        Perform comprehensive seasonality analysis on time series data.
        
        Args:
            data: DataFrame with time series data
            numeric_columns: List of numeric column names to analyze
            
        Returns:
            Dictionary containing seasonality analysis results
        """
        # Initialize result structure
        results = {
            'day_patterns': {},
            'month_patterns': {},
            'cyclical_patterns': {},
            'overall_seasonality': {}
        }
        
        for col in numeric_columns:
            if col not in data.columns:
                continue
                
            col_data = data[col].dropna()
            if len(col_data) < 30:  # Need minimum data points for seasonality
                continue
            
            # Create progress tracker for this column
            from .progress_tracker import ColumnProgressTracker
            progress_tracker = ColumnProgressTracker(col, "seasonality", 3)
            progress_tracker.start_analysis()
            
            # Day-of-week patterns
            progress_tracker.update_step("Day Patterns")
            day_patterns = self._analyze_day_patterns(data, col, col_data)
            time.sleep(0.1)  # Simulate processing time
            
            # Monthly patterns
            progress_tracker.update_step("Month Patterns")
            month_patterns = self._analyze_month_patterns(data, col, col_data)
            time.sleep(0.1)  # Simulate processing time
            
            # Cyclical patterns
            progress_tracker.update_step("Cyclical Patterns")
            cyclical_patterns = self._analyze_cyclical_patterns(col_data, col)
            time.sleep(0.1)  # Simulate processing time
            
            # Store results by column
            results['day_patterns'][col] = day_patterns
            results['month_patterns'][col] = month_patterns
            results['cyclical_patterns'][col] = cyclical_patterns
            
            # Complete analysis
            progress_tracker.complete_analysis()
        
        # Generate overall seasonality assessment
        results['overall_seasonality'] = self._generate_overall_seasonality_assessment(results)
        
        return results
    
    def _analyze_day_patterns(self, data: pd.DataFrame, column_name: str, col_data: pd.Series) -> Dict[str, Any]:
        """
        Analyze day-of-week patterns in the data.
        
        Args:
            data: Full DataFrame with datetime index
            column_name: Name of the column being analyzed
            col_data: Time series data for the column
            
        Returns:
            Dictionary with day-of-week pattern analysis
        """
        try:
            # Ensure we have datetime index
            if not isinstance(data.index, pd.DatetimeIndex):
                # Try to find datetime column
                datetime_cols = [col for col in data.columns if 'time' in col.lower() or 'date' in col.lower()]
                if datetime_cols:
                    data = data.set_index(datetime_cols[0])
                    data.index = pd.to_datetime(data.index)
                else:
                    return {'error': 'No datetime index or column found for day pattern analysis'}
            
            # Get day of week
            day_of_week = data.index.dayofweek
            day_names = [self.day_names[d] for d in day_of_week]
            
            # Create day pattern analysis
            day_stats = {}
            for i, day_name in enumerate(self.day_names):
                day_mask = day_of_week == i
                if day_mask.sum() > 0:
                    # Ensure we use the same index as col_data
                    day_values = data[column_name].dropna()[day_mask[data[column_name].notna()]]
                    day_stats[day_name] = {
                        'count': len(day_values),
                        'mean': day_values.mean(),
                        'std': day_values.std(),
                        'median': day_values.median(),
                        'min': day_values.min(),
                        'max': day_values.max(),
                        'range': day_values.max() - day_values.min()
                    }
            
            # Calculate day-to-day differences
            day_differences = {}
            for i in range(len(self.day_names)):
                current_day = self.day_names[i]
                next_day = self.day_names[(i + 1) % 7]
                
                if current_day in day_stats and next_day in day_stats:
                    mean_diff = day_stats[next_day]['mean'] - day_stats[current_day]['mean']
                    day_differences[f"{current_day}_to_{next_day}"] = {
                        'mean_difference': mean_diff,
                        'percentage_change': (mean_diff / day_stats[current_day]['mean']) * 100 if day_stats[current_day]['mean'] != 0 else 0
                    }
            
            # Identify strongest patterns
            if day_stats:
                means = [day_stats[day]['mean'] for day in self.day_names if day in day_stats]
                if means:
                    max_mean = max(means)
                    min_mean = min(means)
                    mean_range = max_mean - min_mean
                    
                    strongest_day = max(day_stats.keys(), key=lambda x: day_stats[x]['mean'])
                    weakest_day = min(day_stats.keys(), key=lambda x: day_stats[x]['mean'])
                    
                    pattern_strength = mean_range / max_mean if max_mean != 0 else 0
                else:
                    pattern_strength = 0
                    strongest_day = None
                    weakest_day = None
            else:
                pattern_strength = 0
                strongest_day = None
                weakest_day = None
            
            return {
                'day_statistics': day_stats,
                'day_differences': day_differences,
                'pattern_strength': pattern_strength,
                'strongest_day': strongest_day,
                'weakest_day': weakest_day,
                'has_day_of_week_patterns': pattern_strength > 0.1,  # 10% variation threshold
                'has_significant_pattern': pattern_strength > 0.1,  # 10% variation threshold
                'interpretation': self._interpret_day_patterns(day_stats, pattern_strength)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_month_patterns(self, data: pd.DataFrame, column_name: str, col_data: pd.Series) -> Dict[str, Any]:
        """
        Analyze monthly patterns in the data.
        
        Args:
            data: Full DataFrame with datetime index
            column_name: Name of the column being analyzed
            col_data: Time series data for the column
            
        Returns:
            Dictionary with monthly pattern analysis
        """
        try:
            # Ensure we have datetime index
            if not isinstance(data.index, pd.DatetimeIndex):
                # Try to find datetime column
                datetime_cols = [col for col in data.columns if 'time' in col.lower() or 'date' in col.lower()]
                if datetime_cols:
                    data = data.set_index(datetime_cols[0])
                    data.index = pd.to_datetime(data.index)
                else:
                    return {'error': 'No datetime index or column found for month pattern analysis'}
            
            # Get month
            month = data.index.month
            month_names = [self.month_names[m-1] for m in month]
            
            # Create month pattern analysis
            month_stats = {}
            for i, month_name in enumerate(self.month_names):
                month_mask = month == (i + 1)
                if month_mask.sum() > 0:
                    # Ensure we use the same index as col_data
                    month_values = data[column_name].dropna()[month_mask[data[column_name].notna()]]
                    month_stats[month_name] = {
                        'count': len(month_values),
                        'mean': month_values.mean(),
                        'std': month_values.std(),
                        'median': month_values.median(),
                        'min': month_values.min(),
                        'max': month_values.max(),
                        'range': month_values.max() - month_values.min()
                    }
            
            # Calculate month-to-month differences
            month_differences = {}
            for i in range(len(self.month_names)):
                current_month = self.month_names[i]
                next_month = self.month_names[(i + 1) % 12]
                
                if current_month in month_stats and next_month in month_stats:
                    mean_diff = month_stats[next_month]['mean'] - month_stats[current_month]['mean']
                    month_differences[f"{current_month}_to_{next_month}"] = {
                        'mean_difference': mean_diff,
                        'percentage_change': (mean_diff / month_stats[current_month]['mean']) * 100 if month_stats[current_month]['mean'] != 0 else 0
                    }
            
            # Identify strongest patterns
            if month_stats:
                means = [month_stats[month]['mean'] for month in self.month_names if month in month_stats]
                if means:
                    max_mean = max(means)
                    min_mean = min(means)
                    mean_range = max_mean - min_mean
                    
                    strongest_month = max(month_stats.keys(), key=lambda x: month_stats[x]['mean'])
                    weakest_month = min(month_stats.keys(), key=lambda x: month_stats[x]['mean'])
                    
                    pattern_strength = mean_range / max_mean if max_mean != 0 else 0
                else:
                    pattern_strength = 0
                    strongest_month = None
                    weakest_month = None
            else:
                pattern_strength = 0
                strongest_month = None
                weakest_month = None
            
            return {
                'month_statistics': month_stats,
                'month_differences': month_differences,
                'pattern_strength': pattern_strength,
                'strongest_month': strongest_month,
                'weakest_month': weakest_month,
                'has_monthly_patterns': pattern_strength > 0.1,  # 10% variation threshold
                'has_significant_pattern': pattern_strength > 0.1,  # 10% variation threshold
                'interpretation': self._interpret_month_patterns(month_stats, pattern_strength)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_cyclical_patterns(self, col_data: pd.Series, column_name: str) -> Dict[str, Any]:
        """
        Analyze cyclical patterns in the data.
        
        Args:
            col_data: Time series data for the column
            column_name: Name of the column being analyzed
            
        Returns:
            Dictionary with cyclical pattern analysis
        """
        try:
            # Remove trend for better cyclical analysis
            detrended_data = col_data - col_data.rolling(window=min(30, len(col_data)//4), center=True).mean()
            detrended_data = detrended_data.dropna()
            
            if len(detrended_data) < 20:
                return {'error': 'Insufficient data for cyclical analysis'}
            
            # Autocorrelation analysis
            max_lags = min(50, len(detrended_data) // 4)
            autocorr = acf(detrended_data, nlags=max_lags, fft=True)
            
            # Find significant peaks in autocorrelation
            peaks, properties = find_peaks(autocorr[1:], height=0.1, distance=5)
            peak_lags = peaks + 1  # Adjust for 0-based indexing
            
            # Calculate cyclical periods
            cyclical_periods = []
            for lag in peak_lags:
                if lag < len(autocorr):
                    cyclical_periods.append({
                        'lag': lag,
                        'autocorrelation': autocorr[lag],
                        'period_interpretation': self._interpret_cyclical_period(lag)
                    })
            
            # Sort by autocorrelation strength
            cyclical_periods.sort(key=lambda x: x['autocorrelation'], reverse=True)
            
            # Calculate cyclical strength
            if cyclical_periods:
                strongest_cycle = cyclical_periods[0]
                cyclical_strength = strongest_cycle['autocorrelation']
            else:
                cyclical_strength = 0
                strongest_cycle = None
            
            # Spectral analysis for frequency detection
            fft = np.fft.fft(detrended_data)
            freqs = np.fft.fftfreq(len(detrended_data))
            
            # Find dominant frequencies
            power_spectrum = np.abs(fft) ** 2
            dominant_freq_indices = np.argsort(power_spectrum)[-5:]  # Top 5 frequencies
            dominant_frequencies = []
            
            for idx in dominant_freq_indices:
                if freqs[idx] > 0:  # Only positive frequencies
                    period = 1 / freqs[idx]
                    dominant_frequencies.append({
                        'frequency': freqs[idx],
                        'period': period,
                        'power': power_spectrum[idx],
                        'interpretation': self._interpret_cyclical_period(int(period))
                    })
            
            return {
                'cyclical_periods': cyclical_periods,
                'cyclical_strength': cyclical_strength,
                'strongest_cycle': strongest_cycle,
                'dominant_frequencies': dominant_frequencies,
                'has_cyclical_patterns': cyclical_strength > 0.3,
                'has_cyclical_pattern': cyclical_strength > 0.3,
                'interpretation': self._interpret_cyclical_patterns(cyclical_periods, cyclical_strength)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _interpret_day_patterns(self, day_stats: Dict[str, Any], pattern_strength: float) -> str:
        """Interpret day-of-week patterns."""
        if pattern_strength < 0.05:
            return "No significant day-of-week patterns detected"
        elif pattern_strength < 0.1:
            return "Weak day-of-week patterns detected"
        elif pattern_strength < 0.2:
            return "Moderate day-of-week patterns detected"
        else:
            return "Strong day-of-week patterns detected"
    
    def _interpret_month_patterns(self, month_stats: Dict[str, Any], pattern_strength: float) -> str:
        """Interpret monthly patterns."""
        if pattern_strength < 0.05:
            return "No significant monthly patterns detected"
        elif pattern_strength < 0.1:
            return "Weak monthly patterns detected"
        elif pattern_strength < 0.2:
            return "Moderate monthly patterns detected"
        else:
            return "Strong monthly patterns detected"
    
    def _interpret_cyclical_period(self, period: int) -> str:
        """Interpret cyclical period in business context."""
        if period <= 7:
            return f"Weekly cycle ({period} periods)"
        elif period <= 30:
            return f"Monthly cycle ({period} periods)"
        elif period <= 90:
            return f"Quarterly cycle ({period} periods)"
        elif period <= 365:
            return f"Yearly cycle ({period} periods)"
        else:
            return f"Long-term cycle ({period} periods)"
    
    def _interpret_cyclical_patterns(self, cyclical_periods: List[Dict], cyclical_strength: float) -> str:
        """Interpret cyclical patterns."""
        if cyclical_strength < 0.2:
            return "No significant cyclical patterns detected"
        elif cyclical_strength < 0.4:
            return "Weak cyclical patterns detected"
        elif cyclical_strength < 0.6:
            return "Moderate cyclical patterns detected"
        else:
            return "Strong cyclical patterns detected"
    
    def _generate_overall_seasonality_assessment(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate overall seasonality assessment across all columns.
        
        Args:
            results: Complete seasonality analysis results
            
        Returns:
            Dictionary with overall seasonality assessment
        """
        day_patterns = results.get('day_patterns', {})
        month_patterns = results.get('month_patterns', {})
        cyclical_patterns = results.get('cyclical_patterns', {})
        
        total_columns = len(day_patterns)
        significant_day_patterns = 0
        significant_month_patterns = 0
        significant_cyclical_patterns = 0
        
        for col in day_patterns:
            if day_patterns[col].get('has_significant_pattern', False):
                significant_day_patterns += 1
        
        for col in month_patterns:
            if month_patterns[col].get('has_significant_pattern', False):
                significant_month_patterns += 1
        
        for col in cyclical_patterns:
            if cyclical_patterns[col].get('has_cyclical_patterns', False):
                significant_cyclical_patterns += 1
        
        total_patterns = significant_day_patterns + significant_month_patterns + significant_cyclical_patterns
        total_possible_patterns = total_columns * 3
        seasonality_ratio = total_patterns / total_possible_patterns if total_possible_patterns > 0 else 0
        
        assessment = {
            'total_columns': total_columns,
            'significant_day_patterns': significant_day_patterns,
            'significant_month_patterns': significant_month_patterns,
            'significant_cyclical_patterns': significant_cyclical_patterns,
            'day_pattern_rate': significant_day_patterns / total_columns if total_columns > 0 else 0,
            'month_pattern_rate': significant_month_patterns / total_columns if total_columns > 0 else 0,
            'cyclical_pattern_rate': significant_cyclical_patterns / total_columns if total_columns > 0 else 0,
            'overall_seasonality_level': 'high' if seasonality_ratio > 0.5 else
                                       'moderate' if seasonality_ratio > 0.2 else 'low',
            'recommendations': []
        }
        
        # Generate recommendations
        if assessment['day_pattern_rate'] > 0.5:
            assessment['recommendations'].append(
                "Strong day-of-week patterns detected - consider day-of-week dummy variables"
            )
        
        if assessment['month_pattern_rate'] > 0.5:
            assessment['recommendations'].append(
                "Strong monthly patterns detected - consider seasonal decomposition"
            )
        
        if assessment['cyclical_pattern_rate'] > 0.5:
            assessment['recommendations'].append(
                "Strong cyclical patterns detected - consider cyclical models"
            )
        
        if assessment['overall_seasonality_level'] == 'low':
            assessment['recommendations'].append(
                "Low seasonality detected - data may be suitable for trend-based models"
            )
        
        return assessment
