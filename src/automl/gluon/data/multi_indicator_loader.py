"""
Multi-Indicator data Loader for trading Strategy
Загрузчик данных for множественных indicators торговой стратегии
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import logging
from .universal_loader import UniversaldataLoader
from .auto_data_scanner import AutodataScanner, InteractivedataSelector

logger = logging.getLogger(__name__)


class MultiIndicatorLoader:
 """
 Loads and combines data from multiple trading indicators (CSVExport, WAVE2, SHORT3).
 Загружает and объединяет data из множественных торговых indicators.
 """

 def __init__(self, base_path: str = "data/cache/csv_converted/"):
 """
 Initialize Multi-Indicator Loader.

 Args:
 base_path: Base path to data directory
 """
 self.base_path = Path(base_path)
 self.data_loader = UniversaldataLoader()
 self.scanner = AutodataScanner(base_path)
 self.selector = InteractivedataSelector(self.scanner)

 def load_basic_data(self, symbol: str, Timeframe: str) -> pd.dataFrame:
 """
 Load basic OHLCV data for automatic feature generation.
 Загрузить базовые OHLCV data for автоматической генерации признаков.

 Args:
 symbol: Trading symbol (e.g., 'BTCUSD')
 Timeframe: Timeframe (e.g., 'D1', 'H1', 'M15')

 Returns:
 dataFrame with basic OHLCV data
 """
 logger.info(f"Loading basic OHLCV data for {symbol} {Timeframe}...")

 # Try to load CSVExport data (contains OHLCV)
 csv_export_file = self.base_path / f"CSVExport_{symbol}_PERIOD_{Timeframe}.parquet"

 if csv_export_file.exists():
 logger.info(f"Loading CSVExport data from {csv_export_file}")
 data = self.data_loader.load_file(str(csv_export_file))

 # Ensure we have basic OHLCV columns
 required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
 if all(col in data.columns for col in required_columns):
 logger.info(f"✅ Basic OHLCV data loaded: {len(data)} rows, {len(data.columns)} columns")
 return data
 else:
 logger.warning(f"⚠️ CSVExport data Missing required OHLCV columns: {required_columns}")

 # If no CSVExport data, create synthetic data for demonstration
 logger.warning(f"⚠️ No basic data found for {symbol} {Timeframe}, Creating synthetic data...")
 return self._create_synthetic_data(symbol, Timeframe)

 def _create_synthetic_data(self, symbol: str, Timeframe: str) -> pd.dataFrame:
 """
 Create synthetic OHLCV data for demonstration.
 Создать синтетические OHLCV data for демонстрации.
 """
 import numpy as np
 from datetime import datetime, timedelta

 # Generate synthetic data
 n_periods = 1000
 dates = pd.date_range(start='2020-01-01', periods=n_periods, freq='D')

 # Generate price data with some trend and volatility
 np.random.seed(42) # For reproducibility
 base_price = 50000 if 'BTC' in symbol else 1.0
 returns = np.random.normal(0, 0.02, n_periods) # 2% daily volatility
 prices = base_price * np.exp(np.cumsum(returns))

 # Generate OHLCV data
 data = pd.dataFrame({
 'Open': prices * (1 + np.random.normal(0, 0.001, n_periods)),
 'High': prices * (1 + np.abs(np.random.normal(0, 0.01, n_periods))),
 'Low': prices * (1 - np.abs(np.random.normal(0, 0.01, n_periods))),
 'Close': prices,
 'Volume': np.random.uniform(1000, 10000, n_periods)
 })

 # Ensure High >= max(Open, Close) and Low <= min(Open, Close)
 data['High'] = np.maximum(data['High'], np.maximum(data['Open'], data['Close']))
 data['Low'] = np.minimum(data['Low'], np.minimum(data['Open'], data['Close']))

 data.index = dates

 logger.info(f"✅ Synthetic data created: {len(data)} rows")
 return data

 def load_symbol_data(self, symbol: str, Timeframe: str, indicator: str = None) -> Dict[str, pd.dataFrame]:
 """
 Load all indicator data for a specific symbol and Timeframe.
 Загрузить все data indicators for конкретного symbol and Timeframe.

 Args:
 symbol: Trading symbol (e.g., 'BTCUSD')
 Timeframe: Timeframe (e.g., 'D1', 'H1', 'M15')

 Returns:
 Dictionary with loaded dataframes for each indicator
 """
 logger.info(f"Loading data for {symbol} {Timeframe}...")

 data_sources = {}

 # Define file patterns for each indicator
 file_patterns = {
 'csv_export': f"CSVExport_{symbol}_PERIOD_{Timeframe}.parquet",
 'wave2': f"WAVE2_{symbol}_PERIOD_{Timeframe}.parquet",
 'short3': f"SHORT3_{symbol}_PERIOD_{Timeframe}.parquet"
 }

 for indicator, filename in file_patterns.items():
 file_path = self.base_path / filename

 try:
 if file_path.exists():
 logger.info(f"Loading {indicator} from {file_path}")
 data = self.data_loader.load_file(str(file_path))
 data_sources[indicator] = data
 logger.info(f"✅ {indicator}: {len(data)} rows, {len(data.columns)} columns")
 else:
 logger.warning(f"⚠️ File not found: {file_path}")
 data_sources[indicator] = pd.dataFrame()

 except Exception as e:
 logger.error(f"❌ Error Loading {indicator}: {e}")
 data_sources[indicator] = pd.dataFrame()

 return data_sources

 def load_multiple_symbols(self, symbols: List[str], Timeframes: List[str]) -> Dict[str, Dict[str, pd.dataFrame]]:
 """
 Load data for multiple symbols and Timeframes.
 Загрузить data for множественных символов and Timeframes.

 Args:
 symbols: List of Trading symbols
 Timeframes: List of Timeframes

 Returns:
 Nested dictionary: {symbol: {Timeframe: {indicator: dataframe}}}
 """
 logger.info(f"Loading data for {len(symbols)} symbols and {len(Timeframes)} Timeframes...")

 all_data = {}

 for symbol in symbols:
 all_data[symbol] = {}

 for Timeframe in timeframes:
 logger.info(f"📊 Loading {symbol} {Timeframe}...")

 try:
 symbol_data = self.load_symbol_data(symbol, Timeframe)
 all_data[symbol][Timeframe] = symbol_data

 # Log summary
 total_rows = sum(len(df) for df in symbol_data.values() if not df.empty)
 indicators_loaded = sum(1 for df in symbol_data.values() if not df.empty)

 logger.info(f"✅ {symbol} {Timeframe}: {total_rows} total rows, {indicators_loaded} indicators")

 except Exception as e:
 logger.error(f"❌ Failed to load {symbol} {Timeframe}: {e}")
 all_data[symbol][Timeframe] = {}

 return all_data

 def combine_indicators(self, data_sources: Dict[str, pd.dataFrame]) -> pd.dataFrame:
 """
 Combine data from multiple indicators into a single dataframe.
 Объединить data из множественных indicators in один датафрейм.

 Args:
 data_sources: Dictionary with indicator data

 Returns:
 Combined dataframe
 """
 logger.info("Combining indicator data...")

 if not data_sources or all(df.empty for df in data_sources.values()):
 logger.warning("No data to combine")
 return pd.dataFrame()

 # start with CSVExport as base (has OHLCV data)
 if 'csv_export' in data_sources and not data_sources['csv_export'].empty:
 combined_df = data_sources['csv_export'].copy()
 logger.info(f"Base data from CSVExport: {len(combined_df)} rows")
 else:
 # Use first available indicator as base
 base_indicator = next((k for k, v in data_sources.items() if not v.empty), None)
 if base_indicator is None:
 logger.error("No data available to combine")
 return pd.dataFrame()

 combined_df = data_sources[base_indicator].copy()
 logger.info(f"Base data from {base_indicator}: {len(combined_df)} rows")

 # Add other indicators
 for indicator, df in data_sources.items():
 if indicator == 'csv_export' or df.empty:
 continue

 logger.info(f"Adding {indicator} data...")

 # Select only indicator-specific columns (exclude OHLCV duplicates)
 indicator_columns = [col for col in df.columns
 if col not in ['Close', 'High', 'Open', 'Low', 'Volume']]

 if indicator_columns:
 indicator_df = df[indicator_columns].copy()

 # Add prefix to avoid column name conflicts
 indicator_df.columns = [f"{indicator}_{col}" for col in indicator_df.columns]

 # Merge with combined dataframe
 combined_df = combined_df.join(indicator_df, how='outer')
 logger.info(f"✅ Added {len(indicator_columns)} columns from {indicator}")
 else:
 logger.warning(f"No unique columns in {indicator}")

 logger.info(f"Combined data: {len(combined_df)} rows, {len(combined_df.columns)} columns")
 return combined_df

 def create_target_variable(self, data: pd.dataFrame, method: str = 'price_direction', problem_type: str = 'regression') -> pd.dataFrame:
 """
 Create target variable for machine learning.
 Создать целевую переменную for machine learning.

 Args:
 data: Input dataframe
 method: Method for Creating target ('price_direction', 'price_change', 'volatility')
 problem_type: Type of problem ('regression', 'binary', 'multiclass')

 Returns:
 dataframe with target variable added
 """
 logger.info(f"Creating target variable Using method: {method}, problem_type: {problem_type}")

 result_df = data.copy()

 if problem_type == 'binary':
 # Binary classification: 1 if price goes up, 0 if down
 result_df['target'] = (result_df['Close'].diff() > 0).astype(int)
 logger.info("✅ Binary classification target: 1=up, 0=down")

 elif problem_type == 'multiclass':
 # Multiclass classification: 0=down, 1=sideways, 2=up
 price_change = result_df['Close'].pct_change()
 result_df['target'] = pd.cut(price_change,
 bins=[-np.inf, -0.01, 0.01, np.inf],
 labels=[0, 1, 2]).astype(int)
 logger.info("✅ Multiclass target: 0=down, 1=sideways, 2=up")

 elif problem_type == 'regression':
 if method == 'price_change':
 # Regression: actual price change percentage
 result_df['target'] = result_df['Close'].pct_change()
 logger.info("✅ Regression target: price change percentage")
 elif method == 'volatility':
 # Regression: rolling volatility
 result_df['target'] = result_df['Close'].rolling(20).std()
 logger.info("✅ Regression target: rolling volatility")
 else:
 # Default: price change percentage
 result_df['target'] = result_df['Close'].pct_change()
 logger.info("✅ Regression target: price change percentage (default)")
 else:
 raise ValueError(f"Unknown problem type: {problem_type}")

 # Remove rows with NaN target
 initial_rows = len(result_df)
 result_df = result_df.dropna(subset=['target'])
 removed_rows = initial_rows - len(result_df)

 if removed_rows > 0:
 logger.info(f"Removed {removed_rows} rows with NaN target")

 logger.info(f"Target variable created: {len(result_df)} rows")
 return result_df

 def add_Technical_indicators(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 Add common Technical indicators to the data.
 Добавить общие Technical индикаторы к данным.

 Args:
 data: Input dataframe

 Returns:
 dataframe with Technical indicators added
 """
 logger.info("Adding Technical indicators...")

 result_df = data.copy()

 # Moving averages
 for period in [5, 10, 20, 50]:
 result_df[f'sma_{period}'] = result_df['Close'].rolling(period).mean()
 result_df[f'ema_{period}'] = result_df['Close'].ewm(span=period).mean()

 # Price-based indicators
 result_df['price_change'] = result_df['Close'].pct_change()
 result_df['high_low_ratio'] = result_df['High'] / result_df['Low']
 result_df['close_open_ratio'] = result_df['Close'] / result_df['Open']

 # Volatility indicators
 result_df['volatility_20'] = result_df['Close'].rolling(20).std()
 result_df['volatility_50'] = result_df['Close'].rolling(50).std()

 # Volume indicators
 if 'Volume' in result_df.columns:
 result_df['volume_sma_20'] = result_df['Volume'].rolling(20).mean()
 result_df['volume_ratio'] = result_df['Volume'] / result_df['volume_sma_20']

 # RSI
 result_df['rsi_14'] = self._calculate_rsi(result_df['Close'], 14)
 result_df['rsi_21'] = self._calculate_rsi(result_df['Close'], 21)

 # MACD
 macd_line, signal_line, histogram = self._calculate_macd(result_df['Close'])
 result_df['macd'] = macd_line
 result_df['macd_signal'] = signal_line
 result_df['macd_histogram'] = histogram

 logger.info(f"Added {len([col for col in result_df.columns if col not in data.columns])} Technical indicators")
 return result_df

 def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
 """Calculate RSI indicator."""
 delta = prices.diff()
 gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
 loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
 rs = gain / loss
 rsi = 100 - (100 / (1 + rs))
 return rsi

 def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
 """Calculate MACD indicator."""
 ema_fast = prices.ewm(span=fast).mean()
 ema_slow = prices.ewm(span=slow).mean()
 macd_line = ema_fast - ema_slow
 signal_line = macd_line.ewm(span=signal).mean()
 histogram = macd_line - signal_line
 return macd_line, signal_line, histogram

 def get_data_summary(self, data: pd.dataFrame) -> Dict[str, Any]:
 """
 Get comprehensive summary of the data.
 Получить комплексную сводку данных.

 Args:
 data: Input dataframe

 Returns:
 Dictionary with data summary
 """
 if data.empty:
 return {
 'rows': 0,
 'columns': 0,
 'date_range': None,
 'Missing_values': {},
 'data_types': {},
 'summary': 'No data available'
 }

 summary = {
 'rows': len(data),
 'columns': len(data.columns),
 'date_range': {
 'start': data.index.min() if hasattr(data.index, 'min') else None,
 'end': data.index.max() if hasattr(data.index, 'max') else None
 },
 'Missing_values': data.isnull().sum().to_dict(),
 'data_types': data.dtypes.to_dict(),
 'memory_usage': data.memory_usage(deep=True).sum(),
 'numeric_columns': len(data.select_dtypes(include=[np.number]).columns),
 'categorical_columns': len(data.select_dtypes(include=['object', 'category']).columns)
 }

 # Add target variable info if exists
 if 'target' in data.columns:
 target_info = data['target'].describe().to_dict()
 target_info['unique_values'] = data['target'].nunique()
 summary['target_variable'] = target_info

 return summary

 def auto_scan_and_select(self, interactive: bool = True) -> Dict[str, Any]:
 """
 Automatically scan directory and select data interactively.
 Автоматически сканировать директорию and интерактивно выбрать data.

 Args:
 interactive: Whether to Use interactive selection

 Returns:
 Dictionary with selection results
 """
 logger.info("🔍 Auto-scanning data directory...")

 # Scan directory
 scan_results = self.scanner.scan_directory()

 if not scan_results.get('scan_successful', False):
 logger.error(f"❌ Scan failed: {scan_results.get('error')}")
 return {'success': False, 'error': scan_results.get('error')}

 if interactive:
 # Interactive selection
 logger.info("🎯 starting interactive selection...")
 selection = self.selector.interactive_selection()

 if not selection.get('success', False):
 logger.error(f"❌ Selection failed: {selection.get('error')}")
 return selection

 return selection
 else:
 # Auto-select first available combination
 logger.info("🤖 Auto-selecting first available combination...")

 if not self.scanner.available_data:
 return {'success': False, 'error': 'No data available'}

 # Get first indicator
 first_indicator = List(self.scanner.available_data.keys())[0]

 # Get first symbol for this indicator
 first_symbol = List(self.scanner.available_data[first_indicator].keys())[0]

 # Get all Timeframes for this symbol
 Timeframes = self.scanner.get_symbol_Timeframes(first_indicator, first_symbol)

 selection = {
 'success': True,
 'indicator': first_indicator,
 'symbol': first_symbol,
 'Timeframes': Timeframes,
 'file_paths': {}
 }

 # Get file paths
 for Timeframe in timeframes:
 file_path = self.scanner.get_file_path(first_indicator, first_symbol, Timeframe)
 if file_path:
 selection['file_paths'][Timeframe] = file_path

 logger.info(f"✅ Auto-selected: {first_indicator} {first_symbol} {Timeframes}")
 return selection

 def load_selected_data(self, selection: Dict[str, Any]) -> pd.dataFrame:
 """
 Load data based on selection results.
 Загрузить data on basis результатов выбора.

 Args:
 selection: Selection results from auto_scan_and_select

 Returns:
 Combined dataframe with all selected data
 """
 if not selection.get('success', False):
 logger.error(f"❌ Cannot load data: {selection.get('error')}")
 return pd.dataFrame()

 indicator = selection['indicator']
 symbol = selection['symbol']
 Timeframes = selection['Timeframes']
 file_paths = selection.get('file_paths', {})

 logger.info(f"📊 Loading data for {indicator} {symbol} across {len(Timeframes)} Timeframes...")

 all_data = []

 for Timeframe in timeframes:
 if Timeframe in file_paths:
 file_path = file_paths[Timeframe]

 try:
 logger.info(f"📁 Loading {Timeframe} from {file_path}")
 data = self.data_loader.load_file(file_path)

 # Add metadata
 data['indicator'] = indicator
 data['symbol'] = symbol
 data['Timeframe'] = Timeframe

 # Add Timeframe weight
 Timeframe_weights = {'M1': 1, 'M5': 2, 'M15': 3, 'H1': 4, 'H4': 8, 'D1': 16, 'W1': 32, 'MN1': 64}
 data['Timeframe_weight'] = Timeframe_weights.get(Timeframe, 1)

 all_data.append(data)
 logger.info(f"✅ {Timeframe}: {len(data)} rows, {len(data.columns)} columns")

 except Exception as e:
 logger.error(f"❌ Failed to load {Timeframe}: {e}")
 continue
 else:
 logger.warning(f"⚠️ No file path for {Timeframe}")

 if not all_data:
 logger.error("❌ No data loaded successfully")
 return pd.dataFrame()

 # Combine all data
 logger.info("🔄 Combining all data...")
 combined_data = pd.concat(all_data, ignore_index=True)

 # Add Technical indicators
 combined_data = self.add_Technical_indicators(combined_data)

 logger.info(f"📊 Final combined data: {len(combined_data)} rows, {len(combined_data.columns)} columns")

 return combined_data

 def load_multi_indicator_data(self, symbol: str, Timeframes: List[str]) -> pd.dataFrame:
 """
 Load data from multiple indicators (CSVExport/SCHR, WAVE2, SHORT3) for a symbol.
 Загрузить data из множественных indicators for symbol.

 Args:
 symbol: Trading symbol
 Timeframes: List of Timeframes

 Returns:
 Combined dataframe with all indicators
 """
 logger.info(f"📊 Loading multi-indicator data for {symbol} across {len(Timeframes)} Timeframes...")

 all_combined_data = []

 for Timeframe in timeframes:
 try:
 logger.info(f"📊 Loading {symbol} {Timeframe}...")

 # Load all indicators for this symbol/Timeframe
 symbol_data = self.load_symbol_data(symbol, Timeframe)

 # Combine indicators
 combined_symbol_data = self.combine_indicators(symbol_data)

 if not combined_symbol_data.empty:
 # Add metadata
 combined_symbol_data['symbol'] = symbol
 combined_symbol_data['Timeframe'] = Timeframe

 # Add Timeframe weight
 Timeframe_weights = {'M1': 1, 'M5': 2, 'M15': 3, 'H1': 4, 'H4': 8, 'D1': 16, 'W1': 32, 'MN1': 64}
 combined_symbol_data['Timeframe_weight'] = Timeframe_weights.get(Timeframe, 1)

 all_combined_data.append(combined_symbol_data)
 logger.info(f"✅ {symbol} {Timeframe}: {len(combined_symbol_data)} rows")
 else:
 logger.warning(f"⚠️ No data for {symbol} {Timeframe}")

 except Exception as e:
 logger.error(f"❌ Failed to load {symbol} {Timeframe}: {e}")
 continue

 if not all_combined_data:
 logger.error("❌ No data loaded successfully")
 return pd.dataFrame()

 # Combine all data
 logger.info("🔄 Combining all multi-indicator data...")
 final_data = pd.concat(all_combined_data, ignore_index=True)

 # Add Technical indicators
 final_data = self.add_Technical_indicators(final_data)

 logger.info(f"📊 Final multi-indicator data: {len(final_data)} rows, {len(final_data.columns)} columns")

 return final_data

 def auto_load_data(self, interactive: bool = True) -> pd.dataFrame:
 """
 Complete auto-Loading process: scan, select, and load data.
 Полный process автоматической загрузки: сканирование, выбор and Loading data.

 Args:
 interactive: Whether to Use interactive selection

 Returns:
 Combined dataframe with all selected data
 """
 logger.info("🚀 starting auto-Loading process...")

 # Step 1: Auto-scan and select
 selection = self.auto_scan_and_select(interactive=interactive)

 if not selection.get('success', False):
 logger.error(f"❌ Auto-selection failed: {selection.get('error')}")
 return pd.dataFrame()

 # Step 2: Load selected data
 combined_data = self.load_selected_data(selection)

 if combined_data.empty:
 logger.error("❌ No data loaded")
 return pd.dataFrame()

 logger.info("✅ Auto-Loading COMPLETED successfully!")
 return combined_data
