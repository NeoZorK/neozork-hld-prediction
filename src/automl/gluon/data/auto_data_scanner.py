"""
Auto data Scanner for trading Strategy Pipeline
Автоматический сканер данных for пайплайна торговых стратегий

Automatically scans csv_converted folder and extracts indicators, symbols, and Timeframes
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


class AutodataScanner:
 """
 Automatically scans data directory and extracts available indicators, symbols, and Timeframes.
 Автоматически сканирует директорию данных and извлекает доступные индикаторы, символы and Timeframeы.
 """

 def __init__(self, data_path: str = "data/cache/csv_converted/"):
 """
 Initialize Auto data Scanner.

 Args:
 data_path: Path to data directory
 """
 self.data_path = Path(data_path)
 self.available_data = {}
 self.indicators = set()
 self.symbols = set()
 self.Timeframes = set()

 # Supported Timeframes in order of importance
 self.Timeframe_order = ['M1', 'M5', 'M15', 'H1', 'H4', 'D1', 'W1', 'MN1']

 def scan_directory(self) -> Dict[str, Any]:
 """
 Scan directory for available data files.
 Сканировать директорию on presence доступных файлов данных.

 Returns:
 Dictionary with scan results
 """
 logger.info(f"🔍 Scanning directory: {self.data_path}")

 if not self.data_path.exists():
 logger.error(f"❌ data path does not exist: {self.data_path}")
 return {'error': f'data path does not exist: {self.data_path}'}

 # Pattern to match filenames like "INDICATOR_symbol_PERIOD_Timeframe.parquet"
 # Supports CSVExport (SCHR Levels), WAVE2, SHORT3, and other indicators
 # Updated pattern to include CSVExport files with dots in symbols (e.g., AAPL.NAS)
 # CSVExport files have format: CSVExport_symbol_PERIOD_Timeframe.parquet
 # Other indicators have format: INDICATOR_symbol_PERIOD_Timeframe.parquet
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
 symbol, Timeframe = csv_match.groups()
 indicator = "CSVExport" # CSVExport is the indicator name
 else:
 # Try other pattern
 other_match = re.match(other_pattern, filename)
 if other_match:
 indicator, symbol, Timeframe = other_match.groups()
 else:
 continue # Skip files that don't match either pattern

 # Get file info
 file_info = {
 'file_path': str(file_path),
 'filename': filename,
 'indicator': indicator,
 'symbol': symbol,
 'Timeframe': Timeframe,
 'size_mb': file_path.stat().st_size / (1024 * 1024),
 'exists': True
 }

 available_files.append(file_info)

 # Update sets
 self.indicators.add(indicator)
 self.symbols.add(symbol)
 self.Timeframes.add(Timeframe)

 logger.info(f"✅ found: {indicator} {symbol} {Timeframe} ({file_info['size_mb']:.1f} MB)")
 else:
 logger.warning(f"⚠️ Skipped file (doesn't match pattern): {filename}")

 # Organize data by indicator and symbol
 self.available_data = self._organize_data(available_files)

 scan_results = {
 'total_files': len(available_files),
 'indicators': sorted(List(self.indicators)),
 'symbols': sorted(List(self.symbols)),
 'Timeframes': sorted(List(self.Timeframes)),
 'available_data': self.available_data,
 'scan_successful': True
 }

 logger.info(f"📊 Scan COMPLETED: {len(available_files)} files, {len(self.indicators)} indicators, {len(self.symbols)} symbols")

 return scan_results

 def _organize_data(self, files: List[Dict]) -> Dict[str, Dict[str, List[Dict]]]:
 """
 Organize data by indicator and symbol.
 Организовать data on индикаторам and symbolм.
 """
 organized = defaultdict(lambda: defaultdict(List))

 for file_info in files:
 indicator = file_info['indicator']
 symbol = file_info['symbol']
 organized[indicator][symbol].append(file_info)

 # Sort Timeframes by importance
 for indicator in organized:
 for symbol in organized[indicator]:
 organized[indicator][symbol].sort(
 key=lambda x: self.Timeframe_order.index(x['Timeframe'])
 if x['Timeframe'] in self.Timeframe_order else 999
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
 symbols = List(self.available_data[indicator].keys())
 combinations[indicator] = symbols

 return combinations

 def get_symbol_Timeframes(self, indicator: str, symbol: str) -> List[str]:
 """
 Get available Timeframes for specific indicator-symbol combination.
 Получить доступные Timeframeы for конкретной комбинации индикатор-символ.

 Args:
 indicator: Indicator name
 symbol: symbol name

 Returns:
 List of available Timeframes
 """
 if indicator not in self.available_data:
 return []

 if symbol not in self.available_data[indicator]:
 return []

 Timeframes = [file_info['Timeframe'] for file_info in self.available_data[indicator][symbol]]
 return sorted(Timeframes, key=lambda x: self.Timeframe_order.index(x) if x in self.Timeframe_order else 999)

 def get_file_path(self, indicator: str, symbol: str, Timeframe: str) -> Optional[str]:
 """
 Get file path for specific indicator-symbol-Timeframe combination.
 Получить путь к файлу for конкретной комбинации индикатор-символ-Timeframe.

 Args:
 indicator: Indicator name
 symbol: symbol name
 Timeframe: Timeframe

 Returns:
 File path if exists, None otherwise
 """
 if indicator not in self.available_data:
 return None

 if symbol not in self.available_data[indicator]:
 return None

 for file_info in self.available_data[indicator][symbol]:
 if file_info['Timeframe'] == Timeframe:
 return file_info['file_path']

 return None

 def get_all_Timeframes_for_symbol(self, symbol: str) -> List[str]:
 """
 Get all available Timeframes for a symbol across all indicators.
 Получить все доступные Timeframeы for symbol on all индикаторам.

 Args:
 symbol: symbol name

 Returns:
 List of available Timeframes
 """
 Timeframes = set()

 for indicator in self.available_data:
 if symbol in self.available_data[indicator]:
 for file_info in self.available_data[indicator][symbol]:
 Timeframes.add(file_info['Timeframe'])

 return sorted(Timeframes, key=lambda x: self.Timeframe_order.index(x) if x in self.Timeframe_order else 999)

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
 'indicators': sorted(List(self.indicators)),
 'symbols': sorted(List(self.symbols)),
 'Timeframes': sorted(List(self.Timeframes)),
 'combinations': {}
 }

 # Calculate combinations
 for indicator in self.available_data:
 symbols = List(self.available_data[indicator].keys())
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
 print("🔍 AUTO data SCAN RESULTS")
 print("="*60)

 summary = self.get_data_summary()

 print(f"📊 Total Files: {summary['total_files']}")
 print(f"📁 Total Size: {summary['total_size_gb']:.2f} GB")
 print(f"🎯 Indicators: {', '.join(summary['indicators'])}")
 print(f"💱 symbols: {', '.join(summary['symbols'])}")
 print(f"⏰ Timeframes: {', '.join(summary['Timeframes'])}")

 print(f"\n📋 available Combinations:")
 for indicator, info in summary['combinations'].items():
 print(f" {indicator}: {info['count']} symbols ({', '.join(info['symbols'])})")

 print(f"\n🕐 Timeframe coverage:")
 for Timeframe in self.Timeframe_order:
 if Timeframe in self.Timeframes:
 count = sum(
 1 for indicator in self.available_data
 for symbol in self.available_data[indicator]
 for file_info in self.available_data[indicator][symbol]
 if file_info['Timeframe'] == Timeframe
 )
 print(f" {Timeframe}: {count} files")

 print("="*60)


class InteractivedataSelector:
 """
 Interactive data selector for choosing indicators and symbols.
 Интерактивный селектор данных for выбора indicators and символов.
 """

 def __init__(self, scanner: AutodataScanner):
 """
 Initialize Interactive data Selector.

 Args:
 scanner: AutodataScanner instance
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

 print(f"\n🎯 available Indicators:")
 for i, indicator in enumerate(indicators, 1):
 symbol_count = len(self.scanner.available_data[indicator])
 print(f" {i}. {indicator} ({symbol_count} symbols)")

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
 Интерактивный выбор symbol for конкретного индикатора.
 """
 if indicator not in self.scanner.available_data:
 print(f"❌ No data found for indicator: {indicator}")
 return None

 symbols = sorted(self.scanner.available_data[indicator].keys())

 if not symbols:
 print(f"❌ No symbols found for indicator: {indicator}")
 return None

 print(f"\n💱 available symbols for {indicator}:")
 for i, symbol in enumerate(symbols, 1):
 Timeframe_count = len(self.scanner.available_data[indicator][symbol])
 Timeframes = [f['Timeframe'] for f in self.scanner.available_data[indicator][symbol]]
 print(f" {i}. {symbol} ({Timeframe_count} Timeframes: {', '.join(Timeframes)})")

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

 def select_Timeframes(self, indicator: str, symbol: str, auto_select_all: bool = True) -> List[str]:
 """
 Interactive Timeframe selection.
 Интерактивный выбор Timeframes.

 Args:
 indicator: Selected indicator
 symbol: Selected symbol
 auto_select_all: If True, automatically select all available Timeframes

 Returns:
 List of selected Timeframes
 """
 Timeframes = self.scanner.get_symbol_Timeframes(indicator, symbol)

 if not Timeframes:
 print(f"❌ No Timeframes found for {indicator} {symbol}")
 return []

 if auto_select_all:
 print(f"✅ Auto-selected all Timeframes for {indicator} {symbol}: {', '.join(Timeframes)}")
 return Timeframes

 print(f"\n⏰ available Timeframes for {indicator} {symbol}:")
 for i, Timeframe in enumerate(Timeframes, 1):
 print(f" {i}. {Timeframe}")

 print(f" 0. all Timeframes")

 while True:
 try:
 choice = input(f"\nSelect Timeframes (0 for all, or comma-separated numbers): ").strip()

 if choice == "0":
 selected = Timeframes
 print(f"✅ Selected all Timeframes: {', '.join(selected)}")
 return selected

 # Parse comma-separated choices
 choices = [int(x.strip()) - 1 for x in choice.split(',') if x.strip().isdigit()]
 if all(0 <= idx < len(Timeframes) for idx in choices):
 selected = [Timeframes[idx] for idx in choices]
 print(f"✅ Selected Timeframes: {', '.join(selected)}")
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
 print("\n🚀 Interactive data Selection")
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

 # Select Timeframes
 Timeframes = self.select_Timeframes(indicator, symbol, auto_select_all=True)
 if not Timeframes:
 return {'success': False, 'error': 'No Timeframes selected'}

 # Prepare selection results
 selection = {
 'success': True,
 'indicator': indicator,
 'symbol': symbol,
 'Timeframes': Timeframes,
 'file_paths': {}
 }

 # Get file paths for all combinations
 for Timeframe in Timeframes:
 file_path = self.scanner.get_file_path(indicator, symbol, Timeframe)
 if file_path:
 selection['file_paths'][Timeframe] = file_path
 else:
 print(f"⚠️ File not found for {indicator} {symbol} {Timeframe}")

 print(f"\n✅ Selection COMPLETED:")
 print(f" Indicator: {indicator}")
 print(f" symbol: {symbol}")
 print(f" Timeframes: {', '.join(Timeframes)}")
 print(f" Files found: {len(selection['file_paths'])}")

 return selection


def main():
 """
 main function for testing auto data scanner.
 Основная function for тестирования автоматического сканера данных.
 """
 # Initialize scanner
 scanner = AutodataScanner()

 # Scan directory
 print("🔍 Scanning data directory...")
 scan_results = scanner.scan_directory()

 if scan_results.get('scan_successful'):
 scanner.print_scan_results()

 # Test interactive selection
 selector = InteractivedataSelector(scanner)
 selection = selector.interactive_selection()

 if selection.get('success'):
 print(f"\n🎉 Selection successful!")
 print(f"Selected: {selection['indicator']} {selection['symbol']} {selection['Timeframes']}")
 else:
 print(f"\n❌ Selection failed: {selection.get('error')}")
 else:
 print(f"❌ Scan failed: {scan_results.get('error')}")


if __name__ == "__main__":
 main()
