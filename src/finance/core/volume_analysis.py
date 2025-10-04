"""
Volume Analysis Module

This module provides volume analysis functionality for financial data,
including volume patterns, anomalies, and price-volume relationships.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import logging


class VolumeAnalyzer:
    """Analyzes trading volume patterns and relationships."""
    
    def __init__(self):
        """Initialize the volume analyzer."""
        self.logger = logging.getLogger(__name__)
    
    def analyze_volume_patterns(self, data: pd.DataFrame,
                              volume_col: str = 'Volume',
                              price_col: str = 'Close') -> Dict[str, Any]:
        """
        Analyze volume patterns and trends.
        
        Args:
            data: DataFrame with volume and price data
            volume_col: Name of the volume column
            price_col: Name of the price column
            
        Returns:
            Dictionary with volume pattern analysis
        """
        results = {
            'volume_statistics': {},
            'volume_trends': {},
            'volume_anomalies': {},
            'volume_patterns': {}
        }
        
        try:
            if volume_col not in data.columns:
                results['error'] = f"Volume column '{volume_col}' not found"
                return results
            
            volume_data = data[volume_col].dropna()
            
            if len(volume_data) == 0:
                results['error'] = "No volume data available"
                return results
            
            # Basic volume statistics
            results['volume_statistics'] = {
                'total_volume': float(volume_data.sum()),
                'mean_volume': float(volume_data.mean()),
                'median_volume': float(volume_data.median()),
                'std_volume': float(volume_data.std()),
                'min_volume': float(volume_data.min()),
                'max_volume': float(volume_data.max()),
                'volume_range': float(volume_data.max() - volume_data.min()),
                'zero_volume_count': int((volume_data == 0).sum()),
                'zero_volume_percentage': float((volume_data == 0).sum() / len(volume_data) * 100)
            }
            
            # Volume trends
            if len(volume_data) > 1:
                volume_changes = volume_data.pct_change().dropna()
                results['volume_trends'] = {
                    'mean_volume_change': float(volume_changes.mean()),
                    'std_volume_change': float(volume_changes.std()),
                    'max_volume_increase': float(volume_changes.max()),
                    'max_volume_decrease': float(volume_changes.min()),
                    'positive_change_count': int((volume_changes > 0).sum()),
                    'negative_change_count': int((volume_changes < 0).sum()),
                    'volume_volatility': float(volume_changes.std())
                }
            
            # Volume anomalies (spikes)
            volume_mean = volume_data.mean()
            volume_std = volume_data.std()
            volume_threshold = volume_mean + 2 * volume_std
            
            volume_spikes = volume_data[volume_data > volume_threshold]
            results['volume_anomalies'] = {
                'spike_threshold': float(volume_threshold),
                'spike_count': len(volume_spikes),
                'spike_percentage': float(len(volume_spikes) / len(volume_data) * 100),
                'largest_spike': float(volume_spikes.max()) if len(volume_spikes) > 0 else 0.0,
                'spike_details': [
                    {
                        'index': idx,
                        'volume': float(vol),
                        'deviation': float((vol - volume_mean) / volume_std)
                    }
                    for idx, vol in volume_spikes.items()
                ]
            }
            
            # Volume patterns
            if len(volume_data) >= 20:  # Need sufficient data for pattern analysis
                # Calculate moving averages
                volume_ma_5 = volume_data.rolling(window=5).mean()
                volume_ma_20 = volume_data.rolling(window=20).mean()
                
                # Volume above/below moving averages
                above_ma5 = (volume_data > volume_ma_5).sum()
                above_ma20 = (volume_data > volume_ma_20).sum()
                
                results['volume_patterns'] = {
                    'above_ma5_count': int(above_ma5),
                    'above_ma5_percentage': float(above_ma5 / len(volume_data) * 100),
                    'above_ma20_count': int(above_ma20),
                    'above_ma20_percentage': float(above_ma20 / len(volume_data) * 100),
                    'volume_trend_direction': 'increasing' if volume_ma_5.iloc[-1] > volume_ma_20.iloc[-1] else 'decreasing'
                }
        
        except Exception as e:
            self.logger.error(f"Error analyzing volume patterns: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def analyze_price_volume_relationship(self, data: pd.DataFrame,
                                        volume_col: str = 'Volume',
                                        price_col: str = 'Close') -> Dict[str, Any]:
        """
        Analyze the relationship between price and volume.
        
        Args:
            data: DataFrame with volume and price data
            volume_col: Name of the volume column
            price_col: Name of the price column
            
        Returns:
            Dictionary with price-volume relationship analysis
        """
        results = {
            'correlation_analysis': {},
            'volume_price_trends': {},
            'liquidity_analysis': {},
            'market_activity': {}
        }
        
        try:
            if volume_col not in data.columns or price_col not in data.columns:
                results['error'] = f"Required columns not found: {volume_col}, {price_col}"
                return results
            
            # Get clean data
            clean_data = data[[volume_col, price_col]].dropna()
            
            if len(clean_data) < 2:
                results['error'] = "Insufficient data for price-volume analysis"
                return results
            
            volume_data = clean_data[volume_col]
            price_data = clean_data[price_col]
            
            # Calculate price changes
            price_changes = price_data.pct_change().dropna()
            volume_changes = volume_data.pct_change().dropna()
            
            # Align data
            min_len = min(len(price_changes), len(volume_changes))
            price_changes = price_changes.iloc[-min_len:]
            volume_changes = volume_changes.iloc[-min_len:]
            
            if len(price_changes) < 2:
                results['error'] = "Insufficient data after alignment"
                return results
            
            # Correlation analysis
            correlation = price_changes.corr(volume_changes)
            results['correlation_analysis'] = {
                'price_volume_correlation': float(correlation) if not pd.isna(correlation) else 0.0,
                'correlation_strength': self._interpret_correlation(correlation),
                'correlation_direction': 'positive' if correlation > 0 else 'negative' if correlation < 0 else 'neutral'
            }
            
            # Volume-price trends
            # Analyze volume on up vs down days
            up_days = price_changes > 0
            down_days = price_changes < 0
            
            if up_days.sum() > 0 and down_days.sum() > 0:
                # Align volume data with price changes by using the same index
                aligned_volume = volume_data.loc[price_changes.index]
                up_day_volume = aligned_volume[up_days].mean()
                down_day_volume = aligned_volume[down_days].mean()
                
                results['volume_price_trends'] = {
                    'up_day_volume': float(up_day_volume),
                    'down_day_volume': float(down_day_volume),
                    'volume_ratio': float(up_day_volume / down_day_volume) if down_day_volume > 0 else 0.0,
                    'volume_confirmation': 'bullish' if up_day_volume > down_day_volume else 'bearish'
                }
            
            # Liquidity analysis
            price_range = price_data.max() - price_data.min()
            avg_volume = volume_data.mean()
            
            results['liquidity_analysis'] = {
                'price_range': float(price_range),
                'average_volume': float(avg_volume),
                'liquidity_ratio': float(avg_volume / price_range) if price_range > 0 else 0.0,
                'liquidity_level': self._assess_liquidity(avg_volume, price_range)
            }
            
            # Market activity analysis
            high_volume_threshold = volume_data.quantile(0.8)
            low_volume_threshold = volume_data.quantile(0.2)
            
            high_volume_days = volume_data >= high_volume_threshold
            low_volume_days = volume_data <= low_volume_threshold
            
            results['market_activity'] = {
                'high_volume_days': int(high_volume_days.sum()),
                'low_volume_days': int(low_volume_days.sum()),
                'high_volume_percentage': float(high_volume_days.sum() / len(volume_data) * 100),
                'low_volume_percentage': float(low_volume_days.sum() / len(volume_data) * 100),
                'activity_level': self._assess_activity_level(volume_data)
            }
        
        except Exception as e:
            self.logger.error(f"Error analyzing price-volume relationship: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def detect_volume_anomalies(self, data: pd.DataFrame,
                              volume_col: str = 'Volume',
                              z_score_threshold: float = 3.0) -> Dict[str, Any]:
        """
        Detect volume anomalies using statistical methods.
        
        Args:
            data: DataFrame with volume data
            volume_col: Name of the volume column
            z_score_threshold: Z-score threshold for anomaly detection
            
        Returns:
            Dictionary with volume anomaly detection results
        """
        results = {
            'anomaly_count': 0,
            'anomaly_details': [],
            'anomaly_summary': {},
            'volume_distribution': {}
        }
        
        try:
            if volume_col not in data.columns:
                results['error'] = f"Volume column '{volume_col}' not found"
                return results
            
            volume_data = data[volume_col].dropna()
            
            if len(volume_data) < 3:
                results['error'] = "Insufficient data for anomaly detection"
                return results
            
            # Calculate z-scores
            mean_volume = volume_data.mean()
            std_volume = volume_data.std()
            
            if std_volume == 0:
                results['error'] = "Volume data has no variance"
                return results
            
            z_scores = abs((volume_data - mean_volume) / std_volume)
            anomalies = z_scores[z_scores > z_score_threshold]
            
            # Anomaly details
            for idx, z_score in anomalies.items():
                volume_value = volume_data.loc[idx]
                results['anomaly_details'].append({
                    'index': idx,
                    'volume': float(volume_value),
                    'z_score': float(z_score),
                    'deviation': float((volume_value - mean_volume) / std_volume),
                    'is_spike': volume_value > mean_volume,
                    'is_drop': volume_value < mean_volume
                })
            
            results['anomaly_count'] = len(anomalies)
            
            # Anomaly summary
            spike_count = sum(1 for detail in results['anomaly_details'] if detail['is_spike'])
            drop_count = sum(1 for detail in results['anomaly_details'] if detail['is_drop'])
            
            results['anomaly_summary'] = {
                'total_anomalies': len(anomalies),
                'spike_count': spike_count,
                'drop_count': drop_count,
                'anomaly_percentage': float(len(anomalies) / len(volume_data) * 100)
            }
            
            # Volume distribution analysis
            results['volume_distribution'] = {
                'mean': float(mean_volume),
                'std': float(std_volume),
                'skewness': float(volume_data.skew()),
                'kurtosis': float(volume_data.kurtosis()),
                'q25': float(volume_data.quantile(0.25)),
                'q75': float(volume_data.quantile(0.75)),
                'iqr': float(volume_data.quantile(0.75) - volume_data.quantile(0.25))
            }
        
        except Exception as e:
            self.logger.error(f"Error detecting volume anomalies: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def calculate_volume_indicators(self, data: pd.DataFrame,
                                  volume_col: str = 'Volume',
                                  price_col: str = 'Close') -> Dict[str, Any]:
        """
        Calculate volume-based technical indicators.
        
        Args:
            data: DataFrame with volume and price data
            volume_col: Name of the volume column
            price_col: Name of the price column
            
        Returns:
            Dictionary with volume indicators
        """
        results = {
            'volume_indicators': {},
            'volume_ratios': {},
            'volume_trends': {}
        }
        
        try:
            if volume_col not in data.columns:
                results['error'] = f"Volume column '{volume_col}' not found"
                return results
            
            volume_data = data[volume_col].dropna()
            
            if len(volume_data) < 20:
                results['error'] = "Insufficient data for volume indicators"
                return results
            
            # Volume moving averages
            volume_ma_5 = volume_data.rolling(window=5).mean()
            volume_ma_10 = volume_data.rolling(window=10).mean()
            volume_ma_20 = volume_data.rolling(window=20).mean()
            
            # Volume ratios
            volume_ratio_5_20 = volume_ma_5 / volume_ma_20
            volume_ratio_10_20 = volume_ma_10 / volume_ma_20
            
            results['volume_indicators'] = {
                'volume_ma_5': volume_ma_5.iloc[-1] if not pd.isna(volume_ma_5.iloc[-1]) else 0.0,
                'volume_ma_10': volume_ma_10.iloc[-1] if not pd.isna(volume_ma_10.iloc[-1]) else 0.0,
                'volume_ma_20': volume_ma_20.iloc[-1] if not pd.isna(volume_ma_20.iloc[-1]) else 0.0
            }
            
            results['volume_ratios'] = {
                'ratio_5_20': float(volume_ratio_5_20.iloc[-1]) if not pd.isna(volume_ratio_5_20.iloc[-1]) else 0.0,
                'ratio_10_20': float(volume_ratio_10_20.iloc[-1]) if not pd.isna(volume_ratio_10_20.iloc[-1]) else 0.0,
                'current_vs_ma20': float(volume_data.iloc[-1] / volume_ma_20.iloc[-1]) if not pd.isna(volume_ma_20.iloc[-1]) and volume_ma_20.iloc[-1] != 0 else 0.0
            }
            
            # Volume trends
            recent_volume = volume_data.tail(5).mean()
            historical_volume = volume_data.head(-5).mean()
            
            results['volume_trends'] = {
                'recent_volume': float(recent_volume),
                'historical_volume': float(historical_volume),
                'volume_trend': 'increasing' if recent_volume > historical_volume else 'decreasing',
                'trend_strength': float((recent_volume - historical_volume) / historical_volume * 100) if historical_volume != 0 else 0.0
            }
        
        except Exception as e:
            self.logger.error(f"Error calculating volume indicators: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _interpret_correlation(self, correlation: float) -> str:
        """Interpret correlation strength."""
        abs_corr = abs(correlation)
        if abs_corr >= 0.7:
            return 'strong'
        elif abs_corr >= 0.3:
            return 'moderate'
        elif abs_corr >= 0.1:
            return 'weak'
        else:
            return 'negligible'
    
    def _assess_liquidity(self, avg_volume: float, price_range: float) -> str:
        """Assess liquidity level."""
        if price_range == 0:
            return 'unknown'
        
        liquidity_ratio = avg_volume / price_range
        
        if liquidity_ratio > 1000:
            return 'very_high'
        elif liquidity_ratio > 100:
            return 'high'
        elif liquidity_ratio > 10:
            return 'moderate'
        elif liquidity_ratio > 1:
            return 'low'
        else:
            return 'very_low'
    
    def _assess_activity_level(self, volume_data: pd.Series) -> str:
        """Assess market activity level."""
        volume_std = volume_data.std()
        volume_mean = volume_data.mean()
        
        if volume_std == 0:
            return 'stable'
        
        cv = volume_std / volume_mean  # Coefficient of variation
        
        if cv > 1.0:
            return 'very_high'
        elif cv > 0.5:
            return 'high'
        elif cv > 0.2:
            return 'moderate'
        else:
            return 'low'
