# -*- coding: utf-8 -*-
"""
Time Series Analysis Module for NeoZork HLD Prediction.

This module provides comprehensive time series analysis capabilities including:
- Stationarity testing
- Trend analysis
- Seasonality detection
- Volatility analysis
- Autocorrelation analysis
- Forecasting capabilities
- Time series decomposition
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.signal import periodogram
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
from typing import Dict, List, Optional, Tuple, Union, Any
from pathlib import Path
import os
import json
from datetime import datetime, timedelta

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Set seaborn style
sns.set(style="whitegrid", palette="husl")


class TimeSeriesAnalyzer:
    """
    Comprehensive time series analysis tool for financial data.
    
    This class provides methods for analyzing time series data including:
    - Stationarity testing
    - Trend and seasonality analysis
    - Volatility modeling
    - Autocorrelation analysis
    - Forecasting
    """
    
    def __init__(self, data: pd.DataFrame = None):
        """
        Initialize the time series analyzer.
        
        Args:
            data: Input DataFrame with time series data
        """
        self.data = data
        self.results = {}
        self.plots_dir = self._ensure_plots_directory()
        
    def _ensure_plots_directory(self) -> Path:
        """Ensure plots directory exists."""
        plots_dir = Path("results/plots/time_series")
        plots_dir.mkdir(parents=True, exist_ok=True)
        return plots_dir
        
    def set_data(self, data: pd.DataFrame):
        """Set the data for analysis."""
        self.data = data.copy()
        
    def _ensure_datetime_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure DataFrame has a proper datetime index."""
        df = df.copy()
        
        # Check if index is already datetime
        if isinstance(df.index, pd.DatetimeIndex):
            return df
            
        # Try to convert common date columns
        date_columns = ['date', 'time', 'timestamp', 'datetime', 'Date', 'Time']
        for col in date_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                    df.set_index(col, inplace=True)
                    return df
                except:
                    continue
                    
        # If no date column found, create a simple index
        if len(df) > 0:
            df.index = pd.date_range(start='2020-01-01', periods=len(df), freq='D')
            
        return df
        
    def analyze_stationarity(self, column: str = None) -> Dict[str, Any]:
        """
        Perform comprehensive stationarity analysis.
        
        Args:
            column: Column to analyze (if None, uses first numeric column)
            
        Returns:
            Dictionary with stationarity test results
        """
        if self.data is None:
            raise ValueError("No data provided for analysis")
            
        # Select column to analyze
        if column is None:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                raise ValueError("No numeric columns found in data")
            column = numeric_cols[0]
            
        series = self.data[column].dropna()
        
        if len(series) == 0:
            raise ValueError("No numeric columns found in data")
        
        if len(series) < 50:
            raise ValueError(f"Insufficient data for stationarity analysis. Need at least 50 observations, got {len(series)}")
            
        results = {
            'column': column,
            'length': len(series),
            'tests': {}
        }
        
        # Augmented Dickey-Fuller test
        try:
            adf_result = adfuller(series, regression='ct', autolag='AIC')
            results['tests']['adf'] = {
                'statistic': adf_result[0],
                'p_value': adf_result[1],
                'critical_values': adf_result[4],
                'is_stationary': adf_result[1] < 0.05
            }
        except Exception as e:
            results['tests']['adf'] = {'error': str(e)}
            
        # KPSS test
        try:
            kpss_result = kpss(series, regression='ct')
            results['tests']['kpss'] = {
                'statistic': kpss_result[0],
                'p_value': kpss_result[1],
                'critical_values': kpss_result[3],
                'is_stationary': kpss_result[1] > 0.05
            }
        except Exception as e:
            results['tests']['kpss'] = {'error': str(e)}
            
        # Visual analysis
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Stationarity Analysis: {column}', fontsize=16)
        
        # Original series
        axes[0, 0].plot(series.index, series.values)
        axes[0, 0].set_title('Original Time Series')
        axes[0, 0].set_xlabel('Time')
        axes[0, 0].set_ylabel('Value')
        
        # Rolling statistics
        rolling_mean = series.rolling(window=min(20, len(series)//4)).mean()
        rolling_std = series.rolling(window=min(20, len(series)//4)).std()
        
        axes[0, 1].plot(series.index, series.values, label='Original', alpha=0.7)
        axes[0, 1].plot(rolling_mean.index, rolling_mean.values, label='Rolling Mean', linewidth=2)
        axes[0, 1].plot(rolling_std.index, rolling_std.values, label='Rolling Std', linewidth=2)
        axes[0, 1].set_title('Rolling Statistics')
        axes[0, 1].set_xlabel('Time')
        axes[0, 1].set_ylabel('Value')
        axes[0, 1].legend()
        
        # Histogram
        axes[1, 0].hist(series.values, bins=30, alpha=0.7, edgecolor='black')
        axes[1, 0].set_title('Distribution')
        axes[1, 0].set_xlabel('Value')
        axes[1, 0].set_ylabel('Frequency')
        
        # Q-Q plot
        stats.probplot(series.values, dist="norm", plot=axes[1, 1])
        axes[1, 1].set_title('Q-Q Plot (Normal)')
        
        plt.tight_layout()
        
        # Save plot
        plot_path = self.plots_dir / f"stationarity_analysis_{column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        results['plot_path'] = str(plot_path)
        self.results['stationarity'] = results
        
        return results
        
    def analyze_trends(self, column: str = None, window: int = None) -> Dict[str, Any]:
        """
        Analyze trends in the time series.
        
        Args:
            column: Column to analyze
            window: Rolling window size for trend analysis
            
        Returns:
            Dictionary with trend analysis results
        """
        if self.data is None:
            raise ValueError("No data provided for analysis")
            
        if column is None:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                raise ValueError("No numeric columns found in data")
            column = numeric_cols[0]
            
        series = self.data[column].dropna()
        
        if window is None:
            window = min(20, len(series) // 4)
            
        results = {
            'column': column,
            'window': window,
            'trend_analysis': {}
        }
        
        # Linear trend
        x = np.arange(len(series))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, series.values)
        
        results['trend_analysis']['linear'] = {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_value**2,
            'p_value': p_value,
            'std_error': std_err,
            'trend_direction': 'increasing' if slope > 0 else 'decreasing'
        }
        
        # Moving averages
        ma_short = series.rolling(window=window).mean()
        ma_long = series.rolling(window=window*2).mean()
        
        # Trend strength using linear regression on moving averages
        ma_long_clean = ma_long.dropna()
        if len(ma_long_clean) > 1:
            x_ma = np.arange(len(ma_long_clean))
            ma_trend_slope, _, _, _, _ = stats.linregress(x_ma, ma_long_clean.values)
        else:
            ma_trend_slope = 0
        
        results['trend_analysis']['moving_averages'] = {
            'short_ma_window': window,
            'long_ma_window': window * 2,
            'trend_strength': abs(ma_trend_slope),
            'trend_direction': 'increasing' if ma_trend_slope > 0 else 'decreasing'
        }
        
        # Visual analysis
        fig, axes = plt.subplots(2, 1, figsize=(15, 10))
        fig.suptitle(f'Trend Analysis: {column}', fontsize=16)
        
        # Original series with trend lines
        axes[0].plot(series.index, series.values, label='Original', alpha=0.7)
        axes[0].plot(series.index, slope * x + intercept, 'r--', label=f'Linear Trend (slope={slope:.4f})', linewidth=2)
        axes[0].plot(ma_short.index, ma_short.values, 'g-', label=f'MA({window})', linewidth=2)
        axes[0].plot(ma_long.index, ma_long.values, 'b-', label=f'MA({window*2})', linewidth=2)
        axes[0].set_title('Time Series with Trend Lines')
        axes[0].set_xlabel('Time')
        axes[0].set_ylabel('Value')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Trend strength over time
        trend_strength = []
        for i in range(window, len(series)):
            window_data = series.iloc[i-window:i]
            if len(window_data) >= 2:
                x_window = np.arange(len(window_data))
                slope_window, _, _, _, _ = stats.linregress(x_window, window_data.values)
                trend_strength.append(abs(slope_window))
            else:
                trend_strength.append(np.nan)
                
        axes[1].plot(series.index[window:], trend_strength, 'purple', linewidth=2)
        axes[1].set_title('Trend Strength Over Time')
        axes[1].set_xlabel('Time')
        axes[1].set_ylabel('Trend Strength')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        plot_path = self.plots_dir / f"trend_analysis_{column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        results['plot_path'] = str(plot_path)
        self.results['trends'] = results
        
        return results
        
    def analyze_seasonality(self, column: str = None, period: int = None) -> Dict[str, Any]:
        """
        Analyze seasonality in the time series.
        
        Args:
            column: Column to analyze
            period: Seasonal period (if None, will be auto-detected)
            
        Returns:
            Dictionary with seasonality analysis results
        """
        if self.data is None:
            raise ValueError("No data provided for analysis")
            
        if column is None:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                raise ValueError("No numeric columns found in data")
            column = numeric_cols[0]
            
        series = self.data[column].dropna()
        
        if len(series) < 100:
            raise ValueError(f"Insufficient data for seasonality analysis. Need at least 100 observations, got {len(series)}")
            
        results = {
            'column': column,
            'seasonality_analysis': {}
        }
        
        # Auto-detect period using FFT
        if period is None:
            # Compute periodogram
            freqs, power = periodogram(series.values, fs=1.0)
            # Find dominant frequency (excluding DC component)
            dominant_freq_idx = np.argmax(power[1:]) + 1
            period = int(1 / freqs[dominant_freq_idx]) if freqs[dominant_freq_idx] > 0 else 12
            
        results['detected_period'] = period
        
        # Seasonal decomposition
        try:
            decomposition = seasonal_decompose(series, period=period, extrapolate_trend='freq')
            
            # Calculate seasonal strength
            seasonal_strength = np.std(decomposition.seasonal) / np.std(decomposition.resid + decomposition.seasonal)
            
            results['seasonality_analysis']['decomposition'] = {
                'trend': decomposition.trend.tolist(),
                'seasonal': decomposition.seasonal.tolist(),
                'residual': decomposition.resid.tolist(),
                'seasonal_strength': seasonal_strength,
                'has_seasonality': seasonal_strength > 0.1
            }
            
        except Exception as e:
            results['seasonality_analysis']['decomposition'] = {'error': str(e)}
            
        # Visual analysis
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        fig.suptitle(f'Seasonality Analysis: {column}', fontsize=16)
        
        # Original series
        axes[0].plot(series.index, series.values)
        axes[0].set_title('Original Time Series')
        axes[0].set_ylabel('Value')
        axes[0].grid(True, alpha=0.3)
        
        # Trend
        if 'decomposition' in results['seasonality_analysis'] and 'error' not in results['seasonality_analysis']['decomposition']:
            axes[1].plot(series.index, decomposition.trend)
            axes[1].set_title('Trend Component')
            axes[1].set_ylabel('Value')
            axes[1].grid(True, alpha=0.3)
            
            # Seasonal
            axes[2].plot(series.index, decomposition.seasonal)
            axes[2].set_title(f'Seasonal Component (Period={period})')
            axes[2].set_ylabel('Value')
            axes[2].grid(True, alpha=0.3)
            
            # Residual
            axes[3].plot(series.index, decomposition.resid)
            axes[3].set_title('Residual Component')
            axes[3].set_xlabel('Time')
            axes[3].set_ylabel('Value')
            axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        plot_path = self.plots_dir / f"seasonality_analysis_{column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        results['plot_path'] = str(plot_path)
        self.results['seasonality'] = results
        
        return results
        
    def analyze_volatility(self, column: str = None, window: int = None) -> Dict[str, Any]:
        """
        Analyze volatility patterns in the time series.
        
        Args:
            column: Column to analyze
            window: Rolling window size for volatility calculation
            
        Returns:
            Dictionary with volatility analysis results
        """
        if self.data is None:
            raise ValueError("No data provided for analysis")
            
        if column is None:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                raise ValueError("No numeric columns found in data")
            column = numeric_cols[0]
            
        series = self.data[column].dropna()
        
        if window is None:
            window = min(20, len(series) // 4)
            
        results = {
            'column': column,
            'window': window,
            'volatility_analysis': {}
        }
        
        # Calculate returns
        returns = series.pct_change().dropna()
        
        # Rolling volatility
        rolling_vol = returns.rolling(window=window).std() * np.sqrt(252)  # Annualized
        
        # Volatility clustering test
        vol_clustering = returns.rolling(window=window).std()
        vol_autocorr = vol_clustering.autocorr(lag=1)
        
        # GARCH-like volatility persistence
        vol_persistence = vol_clustering.rolling(window=window).mean()
        
        results['volatility_analysis'] = {
            'mean_volatility': rolling_vol.mean(),
            'volatility_of_volatility': rolling_vol.std(),
            'volatility_clustering': vol_autocorr,
            'has_clustering': abs(vol_autocorr) > 0.1,
            'min_volatility': rolling_vol.min(),
            'max_volatility': rolling_vol.max(),
            'volatility_percentiles': {
                '25%': rolling_vol.quantile(0.25),
                '50%': rolling_vol.quantile(0.50),
                '75%': rolling_vol.quantile(0.75)
            }
        }
        
        # Visual analysis
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        fig.suptitle(f'Volatility Analysis: {column}', fontsize=16)
        
        # Returns
        axes[0].plot(returns.index, returns.values, alpha=0.7)
        axes[0].set_title('Returns')
        axes[0].set_ylabel('Return')
        axes[0].grid(True, alpha=0.3)
        
        # Rolling volatility
        axes[1].plot(rolling_vol.index, rolling_vol.values, 'r-', linewidth=2)
        axes[1].axhline(y=rolling_vol.mean(), color='b', linestyle='--', label=f'Mean: {rolling_vol.mean():.4f}')
        axes[1].set_title(f'Rolling Volatility (Window={window})')
        axes[1].set_ylabel('Volatility')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Volatility distribution
        axes[2].hist(rolling_vol.dropna().values, bins=30, alpha=0.7, edgecolor='black')
        axes[2].set_title('Volatility Distribution')
        axes[2].set_xlabel('Volatility')
        axes[2].set_ylabel('Frequency')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        plot_path = self.plots_dir / f"volatility_analysis_{column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        results['plot_path'] = str(plot_path)
        self.results['volatility'] = results
        
        return results
        
    def analyze_autocorrelation(self, column: str = None, max_lag: int = 50) -> Dict[str, Any]:
        """
        Analyze autocorrelation patterns in the time series.
        
        Args:
            column: Column to analyze
            max_lag: Maximum lag for autocorrelation analysis
            
        Returns:
            Dictionary with autocorrelation analysis results
        """
        if self.data is None:
            raise ValueError("No data provided for analysis")
            
        if column is None:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                raise ValueError("No numeric columns found in data")
            column = numeric_cols[0]
            
        series = self.data[column].dropna()
        
        if len(series) < max_lag * 2:
            max_lag = len(series) // 2
            
        results = {
            'column': column,
            'max_lag': max_lag,
            'autocorrelation_analysis': {}
        }
        
        # Calculate ACF and PACF
        try:
            acf_values = acf(series, nlags=max_lag, fft=True)
            pacf_values = pacf(series, nlags=max_lag)
            
            # Find significant lags
            confidence_interval = 1.96 / np.sqrt(len(series))  # 95% confidence
            
            significant_acf_lags = [i for i in range(1, len(acf_values)) if abs(acf_values[i]) > confidence_interval]
            significant_pacf_lags = [i for i in range(1, len(pacf_values)) if abs(pacf_values[i]) > confidence_interval]
            
            results['autocorrelation_analysis'] = {
                'acf_values': acf_values.tolist(),
                'pacf_values': pacf_values.tolist(),
                'confidence_interval': confidence_interval,
                'significant_acf_lags': significant_acf_lags,
                'significant_pacf_lags': significant_pacf_lags,
                'max_acf_lag': max(significant_acf_lags) if significant_acf_lags else 0,
                'max_pacf_lag': max(significant_pacf_lags) if significant_pacf_lags else 0
            }
            
        except Exception as e:
            results['autocorrelation_analysis'] = {'error': str(e)}
            
        # Visual analysis
        fig, axes = plt.subplots(2, 1, figsize=(15, 10))
        fig.suptitle(f'Autocorrelation Analysis: {column}', fontsize=16)
        
        # ACF plot
        plot_acf(series, lags=max_lag, ax=axes[0], alpha=0.05)
        axes[0].set_title('Autocorrelation Function (ACF)')
        axes[0].grid(True, alpha=0.3)
        
        # PACF plot
        plot_pacf(series, lags=max_lag, ax=axes[1], alpha=0.05)
        axes[1].set_title('Partial Autocorrelation Function (PACF)')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        plot_path = self.plots_dir / f"autocorrelation_analysis_{column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        results['plot_path'] = str(plot_path)
        self.results['autocorrelation'] = results
        
        return results
        
    def forecast_series(self, column: str = None, periods: int = 30, 
                       model_type: str = 'auto') -> Dict[str, Any]:
        """
        Generate forecasts for the time series.
        
        Args:
            column: Column to forecast
            periods: Number of periods to forecast
            model_type: Type of model ('auto', 'arima', 'naive', 'snaive')
            
        Returns:
            Dictionary with forecasting results
        """
        if self.data is None:
            raise ValueError("No data provided for analysis")
            
        if column is None:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                raise ValueError("No numeric columns found in data")
            column = numeric_cols[0]
            
        series = self.data[column].dropna()
        
        if len(series) < 50:
            raise ValueError(f"Insufficient data for forecasting. Need at least 50 observations, got {len(series)}")
            
        results = {
            'column': column,
            'periods': periods,
            'model_type': model_type,
            'forecast_results': {}
        }
        
        # Generate forecasts using different methods
        forecasts = {}
        
        # Naive forecast
        if model_type in ['auto', 'naive']:
            try:
                naive_forecast = series.iloc[-1] * np.ones(periods)
                forecasts['naive'] = naive_forecast.tolist()
            except Exception as e:
                forecasts['naive'] = {'error': str(e)}
                
        # Seasonal naive forecast
        if model_type in ['auto', 'snaive']:
            try:
                # Use last season's values
                seasonal_period = min(12, len(series) // 4)  # Default seasonal period
                seasonal_values = series.iloc[-seasonal_period:].values
                snaive_forecast = []
                for i in range(periods):
                    snaive_forecast.append(seasonal_values[i % seasonal_period])
                forecasts['seasonal_naive'] = snaive_forecast
            except Exception as e:
                forecasts['seasonal_naive'] = {'error': str(e)}
                
        # ARIMA forecast
        if model_type in ['auto', 'arima']:
            try:
                # Simple ARIMA(1,1,1) model
                model = ARIMA(series, order=(1, 1, 1))
                fitted_model = model.fit()
                arima_forecast = fitted_model.forecast(steps=periods)
                forecasts['arima'] = arima_forecast.tolist()
                results['forecast_results']['arima_model_info'] = {
                    'aic': fitted_model.aic,
                    'bic': fitted_model.bic,
                    'params': fitted_model.params.tolist()
                }
            except Exception as e:
                forecasts['arima'] = {'error': str(e)}
                
        results['forecast_results']['forecasts'] = forecasts
        
        # Visual analysis
        fig, ax = plt.subplots(1, 1, figsize=(15, 8))
        fig.suptitle(f'Forecast Analysis: {column}', fontsize=16)
        
        # Plot original series
        ax.plot(series.index, series.values, 'b-', label='Original', linewidth=2)
        
        # Plot forecasts
        forecast_index = pd.date_range(start=series.index[-1], periods=periods+1, freq='D')[1:]
        
        colors = ['r', 'g', 'orange', 'purple']
        for i, (method, forecast) in enumerate(forecasts.items()):
            if isinstance(forecast, list):
                ax.plot(forecast_index, forecast, color=colors[i % len(colors)], 
                       linestyle='--', label=f'{method.title()} Forecast', linewidth=2)
        
        ax.set_title('Time Series Forecast')
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        plot_path = self.plots_dir / f"forecast_analysis_{column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        results['plot_path'] = str(plot_path)
        self.results['forecast'] = results
        
        return results
        
    def comprehensive_analysis(self, column: str = None) -> Dict[str, Any]:
        """
        Perform comprehensive time series analysis.
        
        Args:
            column: Column to analyze
            
        Returns:
            Dictionary with all analysis results
        """
        if self.data is None:
            raise ValueError("No data provided for analysis")
            
        print(f"🔍 Starting comprehensive time series analysis...")
        
        comprehensive_results = {
            'timestamp': datetime.now().isoformat(),
            'column': column,
            'analyses': {}
        }
        
        # Run all analyses
        try:
            print("   📊 Analyzing stationarity...")
            comprehensive_results['analyses']['stationarity'] = self.analyze_stationarity(column)
        except Exception as e:
            comprehensive_results['analyses']['stationarity'] = {'error': str(e)}
            
        try:
            print("   📈 Analyzing trends...")
            comprehensive_results['analyses']['trends'] = self.analyze_trends(column)
        except Exception as e:
            comprehensive_results['analyses']['trends'] = {'error': str(e)}
            
        try:
            print("   🔄 Analyzing seasonality...")
            comprehensive_results['analyses']['seasonality'] = self.analyze_seasonality(column)
        except Exception as e:
            comprehensive_results['analyses']['seasonality'] = {'error': str(e)}
            
        try:
            print("   📊 Analyzing volatility...")
            comprehensive_results['analyses']['volatility'] = self.analyze_volatility(column)
        except Exception as e:
            comprehensive_results['analyses']['volatility'] = {'error': str(e)}
            
        try:
            print("   🔗 Analyzing autocorrelation...")
            comprehensive_results['analyses']['autocorrelation'] = self.analyze_autocorrelation(column)
        except Exception as e:
            comprehensive_results['analyses']['autocorrelation'] = {'error': str(e)}
            
        try:
            print("   🔮 Generating forecasts...")
            comprehensive_results['analyses']['forecast'] = self.forecast_series(column)
        except Exception as e:
            comprehensive_results['analyses']['forecast'] = {'error': str(e)}
            
        # Generate summary
        comprehensive_results['summary'] = self._generate_analysis_summary(comprehensive_results['analyses'])
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_path = self.plots_dir / f"comprehensive_analysis_{column}_{timestamp}.json"
        
        with open(results_path, 'w') as f:
            json.dump(comprehensive_results, f, indent=2, default=str)
            
        comprehensive_results['results_file'] = str(results_path)
        self.results['comprehensive'] = comprehensive_results
        
        print(f"✅ Comprehensive analysis completed! Results saved to: {results_path}")
        
        return comprehensive_results
        
    def _generate_analysis_summary(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of all analyses."""
        summary = {
            'key_findings': [],
            'recommendations': [],
            'data_characteristics': {}
        }
        
        # Stationarity summary
        if 'stationarity' in analyses and 'error' not in analyses['stationarity']:
            stationarity = analyses['stationarity']
            if 'tests' in stationarity:
                adf_test = stationarity['tests'].get('adf', {})
                kpss_test = stationarity['tests'].get('kpss', {})
                
                if adf_test.get('is_stationary', False):
                    summary['key_findings'].append("Series appears to be stationary (ADF test)")
                else:
                    summary['key_findings'].append("Series appears to be non-stationary (ADF test)")
                    summary['recommendations'].append("Consider differencing the series for modeling")
                    
        # Trend summary
        if 'trends' in analyses and 'error' not in analyses['trends']:
            trends = analyses['trends']
            if 'trend_analysis' in trends:
                linear_trend = trends['trend_analysis'].get('linear', {})
                direction = linear_trend.get('trend_direction', 'unknown')
                r_squared = linear_trend.get('r_squared', 0)
                
                summary['key_findings'].append(f"Series shows {direction} trend (R² = {r_squared:.3f})")
                
                if r_squared > 0.5:
                    summary['recommendations'].append("Strong trend detected - consider trend-following models")
                    
        # Seasonality summary
        if 'seasonality' in analyses and 'error' not in analyses['seasonality']:
            seasonality = analyses['seasonality']
            if 'seasonality_analysis' in seasonality:
                decomp = seasonality['seasonality_analysis'].get('decomposition', {})
                seasonal_strength = decomp.get('seasonal_strength', 0)
                has_seasonality = decomp.get('has_seasonality', False)
                
                if has_seasonality:
                    summary['key_findings'].append(f"Strong seasonality detected (strength: {seasonal_strength:.3f})")
                    summary['recommendations'].append("Use seasonal models (SARIMA, seasonal decomposition)")
                else:
                    summary['key_findings'].append("No significant seasonality detected")
                    
        # Volatility summary
        if 'volatility' in analyses and 'error' not in analyses['volatility']:
            volatility = analyses['volatility']
            if 'volatility_analysis' in volatility:
                vol_analysis = volatility['volatility_analysis']
                has_clustering = vol_analysis.get('has_clustering', False)
                
                if has_clustering:
                    summary['key_findings'].append("Volatility clustering detected")
                    summary['recommendations'].append("Consider GARCH models for volatility modeling")
                    
        # Autocorrelation summary
        if 'autocorrelation' in analyses and 'error' not in analyses['autocorrelation']:
            autocorr = analyses['autocorrelation']
            if 'autocorrelation_analysis' in autocorr:
                acf_analysis = autocorr['autocorrelation_analysis']
                max_acf_lag = acf_analysis.get('max_acf_lag', 0)
                
                if max_acf_lag > 0:
                    summary['key_findings'].append(f"Significant autocorrelation up to lag {max_acf_lag}")
                    summary['recommendations'].append(f"Consider ARIMA models with order up to {max_acf_lag}")
                    
        return summary
        
    def get_results(self) -> Dict[str, Any]:
        """Get all analysis results."""
        return self.results
        
    def export_results(self, filepath: str = None) -> str:
        """Export all results to a JSON file."""
        if filepath is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = self.plots_dir / f"time_series_analysis_results_{timestamp}.json"
            
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
            
        return str(filepath)


def analyze_time_series(data: pd.DataFrame, column: str = None) -> Dict[str, Any]:
    """
    Convenience function for quick time series analysis.
    
    Args:
        data: Input DataFrame
        column: Column to analyze
        
    Returns:
        Dictionary with analysis results
    """
    analyzer = TimeSeriesAnalyzer(data)
    
    # If no column specified, use first numeric column
    if column is None:
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            raise ValueError("No numeric columns found in data")
        column = numeric_cols[0]
    
    return analyzer.comprehensive_analysis(column)


if __name__ == "__main__":
    # Example usage
    print("Time Series Analysis Module")
    print("=" * 50)
    print("This module provides comprehensive time series analysis capabilities.")
    print("Use the TimeSeriesAnalyzer class for detailed analysis.")
    print("Use the analyze_time_series() function for quick analysis.")
