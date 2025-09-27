"""
Auto Data Scanner for Trading Strategy Pipeline
Автоматический сканер данных для пайплайна торговых стратегий

Automatically scans csv_converted folder and extracts indicators, symbols, and timeframes
from filenames like "SHORT3_GBPUSD_PERIOD_H1.parquet"
"""

import os
import re
import pandas as pd
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class AutoDataScanner:
    """
    Automatically scans data directory and extracts available indicators, symbols, and timeframes.
    Автоматически сканирует директорию данных и извлекает доступные индикаторы, символы и таймфреймы.
    """
    
    def __init__(self, data_path: str = "data/cache/csv_converted/"):
        """
        Initialize Auto Data Scanner.
        
        Args:
            data_path: Path to data directory
        """
        self.data_path = Path(data_path)
        self.available_data = {}
        self.indicators = set()
        self.symbols = set()
        self.timeframes = set()
        
        # Supported timeframes in order of importance
        self.timeframe_order = ['M1', 'M5', 'M15', 'H1', 'H4', 'D1', 'W1', 'MN1']
        
    def scan_directory(self) -> Dict[str, Any]:
        """
        Scan directory for available data files.
        Сканировать директорию на наличие доступных файлов данных.
        
        Returns:
            Dictionary with scan results
        """
        logger.info(f"🔍 Scanning directory: {self.data_path}")
        
        if not self.data_path.exists():
            logger.error(f"❌ Data path does not exist: {self.data_path}")
            return {'error': f'Data path does not exist: {self.data_path}'}
        
        # Pattern to match filenames like "INDICATOR_SYMBOL_PERIOD_TIMEFRAME.parquet"
        # Supports CSVExport (SCHR Levels), WAVE2, SHORT3, and other indicators
        # Updated pattern to include CSVExport files with dots in symbols (e.g., AAPL.NAS)
        # CSVExport files have format: CSVExport_SYMBOL_PERIOD_TIMEFRAME.parquet
        # Other indicators have format: INDICATOR_SYMBOL_PERIOD_TIMEFRAME.parquet
        # We need to handle both formats
        csv_export_pattern = r'^CSVExport_([A-Z0-9.]+)_PERIOD_([A-Z0-9]+)\.parquet$'
        other_pattern = r'^([A-Z0-9_]+)_([A-Z0-9.]+)_PERIOD_([A-Z0-9]+)\.parquet$'
        
        available_files = []
        
        # Scan for parquet files
        for file_path in self.data_path.glob("*.parquet"):
            filename = file_path.name
            
            # Try CSVExport pattern first
            csv_match = re.match(csv_export_pattern, filename)
            if csv_match:
                symbol, timeframe = csv_match.groups()
                indicator = "CSVExport"  # CSVExport is the indicator name
            else:
                # Try other pattern
                other_match = re.match(other_pattern, filename)
                if other_match:
                    indicator, symbol, timeframe = other_match.groups()
                else:
                    continue  # Skip files that don't match either pattern
            
            # Get file info
            file_info = {
                'file_path': str(file_path),
                'filename': filename,
                'indicator': indicator,
                'symbol': symbol,
                'timeframe': timeframe,
                'size_mb': file_path.stat().st_size / (1024 * 1024),
                'exists': True
            }
            
            available_files.append(file_info)
            
            # Update sets
            self.indicators.add(indicator)
            self.symbols.add(symbol)
            self.timeframes.add(timeframe)
            
            logger.info(f"✅ Found: {indicator} {symbol} {timeframe} ({file_info['size_mb']:.1f} MB)")
        else:
                logger.warning(f"⚠️ Skipped file (doesn't match pattern): {filename}")
        
        # Organize data by indicator and symbol
        self.available_data = self._organize_data(available_files)
        
        scan_results = {
            'total_files': len(available_files),
            'indicators': sorted(list(self.indicators)),
            'symbols': sorted(list(self.symbols)),
            'timeframes': sorted(list(self.timeframes)),
            'available_data': self.available_data,
            'scan_successful': True
        }
        
        logger.info(f"📊 Scan completed: {len(available_files)} files, {len(self.indicators)} indicators, {len(self.symbols)} symbols")
        
        return scan_results
    
    def _organize_data(self, files: List[Dict]) -> Dict[str, Dict[str, List[Dict]]]:
        """
        Organize data by indicator and symbol.
        Организовать данные по индикаторам и символам.
        """
        organized = defaultdict(lambda: defaultdict(list))
        
        for file_info in files:
            indicator = file_info['indicator']
            symbol = file_info['symbol']
            organized[indicator][symbol].append(file_info)
        
        # Sort timeframes by importance
        for indicator in organized:
            for symbol in organized[indicator]:
                organized[indicator][symbol].sort(
                    key=lambda x: self.timeframe_order.index(x['timeframe']) 
                    if x['timeframe'] in self.timeframe_order else 999
                )
        
        return dict(organized)
    
    def get_available_combinations(self) -> Dict[str, List[str]]:
        """
        Get available indicator-symbol combinations.
        Получить доступные комбинации индикатор-символ.
        
        Returns:
            Dictionary with available combinations
        """
        combinations = {}
        
        for indicator in self.available_data:
            symbols = list(self.available_data[indicator].keys())
            combinations[indicator] = symbols
        
        return combinations
    
    def get_symbol_timeframes(self, indicator: str, symbol: str) -> List[str]:
        """
        Get available timeframes for specific indicator-symbol combination.
        Получить доступные таймфреймы для конкретной комбинации индикатор-символ.
        
        Args:
            indicator: Indicator name
            symbol: Symbol name
            
        Returns:
            List of available timeframes
        """
        if indicator not in self.available_data:
            return []
        
        if symbol not in self.available_data[indicator]:
            return []
        
        timeframes = [file_info['timeframe'] for file_info in self.available_data[indicator][symbol]]
        return sorted(timeframes, key=lambda x: self.timeframe_order.index(x) if x in self.timeframe_order else 999)
    
    def get_file_path(self, indicator: str, symbol: str, timeframe: str) -> Optional[str]:
        """
        Get file path for specific indicator-symbol-timeframe combination.
        Получить путь к файлу для конкретной комбинации индикатор-символ-таймфрейм.
        
        Args:
            indicator: Indicator name
            symbol: Symbol name
            timeframe: Timeframe
            
        Returns:
            File path if exists, None otherwise
        """
        if indicator not in self.available_data:
            return None
        
        if symbol not in self.available_data[indicator]:
            return None
        
        for file_info in self.available_data[indicator][symbol]:
            if file_info['timeframe'] == timeframe:
                return file_info['file_path']
        
        return None
    
    def get_all_timeframes_for_symbol(self, symbol: str) -> List[str]:
        """
        Get all available timeframes for a symbol across all indicators.
        Получить все доступные таймфреймы для символа по всем индикаторам.
        
        Args:
            symbol: Symbol name
            
        Returns:
            List of available timeframes
        """
        timeframes = set()
        
        for indicator in self.available_data:
            if symbol in self.available_data[indicator]:
                for file_info in self.available_data[indicator][symbol]:
                    timeframes.add(file_info['timeframe'])
        
        return sorted(timeframes, key=lambda x: self.timeframe_order.index(x) if x in self.timeframe_order else 999)
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive data summary.
        Получить комплексную сводку данных.
        
        Returns:
            Dictionary with data summary
        """
        summary = {
            'total_files': sum(
                len(files) for indicator in self.available_data 
                for files in self.available_data[indicator].values()
            ),
            'indicators': sorted(list(self.indicators)),
            'symbols': sorted(list(self.symbols)),
            'timeframes': sorted(list(self.timeframes)),
            'combinations': {}
        }
        
        # Calculate combinations
        for indicator in self.available_data:
            symbols = list(self.available_data[indicator].keys())
            summary['combinations'][indicator] = {
                'symbols': symbols,
                'count': len(symbols)
            }
        
        # Calculate total size
        total_size = 0
        for indicator in self.available_data:
            for symbol in self.available_data[indicator]:
                for file_info in self.available_data[indicator][symbol]:
                    total_size += file_info['size_mb']
        
        summary['total_size_mb'] = total_size
        summary['total_size_gb'] = total_size / 1024
        
        return summary
    
    def print_scan_results(self):
        """
        Print formatted scan results.
        Вывести отформатированные результаты сканирования.
        """
        print("\n" + "="*60)
        print("🔍 AUTO DATA SCAN RESULTS")
        print("="*60)
        
        summary = self.get_data_summary()
        
        print(f"📊 Total Files: {summary['total_files']}")
        print(f"📁 Total Size: {summary['total_size_gb']:.2f} GB")
        print(f"🎯 Indicators: {', '.join(summary['indicators'])}")
        print(f"💱 Symbols: {', '.join(summary['symbols'])}")
        print(f"⏰ Timeframes: {', '.join(summary['timeframes'])}")
        
        print(f"\n📋 Available Combinations:")
        for indicator, info in summary['combinations'].items():
            print(f"   {indicator}: {info['count']} symbols ({', '.join(info['symbols'])})")
        
        print(f"\n🕐 Timeframe Coverage:")
        for timeframe in self.timeframe_order:
            if timeframe in self.timeframes:
                count = sum(
                    1 for indicator in self.available_data
                    for symbol in self.available_data[indicator]
                    for file_info in self.available_data[indicator][symbol]
                    if file_info['timeframe'] == timeframe
                )
                print(f"   {timeframe}: {count} files")
        
        print("="*60)


class InteractiveDataSelector:
    """
    Interactive data selector for choosing indicators and symbols.
    Интерактивный селектор данных для выбора индикаторов и символов.
    """
    
    def __init__(self, scanner: AutoDataScanner):
        """
        Initialize Interactive Data Selector.
        
        Args:
            scanner: AutoDataScanner instance
        """
        self.scanner = scanner
    
    def select_indicator(self) -> str:
        """
        Interactive indicator selection.
        Интерактивный выбор индикатора.
        """
        indicators = sorted(self.scanner.indicators)
        
        if not indicators:
            print("❌ No indicators found!")
            return None
        
        print(f"\n🎯 Available Indicators:")
        for i, indicator in enumerate(indicators, 1):
            symbol_count = len(self.scanner.available_data[indicator])
            print(f"   {i}. {indicator} ({symbol_count} symbols)")
        
        while True:
            try:
                choice = input(f"\nSelect indicator (1-{len(indicators)}): ").strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(indicators):
                        selected = indicators[idx]
                        print(f"✅ Selected: {selected}")
                        return selected
                print("❌ Invalid choice. Please try again.")
            except (ValueError, KeyboardInterrupt):
                print("\n❌ Selection cancelled.")
                return None
    
    def select_symbol(self, indicator: str) -> str:
        """
        Interactive symbol selection for specific indicator.
        Интерактивный выбор символа для конкретного индикатора.
        """
        if indicator not in self.scanner.available_data:
            print(f"❌ No data found for indicator: {indicator}")
            return None
        
        symbols = sorted(self.scanner.available_data[indicator].keys())
        
        if not symbols:
            print(f"❌ No symbols found for indicator: {indicator}")
            return None
        
        print(f"\n💱 Available Symbols for {indicator}:")
        for i, symbol in enumerate(symbols, 1):
            timeframe_count = len(self.scanner.available_data[indicator][symbol])
            timeframes = [f['timeframe'] for f in self.scanner.available_data[indicator][symbol]]
            print(f"   {i}. {symbol} ({timeframe_count} timeframes: {', '.join(timeframes)})")
        
        while True:
            try:
                choice = input(f"\nSelect symbol (1-{len(symbols)}): ").strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(symbols):
                        selected = symbols[idx]
                        print(f"✅ Selected: {selected}")
                        return selected
                print("❌ Invalid choice. Please try again.")
            except (ValueError, KeyboardInterrupt):
                print("\n❌ Selection cancelled.")
                return None
    
    def select_timeframes(self, indicator: str, symbol: str, auto_select_all: bool = True) -> List[str]:
        """
        Interactive timeframe selection.
        Интерактивный выбор таймфреймов.
        
        Args:
            indicator: Selected indicator
            symbol: Selected symbol
            auto_select_all: If True, automatically select all available timeframes
            
        Returns:
            List of selected timeframes
        """
        timeframes = self.scanner.get_symbol_timeframes(indicator, symbol)
        
        if not timeframes:
            print(f"❌ No timeframes found for {indicator} {symbol}")
            return []
        
        if auto_select_all:
            print(f"✅ Auto-selected all timeframes for {indicator} {symbol}: {', '.join(timeframes)}")
            return timeframes
        
        print(f"\n⏰ Available Timeframes for {indicator} {symbol}:")
        for i, timeframe in enumerate(timeframes, 1):
            print(f"   {i}. {timeframe}")
        
        print(f"   0. All timeframes")
        
        while True:
            try:
                choice = input(f"\nSelect timeframes (0 for all, or comma-separated numbers): ").strip()
                
                if choice == "0":
                    selected = timeframes
                    print(f"✅ Selected all timeframes: {', '.join(selected)}")
                    return selected
                
                # Parse comma-separated choices
                choices = [int(x.strip()) - 1 for x in choice.split(',') if x.strip().isdigit()]
                if all(0 <= idx < len(timeframes) for idx in choices):
                    selected = [timeframes[idx] for idx in choices]
                    print(f"✅ Selected timeframes: {', '.join(selected)}")
                    return selected
                
                print("❌ Invalid choice. Please try again.")
            except (ValueError, KeyboardInterrupt):
                print("\n❌ Selection cancelled.")
                return []
    
    def interactive_selection(self) -> Dict[str, Any]:
        """
        Complete interactive selection process.
        Полный интерактивный процесс выбора.
        
        Returns:
            Dictionary with selection results
        """
        print("\n🚀 Interactive Data Selection")
        print("="*40)
        
        # Scan directory first
        scan_results = self.scanner.scan_directory()
        
        if not scan_results.get('scan_successful', False):
            print(f"❌ Scan failed: {scan_results.get('error', 'Unknown error')}")
            return {'success': False, 'error': scan_results.get('error')}
        
        # Print scan results
        self.scanner.print_scan_results()
        
        # Select indicator
        indicator = self.select_indicator()
        if not indicator:
            return {'success': False, 'error': 'No indicator selected'}
        
        # Select symbol
        symbol = self.select_symbol(indicator)
        if not symbol:
            return {'success': False, 'error': 'No symbol selected'}
        
        # Select timeframes
        timeframes = self.select_timeframes(indicator, symbol, auto_select_all=True)
        if not timeframes:
            return {'success': False, 'error': 'No timeframes selected'}
        
        # Prepare selection results
        selection = {
            'success': True,
            'indicator': indicator,
            'symbol': symbol,
            'timeframes': timeframes,
            'file_paths': {}
        }
        
        # Get file paths for all combinations
        for timeframe in timeframes:
            file_path = self.scanner.get_file_path(indicator, symbol, timeframe)
            if file_path:
                selection['file_paths'][timeframe] = file_path
            else:
                print(f"⚠️ File not found for {indicator} {symbol} {timeframe}")
        
        print(f"\n✅ Selection completed:")
        print(f"   Indicator: {indicator}")
        print(f"   Symbol: {symbol}")
        print(f"   Timeframes: {', '.join(timeframes)}")
        print(f"   Files found: {len(selection['file_paths'])}")
        
        return selection


def main():
    """
    Main function for testing auto data scanner.
    Основная функция для тестирования автоматического сканера данных.
    """
    # Initialize scanner
    scanner = AutoDataScanner()
    
    # Scan directory
    print("🔍 Scanning data directory...")
    scan_results = scanner.scan_directory()
    
    if scan_results.get('scan_successful'):
        scanner.print_scan_results()
        
        # Test interactive selection
        selector = InteractiveDataSelector(scanner)
        selection = selector.interactive_selection()
        
        if selection.get('success'):
            print(f"\n🎉 Selection successful!")
            print(f"Selected: {selection['indicator']} {selection['symbol']} {selection['timeframes']}")
        else:
            print(f"\n❌ Selection failed: {selection.get('error')}")
    else:
        print(f"❌ Scan failed: {scan_results.get('error')}")


if __name__ == "__main__":
    main()
