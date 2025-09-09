"""
Indicator Integration for Pocket Hedge Fund.

This module integrates existing technical indicators with the fund management system.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import sys
import os

# Add the src directory to the path to import calculation modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from calculation.indicators import (
    # Trend indicators
    ema_ind, sma_ind, adx_ind, sar_ind, supertrend_ind, wave_ind,
    # Oscillators
    rsi_ind, stoch_ind, cci_ind,
    # Momentum
    macd_ind, stochoscillator_ind,
    # Volatility
    atr_ind, bb_ind,
    # Volume
    obv_ind, vwap_ind,
    # Support/Resistance
    pivot_ind, fiboretr_ind, donchain_ind,
    # Predictive
    hma_ind, tsforecast_ind,
    # Probability
    kelly_ind, montecarlo_ind,
    # Sentiment
    feargreed_ind, cot_ind, putcallratio_ind
)

logger = logging.getLogger(__name__)

class IndicatorIntegration:
    """Integrates existing technical indicators with fund management."""
    
    def __init__(self):
        """Initialize indicator integration."""
        self.indicators = {}
        self.calculated_indicators = {}
        
    async def calculate_indicators(self, data: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """Calculate all available indicators for given data."""
        try:
            logger.info(f"Calculating indicators for {symbol}")
            
            if data.empty:
                raise ValueError("No data provided for indicator calculation")
            
            # Ensure we have required columns
            required_columns = ['open', 'high', 'low', 'close', 'volume']
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            indicators = {}
            
            # Trend Indicators
            try:
                indicators['ema_20'] = await self._calculate_ema(data, 20)
                indicators['ema_50'] = await self._calculate_ema(data, 50)
                indicators['sma_20'] = await self._calculate_sma(data, 20)
                indicators['sma_50'] = await self._calculate_sma(data, 50)
                indicators['adx'] = await self._calculate_adx(data)
                indicators['sar'] = await self._calculate_sar(data)
                indicators['supertrend'] = await self._calculate_supertrend(data)
                indicators['wave'] = await self._calculate_wave(data)
            except Exception as e:
                logger.warning(f"Error calculating trend indicators: {e}")
            
            # Oscillators
            try:
                indicators['rsi'] = await self._calculate_rsi(data)
                indicators['stoch'] = await self._calculate_stoch(data)
                indicators['cci'] = await self._calculate_cci(data)
            except Exception as e:
                logger.warning(f"Error calculating oscillators: {e}")
            
            # Momentum
            try:
                indicators['macd'] = await self._calculate_macd(data)
                indicators['stoch_oscillator'] = await self._calculate_stoch_oscillator(data)
            except Exception as e:
                logger.warning(f"Error calculating momentum indicators: {e}")
            
            # Volatility
            try:
                indicators['atr'] = await self._calculate_atr(data)
                indicators['bollinger_bands'] = await self._calculate_bollinger_bands(data)
            except Exception as e:
                logger.warning(f"Error calculating volatility indicators: {e}")
            
            # Volume
            try:
                indicators['obv'] = await self._calculate_obv(data)
                indicators['vwap'] = await self._calculate_vwap(data)
            except Exception as e:
                logger.warning(f"Error calculating volume indicators: {e}")
            
            # Support/Resistance
            try:
                indicators['pivot_points'] = await self._calculate_pivot_points(data)
                indicators['fibonacci_retracements'] = await self._calculate_fibonacci(data)
                indicators['donchian_channels'] = await self._calculate_donchian(data)
            except Exception as e:
                logger.warning(f"Error calculating support/resistance indicators: {e}")
            
            # Predictive
            try:
                indicators['hma'] = await self._calculate_hma(data)
                indicators['time_series_forecast'] = await self._calculate_ts_forecast(data)
            except Exception as e:
                logger.warning(f"Error calculating predictive indicators: {e}")
            
            # Probability
            try:
                indicators['kelly_criterion'] = await self._calculate_kelly(data)
                indicators['monte_carlo'] = await self._calculate_monte_carlo(data)
            except Exception as e:
                logger.warning(f"Error calculating probability indicators: {e}")
            
            # Sentiment
            try:
                indicators['fear_greed'] = await self._calculate_fear_greed()
                indicators['cot'] = await self._calculate_cot()
                indicators['put_call_ratio'] = await self._calculate_put_call_ratio()
            except Exception as e:
                logger.warning(f"Error calculating sentiment indicators: {e}")
            
            # Store calculated indicators
            self.calculated_indicators[symbol] = indicators
            
            logger.info(f"Successfully calculated {len(indicators)} indicators for {symbol}")
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators for {symbol}: {e}")
            raise
    
    async def _calculate_ema(self, data: pd.DataFrame, period: int) -> pd.Series:
        """Calculate Exponential Moving Average."""
        try:
            return ema_ind.calculate(data['close'], period)
        except Exception as e:
            logger.error(f"Error calculating EMA {period}: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_sma(self, data: pd.DataFrame, period: int) -> pd.Series:
        """Calculate Simple Moving Average."""
        try:
            return sma_ind.calculate(data['close'], period)
        except Exception as e:
            logger.error(f"Error calculating SMA {period}: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_adx(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Average Directional Index."""
        try:
            return adx_ind.calculate(data['high'], data['low'], data['close'])
        except Exception as e:
            logger.error(f"Error calculating ADX: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_sar(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Parabolic SAR."""
        try:
            return sar_ind.calculate(data['high'], data['low'])
        except Exception as e:
            logger.error(f"Error calculating SAR: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_supertrend(self, data: pd.DataFrame) -> pd.Series:
        """Calculate SuperTrend indicator."""
        try:
            return supertrend_ind.calculate(data['high'], data['low'], data['close'])
        except Exception as e:
            logger.error(f"Error calculating SuperTrend: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_wave(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Wave indicator."""
        try:
            return wave_ind.calculate(data['close'])
        except Exception as e:
            logger.error(f"Error calculating Wave: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_rsi(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Relative Strength Index."""
        try:
            return rsi_ind.calculate(data['close'])
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_stoch(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Stochastic Oscillator."""
        try:
            return stoch_ind.calculate(data['high'], data['low'], data['close'])
        except Exception as e:
            logger.error(f"Error calculating Stochastic: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_cci(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Commodity Channel Index."""
        try:
            return cci_ind.calculate(data['high'], data['low'], data['close'])
        except Exception as e:
            logger.error(f"Error calculating CCI: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_macd(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculate MACD."""
        try:
            return macd_ind.calculate(data['close'])
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return {}
    
    async def _calculate_stoch_oscillator(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Stochastic Oscillator."""
        try:
            return stochoscillator_ind.calculate(data['high'], data['low'], data['close'])
        except Exception as e:
            logger.error(f"Error calculating Stochastic Oscillator: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_atr(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Average True Range."""
        try:
            return atr_ind.calculate(data['high'], data['low'], data['close'])
        except Exception as e:
            logger.error(f"Error calculating ATR: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_bollinger_bands(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands."""
        try:
            return bb_ind.calculate(data['close'])
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            return {}
    
    async def _calculate_obv(self, data: pd.DataFrame) -> pd.Series:
        """Calculate On-Balance Volume."""
        try:
            return obv_ind.calculate(data['close'], data['volume'])
        except Exception as e:
            logger.error(f"Error calculating OBV: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_vwap(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Volume Weighted Average Price."""
        try:
            return vwap_ind.calculate(data['high'], data['low'], data['close'], data['volume'])
        except Exception as e:
            logger.error(f"Error calculating VWAP: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_pivot_points(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate Pivot Points."""
        try:
            return pivot_ind.calculate(data['high'], data['low'], data['close'])
        except Exception as e:
            logger.error(f"Error calculating Pivot Points: {e}")
            return {}
    
    async def _calculate_fibonacci(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate Fibonacci Retracements."""
        try:
            return fiboretr_ind.calculate(data['high'], data['low'])
        except Exception as e:
            logger.error(f"Error calculating Fibonacci: {e}")
            return {}
    
    async def _calculate_donchian(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculate Donchian Channels."""
        try:
            return donchain_ind.calculate(data['high'], data['low'])
        except Exception as e:
            logger.error(f"Error calculating Donchian Channels: {e}")
            return {}
    
    async def _calculate_hma(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Hull Moving Average."""
        try:
            return hma_ind.calculate(data['close'])
        except Exception as e:
            logger.error(f"Error calculating HMA: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_ts_forecast(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Time Series Forecast."""
        try:
            return tsforecast_ind.calculate(data['close'])
        except Exception as e:
            logger.error(f"Error calculating Time Series Forecast: {e}")
            return pd.Series(dtype=float)
    
    async def _calculate_kelly(self, data: pd.DataFrame) -> float:
        """Calculate Kelly Criterion."""
        try:
            returns = data['close'].pct_change().dropna()
            return kelly_ind.calculate(returns)
        except Exception as e:
            logger.error(f"Error calculating Kelly Criterion: {e}")
            return 0.0
    
    async def _calculate_monte_carlo(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate Monte Carlo simulation."""
        try:
            returns = data['close'].pct_change().dropna()
            return montecarlo_ind.calculate(returns)
        except Exception as e:
            logger.error(f"Error calculating Monte Carlo: {e}")
            return {}
    
    async def _calculate_fear_greed(self) -> int:
        """Calculate Fear & Greed Index."""
        try:
            return feargreed_ind.calculate()
        except Exception as e:
            logger.error(f"Error calculating Fear & Greed: {e}")
            return 50  # Neutral
    
    async def _calculate_cot(self) -> Dict[str, Any]:
        """Calculate Commitments of Traders."""
        try:
            return cot_ind.calculate()
        except Exception as e:
            logger.error(f"Error calculating COT: {e}")
            return {}
    
    async def _calculate_put_call_ratio(self) -> float:
        """Calculate Put/Call Ratio."""
        try:
            return putcallratio_ind.calculate()
        except Exception as e:
            logger.error(f"Error calculating Put/Call Ratio: {e}")
            return 1.0
    
    def get_trading_signals(self, symbol: str) -> Dict[str, Any]:
        """Generate trading signals based on calculated indicators."""
        try:
            if symbol not in self.calculated_indicators:
                raise ValueError(f"No indicators calculated for {symbol}")
            
            indicators = self.calculated_indicators[symbol]
            signals = {
                'symbol': symbol,
                'timestamp': datetime.now(),
                'signals': {},
                'overall_signal': 'NEUTRAL',
                'confidence': 0.0
            }
            
            # Generate signals based on indicators
            signal_scores = []
            
            # RSI signals
            if 'rsi' in indicators and not indicators['rsi'].empty:
                rsi_latest = indicators['rsi'].iloc[-1]
                if rsi_latest > 70:
                    signals['signals']['rsi'] = 'SELL'
                    signal_scores.append(-1)
                elif rsi_latest < 30:
                    signals['signals']['rsi'] = 'BUY'
                    signal_scores.append(1)
                else:
                    signals['signals']['rsi'] = 'NEUTRAL'
                    signal_scores.append(0)
            
            # MACD signals
            if 'macd' in indicators and isinstance(indicators['macd'], dict):
                macd_line = indicators['macd'].get('macd_line')
                signal_line = indicators['macd'].get('signal_line')
                if macd_line is not None and signal_line is not None:
                    if not macd_line.empty and not signal_line.empty:
                        if macd_line.iloc[-1] > signal_line.iloc[-1]:
                            signals['signals']['macd'] = 'BUY'
                            signal_scores.append(1)
                        else:
                            signals['signals']['macd'] = 'SELL'
                            signal_scores.append(-1)
            
            # Moving Average signals
            if 'ema_20' in indicators and 'ema_50' in indicators:
                ema_20 = indicators['ema_20']
                ema_50 = indicators['ema_50']
                if not ema_20.empty and not ema_50.empty:
                    if ema_20.iloc[-1] > ema_50.iloc[-1]:
                        signals['signals']['ma_trend'] = 'BUY'
                        signal_scores.append(1)
                    else:
                        signals['signals']['ma_trend'] = 'SELL'
                        signal_scores.append(-1)
            
            # Calculate overall signal
            if signal_scores:
                avg_score = sum(signal_scores) / len(signal_scores)
                signals['confidence'] = abs(avg_score)
                
                if avg_score > 0.3:
                    signals['overall_signal'] = 'BUY'
                elif avg_score < -0.3:
                    signals['overall_signal'] = 'SELL'
                else:
                    signals['overall_signal'] = 'NEUTRAL'
            
            return signals
            
        except Exception as e:
            logger.error(f"Error generating trading signals for {symbol}: {e}")
            return {
                'symbol': symbol,
                'timestamp': datetime.now(),
                'signals': {},
                'overall_signal': 'ERROR',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_indicator_summary(self, symbol: str) -> Dict[str, Any]:
        """Get summary of calculated indicators for a symbol."""
        try:
            if symbol not in self.calculated_indicators:
                return {}
            
            indicators = self.calculated_indicators[symbol]
            summary = {
                'symbol': symbol,
                'timestamp': datetime.now(),
                'indicators': {}
            }
            
            for name, indicator in indicators.items():
                if isinstance(indicator, pd.Series):
                    if not indicator.empty:
                        summary['indicators'][name] = {
                            'latest_value': float(indicator.iloc[-1]),
                            'mean': float(indicator.mean()),
                            'std': float(indicator.std()),
                            'min': float(indicator.min()),
                            'max': float(indicator.max())
                        }
                elif isinstance(indicator, dict):
                    summary['indicators'][name] = {
                        'keys': list(indicator.keys()),
                        'latest_values': {}
                    }
                    for key, value in indicator.items():
                        if isinstance(value, pd.Series) and not value.empty:
                            summary['indicators'][name]['latest_values'][key] = float(value.iloc[-1])
                        else:
                            summary['indicators'][name]['latest_values'][key] = value
                else:
                    summary['indicators'][name] = {
                        'value': indicator,
                        'type': type(indicator).__name__
                    }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting indicator summary for {symbol}: {e}")
            return {}
