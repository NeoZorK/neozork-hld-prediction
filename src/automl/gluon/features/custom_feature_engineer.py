"""
Custom Feature Engineer for trading Strategy Features
create 13 пользовательских признаков for торговой стратегии
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import yaml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class CustomFeatureEngineer:
 """
 Creates custom features for trading strategy based on SCHR, Wave, and Short3 indicators.
 """

 def __init__(self, config_path: Optional[str] = None):
 """
 Initialize Custom Feature Engineer.

 Args:
 config_path: Path to custom features configuration file
 """
 self.config_path = config_path or "src/automl/gluon/config/custom_features_config.yaml"
 self.config = self._load_config()

 def _load_config(self) -> Dict[str, Any]:
 """Load configuration from YAML file."""
 try:
 with open(self.config_path, 'r') as f:
 return yaml.safe_load(f)
 except Exception as e:
 logger.warning(f"Could not load config: {e}. Using default configuration.")
 return self._get_default_config()

 def _get_default_config(self) -> Dict[str, Any]:
 """Get default configuration."""
 return {
 "feature_engineering": {
 "schr_features": [],
 "wave_features": [],
 "short3_features": []
 }
 }

 def create_schr_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 Create SCHR Levels based features.

 Args:
 data: Input data with SCHR columns

 Returns:
 data with SCHR features added
 """
 logger.info("Creating SCHR features...")
 df = data.copy()

 # Feature 1: Trend direction probability
 close_col = 'close' if 'close' in df.columns else 'Close'
 if close_col in df.columns:
 df['trend_direction'] = self._calculate_trend_direction(df[close_col])
 df['trend_direction_prob'] = self._calculate_trend_probability(df['trend_direction'])

 # Feature 2: Yellow line breakout probability
 if all(col in df.columns for col in [close_col, 'yellow_line']):
 df['yellow_breakout'] = self._calculate_yellow_breakout(df[close_col], df['yellow_line'])
 df['yellow_breakout_prob'] = self._calculate_breakout_probability(df['yellow_breakout'])

 # Feature 3: Blue line breakdown probability
 if all(col in df.columns for col in [close_col, 'blue_line']):
 df['blue_breakdown'] = self._calculate_blue_breakdown(df[close_col], df['blue_line'])
 df['blue_breakdown_prob'] = self._calculate_breakdown_probability(df['blue_breakdown'])

 # Feature 4: PV sign probability
 if 'pv' in df.columns:
 df['pv_sign'] = np.where(df['pv'] > 0, 1, -1)
 df['pv_sign_prob'] = self._calculate_pv_sign_probability(df['pv_sign'])

 logger.info(f"Created {len([col for col in df.columns if 'prob' in col])} SCHR features")
 return df

 def create_wave_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 Create Wave indicator based features.

 Args:
 data: Input data with Wave columns

 Returns:
 data with Wave features added
 """
 logger.info("Creating Wave features...")
 df = data.copy()

 # Feature 5: Wave signal 5 candles up probability
 if all(col in df.columns for col in ['signal', 'close']):
 df['wave_5_candles'] = self._calculate_wave_5_candles(df['signal'], df['close'])
 df['wave_5_candles_prob'] = self._calculate_wave_5_candles_probability(df['wave_5_candles'])

 # Feature 6: Wave signal 5% direction probability
 if all(col in df.columns for col in ['signal', 'close']):
 df['wave_5_percent'] = self._calculate_wave_5_percent(df['signal'], df['close'])
 df['wave_5_percent_prob'] = self._calculate_wave_5_percent_probability(df['wave_5_percent'])

 # Feature 7: Wave signal with MA condition 5 candles
 if all(col in df.columns for col in ['signal', 'ma', 'open', 'close']):
 condition = (df['signal'] == 1) & (df['ma'] < df['open'])
 df['wave_ma_5_candles'] = self._calculate_wave_ma_5_candles(condition, df['close'])
 df['wave_ma_5_candles_prob'] = self._calculate_wave_ma_5_candles_probability(df['wave_ma_5_candles'])

 # Feature 8: Wave signal with MA condition 5% direction
 if all(col in df.columns for col in ['signal', 'ma', 'open', 'close']):
 condition = (df['signal'] == 1) & (df['ma'] < df['open'])
 df['wave_ma_5_percent'] = self._calculate_wave_ma_5_percent(condition, df['close'])
 df['wave_ma_5_percent_prob'] = self._calculate_wave_ma_5_percent_probability(df['wave_ma_5_percent'])

 # Feature 9: Wave reverse peak sign probability
 if all(col in df.columns for col in ['reverse', 'close']):
 df['wave_peak_sign'] = self._calculate_wave_peak_sign(df['reverse'], df['close'])
 df['wave_peak_sign_prob'] = self._calculate_wave_peak_sign_probability(df['wave_peak_sign'])

 # Feature 10: Wave reverse peak timing probability
 if all(col in df.columns for col in ['reverse', 'close']):
 df['wave_peak_timing'] = self._calculate_wave_peak_timing(df['reverse'], df['close'])
 df['wave_peak_timing_prob'] = self._calculate_wave_peak_timing_probability(df['wave_peak_timing'])

 logger.info(f"Created {len([col for col in df.columns if 'wave' in col and 'prob' in col])} Wave features")
 return df

 def create_short3_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 Create Short3 indicator based features.

 Args:
 data: Input data with Short3 columns

 Returns:
 data with Short3 features added
 """
 logger.info("Creating Short3 features...")
 df = data.copy()

 # Feature 11: Short3 signal 1 up probability
 if all(col in df.columns for col in ['signal', 'close']):
 df['short3_signal_1_up'] = self._calculate_short3_signal_1_up(df['signal'], df['close'])
 df['short3_signal_1_up_prob'] = self._calculate_short3_signal_1_up_probability(df['short3_signal_1_up'])

 # Feature 12: Short3 signal 4 down probability
 if all(col in df.columns for col in ['signal', 'close']):
 df['short3_signal_4_down'] = self._calculate_short3_signal_4_down(df['signal'], df['close'])
 df['short3_signal_4_down_prob'] = self._calculate_short3_signal_4_down_probability(df['short3_signal_4_down'])

 # Feature 13: Short3 direction change probability
 if all(col in df.columns for col in ['direction', 'close']):
 df['short3_direction_change'] = self._calculate_short3_direction_change(df['direction'], df['close'])
 df['short3_direction_change_prob'] = self._calculate_short3_direction_change_probability(df['short3_direction_change'])

 logger.info(f"Created {len([col for col in df.columns if 'short3' in col and 'prob' in col])} Short3 features")
 return df

 def create_all_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 Create all custom features.

 Args:
 data: Input data

 Returns:
 data with all custom features added
 """
 logger.info("Creating all custom features...")

 # Create SCHR features
 data = self.create_schr_features(data)

 # Create Wave features
 data = self.create_wave_features(data)

 # Create Short3 features
 data = self.create_short3_features(data)

 logger.info(f"Total custom features created: {len([col for col in data.columns if 'prob' in col])}")
 return data

 # Helper methods for feature Calculations

 def _calculate_trend_direction(self, close: pd.Series) -> pd.Series:
 """Calculate trend direction."""
 return np.where(close.diff() > 0, 1, np.where(close.diff() < 0, -1, 0))

 def _calculate_trend_probability(self, trend: pd.Series) -> pd.Series:
 """Calculate trend direction probability."""
 return trend.rolling(window=10).mean()

 def _calculate_yellow_breakout(self, close: pd.Series, yellow_line: pd.Series) -> pd.Series:
 """Calculate yellow line breakout."""
 return np.where(close > yellow_line, 1, 0)

 def _calculate_breakout_probability(self, breakout: pd.Series) -> pd.Series:
 """Calculate breakout probability."""
 return breakout.rolling(window=5).mean()

 def _calculate_blue_breakdown(self, close: pd.Series, blue_line: pd.Series) -> pd.Series:
 """Calculate blue line breakdown."""
 return np.where(close < blue_line, 1, 0)

 def _calculate_breakdown_probability(self, breakdown: pd.Series) -> pd.Series:
 """Calculate breakdown probability."""
 return breakdown.rolling(window=5).mean()

 def _calculate_pv_sign_probability(self, pv_sign: pd.Series) -> pd.Series:
 """Calculate PV sign probability."""
 return pv_sign.rolling(window=10).mean()

 def _calculate_wave_5_candles(self, signal: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate wave 5 candles feature."""
 result = pd.Series(0, index=signal.index)
 for i in range(5, len(signal)):
 if signal.iloc[i] == 1:
 # check if next 5 candles are up
 next_5 = close.iloc[i+1:i+6]
 if len(next_5) == 5 and all(next_5.diff() > 0):
 result.iloc[i] = 1
 return result

 def _calculate_wave_5_candles_probability(self, wave_5_candles: pd.Series) -> pd.Series:
 """Calculate wave 5 candles probability."""
 return wave_5_candles.rolling(window=10).mean()

 def _calculate_wave_5_percent(self, signal: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate wave 5% feature."""
 result = pd.Series(0, index=signal.index)
 for i in range(len(signal)):
 if signal.iloc[i] == 1:
 # check if price moves 5% in same direction
 current_price = close.iloc[i]
 future_prices = close.iloc[i+1:i+6]
 if len(future_prices) > 0:
 max_change = (future_prices.max() - current_price) / current_price
 if max_change >= 0.05:
 result.iloc[i] = 1
 return result

 def _calculate_wave_5_percent_probability(self, wave_5_percent: pd.Series) -> pd.Series:
 """Calculate wave 5% probability."""
 return wave_5_percent.rolling(window=10).mean()

 def _calculate_wave_ma_5_candles(self, condition: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate wave MA 5 candles feature."""
 result = pd.Series(0, index=condition.index)
 for i in range(5, len(condition)):
 if condition.iloc[i]:
 # check if next 5 candles are up
 next_5 = close.iloc[i+1:i+6]
 if len(next_5) == 5 and all(next_5.diff() > 0):
 result.iloc[i] = 1
 return result

 def _calculate_wave_ma_5_candles_probability(self, wave_ma_5_candles: pd.Series) -> pd.Series:
 """Calculate wave MA 5 candles probability."""
 return wave_ma_5_candles.rolling(window=10).mean()

 def _calculate_wave_ma_5_percent(self, condition: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate wave MA 5% feature."""
 result = pd.Series(0, index=condition.index)
 for i in range(len(condition)):
 if condition.iloc[i]:
 # check if price moves 5% in same direction
 current_price = close.iloc[i]
 future_prices = close.iloc[i+1:i+6]
 if len(future_prices) > 0:
 max_change = (future_prices.max() - current_price) / current_price
 if max_change >= 0.05:
 result.iloc[i] = 1
 return result

 def _calculate_wave_ma_5_percent_probability(self, wave_ma_5_percent: pd.Series) -> pd.Series:
 """Calculate wave MA 5% probability."""
 return wave_ma_5_percent.rolling(window=10).mean()

 def _calculate_wave_peak_sign(self, reverse: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate wave peak sign feature."""
 result = pd.Series(0, index=reverse.index)
 for i in range(len(reverse)):
 if reverse.iloc[i] == 1:
 # Look for next peak
 future_prices = close.iloc[i+1:i+11]
 if len(future_prices) > 0:
 peak_idx = future_prices.idxmax()
 if peak_idx in future_prices.index:
 result.iloc[i] = 1 if future_prices.loc[peak_idx] > close.iloc[i] else -1
 return result

 def _calculate_wave_peak_sign_probability(self, wave_peak_sign: pd.Series) -> pd.Series:
 """Calculate wave peak sign probability."""
 return wave_peak_sign.rolling(window=10).mean()

 def _calculate_wave_peak_timing(self, reverse: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate wave peak timing feature."""
 result = pd.Series(0, index=reverse.index)
 for i in range(len(reverse)):
 if reverse.iloc[i] == 1:
 # check if peak occurs within 10 candles
 future_prices = close.iloc[i+1:i+11]
 if len(future_prices) > 0:
 peak_idx = future_prices.idxmax()
 if peak_idx in future_prices.index:
 result.iloc[i] = 1
 return result

 def _calculate_wave_peak_timing_probability(self, wave_peak_timing: pd.Series) -> pd.Series:
 """Calculate wave peak timing probability."""
 return wave_peak_timing.rolling(window=10).mean()

 def _calculate_short3_signal_1_up(self, signal: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate Short3 signal 1 up feature."""
 result = pd.Series(0, index=signal.index)
 for i in range(len(signal)):
 if signal.iloc[i] == 1:
 # check if price moves up 5%
 current_price = close.iloc[i]
 future_prices = close.iloc[i+1:i+6]
 if len(future_prices) > 0:
 max_change = (future_prices.max() - current_price) / current_price
 if max_change >= 0.05:
 result.iloc[i] = 1
 return result

 def _calculate_short3_signal_1_up_probability(self, short3_signal_1_up: pd.Series) -> pd.Series:
 """Calculate Short3 signal 1 up probability."""
 return short3_signal_1_up.rolling(window=10).mean()

 def _calculate_short3_signal_4_down(self, signal: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate Short3 signal 4 down feature."""
 result = pd.Series(0, index=signal.index)
 for i in range(len(signal)):
 if signal.iloc[i] == 4:
 # check if price moves down 10%
 current_price = close.iloc[i]
 future_prices = close.iloc[i+1:i+6]
 if len(future_prices) > 0:
 min_change = (future_prices.min() - current_price) / current_price
 if min_change <= -0.10:
 result.iloc[i] = 1
 return result

 def _calculate_short3_signal_4_down_probability(self, short3_signal_4_down: pd.Series) -> pd.Series:
 """Calculate Short3 signal 4 down probability."""
 return short3_signal_4_down.rolling(window=10).mean()

 def _calculate_short3_direction_change(self, direction: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate Short3 direction change feature."""
 result = pd.Series(0, index=direction.index)
 for i in range(10, len(direction)):
 if direction.iloc[i] in [1, 4]:
 # check if direction changes to 2 or 3 in next 10 candles
 future_directions = direction.iloc[i+1:i+11]
 if len(future_directions) > 0 and any(future_directions.isin([2, 3])):
 result.iloc[i] = 1
 return result

 def _calculate_short3_direction_change_probability(self, short3_direction_change: pd.Series) -> pd.Series:
 """Calculate Short3 direction change probability."""
 return short3_direction_change.rolling(window=10).mean()
