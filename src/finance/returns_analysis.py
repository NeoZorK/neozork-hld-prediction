"""
Returns Analysis Module

This module provides comprehensive returns analysis including simple returns,
log returns, and cumulative returns for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging
from scipy import stats
from .color_utils import ColorUtils


class ReturnsAnalysis:
    """Comprehensive returns analysis for financial data."""
    
    def __init__(self):
        """Initialize the returns analyzer."""
        self.logger = logging.getLogger(__name__)
    
    def analyze_returns(self, data: pd.DataFrame, 
                       numeric_columns: List[str]) -> Dict[str, Any]:
        """
        Perform comprehensive returns analysis.
        
        Args:
            data: DataFrame with financial data
            numeric_columns: List of numeric columns to analyze
            
        Returns:
            Dictionary with returns analysis results
        """
        results = {
            'simple_returns': {},
            'log_returns': {},
            'cumulative_returns': {},
            'returns_statistics': {},
            'returns_distribution': {},
            'returns_risk_metrics': {},
            'recommendations': {}
        }
        
        try:
            # Identify price columns for returns calculation
            price_columns = self._identify_price_columns(data, numeric_columns)
            
            if not price_columns:
                results['error'] = "No price columns identified for returns analysis"
                return results
            
            # Calculate different types of returns
            returns_data = self._calculate_all_returns(data, price_columns)
            
            if returns_data.empty:
                results['error'] = "Unable to calculate returns"
                return results
            
            # Simple returns analysis
            results['simple_returns'] = self._analyze_simple_returns(
                returns_data, price_columns
            )
            
            # Log returns analysis
            results['log_returns'] = self._analyze_log_returns(
                returns_data, price_columns
            )
            
            # Cumulative returns analysis
            results['cumulative_returns'] = self._analyze_cumulative_returns(
                returns_data, price_columns
            )
            
            # Returns statistics
            results['returns_statistics'] = self._calculate_returns_statistics(
                returns_data, price_columns
            )
            
            # Returns distribution analysis
            results['returns_distribution'] = self._analyze_returns_distribution(
                returns_data, price_columns
            )
            
            # Risk metrics
            results['returns_risk_metrics'] = self._calculate_risk_metrics(
                returns_data, price_columns
            )
            
            # Generate recommendations
            results['recommendations'] = self._generate_returns_recommendations(
                results
            )
            
        except Exception as e:
            self.logger.error(f"Error in returns analysis: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _identify_price_columns(self, data: pd.DataFrame, 
                               numeric_columns: List[str]) -> List[str]:
        """
        Identify price columns suitable for returns analysis.
        
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
    
    def _calculate_all_returns(self, data: pd.DataFrame, 
                              price_columns: List[str]) -> pd.DataFrame:
        """
        Calculate all types of returns for analysis.
        
        Args:
            data: DataFrame with price data
            price_columns: List of price columns
            
        Returns:
            DataFrame with returns data
        """
        returns_data = pd.DataFrame(index=data.index)
        
        for col in price_columns:
            if col in data.columns:
                price_series = data[col].dropna()
                
                if len(price_series) > 1:
                    # Simple returns (percentage changes)
                    simple_returns = price_series.pct_change()
                    returns_data[f'{col}_simple_returns'] = simple_returns
                    
                    # Log returns
                    log_returns = np.log(price_series / price_series.shift(1))
                    returns_data[f'{col}_log_returns'] = log_returns
                    
                    # Cumulative simple returns
                    cumulative_simple = (1 + simple_returns).cumprod() - 1
                    returns_data[f'{col}_cumulative_simple'] = cumulative_simple
                    
                    # Cumulative log returns
                    cumulative_log = log_returns.cumsum()
                    returns_data[f'{col}_cumulative_log'] = cumulative_log
        
        return returns_data.dropna()
    
    def _analyze_simple_returns(self, returns_data: pd.DataFrame,
                               price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze simple returns (percentage changes).
        
        Args:
            returns_data: DataFrame with returns data
            price_columns: List of price columns
            
        Returns:
            Dictionary with simple returns analysis
        """
        results = {
            'returns_statistics': {},
            'returns_analysis': {},
            'returns_trends': {}
        }
        
        try:
            for col in price_columns:
                returns_col = f'{col}_simple_returns'
                if returns_col in returns_data.columns:
                    col_returns = returns_data[returns_col].dropna()
                    
                    if len(col_returns) == 0:
                        continue
                    
                    # Basic statistics
                    stats_dict = {
                        'count': len(col_returns),
                        'mean': float(col_returns.mean()),
                        'median': float(col_returns.median()),
                        'std': float(col_returns.std()),
                        'min': float(col_returns.min()),
                        'max': float(col_returns.max()),
                        'skewness': float(col_returns.skew()),
                        'kurtosis': float(col_returns.kurtosis()),
                        'q25': float(col_returns.quantile(0.25)),
                        'q75': float(col_returns.quantile(0.75))
                    }
                    
                    results['returns_statistics'][col] = stats_dict
                    
                    # Returns analysis
                    positive_returns = (col_returns > 0).sum()
                    negative_returns = (col_returns < 0).sum()
                    zero_returns = (col_returns == 0).sum()
                    
                    analysis_dict = {
                        'positive_returns_count': int(positive_returns),
                        'negative_returns_count': int(negative_returns),
                        'zero_returns_count': int(zero_returns),
                        'positive_returns_percentage': float(positive_returns / len(col_returns) * 100),
                        'negative_returns_percentage': float(negative_returns / len(col_returns) * 100),
                        'win_rate': float(positive_returns / len(col_returns) * 100),
                        'average_positive_return': float(col_returns[col_returns > 0].mean()) if positive_returns > 0 else 0.0,
                        'average_negative_return': float(col_returns[col_returns < 0].mean()) if negative_returns > 0 else 0.0
                    }
                    
                    results['returns_analysis'][col] = analysis_dict
                    
                    # Returns trends
                    if len(col_returns) >= 20:
                        recent_returns = col_returns.tail(20)
                        historical_returns = col_returns.head(-20)
                        
                        trend_dict = {
                            'recent_mean': float(recent_returns.mean()),
                            'historical_mean': float(historical_returns.mean()),
                            'trend_direction': 'improving' if recent_returns.mean() > historical_returns.mean() else 'declining',
                            'trend_strength': float(abs(recent_returns.mean() - historical_returns.mean())),
                            'volatility_change': float(recent_returns.std() - historical_returns.std())
                        }
                        
                        results['returns_trends'][col] = trend_dict
        
        except Exception as e:
            self.logger.error(f"Error analyzing simple returns: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_log_returns(self, returns_data: pd.DataFrame,
                            price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze log returns.
        
        Args:
            returns_data: DataFrame with returns data
            price_columns: List of price columns
            
        Returns:
            Dictionary with log returns analysis
        """
        results = {
            'log_returns_statistics': {},
            'log_returns_analysis': {},
            'log_returns_advantages': {}
        }
        
        try:
            for col in price_columns:
                returns_col = f'{col}_log_returns'
                if returns_col in returns_data.columns:
                    col_returns = returns_data[returns_col].dropna()
                    
                    if len(col_returns) == 0:
                        continue
                    
                    # Log returns statistics
                    stats_dict = {
                        'count': len(col_returns),
                        'mean': float(col_returns.mean()),
                        'median': float(col_returns.median()),
                        'std': float(col_returns.std()),
                        'min': float(col_returns.min()),
                        'max': float(col_returns.max()),
                        'skewness': float(col_returns.skew()),
                        'kurtosis': float(col_returns.kurtosis()),
                        'variance': float(col_returns.var())
                    }
                    
                    results['log_returns_statistics'][col] = stats_dict
                    
                    # Log returns analysis
                    analysis_dict = {
                        'normality_test': self._test_normality(col_returns),
                        'stationarity_test': self._test_stationarity(col_returns),
                        'autocorrelation': float(col_returns.autocorr(lag=1)) if len(col_returns) > 1 else 0.0,
                        'volatility_clustering': self._assess_volatility_clustering(col_returns)
                    }
                    
                    results['log_returns_analysis'][col] = analysis_dict
                    
                    # Log returns advantages
                    advantages_dict = {
                        'additive_property': True,  # Log returns are additive
                        'symmetric_distribution': abs(col_returns.skew()) < 0.5,
                        'better_statistical_properties': abs(col_returns.skew()) < 1.0 and col_returns.kurtosis() < 3.0,
                        'time_aggregation': True  # Log returns aggregate properly over time
                    }
                    
                    results['log_returns_advantages'][col] = advantages_dict
        
        except Exception as e:
            self.logger.error(f"Error analyzing log returns: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_cumulative_returns(self, returns_data: pd.DataFrame,
                                  price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze cumulative returns.
        
        Args:
            returns_data: DataFrame with returns data
            price_columns: List of price columns
            
        Returns:
            Dictionary with cumulative returns analysis
        """
        results = {
            'cumulative_simple_returns': {},
            'cumulative_log_returns': {},
            'performance_metrics': {}
        }
        
        try:
            for col in price_columns:
                simple_col = f'{col}_cumulative_simple'
                log_col = f'{col}_cumulative_log'
                
                if simple_col in returns_data.columns:
                    simple_cumulative = returns_data[simple_col].dropna()
                    
                    if len(simple_cumulative) > 0:
                        # Cumulative simple returns analysis
                        simple_analysis = {
                            'total_return': float(simple_cumulative.iloc[-1]),
                            'max_return': float(simple_cumulative.max()),
                            'min_return': float(simple_cumulative.min()),
                            'final_return': float(simple_cumulative.iloc[-1]),
                            'return_volatility': float(simple_cumulative.std()),
                            'positive_periods': int((simple_cumulative > 0).sum()),
                            'negative_periods': int((simple_cumulative < 0).sum())
                        }
                        
                        results['cumulative_simple_returns'][col] = simple_analysis
                
                if log_col in returns_data.columns:
                    log_cumulative = returns_data[log_col].dropna()
                    
                    if len(log_cumulative) > 0:
                        # Cumulative log returns analysis
                        log_analysis = {
                            'total_log_return': float(log_cumulative.iloc[-1]),
                            'max_log_return': float(log_cumulative.max()),
                            'min_log_return': float(log_cumulative.min()),
                            'log_return_volatility': float(log_cumulative.std()),
                            'log_return_trend': 'increasing' if log_cumulative.iloc[-1] > log_cumulative.iloc[0] else 'decreasing'
                        }
                        
                        results['cumulative_log_returns'][col] = log_analysis
                
                # Performance metrics
                if simple_col in returns_data.columns and log_col in returns_data.columns:
                    simple_cumulative = returns_data[simple_col].dropna()
                    log_cumulative = returns_data[log_col].dropna()
                    
                    if len(simple_cumulative) > 0 and len(log_cumulative) > 0:
                        # Calculate annualized returns (assuming daily data)
                        periods = len(simple_cumulative)
                        annualized_simple = (1 + simple_cumulative.iloc[-1]) ** (252 / periods) - 1
                        annualized_log = log_cumulative.iloc[-1] * (252 / periods)
                        
                        performance_metrics = {
                            'annualized_simple_return': float(annualized_simple),
                            'annualized_log_return': float(annualized_log),
                            'total_periods': periods,
                            'return_consistency': self._assess_return_consistency(simple_cumulative),
                            'performance_rating': self._rate_performance(simple_cumulative.iloc[-1])
                        }
                        
                        results['performance_metrics'][col] = performance_metrics
        
        except Exception as e:
            self.logger.error(f"Error analyzing cumulative returns: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _calculate_returns_statistics(self, returns_data: pd.DataFrame,
                                     price_columns: List[str]) -> Dict[str, Any]:
        """
        Calculate comprehensive returns statistics.
        
        Args:
            returns_data: DataFrame with returns data
            price_columns: List of price columns
            
        Returns:
            Dictionary with returns statistics
        """
        results = {
            'overall_statistics': {},
            'correlation_analysis': {},
            'returns_comparison': {}
        }
        
        try:
            # Overall statistics
            all_returns = []
            for col in price_columns:
                returns_col = f'{col}_simple_returns'
                if returns_col in returns_data.columns:
                    all_returns.extend(returns_data[returns_col].dropna().tolist())
            
            if all_returns:
                all_returns_series = pd.Series(all_returns)
                results['overall_statistics'] = {
                    'total_observations': len(all_returns_series),
                    'overall_mean': float(all_returns_series.mean()),
                    'overall_std': float(all_returns_series.std()),
                    'overall_skewness': float(all_returns_series.skew()),
                    'overall_kurtosis': float(all_returns_series.kurtosis()),
                    'overall_min': float(all_returns_series.min()),
                    'overall_max': float(all_returns_series.max())
                }
            
            # Correlation analysis between different returns
            returns_cols = [f'{col}_simple_returns' for col in price_columns 
                           if f'{col}_simple_returns' in returns_data.columns]
            
            if len(returns_cols) > 1:
                correlation_matrix = returns_data[returns_cols].corr()
                results['correlation_analysis'] = {
                    'correlation_matrix': correlation_matrix.to_dict(),
                    'average_correlation': float(correlation_matrix.mean().mean()),
                    'max_correlation': float(correlation_matrix.max().max()),
                    'min_correlation': float(correlation_matrix.min().min())
                }
            
            # Returns comparison
            if len(price_columns) > 1:
                comparison = {}
                for col in price_columns:
                    returns_col = f'{col}_simple_returns'
                    if returns_col in returns_data.columns:
                        col_returns = returns_data[returns_col].dropna()
                        if len(col_returns) > 0:
                            comparison[col] = {
                                'mean_return': float(col_returns.mean()),
                                'std_return': float(col_returns.std()),
                                'sharpe_ratio': float(col_returns.mean() / col_returns.std()) if col_returns.std() > 0 else 0.0,
                                'total_return': float((1 + col_returns).prod() - 1)
                            }
                
                results['returns_comparison'] = comparison
        
        except Exception as e:
            self.logger.error(f"Error calculating returns statistics: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_returns_distribution(self, returns_data: pd.DataFrame,
                                    price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze returns distribution characteristics.
        
        Args:
            returns_data: DataFrame with returns data
            price_columns: List of price columns
            
        Returns:
            Dictionary with returns distribution analysis
        """
        results = {
            'distribution_tests': {},
            'distribution_characteristics': {},
            'normality_assessment': {}
        }
        
        try:
            for col in price_columns:
                returns_col = f'{col}_simple_returns'
                if returns_col in returns_data.columns:
                    col_returns = returns_data[returns_col].dropna()
                    
                    if len(col_returns) < 3:
                        continue
                    
                    # Distribution tests
                    distribution_tests = {
                        'shapiro_wilk': self._shapiro_wilk_test(col_returns),
                        'jarque_bera': self._jarque_bera_test(col_returns),
                        'anderson_darling': self._anderson_darling_test(col_returns)
                    }
                    
                    results['distribution_tests'][col] = distribution_tests
                    
                    # Distribution characteristics
                    characteristics = {
                        'skewness': float(col_returns.skew()),
                        'kurtosis': float(col_returns.kurtosis()),
                        'excess_kurtosis': float(col_returns.kurtosis() - 3),
                        'distribution_type': self._classify_distribution(col_returns),
                        'tail_risk': self._assess_tail_risk(col_returns)
                    }
                    
                    results['distribution_characteristics'][col] = characteristics
                    
                    # Normality assessment
                    normality_assessment = {
                        'is_normal': self._assess_normality(col_returns),
                        'normality_score': self._calculate_normality_score(col_returns),
                        'deviations_from_normality': self._identify_normality_deviations(col_returns)
                    }
                    
                    results['normality_assessment'][col] = normality_assessment
        
        except Exception as e:
            self.logger.error(f"Error analyzing returns distribution: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _calculate_risk_metrics(self, returns_data: pd.DataFrame,
                               price_columns: List[str]) -> Dict[str, Any]:
        """
        Calculate risk metrics for returns.
        
        Args:
            returns_data: DataFrame with returns data
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
                returns_col = f'{col}_simple_returns'
                if returns_col in returns_data.columns:
                    col_returns = returns_data[returns_col].dropna()
                    
                    if len(col_returns) == 0:
                        continue
                    
                    # Calculate risk metrics
                    risk_metrics = {
                        'volatility': float(col_returns.std()),
                        'annualized_volatility': float(col_returns.std() * np.sqrt(252)),
                        'var_95': float(col_returns.quantile(0.05)),
                        'var_99': float(col_returns.quantile(0.01)),
                        'cvar_95': float(col_returns[col_returns <= col_returns.quantile(0.05)].mean()),
                        'cvar_99': float(col_returns[col_returns <= col_returns.quantile(0.01)].mean()),
                        'sharpe_ratio': float(col_returns.mean() / col_returns.std()) if col_returns.std() > 0 else 0.0,
                        'sortino_ratio': self._calculate_sortino_ratio(col_returns),
                        'calmar_ratio': self._calculate_calmar_ratio(col_returns)
                    }
                    
                    results['risk_metrics'][col] = risk_metrics
            
            # Risk comparison
            if len(results['risk_metrics']) > 1:
                risk_comparison = {}
                for col, metrics in results['risk_metrics'].items():
                    risk_comparison[col] = {
                        'volatility_rank': self._rank_by_volatility(results['risk_metrics']),
                        'sharpe_rank': self._rank_by_sharpe(results['risk_metrics']),
                        'risk_level': self._assess_risk_level(metrics['volatility'])
                    }
                
                results['risk_comparison'] = risk_comparison
        
        except Exception as e:
            self.logger.error(f"Error calculating risk metrics: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _test_normality(self, returns: pd.Series) -> Dict[str, Any]:
        """Test normality of returns."""
        try:
            if len(returns) < 3:
                return {'test': 'insufficient_data', 'p_value': 1.0, 'is_normal': False}
            
            # Shapiro-Wilk test for small samples
            if len(returns) <= 5000:
                stat, p_value = stats.shapiro(returns)
                return {'test': 'shapiro_wilk', 'p_value': float(p_value), 'is_normal': p_value > 0.05}
            else:
                # D'Agostino-Pearson test for large samples
                stat, p_value = stats.normaltest(returns)
                return {'test': 'dagostino_pearson', 'p_value': float(p_value), 'is_normal': p_value > 0.05}
        except:
            return {'test': 'error', 'p_value': 1.0, 'is_normal': False}
    
    def _test_stationarity(self, returns: pd.Series) -> Dict[str, Any]:
        """Test stationarity of returns."""
        try:
            # Simple stationarity test using rolling statistics
            if len(returns) < 20:
                return {'test': 'insufficient_data', 'is_stationary': False}
            
            # Calculate rolling mean and std
            rolling_mean = returns.rolling(window=10).mean()
            rolling_std = returns.rolling(window=10).std()
            
            # Check if rolling statistics are relatively stable
            mean_stability = rolling_mean.std() / rolling_mean.mean() if rolling_mean.mean() != 0 else 1
            std_stability = rolling_std.std() / rolling_std.mean() if rolling_std.mean() != 0 else 1
            
            is_stationary = mean_stability < 0.5 and std_stability < 0.5
            
            return {
                'test': 'rolling_statistics',
                'is_stationary': is_stationary,
                'mean_stability': float(mean_stability),
                'std_stability': float(std_stability)
            }
        except:
            return {'test': 'error', 'is_stationary': False}
    
    def _assess_volatility_clustering(self, returns: pd.Series) -> str:
        """Assess volatility clustering in returns."""
        try:
            if len(returns) < 10:
                return 'insufficient_data'
            
            # Calculate rolling volatility
            rolling_vol = returns.rolling(window=5).std()
            vol_autocorr = rolling_vol.autocorr(lag=1)
            
            if pd.isna(vol_autocorr):
                return 'unknown'
            elif vol_autocorr > 0.3:
                return 'strong_clustering'
            elif vol_autocorr > 0.1:
                return 'moderate_clustering'
            else:
                return 'weak_clustering'
        except:
            return 'error'
    
    def _shapiro_wilk_test(self, returns: pd.Series) -> Dict[str, Any]:
        """Perform Shapiro-Wilk test."""
        try:
            if len(returns) < 3 or len(returns) > 5000:
                return {'statistic': 0.0, 'p_value': 1.0, 'is_normal': False}
            
            stat, p_value = stats.shapiro(returns)
            return {
                'statistic': float(stat),
                'p_value': float(p_value),
                'is_normal': p_value > 0.05
            }
        except:
            return {'statistic': 0.0, 'p_value': 1.0, 'is_normal': False}
    
    def _jarque_bera_test(self, returns: pd.Series) -> Dict[str, Any]:
        """Perform Jarque-Bera test."""
        try:
            if len(returns) < 4:
                return {'statistic': 0.0, 'p_value': 1.0, 'is_normal': False}
            
            stat, p_value = stats.jarque_bera(returns)
            return {
                'statistic': float(stat),
                'p_value': float(p_value),
                'is_normal': p_value > 0.05
            }
        except:
            return {'statistic': 0.0, 'p_value': 1.0, 'is_normal': False}
    
    def _anderson_darling_test(self, returns: pd.Series) -> Dict[str, Any]:
        """Perform Anderson-Darling test."""
        try:
            if len(returns) < 3:
                return {'statistic': 0.0, 'critical_values': {}, 'is_normal': False}
            
            result = stats.anderson(returns, dist='norm')
            return {
                'statistic': float(result.statistic),
                'critical_values': {str(level): float(cv) for level, cv in zip(result.significance_level, result.critical_values)},
                'is_normal': result.statistic < result.critical_values[2]  # 5% significance level
            }
        except:
            return {'statistic': 0.0, 'critical_values': {}, 'is_normal': False}
    
    def _classify_distribution(self, returns: pd.Series) -> str:
        """Classify the distribution type."""
        try:
            skewness = abs(returns.skew())
            kurtosis = returns.kurtosis()
            
            if skewness < 0.5 and kurtosis < 3.5:
                return 'approximately_normal'
            elif skewness > 1.0:
                return 'highly_skewed'
            elif kurtosis > 5.0:
                return 'heavy_tailed'
            else:
                return 'non_normal'
        except:
            return 'unknown'
    
    def _assess_tail_risk(self, returns: pd.Series) -> str:
        """Assess tail risk based on kurtosis."""
        try:
            kurtosis = returns.kurtosis()
            
            if kurtosis > 5:
                return 'very_high'
            elif kurtosis > 3:
                return 'high'
            elif kurtosis > 1:
                return 'moderate'
            else:
                return 'low'
        except:
            return 'unknown'
    
    def _assess_normality(self, returns: pd.Series) -> bool:
        """Assess if returns are approximately normal."""
        try:
            skewness = abs(returns.skew())
            kurtosis = returns.kurtosis()
            
            return skewness < 0.5 and kurtosis < 3.5
        except:
            return False
    
    def _calculate_normality_score(self, returns: pd.Series) -> float:
        """Calculate a normality score (0-1)."""
        try:
            skewness = abs(returns.skew())
            kurtosis = abs(returns.kurtosis() - 3)
            
            # Normalize scores (lower is better)
            skew_score = max(0, 1 - skewness / 2)
            kurt_score = max(0, 1 - kurtosis / 5)
            
            return (skew_score + kurt_score) / 2
        except:
            return 0.0
    
    def _identify_normality_deviations(self, returns: pd.Series) -> List[str]:
        """Identify specific deviations from normality."""
        deviations = []
        
        try:
            skewness = returns.skew()
            kurtosis = returns.kurtosis()
            
            if abs(skewness) > 0.5:
                deviations.append(f"Skewness: {skewness:.3f} ({'right' if skewness > 0 else 'left'} skewed)")
            
            if kurtosis > 3.5:
                deviations.append(f"Excess kurtosis: {kurtosis - 3:.3f} (heavy tails)")
            elif kurtosis < 2.5:
                deviations.append(f"Excess kurtosis: {kurtosis - 3:.3f} (light tails)")
        
        except:
            deviations.append("Unable to assess deviations")
        
        return deviations
    
    def _calculate_sortino_ratio(self, returns: pd.Series) -> float:
        """Calculate Sortino ratio."""
        try:
            if len(returns) == 0 or returns.std() == 0:
                return 0.0
            
            downside_returns = returns[returns < 0]
            if len(downside_returns) == 0:
                return float('inf')
            
            downside_std = downside_returns.std()
            if downside_std == 0:
                return float('inf')
            
            return returns.mean() / downside_std
        except:
            return 0.0
    
    def _calculate_calmar_ratio(self, returns: pd.Series) -> float:
        """Calculate Calmar ratio."""
        try:
            if len(returns) == 0:
                return 0.0
            
            # Calculate maximum drawdown
            cumulative = (1 + returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown = abs(drawdown.min())
            
            if max_drawdown == 0:
                return float('inf')
            
            annual_return = returns.mean() * 252
            return annual_return / max_drawdown
        except:
            return 0.0
    
    def _assess_return_consistency(self, cumulative_returns: pd.Series) -> str:
        """Assess return consistency."""
        try:
            if len(cumulative_returns) == 0:
                return 'unknown'
            
            # Calculate rolling returns
            rolling_returns = cumulative_returns.pct_change().dropna()
            
            if len(rolling_returns) == 0:
                return 'unknown'
            
            # Assess consistency based on coefficient of variation
            cv = rolling_returns.std() / abs(rolling_returns.mean()) if rolling_returns.mean() != 0 else float('inf')
            
            if cv < 0.5:
                return 'very_consistent'
            elif cv < 1.0:
                return 'consistent'
            elif cv < 2.0:
                return 'moderately_consistent'
            else:
                return 'inconsistent'
        except:
            return 'unknown'
    
    def _rate_performance(self, total_return: float) -> str:
        """Rate performance based on total return."""
        if total_return > 0.5:
            return 'excellent'
        elif total_return > 0.2:
            return 'good'
        elif total_return > 0.0:
            return 'positive'
        elif total_return > -0.1:
            return 'slightly_negative'
        else:
            return 'poor'
    
    def _rank_by_volatility(self, risk_metrics: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
        """Rank by volatility."""
        try:
            volatility_scores = {col: metrics['volatility'] for col, metrics in risk_metrics.items()}
            sorted_cols = sorted(volatility_scores.items(), key=lambda x: x[1])
            return {col: rank + 1 for rank, (col, _) in enumerate(sorted_cols)}
        except:
            return {}
    
    def _rank_by_sharpe(self, risk_metrics: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
        """Rank by Sharpe ratio."""
        try:
            sharpe_scores = {col: metrics['sharpe_ratio'] for col, metrics in risk_metrics.items()}
            sorted_cols = sorted(sharpe_scores.items(), key=lambda x: x[1], reverse=True)
            return {col: rank + 1 for rank, (col, _) in enumerate(sorted_cols)}
        except:
            return {}
    
    def _assess_risk_level(self, volatility: float) -> str:
        """Assess risk level based on volatility."""
        if volatility > 0.05:
            return 'very_high'
        elif volatility > 0.03:
            return 'high'
        elif volatility > 0.02:
            return 'moderate'
        elif volatility > 0.01:
            return 'low'
        else:
            return 'very_low'
    
    def _generate_returns_recommendations(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations based on returns analysis."""
        recommendations = {
            'return_optimization': [],
            'risk_management': [],
            'portfolio_considerations': [],
            'monitoring_suggestions': []
        }
        
        try:
            # Return optimization recommendations
            recommendations['return_optimization'].append("Monitor return consistency for strategy optimization")
            recommendations['return_optimization'].append("Consider return distribution characteristics for model selection")
            
            # Risk management recommendations
            recommendations['risk_management'].append("Use VaR and CVaR metrics for risk assessment")
            recommendations['risk_management'].append("Monitor tail risk indicators")
            
            # Portfolio considerations
            recommendations['portfolio_considerations'].append("Diversify across different return characteristics")
            recommendations['portfolio_considerations'].append("Consider correlation between different assets")
            
            # Monitoring suggestions
            recommendations['monitoring_suggestions'].append("Track return trends and consistency")
            recommendations['monitoring_suggestions'].append("Monitor risk-adjusted returns (Sharpe ratio)")
        
        except Exception as e:
            recommendations['error'] = str(e)
        
        return recommendations
    
    def get_analysis_summary(self, results: Dict[str, Any]) -> str:
        """Get a summary of returns analysis results."""
        summary_parts = []
        
        try:
            # Simple returns summary
            if 'simple_returns' in results:
                sr = results['simple_returns']
                if 'returns_analysis' in sr:
                    for col, analysis in sr['returns_analysis'].items():
                        win_rate = analysis.get('win_rate', 0)
                        summary_parts.append(f"Win Rate ({col}): {win_rate:.1f}%")
            
            # Cumulative returns summary
            if 'cumulative_returns' in results:
                cr = results['cumulative_returns']
                if 'cumulative_simple_returns' in cr:
                    for col, analysis in cr['cumulative_simple_returns'].items():
                        total_return = analysis.get('total_return', 0)
                        summary_parts.append(f"Total Return ({col}): {total_return:.1%}")
            
            # Risk metrics summary
            if 'returns_risk_metrics' in results:
                rm = results['returns_risk_metrics']
                if 'risk_metrics' in rm:
                    for col, metrics in rm['risk_metrics'].items():
                        sharpe = metrics.get('sharpe_ratio', 0)
                        summary_parts.append(f"Sharpe Ratio ({col}): {sharpe:.2f}")
        
        except Exception as e:
            summary_parts.append(f"Error generating summary: {str(e)}")
        
        return " | ".join(summary_parts) if summary_parts else "No returns analysis results available"
