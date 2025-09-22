"""
Financial Features Analysis Module

This module provides comprehensive financial features analysis for time series data,
including price range analysis, price changes, and volatility analysis.

Features:
- Price Range Analysis: High - Low analysis
- Price Changes: Absolute and percentage price changes
- Volatility Analysis: Volatility analysis (standard deviation, coefficient of variation)
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


class FinancialFeatures:
    """Handles financial features analysis for time series data."""
    
    def __init__(self):
        """Initialize the financial features analysis handler."""
        self.volatility_windows = [5, 10, 20, 30]  # Different volatility calculation windows
        self.return_periods = [1, 5, 10, 20]  # Different return calculation periods
    
    def analyze_financial_features(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
        """
        Perform comprehensive financial features analysis on time series data.
        
        Args:
            data: DataFrame with time series data
            numeric_columns: List of numeric column names to analyze
            
        Returns:
            Dictionary containing financial features analysis results
        """
        results = {
            'price_range_analysis': {},
            'price_changes_analysis': {},
            'volatility_analysis': {},
            'overall_financial_assessment': {}
        }
        
        for col in numeric_columns:
            if col not in data.columns:
                continue
                
            col_data = data[col].dropna()
            if len(col_data) < 10:  # Need minimum data points
                continue
            
            print(f"\n🔍 Analyzing financial features for column: {col}")
            print("-" * 50)
            
            # Price range analysis
            price_range = self._analyze_price_range(col_data, col)
            results['price_range_analysis'][col] = price_range
            
            # Price changes analysis
            price_changes = self._analyze_price_changes(col_data, col)
            results['price_changes_analysis'][col] = price_changes
            
            # Volatility analysis
            volatility = self._analyze_volatility(col_data, col)
            results['volatility_analysis'][col] = volatility
        
        # Overall financial assessment
        results['overall_financial_assessment'] = self._generate_overall_financial_assessment(results)
        
        return results
    
    def _analyze_price_range(self, col_data: pd.Series, column_name: str) -> Dict[str, Any]:
        """
        Analyze price range characteristics.
        
        Args:
            col_data: Time series data for the column
            column_name: Name of the column being analyzed
            
        Returns:
            Dictionary with price range analysis
        """
        try:
            # Basic range statistics
            min_price = col_data.min()
            max_price = col_data.max()
            price_range = max_price - min_price
            mean_price = col_data.mean()
            median_price = col_data.median()
            
            # Range as percentage of mean
            range_percentage = (price_range / mean_price) * 100 if mean_price != 0 else 0
            
            # Rolling range analysis
            rolling_ranges = []
            for window in [5, 10, 20, 30]:
                if len(col_data) >= window:
                    rolling_max = col_data.rolling(window=window).max()
                    rolling_min = col_data.rolling(window=window).min()
                    rolling_range = rolling_max - rolling_min
                    rolling_ranges.append({
                        'window': window,
                        'mean_range': rolling_range.mean(),
                        'std_range': rolling_range.std(),
                        'max_range': rolling_range.max(),
                        'min_range': rolling_range.min()
                    })
            
            # Range stability (coefficient of variation of rolling ranges)
            if rolling_ranges:
                range_stability = rolling_ranges[0]['std_range'] / rolling_ranges[0]['mean_range'] if rolling_ranges[0]['mean_range'] != 0 else 0
            else:
                range_stability = 0
            
            # Price distribution within range
            price_quartiles = col_data.quantile([0.25, 0.5, 0.75])
            q1, q2, q3 = price_quartiles[0.25], price_quartiles[0.5], price_quartiles[0.75]
            
            # Range utilization
            range_utilization = {
                'bottom_quartile': ((q1 - min_price) / price_range) * 100 if price_range != 0 else 0,
                'middle_half': (((q3 - q1) / price_range) * 100) if price_range != 0 else 0,
                'top_quartile': ((max_price - q3) / price_range) * 100 if price_range != 0 else 0
            }
            
            return {
                'min_price': min_price,
                'max_price': max_price,
                'price_range': price_range,
                'range_percentage': range_percentage,
                'mean_price': mean_price,
                'median_price': median_price,
                'rolling_ranges': rolling_ranges,
                'range_stability': range_stability,
                'price_quartiles': {
                    'q1': q1,
                    'q2': q2,
                    'q3': q3
                },
                'range_utilization': range_utilization,
                'volatility_level': self._classify_volatility_level(range_percentage),
                'interpretation': self._interpret_price_range(range_percentage, range_stability)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_price_changes(self, col_data: pd.Series, column_name: str) -> Dict[str, Any]:
        """
        Analyze price changes (absolute and percentage).
        
        Args:
            col_data: Time series data for the column
            column_name: Name of the column being analyzed
            
        Returns:
            Dictionary with price changes analysis
        """
        try:
            # Calculate returns for different periods
            returns_analysis = {}
            
            for period in self.return_periods:
                if len(col_data) > period:
                    # Simple returns
                    simple_returns = col_data.pct_change(period).dropna()
                    
                    # Log returns
                    log_returns = np.log(col_data / col_data.shift(period)).dropna()
                    
                    # Absolute changes
                    absolute_changes = col_data.diff(period).dropna()
                    
                    returns_analysis[f'period_{period}'] = {
                        'simple_returns': {
                            'mean': simple_returns.mean(),
                            'std': simple_returns.std(),
                            'min': simple_returns.min(),
                            'max': simple_returns.max(),
                            'skewness': simple_returns.skew(),
                            'kurtosis': simple_returns.kurtosis(),
                            'positive_returns': (simple_returns > 0).sum(),
                            'negative_returns': (simple_returns < 0).sum(),
                            'zero_returns': (simple_returns == 0).sum()
                        },
                        'log_returns': {
                            'mean': log_returns.mean(),
                            'std': log_returns.std(),
                            'min': log_returns.min(),
                            'max': log_returns.max(),
                            'skewness': log_returns.skew(),
                            'kurtosis': log_returns.kurtosis()
                        },
                        'absolute_changes': {
                            'mean': absolute_changes.mean(),
                            'std': absolute_changes.std(),
                            'min': absolute_changes.min(),
                            'max': absolute_changes.max(),
                            'mean_abs': absolute_changes.abs().mean()
                        }
                    }
            
            # Overall return statistics
            if len(col_data) > 1:
                daily_returns = col_data.pct_change().dropna()
                
                # Return distribution analysis
                return_percentiles = daily_returns.quantile([0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
                
                # Extreme returns analysis
                extreme_positive = (daily_returns > daily_returns.quantile(0.95)).sum()
                extreme_negative = (daily_returns < daily_returns.quantile(0.05)).sum()
                
                # Return consistency
                positive_days = (daily_returns > 0).sum()
                negative_days = (daily_returns < 0).sum()
                total_days = len(daily_returns)
                
                return_consistency = {
                    'positive_days': positive_days,
                    'negative_days': negative_days,
                    'positive_percentage': (positive_days / total_days) * 100 if total_days > 0 else 0,
                    'negative_percentage': (negative_days / total_days) * 100 if total_days > 0 else 0,
                    'extreme_positive': extreme_positive,
                    'extreme_negative': extreme_negative
                }
            else:
                return_percentiles = None
                return_consistency = None
            
            return {
                'returns_by_period': returns_analysis,
                'daily_return_percentiles': return_percentiles,
                'return_consistency': return_consistency,
                'overall_volatility': daily_returns.std() if len(col_data) > 1 else 0,
                'return_trend': self._analyze_return_trend(daily_returns) if len(col_data) > 1 else None,
                'interpretation': self._interpret_price_changes(returns_analysis, return_consistency)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_volatility(self, col_data: pd.Series, column_name: str) -> Dict[str, Any]:
        """
        Analyze volatility characteristics.
        
        Args:
            col_data: Time series data for the column
            column_name: Name of the column being analyzed
            
        Returns:
            Dictionary with volatility analysis
        """
        try:
            # Calculate returns for volatility analysis
            if len(col_data) > 1:
                returns = col_data.pct_change().dropna()
            else:
                return {'error': 'Insufficient data for volatility analysis'}
            
            # Volatility by different windows
            volatility_by_window = {}
            for window in self.volatility_windows:
                if len(returns) >= window:
                    rolling_vol = returns.rolling(window=window).std()
                    volatility_by_window[f'window_{window}'] = {
                        'mean_volatility': rolling_vol.mean(),
                        'std_volatility': rolling_vol.std(),
                        'min_volatility': rolling_vol.min(),
                        'max_volatility': rolling_vol.max(),
                        'volatility_trend': self._calculate_trend(rolling_vol.dropna())
                    }
            
            # Overall volatility metrics
            overall_volatility = returns.std()
            if pd.isna(overall_volatility):
                overall_volatility = 0
            annualized_volatility = overall_volatility * np.sqrt(252)  # Assuming daily data
            
            # Coefficient of variation
            coefficient_of_variation = (overall_volatility / col_data.mean()) * 100 if col_data.mean() != 0 else 0
            if pd.isna(coefficient_of_variation):
                coefficient_of_variation = 0
            
            # Volatility clustering analysis
            volatility_clustering = self._analyze_volatility_clustering(returns)
            
            # Volatility regime analysis
            volatility_regimes = self._analyze_volatility_regimes(returns)
            
            # Risk metrics
            risk_metrics = {
                'var_95': returns.quantile(0.05),  # 95% VaR
                'var_99': returns.quantile(0.01),  # 99% VaR
                'expected_shortfall_95': returns[returns <= returns.quantile(0.05)].mean(),
                'expected_shortfall_99': returns[returns <= returns.quantile(0.01)].mean(),
                'max_drawdown': self._calculate_max_drawdown(col_data),
                'sharpe_ratio': returns.mean() / overall_volatility if overall_volatility != 0 else 0
            }
            
            return {
                'volatility_by_window': volatility_by_window,
                'overall_volatility': overall_volatility,
                'annualized_volatility': annualized_volatility,
                'coefficient_of_variation': coefficient_of_variation,
                'volatility_clustering': volatility_clustering,
                'volatility_regimes': volatility_regimes,
                'risk_metrics': risk_metrics,
                'volatility_level': self._classify_volatility_level(coefficient_of_variation),
                'interpretation': self._interpret_volatility(overall_volatility, coefficient_of_variation, volatility_clustering)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _classify_volatility_level(self, volatility_metric: float) -> str:
        """Classify volatility level based on metric."""
        if volatility_metric < 5:
            return 'very_low'
        elif volatility_metric < 15:
            return 'low'
        elif volatility_metric < 30:
            return 'moderate'
        elif volatility_metric < 50:
            return 'high'
        else:
            return 'very_high'
    
    def _interpret_price_range(self, range_percentage: float, range_stability: float) -> str:
        """Interpret price range characteristics."""
        if range_percentage < 10:
            return "Very stable price range - low volatility"
        elif range_percentage < 25:
            return "Moderate price range - normal volatility"
        elif range_percentage < 50:
            return "Wide price range - high volatility"
        else:
            return "Very wide price range - extremely high volatility"
    
    def _interpret_price_changes(self, returns_analysis: Dict, return_consistency: Dict) -> str:
        """Interpret price changes characteristics."""
        if not returns_analysis or not return_consistency:
            return "Insufficient data for price change analysis"
        
        positive_pct = return_consistency.get('positive_percentage', 0)
        
        if positive_pct > 60:
            return "Predominantly positive returns - upward trend"
        elif positive_pct < 40:
            return "Predominantly negative returns - downward trend"
        else:
            return "Balanced positive and negative returns - sideways movement"
    
    def _interpret_volatility(self, overall_volatility: float, coefficient_of_variation: float, 
                            volatility_clustering: Dict) -> str:
        """Interpret volatility characteristics."""
        vol_level = self._classify_volatility_level(coefficient_of_variation)
        
        if vol_level == 'very_low':
            return "Very low volatility - stable asset"
        elif vol_level == 'low':
            return "Low volatility - relatively stable"
        elif vol_level == 'moderate':
            return "Moderate volatility - normal market conditions"
        elif vol_level == 'high':
            return "High volatility - risky asset"
        else:
            return "Very high volatility - extremely risky asset"
    
    def _analyze_return_trend(self, returns: pd.Series) -> Dict[str, Any]:
        """Analyze trend in returns."""
        try:
            if len(returns) < 10:
                return {'error': 'Insufficient data for trend analysis'}
            
            # Linear trend
            x = np.arange(len(returns))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, returns)
            
            # Moving average trend
            ma_short = returns.rolling(window=5).mean()
            ma_long = returns.rolling(window=20).mean()
            
            trend_direction = 'upward' if slope > 0 else 'downward' if slope < 0 else 'flat'
            trend_strength = abs(r_value)
            
            return {
                'slope': slope,
                'r_squared': r_value ** 2,
                'p_value': p_value,
                'trend_direction': trend_direction,
                'trend_strength': trend_strength,
                'is_significant': p_value < 0.05
            }
        except:
            return {'error': 'Trend analysis failed'}
    
    def _calculate_trend(self, data: pd.Series) -> float:
        """Calculate simple trend slope."""
        try:
            if len(data) < 2:
                return 0
            x = np.arange(len(data))
            slope, _, _, _, _ = stats.linregress(x, data)
            return slope
        except:
            return 0
    
    def _analyze_volatility_clustering(self, returns: pd.Series) -> Dict[str, Any]:
        """Analyze volatility clustering (ARCH effects)."""
        try:
            if len(returns) < 20:
                return {'error': 'Insufficient data for volatility clustering analysis'}
            
            # Calculate squared returns
            squared_returns = returns ** 2
            
            # Autocorrelation of squared returns
            autocorr = squared_returns.autocorr(lag=1)
            
            # Ljung-Box test for serial correlation in squared returns
            from statsmodels.stats.diagnostic import acorr_ljungbox
            lb_stat, lb_pvalue = acorr_ljungbox(squared_returns, lags=10, return_df=False)
            
            return {
                'autocorrelation_squared_returns': autocorr,
                'ljung_box_statistic': lb_stat[0] if len(lb_stat) > 0 else 0,
                'ljung_box_pvalue': lb_pvalue[0] if len(lb_pvalue) > 0 else 1,
                'has_clustering': lb_pvalue[0] < 0.05 if len(lb_pvalue) > 0 else False
            }
        except:
            return {'error': 'Volatility clustering analysis failed'}
    
    def _analyze_volatility_regimes(self, returns: pd.Series) -> Dict[str, Any]:
        """Analyze different volatility regimes."""
        try:
            if len(returns) < 30:
                return {'error': 'Insufficient data for volatility regime analysis'}
            
            # Calculate rolling volatility
            rolling_vol = returns.rolling(window=10).std()
            
            # Define volatility regimes based on percentiles
            vol_25 = rolling_vol.quantile(0.25)
            vol_75 = rolling_vol.quantile(0.75)
            
            low_vol_periods = (rolling_vol <= vol_25).sum()
            high_vol_periods = (rolling_vol >= vol_75).sum()
            medium_vol_periods = ((rolling_vol > vol_25) & (rolling_vol < vol_75)).sum()
            
            return {
                'low_volatility_periods': low_vol_periods,
                'medium_volatility_periods': medium_vol_periods,
                'high_volatility_periods': high_vol_periods,
                'low_vol_threshold': vol_25,
                'high_vol_threshold': vol_75,
                'regime_distribution': {
                    'low': low_vol_periods / len(rolling_vol) * 100,
                    'medium': medium_vol_periods / len(rolling_vol) * 100,
                    'high': high_vol_periods / len(rolling_vol) * 100
                }
            }
        except:
            return {'error': 'Volatility regime analysis failed'}
    
    def _calculate_max_drawdown(self, prices: pd.Series) -> float:
        """Calculate maximum drawdown."""
        try:
            cumulative = (1 + prices.pct_change()).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            return drawdown.min()
        except:
            return 0
    
    def _generate_overall_financial_assessment(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate overall financial assessment across all columns.
        
        Args:
            results: Complete financial features analysis results
            
        Returns:
            Dictionary with overall financial assessment
        """
        price_range_analysis = results.get('price_range_analysis', {})
        price_changes_analysis = results.get('price_changes_analysis', {})
        volatility_analysis = results.get('volatility_analysis', {})
        
        total_columns = len(price_range_analysis)
        
        # Count different volatility levels
        volatility_levels = {'very_low': 0, 'low': 0, 'moderate': 0, 'high': 0, 'very_high': 0}
        
        for col in volatility_analysis:
            if 'volatility_level' in volatility_analysis[col]:
                level = volatility_analysis[col]['volatility_level']
                if level in volatility_levels:
                    volatility_levels[level] += 1
        
        # Calculate average metrics
        avg_range_percentage = 0
        avg_volatility = 0
        avg_coefficient_variation = 0
        
        range_count = 0
        vol_count = 0
        
        for col in price_range_analysis:
            if 'range_percentage' in price_range_analysis[col]:
                avg_range_percentage += price_range_analysis[col]['range_percentage']
                range_count += 1
        
        for col in volatility_analysis:
            if 'overall_volatility' in volatility_analysis[col]:
                avg_volatility += volatility_analysis[col]['overall_volatility']
                vol_count += 1
            if 'coefficient_of_variation' in volatility_analysis[col]:
                avg_coefficient_variation += volatility_analysis[col]['coefficient_of_variation']
        
        if range_count > 0:
            avg_range_percentage /= range_count
        if vol_count > 0:
            avg_volatility /= vol_count
            avg_coefficient_variation /= vol_count
        
        assessment = {
            'total_columns': total_columns,
            'volatility_distribution': volatility_levels,
            'average_range_percentage': avg_range_percentage,
            'average_volatility': avg_volatility,
            'average_coefficient_variation': avg_coefficient_variation,
            'overall_risk_level': self._classify_volatility_level(avg_coefficient_variation),
            'recommendations': []
        }
        
        # Generate recommendations
        if assessment['overall_risk_level'] in ['high', 'very_high']:
            assessment['recommendations'].append(
                "High volatility detected - consider risk management strategies"
            )
        
        if avg_range_percentage > 50:
            assessment['recommendations'].append(
                "Very wide price ranges detected - high price volatility"
            )
        
        if volatility_levels['very_high'] > total_columns * 0.3:
            assessment['recommendations'].append(
                "Multiple high-volatility assets detected - portfolio diversification recommended"
            )
        
        return assessment
