"""
Simplified Indicator Integration for Pocket Hedge Fund.

This module provides simplified technical indicators for demonstration.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class IndicatorIntegration:
    """Simplified indicator integration for demonstration."""
    
    def __init__(self):
        """Initialize indicator integration."""
        self.indicators = {}
        self.calculated_indicators = {}
        
    async def calculate_indicators(self, data: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """Calculate simplified indicators for given data."""
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
            
            # Simple Moving Average
            try:
                indicators['sma_20'] = self._calculate_sma(data['close'], 20)
                indicators['sma_50'] = self._calculate_sma(data['close'], 50)
            except Exception as e:
                logger.warning(f"Error calculating SMA: {e}")
            
            # Exponential Moving Average
            try:
                indicators['ema_20'] = self._calculate_ema(data['close'], 20)
                indicators['ema_50'] = self._calculate_ema(data['close'], 50)
            except Exception as e:
                logger.warning(f"Error calculating EMA: {e}")
            
            # RSI
            try:
                indicators['rsi'] = self._calculate_rsi(data['close'])
            except Exception as e:
                logger.warning(f"Error calculating RSI: {e}")
            
            # MACD
            try:
                indicators['macd'] = self._calculate_macd(data['close'])
            except Exception as e:
                logger.warning(f"Error calculating MACD: {e}")
            
            # Bollinger Bands
            try:
                indicators['bollinger_bands'] = self._calculate_bollinger_bands(data['close'])
            except Exception as e:
                logger.warning(f"Error calculating Bollinger Bands: {e}")
            
            # Volume indicators
            try:
                indicators['volume_sma'] = self._calculate_sma(data['volume'], 20)
            except Exception as e:
                logger.warning(f"Error calculating Volume SMA: {e}")
            
            # Store calculated indicators
            self.calculated_indicators[symbol] = indicators
            
            logger.info(f"Successfully calculated {len(indicators)} indicators for {symbol}")
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators for {symbol}: {e}")
            raise
    
    def _calculate_sma(self, data: pd.Series, period: int) -> pd.Series:
        """Calculate Simple Moving Average."""
        return data.rolling(window=period).mean()
    
    def _calculate_ema(self, data: pd.Series, period: int) -> pd.Series:
        """Calculate Exponential Moving Average."""
        return data.ewm(span=period).mean()
    
    def _calculate_rsi(self, data: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """Calculate MACD."""
        ema_fast = self._calculate_ema(data, fast)
        ema_slow = self._calculate_ema(data, slow)
        macd_line = ema_fast - ema_slow
        signal_line = self._calculate_ema(macd_line, signal)
        histogram = macd_line - signal_line
        
        return {
            'macd_line': macd_line,
            'signal_line': signal_line,
            'histogram': histogram
        }
    
    def _calculate_bollinger_bands(self, data: pd.Series, period: int = 20, std_dev: float = 2) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands."""
        sma = self._calculate_sma(data, period)
        std = data.rolling(window=period).std()
        
        return {
            'upper_band': sma + (std * std_dev),
            'middle_band': sma,
            'lower_band': sma - (std * std_dev)
        }
    
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
                if not pd.isna(rsi_latest):
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
                        macd_latest = macd_line.iloc[-1]
                        signal_latest = signal_line.iloc[-1]
                        if not pd.isna(macd_latest) and not pd.isna(signal_latest):
                            if macd_latest > signal_latest:
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
                    ema_20_latest = ema_20.iloc[-1]
                    ema_50_latest = ema_50.iloc[-1]
                    if not pd.isna(ema_20_latest) and not pd.isna(ema_50_latest):
                        if ema_20_latest > ema_50_latest:
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
                        # Get latest non-NaN value
                        latest_value = indicator.dropna().iloc[-1] if not indicator.dropna().empty else None
                        if latest_value is not None:
                            summary['indicators'][name] = {
                                'latest_value': float(latest_value),
                                'mean': float(indicator.mean()) if not indicator.empty else None,
                                'std': float(indicator.std()) if not indicator.empty else None,
                                'min': float(indicator.min()) if not indicator.empty else None,
                                'max': float(indicator.max()) if not indicator.empty else None
                            }
                elif isinstance(indicator, dict):
                    summary['indicators'][name] = {
                        'keys': list(indicator.keys()),
                        'latest_values': {}
                    }
                    for key, value in indicator.items():
                        if isinstance(value, pd.Series) and not value.empty:
                            latest_value = value.dropna().iloc[-1] if not value.dropna().empty else None
                            if latest_value is not None:
                                summary['indicators'][name]['latest_values'][key] = float(latest_value)
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
