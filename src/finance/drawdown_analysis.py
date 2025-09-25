"""
Drawdown Analysis Module

This module provides comprehensive drawdown analysis including maximum drawdown,
drawdown duration, and recovery analysis for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import logging
from .color_utils import ColorUtils


class DrawdownAnalysis:
    """Comprehensive drawdown analysis for financial data."""
    
    def __init__(self):
        """Initialize the drawdown analyzer."""
        self.logger = logging.getLogger(__name__)
    
    def analyze_drawdowns(self, data: pd.DataFrame, 
                         numeric_columns: List[str]) -> Dict[str, Any]:
        """
        Perform comprehensive drawdown analysis.
        
        Args:
            data: DataFrame with financial data
            numeric_columns: List of numeric columns to analyze
            
        Returns:
            Dictionary with drawdown analysis results
        """
        results = {
            'maximum_drawdown': {},
            'drawdown_duration': {},
            'recovery_analysis': {},
            'drawdown_statistics': {},
            'risk_metrics': {},
            'drawdown_patterns': {},
            'recommendations': {}
        }
        
        try:
            # Identify price columns for drawdown analysis
            price_columns = self._identify_price_columns(data, numeric_columns)
            
            if not price_columns:
                results['error'] = "No price columns identified for drawdown analysis"
                return results
            
            # Calculate cumulative returns for drawdown analysis
            cumulative_returns = self._calculate_cumulative_returns(data, price_columns)
            
            if cumulative_returns.empty:
                results['error'] = "Unable to calculate cumulative returns for drawdown analysis"
                return results
            
            # Maximum drawdown analysis
            results['maximum_drawdown'] = self._analyze_maximum_drawdown(
                cumulative_returns, price_columns
            )
            
            # Drawdown duration analysis
            results['drawdown_duration'] = self._analyze_drawdown_duration(
                cumulative_returns, price_columns
            )
            
            # Recovery analysis
            results['recovery_analysis'] = self._analyze_recovery(
                cumulative_returns, price_columns
            )
            
            # Drawdown statistics
            results['drawdown_statistics'] = self._calculate_drawdown_statistics(
                cumulative_returns, price_columns
            )
            
            # Risk metrics
            results['risk_metrics'] = self._calculate_risk_metrics(
                cumulative_returns, price_columns
            )
            
            # Drawdown patterns
            results['drawdown_patterns'] = self._analyze_drawdown_patterns(
                cumulative_returns, price_columns
            )
            
            # Generate recommendations
            results['recommendations'] = self._generate_drawdown_recommendations(
                results
            )
            
        except Exception as e:
            self.logger.error(f"Error in drawdown analysis: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _identify_price_columns(self, data: pd.DataFrame, 
                               numeric_columns: List[str]) -> List[str]:
        """
        Identify price columns suitable for drawdown analysis.
        
        Args:
            data: DataFrame with financial data
            numeric_columns: List of numeric columns
            
        Returns:
            List of price column names
        """
        price_columns = []
        
        # Common price column patterns
        price_keywords = ['close', 'price', 'value', 'rate', 'quote', 'open', 'high', 'low']
        
        for col in numeric_columns:
            col_lower = col.lower()
            
            # Check if column name suggests it's a price
            if any(keyword in col_lower for keyword in price_keywords):
                # Additional validation: check if values are positive and reasonable
                col_data = data[col].dropna()
                if len(col_data) > 0:
                    # Check for reasonable price values (positive, not too small/large)
                    if (col_data > 0).all() and col_data.min() > 0.001 and col_data.max() < 1e6:
                        price_columns.append(col)
        
        return price_columns
    
    def _calculate_cumulative_returns(self, data: pd.DataFrame, 
                                    price_columns: List[str]) -> pd.DataFrame:
        """
        Calculate cumulative returns for drawdown analysis.
        
        Args:
            data: DataFrame with price data
            price_columns: List of price columns
            
        Returns:
            DataFrame with cumulative returns
        """
        cumulative_returns = pd.DataFrame(index=data.index)
        
        for col in price_columns:
            if col in data.columns:
                price_series = data[col].dropna()
                
                if len(price_series) > 1:
                    # Calculate simple returns
                    returns = price_series.pct_change().dropna()
                    
                    # Calculate cumulative returns
                    cumulative = (1 + returns).cumprod()
                    cumulative_returns[f'{col}_cumulative'] = cumulative
        
        return cumulative_returns.dropna()
    
    def _analyze_maximum_drawdown(self, cumulative_returns: pd.DataFrame,
                                price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze maximum drawdown for each price series.
        
        Args:
            cumulative_returns: DataFrame with cumulative returns
            price_columns: List of price columns
            
        Returns:
            Dictionary with maximum drawdown analysis
        """
        results = {
            'maximum_drawdowns': {},
            'drawdown_analysis': {},
            'current_drawdown': {}
        }
        
        try:
            for col in price_columns:
                cumulative_col = f'{col}_cumulative'
                if cumulative_col in cumulative_returns.columns:
                    cumulative_series = cumulative_returns[cumulative_col].dropna()
                    
                    if len(cumulative_series) == 0:
                        continue
                    
                    # Calculate running maximum
                    running_max = cumulative_series.expanding().max()
                    
                    # Calculate drawdown
                    drawdown = (cumulative_series - running_max) / running_max
                    
                    # Maximum drawdown
                    max_drawdown = drawdown.min()
                    max_drawdown_date = drawdown.idxmin()
                    
                    # Current drawdown
                    current_drawdown = drawdown.iloc[-1]
                    
                    # Drawdown analysis
                    drawdown_analysis = {
                        'maximum_drawdown': float(max_drawdown),
                        'maximum_drawdown_percentage': float(max_drawdown * 100),
                        'maximum_drawdown_date': str(max_drawdown_date),
                        'current_drawdown': float(current_drawdown),
                        'current_drawdown_percentage': float(current_drawdown * 100),
                        'drawdown_count': int((drawdown < 0).sum()),
                        'drawdown_frequency': float((drawdown < 0).sum() / len(drawdown) * 100)
                    }
                    
                    results['maximum_drawdowns'][col] = drawdown_analysis
                    
                    # Additional analysis
                    results['drawdown_analysis'][col] = {
                        'average_drawdown': float(drawdown[drawdown < 0].mean()) if (drawdown < 0).any() else 0.0,
                        'drawdown_volatility': float(drawdown.std()),
                        'worst_drawdown_period': self._find_worst_drawdown_period(drawdown),
                        'drawdown_severity': self._assess_drawdown_severity(max_drawdown)
                    }
                    
                    # Current drawdown status
                    results['current_drawdown'][col] = {
                        'is_in_drawdown': current_drawdown < 0,
                        'drawdown_magnitude': abs(current_drawdown),
                        'time_in_drawdown': self._calculate_time_in_drawdown(drawdown),
                        'recovery_needed': abs(current_drawdown) if current_drawdown < 0 else 0.0
                    }
        
        except Exception as e:
            self.logger.error(f"Error analyzing maximum drawdown: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_drawdown_duration(self, cumulative_returns: pd.DataFrame,
                                 price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze drawdown duration patterns.
        
        Args:
            cumulative_returns: DataFrame with cumulative returns
            price_columns: List of price columns
            
        Returns:
            Dictionary with drawdown duration analysis
        """
        results = {
            'duration_statistics': {},
            'duration_patterns': {},
            'longest_drawdowns': {}
        }
        
        try:
            for col in price_columns:
                cumulative_col = f'{col}_cumulative'
                if cumulative_col in cumulative_returns.columns:
                    cumulative_series = cumulative_returns[cumulative_col].dropna()
                    
                    if len(cumulative_series) == 0:
                        continue
                    
                    # Calculate drawdown periods
                    drawdown_periods = self._identify_drawdown_periods(cumulative_series)
                    
                    if not drawdown_periods:
                        continue
                    
                    # Duration statistics
                    durations = [period['duration'] for period in drawdown_periods]
                    
                    duration_stats = {
                        'total_drawdown_periods': len(drawdown_periods),
                        'average_duration': float(np.mean(durations)),
                        'median_duration': float(np.median(durations)),
                        'max_duration': int(max(durations)),
                        'min_duration': int(min(durations)),
                        'duration_std': float(np.std(durations)),
                        'total_time_in_drawdown': sum(durations),
                        'percentage_time_in_drawdown': float(sum(durations) / len(cumulative_series) * 100)
                    }
                    
                    results['duration_statistics'][col] = duration_stats
                    
                    # Duration patterns
                    duration_patterns = {
                        'short_drawdowns': len([d for d in durations if d <= 5]),
                        'medium_drawdowns': len([d for d in durations if 5 < d <= 20]),
                        'long_drawdowns': len([d for d in durations if d > 20]),
                        'drawdown_clustering': self._assess_drawdown_clustering(drawdown_periods)
                    }
                    
                    results['duration_patterns'][col] = duration_patterns
                    
                    # Longest drawdowns
                    longest_drawdowns = sorted(drawdown_periods, key=lambda x: x['duration'], reverse=True)[:5]
                    results['longest_drawdowns'][col] = longest_drawdowns
        
        except Exception as e:
            self.logger.error(f"Error analyzing drawdown duration: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_recovery(self, cumulative_returns: pd.DataFrame,
                         price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze recovery patterns from drawdowns.
        
        Args:
            cumulative_returns: DataFrame with cumulative returns
            price_columns: List of price columns
            
        Returns:
            Dictionary with recovery analysis
        """
        results = {
            'recovery_statistics': {},
            'recovery_patterns': {},
            'recovery_analysis': {}
        }
        
        try:
            for col in price_columns:
                cumulative_col = f'{col}_cumulative'
                if cumulative_col in cumulative_returns.columns:
                    cumulative_series = cumulative_returns[cumulative_col].dropna()
                    
                    if len(cumulative_series) == 0:
                        continue
                    
                    # Calculate recovery metrics
                    recovery_metrics = self._calculate_recovery_metrics(cumulative_series)
                    
                    results['recovery_statistics'][col] = recovery_metrics
                    
                    # Recovery patterns
                    recovery_patterns = {
                        'fast_recoveries': recovery_metrics['fast_recoveries'],
                        'slow_recoveries': recovery_metrics['slow_recoveries'],
                        'average_recovery_time': recovery_metrics['average_recovery_time'],
                        'recovery_success_rate': recovery_metrics['recovery_success_rate']
                    }
                    
                    results['recovery_patterns'][col] = recovery_patterns
                    
                    # Recovery analysis
                    recovery_analysis = {
                        'current_recovery_status': self._assess_current_recovery_status(cumulative_series),
                        'recovery_momentum': self._calculate_recovery_momentum(cumulative_series),
                        'recovery_confidence': self._assess_recovery_confidence(cumulative_series)
                    }
                    
                    results['recovery_analysis'][col] = recovery_analysis
        
        except Exception as e:
            self.logger.error(f"Error analyzing recovery: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _calculate_drawdown_statistics(self, cumulative_returns: pd.DataFrame,
                                     price_columns: List[str]) -> Dict[str, Any]:
        """
        Calculate comprehensive drawdown statistics.
        
        Args:
            cumulative_returns: DataFrame with cumulative returns
            price_columns: List of price columns
            
        Returns:
            Dictionary with drawdown statistics
        """
        results = {
            'overall_statistics': {},
            'drawdown_distribution': {},
            'risk_metrics': {}
        }
        
        try:
            for col in price_columns:
                cumulative_col = f'{col}_cumulative'
                if cumulative_col in cumulative_returns.columns:
                    cumulative_series = cumulative_returns[cumulative_col].dropna()
                    
                    if len(cumulative_series) == 0:
                        continue
                    
                    # Calculate drawdown series
                    running_max = cumulative_series.expanding().max()
                    drawdown = (cumulative_series - running_max) / running_max
                    
                    # Overall statistics
                    overall_stats = {
                        'total_periods': len(cumulative_series),
                        'drawdown_periods': int((drawdown < 0).sum()),
                        'drawdown_frequency': float((drawdown < 0).sum() / len(drawdown) * 100),
                        'average_drawdown': float(drawdown[drawdown < 0].mean()) if (drawdown < 0).any() else 0.0,
                        'drawdown_volatility': float(drawdown.std()),
                        'worst_drawdown': float(drawdown.min()),
                        'current_drawdown': float(drawdown.iloc[-1])
                    }
                    
                    results['overall_statistics'][col] = overall_stats
                    
                    # Drawdown distribution
                    drawdown_dist = {
                        'drawdown_percentiles': {
                            'p25': float(drawdown.quantile(0.25)),
                            'p50': float(drawdown.quantile(0.50)),
                            'p75': float(drawdown.quantile(0.75)),
                            'p90': float(drawdown.quantile(0.90)),
                            'p95': float(drawdown.quantile(0.95)),
                            'p99': float(drawdown.quantile(0.99))
                        },
                        'drawdown_skewness': float(drawdown.skew()),
                        'drawdown_kurtosis': float(drawdown.kurtosis())
                    }
                    
                    results['drawdown_distribution'][col] = drawdown_dist
                    
                    # Risk metrics
                    risk_metrics = {
                        'var_95': float(drawdown.quantile(0.05)),
                        'var_99': float(drawdown.quantile(0.01)),
                        'cvar_95': float(drawdown[drawdown <= drawdown.quantile(0.05)].mean()),
                        'cvar_99': float(drawdown[drawdown <= drawdown.quantile(0.01)].mean()),
                        'downside_deviation': float(drawdown[drawdown < 0].std()) if (drawdown < 0).any() else 0.0
                    }
                    
                    results['risk_metrics'][col] = risk_metrics
        
        except Exception as e:
            self.logger.error(f"Error calculating drawdown statistics: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _calculate_risk_metrics(self, cumulative_returns: pd.DataFrame,
                              price_columns: List[str]) -> Dict[str, Any]:
        """
        Calculate risk metrics based on drawdowns.
        
        Args:
            cumulative_returns: DataFrame with cumulative returns
            price_columns: List of price columns
            
        Returns:
            Dictionary with risk metrics
        """
        results = {
            'risk_metrics': {},
            'risk_comparison': {},
            'risk_assessment': {}
        }
        
        try:
            for col in price_columns:
                cumulative_col = f'{col}_cumulative'
                if cumulative_col in cumulative_returns.columns:
                    cumulative_series = cumulative_returns[cumulative_col].dropna()
                    
                    if len(cumulative_series) == 0:
                        continue
                    
                    # Calculate returns for risk metrics
                    returns = cumulative_series.pct_change().dropna()
                    
                    if len(returns) == 0:
                        continue
                    
                    # Calculate drawdown
                    running_max = cumulative_series.expanding().max()
                    drawdown = (cumulative_series - running_max) / running_max
                    
                    # Risk metrics
                    risk_metrics = {
                        'maximum_drawdown': float(drawdown.min()),
                        'calmar_ratio': self._calculate_calmar_ratio(returns, drawdown.min()),
                        'sterling_ratio': self._calculate_sterling_ratio(returns, drawdown),
                        'burke_ratio': self._calculate_burke_ratio(returns, drawdown),
                        'pain_index': self._calculate_pain_index(drawdown),
                        'ulcer_index': self._calculate_ulcer_index(drawdown)
                    }
                    
                    results['risk_metrics'][col] = risk_metrics
            
            # Risk comparison
            if len(results['risk_metrics']) > 1:
                risk_comparison = {}
                for col, metrics in results['risk_metrics'].items():
                    risk_comparison[col] = {
                        'risk_ranking': self._rank_by_risk(results['risk_metrics']),
                        'risk_level': self._assess_risk_level(metrics['maximum_drawdown']),
                        'risk_score': self._calculate_risk_score(metrics)
                    }
                
                results['risk_comparison'] = risk_comparison
        
        except Exception as e:
            self.logger.error(f"Error calculating risk metrics: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_drawdown_patterns(self, cumulative_returns: pd.DataFrame,
                                 price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze drawdown patterns and trends.
        
        Args:
            cumulative_returns: DataFrame with cumulative returns
            price_columns: List of price columns
            
        Returns:
            Dictionary with drawdown pattern analysis
        """
        results = {
            'pattern_analysis': {},
            'trend_analysis': {},
            'seasonality_analysis': {}
        }
        
        try:
            for col in price_columns:
                cumulative_col = f'{col}_cumulative'
                if cumulative_col in cumulative_returns.columns:
                    cumulative_series = cumulative_returns[cumulative_col].dropna()
                    
                    if len(cumulative_series) == 0:
                        continue
                    
                    # Pattern analysis
                    pattern_analysis = {
                        'drawdown_trend': self._analyze_drawdown_trend(cumulative_series),
                        'drawdown_volatility': self._analyze_drawdown_volatility(cumulative_series),
                        'drawdown_frequency_trend': self._analyze_drawdown_frequency_trend(cumulative_series)
                    }
                    
                    results['pattern_analysis'][col] = pattern_analysis
        
        except Exception as e:
            self.logger.error(f"Error analyzing drawdown patterns: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _identify_drawdown_periods(self, cumulative_series: pd.Series) -> List[Dict[str, Any]]:
        """Identify individual drawdown periods."""
        try:
            # Calculate running maximum
            running_max = cumulative_series.expanding().max()
            drawdown = (cumulative_series - running_max) / running_max
            
            # Find drawdown periods
            drawdown_periods = []
            in_drawdown = False
            start_date = None
            
            for date, dd in drawdown.items():
                if dd < 0 and not in_drawdown:
                    # Start of drawdown
                    in_drawdown = True
                    start_date = date
                elif dd >= 0 and in_drawdown:
                    # End of drawdown
                    in_drawdown = False
                    if start_date is not None:
                        duration = (date - start_date).days if hasattr(date, 'days') else 1
                        max_dd = drawdown.loc[start_date:date].min()
                        drawdown_periods.append({
                            'start_date': str(start_date),
                            'end_date': str(date),
                            'duration': duration,
                            'maximum_drawdown': float(max_dd),
                            'recovery_time': duration
                        })
            
            # Handle case where series ends in drawdown
            if in_drawdown and start_date is not None:
                duration = (cumulative_series.index[-1] - start_date).days if hasattr(cumulative_series.index[-1], 'days') else 1
                max_dd = drawdown.loc[start_date:].min()
                drawdown_periods.append({
                    'start_date': str(start_date),
                    'end_date': 'ongoing',
                    'duration': duration,
                    'maximum_drawdown': float(max_dd),
                    'recovery_time': 'ongoing'
                })
            
            return drawdown_periods
        
        except Exception as e:
            self.logger.error(f"Error identifying drawdown periods: {str(e)}")
            return []
    
    def _find_worst_drawdown_period(self, drawdown: pd.Series) -> Dict[str, Any]:
        """Find the worst drawdown period."""
        try:
            worst_dd = drawdown.min()
            worst_date = drawdown.idxmin()
            
            return {
                'date': str(worst_date),
                'drawdown': float(worst_dd),
                'drawdown_percentage': float(worst_dd * 100)
            }
        except:
            return {'date': 'unknown', 'drawdown': 0.0, 'drawdown_percentage': 0.0}
    
    def _assess_drawdown_severity(self, max_drawdown: float) -> str:
        """Assess drawdown severity."""
        abs_dd = abs(max_drawdown)
        
        if abs_dd > 0.5:
            return 'extreme'
        elif abs_dd > 0.3:
            return 'severe'
        elif abs_dd > 0.2:
            return 'moderate'
        elif abs_dd > 0.1:
            return 'mild'
        else:
            return 'minimal'
    
    def _calculate_time_in_drawdown(self, drawdown: pd.Series) -> int:
        """Calculate current time in drawdown."""
        try:
            # Find the last time the series was at a new high
            running_max = drawdown.expanding().max()
            last_high = drawdown[running_max == 0].index[-1] if (running_max == 0).any() else drawdown.index[0]
            
            # Calculate time since last high
            current_time = drawdown.index[-1]
            if hasattr(current_time, 'days'):
                return (current_time - last_high).days
            else:
                return len(drawdown.loc[last_high:]) - 1
        except:
            return 0
    
    def _assess_drawdown_clustering(self, drawdown_periods: List[Dict[str, Any]]) -> str:
        """Assess if drawdowns are clustered."""
        try:
            if len(drawdown_periods) < 2:
                return 'insufficient_data'
            
            # Calculate time between drawdowns
            periods = [period['duration'] for period in drawdown_periods]
            avg_period = np.mean(periods)
            period_std = np.std(periods)
            
            # High coefficient of variation suggests clustering
            cv = period_std / avg_period if avg_period > 0 else 0
            
            if cv > 1.0:
                return 'highly_clustered'
            elif cv > 0.5:
                return 'moderately_clustered'
            else:
                return 'randomly_distributed'
        except:
            return 'unknown'
    
    def _calculate_recovery_metrics(self, cumulative_series: pd.Series) -> Dict[str, Any]:
        """Calculate recovery metrics."""
        try:
            # Calculate drawdown
            running_max = cumulative_series.expanding().max()
            drawdown = (cumulative_series - running_max) / running_max
            
            # Find recovery periods
            recovery_periods = []
            in_drawdown = False
            drawdown_start = None
            
            for date, dd in drawdown.items():
                if dd < 0 and not in_drawdown:
                    in_drawdown = True
                    drawdown_start = date
                elif dd >= 0 and in_drawdown:
                    in_drawdown = False
                    if drawdown_start is not None:
                        recovery_time = (date - drawdown_start).days if hasattr(date, 'days') else 1
                        recovery_periods.append(recovery_time)
            
            if not recovery_periods:
                return {
                    'fast_recoveries': 0,
                    'slow_recoveries': 0,
                    'average_recovery_time': 0.0,
                    'recovery_success_rate': 0.0
                }
            
            # Calculate metrics
            fast_recoveries = len([r for r in recovery_periods if r <= 5])
            slow_recoveries = len([r for r in recovery_periods if r > 20])
            avg_recovery = np.mean(recovery_periods)
            
            # Recovery success rate (recoveries vs ongoing drawdowns)
            total_drawdowns = len(recovery_periods) + (1 if in_drawdown else 0)
            success_rate = len(recovery_periods) / total_drawdowns if total_drawdowns > 0 else 0
            
            return {
                'fast_recoveries': fast_recoveries,
                'slow_recoveries': slow_recoveries,
                'average_recovery_time': float(avg_recovery),
                'recovery_success_rate': float(success_rate)
            }
        except:
            return {
                'fast_recoveries': 0,
                'slow_recoveries': 0,
                'average_recovery_time': 0.0,
                'recovery_success_rate': 0.0
            }
    
    def _assess_current_recovery_status(self, cumulative_series: pd.Series) -> str:
        """Assess current recovery status."""
        try:
            # Calculate current drawdown
            running_max = cumulative_series.expanding().max()
            current_dd = (cumulative_series.iloc[-1] - running_max.iloc[-1]) / running_max.iloc[-1]
            
            if current_dd >= 0:
                return 'at_high'
            elif current_dd > -0.05:
                return 'near_recovery'
            elif current_dd > -0.1:
                return 'shallow_drawdown'
            elif current_dd > -0.2:
                return 'moderate_drawdown'
            else:
                return 'deep_drawdown'
        except:
            return 'unknown'
    
    def _calculate_recovery_momentum(self, cumulative_series: pd.Series) -> str:
        """Calculate recovery momentum."""
        try:
            if len(cumulative_series) < 10:
                return 'insufficient_data'
            
            # Calculate recent performance
            recent_performance = cumulative_series.tail(10).pct_change().mean()
            
            if recent_performance > 0.01:
                return 'strong_positive'
            elif recent_performance > 0.005:
                return 'positive'
            elif recent_performance > -0.005:
                return 'neutral'
            elif recent_performance > -0.01:
                return 'negative'
            else:
                return 'strong_negative'
        except:
            return 'unknown'
    
    def _assess_recovery_confidence(self, cumulative_series: pd.Series) -> str:
        """Assess recovery confidence."""
        try:
            # Calculate volatility of recent returns
            recent_returns = cumulative_series.tail(20).pct_change().dropna()
            
            if len(recent_returns) < 5:
                return 'insufficient_data'
            
            volatility = recent_returns.std()
            
            if volatility < 0.01:
                return 'high_confidence'
            elif volatility < 0.02:
                return 'moderate_confidence'
            elif volatility < 0.05:
                return 'low_confidence'
            else:
                return 'very_low_confidence'
        except:
            return 'unknown'
    
    def _calculate_calmar_ratio(self, returns: pd.Series, max_dd: float) -> float:
        """Calculate Calmar ratio."""
        try:
            if max_dd == 0:
                return float('inf')
            
            annual_return = returns.mean() * 252
            return annual_return / abs(max_dd)
        except:
            return 0.0
    
    def _calculate_sterling_ratio(self, returns: pd.Series, drawdown: pd.Series) -> float:
        """Calculate Sterling ratio."""
        try:
            if len(returns) == 0:
                return 0.0
            
            annual_return = returns.mean() * 252
            avg_drawdown = drawdown[drawdown < 0].mean()
            
            if avg_drawdown == 0:
                return float('inf')
            
            return annual_return / abs(avg_drawdown)
        except:
            return 0.0
    
    def _calculate_burke_ratio(self, returns: pd.Series, drawdown: pd.Series) -> float:
        """Calculate Burke ratio."""
        try:
            if len(returns) == 0:
                return 0.0
            
            annual_return = returns.mean() * 252
            drawdown_squared = (drawdown[drawdown < 0] ** 2).sum()
            
            if drawdown_squared == 0:
                return float('inf')
            
            return annual_return / np.sqrt(drawdown_squared)
        except:
            return 0.0
    
    def _calculate_pain_index(self, drawdown: pd.Series) -> float:
        """Calculate Pain Index."""
        try:
            return float(drawdown[drawdown < 0].abs().mean())
        except:
            return 0.0
    
    def _calculate_ulcer_index(self, drawdown: pd.Series) -> float:
        """Calculate Ulcer Index."""
        try:
            return float(np.sqrt((drawdown ** 2).mean()))
        except:
            return 0.0
    
    def _rank_by_risk(self, risk_metrics: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
        """Rank by risk level."""
        try:
            risk_scores = {col: metrics['maximum_drawdown'] for col, metrics in risk_metrics.items()}
            sorted_cols = sorted(risk_scores.items(), key=lambda x: x[1])
            return {col: rank + 1 for rank, (col, _) in enumerate(sorted_cols)}
        except:
            return {}
    
    def _assess_risk_level(self, max_drawdown: float) -> str:
        """Assess risk level based on maximum drawdown."""
        abs_dd = abs(max_drawdown)
        
        if abs_dd > 0.4:
            return 'very_high'
        elif abs_dd > 0.2:
            return 'high'
        elif abs_dd > 0.1:
            return 'moderate'
        elif abs_dd > 0.05:
            return 'low'
        else:
            return 'very_low'
    
    def _calculate_risk_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall risk score."""
        try:
            # Weighted combination of risk metrics
            max_dd = abs(metrics.get('maximum_drawdown', 0))
            calmar = metrics.get('calmar_ratio', 0)
            pain = metrics.get('pain_index', 0)
            
            # Normalize and combine
            risk_score = (max_dd * 0.4 + pain * 0.3 + (1 / (1 + calmar)) * 0.3)
            return min(1.0, max(0.0, risk_score))
        except:
            return 0.0
    
    def _analyze_drawdown_trend(self, cumulative_series: pd.Series) -> str:
        """Analyze drawdown trend over time."""
        try:
            if len(cumulative_series) < 20:
                return 'insufficient_data'
            
            # Calculate rolling maximum drawdown
            running_max = cumulative_series.expanding().max()
            drawdown = (cumulative_series - running_max) / running_max
            
            # Analyze trend in drawdown severity
            recent_dd = drawdown.tail(20)
            early_dd = drawdown.head(20)
            
            recent_avg = recent_dd.mean()
            early_avg = early_dd.mean()
            
            if recent_avg > early_avg + 0.01:
                return 'increasing'
            elif recent_avg < early_avg - 0.01:
                return 'decreasing'
            else:
                return 'stable'
        except:
            return 'unknown'
    
    def _analyze_drawdown_volatility(self, cumulative_series: pd.Series) -> str:
        """Analyze drawdown volatility."""
        try:
            if len(cumulative_series) < 10:
                return 'insufficient_data'
            
            # Calculate drawdown volatility
            running_max = cumulative_series.expanding().max()
            drawdown = (cumulative_series - running_max) / running_max
            
            dd_volatility = drawdown.std()
            
            if dd_volatility > 0.1:
                return 'high_volatility'
            elif dd_volatility > 0.05:
                return 'moderate_volatility'
            else:
                return 'low_volatility'
        except:
            return 'unknown'
    
    def _analyze_drawdown_frequency_trend(self, cumulative_series: pd.Series) -> str:
        """Analyze trend in drawdown frequency."""
        try:
            if len(cumulative_series) < 40:
                return 'insufficient_data'
            
            # Calculate rolling maximum
            running_max = cumulative_series.expanding().max()
            drawdown = (cumulative_series - running_max) / running_max
            
            # Split into early and recent periods
            mid_point = len(drawdown) // 2
            early_dd = drawdown.head(mid_point)
            recent_dd = drawdown.tail(mid_point)
            
            # Count drawdown periods
            early_frequency = (early_dd < 0).sum() / len(early_dd)
            recent_frequency = (recent_dd < 0).sum() / len(recent_dd)
            
            if recent_frequency > early_frequency + 0.1:
                return 'increasing_frequency'
            elif recent_frequency < early_frequency - 0.1:
                return 'decreasing_frequency'
            else:
                return 'stable_frequency'
        except:
            return 'unknown'
    
    def _generate_drawdown_recommendations(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations based on drawdown analysis."""
        recommendations = {
            'risk_management': [],
            'position_sizing': [],
            'recovery_strategies': [],
            'monitoring_suggestions': []
        }
        
        try:
            # Risk management recommendations
            recommendations['risk_management'].append("Monitor maximum drawdown levels for risk control")
            recommendations['risk_management'].append("Set drawdown limits based on risk tolerance")
            
            # Position sizing recommendations
            recommendations['position_sizing'].append("Adjust position sizes based on drawdown history")
            recommendations['position_sizing'].append("Consider reducing exposure during high drawdown periods")
            
            # Recovery strategies
            recommendations['recovery_strategies'].append("Implement recovery strategies for deep drawdowns")
            recommendations['recovery_strategies'].append("Monitor recovery momentum and adjust strategies accordingly")
            
            # Monitoring suggestions
            recommendations['monitoring_suggestions'].append("Track drawdown duration and recovery times")
            recommendations['monitoring_suggestions'].append("Monitor drawdown patterns for early warning signals")
        
        except Exception as e:
            recommendations['error'] = str(e)
        
        return recommendations
    
    def get_analysis_summary(self, results: Dict[str, Any]) -> str:
        """Get a summary of drawdown analysis results."""
        summary_parts = []
        
        try:
            # Maximum drawdown summary
            if 'maximum_drawdown' in results:
                md = results['maximum_drawdown']
                if 'maximum_drawdowns' in md:
                    for col, analysis in md['maximum_drawdowns'].items():
                        max_dd = analysis.get('maximum_drawdown_percentage', 0)
                        summary_parts.append(f"Max DD ({col}): {max_dd:.1f}%")
            
            # Drawdown duration summary
            if 'drawdown_duration' in results:
                dd = results['drawdown_duration']
                if 'duration_statistics' in dd:
                    for col, stats in dd['duration_statistics'].items():
                        avg_duration = stats.get('average_duration', 0)
                        summary_parts.append(f"Avg Duration ({col}): {avg_duration:.0f} days")
            
            # Recovery analysis summary
            if 'recovery_analysis' in results:
                ra = results['recovery_analysis']
                if 'recovery_analysis' in ra:
                    for col, analysis in ra['recovery_analysis'].items():
                        status = analysis.get('current_recovery_status', 'unknown')
                        summary_parts.append(f"Recovery Status ({col}): {status}")
        
        except Exception as e:
            summary_parts.append(f"Error generating summary: {str(e)}")
        
        return "\n".join(summary_parts) if summary_parts else "No drawdown analysis results available"
