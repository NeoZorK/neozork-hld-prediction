"""
Updated Custom Feature Engineer for trading Strategy Features
Обновленный инженер признаков with правильными именами columns for SCHR, WAVE2, SHORT3
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import yaml
from pathlib import Path
import logging
import time
from tqdm import tqdm

logger = logging.getLogger(__name__)


class UpdatedCustomFeatureEngineer:
 """
 Creates custom features for trading strategy based on actual column names from data files.
 Создает пользовательские признаки on basis реальных имен columns из files данных.
 """

 def __init__(self, config_path: Optional[str] = None):
 """
 Initialize Updated Custom Feature Engineer.

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
 Create SCHR Levels features (4 features) based on actual CSVExport data.
 Создать признаки SCHR уровней (4 приsign) on basis реальных данных CSVExport.

 CSVExport columns: ['Close', 'High', 'Open', 'Low', 'Volume', 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
 """
 logger.info("Creating SCHR features from CSVExport data...")
 df = data.copy()

 # Progress bar for SCHR features
 with tqdm(total=4, desc="🔧 SCHR Features", unit="feature",
 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
 position=0, leave=True) as pbar:

 # Feature 1: Trend Direction Probability
 # Вероятность направления тренда on basis pressure and pressure_vector
 if 'pressure' in df.columns and 'pressure_vector' in df.columns:
 pbar.set_description("🔧 SCHR: Trend direction")
 df['trend_direction_probability'] = self._calculate_trend_direction_probability(
 df['pressure'], df['pressure_vector']
 )
 pbar.update(1)

 # Feature 2: Yellow Line Breakout Probability
 # Вероятность breakthrough желтой линии (predicted_high) вверх
 if 'predicted_high' in df.columns and 'Close' in df.columns:
 pbar.set_description("🔧 SCHR: Yellow line breakout")
 df['yellow_line_breakout_probability'] = self._calculate_yellow_breakout_probability(
 df['Close'], df['predicted_high']
 )
 pbar.update(1)

 # Feature 3: Blue Line Breakdown Probability
 # Вероятность breakthrough синей линии (predicted_low) вниз
 if 'predicted_low' in df.columns and 'Close' in df.columns:
 pbar.set_description("🔧 SCHR: Blue line breakdown")
 df['blue_line_breakdown_probability'] = self._calculate_blue_breakdown_probability(
 df['Close'], df['predicted_low']
 )
 pbar.update(1)

 # Feature 4: Pressure Vector sign Probability
 # Вероятность sign Pressure Vector
 if 'pressure_vector' in df.columns:
 pbar.set_description("🔧 SCHR: Pressure vector")
 df['pv_sign_probability'] = self._calculate_pv_sign_probability(df['pressure_vector'])
 pbar.update(1)

 logger.info(f"Created {len([col for col in df.columns if 'probability' in col])} SCHR features")
 return df

 def create_wave2_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 Create WAVE2 features (6 features) based on actual WAVE2 data.
 Создать признаки WAVE2 (6 признаков) on basis реальных данных WAVE2.

 WAVE2 columns: ['Close', 'High', 'Open', 'Low', 'Volume', 'wave', 'fast_line', 'ma_line', 'direction', 'signal']
 """
 logger.info("Creating WAVE2 features from WAVE2 data...")
 df = data.copy()

 # Progress bar for WAVE2 features
 with tqdm(total=6, desc="🌊 WAVE2 Features", unit="feature",
 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
 position=1, leave=True) as pbar:

 # Feature 5: Wave signal Up 5 Candles Probability
 # Если signal=1, вероятность движения вверх 5 свечей
 if 'signal' in df.columns and 'Close' in df.columns:
 pbar.set_description("🌊 WAVE2: signal up 5 candles")
 df['wave_signal_up_5_candles_probability'] = self._calculate_wave_signal_up_5_candles(
 df['signal'], df['Close']
 )
 pbar.update(1)

 # Feature 6: Wave signal Continue 5% Probability
 # Вероятность продолжения движения on 5%
 if 'signal' in df.columns and 'Close' in df.columns:
 pbar.set_description("🌊 WAVE2: signal continue 5%")
 df['wave_signal_continue_5_percent_probability'] = self._calculate_wave_continue_5_percent(
 df['signal'], df['Close']
 )
 pbar.update(1)

 # Feature 7: Wave signal MA Below Open Up 5 Candles Probability
 # При MA < Open, вероятность движения вверх 5 свечей
 if all(col in df.columns for col in ['signal', 'ma_line', 'Open', 'Close']):
 pbar.set_description("🌊 WAVE2: MA below open up 5 candles")
 condition = (df['signal'] == 1) & (df['ma_line'] < df['Open'])
 df['wave_signal_ma_below_open_up_5_candles_probability'] = self._calculate_wave_ma_condition_up_5_candles(
 condition, df['Close']
 )
 pbar.update(1)

 # Feature 8: Wave signal MA Below Open Continue 5% Probability
 # При MA < Open, вероятность продолжения on 5%
 if all(col in df.columns for col in ['signal', 'ma_line', 'Open', 'Close']):
 pbar.set_description("🌊 WAVE2: MA below open continue 5%")
 condition = (df['signal'] == 1) & (df['ma_line'] < df['Open'])
 df['wave_signal_ma_below_open_continue_5_percent_probability'] = self._calculate_wave_ma_condition_continue_5_percent(
 condition, df['Close']
 )
 pbar.update(1)

 # Feature 9: Wave Reverse Peak sign Probability
 # Вероятность sign следующего пика разворота
 if 'direction' in df.columns and 'Close' in df.columns:
 pbar.set_description("🌊 WAVE2: Reverse peak sign")
 df['wave_reverse_peak_sign_probability'] = self._calculate_wave_reverse_peak_sign(
 df['direction'], df['Close']
 )
 pbar.update(1)

 # Feature 10: Wave Reverse Peak 10 Candles Probability
 # Вероятность пика разворота in течение 10 свечей
 if 'direction' in df.columns and 'Close' in df.columns:
 pbar.set_description("🌊 WAVE2: Reverse peak 10 candles")
 df['wave_reverse_peak_10_candles_probability'] = self._calculate_wave_reverse_peak_10_candles(
 df['direction'], df['Close']
 )
 pbar.update(1)

 logger.info(f"Created {len([col for col in df.columns if 'wave' in col and 'probability' in col])} WAVE2 features")
 return df

 def create_short3_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 Create SHORT3 features (3 features) based on actual SHORT3 data.
 Создать признаки SHORT3 (3 приsign) on basis реальных данных SHORT3.

 SHORT3 columns: ['Close', 'High', 'Open', 'Low', 'Volume', 'short_trend', 'r_trend', 'global', 'direction', 'r_direction', 'signal', 'r_signal', 'g_direction', 'g_signal']
 """
 logger.info("Creating SHORT3 features from SHORT3 data...")
 df = data.copy()

 # Progress bar for SHORT3 features
 with tqdm(total=3, desc="⚡ SHORT3 Features", unit="feature",
 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
 position=2, leave=True) as pbar:

 # Feature 11: Short3 signal 1 Up 5% Probability
 # Если signal=1, вероятность роста on 5%
 if 'signal' in df.columns and 'Close' in df.columns:
 pbar.set_description("⚡ SHORT3: signal 1 up 5%")
 df['short3_signal_1_up_5_percent_probability'] = self._calculate_short3_signal_1_up_5_percent(
 df['signal'], df['Close']
 )
 pbar.update(1)

 # Feature 12: Short3 signal 4 Down 10% Probability
 # Если signal=4, вероятность падения on 10%
 if 'signal' in df.columns and 'Close' in df.columns:
 pbar.set_description("⚡ SHORT3: signal 4 down 10%")
 df['short3_signal_4_down_10_percent_probability'] = self._calculate_short3_signal_4_down_10_percent(
 df['signal'], df['Close']
 )
 pbar.update(1)

 # Feature 13: Short3 Direction Change 10 Candles Probability
 # Вероятность смены направления in течение 10 свечей
 if 'direction' in df.columns and 'Close' in df.columns:
 pbar.set_description("⚡ SHORT3: Direction change 10 candles")
 df['short3_direction_change_10_candles_probability'] = self._calculate_short3_direction_change_10_candles(
 df['direction'], df['Close']
 )
 pbar.update(1)

 logger.info(f"Created {len([col for col in df.columns if 'short3' in col and 'probability' in col])} SHORT3 features")
 return df

 def create_all_features(self, csv_export_data: pd.dataFrame, wave2_data: pd.dataFrame, short3_data: pd.dataFrame) -> pd.dataFrame:
 """
 Create all 13 custom features by combining all three data sources.
 Создать все 13 пользовательских признаков, объединив все три источника данных.
 """
 logger.info("Creating all 13 custom features from combined data sources...")

 # Overall progress bar for all features
 with tqdm(total=3, desc="🎯 all Features", unit="indicator",
 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
 position=3, leave=True) as main_pbar:

 # start with CSVExport data as base
 result_df = csv_export_data.copy()

 # Add SCHR features
 main_pbar.set_description("🎯 all Features: SCHR")
 result_df = self.create_schr_features(result_df)
 main_pbar.update(1)

 # Merge WAVE2 data and add features
 if not wave2_data.empty:
 main_pbar.set_description("🎯 all Features: WAVE2")
 # Merge on timestamp/index
 wave2_features = self.create_wave2_features(wave2_data)
 result_df = self._merge_dataframes(result_df, wave2_features)
 main_pbar.update(1)

 # Merge SHORT3 data and add features
 if not short3_data.empty:
 main_pbar.set_description("🎯 all Features: SHORT3")
 short3_features = self.create_short3_features(short3_data)
 result_df = self._merge_dataframes(result_df, short3_features)
 main_pbar.update(1)

 logger.info(f"Created total of {len([col for col in result_df.columns if 'probability' in col])} custom features")
 return result_df

 def _merge_dataframes(self, df1: pd.dataFrame, df2: pd.dataFrame) -> pd.dataFrame:
 """Merge two dataframes on their index (timestamp)."""
 if df1.index.equals(df2.index):
 # Same index, can merge directly
 return df1.join(df2, rsuffix='_2')
 else:
 # Different indices, need to align
 return df1.join(df2, how='outer', rsuffix='_2')

 # Helper methods for SCHR features
 def _calculate_trend_direction_probability(self, pressure: pd.Series, pressure_vector: pd.Series) -> pd.Series:
 """Calculate trend direction probability based on pressure indicators."""
 # Normalize pressure values
 pressure_norm = (pressure - pressure.mean()) / pressure.std()
 pv_norm = (pressure_vector - pressure_vector.mean()) / pressure_vector.std()

 # Combine indicators for trend strength
 trend_strength = (pressure_norm + pv_norm) / 2

 # Convert to probability (0-1)
 return 1 / (1 + np.exp(-trend_strength))

 def _calculate_yellow_breakout_probability(self, close: pd.Series, predicted_high: pd.Series) -> pd.Series:
 """Calculate probability of breaking yellow line (predicted_high) upwards."""
 # Calculate distance to predicted high
 distance_to_high = (predicted_high - close) / close

 # Convert to probability
 return 1 / (1 + np.exp(-distance_to_high * 10))

 def _calculate_blue_breakdown_probability(self, close: pd.Series, predicted_low: pd.Series) -> pd.Series:
 """Calculate probability of breaking blue line (predicted_low) downwards."""
 # Calculate distance to predicted low
 distance_to_low = (close - predicted_low) / close

 # Convert to probability
 return 1 / (1 + np.exp(-distance_to_low * 10))

 def _calculate_pv_sign_probability(self, pressure_vector: pd.Series) -> pd.Series:
 """Calculate probability of pressure vector sign."""
 # Normalize pressure vector
 pv_norm = (pressure_vector - pressure_vector.mean()) / pressure_vector.std()

 # Convert to probability
 return 1 / (1 + np.exp(-pv_norm))

 # Helper methods for WAVE2 features
 def _calculate_wave_signal_up_5_candles(self, signal: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate probability of 5 candles up when signal=1."""
 result = pd.Series(0.0, index=signal.index)

 for i in range(5, len(signal)):
 if signal.iloc[i-1] == 1: # signal was 1
 # check if next 5 candles were up
 future_returns = close.iloc[i:i+5].pct_change().dropna()
 if len(future_returns) == 4: # 4 returns for 5 candles
 up_probability = (future_returns > 0).mean()
 result.iloc[i] = up_probability

 return result

 def _calculate_wave_continue_5_percent(self, signal: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate probability of 5% continuation when signal=1."""
 result = pd.Series(0.0, index=signal.index)

 for i in range(1, len(signal)):
 if signal.iloc[i-1] == 1: # signal was 1
 # check if price moved 5% in next period
 future_return = close.iloc[i] / close.iloc[i-1] - 1
 result.iloc[i] = 1 if abs(future_return) >= 0.05 else 0

 return result

 def _calculate_wave_ma_condition_up_5_candles(self, condition: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate probability of 5 candles up when MA condition is met."""
 result = pd.Series(0.0, index=condition.index)

 for i in range(5, len(condition)):
 if condition.iloc[i-1]: # MA condition was met
 future_returns = close.iloc[i:i+5].pct_change().dropna()
 if len(future_returns) == 4:
 up_probability = (future_returns > 0).mean()
 result.iloc[i] = up_probability

 return result

 def _calculate_wave_ma_condition_continue_5_percent(self, condition: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate probability of 5% continuation when MA condition is met."""
 result = pd.Series(0.0, index=condition.index)

 for i in range(1, len(condition)):
 if condition.iloc[i-1]: # MA condition was met
 future_return = close.iloc[i] / close.iloc[i-1] - 1
 result.iloc[i] = 1 if abs(future_return) >= 0.05 else 0

 return result

 def _calculate_wave_reverse_peak_sign(self, direction: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate probability of reverse peak sign."""
 # Look for direction changes
 direction_changes = direction.diff() != 0

 # Calculate probability based on price movement at direction changes
 result = pd.Series(0.0, index=direction.index)
 for i in range(1, len(direction)):
 if direction_changes.iloc[i]:
 # check price movement around direction change
 price_change = close.iloc[i] / close.iloc[i-1] - 1
 result.iloc[i] = 1 / (1 + np.exp(-price_change * 10))

 return result

 def _calculate_wave_reverse_peak_10_candles(self, direction: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate probability of reverse peak within 10 candles."""
 result = pd.Series(0.0, index=direction.index)

 for i in range(10, len(direction)):
 # Look for direction changes in next 10 candles
 future_direction = direction.iloc[i:i+10]
 direction_changes = future_direction.diff() != 0

 if direction_changes.any():
 # Calculate probability based on number of changes
 change_count = direction_changes.sum()
 result.iloc[i] = min(1.0, change_count / 10)

 return result

 # Helper methods for SHORT3 features
 def _calculate_short3_signal_1_up_5_percent(self, signal: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate probability of 5% up when signal=1."""
 result = pd.Series(0.0, index=signal.index)

 for i in range(1, len(signal)):
 if signal.iloc[i-1] == 1: # signal was 1
 future_return = close.iloc[i] / close.iloc[i-1] - 1
 result.iloc[i] = 1 if future_return >= 0.05 else 0

 return result

 def _calculate_short3_signal_4_down_10_percent(self, signal: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate probability of 10% down when signal=4."""
 result = pd.Series(0.0, index=signal.index)

 for i in range(1, len(signal)):
 if signal.iloc[i-1] == 4: # signal was 4
 future_return = close.iloc[i] / close.iloc[i-1] - 1
 result.iloc[i] = 1 if future_return <= -0.10 else 0

 return result

 def _calculate_short3_direction_change_10_candles(self, direction: pd.Series, close: pd.Series) -> pd.Series:
 """Calculate probability of direction change within 10 candles."""
 result = pd.Series(0.0, index=direction.index)

 for i in range(10, len(direction)):
 # Look for direction changes in next 10 candles
 future_direction = direction.iloc[i:i+10]
 direction_changes = future_direction.diff() != 0

 if direction_changes.any():
 change_count = direction_changes.sum()
 result.iloc[i] = min(1.0, change_count / 10)

 return result
