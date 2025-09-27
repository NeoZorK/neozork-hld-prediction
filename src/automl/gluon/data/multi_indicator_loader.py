"""
Multi-Indicator Data Loader for Trading Strategy
Загрузчик данных для множественных индикаторов торговой стратегии
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import logging
from .universal_loader import UniversalDataLoader
from .auto_data_scanner import AutoDataScanner, InteractiveDataSelector

logger = logging.getLogger(__name__)


class MultiIndicatorLoader:
    """
    Loads and combines data from multiple trading indicators (CSVExport, WAVE2, SHORT3).
    Загружает и объединяет данные из множественных торговых индикаторов.
    """
    
    def __init__(self, base_path: str = "data/cache/csv_converted/"):
        """
        Initialize Multi-Indicator Loader.
        
        Args:
            base_path: Base path to data directory
        """
        self.base_path = Path(base_path)
        self.data_loader = UniversalDataLoader()
        self.scanner = AutoDataScanner(base_path)
        self.selector = InteractiveDataSelector(self.scanner)
        
    def load_symbol_data(self, symbol: str, timeframe: str) -> Dict[str, pd.DataFrame]:
        """
        Load all indicator data for a specific symbol and timeframe.
        Загрузить все данные индикаторов для конкретного символа и таймфрейма.
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSD')
            timeframe: Timeframe (e.g., 'D1', 'H1', 'M15')
            
        Returns:
            Dictionary with loaded dataframes for each indicator
        """
        logger.info(f"Loading data for {symbol} {timeframe}...")
        
        data_sources = {}
        
        # Define file patterns for each indicator
        file_patterns = {
            'csv_export': f"CSVExport_{symbol}_PERIOD_{timeframe}.parquet",
            'wave2': f"WAVE2_{symbol}_PERIOD_{timeframe}.parquet", 
            'short3': f"SHORT3_{symbol}_PERIOD_{timeframe}.parquet"
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
                    data_sources[indicator] = pd.DataFrame()
                    
            except Exception as e:
                logger.error(f"❌ Error loading {indicator}: {e}")
                data_sources[indicator] = pd.DataFrame()
        
        return data_sources
    
    def load_multiple_symbols(self, symbols: List[str], timeframes: List[str]) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Load data for multiple symbols and timeframes.
        Загрузить данные для множественных символов и таймфреймов.
        
        Args:
            symbols: List of trading symbols
            timeframes: List of timeframes
            
        Returns:
            Nested dictionary: {symbol: {timeframe: {indicator: dataframe}}}
        """
        logger.info(f"Loading data for {len(symbols)} symbols and {len(timeframes)} timeframes...")
        
        all_data = {}
        
        for symbol in symbols:
            all_data[symbol] = {}
            
            for timeframe in timeframes:
                logger.info(f"📊 Loading {symbol} {timeframe}...")
                
                try:
                    symbol_data = self.load_symbol_data(symbol, timeframe)
                    all_data[symbol][timeframe] = symbol_data
                    
                    # Log summary
                    total_rows = sum(len(df) for df in symbol_data.values() if not df.empty)
                    indicators_loaded = sum(1 for df in symbol_data.values() if not df.empty)
                    
                    logger.info(f"✅ {symbol} {timeframe}: {total_rows} total rows, {indicators_loaded} indicators")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to load {symbol} {timeframe}: {e}")
                    all_data[symbol][timeframe] = {}
        
        return all_data
    
    def combine_indicators(self, data_sources: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Combine data from multiple indicators into a single dataframe.
        Объединить данные из множественных индикаторов в один датафрейм.
        
        Args:
            data_sources: Dictionary with indicator data
            
        Returns:
            Combined dataframe
        """
        logger.info("Combining indicator data...")
        
        if not data_sources or all(df.empty for df in data_sources.values()):
            logger.warning("No data to combine")
            return pd.DataFrame()
        
        # Start with CSVExport as base (has OHLCV data)
        if 'csv_export' in data_sources and not data_sources['csv_export'].empty:
            combined_df = data_sources['csv_export'].copy()
            logger.info(f"Base data from CSVExport: {len(combined_df)} rows")
        else:
            # Use first available indicator as base
            base_indicator = next((k for k, v in data_sources.items() if not v.empty), None)
            if base_indicator is None:
                logger.error("No data available to combine")
                return pd.DataFrame()
            
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
    
    def create_target_variable(self, data: pd.DataFrame, method: str = 'price_direction') -> pd.DataFrame:
        """
        Create target variable for machine learning.
        Создать целевую переменную для машинного обучения.
        
        Args:
            data: Input dataframe
            method: Method for creating target ('price_direction', 'price_change', 'volatility')
            
        Returns:
            Dataframe with target variable added
        """
        logger.info(f"Creating target variable using method: {method}")
        
        result_df = data.copy()
        
        if method == 'price_direction':
            # Binary classification: 1 if price goes up, 0 if down
            result_df['target'] = (result_df['Close'].diff() > 0).astype(int)
            
        elif method == 'price_change':
            # Regression: actual price change percentage
            result_df['target'] = result_df['Close'].pct_change()
            
        elif method == 'volatility':
            # Regression: rolling volatility
            result_df['target'] = result_df['Close'].rolling(20).std()
            
        else:
            raise ValueError(f"Unknown target method: {method}")
        
        # Remove rows with NaN target
        initial_rows = len(result_df)
        result_df = result_df.dropna(subset=['target'])
        removed_rows = initial_rows - len(result_df)
        
        if removed_rows > 0:
            logger.info(f"Removed {removed_rows} rows with NaN target")
        
        logger.info(f"Target variable created: {len(result_df)} rows")
        return result_df
    
    def add_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Add common technical indicators to the data.
        Добавить общие технические индикаторы к данным.
        
        Args:
            data: Input dataframe
            
        Returns:
            Dataframe with technical indicators added
        """
        logger.info("Adding technical indicators...")
        
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
        
        logger.info(f"Added {len([col for col in result_df.columns if col not in data.columns])} technical indicators")
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
    
    def get_data_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
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
                'missing_values': {},
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
            'missing_values': data.isnull().sum().to_dict(),
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
        Автоматически сканировать директорию и интерактивно выбрать данные.
        
        Args:
            interactive: Whether to use interactive selection
            
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
            logger.info("🎯 Starting interactive selection...")
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
            first_indicator = list(self.scanner.available_data.keys())[0]
            
            # Get first symbol for this indicator
            first_symbol = list(self.scanner.available_data[first_indicator].keys())[0]
            
            # Get all timeframes for this symbol
            timeframes = self.scanner.get_symbol_timeframes(first_indicator, first_symbol)
            
            selection = {
                'success': True,
                'indicator': first_indicator,
                'symbol': first_symbol,
                'timeframes': timeframes,
                'file_paths': {}
            }
            
            # Get file paths
            for timeframe in timeframes:
                file_path = self.scanner.get_file_path(first_indicator, first_symbol, timeframe)
                if file_path:
                    selection['file_paths'][timeframe] = file_path
            
            logger.info(f"✅ Auto-selected: {first_indicator} {first_symbol} {timeframes}")
            return selection
    
    def load_selected_data(self, selection: Dict[str, Any]) -> pd.DataFrame:
        """
        Load data based on selection results.
        Загрузить данные на основе результатов выбора.
        
        Args:
            selection: Selection results from auto_scan_and_select
            
        Returns:
            Combined dataframe with all selected data
        """
        if not selection.get('success', False):
            logger.error(f"❌ Cannot load data: {selection.get('error')}")
            return pd.DataFrame()
        
        indicator = selection['indicator']
        symbol = selection['symbol']
        timeframes = selection['timeframes']
        file_paths = selection.get('file_paths', {})
        
        logger.info(f"📊 Loading data for {indicator} {symbol} across {len(timeframes)} timeframes...")
        
        all_data = []
        
        for timeframe in timeframes:
            if timeframe in file_paths:
                file_path = file_paths[timeframe]
                
                try:
                    logger.info(f"📁 Loading {timeframe} from {file_path}")
                    data = self.data_loader.load_file(file_path)
                    
                    # Add metadata
                    data['indicator'] = indicator
                    data['symbol'] = symbol
                    data['timeframe'] = timeframe
                    
                    # Add timeframe weight
                    timeframe_weights = {'M1': 1, 'M5': 2, 'M15': 3, 'H1': 4, 'H4': 8, 'D1': 16, 'W1': 32, 'MN1': 64}
                    data['timeframe_weight'] = timeframe_weights.get(timeframe, 1)
                    
                    all_data.append(data)
                    logger.info(f"✅ {timeframe}: {len(data)} rows, {len(data.columns)} columns")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to load {timeframe}: {e}")
                    continue
            else:
                logger.warning(f"⚠️ No file path for {timeframe}")
        
        if not all_data:
            logger.error("❌ No data loaded successfully")
            return pd.DataFrame()
        
        # Combine all data
        logger.info("🔄 Combining all data...")
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Add technical indicators
        combined_data = self.add_technical_indicators(combined_data)
        
        logger.info(f"📊 Final combined data: {len(combined_data)} rows, {len(combined_data.columns)} columns")
        
        return combined_data
    
    def load_multi_indicator_data(self, symbol: str, timeframes: List[str]) -> pd.DataFrame:
        """
        Load data from multiple indicators (CSVExport/SCHR, WAVE2, SHORT3) for a symbol.
        Загрузить данные из множественных индикаторов для символа.
        
        Args:
            symbol: Trading symbol
            timeframes: List of timeframes
            
        Returns:
            Combined dataframe with all indicators
        """
        logger.info(f"📊 Loading multi-indicator data for {symbol} across {len(timeframes)} timeframes...")
        
        all_combined_data = []
        
        for timeframe in timeframes:
            try:
                logger.info(f"📊 Loading {symbol} {timeframe}...")
                
                # Load all indicators for this symbol/timeframe
                symbol_data = self.load_symbol_data(symbol, timeframe)
                
                # Combine indicators
                combined_symbol_data = self.combine_indicators(symbol_data)
                
                if not combined_symbol_data.empty:
                    # Add metadata
                    combined_symbol_data['symbol'] = symbol
                    combined_symbol_data['timeframe'] = timeframe
                    
                    # Add timeframe weight
                    timeframe_weights = {'M1': 1, 'M5': 2, 'M15': 3, 'H1': 4, 'H4': 8, 'D1': 16, 'W1': 32, 'MN1': 64}
                    combined_symbol_data['timeframe_weight'] = timeframe_weights.get(timeframe, 1)
                    
                    all_combined_data.append(combined_symbol_data)
                    logger.info(f"✅ {symbol} {timeframe}: {len(combined_symbol_data)} rows")
                else:
                    logger.warning(f"⚠️ No data for {symbol} {timeframe}")
                    
            except Exception as e:
                logger.error(f"❌ Failed to load {symbol} {timeframe}: {e}")
                continue
        
        if not all_combined_data:
            logger.error("❌ No data loaded successfully")
            return pd.DataFrame()
        
        # Combine all data
        logger.info("🔄 Combining all multi-indicator data...")
        final_data = pd.concat(all_combined_data, ignore_index=True)
        
        # Add technical indicators
        final_data = self.add_technical_indicators(final_data)
        
        logger.info(f"📊 Final multi-indicator data: {len(final_data)} rows, {len(final_data.columns)} columns")
        
        return final_data
    
    def auto_load_data(self, interactive: bool = True) -> pd.DataFrame:
        """
        Complete auto-loading process: scan, select, and load data.
        Полный процесс автоматической загрузки: сканирование, выбор и загрузка данных.
        
        Args:
            interactive: Whether to use interactive selection
            
        Returns:
            Combined dataframe with all selected data
        """
        logger.info("🚀 Starting auto-loading process...")
        
        # Step 1: Auto-scan and select
        selection = self.auto_scan_and_select(interactive=interactive)
        
        if not selection.get('success', False):
            logger.error(f"❌ Auto-selection failed: {selection.get('error')}")
            return pd.DataFrame()
        
        # Step 2: Load selected data
        combined_data = self.load_selected_data(selection)
        
        if combined_data.empty:
            logger.error("❌ No data loaded")
            return pd.DataFrame()
        
        logger.info("✅ Auto-loading completed successfully!")
        return combined_data
