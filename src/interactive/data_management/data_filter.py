# -*- coding: utf-8 -*-
"""
Data Filter for NeoZork Interactive ML Trading Strategy Development.

This module provides interactive filtering capabilities for data loading
with support for format, source, symbol, and indicator filtering.
"""

from typing import Dict, Any, Optional, List, Tuple
import re
from pathlib import Path
from colorama import Fore, Back, Style


class DataFilter:
    """
    Interactive data filter for data loading configuration.
    
    Features:
    - Filter by format (parquet, json, csv)
    - Filter by source (binance, csvexport, polygon, yfinance)
    - Filter by symbol (BTCUSDT, EURUSD, BTCUSD, etc.)
    - Filter by indicator name (wave, rsi_mom, macd, etc.)
    - Interactive search and selection
    - Real-time filtering results
    """
    
    def __init__(self):
        """Initialize the data filter."""
        self.available_formats = ['parquet', 'json', 'csv']
        self.available_sources = ['binance', 'csvexport', 'polygon', 'yfinance']
        self.available_symbols = []
        self.available_indicators = []
        self.filtered_files = []
        
    def set_available_data(self, files_info: Dict[str, Any]) -> None:
        """
        Set available data from files analysis.
        
        Args:
            files_info: Dictionary containing file information from analysis
        """
        self.available_symbols = []
        self.available_indicators = []
        
        for filename, file_info in files_info.items():
            # Extract symbol
            symbol = self._extract_symbol_from_filename(filename)
            if symbol and symbol not in self.available_symbols:
                self.available_symbols.append(symbol)
            
            # Extract indicator
            indicator = file_info.get('indicator', 'unknown')
            if indicator and indicator not in self.available_indicators:
                self.available_indicators.append(indicator)
        
        # Sort lists for better UX
        self.available_symbols.sort()
        self.available_indicators.sort()
    
    def _extract_symbol_from_filename(self, filename: str) -> Optional[str]:
        """
        Extract symbol from filename.
        
        Args:
            filename: Name of the file
            
        Returns:
            Extracted symbol or None
        """
        try:
            # Common patterns for symbol extraction - more specific patterns
            patterns = [
                r'^([A-Z]{3,6}USD[A-Z]?)',  # BTCUSDT, EURUSD, etc. at start
                r'^([A-Z]{3,6}_[A-Z]{3,6})',  # BTC_USDT, EUR_USD, etc. at start
                r'([A-Z]{3,6}USD[A-Z]?)_',  # BTCUSDT_, EURUSD_ in middle
                r'([A-Z]{3,6}_[A-Z]{3,6})_',  # BTC_USDT_, EUR_USD_ in middle
            ]
            
            for pattern in patterns:
                match = re.search(pattern, filename.upper())
                if match:
                    symbol = match.group(1).replace('_', '')
                    # Validate that the symbol looks like a trading pair
                    if len(symbol) >= 6 and symbol.isalpha() and 'USD' in symbol:
                        return symbol
            
            return None
            
        except Exception:
            return None
    
    def filter_files(self, files_info: Dict[str, Any], 
                    format_filter: Optional[str] = None,
                    source_filter: Optional[str] = None,
                    symbol_filter: Optional[str] = None,
                    indicator_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Filter files based on provided criteria.
        
        Args:
            files_info: Dictionary containing file information
            format_filter: Filter by format (parquet, json, csv)
            source_filter: Filter by source (binance, csvexport, etc.)
            symbol_filter: Filter by symbol (BTCUSDT, EURUSD, etc.)
            indicator_filter: Filter by indicator (wave, rsi_mom, etc.)
            
        Returns:
            List of filtered file information
        """
        try:
            # Validate inputs
            if not files_info:
                print(f"{Fore.YELLOW}⚠️  No files information provided")
                return []
            
            # Validate filters
            if format_filter and format_filter.lower() not in ['parquet', 'json', 'csv']:
                print(f"{Fore.YELLOW}⚠️  Invalid format filter: {format_filter}")
                format_filter = None
            
            if source_filter and source_filter.lower() not in ['binance', 'csvexport', 'polygon', 'yfinance']:
                print(f"{Fore.YELLOW}⚠️  Invalid source filter: {source_filter}")
                source_filter = None
            
            filtered_files = []
            
            for filename, file_info in files_info.items():
                try:
                    # Apply format filter
                    if format_filter:
                        file_format = file_info.get('format', '').replace('.', '').lower()
                        if file_format != format_filter.lower():
                            continue
                    
                    # Apply source filter
                    if source_filter:
                        file_source = file_info.get('source', '').lower()
                        if source_filter.lower() not in file_source:
                            continue
                    
                    # Apply symbol filter
                    if symbol_filter:
                        file_symbol = self._extract_symbol_from_filename(filename)
                        if not file_symbol or symbol_filter.upper() not in file_symbol.upper():
                            continue
                    
                    # Apply indicator filter
                    if indicator_filter:
                        file_indicator = file_info.get('indicator', '').lower()
                        if indicator_filter.lower() not in file_indicator:
                            continue
                    
                    # File passes all filters
                    filtered_files.append({
                        'filename': filename,
                        'file_info': file_info,
                        'symbol': self._extract_symbol_from_filename(filename),
                        'source': file_info.get('source', 'unknown'),
                        'format': file_info.get('format', '').replace('.', '').lower(),
                        'indicator': file_info.get('indicator', 'unknown')
                    })
                    
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠️  Error processing file {filename}: {e}")
                    continue
            
            return filtered_files
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error in filter_files: {e}")
            return []
    
    def get_filter_suggestions(self, files_info: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Get suggestions for available filter values.
        
        Args:
            files_info: Dictionary containing file information
            
        Returns:
            Dictionary with suggestions for each filter type
        """
        suggestions = {
            'formats': [],
            'sources': [],
            'symbols': [],
            'indicators': []
        }
        
        for filename, file_info in files_info.items():
            # Format suggestions
            file_format = file_info.get('format', '').replace('.', '').lower()
            if file_format and file_format not in suggestions['formats']:
                suggestions['formats'].append(file_format)
            
            # Source suggestions
            file_source = file_info.get('source', '').lower()
            if file_source and file_source not in suggestions['sources']:
                suggestions['sources'].append(file_source)
            
            # Symbol suggestions
            symbol = self._extract_symbol_from_filename(filename)
            if symbol and symbol not in suggestions['symbols']:
                suggestions['symbols'].append(symbol)
            
            # Indicator suggestions
            indicator = file_info.get('indicator', '').lower()
            if indicator and indicator not in suggestions['indicators']:
                suggestions['indicators'].append(indicator)
        
        # Sort all suggestions
        for key in suggestions:
            suggestions[key].sort()
        
        return suggestions
    
    def interactive_filter_selection(self, files_info: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        """
        Interactive filter selection interface.
        
        Args:
            files_info: Dictionary containing file information
            
        Returns:
            Tuple of (format_filter, source_filter, symbol_filter, indicator_filter)
        """
        print(f"\n{Fore.YELLOW}🔍 Interactive Data Filter")
        print(f"{Fore.CYAN}{'─'*50}")
        
        # Show quick filter option
        print(f"\n{Fore.GREEN}💡 Quick Filter Options:")
        print(f"  {Fore.WHITE}1. Enter filter string (e.g., 'parquet binance BTCUSDT wave')")
        print(f"  {Fore.WHITE}2. Use interactive step-by-step filtering")
        print(f"  {Fore.WHITE}3. Show all available data first")
        
        choice = input(f"\n{Fore.CYAN}Choose option (1-3) [default: 2]: {Style.RESET_ALL}").strip()
        
        if choice == '1':
            return self._quick_filter_interface(files_info)
        elif choice == '3':
            self._show_all_available_data(files_info)
            return self._step_by_step_filtering(files_info)
        else:
            return self._step_by_step_filtering(files_info)
    
    def _quick_filter_interface(self, files_info: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        """Quick filter interface using a single string input."""
        print(f"\n{Fore.GREEN}🚀 Quick Filter Interface")
        print(f"{Fore.CYAN}{'─'*40}")
        print(f"{Fore.YELLOW}Enter filter criteria separated by spaces:")
        print(f"{Fore.WHITE}Examples:")
        print(f"  • parquet binance BTCUSDT wave")
        print(f"  • json csvexport EURUSD rsi")
        print(f"  • csv polygon AAPL macd")
        
        default_filter = "parquet binance BTCUSDT wave"
        filter_string = input(f"\n{Fore.GREEN}Filter [{default_filter}]: {Style.RESET_ALL}").strip()
        
        if not filter_string:
            print(f"{Fore.YELLOW}Using default filter: {default_filter}")
            filter_string = default_filter
        
        # Parse the filter string
        parts = filter_string.lower().split()
        
        format_filter = None
        source_filter = None
        symbol_filter = None
        indicator_filter = None
        
        for part in parts:
            if part in ['parquet', 'json', 'csv']:
                format_filter = part
            elif part in ['binance', 'csvexport', 'polygon', 'yfinance']:
                source_filter = part
            elif part in ['wave', 'rsi', 'macd', 'pressurevector', 'supportresistants']:
                indicator_filter = part
            elif len(part) >= 3 and part.isalpha():  # Potential symbol
                symbol_filter = part.upper()
        
        return format_filter, source_filter, symbol_filter, indicator_filter
    
    def _show_all_available_data(self, files_info: Dict[str, Any]) -> None:
        """Show all available data for reference."""
        suggestions = self.get_filter_suggestions(files_info)
        
        print(f"\n{Fore.GREEN}📊 All Available Data:")
        print(f"{Fore.CYAN}{'─'*50}")
        
        if suggestions['formats']:
            print(f"\n{Fore.YELLOW}📁 Formats: {', '.join(suggestions['formats'])}")
        if suggestions['sources']:
            print(f"{Fore.YELLOW}🏢 Sources: {', '.join(suggestions['sources'])}")
        if suggestions['symbols']:
            print(f"{Fore.YELLOW}💱 Symbols: {', '.join(suggestions['symbols'])}")
        if suggestions['indicators']:
            print(f"{Fore.YELLOW}📈 Indicators: {', '.join(suggestions['indicators'])}")
        
        # Show file count
        print(f"\n{Fore.WHITE}Total Files: {len(files_info)}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue with filtering...")
    
    def _step_by_step_filtering(self, files_info: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        """Step-by-step filtering interface."""
        print(f"\n{Fore.GREEN}🔧 Step-by-Step Filtering")
        print(f"{Fore.CYAN}{'─'*40}")
        
        # Get suggestions
        suggestions = self.get_filter_suggestions(files_info)
        
        # Format filter
        format_filter = self._get_format_filter(suggestions['formats'])
        
        # Source filter
        source_filter = self._get_source_filter(suggestions['sources'])
        
        # Symbol filter
        symbol_filter = self._get_symbol_filter(suggestions['symbols'])
        
        # Indicator filter
        indicator_filter = self._get_indicator_filter(suggestions['indicators'])
        
        return format_filter, source_filter, symbol_filter, indicator_filter
    
    def _get_format_filter(self, available_formats: List[str]) -> Optional[str]:
        """Get format filter from user input with autocomplete."""
        if not available_formats:
            return None
        
        print(f"\n{Fore.GREEN}📁 Available Formats:")
        for i, fmt in enumerate(available_formats, 1):
            print(f"  {Fore.WHITE}{i}. {fmt.upper()}")
        
        print(f"\n{Fore.CYAN}Enter format filter (e.g., 'parquet', 'json', 'csv') or press Enter to skip:")
        
        while True:
            user_input = input(f"{Fore.GREEN}Format: {Style.RESET_ALL}").strip().lower()
            
            if not user_input:
                return None
            
            # Direct match
            if user_input in available_formats:
                return user_input
            
            # Try to match by number
            try:
                choice_idx = int(user_input) - 1
                if 0 <= choice_idx < len(available_formats):
                    return available_formats[choice_idx]
            except ValueError:
                pass
            
            # Try partial match
            matches = [fmt for fmt in available_formats if fmt.startswith(user_input)]
            if len(matches) == 1:
                print(f"{Fore.GREEN}✅ Auto-completed: {matches[0]}")
                return matches[0]
            elif len(matches) > 1:
                print(f"{Fore.YELLOW}⚠️  Multiple matches: {', '.join(matches)}")
                continue
            
            print(f"{Fore.RED}❌ Format '{user_input}' not found. Available: {', '.join(available_formats)}")
            retry = input(f"{Fore.CYAN}Try again? (y/N): {Style.RESET_ALL}").strip().lower()
            if retry not in ['y', 'yes']:
                return None
    
    def _get_source_filter(self, available_sources: List[str]) -> Optional[str]:
        """Get source filter from user input with autocomplete."""
        if not available_sources:
            return None
        
        print(f"\n{Fore.GREEN}🏢 Available Sources:")
        for i, source in enumerate(available_sources, 1):
            print(f"  {Fore.WHITE}{i}. {source.upper()}")
        
        print(f"\n{Fore.CYAN}Enter source filter (e.g., 'binance', 'csvexport') or press Enter to skip:")
        
        while True:
            user_input = input(f"{Fore.GREEN}Source: {Style.RESET_ALL}").strip().lower()
            
            if not user_input:
                return None
            
            # Direct match
            if user_input in available_sources:
                return user_input
            
            # Try to match by number
            try:
                choice_idx = int(user_input) - 1
                if 0 <= choice_idx < len(available_sources):
                    return available_sources[choice_idx]
            except ValueError:
                pass
            
            # Try partial match
            matches = [source for source in available_sources if source.startswith(user_input)]
            if len(matches) == 1:
                print(f"{Fore.GREEN}✅ Auto-completed: {matches[0]}")
                return matches[0]
            elif len(matches) > 1:
                print(f"{Fore.YELLOW}⚠️  Multiple matches: {', '.join(matches)}")
                continue
            
            print(f"{Fore.RED}❌ Source '{user_input}' not found. Available: {', '.join(available_sources)}")
            retry = input(f"{Fore.CYAN}Try again? (y/N): {Style.RESET_ALL}").strip().lower()
            if retry not in ['y', 'yes']:
                return None
    
    def _get_symbol_filter(self, available_symbols: List[str]) -> Optional[str]:
        """Get symbol filter from user input with autocomplete."""
        if not available_symbols:
            return None
        
        print(f"\n{Fore.GREEN}💱 Available Symbols:")
        for i, symbol in enumerate(available_symbols, 1):
            print(f"  {Fore.WHITE}{i}. {symbol}")
        
        print(f"\n{Fore.CYAN}Enter symbol filter (e.g., 'BTCUSDT', 'EURUSD') or press Enter to skip:")
        
        while True:
            user_input = input(f"{Fore.GREEN}Symbol: {Style.RESET_ALL}").strip().upper()
            
            if not user_input:
                return None
            
            # Direct match
            if user_input in available_symbols:
                return user_input
            
            # Try to match by number
            try:
                choice_idx = int(user_input) - 1
                if 0 <= choice_idx < len(available_symbols):
                    return available_symbols[choice_idx]
            except ValueError:
                pass
            
            # Try partial match
            matches = [symbol for symbol in available_symbols if symbol.startswith(user_input)]
            if len(matches) == 1:
                print(f"{Fore.GREEN}✅ Auto-completed: {matches[0]}")
                return matches[0]
            elif len(matches) > 1:
                print(f"{Fore.YELLOW}⚠️  Multiple matches: {', '.join(matches)}")
                continue
            
            print(f"{Fore.RED}❌ Symbol '{user_input}' not found. Available: {', '.join(available_symbols)}")
            retry = input(f"{Fore.CYAN}Try again? (y/N): {Style.RESET_ALL}").strip().lower()
            if retry not in ['y', 'yes']:
                return None
    
    def _get_indicator_filter(self, available_indicators: List[str]) -> Optional[str]:
        """Get indicator filter from user input with autocomplete."""
        if not available_indicators:
            return None
        
        print(f"\n{Fore.GREEN}📊 Available Indicators:")
        for i, indicator in enumerate(available_indicators, 1):
            print(f"  {Fore.WHITE}{i}. {indicator.upper()}")
        
        print(f"\n{Fore.CYAN}Enter indicator filter (e.g., 'wave', 'rsi_mom', 'macd') or press Enter to skip:")
        
        while True:
            user_input = input(f"{Fore.GREEN}Indicator: {Style.RESET_ALL}").strip().lower()
            
            if not user_input:
                return None
            
            # Direct match
            if user_input in available_indicators:
                return user_input
            
            # Try to match by number
            try:
                choice_idx = int(user_input) - 1
                if 0 <= choice_idx < len(available_indicators):
                    return available_indicators[choice_idx]
            except ValueError:
                pass
            
            # Try partial match
            matches = [indicator for indicator in available_indicators if indicator.startswith(user_input)]
            if len(matches) == 1:
                print(f"{Fore.GREEN}✅ Auto-completed: {matches[0]}")
                return matches[0]
            elif len(matches) > 1:
                print(f"{Fore.YELLOW}⚠️  Multiple matches: {', '.join(matches)}")
                continue
            
            print(f"{Fore.RED}❌ Indicator '{user_input}' not found. Available: {', '.join(available_indicators)}")
            retry = input(f"{Fore.CYAN}Try again? (y/N): {Style.RESET_ALL}").strip().lower()
            if retry not in ['y', 'yes']:
                return None
    
    def display_filtered_results(self, filtered_files: List[Dict[str, Any]]) -> None:
        """
        Display filtered results in a user-friendly format.
        
        Args:
            filtered_files: List of filtered file information
        """
        if not filtered_files:
            print(f"\n{Fore.RED}❌ No files match the selected filters")
            return
        
        print(f"\n{Fore.GREEN}📊 Filtered Results ({len(filtered_files)} files):")
        print(f"{Fore.CYAN}{'─'*80}")
        
        # Group by source and indicator
        grouped = {}
        for file_data in filtered_files:
            source = file_data['source'].upper()
            indicator = file_data['indicator'].upper()
            key = f"{source}_{indicator}"
            
            if key not in grouped:
                grouped[key] = {
                    'source': source,
                    'indicator': indicator,
                    'files': [],
                    'total_size': 0,
                    'total_rows': 0
                }
            
            file_info = file_data['file_info']
            grouped[key]['files'].append(file_data)
            grouped[key]['total_size'] += file_info.get('size_mb', 0)
            grouped[key]['total_rows'] += file_info.get('rows', 0)
        
        # Display grouped results
        for key, group_data in sorted(grouped.items()):
            source = group_data['source']
            indicator = group_data['indicator']
            file_count = len(group_data['files'])
            total_size = group_data['total_size']
            total_rows = group_data['total_rows']
            
            print(f"\n{Fore.YELLOW}📈 {indicator} ({source}):")
            print(f"  {Fore.WHITE}Files: {file_count}, Size: {total_size:.1f}MB, Rows: {total_rows:,}")
            
            # Show individual files
            for file_data in group_data['files']:
                filename = file_data['filename']
                file_info = file_data['file_info']
                format_type = file_data['format'].upper()
                symbol = file_data['symbol'] or 'Unknown'
                size_mb = file_info.get('size_mb', 0)
                rows = file_info.get('rows', 0)
                
                # Extract timeframe from filename
                timeframe = self._extract_timeframe_from_filename(filename)
                
                print(f"    {Fore.CYAN}• {timeframe} - {symbol} - {format_type} - {size_mb:.1f}MB - {rows:,} rows")
    
    def get_loading_summary(self, filtered_files: List[Dict[str, Any]]) -> str:
        """
        Get a summary string for loading confirmation.
        
        Args:
            filtered_files: List of filtered file information
            
        Returns:
            Summary string for loading confirmation
        """
        if not filtered_files:
            return "No files selected"
        
        # Get unique values
        sources = set()
        formats = set()
        symbols = set()
        indicators = set()
        
        for file_data in filtered_files:
            sources.add(file_data['source'])
            formats.add(file_data['format'])
            if file_data['symbol']:
                symbols.add(file_data['symbol'])
            indicators.add(file_data['indicator'])
        
        # Create summary
        summary_parts = []
        if formats:
            summary_parts.append(f"format: {', '.join(sorted(formats))}")
        if sources:
            summary_parts.append(f"source: {', '.join(sorted(sources))}")
        if symbols:
            summary_parts.append(f"symbol: {', '.join(sorted(symbols))}")
        if indicators:
            summary_parts.append(f"indicator: {', '.join(sorted(indicators))}")
        
        return f"Loading to memory: {' '.join(summary_parts)}"
    
    def search_files_by_keywords(self, files_info: Dict[str, Any], keywords: List[str]) -> List[Dict[str, Any]]:
        """
        Search files by keywords in filename or metadata.
        
        Args:
            files_info: Dictionary containing file information
            keywords: List of keywords to search for
            
        Returns:
            List of matching file information
        """
        matching_files = []
        keywords_lower = [kw.lower() for kw in keywords]
        
        for filename, file_info in files_info.items():
            # Check filename
            filename_lower = filename.lower()
            if any(kw in filename_lower for kw in keywords_lower):
                matching_files.append({
                    'filename': filename,
                    'file_info': file_info,
                    'symbol': self._extract_symbol_from_filename(filename),
                    'source': file_info.get('source', 'unknown'),
                    'format': file_info.get('format', '').replace('.', '').lower(),
                    'indicator': file_info.get('indicator', 'unknown')
                })
                continue
            
            # Check metadata
            for key, value in file_info.items():
                if isinstance(value, str) and any(kw in value.lower() for kw in keywords_lower):
                    matching_files.append({
                        'filename': filename,
                        'file_info': file_info,
                        'symbol': self._extract_symbol_from_filename(filename),
                        'source': file_info.get('source', 'unknown'),
                        'format': file_info.get('format', '').replace('.', '').lower(),
                        'indicator': file_info.get('indicator', 'unknown')
                    })
                    break
        
        return matching_files
    
    def filter_by_timeframe(self, files_info: Dict[str, Any], timeframes: List[str]) -> List[Dict[str, Any]]:
        """
        Filter files by timeframe.
        
        Args:
            files_info: Dictionary containing file information
            timeframes: List of timeframes to filter by (e.g., ['M5', 'D1', 'H1'])
            
        Returns:
            List of filtered file information
        """
        filtered_files = []
        timeframes_upper = [tf.upper() for tf in timeframes]
        
        for filename, file_info in files_info.items():
            # Extract timeframe from filename
            file_timeframe = self._extract_timeframe_from_filename(filename)
            if file_timeframe.upper() in timeframes_upper:
                filtered_files.append({
                    'filename': filename,
                    'file_info': file_info,
                    'symbol': self._extract_symbol_from_filename(filename),
                    'source': file_info.get('source', 'unknown'),
                    'format': file_info.get('format', '').replace('.', '').lower(),
                    'indicator': file_info.get('indicator', 'unknown'),
                    'timeframe': file_timeframe
                })
        
        return filtered_files
    
    def _extract_timeframe_from_filename(self, filename: str) -> str:
        """
        Extract timeframe from filename.
        
        Args:
            filename: Name of the file
            
        Returns:
            Extracted timeframe or 'Unknown'
        """
        try:
            # Common timeframe patterns
            timeframes = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1', 'MN1']
            
            for tf in timeframes:
                if f'_{tf}_' in filename or f'_{tf}.' in filename or filename.endswith(f'_{tf}'):
                    return tf
            
            # Special case for CSVExport files
            if 'CSVExport' in filename:
                if 'PERIOD_' in filename:
                    period_part = filename.split('PERIOD_')[-1].split('.')[0]
                    if period_part in timeframes:
                        return period_part
            
            return 'Unknown'
            
        except Exception:
            return 'Unknown'
    
    def get_file_statistics(self, filtered_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics for filtered files.
        
        Args:
            filtered_files: List of filtered file information
            
        Returns:
            Dictionary containing statistics
        """
        if not filtered_files:
            return {
                'total_files': 0,
                'total_size_mb': 0,
                'total_rows': 0,
                'unique_sources': 0,
                'unique_formats': 0,
                'unique_symbols': 0,
                'unique_indicators': 0
            }
        
        total_size = 0
        total_rows = 0
        sources = set()
        formats = set()
        symbols = set()
        indicators = set()
        
        for file_data in filtered_files:
            file_info = file_data['file_info']
            total_size += file_info.get('size_mb', 0)
            total_rows += file_info.get('rows', 0)
            sources.add(file_data['source'])
            formats.add(file_data['format'])
            if file_data['symbol']:
                symbols.add(file_data['symbol'])
            indicators.add(file_data['indicator'])
        
        return {
            'total_files': len(filtered_files),
            'total_size_mb': total_size,
            'total_rows': total_rows,
            'unique_sources': len(sources),
            'unique_formats': len(formats),
            'unique_symbols': len(symbols),
            'unique_indicators': len(indicators),
            'sources': sorted(list(sources)),
            'formats': sorted(list(formats)),
            'symbols': sorted(list(symbols)),
            'indicators': sorted(list(indicators))
        }
    
    def display_statistics(self, filtered_files: List[Dict[str, Any]]) -> None:
        """
        Display statistics for filtered files.
        
        Args:
            filtered_files: List of filtered file information
        """
        stats = self.get_file_statistics(filtered_files)
        
        print(f"\n{Fore.GREEN}📊 Filter Statistics:")
        print(f"{Fore.CYAN}{'─'*50}")
        print(f"{Fore.WHITE}Total Files: {stats['total_files']}")
        print(f"{Fore.WHITE}Total Size: {stats['total_size_mb']:.1f} MB")
        print(f"{Fore.WHITE}Total Rows: {stats['total_rows']:,}")
        print(f"{Fore.WHITE}Unique Sources: {stats['unique_sources']}")
        print(f"{Fore.WHITE}Unique Formats: {stats['unique_formats']}")
        print(f"{Fore.WHITE}Unique Symbols: {stats['unique_symbols']}")
        print(f"{Fore.WHITE}Unique Indicators: {stats['unique_indicators']}")
        
        if stats['sources']:
            print(f"\n{Fore.YELLOW}Sources: {', '.join(stats['sources'])}")
        if stats['formats']:
            print(f"{Fore.YELLOW}Formats: {', '.join(stats['formats'])}")
        if stats['symbols']:
            print(f"{Fore.YELLOW}Symbols: {', '.join(stats['symbols'])}")
        if stats['indicators']:
            print(f"{Fore.YELLOW}Indicators: {', '.join(stats['indicators'])}")
    
    def quick_filter(self, files_info: Dict[str, Any], filter_string: str) -> List[Dict[str, Any]]:
        """
        Quick filter using a single string with multiple criteria.
        
        Args:
            files_info: Dictionary containing file information
            filter_string: String like "parquet binance BTCUSDT wave"
            
        Returns:
            List of filtered file information
        """
        try:
            if not filter_string or not filter_string.strip():
                print(f"{Fore.YELLOW}⚠️  Empty filter string provided")
                return []
            
            # Parse filter string
            parts = filter_string.lower().strip().split()
            
            if not parts:
                print(f"{Fore.YELLOW}⚠️  No valid filter criteria found")
                return []
            
            format_filter = None
            source_filter = None
            symbol_filter = None
            indicator_filter = None
            
            # Track what was found for validation
            found_criteria = []
            
            for part in parts:
                if part in ['parquet', 'json', 'csv']:
                    format_filter = part
                    found_criteria.append(f"format: {part}")
                elif part in ['binance', 'csvexport', 'polygon', 'yfinance']:
                    source_filter = part
                    found_criteria.append(f"source: {part}")
                elif part in ['wave', 'rsi', 'macd', 'pressurevector', 'supportresistants']:
                    indicator_filter = part
                    found_criteria.append(f"indicator: {part}")
                elif len(part) >= 3 and part.isalpha():  # Potential symbol
                    symbol_filter = part.upper()
                    found_criteria.append(f"symbol: {part.upper()}")
                else:
                    print(f"{Fore.YELLOW}⚠️  Unknown filter criteria: {part}")
            
            if found_criteria:
                print(f"{Fore.GREEN}✅ Applied filters: {', '.join(found_criteria)}")
            else:
                print(f"{Fore.RED}❌ No valid filter criteria found in: {filter_string}")
                return []
            
            return self.filter_files(
                files_info,
                format_filter=format_filter,
                source_filter=source_filter,
                symbol_filter=symbol_filter,
                indicator_filter=indicator_filter
            )
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error in quick_filter: {e}")
            return []
