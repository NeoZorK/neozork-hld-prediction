"""
GARCH Models Module

This module provides GARCH (Generalized Autoregressive Conditional Heteroskedasticity)
modeling functionality for volatility analysis in financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import logging
from scipy import stats

try:
    from arch import arch_model
    ARCH_AVAILABLE = True
except ImportError:
    ARCH_AVAILABLE = False
    print("Warning: arch package not available. GARCH modeling will be limited.")


class GARCHModeler:
    """Models volatility using GARCH family models."""
    
    def __init__(self):
        """Initialize the GARCH modeler."""
        self.logger = logging.getLogger(__name__)
        self.arch_available = ARCH_AVAILABLE
    
    def fit_garch_model(self, returns: pd.Series, 
                       model_type: str = 'GARCH',
                       p: int = 1, q: int = 1,
                       vol: str = 'GARCH') -> Dict[str, Any]:
        """
        Fit a GARCH model to returns data.
        
        Args:
            returns: Series of returns data
            model_type: Type of GARCH model ('GARCH', 'EGARCH', 'GJR-GARCH')
            p: Number of autoregressive terms
            q: Number of moving average terms
            vol: Volatility model type
            
        Returns:
            Dictionary with GARCH model results
        """
        results = {
            'model_type': model_type,
            'parameters': {},
            'fit_statistics': {},
            'volatility_forecast': {},
            'model_summary': {},
            'success': False
        }
        
        try:
            if not self.arch_available:
                results['error'] = "ARCH package not available. Install with: pip install arch"
                return results
            
            if len(returns) < 50:
                results['error'] = "Insufficient data for GARCH modeling (need at least 50 observations)"
                return results
            
            # Clean returns data
            clean_returns = returns.dropna()
            
            if len(clean_returns) < 50:
                results['error'] = "Insufficient clean data for GARCH modeling"
                return results
            
            # Fit GARCH model
            if model_type == 'GARCH':
                model = arch_model(clean_returns, vol=vol, p=p, q=q)
            elif model_type == 'EGARCH':
                model = arch_model(clean_returns, vol='EGARCH', p=p, q=q)
            elif model_type == 'GJR-GARCH':
                model = arch_model(clean_returns, vol='GARCH', p=p, o=1, q=q)
            else:
                results['error'] = f"Unsupported model type: {model_type}"
                return results
            
            # Fit the model
            fitted_model = model.fit(disp='off')
            
            # Extract parameters
            results['parameters'] = {
                'omega': float(fitted_model.params['omega']),
                'alpha': [float(fitted_model.params[f'alpha[{i}]']) for i in range(p)],
                'beta': [float(fitted_model.params[f'beta[{i}]']) for i in range(q)],
                'gamma': float(fitted_model.params.get('gamma[1]', 0.0)) if model_type == 'GJR-GARCH' else None
            }
            
            # Fit statistics
            results['fit_statistics'] = {
                'log_likelihood': float(fitted_model.loglikelihood),
                'aic': float(fitted_model.aic),
                'bic': float(fitted_model.bic),
                'convergence': fitted_model.convergence_flag,
                'iterations': fitted_model.num_iterations
            }
            
            # Volatility forecast
            forecast = fitted_model.forecast(horizon=1)
            results['volatility_forecast'] = {
                'next_period_volatility': float(forecast.variance.iloc[-1, 0] ** 0.5),
                'conditional_variance': float(forecast.variance.iloc[-1, 0])
            }
            
            # Model summary
            results['model_summary'] = {
                'model_equation': self._get_model_equation(model_type, results['parameters']),
                'persistence': self._calculate_persistence(results['parameters']),
                'unconditional_variance': self._calculate_unconditional_variance(results['parameters'])
            }
            
            results['success'] = True
            
        except Exception as e:
            self.logger.error(f"Error fitting GARCH model: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def analyze_volatility_clustering(self, returns: pd.Series,
                                    window: int = 20) -> Dict[str, Any]:
        """
        Analyze volatility clustering in returns data.
        
        Args:
            returns: Series of returns data
            window: Window size for rolling volatility calculation
            
        Returns:
            Dictionary with volatility clustering analysis
        """
        results = {
            'volatility_statistics': {},
            'clustering_analysis': {},
            'regime_detection': {},
            'persistence_analysis': {}
        }
        
        try:
            clean_returns = returns.dropna()
            
            if len(clean_returns) < window * 2:
                results['error'] = f"Insufficient data for volatility clustering analysis (need at least {window * 2} observations)"
                return results
            
            # Calculate rolling volatility
            rolling_vol = clean_returns.rolling(window=window).std()
            
            # Volatility statistics
            results['volatility_statistics'] = {
                'mean_volatility': float(rolling_vol.mean()),
                'std_volatility': float(rolling_vol.std()),
                'min_volatility': float(rolling_vol.min()),
                'max_volatility': float(rolling_vol.max()),
                'volatility_range': float(rolling_vol.max() - rolling_vol.min()),
                'volatility_skewness': float(rolling_vol.skew()),
                'volatility_kurtosis': float(rolling_vol.kurtosis())
            }
            
            # Clustering analysis
            vol_changes = rolling_vol.pct_change().dropna()
            
            # Calculate autocorrelation of volatility
            vol_autocorr = rolling_vol.autocorr(lag=1)
            vol_changes_autocorr = vol_changes.autocorr(lag=1)
            
            results['clustering_analysis'] = {
                'volatility_autocorrelation': float(vol_autocorr) if not pd.isna(vol_autocorr) else 0.0,
                'volatility_changes_autocorrelation': float(vol_changes_autocorr) if not pd.isna(vol_changes_autocorr) else 0.0,
                'clustering_strength': self._assess_clustering_strength(vol_autocorr),
                'persistence_level': self._assess_persistence(vol_autocorr)
            }
            
            # Regime detection
            vol_median = rolling_vol.median()
            high_vol_periods = rolling_vol > vol_median
            low_vol_periods = rolling_vol <= vol_median
            
            # Calculate regime durations
            high_vol_durations = self._calculate_regime_durations(high_vol_periods)
            low_vol_durations = self._calculate_regime_durations(low_vol_periods)
            
            results['regime_detection'] = {
                'high_vol_periods': int(high_vol_periods.sum()),
                'low_vol_periods': int(low_vol_periods.sum()),
                'high_vol_percentage': float(high_vol_periods.sum() / len(rolling_vol) * 100),
                'low_vol_percentage': float(low_vol_periods.sum() / len(rolling_vol) * 100),
                'avg_high_vol_duration': float(np.mean(high_vol_durations)) if high_vol_durations else 0.0,
                'avg_low_vol_duration': float(np.mean(low_vol_durations)) if low_vol_durations else 0.0,
                'max_high_vol_duration': int(max(high_vol_durations)) if high_vol_durations else 0,
                'max_low_vol_duration': int(max(low_vol_durations)) if low_vol_durations else 0
            }
            
            # Persistence analysis
            results['persistence_analysis'] = {
                'volatility_persistence': float(vol_autocorr) if not pd.isna(vol_autocorr) else 0.0,
                'half_life': self._calculate_half_life(vol_autocorr),
                'mean_reversion_speed': self._calculate_mean_reversion_speed(vol_autocorr)
            }
        
        except Exception as e:
            self.logger.error(f"Error analyzing volatility clustering: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def calculate_rolling_volatility(self, returns: pd.Series,
                                   windows: List[int] = [5, 10, 20, 30, 60]) -> Dict[str, Any]:
        """
        Calculate rolling volatility for different windows.
        
        Args:
            returns: Series of returns data
            windows: List of window sizes for rolling volatility
            
        Returns:
            Dictionary with rolling volatility results
        """
        results = {
            'rolling_volatility': {},
            'volatility_comparison': {},
            'volatility_trends': {}
        }
        
        try:
            clean_returns = returns.dropna()
            
            if len(clean_returns) < max(windows):
                results['error'] = f"Insufficient data for rolling volatility calculation (need at least {max(windows)} observations)"
                return results
            
            # Calculate rolling volatility for each window
            for window in windows:
                if len(clean_returns) >= window:
                    rolling_vol = clean_returns.rolling(window=window).std()
                    
                    results['rolling_volatility'][f'window_{window}'] = {
                        'current_volatility': float(rolling_vol.iloc[-1]) if not pd.isna(rolling_vol.iloc[-1]) else 0.0,
                        'mean_volatility': float(rolling_vol.mean()),
                        'std_volatility': float(rolling_vol.std()),
                        'min_volatility': float(rolling_vol.min()),
                        'max_volatility': float(rolling_vol.max())
                    }
            
            # Volatility comparison
            if len(results['rolling_volatility']) > 1:
                current_vols = [data['current_volatility'] for data in results['rolling_volatility'].values()]
                results['volatility_comparison'] = {
                    'volatility_range': float(max(current_vols) - min(current_vols)),
                    'volatility_consistency': float(np.std(current_vols)),
                    'short_term_vol': current_vols[0] if current_vols else 0.0,
                    'long_term_vol': current_vols[-1] if current_vols else 0.0,
                    'volatility_ratio': float(current_vols[0] / current_vols[-1]) if current_vols[-1] != 0 else 0.0
                }
            
            # Volatility trends
            if len(results['rolling_volatility']) >= 2:
                short_vol = results['rolling_volatility'].get('window_5', {}).get('current_volatility', 0)
                long_vol = results['rolling_volatility'].get('window_20', {}).get('current_volatility', 0)
                
                results['volatility_trends'] = {
                    'trend_direction': 'increasing' if short_vol > long_vol else 'decreasing',
                    'trend_strength': float(abs(short_vol - long_vol) / long_vol * 100) if long_vol != 0 else 0.0,
                    'volatility_regime': self._classify_volatility_regime(short_vol, long_vol)
                }
        
        except Exception as e:
            self.logger.error(f"Error calculating rolling volatility: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _get_model_equation(self, model_type: str, parameters: Dict[str, Any]) -> str:
        """Get model equation string."""
        if model_type == 'GARCH':
            return f"σ²ₜ = ω + α₁ε²ₜ₋₁ + β₁σ²ₜ₋₁"
        elif model_type == 'EGARCH':
            return f"log(σ²ₜ) = ω + α₁|εₜ₋₁/σₜ₋₁| + γ₁εₜ₋₁/σₜ₋₁ + β₁log(σ²ₜ₋₁)"
        elif model_type == 'GJR-GARCH':
            return f"σ²ₜ = ω + α₁ε²ₜ₋₁ + γ₁Iₜ₋₁ε²ₜ₋₁ + β₁σ²ₜ₋₁"
        else:
            return "Unknown model"
    
    def _calculate_persistence(self, parameters: Dict[str, Any]) -> float:
        """Calculate model persistence."""
        alpha_sum = sum(parameters.get('alpha', [0]))
        beta_sum = sum(parameters.get('beta', [0]))
        return alpha_sum + beta_sum
    
    def _calculate_unconditional_variance(self, parameters: Dict[str, Any]) -> float:
        """Calculate unconditional variance."""
        omega = parameters.get('omega', 0)
        persistence = self._calculate_persistence(parameters)
        
        if persistence >= 1:
            return float('inf')
        else:
            return omega / (1 - persistence)
    
    def _assess_clustering_strength(self, autocorr: float) -> str:
        """Assess volatility clustering strength."""
        abs_autocorr = abs(autocorr)
        if abs_autocorr >= 0.3:
            return 'strong'
        elif abs_autocorr >= 0.1:
            return 'moderate'
        else:
            return 'weak'
    
    def _assess_persistence(self, autocorr: float) -> str:
        """Assess volatility persistence."""
        if autocorr >= 0.5:
            return 'high'
        elif autocorr >= 0.2:
            return 'moderate'
        else:
            return 'low'
    
    def _calculate_regime_durations(self, regime_series: pd.Series) -> List[int]:
        """Calculate durations of regime periods."""
        durations = []
        current_duration = 0
        
        for is_regime in regime_series:
            if is_regime:
                current_duration += 1
            else:
                if current_duration > 0:
                    durations.append(current_duration)
                    current_duration = 0
        
        # Add final duration if series ends in regime
        if current_duration > 0:
            durations.append(current_duration)
        
        return durations
    
    def _calculate_half_life(self, autocorr: float) -> float:
        """Calculate half-life of volatility shocks."""
        if autocorr <= 0:
            return float('inf')
        else:
            return -np.log(2) / np.log(autocorr)
    
    def _calculate_mean_reversion_speed(self, autocorr: float) -> float:
        """Calculate mean reversion speed."""
        return 1 - autocorr
    
    def _classify_volatility_regime(self, short_vol: float, long_vol: float) -> str:
        """Classify volatility regime."""
        if short_vol > long_vol * 1.2:
            return 'high_volatility'
        elif short_vol < long_vol * 0.8:
            return 'low_volatility'
        else:
            return 'normal_volatility'
