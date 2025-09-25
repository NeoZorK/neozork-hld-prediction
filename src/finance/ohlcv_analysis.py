"""
OHLCV Analysis Module

This module provides comprehensive OHLCV data analysis including price validation,
volume analysis, and price-volume relationships for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging
from .core.price_validation import PriceValidator
from .core.volume_analysis import VolumeAnalyzer
from .color_utils import ColorUtils


class OHLCVAnalysis:
    """Comprehensive OHLCV data analysis."""
    
    def __init__(self):
        """Initialize the OHLCV analyzer."""
        self.logger = logging.getLogger(__name__)
        self.price_validator = PriceValidator()
        self.volume_analyzer = VolumeAnalyzer()
    
    def analyze_ohlcv_data(self, data: pd.DataFrame, 
                          numeric_columns: List[str]) -> Dict[str, Any]:
        """
        Perform comprehensive OHLCV analysis.
        
        Args:
            data: DataFrame with financial data
            numeric_columns: List of numeric columns to analyze
            
        Returns:
            Dictionary with OHLCV analysis results
        """
        results = {
            'price_validation': {},
            'volume_analysis': {},
            'price_volume_relationships': {},
            'data_quality_assessment': {},
            'recommendations': {}
        }
        
        try:
            # Identify OHLCV columns
            ohlcv_columns = self._identify_ohlcv_columns(data, numeric_columns)
            
            if not ohlcv_columns:
                results['error'] = "No OHLCV columns identified in the data"
                return results
            
            # Price validation
            if ohlcv_columns['price_columns']:
                results['price_validation'] = self._analyze_price_validation(
                    data, ohlcv_columns['price_columns']
                )
            
            # Volume analysis
            if ohlcv_columns['volume_columns']:
                results['volume_analysis'] = self._analyze_volume_data(
                    data, ohlcv_columns['volume_columns']
                )
            
            # Price-volume relationships
            if ohlcv_columns['price_columns'] and ohlcv_columns['volume_columns']:
                results['price_volume_relationships'] = self._analyze_price_volume_relationships(
                    data, ohlcv_columns['price_columns'], ohlcv_columns['volume_columns']
                )
            
            # Data quality assessment
            results['data_quality_assessment'] = self._assess_data_quality(
                data, ohlcv_columns
            )
            
            # Generate recommendations
            results['recommendations'] = self._generate_recommendations(
                results['price_validation'],
                results['volume_analysis'],
                results['data_quality_assessment']
            )
            
        except Exception as e:
            self.logger.error(f"Error in OHLCV analysis: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _identify_ohlcv_columns(self, data: pd.DataFrame, 
                               numeric_columns: List[str]) -> Dict[str, List[str]]:
        """
        Identify OHLCV columns in the data.
        
        Args:
            data: DataFrame with financial data
            numeric_columns: List of numeric columns
            
        Returns:
            Dictionary with identified OHLCV columns
        """
        ohlcv_columns = {
            'price_columns': [],
            'volume_columns': [],
            'all_columns': []
        }
        
        # Common OHLCV column names
        price_keywords = ['open', 'high', 'low', 'close', 'price']
        volume_keywords = ['volume', 'vol', 'quantity', 'amount']
        
        for col in numeric_columns:
            col_lower = col.lower()
            
            # Check for price columns
            if any(keyword in col_lower for keyword in price_keywords):
                ohlcv_columns['price_columns'].append(col)
                ohlcv_columns['all_columns'].append(col)
            
            # Check for volume columns
            if any(keyword in col_lower for keyword in volume_keywords):
                ohlcv_columns['volume_columns'].append(col)
                ohlcv_columns['all_columns'].append(col)
        
        return ohlcv_columns
    
    def _analyze_price_validation(self, data: pd.DataFrame, 
                                price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze price validation for identified price columns.
        
        Args:
            data: DataFrame with price data
            price_columns: List of price columns
            
        Returns:
            Dictionary with price validation results
        """
        results = {
            'ohlc_validation': {},
            'price_gaps': {},
            'price_anomalies': {},
            'price_consistency': {},
            'price_statistics': {}
        }
        
        try:
            # Identify OHLC columns
            ohlc_columns = self._identify_ohlc_columns(data, price_columns)
            
            if ohlc_columns:
                # OHLC relationship validation
                results['ohlc_validation'] = self.price_validator.validate_ohlc_relationships(
                    data, 
                    ohlc_columns.get('open', 'Open'),
                    ohlc_columns.get('high', 'High'),
                    ohlc_columns.get('low', 'Low'),
                    ohlc_columns.get('close', 'Close')
                )
                
                # Price gaps detection
                if ohlc_columns.get('open') and ohlc_columns.get('close'):
                    results['price_gaps'] = self.price_validator.detect_price_gaps(
                        data,
                        ohlc_columns['close'],
                        ohlc_columns['open']
                    )
            
            # Price anomalies detection
            results['price_anomalies'] = self.price_validator.detect_price_anomalies(
                data, price_columns
            )
            
            # Price consistency validation
            results['price_consistency'] = self.price_validator.validate_price_consistency(
                data, price_columns
            )
            
            # Price statistics
            results['price_statistics'] = self.price_validator.get_price_statistics(
                data, price_columns
            )
            
        except Exception as e:
            self.logger.error(f"Error in price validation: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_volume_data(self, data: pd.DataFrame, 
                            volume_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze volume data for identified volume columns.
        
        Args:
            data: DataFrame with volume data
            volume_columns: List of volume columns
            
        Returns:
            Dictionary with volume analysis results
        """
        results = {
            'volume_patterns': {},
            'volume_anomalies': {},
            'volume_indicators': {}
        }
        
        try:
            # Use the first volume column for analysis
            volume_col = volume_columns[0]
            
            # Volume patterns analysis
            results['volume_patterns'] = self.volume_analyzer.analyze_volume_patterns(
                data, volume_col
            )
            
            # Volume anomalies detection
            results['volume_anomalies'] = self.volume_analyzer.detect_volume_anomalies(
                data, volume_col
            )
            
            # Volume indicators calculation
            results['volume_indicators'] = self.volume_analyzer.calculate_volume_indicators(
                data, volume_col
            )
            
        except Exception as e:
            self.logger.error(f"Error in volume analysis: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_price_volume_relationships(self, data: pd.DataFrame,
                                          price_columns: List[str],
                                          volume_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze relationships between price and volume.
        
        Args:
            data: DataFrame with price and volume data
            price_columns: List of price columns
            volume_columns: List of volume columns
            
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
            # Use the first price and volume columns
            price_col = price_columns[0]
            volume_col = volume_columns[0]
            
            # Price-volume relationship analysis
            pv_analysis = self.volume_analyzer.analyze_price_volume_relationship(
                data, volume_col, price_col
            )
            
            results.update(pv_analysis)
            
        except Exception as e:
            self.logger.error(f"Error in price-volume relationship analysis: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _assess_data_quality(self, data: pd.DataFrame, 
                            ohlcv_columns: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Assess overall data quality for OHLCV analysis.
        
        Args:
            data: DataFrame with financial data
            ohlcv_columns: Dictionary with identified OHLCV columns
            
        Returns:
            Dictionary with data quality assessment
        """
        results = {
            'completeness_score': 0.0,
            'consistency_score': 0.0,
            'quality_issues': [],
            'recommendations': []
        }
        
        try:
            total_columns = len(ohlcv_columns['all_columns'])
            if total_columns == 0:
                results['quality_issues'].append("No OHLCV columns identified")
                return results
            
            # Check for missing values
            missing_data = {}
            for col in ohlcv_columns['all_columns']:
                if col in data.columns:
                    missing_count = data[col].isna().sum()
                    missing_pct = (missing_count / len(data)) * 100
                    missing_data[col] = {
                        'missing_count': int(missing_count),
                        'missing_percentage': float(missing_pct)
                    }
            
            # Calculate completeness score
            if missing_data:
                avg_missing = np.mean([info['missing_percentage'] for info in missing_data.values()])
                results['completeness_score'] = max(0, 100 - avg_missing)
            
            # Check for data consistency
            consistency_issues = []
            
            # Check for negative prices
            for col in ohlcv_columns['price_columns']:
                if col in data.columns:
                    negative_count = (data[col] < 0).sum()
                    if negative_count > 0:
                        consistency_issues.append(f"Negative prices in {col}: {negative_count} occurrences")
            
            # Check for zero volumes
            for col in ohlcv_columns['volume_columns']:
                if col in data.columns:
                    zero_count = (data[col] == 0).sum()
                    if zero_count > 0:
                        consistency_issues.append(f"Zero volumes in {col}: {zero_count} occurrences")
            
            results['quality_issues'] = consistency_issues
            
            # Generate quality recommendations
            if results['completeness_score'] < 80:
                results['recommendations'].append("Data completeness is low - consider data cleaning")
            
            if consistency_issues:
                results['recommendations'].append("Data consistency issues detected - review data quality")
            
            if not ohlcv_columns['price_columns']:
                results['recommendations'].append("No price columns identified - check column names")
            
            if not ohlcv_columns['volume_columns']:
                results['recommendations'].append("No volume columns identified - check column names")
        
        except Exception as e:
            self.logger.error(f"Error assessing data quality: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _generate_recommendations(self, price_validation: Dict[str, Any],
                                volume_analysis: Dict[str, Any],
                                data_quality: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate recommendations based on analysis results.
        
        Args:
            price_validation: Price validation results
            volume_analysis: Volume analysis results
            data_quality: Data quality assessment
            
        Returns:
            Dictionary with recommendations
        """
        recommendations = {
            'data_cleaning': [],
            'analysis_improvements': [],
            'risk_considerations': [],
            'next_steps': []
        }
        
        try:
            # Data cleaning recommendations
            if price_validation.get('data_quality_score', 100) < 90:
                recommendations['data_cleaning'].append("Review and clean price data for better quality")
            
            if volume_analysis.get('volume_patterns', {}).get('zero_volume_percentage', 0) > 10:
                recommendations['data_cleaning'].append("High percentage of zero volumes - investigate data source")
            
            if data_quality.get('completeness_score', 100) < 80:
                recommendations['data_cleaning'].append("Low data completeness - consider data imputation")
            
            # Analysis improvements
            if price_validation.get('ohlc_validation', {}).get('invalid_rows', 0) > 0:
                recommendations['analysis_improvements'].append("OHLC validation issues detected - review price relationships")
            
            if volume_analysis.get('volume_anomalies', {}).get('anomaly_count', 0) > 0:
                recommendations['analysis_improvements'].append("Volume anomalies detected - investigate unusual trading activity")
            
            # Risk considerations
            if price_validation.get('price_gaps', {}).get('significant_gaps', 0) > 0:
                recommendations['risk_considerations'].append("Significant price gaps detected - consider gap risk in trading")
            
            if volume_analysis.get('volume_patterns', {}).get('volume_volatility', 0) > 0.5:
                recommendations['risk_considerations'].append("High volume volatility - consider position sizing adjustments")
            
            # Next steps
            recommendations['next_steps'].append("Consider running volatility analysis for risk assessment")
            recommendations['next_steps'].append("Perform returns analysis for performance evaluation")
            recommendations['next_steps'].append("Run drawdown analysis for risk management")
        
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            recommendations['error'] = str(e)
        
        return recommendations
    
    def _identify_ohlc_columns(self, data: pd.DataFrame, 
                             price_columns: List[str]) -> Dict[str, str]:
        """
        Identify specific OHLC columns from price columns.
        
        Args:
            data: DataFrame with price data
            price_columns: List of price columns
            
        Returns:
            Dictionary with identified OHLC columns
        """
        ohlc_columns = {}
        
        # Common OHLC column patterns
        patterns = {
            'open': ['open', 'o'],
            'high': ['high', 'h'],
            'low': ['low', 'l'],
            'close': ['close', 'c']
        }
        
        for col in price_columns:
            col_lower = col.lower()
            
            for ohlc_type, keywords in patterns.items():
                if any(keyword in col_lower for keyword in keywords):
                    ohlc_columns[ohlc_type] = col
                    break
        
        return ohlc_columns
    
    def get_analysis_summary(self, results: Dict[str, Any]) -> str:
        """
        Get a detailed summary of OHLCV analysis results with interpretations.
        
        Args:
            results: OHLCV analysis results
            
        Returns:
            Detailed summary string with interpretations
        """
        summary_parts = []
        
        try:
            # Price validation summary with interpretation
            if 'price_validation' in results:
                pv = results['price_validation']
                if 'ohlc_validation' in pv:
                    ohlc = pv['ohlc_validation']
                    valid_pct = (ohlc.get('valid_rows', 0) / ohlc.get('total_rows', 1)) * 100
                    
                    # Interpret price validation results
                    if valid_pct >= 95:
                        price_status = "✅ Excellent"
                    elif valid_pct >= 80:
                        price_status = "⚠️ Good"
                    elif valid_pct >= 50:
                        price_status = "🔶 Fair"
                    else:
                        price_status = "❌ Poor"
                    
                    summary_parts.append(f"Price Validation: {valid_pct:.1f}% valid rows {price_status}")
            
            # Volume analysis summary with interpretation
            if 'volume_analysis' in results:
                va = results['volume_analysis']
                if 'volume_patterns' in va:
                    vp = va['volume_patterns']
                    zero_vol_pct = vp.get('zero_volume_percentage', 0)
                    
                    # Interpret volume analysis results
                    if zero_vol_pct == 0:
                        volume_status = "✅ Perfect"
                    elif zero_vol_pct <= 5:
                        volume_status = "✅ Good"
                    elif zero_vol_pct <= 15:
                        volume_status = "⚠️ Acceptable"
                    else:
                        volume_status = "❌ Problematic"
                    
                    summary_parts.append(f"Volume Analysis: {zero_vol_pct:.1f}% zero volumes {volume_status}")
            
            # Data quality summary with interpretation
            if 'data_quality_assessment' in results:
                dq = results['data_quality_assessment']
                completeness = dq.get('completeness_score', 0)
                
                # Interpret data quality results
                if completeness >= 99:
                    quality_status = "✅ Excellent"
                elif completeness >= 95:
                    quality_status = "✅ Very Good"
                elif completeness >= 90:
                    quality_status = "⚠️ Good"
                elif completeness >= 80:
                    quality_status = "🔶 Fair"
                else:
                    quality_status = "❌ Poor"
                
                summary_parts.append(f"Data Quality: {completeness:.1f}% completeness {quality_status}")
            
            # Price-volume relationships summary with interpretation
            if 'price_volume_relationships' in results:
                pvr = results['price_volume_relationships']
                if 'correlation_analysis' in pvr:
                    corr = pvr['correlation_analysis'].get('price_volume_correlation', 0)
                    
                    # Interpret correlation results
                    abs_corr = abs(corr)
                    if abs_corr >= 0.7:
                        corr_strength = "Strong"
                        corr_status = "✅" if corr > 0 else "⚠️"
                    elif abs_corr >= 0.3:
                        corr_strength = "Moderate"
                        corr_status = "✅" if corr > 0 else "⚠️"
                    elif abs_corr >= 0.1:
                        corr_strength = "Weak"
                        corr_status = "🔶"
                    else:
                        corr_strength = "Negligible"
                        corr_status = "🔶"
                    
                    direction = "positive" if corr > 0 else "negative" if corr < 0 else "neutral"
                    summary_parts.append(f"Price-Volume Correlation: {corr:.3f} ({corr_strength} {direction}) {corr_status}")
            
        except Exception as e:
            summary_parts.append(f"Error generating summary: {str(e)}")
        
        return " | ".join(summary_parts) if summary_parts else "No analysis results available"
