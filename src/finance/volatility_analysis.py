"""
Volatility Analysis Module

This module provides comprehensive volatility analysis including rolling volatility,
GARCH models, and volatility clustering for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging
from .core.garch_models import GARCHModeler
from .color_utils import ColorUtils


class VolatilityAnalysis:
    """Comprehensive volatility analysis for financial data."""
    
    def __init__(self):
        """Initialize the volatility analyzer."""
        self.logger = logging.getLogger(__name__)
        self.garch_modeler = GARCHModeler()
    
    def analyze_volatility(self, data: pd.DataFrame, 
                         numeric_columns: List[str]) -> Dict[str, Any]:
        """
        Perform comprehensive volatility analysis.
        
        Args:
            data: DataFrame with financial data
            numeric_columns: List of numeric columns to analyze
            
        Returns:
            Dictionary with volatility analysis results
        """
        results = {
            'rolling_volatility': {},
            'garch_models': {},
            'volatility_clustering': {},
            'volatility_regimes': {},
            'volatility_forecasting': {},
            'recommendations': {}
        }
        
        try:
            # Identify price columns for volatility analysis
            price_columns = self._identify_price_columns(data, numeric_columns)
            
            if not price_columns:
                results['error'] = "No price columns identified for volatility analysis"
                return results
            
            # Calculate returns for volatility analysis
            returns_data = self._calculate_returns(data, price_columns)
            
            if returns_data.empty:
                results['error'] = "Unable to calculate returns for volatility analysis"
                return results
            
            # Rolling volatility analysis
            results['rolling_volatility'] = self._analyze_rolling_volatility(
                returns_data, price_columns
            )
            
            # GARCH modeling
            results['garch_models'] = self._analyze_garch_models(
                returns_data, price_columns
            )
            
            # Volatility clustering analysis
            results['volatility_clustering'] = self._analyze_volatility_clustering(
                returns_data, price_columns
            )
            
            # Volatility regime detection
            results['volatility_regimes'] = self._detect_volatility_regimes(
                returns_data, price_columns
            )
            
            # Volatility forecasting
            results['volatility_forecasting'] = self._forecast_volatility(
                returns_data, price_columns
            )
            
            # Generate recommendations
            results['recommendations'] = self._generate_volatility_recommendations(
                results
            )
            
        except Exception as e:
            self.logger.error(f"Error in volatility analysis: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _identify_price_columns(self, data: pd.DataFrame, 
                               numeric_columns: List[str]) -> List[str]:
        """
        Identify price columns suitable for volatility analysis.
        
        Args:
            data: DataFrame with financial data
            numeric_columns: List of numeric columns
            
        Returns:
            List of price column names
        """
        price_columns = []
        
        # Common price column patterns
        price_keywords = ['close', 'price', 'value', 'rate', 'quote']
        
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
    
    def _calculate_returns(self, data: pd.DataFrame, 
                          price_columns: List[str]) -> pd.DataFrame:
        """
        Calculate returns for volatility analysis.
        
        Args:
            data: DataFrame with price data
            price_columns: List of price columns
            
        Returns:
            DataFrame with returns data
        """
        returns_data = pd.DataFrame(index=data.index)
        
        for col in price_columns:
            if col in data.columns:
                # Calculate simple returns
                returns_data[f'{col}_returns'] = data[col].pct_change()
                
                # Calculate log returns
                returns_data[f'{col}_log_returns'] = np.log(data[col] / data[col].shift(1))
        
        return returns_data.dropna()
    
    def _analyze_rolling_volatility(self, returns_data: pd.DataFrame,
                                   price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze rolling volatility for different time windows.
        
        Args:
            returns_data: DataFrame with returns data
            price_columns: List of price columns
            
        Returns:
            Dictionary with rolling volatility analysis
        """
        results = {
            'volatility_windows': {},
            'volatility_comparison': {},
            'volatility_trends': {},
            'annualized_volatility': {}
        }
        
        try:
            # Different volatility windows
            windows = [5, 10, 20, 30, 60]
            
            for col in price_columns:
                returns_col = f'{col}_returns'
                if returns_col in returns_data.columns:
                    col_results = {}
                    
                    for window in windows:
                        if len(returns_data) >= window:
                            # Calculate rolling volatility
                            rolling_vol = returns_data[returns_col].rolling(window=window).std()
                            
                            # Annualize volatility (assuming daily data)
                            annualized_vol = rolling_vol * np.sqrt(252)
                            
                            col_results[f'window_{window}'] = {
                                'current_volatility': float(rolling_vol.iloc[-1]) if not pd.isna(rolling_vol.iloc[-1]) else 0.0,
                                'mean_volatility': float(rolling_vol.mean()),
                                'std_volatility': float(rolling_vol.std()),
                                'annualized_volatility': float(annualized_vol.iloc[-1]) if not pd.isna(annualized_vol.iloc[-1]) else 0.0,
                                'volatility_percentile_25': float(rolling_vol.quantile(0.25)),
                                'volatility_percentile_75': float(rolling_vol.quantile(0.75))
                            }
                    
                    results['volatility_windows'][col] = col_results
            
            # Volatility comparison across windows
            if results['volatility_windows']:
                results['volatility_comparison'] = self._compare_volatility_windows(
                    results['volatility_windows']
                )
            
            # Volatility trends
            results['volatility_trends'] = self._analyze_volatility_trends(
                results['volatility_windows']
            )
        
        except Exception as e:
            self.logger.error(f"Error analyzing rolling volatility: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_garch_models(self, returns_data: pd.DataFrame,
                            price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze GARCH models for volatility modeling.
        
        Args:
            returns_data: DataFrame with returns data
            price_columns: List of price columns
            
        Returns:
            Dictionary with GARCH model analysis
        """
        results = {
            'garch_models': {},
            'model_comparison': {},
            'volatility_forecasts': {}
        }
        
        try:
            for col in price_columns:
                returns_col = f'{col}_returns'
                if returns_col in returns_data.columns:
                    col_returns = returns_data[returns_col].dropna()
                    
                    if len(col_returns) < 50:
                        continue
                    
                    col_results = {}
                    
                    # Try different GARCH models
                    model_types = ['GARCH', 'EGARCH', 'GJR-GARCH']
                    
                    for model_type in model_types:
                        try:
                            garch_result = self.garch_modeler.fit_garch_model(
                                col_returns, model_type=model_type
                            )
                            
                            if garch_result.get('success', False):
                                col_results[model_type] = garch_result
                        except Exception as e:
                            col_results[model_type] = {'error': str(e)}
                    
                    results['garch_models'][col] = col_results
            
            # Model comparison
            results['model_comparison'] = self._compare_garch_models(
                results['garch_models']
            )
            
            # Volatility forecasts
            results['volatility_forecasts'] = self._extract_volatility_forecasts(
                results['garch_models']
            )
        
        except Exception as e:
            self.logger.error(f"Error analyzing GARCH models: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_volatility_clustering(self, returns_data: pd.DataFrame,
                                     price_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze volatility clustering patterns.
        
        Args:
            returns_data: DataFrame with returns data
            price_columns: List of price columns
            
        Returns:
            Dictionary with volatility clustering analysis
        """
        results = {
            'clustering_analysis': {},
            'regime_detection': {},
            'persistence_analysis': {}
        }
        
        try:
            for col in price_columns:
                returns_col = f'{col}_returns'
                if returns_col in returns_data.columns:
                    col_returns = returns_data[returns_col].dropna()
                    
                    if len(col_returns) < 20:
                        continue
                    
                    # Volatility clustering analysis
                    clustering_result = self.garch_modeler.analyze_volatility_clustering(
                        col_returns
                    )
                    
                    results['clustering_analysis'][col] = clustering_result
        
        except Exception as e:
            self.logger.error(f"Error analyzing volatility clustering: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _detect_volatility_regimes(self, returns_data: pd.DataFrame,
                                 price_columns: List[str]) -> Dict[str, Any]:
        """
        Detect volatility regimes in the data.
        
        Args:
            returns_data: DataFrame with returns data
            price_columns: List of price columns
            
        Returns:
            Dictionary with volatility regime detection
        """
        results = {
            'regime_analysis': {},
            'regime_transitions': {},
            'regime_statistics': {}
        }
        
        try:
            for col in price_columns:
                returns_col = f'{col}_returns'
                if returns_col in returns_data.columns:
                    col_returns = returns_data[returns_col].dropna()
                    
                    if len(col_returns) < 50:
                        continue
                    
                    # Calculate rolling volatility for regime detection
                    rolling_vol = col_returns.rolling(window=20).std()
                    
                    # Define volatility regimes based on percentiles
                    vol_25 = rolling_vol.quantile(0.25)
                    vol_75 = rolling_vol.quantile(0.75)
                    
                    # Classify regimes
                    low_vol_regime = rolling_vol <= vol_25
                    high_vol_regime = rolling_vol >= vol_75
                    normal_vol_regime = (rolling_vol > vol_25) & (rolling_vol < vol_75)
                    
                    # Calculate regime statistics
                    regime_stats = {
                        'low_vol_periods': int(low_vol_regime.sum()),
                        'high_vol_periods': int(high_vol_regime.sum()),
                        'normal_vol_periods': int(normal_vol_regime.sum()),
                        'low_vol_percentage': float(low_vol_regime.sum() / len(rolling_vol) * 100),
                        'high_vol_percentage': float(high_vol_regime.sum() / len(rolling_vol) * 100),
                        'normal_vol_percentage': float(normal_vol_regime.sum() / len(rolling_vol) * 100)
                    }
                    
                    # Calculate regime transitions
                    regime_changes = (low_vol_regime != low_vol_regime.shift(1)).sum()
                    
                    results['regime_analysis'][col] = {
                        'regime_statistics': regime_stats,
                        'regime_changes': int(regime_changes),
                        'current_regime': self._get_current_regime(rolling_vol.iloc[-1], vol_25, vol_75)
                    }
        
        except Exception as e:
            self.logger.error(f"Error detecting volatility regimes: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _forecast_volatility(self, returns_data: pd.DataFrame,
                           price_columns: List[str]) -> Dict[str, Any]:
        """
        Forecast volatility using various methods.
        
        Args:
            returns_data: DataFrame with returns data
            price_columns: List of price columns
            
        Returns:
            Dictionary with volatility forecasts
        """
        results = {
            'simple_forecasts': {},
            'garch_forecasts': {},
            'forecast_comparison': {}
        }
        
        try:
            for col in price_columns:
                returns_col = f'{col}_returns'
                if returns_col in returns_data.columns:
                    col_returns = returns_data[returns_col].dropna()
                    
                    if len(col_returns) < 20:
                        continue
                    
                    # Simple volatility forecast (using recent volatility)
                    recent_vol = col_returns.tail(20).std()
                    results['simple_forecasts'][col] = {
                        'next_period_volatility': float(recent_vol),
                        'annualized_volatility': float(recent_vol * np.sqrt(252))
                    }
        
        except Exception as e:
            self.logger.error(f"Error forecasting volatility: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _compare_volatility_windows(self, volatility_windows: Dict[str, Any]) -> Dict[str, Any]:
        """Compare volatility across different windows."""
        comparison = {
            'window_comparison': {},
            'volatility_ranking': {},
            'consistency_analysis': {}
        }
        
        try:
            # This would contain logic to compare volatility across different windows
            # Implementation depends on specific requirements
            pass
        
        except Exception as e:
            comparison['error'] = str(e)
        
        return comparison
    
    def _analyze_volatility_trends(self, volatility_windows: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze volatility trends across different windows."""
        trends = {
            'trend_direction': {},
            'trend_strength': {},
            'trend_consistency': {}
        }
        
        try:
            # This would contain logic to analyze volatility trends
            # Implementation depends on specific requirements
            pass
        
        except Exception as e:
            trends['error'] = str(e)
        
        return trends
    
    def _compare_garch_models(self, garch_models: Dict[str, Any]) -> Dict[str, Any]:
        """Compare different GARCH models."""
        comparison = {
            'model_ranking': {},
            'best_model': {},
            'model_selection': {}
        }
        
        try:
            # This would contain logic to compare GARCH models
            # Implementation depends on specific requirements
            pass
        
        except Exception as e:
            comparison['error'] = str(e)
        
        return comparison
    
    def _extract_volatility_forecasts(self, garch_models: Dict[str, Any]) -> Dict[str, Any]:
        """Extract volatility forecasts from GARCH models."""
        forecasts = {
            'forecast_values': {},
            'forecast_confidence': {},
            'forecast_accuracy': {}
        }
        
        try:
            # This would contain logic to extract volatility forecasts
            # Implementation depends on specific requirements
            pass
        
        except Exception as e:
            forecasts['error'] = str(e)
        
        return forecasts
    
    def _get_current_regime(self, current_vol: float, vol_25: float, vol_75: float) -> str:
        """Determine current volatility regime."""
        if current_vol <= vol_25:
            return 'low_volatility'
        elif current_vol >= vol_75:
            return 'high_volatility'
        else:
            return 'normal_volatility'
    
    def _generate_volatility_recommendations(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations based on volatility analysis."""
        recommendations = {
            'risk_management': [],
            'trading_strategies': [],
            'portfolio_considerations': [],
            'monitoring_suggestions': []
        }
        
        try:
            # Risk management recommendations
            recommendations['risk_management'].append("Monitor volatility regimes for position sizing adjustments")
            recommendations['risk_management'].append("Use volatility forecasts for risk assessment")
            
            # Trading strategy recommendations
            recommendations['trading_strategies'].append("Consider volatility-based entry/exit strategies")
            recommendations['trading_strategies'].append("Adapt strategy parameters based on volatility regimes")
            
            # Portfolio considerations
            recommendations['portfolio_considerations'].append("Diversify across different volatility regimes")
            recommendations['portfolio_considerations'].append("Consider volatility clustering in portfolio construction")
            
            # Monitoring suggestions
            recommendations['monitoring_suggestions'].append("Track volatility trends and regime changes")
            recommendations['monitoring_suggestions'].append("Update volatility models regularly")
        
        except Exception as e:
            recommendations['error'] = str(e)
        
        return recommendations
    
    def get_analysis_summary(self, results: Dict[str, Any]) -> str:
        """Get a summary of volatility analysis results."""
        summary_parts = []
        
        try:
            # Rolling volatility summary
            if 'rolling_volatility' in results:
                rv = results['rolling_volatility']
                if 'volatility_windows' in rv:
                    # Get current volatility from 20-day window
                    for col, windows in rv['volatility_windows'].items():
                        if 'window_20' in windows:
                            current_vol = windows['window_20'].get('current_volatility', 0)
                            summary_parts.append(f"Current Volatility ({col}): {current_vol:.4f}")
            
            # GARCH models summary
            if 'garch_models' in results:
                gm = results['garch_models']
                successful_models = sum(1 for col_models in gm.values() 
                                     for model in col_models.values() 
                                     if model.get('success', False))
                summary_parts.append(f"GARCH Models: {successful_models} successful")
            
            # Volatility clustering summary
            if 'volatility_clustering' in results:
                vc = results['volatility_clustering']
                if 'clustering_analysis' in vc:
                    summary_parts.append("Volatility Clustering: Analyzed")
            
        except Exception as e:
            summary_parts.append(f"Error generating summary: {str(e)}")
        
        return " | ".join(summary_parts) if summary_parts else "No volatility analysis results available"
